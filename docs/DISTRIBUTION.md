# Assistant downloads

The [bundles directory](../bundles/) contains files for offline inspection
or use in an assistant. Open a file on GitHub and select **Download raw file**.

| File | Use |
| --- | --- |
| APEX_INSTRUCTIONS.md | Read and paste the behavior instructions in your assistant's instruction field. |
| APEX_CHATGPT_KNOWLEDGE.md | Open or attach the standalone knowledge document. Its internal links lead to embedded sections. Search by source path in a plain-text viewer. |
| APEX_SKILLS.zip | Extract into its own folder and open the included README.md. It points to the 11 skills, metadata, templates, checklists and workflows. |
| APEX_CODEX_SETUP.md | Walk through a project-local Codex session. |
| APEX_SCIENTIFIC_TOOLKIT.zip | Extract into its own folder and open the included README.md. It points to local examples, research and review templates, six skills and their checklists. |

The Markdown and extracted ZIPs can be read offline outside a checkout.
In the knowledge document, a path shown in code identifies a source in the
repository. External citations require a connection. You can paste the
relevant sections into an assistant that accepts text. Check your host's
instructions for uploads and native skill discovery. Share only sources
approved for the selected host.

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
Output is independent of the download directory. ZIP entries are sorted
and use fixed timestamps. The builder rejects symbolic links in listed
sources or in generated file destinations.
The manifest identifies the version and Apache-2.0 license. Verify downloaded
file integrity on Linux by running `sha256sum -c SHA256SUMS` inside the
download directory with all seven files present. Compare against checksums from
a separately trusted revision when provenance matters.
