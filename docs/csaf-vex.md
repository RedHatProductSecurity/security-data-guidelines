# Red Hat CSAF-VEX Advisories

## Red Hat Security Data Overview 
The Red Hat Product Security was originally founded in 2001 and has always been committed to providing our customers 
and partners with complete and accurate security data for all Red Hat software. In the past, Red Hat published security 
advisory information using Common Vulnerability Reporting Framework (CVRF) and CVE information using the Open 
Vulnerability and Assessment Language (OVAL) format. Over the last few years, the Common Security Advisory Framework 
(CSAF) 2.0 standard was published and is now the successor to the CVRF version 1.2 as there are many enhancements to the
information provided in each CSAF file. 

On February 1st, 2023, Red Hat first announced the general availability of CSAF 2.0 documents. This version of our CSAF 
files are published using the VEX profile (Vulnerability Exploitability eXchange) and the document type is now known as 
csaf_vex. Since then Red Hat has continued to make improvements to our published security data, including the GA release
of our VEX files on July 10th, 2024. While publishing our CSAF files was extremely helpful for correlating security data
to individual advisories, we began publishing VEX files to make it easier for our partners and customers to correlate 
both fixed and unfixed security information to an individual CVE. Additionally, the publication of our VEX files
announced the deprecation of our previously published OVAL data, which did not provide the same level of detailed 
security information. 

Currently, Red Hat Product Security publishes CSAF advisories for every single Red Hat security advisory and VEX files 
for every single CVE record that is associated with the Red Hat portfolio in any way.

## Red Hat and CSAF/VEX
### CSAF Overview
The Common Security Advisory Framework (CSAF) was originally published as an open standard by OASIS Open in November 2022.
CSAF files provide a structured, machine-readable way of representing and sharing security advisory information 
across all software and hardware providers. 
 
