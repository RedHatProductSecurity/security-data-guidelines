# Technical Guidance for Vulnerability Scanning Vendors

## Certification Overview 
The Red Hat Vulnerability Scanner Certification is a collaboration with security partners to deliver more accurate and 
reliable container vulnerability scanning results of Red Hat products and packages. Security partners can now consume 
and leverage Red Hat’s extensive and evolving set of published security data to minimize customer false positives and 
other discrepancies.

For more detailed information on the program please see the [Partner Guide for Red Hat Vulnerability Scanner Certification](https://redhat-connect.gitbook.io/partner-guide-red-hat-vulnerability-scanner-cert)

## Frequently Asked Questions (FAQs)
Vendors are encouraged to raise any questions regarding security data by opening a ticket in the public 
[SECDATA Jira project](https://issues.redhat.com/projects/SECDATA/). 

Many scanning vendors face similar challenges when reading and parsing Red Hat's security data. To check if your question 
has already been asked, you can review the list of questions asked [here](https://issues.redhat.com/browse/SECDATA-862?filter=12444038).

### RHSAs for Main Stream vs EUS / AUS / TUS 

For a container image based on RHEL 9.4, RHSAs should be reported as follows:

* If available, the vendor should always report the RHSA for RHEL 9.4 main fix
* If there is an RHSA for RHEL 9.4 main + EUS and an RHSA for RHEL 9.5 main: 
  * Report the RHSA for RHEL 9.4 main + EUS
  * If the vendor allows for multiple reports, consider reporting both RHSAs
* If there is not a RHEL 9.4 main fix or RHEL 9.4 main + EUS fix:
  * Report the RHSA for the next main fix (RHEL 9.5), over a RHEL 9.4 EUS fix 
  * If the vendor allows for multiple reports, consider reporting both RHSAs
* If there is not a RHEL 9.4 main fix, RHEL 9.4 main + EUS fix or a  RHEL 9.5 main fix for the next version, but there 
is a main fix for a previous version (RHEL 9.3) and an RHEL 9.4 EUS fix for the existing version:
  * Report the RHSA for the RHEL 9.4 EUS fix
* If there are only RHSAs for previous versions (RHEL 9.3, RHEL 9.2, etc)
  * Ensure that there is an affected status for RHEL 9.4 as the CVE may predate the RHEL 9.4 release and has already 
  been patched  



## Additional Questions or Concerns 
Red Hat is committed to continually improving our security data; any future changes to the data itself or the format of 
the files are tracked in the [Red Hat Security Data Changelog](https://access.redhat.com/articles/5554431).

Please contact Red Hat Product Security with any questions regarding security data at [secalert@redhat.com](secalert@redhat.com) or file an 
issue in the public [SECDATA Jira project](https://issues.redhat.com/projects/SECDATA/issues/SECDATA-525?filter=allopenissues).