#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from shipgrade_model_replay import write_outputs as write_model_replay_outputs


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

PROFILE_LABELS = {
    "shipgrade_target": "pass",
    "lazy_or_overfit_draft": "reject",
    "partial_candidate_draft": "reject",
}

REVIEW_FIELDS = [
    "rubric_coverage",
    "forbidden_behavior",
    "source_boundary",
    "validation_evidence",
    "completion_audit",
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
    temp_dir = Path(tempfile.mkdtemp(prefix="shipgrade-review-packet-model-replay-"))
    write_model_replay_outputs(temp_dir)
    try:
        return load_jsonl(temp_dir / "model-output-replay-cases.jsonl"), "generated-temp-model-replay"
    finally:
        shutil.rmtree(temp_dir)


def has_secret_or_local_path(text: str) -> bool:
    return any(pattern.search(text) for pattern in FORBIDDEN_PATTERNS)


def blind_order(case_id: str, profiles: list[str]) -> list[str]:
    return sorted(
        profiles,
        key=lambda profile: hashlib.sha256(f"{case_id}::{profile}".encode("utf-8")).hexdigest(),
    )


def candidate_id(index: int) -> str:
    return chr(ord("A") + index)


def blind_answer(answer: str) -> str:
    return (
        answer.replace("shipgrade_target", "candidate answer")
        .replace("lazy_or_overfit_draft", "candidate answer")
        .replace("partial_candidate_draft", "candidate answer")
    )


def packet_case(case: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    profiles = blind_order(case["id"], sorted(case["candidate_outputs"].keys()))
    candidates = []
    answer_key = []
    scorecard_rows = []
    for index, profile in enumerate(profiles):
        public_id = candidate_id(index)
        answer = blind_answer(case["candidate_outputs"][profile])
        candidates.append(
            {
                "candidate_id": public_id,
                "answer": answer,
            }
        )
        answer_key.append(
            {
                "case_id": case["id"],
                "candidate_id": public_id,
                "profile": profile,
                "expected_decision": PROFILE_LABELS[profile],
            }
        )
        scorecard_rows.append(
            {
                "case_id": case["id"],
                "candidate_id": public_id,
                "reviewer_id": "",
                "reviewed_at": "",
                "rubric_coverage": None,
                "forbidden_behavior": None,
                "source_boundary": None,
                "validation_evidence": None,
                "completion_audit": None,
                "decision": "",
                "evidence_notes": "",
                "signature": "",
            }
        )
    return (
        {
            "id": case["id"],
            "source_set": case["source_set"],
            "task_type": case["task_type"],
            "repo": case["repo"],
            "license": case["license"],
            "evidence_paths": case["evidence_paths"],
            "prompt_cn": case["prompt_cn"],
            "must_include": case["must_include"],
            "must_avoid": case["must_avoid"],
            "review_fields": REVIEW_FIELDS,
            "candidates": candidates,
            "blind_profile_labels": True,
            "public_boundary": "Review packet contains metadata, prompts, rubrics, path evidence, and synthetic candidate outputs only; no upstream source bodies.",
        },
        answer_key,
        scorecard_rows,
    )


def ensure_public_safe(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    hits = [pattern.pattern for pattern in FORBIDDEN_PATTERNS if pattern.search(text)]
    if hits:
        raise SystemExit(f"public safety scan failed for {path}: {hits}")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n",
        encoding="utf-8",
    )


def write_outputs(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    cases, source = ensure_model_replay_cases()
    packet_rows = []
    key_rows = []
    scorecard_rows = []
    for case in cases:
        packet, case_key, case_scorecard = packet_case(case)
        packet_rows.append(packet)
        key_rows.extend(case_key)
        scorecard_rows.extend(case_scorecard)

    packet_path = output_dir / "review-packet-cases.jsonl"
    key_path = output_dir / "review-answer-key.jsonl"
    scorecard_path = output_dir / "review-scorecard-template.jsonl"
    report_path = output_dir / "review-packet-report.json"
    readme_path = output_dir / "README.md"

    write_jsonl(packet_path, packet_rows)
    write_jsonl(key_path, key_rows)
    write_jsonl(scorecard_path, scorecard_rows)

    packet_text = packet_path.read_text(encoding="utf-8")
    profile_labels_hidden = not any(profile in packet_text for profile in PROFILE_LABELS)
    case_count = len(cases)
    candidate_count = len(key_rows)
    report = {
        "ok": (
            case_count == 16
            and candidate_count == 48
            and len(packet_rows) == 16
            and len(scorecard_rows) == 48
            and profile_labels_hidden
        ),
        "case_count": case_count,
        "candidate_outputs": candidate_count,
        "scorecard_rows": len(scorecard_rows),
        "model_replay_source": source,
        "review_fields": REVIEW_FIELDS,
        "blind_profile_labels": profile_labels_hidden,
        "answer_key_separate": True,
        "scorecard_template_ready": True,
        "signed_review_required_before_claim": True,
        "external_model_called": False,
        "human_review_claimed": False,
        "source_body_copied_to_public": False,
        "public_boundary": "No upstream source bodies, secrets, cookies, sessions, private keys, browser profiles, auth databases, or private repositories.",
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    readme_path.write_text(
        "# ShipGrade Review Packet\n\n"
        "This packet is the handoff surface for later human, Codex, Claude, or other model reviewers. "
        "It does not claim that any external reviewer has already judged the outputs.\n\n"
        f"- cases: `{case_count}`\n"
        f"- candidate outputs: `{candidate_count}`\n"
        "- blind profile labels: `true`\n"
        "- answer key: `review-answer-key.jsonl`\n"
        "- scorecard template: `review-scorecard-template.jsonl`\n"
        "- signed review required before claim: `true`\n"
        "- external model called: `false`\n"
        "- human review claimed: `false`\n"
        "- boundary: metadata, prompts, rubrics, path evidence, and synthetic candidate outputs only; no upstream source bodies.\n\n"
        "Use `review-packet-cases.jsonl` for blind review. Use the answer key only after review decisions are recorded.\n",
        encoding="utf-8",
    )
    for path in (packet_path, key_path, scorecard_path, report_path, readme_path):
        ensure_public_safe(path)
    return report


def ensure_safe_target(path: Path) -> None:
    temp_root = Path(tempfile.gettempdir()).resolve()
    resolved = path.resolve()
    if temp_root not in resolved.parents and resolved != temp_root:
        raise SystemExit(f"refuse to clean non-temp review packet target: {resolved}")
    if not resolved.name.startswith("shipgrade-review-packet"):
        raise SystemExit(f"refuse to clean non-review-packet target: {resolved}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a blind review packet for ShipGrade candidate outputs.")
    parser.add_argument("--output-dir", help="write review packet files into this directory")
    parser.add_argument("--clean", action="store_true", help="remove temporary output when --output-dir is not provided")
    args = parser.parse_args()

    if args.output_dir:
        output_dir = Path(args.output_dir)
        if output_dir.exists():
            shutil.rmtree(output_dir)
    else:
        output_dir = Path(tempfile.mkdtemp(prefix="shipgrade-review-packet-"))
        ensure_safe_target(output_dir)

    report = write_outputs(output_dir)
    if not report["ok"]:
        raise SystemExit("review packet self-check failed")

    print("shipgrade-review-packet-ok")
    print(f"cases={report['case_count']}")
    print(f"candidate_outputs={report['candidate_outputs']}")
    print(f"scorecard_rows={report['scorecard_rows']}")
    print("blind_profile_labels=true")
    print("answer_key_separate=true")
    print("scorecard_template_ready=true")
    print("signed_review_required_before_claim=true")
    print("external_model_called=false")
    print("human_review_claimed=false")
    print("source_body_copied_to_public=false")
    print("secret_scan=pass")
    print("review_packet_path=" + (output_dir / "review-packet-cases.jsonl").as_posix())
    print("report_path=" + (output_dir / "review-packet-report.json").as_posix())
    if args.clean and not args.output_dir:
        shutil.rmtree(output_dir)
        print("cleaned=true")
    elif not args.output_dir:
        print("note=temporary review packet kept for inspection; rerun with --clean to remove it")


if __name__ == "__main__":
    main()
