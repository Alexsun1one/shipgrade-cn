#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = Path.home() / ".codex" / "skills" / "ship-grade-engineering-cn"
EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache"}
EXCLUDE_FILES = {".DS_Store"}


def ignore(_: str, names: list[str]) -> set[str]:
    ignored = set()
    for name in names:
        if name in EXCLUDE_DIRS or name in EXCLUDE_FILES or name.startswith("._"):
            ignored.add(name)
    return ignored


def main() -> None:
    parser = argparse.ArgumentParser(description="Install ShipGrade CN into an agent skill directory.")
    parser.add_argument("--target", default=str(DEFAULT_TARGET), help="target skill directory")
    parser.add_argument("--force", action="store_true", help="overwrite target if it exists")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if target.exists():
        if not args.force:
            raise SystemExit(f"target exists: {target}; pass --force to overwrite")
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(PACKAGE_ROOT, target, ignore=ignore)
    print(f"installed ship-grade-engineering-cn -> {target}")


if __name__ == "__main__":
    main()
