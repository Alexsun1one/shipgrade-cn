#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


BEGIN = "<!-- SHIPGRADE-CN:BEGIN -->"
END = "<!-- SHIPGRADE-CN:END -->"

AGENTS_BLOCK = f"""{BEGIN}
# ShipGrade CN

Use `ship-grade-engineering-cn` when a user asks for real engineering delivery, not advice.

- Convert the request into target / non-target / evidence / acceptance / risk before editing.
- If `.shipgrade/pattern-brief.md` exists, treat it as task evidence and cite the adopted pattern in the handoff.
- Make the smallest aligned change that can be verified.
- Run a meaningful validation command, browser smoke, log probe, or explicit manual check.
- Preserve source/license boundaries and never copy secret/token/cookie/session/auth/private key material.
- Update `.shipgrade/handoff.md` after substantive work so the next agent can continue.
{END}
"""

CLAUDE_BLOCK = f"""{BEGIN}
# ShipGrade CN

Use this project through the ShipGrade loop: define the verifiable result, inspect local rules and `.shipgrade/pattern-brief.md` when present, ship the smallest safe slice, validate it, then write a handoff. Challenge shallow completion claims and require evidence.
{END}
"""

FILES = {
    ".shipgrade/task-brief.md": """# Task Brief

## 用户原话

> 粘贴用户原始需求。不要急着改,先压成可验收任务。

## 目标

- 这次完成后,用户能看到/运行/打开什么?

## 非目标

- 这次明确不碰什么?

## 当前证据

- 相关文件:
- 相关命令:
- 相关日志/截图/外部来源:
- 可选模式 brief: `.shipgrade/pattern-brief.md`

## 验收标准

- [ ] 有具体产物路径。
- [ ] 有命令、浏览器 smoke、日志探针或人工检查点。
- [ ] 说明失败边界和未覆盖项。

## 风险边界

- 可能误伤:
- 许可证/来源:
- 禁止进入产物: secret/token/cookie/session/auth/private key。

## 第一刀

- 先做最小可验证 slice:

## 需要读取

- [ ] AGENTS/CLAUDE/Cursor rules
- [ ] `.shipgrade/pattern-brief.md`（如果存在）
- [ ] 相关代码/配置
- [ ] 相关测试/日志
""",
    ".shipgrade/quality-gate.md": """# Quality Gate

## Result

- [ ] 结果存在: 文件、服务、模型、配置或文档可被打开。
- [ ] 改动范围和非目标清楚。
- [ ] 用户已有改动未被覆盖。

## Evidence

- [ ] 验证存在: 测试、构建、截图、日志、探针或人工检查点。
- [ ] 验证命令写明退出结果或观察结果。
- [ ] 如果使用蒸馏模式,已引用 `.shipgrade/pattern-brief.md`。

## Source / License / Safety

- [ ] 来源/许可证边界存在。
- [ ] 禁止事项存在: secret/token/cookie/session/auth/private key 不进入产物。
- [ ] 没有复制上游源码正文或许可证不清正文。

## Handoff

- [ ] AGENTS.md / Claude / Cursor 入口已接线或明确说明无需接线。
- [ ] `.shipgrade/handoff.md` 已更新。
- [ ] 下一步入口足够具体,下一位 agent 可以继续。
""",
    ".shipgrade/handoff.md": """# Handoff

## 当前目标

## 采用的蒸馏模式

- Pattern brief: `.shipgrade/pattern-brief.md`（如未使用,说明原因）

## 已完成

| 产物 | 路径 | 说明 |
| --- | --- | --- |

## 验证证据

| 命令/检查 | 结果 | 备注 |
| --- | --- | --- |

## 来源和许可证

## 风险边界

## 未解决

## 关键路径

## 下一步
""",
    ".shipgrade/AGENTS.snippet.md": """# ShipGrade CN Snippet

Use ship-grade-engineering-cn when the user wants real engineering delivery.

- Convert the goal into a verifiable outcome.
- Read current project rules before editing.
- If `.shipgrade/pattern-brief.md` exists, use it as evidence, not decoration.
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
- Use `.shipgrade/pattern-brief.md` when present to review against an explicit engineering pattern.
- Keep Chinese-team execution details concrete.
- Treat local model outputs as drafts/checks, not final judgment.
""",
    ".cursor/rules/shipgrade.mdc": """---
description: Ship-grade Chinese engineering workflow
globs:
  - "**/*"
alwaysApply: false
---

Use ship-grade-engineering-cn for real engineering delivery. Keep changes small, verified, source-aware, license-aware, pattern-aware when `.shipgrade/pattern-brief.md` exists, and handoff-ready.
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


def render_pattern_brief(root: Path, pattern_key: str, task_type: str, force: bool) -> str:
    brief = root / ".shipgrade" / "pattern-brief.md"
    if brief.exists() and not force:
        return "skip existing .shipgrade/pattern-brief.md"
    patterns_tool = Path(__file__).resolve().with_name("shipgrade_patterns.py")
    if not patterns_tool.exists():
        raise SystemExit("shipgrade_patterns.py not found; cannot render pattern brief")
    result = subprocess.run(
        [
            sys.executable,
            str(patterns_tool),
            "brief",
            pattern_key,
            "--type",
            task_type,
            "--write",
            str(brief),
        ],
        cwd=patterns_tool.parents[1],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(result.stdout + result.stderr)
    return f"write .shipgrade/pattern-brief.md pattern={pattern_key} type={task_type}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize a ShipGrade CN workspace in a project.")
    parser.add_argument("target", nargs="?", default=".", help="project directory")
    parser.add_argument("--force", action="store_true", help="overwrite generated files")
    parser.add_argument("--no-wire", action="store_true", help="do not add managed ShipGrade blocks to AGENTS.md and CLAUDE.md")
    parser.add_argument("--pattern", help="also render .shipgrade/pattern-brief.md from a distilled pattern key")
    parser.add_argument("--task-type", default="engineering_plan", help="task type for --pattern, for example engineering_plan or review")
    args = parser.parse_args()

    root = Path(args.target).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    print(f"shipgrade init: {root}")
    for rel, text in FILES.items():
        print(write_file(root, rel, text, args.force))
    if args.pattern:
        print(render_pattern_brief(root, args.pattern, args.task_type, args.force))
    if not args.no_wire:
        print(upsert_block(root / "AGENTS.md", AGENTS_BLOCK, args.force))
        print(upsert_block(root / "CLAUDE.md", CLAUDE_BLOCK, args.force))
    if args.pattern:
        print("next: fill .shipgrade/task-brief.md, cite .shipgrade/pattern-brief.md, run validation, then update .shipgrade/handoff.md")
    else:
        print("next: fill .shipgrade/task-brief.md, optionally add --pattern on re-run, run validation, then update .shipgrade/handoff.md")


if __name__ == "__main__":
    main()
