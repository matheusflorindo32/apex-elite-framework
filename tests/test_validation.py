from __future__ import annotations

import json
import shutil

from aef.models import Severity
from aef.validation import validate_repository


def test_repository_passes_validation(repo_root):
    report = validate_repository(repo_root)
    assert report.passed, report.to_dict()
    assert report.checks["skills"] == 11
    assert report.checks["examples"] >= 5


def test_duplicate_alias_is_detected(repo_root, tmp_path):
    copy = tmp_path / "repo"
    shutil.copytree(repo_root, copy, ignore=shutil.ignore_patterns(".git", ".venv", ".pytest_cache", "__pycache__"))
    path = copy / "config" / "skills.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["skills"][1]["alias"] = data["skills"][0]["alias"]
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    report = validate_repository(copy)
    assert any(issue.code == "skills.alias.duplicate" and issue.severity == Severity.HIGH for issue in report.issues)
    assert not report.passed


def test_broken_internal_link_is_detected(repo_root, tmp_path):
    copy = tmp_path / "repo"
    shutil.copytree(repo_root, copy, ignore=shutil.ignore_patterns(".git", ".venv", ".pytest_cache", "__pycache__"))
    path = copy / "docs" / "BROKEN.md"
    path.write_text("# Broken\n\n[ausente](nao-existe.md)\n", encoding="utf-8")
    report = validate_repository(copy)
    assert any(issue.code == "links.broken" and issue.path == "docs/BROKEN.md" for issue in report.issues)
    assert not report.passed

