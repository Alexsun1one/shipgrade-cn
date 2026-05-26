#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "START_HERE.md",
    "SHIPGRADE.md",
    "SKILL.md",
    "AGENTS.md",
    "CLAUDE.md",
    "cursor-rules.mdc",
    "LICENSE.md",
    "NOTICE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "RELEASE_CHECKLIST.md",
    ".github/workflows/validate.yml",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/skill_request.md",
    ".github/pull_request_template.md",
    "agents/openai.yaml",
    "tools/shipgrade_doctor.py",
    "tools/shipgrade_init.py",
    "tools/shipgrade_demo.py",
    "tools/shipgrade_patterns.py",
    "tools/shipgrade_zero_install_demo.py",
    "tools/shipgrade_external_trial.py",
    "tools/shipgrade_multi_repo_eval.py",
    "tools/shipgrade_real_issue_case.py",
    "tools/shipgrade_real_task_suite.py",
    "tools/shipgrade_eval_corpus.py",
    "tools/shipgrade_holdout_replay.py",
    "tools/shipgrade_model_replay.py",
    "tools/shipgrade_judge_panel.py",
    "tools/install_skill.py",
    "tools/shipgrade_release_check.py",
    "demo/demo-task.md",
    "demo/demo-output.md",
    "docs/source-attribution.md",
    "docs/source-depth-dossier.md",
    "docs/deep-code-case-studies.md",
    "docs/transcript-evidence.md",
    "manifest.json",
    "QUALITY_REPORT.json",
]

SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"][^'\"]{16,}['\"]"),
]


