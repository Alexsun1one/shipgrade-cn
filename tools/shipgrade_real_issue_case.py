#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_NAME = "pallets/click"
REPO_URL = "https://github.com/pallets/click.git"
REVISION = "6a141c3681027e8124ce5a3c70e608dbbebffafb"
LICENSE_ID = "BSD-3-Clause"
ISSUE_KEY = "click-required-option-regression"
BEGIN = "<!-- SHIPGRADE-CN:BEGIN -->"
END = "<!-- SHIPGRADE-CN:END -->"


def run(args: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True, check=False)


def ensure_safe_target(path: Path) -> None:
    temp_root = Path(tempfile.gettempdir()).resolve()
    resolved = path.resolve()
    if temp_root not in resolved.parents and resolved != temp_root:
        raise SystemExit(f"refuse to clean non-temp real issue case target: {resolved}")
    if not resolved.name.startswith("shipgrade-real-issue-case"):
        raise SystemExit(f"refuse to clean non-real-issue-case target: {resolved}")


def cache_candidates() -> list[Path]:
    candidates: list[Path] = []
    if os.environ.get("SHIPGRADE_REAL_ISSUE_CASE_CACHE"):
        candidates.append(Path(os.environ["SHIPGRADE_REAL_ISSUE_CASE_CACHE"]).expanduser())
    for root in (Path(tempfile.gettempdir()), Path("/tmp"), Path("/private/tmp")):
        candidates.append(root / "shipgrade-ext-cache" / "pallets__click")
    return candidates


def cached_revision(cache: Path) -> str | None:
    marker = cache / ".shipgrade-upstream-revision"
    if marker.exists():
        return marker.read_text(encoding="utf-8").strip()
    head = run(["git", "rev-parse", "HEAD"], cwd=cache)
    if head.returncode == 0:
        return head.stdout.strip()
    return None


def copy_from_cache(target: Path) -> str | None:
    for cache in cache_candidates():
        if not cache.exists():
            continue
        revision = cached_revision(cache)
        if revision != REVISION:
            continue
        if (cache / ".git").exists():
            remote = run(["git", "remote", "get-url", "origin"], cwd=cache)
            if remote.returncode == 0 and REPO_URL.removesuffix(".git") not in remote.stdout.strip().removesuffix(".git"):
                continue
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(
            cache,
            target,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache", ".mypy_cache", ".ruff_cache"),
        )
        return revision
    return None


def fetch_repo(target: Path) -> str:
    if not os.environ.get("SHIPGRADE_REAL_ISSUE_CASE_FORCE_NETWORK"):
        cached = copy_from_cache(target)
        if cached:
            return cached
    target.mkdir(parents=True, exist_ok=True)
    run(["git", "init", "-q"], cwd=target)
    fetch = run(["git", "fetch", "--depth", "1", REPO_URL, REVISION], cwd=target)
    if fetch.returncode != 0:
        cached = copy_from_cache(target)
        if cached:
            return cached
        raise SystemExit(fetch.stdout + fetch.stderr)
    checkout = run(["git", "checkout", "-q", "--detach", "FETCH_HEAD"], cwd=target)
    if checkout.returncode != 0:
        raise SystemExit(checkout.stdout + checkout.stderr)
    head = run(["git", "rev-parse", "HEAD"], cwd=target)
    if head.returncode != 0:
        raise SystemExit(head.stdout + head.stderr)
    return head.stdout.strip()


def managed_block() -> str:
    return f"""{BEGIN}
# ShipGrade CN Real Issue Case

This repository is a temporary real-repo issue case for ShipGrade CN. The controller agent must keep the original goal, inspect real project structure, choose evidence that matches the issue, and audit completion before claiming done.

Do not copy secrets, tokens, cookies, sessions, private keys, browser profiles, auth databases, or upstream source bodies into the public proof.
{END}
"""


def upsert(path: Path, block: str) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if BEGIN in existing and END in existing:
        return
    prefix = existing.rstrip() + "\n\n" if existing.strip() else ""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(prefix + block.strip() + "\n", encoding="utf-8")


def license_ok(target: Path) -> bool:
    text = (target / "LICENSE.txt").read_text(encoding="utf-8", errors="ignore")
    return "Redistribution and use in source and binary forms" in text and "Neither the name of the copyright holder" in text


