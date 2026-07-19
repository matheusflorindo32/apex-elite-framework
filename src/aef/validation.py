"""Validação estrutural e documental do framework."""

from __future__ import annotations

import json
import re
from pathlib import Path

from .catalog import load_json, load_project_types, load_skills
from .frontmatter import FrontMatterError, parse_skill
from .models import Issue, Severity, ValidationReport
from .planning import build_plan
from .schema import validate_team_plan

REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "SECURITY.md",
    "VERSION",
    "pyproject.toml",
    "config/skills.json",
    "config/project-types.json",
    "schemas/team-plan.schema.json",
    "docs/ARCHITECTURE.md",
    "docs/USAGE.md",
    "docs/CREATING_SKILLS.md",
    "docs/QUALITY_MODEL.md",
    "docs/VERSIONING.md",
    "workflows/loop-control.md",
    "checklists/final-qa.md",
)

REQUIRED_EXAMPLES = {
    "catalog",
    "scientific-review",
    "software-project",
    "documentary-research",
    "automation",
}

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SKILL_NAME = re.compile(r"^[a-z0-9-]{1,63}$")


def validate_repository(root: Path) -> ValidationReport:
    report = ValidationReport()
    _validate_required_files(root, report)
    _validate_skills(root, report)
    _validate_project_types(root, report)
    _validate_schema(root, report)
    _validate_examples(root, report)
    _validate_links(root, report)
    return report


def _validate_required_files(root: Path, report: ValidationReport) -> None:
    for relative in REQUIRED_FILES:
        report.count("required_files")
        if not (root / relative).is_file():
            report.add(Issue("required.missing", f"arquivo obrigatório ausente: {relative}", Severity.CRITICAL, relative))


