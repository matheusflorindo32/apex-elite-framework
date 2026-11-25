# Security review of the international candidate

Baseline `35de85a18ddd8d21a1899fcf0a4e11f8b9c9cd83`. Scope covers APEX source, public Git objects available in the clone, development lock, CI and generated downloads. Assessment date 2026-11-25.

| Severity | Surface and observation | Candidate disposition |
| --- | --- | --- |
| Medium | The baseline exporter's file globs accepted new local Markdown and resolved links. A private document could enter an upload inadvertently. | The exporter now uses a reviewed list of source paths, rejects linked inputs and has a regression test. Review each listed source before distribution. |
| Medium | Baseline catalog, template and checklist paths came from local configuration without a boundary on the resolved location. | The core now checks resolved resource paths. Use trusted source trees. |
| Medium | Both CI actions used moving major tags. Checkout persisted credentials. | The candidate pins both actions to commits, disables credential persistence, retains read-only repository contents and runs on pull_request. Changes to workflow and dependency pins still require maintainer review. |
| Medium | PyPI's version-specific advisory data for the development dependency pytest 8.4.2 lists GHSA-6w46-j5rx-g56g and PYSEC-2026-1845, with 9.0.3 listed as fixed. | See candidate dependency check below. |
| Low | User-selected CLI output paths overwrite existing files. Markdown plans quote user-supplied text, which remains untrusted in subsequent assistant sessions. | Choose a new output file, review generated documents locally and require human approval for external effects. The local planner does not execute text supplied as a request. |
| Informational | The baseline declares zero Python runtime dependencies, has hash-bearing registry entries in uv.lock, read-only CI permissions and Dependabot for uv and GitHub Actions. | Keep the lock reviewed. Hosted-runner images, the uv executable and isolated build requirements introduce separate supply-chain dependencies. |

## Secret and dependency checks

A local scan enumerated objects reachable from the available refs with `git rev-list --objects --all`, selected blobs with `git cat-file -t`, and examined contents without printing matches. Among 135 unique blobs inspected, zero contained an OpenSSH/RSA/EC/DSA/PKCS8 private-key header, a standard AWS AKIA access-key ID or a standard GitHub token pattern. The check covered the refs present at scan time. Other secret types, opaque personal data, deleted remote refs and hosted artifacts require separate review.

For every registry package in the baseline lock, the reviewer queried PyPI's version JSON endpoint and inspected its vulnerabilities array. Colorama 0.4.6, iniconfig 2.3.0, packaging 26.2, pluggy 1.6.0 and pygments 2.20.0 returned empty arrays. Pytest returned the advisory identifiers above. Advisory coverage depends on upstream data and can change. [PyPI JSON API](https://docs.pypi.org/api/json/)

## Privacy, licensing and hosted controls

The Apache-2.0 license and attribution travel with the skill archives. Scientific inputs should be synthetic or approved for the selected assistant. The scientific toolkit ships local APEX material. Uploads to an external service require a separate decision about consent, confidentiality and retention.

A checksum detects changes relative to the manifest. Anyone with repository write access could replace a bundle and its checksum together. Release signing, a hosted SBOM, CodeQL and OpenSSF Scorecard remain possible extensions. GitHub secret scanning, push protection and private vulnerability reporting require verification by the repository administrator. Follow the repository [security policy](../../SECURITY.md) for coordinated reporting.

The independent reviewer checked all six pinned registry dependency versions after upgrading pytest to 9.2.0. The PyPI version JSON returned no listed advisories at review time.
