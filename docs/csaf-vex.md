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
three main sections: document metadata, a product tree array and vulnerability metadata. The full document structure can
be found here [insert link].

### Document Metadata 
The "document_metadata" section contains general information about the published document itself 
including CVE severity, vendor, published date and revision history. 

General CVE Severity:

```
"aggregate_severity": {
"namespace": "https://access.redhat.com/security/updates/classification/",
"text": "moderate"
},
```

CVE ID, publish date, and last update:

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
}
```

### Product Tree 
The “product_tree” section identifies all affected Red Hat software, represents the nested 
relationship of component to product and  provides CPEs or PURLs depending on the affected layer. There are two main 
objects in the “product_tree” object; “branches” and “relationships”.

#### Branches

The "product_family" category represents a general Red Hat product stream. The following information is included:
```
```

The "product_name" category includes information about a specific Red Hat product version. The following information is 
included:

```
```

The "product_version" category includes information about a specific affected package. The following information is 
included:
```
```

#### Relationships
Also included in the "product_tree" section is a "relationships" object which is used by Red Hat to help represent layered 
products. A relationship entry will be present for all "product_version" objects found in the "product_tree" object. 
All of these nested objects are of the “default_component_of” category and include:

```
```


### Vulnerability Metadata 
The "vulnerability_metadata" section reports vulnerability fix status for any "product_id" listed in the product_tree. 
The following fix statuses are available:

* Fixed: Contains the same fixed component versions and other details (product_tree objects) that the CSAF advisory 
reports for that CVE
* Known Affected: Confirmation that the specific component and product is affected by a particular CVE
* Known Not Affected: Confirmation that the specific component and product is not affected by a particular CVE
* Under Investigation: Information that the Red Hat Product Security team is verifying the applicability and impact of 
a specific CVE to the specific component and product

```
```

For all the product_ids found in the “Fixed” array, these will also be listed in the “remediations” 
array, which correlates each product_id to the correct RHSAs. The RHSA can be determined by the “url” field in the same 
remediation object.


## Additional Notes
https://www.redhat.com/en/about/brand/standards/history
https://www.redhat.com/en/blog/20-years-red-hat-product-security-inception-customer-experience
