#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PATTERNS = [
    re.compile(r"/Users/"),
    re.compile(r"/var/folders"),
    re.compile(r"/private/var"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
]

BASE_EVAL_CORPUS = ROOT / "docs" / "eval-corpus" / "real-task-eval-cases.jsonl"

HOLDOUT_CASES: list[dict[str, Any]] = [
    {
        "id": "spec-kit-spec-drift-review",
        "task_type": "review",
        "repo": "github/spec-kit",
        "license": "MIT",
        "evidence_paths": ["pyproject.toml", ".github/workflows/quick-check.yml", "templates/", "tests/"],
        "prompt_cn": "审查一个 spec-first 项目改动是否让 spec、plan、tasks 与实现脱节。请给出审查切入点、证据路径和扣分项。",
        "must_include": ["spec", "plan", "tasks", "quick-check", "templates"],
        "must_avoid": ["只看 README", "直接相信实现", "不用跑"],
        "rubric": {
            "full_credit": [
                "先对齐 spec / plan / tasks 三层是否一致",
                "读取 quick-check 或等价本地质量门",
                "检查模板入口是否和生成产物一致",
                "明确不能只看实现或 README",
            ],
            "deductions": ["只看 README", "忽略模板漂移", "没有验证命令"],
        },
        "strong_answer": "先按 spec、plan、tasks 三层比对意图与实现,再读 pyproject.toml、.github/workflows/quick-check.yml、templates/ 和 tests/。验收要包含 quick-check 或等价本地命令,并指出模板入口与生成产物的 drift 风险。",
        "weak_answer": "README 写得清楚就行,直接相信实现,不用跑。",
    },
    {
        "id": "browser-use-agent-runtime-boundary",
        "task_type": "migration",
        "repo": "browser-use/browser-use",
        "license": "MIT",
        "evidence_paths": ["pyproject.toml", ".github/workflows/test.yaml", "browser_use/agent/", "tests/"],
        "prompt_cn": "把 browser automation agent 项目的运行边界迁移成 ShipGrade quality gate,要区分本地可验证与真实浏览器/模型依赖。",
        "must_include": ["pyproject.toml", "test.yaml", "browser_use/agent", "local gate", "browser/model boundary"],
        "must_avoid": ["跑 import 就够", "不需要隔离", "真实浏览器随便跑"],
        "rubric": {
            "full_credit": [
                "从 pyproject 和 workflow 推导本地 gate",
                "区分 deterministic tests 与 browser/model dependent checks",
                "给出 sandbox 和 secret/cookie/session 禁止边界",
                "说明 remote-only 或环境依赖风险",
            ],
            "deductions": ["把 import smoke 当完整验证", "忽略浏览器会话安全", "没有环境边界"],
        },
        "strong_answer": "先读 pyproject.toml 和 .github/workflows/test.yaml,把 browser_use/agent 与 tests/ 里的 deterministic 部分整理成 local gate。真实浏览器和模型调用要写 browser/model boundary,禁止 cookie/session/auth profile 进入样本。",
        "weak_answer": "跑 import 就够,真实浏览器随便跑,不需要隔离。",
    },
    {
        "id": "promptfoo-eval-first-quality-loop",
        "task_type": "engineering_plan",
        "repo": "promptfoo/promptfoo",
        "license": "MIT",
        "evidence_paths": ["package.json", ".github/workflows/eval-on-pr.yml", "src/", "test/", "examples/"],
        "prompt_cn": "为一个 LLM eval 工具仓设计本地质量门,避免把单个 smoke 当成 eval 质量证明。",
        "must_include": ["package.json", "eval-on-pr", "test", "examples", "quality gate"],
        "must_avoid": ["一个 smoke 过了", "不用 eval", "凭感觉"],
        "rubric": {
            "full_credit": [
                "从 package scripts 和 eval workflow 推导质量门",
                "区分单元测试、示例、eval schema 和远端依赖",
                "明确一个 smoke 不能证明 eval 质量",
                "输出可复跑 gate",
            ],
            "deductions": ["只跑一个 smoke", "不看 eval workflow", "没有负例"],
        },
        "strong_answer": "先读取 package.json、.github/workflows/eval-on-pr.yml、test/ 和 examples/,把测试、示例和 eval schema 分成 quality gate。一个 smoke 只能当入口,不能替代 eval 质量证明。",
        "weak_answer": "一个 smoke 过了就可以,不用 eval,凭感觉判断质量。",
    },
    {
        "id": "inspect-ai-tool-sandbox-review",
        "task_type": "review",
        "repo": "UKGovernmentBEIS/inspect_ai",
        "license": "MIT",
        "evidence_paths": ["pyproject.toml", "src/inspect_ai/tool/", "src/inspect_ai/solver/", "tests/"],
        "prompt_cn": "审查一个 agent eval 工具改动,重点看 tool sandbox、solver 边界和测试覆盖。",
        "must_include": ["tool", "solver", "sandbox", "pyproject.toml", "tests"],
        "must_avoid": ["直接执行任意工具", "忽略 sandbox", "不补测试"],
        "rubric": {
            "full_credit": [
                "检查 tool / solver 的职责边界",
                "说明 sandbox 与外部命令限制",
                "从 pyproject 推导本地验证",
                "要求 tests 覆盖失败路径",
            ],
            "deductions": ["忽略 sandbox", "允许任意外部命令", "没有测试"],
        },
        "strong_answer": "从 pyproject.toml、src/inspect_ai/tool/、src/inspect_ai/solver/ 和 tests/ 入手,先界定 tool 与 solver 边界,再检查 sandbox 限制和失败路径测试。",
        "weak_answer": "直接执行任意工具就行,忽略 sandbox,不补测试。",
    },
    {
        "id": "superclaude-command-layering-repair",
        "task_type": "repair",
        "repo": "SuperClaude-Org/SuperClaude_Framework",
        "license": "MIT",
        "evidence_paths": ["pyproject.toml", "Makefile", "SuperClaude/", "tests/"],
        "prompt_cn": "修复一个命令/角色/规则混杂导致的 skill 行为漂移。请给出分层修复策略与验证命令。",
        "must_include": ["command", "persona", "rule", "Makefile", "tests"],
        "must_avoid": ["全部塞进一个提示词", "不用分层", "没有回归"],
        "rubric": {
            "full_credit": [
                "把 command、persona、rule 分层处理",
                "保留用户入口的低门槛",
                "从 Makefile 或 pyproject 推导验证",
                "补回归或 fixture 检查",
            ],
            "deductions": ["全部塞进一个提示词", "没有分层", "没有回归验证"],
        },
        "strong_answer": "先把 command、persona、rule 三层拆开,用 Makefile、pyproject.toml 和 tests/ 找回归入口。修复后要证明入口仍简单,但内部规则不再互相覆盖。",
        "weak_answer": "全部塞进一个提示词就行,不用分层,没有回归也可以。",
    },
    {
        "id": "humanlayer-agent-handoff-anti-pattern",
        "task_type": "anti_pattern_detection",
        "repo": "humanlayer/12-factor-agents",
        "license": "Apache-2.0",
        "evidence_paths": ["README.md", "content/", "packages/", "examples/"],
        "prompt_cn": "判断一个 agent handoff 是否违反 12-factor agent 思路: 没有状态、没有恢复点、没有人工接管边界。",
        "must_include": ["state", "resume", "human handoff", "boundary", "reject"],
        "must_avoid": ["聊天记录就行", "没有恢复点也接受", "不用人工边界"],
        "rubric": {
            "full_credit": [
                "拒绝只靠聊天记录的交付",
                "要求状态、恢复点和人工接管边界",
                "说明 agent 任务可中断可恢复",
                "给出 handoff 修复字段",
            ],
            "deductions": ["接受无状态 handoff", "没有人工边界", "没有恢复点"],
        },
        "strong_answer": "reject。这个 handoff 不能只靠聊天记录,必须写 state、resume point、human handoff boundary 和下一步。缺少恢复点会导致 agent 任务不可恢复。",
        "weak_answer": "全靠聊天记录就行,没有恢复点也接受,不用人工边界。",
    },
    {
        "id": "addyosmani-agent-skills-install-boundary",
        "task_type": "skill_design",
        "repo": "addyosmani/agent-skills",
        "license": "MIT",
        "evidence_paths": [".github/workflows/test-plugin-install.yml", ".claude/commands/", "skills/", "README.md"],
        "prompt_cn": "设计一个技能安装边界,避免把 README、命令和技能本体混成不可维护的仓库。",
        "must_include": ["SKILL.md", "install", "workflow", "commands", "boundary"],
        "must_avoid": ["只写 README 就够", "复制所有命令", "没有安装验证"],
        "rubric": {
            "full_credit": [
                "明确 SKILL.md 是 agent 入口",
                "把 commands / skills / docs 分层",
                "保留安装验证 workflow",
                "说明不要复制无关命令",
            ],
            "deductions": ["只写 README", "没有安装验证", "命令无边界复制"],
        },
        "strong_answer": "以 SKILL.md 作为 agent 入口,把 commands、skills 和 docs 分层,并参考 test-plugin-install workflow 做 install 验证。安装 boundary 要写清哪些命令能迁移、哪些只做来源参考。",
        "weak_answer": "只写 README 就够,复制所有命令,没有安装验证也行。",
    },
    {
        "id": "ecc-catalog-runtime-gate",
        "task_type": "runtime_gate",
        "repo": "affaan-m/ECC",
        "license": "MIT",
        "evidence_paths": ["package.json", "pyproject.toml", ".github/workflows/ci.yml", ".opencode/"],
        "prompt_cn": "把一个 prompt/command catalog 的质量门落成本地 runtime gate,避免只靠目录数量证明质量。",
        "must_include": ["package.json", "pyproject.toml", "ci.yml", "catalog", "runtime gate"],
        "must_avoid": ["只数条目", "不跑命令", "质量自然高"],
        "rubric": {
            "full_credit": [
                "从 package、pyproject 和 CI 推导 runtime gate",
                "区分 catalog completeness 与可运行质量",
                "要求至少一个低副作用命令或 schema 检查",
                "记录未覆盖边界",
            ],
            "deductions": ["只数条目", "不跑命令", "把数量当质量"],
        },
        "strong_answer": "先读 package.json、pyproject.toml 和 .github/workflows/ci.yml,把 catalog 完整性和 runtime gate 分开。目录数量不是质量,至少要有低副作用命令或 schema 检查。",
        "weak_answer": "只数条目就能证明质量,不跑命令,质量自然高。",
    },
]


