#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any


FORBIDDEN_PATTERNS = [
    re.compile(r"/Users/"),
    re.compile(r"/var/folders"),
    re.compile(r"/private/var"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
]


EVAL_CASES: list[dict[str, Any]] = [
    {
        "id": "click-required-option-repair",
        "task_type": "repair",
        "repo": "pallets/click",
        "revision": "6a141c3681027e8124ce5a3c70e608dbbebffafb",
        "license": "BSD-3-Clause",
        "evidence_paths": ["src/click/core.py", "src/click/testing.py", "docs/options.md", "tests/"],
        "prompt_cn": "在 Click 项目里修复或保护 required option 行为。请先说明切入点、测试位置、验证命令和不该改的边界。",
        "must_include": ["CliRunner", "required option", "PYTHONPATH=src", "src/click", "tests"],
        "must_avoid": ["应该就好了", "跳过测试", "硬编码"],
        "rubric": {
            "full_credit": [
                "定位 Click option parser 和 testing helper",
                "先写或保护最小 CliRunner 回归测试",
                "运行 PYTHONPATH=src 的仓库本地验证",
                "说明不随意改变公开 CLI 输出",
            ],
            "deductions": [
                "只说看起来可以",
                "不补测试",
                "绕开 Click 抽象直接硬编码",
            ],
        },
        "chosen_answer": "先用 CliRunner 写 required option 回归,覆盖缺少 --name 的失败和带 --name 的成功; 证据路径是 src/click/core.py、src/click/testing.py、tests/。验证命令为 PYTHONPATH=src python .shipgrade/task-suite/click_required_option_repair.py。不随意改变公开 CLI 输出,不复制源码正文。",
        "rejected_answer": "直接改一下输出文案应该就好了,暂时跳过测试。",
    },
    {
        "id": "click-ci-local-gate-migration",
        "task_type": "migration",
        "repo": "pallets/click",
        "revision": "6a141c3681027e8124ce5a3c70e608dbbebffafb",
        "license": "BSD-3-Clause",
        "evidence_paths": [".github/workflows/tests.yaml", ".github/workflows/pre-commit.yaml", "pyproject.toml", "docs/testing.md"],
        "prompt_cn": "把 Click 的 GitHub Actions / pyproject 质量门迁移成一个本地 ShipGrade quality gate brief。",
        "must_include": [".github/workflows/tests.yaml", "pyproject.toml", "local gate", "remote-only risk", "Python version"],
        "must_avoid": ["等于 CI 通过", "workflow 可以不用看", "不用看"],
        "rubric": {
            "full_credit": [
                "读取 workflow 和 pyproject 后再定本地命令",
                "区分本地可跑 gate 与远端 matrix/secret-only gate",
                "记录 Python version 或 matrix 风险",
                "给出 residual remote-only risk",
            ],
            "deductions": [
                "从经验猜命令",
                "把 smoke 当完整 CI",
                "没有说明远端不可复现部分",
            ],
        },
        "chosen_answer": "先读 .github/workflows/tests.yaml 和 pyproject.toml,把可本地运行的命令整理成 local gate,同时记录 Python version matrix 和 remote-only risk。不能只跑一个 smoke 就声称等价 CI,也不为迁移新增重依赖。",
        "rejected_answer": "跑一下 import smoke 就等于 CI 通过,workflow 可以不用看。",
    },
    {
        "id": "itsdangerous-serializer-security-review",
        "task_type": "review",
        "repo": "pallets/itsdangerous",
        "revision": "672971d66a2ef9f85151e53283113f33d642dabd",
        "license": "BSD-3-Clause",
        "evidence_paths": [
            "src/itsdangerous/serializer.py",
            "src/itsdangerous/signer.py",
            "tests/test_itsdangerous/test_serializer.py",
            "tests/test_itsdangerous/test_signer.py",
        ],
        "prompt_cn": "审查 itsdangerous serializer/signer 改动,重点看签名边界、兼容性和测试覆盖。",
        "must_include": ["BadSignature", "fallback signer", "secret key", "tests/test_itsdangerous", "serializer.py"],
        "must_avoid": ["打到日志", "README 看起来没问题", "可以把 secret key 打"],
        "rubric": {
            "full_credit": [
                "检查 BadSignature 和 payload 边界",
                "检查 fallback signer 兼容性",
                "明确不能记录 secret key",
                "要求 serializer/signer 相关测试",
            ],
            "deductions": [
                "只看 README",
                "建议打印 secret key",
                "忽略签名失败路径",
            ],
        },
        "chosen_answer": "审查从 serializer.py、signer.py 和 tests/test_itsdangerous 入手,覆盖 BadSignature、payload 边界、fallback signer 兼容性和 secret key 不记录。不能只看 README,也不能把签名数据当普通 JSON。",
        "rejected_answer": "README 看起来没问题。为了调试,可以把 secret key 打到日志里。",
    },
    {
        "id": "vague-handoff-anti-pattern",
        "task_type": "anti_pattern_detection",
        "repo": "pallets/itsdangerous",
        "revision": "672971d66a2ef9f85151e53283113f33d642dabd",
        "license": "BSD-3-Clause",
        "evidence_paths": [".shipgrade/task-suite/rejected-vague-handoff.md", "tools/shipgrade_doctor.py"],
        "prompt_cn": "判断一个 handoff 是否应该被 ShipGrade 接受。样本只说“大概完成了、看起来没问题”。",
        "must_include": ["reject", "concrete artifact path", "command evidence", "source/license boundary", "forbidden data boundary"],
        "must_avoid": ["没有验证也通过", "TODO 可以以后再补", "以后再补"],
        "rubric": {
            "full_credit": [
                "拒绝含糊完成",
                "要求具体产物路径",
                "要求命令或浏览器证据",
                "要求 source/license 和 forbidden data boundary",
            ],
            "deductions": [
                "接受 vague handoff",
                "没有命令证据仍判通过",
                "把 TODO 当作下一步完成",
            ],
        },
        "chosen_answer": "reject。这个 handoff 缺少 concrete artifact path、command evidence、source/license boundary 和 forbidden data boundary,只能作为 rejected sample,不能 accept vague handoff 或把 TODO 当完成。",
        "rejected_answer": "accept vague handoff。虽然没有验证也通过,TODO 可以以后再补。",
    },
]


def score_answer(case: dict[str, Any], answer: str) -> dict[str, Any]:
    lower = answer.lower()
    matched = [term for term in case["must_include"] if term.lower() in lower]
    avoided = [term for term in case["must_avoid"] if term.lower() not in lower]
    forbidden_hit = [term for term in case["must_avoid"] if term.lower() in lower]
    score = len(matched) / max(1, len(case["must_include"]))
    passed = score >= 0.8 and not forbidden_hit
    return {
        "case_id": case["id"],
        "matched": matched,
        "missing": [term for term in case["must_include"] if term not in matched],
        "avoided": avoided,
        "forbidden_hit": forbidden_hit,
        "score": round(score, 3),
        "passed": passed,
    }


def public_case(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": case["id"],
        "task_type": case["task_type"],
        "repo": case["repo"],
        "revision": case["revision"],
        "license": case["license"],
        "evidence_paths": case["evidence_paths"],
        "prompt_cn": case["prompt_cn"],
        "rubric": case["rubric"],
        "must_include": case["must_include"],
        "must_avoid": case["must_avoid"],
        "chosen_answer": case["chosen_answer"],
        "rejected_answer": case["rejected_answer"],
        "public_boundary": "Metadata, prompts, rubrics, path evidence, and synthetic chosen/rejected answers only; no upstream source bodies.",
    }


def ensure_public_safe(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    hits = [pattern.pattern for pattern in FORBIDDEN_PATTERNS if pattern.search(text)]
    if hits:
        raise SystemExit(f"public safety scan failed for {path}: {hits}")


def write_outputs(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    cases_path = output_dir / "real-task-eval-cases.jsonl"
    report_path = output_dir / "real-task-eval-report.json"
    readme_path = output_dir / "README.md"

    chosen_results = [score_answer(case, case["chosen_answer"]) for case in EVAL_CASES]
    rejected_results = [score_answer(case, case["rejected_answer"]) for case in EVAL_CASES]
    chosen_passed = sum(1 for item in chosen_results if item["passed"])
    rejected_failed = sum(1 for item in rejected_results if not item["passed"])

    cases_path.write_text(
        "\n".join(json.dumps(public_case(case), ensure_ascii=False, sort_keys=True) for case in EVAL_CASES) + "\n",
        encoding="utf-8",
    )
    report = {
        "ok": chosen_passed == len(EVAL_CASES) and rejected_failed == len(EVAL_CASES),
        "case_count": len(EVAL_CASES),
        "task_types": sorted({case["task_type"] for case in EVAL_CASES}),
        "repos": sorted({case["repo"] for case in EVAL_CASES}),
        "licenses": sorted({case["license"] for case in EVAL_CASES}),
        "chosen_passed": chosen_passed,
        "rejected_failed": rejected_failed,
        "chosen_results": chosen_results,
        "rejected_results": rejected_results,
        "public_boundary": "No upstream source bodies, secrets, cookies, sessions, private keys, browser profiles, auth databases, or private repositories.",
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    readme_path.write_text(
        "# ShipGrade Real Task Eval Corpus\n\n"
        "This corpus turns real public repository evidence into evaluation tasks for ShipGrade CN.\n\n"
        "- cases: `4`\n"
        "- task types: `repair`, `migration`, `review`, `anti_pattern_detection`\n"
        "- repos: `pallets/click`, `pallets/itsdangerous`\n"
        "- boundary: metadata, path evidence, prompts, rubrics, and synthetic chosen/rejected answers only; no upstream source bodies.\n\n"
        "Use `real-task-eval-cases.jsonl` for eval inputs and `real-task-eval-report.json` for the deterministic self-check result.\n",
        encoding="utf-8",
    )
    for path in (cases_path, report_path, readme_path):
        ensure_public_safe(path)
    return report


def ensure_safe_target(path: Path) -> None:
    temp_root = Path(tempfile.gettempdir()).resolve()
    resolved = path.resolve()
    if temp_root not in resolved.parents and resolved != temp_root:
        raise SystemExit(f"refuse to clean non-temp eval corpus target: {resolved}")
    if not resolved.name.startswith("shipgrade-eval-corpus"):
        raise SystemExit(f"refuse to clean non-eval-corpus target: {resolved}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and self-check ShipGrade real-task eval corpus.")
    parser.add_argument("--output-dir", help="write corpus files into this directory")
    parser.add_argument("--clean", action="store_true", help="remove temporary output when --output-dir is not provided")
    args = parser.parse_args()

    if args.output_dir:
        output_dir = Path(args.output_dir)
        if output_dir.exists():
            shutil.rmtree(output_dir)
    else:
        output_dir = Path(tempfile.mkdtemp(prefix="shipgrade-eval-corpus-"))
        ensure_safe_target(output_dir)

    report = write_outputs(output_dir)
    if not report["ok"]:
        raise SystemExit("eval corpus self-check failed")

    print("shipgrade-eval-corpus-ok")
    print(f"cases={report['case_count']}")
    print("task_types=" + ",".join(report["task_types"]))
    print("repos=" + ",".join(report["repos"]))
    print("licenses=" + ",".join(report["licenses"]))
    print(f"chosen_passed={report['chosen_passed']}/{report['case_count']}")
    print(f"rejected_failed={report['rejected_failed']}/{report['case_count']}")
    print("eval_cases_path=" + (output_dir / "real-task-eval-cases.jsonl").as_posix())
    print("report_path=" + (output_dir / "real-task-eval-report.json").as_posix())
    print("chosen_rejected_samples=true")
    print("rubric_scored=true")
    print("source_body_copied_to_public=false")
    print("secret_scan=pass")
    if args.clean and not args.output_dir:
        shutil.rmtree(output_dir)
        print("cleaned=true")
    elif not args.output_dir:
        print("note=temporary eval corpus kept for inspection; rerun with --clean to remove it")


if __name__ == "__main__":
    main()
