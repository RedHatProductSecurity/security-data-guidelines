import json
from pathlib import Path
from types import SimpleNamespace

# A root component package identified by purls containing all the repositories it is available from.
ubi9_micro_9_4_6_1716471860 = SimpleNamespace(
    name="ubi9-micro-container",
    version="9.4-6.1716471860",
    filename="",
    license_concluded="GPL-2.0-or-later",
    checksums=["sha-256:1c8483e0fda0e990175eb9855a5f15e0910d2038dd397d9e2b357630f0321e6d"],
    # It's not really clear which purl to 'pick' as the summary.
    # Maybe the longest one out of ubi-micro or ubi9-micro?
    purl_summary="pkg:oci/ubi9-micro@sha256%3A1c8483e0fda0e990175eb9855a5f15e0910d2038dd397d9e2b357630f0321e6d",
    purls=[
        "pkg:oci/ubi-micro@sha256%3A1c8483e0fda0e990175eb9855a5f15e0910d2038dd397d9e2b357630f0321e6d?repository_url=registry.access.redhat.com/ubi9/ubi-micro&tag=9.4-6.1716471860",
        "pkg:oci/ubi9-micro@sha256%3A1c8483e0fda0e990175eb9855a5f15e0910d2038dd397d9e2b357630f0321e6d?repository_url=registry.access.redhat.com/ubi9-micro&tag=9.4-6.1716471860",
    ],
)

gcc_11_3_1_4_3 = SimpleNamespace(
    name="gcc",
    version="11.3.1-4.3.el9",
    filename="gcc-11.3.1-4.3.el9.src.rpm",
    license_concluded="GPL-3.0+",
    checksums=["sha-256:31b5079268339cff7ba65a0aee77930560c5adef4b1b3f8f5927a43ee46a56ab"],
    purl_summary="pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src",
    purls=[
        "pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src&repository_id=rhel-9-for-aarch64-baseos-eus-source-rpms",
        "pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src&repository_id=rhel-9-for-s390x-baseos-eus-source-rpms",
        "pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src&repository_id=rhel-9-for-ppc64le-baseos-eus-source-rpms",
        "pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src&repository_id=rhel-9-for-i686-baseos-eus-source-rpms",
        "pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src&repository_id=rhel-9-for-x86_64-baseos-eus-source-rpms",
        "pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src&repository_id=rhel-9-for-aarch64-baseos-aus-source-rpms",
        "pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src&repository_id=rhel-9-for-s390x-baseos-aus-source-rpms",
        "pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src&repository_id=rhel-9-for-ppc64le-baseos-aus-source-rpms",
        "pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src&repository_id=rhel-9-for-i686-baseos-aus-source-rpms",
        "pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src&repository_id=rhel-9-for-x86_64-baseos-aus-source-rpms",
        "pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src&repository_id=rhel-9-for-aarch64-baseos-e4s-source-rpms",
        "pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src&repository_id=rhel-9-for-s390x-baseos-e4s-source-rpms",
        "pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src&repository_id=rhel-9-for-ppc64le-baseos-e4s-source-rpms",
        "pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src&repository_id=rhel-9-for-i686-baseos-e4s-source-rpms",
        "pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src&repository_id=rhel-9-for-x86_64-baseos-e4s-source-rpms",
    ],
)

openssl_3_0_7_17 = SimpleNamespace(
    name="openssl",
    version="3.0.7-17.el9_2",
    filename="openssl-3.0.7-17.el9_2.src.rpm",
    license_concluded="Apache-2.0",
    checksums=["sha-256:31b5079268339cff7ba65a0aee77930560c5adef4b1b3f8f5927a43ee46a56d9"],
    purl_summary="pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src",
    purls=[
        "pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src&repository_id=rhel-9-for-aarch64-baseos-eus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src&repository_id=rhel-9-for-s390x-baseos-eus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src&repository_id=rhel-9-for-ppc64le-baseos-eus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src&repository_id=rhel-9-for-i686-baseos-eus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src&repository_id=rhel-9-for-x86_64-baseos-eus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src&repository_id=rhel-9-for-aarch64-baseos-aus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src&repository_id=rhel-9-for-s390x-baseos-aus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src&repository_id=rhel-9-for-ppc64le-baseos-aus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src&repository_id=rhel-9-for-i686-baseos-aus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src&repository_id=rhel-9-for-x86_64-baseos-aus-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src&repository_id=rhel-9-for-aarch64-baseos-e4s-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src&repository_id=rhel-9-for-s390x-baseos-e4s-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src&repository_id=rhel-9-for-ppc64le-baseos-e4s-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src&repository_id=rhel-9-for-i686-baseos-e4s-source-rpms",
        "pkg:rpm/redhat/openssl@3.0.7-17.el9_2?arch=src&repository_id=rhel-9-for-x86_64-baseos-e4s-source-rpms",
    ],
)

