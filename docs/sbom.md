# Understanding SBOMs

A Software Bill of Materials (SBOM) is at its core a listing of software components for a given deliverable. That
deliverable may be a single RPM package, a container image, or an entire product version. There are several use
cases where SBOMs are beneficial:

- in-depth review of the composition of a particular product for procurement or audit purposes,

- accurate vulnerability risk assessment when combined with VEX data,

- or faster incident response when aggregating SBOMs for an entire product portfolio.

When talking about inventories of components, it's also important to describe what the current design goals of a
comprehensive SBOM are:

- Provide a complete and accurate listing of software components and their relationships to each other from a
  supply chain perspective:

    - For each software component, an SBOM must list its provenance. That is, if the (downstream) component is a
      redistributed version of an open source project (upstream), the downstream component must be directly linked
      to its upstream counterpart. If an upstream component is augmented in a mirrored repository before being used
      in a build of a downstream component, this version of the component (also called a midstream component) must
      be recorded as a separate package.

    - A manifest must list all components that are included in the final deliverable that can be deployed and run by an
      end user. Any software dependencies that are used strictly during the build process must be listed as well, but
      separate from the runtime dependencies.

- Define an accurate identification of components and products usable across all published security data.

It's equally important to clarify what remains outside the scope of an SBOM:

