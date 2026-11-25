"""Build or verify the reviewed, offline APEX downloads."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_STORED, ZipFile, ZipInfo

from export_chatgpt_knowledge import read_sources, render_sources

ROOT = Path(__file__).resolve().parents[1]
COMMON = {
    "LICENSE", "VERSION", "AGENTS.md", "chatgpt/INSTRUCTIONS.md",
    "config/skills.json", "schemas/team-plan.schema.json", "templates/project-brief.md",
    "checklists/final-qa.md", "workflows/default-workflow.md", "workflows/loop-control.md",
}
SCIENCE = COMMON | {
    "templates/scientific-review.md", "templates/research-project.md",
    "checklists/scientific-qa.md", "checklists/research-qa.md",
    "examples/scientific-review.md", "examples/documentary-research.md",
    "docs/RESEARCHERS.md", "docs/ECOSYSTEM.md",
}
SCIENCE_SKILLS = {
    "scientific", "research", "editorial", "quality-assurance",
    "commander", "elite-project-orchestrator",
}
SKILLS_README = """# APEX skill collection

Keep the extracted folders together. Open the [APEX operating guide](AGENTS.md)
and the [coordinator skill](skills/elite-project-orchestrator/SKILL.md).
Choose a specialty from the [skill catalog](config/skills.json), then pair its
SKILL.md with the relevant template and checklist. The
[project types](config/project-types.json) identify the matching files.

For an assistant that accepts text, attach or paste the chosen files and the
[assistant instructions](chatgpt/INSTRUCTIONS.md). For native skill discovery,
copy the chosen skill directory from `skills/` according to your host's
installation instructions, keeping its metadata with it.

Use the [project brief](templates/project-brief.md) and
[final checklist](checklists/final-qa.md) with a sample request: “Use @EPO to
plan a 30-minute lesson on probability and give me an acceptance checklist.”

[Version](VERSION) · [License](LICENSE)
"""
SCIENCE_README = """# APEX scientific toolkit

Start with the [research guide](docs/RESEARCHERS.md), then open the
[coordinator skill](skills/elite-project-orchestrator/SKILL.md) and the
[methodology skill](skills/scientific/SKILL.md) or
[documentary research skill](skills/research/SKILL.md).

For a paper critique, use the [review template](templates/scientific-review.md),
[worked example](examples/scientific-review.md), and
[scientific checklist](checklists/scientific-qa.md).
For a source search, use the [research template](templates/research-project.md),
[worked example](examples/documentary-research.md), and
[research checklist](checklists/research-qa.md).

Attach or paste the chosen files and the
[assistant instructions](chatgpt/INSTRUCTIONS.md) in a text-capable assistant.
Start with an example or research materials you have permission to share.
Verify sources and conclusions yourself before using the result.

The [included catalog](config/skills.json) lists the toolkit's six skills.
Use the separate APEX_SKILLS.zip for other aliases such as @Design.

[Final checklist](checklists/final-qa.md) · [Version](VERSION) · [License](LICENSE)
"""


def archive(files: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    with ZipFile(stream, "w", compression=ZIP_STORED) as bundle:
        for name, data in sorted(files.items()):
            info = ZipInfo(name)  # Fixed ZIP epoch on every operating system.
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, data)
    return stream.getvalue()


def generate() -> dict[str, bytes]:
    text_sources = read_sources(ROOT)
    sources = {name: content.encode() for name, content in text_sources.items()}
    skills = {
        name: data for name, data in sources.items()
        if name in COMMON or name == "config/project-types.json"
        or name.startswith(("skills/", "checklists/", "templates/"))
    }
    skills["README.md"] = SKILLS_README.encode()
    science = {name: sources[name] for name in SCIENCE}
    science.update({
        name: data for name, data in skills.items()
        if name.startswith("skills/") and name.split("/")[1] in SCIENCE_SKILLS
    })
    catalog = json.loads(science["config/skills.json"])
    catalog["skills"] = [
        skill for skill in catalog["skills"] if skill["directory"] in SCIENCE_SKILLS
    ]
    science["config/skills.json"] = (json.dumps(catalog, indent=2) + "\n").encode()
    science["README.md"] = SCIENCE_README.encode()
    outputs = {
        "APEX_CHATGPT_KNOWLEDGE.md": render_sources(text_sources).encode(),
        "APEX_INSTRUCTIONS.md": sources["chatgpt/INSTRUCTIONS.md"],
        "APEX_SKILLS.zip": archive(skills),
        "APEX_SCIENTIFIC_TOOLKIT.zip": archive(science),
        "APEX_CODEX_SETUP.md": sources["docs/CODEX_SETUP.md"],
    }
    metadata = {"version": sources["VERSION"].decode().strip(), "license": "Apache-2.0",
                "sha256": {name: hashlib.sha256(data).hexdigest()
                           for name, data in sorted(outputs.items())}}
    outputs["manifest.json"] = (json.dumps(metadata, indent=2) + "\n").encode()
    outputs["SHA256SUMS"] = "".join(
        f"{hashlib.sha256(data).hexdigest()}  {name}\n"
        for name, data in sorted(outputs.items())
    ).encode()
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report missing or stale files")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "bundles")
    args = parser.parse_args()
    target = args.output_dir
    if target.is_symlink() or (target.exists() and not target.is_dir()):
        parser.error("Output directory must be a regular directory")
    expected = generate()
    for name in expected:
        path = target / name
        if path.is_symlink() or (path.exists() and not path.is_file()):
            parser.error(f"Output must be a regular file: {path}")
    if not args.check:
        target.mkdir(parents=True, exist_ok=True)
    if args.check:
        stale = [name for name, data in expected.items()
                 if not (target / name).is_file() or (target / name).read_bytes() != data]
        if target.is_dir():
            stale.extend(sorted(p.name for p in target.iterdir() if p.name not in expected))
        if stale:
            print("Bundle mismatch: " + ", ".join(stale), file=sys.stderr)
            return 1
    else:
        with TemporaryDirectory(dir=target) as staging_dir:
            staging = Path(staging_dir)
            for name, data in expected.items():
                (staging / name).write_bytes(data)
            for name in expected:
                (staging / name).replace(target / name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
