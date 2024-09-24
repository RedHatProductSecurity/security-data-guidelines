import json
import sys

from packageurl import PackageURL

repo_id_map = {
    # https://access.redhat.com/downloads/content/openshift-pipelines-client/1.15.0-11496.el8/x86_64/fd431d51/package
    "openshift-pipelines-client-1.14.3-11352.el8": ["pipelines-1.14-for-rhel-8-{arch}-rpms"],
    # https://access.redhat.com/downloads/content/openssl/3.0.7-18.el9_2/x86_64/fd431d51/package
    "openssl-3.0.7-18.el9_2": [
        "rhel-9-for-{arch}-baseos-eus-rpms",
        "rhel-9-for-{arch}-baseos-aus-rpms",
        "rhel-9-for-{arch}-baseos-e4s-rpms",
    ],
    # https://access.redhat.com/downloads/content/poppler/21.01.0-19.el9/x86_64/fd431d51/package
    "poppler-21.01.0-19.el9": [
        "rhel-9-for-{arch}-appstream-rpms",
        "rhel-9-for-{arch}-baseos-eus-rpms",
        "rhel-9-for-{arch}-baseos-aus-rpms",
        "rhel-9-for-{arch}-baseos-e4s-rpms",
    ],
}


def get_rpm_purl(ext_refs):
    purl_str = next(
        (ref["referenceLocator"] for ref in ext_refs if ref["referenceType"] == "purl"),
        None,
    )
    print(purl_str)
    if purl_str is None or (not purl_str.startswith("pkg:rpm/redhat")):
        return None
    return PackageURL.from_string(purl_str)


sbom_file = sys.argv[1]
sbom_name = sbom_file.rsplit("/", 1)[-1].removesuffix(".spdx.json")

if sbom_name not in repo_id_map:
    print(f"ERROR: Repo ID mapping for {sbom_name} not defined!")
    sys.exit(1)

with open(sbom_file) as fp:
    sbom = json.load(fp)

all_arches = set()
for pkg in sbom["packages"]:
    purl = get_rpm_purl(pkg.get("externalRefs", []))
    if purl is not None and purl.qualifiers["arch"] != "src":
        all_arches.add(purl.qualifiers["arch"])

for pkg in sbom["packages"]:
    purl = get_rpm_purl(pkg.get("externalRefs", []))
    if purl is None:
        continue

    new_refs = []
    for repo_id in repo_id_map[sbom_name]:
        if purl.qualifiers["arch"] == "src":
            for arch in all_arches:
                purl.qualifiers["repository_id"] = (
                    repo_id.format(arch=arch).removesuffix("-rpms") + "-source-rpms"
                )
                release_ref = {
                    "referenceCategory": "PACKAGE-MANAGER",
                    "referenceType": "purl",
                    "referenceLocator": purl.to_string(),
                }
                new_refs.append(release_ref)
        else:
            if purl.name.endswith("-debugsource"):
                repo_id = repo_id.removesuffix("-rpms") + "-source-rpms"
            elif purl.name.endswith("-debuginfo"):
                repo_id = repo_id.replace("-rpms", "-debug-rpms")
            purl.qualifiers["repository_id"] = repo_id.format(arch=purl.qualifiers["arch"])
            release_ref = {
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": purl.to_string(),
            }
            new_refs.append(release_ref)

    pkg["externalRefs"] = sorted(new_refs, key=lambda ref: ref["referenceLocator"])

with open(f"{sbom_name}.spdx.json", "w") as fp:
    json.dump(sbom, fp, indent=2)