openssl_3_0_7_18 = SimpleNamespace(
    name="openssl",
    version="3.0.7-18.el9_2",
    filename="openssl-3.0.7-18.el9_2.src.rpm",
    license_concluded="Apache-2.0",
    checksums=["sha-256:9215c64e7289a058248728089e4d98ed1cc392bb5eb9b8fcbe661d57e8145bbd"],
    purl_summary="pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=src",
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

# A product version and all of its variants with their unique CPE IDs.
rhel_9_eus = SimpleNamespace(
    name="Red Hat Enterprise Linux",
    name_short="RHEL",
    version="9.2 EUS",
    cpes=["cpe:/a:redhat:rhel_eus:9.2::appstream", "cpe:/a:redhat:rhel_eus:9.2::baseos"],
    released="2006-08-14T02:34:56Z",
    packages=[openssl_3_0_7_18],
)

rhel_9_2_main_eus = SimpleNamespace(
    name="Red Hat Enterprise Linux",
    name_short="RHEL",
    version="9.2 MAIN+EUS",
    cpes=[
        "cpe:/o:redhat:enterprise_linux:9::baseos",
        "cpe:/a:redhat:enterprise_linux:9::appstream",
        "cpe:/a:redhat:rhel_eus:9.2::appstream",
        "cpe:/a:redhat:rhel_eus:9.2::baseos",
    ],
    released="2006-08-01T02:34:56Z",
    packages=[openssl_3_0_7_17, gcc_11_3_1_4_3],
)

rhel_9_4_main_eus = SimpleNamespace(
    name="Red Hat Enterprise Linux",
    name_short="RHEL",
    version="9.4 MAIN+EUS",
    cpes=["cpe:/o:redhat:enterprise_linux:9::baseos"],
    released="2008-08-01T02:34:56Z",
    packages=[ubi9_micro_9_4_6_1716471860],
)


def create_spdx(product):
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
            "created": product.released,
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
        ],
        "files": [],
        "relationships": [
            {
                "spdxElementId": "SPDXRef-DOCUMENT",
                "relationshipType": "DESCRIBES",
                "relatedSpdxElement": f"SPDXRef-{name_short.upper()}",
            }
        ],
    }

    for pkg in product.packages:
        sbom["packages"].append(
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
        )

        sbom["relationships"].append(
            {
                "spdxElementId": f"SPDXRef-{pkg.name}-{pkg.version.replace('_', '-')}",
                "relationshipType": "PACKAGE_OF",
                "relatedSpdxElement": f"SPDXRef-{name_short.upper()}",
            }
        )

    return fname, sbom


def create_cdx(product):
    fname = (
        f"{product.name_short.lower().replace(' ', '-')}"
        f"-{product.version.lower().replace(' ', '-')}.cdx.json"
    )
    # Products MUST use the type "operating-system" (in case of RHEL) or "framework"
    # (for all other, non-OS products).

    product_component = {
        "bom-ref": min(product.cpes, key=len),
        "type": "operating-system",
        "name": product.name,
        "version": product.version,
        "supplier": {"name": "Red Hat", "url": ["https://www.redhat.com"]},
        "evidence": {"identity": [{"field": "cpe", "concludedValue": cpe} for cpe in product.cpes]},
    }
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "version": 1,
        "serialNumber": "urn:uuid:337d9115-4e7c-4e76-b389-51f7aed6eba8",
        "metadata": {
            "component": product_component,
            "supplier": {"name": "Red Hat", "url": ["https://www.redhat.com"]},
            "timestamp": product.released,
            "tools": [{"name": "example tool", "version": "1.2.3"}],
        },
        "components": [product_component.copy()],
    }

    for pkg in product.packages:
        component = {
            "type": "library",
            "name": pkg.name,
            "version": pkg.version,
            "purl": pkg.purl_summary,
            "bom-ref": pkg.purl_summary,
            "supplier": {"name": "Red Hat", "url": ["https://www.redhat.com"]},
            "licenses": [{"license": {"id": pkg.license_concluded}}],
            "hashes": [
                {
                    "alg": checksum.split(":")[0].upper(),
                    "content": checksum.split(":")[1],
                }
                for checksum in pkg.checksums
            ],
            "evidence": {
                "identity": [{"field": "purl", "concludedValue": purl} for purl in pkg.purls]
            },
        }
        sbom["components"].append(component)

    return fname, sbom


def main():
    curr_dir = Path(__file__).parent
    for product in (rhel_9_4_main_eus, rhel_9_2_main_eus, rhel_9_eus):
        fname, sbom = create_spdx(product)
        with open(curr_dir / fname, "w") as fp:
            fp.write(json.dumps(sbom, indent=2) + "\n")

        fname, sbom = create_cdx(product)
        with open(curr_dir / fname, "w") as fp:
            fp.write(json.dumps(sbom, indent=2) + "\n")


if __name__ == "__main__":
    main()
