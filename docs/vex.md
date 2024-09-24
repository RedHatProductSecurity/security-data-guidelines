# Red Hat VEX Files

## VEX Overview
The CSAF standard acknowledges the need for different use cases and has therefore defined a variety of profiles. 
Each profile describes the necessary fields and information needed for that specific use case. Red Hat has adopted the 
Vulnerability Exploitability eXchange (VEX) profile, which is intended to provide the affected state of a vulnerability
on a product or component. 

Red Hat's VEX files are always associated with one CVE and include fix status information for all vulnerable packages
and Red Hat products. Red Hat’s VEX files are publicly available per CVE 
[here](security.access.redhat.com/data).

## Document Structure
The CSAF standard VEX profile requires three main sections: document metadata, a product tree and vulnerability metadata. 
The full document structure, without values, can be found 
[here](https://github.com/RedHatProductSecurity/security-data-guidelines/blob/csaf-vex-guidelines/docs/csaf-vex.json).

The following sections break down the information included in VEX documents using the 
[VEX file for CVE-2023-20593](https://access.redhat.com/security/data/csaf/v2/vex/2023/cve-2023-20593.json) as an example.

### Document Metadata 
The `document` section contains general information about the published document itself including the CVE severity, vendor,
published date and revision history.

The `aggregate_severity.text` object displays the general CVE severity:

```
"aggregate_severity": {
    "namespace": "https://access.redhat.com/security/updates/classification/",
    "text": "moderate"
},
```

The following objects provide general information about the VEX file itself: 

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

Vendor information is represented in the `publisher` object:
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
* `id`: Provides the official CVE ID.
* `initial_release_date`: Represents the date that the Red Hat first published information on the CVE.
* `revision_history`: Details any changes made to the CVE information published by Red Hat.

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
The `product_tree` section identifies all affected Red Hat software, represents the nested 
relationship of component to product and provides CPEs or PURLs depending on the affected layer. There are two main 
objects in the `product_tree` object: `branches` and `relationships`.

#### Branches
The parent `branches` object has one child object of the `vendor` category with the name set to "Red Hat". All 
affected Red Hat products and components will be nested in that `branches` array. Compressed down, the parent branches 
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

All nested objects included in the `branches` object of the `vendor` category fall into the following subcategories:
* `product_family`: Represents a general Red Hat product stream and includes one or more 
nested objects of the `product_name` category.
* `product_name`: Represents a specific product release and is always nested under the 
corresponding `product_family` category.
* `product_version`: Represents a specific component. When displayed unnested, the 
component is not fixed yet and will not include a specific version number.
* `architecture`: Represents fixed components by their architecture and includes nested 
  `product_version` objects. These `product_version` objects will be fixed and provide the specific version number. 



##### Product Family and Product Name Examples
The `product_family` category represents a general Red Hat product stream and includes one or 
more nested objects of the `product_name` category that represents an individual release. The `product_name` object will
always include the name of the product, a product ID and a product identification helper in the form of a CPE. 

In the example below, you can see that the `product_family` object is for Red Hat Enterprise Linux 6 and nested within 
is the `product_name` object Red Hat Enterprise Linux 6 with the CPE "cpe:/o:redhat:enterprise_linux:6". 

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
The `product_version` category includes information about a specific affected package. The `product_version` object will 
always include the name of the component, a product ID and a product identification helper in the form of a 
[PURL](https://redhatproductsecurity.github.io/security-data-guidelines/purl/). When 
displayed unnested under an `architecture` object, the `name` attribute will not reference a specific version number 
because these components are unfixed.

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
Similarly to the `product_family` object, the `architecture` category represents a specific architecture for packages 
and includes one or more `product_version` objects. As before, the `product_version` category will still include the same
information: the name of the component, a product ID and product identification helper in the form of a 
[PURL](https://redhatproductsecurity.github.io/security-data-guidelines/purl/). However, 
when `product_versions` are nested under `architecture` object, they are fixed components and the `name` attribute will 
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
Also included in the `product_tree` section is a `relationships` object which is used by Red Hat to help represent 
layered products. One or more relationship entries will be present for all `product_version` objects found in the 
`branches` object. All of these objects are of the `default_component_of` category and include the full product 
name and product ID (a combination of the `product_name` and the `product_version`), a reference to the component name 
and a reference to the product name. 

Continuing with the previous examples, we know that there should be at least one entry in the `relationships` object 
that correlates to the `product_version` object for kernel. Looking at the VEX file, there are actually four entries for 
kernel, all which relate to the different `product_name` objects from before. The below is the specific entry as it 
relates to Red Hat Enterprise Linux 6.

Here you can see that the `full_product_name` includes a `name` and a `product_id` which are the combination of the product,
Red Hat Enterprise Linux 6, and the component, kernel. The `product_reference` will always refer to the component's name
while the `relates_to_product_reference` will refer to the product name.

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
The `vulnerabilities` section reports vulnerability metadata for the CVE and also contains a 
`product_status` object that reports affected status and fix information for any `product_id` listed in the `product_tree` and a `remediations` 
object. 

#### General CVE Information
Basic CVE information is represented using the following objects:
* `cve`: The official CVE ID. 
* `cwe`: Information about the corresponding CWE, include the CWE ID and the name. 
* `discovery_date`: The first reported date of the vulnerability. Note: This date can differ from the previously 
mentioned `initial_release_date` if the CVE was coordinated under embargo.
```
"cve": "CVE-2023-20593",
"cwe": {
  "id": "CWE-1239",
  "name": "Improper Zeroization of Hardware Register"
},
"discovery_date": "2023-05-31T00:00:00+00:00",
```

Additional CVE information can be found in the `notes` object:
* `description`: This category includes a written description of the CVE.
* `summary`: This category includes a short summary of the CVE.
* `statement`: This category includes a statement from Red Hat on the CVE, when applicable (not present in the example).
* `general`: This category includes a general statement on the applicability of CVSS scores. 
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

A CVE can have a single CVSS score that is  associated to all products and components in the VEX file or there can 
be different CVSS score metrics for different subset of products and components (per component Severity and CVSS metadata)

All CVSS scores associated with the CVE will have entries included `scores` object:
* `cvss_v3`: Includes attributes for each CVSS base value, the complete CVSS vector string and the version of CVSS that 
is used.
* `products`: Includes all product IDs, both for products and components, that are represented by the scores in the 
`cvss_v3` object.
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
```

Similarly to CVSS scores, a CVE can have one severity impact value that represents all products and components in the
VEX file or there can be different severity impact values for different subset of products and components 
(per component Severity and CVSS metadata). 

All severity impact values with the CVE will have entires includes in the `threats` object:
* `category`: The "impact" value identifies that the following information is the severity impact value of a CVE.
* `details`: Reports the appropriate [Red Hat Severity Rating](https://access.redhat.com/security/updates/classification/) 
for the associated `product_ids`. 
* `product_ids`: Includes all product IDs, both for products and components, that have the severity rating in the 
`details` object. 
```
"threats": [
    {
        "category": "impact",
        "details": "Moderate",
        "product_ids": []
    }
],
```

Additional CVE resources are described in the `references` object:
* `category`: Either of the type "self" or "external".
* `summary`: A summary of the provided resource.
* `url`: A link to the resource.
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
The `product_status` object includes the following fix statuses:

* `fixed`: Contains the same fixed component versions and other details (product_tree objects) that the are reported fixed
for a given CVE.
* `known_affected`: Confirmation that the specific component and product is affected by a particular CVE.
* `known_not_affected`: Confirmation that the specific component and product is not affected by a particular CVE.
* `under_investigation`: Information that the Red Hat Product Security team is verifying the applicability and impact of 
a specific CVE to the specific component and product.

Compressed down, a `product_status` object that included products of each category, would look like:

```
"product_status": {
    "fixed": []
    "known_affected": [],
    "known_not_affected": [],
    "under_investigation": []
},
```
Although, not every VEX file will include every product status, only the categories that have products and components 
which fall into those statuses. 

Continuing with our previous examples with CVE-2023-20593, the full product ID "red_hat_enterprise_linux_6:kernel" 
can be found in the `known_not_affected` list:

```
"known_not_affected": [
  ...,
  "red_hat_enterprise_linux_6:kernel",
  "red_hat_enterprise_linux_6:microcode_ctl"
]
  
```

Our other full product ID "7Server-7.4.AUS:kernel-0:3.10.0-693.112.1.el7.src" can be found in the `fixed` list:
```
"fixed": [
  ...,
  "7Server-7.4.AUS:kernel-0:3.10.0-693.112.1.el7.src",
  "7Server-7.4.AUS:kernel-0:3.10.0-693.112.1.el7.x86_64",
  ...
]
```

#### Remediations 
The `remediations` object provides additional information about the previously identified product status. The following 
remediation statuses are available per `product_status` category:

* `fixed`
  * `vendor_fix`: For all the product IDs with a fixed product status there will be a corresponding entry
    in the remediations object that correlates each full product ID to the correct RHSAs. The RHSA can be determined by
    the `url` field. 
    * `Details`: "Fixed".
    * `URL`: A link to the RHSA that released the fix.
  * `workaround`: If a mitigation exists, it applies to all components regardless of their fix state.
    * `Details`: "Mitigation"
* `known_affected`
  * `no_fix_planned`: Will include any product IDs with the known affected product status that will not be fixed by Red 
  Hat, either because it is out of support scope or the engineering team has decided not to fix it for other reasons.
    * `Details`: "Will not fix" or "Out of support scope".
  * `none_available`: Will include any product IDs with the known affected product status that are either still reported 
  affected, meaning a fix is likely in progress, or deferred, which may be fixed at a future date. 
    * `Details`: "Affected" or "Deferred". 
  * `workaround`: If a mitigation exists, it applies to all components regardless of their fix state.
    * `Details`: "Mitigation".
* `known_not_affected`: There are no remediation objects for the known not affected status since it is implicitly 
assumed that there are no remediations needed if the product and component are not affected.
* `under_investigation`: There are no remediation objects for the under investigation status since it is implicitly 
assumed that no remediations exist since we are still investigating the vulnerability.

As with the `product_status` object, there may not be a `remediations` entry for every category. Additionally, 
in VEX files, there may be more than one `vendor_fix` object if more than one RHSA released fixes for the CVE.

Following our two previous kernel examples, we can see that for the unfixed kernel component 
"red_hat_enterprise_linux_6:kernel" there is no entry in the remediation section. This is expected behavior because 
it was listed in the `known_not_affected` product status and therefore no remediation is needed.

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
