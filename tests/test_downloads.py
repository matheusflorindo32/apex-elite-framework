import hashlib
import json
import subprocess
import sys
from zipfile import ZipFile


def test_downloads(repo_root, tmp_path):
    build = [sys.executable, str(repo_root / "scripts/build_bundles.py"),
             "--output-dir", str(tmp_path)]
    subprocess.run(build, check=True)
    subprocess.run([*build, "--check"], check=True)
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    for name, digest in manifest["sha256"].items():
        assert hashlib.sha256((tmp_path / name).read_bytes()).hexdigest() == digest
    with ZipFile(tmp_path / "APEX_SKILLS.zip") as archive:
        for skill in (repo_root / "skills").glob("*/SKILL.md"):
            assert archive.read(skill.relative_to(repo_root).as_posix()).decode() == skill.read_text(encoding="utf-8")
    with ZipFile(tmp_path / "APEX_SCIENTIFIC_TOOLKIT.zip") as archive:
        assert "skills/scientific/SKILL.md" in archive.namelist()
        assert "LICENSE" in archive.namelist()
    (tmp_path / "APEX_INSTRUCTIONS.md").write_bytes(b"stale")
    assert subprocess.run([*build, "--check"]).returncode == 1
