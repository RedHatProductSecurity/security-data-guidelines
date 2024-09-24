# Red Hat CSAF Files

## CSAF Overview
The [Common Security Advisory Framework (CSAF)](https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html) 
was originally published as an open standard by OASIS Open in November 2022. CSAF files provide a structured, 
machine-readable way of representing and sharing security advisory information across all software and hardware providers. 
 
Red Hat's CSAF files are always associated with RHSA and a given security advisory may include one or more product 
version(s) and one or more components, depending on the product type and update scope. The RHSA itself can also 
include updates to address one or more vulnerabilities. Red Hat’s CSAF files are publicly available per RHSA 
[here](security.access.redhat.com/data).

## Document Structure
The CSAF standard requires three main sections: document metadata, a product tree and vulnerability metadata.
The full document structure, without values, can be found
[here](https://github.com/RedHatProductSecurity/security-data-guidelines/blob/csaf-vex-guidelines/docs/csaf.json).

The following sections break down the information included in VEX documents using the
[RHSA]() as an example.

### Document Metadata 
The `document` section contains general information about the published document itself including CVE severity, vendor,
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

```
```

### Product Tree 
The `product_tree` section identifies all fixed Red Hat software, represents the nested 
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
* `architecture`: Represents fixed components by their architecture and includes nested 
  `product_version` category.  
* `product_version`: Represents a specific component and version number and is always nested under the corresponding
`architecture` category.



##### Product Family and Product Name Examples
The `product_family` category represents a general Red Hat product stream and includes one or 
more nested objects of the `product_name` category that represents an individual release. The `product_name` object will
always include the name of the product, a product ID and a product identification helper in the form of a CPE. 

In the example below, you can see that the `product_family` object is for ___ and nested within 
is the `product_name` object ___ with the CPE "". 

```
```

##### Architecture and Fixed Product Versions
Similarly to the `product_family` object, the `architecture` category represents a specific architecture for packages 
and includes one or more `product_version` objects. The `product_version` category includes the name of the component, 
a product ID and product identification helper in the form of a 
[PURL](https://redhatproductsecurity.github.io/security-data-guidelines/purl/). The `name` attribute will 
include the fixed version number and the specific architecture format. 

In the example below, you can see the fixed ___ component's name is "___" which includes
the version number "___" and architecture format "___".
```
```

#### Relationships
Also included in the `product_tree` section is a `relationships` object which is used by Red Hat to help represent 
layered products. One or more relationship entries will be present for all `product_version` objects found in the 
`branches` object. All of these objects are of the `default_component_of` category and include the full product 
name and product ID (a combination of the `product_name` and the `product_version`), a reference to the component name 
and a reference to the product name. 

Continuing with the previous examples, we know that there should be at least one entry in the `relationships` object 
that correlates to the `product_version` object for ___. 

Here you can see that the `full_product_name` includes a `name` and a `product_id` which are the combination of the product,
___, and the component, ___. The `product_reference` will always refer to the component's name
while the `relates_to_product_reference` will refer to the product name.

```
{
  "category": "default_component_of",
  "full_product_name": {
    "name": "",
    "product_id": ""
  },
  "product_reference": "",
  "relates_to_product_reference": ""
},
```

### Vulnerability Metadata
The `vulnerabilities` section reports vulnerability metadata for any CVEs included in the RHSA and also contains a 
`product_status` object that lists all the fixed `product_id` listed in the `product_tree` and a `remediations` 
object. 

#### General CVE Information
As previously mentioned, one RHSA can release a fix for multiple CVEs. Each CVE included in the CSAF file will be 
represented ___.


Basic CVE information is represented using the following objects:
* `cve`: The official CVE ID 
* `cwe`: Information about the corresponding CWE, include the CWE ID and the name 
* `discovery_date`: The first reported date of the vulnerability. Note: This date can differ from the previously 
mentioned `initial_release_date` if the CVE was coordinated under embargo
```
```

Additional CVE information can be found in the `notes` object:
* `description`: This category includes a written description of the CVE
* `summary`: This category includes a short summary of the CVE
* `statement`: This category includes a statement from Red Hat on the CVE, when applicable (Not present in the example)
* `general`: This category includes a general statement on the applicability of CVSS scores 
```
"notes": [
],
```

A single CVE can are provided per CVE using the `scores` object:
* `cvss_v3`: Includes attributes for each CVSS base value, the complete vector string and the version of CVSS used
* `products`: 

```
"scores": [
],
```

```
"threats": [
    {
        "category": "impact",
        "details": "",
        "product_ids": []
    }
],
```

Additional CVE resources are described in the `references` object:
* `category`: Either of the type "self" when references to the CVE link 
```
 "references": [
 ]
```

#### Product Fix Status
The `product_status` object only includes the following fix statuses in a CSAF file:

* `fixed`: Contains the same fixed component versions and other details (product_tree objects) that the are reported fixed
by the RHSA.

All previously identified product IDs can be found in the `fixed` list:
```
"fixed": [
]
```

#### Remediations 
In the CSAF files, the only `remediations` category present will be one `vendor_fix` object that maps to the RHSA that
the CSAF file represents.

* `fixed`
  * `vendor_fix`: For all the product IDs with a fixed product status there will be a corresponding entry
    in the remediations object that correlates each full product ID to the correct RHSAs. The RHSA can be determined by
    the `url` field.
    * `Details`: "Fixed".
    * `URL`: A link to the RHSA that released the fix.

For our fixed kernel component "7Server-7.4.AUS:kernel-0:3.10.0-693.112.1.el7.src", there are two remediation entries.
One represents the vendor fix that was released and the other represents that there is a reported mitigation for this 
CVE.

```
```


## Additional Notes
https://www.redhat.com/en/about/brand/standards/history
https://www.redhat.com/en/blog/20-years-red-hat-product-security-inception-customer-experience
