from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPO_URL = "https://github.com/pypa/sampleproject.git"
DEFAULT_REPO_NAME = "pypa/sampleproject"
DEFAULT_REVISION = "621e4974ca25ce531773def586ba3ed8e736b3fc"
CACHE_ENV = "SHIPGRADE_EXTERNAL_TRIAL_CACHE"
BEGIN = "<!-- SHIPGRADE-CN:BEGIN -->"
END = "<!-- SHIPGRADE-CN:END -->"


def run(args: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True, check=False)


def ensure_safe_target(path: Path) -> None:
    temp_root = Path(tempfile.gettempdir()).resolve()
    resolved = path.resolve()
    if temp_root not in resolved.parents and resolved != temp_root:
        raise SystemExit(f"refuse to clean non-temp external trial target: {resolved}")
    if not resolved.name.startswith("shipgrade-external-trial"):
        raise SystemExit(f"refuse to clean non-external-trial target: {resolved}")


def fetch_repo(target: Path, repo_url: str, revision: str) -> str:
    if not os.environ.get("SHIPGRADE_EXTERNAL_TRIAL_FORCE_NETWORK"):
        cached_head = copy_from_cache(target, repo_url, revision)
        if cached_head:
            return cached_head
    target.mkdir(parents=True, exist_ok=True)
    run(["git", "init", "-q"], cwd=target)
    fetch = run(["git", "fetch", "--depth", "1", repo_url, revision], cwd=target)
    if fetch.returncode != 0:
        cached_head = copy_from_cache(target, repo_url, revision)
        if cached_head:
            return cached_head
        raise SystemExit(fetch.stdout + fetch.stderr)
    checkout = run(["git", "checkout", "-q", "--detach", "FETCH_HEAD"], cwd=target)
    if checkout.returncode != 0:
        raise SystemExit(checkout.stdout + checkout.stderr)
    head = run(["git", "rev-parse", "HEAD"], cwd=target)
    if head.returncode != 0:
        raise SystemExit(head.stdout + head.stderr)
    return head.stdout.strip()


def cache_candidates() -> list[Path]:
    candidates: list[Path] = []
    if os.environ.get(CACHE_ENV):
        candidates.append(Path(os.environ[CACHE_ENV]).expanduser())
    candidates.append(Path(tempfile.gettempdir()) / "shipgrade-ext-probe-sampleproject")
    candidates.append(Path("/tmp") / "shipgrade-ext-probe-sampleproject")
    candidates.append(Path("/private/tmp") / "shipgrade-ext-probe-sampleproject")
    return candidates


def copy_from_cache(target: Path, repo_url: str, revision: str) -> str | None:
    for cache in cache_candidates():
        if not cache.exists() or not (cache / ".git").exists():
            continue
        head = run(["git", "rev-parse", "HEAD"], cwd=cache)
        remote = run(["git", "remote", "get-url", "origin"], cwd=cache)
        if head.returncode != 0 or remote.returncode != 0:
            continue
        if head.stdout.strip() != revision:
            continue
        if repo_url.removesuffix(".git") not in remote.stdout.strip().removesuffix(".git"):
            continue
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(cache, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))
        return head.stdout.strip()
    return None


def managed_block() -> str:
    return f"""{BEGIN}
# ShipGrade CN External Trial

This public repository was wired from `SHIPGRADE.md` only. Do not copy secrets, tokens, cookies, sessions, private keys, browser profiles, or private source bodies.

Every handoff must include:

```text
结果: concrete changed artifact/path/state
证据: command/test/build/browser/log/manual check and observed result
风险: bounded residual risk
接手: next file, command, issue, or decision point
```
{END}
"""


