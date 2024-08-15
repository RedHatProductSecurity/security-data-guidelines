# Identifying Red Hat components using Package URL

The [Package URL (purl) specification](https://github.com/package-url/purl-spec) has become a widely used proposed
standard for identifying and locating software components throughout the open source software community. It is
supported by various tools and data formats and provides an easy way for representing package metadata across
different contexts and ecosystems.

Red Hat uses purl to identify software components in our
[CSAF](https://www.redhat.com/en/blog/csaf-vex-documents-now-generally-available) advisory and
[VEX](https://www.redhat.com/en/blog/vulnerability-exploitability-exchange-vex-beta-files-now-available) files as
well as our
[SBOM](https://www.redhat.com/en/blog/future-red-hat-security-data?channel=/en/blog/channel/security) files. We will
continue expanding our use of purl across additional security-related metadata files and software solutions in the
future as well.

To increase the interoperability of all tools processing purl strings, each purl generator must ensure that
identical software components are identified with the same purls. Adopting a consistent purl convention across the
industry improves collaboration among organizations and simplifies the exchange of (not-just-) security-related
metadata.

Below, we will cover several areas where the purl specification is overly ambiguous and allows for different ways to
interpret the same information, increasing the difficulty of processing purls created by disparate
tools. The following sections highlight how Red Hat will use purl for Red Hat produced or hosted software components.
We encourage all vendors and open source projects that generate purls that identify Red Hat components to follow
these same conventions.

Throughout this document, the terms "(software) component", "artifact", and "package" will be used interchangeably
to refer to the same concept.

## Identifying RPM packages

The [`rpm` purl type](https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst#rpm) identifies,
unsurprisingly, an RPM package. When it comes to the naming conventions of a single RPM file, Red Hat uses the NEVRA
convention that follows the `<name>-<epoch>:<version>-<release>.<architecture>.rpm` file name pattern, for example
`emacs-27.2-9.el9.x86_64.rpm`. For more information about RPM packaging conventions, see the
[RPM Packaging Guide](https://rpm-packaging-guide.github.io/)

Representing this information in a purl presents a few challenges because the purpose of the purl specification is
to not only identify a particular package (the file name already does that) but also the location from where the
package can be accessed. The emacs package example above can be represented using the following purl:

```
pkg:rpm/redhat/emacs@27.2-9.el9?arch=x86_64&repository_id=rhel-9-for-x86_64-appstream-rpms
```

The namespace value of `redhat` signifies this as an RPM package produced and distributed by Red Hat. This value
also differentiates packages available in Red Hat repositories from those that could potentially share the same name,
version, and repository name but were provided by a different vendor.

If a purl identifies a Source RPM (SRPM, a package containing source code files that are used to build one or more
RPMs containing binary artifacts), the `arch` qualifier must use the special value `src`. In the NEVRA file name
pattern, SRPM packages use a `.src.rpm` suffix. Packages that are not architecture-specific must use the special
`noarch` value in the arch qualifier.

An RPM package may also include an epoch number; if not present, it is assumed to be `0`. In a purl, epoch is
not part of the version field, but instead is specified using the `epoch` qualifier (e.g. `epoch=1`).
If the package version includes a non-zero epoch value, it must be specified using its own epoch qualifier:

```
pkg:rpm/redhat/emacs@27.2-9.el9?epoch=1&arch=src&repository_id=rhel-9-for-x86_64-appstream-rpms
```

The `rpm` purl type suggests the use of the `repository_url` qualifier to point to the base URL of the RPM
repository from where the RPM can be downloaded. We are purposefully not using the `repository_url` qualifier in Red
Hat purls because the base URL can vary depending on whether packages are sourced from Red Hat-hosted repositories
(at _cdn.redhat.com_), local Red Hat Satellite-mirrored repositories, or Cloud provider-hosted repositories. Instead,
Red Hat purls use a `repository_id` qualifier that identifies the repository from which the package can be
downloaded using YUM or DNF. 

The repository ID is a unique value that identifies an RPM repository from where RPM packages can be fetched. If the
ID of the repository is the same and the other attributes of the RPM match, such packages even though sourced from
varying URLs can be considered the same for the purposes of simple identification. Given a repository ID, you can
resolve it to a URL using your chosen base URL and a relative path of that repository that exists in the
[repository-to-cpe.json mapping file](https://access.redhat.com/security/data/meta/v1/repository-to-cpe.json). This
file maps repository IDs to both relative URL paths and CPE IDs that represent product versions in all of Red Hat's
security data files.

Another qualifier defined for the `rpm` purl type is `distro`, which is an arbitrary value that describes the Linux
distribution that the package is included in. The `distro` qualifier is not recommended to be used for Red Hat RPMs
because its values are not standardized and may, depending on how the value is interpreted, inaccurately identify a
package as being specific to a particular version of a distribution even though it may be available in multiple
distribution versions.

## Identifying RPM modules

[RPM modules](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/managing_software_with_the_dnf_tool/assembly_distribution-of-content-in-rhel-9_managing-software-with-the-dnf-tool#con_modules_assembly_distribution-of-content-in-rhel-9)
allow grouping a set of RPMs to represent a single component. Installing for example the `nodejs` module may result in
the installation of the `c-ares` library, the `npm` package manager, the `nodejs` runtime, among other RPM packages.
While RPM modules do not yet have an existing purl type, a proposal to add one called `rpmmod` has been submitted to
the purl specification that, but has not yet been merged as of today:
[https://github.com/package-url/purl-spec/pull/199](https://github.com/package-url/purl-spec/pull/199).

RPM modules follow a slightly different naming convention than regular RPMs. Each RPM module can be identified using
[NSVC](https://docs.fedoraproject.org/en-US/modularity/core-concepts/nsvca/#_forms): Name, Stream, Version, Context.
The purl for the `squid:4` module available for RHEL 8.6 EUS would be the following:

```
pkg:rpmmod/redhat/squid@4%3A8040020210420090912%3A522a0ee4?arch=ppc64le&repository_id=rhel-8-for-x86_64-appstream-eus-rpms__8_DOT_6
```

The version string is a percent-encoded value that contains the Stream, Version, and Context:
`4:8040020210420090912:522a0ee4`.

## Identifying container images

An Open Container Initiative (OCI) artifact is an arbitrary file that adheres to the OCI specification. Here we'll
focus on the identification of container images (though similar purl rules should apply to arbitrary OCI artifacts).
Container images published in the [Red Hat Ecosystem Catalog](https://catalog.redhat.com/software/containers/search)
should be identified using the
[`oci` purl type](https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst#oci).

OCI image artifacts using the
[Image Manifest specification](https://github.com/opencontainers/image-spec/blob/main/manifest.md)
are identified by a digest value and the URL of the repository from where they can be pulled. If we look at an example
container image such as
[`registry.redhat.io/ubi9/ubi:9.3-1610`](https://catalog.redhat.com/software/containers/ubi9/ubi/615bcf606feffc5384e8452e?architecture=amd64&image=65e093e60a21b531a96f93ca),
its digest value for the amd64 architecture is:
`sha256:8bca3b1be5750aeb94ef1351aa22636a54112f595d11a4d5c777890b80dfd387`. In purl, this information is represented as:

```
pkg:oci/ubi@sha256%3A8bca3b1be5750aeb94ef1351aa22636a54112f595d11a4d5c777890b80dfd387?arch=amd64&repository_url=registry.redhat.io/ubi9/ubi&tag=9.3-1610
```

Note that an image with a particular digest value may appear in multiple repositories, so the purl would only differ
in the value of the repo namespace in the `repository_url` qualifier, while representing the same image.

Only tags that are unique to a particular container image should be specified in the purl; tags such as latest or
9.3 should not be included because they represent an ever-changing piece of information that may be outdated at the
time the purl is used.

A purl may also refer to the [Image Index](https://github.com/opencontainers/image-spec/blob/main/image-index.md),
which is a higher-level representation of a set of image manifests. An image index has its own unique digest value:

```
pkg:oci/ubi@sha256%3A66233eebd72bb5baa25190d4f55e1dc3fff3a9b77186c1f91a0abdb274452072?repository_url=registry.redhat.io/ubi9/ubi&tag=9.3-1610
```

The `arch` qualifier is simply omitted in this purl.

## Identifying Maven packages

Maven packages distributed by Red Hat follow standard purl-spec rules of the
[`maven` purl type](https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst#maven):

```
pkg:maven/io.vertx/vertx-web@4.4.8.redhat-00001?type=jar&repository_url=https://maven.repository.redhat.com/ga/
```

The version string will contain a `redhat-NNNNN` suffix to indicate that the component was built from source by
Red Hat. If the type qualifier is not set, it is assumed to be `jar` (as described in the
[POM documentation](https://maven.apache.org/pom.html)). The value in the `repository_url` should be Red
Hat's Maven repository at [https://maven.repository.redhat.com/ga/](https://maven.repository.redhat.com/ga/).

## Additional Notes

The guidelines highlighted in this document represent an ideal state across all of Red Hat-published security data
that we want to achieve in the long term. In some cases, purl identifiers may be missing some of the metadata
presented here or not specify it. Please
[contact Red Hat Product Security](https://access.redhat.com/security/team/contact/) or file a Jira issue in the
[SECDATA project](https://issues.redhat.com/projects/SECDATA) if you find any discrepancies in Red Hat's security data.
Feedback on our usage of purl is always welcome and appreciated.

Also of note is the purpose of using purls as identifiers versus locators. Some purls may include certain qualifiers
that make it easier to identify them but are redundant for the purposes of locating a package. Alternatively, purls
that present different sets of qualifiers may still point to the same object. A good analogy for better
understanding this concept that is worth quoting here can be found in
[issue #242](https://github.com/package-url/purl-spec/issues/242) in the purl-spec:

> Each package type is like a country or state and defines how you can identify and locate a place reasonably
> uniquely. Uniquely enough that the post can deliver the mail. In a city with well[-]defined streets and street
> numbers, you get a precise location with the street name and number and may be an apartment number. In some cases
> you may want the address for a single person with its name, or the whole household. If someone is off the grid in
> the bayou or some isolated mountain, crafting a proper address may be more hairy and fuzzy. Worst case I may need
> GPS coordinates for these edge cases. I may also have many different ways to write an address or a name. Heck,
> some folks also live in orbit on the ISS and GPS will not work there!
