"""
``bundled()`` / ``golang()`` from Koji Provides (Deptopia ``internal/sources/rpm.go``).

Lightweight SPDX 2 document fragments for manifests (packages + DEPENDENCY_OF).
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

LANG_TO_PURL_TYPE: dict[str, str] = {
    "golang": "golang",
    "python": "pypi",
    "nodejs": "npm",
    "rust": "cargo",
    "ruby": "gem",
    "java": "maven",
    "generic": "generic",
}

_GITHUB_OWNER_REPO_RE = re.compile(
    r"(?:git\+)?https?://(?:www\.)?github\.com/([^/\s)>\"']+)/([^/\s)>\"'#]+)",
    re.IGNORECASE,
)


@dataclass
class RpmDep:
    """Koji ``getRPMDeps`` row."""

    name: str
    version: str
    dep_type: int  # 0 requires, 1 provides


@dataclass
class BundledDep:
    """Single ``bundled()`` or ``golang()`` provide after parsing."""

    path: str
    version: str
    lang: str  # "generic", "golang", "python", ...
    vcs_url: str = ""
    download_url: str = ""


def _github_owner_repo(url: str) -> tuple[str, str] | None:
    """Parse ``(owner, repo)`` from a github.com URL, or return ``None``."""
    if not url:
        return None
    match = _GITHUB_OWNER_REPO_RE.search(url)
    if not match:
        return None
    owner = match.group(1).lower().rstrip(".")
    repo = match.group(2).lower().rstrip(".")
    if repo.endswith(".git"):
        repo = repo[:-4]
    return owner, repo


def _bundled_purls(dep: BundledDep) -> list[str]:
    """Return one or more purls for a bundled dependency."""
    ver = f"@{dep.version}" if dep.version else ""
    purl_type = LANG_TO_PURL_TYPE.get(dep.lang, "generic")

    if purl_type != "generic":
        base = f"pkg:{purl_type}/{dep.path}{ver}"
        qualifiers: list[str] = []
        if dep.vcs_url:
            qualifiers.append(f"vcs_url={quote(dep.vcs_url, safe='')}")
        if dep.download_url:
            qualifiers.append(f"download_url={quote(dep.download_url, safe='')}")
        if qualifiers:
            return [f"{base}?{'&'.join(qualifiers)}"]
        return [base]

    github_coords = _github_owner_repo(dep.vcs_url) or _github_owner_repo(dep.download_url)
    non_github_vcs = dep.vcs_url if dep.vcs_url and not _github_owner_repo(dep.vcs_url) else ""
    non_github_download = (
        dep.download_url if dep.download_url and not _github_owner_repo(dep.download_url) else ""
    )

    if github_coords:
        owner, repo = github_coords
        purls = [f"pkg:github/{owner}/{repo}{ver}"]
        generic_quals: list[str] = []
        if non_github_vcs:
            generic_quals.append(f"vcs_url={quote(non_github_vcs, safe='')}")
        if non_github_download:
            generic_quals.append(f"download_url={quote(non_github_download, safe='')}")
        if generic_quals:
            purls.append(f"pkg:generic/{dep.path}{ver}?{'&'.join(generic_quals)}")
        return purls

    base = f"pkg:generic/{dep.path}{ver}"
    qualifiers: list[str] = []
    if dep.vcs_url:
        qualifiers.append(f"vcs_url={quote(dep.vcs_url, safe='')}")
    if dep.download_url:
        qualifiers.append(f"download_url={quote(dep.download_url, safe='')}")
    if qualifiers:
        return [f"{base}?{'&'.join(qualifiers)}"]
    return [base]


def _bundled_purl(dep: BundledDep) -> str:
    """Primary purl for a bundled dependency (first entry from ``_bundled_purls``)."""
    return _bundled_purls(dep)[0]


def source_purls(
    name: str,
    version: str,
    download_url: str,
    *,
    checksum: str = "",
) -> list[str]:
    """Return one or more purls for an upstream source archive (``Source0``, ``Source-origin``, …)."""
    ver = f"@{version}" if version else ""
    github_coords = _github_owner_repo(download_url)

    if github_coords:
        owner, repo = github_coords
        return [f"pkg:github/{owner}/{repo}{ver}"]

    base = f"pkg:generic/{name}{ver}"
    qualifiers: list[str] = []
    if download_url:
        qualifiers.append(f"download_url={quote(download_url, safe='')}")
    if checksum:
        qualifiers.append(f"checksum={checksum}")
    if qualifiers:
        return [f"{base}?{'&'.join(qualifiers)}"]
    return [base]


def source_purl(
    name: str,
    version: str,
    download_url: str,
    *,
    checksum: str = "",
) -> str:
    """Primary purl for a source archive (first entry from ``source_purls``)."""
    return source_purls(name, version, download_url, checksum=checksum)[0]


def _bundled_display_lang(dep: BundledDep) -> str:
    if dep.lang != "generic":
        return dep.lang
    if _github_owner_repo(dep.vcs_url) or _github_owner_repo(dep.download_url):
        return "github"
    return dep.lang


def _bundled_display_name(dep: BundledDep) -> str:
    if _bundled_display_lang(dep) == "github":
        coords = _github_owner_repo(dep.vcs_url) or _github_owner_repo(dep.download_url)
        label = f"{coords[0]}/{coords[1]}" if coords else dep.path
    else:
        label = dep.path
    lang = _bundled_display_lang(dep)
    name = f"{label} ({lang})"
    if dep.version:
        name = f"{name} {dep.version}"
    return name


def _download_location(dep: BundledDep) -> str:
    if dep.vcs_url:
        return dep.vcs_url
    if dep.download_url:
        return dep.download_url
    return "NOASSERTION"


def _dep_lang_from_inner(name_inner: str) -> tuple[str, str]:
    """Map inner provide name → (path, lang). Mirrors ``getDepListLangFromName``."""
    if name_inner.startswith("golang)") and "(" in name_inner:
        ss = name_inner[len("golang)") :].lstrip()
        if ss.startswith("(") and ")" in ss:
            path = ss[1 : ss.index(")")]
            return path, "golang"

    s = name_inner
    if " with " in s:
        s = s.strip().strip("()")
        s = s.split(" ", 1)[0]

    parts = s.split("(", 1)
    if len(parts) > 1:
        prefix, rest = parts[0], parts[1].rstrip(")")
        lp = prefix.lower()
        if "golang" in lp:
            return rest, "golang"
        if "python" in lp:
            return rest, "python"
        if "npm" in lp or "nodejs" in lp:
            return rest, "nodejs"
        if "ruby" in lp:
            return rest, "ruby"
        if "crate" in lp:
            return rest, "rust"
        if "mvn" in lp:
            return rest, "java"

    sl = name_inner.lower()
    if sl.startswith("nodejs-"):
        return name_inner.split("-", 1)[1], "nodejs"
    if sl.startswith("python-") or sl.startswith("python3-") or sl.startswith("python2-"):
        return name_inner.split("-", 1)[1], "python"
    if sl.startswith("rubygem-"):
        return name_inner.split("-", 1)[1], "ruby"

    return name_inner, "generic"


def _parse_wrapped(
    prefix: str, rpm_name: str, rpm_ver: str, default_lang: str
) -> BundledDep | None:
    pfx = prefix + "("
    if not rpm_name.startswith(pfx) or not rpm_name.endswith(")"):
        return None
    inner = rpm_name[len(pfx) : -1]
    path, lang = _dep_lang_from_inner(inner)
    if lang == "generic" and default_lang != "generic":
        lang = default_lang
    return BundledDep(path=path, version=rpm_ver, lang=lang)


def bundled_golang_from_provides(provides: list[RpmDep]) -> list[BundledDep]:
    """Extract ``bundled(...)`` and ``golang(...)`` Provides (type 1 rows)."""
    out: list[BundledDep] = []
    seen: set[tuple[str, str, str]] = set()
    for d in provides:
        b = _parse_wrapped("bundled", d.name, d.version, "generic")
        if b:
            key = (b.path, b.version, b.lang)
            if key not in seen:
                seen.add(key)
                out.append(b)
            continue
        g = _parse_wrapped("golang", d.name, d.version, "golang")
        if g:
            key = (g.path, g.version, g.lang)
            if key not in seen:
                seen.add(key)
                out.append(g)
    return out


def _ref_id(s: str) -> str:
    h = hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]
    return f"SPDXRef-Bundled-{h}"


def bundled_provides_to_spdx_fragments(
    bundled: list[BundledDep],
    *,
    srpm_spdx_id: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Return ``(packages, relationships)`` SPDX JSON-LD-style dicts (subset).

    Each bundled dep becomes a package; ``DEPENDENCY_OF`` links it to ``srpm_spdx_id``.
    """
    packages: list[dict[str, Any]] = []
    rels: list[dict[str, Any]] = []
    for b in bundled:
        purls = _bundled_purls(b)
        purl = purls[0]
        pid = _ref_id(purl)
        external_refs = [
            {
                "referenceCategory": "PACKAGE-MANAGER",
                "referenceType": "purl",
                "referenceLocator": locator,
            }
            for locator in purls
        ]
        packages.append(
            {
                "SPDXID": pid,
                "name": _bundled_display_name(b),
                "versionInfo": b.version or "NOASSERTION",
                "downloadLocation": _download_location(b),
                "filesAnalyzed": False,
                "primaryPackagePurpose": "LIBRARY",
                "externalRefs": external_refs,
            }
        )
        rels.append(
            {
                "spdxElementId": pid,
                "relationshipType": "DEPENDENCY_OF",
                "relatedSpdxElement": srpm_spdx_id,
            }
        )
    return packages, rels


def bundled_provides_to_cdx_components(bundled: list[BundledDep]) -> list[dict[str, Any]]:
    """Return CycloneDX components for bundled deps (type ``library``)."""
    components: list[dict[str, Any]] = []
    for b in bundled:
        purl = _bundled_purl(b)
        components.append(
            {
                "bom-ref": purl,
                "type": "library",
                "name": _bundled_display_name(b),
                "version": b.version or None,
                "purl": purl,
            }
        )
    return components
