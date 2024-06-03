import json
import koji
import sys

koji_profile = sys.argv[1]
build_id = sys.argv[2]
profile = koji.get_profile_module(koji_profile)
session = koji.ClientSession(profile.config.server)
build = session.getBuild(build_id)
rpms = session.listBuildRPMs(build_id)

pkgs = {}
relationships = []
for rpm in rpms:
    (name, version, release, nvr, arch) = (rpm['name'], rpm['version'], rpm['release'], rpm['nvr'], rpm['arch'])
    if arch == 'src':
        spdxid = "SPDXRef-SRPM"
    else:
        spdxid = f"SPDXRef-{arch}-{name}"

    package = {
        "SPDXID": spdxid,
        "name": name,
        "versionInfo": f"{version}-{release}.{arch}",
        "downloadLocation": "NOASSERTION",
        "packageFileName": f"{nvr}.{arch}.rpm",
        "externalRefs": [
            {
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": f"pkg:rpm/redhat/{name}@{version}-{release}?arch={arch}",
            }
        ],
        "checksums": [
            {
                "algorithm": "MD5",
                "checksumValue": rpm['payloadhash'],
            },
        ]
    }
    pkgs.setdefault(arch, []).append(package)

    relationships.append({
        "spdxElementId": "SPDXRef-DOCUMENT",
        "relationshipType": "DESCRIBES",
        "relatedSpdxElement": spdxid,
    })

    if arch != 'src':
        relationships.append({
            "spdxElementId": spdxid,
            "relationshipType": "GENERATED_FROM",
            "relatedSpdxElement": "SPDXRef-SRPM"
        })

packages = [package for package in pkgs['src']]
del pkgs['src']
packages.extend([package for arch in pkgs for package in pkgs[arch]])

spdx = {
    "spdxVersion": "SPDX-2.3",
    "dataLicense": "CC0-1.0",
    "SPDXID": "SPDXRef-DOCUMENT",
    "creationInfo": {
        "created": "2006-08-14T02:34:56-06:00",
        "creators": [
            "example SPDX document only",
        ],
    },
    "name": build['nvr'],
    "packages": packages,
    "relationships": relationships,
}

json.dump(spdx, sys.stdout, indent=2)
