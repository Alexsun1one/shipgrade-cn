from __future__ import annotations

import py_compile
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise SystemExit(
            "command failed: "
            + " ".join(args)
            + "\n"
            + result.stdout
            + "\n"
            + result.stderr
        )
    return result.stdout


def cleanup_generated_python_metadata() -> None:
    for cache_dir in ROOT.rglob("__pycache__"):
        if cache_dir.is_dir():
            shutil.rmtree(cache_dir)
    for compiled in ROOT.rglob("*.pyc"):
        compiled.unlink(missing_ok=True)


def main() -> None:
    for tool in sorted((ROOT / "tools").glob("*.py")):
        py_compile.compile(str(tool), doraise=True)
    cleanup_generated_python_metadata()
    run([sys.executable, "tools/shipgrade_release_check.py"])
    run([sys.executable, "tools/shipgrade_doctor.py", "demo/demo-output.md"])
    cleanup_generated_python_metadata()
    print("shipgrade-verify-ok")


if __name__ == "__main__":
    main()
