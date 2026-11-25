"""Exporta o conteúdo operacional do AEF para um arquivo de conhecimento do ChatGPT."""

from __future__ import annotations

import argparse
import re
from collections.abc import Iterator
from pathlib import Path, PurePosixPath
from posixpath import normpath
from tempfile import TemporaryDirectory
from urllib.parse import quote, unquote

INLINE_LINK = re.compile(
    r"(?<!\\)(`+[^\n]*?`+)|(?<!\\)(!?)\[([^\[\]\n]*)\]\("
    r"(<[^>\n]+>|[^()\s]+)([ \t]+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^()\n]*\)))?\)"
)
REFERENCE = re.compile(r"^( {0,3}\[[^\]\n]+\]:[ \t]*)(<[^>\n]+>|\S+)(.*)$")
HEADING = re.compile(r"^ {0,3}#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
DOWNLOAD_SOURCES = {
    "bundles/APEX_INSTRUCTIONS.md": "chatgpt/INSTRUCTIONS.md",
    "bundles/APEX_CODEX_SETUP.md": "docs/CODEX_SETUP.md",
}


def discover_files(root: Path) -> list[Path]:
    root = root.resolve()
    manifest = root / "scripts" / "bundle_sources.txt"
    if manifest.resolve() != manifest:
        raise ValueError("Unsafe source manifest path")
    files = {}
    for name in manifest.read_text(encoding="utf-8").splitlines():
        relative = PurePosixPath(name)
        path = root / name
        if (
            not relative.parts
            or relative.is_absolute()
            or ".." in relative.parts
            or relative.as_posix() != name
            or any(character in name for character in "\\:\x00")
            or path.resolve() != path
        ):
            raise ValueError(f"Unsafe bundle path: {name}")
        if not path.is_file():
            raise FileNotFoundError(path)
        if name.casefold() in files:
            raise ValueError(f"Duplicate bundle path: {name}")
        files[name.casefold()] = path
    return sorted(files.values(), key=lambda path: path.relative_to(root).as_posix())


def read_sources(root: Path) -> dict[str, str]:
    root = root.resolve()
    return {
        path.relative_to(root).as_posix(): path.read_text(encoding="utf-8")
        for path in discover_files(root)
    }


def markdown_lines(content: str) -> Iterator[tuple[str, bool]]:
    """Yield each line with a flag for fenced code."""
    fence = ""
    for line in content.splitlines():
        marker = FENCE.match(line)
        if not fence and marker:
            fence = marker.group(1)
            yield line, True
        elif fence:
            yield line, True
            if marker and marker.group(1).startswith(fence) and not marker.group(2).strip():
                fence = ""
        else:
            yield line, False


def heading_anchors(content: str) -> dict[int, str]:
    headings = {}
    used: set[str] = set()
    for index, (line, fenced) in enumerate(markdown_lines(content)):
        match = HEADING.match(line) if not fenced else None
        if match:
            slug = re.sub(r"[^\w -]", "", match.group(1).lower()).replace(" ", "-")
            anchor = slug
            suffix = 0
            while anchor in used:
                suffix += 1
                anchor = f"{slug}-{suffix}"
            headings[index] = anchor
            used.add(anchor)
    return headings


def source_anchor(name: str) -> str:
    # Keep paths recognizable without reserving percent escapes in URL fragments.
    return "apex-file-" + quote(name, safe="").replace("~", "%7E").replace("%", "~")


def render_markdown(
    name: str,
    content: str,
    headings: dict[str, dict[int, str]],
    referenced_headings: set[tuple[str, str]],
) -> str:
    def target_for(raw: str) -> tuple[str, str]:
        target = raw.removeprefix("<").removesuffix(">")
        if target.startswith(("https://", "http://", "mailto:")):
            return raw, ""
        local, _, fragment = target.partition("#")
        local, fragment = unquote(local), unquote(fragment)
        if (
            local.startswith("/")
            or any(character in local for character in "\\:")
            or any(character in local + fragment for character in "`\x00\r\n")
        ):
            return "", ""
        path = normpath(str(PurePosixPath(name).parent / local)) if local else name
        if path == ".." or path.startswith("../"):
            return "", ""
        if path == "bundles/APEX_CHATGPT_KNOWLEDGE.md":
            return "#apex-knowledge", ""
        path = DOWNLOAD_SOURCES.get(path, path)
        if path not in headings:
            return "", f" (`{path}{'#' + fragment if fragment else ''}`)"
        anchor = source_anchor(path)
        if fragment:
            if fragment not in headings[path].values():
                raise ValueError(f"Unknown heading in {name}: {target}")
            referenced_headings.add((path, fragment))
            anchor += "-" + fragment
        return "#" + anchor, ""

    def replace_link(match: re.Match[str]) -> str:
        code, _, label, target, title = match.groups()
        if code:
            return code
        destination, citation = target_for(target)
        return f"[{label}]({destination}{title or ''})" if destination else label + citation

    output = []
    for line, fenced in markdown_lines(content):
        if not fenced:
            # Reduce image syntax to alternative text before rewriting links around images.
            line = INLINE_LINK.sub(lambda m: m.group(3) if m.group(2) else m.group(0), line)
            line = INLINE_LINK.sub(replace_link, line)
            reference = REFERENCE.match(line)
            if reference:
                label, target, title = reference.groups()
                destination, citation = target_for(target)
                line = label + destination + title if destination else label.rstrip() + citation
        output.append(line)
    return "\n".join(output)


def render_bundle(root: Path, output_dir: Path | None = None) -> str:
    # Keep the argument for existing callers. Anchors make the file location-independent.
    return render_sources(read_sources(root))


def render_sources(sources: dict[str, str]) -> str:
    sources = {name: content.strip() for name, content in sources.items()}
    headings = {name: heading_anchors(content) if name.endswith(".md") else {}
                for name, content in sources.items()}
    referenced_headings: set[tuple[str, str]] = set()
    sources = {
        name: render_markdown(name, content, headings, referenced_headings)
        if name.endswith(".md") else content
        for name, content in sources.items()
    }
    sections = [
        '<a name="apex-knowledge"></a>',
        "",
        "# Apex Elite Framework — Base de conhecimento para ChatGPT",
        "",
        "Versão consolidada e determinística das Skills, configurações, schemas, templates, checklists, workflows e exemplos do AEF.",
        "",
        "Use as instruções do GPT para comportamento e este arquivo para conhecimento operacional. Conteúdo delimitado por caminho de origem.",
        "",
        "Os links internos levam aos arquivos incluídos neste documento. Caminhos em código identificam recursos do repositório. Pesquise pelo caminho do arquivo em leitores de texto simples.",
        "",
    ]
    for relative, content in sources.items():
        anchor = source_anchor(relative)
        lines = content.splitlines()
        suffix = PurePosixPath(relative).suffix
        if suffix in {".json", ".yaml"}:
            lines = [f"```{suffix[1:]}", *lines, "```"]
        for index, fragment in reversed(headings[relative].items()):
            if (relative, fragment) in referenced_headings:
                lines[index:index] = [f'<a name="{anchor}-{fragment}"></a>', ""]
        sections.extend(
            [
                "---",
                "",
                f'<a name="{anchor}"></a>',
                "",
                f"## Arquivo: `{relative}`",
                "",
                "\n".join(lines),
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
    output = args.output
    if output.is_symlink():
        raise ValueError(f"Unsafe export output: {output}")
    content = render_bundle(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output.parent) as stage:
        staged = Path(stage) / output.name
        staged.write_text(content, encoding="utf-8", newline="\n")
        staged.replace(output)
    print(f"{output} ({len(content)} caracteres)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

