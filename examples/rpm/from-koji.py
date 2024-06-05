import hashlib
import json
import koji
import os
import re
import subprocess
import sys
from tempfile import TemporaryDirectory

source_re = re.compile(r"^(Source\d+):\s*((.*/)?(.*))$")
tarball_re = re.compile(
    r"^([^0-9]*)-([0-9a-f\.-]*)[\.-][a-z]"
)  # Obviously not universal
koji_profile = sys.argv[1]
build_id = sys.argv[2]
profile = koji.get_profile_module(koji_profile)
session = koji.ClientSession(profile.config.server)
build = session.getBuild(build_id)
rpms = session.listBuildRPMs(build_id)
packages = []
relationships = []
files = []


def run_syft(builddir):
    syft = subprocess.run(
        cwd=os.path.dirname(builddir),
        stdout=subprocess.PIPE,
        args=[
            "syft",
            "-o",
            "spdx-json",
            os.path.basename(builddir),
        ],
    )
    result = json.loads(syft.stdout)
    syft_pkgs = result.get("packages", [])
    if len(syft_pkgs) < 2:
        return

    packages.extend(syft_pkgs)
    files.extend(result.get("files", []))
    syft_rels = result.get("relationships", [])

    # Adjust top-level relationship to document, to link it into Source0
    # of our sources.
    for relationship in syft_rels:
        if (
            relationship["spdxElementId"] == "SPDXRef-DOCUMENT"
            and relationship["relationshipType"] == "DESCRIBES"
        ):
            relationship["spdxElementId"] = "SPDXRef-Source0"  # pick first one
            relationship["relationshipType"] = "CONTAINS"

    relationships.extend(syft_rels)


def handle_srpm(filename, name):
    with TemporaryDirectory(dir=os.getcwd()) as srcdir:
        subprocess.run(
            cwd=srcdir,
            args=[
                "rpm",
                "-D",
                f"%_topdir {srcdir}",
                "-i",
                filename,
            ],
        )
        # Fix openshift spec file
        subprocess.run(
            cwd=srcdir,
            args=[
                "sed",
                "-i",
                "-e",
                "s,/builddir/build/BUILD,%{_builddir},",
                "-e",
                "s,/builddir/build/SOURCES,%{_topdir}/SOURCES,",
                os.path.join("SPECS", f"{name}.spec"),
            ],
        )
        subprocess.run(
            cwd=srcdir,
            args=[
                "rpmbuild",
                "-D",
                f"%_topdir {srcdir}",
                "-bp",
                "--nodeps",
                f"SPECS/{name}.spec",
            ],
        )

        builddir = os.path.join(srcdir, "BUILD")
        for dirpath, dirnames, _ in os.walk(builddir):
            if dirpath == builddir:
                continue
            dirnames.clear()
            run_syft(dirpath)

        # Add sources as SPDX packages
        spectool = subprocess.run(
            cwd=srcdir,
            stdout=subprocess.PIPE,
            args=[
                "rpmdev-spectool",
                "--sources",
                f"SPECS/{name}.spec",
            ],
        )
        for line in spectool.stdout.decode("utf-8").splitlines():
            m = source_re.match(line)
            if m:
                (sourceN, url, _, sfn) = m.groups()

                # Parse filename
                tarball_match = tarball_re.match(sfn)
                if not tarball_match:
                    continue

                (sname, sver) = tarball_re.match(sfn).groups()

                # Calculate checksum
                sha256 = hashlib.sha256()
                with open(os.path.join(srcdir, "SOURCES", sfn), "rb") as sfp:
                    while True:
                        data = sfp.read()
                        if not data:
                            break
                        sha256.update(data)

            if url is None or ":" not in url:
                url = "NOASSERTION"

            sref = f"SPDXRef-{sourceN}"
            spackage = {
                "SPDXID": sref,
                "name": sname,
                "versionInfo": sver,
                "downloadLocation": url,
                "packageFileName": sfn,
                "checksums": [
                    {
                        "algorithm": "SHA256",
                        "checksumValue": sha256.hexdigest(),
                    },
                ],
            }
            if not sver:
                del spackage['versionInfo']
            pkgs_by_arch.setdefault(arch, []).append(spackage)

            relationships.append(
                {
                    "spdxElementId": "SPDXRef-SRPM",
                    "relationshipType": "CONTAINS",
                    "relatedSpdxElement": sref,
                }
            )


with TemporaryDirectory() as tmpdir:
    subprocess.run(
        cwd=tmpdir,
        stdout=None,
        args=["koji", "-p", koji_profile, "download-build", build_id],
    )
    pkgs_by_arch = {}
    for rpm in rpms:
        (name, version, release, nvr, arch) = (
            rpm["name"],
            rpm["version"],
            rpm["release"],
            rpm["nvr"],
            rpm["arch"],
        )
        if name.endswith("-debuginfo") or name.endswith("-debugsource"):
            continue
        filename = f"{tmpdir}/{name}-{version}-{release}.{arch}.rpm"
        if arch == "src":
            spdxid = "SPDXRef-SRPM"
        else:
            spdxid = f"SPDXRef-{arch}-{name}"

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
            ],
        }
        pkgs_by_arch.setdefault(arch, []).append(package)

        relationships.append(
            {
                "spdxElementId": "SPDXRef-DOCUMENT",
                "relationshipType": "DESCRIBES",
                "relatedSpdxElement": spdxid,
            }
        )

        if arch != "src":
            relationships.append(
                {
                    "spdxElementId": spdxid,
                    "relationshipType": "GENERATED_FROM",
                    "relatedSpdxElement": "SPDXRef-SRPM",
                }
            )
        else:
            handle_srpm(filename, name)

packages.extend([package for package in pkgs_by_arch["src"]])
del pkgs_by_arch["src"]
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
    "name": build["nvr"],
    "packages": packages,
    "files": files,
    "relationships": relationships,
}

with open(f"{build_id}-sbom.json", "w") as fp:
    json.dump(spdx, fp, indent=2)
