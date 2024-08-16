import json
import sys

from packageurl import PackageURL

sbom_file = sys.argv[1]
sbom_name = sbom_file.rsplit("/", 1)[-1].removesuffix(".spdx.json")

with open(sbom_file) as fp:
    sbom = json.load(fp)


for pkg in sbom["packages"]:
    for purl_ref in [ref for ref in pkg.get("externalRefs", []) if ref["referenceType"] == "purl"]:
        purl = PackageURL.from_string(purl_ref["referenceLocator"])
        if purl.type == "oci":
            purl.qualifiers.pop("tag", None)
            purl.qualifiers.pop("repository_url", None)
            purl_ref["referenceLocator"] = purl.to_string()


with open(f"{sbom_name}.spdx.json", "w") as fp:
    json.dump(sbom, fp, indent=2)
