"""Offline validation of the published TeamPlan contract."""

from __future__ import annotations

from typing import Any


def validate_team_plan(plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_arrays = {"project_type", "phases", "risks", "acceptance_criteria", "stop_conditions"}
    optional_arrays = {"skills", "checklists"}
    allowed = required_arrays | optional_arrays | {"roles", "request", "template"}
    if set(plan) - allowed:
        errors.append("campos desconhecidos no plano")
    for field in sorted(required_arrays | (optional_arrays & plan.keys())):
        values = plan.get(field)
        if not isinstance(values, list) or (field in required_arrays and not values):
            errors.append(f"lista inválida: {field}")
            continue
        if not all(isinstance(value, str) and value for value in values):
            errors.append(f"{field} deve conter textos não vazios")
            continue
        if field in {"skills", "project_type"} and len(values) != len(set(values)):
            errors.append(f"itens duplicados em {field}")
        if field == "skills" and any(not value.startswith("@") for value in values):
            errors.append("alias de skill inválido")
    if "request" in plan and not isinstance(plan["request"], str):
        errors.append("request deve ser texto")
    if plan.get("template") is not None and not isinstance(plan["template"], str):
        errors.append("template deve ser texto ou null")

    roles = plan.get("roles")
    if not isinstance(roles, list) or not roles:
        errors.append("roles deve ser uma lista não vazia")
        return errors
    fields = {"role", "skill", "reason", "responsibility", "approval_criterion"}
    for index, role in enumerate(roles):
        if not isinstance(role, dict) or role.keys() != fields:
            errors.append(f"campos inválidos em roles[{index}]")
            continue
        if not all(isinstance(value, str) and value.strip() for value in role.values()):
            errors.append(f"roles[{index}] deve conter textos não vazios")
    return errors
