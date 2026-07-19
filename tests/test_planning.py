from __future__ import annotations

import json

import pytest

from aef.planning import build_plan, plan_to_markdown, render_brief, render_checklists, resolve_project_type
from aef.schema import validate_team_plan


@pytest.mark.parametrize("project_type", ["general", "catalog", "scientific", "software", "research", "automation"])
def test_every_project_type_generates_valid_plan(repo_root, project_type):
    plan = build_plan(repo_root, project_type, "Pedido de teste")
    assert validate_team_plan(plan) == []
    assert plan["roles"]
    assert plan["risks"]
    assert plan["acceptance_criteria"]
    assert plan["stop_conditions"]


def test_catalog_plan_contains_material_roles(repo_root):
    plan = build_plan(repo_root, "catalog")
    role_skills = {role["skill"] for role in plan["roles"]}
    assert role_skills == {"editorial", "design", "marketing", "quality-assurance"}
    rendered = plan_to_markdown(plan)
    assert "## Riscos" in rendered
    assert "## Critérios de aceite" in rendered
    assert "## Condições de parada" in rendered


def test_resolves_type_from_keywords_and_falls_back(repo_root):
    assert resolve_project_type(repo_root, None, "Preciso criar um catálogo de produtos") == "catalog"
    assert resolve_project_type(repo_root, None, "Tarefa sem sinal específico") == "general"
    with pytest.raises(ValueError, match="tipo desconhecido"):
        resolve_project_type(repo_root, "inexistente")


def test_brief_and_checklist_are_rendered(repo_root):
    brief = render_brief(repo_root, "automation")
    checklist = render_checklists(repo_root, "automation")
    assert "Condições de parada" in brief
    assert "QA — Automação" in checklist
    assert "Checklist final universal" in checklist


def test_schema_is_valid_json(repo_root):
    schema = json.loads((repo_root / "schemas" / "team-plan.schema.json").read_text(encoding="utf-8"))
    assert schema["$schema"].endswith("2020-12/schema")
    assert schema["additionalProperties"] is False

