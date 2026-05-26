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
CACHE_ROOT_ENV = "SHIPGRADE_MULTI_REPO_EVAL_CACHE_ROOT"


CASES: list[dict[str, Any]] = [
    {
        "name": "pypa/sampleproject",
        "url": "https://github.com/pypa/sampleproject.git",
        "revision": "621e4974ca25ce531773def586ba3ed8e736b3fc",
        "license": "MIT",
        "license_file": "LICENSE.txt",
        "license_terms": ["Permission is hereby granted, free of charge", "THE SOFTWARE IS PROVIDED"],
        "required_paths": ["pyproject.toml", "src/sample/simple.py", "tests/test_simple.py"],
        "validations": [
            {"label": "python -m py_compile src/sample/simple.py", "args": ["-m", "py_compile", "src/sample/simple.py"]},
            {"label": "PYTHONPATH=src python -m unittest tests.test_simple", "args": ["-m", "unittest", "tests.test_simple"], "env": {"PYTHONPATH": "src"}},
        ],
    },
    {
        "name": "pallets/click",
        "url": "https://github.com/pallets/click.git",
        "revision": "6a141c3681027e8124ce5a3c70e608dbbebffafb",
        "license": "BSD-3-Clause",
        "license_file": "LICENSE.txt",
        "license_terms": ["Redistribution and use in source and binary forms", "Neither the name of the copyright holder"],
        "required_paths": ["pyproject.toml", "src/click/core.py", "src/click/testing.py"],
        "validations": [
            {"label": "python -m py_compile src/click/core.py src/click/decorators.py src/click/testing.py", "args": ["-m", "py_compile", "src/click/core.py", "src/click/decorators.py", "src/click/testing.py"]},
            {
                "label": "PYTHONPATH=src python -c click CliRunner smoke",
                "args": [
                    "-c",
                    "import click\n@click.command()\ndef hi():\n    click.echo('hi')\nfrom click.testing import CliRunner\nr=CliRunner().invoke(hi, [])\nassert r.exit_code == 0 and r.output.strip() == 'hi'",
                ],
                "env": {"PYTHONPATH": "src"},
            },
        ],
    },
    {
        "name": "pallets/itsdangerous",
        "url": "https://github.com/pallets/itsdangerous.git",
        "revision": "672971d66a2ef9f85151e53283113f33d642dabd",
        "license": "BSD-3-Clause",
        "license_file": "LICENSE.txt",
        "license_terms": ["Redistribution and use in source and binary forms", "Neither the name of the copyright holder"],
        "required_paths": ["pyproject.toml", "src/itsdangerous/serializer.py", "src/itsdangerous/url_safe.py"],
        "validations": [
            {"label": "python -m py_compile src/itsdangerous/serializer.py src/itsdangerous/url_safe.py src/itsdangerous/signer.py", "args": ["-m", "py_compile", "src/itsdangerous/serializer.py", "src/itsdangerous/url_safe.py", "src/itsdangerous/signer.py"]},
            {
                "label": "PYTHONPATH=src python -c itsdangerous serializer roundtrip",
                "args": [
                    "-c",
                    "from itsdangerous import URLSafeSerializer\ns=URLSafeSerializer('shipgrade-secret')\nt=s.dumps({'id': 1})\nassert s.loads(t)['id'] == 1",
                ],
                "env": {"PYTHONPATH": "src"},
            },
        ],
    },
]


def safe_name(name: str) -> str:
    return name.replace("/", "__")


def run(args: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True, check=False)


def ensure_safe_root(path: Path) -> None:
    temp_root = Path(tempfile.gettempdir()).resolve()
    resolved = path.resolve()
    if temp_root not in resolved.parents and resolved != temp_root:
        raise SystemExit(f"refuse to clean non-temp multi-repo eval target: {resolved}")
    if not resolved.name.startswith("shipgrade-multi-repo-eval"):
        raise SystemExit(f"refuse to clean non-multi-repo-eval target: {resolved}")


def cache_candidates(case: dict[str, Any]) -> list[Path]:
    candidates: list[Path] = []
    if os.environ.get(CACHE_ROOT_ENV):
        candidates.append(Path(os.environ[CACHE_ROOT_ENV]).expanduser() / safe_name(case["name"]))
    for root in (Path(tempfile.gettempdir()), Path("/tmp"), Path("/private/tmp")):
        candidates.append(root / "shipgrade-ext-cache" / safe_name(case["name"]))
    if case["name"] == "pypa/sampleproject":
        for root in (Path(tempfile.gettempdir()), Path("/tmp"), Path("/private/tmp")):
            candidates.append(root / "shipgrade-ext-probe-sampleproject")
    return candidates


