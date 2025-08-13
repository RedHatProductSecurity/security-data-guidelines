# Technical Guidance for Vulnerability Scanning Vendors

## Certification Overview 
The Red Hat Vulnerability Scanner Certification is a collaboration with security partners to deliver more accurate and 
reliable container vulnerability scanning results of Red Hat products and packages. Security partners can now consume 
and leverage Red Hat’s extensive and evolving set of published security data to minimize customer false positives and 
other discrepancies.

For more detailed information on the program please see the [Partner Guide for Red Hat Vulnerability Scanner Certification](https://redhat-connect.gitbook.io/partner-guide-red-hat-vulnerability-scanner-cert)

The following sections in this article will cover the basic principles for how scanning vendors should use Red Hat security 
data to accurately report on vulnerabilities, specifically for Red Hat containers images. 

The examples used in this article will be for the following images: 

[Repository: registry.redhat.io/rhel9/python-312 Tag: 1-25](https://catalog.redhat.com/software/containers/rhel9/python-312/657b088123df896ebfacf1f0?q=python&container-tabs=overview&image=66cf3054a2c0cf86bc022be9) 
[Repository: registry.redhat.io/openshift4/ose-console-rhel9 Tag: v4.16.0-202409181705.p0.g0b1616c.assembly.stream.el9](https://catalog.redhat.com/software/containers/openshift4/ose-console-rhel9/65280984f0f695f11b13a24e?image=66eb1a1cdf6256d9be4690e6&architecture=amd64)

## Package Identification and purls
In order to accurately report on vulnerabilities in Red Hat products, scanning vendors must properly identify the 
Red Hat package versions for RPMs, RPM modules and container first content, to identify any backported fixes. The
following section provides guidance on how to find information about packages and how they are reported in Red Hat's 
CSAF advisories and VEX  content. 

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

Additionally, SRPMs can be discovered from a binary RPM by using the following command: 
 ```
# Example return of SRPM query
$ rpm -q --qf "%{SOURCERPM}\n" libgcc-11.3.1-4.3.el9.x86_64    
   
gcc-11.3.1-4.3.el9.src.rpm
 ```
SRPMS, RPMs and RPM modules are represented in CSAF advisories and VEX data using the `rpm` purl type. 

```
# Example of a RPM purl
pkg:rpm/redhat/libgcc-11.3.1-4.3.el9?arch=x86_64

# Example of a SRPM purl 
pkg:rpm/redhat/gcc?arch=src
```

More detailed information about RPM purl usage can be found [here](https://redhatproductsecurity.github.io/security-data-guidelines/purl/#identifying-rpm-packages).

### Container metadata and container first content 
Container images frequently include non-RPM packages, often referred to as container first content. Non-RPM packages 
that are present found in a container image will be reported on the container itself instead of the package name. Containers 
will use the `oci` purl type. 

```
# Example of a container purl 
pkg:oci/ose-console-rhel9?repository_url=registry.redhat.io/openshift4/ose-console-rhel9

```
More detailed information about OCI purl usage can be found [here](https://redhatproductsecurity.github.io/security-data-guidelines/purl/#identifying-container-images).

### Purl differences based on fix status
Although both RPM, RPM modules and containers are represented in CSAF advisories and VEX data using standard purls, 
there are a few differences in their representation depending on the fix status. 

* Unfixed: Includes the `under_investigation`, `known_affected` and `known_not_affected` product statuses
  * Component version: All unfixed components, both `rpm` and `oci` purl formats will not include any component versioning
  * Architecture: SRPMs will have the qualifier `arch=src`, but both binary RPMs and container will not include any
architecture information
* Fixed: Includes the `fixed` product status 
  * Component version: All fixed components will include versioning in  the `rpm` and `oci` purl formats 
  * Architecture: All fixed components will include architecture information in the `rpm` and `oci` purl formats

## Determining CPEs 
Common Platform Enumeration (CPE) is a standardized method of describing and identifying classes of applications, 
operating systems, and hardware devices present among an enterprise's computing assets.

Red Hat uses CPEs to uniquely identify each product and version, following the CPE 2.2 schema. Detailed information about 
Red Hat CPEs can be found [here]. 

### RPM Repositories
Each Red Hat published container image published after June 2020 includes content manifest JSON files for each layer included in 
the container image. Inside each content manifest JSON file, you'll find a content sets object, which specifies the 
repository names that provided the packages found in the container image. Scanning vendors should use the repositories 
listed in the content sets object to map to the correct CPEs.  

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

### Openshift CPEs 
<!-- TODO: Add information on how to determine CPEs for container first content --> 

## Using CSAF-VEX
Red Hat current publishes security data following the the CSAF standard. Red Hat Product Security currently publishes 
[CSAF advisories](https://security.access.redhat.com/data/csaf/v2/advisories/) for every single Red Hat Security Advisory 
(RHSA) and [VEX files](https://security.access.redhat.com/data/csaf/v2/vex/) for every single CVE record that is associated 
with the Red Hat portfolio in any way.

A detailed breakdown of the format and information included in these files can be found
[here](https://redhatproductsecurity.github.io/security-data-guidelines/csaf-vex/).

For the following examples in this section, we will be taking a look how [CVE-2022-27943](https://security.access.redhat.com/data/csaf/v2/vex/2022/cve-2022-27943.json) 
affects the gcc component in the rhel9/python-312:1-25 container image.

### Using purls and CPE to find Product IDs 
CSAF advisories and VEX data includes information about products, packages and the relationships between products and packages. 
A `product_name` entry will represent a product and include a `production_identification_helper` in the form of a CPE.
For any relevant components, a `product_version`entry will be present and include a `product_ifentification_helper` in the
form a purl. Vendors should use the previous steps to be able to identify the appropriate `product_name` and `product_version` 
entries. 

For each valid combination of `product_name` and `product_version` there will also be a dedicated `default_component_of` 
entry in the `relationships` section of the file. The `default_component_of` object will reference the `product_id` of 
each `product_name` and `product` version entry, while providing a new `product_id` that represents a unique combination
of a product (CPE) and component (purl). Once identified, this `product_id` should be used to find severity, affectedness 
information and any available security fixes.

The following example shows what a `product_name` entry would look like for Red Hat Enterprise Linux 9. The `product_id` 
for this entry is "red_hat_enterprise_linux_9". 

```
# Example of product_name with product CPE
{
    "branches": [
        {
            "category": "product_name",
            "name": "Red Hat Enterprise Linux 9",
            "product": {
                "name": "Red Hat Enterprise Linux 9",
                "product_id": "red_hat_enterprise_linux_9",
                "product_identification_helper": {
                    "cpe": "cpe:/o:redhat:enterprise_linux:9"
                }
            }
        }
    ],
    "category": "product_family",
    "name": "Red Hat Enterprise Linux 9"
},
```

The following example shows what a `product_version` entry looks like for the gcc SRPM. The `product_id` for this entry 
is "gcc". 

```
# Example of product_version with component purl
{
    "branches": [
    ... },
        {
            "category": "product_version",
            "name": "gcc",
            "product": {
                "name": "gcc",
                "product_id": "gcc",
                "product_identification_helper": {
                    "purl": "pkg:rpm/redhat/gcc?arch=src"
                }
            }
        }
    ],
    "category": "vendor",
    "name": "Red Hat"
},
```

Using the previously identified `product_id` from `product_name` and `product_version` entries, we are able to map to
the following relationship entry. The `product_id` of the `product_name` will be refenced in the `relates_to_product_reference` 
attribute and the `product_id` of the `product_version` will be found in the `product_reference` attribute. 

The following is an example of what a relationship entry would like for the product "Red Hat Enterprise Linux 9" and 
the component "gcc". The `product_id` for the combination of the product and component is "red_hat_enterprise_linux_9:gcc".

```
# Example of default_component_of relationship 

"relationships": [
    {
        "category": "default_component_of",
        "full_product_name": {
            "name": "gcc as a component of Red Hat Enterprise Linux 9",
            "product_id": "red_hat_enterprise_linux_9:gcc"
        },
        "product_reference": "gcc",
        "relates_to_product_reference": "red_hat_enterprise_linux_9"
    },
  ]
},
```

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
After following the previous steps, scanning vendors can use the full product/component `product_id`
"red_hat_enterprise_linux_9:gcc", to determine affectedness information about the product and 
component in the `vulnerabilities`section of the document. Each product/component `product_id ` will be listed in the 
`product_status` category that corresponds to the affectedness of that product/component pair.

CVEs should be reported as follows, based on the `product_status` for the product/component pair.

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

<!-- TODO: Add CVE example with different severities per product pair CVE-2024-1485 -->
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

### Repository relative URLs 
https://issues.redhat.com/browse/SECDATA-1089
https://issues.redhat.com/browse/SECDATA-797
https://issues.redhat.com/browse/SECDATA-1020

###  Empty content sets
https://issues.redhat.com/browse/SECDATA-966

### Duplicate RHSAs
https://issues.redhat.com/browse/SECDATA-969




## Additional Questions or Concerns 
Red Hat is committed to continually improving our security data; any future changes to the data itself or the format of 
the files are tracked in the [Red Hat Security Data Changelog](https://access.redhat.com/articles/5554431).

Please contact Red Hat Product Security with any questions regarding security data at [secalert@redhat.com](secalert@redhat.com) or file an 
issue in the public [SECDATA Jira project](https://issues.redhat.com/projects/SECDATA/issues/SECDATA-525?filter=allopenissues).