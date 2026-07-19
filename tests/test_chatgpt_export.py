from __future__ import annotations

import importlib.util
from pathlib import Path


def load_exporter(repo_root: Path):
    path = repo_root / "scripts" / "export_chatgpt_knowledge.py"
    spec = importlib.util.spec_from_file_location("export_chatgpt_knowledge", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_bundle_contains_every_skill_and_quality_resource(repo_root):
    exporter = load_exporter(repo_root)
    bundle = exporter.render_bundle(repo_root)
    skill_paths = sorted((repo_root / "skills").glob("*/SKILL.md"))
    assert len(skill_paths) == 11
    for path in skill_paths:
        assert f"## Arquivo: `{path.relative_to(repo_root).as_posix()}`" in bundle
    for required in (
        "config/project-types.json",
        "checklists/final-qa.md",
        "workflows/loop-control.md",
        "templates/catalogo-premium.md",
        "docs/QUALITY_MODEL.md",
    ):
        assert f"## Arquivo: `{required}`" in bundle


def test_bundle_is_deterministic(repo_root):
    exporter = load_exporter(repo_root)
    assert exporter.render_bundle(repo_root) == exporter.render_bundle(repo_root)

