"""Consume a Tropa Scientific Skills v1 handoff from local reviewed files."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path
from typing import Any

from .schema import validate_team_plan

ENVELOPE_LIMIT = 8192
ARTIFACT_LIMIT = 1024 * 1024
ARTIFACTS = {"plan", "acceptance-criteria"}


def _read(path: Path, label: str, limit: int) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_BINARY", 0)
    try:
        with os.fdopen(os.open(path, flags), "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                raise ValueError(f"{label}: arquivo regular esperado")
            data = stream.read(limit + 1)
    except OSError as exc:
        raise ValueError(f"{label}: arquivo inacessível") from exc
    if len(data) > limit:
        raise ValueError(f"{label}: tamanho excede o limite")
    return data


def _unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("chave JSON repetida")
    return result


def _json(data: bytes, label: str) -> Any:
    try:
        return json.loads(data.decode("utf-8-sig"), object_pairs_hook=_unique_keys)
    except (ValueError, RecursionError) as exc:
        raise ValueError(f"{label}: JSON inválido") from exc


def consume(
    envelope_path: Path, plan_path: Path, criteria_path: Path, expected_revision: str
) -> dict[str, Any]:
    if not re.fullmatch(r"[0-9a-f]{40}", expected_revision):
        raise ValueError("revisão esperada deve ser um SHA Git completo")
    envelope = _json(_read(envelope_path, "handoff", ENVELOPE_LIMIT), "handoff")
    if not isinstance(envelope, dict) or envelope.keys() != {
        "contract_version", "source", "source_revision", "target", "status", "artifacts"
    }:
        raise ValueError("campos inválidos no handoff")
    if type(envelope["contract_version"]) is not int or envelope["contract_version"] != 1:
        raise ValueError("versão de contrato incompatível")
    if (envelope["source"] != "tropa-scientific-skills"
            or envelope["target"] != "apex-elite-framework" or envelope["status"] != "prepared"):
        raise ValueError("origem, destino ou estado incompatível")
    if envelope["source_revision"] != expected_revision:
        raise ValueError("revisão de origem divergente")
    digests = envelope["artifacts"]
    if not isinstance(digests, dict) or digests.keys() != ARTIFACTS or any(
        not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value)
        for value in digests.values()
    ):
        raise ValueError("artefatos ou digests inválidos")

    decoded = {}
    for label, path in (("plan", plan_path), ("acceptance-criteria", criteria_path)):
        data = _read(path, label, ARTIFACT_LIMIT)
        if hashlib.sha256(data).hexdigest() != digests[label]:
            raise ValueError(f"{label}: SHA-256 divergente")
        decoded[label] = _json(data, label)

    plan = decoded["plan"]
    if not isinstance(plan, dict) or validate_team_plan(plan):
        raise ValueError("plan: Team Plan inválido")
    if decoded["acceptance-criteria"] != plan["acceptance_criteria"]:
        raise ValueError("acceptance-criteria: critérios divergentes do Team Plan")

    return {
        "status": "verified",
        "source_revision": expected_revision,
        "artifacts": digests,
        "team_plan": plan,
    }
