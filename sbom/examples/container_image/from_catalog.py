import json
import itertools
import sys

import requests

# These container images (identified by their NVR) are known to contain only RPM packages and no
# other content type.
RPM_CONTAINER_IMAGES = [
    "ubi9-micro-container-9.4-6.1716471860",
    "kernel-module-management-operator-container-1.1.2-25",  # Contains openssl-3.0.7-18.el9_2
]

catalog_url = "https://catalog.redhat.com/api/containers/v1/"
nvr_api = catalog_url + "images/nvr/"
rpm_manifest_api = catalog_url + "images/id/{catalog_image_id}/rpm-manifest"

rpm_sbom_url = "https://access.redhat.com/security/data/sbom/v1/rpm/"


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


def create_sbom(doc_id, image_id, root_package, packages, rel_type):
    relationships = [
        {
            "spdxElementId": f"SPDXRef-DOCUMENT-{doc_id}",
            "relationshipType": "DESCRIBES",
            "relatedSpdxElement": root_package["SPDXID"],
        }
    ]
    for pkg in packages:
        relationships.append(
            {
                "spdxElementId": root_package["SPDXID"],
                "relationshipType": rel_type,
                "relatedSpdxElement": pkg["SPDXID"],
            }
        )

    spdx = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": f"SPDXRef-DOCUMENT-{doc_id}",
        "creationInfo": {
            "created": "2006-08-14T02:34:56-06:00",
            "creators": [
                "Tool: example SPDX document only",
            ],
        },
        "name": image_id,
        "packages": [root_package] + packages,
        "relationships": relationships,
    }

    with open(f"{image_id}.spdx.json", "w") as fp:
        json.dump(spdx, fp, indent=2)


def generate_sboms_for_image(image_nvr):
    # Split to e.g. "ubi9-micro-container" and "9.4-6.1716471860"
    image_nvr_name, *image_nvr_version = image_nvr.rsplit("-", maxsplit=2)
    image_nvr_version = "-".join(image_nvr_version)

    image_index_pkg = None
    per_arch_images = []
    doc_id_generator = itertools.count(1)  # Reserve 0 for the image list SBOM.

    for image in get_image_data(image_nvr):
        packages = []

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
        for label in image["parsed_data"]["labels"]:
            if label["name"].lower() == "license":
                image_license = label["value"]

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
                    f"pkg:oci/{name}@sha256%3A{image_index_digest}?"
                    f"repository_url={repo_url}&tag={tag}"
                )
                ref = {
                    "referenceCategory": "PACKAGE-MANAGER",
                    "referenceType": "purl",
                    "referenceLocator": purl,
                }
                image_index_pkg["externalRefs"].append(ref)

        spdx_image_id = f"SPDXRef-{image_nvr_name}-{image['architecture']}"
        image_pkg = {
            "SPDXID": spdx_image_id,
            "name": f"{image_nvr_name}_{image['architecture']}",
            "versionInfo": image_nvr_version,
            "supplier": "Organization: Red Hat",
            "downloadLocation": "NOASSERTION",
            "licenseDeclared": image_license,
            "externalRefs": [],
            "checksums": [
                {
                    "algorithm": "SHA256",
                    "checksumValue": image_digest,
                }
            ],
        }
        for name, repo_url, tag in sorted(repos):
            purl = (
                f"pkg:oci/{name}@sha256%3A{image_index_digest}?"
                f"arch={image['architecture']}&repository_url={repo_url}&tag={tag}"
            )
            ref = {
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": purl,
            }
            image_pkg["externalRefs"].append(ref)
        per_arch_images.append(image_pkg)

        for rpm in get_rpms(catalog_image_id):
            rpm_purl = (
                f"pkg:rpm/redhat/{rpm['name']}@{rpm['version']}-{rpm['release']}?"
                # We don't have a way to find out which content set (RPM repo) an RPM came from,
                # so we arbitrarily choose one here (assuming we have this mapping via RPM
                # lockfiles or other means eventually).
                f"arch={rpm['architecture']}&repository_id={content_sets[0]}"
            )
            spdx_rpm_id = f"SPDXRef-{rpm['architecture']}-{rpm['name']}"
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
                # We don't have data on a checksum for binary RPMs included in images; should we?
            }
            packages.append(rpm_pkg)

        create_sbom(
            doc_id=next(doc_id_generator),
            image_id=f"{image_nvr}_" f"{image['architecture']}",
            root_package=image_pkg,
            packages=packages,
            rel_type="CONTAINS",
        )

    create_sbom(
        doc_id=0,
        image_id=image_nvr,
        root_package=image_index_pkg,
        packages=per_arch_images,
        rel_type="DESCENDANT_OF",
    )


for rpm_image in RPM_CONTAINER_IMAGES:
    generate_sboms_for_image(rpm_image)
