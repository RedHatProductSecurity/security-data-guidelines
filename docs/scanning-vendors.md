# Vulnerability Scanning and CSAF/VEX 

## Red Hat's Vulnerability Scanning Certification Program
The Red Hat Vulnerability Scanner Certification is a collaboration with security partners to deliver accurate and 
reliable container vulnerability scanning results of Red Hat-published images and packages. More about the Vulnerability 
Scanner Certification program can be found 
[here](https://connect.redhat.com/en/partner-with-us/red-hat-vulnerability-scanner-certification?extIdCarryOver=true&sc_cid=701f2000001Css5AAC).

The full list of requirements that vendors must meet to be certified are detailed 
[here](https://redhat-connect.gitbook.io/partner-guide-red-hat-vulnerability-scanner-cert/requirements).

## Technical Guidance on CSAF/VEX Adoption for Vendors
### Package Identification 
In order to accurately find vulnerability information on a particular package within a repository, it’s necessary to 
first properly identify the Red Hat package version, which can differ from upstream versions due to [Red Hat’s 
backporting policy](https://access.redhat.com/security/updates/backporting). 

A detailed explanation of how Red Hat uses PURL's can be found 
[here](https://github.com/RedHatProductSecurity/security-data-guidelines/blob/csaf-vex-guidelines/docs/purl.md).

### Determining CPE 
Common Platform Enumeration (CPE) is a standardized method of describing and identifying classes of applications, 
operating systems, and hardware devices present among an enterprise's computing assets.

Each CPE uniquely identifies the Red Hat platform (product) and version and can be referenced across all of Red Hat’s 
security data. Identifying CPEs is important because a package, identified during the container scan, can have a 
different severity impact rating and state for identified CVE(s) based on the platform and version specific repository 
it belongs to.

#### Container Identification 
In order to correctly identify the container images included in an environment, you can use the podman images command 
to get basic information about container images. Red Hat strongly recommends providing the container repository, 
container tag and container image ID in all vulnerability scans.

#### Repository Identification
Each Red Hat published container image after June 2020 includes content manifest JSON files. The running container’s 
"/root/buildinfo/content_manifests" folder contains the aggregation of all layer’s content manifests, which could have 
different content sets. An individual content manifest JSON file includes a “content_sets” array which provides the 
repository names from which the packages from that container image were installed from. Red Hat recommends extracting 
the “content_sets” data from all json files.

#### CPE Mapping 
After correctly pulling the repository names from the content manifest JSON files, you can use the Red Hat CPE to 
Repository mapping to identify the associated CPEs. The mapping JSON file includes objects for all Red Hat repositories.
Find the corresponding object for the repository name and extract the nested CPE object for the list of all associated 
CPEs.

### Using CSAF/VEX to Find Fix Status
CPEs can be mapped to the product_name objects while individual package PURLs should be mapped to the product_version 
objects.



## Additional Notes