def _validate_skills(root: Path, report: ValidationReport) -> None:
    try:
        config = load_json(root / "config" / "skills.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report.add(Issue("skills.config", str(exc), Severity.CRITICAL, "config/skills.json"))
        return

    entries = config.get("skills", [])
    if not isinstance(entries, list) or not entries:
        report.add(Issue("skills.empty", "catálogo de skills deve ser uma lista não vazia", Severity.CRITICAL, "config/skills.json"))
        return

    aliases: set[str] = set()
    names: set[str] = set()
    directories: set[str] = set()
    for entry in entries:
        report.count("skills")
        if not isinstance(entry, dict):
            report.add(Issue("skills.entry", "entrada de skill inválida", Severity.HIGH, "config/skills.json"))
            continue
        directory = str(entry.get("directory", ""))
        alias = str(entry.get("alias", ""))
        skill_path = root / "skills" / directory / "SKILL.md"
        if directory in directories:
            report.add(Issue("skills.directory.duplicate", f"diretório duplicado: {directory}", Severity.HIGH, "config/skills.json"))
        directories.add(directory)
        if not alias.startswith("@"):
            report.add(Issue("skills.alias.format", f"alias deve iniciar com @: {alias}", Severity.HIGH, "config/skills.json"))
        if alias.casefold() in aliases:
            report.add(Issue("skills.alias.duplicate", f"alias duplicado: {alias}", Severity.HIGH, "config/skills.json"))
        aliases.add(alias.casefold())

        try:
            document = parse_skill(skill_path)
        except (OSError, FrontMatterError) as exc:
            report.add(Issue("skills.frontmatter", str(exc), Severity.HIGH, skill_path.relative_to(root).as_posix()))
            continue

        keys = set(document.metadata)
        if keys != {"name", "description"}:
            report.add(
                Issue(
                    "skills.frontmatter.keys",
                    f"front matter deve conter apenas name e description; encontrado: {', '.join(sorted(keys))}",
                    Severity.HIGH,
                    skill_path.relative_to(root).as_posix(),
                )
            )
        name = document.metadata.get("name", "")
        if not SKILL_NAME.fullmatch(name):
            report.add(Issue("skills.name.format", f"nome de skill inválido: {name}", Severity.HIGH, skill_path.relative_to(root).as_posix()))
        if name in names:
            report.add(Issue("skills.name.duplicate", f"nome de skill duplicado: {name}", Severity.HIGH, skill_path.relative_to(root).as_posix()))
        names.add(name)
        if name != directory:
            report.add(Issue("skills.directory.name", f"diretório '{directory}' difere do nome '{name}'", Severity.HIGH, skill_path.relative_to(root).as_posix()))

        openai_yaml = skill_path.parent / "agents" / "openai.yaml"
        if not openai_yaml.is_file():
            report.add(Issue("skills.ui.missing", "agents/openai.yaml ausente", Severity.HIGH, openai_yaml.relative_to(root).as_posix()))
        else:
            report.count("skill_interfaces")
            try:
                interface = openai_yaml.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                report.add(Issue("skills.ui.encoding", str(exc), Severity.HIGH, openai_yaml.relative_to(root).as_posix()))
            else:
                for field in ("display_name:", "short_description:", "default_prompt:"):
                    if field not in interface:
                        report.add(Issue("skills.ui.field", f"campo ausente: {field}", Severity.HIGH, openai_yaml.relative_to(root).as_posix()))
                if f"${name}" not in interface:
                    report.add(Issue("skills.ui.prompt", f"default_prompt deve mencionar ${name}", Severity.HIGH, openai_yaml.relative_to(root).as_posix()))

    actual_directories = {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}
    for unlisted in sorted(actual_directories - directories):
        report.add(Issue("skills.unlisted", f"skill não catalogada: {unlisted}", Severity.HIGH, f"skills/{unlisted}/SKILL.md"))


def _validate_project_types(root: Path, report: ValidationReport) -> None:
    try:
        project_types = load_project_types(root)
        skill_names = {skill.name for skill in load_skills(root)}
    except (OSError, ValueError, json.JSONDecodeError, FrontMatterError) as exc:
        report.add(Issue("project_types.config", str(exc), Severity.CRITICAL, "config/project-types.json"))
        return

    if "general" not in project_types:
        report.add(Issue("project_types.general", "tipo 'general' é obrigatório", Severity.HIGH, "config/project-types.json"))
    for project_type, definition in project_types.items():
        report.count("project_types")
        roles = definition.get("roles", [])
        if not roles:
            report.add(Issue("project_types.roles", f"tipo sem papéis: {project_type}", Severity.HIGH, "config/project-types.json"))
            continue
        for role in roles:
            missing = {"role", "skill", "reason", "responsibility", "approval_criterion"} - set(role)
            if missing:
                report.add(Issue("project_types.role.fields", f"papel de {project_type} sem: {', '.join(sorted(missing))}", Severity.HIGH, "config/project-types.json"))
            if role.get("skill") not in skill_names:
                report.add(Issue("project_types.skill", f"skill desconhecida em {project_type}: {role.get('skill')}", Severity.HIGH, "config/project-types.json"))
        try:
            plan = build_plan(root, project_type)
        except ValueError as exc:
            report.add(Issue("project_types.plan", str(exc), Severity.HIGH, "config/project-types.json"))
            continue
        for error in validate_team_plan(plan):
            report.add(Issue("schema.team_plan", f"{project_type}: {error}", Severity.HIGH, "schemas/team-plan.schema.json"))


def _validate_schema(root: Path, report: ValidationReport) -> None:
    path = root / "schemas" / "team-plan.schema.json"
    try:
        schema = load_json(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report.add(Issue("schema.json", str(exc), Severity.CRITICAL, path.relative_to(root).as_posix()))
        return
    report.count("json_schemas")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        report.add(Issue("schema.draft", "schema deve declarar JSON Schema 2020-12", Severity.HIGH, path.relative_to(root).as_posix()))
    required = set(schema.get("required", []))
    if not {"project_type", "roles", "acceptance_criteria"} <= required:
        report.add(Issue("schema.required", "campos essenciais ausentes em required", Severity.HIGH, path.relative_to(root).as_posix()))


def _validate_examples(root: Path, report: ValidationReport) -> None:
    examples = {path.stem for path in (root / "examples").glob("*.md")}
    report.count("examples", len(examples))
    for missing in sorted(REQUIRED_EXAMPLES - examples):
        report.add(Issue("examples.missing", f"exemplo obrigatório ausente: {missing}.md", Severity.HIGH, "examples"))
    for path in (root / "examples").glob("*.md"):
        content = path.read_text(encoding="utf-8")
        for heading in ("## Pedido", "## Equipe esperada", "## Critérios de aceite"):
            if heading not in content:
                report.add(Issue("examples.incomplete", f"seção ausente: {heading}", Severity.MEDIUM, path.relative_to(root).as_posix()))


def _validate_links(root: Path, report: ValidationReport) -> None:
    ignored = {".git", ".venv", ".pytest_cache", "dist", "build"}
    for path in root.rglob("*.md"):
        if ignored & set(path.relative_to(root).parts):
            continue
        content = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(content):
            clean = target.split("#", 1)[0].strip().strip("<>")
            if not clean or clean.startswith(("http://", "https://", "mailto:")):
                continue
            report.count("internal_links")
            if not (path.parent / clean).resolve().exists():
                report.add(Issue("links.broken", f"link interno quebrado: {target}", Severity.HIGH, path.relative_to(root).as_posix()))


def report_to_markdown(report: ValidationReport) -> str:
    data = report.to_dict()
    lines = [
        "# Relatório de Auditoria",
        "",
        f"**Status:** {data['status']}",
        "",
        "## Verificações",
        "",
    ]
    lines.extend(f"- {name}: {count}" for name, count in sorted(data["checks"].items()))
    lines.extend(["", "## Severidades", ""])
    lines.extend(f"- {name}: {count}" for name, count in data["summary"].items())
    lines.extend(["", "## Achados", ""])
    if not data["issues"]:
        lines.append("Nenhum achado.")
    else:
        for issue in data["issues"]:
            location = f" — `{issue['path']}`" if issue.get("path") else ""
            lines.append(f"- **{issue['severity']}** `{issue['code']}`: {issue['message']}{location}")
    return "\n".join(lines).rstrip() + "\n"
