from __future__ import annotations

import json

from aef.cli import main


def test_skills_list(repo_root, capsys):
    result = main(["--root", str(repo_root), "skills", "list"])
    output = capsys.readouterr().out
    assert result == 0
    assert "@EPO" in output
    assert "@QA" in output


def test_plan_json_can_be_written(repo_root, tmp_path):
    output = tmp_path / "plan.json"
    result = main(["--root", str(repo_root), "plan", "--type", "software", "--format", "json", "--output", str(output)])
    assert result == 0
    plan = json.loads(output.read_text(encoding="utf-8"))
    assert plan["project_type"] == ["software"]
    assert plan["roles"]


def test_validate_json(repo_root, capsys):
    result = main(["--root", str(repo_root), "validate", "--format", "json"])
    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["status"] == "aprovado"

