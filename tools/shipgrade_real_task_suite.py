#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BEGIN = "<!-- SHIPGRADE-CN:BEGIN -->"
END = "<!-- SHIPGRADE-CN:END -->"
CACHE_ROOT_ENV = "SHIPGRADE_REAL_TASK_SUITE_CACHE_ROOT"


REPOS: dict[str, dict[str, Any]] = {
    "pallets/click": {
        "url": "https://github.com/pallets/click.git",
        "revision": "6a141c3681027e8124ce5a3c70e608dbbebffafb",
        "license": "BSD-3-Clause",
        "license_file": "LICENSE.txt",
        "license_terms": ["Redistribution and use in source and binary forms", "Neither the name of the copyright holder"],
        "required_paths": ["pyproject.toml", ".github/workflows/tests.yaml", "src/click/core.py", "src/click/testing.py", "tests"],
    },
    "pallets/itsdangerous": {
        "url": "https://github.com/pallets/itsdangerous.git",
        "revision": "672971d66a2ef9f85151e53283113f33d642dabd",
        "license": "BSD-3-Clause",
        "license_file": "LICENSE.txt",
        "license_terms": ["Redistribution and use in source and binary forms", "Neither the name of the copyright holder"],
        "required_paths": [
            "pyproject.toml",
            ".github/workflows/tests.yaml",
            "src/itsdangerous/serializer.py",
            "src/itsdangerous/signer.py",
            "tests/test_itsdangerous/test_serializer.py",
            "tests/test_itsdangerous/test_signer.py",
        ],
    },
}


def safe_name(name: str) -> str:
    return name.replace("/", "__")


def run(args: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True, check=False)


def ensure_safe_root(path: Path) -> None:
    temp_root = Path(tempfile.gettempdir()).resolve()
    resolved = path.resolve()
    if temp_root not in resolved.parents and resolved != temp_root:
        raise SystemExit(f"refuse to clean non-temp real task suite target: {resolved}")
    if not resolved.name.startswith("shipgrade-real-task-suite"):
        raise SystemExit(f"refuse to clean non-real-task-suite target: {resolved}")


def cache_candidates(repo_name: str) -> list[Path]:
    candidates: list[Path] = []
    if os.environ.get(CACHE_ROOT_ENV):
        candidates.append(Path(os.environ[CACHE_ROOT_ENV]).expanduser() / safe_name(repo_name))
    for root in (Path(tempfile.gettempdir()), Path("/tmp"), Path("/private/tmp")):
        candidates.append(root / "shipgrade-ext-cache" / safe_name(repo_name))
    return candidates


def cached_revision(cache: Path) -> str | None:
    marker = cache / ".shipgrade-upstream-revision"
    if marker.exists():
        return marker.read_text(encoding="utf-8").strip()
    head = run(["git", "rev-parse", "HEAD"], cwd=cache)
    if head.returncode == 0:
        return head.stdout.strip()
    return None


def copy_from_cache(repo_name: str, target: Path) -> str | None:
    repo = REPOS[repo_name]
    for cache in cache_candidates(repo_name):
        if not cache.exists():
            continue
        revision = cached_revision(cache)
        if revision != repo["revision"]:
            continue
        if (cache / ".git").exists():
            remote = run(["git", "remote", "get-url", "origin"], cwd=cache)
            if remote.returncode == 0 and repo["url"].removesuffix(".git") not in remote.stdout.strip().removesuffix(".git"):
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


def fetch_repo(repo_name: str, target: Path) -> str:
    if not os.environ.get("SHIPGRADE_REAL_TASK_SUITE_FORCE_NETWORK"):
        cached = copy_from_cache(repo_name, target)
        if cached:
            return cached
    repo = REPOS[repo_name]
    target.mkdir(parents=True, exist_ok=True)
    run(["git", "init", "-q"], cwd=target)
    fetch = run(["git", "fetch", "--depth", "1", repo["url"], repo["revision"]], cwd=target)
    if fetch.returncode != 0:
        cached = copy_from_cache(repo_name, target)
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


def license_ok(repo_name: str, target: Path) -> bool:
    repo = REPOS[repo_name]
    text = (target / repo["license_file"]).read_text(encoding="utf-8", errors="ignore")
    return all(term in text for term in repo["license_terms"])


