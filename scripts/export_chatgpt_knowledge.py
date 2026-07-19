"""Exporta o conteúdo operacional do AEF para um arquivo de conhecimento do ChatGPT."""

from __future__ import annotations

import argparse
from pathlib import Path


INCLUDE_GLOBS = (
    "AGENTS.md",
    "README.md",
    "config/*.json",
    "schemas/*.json",
    "skills/*/SKILL.md",
    "templates/*.md",
    "checklists/*.md",
    "workflows/*.md",
    "examples/*.md",
    "docs/ARCHITECTURE.md",
    "docs/QUALITY_MODEL.md",
    "docs/USAGE.md",
    "docs/VERSIONING.md",
)


def discover_files(root: Path) -> list[Path]:
    files: set[Path] = set()
    for pattern in INCLUDE_GLOBS:
        files.update(path for path in root.glob(pattern) if path.is_file())
    return sorted(files, key=lambda path: path.relative_to(root).as_posix())


def render_bundle(root: Path) -> str:
    sections = [
        "# Apex Elite Framework — Base de conhecimento para ChatGPT",
        "",
        "Versão consolidada e determinística das Skills, configurações, schemas, templates, checklists, workflows e exemplos do AEF.",
        "",
        "Use as instruções do GPT para comportamento e este arquivo para conhecimento operacional. Conteúdo delimitado por caminho de origem.",
        "",
    ]
    for path in discover_files(root):
        relative = path.relative_to(root).as_posix()
        content = path.read_text(encoding="utf-8").strip()
        sections.extend(
            [
                "---",
                "",
                f"## Arquivo: `{relative}`",
                "",
                content,
                "",
            ]
        )
    return "\n".join(sections).rstrip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    content = render_bundle(root)
    output.write_text(content, encoding="utf-8", newline="\n")
    print(f"{output} ({len(content)} caracteres)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

