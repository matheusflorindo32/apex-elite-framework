from __future__ import annotations

import re

from aef.catalog import load_project_types, load_skills, repository_root


def test_loads_unique_skills(repo_root):
    skills = load_skills(repo_root)
    assert len(skills) == 11
    assert len({skill.name for skill in skills}) == len(skills)
    assert len({skill.alias.casefold() for skill in skills}) == len(skills)
    assert {frozenset(skill.document.metadata) for skill in skills} == {frozenset({"name", "description"})}


def test_project_types_have_supported_minimum(repo_root):
    project_types = load_project_types(repo_root)
    assert {"general", "catalog", "scientific", "software", "research", "automation"} <= set(project_types)


def test_repository_root_can_be_discovered_from_nested_path(repo_root):
    assert repository_root(repo_root / "tests") == repo_root

def test_public_directories_link_each_alias_to_its_registered_skill(repo_root):
    expected = {(skill.alias, skill.name) for skill in load_skills(repo_root)}
    skill_link = re.compile(r"\[(@[\w-]+)\]\((?:\.\./)?skills/([\w-]+)/SKILL\.md\)")
    for relative in ("README.md", "README.pt-BR.md", "docs/SKILLS.md"):
        content = (repo_root / relative).read_text(encoding="utf-8")
        assert set(skill_link.findall(content)) == expected, relative