def cached_revision(cache: Path) -> str | None:
    marker = cache / ".shipgrade-upstream-revision"
    if marker.exists():
        return marker.read_text(encoding="utf-8").strip()
    head = run(["git", "rev-parse", "HEAD"], cwd=cache)
    if head.returncode == 0:
        return head.stdout.strip()
    return None


def copy_from_cache(case: dict[str, Any], target: Path) -> str | None:
    for cache in cache_candidates(case):
        if not cache.exists():
            continue
        revision = cached_revision(cache)
        if revision != case["revision"]:
            continue
        if (cache / ".git").exists():
            remote = run(["git", "remote", "get-url", "origin"], cwd=cache)
            if remote.returncode == 0 and case["url"].removesuffix(".git") not in remote.stdout.strip().removesuffix(".git"):
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


def fetch_case(case: dict[str, Any], target: Path) -> str:
    if not os.environ.get("SHIPGRADE_MULTI_REPO_EVAL_FORCE_NETWORK"):
        cached = copy_from_cache(case, target)
        if cached:
            return cached
    target.mkdir(parents=True, exist_ok=True)
    run(["git", "init", "-q"], cwd=target)
    fetch = run(["git", "fetch", "--depth", "1", case["url"], case["revision"]], cwd=target)
    if fetch.returncode != 0:
        cached = copy_from_cache(case, target)
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


def license_ok(case: dict[str, Any], target: Path) -> bool:
    text = (target / case["license_file"]).read_text(encoding="utf-8", errors="ignore")
    return all(term in text for term in case["license_terms"])


def managed_block(case: dict[str, Any]) -> str:
    return f"""{BEGIN}
# ShipGrade CN Multi-Repo Eval

This repository is part of the ShipGrade CN external eval set: `{case["name"]}`. It was wired from `SHIPGRADE.md` only.

Do not copy secrets, tokens, cookies, sessions, private keys, browser profiles, auth databases, or upstream source bodies into the public proof.

Every handoff must include result, validation evidence, source/license boundary, residual risk, forbidden data boundary, and next handoff point.
{END}
"""


def upsert(path: Path, block: str) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if BEGIN in existing and END in existing:
        return
    prefix = existing.rstrip() + "\n\n" if existing.strip() else ""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(prefix + block.strip() + "\n", encoding="utf-8")


def write_trial_files(case: dict[str, Any], target: Path, revision: str) -> None:
    block = managed_block(case)
    (target / "SHIPGRADE.md").write_text((ROOT / "SHIPGRADE.md").read_text(encoding="utf-8"), encoding="utf-8")
    upsert(target / "AGENTS.md", block)
    upsert(target / "CLAUDE.md", block)
    cursor_rule = target / ".cursor" / "rules" / "shipgrade.mdc"
    cursor_rule.parent.mkdir(parents=True, exist_ok=True)
    cursor_rule.write_text("---\ndescription: ShipGrade CN multi-repo eval\nalwaysApply: false\n---\n\n" + block.strip() + "\n", encoding="utf-8")
    workbench = target / ".shipgrade"
    workbench.mkdir(exist_ok=True)
    required = ", ".join(f"`{path}`" for path in case["required_paths"])
    validations = "\n".join(f"- `{item['label']}`" for item in case["validations"])
    (workbench / "task-brief.md").write_text(
        "# ShipGrade Multi-Repo Eval Task Brief\n\n"
        "## 目标\n"
        f"在 `{case['name']}` 临时 clone 中只通过 `SHIPGRADE.md` 接入 ShipGrade CN,并完成仓库原生轻量验证。\n\n"
        "## 非目标\n"
        "- 不修改上游业务源码。\n"
        "- 不安装 ShipGrade helper 到目标仓库。\n"
        "- 不把上游源码正文复制进公开 proof。\n\n"
        "## 当前证据\n"
        f"- 来源: `{case['url']}`\n"
        f"- revision: `{revision}`\n"
        f"- license: `{case['license']}`\n"
        f"- required paths: {required}\n\n"
        "## 验收\n"
        "- agent 规则文件带有 `SHIPGRADE-CN:BEGIN`。\n"
        "- `.shipgrade/handoff.md` 被 `shipgrade_doctor.py` 判定为 `ship-grade-ok`。\n"
        f"{validations}\n",
        encoding="utf-8",
    )


def run_validations(case: dict[str, Any], target: Path) -> list[str]:
    lines: list[str] = []
    for item in case["validations"]:
        env = os.environ.copy()
        env.update(item.get("env", {}))
        args = [sys.executable] + item["args"]
        result = run(args, cwd=target, env=env)
        if result.returncode != 0:
            raise SystemExit(f"{case['name']} validation failed: {item['label']}\n{result.stdout}\n{result.stderr}")
        lines.append(f"{item['label']}: ok exit 0")
    return lines


