# Example SBOMs for generic archives (zip / tar)

These examples show what an SPDX 2.3 SBOM for a Red Hat-distributed CLI archive
should look like. They are illustrative and are **not** produced by Konflux.

## helm-cli-4.1.4-linux-amd64

[build/helm-cli-4.1.4-linux-amd64.spdx.json](build/helm-cli-4.1.4-linux-amd64.spdx.json)
describes the linux/amd64 Helm CLI archive published with
[RHSA-2026:26441](https://access.redhat.com/errata/RHSA-2026:26441).

- Archive identity, `packageFileName`, and SHA-256 come from the advisory
  `content.artifacts` row for `helm-linux-amd64.tar.gz`. The purl
  `download_url` is the exact archive file under
  [mirror.openshift.com/pub/cgw/helm/4.1.4/](https://mirror.openshift.com/pub/cgw/helm/4.1.4/)
  (not the truncated `download_url` on that advisory row).
- The golang packages are a **subset** of modules discovered by Syft from the
  published binary at that same mirror directory.
  A production SBOM should list every cataloged `pkg:golang/…` module, including
  `pkg:golang/stdlib`.
- `creationInfo.creators` includes Anchore/Syft to record how those modules were
  discovered, plus the required `Organization: Red Hat`.
- The midstream git URL and commit are stand-ins (same pattern as the container
  image examples that use `git.example.com`).
- Upstream uses `pkg:github/helm/helm@v4.1.4` from the advisory reference to the
  Helm v4.1.4 release.

See [Understanding SBOMs — Generic archive](../../../docs/sbom.md#generic-archive-zip--tar).
