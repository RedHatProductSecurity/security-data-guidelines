# Red Hat SBOMs 

## SBOM Overview 

A Software Bill of Materials (SBOM) is at its core a listing of software components for a given deliverable. That
deliverable may be a single RPM package, a container image, or an entire product version. There are several use
cases where SBOMs are beneficial:

- in-depth review of the composition of a particular product for procurement or audit purposes,

- accurate vulnerability risk assessment when combined with VEX data,

- or faster incident response when aggregating SBOMs for an entire product portfolio, as well as the pipeline components
  that build them.

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

## How SBOMs are Used

Manifest data is critical for identifying which products or CI/CD pipelines utilize specific component versions.  Red Hat uses this manifest to accurately determine the scope of affected software when a vulnerability is identified.  Inaccurate data results in flawed vulnerability tracking and reporting.  Our Vulnerability Management team uses this data in the three primary functions of Assessment, Remediation, and Response.  


## SBOM Formats

The two most widely used SBOM formats are [SPDX](https://spdx.dev/) and
[CycloneDX](https://cyclonedx.org/). Both offer similar features and data fields, and can be used to represent
complex inventories of components, their metadata (such as provenance or licensing), and additional document properties.

Most of this document focuses on Red Hat's use of SPDX 2.3 in its published SBOMs. CycloneDX 1.6 guidance for RPM
builds is in the [RPM (CycloneDX 1.6)](#rpm-cyclonedx-16) section below; SPDX 3.0 guidelines may be added in the
future.

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

For component-level _Release-time_ SBOMs (for example, container images), the package that represents the component may include product CPE(s) in its externalRefs with referenceCategory `SECURITY` and referenceType `cpe22Type` (and the CPE string in referenceLocator), so the component is explicitly associated with the Red Hat product(s) it is released as part of.

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

### Product vs Pipeline

_Product_ SBOMs, as described above in the Build vs Release section, align with the _Build_ SBOM type from CISA's guidance on
[Types of SBOM Documents](https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf).

_Pipeline_ SBOMs document the software components that make up systems, tools, and infrastructure (STIs) composing a Pipeline
for building our products. These SBOMs may align with _Build_ SBOM type as defined by CISA, or they may align with _Source_,
_Analyzed_, or even _Deployed_ SBOM types. The difference between these types lies in how the SBOMs are generated, which
depends on when during the build and deploy process of a Pipeline STI the SBOM is generated.


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
These types of SBOMs are mostly used for procurement and audit.

Red Hat aims to publish Complete SBOMs at
[https://security.access.redhat.com/data/sbom/](https://security.access.redhat.com/data/sbom/) while Shallow SBOMs
may be published for individual components such as container images.

