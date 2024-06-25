#!/usr/bin/python
import argparse
import json


def create_sbom(cpeid, name, versionInfo, component_sbom):
    # Collect component purls
    packages = [
        {
            "SPDXID": "SPDXRef-product",
            "name": name,
            "versionInfo": versionInfo,
            "supplier": "Organization: Red Hat",
            "downloadLocation": "https://developers.redhat.com/products/rhel/download",
            "externalRefs": [
                {
                    "referenceCategory": "SECURITY",
                    "referenceType": "cpe22Type",
                    "referenceLocator": cpeid,
                }
            ],
        }
    ]
    relationships = [
        {
            "spdxElementId": "SPDX-Document",
            "relationshipType": "DESCRIBES",
            "relatedSpdxElement": "SPDXRef-product",
        }
    ]

    described_packages = []
    for fp in component_sbom:
        sbom = json.load(fp)
        docid = sbom["SPDXID"]
        described_package_refs = [
            relation["relatedSpdxElement"]
            for relation in sbom["relationships"]
            if relation["spdxElementId"] == docid
            and relation["relationshipType"] == "DESCRIBES"
        ]
        described_packages.extend(
            [
                package
                for package in sbom["packages"]
                if package["SPDXID"] in described_package_refs
            ]
        )

    for n, described_package in enumerate(described_packages):
        spdxref = f"SPDXRef-component-{n}"
        described_package["SPDXID"] = spdxref
        described_package["downloadLocation"] = "https://developers.redhat.com/products/rhel/download#or_exact_URL"
        packages.append(described_package)

        relationships.append(
            {
                "spdxElementId": "SPDXRef-product",
                "relationshipType": "PACKAGE_OF",
                "relatedSpdxElement": spdxref,
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
        "name": name,
        "documentNamespace": f"https://access.redhat.com/security/data/sbom/beta/spdx/{name}-{versionInfo}.json",
        "packages": packages,
        "relationships": relationships,
    }
    print(json.dumps(spdx, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Create product-level SBOM",
    )
    parser.add_argument("cpeid")
    parser.add_argument("name")
    parser.add_argument("versionInfo")
    parser.add_argument("component_sbom", nargs="*", type=argparse.FileType("r"))
    args = parser.parse_args()
    create_sbom(args.cpeid, args.name, args.versionInfo, args.component_sbom)


if __name__ == "__main__":
    main()
