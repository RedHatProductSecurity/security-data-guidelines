# CSAF VEX-GA Release

## VEX-GA Announcement

Red Hat Product Security is pleased to share that the GA version of our new VEX (Vulnerability Exploit eXchange) files is now available [here](https://security.access.redhat.com/data/csaf/v2/vex-feed/).

### GA Overview

This new release focuses on data precision and standardizing our CSAF VEX format. Key improvements include:

- **Improved Product Granularity**: Currently, unfixed products are only represented at the major version (RHEL 9). The new version of VEX files explicitly lists supported streams (RHEL 9.6, RHEL 9.4 EUS, RHEL 9.2 EUS, etc.).
- **Simplified Product Trees**: Removing inconsistent branch nesting for `architecture` and `product_family` branches to simplify the product tree structure. We are also removing redundant architecture representations for components and multiple product variants to reduce the total number of product entries.
- **Enhanced Validation**: Better validation for CSAF VEX formats and identification helpers like CPEs and PURLs.
- **Consistency Fixes**: Standardized product `name` and `product_id` formats to ensure consistency between `fixed` and `unfixed` statuses.
- **Streamlined Content**: We’ve removed unrequired fields (duplicate titles, redundant CVSS scores, unnecessary note objects) and ensured `fixed` product and components no longer appear in `workaround` remediation objects.
- **Modernized Infrastructure**: We have migrated VEX publication to a completely new service that improves performance and supportability.

More detailed information on the differences between legacy VEX files and GA VEX files will be found [here](https://redhatproductsecurity.github.io/security-data-guidelines/vex-ga-details/).

### Bugs Fixed in GA Release


| Area                                 | Priority | Impact                                                                                                                              |
| ------------------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Product Tree Deduplication           | Blocker  | VEX files now contain cleaner, deduplicated product trees. Scanners see fewer ambiguous or repeated product entries per CVE         |
| Identifier Fidelity (CPE, PURL, CWE) | Blocker  | More accurate CPEs, PURLs, and CWEs. Fewer edge cases where a scanner cannot match the VEX identifier to an installed component     |
| Coverage and Reliability             | Critical | More CVEs generating valid VEX files. The current 98.9% success rate is primarily driven by these fixes                             |
| Data Integrity and Confidentiality   | Blocker  | Partners can trust that no embargoed or pre-disclosure data leaks into the feed, and container VEX entries are correctly structured |
| Data Quality Investigation           | Critical | Enabled resolution of multiple Blocker issues                                                                                       |


### Future Enhancements

- **Component-level Accuracy**: Instead of determining affectedness at the SRPM level, we will begin reporting the affectedness of binary RPMs and eventually aim to report down to the individual libraries/files that are affected. Binary RPM information is currently only availble for some vulnerabilities. Product Security is working to address this gap as soon as possible.
- **Middleware Improvements**: Security Data for Red Hat Middleware products will continue to be improved. 
- **CSAF Advisory File Improvements**: While this effort currently only focuses on VEX files, we plan to make similar changes to our CSAF Advisory files as well. 
- **Unified Container Reporting**: Direct reporting of all vulnerabilities (RPM and non-RPM) to the container image to provide a more streamlined scanning experience for vendors and better remediation information for customers.
- **CSAF 2.1 Adoption**: We will assess and plan support following the publication of the new version of the CSAF standard, which will include the adoption of `product_version_range` for components.

### How to Provide Feedback

For any issues or questions you have,  please file a jira issue with the following:

- **Project**: [SECDATA](https://redhat.atlassian.net/projects/SECDATA/summary)
- **Issue Type**: Ticket 
- **Component**: ‘feedback-new-vex’ 
- **Description**: The question or issue you wish to raise. Please provide a detailed explanation, the VEX file you are referencing and a specific example of the data.

