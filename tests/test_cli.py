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


def test_missing_root_is_invalid_input(tmp_path, capsys):
    result = main(["--root", str(tmp_path / "raiz ausente"), "validate"])
    assert result == 2
    assert "raiz inválida" in capsys.readouterr().err


def test_plan_rejects_invalid_config_and_recovers(repo_root, tmp_path, capsys):
    config = tmp_path / "config"
    config.mkdir()
    (config / "skills.json").write_text('{"skills": []}', encoding="utf-8")
    path = config / "project-types.json"
    original = json.loads((repo_root / "config/project-types.json").read_text(encoding="utf-8"))
    general = original["project_types"]["general"]
    path.write_text('{"project_types": {}}', encoding="utf-8")
    output = tmp_path / "plano.json"
    command = ["--root", str(tmp_path), "plan", "--format", "json", "--output", str(output)]

    assert main(command) == 2
    assert "tipo 'general' ausente" in capsys.readouterr().err
    assert not output.exists()

    general["roles"] = []
    path.write_text(json.dumps(original), encoding="utf-8")
    assert main(command) == 2
    assert "plano inválido" in capsys.readouterr().err
    assert not output.exists()

    assert main([*command, "--type", ""]) == 2
    assert "tipo desconhecido" in capsys.readouterr().err
    assert not output.exists()

    assert main(["--root", str(repo_root), *command[2:]]) == 0
    assert json.loads(output.read_text(encoding="utf-8"))["project_type"] == ["general"]

