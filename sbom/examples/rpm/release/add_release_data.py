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
    # https://access.redhat.com/downloads/content/delve/1.7.2-1.module+el8.6.0+12972+ebab5911/x86_64/fd431d51/package
    "delve-1.7.2-1.module+el8.6.0+12972+ebab5911": [
        "rhel-8-for-{arch}-appstream-rpms",
        "rhel-8-for-{arch}-appstream-eus-rpms",
        "rhel-8-for-{arch}-appstream-aus-rpms",
        "rhel-8-for-{arch}-appstream-tus-rpms",
        "rhel-8-for-{arch}-appstream-e4s-rpms",
    ],
    # https://access.redhat.com/downloads/content/go-toolset/1.17.13-2.module+el8.6.0+22782+bd95fb4c/x86_64/fd431d51/package
    "go-toolset-1.17.13-2.module+el8.6.0+22782+bd95fb4c": [
        "rhel-8-for-{arch}-appstream-aus-rpms",
        "rhel-8-for-{arch}-appstream-tus-rpms",
        "rhel-8-for-{arch}-appstream-e4s-rpms",
    ],
    # https://access.redhat.com/downloads/content/golang/1.17.13-9.module+el8.6.0+23245+b36ba85c/x86_64/fd431d51/package
    "golang-1.17.13-9.module+el8.6.0+23245+b36ba85c": [
        "rhel-8-for-{arch}-appstream-aus-rpms",
        "rhel-8-for-{arch}-appstream-tus-rpms",
        "rhel-8-for-{arch}-appstream-e4s-rpms",
    ]
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
sbom_name = sbom_file.rsplit("/", 1)[-1].removesuffix(".spdx.json").removesuffix(".cdx.json")

if sbom_name not in repo_id_map:
    print(f"ERROR: Repo ID mapping for {sbom_name} not defined!")
    sys.exit(1)

if sbom_file.endswith(".spdx.json"):
    with open(sbom_file) as fp:
        sbom = json.load(fp)

    all_arches = set()
    for components in sbom["packages"]:
        purl = get_rpm_purl(components.get("externalRefs", []))
        if purl is not None and purl.qualifiers["arch"] != "src":
            all_arches.add(purl.qualifiers["arch"])

    for components in sbom["packages"]:
        purl = get_rpm_purl(components.get("externalRefs", []))
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

        components["externalRefs"] = sorted(new_refs, key=lambda ref: ref["referenceLocator"])

        with open(f"{sbom_name}.spdx.json", "w") as fp:
            # Add an extra newline at the end since a lot of editors add one when you save a file,
            # and these files get opened and read in editors a lot.
            fp.write(json.dumps(sbom, indent=2) + "\n")

elif sbom_file.endswith(".cdx.json"):
    with open(sbom_file) as fp:
        sbom = json.load(fp)

    all_arches = set()
    for component in sbom["components"]:
        purl = component.get("purl")
        if not purl.startswith("pkg:rpm/redhat"):
            continue
        purl_obj = PackageURL.from_string(purl)
        if purl_obj.qualifiers["arch"] == "src":
            continue
        all_arches.add(purl_obj.qualifiers["arch"])

    for component in sbom["components"]:
        purl = component.get("purl")
        if not purl.startswith("pkg:rpm/redhat"):
            continue

        purl_data = PackageURL.from_string(purl)

        new_refs = []
        for repo_id in repo_id_map[sbom_name]:
            if purl_data.qualifiers["arch"] == "src":
                for arch in all_arches:
                    purl_data.qualifiers["repository_id"] = (
                        repo_id.format(arch=arch).removesuffix("-rpms") + "-source-rpms"
                    )
                    release_ref = {
                        "field": "purl",
                        "concludedValue": purl,
                    }
                    new_refs.append(release_ref)
            else:
                if purl_data.name.endswith("-debugsource"):
                    repo_id = repo_id.removesuffix("-rpms") + "-source-rpms"
                elif purl_data.name.endswith("-debuginfo"):
                    repo_id = repo_id.replace("-rpms", "-debug-rpms")
                purl_data.qualifiers["repository_id"] = repo_id.format(
                    arch=purl_data.qualifiers["arch"]
                )
                release_ref = {
                    "field": "purl",
                    "concludedValue": purl,
                }
                new_refs.append(release_ref)

        component["evidence"] = {"identity": new_refs}

        with open(f"{sbom_name}.cdx.json", "w") as fp:
            # Add an extra newline at the end since a lot of editors add one when you save a file,
            # and these files get opened and read in editors a lot.
            fp.write(json.dumps(sbom, indent=2) + "\n")
