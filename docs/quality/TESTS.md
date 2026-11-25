# Candidate test record

The baseline suite passed 25 tests. In a clean environment outside the clone the baseline wheel returned exit 2 for `aef skills list`. The candidate embeds config, skills, templates, checklists, schemas and workflows in the wheel. Installed validation checks runtime resources. Repository validation additionally checks source documentation and examples.

| Candidate check | Scope |
|---|---|
| pytest | CLI, aliases, registry, planning, invalid inputs, stop conditions, export, schema and resource paths |
| aef validate | Repository structure, internal file links, six example documents, eleven skill interfaces |
| scripts/build_bundles.py --check | Byte comparison for generated downloads and checksum inventory |
| uv build then scripts/check_install.py | Install wheel and sdist in separate new environments; list skills, generate brief, plan and checklist, validate and audit |

See the candidate PR for the hosted matrix. Graphical clients, screen readers, novice completion times, and performance under load require separate evaluation.
