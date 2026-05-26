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

from shipgrade_model_replay import score_answer, write_outputs as write_model_replay_outputs


ROOT = Path(__file__).resolve().parents[1]

MODEL_REPLAY_DIR = ROOT / "docs" / "model-replay"
MODEL_REPLAY_CASES = MODEL_REPLAY_DIR / "model-output-replay-cases.jsonl"

FORBIDDEN_PATTERNS = [
    re.compile(r"/Users/"),
    re.compile(r"/var/folders"),
    re.compile(r"/private/var"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
]

JUDGES = [
    {
        "id": "controller_quality",
        "purpose": "Checks whether the answer satisfies task-specific must-include terms without forbidden behavior.",
    },
    {
        "id": "source_boundary",
        "purpose": "Checks path-level evidence, license/source metadata, and forbidden-data boundaries.",
    },
    {
        "id": "completion_audit",
        "purpose": "Checks whether the answer is complete enough to avoid vague handoff or unverified completion.",
    },
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def ensure_model_replay_cases() -> tuple[list[dict[str, Any]], str]:
    if MODEL_REPLAY_CASES.exists():
        return load_jsonl(MODEL_REPLAY_CASES), "docs/model-replay"
    temp_dir = Path(tempfile.mkdtemp(prefix="shipgrade-judge-panel-model-replay-"))
    write_model_replay_outputs(temp_dir)
    try:
        return load_jsonl(temp_dir / "model-output-replay-cases.jsonl"), "generated-temp-model-replay"
    finally:
        shutil.rmtree(temp_dir)


def has_secret_or_local_path(text: str) -> bool:
    return any(pattern.search(text) for pattern in FORBIDDEN_PATTERNS)


def path_evidence_hit(case: dict[str, Any], answer: str) -> bool:
    lower = answer.lower()
    for path in case["evidence_paths"]:
        path_text = str(path).strip("/").lower()
        leaf = Path(path_text).name.lower()
        if path_text and path_text in lower:
            return True
        if leaf and leaf != "." and leaf in lower:
            return True
    return False


def vote(case: dict[str, Any], profile: str, answer: str) -> dict[str, Any]:
    scored = score_answer(
        {
            "id": case["id"],
            "must_include": case["must_include"],
            "must_avoid": case["must_avoid"],
        },
        answer,
    )
    include_score = scored["score"]
    forbidden_hit = scored["forbidden_hit"]
    evidence_hit = path_evidence_hit(case, answer)
    unsafe_text = has_secret_or_local_path(answer)
    boundary_grounded = any(
        term in answer.lower()
        for term in (
            "boundary",
            "source/license",
            "forbidden data",
            "secret",
            "cookie",
            "session",
            "sandbox",
        )
    )

    votes = [
        {
            "judge": "controller_quality",
            "passed": include_score >= 0.8 and not forbidden_hit,
            "reason": "rubric coverage is sufficient and no forbidden behavior hit"
            if include_score >= 0.8 and not forbidden_hit
            else "rubric coverage or forbidden-behavior check failed",
        },
        {
            "judge": "source_boundary",
            "passed": (evidence_hit or boundary_grounded or include_score >= 0.8)
            and not forbidden_hit
            and not unsafe_text
            and bool(case.get("license")),
            "reason": "answer cites repository evidence and keeps public-data boundary"
            if (evidence_hit or boundary_grounded or include_score >= 0.8)
            and not forbidden_hit
            and not unsafe_text
            and bool(case.get("license"))
            else "answer lacks evidence-path grounding or violates boundary terms",
        },
        {
            "judge": "completion_audit",
            "passed": include_score >= 0.8 and not forbidden_hit and not unsafe_text,
            "reason": "answer is complete enough for handoff audit"
            if include_score >= 0.8 and not forbidden_hit and not unsafe_text
            else "answer is too vague, partial, or unsafe for completion audit",
        },
    ]
    passed_votes = sum(1 for item in votes if item["passed"])
    return {
        "case_id": case["id"],
        "source_set": case["source_set"],
        "repo": case["repo"],
        "profile": profile,
        "score": include_score,
        "matched": scored["matched"],
        "missing": scored["missing"],
        "forbidden_hit": forbidden_hit,
        "evidence_hit": evidence_hit,
        "unsafe_text": unsafe_text,
        "votes": votes,
        "passed_votes": passed_votes,
        "majority_passed": passed_votes >= 2,
    }


def public_case(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": case["id"],
        "source_set": case["source_set"],
        "task_type": case["task_type"],
        "repo": case["repo"],
        "license": case["license"],
        "evidence_paths": case["evidence_paths"],
        "prompt_cn": case["prompt_cn"],
        "must_include": case["must_include"],
        "must_avoid": case["must_avoid"],
        "judge_lenses": JUDGES,
        "profiles": sorted(case["candidate_outputs"].keys()),
        "public_boundary": "Judge panel packets contain metadata, prompts, rubrics, path evidence, and synthetic candidate outputs only; no upstream source bodies.",
    }


def ensure_public_safe(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    hits = [pattern.pattern for pattern in FORBIDDEN_PATTERNS if pattern.search(text)]
    if hits:
        raise SystemExit(f"public safety scan failed for {path}: {hits}")


def write_outputs(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    cases_path = output_dir / "judge-panel-cases.jsonl"
    report_path = output_dir / "judge-panel-report.json"
    readme_path = output_dir / "README.md"

    cases, source = ensure_model_replay_cases()
    results = []
    for case in cases:
        for profile, answer in sorted(case["candidate_outputs"].items()):
            results.append(vote(case, profile, answer))

    case_count = len(cases)
    target_unanimous_pass = sum(
        1 for item in results if item["profile"] == "shipgrade_target" and item["passed_votes"] == len(JUDGES)
    )
    lazy_majority_rejected = sum(
        1 for item in results if item["profile"] == "lazy_or_overfit_draft" and not item["majority_passed"]
    )
    partial_majority_rejected = sum(
        1 for item in results if item["profile"] == "partial_candidate_draft" and not item["majority_passed"]
    )
    judge_lenses = [judge["id"] for judge in JUDGES]
    cases_path.write_text(
        "\n".join(json.dumps(public_case(case), ensure_ascii=False, sort_keys=True) for case in cases) + "\n",
        encoding="utf-8",
    )
    report = {
        "ok": (
            case_count == 16
            and len(JUDGES) == 3
            and target_unanimous_pass == case_count
            and lazy_majority_rejected == case_count
            and partial_majority_rejected == case_count
        ),
        "case_count": case_count,
        "profiles": 3,
        "judges": len(JUDGES),
        "judge_lenses": judge_lenses,
        "model_replay_source": source,
        "target_unanimous_pass": target_unanimous_pass,
        "lazy_majority_rejected": lazy_majority_rejected,
        "partial_majority_rejected": partial_majority_rejected,
        "results": results,
        "cross_judge_packet_ready": True,
        "deterministic_judge_panel": True,
        "external_model_called": False,
        "human_review_claimed": False,
        "public_boundary": "No upstream source bodies, secrets, cookies, sessions, private keys, browser profiles, auth databases, or private repositories.",
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    readme_path.write_text(
        "# ShipGrade Judge Panel\n\n"
        "This deterministic judge panel turns model replay cases into a cross-review packet. It does not claim that an external model or human has already reviewed the outputs.\n\n"
        f"- cases: `{case_count}`\n"
        "- profiles: `3`\n"
        "- judge lenses: `controller_quality`, `source_boundary`, `completion_audit`\n"
        f"- target profile: `{target_unanimous_pass}/{case_count}` unanimous pass\n"
        f"- lazy profile: `{lazy_majority_rejected}/{case_count}` majority rejected\n"
        f"- partial profile: `{partial_majority_rejected}/{case_count}` majority rejected\n"
        "- boundary: metadata, prompts, rubrics, path evidence, and synthetic candidate outputs only; no upstream source bodies.\n\n"
        "Use `judge-panel-cases.jsonl` as a human/Codex/Claude review packet and `judge-panel-report.json` as the deterministic CI gate.\n",
        encoding="utf-8",
    )
    for path in (cases_path, report_path, readme_path):
        ensure_public_safe(path)
    return report


def ensure_safe_target(path: Path) -> None:
    temp_root = Path(tempfile.gettempdir()).resolve()
    resolved = path.resolve()
    if temp_root not in resolved.parents and resolved != temp_root:
        raise SystemExit(f"refuse to clean non-temp judge panel target: {resolved}")
    if not resolved.name.startswith("shipgrade-judge-panel"):
        raise SystemExit(f"refuse to clean non-judge-panel target: {resolved}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and self-check ShipGrade deterministic judge-panel packets.")
    parser.add_argument("--output-dir", help="write judge panel files into this directory")
    parser.add_argument("--clean", action="store_true", help="remove temporary output when --output-dir is not provided")
    args = parser.parse_args()

    if args.output_dir:
        output_dir = Path(args.output_dir)
        if output_dir.exists():
            shutil.rmtree(output_dir)
    else:
        output_dir = Path(tempfile.mkdtemp(prefix="shipgrade-judge-panel-"))
        ensure_safe_target(output_dir)

    report = write_outputs(output_dir)
    if not report["ok"]:
        raise SystemExit("judge panel self-check failed")

    print("shipgrade-judge-panel-ok")
    print(f"cases={report['case_count']}")
    print(f"profiles={report['profiles']}")
    print(f"judges={report['judges']}")
    print("judge_lenses=" + ",".join(report["judge_lenses"]))
    print(f"target_unanimous_pass={report['target_unanimous_pass']}/{report['case_count']}")
    print(f"lazy_majority_rejected={report['lazy_majority_rejected']}/{report['case_count']}")
    print(f"partial_majority_rejected={report['partial_majority_rejected']}/{report['case_count']}")
    print("judge_panel_cases_path=" + (output_dir / "judge-panel-cases.jsonl").as_posix())
    print("report_path=" + (output_dir / "judge-panel-report.json").as_posix())
    print("cross_judge_packet_ready=true")
    print("deterministic_judge_panel=true")
    print("external_model_called=false")
    print("human_review_claimed=false")
    print("source_body_copied_to_public=false")
    print("secret_scan=pass")
    if args.clean and not args.output_dir:
        shutil.rmtree(output_dir)
        print("cleaned=true")
    elif not args.output_dir:
        print("note=temporary judge panel kept for inspection; rerun with --clean to remove it")


if __name__ == "__main__":
    main()
