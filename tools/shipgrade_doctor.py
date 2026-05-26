#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_GROUPS = {
    "result": ["已完成", "交付", "结果", "What Changed", "Done"],
    "validation": ["验证", "证据", "测试", "Validation", "Evidence"],
    "boundary": ["风险", "边界", "已知限制", "Known Limits", "Residual Risk"],
    "source_license": ["来源", "许可证", "license", "source"],
    "forbidden": ["禁止", "不要", "secret", "token", "cookie", "session"],
    "handoff": ["接手", "下一步", "handoff", "Next"],
}

SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"][^'\"]{16,}['\"]"),
]

COMMAND_WORDS = (
    "pnpm",
    "npm",
    "yarn",
    "python",
    "python3",
    "pytest",
    "uv",
    "bash",
    "sh",
    "cargo",
    "go test",
    "ruff",
    "mypy",
    "tsc",
    "vitest",
    "playwright",
    "curl",
    "make",
)

PASS_WORDS = ("passed", "pass", "通过", "成功", "ok", "exit: `0`", "exit `0`", "退出码 `0`", "returncode `0`")
VAGUE_FAILURE_WORDS = ("看起来", "应该", "可能", "大概", "未验证", "没跑", "没有运行", "待验证", "TODO", "todo", "not run")
ARTIFACT_RE = re.compile(r"`[^`]+(?:/|\\|\.tsx|\.ts|\.jsx|\.js|\.py|\.md|\.json|\.ya?ml|\.sh|\.ps1|\.html|localhost|https?://)[^`]*`")


def has_command_evidence(text: str) -> bool:
    lower = text.lower()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        lowered = line.lower()
        if not any(command in lowered for command in COMMAND_WORDS):
            continue
        if any(word.lower() in lowered for word in PASS_WORDS):
            return True
        if re.search(r"(exit|returncode|退出码|返回码)\s*:?\s*`?0`?", lowered):
            return True
    if re.search(r"浏览器\s*smoke[:：].*(点击|console|network|截图|screenshot).*(无\s*error|预期|通过|passed)", text, re.I):
        return True
    return False


def inspect(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []
    for name, terms in REQUIRED_GROUPS.items():
        if not any(term in text for term in terms):
            issues.append(f"missing:{name}")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            issues.append("possible_secret")
    if re.search(r"(?m)^\s*-\s*\[\s\]", text):
        issues.append("unchecked_quality_gate")
    if any(word in text for word in VAGUE_FAILURE_WORDS):
        issues.append("vague_or_unverified_language")
    if not ARTIFACT_RE.search(text):
        issues.append("missing_concrete_artifact_path")
    if not has_command_evidence(text):
        issues.append("missing_command_or_browser_evidence")
    forbidden_text = text.lower()
    for required in ("secret", "token", "cookie", "session"):
        if required not in forbidden_text:
            issues.append(f"missing_forbidden_boundary:{required}")
    return not issues, issues


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: shipgrade_doctor.py <markdown-file> [...]", file=sys.stderr)
        raise SystemExit(2)
    failed = False
    for raw in sys.argv[1:]:
        path = Path(raw)
        if not path.exists():
            print(f"{path}: missing")
            failed = True
            continue
        ok, issues = inspect(path)
        if ok:
            print(f"{path}: ship-grade-ok")
        else:
            print(f"{path}: ship-grade-fail {' '.join(issues)}")
            failed = True
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
