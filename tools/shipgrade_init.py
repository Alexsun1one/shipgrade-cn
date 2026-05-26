#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


BEGIN = "<!-- SHIPGRADE-CN:BEGIN -->"
END = "<!-- SHIPGRADE-CN:END -->"

AGENTS_BLOCK = f"""{BEGIN}
# ShipGrade CN

Use `ship-grade-engineering-cn` when a user asks for real engineering delivery, not advice.

- Convert the request into target / non-target / evidence / acceptance / risk before editing.
- Make the smallest aligned change that can be verified.
- Run a meaningful validation command, browser smoke, log probe, or explicit manual check.
- Preserve source/license boundaries and never copy secret/token/cookie/session/auth/private key material.
- Update `.shipgrade/handoff.md` after substantive work so the next agent can continue.
{END}
"""

CLAUDE_BLOCK = f"""{BEGIN}
# ShipGrade CN

Use this project through the ShipGrade loop: define the verifiable result, inspect local rules, ship the smallest safe slice, validate it, then write a handoff. Challenge shallow completion claims and require evidence.
{END}
"""

FILES = {
    ".shipgrade/task-brief.md": """# Task Brief

## 用户原话

## 目标

## 非目标

## 当前证据

## 验收标准

## 风险边界

## 第一刀

## 需要读取

- [ ] AGENTS/CLAUDE/Cursor rules
- [ ] 相关代码/配置
- [ ] 相关测试/日志
""",
    ".shipgrade/quality-gate.md": """# Quality Gate

- [ ] 结果存在: 文件、服务、模型、配置或文档可被打开。
- [ ] 验证存在: 测试、构建、截图、日志、探针或人工检查点。
- [ ] 来源/许可证边界存在。
- [ ] 禁止事项存在: secret/token/cookie/session/auth/private key 不进入产物。
- [ ] 用户已有改动未被覆盖。
- [ ] AGENTS.md / Claude / Cursor 入口已接线或明确说明无需接线。
- [ ] handoff 已更新。
""",
    ".shipgrade/handoff.md": """# Handoff

## 当前目标

## 已完成

## 验证证据

## 来源和许可证

## 未解决

## 关键路径

## 下一步
""",
    ".shipgrade/AGENTS.snippet.md": """# ShipGrade CN Snippet

Use ship-grade-engineering-cn when the user wants real engineering delivery.

- Convert the goal into a verifiable outcome.
- Read current project rules before editing.
- Make the smallest aligned change.
- Run the fastest meaningful validation.
- Preserve source, license, validation evidence, and forbidden actions.
- Do not copy secrets, auth/session/cookie data, private keys, leaked prompts/source, or unclear-license body text.
- Write a handoff after substantive work.
""",
    "CLAUDE.shipgrade.md": """# ShipGrade CN For Claude Code

Act as a senior reviewer and teacher.

- Challenge shallow plans.
- Demand validation evidence.
- Separate fact, inference, and assumption.
- Keep Chinese-team execution details concrete.
- Treat local model outputs as drafts/checks, not final judgment.
""",
    ".cursor/rules/shipgrade.mdc": """---
description: Ship-grade Chinese engineering workflow
globs:
  - "**/*"
alwaysApply: false
---

Use ship-grade-engineering-cn for real engineering delivery. Keep changes small, verified, source-aware, license-aware, and handoff-ready.
""",
}


def write_file(root: Path, rel: str, text: str, force: bool) -> str:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return f"skip existing {rel}"
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return f"write {rel}"


def upsert_block(path: Path, block: str, force: bool) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if BEGIN in existing and END in existing:
        if not force:
            return f"skip wired {path.name}"
        pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.DOTALL)
        updated = pattern.sub(block.strip(), existing)
    else:
        separator = "\n\n" if existing.strip() else ""
        updated = existing.rstrip() + separator + block.strip()
    path.write_text(updated.rstrip() + "\n", encoding="utf-8")
    return f"wire {path.name}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize a ShipGrade CN workspace in a project.")
    parser.add_argument("target", nargs="?", default=".", help="project directory")
    parser.add_argument("--force", action="store_true", help="overwrite generated files")
    parser.add_argument("--no-wire", action="store_true", help="do not add managed ShipGrade blocks to AGENTS.md and CLAUDE.md")
    args = parser.parse_args()

    root = Path(args.target).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    print(f"shipgrade init: {root}")
    for rel, text in FILES.items():
        print(write_file(root, rel, text, args.force))
    if not args.no_wire:
        print(upsert_block(root / "AGENTS.md", AGENTS_BLOCK, args.force))
        print(upsert_block(root / "CLAUDE.md", CLAUDE_BLOCK, args.force))
    print("next: fill .shipgrade/task-brief.md, run a real validation, then update .shipgrade/handoff.md")


if __name__ == "__main__":
    main()
