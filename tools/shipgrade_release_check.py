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


def main() -> None:
    for path in ROOT.rglob("*"):
        if path.name == "__pycache__" or path.name == ".DS_Store" or path.name.startswith("._") or path.suffix in {".pyc", ".pyo"}:
            fail(f"generated metadata should not be committed: {path.relative_to(ROOT)}")

    for rel in REQUIRED_FILES:
        read(rel)
    assert_skill_frontmatter()

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
    demo_out = run([sys.executable, "tools/shipgrade_demo.py"])
    if "shipgrade-demo-ok" not in demo_out or "fake_rejection=" not in demo_out:
        fail("demo tool did not prove init/reject/accept path")
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