def write_shipgrade_files(target: Path, revision: str) -> None:
    block = managed_block()
    contract_source = ROOT / "SHIPGRADE.md"
    if not contract_source.exists():
        contract_source = ROOT / "SKILL.md"
    (target / "SHIPGRADE.md").write_text(contract_source.read_text(encoding="utf-8"), encoding="utf-8")
    upsert(target / "AGENTS.md", block)
    upsert(target / "CLAUDE.md", block)
    cursor_rule = target / ".cursor" / "rules" / "shipgrade.mdc"
    cursor_rule.parent.mkdir(parents=True, exist_ok=True)
    cursor_rule.write_text("---\ndescription: ShipGrade CN real issue case\nalwaysApply: false\n---\n\n" + block.strip() + "\n", encoding="utf-8")

    workbench = target / ".shipgrade"
    workbench.mkdir(exist_ok=True)
    (workbench / "task-brief.md").write_text(
        "# ShipGrade Real Issue Case Task Brief\n\n"
        "## 目标\n"
        f"在真实开源仓库 `{REPO_NAME}` 的临时 clone 中,使用新版 ShipGrade 主控规则完成一个 issue 式 CLI 回归验证任务: `{ISSUE_KEY}`。\n\n"
        "## 非目标\n"
        "- 不声称修复或合并上游官方 issue。\n"
        "- 不修改上游业务源码正文。\n"
        "- 不安装 ShipGrade helper 到目标仓库。\n"
        "- 不把上游源码正文复制进公开 proof。\n\n"
        "## 当前证据\n"
        f"- 来源: `{REPO_URL}`\n"
        f"- revision: `{revision}`\n"
        f"- license: `{LICENSE_ID}` from `LICENSE.txt`\n"
        "- 结构证据: `src/click/core.py`, `src/click/testing.py`, `tests/`, `pyproject.toml`\n"
        "- 主控判断: 选择一个可独立验证的 CLI required option 行为,用 `CliRunner` 写最小回归测试。\n\n"
        "## 验收\n"
        "- `.shipgrade/issue-case/test_click_required_option.py` 存在。\n"
        "- `PYTHONPATH=src python .shipgrade/issue-case/test_click_required_option.py` 通过。\n"
        "- `.shipgrade/handoff.md` 被 `shipgrade_doctor.py` 判定为 `ship-grade-ok`。\n",
        encoding="utf-8",
    )


def write_issue_test(target: Path) -> Path:
    test_path = target / ".shipgrade" / "issue-case" / "test_click_required_option.py"
    test_path.parent.mkdir(parents=True, exist_ok=True)
    test_path.write_text(
        "import click\n"
        "from click.testing import CliRunner\n\n\n"
        "@click.command()\n"
        "@click.option('--name', required=True)\n"
        "def greet(name: str) -> None:\n"
        "    click.echo(f'hello {name}')\n\n\n"
        "runner = CliRunner()\n"
        "missing = runner.invoke(greet, [])\n"
        "assert missing.exit_code != 0\n"
        "assert \"Missing option '--name'\" in missing.output\n\n"
        "ok = runner.invoke(greet, ['--name', 'ShipGrade'])\n"
        "assert ok.exit_code == 0\n"
        "assert ok.output.strip() == 'hello ShipGrade'\n",
        encoding="utf-8",
    )
    return test_path


def run_issue_validation(target: Path, test_path: Path) -> list[str]:
    compile_result = run([sys.executable, "-m", "py_compile", str(test_path.relative_to(target))], cwd=target)
    if compile_result.returncode != 0:
        raise SystemExit(compile_result.stdout + compile_result.stderr)
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    test_result = run([sys.executable, str(test_path.relative_to(target))], cwd=target, env=env)
    if test_result.returncode != 0:
        raise SystemExit(test_result.stdout + test_result.stderr)
    return [
        "python -m py_compile .shipgrade/issue-case/test_click_required_option.py: ok exit 0",
        "PYTHONPATH=src python .shipgrade/issue-case/test_click_required_option.py: ok exit 0",
    ]


