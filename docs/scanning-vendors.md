# Technical Guidance for Vulnerability Scanning Vendors

## Introduction
The following sections in this article will cover the basic principles for how scanning vendors should use Red Hat security 
data to accurately report on vulnerabilities, specifically for Red Hat containers images. 

### Process Overview 
Red Hat security data reports vulnerability information per product and component combination. In order to accurately report 
vulnerability information against Red Hat products using CSAF advisories and VEX data, vendors should follow these process steps: 

1. **Component Identification:** Determine what components are included in the scanned container, including information about the container itself.
2. **Product Identification:** Determine what product the components are correlated to using container metadata.
3. **Product and Component Matching:** Using the information gather in steps 1 & 2, vendors will identify components using purls, products using CPEs and product/component pairs using unique product IDs. 
4. **Determine Vulnerability Information:** Vulnerability information such 

The rest of this document will cover each of these topics in more detail and include relevant examples from the following images: 

[Repository: registry.redhat.io/rhel9/python-312 Tag: 1-25](https://catalog.redhat.com/software/containers/rhel9/python-312/657b088123df896ebfacf1f0?q=python&container-tabs=overview&image=66cf3054a2c0cf86bc022be9) 

[Repository: registry.redhat.io/openshift4/ose-console-rhel9 Tag: v4.16.0-202409181705.p0.g0b1616c.assembly.stream.el9](https://catalog.redhat.com/software/containers/openshift4/ose-console-rhel9/65280984f0f695f11b13a24e?image=66eb1a1cdf6256d9be4690e6&architecture=amd64)

## Component Identification and purls
In order to accurately report on vulnerabilities in Red Hat products, scanning vendors must properly identify the 
Red Hat package versions for RPMs, RPM modules and container first content, to correctly identify delivered Red Hat 
security patches. The following section provides guidance on how to find information about packages and how they are 
reported in Red Hat's CSAF advisories and VEX  content. 

### RPMs and RPM modules 
An RPM package is a file format used by the Red Hat Package Manager (RPM) system for software distribution and management, 
which package consists of an archive of files and metadata used to install and erase these files.

There are two types of RPM packages: source RPMs and binary RPMs. Both types share the same file format and tooling, but have
different contents and serve different purposes. A source RPM (SRPM) contains source code and a spec file, which 
describes how to build the source code into a binary RPM, while a binary RPM contains the binaries built from the 
sources and patches.

Similarly, an RPM module is a set of RPM packages that represent a component and are usually installed together. A typical module 
contains packages with an application, packages with the application-specific dependency libraries, packages with 
documentation for the application, and packages with helper utilities. 

#### Binary RPMs
Both binary RPMs and RPM modules installed in a container image can be discovered using the `rpm -qa` command.
```
# Example return of RPM query
$ rpm -qa

libgcc-11.3.1-4.3.el9.x86_64
subscription-manager-rhsm-certificates-20220623-1.el9.noarch
setup-2.13.7-9.el9.noarch
filesystem-3.16-2.el9.x86_64
basesystem-11-13.el9.noarch
```

#### SRPMs
Additionally, SRPMs can be discovered from a binary RPM by using the following command: 
 ```
# Example return of SRPM query
$ rpm -q --qf '%{NEVRA} %{SOURCERPM}\n' libgcc-11.3.1-4.3.el9.x86_64

libgcc-11.3.1-4.3.el9.x86_64 gcc-11.3.1-4.3.el9.src.rpm
 ```

### Container metadata and container first content 
Container images frequently include non-RPM packages, often referred to as container first content. Non-RPM packages 
that exist in a container image are reported in security data (CVE pages, CSAF/VEX files) on the container 
level instead of the package name. 

#### Container name and pullspec
From within the pod, you can determine the container name and pullspec in a given namespace using the following command. 

```
 # Example of using oc get pod 
 $ oc get pod <pod-name> -o jsonpath=' {.spec.containers[*].name}' -n <namespace>
 TODO example output
```

#### Container tag, Openshift version and other metadata
If you already have the pullspec for the container image you are scanning, you can use the following commands to 
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

* Container Name: name=openshift/ose-console-rhel9
* Container Tag: release=202409181705.p0.g0b1616c.assembly.stream.el9 
* Openshift Minor Version: version=v4.16.0

```
# Example using podman inspect with the pullspec
$ podman inspect registry.redhat.io/rhel9/python-312@sha256:297775052f3359f454971aa08fa1691e1aa00e77331060ef3dad0c0395943ea2  
[
     {
          "Id": "c61270b11bce136ba431556967613299bd5198f7d82b5be53628e7f2a836db34",
          "Digest": "sha256:297775052f3359f454971aa08fa1691e1aa00e77331060ef3dad0c0395943ea2",
          "RepoTags": [],
          "RepoDigests": [
               "registry.redhat.io/rhel9/python-312@sha256:297775052f3359f454971aa08fa1691e1aa00e77331060ef3dad0c0395943ea2"
          ],
          "Parent": "",
          "Comment": "",
          "Created": "2024-08-28T14:01:20.979463657Z",
          "Config": {
               "User": "1001",
               "ExposedPorts": {
                    "8080/tcp": {}
               },
               "Env": [
                    "container=oci",
                    "STI_SCRIPTS_URL=image:///usr/libexec/s2i",
                    "STI_SCRIPTS_PATH=/usr/libexec/s2i",
                    "APP_ROOT=/opt/app-root",
                    "HOME=/opt/app-root/src",
                    "PLATFORM=el9",
                    "NODEJS_VER=20",
                    "PYTHON_VERSION=3.12",
                    "PATH=/opt/app-root/src/.local/bin/:/opt/app-root/src/bin:/opt/app-root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                    "PYTHONUNBUFFERED=1",
                    "PYTHONIOENCODING=UTF-8",
                    "LC_ALL=en_US.UTF-8",
                    "LANG=en_US.UTF-8",
                    "CNB_STACK_ID=com.redhat.stacks.ubi9-python-312",
                    "CNB_USER_ID=1001",
                    "CNB_GROUP_ID=0",
                    "PIP_NO_CACHE_DIR=off",
                    "SUMMARY=Platform for building and running Python 3.12 applications",
                    "DESCRIPTION=Python 3.12 available as container is a base platform for building and running various Python 3.12 applications and frameworks. Python is an easy to learn, powerful programming language. It has efficient high-level data structures and a simple but effective approach to object-oriented programming. Python's elegant syntax and dynamic typing, together with its interpreted nature, make it an ideal language for scripting and rapid application development in many areas on most platforms.",
                    "BASH_ENV=/opt/app-root/bin/activate",
                    "ENV=/opt/app-root/bin/activate",
                    "PROMPT_COMMAND=. /opt/app-root/bin/activate"
               ],
               "Entrypoint": [
                    "container-entrypoint"
               ],
               "Cmd": [
                    "/bin/sh",
                    "-c",
                    "$STI_SCRIPTS_PATH/usage"
               ],
               "WorkingDir": "/opt/app-root/src",
               "Labels": {
                    "architecture": "x86_64",
                    "build-date": "2024-08-28T13:57:37",
                    "com.redhat.component": "python-312-container",
                    "com.redhat.license_terms": "https://www.redhat.com/en/about/red-hat-end-user-license-agreements#UBI",
                    "description": "Python 3.12 available as container is a base platform for building and running various Python 3.12 applications and frameworks. Python is an easy to learn, powerful programming language. It has efficient high-level data structures and a simple but effective approach to object-oriented programming. Python's elegant syntax and dynamic typing, together with its interpreted nature, make it an ideal language for scripting and rapid application development in many areas on most platforms.",
                    "distribution-scope": "public",
                    "io.buildah.version": "1.29.0",
                    "io.buildpacks.stack.id": "com.redhat.stacks.ubi9-python-312",
                    "io.k8s.description": "Python 3.12 available as container is a base platform for building and running various Python 3.12 applications and frameworks. Python is an easy to learn, powerful programming language. It has efficient high-level data structures and a simple but effective approach to object-oriented programming. Python's elegant syntax and dynamic typing, together with its interpreted nature, make it an ideal language for scripting and rapid application development in many areas on most platforms.",
                    "io.k8s.display-name": "Python 3.12",
                    "io.openshift.expose-services": "8080:http",
                    "io.openshift.s2i.scripts-url": "image:///usr/libexec/s2i",
                    "io.openshift.tags": "builder,python,python312,python-312,rh-python312",
                    "io.s2i.scripts-url": "image:///usr/libexec/s2i",
                    "maintainer": "SoftwareCollections.org <sclorg@redhat.com>",
                    "name": "ubi9/python-312",
                    "release": "25",
                    "summary": "Platform for building and running Python 3.12 applications",
                    "url": "https://access.redhat.com/containers/#/registry.access.redhat.com/ubi9/python-312/images/1-25",
                    "usage": "s2i build https://github.com/sclorg/s2i-python-container.git --context-dir=3.12/test/setup-test-app/ ubi9/python-312 python-sample-app",
                    "vcs-ref": "4cd1d8f166d0b901dd5a2659bb128d69c760b5a3",
                    "vcs-type": "git",
                    "vendor": "Red Hat, Inc.",
                    "version": "1"
               }
          },

```

* Container Name: "name": "ubi9/python-312"
* Container Tag: "release": "25"

## Product Identification
Common Platform Enumeration (CPE) is a standardized method of describing and identifying classes of applications, 
operating systems, and hardware devices present among an enterprise's computing assets.

Red Hat uses CPEs to uniquely identify each product and version, following the CPE 2.2 schema. Detailed information about 
Red Hat CPEs can be found [here](https://redhatproductsecurity.github.io/security-data-guidelines/cpe/). 

### RPM Repositories
Each Red Hat published container image published after June 2020 includes content manifest JSON files for each layer included in 
the container image. Inside each content manifest JSON file, you'll find a content sets object, which specifies the 
repository names that provided the packages found in the container image. Scanning vendors should use the repositories 
listed in the content sets object to map the repositories used within the image to the correct CPEs.  

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

### RPM Repository to CPE mapping 
Red Hat maintains a JSON file to map Red Hat RPM repositories to our CPEs. Once you have identified the repositories
used for the product and version by following the previous steps, you search for the repository label and determine
both the set of related CPEs and the list of repository relative URLs. The repository to CPE mapping is located 
[here](https://security.access.redhat.com/data/metrics/repository-to-cpe.json).

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
```

```
# Example of repository to CPE mapping for openshift4/ose-console-rhel9 repositories
"rhel-9-for-x86_64-appstream-eus-rpms__9_DOT_2": {
    "cpes": [
        "cpe:/a:redhat:rhel_eus:9.2::appstream"], 
    "repo_relative_urls": [
        "content/eus/rhel9/9.2/x86_64/appstream/os"]
},
```


## Product and Component Matching in CSAF-VEX 
Red Hat security metadata reports vulnerability information per product and component combination. 

CSAF advisories and VEX data includes information about each potentially affected product and component and the relationships
between the applicable products and components. Vendors must identify both the relevant products and components 
individually and then determine the available product/component combinations in order to report vulnerability information correctly. 

A detailed breakdown of the format and information included in these files can be found
[here](https://redhatproductsecurity.github.io/security-data-guidelines/csaf-vex/).

### Product matching using CPEs in CSAF-VEX
CSAF advisories and VEX data represents products using a `product_name` object. The `product_name` entry will include a 
`production_identification_helper` in the form of a CPE. Vendors should follow the previous steps to determine a list of 
potential CPEs that can be used to match to `product_name` entries. More information about `product_name` objects can be
found [here](https://redhatproductsecurity.github.io/security-data-guidelines/csaf-vex/#product-family-and-product-name-examples)

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

#### CPE Examples

RHEL 9 and Before
```
# Example of MAIN/EUS unfixed CPE for RHEL 9 and before
cpe:/o:redhat:enterprise_linux:9
```

```
# Example of a main stream fixed CPE for RHEL 9 and before
cpe:/a:redhat:enterprise_linux:9::appstream
```

```
# Example of an EUS stream fixed CPE 
cpe:/a:redhat:rhel_eus:9.2::appstream
```

RHEL 10 Examples
```
# Example of MAIN/EUS unfixed CPE for RHEL 10
cpe:/o:redhat:enterprise_linux:10
```

```
# Example of a main stream fixed CPE for RHEL 10
cpe:/o:redhat:enterprise_linux:10.0
```

```
# Example of an EUS stream fixed CPE for RHEL 10 
cpe:/o:redhat:enterprise_linux_eus:10.2 
```

Openshift Examples
```
# Example of an unfixed CPE for Openshift 
cpe:/a:redhat:openshift:4 
```

```
# Example of a fixed CPE for Openshift 
cpe:/a:redhat:openshift:4.16::el9
```

#### CPE Matching Logic
Due to the differences in CPE representation based on fix status, Red Hat recommends vendors attempt to match to CPEs
using only the first 5 segments of the CPE. When available, it is best to use CPEs with a direct match to the repository
information gathered from the container, but this is not always the case.

If the repositories used in a container image are xUS streams, it is also necessary to check for the existence of a main
stream CPEs as well, if the vulnerability is unfixed or did not release a fix to the xUS stream.

<!-- Add example of what CPEs should be matched--> 

### Component matching using purls in CSAF-VEX
CSAF advisories and VEX data represents components using a `product_version` object. The `product_version` entry will 
include a `production_identification_helper` in the form of a purl. Vendors should follow the previous steps to identify 
components and then format the appropriate purls to match to `product_version` entries. More information about 
`product_version` objects can be found [here](https://redhatproductsecurity.github.io/security-data-guidelines/csaf-vex/#unfixed-product-versions-vex-only-examples).

#### Purls in CSAF-VEX
Similarly to CPEs, purls in CSAF advisories and VEX data are represented differently based on fix status.

* Unfixed: Includes the `under_investigation`, `known_affected` and most `known_not_affected` product statuses
  * Component version: All unfixed components, both `rpm` and `oci` purl formats will not include any component versioning
  * Architecture: SRPMs will have the qualifier `arch=src`, but both binary RPMs and container will not include any
    architecture information
* Fixed: Includes all `fixed` product status and the occasional `known_not-affected` product statuses
  * Component version: All fixed components will include versioning in  the `rpm` and `oci` purl formats
  * Architecture: All fixed components will include architecture information in the `rpm` and `oci` purl formats

#### Purl Examples

SRPMS, RPMs and RPM modules are represented in CSAF advisories and VEX data using the `rpm` purl type. More detailed
information about RPM purl usage can be found
[here](https://redhatproductsecurity.github.io/security-data-guidelines/purl/#identifying-rpm-packages).

```
# Example of an unfixed RPM purl 
TODO
```

```
# Example of a fixed RPM purl
TODO
```

```
# Example of an unfixed SRPM purl
TODO
```

```
# Example of a fixed SRPM purl 
TODO
```

```
# Example of an unfixed RPM module purl
TODO
```

```
# Example of a fixed RPM module purl 
TODO
```

Non-rpm content is represented at the container level. Containers are represented with the `oci` purl type. More detailed information about OCI
purl usage can be found [here](https://redhatproductsecurity.github.io/security-data-guidelines/purl/#identifying-container-images).
```
# Example of an unfixed container purl 
TODO
```

```
# Example of a fixed container purl 
TODO
```

#### Purl Matching Logic
As seen above, purls in CSAF advisories and VEX files can be represented differently based on fix status. When attempting
to match a component using purls in these files, Red Hat recommends vendors to matching to against any component entries 
based on component name. 

### Using purls and CPE to find Product IDs 
Vendors should use the previous steps to be able to identify the appropriate `product_name` objects using CPE and `product_version` 
objects using purl. 

In order to determine unique `product_id` combinations for each product/component pair, vendors should use the `relationship`
object. More information about how to determine unique `product_id` combinations using `product_name`, `product_version` and `relationships` can 
be found [here](https://redhatproductsecurity.github.io/security-data-guidelines/csaf-vex/#relationships).


## Determine Vulnerability Information
After following the previous steps, vendors should now have a list of unqiue product/component pairs in the form of 
unique `product_id` combinations. These `product_id` combinations should be used to determine severity, affectedness information and any available security fixes.

### CVE Information
Basic CVE information is represented in the `vulnerabilities` section of CSAF advisories and VEX data:

* `cve`: The official CVE ID
* `cwe`: Information about the corresponding CWE, include the CWE ID and the name 
* `discovery_date`: The first reported date of the vulnerability

```
"vulnerabilities": [
    {
      "cve": "CVE-2022-27943",
      "cwe": {
        "id": "CWE-400",
        "name": "Uncontrolled Resource Consumption"
      },
      "discovery_date": "2022-04-04T00:00:00+00:00",
```


### Affectedness 
Affectedness information is also found in the `vulnerabilities`section of the document. Each product/component `product_id` 
will be listed in the `product_status` category that corresponds to the affectedness of that product/component pair.

CVEs should be reported as follows, based on the `product_status` for the product/component pair.

<!-- https://issues.redhat.com/browse/SECDATA-696 and https://issues.redhat.com/browse/SECDATA-744-->
<!-- TODO: Add text about old CVEs that may not have a product match --> 
<!-- TODO: Add column to table about product information -->

| Product Status        | Component Details                                                                                 | Reporting Information                                                                                                                   |
|-----------------------|---------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| `under_investigation` | No version information available.                                                                                                  | Reported                                                                                                                                | 
| `known_affected`      | No version information available.                                                                                               | Reported                                                                                                                                |
| `known_not_affected`  | No version information available.                                                                 | Not reported                                                                                                                            |
| `fixed`               | The fixed component version is newer than the component version included in the scanned software. | Reported: In this case, the component is vulnerable and should be upgraded. The associated RHSA should also be reported with this CVE.  |
|`fixed` | The fixed component version is older than the component version included in the scanned software. | Not reported: In this case, the component should be considered already fixed and is not vulnerable in the scanned software.             |

For the "red_hat_enterprise_linux_9:gcc" product/component pair, it is listed in the `known_affected` section.

<!-- TODO: Add CVE example with "known_not_affected"  CVE-2024-43790 / vim -->

```
"vulnerabilities": [
    {
        ...
        "product_status": {
            "known_affected": [
                ... , 
                "red_hat_enterprise_linux_9:gcc"
            ],
        }
    }
]
```

### RHSAs 
Remediation information is also available in the `vulnerabilities` section. Each product/component pair is also listed
with `category` and `details` attributes that describe the fix status of that product and component. 

For the "red_hat_enterprise_linux_9:gcc" product/component pair, there is no fix available so you see the `product_id` 
listed in the `none_available` category, with details `fixed_deffered`of the `remediations` object. 

<!-- TODO: Add CVE example with RHSA CVE-2024-2511 / RHSA-2024:9333 -->
<!-- TODO: Add CVE example with OCP RHSA CVE-2024-24791 / RHSA-2024:8260 -->

```
"remediations": [
    ...
    },
    {
        "category": "none_available",
        "details": "Fix deferred",
        "product_ids": [
            ... ,
            "red_hat_enterprise_linux_9:gcc"
        ]
    }
] 
```

### CVSS score and Severity

The last sections in the `vulnerabilities` object to be aware of are the `scores` object and the `threats` object.
Both CVSS scores and Red Hat severities are available when the product/component pair differs from the aggregate CVE severity.
Red Hat recommends that scanning vendors check the per product CVSS scores and severity scores for each vulnerability 
and report the product/component severity instead of the aggregate severity for the CVE, when applicable. 

For the "red_hat_enterprise_linux_9:gcc" product/component pair, the CVSS base score is "5.5" with a vector string of
"CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H".
```
"scores": [
    {
        "cvss_v3": {
            "attackComplexity": "LOW",
            "attackVector": "LOCAL",
            "availabilityImpact": "HIGH",
            "baseScore": 5.5,
            "baseSeverity": "MEDIUM",
            "confidentialityImpact": "NONE",
            "integrityImpact": "NONE",
            "privilegesRequired": "NONE",
            "scope": "UNCHANGED",
            "userInteraction": "REQUIRED",
            "vectorString": "CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H",
            "version": "3.1"
        },
        "products": [
            ... ,
            "red_hat_enterprise_linux_9:gcc",
            "red_hat_virtualization_4:gcc"
        ]
    }
],
```

For the "red_hat_enterprise_linux_9:gcc" product/component pair, the Red Hat severity is "Low". 
```
"threats": [
    {
        "category": "impact",
        "details": "Low",
          "product_ids": [
             ... ,
            "red_hat_enterprise_linux_9:gcc",
            "red_hat_virtualization_4:gcc"
          ]
        }
      ],
```


## Frequently Asked Questions (FAQs)
Vendors are encouraged to raise any questions regarding security data by opening a ticket in the public
[SECDATA Jira project](https://issues.redhat.com/projects/SECDATA/).

Many scanning vendors face similar challenges when reading and parsing Red Hat's security data. To check if your question
has already been asked, you can review the list of questions asked [here](https://issues.redhat.com/browse/SECDATA-862?filter=12444038).

### Python vulnerabilities 
https://issues.redhat.com/browse/SECDATA-831

### Differences in OVAL and VEX CPEs
https://issues.redhat.com/browse/SECDATA-1141 

### Repository relative URLs 
https://issues.redhat.com/browse/SECDATA-1089
https://issues.redhat.com/browse/SECDATA-797
https://issues.redhat.com/browse/SECDATA-1020

### Empty content sets
https://issues.redhat.com/browse/SECDATA-966

### Duplicate RHSAs
https://issues.redhat.com/browse/SECDATA-969

## Additional Questions or Concerns 
Red Hat is committed to continually improving our security data; any future changes to the data itself or the format of 
the files are tracked in the [Red Hat Security Data Changelog](https://access.redhat.com/articles/5554431).

Please contact Red Hat Product Security with any questions regarding security data at [secalert@redhat.com](secalert@redhat.com) or file an 
issue in the public [SECDATA Jira project](https://issues.redhat.com/projects/SECDATA/issues/SECDATA-525?filter=allopenissues).