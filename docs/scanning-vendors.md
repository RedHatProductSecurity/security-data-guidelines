# Technical Guidance for Vulnerability Scanning Vendors

## Introduction
This article covers the basic principles for how scanning vendors should use Red Hat security data to accurately report 
on vulnerabilities, specifically for Red Hat containers images. 

### Process Overview 
Red Hat security data reports vulnerability information per product and component combination. In order to accurately report 
vulnerability information against Red Hat products using CSAF advisories and VEX data, vendors should follow these process steps: 

1. **Component Identification:** Determine what components are included in the scanned container, including information 
about the container itself and represent them using purls.
2. **Product Identification:** Determine what product the components are correlated to using container metadata using 
repositories and represent them with CPEs.
3. **Product and Component Matching:** Identify product/component pairs with product IDs by matching components to purls 
and products to CPEs.
4. **Determine Vulnerability Information:** Find vulnerability information such as severity, affectedness information 
and any available security fixes by using the product/component product IDs.

The rest of this document will cover each of these topics in more detail and include relevant examples from the following images: 

[Repository: registry.redhat.io/rhel9/python-312 Tag: 1-25](https://catalog.redhat.com/software/containers/rhel9/python-312/657b088123df896ebfacf1f0?q=python&container-tabs=overview&image=66cf3054a2c0cf86bc022be9) 

[Repository: registry.redhat.io/openshift4/ose-console-rhel9 Tag: v4.16.0-202409181705.p0.g0b1616c.assembly.stream.el9](https://catalog.redhat.com/software/containers/openshift4/ose-console-rhel9/65280984f0f695f11b13a24e?image=66eb1a1cdf6256d9be4690e6&architecture=amd64)

## Component Identification
The Package URL (purl) specification has become a widely used standard for identifying and locating software 
components throughout the open source software community.

Red Hat uses purl to identify software components, including RPMs, RPM modules and container first content, in our 
CSAF advisory and VEX files as well as our SBOM files. Detailed information about Red Hat purls can be found 
[here](https://redhatproductsecurity.github.io/security-data-guidelines/purl/).

### RPMs and RPM modules 
An RPM package is a file format used by the Red Hat Package Manager (RPM) system for software distribution and management, 
which package consists of an archive of files and metadata used to install and erase these files.

There are two types of RPM packages: source RPMs, which contain source code and a spec file and binary RPMs, which are
the files built from source packages and patches. 

Additionally, an RPM module is a set of RPM packages that represent a component and are usually installed together. 
Starting from RHEL 10, there will be no more RPM modules.

SRPMS, RPMs and RPM modules are represented in CSAF advisories and VEX data using the `rpm` purl type. More detailed
information about RPM purl usage can be found
[here](https://redhatproductsecurity.github.io/security-data-guidelines/purl/#identifying-rpm-packages).


#### Binary RPMs
Both binary RPMs and RPM modules installed in a container image can be discovered using the `rpm -qa` command from within 
the container image.
```
# Example return of RPM query
$ rpm -qa --qf '%{NAME} %{EPOCHNUM} %{VERSION} %{RELEASE} %{ARCH}\n'

libgcc 0 11.3.1 4.3.el9 x86_64
subscription-manager-rhsm-certificates 0 20220623 1.el9 noarch
setup 0 2.13.7 9.el9 noarch
filesystem 0 3.16 2.el9 x86_64
basesystem 0 11 13.el9 noarch
```

Using this information, we can format a purl for the libgcc component. 
```
# Example of binary RPM purl using name, version and architecture

pkg:rpm/redhat/libgcc@11.3.1-4.3.el9?arch=x86_64
```

#### SRPMs
Additionally, SRPMs can be discovered from a binary RPM by using the following command from within the container image.

```
# Example return of SRPM query
$ rpm -q --qf '%{SOURCERPM}\n' libgcc  
                    
gcc-11.3.1-4.3.el9.src.rpm
```

The gcc source component can be represented using the following purl.
```
# Example of SRPM purl using name, version and architecture 

pkg:rpm/redhat/gcc@11.3.1-4.3.el9?arch=src
```

#### RPM modules
RPM modules can be discovered using the same command seen in the Binary RPMs section, but will be represented slightly 
differently in purl format. 

The following is an example of how the nodejs-docs rpm from the nodejs module is represented in a purl 
```
# Example of RPM module purl using name, version, rpmmod qualifier and architecture 

pkg:rpm/redhat/nodejs-docs@20.16.0-1.module%2Bel9.4.0%2B22197%2b9e60f127?arch=x86_64&epoch=1&rpmmod=nodejs:20:9040020240807145403:rhel9
```

### Container metadata and container first content 
Container images frequently include non-RPM packages, often referred to as container first content. Non-RPM packages 
that exist in a container image are reported in security data (CVE pages, CSAF/VEX files) on the container 
level instead of the package name.

Containers are represented with the `oci` purl type. More detailed information about OCI
purl usage can be found [here](https://redhatproductsecurity.github.io/security-data-guidelines/purl/#identifying-container-images).

#### Container name and pullspec
From within the OpenShift cluster, you can determine the container pullspecs in a given namespace using the following command.
```
 # oc get pod command
 
 $ oc get pod <pod-name> -o jsonpath=' {.spec.containers[*].name}' -n <namespace>
```

#### Container tag, Openshift version and other metadata
If you already have the pullspec for the container image you are scanning, you can use the following method to 
determine additional container metadata.
```
# Example using oc image command with the pullspec
$ oc image info registry.redhat.io/openshift4/ose-console-rhel9@sha256:4a6ea66336fc875f84f24bf9ebfdf5b7c166eb19dd68d88ec6035392162b4c5a

Name:        registry.redhat.io/openshift4/ose-console-rhel9@sha256:4a6ea66336fc875f84f24bf9ebfdf5b7c166eb19dd68d88ec6035392162b4c5a
Media Type:  application/vnd.docker.distribution.manifest.v2+json
Created:     1y ago
Image Size:  210.8MB in 4 layers
Layers:      78.17MB sha256:ca1636478fe5b8e2a56600e24d6759147feb15020824334f4a798c1cb6ed58e2
             47.67MB sha256:24f5353c85f58ec262052e1b10214db36acc498ffe45b3ffd8ac3af8d7eec61c
             10.47MB sha256:0cb75215d50fe354485561a528b8b0239ac54a68fd3a6b670f3654ba54b24ec0
             74.45MB sha256:356fed97f66574bd12d47f144a3bf53471b52b11e99b79a3701da0f9f45eafe9
OS:          linux
Arch:        amd64
Command:     /opt/bridge/bin/bridge --public-dir=/opt/bridge/static
Working Dir: /
User:        1001
Environment: PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
             container=oci
             GODEBUG=x509ignoreCN=0,madvdontneed=1
             __doozer=merge
             BUILD_RELEASE=202409181705.p0.g0b1616c.assembly.stream.el9
             BUILD_VERSION=v4.16.0
             OS_GIT_MAJOR=4
             OS_GIT_MINOR=16
             OS_GIT_PATCH=0
             OS_GIT_TREE_STATE=clean
             OS_GIT_VERSION=4.16.0-202409181705.p0.g0b1616c.assembly.stream.el9-0b1616c
             SOURCE_GIT_TREE_STATE=clean
             __doozer_group=openshift-4.16
             __doozer_key=openshift-enterprise-console
             __doozer_version=v4.16.0
             OS_GIT_COMMIT=0b1616c
             SOURCE_DATE_EPOCH=1726676250
             SOURCE_GIT_COMMIT=0b1616cb0c45e5fdb5792fb96ffce1f157705369
             SOURCE_GIT_TAG=v6.0.6-23073-g0b1616cb0c
             SOURCE_GIT_URL=https://github.com/openshift/console
Labels:      License=GPLv2+
             architecture=x86_64
             build-date=2024-09-18T17:30:51
             com.redhat.component=openshift-enterprise-console-container
             com.redhat.license_terms=https://www.redhat.com/agreements
             description=This is a component of OpenShift Container Platform and provides a web console.
             distribution-scope=public
             io.buildah.version=1.29.0
             io.k8s.description=This is a component of OpenShift Container Platform and provides a web console.
             io.k8s.display-name=OpenShift Console
             io.openshift.build.commit.id=0b1616cb0c45e5fdb5792fb96ffce1f157705369
             io.openshift.build.commit.url=https://github.com/openshift/console/commit/0b1616cb0c45e5fdb5792fb96ffce1f157705369
             io.openshift.build.source-location=https://github.com/openshift/console
             io.openshift.expose-services=
             io.openshift.maintainer.component=Management Console
             io.openshift.maintainer.project=OCPBUGS
             io.openshift.tags=openshift,console
             maintainer=Samuel Padgett <spadgett@redhat.com>
             name=openshift/ose-console-rhel9
             release=202409181705.p0.g0b1616c.assembly.stream.el9
             summary=Provides the latest release of the Red Hat Extended Life Base Image.
             url=https://access.redhat.com/containers/#/registry.access.redhat.com/openshift/ose-console-rhel9/images/v4.16.0-202409181705.p0.g0b1616c.assembly.stream.el9
             vcs-ref=29bd3d1b3311656960d7b3a53d39f52f318a1da9
             vcs-type=git
             vendor=Red Hat, Inc.
             version=v4.16.0

```
 
From the output above, we can determine the following information for this image:

* Container Name and Repository: `Name:   registry.redhat.io/openshift4/ose-console-rhel9@sha256:4a6ea66336fc875f84f24bf9ebfdf5b7c166eb19dd68d88ec6035392162b4c5a` 
  * Name: `ose-console-rhel9`
  * Repository: `registry.redhat.io/openshift4/ose-console-rhel9`
* Container Architecture: `Arch: amd64` 
* Container Tag: `release=202409181705.p0.g0b1616c.assembly.stream.el9`
* OpenShift version: `version=v4.16.0`

Using this information, we can represent this container image with the following purl.
```
# Example of the container purl using name, architecture, repository and tag

pkg:oci/ose-console-rhel9@sha256:4a6ea66336fc875f84f24bf9ebfdf5b7c166eb19dd68d88ec6035392162b4c5a?arch=amd64&repository_url=registry.redhat.io/openshift4/ose-console-rhel9&tag=v4.16.0-202409181705.p0.g0b1616c.assembly.stream.el9"
```

## Product Identification
Common Platform Enumeration (CPE) is a standardized method of describing and identifying classes of applications, 
operating systems, and hardware devices present among an enterprise's computing assets.

Red Hat uses CPEs to uniquely identify each product and version, following the CPE 2.2 schema. Detailed information about 
Red Hat CPEs can be found [here](https://redhatproductsecurity.github.io/security-data-guidelines/cpe/). 

### RPM Repositories
Each Red Hat container images published after June 2020 include information about the repositories from which 
the packages used in the container are sourced. Scanning vendors will use the repositories to identify CPEs that are 
associated with the scanned image. The following sections explain different ways to identify repository information for 
a container image. 

#### Content Manifest JSON files
Previously, content manifest JSON files were included for each layer in the container image in the `root/buildinfo/` 
directory. Inside each content manifest JSON file, you'll find a `content_sets` object, which specifies the
repository names that provided the packages found in the container image. 

The following examples show how to get a list of the content manifest files from within a container image.
```
# Example of content manifest files for rhel9/python-312 image 
$ ls /root/buildinfo/content_manifests 

python-312-container-1-25.json
s2i-core-container-1-511.json
s2i-base-container-1-530.json	
ubi9-container-9.4-1214.json
```

```
# Example of content manifest files for openshift4/ose-console-rhel9 image
$ ls /root/buildinfo/content_manifests 

openshift-base-rhel9-container-v4.16.0-202409032335.p0.gb45ea65.assembly.stream.el9.json
openshift-enterprise-base-rhel9-container-v4.16.0-202409051837.p0.gb58673a.assembly.stream.el9.json
openshift-enterprise-console-container-v4.16.0-202409181705.p0.g0b1616c.assembly.stream.el9.json
rhel-els-container-9.2-483.json
```

The following examples provide a look at the content sets object within an individual manifest file.
```
# Example of repositories in content sets for rhel9/python-312 image 
$ cat /root/buildinfo/content_manifests/python-312-container-1-25.json
...
},
"content_sets": [
        "rhel-9-for-aarch64-baseos-rpms",
        "rhel-9-for-aarch64-appstream-rpms"
    ],
}
```
The two repositories identified for the rhel9/python-312 container are `rhel-9-for-aarch64-baseos-rpms` and `rhel-9-for-aarch64-appstream-rpms`.

```
# Example of repositories in content sets for openshift4/ose-console-rhel9 image
$ cat /root/buildinfo/content_manifests/openshift-enterprise-console-container-v4.16.0-202409181705.p0.g0b1616c.assembly.stream.el9.json

...
},
"content_sets": [
        "rhel-9-for-x86_64-appstream-eus-rpms__9_DOT_2",
        "rhel-9-for-x86_64-baseos-eus-rpms__9_DOT_2"
    ]
}
```
The two repositories identified for the openshift4/ose-console-rhel9 container are `rhel-9-for-x86_64-appstream-eus-rpms__9_DOT_2`
and `rhel-9-for-x86_64-baseos-eus-rpms__9_DOT_2`.

#### Content Sets JSON files
Starting from January 2025, the content manifest files have been replaced by a single content-sets.json file available in the
`/usr/share/buildinfo/` directory and the same content is copied to the legacy location `/root/buildinfo/content_manifests/`. 
In some container images, access to the root directory is locked, so the `/root/buildinfo/` location will be deprecated 
in the future and the main location for the content-sets.json metadata will remain in `/usr/share/buildinfo`.

The following is an example of how to determine the repositories used from the new content sets JSON file. 
```
# Example of repositories in the content sets JSON 
$ cat cat /usr/share/buildinfo/content-sets.json

{
  "metadata": {
    "icm_version": 1,
    "icm_spec": "https://raw.githubusercontent.com/containerbuildsystem/atomic-reactor/master/atomic_reactor/schemas/content_manifest.json",
    "image_layer_index": 0
  },
  "from_dnf_hint": true,
  "content_sets": [
    "rhel-9-for-aarch64-appstream-rpms",
    "rhel-9-for-aarch64-appstream-source-rpms",
    "rhel-9-for-aarch64-baseos-rpms",
    "rhel-9-for-aarch64-baseos-source-rpms",
    "rhel-9-for-ppc64le-appstream-rpms",
    "rhel-9-for-ppc64le-appstream-source-rpms",
    "rhel-9-for-ppc64le-baseos-rpms",
    "rhel-9-for-ppc64le-baseos-source-rpms",
    "rhel-9-for-s390x-appstream-rpms",
    "rhel-9-for-s390x-appstream-source-rpms",
    "rhel-9-for-s390x-baseos-rpms",
    "rhel-9-for-s390x-baseos-source-rpms",
    "rhel-9-for-x86_64-appstream-rpms",
    "rhel-9-for-x86_64-appstream-source-rpms",
    "rhel-9-for-x86_64-baseos-rpms",
    "rhel-9-for-x86_64-baseos-source-rpms"
  ]
}
```

#### Querying Repositories for Binary RPMs 
Although container images provide a list of repositories from which the packages in the image are sourced, vendors may also 
be interested in determining the repository that provided a specific binary RPM. This can be done using the dnf database, but 
dnf is not always shipped with container images. 
```
# Example return of repository query 
$ dnf repoquery --qf "%{repoid}" libgcc-11.3.1-4.3.el9.x86_64

rhel-9-for-x86_64-baseos-rpms
```

### RPM Repository to CPE mapping 
Red Hat maintains a JSON file to map Red Hat RPM repositories to our CPEs. Once you have identified the repositories
used for the product and version by following the previous steps, you search for the repository label and determine
both the set of related CPEs and the list of repository relative URLs. The repository to CPE mapping is located 
[here](https://security.access.redhat.com/data/metrics/repository-to-cpe.json).

The following are examples of how to determine CPEs from repositories using the repository-to-CPE JSON file.
```
# Example of repository to CPE mapping for rhel9/python-312 repositories
"rhel-9-for-aarch64-baseos-rpms": {
    "cpes": [
        "cpe:/o:redhat:enterprise_linux:9::baseos"], 
    "repo_relative_urls": [
        "content/dist/rhel9/9.1/aarch64/baseos/os", 
        "content/dist/rhel9/9.2/aarch64/baseos/os", 
        "content/dist/rhel9/9.3/aarch64/baseos/os", 
        "content/dist/rhel9/9.4/aarch64/baseos/os", 
        "content/dist/rhel9/9.5/aarch64/baseos/os", 
        "content/dist/rhel9/9.6/aarch64/baseos/os", 
        "content/dist/rhel9/9.7/aarch64/baseos/os", 
        "content/dist/rhel9/9.8/aarch64/baseos/os", 
        "content/dist/rhel9/9/aarch64/baseos/os"]
},
...
"rhel-9-for-aarch64-appstream-rpms": {
    "cpes": [
        "cpe:/a:redhat:enterprise_linux:9::appstream"], 
    "repo_relative_urls": [
        "content/dist/rhel9/9.1/aarch64/appstream/os", 
        "content/dist/rhel9/9.2/aarch64/appstream/os", 
        "content/dist/rhel9/9.3/aarch64/appstream/os", 
        "content/dist/rhel9/9.4/aarch64/appstream/os", 
        "content/dist/rhel9/9.5/aarch64/appstream/os", 
        "content/dist/rhel9/9.6/aarch64/appstream/os", 
        "content/dist/rhel9/9.7/aarch64/appstream/os", 
        "content/dist/rhel9/9.8/aarch64/appstream/os", 
        "content/dist/rhel9/9/aarch64/appstream/os"]
},
```
The two CPEs that we have identified for the rhel9/python-312 image are `cpe:/o:redhat:enterprise_linux:9::baseos` and 
`cpe:/a:redhat:enterprise_linux:9::appstream`.

```
# Example of repository to CPE mapping for openshift4/ose-console-rhel9 repositories
"rhel-9-for-x86_64-appstream-eus-rpms__9_DOT_2": {
    "cpes": [
        "cpe:/a:redhat:rhel_eus:9.2::appstream"], 
    "repo_relative_urls": [
        "content/eus/rhel9/9.2/x86_64/appstream/os"]
},
...
"rhel-9-for-x86_64-baseos-eus-rpms__9_DOT_2": {
    "cpes": [
        "cpe:/o:redhat:rhel_eus:9.2::baseos"], 
    "repo_relative_urls": [
        "content/eus/rhel9/9.2/x86_64/baseos/os"]
},
```
The two CPEs we have identified for the openshift4/ose-console-rhel9 image are `cpe:/a:redhat:rhel_eus:9.2::appstream"` 
and `cpe:/o:redhat:rhel_eus:9.2::baseos`.

## Product and Component Matching in CSAF-VEX 
The [Common Security Advisory Framework (CSAF)](https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html) is a 
standard that provides a structured, machine-readable way of representing and sharing security advisory information 
across all software and hardware providers. 

Red Hat Product Security publishes CSAF files for every single Red Hat Security Advisory (RHSA) and VEX files for every 
single CVE record that is associated with the Red Hat portfolio in any way.

CSAF advisories and VEX data includes information about products, components and the relationships
between the applicable products and components. Scanning vendors should identify the relevant products and components 
individually and then determine the available product/component combinations. 

A detailed breakdown of the format and information included in these files can be found
[here](https://redhatproductsecurity.github.io/security-data-guidelines/csaf-vex/).

### Product matching using CPEs in CSAF-VEX
CSAF advisories and VEX data represent products using a `product_name` object. The `product_name` entry will include a 
`production_identification_helper` in the form of a CPE. Vendors should follow the previous steps to determine a list of 
potential CPEs that can be used to match to `product_name` entries. More information about `product_name` objects can be
found [here](https://redhatproductsecurity.github.io/security-data-guidelines/csaf-vex/#product-family-and-product-name-examples).

#### CPEs in CSAF-VEX
CPEs in CSAF advisories and VEX data are represented slightly different based on fix status.

* Unfixed: Includes the `under_investigation`, `known_affected` and most `known_not_affected` product statuses
  * Product version: Unfixed products will only include the major product version in the CPE
  * Channel specifiers: Channel specifiers will not be included in CPEs (only applicable to RHEL 9 and before)
* Fixed: Includes all `fixed` product status and the occasional `known_not-affected` product statuses
  * Product version:
    * RHEL 9 and before: Fixed products will include a major version for main stream products and a major and minor version for xUS streams
    * RHEL 10: Fixed products will include a major and minor version for both main and xUS streams
    * Channel specifiers: Channel specifiers will be included for CPEs (only applicable to RHEL 9 and before)

#### CPE Matching Logic
Due to the differences in CPE representation based on fix status, Red Hat recommends vendors attempt to match to CPEs
using only the first 5 segments of the CPE and excluding any channel specifies. When available, it is best to use CPEs 
with a direct match to the repository information gathered from the container, but there may not always be a direct match.

If the repositories used in a container image are xUS streams, it is also necessary to check for the existence of a main
stream CPEs as well, if the vulnerability is unfixed or did not release a fix to the xUS stream.

Additionally, if the scanned container includes any container first content, scanning vendors should also check for an OpenShift CPE. 

The following are examples of the CPEs that should be used to account for matching and then the potential matches depending on 
the CVE fix statuses and product streams.
```
# Example of CPEs that should be checked for the rhel9/python-312 image  

cpe:/o:redhat:enterprise_linux:9
cpe:/a:redhat:enterprise_linux:9
```
Examples of potential CPE matches depending on fix statuses for the rhel9/python-312 container.

| CPE                                          | product_id                 | Notes                                            |
|----------------------------------------------|----------------------------|--------------------------------------------------|
| cpe:/o:redhat:enterprise_linux:9             | red_hat_enterprise_linux_9 | CVE is unfixed                                   | 
| cpe:/o:redhat:enterprise_linux:9::baseos     | BaseOS-9.5.0.Z.MAIN        | CVE-2020-11023 is fixed for RHEL 9 MAIN stream   |
| cpe:/a:redhat:enterprise_linux:9::appstream  | AppStream-9.5.0.Z.MAIN     | CVE-2020-11023 is fixed for RHEL 9 MAIN stream   |                                   
| cpe:/a:redhat:enterprise_linux:9::crb        | CRB-9.5.0.Z.MAIN           | CVE-2020-11023 is fixed for RHEL 9 MAIN stream   |                                   

For CVE-2020-11023, there are direct matches for both `cpe:/o:redhat:enterprise_linux:9` and `cpe:/a:redhat:enterprise_linux:9`, 
so the `BaseOS-9.5.0.Z.MAIN `, `AppStream-9.5.0.Z.MAIN` and `CRB-9.5.0.Z.MAIN ` product IDs should be used. 


For the OpenShift container, we also add OpenShift CPEs, because this container includes container first content. 
Using the OpenShift version discovered earlier, vendors can format those OpenShift CPEs. 
```
# Example of CPEs that should be checked for the openshift4/ose-console-rhel9

cpe:/o:redhat:enterprise_linux:9
cpe:/a:redhat:rhel_eus:9.2
cpe:/o:redhat:rhel_eus:9.2
cpe:/a:redhat:openshift:4
cpe:/a:redhat:openshift:4.16 
```

Examples of potential CPE matches depending on fix statuses for the openshift4/ose-console-rhel9 container.

| CPE                                      | product_id                             | Notes                                                      |
|------------------------------------------|----------------------------------------|------------------------------------------------------------|
| cpe:/o:redhat:enterprise_linux:9         | red_hat_enterprise_linux_9             | CVE is unfixed                                             | 
| cpe:/o:redhat:enterprise_linux:9::baseos | BaseOS-9.5.0.Z.MAIN                    | CVE-2020-11023 is fixed for RHEL 9 MAIN stream             |
| cpe:/o:redhat:rhel_eus:9.2::baseos       | BaseOS-9.2.0.Z.EUS                     | CVE-2020-11023 is fixed for RHEL 9.2 EUS                   |
| cpe:/a:redhat:rhel_eus:9.2::appstream    | AppStream-9.2.0.Z.EUS                  | CVE-2020-11023 is fixed for RHEL 9.2 EUS                   |
| cpe:/a:redhat:rhel_eus:9.2::crb          | CRB-9.2.0.Z.EUS                        | CVE-2020-11023 is fixed for RHEL 9.2 EUS                   |
| cpe:/a:redhat:openshift:4                | red_hat_openshift_container_platform_4 | CVE is unfixed                                             |
| cpe:/a:redhat:openshift:4.12::el8        | 8Base-RHOSE-4.12                       | CVE-2024-24791 is fixed for OpenShift 4.12 based on RHEL 8 |
| cpe:/a:redhat:openshift:4.12::el9        | 9Base-RHOSE-4.12                       | CVE-2024-24791 is fixed for OpenShift 4.12 based on RHEL 9 |
| cpe:/a:redhat:openshift:4.13::el8        | 8Base-RHOSE-4.13                       | CVE-2024-24791 is fixed for OpenShift 4.13 based on RHEL 8 |
| cpe:/a:redhat:openshift:4.13::el9        | 9Base-RHOSE-4.13                       | CVE-2024-24791 is fixed for OpenShift 4.13 based on RHEL 9 |
| cpe:/a:redhat:openshift:4.14::el8        | 8Base-RHOSE-4.14                       | CVE-2024-24791 is fixed for OpenShift 4.14 based on RHEL 8 |
| cpe:/a:redhat:openshift:4.14::el9        | 9Base-RHOSE-4.14                       | CVE-2024-24791 is fixed for OpenShift 4.14 based on RHEL 9 |
| cpe:/a:redhat:openshift:4.15::el8        | 8Base-RHOSE-4.15                       | CVE-2024-24791 is fixed for OpenShift 4.15 based on RHEL 8 |
| cpe:/a:redhat:openshift:4.15::el9        | 9Base-RHOSE-4.15                       | CVE-2024-24791 is fixed for OpenShift 4.15 based on RHEL 9 |
| cpe:/a:redhat:openshift:4.16::el9        | 9Base-RHOSE-4.16                       | CVE-2024-24791 is fixed for OpenShift 4.16 based on RHEL 9 |
| cpe:/a:redhat:openshift:4.17::el9        | 9Base-RHOSE-4.17                       | CVE-2024-24791 is fixed for OpenShift 4.17 based on RHEL 9 |

For CVE-2024-24791, there is a direct match for `cpe:/a:redhat:openshift:4.16 `, so the `9Base-RHOSE-4.16` product ID should 
be used for any container first content. 

### Component matching using purls in CSAF-VEX
CSAF advisories and VEX data represent components using a `product_version` object. The `product_version` entry will 
include a `production_identification_helper` in the form of a purl. Vendors should follow the previous steps to identify 
components and then format the appropriate purls to match to `product_version` entries. More information about 
`product_version` objects can be found [here](https://redhatproductsecurity.github.io/security-data-guidelines/csaf-vex/#unfixed-product-versions-vex-only-examples).

#### Purls in CSAF-VEX
Similarly to CPEs, purls in CSAF advisories and VEX data are represented differently based on fix status.

* Unfixed: Includes the `under_investigation`, `known_affected` and most `known_not_affected` product statuses
  * Component version: All unfixed components, both `rpm` and `oci` purl formats will not include any component versioning
  * Architecture: SRPMs will have the qualifier `arch=src`, but both binary RPMs and container will not include any
    architecture information
* Fixed: Includes all `fixed` product status and the occasional `known_not_affected` product statuses
  * Component version: All fixed components will include versioning in  the `rpm` and `oci` purl formats
  * Architecture: All fixed components will include architecture information in the `rpm` and `oci` purl formats

#### Purl Matching Logic
As seen above, purls in CSAF advisories and VEX files can be represented differently based on fix status. When attempting
to match a component using purls in these files, Red Hat recommends vendors to matching to against any component entries 
based on component name. 

The following are examples of the purls that could be matched depending on both the fix status and the 
fix component version.

##### RPMs, SRPMS, RPM modules
```
# Example of potential purls that should be checked for libgcc component 

pkg:rpm/redhat/libgcc 
pkg:rpm/redhat/libgcc@ 
```

Example of potential purl matches depending on fix status for the libgcc component, limited to the x86_64 architecture.  

| purl                                               | product_id                       | Notes                       |
|----------------------------------------------------|----------------------------------|-----------------------------|
| pkg:rpm/redhat/libgcc                              | libgcc                           | CVE is unfixed              | 
| pkg:rpm/redhat/libgcc@4.8.5-45.el7_9?arch=x86_64   | libgcc-0:4.8.5-45.el7_9.x86_64   | CVE-2020-11023 is fixed     |
| pkg:rpm/redhat/libgcc@4.8.5-40.el7_7?arch=x86_64   | libgcc-0:4.8.5-40.el7_7.x86_64   | CVE-2020-11023 is fixed     |
| pkg:rpm/redhat/libgcc@11.5.0-5.el9_5?arch=x86_64   | libgcc-0:11.5.0-5.el9_5.x86_64   | CVE-2020-11023 is fixed     |
| pkg:rpm/redhat/libgcc@8.4.1-1.4.el8_4?arch=x86_64  | libgcc-0:8.4.1-1.4.el8_4.x86_64  | CVE-2020-11023 is fixed     |
| pkg:rpm/redhat/libgcc@8.5.0-18.3.el8_8?arch=x86_64 | libgcc-0:8.5.0-18.3.el8_8.x86_64 | CVE-2020-11023 is fixed     |
| pkg:rpm/redhat/libgcc@8.3.1-8.el8_2?arch=x86_64    | libgcc-0:8.3.1-8.el8_2.x86_64    | CVE-2020-11023 is fixed     |
| pkg:rpm/redhat/libgcc@11.4.1-4.el9_4?arch=x86_64   | libgcc-0:11.4.1-4.el9_4.x86_64   | CVE-2020-11023 is fixed     |
| pkg:rpm/redhat/libgcc@8.5.0-23.el8_10?arch=x86_64  | libgcc-0:8.5.0-23.el8_10.x86_64  | CVE-2020-11023 is fixed     |
| pkg:rpm/redhat/libgcc@11.3.1-4.4.el9_2?arch=x86_64 | libgcc-0:11.3.1-4.4.el9_2.x86_64 | CVE-2020-11023 is fixed     |
| pkg:rpm/redhat/libgcc@8.5.0-10.4.el8_6?arch=x86_64 | libgcc-0:8.5.0-10.4.el8_6.x86_64 | CVE-2020-11023 is fixed     |
| pkg:rpm/redhat/libgcc@11.2.1-9.5.el9_0?arch=x86_64 | libgcc-0:11.2.1-9.5.el9_0.x86_64 | CVE-2020-11023 is fixed     |


##### Container first content
```
# Example of potential purls that should be checked for the ose-console-rhel9 container 

pkg:oci/ose-console-rhel9
pkg:oci/ose-console-rhel9@
```
Example of potential purl matches depending on fix status for the openshift4/ose-console-rhel9 container, 
limited to the amd64 architecture.

| purl                                                                                                                                                                                                                                  | proudct_id                                                                                                  | Notes                   |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------|
| pkg:oci/ose-console-rhel9?repository_url=registry.redhat.io/openshift4/ose-console-rhel9                                                                                                                                              | openshift4/ose-console-rhel9                                                                                | CVE is unfixed          |
| pkg:oci/ose-console-rhel9@sha256:fb32b644069ea9dbd35da2895d9fe9fda94ed50fb0707121645b168c31b57bde?arch=amd64&repository_url=registry.redhat.io/openshift4/ose-console-rhel9&tag=v4.16.0-202410180404.p0.g95b8916.assembly.stream.el9  | openshift4/ose-console-rhel9@sha256:fb32b644069ea9dbd35da2895d9fe9fda94ed50fb0707121645b168c31b57bde_amd64  | CVE-2024-24791 is fixed |
| pkg:oci/ose-console-rhel9@sha256:1b5f3e45a6778bad18ab5acbca08ee4390cd8b1fdefd2ca3020de7b127f3a54c?arch=amd64&repository_url=registry.redhat.io/openshift4/ose-console-rhel9&tag=v4.17.0-202410091535.p0.ge61f187.assembly.stream.el9  | openshift4/ose-console-rhel9@sha256:1b5f3e45a6778bad18ab5acbca08ee4390cd8b1fdefd2ca3020de7b127f3a54c_amd64  | CVE-2024-24791 is fixed |                  

### Using purls and CPE to find Product IDs 
Vendors should use the previous steps to be able to identify the appropriate `product_name` objects using CPE and `product_version` 
objects using purl. 

In order to determine unique `product_id` combinations for each product/component pair, vendors should use the `relationship`
object. More information about how to determine unique `product_id` combinations using `product_name`, `product_version` and `relationships` can 
be found [here](https://redhatproductsecurity.github.io/security-data-guidelines/csaf-vex/#relationships).

For CVE-2020-11023, the following product/component IDs are available for the rhel9/python-312 container and the libgcc component, using the
`BaseOS-9.5.0.Z.MAIN `, `AppStream-9.5.0.Z.MAIN` and `CRB-9.5.0.Z.MAIN ` product IDs to filter out any potential purl matches for irrelevant product streams. 

| Product product_id         | Component product_id           | Product/Component product_id                          | Notes                        | 
|----------------------------|--------------------------------|-------------------------------------------------------|------------------------------|
| BaseOS-9.5.0.Z.MAIN        | libgcc-0:11.5.0-5.el9_5.x86_64 | BaseOS-9.5.0.Z.MAIN:libgcc-0:11.5.0-5.el9_5.x86_64    | CVE-2020-11023 is fixed      |
| AppStream-9.5.0.Z.MAIN     | libgcc-0:11.5.0-5.el9_5.x86_64 | AppStream-9.5.0.Z.MAIN:libgcc-0:11.5.0-5.el9_5.x86_64 | CVE-2020-11023 is fixed      |
| CRB-9.5.0.Z.MAIN           | libgcc-0:11.5.0-5.el9_5.x86_64 | CRB-9.5.0.Z.MAIN:libgcc-0:11.5.0-5.el9_5.x86_64       | CVE-2020-11023 is fixed      |


For CVE-2024-24791, the following product/component ID is available for the openshift4/ose-console-rhel9 container, using the `9Base-RHOSE-4.16` product ID 
value to filter out any potential purl matches for irrelevant product streams.

| Product product_id                      | Component product_id                                                                                       | Product/Component product_id                                                                                                         | Notes                     |
|-----------------------------------------|------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|---------------------------|
| 9Base-RHOSE-4.16                        | openshift4/ose-console-rhel9@sha256:fb32b644069ea9dbd35da2895d9fe9fda94ed50fb0707121645b168c31b57bde_amd64 | 9Base-RHOSE-4.16:openshift4/ose-console-rhel9-operator@sha256:514ab7310f840027dc2609b10fa465eb6282c11d110f3d69efcf21ea5ef63ec9_amd64 | CVE-2024-24791 is fixed   |

## Determine Vulnerability Information
After following the previous steps, vendors should now have a list of unique product/component pairs in the form of 
unique `product_id` combinations. These `product_id` combinations should be used to determine severity, affectedness information and any available security fixes.

The following section will continue with CVE-2020-11023 for the rhel9/python-312 container and the libgcc component. 

### CVE Information
Basic CVE information is represented in the `vulnerabilities` section of CSAF advisories and VEX data:

* `cve`: The official CVE ID
* `cwe`: Information about the corresponding CWE, include the CWE ID and the name 
* `discovery_date`: The first reported date of the vulnerability

```
"vulnerabilities": [
    {
      "cve": "CVE-2020-11023",
      "cwe": {
        "id": "CWE-79",
        "name": "Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')"
      },
      "discovery_date": "2020-06-23T00:00:00+00:00",
```


### Affectedness 
Affectedness information is also found in the `vulnerabilities`section of the document. Each product/component `product_id` 
will be listed in the `product_status` category that corresponds to the affectedness of that product/component pair.

CVEs should be reported as follows, based on the `product_status` for the product/component pair.

| Product Status                           | Product Details                               | Component Details                                                                                                         | Reporting Information                                                                                         |
|------------------------------------------|-----------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| `under_investigation` or `known_affected`| Only main product version information available | No component version information available                                                                                | Reported                                                                                                      | 
| `known_not_affected`                     | Only main product version information available | Component version may be available                                                                                        | Not reported                                                                                                  |
| `fixed`                                  | A CPE match exists                      | The fixed component version is newer than the component version included in the scanned software                          | Reported: The component is vulnerable and an associated RHSA should also be reported.                         |
| `fixed`                                  | A CPE match exists                      | The fixed component version is either a direct match or older than the component version included in the scanned software | Not reported: The component should be considered already fixed and is not vulnerable in the scanned software. |

In the previous example, for CVE-2020-11023, the three product/component `product_id`s identified are listed in the `fixed` 
product status. Because the libgcc-0:11.5.0-5.el9_5 component version is newer than the identified libgcc-0:11.3.1-4.3.el9 
component version that was present in the rhel9/python-312 container, the package is considered vulnerable and this CVE should be reported.
```
"vulnerabilities": [
    {
        ...
        "product_status": {
            "fixed": [
                ... , 
                "AppStream-9.5.0.Z.MAIN:libgcc-0:11.5.0-5.el9_5.x86_64",
                "BaseOS-9.5.0.Z.MAIN:libgcc-0:11.5.0-5.el9_5.x86_64",
                "CRB-9.5.0.Z.MAIN:libgcc-0:11.5.0-5.el9_5.x86_64" 
                ...
            ],
        }
    }
]
```

### RHSAs 
Remediation information is also available in the `vulnerabilities` section. Each product/component pair is also listed
with `category` and `details` attributes that describe the fix status of that product and component. 

For CVE-2020-11023, the three product/component `product_id`s identified are fixed, so they are also listed  
in the `vendor_fix` category of the `remediations` object. The `url` field will provide the RHSA link that shipped the fixes.
```
"remediations": [
    ...
    },
    {
        "category": "vendor_fix",
        "details": "For details on how to apply this update, which includes the changes described in this advisory, refer to:\n\nhttps://access.redhat.com/articles/11258",
        "product_ids": [
            ... , 
             "AppStream-9.5.0.Z.MAIN:libgcc-0:11.5.0-5.el9_5.x86_64",
             "BaseOS-9.5.0.Z.MAIN:libgcc-0:11.5.0-5.el9_5.x86_64",
             "CRB-9.5.0.Z.MAIN:libgcc-0:11.5.0-5.el9_5.x86_64" 
            ...
        ],
        "url": "https://access.redhat.com/errata/RHSA-2025:1346"
    }
] 
```

### CVSS score and Severity
The last sections in the `vulnerabilities` object to be aware of are the `scores` object and the `threats` object.
Both CVSS scores and Red Hat severities are available when the product/component pair differs from the aggregate CVE severity.
Red Hat recommends that scanning vendors check the per product CVSS scores and severity scores for each vulnerability 
and report the product/component severity instead of the aggregate severity for the CVE, when applicable. 

For the rhel9/python-312 container and the libgcc component, the CVSS base score of 6.1 with a CVSS vector of 
CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N.
```
"scores": [
    {
        "cvss_v3": {
            "attackComplexity": "LOW",
            "attackVector": "NETWORK",
            "availabilityImpact": "NONE",
            "baseScore": 6.1,
            "baseSeverity": "MEDIUM",
            "confidentialityImpact": "LOW",
            "integrityImpact": "LOW",
            "privilegesRequired": "NONE",
            "scope": "CHANGED",
            "userInteraction": "REQUIRED",
            "vectorString": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
            "version": "3.1"
        },
        "products": [
            ... , 
             "AppStream-9.5.0.Z.MAIN:libgcc-0:11.5.0-5.el9_5.x86_64",
             "BaseOS-9.5.0.Z.MAIN:libgcc-0:11.5.0-5.el9_5.x86_64",
             "CRB-9.5.0.Z.MAIN:libgcc-0:11.5.0-5.el9_5.x86_64" 
            ...
        ]
    }
],
```

A Low Red Hat severity should be reported for the rhel9/python-312 container and the libgcc component.
```
"threats": [
    {
        "category": "impact",
        "details": "Low",
          "product_ids": [
             ... , 
             "AppStream-9.5.0.Z.MAIN:libgcc-0:11.5.0-5.el9_5.x86_64",
             "BaseOS-9.5.0.Z.MAIN:libgcc-0:11.5.0-5.el9_5.x86_64",
             "CRB-9.5.0.Z.MAIN:libgcc-0:11.5.0-5.el9_5.x86_64" 
             ...
          ]
        }
      ],
```


## Frequently Asked Questions (FAQs)
Vendors are encouraged to raise any questions regarding security data by opening a 'Ticket' issue type in the public
[SECDATA Jira project](https://issues.redhat.com/projects/SECDATA/).

Many scanning vendors face similar challenges when reading and parsing Red Hat's security data. To check if your question
has already been asked, you can review the list of questions asked [here](https://issues.redhat.com/browse/SECDATA-862?filter=12444038).

### Python and VENV 
[https://issues.redhat.com/browse/SECDATA-831](https://issues.redhat.com/browse/SECDATA-831)

### Repository Relative URLs 
[https://issues.redhat.com/browse/SECDATA-1089](https://issues.redhat.com/browse/SECDATA-1089)
[https://issues.redhat.com/browse/SECDATA-797](https://issues.redhat.com/browse/SECDATA-797)
[https://issues.redhat.com/browse/SECDATA-1020](https://issues.redhat.com/browse/SECDATA-1020)

### Empty Content Sets
[https://issues.redhat.com/browse/SECDATA-966](https://issues.redhat.com/browse/SECDATA-966)

### Differences in OVAL and VEX CPEs
[https://issues.redhat.com/browse/SECDATA-1141](https://issues.redhat.com/browse/SECDATA-1141)

### Duplicate RHSAs
[https://issues.redhat.com/browse/SECDATA-969](https://issues.redhat.com/browse/SECDATA-969)

## Additional Questions or Concerns 
Red Hat is committed to continually improving our security data; any future changes to the data itself or the format of 
the files are tracked in the [Red Hat Security Data Changelog](https://access.redhat.com/articles/5554431).

For any potential bugs identified regarding security data, please file a 'Bug' issue type in the public [SECDATA Jira project](https://issues.redhat.com/projects/SECDATA/).