def load_base_repos() -> set[str]:
    if not BASE_EVAL_CORPUS.exists():
        return set()
    repos: set[str] = set()
    for line in BASE_EVAL_CORPUS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        value = json.loads(line)
        repo = value.get("repo")
        if isinstance(repo, str):
            repos.add(repo)
    return repos


def score_answer(case: dict[str, Any], answer: str) -> dict[str, Any]:
    lower = answer.lower()
    matched = [term for term in case["must_include"] if term.lower() in lower]
    forbidden_hit = [term for term in case["must_avoid"] if term.lower() in lower]
    score = len(matched) / max(1, len(case["must_include"]))
    passed = score >= 0.8 and not forbidden_hit
    return {
        "case_id": case["id"],
        "matched": matched,
        "missing": [term for term in case["must_include"] if term not in matched],
        "forbidden_hit": forbidden_hit,
        "score": round(score, 3),
        "passed": passed,
    }


def public_case(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": case["id"],
        "task_type": case["task_type"],
        "repo": case["repo"],
        "license": case["license"],
        "evidence_paths": case["evidence_paths"],
        "prompt_cn": case["prompt_cn"],
        "rubric": case["rubric"],
        "must_include": case["must_include"],
        "must_avoid": case["must_avoid"],
        "strong_answer": case["strong_answer"],
        "weak_answer": case["weak_answer"],
        "public_boundary": "Holdout metadata, prompts, rubrics, path evidence, and synthetic replay answers only; no upstream source bodies.",
    }


