# Red Hat CycloneDX Property Taxonomy

_Version: v1.0.0_

This is the official Red Hat property taxonomy for CycloneDX. For more information about CycloneDX property taxonomies,
refer to the [official documentation](https://github.com/CycloneDX/cyclonedx-property-taxonomy).

| Property                                                                 | Description                                                                                                                            | Scope                |
|--------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|----------------------|
| `redhat:advisory_id`                                                     | The [Red Hat Errata](https://access.redhat.com/articles/explaining_redhat_errata) numeric identifier for which the SBOM was generated. | `metadata`           |
| `redhat:deliverable-url`                                                 | If an SBOM was generated from a ZIP file, it indicates the URL location of the file.                                                   | `metadata/component` |
| `redhat:deliverable-checksum`                                            | If an SBOM was generated from a ZIP file, it indicates the checksum (sha256) of the file.                                              | `metadata/component` |
| `sbomer:image:labels:architecture`                                       | Specifies the CPU architecture for which a container image is built, such as `amd64`, `arm64`, etc.                                    | `components[]`       |
| `sbomer:image:labels:build-date`                                         | Indicates the date and time when a container image was built.                                                                          | `components[]`       |
| `sbomer:image:labels:com.redhat.component`                               | Specifies the Red Hat component name associated with a container image.                                                                | `components[]`       |
| `sbomer:image:labels:com.redhat.delivery.backport`                       | A flag indicating whether a container image includes backported features or fixes (`true`) or not (`false`).                           | `components[]`       |
| `sbomer:image:labels:com.redhat.delivery.operator.bundle`                | A flag indicating whether a container image is an Operator bundle for Red Hat OpenShift (`true`) or not (`false`).                     | `components[]`       |
| `sbomer:image:labels:com.redhat.license_terms`                           | Provides a URL to the license terms applicable to a container image.                                                                   | `components[]`       |
| `sbomer:image:labels:com.redhat.openshift.versions`                      | Specifies the compatible OpenShift versions for a container image.                                                                     | `components[]`       |
| `sbomer:image:labels:description`                                        | Provides a brief description of container image's purpose or contents.                                                                 | `components[]`       |
| `sbomer:image:labels:distribution-scope`                                 | Defines the scope of distribution, such as `public` or `private`.                                                                      | `components[]`       |
| `sbomer:image:labels:io.buildah.version`                                 | Specifies the version of Buildah used to build a container image.                                                                      | `components[]`       |
| `sbomer:image:labels:io.k8s.description`                                 | Provides a description of container image for Kubernetes environments.                                                                 | `components[]`       |
| `sbomer:image:labels:io.k8s.display-name`                                | Specifies a human-readable name for a container image in Kubernetes contexts.                                                          | `components[]`       |
| `sbomer:image:labels:io.openshift.tags`                                  | Lists tags associated with container image for OpenShift categorization.                                                               | `components[]`       |
| `sbomer:image:labels:lvms.tags`                                          | Specifies tags related to Logical Volume Management (LVM) systems.                                                                     | `components[]`       |
| `sbomer:image:labels:maintainer`                                         | Provides contact information for a container image's maintainer.                                                                       | `components[]`       |
| `sbomer:image:labels:name`                                               | Specifies the name of a container image.                                                                                               | `components[]`       |
| `sbomer:image:labels:operators.operatorframework.io.bundle.channels.v1`  | Lists the channels for the Operator bundle, such as `stable` or `beta`.                                                                | `components[]`       |
| `sbomer:image:labels:operators.operatorframework.io.bundle.manifests.v1` | Indicates the location of the Operator bundle manifests.                                                                               | `components[]`       |
| `sbomer:image:labels:operators.operatorframework.io.bundle.mediatype.v1` | Specifies the media type or format of the operator bundle, such as Helm charts or plain Kubernetes manifests.                          | `components[]`       |
| `sbomer:image:labels:operators.operatorframework.io.bundle.metadata.v1`  | Indicates the path within the image to the directory containing metadata files about the bundle.                                       | `components[]`       |
| `sbomer:image:labels:operators.operatorframework.io.bundle.package.v1`   | Denotes the package name of the operator bundle.                                                                                       | `components[]`       |
| `sbomer:image:labels:release`                                            | Specifies the release version of a container image or software contained within.                                                       | `components[]`       |
| `sbomer:image:labels:summary`                                            | Provides a brief summary of a container image's purpose or contents.                                                                   | `components[]`       |
| `sbomer:image:labels:url`                                                | Offers a URL to more information about a container image or the project it represents.                                                 | `components[]`       |
| `sbomer:image:labels:vcs-ref`                                            | Indicates the specific commit reference from the version control system used to build a container image.                               | `components[]`       |
| `sbomer:image:labels:vcs-type`                                           | Specifies the type of version control system used, such as Git or SVN.                                                                 | `components[]`       |
| `sbomer:image:labels:vendor`                                             | Identifies the organization or individual responsible for a container image.                                                           | `components[]`       |
| `sbomer:image:labels:version`                                            | Denotes the version of the application or component contained within a container image.                                                | `components[]`       |

The `Scope` column describes which `properties` section is the intended location for the property. For example,
a scope of `metadata` means that the property is intended for use in `metadata/properties`. This is meant as a
recommendation only.
