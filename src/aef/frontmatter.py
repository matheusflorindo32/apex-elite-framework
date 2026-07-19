"""Parser estrito do front matter mínimo usado pelas skills."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SkillDocument:
    path: Path
    metadata: dict[str, str]
    body: str


class FrontMatterError(ValueError):
    """Indica um documento de skill inválido."""


def parse_skill(path: Path) -> SkillDocument:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontMatterError("front matter deve iniciar na primeira linha")

    try:
        closing = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise FrontMatterError("front matter não foi encerrado") from exc

    metadata: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:closing], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise FrontMatterError(f"linha {line_number} não contém chave e valor")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip().strip('"').strip("'")
        if not key or not value:
            raise FrontMatterError(f"linha {line_number} contém chave ou valor vazio")
        if key in metadata:
            raise FrontMatterError(f"chave duplicada: {key}")
        metadata[key] = value

    body = "\n".join(lines[closing + 1 :]).strip()
    if not body:
        raise FrontMatterError("corpo da skill está vazio")
    return SkillDocument(path=path, metadata=metadata, body=body)

