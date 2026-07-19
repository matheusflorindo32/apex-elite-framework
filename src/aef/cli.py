"""Interface de linha de comando do AEF."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from . import __version__
from .catalog import load_project_types, load_skills, repository_root
from .planning import (
    build_plan,
    plan_to_markdown,
    render_brief,
    render_checklists,
    resolve_project_type,
    write_output,
)
from .validation import report_to_markdown, validate_repository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aef", description="Apex Elite Framework")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--root", type=Path, help="raiz alternativa do framework")
    commands = parser.add_subparsers(dest="command", required=True)

    skills = commands.add_parser("skills", help="operações com skills")
    skills_commands = skills.add_subparsers(dest="skills_command", required=True)
    skills_commands.add_parser("list", help="listar skills registradas")

    validate = commands.add_parser("validate", help="validar todo o framework")
    validate.add_argument("--format", choices=("text", "json"), default="text")
    validate.add_argument("--output", type=Path)

    brief = commands.add_parser("brief", help="operações com project brief")
    brief_commands = brief.add_subparsers(dest="brief_command", required=True)
    brief_new = brief_commands.add_parser("new", help="gerar novo project brief")
    brief_new.add_argument("--type", dest="project_type", required=True)
    brief_new.add_argument("--output", type=Path)

    plan = commands.add_parser("plan", help="gerar Team Plan")
    plan.add_argument("--type", dest="project_type")
    plan.add_argument("--request", default="")
    plan.add_argument("--format", choices=("markdown", "json"), default="markdown")
    plan.add_argument("--output", type=Path)

    checklist = commands.add_parser("checklist", help="mostrar checklists aplicáveis")
    checklist.add_argument("--type", dest="project_type", required=True)
    checklist.add_argument("--output", type=Path)

    audit = commands.add_parser("audit", help="gerar auditoria em Markdown ou JSON")
    audit.add_argument("--format", choices=("markdown", "json"), default="markdown")
    audit.add_argument("--output", type=Path)
    return parser


def _root(args: argparse.Namespace) -> Path:
    return args.root.resolve() if args.root else repository_root()


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        root = _root(args)
        if args.command == "skills":
            for skill in load_skills(root):
                print(f"{skill.alias:<14} {skill.name:<28} {skill.description}")
            return 0

        if args.command == "validate":
            report = validate_repository(root)
            content = json.dumps(report.to_dict(), ensure_ascii=False, indent=2) + "\n" if args.format == "json" else report_to_markdown(report)
            if args.output:
                write_output(content, args.output)
                print(args.output)
            else:
                print(content, end="")
            return 0 if report.passed else 1

        if args.command == "brief":
            project_type = resolve_project_type(root, args.project_type)
            content = render_brief(root, project_type)
            if args.output:
                write_output(content, args.output)
                print(args.output)
            else:
                print(content, end="")
            return 0

        if args.command == "plan":
            project_type = resolve_project_type(root, args.project_type, args.request)
            plan = build_plan(root, project_type, args.request)
            content: str | dict[str, object] = plan if args.format == "json" else plan_to_markdown(plan)
            rendered = write_output(content, args.output)
            if args.output:
                print(args.output)
            else:
                print(rendered, end="")
            return 0

        if args.command == "checklist":
            project_type = resolve_project_type(root, args.project_type)
            content = render_checklists(root, project_type)
            if args.output:
                write_output(content, args.output)
                print(args.output)
            else:
                print(content, end="")
            return 0

        if args.command == "audit":
            report = validate_repository(root)
            content = json.dumps(report.to_dict(), ensure_ascii=False, indent=2) + "\n" if args.format == "json" else report_to_markdown(report)
            if args.output:
                write_output(content, args.output)
                print(args.output)
            else:
                print(content, end="")
            return 0 if report.passed else 1

        parser.error("comando não implementado")
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

