import hashlib
import json

import pytest

from aef.cli import main

REVISION = "a" * 40


@pytest.fixture
def handoff(tmp_path, repo_root):
    plan_path = tmp_path / "plan.json"
    criteria_path = tmp_path / "criteria.json"
    envelope_path = tmp_path / "handoff.json"
    assert main(["--root", str(repo_root), "plan", "--type", "software", "--format", "json",
                 "--output", str(plan_path)]) == 0
    plan = json.loads(plan_path.read_bytes())
    criteria_path.write_text(json.dumps(plan["acceptance_criteria"]), encoding="utf-8")
    envelope = {
        "contract_version": 1,
        "source": "tropa-scientific-skills",
        "source_revision": REVISION,
        "target": "apex-elite-framework",
        "status": "prepared",
        "artifacts": {
            "plan": hashlib.sha256(plan_path.read_bytes()).hexdigest(),
            "acceptance-criteria": hashlib.sha256(criteria_path.read_bytes()).hexdigest(),
        },
    }
    envelope_path.write_text(json.dumps(envelope), encoding="utf-8")
    command = ["handoff", "consume", "--envelope", str(envelope_path), "--plan", str(plan_path),
               "--acceptance-criteria", str(criteria_path), "--expected-revision", REVISION]
    return command, plan, envelope_path, envelope, plan_path, criteria_path


def test_handoff_returns_verified_team_plan(handoff, capsys):
    command, plan, _, envelope, *_ = handoff
    capsys.readouterr()
    assert main(command) == 0
    result = json.loads(capsys.readouterr().out)
    assert result == {
        "status": "verified",
        "source_revision": REVISION,
        "artifacts": envelope["artifacts"],
        "team_plan": plan,
    }


@pytest.mark.parametrize("failure", ["revision", "digest", "criteria", "duplicate", "unknown",
                                    "type", "size", "invalid-plan", "version"])
def test_handoff_rejects_invalid_input_without_printing_it(handoff, capsys, failure):
    command, plan, envelope_path, envelope, plan_path, criteria_path = handoff
    marker = "private-shaped-test-marker"
    if failure == "revision":
        command[-1] = "b" * 40
    elif failure == "digest":
        plan_path.write_text(marker, encoding="utf-8")
    elif failure == "criteria":
        criteria_path.write_text(json.dumps([marker]), encoding="utf-8")
        envelope["artifacts"]["acceptance-criteria"] = hashlib.sha256(criteria_path.read_bytes()).hexdigest()
    elif failure == "duplicate":
        envelope_path.write_text(json.dumps(envelope)[:-1] + ', "status": "prepared"}', encoding="utf-8")
    elif failure == "unknown":
        envelope[marker] = "unexpected"
    elif failure == "type":
        plan_path.unlink()
        plan_path.mkdir()
    elif failure == "size":
        plan_path.write_bytes(b"x" * (1024 * 1024 + 1))
    elif failure == "invalid-plan":
        plan["roles"] = []
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        envelope["artifacts"]["plan"] = hashlib.sha256(plan_path.read_bytes()).hexdigest()
    elif failure == "version":
        envelope["contract_version"] = True
    if failure != "duplicate":
        envelope_path.write_text(json.dumps(envelope), encoding="utf-8")

    capsys.readouterr()
    assert main(command) == 2
    output = capsys.readouterr()
    assert output.out == ""
    assert marker not in output.err
