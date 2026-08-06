# CSAF-VEX GA Details

This document is intended to cover the changes made in the new release of GA VEX files compared to the legacy VEX files. These changes are broken out by the three main CSAF VEX document sections: Document, Product Tree and Vulnerabilities. 

## Document Section

The new GA VEX files include a few minor changes to the `document` section, outlined in the sections below. 

### Document Changes

#### Title

Previously, the `document.title` followed the format component:CVE title. The title in the GA VEX files removed the component prefix. This decision was made to simplify the title and remove confusion when a CVE affects multiple components. 

```json
# Example of legacy VEX title 
"title": "glibc: Integer overflow in memalign leads to heap corruption",
```

```json
# Example of GA VEX title 
"title": "Integer overflow in memalign leads to heap corruption",
```

#### Tracking

The `document.tracking` object has two changes in the new GA VEX files: the generator name has changed and the revision history has been simplified.

In the new GA VEX files, the `document.tracking.generator.engine.name` now references the new service responsible for creating VEX files, "CSAF Generator". 

```json
# Example of legacy VEX generator 
"generator": {
        "date": "2026-02-24T17:08:13+00:00",
        "engine": {
          "name": "Red Hat SDEngine",
          "version": "4.7.1"
        }
},

```

```json
# Example of GA VEX generator 
"generator": {
        "date": "2026-02-27T12:07:46+00:00",
        "engine": {
          "name": "CSAF Generator",
          "version": "1.0.3"
        }
},
```

The `document.tracking.revision_history` has also been updated in the new GA VEX files. Previously, the revision history object implemented some logic to create a history of changes, which was neither accurate nor comprehensive of the historical changes to an individual VEX file. In the new GA VEX files, there will only be one revision that represents the last generated version. 

```json
# Example of legacy VEX revision history
"revision_history": [
  {
    "date": "2026-01-14T21:01:11.037000+00:00",
    "number": "1",
    "summary": "Initial version"
  },
  {
    "date": "2026-02-10T16:17:28+00:00",
    "number": "2",
    "summary": "Current version"
  },
  {
    "date": "2026-02-24T17:08:13+00:00",
    "number": "3",
    "summary": "Last generated version"
  }
],
```

```json
# Example of GA VEX revision history
"revision_history": [
  {
    "date": "2026-02-27T12:07:46+00:00",
    "number": "1",
    "summary": "Last generated version"
  }
],

```

### Removed Document Objects

The following optional objects were removed from the `document` section and will not be present in the new GA VEX files:

- `document.distribution`
- `document.lang`
- `document.notes`
- `document.references`

## Product Tree Section

The `product_tree` section of VEX files includes the most significant changes between legacy VEX files and the new GA VEX files. 

### Branch Removal

In the `product_tree` section of a VEX file, legacy VEX files used to nest `product_name` objects under `product_family` branches and `product_version` objects under `architecture` branches, depending on the fix status of each. The new GA VEX files remove any branch nesting. All `product_name` and `product_version` objects will only be nested under the parent `vendor` branch. 

```json
# Example of legacy VEX branch nesting
 "branches": [
  {
    "branches": [
      {
        "branches": [
          {
            "category": "product_name",
            "name": "Red Hat Enterprise Linux 8",
            "product": {
              "name": "Red Hat Enterprise Linux 8",
              "product_id": "red_hat_enterprise_linux_8",
              "product_identification_helper": {
                "cpe": "cpe:/o:redhat:enterprise_linux:8"
              }
            }
          }
        ],
        "category": "product_family",
        "name": "Red Hat Enterprise Linux 8"
      }
    ],
    "category": "vendor",
    "name": "Red Hat"
  }
],
```

```json
# Example of GA VEX branch nesting
 "branches": [
  {
    "category": "vendor",
    "name": "Red Hat",
    "branches": [
      {
        "category": "product_name",
        "name": "Red Hat Enterprise Linux 8.10.z",
        "product": {
          "name": "Red Hat Enterprise Linux 8.10.z",
          "product_id": "rhel-8.10.z",
          "product_identification_helper": {
            "cpe": "cpe:/a:redhat:enterprise_linux:8"
          }
        }
      },
    ]
  }
 ]
```

