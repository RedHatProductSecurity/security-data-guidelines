import json
from pathlib import Path
from types import SimpleNamespace

# A product version and all of its variants with their unique CPE IDs.
product = SimpleNamespace(
    name="Red Hat Enterprise Linux",
    name_short="RHEL",
    version="9.2 EUS",
    cpes=["cpe:/a:redhat:rhel_eus:9.2::appstream", "cpe:/a:redhat:rhel_eus:9.2::baseos"],
)

# A root component package identified by purls containing all the repositories it is available from.
pkg = SimpleNamespace(
    name="openssl",
    version="3.0.7-18.el9_2",
    filename="openssl-3.0.7-18.el9_2.src.rpm",
    license_concluded="Apache-2.0",
    checksums=["sha-256:31b5079268339cff7ba65a0aee77930560c5adef4b1b3f8f5927a43ee46a56d9"],
    purls=[
        "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src&repository_id=rhel-9-for-aarch64-baseos-eus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src&repository_id=rhel-9-for-s390x-baseos-eus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src&repository_id=rhel-9-for-ppc64le-baseos-eus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src&repository_id=rhel-9-for-i686-baseos-eus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src&repository_id=rhel-9-for-x86_64-baseos-eus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src&repository_id=rhel-9-for-aarch64-baseos-aus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src&repository_id=rhel-9-for-s390x-baseos-aus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src&repository_id=rhel-9-for-ppc64le-baseos-aus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src&repository_id=rhel-9-for-i686-baseos-aus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src&repository_id=rhel-9-for-x86_64-baseos-aus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src&repository_id=rhel-9-for-aarch64-baseos-e4s-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src&repository_id=rhel-9-for-s390x-baseos-e4s-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src&repository_id=rhel-9-for-ppc64le-baseos-e4s-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src&repository_id=rhel-9-for-i686-baseos-e4s-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src&repository_id=rhel-9-for-x86_64-baseos-e4s-source-rpms",
    ],
)


def create_spdx():
    name = f"{product.name} {product.version}"
    name_short = (
        f"{product.name_short.lower().replace(' ', '-')}"
        f"-{product.version.lower().replace(' ', '-')}"
    )
    fname = name_short + ".spdx.json"
    sbom = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "creationInfo": {
            "created": "2006-08-14T02:34:56Z",
            "creators": ["Tool: example SPDX document only"],
        },
        "name": name,
        "documentNamespace": f"https://www.redhat.com/{fname}",
        "packages": [
            {
                "SPDXID": f"SPDXRef-{name_short.upper()}",
                "name": product.name,
                "versionInfo": product.version,
                "supplier": "Organization: Red Hat",
                "downloadLocation": "NOASSERTION",
                "licenseConcluded": "NOASSERTION",
                "externalRefs": [
                    {
                        "referenceCategory": "SECURITY",
                        "referenceLocator": cpe,
                        "referenceType": "cpe22Type",
                    }
                    for cpe in product.cpes
                ],
            }
        ]
        + [
            {
                "SPDXID": f"SPDXRef-{pkg.name}-{pkg.version.replace('_', '-')}",
                "name": pkg.name,
                "versionInfo": pkg.version,
                "supplier": "Organization: Red Hat",
                "downloadLocation": "NOASSERTION",
                "packageFileName": pkg.filename,
                "licenseConcluded": pkg.license_concluded,
                "externalRefs": [
                    {
                        "referenceCategory": "PACKAGE-MANAGER",
                        "referenceType": "purl",
                        "referenceLocator": purl,
                    }
                    for purl in pkg.purls
                ],
                "checksums": [
                    {
                        "algorithm": checksum.split(":")[0].upper().replace("-", ""),
                        "checksumValue": checksum.split(":")[1],
                    }
                    for checksum in pkg.checksums
                ],
            }
        ],
        "files": [],
        "relationships": [
            {
                "spdxElementId": "SPDXRef-DOCUMENT",
                "relationshipType": "DESCRIBES",
                "relatedSpdxElement": f"SPDXRef-{name_short.upper()}",
            },
            {
                "spdxElementId": f"SPDXRef-{pkg.name}-{pkg.version.replace('_', '-')}",
                "relationshipType": "PACKAGE_OF",
                "relatedSpdxElement": f"SPDXRef-{name_short.upper()}",
            },
        ],
    }

    return fname, sbom


def create_cdx():
    fname = (
        f"{product.name_short.lower().replace(' ', '-')}"
        f"-{product.version.lower().replace(' ', '-')}.cdx.json"
    )
    # Products MUST use the type "operating-system" (in case of RHEL) or "framework"
    # (for all other, non-OS products).
    product_component = {
        "type": "operating-system",
        "name": product.name,
        "version": product.version,
        "supplier": {"name": "Red Hat", "url": ["https://www.redhat.com"]},
    }
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "version": 1,
        "serialNumber": "urn:uuid:337d9115-4e7c-4e76-b389-51f7aed6eba8",
        "metadata": {
            # Note that `metadata.component` is a singular component and thus cannot support
            # listing more than one CPE. These are specified in the equivalent components within
            # the `components` array.
            "component": product_component,
            "timestamp": "2006-08-14T02:34:56Z",
            "tools": [{"name": "example tool", "version": "1.2.3"}],
        },
        "components": [
            product_component.copy() | {"bom-ref": cpe, "cpe": cpe} for cpe in product.cpes
        ],
        "dependencies": [],
    }

    for purl in pkg.purls:
        component = {
            # Individual packages must use type "container" (for purls of type pkg:oci)
            # "library" (for everything else).
            "type": "library",
            "name": pkg.name,
            "version": pkg.version,
            "purl": purl,
            "bom-ref": purl,
            "supplier": {"name": "Red Hat", "url": ["https://www.redhat.com"]},
            "licenses": [{"license": {"id": pkg.license_concluded}}],
            "hashes": [
                {
                    "alg": checksum.split(":")[0].upper(),
                    "content": checksum.split(":")[1],
                }
                for checksum in pkg.checksums
            ],
        }
        sbom["components"].append(component)

    for purl in pkg.purls:
        dep = {"ref": purl, "dependsOn": [cpe for cpe in product.cpes]}
        sbom["dependencies"].append(dep)

    return fname, sbom


def main():
    curr_dir = Path(__file__).parent
    fname, sbom = create_spdx()
    with open(curr_dir / fname, "w") as fp:
        fp.write(json.dumps(sbom, indent=2) + "\n")

    fname, sbom = create_cdx()
    with open(curr_dir / fname, "w") as fp:
        fp.write(json.dumps(sbom, indent=2) + "\n")


if __name__ == "__main__":
    main()
