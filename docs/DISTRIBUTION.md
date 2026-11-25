# Assistant downloads

The [bundles directory](../bundles/) contains files for offline inspection
or use in an assistant. Open a file on GitHub and select **Download raw file**.

| File | Use |
| --- | --- |
| APEX_INSTRUCTIONS.md | Read and paste the behavior instructions in your assistant's instruction field. |
| APEX_CHATGPT_KNOWLEDGE.md | Attach the operational Markdown as context. Hosts that accept text files can use the same download, subject to context and upload limits. |
| APEX_SKILLS.zip | Extract the 11 skill folders and their metadata. Follow the target host's installation procedure. |
| APEX_CODEX_SETUP.md | Walk through a project-local Codex session. |
| APEX_SCIENTIFIC_TOOLKIT.zip | Extract APEX's planning and review materials for research tasks. This package contains APEX sources only. |

## Rebuild and verify

Run these commands at the root of a checkout with Python 3.11 or later.

```sh
python scripts/build_bundles.py
python scripts/build_bundles.py --check
```

The check compares the complete output directory with a fresh in-memory build.
A mismatch returns exit code 1. Treat `bundles/` as generated. Change the
sources, rebuild, review the diff and commit both in the same change.
`scripts/bundle_sources.txt` enumerates distributable text sources. Review
each new entry for license, privacy, sensitivity and third-party content.
The manifest identifies the version and Apache-2.0 license. Verify downloaded
file integrity on Linux by running `sha256sum -c SHA256SUMS` inside the
download directory with all seven files present. Compare against checksums from
a separately trusted revision when provenance matters.
