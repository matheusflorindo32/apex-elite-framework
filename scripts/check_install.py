"""Exercise a wheel and sdist with uv in isolated environments outside the checkout."""

from pathlib import Path
import json
import os
import subprocess
import sys
from tempfile import TemporaryDirectory


def check(artifact: Path) -> None:
    with TemporaryDirectory() as temporary:
        cwd = Path(temporary)
        environment = cwd / "environment"
        bindir = environment / ("Scripts" if os.name == "nt" else "bin")
        python = bindir / ("python.exe" if os.name == "nt" else "python")
        cli = bindir / ("aef.exe" if os.name == "nt" else "aef")
        subprocess.run(["uv", "venv", "--python", sys.executable, environment], cwd=cwd, check=True)
        subprocess.run(["uv", "pip", "install", "--python", python, artifact], cwd=cwd, check=True)
        for command in [
            ["skills", "list"], ["brief", "new", "--type", "software"],
            ["checklist", "--type", "software"], ["validate"], ["audit"],
        ]:
            subprocess.run([cli, *command], cwd=cwd, check=True, stdout=subprocess.DEVNULL)
        result = subprocess.check_output([cli, "plan", "--type", "software", "--format", "json"], cwd=cwd)
        assert json.loads(result)["project_type"] == ["software"]


if __name__ == "__main__":
    distribution = Path(sys.argv[1]).resolve()
    for pattern in ("*.whl", "*.tar.gz"):
        artifact, = distribution.glob(pattern)
        check(artifact)
