import json
import re
import sys

import koji
import requests
import subprocess
import tempfile
import urllib.parse
import yaml

# These container images (identified by their NVR) are known to contain only RPM packages and no
# other content type.
RPM_CONTAINER_IMAGES = {
    "ubi9-micro-container-9.4-6.1716471860": "https://git.example.com/containers/ubi9-micro#433dec61d526247ac9533c1d9b97e98a1127c782",
    "kernel-module-management-operator-container-1.1.2-25": "https://git.example.com/containers/kernel-module-management-operator#799f12ccdec1ead269f54c4e3e51c28d7c794ae4",  # Contains openssl-3.0.7-18.el9_2
}

catalog_url = "https://catalog.redhat.com/api/containers/v1/"
nvr_api = catalog_url + "images/nvr/"
rpm_manifest_api = catalog_url + "images/id/{catalog_image_id}/rpm-manifest"

profile = koji.get_profile_module("brew")
koji_session = koji.ClientSession(profile.config.server)


def sanitize_spdxid(value):
    """ "Emit a valid SPDXRef-"[idstring]"

    where [idstring] is a unique string containing letters, numbers, ., and/or -.
    """
    value = value.replace("_", "-")  # Replace underscores with dashes to retain readability
    # Remove everything else (yes, there is a minor chance for conflicting IDs, but this is an
    # example script with minimal examples; do not use this in production).
    return re.sub(r"[^a-zA-Z0-9.-]", "", value)


def get_image_data(image_nvr):
    response = requests.get(nvr_api + image_nvr)
    response.raise_for_status()
    # This is a paged response, but we're assuming there are not 100+ images for a single
    # container image NVR.
    return sorted(response.json()["data"], key=lambda image: image["_id"])


def get_rpms(image_id):
    response = requests.get(rpm_manifest_api.format(catalog_image_id=image_id))
    response.raise_for_status()
    return sorted(response.json()["rpms"], key=lambda rpm: rpm["nvra"])


def create_sbom(
    image_id, root_package, packages, rel_type, other_pkgs=None, other_rels=None, source_pkgs=None
):
    relationships = list(other_rels or [])
    relationships.insert(
        0,
        {
            "spdxElementId": "SPDXRef-DOCUMENT",
            "relationshipType": "DESCRIBES",
            "relatedSpdxElement": root_package["SPDXID"],
        },
    )

    for pkg in packages:
        lhs = root_package["SPDXID"]
        rhs = pkg["SPDXID"]
        if rel_type.endswith("_OF"):
            # .._OF relationships go the other way
            lhs, rhs = rhs, lhs
        relationships.append(
            {
                "spdxElementId": lhs,
                "relationshipType": rel_type,
                "relatedSpdxElement": rhs,
            }
        )

    packages = packages + list(source_pkgs or [])

    # This is a convention in the script only that the first source_pkg is the
    # midststream repository
    if source_pkgs:
        first_source_package = source_pkgs.pop(0)
        relationships.append(
            {
                "spdxElementId": root_package["SPDXID"],
                "relationshipType": "GENERATED_FROM",
                "relatedSpdxElement": first_source_package["SPDXID"],
            }
        )
        if source_pkgs:
            for source in source_pkgs:
                relationships.append(
                    {
                        "spdxElementId": first_source_package["SPDXID"],
                        "relationshipType": "DEPENDS_ON",
                        "relatedSpdxElement": source["SPDXID"],
                    }
                )

    spdx = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "creationInfo": {
            "created": "2006-08-14T02:34:56Z",
            "creators": ["Tool: example SPDX document only", "Organization: Red Hat"],
        },
        "name": image_id,
        "documentNamespace": f"https://www.redhat.com/{image_id}.spdx.json",
        "packages": [root_package] + packages + (other_pkgs or []),
        "relationships": relationships,
    }

    with open(f"{image_id}.spdx.json", "w") as fp:
        # Add an extra newline at the end since a lot of editors add one when you save a file,
        # and these files get opened and read in editors a lot.
        fp.write(json.dumps(spdx, indent=2) + "\n")


