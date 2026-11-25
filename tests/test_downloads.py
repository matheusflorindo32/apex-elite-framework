import hashlib
import json
import re
import shutil
import stat
import subprocess
import sys
from pathlib import PurePosixPath
from zipfile import ZipFile

import pytest


DOWNLOADS = {
    "APEX_CHATGPT_KNOWLEDGE.md", "APEX_INSTRUCTIONS.md", "APEX_CODEX_SETUP.md",
    "APEX_SKILLS.zip", "APEX_SCIENTIFIC_TOOLKIT.zip",
}
LINK = re.compile(r"\]\(([^()\s]+)\)")


def test_downloads(repo_root, tmp_path):
    output = tmp_path / "download"
    command = [sys.executable, str(repo_root / "scripts/build_bundles.py"), "--output-dir"]
    build = [*command, str(output)]
    subprocess.run(build, check=True, cwd=tmp_path)
    subprocess.run([*build, "--check"], check=True, cwd=tmp_path)
    second = tmp_path / "second" / "download"
    subprocess.run([*command, str(second)], check=True, cwd=tmp_path)
    assert {path.name for path in output.iterdir()} == DOWNLOADS | {"manifest.json", "SHA256SUMS"}
    for path in output.iterdir():
        assert path.read_bytes() == (second / path.name).read_bytes()

    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["version"] == (repo_root / "VERSION").read_text(encoding="utf-8").strip()
    assert manifest["license"] == "Apache-2.0"
    hashes = {name: hashlib.sha256((output / name).read_bytes()).hexdigest() for name in DOWNLOADS}
    assert manifest["sha256"] == hashes
    hashes["manifest.json"] = hashlib.sha256((output / "manifest.json").read_bytes()).hexdigest()
    assert (output / "SHA256SUMS").read_text(encoding="utf-8").splitlines() == [
        f"{digest}  {name}" for name, digest in sorted(hashes.items())
    ]

    extra = output / "extra.txt"
    extra.touch()
    assert subprocess.run([*build, "--check"], cwd=tmp_path).returncode == 1
    extra.unlink()
    (output / "APEX_INSTRUCTIONS.md").write_bytes(b"stale")
    assert subprocess.run([*build, "--check"], cwd=tmp_path).returncode == 1


def markdown_targets(document):
    content = document.read_text(encoding="utf-8")
    return [target for target in LINK.findall(content)
            if not target.startswith(("https://", "http://", "mailto:"))]


def test_detached_markdown(repo_root, tmp_path):
    output = tmp_path / "download"
    subprocess.run([sys.executable, str(repo_root / "scripts/build_bundles.py"),
                    "--output-dir", str(output)], check=True, cwd=tmp_path)
    detached = tmp_path / "standalone"
    detached.mkdir()
    for name in sorted(DOWNLOADS):
        if name.endswith(".md"):
            shutil.copyfile(output / name, detached / name)

    knowledge = detached / "APEX_CHATGPT_KNOWLEDGE.md"
    content = knowledge.read_text(encoding="utf-8")
    anchors = re.findall(r'<a name="([^"]+)"></a>', content)
    assert len(anchors) == len(set(anchors))
    assert "## Arquivo: `docs/QUICK_START.md`" in content
    assert "## Arquivo: `docs/QUICK_START.pt-BR.md`" in content
    for button in ("Copy raw file", "Download raw file"):
        assert button not in content
        for guide in ("QUICK_START.md", "QUICK_START.pt-BR.md"):
            assert button in (repo_root / "docs" / guide).read_text(encoding="utf-8")
    targets = markdown_targets(knowledge)
    assert len(targets) > 20
    assert all(target.startswith("#") and target[1:] in anchors for target in targets)
    assert "![" not in content
    assert "file://" not in content
    for name in ("APEX_INSTRUCTIONS.md", "APEX_CODEX_SETUP.md"):
        assert not markdown_targets(detached / name)

    exported = tmp_path / "one" / "two" / "standalone.md"
    subprocess.run([sys.executable, str(repo_root / "scripts/export_chatgpt_knowledge.py"),
                    "--output", str(exported)], check=True, cwd=tmp_path)
    assert exported.read_bytes() == knowledge.read_bytes()


