from __future__ import annotations

import argparse
import json
import re
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "README.en.md",
    "START_HERE.md",
    "SHIPGRADE.md",
    "SKILL.md",
    "agents/openai.yaml",
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
    ".github/repo-metadata.json",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/skill_request.md",
    ".github/pull_request_template.md",
    "docs/EVIDENCE_INDEX.md",
    "docs/public-evidence-manifest.json",
    "docs/zero-install.md",
    "docs/repository-engineering-distillation-pipeline.md",
    "docs/repo-engineering-distillation-assets.md",
    "docs/sandbox-runtime-cases.md",
    "docs/high-signal-source-radar.md",
    "docs/source-promotion-queue.md",
    "docs/source-promotion-batch.md",
    "docs/source-promotion-sandbox-cases.md",
    "docs/deep-code-case-studies.md",
    "docs/evidence/source_promotion_batch.json",
    "docs/evidence/source_promotion_sandbox_cases.json",
    "docs/evidence/repo_engineering_distillation_summary.json",
    "docs/evidence/repo_engineering_distillation/repo_cards.jsonl",
    "docs/evidence/repo_engineering_distillation/pattern_cards.jsonl",
    "docs/evidence/repo_engineering_distillation/task_cards.jsonl",
    "docs/evidence/repo_engineering_distillation/eval_cases.jsonl",
    "docs/DEMO_PROOF.md",
    "docs/demo-proof.json",
    "docs/ADOPTION_PROOF.md",
    "docs/adoption-proof.json",
    "tools/shipgrade_verify.py",
    "tools/shipgrade_release_check.py",
    "tools/shipgrade_demo.py",
    "tools/shipgrade_zero_install_demo.py",
    "tools/shipgrade_patterns.py",
    "tools/github_publish_preflight.py",
    "scripts/create-public-stage.py",
    "scripts/verify.sh",
    "assets/shipgrade-hero-cn.png",
    "assets/shipgrade-loop.png",
    "assets/shipgrade-terminal-demo.png",
    "assets/shipgrade-demo.gif",
    "assets/shipgrade-proof-map-cn.png",
    "assets/shipgrade-audience-cn.png",
]

SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"][^'\"]{16,}['\"]"),
]

LOCAL_PATH_PATTERNS = [
    re.compile(r"/Users/"),
    re.compile(r"/var/folders"),
    re.compile(r"/private/var"),
    re.compile("sun" + "wuyuan"),
]


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def add(checks: list[dict[str, Any]], check_id: str, passed: bool, detail: str) -> None:
    checks.append({"id": check_id, "passed": bool(passed), "detail": detail})


def png_dimensions(rel: str) -> tuple[int, int] | None:
    path = ROOT / rel
    if not path.exists():
        return None
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return None
    return struct.unpack(">II", data[16:24])


