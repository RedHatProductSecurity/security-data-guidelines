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
The [Common Security Advisory Framework (CSAF)](https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html) 
was originally published as an open standard by OASIS Open in November 2022. CSAF files provide a structured, 
machine-readable way of representing and sharing security advisory information across all software and hardware providers. 
 
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
CSAF machine-readable standard and use the VEX profile to convey security information. The CSAF-VEX standard includes
three main sections: document metadata, a product tree and vulnerability metadata. The full document structure can
be found 
[here](https://github.com/RedHatProductSecurity/security-data-guidelines/blob/csaf-vex-guidelines/docs/csaf-vex.json).

The following sections break down the information included in CSAF/VEX documents using the 
[VEX file for CVE-2023-20593](https://access.redhat.com/security/data/csaf/v2/vex/2022/cve-2023-20593.json) as an example.

### Document Metadata 
The "document" section contains general information about the published document itself including CVE severity, vendor,
published date and revision history.

CVE severity:

```
"aggregate_severity": {
    "namespace": "https://access.redhat.com/security/updates/classification/",
    "text": "moderate"
},
```

VEX metadata: 

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
"id": "CVE-2023-20593",
"initial_release_date": "2023-07-25T06:30:00+00:00",
"revision_history": [
  {
    "date": "2023-07-25T06:30:00+00:00",
    "number": "1",
    "summary": "Initial version"
  },
  {
    "date": "2024-04-18T04:20:20+00:00",
    "number": "2",
    "summary": "Current version"
  },
  {
    "date": "2024-09-13T20:58:30+00:00",
    "number": "3",
    "summary": "Last generated version"
  }
],
"status": "final",
"version": "3"
```

### Product Tree 
The “product_tree” section identifies all affected Red Hat software, represents the nested 
relationship of component to product and provides CPEs or PURLs depending on the affected layer. There are two main 
objects in the “product_tree” object: “branches” and “relationships”.

#### Branches
The parent "branches" object has one child object of the "vendor" category with the name set to "Red Hat". All 
affected Red Hat products and components will be nested in that "branches" array. Compressed down, the parent branches 
object would look like:

```
{
  "branches": [
    {
      "branches": []
      "category": "vendor"
      "name": "Red Hat:
    }
  ]
}
```

All nested objects included in the "branches" object of the "vendor" category fall into the following subcategories:
* "product_family": The "product_family" category represents a general Red Hat product stream and includes one or more 
nested objects of the "product_name".
* "product_name": The "product_name" category represents a specific product release and is always nested under the 
corresponding "product_family"
* "product_version": The "product version" category represents a specific component. When displayed unnested, the 
component is not fixed yet and will not include a specific version number. Note: This will only be present in VEX files
since CSAF files are per advisory and will only include fixed components.
* "architecture": The "architecture" category represents fixed components by their architecture and includes nested 
  "product_version" objects. These "product_version" will be fixed and provide the specific version number. 



##### Product Family and Product Name Examples
The "product_family" category represents a general Red Hat product stream and includes one or 
more nested objects of the "product_name" category that represents an individual release. The "product_name" object will
always include the name of the product, a product ID and a product identification helper in the form of a CPE. 

In the example below, you can see that the "product_family" object is for Red Hat Enterprise Linux 6 and nested within 
is the "product_name" object Red Hat Enterprise Linux 6 with the CPE "cpe:/o:redhat:enterprise_linux:6". 

```
{
  "branches": [
    {
      "category": "product_name",
      "name": "Red Hat Enterprise Linux 6",
      "product": {
        "name": "Red Hat Enterprise Linux 6",
        "product_id": "red_hat_enterprise_linux_6",
        "product_identification_helper": {
          "cpe": "cpe:/o:redhat:enterprise_linux:6"
        }
      }
    }
  ],
"category": "product_family",
"name": "Red Hat Enterprise Linux 6"
},
```

##### Unfixed Product Versions (VEX only) Examples
The "product_version" category includes information about a specific affected package. The "product_version" object will 
always include the name of the component, a product ID and a product identification helper in the form of a PURL. When 
displayed unnested under an "architecture" object, the "name" attribute will not reference a specific version number 
because these components are unfixed. Again, these unfixed "product_version" components will only be found in VEX files 
since CSAF files always represent a released RHSA.

In the example below, the unfixed kernel component's name is "kernel" and doesn't include a specific version number or 
an architecture format.

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

##### Architecture and Fixed Product Versions
Similarly to the "product_family" object, the "architecture" category represents a specific architecture for packages 
and includes one or more "product_version" objects. As before, the "product_version" category will still include the same
information: the name of the component, a product ID and product identification helper in the form of a PURL. However, 
when product_versions are nested under architecture object, they are fixed components and the "name" attribute will 
include a specific version number and the specific architecture format. 

In the example below, you can see the fixed kernel component's name is "kernel-0:3.10.0-693.112.1.el7.src" which includes
the specific version number "0:3.10.0-693.112.1.el7" and architecture format ".src".
```
{ 
  "branches": [
    {
      "category": "product_version",
      "name": "kernel-0:3.10.0-693.112.1.el7.src",
      "product": {
        "name": "kernel-0:3.10.0-693.112.1.el7.src",
        "product_id": "kernel-0:3.10.0-693.112.1.el7.src",
        "product_identification_helper": {
          "purl": "pkg:rpm/redhat/kernel@3.10.0-693.112.1.el7?arch=src"
        }
      }
    }
  ],
  "category": "architecture",
  "name": "src"
}
```

#### Relationships
Also included in the "product_tree" section is a "relationships" object which is used by Red Hat to help represent 
layered products. One or more relationship entries will be present for all "product_version" objects found in the 
"branches" object. All of these objects are of the “default_component_of” category and include the full product 
name and product ID (a combination of the "product_name" and the "product_version"), a reference to the component name 
and a reference to the product name. 

Continuing with the previous examples, we know that there should be at least one entry in the "relationships" object 
that correlates to the "product_version" object for kernel. Looking at the VEX file, there are actually four entries for 
kernel, all which relate to the different "product_name" objects from before. The below is the specific entry as it 
relates to Red Hat Enterprise Linux 6.

Here you can see that the "full_product_name" includes a name and a product ID which are the combination of the product,
Red Hat Enterprise Linux 6, and the component, kernel. The "product_reference" will always refer to the component's name
while the "relates_to_product_reference" will refer to the product name.

```
{
  "category": "default_component_of",
  "full_product_name": {
    "name": "kernel as a component of Red Hat Enterprise Linux 6",
    "product_id": "red_hat_enterprise_linux_6:kernel"
  },
  "product_reference": "kernel",
  "relates_to_product_reference": "red_hat_enterprise_linux_6"
},
```

For the fixed component kernel-0:3.10.0-693.112.1.el7.src, a relationship entry looks like: 
```
{
  "category": "default_component_of",
  "full_product_name": {
    "name": "kernel-0:3.10.0-693.112.1.el7.src as a component of Red Hat Enterprise Linux Server AUS (v. 7.4)",
    "product_id": "7Server-7.4.AUS:kernel-0:3.10.0-693.112.1.el7.src"
  },
  "product_reference": "kernel-0:3.10.0-693.112.1.el7.src",
  "relates_to_product_reference": "7Server-7.4.AUS"
},
```

### Vulnerability Metadata
The "vulnerabilities" section reports vulnerability metadata for any CVEs included in the document and also contains a 
"product_status" object that reports fix status for any "product_id" listed in the "product_tree" and a "remediations" 
object. 

#### CVE Information
CVE ID, CWE and publication date:
```
"cve": "CVE-2023-20593",
      "cwe": {
        "id": "CWE-1239",
        "name": "Improper Zeroization of Hardware Register"
      },
      "discovery_date": "2023-05-31T00:00:00+00:00",
```

CVE description, summary and statement:
```
"notes": [
  {
    "category": "description",
    "text": "A flaw was found in hw, in “Zen 2” CPUs. This issue may allow an attacker to access sensitive information under specific microarchitectural circumstances.",
    "title": "Vulnerability description"
  },
  {
    "category": "summary",
    "text": "hw: amd: Cross-Process Information Leak",
    "title": "Vulnerability summary"
  },
  {
    "category": "general",
    "text": "The CVSS score(s) listed for this vulnerability do not reflect the associated product's status, and are included for informational purposes to better understand the severity of this vulnerability.",
    "title": "CVSS score applicability"
  }
],
```

CVSS score and severity:
```
"scores": [
    {
        "cvss_v3": {
            "attackComplexity": "LOW",
            "attackVector": "LOCAL",
            "availabilityImpact": "NONE",
            "baseScore": 6.5,
            "baseSeverity": "MEDIUM",
            "confidentialityImpact": "HIGH",
            "integrityImpact": "NONE",
            "privilegesRequired": "LOW",
            "scope": "CHANGED",
            "userInteraction": "NONE",
            "vectorString": "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N",
            "version": "3.1"
        },
        "products": []
    }
],
"threats": [
    {
        "category": "impact",
        "details": "Moderate",
        "product_ids": []
    }
],
```
Additional CVE resources:
```
 "references": [
        {
          "category": "self",
          "summary": "Canonical URL",
          "url": "https://access.redhat.com/security/cve/CVE-2023-20593"
        },
        {
          "category": "external",
          "summary": "RHBZ#2217845",
          "url": "https://bugzilla.redhat.com/show_bug.cgi?id=2217845"
        },
        {
          "category": "external",
          "summary": "https://www.cve.org/CVERecord?id=CVE-2023-20593",
          "url": "https://www.cve.org/CVERecord?id=CVE-2023-20593"
        },
        {
          "category": "external",
          "summary": "https://nvd.nist.gov/vuln/detail/CVE-2023-20593",
          "url": "https://nvd.nist.gov/vuln/detail/CVE-2023-20593"
        },
        {
          "category": "external",
          "summary": "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=522b1d69219d8f083173819fde04f994aa051a98",
          "url": "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=522b1d69219d8f083173819fde04f994aa051a98"
        },
        {
          "category": "external",
          "summary": "https://www.amd.com/en/resources/product-security/bulletin/amd-sb-7008.html",
          "url": "https://www.amd.com/en/resources/product-security/bulletin/amd-sb-7008.html"
        }
      ],
```

#### Product Fix Status
The "product_status" includes the following fix statuses:

* "fixed": Contains the same fixed component versions and other details (product_tree objects) that the are reported fixed
for a given CVE
* "known_affected": Confirmation that the specific component and product is affected by a particular CVE
* "known_not_affected": Confirmation that the specific component and product is not affected by a particular CVE
* "under_investigation": Information that the Red Hat Product Security team is verifying the applicability and impact of 
a specific CVE to the specific component and product

Compressed down, a product_status object that included products of each category, would look like:

```
"product_status": {
    "fixed": []
    "known_affected": [],
    "known_not_affected": [],
    "under_investigation": []
},
```
Note: It's important to remember that with VEX files, not every "product_status" will be included, only the categories that 
have products which fall into those statuses. For CSAF files, the only included status will be the "fixed" category.

Continuing with our previous examples with CVE-2023-20593, the full product ID "red_hat_enterprise_linux_6:kernel" 
can be found in the "known_not_affected" list:

```
"known_not_affected": [
  ...,
  "red_hat_enterprise_linux_6:kernel",
  "red_hat_enterprise_linux_6:microcode_ctl"
]
  
```

Our other full product ID "7Server-7.4.AUS:kernel-0:3.10.0-693.112.1.el7.src" can be found in the "fixed" list:
```
"fixed": [
  ...,
  "7Server-7.4.AUS:kernel-0:3.10.0-693.112.1.el7.src",
  "7Server-7.4.AUS:kernel-0:3.10.0-693.112.1.el7.x86_64",
  ...
]
```

#### Remediations 
The "remediations" object provides additional information about the previously identified product status. The following 
remediations status are available per product_status:

* "fixed" product status
  * "vendor_fix": For all the product_IDs found in the “fixed” product_status there will be a corresponding entry
    in the "remediations" object that correlates each full product ID to the correct RHSAs. The RHSA can be determined by
    the “url” field. 
    * Details: "Fixed"
    * URL: Link to the RHSA
  * "workaround": If a mitigation exists, it applies to all components regardless of their fix state.
    * Details: "Mitigation"
* "known_affected": For all the full product IDs found in the "known_affected" product status, there will be additional 
entries in the "remediations" object that fall into the following categories.
  * "no_fix_planned": Will include any product_IDs in the "known_affected" product status that will not be fixed by Red 
  Hat, either because it is out of support scope or the engineering team has decided not to fix it for other reasons.
    * Details: "Will not fix" or "Out of support scope"
  * "none_available": Will include any product_IDs in the "known_affected" product status that are either still reported 
  affected, meaning a fix is likely in progress, or deferred, which may be fixed at a future date. 
    * Details: "Affected" or "Deferred" 
  * "workaround": If a mitigation exists, it applies to all components regardless of their fix state.
    * Details: "Mitigation"
* "known_not_affected": There are no "remediation" objects for the known not affected status since it is implicitly 
assumed that there are no remediations needed if the product and component are not affected.
* "under_investigation": There are no "remediation" objects for the under investigation status since it is implicitly 
assumed that no remediations exist since we are still investigating the vulnerability.

Note: As with the "product_status" object, there may not be an entry for every category. Additionally, in VEX files, 
there may be more than one "vendor_fix" object if more than one RHSA released fixes for the CVE. In the CSAF files, 
the only "remediation" category present will be one "vendor_fix" object that correlates to the RHSA that the CSAF 
file represents.

Following our two previous kernel examples, we can see that for the unfixed kernel component 
"red_hat_enterprise_linux_6:kernel" there is no entry in the remediations section. This is expected behavior because 
it was listed in the "known_not_affected" product status and therefore no remediation is needed.

For our fixed kernel component "7Server-7.4.AUS:kernel-0:3.10.0-693.112.1.el7.src", there are two remediation entries.
One represents the vendor fix that was released and the other represents that there is a reported mitigation for this 
CVE.

```
{
  "category": "vendor_fix",
  "details": "For details on how to apply this update, which includes the changes described in this advisory, refer to:\n\nhttps://access.redhat.com/articles/11258\n\nThe system must be rebooted for this update to take effect.",
  "product_ids": [
    "7Server-7.4.AUS:kernel-0:3.10.0-693.112.1.el7.src",
    "7Server-7.4.AUS:kernel-0:3.10.0-693.112.1.el7.x86_64",
    ...
  ]
}
```

```
{
  "category": "workaround",
  "details": "Mitigation for this issue is either not available or the currently available options don't meet the Red Hat Product Security criteria comprising ease of use and deployment, applicability to widespread installation base or stability.",
  "product_ids": [
    ...,
    "7Server-7.4.AUS:kernel-0:3.10.0-693.112.1.el7.src",
    "7Server-7.4.AUS:kernel-0:3.10.0-693.112.1.el7.x86_64",
    ...
  ]
  
```


## Additional Notes
https://www.redhat.com/en/about/brand/standards/history
https://www.redhat.com/en/blog/20-years-red-hat-product-security-inception-customer-experience
