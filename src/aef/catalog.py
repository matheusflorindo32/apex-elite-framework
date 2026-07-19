"""Carregamento do catálogo de skills e tipos de projeto."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .frontmatter import SkillDocument, parse_skill


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    alias: str
    role: str
    document: SkillDocument


def repository_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "config" / "skills.json").is_file() and (candidate / "skills").is_dir():
            return candidate
    package_root = Path(__file__).resolve().parents[2]
    if (package_root / "config" / "skills.json").is_file():
        return package_root
    raise FileNotFoundError("raiz do Apex Elite Framework não encontrada")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        data = json.load(stream)
    if not isinstance(data, dict):
        raise ValueError(f"objeto JSON esperado em {path}")
    return data


def load_skills(root: Path) -> list[Skill]:
    config = load_json(root / "config" / "skills.json")
    entries = config.get("skills", [])
    if not isinstance(entries, list):
        raise ValueError("config/skills.json: 'skills' deve ser uma lista")

    result: list[Skill] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("cada entrada de skill deve ser um objeto")
        directory = str(entry.get("directory", ""))
        document = parse_skill(root / "skills" / directory / "SKILL.md")
        result.append(
            Skill(
                name=document.metadata.get("name", ""),
                description=document.metadata.get("description", ""),
                alias=str(entry.get("alias", "")),
                role=str(entry.get("role", "specialist")),
                document=document,
            )
        )
    return result


def load_project_types(root: Path) -> dict[str, dict[str, Any]]:
    config = load_json(root / "config" / "project-types.json")
    project_types = config.get("project_types", {})
    if not isinstance(project_types, dict):
        raise ValueError("config/project-types.json: 'project_types' deve ser um objeto")
    return project_types

