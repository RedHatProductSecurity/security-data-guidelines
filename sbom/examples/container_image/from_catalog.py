import json
import sys

import requests

# These container images (identified by their NVR) are known to contain only RPM packages and no
# other content type.
RPM_CONTAINER_IMAGES = [
    "ubi9-micro-container-9.4-6.1716471860",
    "podman-container-9.4-8",
    "kernel-module-management-operator-container-1.1.2-25",
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
    yield from response.json()["data"]


def get_rpms(image_id):
    response = requests.get(rpm_manifest_api.format(catalog_image_id=image_id))
    response.raise_for_status()
    yield from response.json()["rpms"]


def generate_sbom_for_image(image_nvr):
    # Split to e.g. "ubi9-micro-container" and "9.4-6.1716471860"
    image_nvr_name, *image_nvr_version = image_nvr.rsplit("-", maxsplit=2)
    image_nvr_version = "-".join(image_nvr_version)

    packages = []
    relationships = []
    image_index_pkg_created = False

    for image in get_image_data(image_nvr):
        catalog_image_id = image["_id"]
        image_digest = image["image_id"]
        content_sets = image["content_sets"]

        # A container image may be available through more than one repo; collect all repos,
        # registries they are available from, and the most specific tag for each repo image.
        repos = set()
        image_index_digest = ""
        for repo in image["repositories"]:
            registry = repo["registry"]
            repo_name = repo["repository"]
            repo_namespace, _, repo_name = repo_name.rpartition("/")
            if repo_namespace:
                registry = f"{registry}/{repo_namespace}"
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
            repos.add((repo_name, registry, tags[0]["name"]))
            image_index_digest = repo["manifest_list_digest"].lstrip("sha256:")

        if not repos or not image_index_digest:
            print("ERROR: No repos or image index digest found for image ID: {catalog_image_id}")
            sys.exit(1)

        # Get license information from labels if it is set
        # TODO: is this a license statement in SPDX licence format? Does it apply to the image
        #  itself rather than its content (which is individually-licensed components?)
        image_license = "NOASSERTION"
        for label in image["parsed_data"]["labels"]:
            if label["name"].lower() == "license":
                image_license = label["value"]

        # Create an index image object, but since all arch-specific images are descendents of one
        # and the same index image, we only have to create it once.
        if not image_index_pkg_created:
            image_index_pkg = {
                "SPDXID": "SPDXRef-image-index",
                "name": image_nvr_name,
                "versionInfo": image_nvr_version,
                "supplier": "Organization: Red Hat",
                "downloadLocation": "NOASSERTION",  # TODO: should this be set to the registry+repo?
                "licenseDeclared": image_license,
                "externalRefs": [],
                "checksums": [
                    {
                        "algorithm": "SHA256",
                        "checksumValue": image_index_digest,
                    }
                ],
            }
            for name, registry, tag in sorted(repos):
                purl = (
                    f"pkg:oci/{name}@sha256%3A{image_index_digest}?"
                    f"repository_url={registry}&tag={tag}"
                )
                ref = {
                    "referenceCategory": "PACKAGE-MANAGER",
                    "referenceType": "purl",
                    "referenceLocator": purl,
                }
                image_index_pkg["externalRefs"].append(ref)

            packages.append(image_index_pkg)
            relationships.append(
                {
                    "spdxElementId": "SPDXRef-DOCUMENT",
                    "relationshipType": "DESCRIBES",
                    "relatedSpdxElement": "SPDXRef-image-index",
                }
            )
            image_index_pkg_created = True

        spdx_image_id = f"SPDXRef-{image_nvr_name}-{image['architecture']}"
        image_pkg = {
            "SPDXID": spdx_image_id,
            "name": f"{image_nvr_name}_{image['architecture']}",
            "versionInfo": image_nvr_version,
            "supplier": "Organization: Red Hat",
            "downloadLocation": "NOASSERTION",  # TODO: should this be set to the registry+repo?
            "licenseDeclared": image_license,
            "externalRefs": [],
            "checksums": [
                {
                    "algorithm": "SHA256",
                    "checksumValue": image_digest,
                }
            ],
        }
        for name, registry, tag in sorted(repos):
            purl = (
                f"pkg:oci/{name}@sha256%3A{image_index_digest}?"
                f"arch={image['architecture']}&repository_url={registry}&tag={tag}"
            )
            ref = {
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": purl,
            }
            image_pkg["externalRefs"].append(ref)

        packages.append(image_pkg)
        relationships.append(
            {
                "spdxElementId": "SPDXRef-image-index",
                "relationshipType": "CONTAINS",
                "relatedSpdxElement": spdx_image_id,
            }
        )

        for rpm in get_rpms(catalog_image_id):
            purl = (
                f"pkg:rpm/redhat/{rpm['name']}@{rpm['version']}-{rpm['release']}?"
                # We don't have a way to find out which content set (RPM repo) an RPM came from,
                # so we arbitrarily choose one here (assuming we have this mapping via RPM
                # lockfiles or other means eventually).
                f"arch={rpm['architecture']}&repository_id={content_sets[0]}"
            )
            srpm = rpm["srpm_nevra"].rstrip(".src")
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
                        "referenceLocator": purl,
                    },
                    {
                        "referenceCategory": "OTHER",
                        "referenceType": "sbom_ref",
                        # Or wherever else we host per-RPM SBOMs.
                        "referenceLocator": (
                            f"https://access.redhat.com/security/data/sbom/v1/rpm/"
                            f"{srpm}.spdx.json.bz2"
                        ),
                    },
                ],
                # We don't have data on a checksum for binary RPMs included in images; should we?
            }
            packages.append(rpm_pkg)
            relationships.append(
                {
                    "spdxElementId": spdx_image_id,
                    "relationshipType": "CONTAINS",
                    "relatedSpdxElement": spdx_rpm_id,
                }
            )

    spdx = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "creationInfo": {
            "created": "2006-08-14T02:34:56-06:00",
            "creators": [
                "Tool: example SPDX document only",
            ],
        },
        "name": image_nvr,
        "packages": packages,
        "relationships": relationships,
    }

    with open(f"{image_nvr}.spdx.json", "w") as fp:
        json.dump(spdx, fp, indent=2)


for rpm_image in RPM_CONTAINER_IMAGES:
    generate_sbom_for_image(rpm_image)