def ensure_public_safe(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    hits = [pattern.pattern for pattern in FORBIDDEN_PATTERNS if pattern.search(text)]
    if hits:
        raise SystemExit(f"public safety scan failed for {path}: {hits}")


def write_outputs(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    cases_path = output_dir / "holdout-replay-cases.jsonl"
    report_path = output_dir / "holdout-replay-report.json"
    readme_path = output_dir / "README.md"

    base_repos = load_base_repos()
    holdout_repos = {case["repo"] for case in HOLDOUT_CASES}
    overlap = sorted(base_repos & holdout_repos)
    strong_results = [score_answer(case, case["strong_answer"]) for case in HOLDOUT_CASES]
    weak_results = [score_answer(case, case["weak_answer"]) for case in HOLDOUT_CASES]
    strong_passed = sum(1 for item in strong_results if item["passed"])
    weak_failed = sum(1 for item in weak_results if not item["passed"])

    cases_path.write_text(
        "\n".join(json.dumps(public_case(case), ensure_ascii=False, sort_keys=True) for case in HOLDOUT_CASES) + "\n",
        encoding="utf-8",
    )
    report = {
        "ok": strong_passed == len(HOLDOUT_CASES) and weak_failed == len(HOLDOUT_CASES) and not overlap,
        "case_count": len(HOLDOUT_CASES),
        "task_types": sorted({case["task_type"] for case in HOLDOUT_CASES}),
        "repos": sorted(holdout_repos),
        "licenses": sorted({case["license"] for case in HOLDOUT_CASES}),
        "base_eval_repos": sorted(base_repos),
        "base_overlap_repos": overlap,
        "holdout_not_training": not overlap,
        "strong_passed": strong_passed,
        "weak_failed": weak_failed,
        "strong_results": strong_results,
        "weak_results": weak_results,
        "public_boundary": "No upstream source bodies, secrets, cookies, sessions, private keys, browser profiles, auth databases, or private repositories.",
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    readme_path.write_text(
        "# ShipGrade Holdout Replay\n\n"
        "This holdout set replays strong and weak answers on repositories that are not part of the scored real-task eval corpus.\n\n"
        "- cases: `8`\n"
        "- base overlap repos: `0`\n"
        "- strong answers: `8/8` pass\n"
        "- weak answers: `8/8` fail\n"
        "- boundary: metadata, path evidence, prompts, rubrics, and synthetic replay answers only; no upstream source bodies.\n\n"
        "Use `holdout-replay-cases.jsonl` for replay inputs and `holdout-replay-report.json` for the deterministic self-check result.\n",
        encoding="utf-8",
    )
    for path in (cases_path, report_path, readme_path):
        ensure_public_safe(path)
    return report


def ensure_safe_target(path: Path) -> None:
    temp_root = Path(tempfile.gettempdir()).resolve()
    resolved = path.resolve()
    if temp_root not in resolved.parents and resolved != temp_root:
        raise SystemExit(f"refuse to clean non-temp holdout replay target: {resolved}")
    if not resolved.name.startswith("shipgrade-holdout-replay"):
        raise SystemExit(f"refuse to clean non-holdout-replay target: {resolved}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and self-check ShipGrade holdout replay cases.")
    parser.add_argument("--output-dir", help="write holdout replay files into this directory")
    parser.add_argument("--clean", action="store_true", help="remove temporary output when --output-dir is not provided")
    args = parser.parse_args()

    if args.output_dir:
        output_dir = Path(args.output_dir)
        if output_dir.exists():
            shutil.rmtree(output_dir)
    else:
        output_dir = Path(tempfile.mkdtemp(prefix="shipgrade-holdout-replay-"))
        ensure_safe_target(output_dir)

    report = write_outputs(output_dir)
    if not report["ok"]:
        raise SystemExit("holdout replay self-check failed")

    print("shipgrade-holdout-replay-ok")
    print(f"cases={report['case_count']}")
    print("task_types=" + ",".join(report["task_types"]))
    print("repos=" + ",".join(report["repos"]))
    print("licenses=" + ",".join(report["licenses"]))
    print(f"base_overlap_repos={len(report['base_overlap_repos'])}")
    print(f"strong_passed={report['strong_passed']}/{report['case_count']}")
    print(f"weak_failed={report['weak_failed']}/{report['case_count']}")
    print("holdout_replay_cases_path=" + (output_dir / "holdout-replay-cases.jsonl").as_posix())
    print("report_path=" + (output_dir / "holdout-replay-report.json").as_posix())
    print("holdout_not_training=true")
    print("rubric_scored=true")
    print("source_body_copied_to_public=false")
    print("secret_scan=pass")
    if args.clean and not args.output_dir:
        shutil.rmtree(output_dir)
        print("cleaned=true")
    elif not args.output_dir:
        print("note=temporary holdout replay kept for inspection; rerun with --clean to remove it")


if __name__ == "__main__":
    main()
