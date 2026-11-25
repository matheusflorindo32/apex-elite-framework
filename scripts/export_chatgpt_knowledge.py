"""Exporta o conteúdo operacional do AEF para um arquivo de conhecimento do ChatGPT."""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


def discover_files(root: Path) -> list[Path]:
    root = root.resolve()
    manifest = root / "scripts" / "bundle_sources.txt"
    if manifest.resolve() != manifest:
        raise ValueError("Unsafe source manifest path")
    files = []
    for name in manifest.read_text(encoding="utf-8").splitlines():
        path = root / name
        if Path(name).is_absolute() or ".." in Path(name).parts or path.resolve() != path:
            raise ValueError(f"Unsafe bundle path: {name}")
        if not path.is_file():
            raise FileNotFoundError(path)
        files.append(path)
    return sorted(files, key=lambda path: path.relative_to(root).as_posix())


def render_bundle(root: Path, output_dir: Path | None = None) -> str:
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
        if path.suffix == ".md":
            base = output_dir or root / "bundles"

            def rebase(match: re.Match[str]) -> str:
                target = match.group(1)
                if target.startswith(("#", "/", "https:", "http:", "mailto:")):
                    return match.group(0)
                local, separator, anchor = target.partition("#")
                try:
                    relative_path = Path(os.path.relpath(path.parent / local, base)).as_posix()
                except ValueError:  # Windows source and export on different volumes
                    relative_path = (path.parent / local).resolve().as_uri()
                return f"]({relative_path}{separator}{anchor})"

            content = re.sub(r"\]\(([^()\s]+)\)", rebase, content)
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
    content = render_bundle(root, output.parent)
    output.write_text(content, encoding="utf-8", newline="\n")
    print(f"{output} ({len(content)} caracteres)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