def get_package_name_from_uri(uri: str) -> str:
    parse_image_repo = urllib.parse.urlparse(uri)
    return parse_image_repo.path.split("/")[1]


def generate_sboms_for_image(image_nvr):
    # Split to e.g. "ubi9-micro-container" and "9.4-6.1716471860"
    image_nvr_name, *image_nvr_version = image_nvr.rsplit("-", maxsplit=2)
    image_nvr_version = "-".join(image_nvr_version)

    image_index_pkg = None
    midstream_repo = None
    source_pkgs = []
    per_arch_images = []

    for image in get_image_data(image_nvr):
        packages = []
        other_pkgs = []
        other_rels = []

        catalog_image_id = image["_id"]
        image_digest = image["image_id"]
        content_sets = image["content_sets"]

        # A container image may be available through more than one repo; collect all repos,
        # registries they are available from, and the most specific tag for each repo image.
        repos = set()
        image_index_digest = ""
        for repo in image["repositories"]:
            repo_url = f"{repo['registry']}/{repo['repository']}"
            tags = list(
                sorted(
                    [t for t in repo["tags"] if t["name"] != "latest"],
                    # Sort by the length of the tag, ignoring "latest"; this is a very dumb
                    # heuristic to find the most specific tag for a particular image. From tags
                    # such as "9.4", "latest", and "9.4-6.1716471860", it will select the last one.
                    key=lambda x: len(x["name"]),
                    reverse=True,
                )
            )
            if not tags:
                print(f"ERROR: no usable tag found for image ID: {catalog_image_id}")
                sys.exit(1)
            repo_name = repo["repository"].split("/")[-1]
            repos.add((repo_name, repo_url, tags[0]["name"]))
            image_index_digest = repo["manifest_list_digest"].lstrip("sha256:")

        if not repos or not image_index_digest:
            print("ERROR: No repos or image index digest found for image ID: {catalog_image_id}")
            sys.exit(1)

        # Get license information from labels if it is set
        image_license = "NOASSERTION"
        spdx_license_ids = {
            "Apache License 2.0": "Apache-2.0",
        }
        for label in image["parsed_data"]["labels"]:
            if label["name"].lower() == "license":
                image_license = label["value"]
                image_license = spdx_license_ids.get(image_license, image_license)

        # Create an index image object, but since all arch-specific images are descendents of one
        # and the same index image, we only have to create it once. Its SBOM is created at the
        # end after we collect information about all arch-specific images.
        if not image_index_pkg:
            image_index_pkg = {
                "SPDXID": "SPDXRef-image-index",
                "name": image_nvr_name,
                "versionInfo": image_nvr_version,
                "supplier": "Organization: Red Hat",
                "downloadLocation": "NOASSERTION",
                "licenseDeclared": image_license,
                "externalRefs": [],
                "checksums": [
                    {
                        "algorithm": "SHA256",
                        "checksumValue": image_index_digest,
                    }
                ],
            }
            for name, repo_url, tag in sorted(repos):
                purl = (
                    f"pkg:oci/{name}@sha256:{image_index_digest}?"
                    f"repository_url={repo_url}&tag={tag}"
                )
                ref = {
                    "referenceCategory": "PACKAGE-MANAGER",
                    "referenceType": "purl",
                    "referenceLocator": purl,
                }
                image_index_pkg["externalRefs"].append(ref)

        arch = image["architecture"]
        spdx_image_id = sanitize_spdxid(f"SPDXRef-{image_nvr_name}-{arch}")
        image_pkg = {
            "SPDXID": spdx_image_id,
            "name": f"{image_nvr_name}_{arch}",
            "versionInfo": image_nvr_version,
            "supplier": "Organization: Red Hat",
            "downloadLocation": "NOASSERTION",
            "licenseDeclared": image_license,
            "externalRefs": [],
            "checksums": [
                {
                    "algorithm": "SHA256",
                    "checksumValue": image_digest.lstrip("sha256:"),
                }
            ],
        }
        for name, repo_url, tag in sorted(repos):
            purl = (
                f"pkg:oci/{name}@sha256:{image_digest}?"
                f"arch={arch}&repository_url={repo_url}&tag={tag}"
            )
            ref = {
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": purl,
            }
            image_pkg["externalRefs"].append(ref)
        per_arch_images.append(image_pkg)

        image_data = koji_session.getBuild(image_nvr)

        # Add in source repositories. but since all arch-specific images are descendents of one
        # and the same source repository, we only have to create it once. It's added only to the image
        # index SBOM at the end.
        if not source_pkgs:
            # There is where the actual image source can be read from. Because this is private data, I'm hardcoding some values here
            image_source = image_data["source"]
            image_repo, repo_commit = split_source_repo_parts(image_source)

            mock_source = RPM_CONTAINER_IMAGES[image_nvr]
            mock_repo, mock_commit = split_source_repo_parts(mock_source)
            package_name = get_package_name_from_uri(mock_repo)
            source_pkgs.append(
                {
                    "SPDXID": f"{image_nvr}-Source",
                    "name": package_name,
                    "versionInfo": f"{mock_commit}",
                    "supplier": "Organization: Red Hat",
                    "downloadLocation": mock_source,
                    "licenseDeclared": "NOASSERTION",
                    "externalRefs": [
                        {
                            "referenceCategory": "PACKAGE-MANAGER",
                            "referenceType": "purl",
                            "referenceLocator": f"pkg:generic/{package_name}@{repo_commit}?download_url={mock_source}",
                        },
                    ],
                }
            )

            remote_repo = ""
            remote_ref = ""

            # Clone the repository to a temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                subprocess.run(["git", "clone", image_repo, temp_dir])

                # Change to the specific commit
                subprocess.run(["git", "checkout", repo_commit], cwd=temp_dir)

                # Remote Sources could be a list, for example
                # https://pkgs.devel.redhat.com/cgit/containers/quay/tree/container.yaml?h=quay-3.13-rhel-8
                # Read the YAML file
                with open(f"{temp_dir}/container.yaml", "r") as file:
                    container_data = yaml.safe_load(file)
                    remote_source = container_data.get("remote_source", {})
                    remote_repo = remote_source.get("repo", "")
                    remote_ref = remote_source.get("ref", "")

            if remote_repo:
                package_name = get_package_name_from_uri(remote_repo)
                remote_source = f"{remote_repo}#{remote_ref}"
                source_pkgs.append(
                    {
                        "SPDXID": f"{image_nvr}-Source-origin",
                        "name": name,
                        "versionInfo": remote_ref,
                        "supplier": "Organization: Red Hat",
                        "downloadLocation": remote_source,
                        "licenseDeclared": "NOASSERTION",
                        "externalRefs": [
                            {
                                "referenceCategory": "PACKAGE-MANAGER",
                                "referenceType": "purl",
                                "referenceLocator": f"pkg:generic/{package_name}@{remote_ref}?download_url={image_source}",
                            },
                        ],
                    }
                )

        # Add in parent images
        for key in ("extra", "typeinfo", "image"):
            image_data = image_data.get(key, {})

        parent_image_builds = image_data.get("parent_image_builds", {})
        parent_images = image_data.get("parent_images", [])
        direct_parent_index = len(parent_images) - 1
        for index, parent_image in enumerate(parent_images):
            try:
                parent_image_build_id = parent_image_builds[parent_image]["id"]
            except KeyError:
                # Skip scratch builds
                continue

            parent_archives = koji_session.listArchives(parent_image_build_id)
            parent_digests = [
                list(a["extra"]["docker"]["digests"].values())[0]
                for a in parent_archives
                if a["btype"] == "image" and a["extra"]["docker"]["config"]["architecture"] == arch
            ]
            parent_digest = parent_digests[0] if parent_digests else ""
            if parent_digests:
                version = f"@{parent_digest}"
            else:
                version = ""

            registry, rest = parent_image.split("/", maxsplit=1)
            use_registry = registry in ("registry.redhat.io", "registry.access.redhat.com")
            name, tag = rest.rsplit(":", maxsplit=1)
            if "/" in name:
                namespace, name = name.rsplit("/", maxsplit=1)
                registry += "/" + namespace

            registry_q = f"&repository_url={registry}" if use_registry else ""
            parent_spdx_id = sanitize_spdxid(f"SPDXRef-parent-image-{index}-{arch}")
            purl = f"pkg:oci/{name}{version}?tag={tag}{registry_q}"

            parent_pkg = {
                "SPDXID": parent_spdx_id,
                "name": f"{name}_{arch}",
                "versionInfo": f"{tag}",
                "supplier": "Organization: Red Hat",
                "downloadLocation": "NOASSERTION",
                "licenseDeclared": "NOASSERTION",
                "externalRefs": [
                    {
                        "referenceCategory": "PACKAGE-MANAGER",
                        "referenceType": "purl",
                        "referenceLocator": purl,
                    },
                ],
            }
            if parent_digest:
                parent_pkg["checksums"] = [
                    {
                        "algorithm": "SHA256",
                        "checksumValue": parent_digest.lstrip("sha256:"),
                    }
                ]
            other_pkgs.append(parent_pkg)

            if index == direct_parent_index:
                other_rels.append(
                    {
                        "spdxElementId": spdx_image_id,
                        "relationshipType": "DESCENDANT_OF",
                        "relatedSpdxElement": parent_spdx_id,
                    }
                )
            else:
                other_rels.append(
                    {
                        "spdxElementId": parent_spdx_id,
                        "relationshipType": "BUILD_TOOL_OF",
                        "relatedSpdxElement": spdx_image_id,
                    }
                )

        for rpm in get_rpms(catalog_image_id):
            rpm_purl = (
                f"pkg:rpm/redhat/{rpm['name']}@{rpm['version']}-{rpm['release']}?"
                # We don't have a way to find out which content set (RPM repo) an RPM came from,
                # so we arbitrarily choose one here (assuming we have this mapping via RPM
                # lockfiles or other means eventually).
                f"arch={rpm['architecture']}&repository_id={content_sets[0]}"
            )
            spdx_rpm_id = sanitize_spdxid(f"SPDXRef-{rpm['architecture']}-{rpm['name']}")
            rpm_pkg = {
                "SPDXID": spdx_rpm_id,
                "name": rpm["name"],
                "versionInfo": rpm["version"],
                "supplier": "Organization: Red Hat",
                "downloadLocation": "NOASSERTION",  # Unset on purpose; refer to RPM SBOM
                "packageFileName": rpm["nvra"] + ".rpm",
                "licenseDeclared": "NOASSERTION",  # Unset on purpose; refer to RPM SBOM
                "externalRefs": [
                    {
                        "referenceCategory": "PACKAGE-MANAGER",
                        "referenceType": "purl",
                        "referenceLocator": rpm_purl,
                    },
                ],
                # We don't have checksums available from Pyxis, but they should be available
                # during the build process. For example purposes, we'll use a mock value.
                "checksums": [
                    {
                        "algorithm": "SHA256",
                        "checksumValue": "abcd1234" * 8,
                    }
                ],
            }
            packages.append(rpm_pkg)

        create_sbom(
            image_id=f"{image_nvr}_" f"{arch}",
            root_package=image_pkg,
            packages=packages,
            rel_type="CONTAINS",
            other_pkgs=other_pkgs,
            other_rels=other_rels,
        )

    create_sbom(
        image_id=image_nvr,
        root_package=image_index_pkg,
        packages=per_arch_images,
        rel_type="VARIANT_OF",
        other_pkgs=None,
        other_rels=None,
        source_pkgs=source_pkgs,
    )


def split_source_repo_parts(image_source):
    image_source_parts = image_source.rsplit("#", 2)
    if len(image_source_parts) == 2:
        image_repo = image_source_parts[0]
        repo_commit = image_source_parts[1]
    return image_repo, repo_commit


for rpm_image in RPM_CONTAINER_IMAGES.keys():
    generate_sboms_for_image(rpm_image)
