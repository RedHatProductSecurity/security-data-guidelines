Example SBOMs for RPMs
======================

Here are some examples of SBOMs for RPMs, based on some real existing
RPMs. They are intended to show what such SBOMs should look like at build
time with perfect knowledge. The build system which produced these RPMs
(Koji) did not have this knowledge, but a future one may have enough to
produce SBOMs like this.

Signing
-------

When calculating the checksums for RPM files, be aware that there are unsigned
and signed versions of these files.

Repository ID
-------------

Note that the *purl references* do not strictly adhere to the RPM purl guidelines
elsewhere in this repository, in that they do not include a `repository_id`
qualifier. The reasoning for this is that the repository ID is a release
destination not necessarily known at build time when these SBOMs are to
be produced.

When comparing two `pkg:rpm` purls, identical except that one has a
`repository_id` qualifier and the other does not, many systems may treat
these as distinct.

Build provenance
----------------

Build-time RPM SBOMs can carry upstream provenance from the RPM manifest path:

- spec `%URL:` → SPDX SRPM `homepage` / CycloneDX `externalReferences.website` (verbatim public URL)
- Koji `build.source` → CycloneDX `externalReferences.vcs` on the SRPM (placeholder URL in committed examples)
- `SourceN` tarballs / SBOMer pedigree → SPDX `CONTAINS` / `GENERATED_FROM` or CycloneDX `pedigree.ancestors`

The example generator [`from-koji.py`](from-koji.py) implements this via `parse_spec_url()`, `parse_koji_source()`, and
`build_srpm_provenance()`. Producers record observed facts only — they do not translate RPM names to upstream project
names (for example `automation-controller` is not renamed to `awx` in the SBOM).

See [Understanding SBOMs — RPM build provenance](../../../../docs/sbom.md#rpm-build-provenance) and
[Upstream source purls for RPM builds](../../../../docs/purl.md#upstream-source-purls-for-rpm-builds).

Bundled dependencies
--------------------

Build-time SBOMs may include packages for `bundled()` / `golang()` Provides
from the RPM spec (see [Understanding SBOMs — Bundled dependencies](../../../../docs/sbom.md#bundled-dependencies)).
The `vim-9.1.083-5.el10` example includes `bundled(libvterm)` linked to the
SRPM with `DEPENDENCY_OF`.

When a container image is built including RPMs, the SBOM for the container
image should refer to the RPMs using external references both with and without
the `repository_id` qualifier, to ensure purl matching to the original RPM
SBOM can succeed. An example:

```json
  "packages": {
    "name": "openssl",
    "versionInfo": "3.0.7-18.el9_2",
    "supplier": "Organization: Red Hat, Inc.",
    "originator": "Organization: Red Hat, Inc.",
    "externalRefs": [
      {
        "referenceCategory": "PACKAGE-MANAGER",
        "referenceType": "purl",
        "referenceLocator": "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=x86_64"
      },
      {
        "referenceCategory": "PACKAGE-MANAGER",
        "referenceType": "purl",
        "referenceLocator": "pkg:rpm/redhat/openssl@3.0.7-18.el9_2?arch=x86_64&repository_id=..."
      },
    ]
  }
```