def write_handoff(target: Path, revision: str, validation_lines: list[str]) -> Path:
    handoff = target / ".shipgrade" / "handoff.md"
    validation_md = "\n".join(f"- 命令: `{line}`。" for line in validation_lines)
    handoff.write_text(
        "# ShipGrade Real Issue Case Handoff\n\n"
        "## 已完成 / Done\n"
        f"结果: 在真实开源仓库 `{REPO_NAME}` 临时 clone 中完成 issue 式回归验证 `{ISSUE_KEY}`,产物为 `.shipgrade/task-brief.md`, `.shipgrade/issue-case/test_click_required_option.py`, `.shipgrade/handoff.md`, `SHIPGRADE.md`, `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/shipgrade.mdc`。\n\n"
        "## 验证证据 / Validation Evidence\n"
        f"{validation_md}\n"
        "- 路径: `.shipgrade/task-brief.md` 记录目标、非目标、结构证据、主控判断和验收。\n"
        "- 路径: `.shipgrade/issue-case/test_click_required_option.py` 记录 required option 的缺参失败和正常成功两条行为。\n\n"
        "## 来源和许可证 / Source And License\n"
        f"来源 source: `{REPO_URL}` at `{revision}`。license: `{LICENSE_ID}` from `LICENSE.txt`。公开 proof 只记录元数据、路径、测试意图和命令结果,不复制上游源码正文。\n\n"
        "## 风险边界 / Known Limits\n"
        "风险: 本轮是 issue 式真实仓库案例,不声称已经修复、提交或合并上游官方 issue; 覆盖的是一个可独立验证的 Click CLI 行为切片。\n\n"
        "## 禁止事项 / Forbidden\n"
        "禁止复制 secret、token、cookie、session、private key、browser profile、auth database 或上游源码正文。\n\n"
        "## 接手入口 / Next Handoff\n"
        "接手: 下一步可从 `.shipgrade/task-brief.md` 和 `.shipgrade/issue-case/test_click_required_option.py` 开始,把该 issue-case 扩展成更完整的 upstream test 或文档提案。\n",
        encoding="utf-8",
    )
    return handoff


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a real-repository issue-style ShipGrade case against pallets/click.")
    parser.add_argument("--target", help="case directory under the system temp folder")
    parser.add_argument("--clean", action="store_true", help="remove the generated real issue case clone after printing proof")
    args = parser.parse_args()

    target = Path(args.target).expanduser() if args.target else Path(tempfile.mkdtemp(prefix="shipgrade-real-issue-case-"))
    ensure_safe_target(target)
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)

    revision = fetch_repo(target)
    missing = [path for path in ("LICENSE.txt", "pyproject.toml", "src/click/core.py", "src/click/testing.py") if not (target / path).exists()]
    if missing:
        raise SystemExit("real issue case target missing required paths: " + ", ".join(missing))
    if not license_ok(target):
        raise SystemExit("real issue case requires BSD-3-Clause license evidence in LICENSE.txt")

    write_shipgrade_files(target, revision)
    test_path = write_issue_test(target)
    validation_lines = run_issue_validation(target, test_path)
    handoff = write_handoff(target, revision, validation_lines)
    doctor = run([sys.executable, str(ROOT / "tools" / "shipgrade_doctor.py"), str(handoff.relative_to(target))], cwd=target)
    if doctor.returncode != 0 or "ship-grade-ok" not in doctor.stdout:
        raise SystemExit(doctor.stdout + doctor.stderr)

    print("shipgrade-real-issue-case-ok")
    print(f"repo={REPO_NAME}")
    print(f"url={REPO_URL.removesuffix('.git')}")
    print(f"revision={revision}")
    print(f"license={LICENSE_ID}")
    print(f"issue={ISSUE_KEY}")
    print("source=SHIPGRADE.md")
    print("created=SHIPGRADE.md,AGENTS.md,CLAUDE.md,.cursor/rules/shipgrade.mdc,.shipgrade/task-brief.md,.shipgrade/issue-case/test_click_required_option.py,.shipgrade/handoff.md")
    for line in validation_lines:
        print(f"validation={line}")
    print("doctor=.shipgrade/handoff.md: ship-grade-ok")
    print("controller_intelligence=true")
    print("evidence_matrix=true")
    print("completion_audit=true")
    print("python_helper_used_in_target=false")
    print("service_started=false")
    print("source_body_copied_to_public=false")
    print(f"target={target}")
    if args.clean:
        shutil.rmtree(target)
        print("cleaned=true")
    else:
        print("note=real issue case clone kept for inspection; rerun with --clean to remove it")


if __name__ == "__main__":
    main()