Red Hat's CSAF files are always associated with one specific advisory and a given advisory may include one or more product 
version(s) and one or more components, depending on the product type and update scope. The advisory itself can also 
include updates to address one or more vulnerabilities. Red Hat’s CSAF files are publicly available per advisory 
[here](https://access.redhat.com/security/data/csaf/v2/advisories).

### VEX Overview
The CSAF standard acknowledges the need for different use cases and has therefore defined a variety of profiles. 
Each profile describes the necessary fields and information needed for that specific use case. Red Hat has adopted the 
Vulnerability Exploitability eXchange (VEX) profile, which is intended to provide the affected state of a vulnerability
on a product or component. 

Red Hat's VEX files are always associated with one CVE and include fix status information for all vulnerable packages
and Red Hat products. Red Hat’s VEX files are publicly available per CVE 
[here](https://access.redhat.com/security/data/csaf/v2/vex/).

## Document Structure
Although CSAF and VEX files ultimately serve different purposes, both CSAF and VEX files meet the 
CSAF machine readable standard and use the VEX profile to convey security information. The CSAF-VEX standard includes
three main sections: document metadata, a product tree and vulnerability metadata. The full document structure can
be found 
[here](https://github.com/RedHatProductSecurity/security-data-guidelines/blob/csaf-vex-guidelines/docs/csaf-vex.json).

The next sections break down each section of the document using the 
[VEX file for CVE-2022-1247](https://access.redhat.com/security/data/csaf/v2/vex/2022/cve-2022-1247.json).

### Document Metadata 
The "document" section contains general information about the published document itself including CVE severity, vendor,
published date and revision history. 

General CVE Severity:

```
"aggregate_severity": {
    "namespace": "https://access.redhat.com/security/updates/classification/",
    "text": "moderate"
},
```

VEX Metadata: 

```
"category": "csaf_vex",
"csaf_version": "2.0",
"distribution": {
    "text": "Copyright © Red Hat, Inc. All rights reserved.",
    "tlp": {
        "label": "WHITE",
        "url": "https://www.first.org/tlp/"
    }
},
"lang": "en",
"notes": [
    {
        "category": "legal_disclaimer",
        "text": "This content is licensed under the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/). If you distribute this content, or a modified version of it, you must provide attribution to Red Hat Inc. and provide a link to the original.",
        "title": "Terms of Use"
    }
],
```

Vendor information:
```
"publisher": {
    "category": "vendor",
    "contact_details": "https://access.redhat.com/security/team/contact/",
    "issuing_authority": "Red Hat Product Security is responsible for vulnerability handling across all Red Hat offerings.",
    "name": "Red Hat Product Security",
    "namespace": "https://www.redhat.com"
},
```

CVE ID, CVE publish date and CVE revision history:

```
"id": "CVE-2022-1247",
"initial_release_date": "2022-05-11T09:37:00+00:00",
"revision_history": [
    {
        "date": "2022-05-11T09:37:00+00:00",
        "number": "1",
        "summary": "Initial version"
    },
    {
        "date": "2023-09-19T14:13:41+00:00",
        "number": "2",
        "summary": "Current version"
    },
    {
        "date": "2024-08-20T07:48:38+00:00",
        "number": "3",
        "summary": "Last generated version"
    }
],
"status": "final",
"version": "3"
```

### Product Tree 
The “product_tree” section identifies all affected Red Hat software, represents the nested 
relationship of component to product and  provides CPEs or PURLs depending on the affected layer. There are two main 
objects in the “product_tree” object; “branches” and “relationships”.

#### Branches

The parent "branches" object includes nested objects of three subcategories: "product_family", "product_name" and 
"product_version". The "product_family" category represents a general Red Hat product stream and 
includes one or more nested objects with the "product_name" category that represent an individual release. The 
"product_name" object will always include the name of the product, a product ID and a product identification helper in 
the form of a CPE. 

In the example below, you can see that the "product_family" object is for Red Hat Enterprise Linux 9 and nested within 
is the "product_name" object Red Hat Enterprise Linux 9. 

```
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

The "product_version" category includes information about a specific affected package. The "product_name" object will 
always include the name of the component, a product ID and a product identification helper in the form of a PURL. The 
example below represents the affected component kernel. 

```
{
    "category": "product_version",
    "name": "kernel",
    "product": {
        "name": "kernel",
        "product_id": "kernel",
        "product_identification_helper": {
            "purl": "pkg:rpm/redhat/kernel?arch=src"
        }
    }
},
```

#### Relationships
Also included in the "product_tree" section is a "relationships" object which is used by Red Hat to help represent 
layered products. One or more relationship entries will be present for all "product_version" objects found in the 
"branches" object. All of these nested objects are of the “default_component_of” category and include the full product 
name and product id (a combination of the "product_name" and the "product_version"), a reference to the component name 
and a reference to the product name. 

Continuing with the previous examples, we know that there should be at least one entry in the "relationships" object 
that correlates to the "product_version" object for kernel. Looking at the VEX file, there are actually four entries for 
kernel, all which relate to the different "product_name" objects from before. The below is the specific entry as it 
relates to Red Hat Enterprise Linux 9.

Here you can see that the "full_product_name" includes a name and a product_id which are the combination of the product,
Red Hat Enterprise Linux 9, and the component, kernel. The "product_reference" will always refer to the component's name
while the "relates_to_product_reference" will refer to the product name.

```
{
"category": "default_component_of",
"full_product_name": {
        "name": "kernel as a component of Red Hat Enterprise Linux 9",
        "product_id": "red_hat_enterprise_linux_9:kernel"
    },
    "product_reference": "kernel",
    "relates_to_product_reference": "red_hat_enterprise_linux_9"
},
```


### Vulnerability Metadata 

The "vulnerabilities" section reports vulnerability metadata for any CVEs included in the document and also contains a 
"product_status" object that reports fix status for any "product_id" listed in the "product_tree". 

CVE ID, CWE and Publication Date:
```
"cve": "CVE-2022-1247",
      "cwe": {
        "id": "CWE-366",
        "name": "Race Condition within a Thread"
      },
      "discovery_date": "2022-03-22T00:00:00+00:00",
```

CVE Description, Summary and Statement:
```
"notes": [
    {
        "category": "description",
        "text": "An issue found in linux-kernel that leads to a race condition in rose_connect(). The rose driver uses rose_neigh->use to represent how many objects are using the rose_neigh. When a user wants to delete a rose_route via rose_ioctl(), the rose driver calls rose_del_node() and removes neighbours only if their “count” and “use” are zero.",
        "title": "Vulnerability description"
    },
    {
        "category": "summary",
        "text": "kernel: A race condition bug in rose_connect()",
        "title": "Vulnerability summary"
    },
    {
        "category": "other",
        "text": "There was no shipped kernel version that was seen affected by this problem. These files are not built in our source code.",
        "title": "Statement"
    },
    {
        "category": "general",
        "text": "The CVSS score(s) listed for this vulnerability do not reflect the associated product's status, and are included for informational purposes to better understand the severity of this vulnerability.",
        "title": "CVSS score applicability"
    }
],
```

CVSS Score and Severity:
```
"scores": [
    {
        "cvss_v3": {
            "attackComplexity": "LOW",
            "attackVector": "LOCAL",
            "availabilityImpact": "HIGH",
            "baseScore": 7.8,
            "baseSeverity": "HIGH",
            "confidentialityImpact": "HIGH",
            "integrityImpact": "HIGH",
            "privilegesRequired": "LOW",
            "scope": "UNCHANGED",
            "userInteraction": "NONE",
            "vectorString": "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H",
            "version": "3.1"
        },
        "products": [
            "red_hat_enterprise_linux_9:kernel",
            "red_hat_enterprise_linux_9:kernel-rt"
        ]
    }
],
"threats": [
    {
        "category": "impact",
        "details": "Moderate",
        "product_ids": [
            "red_hat_enterprise_linux_9:kernel",
            "red_hat_enterprise_linux_9:kernel-rt"
        ]
    }
],
```

The "product_status" includes the following fix statuses:

* Fixed: Contains the same fixed component versions and other details (product_tree objects) that the CSAF advisory 
reports for that CVE
* Known Affected: Confirmation that the specific component and product is affected by a particular CVE
* Known Not Affected: Confirmation that the specific component and product is not affected by a particular CVE
* Under Investigation: Information that the Red Hat Product Security team is verifying the applicability and impact of 
a specific CVE to the specific component and product

```
"product_status": {
    "known_affected": [
        "red_hat_enterprise_linux_9:kernel",
        "red_hat_enterprise_linux_9:kernel-rt"
    ],
    "known_not_affected": [
        "red_hat_enterprise_linux_6:kernel",
        "red_hat_enterprise_linux_7:kernel",
        "red_hat_enterprise_linux_7:kernel-rt",
        "red_hat_enterprise_linux_8:kernel",
        "red_hat_enterprise_linux_8:kernel-rt"
    ]
},
```
For all the product_ids found in the “Fixed” array, these will also be listed in the “remediations” 
array, which correlates each product_id to the correct RHSAs. The RHSA can be determined by the “url” field in the same 
remediation object.


Additional CVE Resources:
```
"references": [
    {
        "category": "self",
        "summary": "Canonical URL",
        "url": "https://access.redhat.com/security/cve/CVE-2022-1247"
    },
    {
        "category": "external",
        "summary": "RHBZ#2066799",
        "url": "https://bugzilla.redhat.com/show_bug.cgi?id=2066799"
    },
    {
        "category": "external",
        "summary": "https://www.cve.org/CVERecord?id=CVE-2022-1247",
        "url": "https://www.cve.org/CVERecord?id=CVE-2022-1247"
    },
    {
        "category": "external",
        "summary": "https://nvd.nist.gov/vuln/detail/CVE-2022-1247",
        "url": "https://nvd.nist.gov/vuln/detail/CVE-2022-1247"
    }
],
```


## Additional Notes
https://www.redhat.com/en/about/brand/standards/history
https://www.redhat.com/en/blog/20-years-red-hat-product-security-inception-customer-experience
