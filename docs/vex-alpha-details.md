# CSAF-VEX Alpha Details

This document is intended to cover the changes made in the new release of alpha VEX files compared to the legacy VEX files. These changes are broken out by the three main CSAF VEX document sections: Document, Product Tree and Vulnerabilities. 

## Document Section 

### Document Changes 

#### Title 
Previously, the `document.title` followed the format component:CVE title. The title in the alpha VEX files removed the component prefix. This decision was made to simplify the title and remove confusion when a CVE affects multiple components. 

```json
# Example of legacy VEX title 
"title": "glibc: Integer overflow in memalign leads to heap corruption",
```

```json
# Example of alpha VEX title 
"title": "Integer overflow in memalign leads to heap corruption",
```

#### Tracking 
The `document.tracking` object has two changes in the new alpha VEX files: the generator name has changed and the revision history has been simplified.

In the new alpha VEX files, the `document.tracking.generator.engine.name` now references the new service responsible for creating VEX files, "CSAF Generator". 

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
# Example of alpha VEX generator 
"generator": {
        "date": "2026-02-27T12:07:46+00:00",
        "engine": {
          "name": "CSAF Generator",
          "version": "1.0.3"
        }
},
```

The `document.tracking.revision_history` has also been updated in the new alpha VEX files. Previously, the revision history object implemented some logic to create a history of changes, which was neither accurate nor comprehensive of the historical changes to an individual VEX file. In the new alpha VEX files, there will only be one revision that represents the last generated version. 

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
# Example of alpha VEX revision history
"revision_history": [
  {
    "date": "2026-02-27T12:07:46+00:00",
    "number": "1",
    "summary": "Last generated version"
  }
],

```

### Removed Document Objects 
The following optional objects were removed in the document section and will not be present in the new alpha VEX files:

* `document.distribution`
* `document.lang`
* `document.notes`
* `document.references`


## Product Tree Section 

### Branch Removal 
In the product tree section of a VEX file, legacy VEX files use to nest `product_name` objects under `product_family` branches and `product_version` objects under `architecture` branches, depending on the fix status of each. The new alpha VEX files remove any branch nesting. All `product_name` and `product_version` objects will only be nested under the parent `vendor` branch. 

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
# Example of alpha VEX branch nesting
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
The new alpha VEX files include three notable changes to product representation: products are now always represented with a minor version, the product naming convention has been modified for improved consistency and product variants have been eliminated for simplicity. 

#### Product Granularity
Previously, legacy VEX files only represented a product with a minor version when a fix was available. New alpha VEX files include representation for any supported minor version, regardless of fix status. This change is intended to provide better affectedness information for each support version of a product that may be impacted by a vulnerability. 

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

The [alpha VEX file](https://security.access.redhat.com/data/csaf/v2/vex-alpha/2026/cve-2026-0861.json) includes 5 `product_name` entries to represent the status of each supported version of Red Hat Enterprise Linux 8. 

```json
# Example of alpha VEX RHEL 8 product representation 
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

```json
# Example of legacy VEX 
```

```json
# Example of alpha VEX 
```

#### Product Variants

### Component Changes

#### Architecture Removal

## Vulnerabilities Section


### Remediations 

### CVSS Score
The new alpha VEX files simplify the representation of CVSS scores by eliminating the individual metrics, which are still represented in the `vectorString`.  

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
# Example of alpha VEX CVSS scores
"cvss_v3": {
  "version": "3.1",
  "vectorString": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H",
  "baseScore": 8.1,
  "baseSeverity": "HIGH"
},
```

### Removed Vulnerabilties Objects

* `vulnerabilities.ids`: Entire object has been removed
* `vulnerabilities.notes`: Note objects of the summary category and the general category have been removed
* `vulnerabilities.references`: References to legacy Bugzilla flaws have been removed from this section
* `vulenrabilities.release_date`: Removed as this date is a duplicate value to `vulnerabilities.discovery_date`

## How to Provide Feedback

For any issues or questions you have,  please file a jira issue with the following:

- **Project**: [SECDATA](https://issues.redhat.com/projects/SECDATA/summary)
- **Issue Type**: Ticket 
- **Component**: ‘feedback-new-vex’ 
- **Description**: The question or issue you wish to raise. Please provide a detailed explanation, the VEX file you are referencing and a specific example of the data.