def test_detached_archives(repo_root, tmp_path):
    output = tmp_path / "download"
    subprocess.run([sys.executable, str(repo_root / "scripts/build_bundles.py"),
                    "--output-dir", str(output)], check=True, cwd=tmp_path)
    source_skills = {path.parent.name: path for path in (repo_root / "skills").glob("*/SKILL.md")}
    scientific_skills = {
        "commander", "editorial", "elite-project-orchestrator", "quality-assurance",
        "research", "scientific",
    }
    for name, expected_skills in (("APEX_SKILLS", set(source_skills)),
                                  ("APEX_SCIENTIFIC_TOOLKIT", scientific_skills)):
        extracted = tmp_path / "unpacked" / name
        with ZipFile(output / f"{name}.zip") as archive:
            names = archive.namelist()
            assert names == sorted(set(names))
            assert len({member.casefold() for member in names}) == len(names)
            for member in archive.infolist():
                path = PurePosixPath(member.filename)
                assert not path.is_absolute()
                assert ".." not in path.parts and "\\" not in member.filename and ":" not in member.filename
                assert stat.S_ISREG(member.external_attr >> 16)
                assert member.date_time == (1980, 1, 1, 0, 0, 0)
            assert archive.testzip() is None
            archive.extractall(extracted)

        assert (extracted / "README.md").is_file()
        assert (extracted / "LICENSE").is_file()
        catalog = json.loads((extracted / "config/skills.json").read_text(encoding="utf-8"))
        assert {skill["directory"] for skill in catalog["skills"]} == expected_skills
        assert {path.parent.name for path in (extracted / "skills").glob("*/SKILL.md")} == expected_skills
        for slug in expected_skills:
            relative = source_skills[slug].relative_to(repo_root)
            assert (extracted / relative).read_text(encoding="utf-8") == source_skills[slug].read_text(encoding="utf-8")
            assert (extracted / relative.parent / "agents/openai.yaml").is_file()
        aliases = {skill["alias"] for skill in catalog["skills"]}
        for document in extracted.rglob("*.md"):
            mentioned = set(re.findall(r"@[A-Za-z][\w-]*", document.read_text(encoding="utf-8")))
            assert mentioned <= aliases, (document, mentioned - aliases)
            for target in markdown_targets(document):
                local = target.split("#", 1)[0]
                if local:
                    resolved = (document.parent / local).resolve()
                    assert resolved.is_relative_to(extracted.resolve()) and resolved.is_file(), (document, target)

    skill_pack = tmp_path / "unpacked" / "APEX_SKILLS"
    project_types = json.loads((skill_pack / "config/project-types.json").read_text(encoding="utf-8"))
    for project in project_types["project_types"].values():
        for resource in (project["template"], *project["checklists"]):
            assert (skill_pack / resource).is_file()


@pytest.mark.parametrize("entry", ["../outside.md", "dir/../../outside.md", "C:/outside.md", "dir\\outside.md", "./source.md"])
def test_export_rejects_unsafe_manifest_paths(repo_root, tmp_path, entry):
    root = tmp_path / "checkout"
    (root / "scripts").mkdir(parents=True)
    (root / "scripts/bundle_sources.txt").write_text(entry + "\n", encoding="utf-8")
    output = tmp_path / "detached.md"
    result = subprocess.run([sys.executable, str(repo_root / "scripts/export_chatgpt_knowledge.py"),
                             "--root", str(root), "--output", str(output)],
                            capture_output=True, text=True, cwd=tmp_path)
    assert result.returncode != 0
    assert "Unsafe bundle path" in result.stderr
    assert not output.exists()


def test_export_reads_only_listed_sources(repo_root, tmp_path):
    root = tmp_path / "checkout"
    (root / "scripts").mkdir(parents=True)
    (root / "scripts/bundle_sources.txt").write_text("source.md\n", encoding="utf-8")
    (root / "source.md").write_text("[Unavailable](local-only.md)\n", encoding="utf-8")
    (root / "local-only.md").write_text("unlisted-content-marker\n", encoding="utf-8")
    output = tmp_path / "standalone.md"
    subprocess.run([sys.executable, str(repo_root / "scripts/export_chatgpt_knowledge.py"),
                    "--root", str(root), "--output", str(output)], check=True, cwd=tmp_path)
    content = output.read_text(encoding="utf-8")
    assert "Unavailable (`local-only.md`)" in content
    assert "unlisted-content-marker" not in content
    assert not markdown_targets(output)


def test_linked_output_is_rejected(repo_root, tmp_path):
    output = tmp_path / "download"
    output.mkdir()
    outside = tmp_path / "outside.md"
    outside.write_bytes((repo_root / "bundles/APEX_INSTRUCTIONS.md").read_bytes())
    linked = output / "APEX_INSTRUCTIONS.md"
    try:
        linked.symlink_to(outside)
    except OSError:
        pytest.skip("symlinks unavailable on this filesystem")
    original = outside.read_bytes()

    build = [sys.executable, str(repo_root / "scripts/build_bundles.py"), "--output-dir", str(output)]
    for args in (build, [*build, "--check"]):
        result = subprocess.run(args, capture_output=True, text=True, cwd=tmp_path)
        assert result.returncode != 0
        assert "Output must be a regular file" in result.stderr
    result = subprocess.run([sys.executable, str(repo_root / "scripts/export_chatgpt_knowledge.py"),
                             "--output", str(linked)], capture_output=True, text=True, cwd=tmp_path)
    assert result.returncode != 0
    assert "Unsafe export output" in result.stderr
    assert linked.is_symlink()
    assert outside.read_bytes() == original