def upsert(path: Path, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if BEGIN in existing and END in existing:
        return
    prefix = existing.rstrip() + "\n\n" if existing.strip() else ""
    path.write_text(prefix + block.strip() + "\n", encoding="utf-8")


def write_trial_files(target: Path, repo_name: str, repo_url: str, revision: str, license_id: str) -> None:
    block = managed_block()
    (target / "SHIPGRADE.md").write_text((ROOT / "SHIPGRADE.md").read_text(encoding="utf-8"), encoding="utf-8")
    upsert(target / "AGENTS.md", block)
    upsert(target / "CLAUDE.md", block)
    cursor_rule = target / ".cursor" / "rules" / "shipgrade.mdc"
    cursor_rule.parent.mkdir(parents=True, exist_ok=True)
    cursor_rule.write_text("---\ndescription: ShipGrade CN external trial\nalwaysApply: false\n---\n\n" + block.strip() + "\n", encoding="utf-8")

    workbench = target / ".shipgrade"
    workbench.mkdir(exist_ok=True)
    (workbench / "task-brief.md").write_text(
        "# ShipGrade External Trial Task Brief\n\n"
        "## 目标\n"
        f"在公开仓库 `{repo_name}` 的临时 clone 中,只通过 `SHIPGRADE.md` 接入 ShipGrade CN 规则,并证明现有 Python 行为仍通过。\n\n"
        "## 非目标\n"
        "- 不改上游业务源码。\n"
        "- 不安装 ShipGrade Python helper 到目标仓库。\n"
        "- 不发布目标仓库内容到 ShipGrade 包。\n\n"
        "## 当前证据\n"
        f"- 来源: `{repo_url}`\n"
        f"- revision: `{revision}`\n"
        f"- license: `{license_id}`\n"
        "- 关键路径: `pyproject.toml`, `src/sample/simple.py`, `tests/test_simple.py`\n\n"
        "## 验收\n"
        "- `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/shipgrade.mdc` 带有 ShipGrade 托管规则块。\n"
        "- `.shipgrade/handoff.md` 被 `shipgrade_doctor.py` 判定为 `ship-grade-ok`。\n"
        "- `PYTHONPATH=src python -m unittest tests.test_simple` 通过。\n",
        encoding="utf-8",
    )


def run_target_validation(target: Path) -> tuple[str, str]:
    compile_result = run([sys.executable, "-m", "py_compile", "src/sample/simple.py"], cwd=target)
    if compile_result.returncode != 0:
        raise SystemExit(compile_result.stdout + compile_result.stderr)
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    unit_result = run([sys.executable, "-m", "unittest", "tests.test_simple"], cwd=target, env=env)
    if unit_result.returncode != 0:
        raise SystemExit(unit_result.stdout + unit_result.stderr)
    return "python -m py_compile src/sample/simple.py: ok exit 0", "PYTHONPATH=src python -m unittest tests.test_simple: ok exit 0"


def write_handoff(target: Path, repo_name: str, repo_url: str, revision: str, license_id: str, compile_line: str, unit_line: str) -> Path:
    handoff = target / ".shipgrade" / "handoff.md"
    handoff.write_text(
        "# ShipGrade External Trial Handoff\n\n"
        "## 已完成 / Done\n"
        f"结果: 在 `{repo_name}` 临时 clone 中完成 ShipGrade 零安装接入,生成 `SHIPGRADE.md`, `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/shipgrade.mdc`, `.shipgrade/task-brief.md`, `.shipgrade/handoff.md`。\n\n"
        "## 验证证据 / Validation Evidence\n"
        f"- 命令: `{compile_line}`。\n"
        f"- 命令: `{unit_line}`。\n"
        "- 路径: `.shipgrade/task-brief.md` 包含目标、非目标、证据和验收。\n"
        "- 路径: `AGENTS.md` 和 `CLAUDE.md` 包含 `SHIPGRADE-CN:BEGIN` 托管规则块。\n\n"
        "## 来源和许可证 / Source And License\n"
        f"来源 source: `{repo_url}` at `{revision}`。license: `{license_id}` from `LICENSE.txt`。ShipGrade 公开包只记录元数据、路径和命令结果。\n\n"
        "## 风险边界 / Known Limits\n"
        "风险: 本轮只验证外部小型 Python 仓库的规则接入、既有单测和 handoff 审核; 业务源码保持原样,打包发布流程留给后续任务。\n\n"
        "## 禁止事项 / Forbidden\n"
        "禁止复制 secret、token、cookie、session、private key、browser profile、auth database 或私有源码正文。\n\n"
        "## 接手入口 / Next Handoff\n"
        "接手: 下一步可从 `.shipgrade/task-brief.md` 开始,为真实 issue 增加最小源码改动,再复跑 `PYTHONPATH=src python -m unittest tests.test_simple`。\n",
        encoding="utf-8",
    )
    return handoff


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a zero-install ShipGrade trial against a small public repository.")
    parser.add_argument("--repo-url", default=DEFAULT_REPO_URL)
    parser.add_argument("--repo-name", default=DEFAULT_REPO_NAME)
    parser.add_argument("--revision", default=DEFAULT_REVISION)
    parser.add_argument("--target", help="trial directory under the system temp folder")
    parser.add_argument("--clean", action="store_true", help="remove the generated external trial clone after printing proof")
    args = parser.parse_args()

    target = Path(args.target).expanduser() if args.target else Path(tempfile.mkdtemp(prefix="shipgrade-external-trial-"))
    ensure_safe_target(target)
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)

    head = fetch_repo(target, args.repo_url, args.revision)
    license_text = (target / "LICENSE.txt").read_text(encoding="utf-8", errors="ignore")
    license_id = "MIT" if "Permission is hereby granted, free of charge" in license_text and "THE SOFTWARE IS PROVIDED" in license_text else "UNKNOWN"
    if license_id != "MIT":
        raise SystemExit("external trial requires MIT license evidence in LICENSE.txt")

    required_paths = ["pyproject.toml", "src/sample/simple.py", "tests/test_simple.py", "LICENSE.txt"]
    missing = [rel for rel in required_paths if not (target / rel).exists()]
    if missing:
        raise SystemExit("external trial target missing required paths: " + ", ".join(missing))

    write_trial_files(target, args.repo_name, args.repo_url, head, license_id)
    compile_line, unit_line = run_target_validation(target)
    handoff = write_handoff(target, args.repo_name, args.repo_url, head, license_id, compile_line, unit_line)
    doctor = run([sys.executable, str(ROOT / "tools" / "shipgrade_doctor.py"), str(handoff.relative_to(target))], cwd=target)
    if doctor.returncode != 0 or "ship-grade-ok" not in doctor.stdout:
        raise SystemExit(doctor.stdout + doctor.stderr)

    tracked = run(["git", "ls-files"], cwd=target)
    tracked_count = len([line for line in tracked.stdout.splitlines() if line.strip()]) if tracked.returncode == 0 else 0

    print("shipgrade-external-trial-ok")
    print(f"repo={args.repo_name}")
    print(f"url={args.repo_url.removesuffix('.git')}")
    print(f"revision={head}")
    print(f"license={license_id}")
    print(f"tracked_files={tracked_count}")
    print("source=SHIPGRADE.md")
    print("created=SHIPGRADE.md,AGENTS.md,CLAUDE.md,.cursor/rules/shipgrade.mdc,.shipgrade/task-brief.md,.shipgrade/handoff.md")
    print(f"validation={compile_line}")
    print(f"validation={unit_line}")
    print("doctor=.shipgrade/handoff.md: ship-grade-ok")
    print("python_helper_used_in_target=false")
    print("service_started=false")
    print("source_body_copied_to_public=false")
    print(f"target={target}")
    if args.clean:
        shutil.rmtree(target)
        print("cleaned=true")
    else:
        print("note=external trial clone kept for inspection; rerun with --clean to remove it")


if __name__ == "__main__":
    main()