def write_handoff(case: dict[str, Any], target: Path, revision: str, validation_lines: list[str]) -> Path:
    handoff = target / ".shipgrade" / "handoff.md"
    validation_md = "\n".join(f"- 命令: `{line}`。" for line in validation_lines)
    handoff.write_text(
        "# ShipGrade Multi-Repo Eval Handoff\n\n"
        "## 已完成 / Done\n"
        f"结果: 在 `{case['name']}` 临时 clone 中完成 ShipGrade 零安装接入,生成 `SHIPGRADE.md`, `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/shipgrade.mdc`, `.shipgrade/task-brief.md`, `.shipgrade/handoff.md`。\n\n"
        "## 验证证据 / Validation Evidence\n"
        f"{validation_md}\n"
        "- 路径: `.shipgrade/task-brief.md` 包含目标、非目标、证据和验收。\n"
        "- 路径: `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/shipgrade.mdc` 包含 `SHIPGRADE-CN:BEGIN`。\n\n"
        "## 来源和许可证 / Source And License\n"
        f"来源 source: `{case['url']}` at `{revision}`。license: `{case['license']}` from `{case['license_file']}`。公开 proof 只记录元数据、路径和命令结果。\n\n"
        "## 风险边界 / Known Limits\n"
        "风险: 本轮验证零安装接入、轻量原生检查和 handoff 审核; 未声称真实用户采用、完整测试矩阵或上游发布流程完成。\n\n"
        "## 禁止事项 / Forbidden\n"
        "禁止复制 secret、token、cookie、session、private key、browser profile、auth database 或上游源码正文。\n\n"
        "## 接手入口 / Next Handoff\n"
        "接手: 下一步可从 `.shipgrade/task-brief.md` 选择真实 issue,完成最小源码改动后复跑本 handoff 中列出的验证命令。\n",
        encoding="utf-8",
    )
    return handoff


def run_case(case: dict[str, Any], root: Path) -> dict[str, Any]:
    target = root / safe_name(case["name"])
    revision = fetch_case(case, target)
    required = [case["license_file"], *case["required_paths"]]
    missing = [path for path in required if not (target / path).exists()]
    if missing:
        raise SystemExit(f"{case['name']} missing required paths: {', '.join(missing)}")
    if not license_ok(case, target):
        raise SystemExit(f"{case['name']} license text did not match expected {case['license']} markers")
    write_trial_files(case, target, revision)
    validation_lines = run_validations(case, target)
    handoff = write_handoff(case, target, revision, validation_lines)
    doctor = run([sys.executable, str(ROOT / "tools" / "shipgrade_doctor.py"), str(handoff.relative_to(target))], cwd=target)
    if doctor.returncode != 0 or "ship-grade-ok" not in doctor.stdout:
        raise SystemExit(doctor.stdout + doctor.stderr)
    tracked = run(["git", "ls-files"], cwd=target)
    tracked_count = len([line for line in tracked.stdout.splitlines() if line.strip()]) if tracked.returncode == 0 else 0
    return {
        "name": case["name"],
        "url": case["url"].removesuffix(".git"),
        "revision": revision,
        "license": case["license"],
        "tracked_files": tracked_count,
        "validation_count": len(validation_lines),
        "validation_lines": validation_lines,
        "doctor": ".shipgrade/handoff.md: ship-grade-ok",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run ShipGrade zero-install eval across multiple small public repositories.")
    parser.add_argument("--target", help="eval root under the system temp folder")
    parser.add_argument("--clean", action="store_true", help="remove the generated multi-repo eval root after printing proof")
    args = parser.parse_args()

    root = Path(args.target).expanduser() if args.target else Path(tempfile.mkdtemp(prefix="shipgrade-multi-repo-eval-"))
    ensure_safe_root(root)
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)

    results = [run_case(case, root) for case in CASES]
    passed = len(results)
    print("shipgrade-multi-repo-eval-ok")
    print(f"cases={len(CASES)}")
    print(f"passed={passed}")
    for result in results:
        print(f"case={result['name']} revision={result['revision']} license={result['license']} validations={result['validation_count']} doctor=ship-grade-ok")
        for line in result["validation_lines"]:
            print(f"validation={result['name']} :: {line}")
    print("source=SHIPGRADE.md")
    print("python_helper_used_in_target=false")
    print("service_started=false")
    print("source_body_copied_to_public=false")
    print(f"target={root}")
    if args.clean:
        shutil.rmtree(root)
        print("cleaned=true")
    else:
        print("note=multi-repo eval root kept for inspection; rerun with --clean to remove it")


if __name__ == "__main__":
    main()
