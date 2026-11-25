"""Build or verify the reviewed, offline APEX downloads."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
from tempfile import TemporaryDirectory
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo

from export_chatgpt_knowledge import discover_files, render_bundle

ROOT = Path(__file__).resolve().parents[1]
SCIENCE = {
    "LICENSE", "VERSION", "AGENTS.md", "config/skills.json",
    "templates/scientific-review.md", "templates/research-project.md",
    "checklists/scientific-qa.md", "checklists/research-qa.md", "checklists/final-qa.md",
    "examples/scientific-review.md", "examples/documentary-research.md",
    "workflows/default-workflow.md", "workflows/loop-control.md",
    "docs/RESEARCHERS.md", "docs/ECOSYSTEM.md",
}


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
    sources = {
        p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8").encode()
        for p in discover_files(ROOT)
    }
    skills = {name: data for name, data in sources.items()
              if name.startswith("skills/") or name in {"LICENSE", "VERSION"}}
    science = {name: sources[name] for name in SCIENCE}
    for name, data in skills.items():
        if name.startswith(tuple(f"skills/{skill}/" for skill in
                                 ("scientific", "research", "editorial", "quality-assurance",
                                  "commander", "elite-project-orchestrator"))):
            science[name] = data
    outputs = {
        "APEX_CHATGPT_KNOWLEDGE.md": render_bundle(ROOT).encode(),
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
    if target.is_symlink():
        parser.error("Output directory must not be a symbolic link")
    if not args.check:
        target.mkdir(parents=True, exist_ok=True)
    expected = generate()
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
