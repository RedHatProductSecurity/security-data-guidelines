# Red Hat CycloneDX Property Taxonomy, v1.0.0

This is the official Red Hat property taxonomy for CycloneDX.

For more information about CycloneDX property taxonomies, refer to
their [official documentation](https://github.com/CycloneDX/cyclonedx-property-taxonomy).

## Red Hat properties

<table>
<thead>
    <tr>
        <th>Property</th>
        <th>Description</th>
        <th>Scope</th>
    </tr>
</thead>
<tbody>
    <tr style="vertical-align: top;">
        <td><b>redhat:advisory_id</b></td>
        <td>The <a href="https://access.redhat.com/articles/explaining_redhat_errata">Red Hat Errata</a> numeric identifier for which the SBOM was generated.</td>
        <td><code>metadata</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>redhat:deliverable-url</b></td>
        <td>If the SBOM was generated from a ZIP file, it indicates the url location of the file.</td>
        <td><code>metadata/component</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>redhat:deliverable-checksum</b></td>
        <td>If the SBOM was generated from a ZIP file, it indicates the checksum (sha256) of the file.</td>
        <td><code>metadata/component</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:architecture</b></td>
        <td>Specifies the CPU architecture for which the image is built, such as amd64, arm64, etc.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:build-date</b></td>
        <td>Indicates the date and time when the image was built.​</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:com.redhat.component</b></td>
        <td>Specifies the Red Hat component name associated with the image.​</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:com.redhat.delivery.backport</b></td>
        <td>A flag indicating whether the image includes backported features or fixes (<code>true</code>) or not (<code>false</code>).</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:com.redhat.delivery.operator.bundle</b></td>
        <td>A flag indicating whether the image is an Operator bundle for Red Hat OpenShift (<code>true</code>) or not (<code>false</code>).​</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:com.redhat.license_terms</b></td>
        <td>Provides a URL to the license terms applicable to the image.​</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:com.redhat.openshift.versions</b></td>
        <td>Specifies the compatible OpenShift versions for the image.​</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:description</b></td>
        <td>Provides a brief description of the image's purpose or contents.​</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:distribution-scope</b></td>
        <td>Defines the scope of distribution, such as <code>public</code> or <code>private</code>.​</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:io.buildah.version</b></td>
        <td>Specifies the version of Buildah used to build the image.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:io.k8s.description</b></td>
        <td>Provides a description of the image for Kubernetes environments.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:io.k8s.display-name</b></td>
        <td>Specifies a human-readable name for the image in Kubernetes contexts.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:io.openshift.tags</b></td>
        <td>Lists tags associated with the image for OpenShift categorization.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:lvms.tags</b></td>
        <td>Specifies tags related to Logical Volume Management (LVM) systems.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:maintainer</b></td>
        <td>Provides contact information for the image's maintainer.​</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:name</b></td>
        <td>Specifies the name of the image.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:operators.operatorframework.io.bundle.channels.v1</b></td>
        <td>Lists the channels for the Operator bundle, such as stable or beta.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:operators.operatorframework.io.bundle.manifests.v1</b></td>
        <td>Indicates the location of the Operator bundle manifests.​</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:operators.operatorframework.io.bundle.mediatype.v1</b></td>
        <td>Specifies the media type or format of the operator bundle, such as Helm charts or plain Kubernetes manifests.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:operators.operatorframework.io.bundle.metadata.v1</b></td>
        <td>Indicates the path within the image to the directory containing metadata files about the bundle.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:operators.operatorframework.io.bundle.package.v1</b></td>
        <td>Denotes the package name of the operator bundle.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:release</b></td>
        <td>Specifies the release version of the image or software contained within.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:summary</b></td>
        <td>Provides a brief summary of the image's purpose or contents.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:url</b></td>
        <td>Offers a URL to more information about the image or the project it represents.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:vcs-ref</b></td>
        <td>Indicates the specific commit reference from the version control system used to build the image.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:vcs-type</b></td>
        <td>Specifies the type of version control system used, such as Git or SVN.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:vendor</b></td>
        <td>Identifies the organization or individual responsible for the image.</td>
        <td><code>components[]</code></td>
    </tr>
    <tr style="vertical-align: top;">
        <td><b>sbomer:image:labels:version</b></td>
        <td>Denotes the version of the application or component contained within the image.</td>
        <td><code>components[]</code></td>
    </tr>
</tbody>
</table>

The **Scope** column describes which `properties` section is the intended location for the property. For example,
a scope of `metadata` means that the property is intended for use in `metadata/properties`. This is meant as a
recommendation only.


## Additional Notes

The properties listed in this document represent an ideal state across all of Red Hat-published security data
that we want to achieve in the long term. In some SBOMs, components or metadata may be missing some properties or their
content may not be accurate. Please
[contact Red Hat Product Security](https://access.redhat.com/security/team/contact/) or file a Jira issue in the
[SECDATA project](https://issues.redhat.com/projects/SECDATA) if you find any discrepancies in Red Hat's security data.
Feedback on our SBOM design and publishing is always welcome and appreciated.


## License

Copyright (c) 2024 Red Hat Product Security

Licensed under MIT License.

