import hashlib
import json
import koji
import subprocess
import sys
from tempfile import TemporaryDirectory

koji_profile = sys.argv[1]
build_id = sys.argv[2]
profile = koji.get_profile_module(koji_profile)
session = koji.ClientSession(profile.config.server)
build = session.getBuild(build_id)
rpms = session.listBuildRPMs(build_id)
with TemporaryDirectory() as tmpdir:
    subprocess.run(cwd=tmpdir, args=['koji', '-p', koji_profile, 'download-build', build_id])
    pkgs_by_arch = {}
    relationships = []
    for rpm in rpms:
        (name, version, release, nvr, arch) = (rpm['name'], rpm['version'], rpm['release'], rpm['nvr'], rpm['arch'])
        if name.endswith("-debuginfo") or name.endswith("-debugsource"):
            continue
        if arch == 'src':
            spdxid = "SPDXRef-SRPM"
        else:
            spdxid = f"SPDXRef-{arch}-{name}"

        sha256 = hashlib.sha256()
        with open(f"{tmpdir}/{name}-{version}-{release}.{arch}.rpm", "rb") as rf:
            while True:
                data = rf.read()
                if not data:
                    break
                sha256.update(data)

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
                    "algorithm": "SHA256",
                    "checksumValue": sha256.hexdigest(),
                },
            ]
        }
        pkgs_by_arch.setdefault(arch, []).append(package)

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

packages = [package for package in pkgs_by_arch['src']]
del pkgs_by_arch['src']
packages.extend([package for arch in pkgs_by_arch for package in pkgs_by_arch[arch]])

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
