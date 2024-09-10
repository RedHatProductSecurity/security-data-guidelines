# Red Hat CSAF-VEX Advisories

## Red Hat Security Data Overview 
Red Hat has always been committed to providing our customers and partners with complete and accurate security data for
all Red Hat software. In the past, Red Hat published security advisory information using Common Vulnerability Reporting 
Framework (CVRF) and CVE information using the Open Vulnerability and Assessment Language (OVAL) format. Over the last 
few years, the Common Security Advisory Framework (CSAF) 2.0 standard was published and is now the successor to the 
CVRF version 1.2 as there are many enhancements to the information provided in each CSAF file. 

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
CSAF files provide a standard structured, machine-readable way of representing and sharing security advisory information 
across all software and hardware providers. 

Our CSAF files are always associated with one specific advisory and a given advisory may include one or more product 
version(s) and one or more components, depending on the product type and update scope. The advisory itself can also 
include updates to address one or more vulnerabilities. Red Hat’s CSAF files are publicly available per advisory at
https://access.redhat.com/security/data/csaf/v2/advisories.

### VEX Overview
[Vex profile info]
The CSAF standard acknowledges the need for different use cases and has therefore defined a variety of profiles. Each
profile describes the necessary fields and information needed for a specific use case. Red Hat has adopted the 
Vulnerability Exploitability eXchange (VEX) profile, which is intended to provide the affected state of a vulnerability
on a product or component. 

Red Hat's VEX files are always associated with one CVE and include fix status information for all vulnerable packages and 
Red Hat products. Red Hat’s VEX files are publicly available per CVE at
https://access.redhat.com/security/data/csaf/v2/vex/.

## Document Structure
Although both CSAF and VEX files ultimately serve different purposes, both CSAF and VEX files meet the 
CSAF machine readable standard and use the VEX profile to convey security information. The CSAF-VEX standard includes
three main sections: document metadata, a product tree array and vulnerability metadata.

### Document Metadata 


### Product Tree 


### Vulnerability Metadata 



## Technical Guidance on Adopting CSAF/VEX 

## Additional Notes
