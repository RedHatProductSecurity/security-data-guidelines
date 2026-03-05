# CSAF-VEX Alpha Details

This document is intended to cover the changes made in the new release of Alpha VEX files compared to the legacy VEX files. These changes are broken out by the three main CSAF VEX document sections: Document, Product Tree and Vulnerabilities. 

## Document Section 

### Document Changes 

#### Title 
Previously, the `document.title` followed the format component:CVE title. The title in the Alpha VEX files removed the component prefix. This decision was made to simplify the title and remove confusion when a CVE affects multiple components. 

```json
# Example of legacy VEX title 
"title": "glibc: Integer overflow in memalign leads to heap corruption",
```

```json
# Example of Alpha VEX title 
"title": "Integer overflow in memalign leads to heap corruption",
```

#### Tracking 
The `document.tracking` object has two changes in the new Alpha VEX files: the generator name has changed and the revision hisotry has been simplified.

In the new Alpha VEX files, the `document.tracking.generator.engine.name` now references the new service responsible for creating VEX files, "CSAF Generator". 

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
# Example of Alpha VEX generator 
"generator": {
        "date": "2026-02-27T12:07:46+00:00",
        "engine": {
          "name": "CSAF Generator",
          "version": "1.0.3"
        }
},
```

The `document.tracking.revision_history` has also been updated in the new Alpha VEX files. Previously, the revision history object implemented some logic to create a history of changes, which was neither accurate nor comprehensive of the historical changes to an individual VEX file. In the new Alpha VEX files, there will only be one revision that represents the last generated version. 

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
# Example of Alpha VEX revision history
"revision_history": [
  {
    "date": "2026-02-27T12:07:46+00:00",
    "number": "1",
    "summary": "Last generated version"
  }
],

```

### Removed Objects
The following optional objects were removed in the Document section and will not be present in the new Alpha VEX files:

* `document.distribution`
* `document.lang`
* `document.notes`
* `document.references`


## Product Tree Section 

### Branch Removal 

### Product Changes

#### Product Granularity

#### Product Names

### Component Changes

#### Architectural Changes

## Vulnerabilities Section

### Remediations 

### CVSS Score

## How to Provide Feedback

For any issues or questions you have,  please file a jira issue with the following:

- **Project**: [SECDATA](https://issues.redhat.com/projects/SECDATA/summary)
- **Issue Type**: Ticket 
- **Component**: ‘feedback-new-vex’ 
- **Description**: The question or issue you wish to raise. Please provide a detailed explanation, the VEX file you are referencing and a specific example of the data.