- Provide a component dependency graph: providing dependency relationships between components as part of an
  application or an operating system is currently out of scope. This type of information is varied between different
  ecosystems, and it would be difficult to express it correctly in product-level SBOMs.
  The relationships currently represented are limited to more direct dependencies, such as those between a container
  image and the packages it includes, an operating system and its constituent packages, or a package and its
  upstream counterpart. We do not include application-level dependencies, like those where a Python package such as
  [`requests`](https://pypi.org/project/requests/) depends on another package like
  [`certifi`](https://pypi.org/project/certifi/).

- Inclusion of complete listings of individual files for each component: for each listed component in an SBOM, it is
  assumed that the user can fetch it from its indicated location, and inspect the component itself to list out its
  files. For example, when downloading a source RPM, the downloaded archive can be unpacked and inspected to acquire
  a list of files contained in it.

## Formats

The two most widely used SBOM formats are [SPDX](https://spdx.dev/) and
[CycloneDX](https://cyclonedx.org/). Both offer similar features and data fields, and can be used to represent
complex inventories of components, their metadata (such as provenance or licensing), and additional document properties.

Most of this document focuses on Red Hat's use of SPDX 2.3 in its published SBOMs. In the future, we may add similar
guidelines for CycloneDX and SPDX 3.0.

## Types

Depending on how an SBOM is generated, it will contain varying levels of information. The sections below highlight
different viewpoints of when an SBOM is created and what type of data it includes.

### Build vs Release

_Build-time_ SBOMs are created during the initial build process of an artifact (for example, when an RPM is created
from source files or a container image is built using [`buildah`](https://buildah.io/)). These SBOMs document the
components used during the build process to produce the final artifact as well as any components used for the build
process itself. This SBOM type also aligns with the _Build_ SBOM type from CISA's guidance on
[Types of SBOM Documents](https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf).

_Release-time_ SBOMs are created when an artifact is released or published. These SBOMs build upon build-time
SBOMs by incorporating additional metadata, such as the repositories or locations where an artifact is
published, and associating it with the relevant product information if there is any. Release-time SBOMs reflect the
state of the software as it is distributed to end users. This SBOM type should still be considered as a _Build_ SBOM
as defined by CISA, but it simply includes additional metadata that is not available during the build process and is
added later on. For lack of a better term, we could call these _Curated Build SBOMs_.

Red Hat's publicly available SBOMs are of the release-time type, including details about where an artifact
can be located after being released.

**Example**:

- Build-time SBOM of the `ubi9-micro` container image along with all of its installed components (RPMs):
  [build/ubi9-micro-container-9.4-6.1716471860_amd64](https://github.com/RedHatProductSecurity/security-data-guidelines/blob/main/sbom/examples/container_image/build/ubi9-micro-container-9.4-6.1716471860_amd64.spdx.json)
- Release-time SBOM of the same `ubi9-micro` container image:
  [release/ubi9-micro-container-9.4-6.1716471860_amd64](https://github.com/RedHatProductSecurity/security-data-guidelines/blob/main/sbom/examples/container_image/release/ubi9-micro-container-9.4-6.1716471860_amd64.spdx.json)

The difference between these two SBOMs is relatively minor; the release-time SBOM contains information on where the
container image (identified by two distinct purls) itself is available from:

```diff
--- sbom/examples/container_image/build/ubi9-micro-container-9.4-6.1716471860_amd64.spdx.json
+++ sbom/examples/container_image/release/ubi9-micro-container-9.4-6.1716471860_amd64.spdx.json
@@ -22,12 +22,12 @@
         {
           "referenceCategory": "PACKAGE-MANAGER",
           "referenceType": "purl",
-          "referenceLocator": "pkg:oci/ubi-micro@sha256%3A1c84[...]?arch=amd64"
+          "referenceLocator": "pkg:oci/ubi-micro@sha256%3A1c84[...]?arch=amd64&repository_url=registry.access.redhat.com/ubi9/ubi-micro&tag=9.4-6.1716471860"
         },
         {
           "referenceCategory": "PACKAGE-MANAGER",
           "referenceType": "purl",
-          "referenceLocator": "pkg:oci/ubi9-micro@sha256%3A1c84[...]?arch=amd64"
+          "referenceLocator": "pkg:oci/ubi9-micro@sha256%3A1c84[...]?arch=amd64&repository_url=registry.access.redhat.com/ubi9-micro&tag=9.4-6.1716471860"
         }
       ],
```

### Component-Level vs Product-Level

_Component-level_ SBOMs describe individual components, such as a single RPM package or a container
image. They document the full listing of individual components, libraries, and other relevant
software that went into building that component. Component-level SBOMs also include provenance metadata for certain
components. For example, a component-level SBOM of an RPM will point to the upstream sources that that RPM is based on.

_Product-level_ SBOMs describe an entire product and the subset of its components that were built and included in
the final product. A product-level SBOM may cover one or more component-level SBOMs, providing a way to connect each
release component to its parent product.

**Example**:

- Component-level SBOM of the `openssl-3.0.7-18.el9_2` RPM package:
  [release/openssl-3.0.7-18.el9_2](https://github.com/RedHatProductSecurity/security-data-guidelines/blob/main/sbom/examples/rpm/release/openssl-3.0.7-18.el9_2.spdx.json)

- Product-level SBOM of the `openssl-3.0.7-18.el9_2` RPM package as included in RHEL 9.2 EUS repositories:
  [product/rhel-9.2-eus](https://github.com/RedHatProductSecurity/security-data-guidelines/blob/main/sbom/examples/product/rhel-9.2-eus.spdx.json)

Note that the root package described by the component-level SBOM, the OpenSSL Source RPM (SRPM), is the only
reference present in the product-level SBOM to not duplicate information between the two SBOMs. The purl
reference from the SRPM package can be used to discover the component-level SBOM from the product-level SBOM.

### Shallow vs Complete

_Shallow_ SBOMs describe only the current layer of components that were used to build a specific artifact. They
focus on the immediate components without necessarily documenting their origins. The benefit of this approach is
smaller SBOM files, and the ability to make incremental changes in select SBOMs while others remain unchanged when
composing multiple SBOMs into a larger set (to describe a product, for example).

_Complete_ SBOMs provide a full, in-depth representation of all levels of the build process in a single file. A
Complete SBOM includes all component layers and their dependencies, offering a complete view of a product's composition.
These types of SBOMs are mostly used for procurement and audit purposes.

Red Hat aims to publish Complete SBOMs at
[https://security.access.redhat.com/data/sbom/](https://security.access.redhat.com/data/sbom/) while Shallow SBOMs
may be published for individual components such as container images.

## Document Structure

The following snippet shows a minimal SBOM document:

=== "SPDX 2.3"

    ```json
    {
      "spdxVersion": "SPDX-2.3",// (1)!
      "dataLicense": "CC0-1.0",// (2)!
      "SPDXID": "SPDXRef-DOCUMENT",// (3)!
      "creationInfo": {
        "created": "2006-08-14T02:34:56Z",// (4)!
        "creators": [
          "Tool: example SPDX document only"
        ]
      },
      "name": "ubi9-micro-container-9.4-6.1716471860_amd64",
      "documentNamespace": "https://www.redhat.com/ubi9-micro-container-9.4-6.1716471860_amd64.spdx.json",
      "packages": [...],
      "files": [],
      "relationships": [...]
    }
    ```

    1. SPDX version 2.3 as described at [https://spdx.github.io/spdx-spec/v2.3/](https://spdx.github.io/spdx-spec/v2.3/).

    2. The CC0-1.0 license is required by the SPDX specification.

    3. [`SPDXID`](https://spdx.github.io/spdx-spec/v2.3/document-creation-information/#63-spdx-identifier-field)
       must be set to `SPDXRef-DOCUMENT`.

    4. UTC timestamps must use the `YYYY-MM-DDThh:mm:ssZ` format.

A more detailed breakdown of some of the fields:

`creationInfo`
:   This field must contain at least the
    [`created`](https://spdx.github.io/spdx-spec/v2.3/document-creation-information/#68-creator-field) and
    [`creators`](https://spdx.github.io/spdx-spec/v2.3/document-creation-information/#69-created-field)
    fields. The timestamp in the `created` field must be set to an ISO 8601-formatted date and time string using
    the UTC timezone. The `creators` field must identify the tool and its version that was used to generate the SBOM
    file (for example, `Tool: SBOMer 1.2.3` or even `Tool: pkg:github/project-ncl/sbomer@1.0.0.M3`).
    Optionally, the organization responsible for generating the SBOM can be included in a separate string
    (for example, `Organization: Red Hat Product Security (secalert@redhat.com)`).

[`name`](https://spdx.github.io/spdx-spec/v2.3/document-creation-information/#64-document-name-field)
:   This is an arbitrary value that should describe the main artifact described by the SBOM document. This can be a
    product, a container image, or a specific package. The name should contain a descriptive value for that given
    artifact along with a version identifier. This field should only serve as a human-readable value and be shown in
    user interfaces for informational purposes. The metadata of the main package (the one _DESCRIBED_ by
    the SBOM document) should be used for any automation purposes. Note also that the `name` value may not be unique
    to a single SBOM document.

[`documentNamespace`](https://spdx.github.io/spdx-spec/v2.3/document-creation-information/#65-spdx-document-namespace-field)
:   This field uniquely identifies the SPDX SBOM document and must be a valid URI, even though that URI does not
    have to be accessible. Red Hat SBOMs can use one of two possible values:

    - A URI that is namespaced to a generic Red Hat location: `https://www.redhat.com/[DocumentID].spdx.json`.
      This URI is not accessible and only serves the purpose of identifying the document to its namespace (here,
      Red Hat).

    - A URI that is namespaced to `access.redhat.com/security/data`:
     `https://security.access.redhat.com/data/sbom/spdx/[DocumentID].spdx.json`. This URI is assumed to be accessible
      and the identified SBOM can be downloaded from the specified location.

    The `documentNamespace` value has no direct relationship to the `name` value.

The `packages` and `relationships` fields are described in depth in the sections below for each respective software
content type. The `files` field is currently unused and will thus either not be present at all, or set to an empty
list. All software components in an SBOM are described as packages; all files are assumed to be a part of _some_
package and should thus not be listed on their own in the `files` field.

### Packages and Relationships

The purpose of listing out all components as separate package objects ensures we can define meaningful relationships
between them. Some packages may for example embed other software components, and other packages may be used only
during the build process of creating a set of packages. Differentiating between these different types of components
allows us to narrow down the scope of responding to vulnerabilities to only the components that are truly affected
by a given vulnerability.

The following example shows the structure of a package object for a specific component:

=== "SPDX 2.3"

    ```json
    {
      "SPDXID": "SPDXRef-[UUID]",// (1)!
      "name": "ubi9-micro-container",
      "versionInfo": "9.4-6.1716471860",
      "supplier": "Organization: Red Hat",// (2)!
      "downloadLocation": "NOASSERTION",
      "licenseConcluded": "NOASSERTION",
      "externalRefs": [...],
      "checksums": [...]
    }
    ```

    1. A unique identifier of a given component within this document. This value should only be used to associate
       relationships to other components described in an SBOM via their relationships.

    2. The value `Organization: Red Hat` must be used for all components that are distributed by Red Hat.

A more detailed breakdown of some of the fields:

[`name`](https://spdx.github.io/spdx-spec/v2.3/package-information/#71-package-name-field)
:   The name of the component. This value may differ for different types of package ecosystems. It is recommended to
    use the `name` field of the associated purl string for consistent results.

[`versionInfo`](https://spdx.github.io/spdx-spec/v2.3/package-information/#73-package-version-field)
:   The version of the component. This value may differ for different types of package ecosystems. It is
    recommended to use the `version` field of the associated purl string for consistent results.

[`downloadLocation`](https://spdx.github.io/spdx-spec/v2.3/package-information/#77-package-download-location-field)
:   This field is used to point to the VCS that holds the related source code for this component. In most cases,
    this field will be set to `NOASSERTION` because the upstream equivalent of a downstream component is represented
    with its own package object.

[`licenseConcluded`](https://spdx.github.io/spdx-spec/v2.3/package-information/#713-concluded-license-field)
:   The concluded license of the package, based on the information available during the build. If during the build,
    this information cannot be determined, the value `NOASSERTION` should be used.

[`externalRefs`](https://spdx.github.io/spdx-spec/v2.3/package-information/#722-external-reference-comment-field)
:   At least one of the references must include a Package URL (purl) unless the object is describing a product.
    [Identifying Red Hat components using Package URL](./purl.md) documents what purl strings for different types of
    components should look like. Note that multiple purls may be used for a single package to identify multiple
    locations from where the package can be accessed.

[`checksums`](https://spdx.github.io/spdx-spec/v2.3/package-information/#710-package-checksum-field)
:   The checksums of the component. The type of checksum used will depend on the type of the component. See below
    sections for more information.


#### Container Image

A container image can be represented by a package object using the following data:

=== "SPDX 2.3"

    ```json
    {
      "SPDXID": "SPDXRef-image-index",
      "name": "ubi9-micro-container",// (1)!
      "versionInfo": "9.4-6.1716471860",
      "supplier": "Organization: Red Hat",
      "downloadLocation": "NOASSERTION",
      "licenseDeclared": "NOASSERTION",
      "externalRefs": [
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:oci/ubi-micro@sha256%3A1c8483e0fda0e990175eb9855a5f15e0910d2038dd397d9e2b357630f0321e6d?repository_url=registry.access.redhat.com/ubi9&tag=9.4-6.1716471860"
        },
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:oci/ubi9-micro@sha256%3A1c8483e0fda0e990175eb9855a5f15e0910d2038dd397d9e2b357630f0321e6d?repository_url=registry.access.redhat.com&tag=9.4-6.1716471860"
        }
      ],
      "checksums": [
        {
          "algorithm": "SHA256",
          "checksumValue": "1c8483e0fda0e990175eb9855a5f15e0910d2038dd397d9e2b357630f0321e6d"
        }
      ],
    }
    ```

    1. The name does not necessarily have to reflect what the container image is named in the container registry;
       the name component of the associated purl identifier should be used instead.

[`checksums`](https://spdx.github.io/spdx-spec/v2.3/package-information/#710-package-checksum-field)
:   The checksum value for a container image refers to the image digest value as defined in the
    [OCI Image Format](https://github.com/opencontainers/image-spec/blob/v1.0.1/descriptor.md#digests).

purl identifiers
:   A container image may have one or more purls, depending on whether the same image is available in different
    registries, or different repositories within the same registry. Note that if multiple purls are present,
    they should only ever differ in their qualifier values, not the main components such as package type, name, or
    version; multiple package objects should be used if those values differ.

license information
:   Licensing information should in most cases be set to `NOASSERTION` since licensing is set on the software
    components provided by the container image, and not the image itself.

[`downloadLocation`](https://spdx.github.io/spdx-spec/v2.3/package-information/#77-package-download-location-field)
:   The `downloadlocation` will never be set; container images don't have their own VCS repos. The location from
    where the image itself can be downloaded can be acquired from the purl identifier.

An SBOM should contain representation of both an
[Image Index](https://github.com/opencontainers/image-spec/blob/main/image-index.md) and an architecture-specific
image itself. The following is an example of an SPDX relationship between the two:

=== "SPDX 2.3"

    ```json
    {
      "relationships": [
        {
          "spdxElementId": "SPDXRef-DOCUMENT",
          "relationshipType": "DESCRIBES",
          "relatedSpdxElement": "SPDXRef-image-index"
        },
        {
          "spdxElementId": "SPDXRef-ubi9-micro-container-ppc64le",
          "relationshipType": "VARIANT_OF",
          "relatedSpdxElement": "SPDXRef-image-index"
        }
      ]
    }
    ```

An SBOM that represent a container image must also list out all the components included in that image, and create
relationships to the architecture-specific image that they are included in:

=== "SPDX 2.3"

    ```json
    {
      "spdxElementId": "SPDXRef-ubi9-micro-container-amd64",
      "relationshipType": "CONTAINS",
      "relatedSpdxElement": "SPDXRef-x86_64-bash"
    }
    ```

A container image SBOM must also list its parent container image and any container images that were used in the
process of building the container image (that is, used in a multi-stage build). As an example, consider the following
Dockerfile used to create an image (`example-container`) by building the `foo` and `bar` dependencies using separate
images:

```Dockerfile
# Dockerfile of example-container
FROM img-a AS stage1
RUN make foo

FROM img-b AS stage2
RUN make bar

FROM ubi9
COPY --from=stage1 /work/foo /foo
COPY --from=stage2 /work/bar /bar
```

The relationship of `example-container` image to the two container images (`stage1` and `stage2`) that were used to
build `foo` and `bar` so they can be added to the final layers can be represented as:

=== "SPDX 2.3"

    ```json
    {
      "spdxElementId": "SPDXRef-stage1-amd64",
      "relationshipType": "BUILD_TOOL_OF",
      "relatedSpdxElement": "SPDXRef-example-container-container-amd64"
    },
    {
      "spdxElementId": "SPDXRef-stage2-amd64",
      "relationshipType": "BUILD_TOOL_OF",
      "relatedSpdxElement": "SPDXRef-example-container-container-amd64"
    }
    ```

The parent image of `example-container` is `ubi9`. Its relationship to `example-container` can be represented as:

=== "SPDX 2.3"

    ```json
    {
      "spdxElementId": "SPDXRef-example-container-amd64",
      "relationshipType": "DESCENDANT_OF",
      "relatedSpdxElement": "SPDXRef-ubi9-amd64"
    }
    ```

<!-- TODO: add diagram that shows all the relationships -->

#### RPM

An architecture-specific RPM built by Red Hat can be represented by a package object using the following data:

=== "SPDX 2.3"

    ```json
    {
      "SPDXID": "SPDXRef-aarch64-openssl-libs",
      "name": "openssl-libs",
      "versionInfo": "3.0.7-18.el9_2",
      "supplier": "Organization: Red Hat",
      "downloadLocation": "NOASSERTION",
      "packageFileName": "openssl-libs-3.0.7-18.el9_2.aarch64.rpm",
      "licenseConcluded": "Apache-2.0",
      "externalRefs": [
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:rpm/redhat/openssl-libs@3.0.7-18.el9_2?arch=aarch64&repository_id=rhel-9-for-aarch64-baseos-eus-rpms"
        },
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:rpm/redhat/openssl-libs@3.0.7-18.el9_2?arch=aarch64&repository_id=rhel-9-for-aarch64-baseos-aus-rpms"
        },
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:rpm/redhat/openssl-libs@3.0.7-18.el9_2?arch=aarch64&repository_id=rhel-9-for-aarch64-baseos-e4s-rpms"
        }
      ],
      "checksums": [
        {
          "algorithm": "SHA256",
          "checksumValue": "cae5941219fd64e75c2b29509c6fe712bef77181a586702275a46a5e812d4dd4"
        }
      ],
      "annotations": [
        {
          "annotationType": "OTHER",
          "annotator": "Tool: example SPDX document only",
          "annotationDate": "2006-08-14T02:34:56+00:00",
          "comment": "sigmd5: 4cc665dd3173c8952184293588f9ee46"
        }
      ]
    }
    ```

[`downloadLocation`](https://spdx.github.io/spdx-spec/v2.3/package-information/#77-package-download-location-field)
:   The `downloadlocation` will never be set; container images don't have their own VCS repos. The location from
    where the image itself can be downloaded can be acquired from the purl identifier.

purl identifiers
:   A single RPM package may be available from multiple DNF/Yum repositories, in which case it will include a purl
    identifier for each repository it can be downloaded from. Note that if multiple purls are present,
    they should only ever differ in their qualifier values, not the main components such as package type, name, or
    version; multiple package objects should be used if those values differ.

[`checksums`](https://spdx.github.io/spdx-spec/v2.3/package-information/#710-package-checksum-field)
:   Minimally, the list of checksums must include the SHA256 checksum of the RPM file or source archive itself.
    All other checksums should be specified as annotations (see below). 

[`annotations`](https://spdx.github.io/spdx-spec/v2.3/annotations/)
:   A list of annotations may provide additional information that is specific to the RPM format. In the example
    above, two checksum values are included:
    - The MD5 checksum of the signed header of the RPM package is included.
    - The SHA256 checksum of the RPM header (this value does not change when an RPM is signed; unlike the file SHA256 \
      checksum used in `checksums`).

Each set of architecture-specific RPMs also have an associated source RPM (SRPM) that bundles all the source code
that was used to build those RPMs. SRPMs should be represented as a separate package object in an SBOM, and their
relationship to architecture-specific RPMs can be represented with:

=== "SPDX 2.3"

    ```json
    {
      "spdxElementId": "SPDXRef-ppc64le-openssl-libs",
      "relationshipType": "GENERATED_FROM",
      "relatedSpdxElement": "SPDXRef-SRPM"
    }
    ```

SRPMs are also linked to one or more upstream sources that were used to build the downstream RPMs. An upstream
source can be represented by a package object using the following data:

=== "SPDX 2.3"

    ```json
    {
      "SPDXID": "SPDXRef-Source0-origin",
      "name": "openssl",
      "versionInfo": "3.0.7",
      "downloadLocation": "https://openssl.org/source/openssl-3.0.7.tar.gz",
      "homepage": "https://openssl-library.org/",
      "packageFileName": "openssl-3.0.7.tar.gz",
      "checksums": [
        {
          "algorithm": "SHA256",
          "checksumValue": "83049d042a260e696f62406ac5c08bf706fd84383f945cf21bd61e9ed95c396e"
        }
      ],
      "externalRefs": [
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:generic/openssl@3.0.7?download_url=https://openssl.org/source/openssl-3.0.7.tar.gz&checksum=sha256:83049d042a260e696f62406ac5c08bf706fd84383f945cf21bd61e9ed95c396e"
        }
      ]
    }
    ```

purl identifiers
:   In cases where the upstream source is a package in a registry such as PyPI or NPM, the purl identifier will use
    the respective package type. For components that are distributed as standalone bundles (such as OpenSSL in the
    example above), `generic` purls should be used with an exact download URL from where a specific bundle of source
    code was fetched from, including a checksum (which should also be specified in the `checksums` field).

To associate a set of source archives with the SRPM that includes them, use:

=== "SPDX 2.3"

    ```json
    {
      "spdxElementId": "SPDXRef-SRPM",
      "relationshipType": "CONTAINS",
      "relatedSpdxElement": "SPDXRef-Source0"
    }
    ```

#### Product

Individual components such as packages and container images are almost always provided as part of a specific product.
Products represent a bundle of components that can be purchased, has a life cycle
([example](https://access.redhat.com/support/policy/updates/errata#RHEL8_and_9_Life_Cycle)) defined for it, and
a support policy.

If one or more components described in a given SBOM are being provided as part of a product, that product should
be represented with its own package object:

=== "SPDX 2.3"

    ```json
    {
      "SPDXID": "SPDXRef-RHEL-9.2-EUS",
      "name": "Red Hat Enterprise Linux",
      "versionInfo": "9.2 EUS",
      "supplier": "Organization: Red Hat",
      "downloadLocation": "NOASSERTION",// (1)!
      "licenseConcluded": "NOASSERTION",// (2)!
      "externalRefs": [
        {
          "referenceCategory": "SECURITY",
          "referenceLocator": "cpe:/a:redhat:rhel_eus:9.2::baseos",
          "referenceType": "cpe22Type"
        }
      ]
    }
    ```

    1. Not used because this product component is not specific enough to an architecture or ISO variant (for example,
       workstation vs server) for there to be an exact download location.

    2. Not set, only components have licenses.

`name`
:   This field must contain a human-readable name of the product.

`versionInfo`
:   This field must contain the most granular version of the product, for which the SBOM was generated.

`externalRefs`
:   External references must contain a unique identifier of the product. Red Hat uses CPE IDs to identify products.
    A given product may have one or more of these identifiers, covering all possible variants of a single product
    version.

A relationship between a component and the product it is a part of can be represented as:

=== "SPDX 2.3"

    ```json
    {
      "spdxElementId": "SPDXRef-SRPM-1",
      "relationshipType": "PACKAGE_OF",
      "relatedSpdxElement": "SPDXRef-RHEL-9.2-EUS"
    }
    ```

## Additional Notes

The guidelines highlighted in this document represent an ideal state across all of Red Hat-published security data
that we want to achieve in the long term. In some SBOMs, components may be missing their provenance data or their
license expressions may not be accurate. Please
[contact Red Hat Product Security](https://access.redhat.com/security/team/contact/) or file a Jira issue in the
[SECDATA project](https://issues.redhat.com/projects/SECDATA) if you find any discrepancies in Red Hat's security data.
Feedback on our SBOM design and publishing is always welcome and appreciated.