def fail(message: str) -> None:
    print(f"release-check-fail: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        fail(f"missing {rel}")
    text = path.read_text(encoding="utf-8")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            fail(f"possible secret in {rel}")
    return text


def run(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        fail(f"command failed: {' '.join(args)}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def assert_skill_frontmatter() -> None:
    text = read("SKILL.md")
    if not text.startswith("---\n"):
        fail("SKILL.md missing YAML frontmatter")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail("SKILL.md invalid YAML frontmatter")
    frontmatter = match.group(1)
    if "name: ship-grade-engineering-cn" not in frontmatter:
        fail("SKILL.md frontmatter missing canonical name")
    if "description:" not in frontmatter or "Use when" not in frontmatter:
        fail("SKILL.md frontmatter description must include trigger guidance")


def assert_world_class_contract() -> None:
    shipgrade = read("SHIPGRADE.md")
    for term in (
        "不是计划交付",
        "主控智能",
        "信源蒸馏怎么做",
        "证据矩阵",
        "完成审计",
        "不要用一个小 smoke 证明一个大目标",
    ):
        if term not in shipgrade:
            fail(f"SHIPGRADE.md missing world-class contract term: {term}")

    skill = read("SKILL.md")
    for term in (
        "主控智能职责",
        "信源蒸馏协议",
        "完成审计",
        "不能用计划、loss、stars、README 摘要或单个 smoke 冒充质量",
        "中文小白能入口,进阶用户能执行,专业工程师能审计",
    ):
        if term not in skill:
            fail(f"SKILL.md missing world-class contract term: {term}")


def main() -> None:
    for path in ROOT.rglob("*"):
        if path.name == "__pycache__" or path.name == ".DS_Store" or path.name.startswith("._") or path.suffix in {".pyc", ".pyo"}:
            fail(f"generated metadata should not be committed: {path.relative_to(ROOT)}")

    for rel in REQUIRED_FILES:
        read(rel)
    assert_skill_frontmatter()
    assert_world_class_contract()

    manifest = json.loads(read("manifest.json"))
    files = manifest.get("files") or {}
    for key in ("license", "notice", "release_check", "install", "github_workflow"):
        if key not in files:
            fail(f"manifest missing files.{key}")
    if manifest.get("release_readiness", {}).get("standalone_ci") is not True:
        fail("manifest missing standalone CI readiness")

    quality = json.loads(read("QUALITY_REPORT.json"))
    if quality.get("release_files", 0) < 8:
        fail("quality report missing release file count")
    if quality.get("standalone_release_check") is not True:
        fail("quality report missing standalone release check flag")

    doctor_out = run([sys.executable, "tools/shipgrade_doctor.py", "demo/demo-output.md"])
    if "ship-grade-ok" not in doctor_out:
        fail("doctor did not accept demo output")
    patterns_out = run([sys.executable, "tools/shipgrade_patterns.py", "validate"])
    if "shipgrade-patterns-ok" not in patterns_out:
        fail("patterns tool did not validate distilled assets")
    patterns_show = run([sys.executable, "tools/shipgrade_patterns.py", "show", "command_topology_quality_gate"])
    if "先读命令拓扑" not in patterns_show:
        fail("patterns tool did not show core pattern")
    with tempfile.TemporaryDirectory() as tmp:
        pattern_target = Path(tmp) / "pattern-project"
        run([sys.executable, "tools/shipgrade_init.py", str(pattern_target), "--pattern", "command_topology_quality_gate"])
        pattern_brief = pattern_target / ".shipgrade" / "pattern-brief.md"
        if not pattern_brief.exists() or "先读命令拓扑" not in pattern_brief.read_text(encoding="utf-8"):
            fail("init --pattern did not create pattern brief")
    zero_install_out = run([sys.executable, "tools/shipgrade_zero_install_demo.py", "--clean"])
    if "shipgrade-zero-install-demo-ok" not in zero_install_out or "preserved_existing_rules=true" not in zero_install_out:
        fail("zero-install demo did not prove SHIPGRADE.md adoption")
    external_trial_out = run([sys.executable, "tools/shipgrade_external_trial.py", "--clean"])
    if "shipgrade-external-trial-ok" not in external_trial_out or "doctor=.shipgrade/handoff.md: ship-grade-ok" not in external_trial_out:
        fail("external trial did not prove SHIPGRADE.md adoption on a public repo")
    multi_repo_eval_out = run([sys.executable, "tools/shipgrade_multi_repo_eval.py", "--clean"])
    if "shipgrade-multi-repo-eval-ok" not in multi_repo_eval_out or "passed=3" not in multi_repo_eval_out:
        fail("multi-repo eval did not prove repeated SHIPGRADE.md adoption")
    demo_out = run([sys.executable, "tools/shipgrade_demo.py"])
    if "shipgrade-demo-ok" not in demo_out or "fake_rejection=" not in demo_out:
        fail("demo tool did not prove init/reject/accept path")
    real_issue_out = run([sys.executable, "tools/shipgrade_real_issue_case.py", "--clean"])
    if (
        "shipgrade-real-issue-case-ok" not in real_issue_out
        or "repo=pallets/click" not in real_issue_out
        or "issue=click-required-option-regression" not in real_issue_out
        or "doctor=.shipgrade/handoff.md: ship-grade-ok" not in real_issue_out
    ):
        fail("real issue case did not prove ShipGrade controller workflow on a real public repo")
    task_suite_out = run([sys.executable, "tools/shipgrade_real_task_suite.py", "--clean"])
    if (
        "shipgrade-real-task-suite-ok" not in task_suite_out
        or "cases=4" not in task_suite_out
        or "task_types=repair,migration,review,anti_pattern_detection" not in task_suite_out
        or "chosen_rejected_samples=true" not in task_suite_out
        or "doctor_handoffs=2/2" not in task_suite_out
    ):
        fail("real task suite did not prove multi-type engineering eval coverage")
    eval_corpus_out = run([sys.executable, "tools/shipgrade_eval_corpus.py", "--clean"])
    if (
        "shipgrade-eval-corpus-ok" not in eval_corpus_out
        or "cases=4" not in eval_corpus_out
        or "chosen_passed=4/4" not in eval_corpus_out
        or "rejected_failed=4/4" not in eval_corpus_out
        or "rubric_scored=true" not in eval_corpus_out
        or "source_body_copied_to_public=false" not in eval_corpus_out
    ):
        fail("eval corpus did not prove chosen/rejected scoring")
    holdout_replay_out = run([sys.executable, "tools/shipgrade_holdout_replay.py", "--clean"])
    if (
        "shipgrade-holdout-replay-ok" not in holdout_replay_out
        or "cases=8" not in holdout_replay_out
        or "base_overlap_repos=0" not in holdout_replay_out
        or "strong_passed=8/8" not in holdout_replay_out
        or "weak_failed=8/8" not in holdout_replay_out
        or "holdout_not_training=true" not in holdout_replay_out
        or "rubric_scored=true" not in holdout_replay_out
        or "source_body_copied_to_public=false" not in holdout_replay_out
        or "secret_scan=pass" not in holdout_replay_out
    ):
        fail("holdout replay did not prove unseen-repo chosen/weak separation")
    model_replay_out = run([sys.executable, "tools/shipgrade_model_replay.py", "--clean"])
    if (
        "shipgrade-model-replay-ok" not in model_replay_out
        or "cases=12" not in model_replay_out
        or "base_eval_cases=4" not in model_replay_out
        or "holdout_cases=8" not in model_replay_out
        or "profiles=3" not in model_replay_out
        or "target_passed=12/12" not in model_replay_out
        or "lazy_failed=12/12" not in model_replay_out
        or "candidate_outputs_replayed=true" not in model_replay_out
        or "failure_stratified=true" not in model_replay_out
        or "source_body_copied_to_public=false" not in model_replay_out
        or "secret_scan=pass" not in model_replay_out
    ):
        fail("model output replay did not prove candidate replay and failure stratification")
    judge_panel_out = run([sys.executable, "tools/shipgrade_judge_panel.py", "--clean"])
    if (
        "shipgrade-judge-panel-ok" not in judge_panel_out
        or "cases=12" not in judge_panel_out
        or "profiles=3" not in judge_panel_out
        or "judges=3" not in judge_panel_out
        or "judge_lenses=controller_quality,source_boundary,completion_audit" not in judge_panel_out
        or "target_unanimous_pass=12/12" not in judge_panel_out
        or "lazy_majority_rejected=12/12" not in judge_panel_out
        or "partial_majority_rejected=12/12" not in judge_panel_out
        or "cross_judge_packet_ready=true" not in judge_panel_out
        or "deterministic_judge_panel=true" not in judge_panel_out
        or "external_model_called=false" not in judge_panel_out
        or "human_review_claimed=false" not in judge_panel_out
        or "source_body_copied_to_public=false" not in judge_panel_out
        or "secret_scan=pass" not in judge_panel_out
    ):
        fail("judge panel did not prove deterministic cross-review readiness")
    with tempfile.TemporaryDirectory() as tmp:
        fake = Path(tmp) / "fake-pass.md"
        fake.write_text(
            "# Fake Pass\n\n"
            "## 已完成\n结果: 看起来好了。\n\n"
            "## 验证证据\n验证: 应该通过。\n\n"
            "## 来源和许可证\n来源: 当前项目。许可证: 未引入外部代码。\n\n"
            "## 风险边界\n风险: 可能还有问题。\n\n"
            "## 禁止事项\n不要复制 secret token cookie session。\n\n"
            "## 接手入口\n下一步: TODO。\n",
            encoding="utf-8",
        )
        fake_result = subprocess.run(
            [sys.executable, "tools/shipgrade_doctor.py", str(fake)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if fake_result.returncode == 0:
            fail("doctor accepted fake completion evidence")

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "project"
        run([sys.executable, "tools/shipgrade_init.py", str(target)])
        if not (target / ".shipgrade" / "task-brief.md").exists():
            fail("init did not create task brief")
        if "SHIPGRADE-CN:BEGIN" not in (target / "AGENTS.md").read_text(encoding="utf-8"):
            fail("init did not wire AGENTS.md")
        if "SHIPGRADE-CN:BEGIN" not in (target / "CLAUDE.md").read_text(encoding="utf-8"):
            fail("init did not wire CLAUDE.md")
        install_target = Path(tmp) / "skill-install"
        run([sys.executable, "tools/install_skill.py", "--target", str(install_target)])
        if not (install_target / "SKILL.md").exists():
            fail("install did not copy SKILL.md")

    print("shipgrade-release-check-ok")


if __name__ == "__main__":
    main()
