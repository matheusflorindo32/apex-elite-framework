"""Check the local release artifacts and exercise their installed CLI offline."""

from argparse import ArgumentParser
from email.parser import BytesParser
import json
import os
from pathlib import Path
import subprocess
import sys
from tarfile import open as open_tar
from tempfile import TemporaryDirectory
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
PROJECT = "apex-elite-framework"
RESOURCE_DIRECTORIES = ("config", "skills", "templates", "checklists", "schemas", "workflows")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def check_contents(wheel: Path, sdist: Path, version: str) -> None:
    resources = [
        path.relative_to(ROOT).as_posix()
        for directory in RESOURCE_DIRECTORIES
        for path in sorted((ROOT / directory).rglob("*"))
        if path.is_file()
    ]
    prefix = f"{PROJECT.replace('-', '_')}-{version}"
    dist_info = prefix + ".dist-info"
    license_bytes = (ROOT / "LICENSE").read_bytes()

    with ZipFile(wheel) as archive:
        for path in resources:
            require(
                archive.read("aef/resources/" + path) == (ROOT / path).read_bytes(),
                f"{wheel.name}: resource differs from source: {path}",
            )
        require(archive.read(f"{dist_info}/licenses/LICENSE") == license_bytes, "wheel license differs")
        metadata = BytesParser().parsebytes(archive.read(f"{dist_info}/METADATA"))
        require(metadata["Name"] == PROJECT and metadata["Version"] == version, "wheel metadata differs")
        require(not metadata.get_all("Requires-Dist"), "wheel declares runtime dependencies")

    with open_tar(sdist, "r:gz") as archive:
        for path in (*resources, "LICENSE", "pyproject.toml", "VERSION", "README.md", "src/aef/cli.py", "PKG-INFO"):
            member = archive.extractfile(f"{prefix}/{path}")
            require(member is not None, f"{sdist.name}: missing regular file: {path}")
            with member:
                contents = member.read()
            if path == "PKG-INFO":
                metadata = BytesParser().parsebytes(contents)
                require(metadata["Name"] == PROJECT and metadata["Version"] == version, "sdist metadata differs")
                require(not metadata.get_all("Requires-Dist"), "sdist declares runtime dependencies")
            else:
                require(contents == (ROOT / path).read_bytes(), f"{sdist.name}: file differs from source: {path}")


def check(artifact: Path, version: str) -> None:
    with TemporaryDirectory(prefix="aef instalação ") as temporary:
        cwd = Path(temporary)
        environment = cwd / "ambiente isolado"
        bindir = environment / ("Scripts" if os.name == "nt" else "bin")
        python = bindir / ("python.exe" if os.name == "nt" else "python")
        cli = bindir / ("aef.exe" if os.name == "nt" else "aef")

        env = os.environ.copy()
        for name in ("PYTHONHOME", "PYTHONPATH", "VIRTUAL_ENV"):
            env.pop(name, None)
        env["PYTHONUTF8"] = "1"
        env["UV_OFFLINE"] = "1"
        subprocess.run(["uv", "venv", "--python", sys.executable, environment], cwd=cwd, env=env, check=True)
        subprocess.run(
            ["uv", "pip", "install", "--no-deps", "--python", python, artifact],
            cwd=cwd, env=env, check=True,
        )

        def run(*command: str, status: int = 0) -> str:
            result = subprocess.run([cli, *command], cwd=cwd, env=env, capture_output=True, encoding="utf-8")
            require(
                result.returncode == status and "Traceback" not in result.stderr,
                f"{artifact.name}: {command} returned {result.returncode}, expected {status}\n{result.stderr}",
            )
            return result.stdout

        require(run("--version").strip() == f"aef {version}", f"{artifact.name}: CLI version differs")
        skills = run("skills", "list")
        require("@EPO" in skills and "@QA" in skills, f"{artifact.name}: installed skills missing")
        require("## Problema" in run("brief", "new", "--type", "software"), f"{artifact.name}: brief invalid")
        checklist = run("checklist", "--type", "software")
        require("Checklist final universal" in checklist, f"{artifact.name}: checklist invalid")

        for command in ("validate", "audit"):
            report = json.loads(run(command, "--format", "json"))
            require(
                report["status"] == "aprovado" and report["checks"]["json_schemas"] == 1,
                f"{artifact.name}: installed {command} report invalid",
            )

        output = cwd / "saídas locais" / "plano.json"
        request = "Planejar um aplicativo de leitura em português"
        plan_command = ("plan", "--type", "software", "--request", request, "--format", "json")
        run(*plan_command, "--output", str(output))
        plan = json.loads(output.read_text(encoding="utf-8"))
        require(plan["project_type"] == ["software"] and plan["request"] == request, f"{artifact.name}: plan invalid")
        subprocess.run(
            [
                python, "-I", "-c",
                (
                    "import json, sys; from pathlib import Path; from aef.schema import validate_team_plan; "
                    "errors = validate_team_plan(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))); "
                    "sys.exit('\\n'.join(errors) if errors else 0)"
                ),
                output,
            ],
            cwd=cwd, env=env, check=True,
        )

        run("plan", "--type", "inexistente", "--output", str(output), status=2)
        run("--root", str(cwd / "raiz ausente"), "validate", status=2)
        blocked = cwd / "arquivo bloqueando diretório"
        blocked.touch()
        run(*plan_command, "--output", str(blocked / "plano.json"), status=2)
        require(json.loads(output.read_text(encoding="utf-8")) == plan, f"{artifact.name}: plan changed on failure")
        require(json.loads(run(*plan_command)) == plan, f"{artifact.name}: plan recovery failed")

        config = cwd / "config"
        config.mkdir()
        (cwd / "skills").mkdir()
        (config / "skills.json").write_text("{", encoding="utf-8")
        run("skills", "list", status=2)
        report = json.loads(run("validate", "--format", "json", status=1))
        require(any(issue["code"] == "skills.config" for issue in report["issues"]), "invalid config was not reported")
        (config / "skills.json").unlink()
        require(run("skills", "list") == skills, f"{artifact.name}: packaged catalog recovery failed")
        print(f"Checked {artifact.name} outside the checkout (offline)")


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("distribution", type=Path)
    distribution = parser.parse_args().distribution.resolve()
    artifacts = []
    for pattern in ("*.whl", "*.tar.gz"):
        matches = sorted(distribution.glob(pattern))
        if len(matches) != 1:
            parser.error(f"expected exactly one {pattern} in {distribution}; found {len(matches)}")
        artifacts.append(matches[0])
    wheel, sdist = artifacts
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    check_contents(wheel, sdist, version)
    for artifact in artifacts:
        check(artifact, version)


if __name__ == "__main__":
    main()
