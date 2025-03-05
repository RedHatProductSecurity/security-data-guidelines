import json
import sys

from packageurl import PackageURL

sbom_file = sys.argv[1]
sbom_name = sbom_file.rsplit("/", 1)[-1].removesuffix(".spdx.json")

with open(sbom_file) as fp:
    sbom = json.load(fp)


relationships = sbom["relationships"]

# Find the described packages
described = [
    rel["relatedSpdxElement"]
    for rel in relationships
    if rel["spdxElementId"] == "SPDXRef-DOCUMENT" and rel["relationshipType"] == "DESCRIBES"
]
# Find any packages that are VARIANT_OF the described packages
variants = [
    rel["spdxElementId"]
    for rel in relationships
    if rel["relatedSpdxElement"] in described and rel["relationshipType"] == "VARIANT_OF"
]
built = described + variants
for pkg in [pkg for pkg in sbom["packages"] if pkg["SPDXID"] in built]:
    for purl_ref in [ref for ref in pkg.get("externalRefs", []) if ref["referenceType"] == "purl"]:
        purl = PackageURL.from_string(purl_ref["referenceLocator"])
        if purl.type == "oci":
            purl.qualifiers.pop("tag", None)
            purl.qualifiers.pop("repository_url", None)
            # Escape colon because: https://github.com/package-url/packageurl-python/issues/152
            purl_ref["referenceLocator"] = purl.to_string().replace("sha256:", "sha256%3A")


with open(f"{sbom_name}.spdx.json", "w") as fp:
    # Add an extra newline at the end since a lot of editors add one when you save a file,
    # and these files get opened and read in editors a lot.
    fp.write(json.dumps(sbom, indent=2) + "\n")
