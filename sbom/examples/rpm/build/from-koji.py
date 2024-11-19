import hashlib
import json
import os
import re
import subprocess
import sys
from tempfile import TemporaryDirectory

import koji

# Script requires these RPMs: brewkoji, rpmdevtools, rpm-build
# Run with: ./from-koji.py brew <NVR>

source_re = re.compile(r"^(Source\d+):\s*((.*/)?(.*))$")
tarball_re = re.compile(r"^([^0-9]*)-([0-9a-f\.-]*)[\.-][a-z]")  # Obviously not universal
koji_profile = sys.argv[1]
build_id = sys.argv[2]
profile = koji.get_profile_module(koji_profile)
session = koji.ClientSession(profile.config.server)
build = session.getBuild(build_id)
rpms = session.listBuildRPMs(build_id)
packages = []
relationships = []
files = []
license_replacements = {
    " and ": " AND ",
    " or ": " OR ",
    "ASL 2.0": "Apache-2.0",
}


def sanitize_spdxid(value):
    """ "Emit a valid SPDXRef-"[idstring]"

    where [idstring] is a unique string containing letters, numbers, ., and/or -.
    """
    value = value.replace("_", "-")  # Replace underscores with dashes to retain readability
    # Remove everything else (yes, there is a minor chance for conflicting IDs, but this is an
    # example script with minimal examples; do not use this in production).
    return re.sub(r"[^a-zA-Z0-9.-]", "", value)


def get_license(filename):
    licensep = subprocess.run(
        stdout=subprocess.PIPE,
        check=True,
        args=[
            "rpm",
            "-qp",
            "--qf",
            "%{LICENSE}",
            filename,
        ],
    )
    license = licensep.stdout.decode("utf-8")
    for orig, repl in license_replacements.items():
        license = re.sub(orig, repl, license)

    return license


def get_rpm_sha256header(filename):
    sha256 = subprocess.run(
        stdout=subprocess.PIPE,
        check=True,
        args=[
            "rpm",
            "-qp",
            "--qf",
            "%{SHA256HEADER}",
            filename,
        ],
    )
    return sha256.stdout.decode("utf-8")


def get_rpm_sigmd5(filename):
    sha256 = subprocess.run(
        stdout=subprocess.PIPE,
        check=True,
        args=[
            "rpm",
            "-qp",
            "--qf",
            "%{SIGMD5}",
            filename,
        ],
    )
    return sha256.stdout.decode("utf-8")


def run_syft(builddir):
    syft = subprocess.run(
        cwd=os.path.dirname(builddir),
        check=True,
        stdout=subprocess.PIPE,
        args=[
            "syft",
            "-o",
            "spdx-json",
            # Ignore GitHub actions, which are more like build-time dependencies
            "--select-catalogers",
            "-github-actions-usage-cataloger,-github-action-workflow-usage-cataloger",
            os.path.basename(builddir),
        ],
    )
    result = json.loads(syft.stdout)
    syft_pkgs = result.get("packages", [])
    if len(syft_pkgs) < 2:
        return

    for pkg in syft_pkgs:
        if "externalRefs" not in pkg:
            continue

        # For the example data we only care about purl references
        refs = [ref for ref in pkg["externalRefs"] if ref["referenceCategory"] == "PACKAGE-MANAGER"]
        if refs:
            pkg["externalRefs"] = refs
        else:
            del pkg["externalRefs"]

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

    filtered_rels = []
    for relationship in syft_rels:
        if not (
            relationship["relationshipType"] == "OTHER"
            and relationship["comment"].startswith("evident-by:")
        ):
            filtered_rels.append(relationship)

    relationships.extend(filtered_rels)


def mock_midstream(digest, alg, source, sname, sver, url, ext):
    # Model a midstream repository for this.
    # Hard-code example value for 3.0.7
    upackage = {
        "SPDXID": f"SPDXRef-{source}-origin",
        "name": sname,
        "versionInfo": sver,
        "downloadLocation": url,
        "checksums": [
            {
                "algorithm": alg,
                "checksumValue": digest,
            },
        ],
        "externalRefs": [
            {
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator":
                    f"pkg:generic/{sname}@{sver}?download_url={url}&checksum={alg}:{digest}",
            }
        ],
    }
    if ext:
        upackage["packageFileName"] = f"{sname}-{sver}.{ext}"

    pkgs_by_arch.setdefault(arch, []).append(upackage)
    relationships.append(
        {
            "spdxElementId": f"SPDXRef-{source}",
            "relationshipType": "GENERATED_FROM",
            "relatedSpdxElement": f"SPDXRef-{source}-origin",
        }
    )

    # Construct the URL for the sourceN package
    url = f"https://github.com/(RH {sname} midstream repo)/archive/refs/tags/{sver}"
    if ext:
        url = f"{url}.{ext}"
    return url