def gif_dimensions(rel: str) -> tuple[int, int] | None:
    path = ROOT / rel
    if not path.exists():
        return None
    data = path.read_bytes()
    if not data.startswith((b"GIF87a", b"GIF89a")):
        return None
    return struct.unpack("<HH", data[6:10])


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def collect_checks(run_verify: bool) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    missing = [rel for rel in REQUIRED_FILES if not (ROOT / rel).exists()]
    add(checks, "required-files", not missing, "missing=" + ", ".join(missing[:10]) if missing else f"{len(REQUIRED_FILES)} required files present")

    readme = read_text("README.md")
    readme_terms = [
        "零安装: 只用一个 MD 文件",
        "Python 是可选增强,不是使用前提",
        "30 秒看懂差异",
        "两种接入方式",
        "SHIPGRADE.md",
        "docs/zero-install.md",
        "python3 tools/shipgrade_zero_install_demo.py --clean",
        "docs/ADOPTION_PROOF.md",
        "python3 tools/shipgrade_demo.py",
        "python3 tools/shipgrade_init.py /path/to/your-project --pattern command_topology_quality_gate",
        "python3 tools/shipgrade_patterns.py list",
        "用蒸馏出来的模式开工",
        "docs/DEMO_PROOF.md",
        "assets/shipgrade-hero-cn.png",
        "assets/shipgrade-demo.gif",
        "assets/shipgrade-proof-map-cn.png",
        "assets/shipgrade-audience-cn.png",
        "仓库工程蒸馏流水线",
        "四类蒸馏资产",
        "docs/repository-engineering-distillation-pipeline.md",
        "docs/repo-engineering-distillation-assets.md",
        "Repo Cards / 15 Pattern Cards",
        "怎么用",
        "里面有什么",
        "工作流结构",
        "证据快照",
        "发布前检查",
        "拒绝“看起来好了”的假完成",
        "docs/GITHUB_PUBLISH_PREFLIGHT.md",
        "docs/EVIDENCE_INDEX.md",
        "代码级案例研究",
        "晋级信源沙箱",
    ]
    missing_terms = [term for term in readme_terms if term not in readme]
    add(checks, "readme-launch-surface", not missing_terms, "missing_terms=" + ", ".join(missing_terms) if missing_terms else "README has hook, proof, and preflight surface")

    readme_en = read_text("README.en.md")
    readme_en_terms = [
        "Zero Install: One MD File",
        "Quick Demo",
        "Two Install Paths",
        "SHIPGRADE.md",
        "docs/zero-install.md",
        "python3 tools/shipgrade_zero_install_demo.py --clean",
        "docs/ADOPTION_PROOF.md",
        "Generated Structure",
        "What Is Inside",
        "Evidence Snapshot",
        "Release Preflight",
        "Repository Engineering Distillation Pipeline",
        "Distilled Asset Types",
        "docs/repo-engineering-distillation-assets.md",
        "Repo Cards / 15 Pattern Cards",
        "python3 tools/shipgrade_demo.py",
        "python3 tools/shipgrade_init.py",
        "python3 tools/shipgrade_init.py /path/to/your-project --pattern command_topology_quality_gate",
        "python3 tools/shipgrade_patterns.py list",
        "Use A Distilled Pattern",
        "docs/EVIDENCE_INDEX.md",
        "docs/source-promotion-sandbox-cases.md",
    ]
    missing_en_terms = [term for term in readme_en_terms if term not in readme_en]
    add(checks, "readme-english-surface", not missing_en_terms, "missing_terms=" + ", ".join(missing_en_terms) if missing_en_terms else "README.en.md has standalone onboarding surface")

    shipgrade = read_text("SHIPGRADE.md")
    shipgrade_terms = [
        "ShipGrade CN 零安装规则",
        "中文工程交付契约",
        "用户只需要说什么",
        "如果用户只说“用 ShipGrade 做”",
        "不要覆盖用户已有规则",
        "每次任务开始前",
        "每次任务完成时",
        "中文小白",
        "专业工程师",
        "可选增强,不是前置条件",
        "No Python installation",
    ]
    missing_shipgrade_terms = [term for term in shipgrade_terms if term not in shipgrade]
    add(checks, "shipgrade-zero-install-rule", not missing_shipgrade_terms, "missing_terms=" + ", ".join(missing_shipgrade_terms) if missing_shipgrade_terms else "SHIPGRADE.md is Chinese-first and zero-install")

    skill = read_text("SKILL.md")
    frontmatter = re.match(r"^---\n(.*?)\n---\n", skill, re.DOTALL)
    frontmatter_text = frontmatter.group(1) if frontmatter else ""
    add(
        checks,
        "skill-frontmatter",
        bool(frontmatter)
        and "name: ship-grade-engineering-cn" in frontmatter_text
        and "description:" in frontmatter_text
        and "Use when" in frontmatter_text,
        "machine-readable frontmatter with name/description triggers" if frontmatter else "missing YAML frontmatter",
    )

    workflow = read_text(".github/workflows/validate.yml")
    workflow_terms = ["pull_request:", "push:", "actions/setup-python@v5", "python tools/shipgrade_release_check.py"]
    missing_workflow_terms = [term for term in workflow_terms if term not in workflow]
    add(checks, "github-workflow", not missing_workflow_terms, "missing_terms=" + ", ".join(missing_workflow_terms) if missing_workflow_terms else "validate workflow has PR/push and release check")

    metadata = json.loads(read_text(".github/repo-metadata.json"))
    topics = metadata.get("topics") if isinstance(metadata.get("topics"), list) else []
    required_topics = ["agent-skills", "ai-engineering", "codex", "claude-code", "cursor", "chinese"]
    missing_topics = [topic for topic in required_topics if topic not in topics]
    add(checks, "repo-metadata", metadata.get("name") == "shipgrade-cn" and not missing_topics, f"topics={len(topics)} missing={missing_topics}")

    evidence = json.loads(read_text("docs/public-evidence-manifest.json"))
    evidence_files = evidence.get("evidence_files") if isinstance(evidence.get("evidence_files"), list) else []
    add(checks, "public-evidence-manifest", len(evidence_files) >= 16, f"evidence_files={len(evidence_files)}")

    distillation = json.loads(read_text("docs/evidence/repo_engineering_distillation_summary.json"))
    distillation_counts = {
        "repo_cards": sum(1 for line in read_text("docs/evidence/repo_engineering_distillation/repo_cards.jsonl").splitlines() if line.strip()),
        "pattern_cards": sum(1 for line in read_text("docs/evidence/repo_engineering_distillation/pattern_cards.jsonl").splitlines() if line.strip()),
        "task_cards": sum(1 for line in read_text("docs/evidence/repo_engineering_distillation/task_cards.jsonl").splitlines() if line.strip()),
        "eval_cases": sum(1 for line in read_text("docs/evidence/repo_engineering_distillation/eval_cases.jsonl").splitlines() if line.strip()),
    }
    add(
        checks,
        "repo-engineering-distillation-assets",
        distillation.get("repo_card_count", 0) >= 8
        and distillation.get("pattern_card_count", 0) >= 10
        and distillation.get("task_card_count", 0) >= 50
        and distillation.get("eval_case_count") == distillation_counts["eval_cases"]
        and distillation_counts["task_cards"] == distillation_counts["eval_cases"],
        f"summary={distillation.get('repo_card_count')}/{distillation.get('pattern_card_count')}/{distillation.get('task_card_count')}/{distillation.get('eval_case_count')} files={distillation_counts}",
    )

    patterns_validate = run([sys.executable, "tools/shipgrade_patterns.py", "validate"])
    patterns_show = run([sys.executable, "tools/shipgrade_patterns.py", "show", "command_topology_quality_gate"])
    with tempfile.TemporaryDirectory() as tmp:
        brief_path = Path(tmp) / "pattern-brief.md"
        patterns_brief = run(
            [
                sys.executable,
                "tools/shipgrade_patterns.py",
                "brief",
                "command_topology_quality_gate",
                "--type",
                "engineering_plan",
                "--write",
                str(brief_path),
            ]
        )
        brief_text = brief_path.read_text(encoding="utf-8") if brief_path.exists() else ""
    add(
        checks,
        "patterns-tool",
        patterns_validate.returncode == 0
        and "shipgrade-patterns-ok" in patterns_validate.stdout
        and patterns_show.returncode == 0
        and "先读命令拓扑" in patterns_show.stdout
        and patterns_brief.returncode == 0
        and "shipgrade-pattern-brief-ok" in patterns_brief.stdout
        and "验收标准" in brief_text,
        patterns_validate.stdout.strip().splitlines()[-1] + "; show=command_topology_quality_gate; brief=pattern-brief-ok",
    )

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "pattern-init-project"
        init_pattern = run(
            [
                sys.executable,
                "tools/shipgrade_init.py",
                str(target),
                "--pattern",
                "command_topology_quality_gate",
            ]
        )
        pattern_brief = target / ".shipgrade" / "pattern-brief.md"
        agents_text = (target / "AGENTS.md").read_text(encoding="utf-8") if (target / "AGENTS.md").exists() else ""
        brief_text = pattern_brief.read_text(encoding="utf-8") if pattern_brief.exists() else ""
        pattern_brief_exists = pattern_brief.exists()
    add(
        checks,
        "init-pattern-workbench",
        init_pattern.returncode == 0
        and pattern_brief_exists
        and "先读命令拓扑" in brief_text
        and ".shipgrade/pattern-brief.md" in agents_text,
        "shipgrade_init --pattern writes pattern-brief and wires agent rules",
    )

    batch = json.loads(read_text("docs/evidence/source_promotion_batch.json"))
    add(
        checks,
        "source-promotion-batch",
        batch.get("selected_count", 0) >= 4 and batch.get("audited_count", 0) >= 4 and batch.get("runtime_candidate_count", 0) >= 2,
        f"selected={batch.get('selected_count')} audited={batch.get('audited_count')} runtime={batch.get('runtime_candidate_count')} static_smoke={batch.get('static_smoke_pass_count')}",
    )

    promotion_sandbox = json.loads(read_text("docs/evidence/source_promotion_sandbox_cases.json"))
    add(
        checks,
        "source-promotion-sandbox-cases",
        promotion_sandbox.get("passed_case_count") == promotion_sandbox.get("case_count")
        and promotion_sandbox.get("case_count", 0) >= 3
        and promotion_sandbox.get("passed_required_step_count") == promotion_sandbox.get("required_step_count")
        and promotion_sandbox.get("configured_test_count", 0) >= 250,
        f"cases={promotion_sandbox.get('passed_case_count')}/{promotion_sandbox.get('case_count')} required={promotion_sandbox.get('passed_required_step_count')}/{promotion_sandbox.get('required_step_count')} configured_tests={promotion_sandbox.get('configured_test_count')}",
    )

    sandbox = json.loads(read_text("docs/evidence/sandbox_runtime_cases.json"))
    add(
        checks,
        "sandbox-runtime-matrix",
        sandbox.get("passed_case_count") == sandbox.get("case_count") == 3 and sandbox.get("passed_step_count") == sandbox.get("step_count") == 12,
        f"cases={sandbox.get('passed_case_count')}/{sandbox.get('case_count')} steps={sandbox.get('passed_step_count')}/{sandbox.get('step_count')}",
    )

    dims = png_dimensions(metadata.get("social_preview", ""))
    add(checks, "social-preview", bool(dims and dims[0] >= 1200 and dims[1] >= 650), f"dimensions={dims}")
    gif_dims = gif_dimensions("assets/shipgrade-demo.gif")
    add(checks, "demo-gif", bool(gif_dims and gif_dims[0] >= 1000 and gif_dims[1] >= 560), f"dimensions={gif_dims}")

    template_files = [
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/skill_request.md",
        ".github/pull_request_template.md",
    ]
    template_text = "\n".join(read_text(rel) for rel in template_files)
    add(checks, "issue-pr-templates", all((ROOT / rel).exists() for rel in template_files) and "Validation" in template_text, "issue and PR templates include validation language")

    forbidden_hits = []
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.name in {"__pycache__", ".DS_Store"} or path.name.startswith("._") or path.suffix in {".pyc", ".pyo"}:
            forbidden_hits.append(path.relative_to(ROOT).as_posix())
            continue
        if path.is_file() and path.suffix in {".md", ".py", ".json", ".yml", ".yaml", ".sh", ".mdc"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(pattern.search(text) for pattern in SECRET_PATTERNS):
                forbidden_hits.append(path.relative_to(ROOT).as_posix())
            if path.suffix in {".md", ".json", ".yml", ".yaml", ".mdc"} and any(pattern.search(text) for pattern in LOCAL_PATH_PATTERNS):
                forbidden_hits.append(path.relative_to(ROOT).as_posix())
    add(checks, "secret-and-metadata-scan", not forbidden_hits, "hits=" + ", ".join(forbidden_hits[:8]) if forbidden_hits else "no generated metadata, local paths, or secret patterns")

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
        fake_result = run([sys.executable, "tools/shipgrade_doctor.py", str(fake)])
    add(checks, "doctor-fake-rejection", fake_result.returncode != 0, "fake completion rejected" if fake_result.returncode != 0 else "fake completion accepted")

    demo_proof = read_text("docs/DEMO_PROOF.md")
    demo_proof_payload = json.loads(read_text("docs/demo-proof.json"))
    demo_terms = ["shipgrade-demo-ok", "fake_rejection=", "ship-grade-fail", "accepted=", "ship-grade-ok"]
    missing_demo_terms = [term for term in demo_terms if term not in demo_proof]
    add(
        checks,
        "demo-proof",
        not missing_demo_terms and demo_proof_payload.get("ok") is True,
        "demo proof captures init/reject/accept path" if not missing_demo_terms else "missing_terms=" + ", ".join(missing_demo_terms),
    )

    adoption_proof = read_text("docs/ADOPTION_PROOF.md")
    adoption_payload = json.loads(read_text("docs/adoption-proof.json"))
    adoption_terms = ["shipgrade-zero-install-demo-ok", "source=SHIPGRADE.md", "preserved_existing_rules=true", "python_helper_used_in_target=false", "service_started=false"]
    missing_adoption_terms = [term for term in adoption_terms if term not in adoption_proof]
    add(
        checks,
        "zero-install-adoption-proof",
        not missing_adoption_terms and adoption_payload.get("ok") is True,
        "SHIPGRADE.md-only adoption proof preserves existing rules and avoids target Python/service" if not missing_adoption_terms else "missing_terms=" + ", ".join(missing_adoption_terms),
    )

    if run_verify:
        verify = run([sys.executable, "tools/shipgrade_verify.py"])
        add(checks, "shipgrade-verify", verify.returncode == 0 and "shipgrade-verify-ok" in verify.stdout, (verify.stdout + verify.stderr)[-500:])

    return checks


def write_docs(checks: list[dict[str, Any]]) -> None:
    passed = sum(1 for check in checks if check["passed"])
    payload = {
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "kind": "local_github_publish_preflight",
        "boundary": "Local preflight only. Real remote GitHub Actions must still be verified after publishing.",
        "passed": passed,
        "total": len(checks),
        "checks": checks,
    }
    (ROOT / "docs" / "github-publish-preflight.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# GitHub Publish Preflight",
        "",
        "This is a local publish-readiness report for the standalone GitHub repository. It does not claim that remote GitHub Actions have run yet.",
        "",
        f"- passed: `{passed}/{len(checks)}`",
        "- remote CI boundary: `must be verified after the real GitHub repository exists`",
        "",
        "| check | status | detail |",
        "| --- | --- | --- |",
    ]
    for check in checks:
        status = "pass" if check["passed"] else "fail"
        detail = str(check["detail"]).replace("|", "/").replace("\n", " ")[:240]
        lines.append(f"| `{check['id']}` | `{status}` | {detail} |")
    lines.extend(
        [
            "",
            "## Publish Command Surface",
            "",
            "```bash",
            "python3 tools/github_publish_preflight.py --write-docs --run-verify",
            "python3 tools/shipgrade_verify.py",
            "python3 tools/shipgrade_zero_install_demo.py --clean",
            "python3 tools/shipgrade_demo.py",
            "python3 tools/shipgrade_init.py /tmp/my-project --pattern command_topology_quality_gate",
            "python3 tools/shipgrade_patterns.py validate",
            "python3 tools/shipgrade_patterns.py brief command_topology_quality_gate --type engineering_plan --write .shipgrade/pattern-brief.md",
            "python3 scripts/create-public-stage.py /tmp/shipgrade-cn-public --init-git",
            "bash scripts/package.sh",
            "```",
            "",
            "## Boundary",
            "",
            "- This report checks the local release artifact, not a remote GitHub repository.",
            "- After publishing, verify the real Actions run, repository topics, social preview, release archive, and issue templates on GitHub.",
        ]
    )
    (ROOT / "docs" / "GITHUB_PUBLISH_PREFLIGHT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local GitHub publish preflight checks for ShipGrade CN.")
    parser.add_argument("--write-docs", action="store_true", help="Write docs/GITHUB_PUBLISH_PREFLIGHT.md and docs/github-publish-preflight.json")
    parser.add_argument("--run-verify", action="store_true", help="Also run tools/shipgrade_verify.py")
    args = parser.parse_args()

    checks = collect_checks(run_verify=args.run_verify)
    if args.write_docs:
        write_docs(checks)
    failed = [check for check in checks if not check["passed"]]
    if failed:
        print("github-publish-preflight-fail " + " ".join(check["id"] for check in failed))
        raise SystemExit(1)
    print(f"github-publish-preflight-ok checks={len(checks)}")


if __name__ == "__main__":
    main()
