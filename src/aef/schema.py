"""Validação local do contrato TeamPlan sem dependência de API ou jsonschema."""

from __future__ import annotations

from typing import Any


def validate_team_plan(plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("project_type", "roles", "acceptance_criteria"):
        if key not in plan:
            errors.append(f"campo obrigatório ausente: {key}")

    if not isinstance(plan.get("project_type"), list) or not plan.get("project_type"):
        errors.append("project_type deve ser uma lista não vazia")
    if not isinstance(plan.get("acceptance_criteria"), list) or not plan.get("acceptance_criteria"):
        errors.append("acceptance_criteria deve ser uma lista não vazia")

    roles = plan.get("roles")
    if not isinstance(roles, list) or not roles:
        errors.append("roles deve ser uma lista não vazia")
        return errors
    required_role_fields = ("role", "reason", "responsibility", "approval_criterion")
    for index, role in enumerate(roles):
        if not isinstance(role, dict):
            errors.append(f"roles[{index}] deve ser um objeto")
            continue
        for field in required_role_fields:
            if not isinstance(role.get(field), str) or not role[field].strip():
                errors.append(f"roles[{index}].{field} deve ser texto não vazio")
    return errors

