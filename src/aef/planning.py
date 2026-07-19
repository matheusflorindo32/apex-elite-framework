"""Seleção determinística de equipe e geração de artefatos."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .catalog import Skill, load_project_types, load_skills


def resolve_project_type(root: Path, requested_type: str | None, request: str = "") -> str:
    project_types = load_project_types(root)
    if requested_type:
        normalized = requested_type.casefold().strip()
        if normalized not in project_types:
            options = ", ".join(sorted(project_types))
            raise ValueError(f"tipo desconhecido '{requested_type}'. Opções: {options}")
        return normalized

    terms = set(re.findall(r"[\wÀ-ÿ-]+", request.casefold()))
    scored: list[tuple[int, str]] = []
    for name, definition in project_types.items():
        keywords = {str(item).casefold() for item in definition.get("keywords", [])}
        scored.append((len(terms & keywords), name))
    best_score, best_name = max(scored, default=(0, "general"))
    return best_name if best_score else "general"


def build_plan(root: Path, project_type: str, request: str = "") -> dict[str, Any]:
    definitions = load_project_types(root)
    definition = definitions[project_type]
    skills_by_name = {skill.name: skill for skill in load_skills(root)}
    roles: list[dict[str, str]] = []

    for role in definition.get("roles", []):
        roles.append(
            {
                "role": str(role["role"]),
                "skill": str(role["skill"]),
                "reason": str(role["reason"]),
                "responsibility": str(role["responsibility"]),
                "approval_criterion": str(role["approval_criterion"]),
            }
        )

    selected_names = {role["skill"] for role in roles}
    missing = selected_names - skills_by_name.keys()
    if missing:
        raise ValueError(f"skills inexistentes no plano: {', '.join(sorted(missing))}")

    return {
        "project_type": [project_type],
        "request": request.strip(),
        "skills": [skills_by_name[name].alias for name in sorted(selected_names)],
        "roles": roles,
        "phases": definition.get("phases", []),
        "risks": definition.get("risks", []),
        "acceptance_criteria": definition.get("acceptance_criteria", []),
        "checklists": definition.get("checklists", []),
        "template": definition.get("template"),
        "stop_conditions": [
            "Todos os critérios obrigatórios foram atendidos.",
            "Não existem defeitos críticos ou altos em aberto.",
            "O limite de três ciclos de correção foi atingido.",
            "Não houve progresso mensurável em duas iterações consecutivas.",
        ],
    }


def plan_to_markdown(plan: dict[str, Any]) -> str:
    lines = [
        "# Team Plan",
        "",
        f"**Tipo:** {', '.join(plan['project_type'])}",
        f"**Pedido:** {plan.get('request') or 'Não informado'}",
        "",
        "## Equipe selecionada",
        "",
    ]
    for role in plan["roles"]:
        lines.extend(
            [
                f"### {role['role']} ({role['skill']})",
                "",
                f"- Justificativa: {role['reason']}",
                f"- Responsabilidade: {role['responsibility']}",
                f"- Critério de aprovação: {role['approval_criterion']}",
                "",
            ]
        )

    for title, key in (
        ("Fases", "phases"),
        ("Riscos", "risks"),
        ("Critérios de aceite", "acceptance_criteria"),
        ("Condições de parada", "stop_conditions"),
    ):
        lines.extend([f"## {title}", ""])
        lines.extend(f"{index}. {item}" for index, item in enumerate(plan[key], start=1))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_brief(root: Path, project_type: str) -> str:
    definition = load_project_types(root)[project_type]
    template = root / str(definition.get("template", "templates/project-brief.md"))
    content = template.read_text(encoding="utf-8")
    return f"<!-- Tipo de projeto: {project_type} -->\n\n{content.rstrip()}\n"


def render_checklists(root: Path, project_type: str) -> str:
    definition = load_project_types(root)[project_type]
    sections = []
    for relative in definition.get("checklists", ["checklists/final-qa.md"]):
        path = root / str(relative)
        sections.append(path.read_text(encoding="utf-8").strip())
    return "\n\n---\n\n".join(sections) + "\n"


def write_output(content: str | dict[str, Any], output: Path | None) -> str:
    rendered = json.dumps(content, ensure_ascii=False, indent=2) + "\n" if isinstance(content, dict) else content
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    return rendered