def handle_srpm(filename, name):
    with TemporaryDirectory(dir=os.getcwd()) as srcdir:
        subprocess.run(
            check=True,
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
            check=True,
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
            check=True,
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
            check=True,
            stdout=subprocess.PIPE,
            args=[
                "rpmdev-spectool",
                "--sources",
                f"SPECS/{name}.spec",
            ],
        )
        for line in spectool.stdout.decode("utf-8").splitlines():
            m = source_re.match(line)
            if not m:
                continue

            (source, url, _, sfn) = m.groups()

            # Parse filename
            tarball_match = tarball_re.match(sfn)
            if not tarball_match:
                continue

            (sname, sver) = tarball_re.match(sfn).groups()

            # See Component Registry for a full worked example of unpacking sources
            # https://github.com/RedHatProductSecurity/component-registry/blob/
            #   c05d571ee37fde97a0bf109bcba23e3255df3964/corgi/tasks/sca.py#L296
            if sname == "openssl":
                digest = "83049d042a260e696f62406ac5c08bf706fd84383f945cf21bd61e9ed95c396e"
                alg = "SHA256"
                ext = re.sub(r".*-hobbled\.", "", sfn)
                upstream_url = f"https://openssl.org/source/openssl-{sver}.{ext}"
                url = mock_midstream(digest, alg, source, sname, sver, upstream_url, ext)

            # From distgit rpms/tektoncd-cli/tree/source-repos
            #   ?h=pipelines-1.15-rhel-8&id=c30abfafca5c2865129111a8b7b3e96499d6dbbf
            elif sname == "tektoncd-cli":
                digest = "f8b6dc07a0f51f93a138c287ccdc81fbef410554"
                alg = "SHA1"
                upstream_url = "https://github.com/tektoncd/cli"
                url = mock_midstream(digest, alg, source, sname, sver, upstream_url, "")

            elif sname == "pipeline-as-code":
                digest = "cfdf86bdbf1cdfbeadad20747a77294da4bc8c90"
                alg = "SHA1"
                upstream_url = "github.com/openshift-pipelines/pipelines-as-code"
                url = mock_midstream(digest, alg, source, sname, sver, upstream_url, "")

            elif sname == "openshift-pipelines-opc":
                digest = "c5d28fe15a4a8f6d483cdb984bc25d720d9c6631"
                alg = "SHA1"
                upstream_url = "github.com/openshift-pipelines/opc"
                url = mock_midstream(digest, alg, source, sname, sver, upstream_url, "")

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

            sref = f"SPDXRef-{source}"
            digest = sha256.hexdigest()
            spackage = {
                "SPDXID": sanitize_spdxid(sref),
                "name": sname,
                "versionInfo": sver,
                "downloadLocation": url,
                "packageFileName": sfn,
                "checksums": [
                    {
                        "algorithm": "SHA256",
                        "checksumValue": digest,
                    },
                ],
            }
            if not sver:
                del spackage["versioninfo"]

            if url != "NOASSERTION":
                purl = f"pkg:generic/{name}@{version}?download_url={url}"
                spackage["externalRefs"] = [
                    {
                        "referenceCategory": "PACKAGE-MANAGER",
                        "referenceType": "purl",
                        "referenceLocator": purl,
                    }
                ]

            pkgs_by_arch.setdefault(arch, []).append(spackage)

            relationships.append(
                {
                    "spdxElementId": "SPDXRef-SRPM",
                    "relationshipType": "CONTAINS",
                    "relatedSpdxElement": sref,
                }
            )


downloaddir = str(build_id)
try:
    os.mkdir(downloaddir)
    subprocess.run(
        cwd=str(downloaddir),
        check=True,
        stdout=None,
        args=["koji", "-p", koji_profile, "download-build", "--debuginfo", build_id],
    )
except FileExistsError:
    pass

pkgs_by_arch = {}
for rpm in rpms:
    (name, version, release, nvr, arch) = (
        rpm["name"],
        rpm["version"],
        rpm["release"],
        rpm["nvr"],
        rpm["arch"],
    )
    filename = f"{downloaddir}/{name}-{version}-{release}.{arch}.rpm"
    if arch == "src":
        spdxid = "SPDXRef-SRPM"
    else:
        spdxid = sanitize_spdxid(f"SPDXRef-{arch}-{name}")

    license = get_license(filename)
    digest = get_rpm_sha256header(filename)
    sigmd5 = get_rpm_sigmd5(filename)
    package = {
        "SPDXID": spdxid,
        "name": name,
        "versionInfo": f"{version}-{release}",
        "supplier": "Organization: Red Hat",
        "downloadLocation": "NOASSERTION",
        "packageFileName": f"{nvr}.{arch}.rpm",
        "licenseConcluded": license,
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
                "checksumValue": digest,
            },
        ],
        "annotations": [
            {
                "annotationType": "OTHER",
                # Same as document.creationInfo.creators
                "annotator": "Tool: example SPDX document only",
                # Same as document.creationInfo.created
                "annotationDate": "2006-08-14T02:34:56Z",
                "comment": f"sigmd5: {sigmd5}",
            }
        ],
    }
    pkgs_by_arch.setdefault(arch, []).append(package)

    if arch == "src":
        relationships.append(
            {
                "spdxElementId": "SPDXRef-DOCUMENT",
                "relationshipType": "DESCRIBES",
                "relatedSpdxElement": spdxid,
            }
        )
        handle_srpm(filename, name)
    else:
        relationships.append(
            {
                "spdxElementId": spdxid,
                "relationshipType": "GENERATED_FROM",
                "relatedSpdxElement": "SPDXRef-SRPM",
            }
        )

packages.extend([package for package in pkgs_by_arch["src"]])
del pkgs_by_arch["src"]
packages.extend([package for arch in pkgs_by_arch for package in pkgs_by_arch[arch]])

spdx = {
    "spdxVersion": "SPDX-2.3",
    "dataLicense": "CC0-1.0",
    "SPDXID": "SPDXRef-DOCUMENT",
    "creationInfo": {
        "created": "2006-08-14T02:34:56Z",
        "creators": [
            "Tool: example SPDX document only",
        ],
    },
    "name": build["nvr"],
    "documentNamespace": f"https://www.redhat.com/{build['nvr']}.spdx.json",
    "packages": packages,
    "files": files,
    "relationships": relationships,
}

with open(f"{build_id}.spdx.json", "w") as fp:
    # Add an extra newline at the end since a lot of editors add one when you save a file,
    # and these files get opened and read in editors a lot.
    fp.write(json.dumps(spdx, indent=2) + "\n")
