# CSAF VEX-Alpha Files

## VEX Alpha Release
Red Hat Product Security is pleased to share that the Alpha version of our new VEX (Vulnerability Exploit eXchange) files is now available [here](https://security.access.redhat.com/data/csaf/v2/vex-alpha/).

### Current Updates
This update focuses on data precision and standardizing our CSAF VEX format. Key improvements include:

* **Improved Product Granularity**: Currently, unfixed products are only represented at the major version (RHEL 9). The new version of VEX files will explicitly list affected supported streams (RHEL 9.6, RHEL 9.4 EUS, RHEL 9.2 EUS, etc.).
Simplified Product Trees: Removing inconsistent branch nesting for ‘architecture’ and ‘product_family’ branches to simplify the product tree structure. We are also removing redundant architecture representation for components and duplication of product variants to reduce the total number of product entries.
* **Enhanced Validation**: Better validation for CSAF VEX formats and identification helpers like CPEs and PURLs
* **Consistency Fixes**: Standardized product ‘name’ and ‘product_id’ formats to ensure consistency between "fixed" and "unfixed" statuses.
* **Streamlined Content**: We’ve removed unrequired fields (duplicate titles, redundant CVSS scores, unnecessary note objects) and ensured ‘fixed’ product and components no longer appear in ‘workaround’ remediation objects.
* **Modernized Infrastructure**: We have migrated VEX publication to a completely new service that improves performance and supportability. 


### Alpha Limitations & Known Issues
As we perform final data cleanup and address some remaining functionality, you may notice daily fluctuations in file content. Please be aware of the following known issues:

* **Binary RPMs**: Currently unavailable for unfixed items. Product security has a critical dependency that must be unblocked before this is able to be addressed.
* **Data Accuracy**: Some products and components may be missing or product statuses may be temporarily incorrect during this transition.
Legacy Data: Some older CVEs may display inaccurate CPEs (e.g., RHEL 7 transitioning from mainstream to EUS CPEs).
* **Data Deletion**: Removing files and handling rejected flaws is currently unsupported. 
* **Scope**: Middleware remains out of scope for this project phase.

### Short Term Adoption Timeline 

* **Beta VEX (End of March)**: Will address any outstanding known issues and initial vendor feedback. We will recommend that vendors begin the adoption process at this time.
* **GA VEX (Red Hat Summit)**: Upon GA, old VEX files will be deprecated. No further enhancements will be made to the SD Engine for old files, though they will remain published for a transition period based on vendor adoption.

### Future Enhancements

* **CSAF Advisory File Improvements**: While this effort currently only focuses on VEX files, we plan to make similar changes to our CSAF Advisory files as well. 
* **Component-level Accuracy**: Instead of determining affectedness at the SRPM level, we will begin reporting the affectedness of binary RPMs and eventually aim to report down to the individual libraries/files that are affected. 
* **Unified Container Reporting**: Direct reporting of all vulnerabilities (RPM and non-RPM) to the container image to provide a more streamlined scanning experience for vendors and better remediation information for customers.
* **CSAF 2.1 Adoption**: We will assess and plan support following the publication of the new version of the CSAF standard.

### How to Provide Feedback
For any issues or questions you have,  please file a jira issue with the following:

* Project: [SECDATA](https://issues.redhat.com/projects/SECDATA/summary)
* Issue Type: Ticket 
* Component: ‘feedback-new-vex’ 
* Description: The question or issue you wish to raise. Please provide a detailed explanation, the VEX file you are referencing and a specific example of the data.  