### Product Changes

The new GA VEX files include three notable changes to product representation: products are now always represented with a minor version, the product naming convention has been modified for improved consistency and product variants have been eliminated for simplicity. 

#### Product Granularity

Previously, legacy VEX files only represented a product with a minor version when a fix was available. New GA VEX files include representation for any supported minor version, regardless of fix status. This change is intended to provide better affectedness information for each support version of a product that may be impacted by a vulnerability. 

In the example for CVE-2026-0861, the [legacy VEX file](https://security.access.redhat.com/data/csaf/v2/vex/2026/cve-2026-0861.json) only includes a single `product_name` entry to represent the status of Red Hat Enterprise Linux 8. 

```json
# Example of legacy VEX RHEL 8 product representation
{
  "category": "product_name",
  "name": "Red Hat Enterprise Linux 8",
  "product": {
    "name": "Red Hat Enterprise Linux 8",
    "product_id": "red_hat_enterprise_linux_8",
    "product_identification_helper": {
      "cpe": "cpe:/o:redhat:enterprise_linux:8"
    }
  }
}
```

The [GA VEX file](https://security.access.redhat.com/data/csaf/v2/vex-feed/2026/cve-2026-0861.json) includes 5 `product_name` entries to represent the status of each supported version of Red Hat Enterprise Linux 8. 

```json
# Example of GA VEX RHEL 8 product representation 
{
  "category": "product_name",
  "name": "Red Hat Enterprise Linux 8.10.z",
  "product": {
    "name": "Red Hat Enterprise Linux 8.10.z",
    "product_id": "rhel-8.10.z",
    "product_identification_helper": {
      "cpe": "cpe:/a:redhat:enterprise_linux:8"
    }
  }
},
{
  "category": "product_name",
  "name": "Red Hat Enterprise Linux 8.2.0.z",
  "product": {
    "name": "Red Hat Enterprise Linux 8.2.0.z",
    "product_id": "rhel-8.2.0.z",
    "product_identification_helper": {
      "cpe": "cpe:/a:redhat:rhel_aus:8.2"
    }
  }
},
{
  "category": "product_name",
  "name": "Red Hat Enterprise Linux 8.4.0.z",
  "product": {
    "name": "Red Hat Enterprise Linux 8.4.0.z",
    "product_id": "rhel-8.4.0.z",
    "product_identification_helper": {
      "cpe": "cpe:/a:redhat:rhel_eus:8.4"
    }
  }
},
{
  "category": "product_name",
  "name": "Red Hat Enterprise Linux 8.6.0.z",
  "product": {
    "name": "Red Hat Enterprise Linux 8.6.0.z",
    "product_id": "rhel-8.6.0.z",
    "product_identification_helper": {
      "cpe": "cpe:/a:redhat:rhel_eus:8.6"
    }
  }
},
{
  "category": "product_name",
  "name": "Red Hat Enterprise Linux 8.8.0.z",
  "product": {
    "name": "Red Hat Enterprise Linux 8.8.0.z",
    "product_id": "rhel-8.8.0.z",
    "product_identification_helper": {
      "cpe": "cpe:/a:redhat:rhel_eus:8.8"
    }
  }
},
```

#### Product Naming

Previously, legacy VEX files used different naming schemas based on the fix status of the product. The new GA VEX files has standardized on a naming schema to improve consistency of a product's representation throughout the entire lifecycle of a VEX file.  

By comparing the Openshift 4.18 in legacy VEX files for [CVE-2023-26819](https://security.access.redhat.com/data/csaf/v2/vex/2025/cve-2023-126819.json) and [CVE-2025-6176](https://security.access.redhat.com/data/csaf/v2/vex/2025/cve-2025-6176.json), you can see that the `product_id` changes format from "red_hat_openshift_container_platform_4" in an unfixed state to "9Base-RHOSE-4.18" in a fixed state. 

```json
# Example of legacy VEX unfixed product name for CVE-2023-26819
{
  "category": "product_name",
  "name": "Red Hat OpenShift Container Platform 4",
  "product": {
    "name": "Red Hat OpenShift Container Platform 4",
    "product_id": "red_hat_openshift_container_platform_4",
    "product_identification_helper": {
      "cpe": "cpe:/a:redhat:openshift:4"
    }
  }
}

# Example of legacy VEX fixed product name for CVE-2025-6176
{
  "category": "product_name",
  "name": "Red Hat OpenShift Container Platform 4.18",
  "product": {
    "name": "Red Hat OpenShift Container Platform 4.18",
    "product_id": "9Base-RHOSE-4.18",
    "product_identification_helper": {
      "cpe": "cpe:/a:redhat:openshift:4.18::el9"
    }
  }
}
```

In new GA VEX files for [CVE-2023-26819](https://security.access.redhat.com/data/csaf/v2/vex-feed/2023/cve-2023-26819.json) and [CVE-2025-6176](https://security.access.redhat.com/data/csaf/v2/vex-feed/2025/cve-2025-6176.json), the `product_id` value follows the same naming convention between fixed and unfixed states, only varying in the channel specifier. 

```json
# Example of GA VEX unfixed product name for CVE-2023-26819
{
  "category": "product_name",
  "name": "OpenShift Container Platform 4.18",
  "product": {
    "name": "OpenShift Container Platform 4.18",
    "product_id": "openshift-4.18",
    "product_identification_helper": {
      "cpe": "cpe:/a:redhat:openshift:4.18"
    }
  }
}

# Example of GA VEX fixed product name for CVE-2025-6176
{
  "category": "product_name",
  "name": "OpenShift Container Platform 4.18",
  "product": {
    "name": "OpenShift Container Platform 4.18",
    "product_id": "openshift-4.18::el9",
    "product_identification_helper": {
      "cpe": "cpe:/a:redhat:openshift:4.18::el9"
    }
  }
},

```

### Component Changes

In additon to the product representation changes, there are a few changes to component representation. 

#### Component Naming

A minor change was made to the component naming in the new GA VEX files. The `product_version.name` and `product.name` fields for components will not include any version information, even when fixed in the new GA VEX files. Additionally, epoch values will always be present in both the `product_id` and the `purl`.

```json
# Example of legacy VEX component naming for unfixed component
{
  "category": "product_version",
  "name": "libxml2.src",
  "product": {
    "name": "libxml2.src",
    "product_id": "libxml2.src",
    "product_identification_helper": {
      "purl": "pkg:rpm/redhat/libxml2?arch=src"
    }
  }
}

# Example of legacy VEX component naming for fixed component
{
  "category": "product_version",
  "name": "libxml2-0:2.9.13-10.el9_6.src",
  "product": {
    "name": "libxml2-0:2.9.13-10.el9_6.src",
    "product_id": "libxml2-0:2.9.13-10.el9_6.src",
    "product_identification_helper": {
      "purl": "pkg:rpm/redhat/libxml2@2.9.13-10.el9_6?arch=src"
    }
  }
}
```

```json
# Example of GA VEX component naming for unfixed component 
{
  "category": "product_version",
  "name": "libxml2",
  "product": {
    "name": "libxml2",
    "product_id": "libxml2",
    "product_identification_helper": {
      "purl": "pkg:rpm/redhat/libxml2?arch=src"
    }
  }
}

# Example of GA VEX component naming for fixed component
{
  "category": "product_version",
  "name": "libxml2",
  "product": {
    "name": "libxml2",
    "product_id": "libxml2-0:2.9.13-10.el9_6.src",
    "product_identification_helper": {
      "purl": "pkg:rpm/redhat/libxml2@2.9.13-10.el9_6?arch=src&epoch=0"
    }
  }
}
```

#### Architecture Removal

In legacy VEX files, fixed components were represented multiple times for their different architectures. To reduce the total number of component and relationship entries, we have decided to remove architecture representation for components in both their `name`, `product_id` and `purl`. The only exception to this is for SRPM components, which will include a ".src" in the `name` and `product_id` and "arch=src" in the `purl`.

```json
# Example of legacy VEX component architecture
{
  "category": "product_version",
  "name": "glibc-0:2.34-231.el9_7.10.aarch64",
  "product": {
    "name": "glibc-0:2.34-231.el9_7.10.aarch64",
    "product_id": "glibc-0:2.34-231.el9_7.10.aarch64",
    "product_identification_helper": {
      "purl": "pkg:rpm/redhat/glibc@2.34-231.el9_7.10?arch=aarch64"
    }
  }
},
{
  "category": "product_version",
  "name": "glibc-0:2.34-231.el9_7.10.ppc64le",
  "product": {
    "name": "glibc-0:2.34-231.el9_7.10.ppc64le",
    "product_id": "glibc-0:2.34-231.el9_7.10.ppc64le",
    "product_identification_helper": {
      "purl": "pkg:rpm/redhat/glibc@2.34-231.el9_7.10?arch=ppc64le"
    }
  }
},
{
  "category": "product_version",
  "name": "glibc-0:2.34-231.el9_7.10.x86_64",
  "product": {
    "name": "glibc-0:2.34-231.el9_7.10.x86_64",
    "product_id": "glibc-0:2.34-231.el9_7.10.x86_64",
    "product_identification_helper": {
      "purl": "pkg:rpm/redhat/glibc@2.34-231.el9_7.10?arch=x86_64"
    }
  }
},
{
  "category": "product_version",
  "name": "glibc-0:2.34-231.el9_7.10.s390x",
  "product": {
    "name": "glibc-0:2.34-231.el9_7.10.s390x",
    "product_id": "glibc-0:2.34-231.el9_7.10.s390x",
    "product_identification_helper": {
      "purl": "pkg:rpm/redhat/glibc@2.34-231.el9_7.10?arch=s390x"
    }
  }
},

```

```json
# Example of GA VEX component architecture 
{ 
  "category": "product_version", 
  "name": "glibc", 
  "product": { 
    "name": "glibc", 
    "product_id": "glibc-0:2.34-231.el9_7.10.src", 
    "product_identification_helper": { 
      "purl": "pkg:rpm/redhat/glibc@2.34-231.el9_7.10?arch=src&epoch=0" 
    } 
  }
}, 

```

#### Binary RPMs

Binary RPM information is primarily available for Red Hat Hardened Images. Binary RPM information will start being available for newer CVEs soon. Product Security is actively working to address this gap as quickly as possible. 

## Vulnerabilities Section

Finally, there were a few changes made the the `vulnerabilties` section of the new GA VEX files. 

### Remediations

A minor change to the `vulnerabilites.remediations` object was included in the new GA VEX files. Product and component pairs that have a 'fixed' product status will no longer be listed under a `category: workaround` remediation object. Fixed product and componets will only be listed under a `category: vendor_fix` remediation object. 

### CVSS Score

The new GA VEX files simplify the representation of CVSS scores by eliminating the individual metrics, which are still represented in the `vectorString`.  

```json
# Example of legacy VEX CVSS scores
"cvss_v3": {
  "attackComplexity": "HIGH",
  "attackVector": "NETWORK",
  "availabilityImpact": "HIGH",
  "baseScore": 8.1,
  "baseSeverity": "HIGH",
  "confidentialityImpact": "HIGH",
  "integrityImpact": "HIGH",
  "privilegesRequired": "NONE",
  "scope": "UNCHANGED",
  "userInteraction": "NONE",
  "vectorString": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H",
  "version": "3.1"
},
```

```json
# Example of GA VEX CVSS scores
"cvss_v3": {
  "version": "3.1",
  "vectorString": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H",
  "baseScore": 8.1,
  "baseSeverity": "HIGH"
},
```

### Removed Vulnerabilties Objects

- `vulnerabilities.ids`: Entire object has been removed
- `vulnerabilities.notes`: Note objects of the summary category and the general category have been removed
- `vulnerabilities.references`: References to legacy Bugzilla flaws have been removed from this section
- `vulenrabilities.release_date`: Removed as this date is a duplicate value to `vulnerabilities.discovery_date`

## How to Provide Feedback

For any issues or questions you have,  please file a jira issue with the following:

- **Project**: [SECDATA](https://redhat.atlassian.net/projects/SECDATA/summary)
- **Issue Type**: Ticket 
- **Component**: ‘feedback-new-vex’ 
- **Description**: The question or issue you wish to raise. Please provide a detailed explanation, the VEX file you are referencing and a specific example of the data.

