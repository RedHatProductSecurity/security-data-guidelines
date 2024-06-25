#!/bin/bash
SBOM=product.spdx.json
cpeid=$(jq -r '.packages[] | select(.SPDXID=="SPDXRef-product").externalRefs[0].referenceLocator' "$SBOM")
name=$(jq -r '.packages[] | select(.SPDXID=="SPDXRef-product").name' "$SBOM")
versionInfo=$(jq -r '.packages[] | select(.SPDXID=="SPDXRef-product").versionInfo' "$SBOM")
python ./create.py "$cpeid" "$name" "$versionInfo" ../rpm/*.spdx.json > "$SBOM"
