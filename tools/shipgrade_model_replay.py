#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from shipgrade_eval_corpus import EVAL_CASES
from shipgrade_holdout_replay import HOLDOUT_CASES


ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PATTERNS = [
    re.compile(r"/Users/"),
    re.compile(r"/var/folders"),
    re.compile(r"/private/var"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
]

BASE_EVAL_CORPUS = ROOT / "docs" / "eval-corpus" / "real-task-eval-cases.jsonl"
HOLDOUT_REPLAY_CORPUS = ROOT / "docs" / "holdout-replay" / "holdout-replay-cases.jsonl"

LAYER_PATTERNS = {
    "validation_evidence_gap": [
        "test",
        "tests",
        "quick-check",
        "workflow",
        "ci.yml",
        "test.yaml",
        "eval-on-pr",
        "local gate",
        "runtime gate",
        "pyproject",
        "package.json",
        "makefile",
        "command evidence",
        "pypath",
        "pythonpath",
    ],
    "source_boundary_gap": [
        "boundary",
        "source/license",
        "forbidden data",
        "secret key",
        "secret",
        "cookie",
        "session",
        "browser/model boundary",
        "sandbox",
    ],
    "completion_audit_gap": [
        "reject",
        "state",
        "resume",
        "handoff",
        "human handoff",
        "todo",
        "concrete artifact path",
    ],
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def load_base_cases() -> list[dict[str, Any]]:
    return load_jsonl(BASE_EVAL_CORPUS) or list(EVAL_CASES)


def load_holdout_cases() -> list[dict[str, Any]]:
    return load_jsonl(HOLDOUT_REPLAY_CORPUS) or list(HOLDOUT_CASES)


def normalize_case(case: dict[str, Any], source_set: str) -> dict[str, Any]:
    strong_key = "chosen_answer" if "chosen_answer" in case else "strong_answer"
    weak_key = "rejected_answer" if "rejected_answer" in case else "weak_answer"
    return {
        "id": case["id"],
        "source_set": source_set,
        "task_type": case["task_type"],
        "repo": case["repo"],
        "license": case["license"],
        "evidence_paths": case["evidence_paths"],
        "prompt_cn": case["prompt_cn"],
        "rubric": case["rubric"],
        "must_include": case["must_include"],
        "must_avoid": case["must_avoid"],
        "target_answer": case[strong_key],
        "lazy_answer": case[weak_key],
    }


def score_answer(case: dict[str, Any], answer: str) -> dict[str, Any]:
    lower = answer.lower()
    matched = [term for term in case["must_include"] if term.lower() in lower]
    forbidden_hit = [term for term in case["must_avoid"] if term.lower() in lower]
    score = len(matched) / max(1, len(case["must_include"]))
    return {
        "case_id": case["id"],
        "matched": matched,
        "missing": [term for term in case["must_include"] if term.lower() not in lower],
        "forbidden_hit": forbidden_hit,
        "score": round(score, 3),
        "passed": score >= 0.8 and not forbidden_hit,
    }


def synthesize_partial_candidate(case: dict[str, Any]) -> str:
    anchors = "、".join(case["must_include"][:2])
    return (
        f"先围绕 {anchors} 做一个候选切入,但这只是 partial_candidate_draft。"
        "仍需要补齐验证证据、来源/边界说明、失败路径和接手点,不能作为完成交付。"
    )


def classify_failure(case: dict[str, Any], result: dict[str, Any]) -> list[str]:
    if result["passed"]:
        return []
    layers: set[str] = set()
    missing_text = " ".join(str(term).lower() for term in result["missing"])
    forbidden_text = " ".join(str(term).lower() for term in result["forbidden_hit"])
    for layer, patterns in LAYER_PATTERNS.items():
        if any(pattern in missing_text or pattern in forbidden_text for pattern in patterns):
            layers.add(layer)
    if result["forbidden_hit"]:
        layers.add("forbidden_behavior_hit")
    if not layers:
        layers.add("rubric_coverage_gap")
    return sorted(layers)


def replay_profiles(cases: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    replay_cases = []
    results = []
    for case in cases:
        outputs = {
            "shipgrade_target": case["target_answer"],
            "lazy_or_overfit_draft": case["lazy_answer"],
            "partial_candidate_draft": synthesize_partial_candidate(case),
        }
        replay_cases.append(
            {
                "id": case["id"],
                "source_set": case["source_set"],
                "task_type": case["task_type"],
                "repo": case["repo"],
                "license": case["license"],
                "evidence_paths": case["evidence_paths"],
                "prompt_cn": case["prompt_cn"],
                "rubric": case["rubric"],
                "must_include": case["must_include"],
                "must_avoid": case["must_avoid"],
                "candidate_outputs": outputs,
                "public_boundary": "Public metadata, prompts, rubrics, path evidence, and synthetic replay outputs only; no upstream source bodies.",
            }
        )
        for profile, answer in outputs.items():
            scored = score_answer(case, answer)
            results.append(
                {
                    "case_id": case["id"],
                    "source_set": case["source_set"],
                    "repo": case["repo"],
                    "profile": profile,
                    "passed": scored["passed"],
                    "score": scored["score"],
                    "matched": scored["matched"],
                    "missing": scored["missing"],
                    "forbidden_hit": scored["forbidden_hit"],
                    "failure_layers": classify_failure(case, scored),
                }
            )
    return replay_cases, results


def summarize_profiles(results: list[dict[str, Any]], case_count: int) -> dict[str, dict[str, Any]]:
    summaries: dict[str, dict[str, Any]] = {}
    for profile in sorted({item["profile"] for item in results}):
        items = [item for item in results if item["profile"] == profile]
        passed = sum(1 for item in items if item["passed"])
        failed = case_count - passed
        layers = sorted({layer for item in items for layer in item["failure_layers"]})
        summaries[profile] = {
            "passed": passed,
            "failed": failed,
            "failure_layers": layers,
        }
    return summaries


def ensure_public_safe(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    hits = [pattern.pattern for pattern in FORBIDDEN_PATTERNS if pattern.search(text)]
    if hits:
        raise SystemExit(f"public safety scan failed for {path}: {hits}")


def write_outputs(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    cases_path = output_dir / "model-output-replay-cases.jsonl"
    report_path = output_dir / "model-output-replay-report.json"
    readme_path = output_dir / "README.md"

    base_cases = [normalize_case(case, "base_eval") for case in load_base_cases()]
    holdout_cases = [normalize_case(case, "holdout_replay") for case in load_holdout_cases()]
    cases = base_cases + holdout_cases
    replay_cases, results = replay_profiles(cases)
    summaries = summarize_profiles(results, len(cases))
    failure_layers = sorted({layer for item in results for layer in item["failure_layers"]})
    target_passed = summaries["shipgrade_target"]["passed"]
    lazy_failed = summaries["lazy_or_overfit_draft"]["failed"]
    partial_failed = summaries["partial_candidate_draft"]["failed"]
    required_layers = {"validation_evidence_gap", "source_boundary_gap", "completion_audit_gap"}

    cases_path.write_text(
        "\n".join(json.dumps(case, ensure_ascii=False, sort_keys=True) for case in replay_cases) + "\n",
        encoding="utf-8",
    )
    report = {
        "ok": (
            len(base_cases) == 4
            and len(holdout_cases) == 8
            and len(cases) == 12
            and target_passed == 12
            and lazy_failed == 12
            and partial_failed >= 6
            and required_layers.issubset(set(failure_layers))
        ),
        "case_count": len(cases),
        "base_eval_cases": len(base_cases),
        "holdout_cases": len(holdout_cases),
        "profiles": 3,
        "target_passed": target_passed,
        "lazy_failed": lazy_failed,
        "partial_failed": partial_failed,
        "failure_layers": failure_layers,
        "profile_summaries": summaries,
        "results": results,
        "candidate_outputs_replayed": True,
        "failure_stratified": True,
        "public_boundary": "No upstream source bodies, secrets, cookies, sessions, private keys, browser profiles, auth databases, or private repositories.",
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    readme_path.write_text(
        "# ShipGrade Model Output Replay\n\n"
        "This replay gate scores candidate/model-style outputs against the base eval and holdout replay cases, then stratifies failed outputs by failure layer.\n\n"
        "- cases: `12`\n"
        "- base eval cases: `4`\n"
        "- holdout cases: `8`\n"
        "- profiles: `shipgrade_target`, `lazy_or_overfit_draft`, `partial_candidate_draft`\n"
        "- target profile: `12/12` pass\n"
        "- lazy profile: `12/12` fail\n"
        "- boundary: metadata, path evidence, prompts, rubrics, and synthetic replay outputs only; no upstream source bodies.\n\n"
        "Use `model-output-replay-cases.jsonl` for candidate replay inputs and `model-output-replay-report.json` for deterministic scoring and failure stratification.\n",
        encoding="utf-8",
    )
    for path in (cases_path, report_path, readme_path):
        ensure_public_safe(path)
    return report


def ensure_safe_target(path: Path) -> None:
    temp_root = Path(tempfile.gettempdir()).resolve()
    resolved = path.resolve()
    if temp_root not in resolved.parents and resolved != temp_root:
        raise SystemExit(f"refuse to clean non-temp model replay target: {resolved}")
    if not resolved.name.startswith("shipgrade-model-replay"):
        raise SystemExit(f"refuse to clean non-model-replay target: {resolved}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay candidate/model outputs through ShipGrade eval and holdout gates.")
    parser.add_argument("--output-dir", help="write model replay files into this directory")
    parser.add_argument("--clean", action="store_true", help="remove temporary output when --output-dir is not provided")
    args = parser.parse_args()

    if args.output_dir:
        output_dir = Path(args.output_dir)
        if output_dir.exists():
            shutil.rmtree(output_dir)
    else:
        output_dir = Path(tempfile.mkdtemp(prefix="shipgrade-model-replay-"))
        ensure_safe_target(output_dir)

    report = write_outputs(output_dir)
    if not report["ok"]:
        raise SystemExit("model output replay self-check failed")

    print("shipgrade-model-replay-ok")
    print(f"cases={report['case_count']}")
    print(f"base_eval_cases={report['base_eval_cases']}")
    print(f"holdout_cases={report['holdout_cases']}")
    print(f"profiles={report['profiles']}")
    print(f"target_passed={report['target_passed']}/{report['case_count']}")
    print(f"lazy_failed={report['lazy_failed']}/{report['case_count']}")
    print(f"partial_failed={report['partial_failed']}/{report['case_count']}")
    print("failure_layers=" + ",".join(report["failure_layers"]))
    print("model_replay_cases_path=" + (output_dir / "model-output-replay-cases.jsonl").as_posix())
    print("report_path=" + (output_dir / "model-output-replay-report.json").as_posix())
    print("candidate_outputs_replayed=true")
    print("failure_stratified=true")
    print("source_body_copied_to_public=false")
    print("secret_scan=pass")
    if args.clean and not args.output_dir:
        shutil.rmtree(output_dir)
        print("cleaned=true")
    elif not args.output_dir:
        print("note=temporary model replay kept for inspection; rerun with --clean to remove it")


if __name__ == "__main__":
    main()