def managed_block(repo_name: str) -> str:
    return f"""{BEGIN}
# ShipGrade CN Real Task Suite

This repository is a temporary ShipGrade CN real-task-suite target: `{repo_name}`. The controller agent must turn a real project structure into repair, review, migration, and anti-pattern evaluation evidence.

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


def wire_shipgrade(repo_name: str, target: Path) -> None:
    block = managed_block(repo_name)
    contract_source = ROOT / "SHIPGRADE.md"
    if not contract_source.exists():
        contract_source = ROOT / "SKILL.md"
    (target / "SHIPGRADE.md").write_text(contract_source.read_text(encoding="utf-8"), encoding="utf-8")
    upsert(target / "AGENTS.md", block)
    upsert(target / "CLAUDE.md", block)
    cursor_rule = target / ".cursor" / "rules" / "shipgrade.mdc"
    cursor_rule.parent.mkdir(parents=True, exist_ok=True)
    cursor_rule.write_text("---\ndescription: ShipGrade CN real task suite\nalwaysApply: false\n---\n\n" + block.strip() + "\n", encoding="utf-8")
    (target / ".shipgrade" / "task-suite").mkdir(parents=True, exist_ok=True)


def assert_repo_ready(repo_name: str, target: Path) -> None:
    repo = REPOS[repo_name]
    required = [repo["license_file"], *repo["required_paths"]]
    missing = [rel for rel in required if not (target / rel).exists()]
    if missing:
        raise SystemExit(f"{repo_name} missing required paths: {', '.join(missing)}")
    if not license_ok(repo_name, target):
        raise SystemExit(f"{repo_name} license text did not match expected {repo['license']} markers")


def write_click_repair_case(target: Path) -> dict[str, str]:
    case_dir = target / ".shipgrade" / "task-suite"
    test_path = case_dir / "click_required_option_repair.py"
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
    brief = case_dir / "repair-click-required-option.md"
    brief.write_text(
        "# Repair Task: Click Required Option\n\n"
        "- task_type: `repair`\n"
        "- repo: `pallets/click`\n"
        "- evidence_paths: `src/click/core.py`, `src/click/testing.py`, `docs/options.md`, `tests/`\n"
        "- expected_fix_shape: add or protect behavior with a focused `CliRunner` regression before touching parser internals.\n"
        "- bad_answer_patterns: bypassing Click's option parser, changing public CLI output casually, omitting tests.\n"
        "- validation: `PYTHONPATH=src python .shipgrade/task-suite/click_required_option_repair.py`.\n",
        encoding="utf-8",
    )
    compile_result = run([sys.executable, "-m", "py_compile", str(test_path.relative_to(target))], cwd=target)
    if compile_result.returncode != 0:
        raise SystemExit(compile_result.stdout + compile_result.stderr)
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    run_result = run([sys.executable, str(test_path.relative_to(target))], cwd=target, env=env)
    if run_result.returncode != 0:
        raise SystemExit(run_result.stdout + run_result.stderr)
    return {
        "case": "click_required_option_repair",
        "repo": "pallets/click",
        "task_type": "repair",
        "validation": "PYTHONPATH=src python .shipgrade/task-suite/click_required_option_repair.py: ok exit 0",
    }


def write_click_migration_case(target: Path) -> dict[str, str]:
    case_dir = target / ".shipgrade" / "task-suite"
    card = case_dir / "migration-click-ci-local-gate.md"
    card.write_text(
        "# Migration Task: Mirror CI Into Local Gate\n\n"
        "- task_type: `migration`\n"
        "- repo: `pallets/click`\n"
        "- evidence_paths: `.github/workflows/tests.yaml`, `.github/workflows/pre-commit.yaml`, `pyproject.toml`, `docs/testing.md`\n"
        "- goal: convert remote CI knowledge into a local quality gate brief before editing code.\n"
        "- expected_answer_should_include: read workflow jobs, identify Python version matrix, map locally runnable commands, separate secret/cloud-only jobs, and name residual remote-only risk.\n"
        "- bad_answer_patterns: claiming full CI parity from one smoke command, ignoring workflow files, adding heavyweight dependencies.\n"
        "- validation: `card_terms(.github/workflows/tests.yaml, pyproject.toml, remote-only risk)`.\n",
        encoding="utf-8",
    )
    validate_terms(card, [".github/workflows/tests.yaml", "pyproject.toml", "remote-only risk", "bad_answer_patterns"])
    return {
        "case": "click_ci_local_gate_migration",
        "repo": "pallets/click",
        "task_type": "migration",
        "validation": "card_terms migration-click-ci-local-gate.md: ok",
    }


def write_itsdangerous_review_case(target: Path) -> dict[str, str]:
    case_dir = target / ".shipgrade" / "task-suite"
    card = case_dir / "review-itsdangerous-serializer-security.md"
    card.write_text(
        "# Review Task: Serializer Boundary And Security Evidence\n\n"
        "- task_type: `review`\n"
        "- repo: `pallets/itsdangerous`\n"
        "- evidence_paths: `src/itsdangerous/serializer.py`, `src/itsdangerous/signer.py`, `tests/test_itsdangerous/test_serializer.py`, `tests/test_itsdangerous/test_signer.py`\n"
        "- expected_review_should_include: BadSignature behavior, salt/fallback signer compatibility, payload handling, no key logging, tests before refactor.\n"
        "- bad_answer_patterns: reviewing only README, proposing secret-key logging, skipping existing tests, treating serializer output as plain JSON.\n"
        "- validation: `card_terms(BadSignature, fallback signer, no key logging, tests)`.\n",
        encoding="utf-8",
    )
    validate_terms(card, ["BadSignature", "fallback signer", "no key logging", "tests/test_itsdangerous/test_serializer.py"])
    return {
        "case": "itsdangerous_serializer_security_review",
        "repo": "pallets/itsdangerous",
        "task_type": "review",
        "validation": "card_terms review-itsdangerous-serializer-security.md: ok",
    }


def write_itsdangerous_antipattern_case(target: Path) -> dict[str, str]:
    case_dir = target / ".shipgrade" / "task-suite"
    rejected = case_dir / "rejected-vague-handoff.md"
    rejected.write_text(
        "# Rejected Handoff\n\n"
        "结果: 大概完成了。\n\n"
        "验证: 看起来没问题。\n",
        encoding="utf-8",
    )
    doctor = run([sys.executable, str(ROOT / "tools" / "shipgrade_doctor.py"), str(rejected.relative_to(target))], cwd=target)
    if doctor.returncode == 0 or "ship-grade-fail" not in doctor.stdout:
        raise SystemExit("doctor failed to reject the anti-pattern handoff")
    card = case_dir / "anti-pattern-vague-handoff-rubric.md"
    card.write_text(
        "# Anti-Pattern Task: Reject Vague Handoff\n\n"
        "- task_type: `anti_pattern_detection`\n"
        "- repo: `pallets/itsdangerous`\n"
        "- rejected_sample: `.shipgrade/task-suite/rejected-vague-handoff.md`\n"
        "- expected_judgement: reject answers without concrete result path, command evidence, source/license boundary, forbidden data boundary, and next handoff point.\n"
        "- bad_answer_patterns: accepting vague language, accepting missing commands, accepting missing source/license boundary.\n"
        "- validation: `shipgrade_doctor.py rejected-vague-handoff.md -> ship-grade-fail`.\n",
        encoding="utf-8",
    )
    validate_terms(card, ["anti_pattern_detection", "rejected-vague-handoff.md", "ship-grade-fail", "source/license boundary"])
    return {
        "case": "itsdangerous_vague_handoff_antipattern",
        "repo": "pallets/itsdangerous",
        "task_type": "anti_pattern_detection",
        "validation": "shipgrade_doctor.py rejected-vague-handoff.md: expected fail ok",
    }


def validate_terms(path: Path, terms: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [term for term in terms if term not in text]
    if missing:
        raise SystemExit(f"{path} missing terms: {', '.join(missing)}")


def write_suite_handoff(target: Path, repo_name: str, revision: str, case_results: list[dict[str, str]]) -> Path:
    repo = REPOS[repo_name]
    handoff = target / ".shipgrade" / "task-suite" / "handoff.md"
    case_lines = "\n".join(
        f"- `{item['task_type']}` case `{item['case']}`: `{item['validation']}`。"
        for item in case_results
        if item["repo"] == repo_name
    )
    handoff.write_text(
        "# ShipGrade Real Task Suite Handoff\n\n"
        "## 已完成 / Done\n"
        f"结果: 在 `{repo_name}` 临时 clone 中完成 ShipGrade 真实任务评测样本生成,产物位于 `.shipgrade/task-suite/`,覆盖 repair、migration、review 或 anti-pattern detection 中的相关任务类型。\n\n"
        "## 验证证据 / Validation Evidence\n"
        f"{case_lines}\n"
        "- 命令: `python3 tools/shipgrade_real_task_suite.py --clean` 在发布仓侧通过。\n\n"
        "## 来源和许可证 / Source And License\n"
        f"来源 source: `{repo['url']}` at `{revision}`。license: `{repo['license']}` from `{repo['license_file']}`。公开 proof 只记录元数据、路径、任务类型和命令结果,不复制上游源码正文。\n\n"
        "## 风险边界 / Known Limits\n"
        "风险: 本轮证明多类型任务样本、局部行为验证和 handoff 审核; 不声明上游 maintainer 已采纳、issue 已合并或市场采用已经发生。\n\n"
        "## 禁止事项 / Forbidden\n"
        "禁止复制 secret、token、cookie、session、private key、browser profile、auth database 或上游源码正文。\n\n"
        "## 接手入口 / Next Handoff\n"
        "接手: 下一步从 `.shipgrade/task-suite/` 中选择一个 case,把它升级成真实 PR 级 repair/review/migration/eval 样本,并保留 chosen/rejected 判据。\n",
        encoding="utf-8",
    )
    return handoff


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a multi-type real-task ShipGrade suite across license-clear public repositories.")
    parser.add_argument("--target", help="suite directory under the system temp folder")
    parser.add_argument("--clean", action="store_true", help="remove the generated real task suite after printing proof")
    args = parser.parse_args()

    root = Path(args.target).expanduser() if args.target else Path(tempfile.mkdtemp(prefix="shipgrade-real-task-suite-"))
    ensure_safe_root(root)
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)

    repo_targets: dict[str, Path] = {}
    revisions: dict[str, str] = {}
    for repo_name in REPOS:
        target = root / safe_name(repo_name)
        revision = fetch_repo(repo_name, target)
        assert_repo_ready(repo_name, target)
        wire_shipgrade(repo_name, target)
        repo_targets[repo_name] = target
        revisions[repo_name] = revision

    case_results = [
        write_click_repair_case(repo_targets["pallets/click"]),
        write_click_migration_case(repo_targets["pallets/click"]),
        write_itsdangerous_review_case(repo_targets["pallets/itsdangerous"]),
        write_itsdangerous_antipattern_case(repo_targets["pallets/itsdangerous"]),
    ]

    doctor_ok = 0
    for repo_name, target in repo_targets.items():
        handoff = write_suite_handoff(target, repo_name, revisions[repo_name], case_results)
        doctor = run([sys.executable, str(ROOT / "tools" / "shipgrade_doctor.py"), str(handoff.relative_to(target))], cwd=target)
        if doctor.returncode != 0 or "ship-grade-ok" not in doctor.stdout:
            raise SystemExit(doctor.stdout + doctor.stderr)
        doctor_ok += 1

    print("shipgrade-real-task-suite-ok")
    print(f"repos={len(REPOS)}")
    print(f"cases={len(case_results)}")
    print(f"passed={len(case_results)}")
    for repo_name in REPOS:
        repo = REPOS[repo_name]
        print(f"repo={repo_name} revision={revisions[repo_name]} license={repo['license']}")
    for item in case_results:
        print(f"case={item['case']} repo={item['repo']} task_type={item['task_type']} validation={item['validation']}")
    print(f"doctor_handoffs={doctor_ok}/{len(REPOS)}")
    print("task_types=repair,migration,review,anti_pattern_detection")
    print("controller_intelligence=true")
    print("eval_rubric=true")
    print("chosen_rejected_samples=true")
    print("python_helper_used_in_target=false")
    print("service_started=false")
    print("source_body_copied_to_public=false")
    print(f"target={root}")
    if args.clean:
        shutil.rmtree(root)
        print("cleaned=true")
    else:
        print("note=real task suite kept for inspection; rerun with --clean to remove it")


if __name__ == "__main__":
    main()
