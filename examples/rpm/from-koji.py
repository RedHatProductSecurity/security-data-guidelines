import hashlib
import json
import koji
import os.path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory

source_re = re.compile(r"^(Source\d+):\s*((.*/)?(.*))$")
tarball_re = re.compile(r"^([^0-9]*)-([0-9\.-]*)\.[a-z]")  # Obviously not universal
koji_profile = sys.argv[1]
build_id = sys.argv[2]
profile = koji.get_profile_module(koji_profile)
session = koji.ClientSession(profile.config.server)
build = session.getBuild(build_id)
rpms = session.listBuildRPMs(build_id)
with TemporaryDirectory() as tmpdir:
    subprocess.run(cwd=tmpdir, stdout=None, args=['koji', '-p', koji_profile, 'download-build', build_id])
    pkgs_by_arch = {}
    relationships = []
    for rpm in rpms:
        (name, version, release, nvr, arch) = (rpm['name'], rpm['version'], rpm['release'], rpm['nvr'], rpm['arch'])
        if name.endswith("-debuginfo") or name.endswith("-debugsource"):
            continue
        filename = f"{tmpdir}/{name}-{version}-{release}.{arch}.rpm"
        if arch == 'src':
            spdxid = "SPDXRef-SRPM"
            versionInfo = f"{version}-{release}"
        else:
            spdxid = f"SPDXRef-{arch}-{name}"
            versionInfo = f"{version}-{release}.{arch}"

        sha256 = hashlib.sha256()
        with open(filename, "rb") as rf:
            while True:
                data = rf.read()
                if not data:
                    break
                sha256.update(data)

        package = {
            "SPDXID": spdxid,
            "name": name,
            "versionInfo": versionInfo,
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
        else:
            with TemporaryDirectory() as srcdir:
                subprocess.run(cwd=srcdir, shell=True, args=f"rpm2cpio {filename} | cpio -id")
                spectool = subprocess.run(cwd=srcdir, stdout=subprocess.PIPE, args=[
                    'rpmdev-spectool',
                    '--sources',
                    f"{name}.spec",
                ])
                for line in spectool.stdout.decode('utf-8').splitlines():
                    m = source_re.match(line)
                    if m:
                        (sourceN, url, _, sfn) = m.groups()

                        # Parse filename
                        (sname, sver) = tarball_re.match(sfn).groups()

                        # Calculate checksum
                        sha256 = hashlib.sha256()
                        with open(os.path.join(srcdir, sfn), "rb") as sfp:
                            while True:
                                data = sfp.read()
                                if not data:
                                    break
                                sha256.update(data)

                    if url is None or ':' not in url:
                        url = 'NOASSERTION'

                    sref = f"SPDXRef-{sourceN}"
                    spackage = {
                        "SPDXID": sref,
                        "name": sname,
                        "versionInfo": sver,
                        "downloadLocation": url,
                        "checksums": [
                            {
                                "algorithm": "SHA256",
                                "checksumValue": sha256.hexdigest(),
                            },
                        ],
                    }
                    pkgs_by_arch.setdefault(arch, []).append(spackage)

                    relationships.append({
                        "spdxElementId": "SPDXRef-SRPM",
                        "relationshipType": "CONTAINS",
                        "relatedSpdxElement": sref,
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

with open(f"{build_id}-sbom.json", "w") as fp:
    json.dump(spdx, fp, indent=2)
