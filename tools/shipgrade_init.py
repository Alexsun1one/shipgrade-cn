#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
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
    ".shipgrade/START_HERE.md": """# ShipGrade Workbench Start

ShipGrade CN 不是“装上就自动做出很牛产品”的魔法按钮。它给你的 AI 编程工具加上一层产品总工和交付审计器: 先把想法压成可验证任务,再要求它交付能打开、能运行、能复查的结果。

## 第一眼先打开什么

- 可视化状态页: `.shipgrade/product-map.html`
- 任务入口: `.shipgrade/task-brief.md`
- 质量门: `.shipgrade/quality-gate.md`
- 交接单: `.shipgrade/handoff.md`

## 第一步会输出什么

1. 一个项目工作台,告诉你“目标、第一刀、证据、质量门、接手点”分别在哪里。
2. 一份 task brief,把口语需求变成目标、非目标、当前证据、验收标准和风险边界。
3. 一份 quality gate,防止 agent 用“看起来好了”冒充完成。
4. 一份 handoff,让未来的你或下一个 agent 能继续。

## 对你的工作有什么帮助

- 新项目: 先生成可执行 brief,避免从空白聊天开始。
- 修 bug: 先锁定可复现证据和最小验证命令。
- 做产品: 先明确用户能看到什么、怎么验收、哪些暂时不做。
- 多 agent 协作: Codex / Claude / Cursor 读同一套规则,不会各说各话。

## 当前想法

{{SHIPGRADE_IDEA_MD}}
""",
    ".shipgrade/product-map.html": """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
  <title>ShipGrade Workbench</title>
  <style>
    :root { --bg:#f8fafc; --panel:#fff; --ink:#0f172a; --muted:#475569; --line:#dbe4ee; --teal:#0f766e; --blue:#2563eb; --amber:#b45309; --rose:#be123c; }
    * { box-sizing: border-box; }
    body { margin:0; background:var(--bg); color:var(--ink); font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; line-height:1.55; }
    main { width:min(1120px,calc(100% - 32px)); margin:0 auto; padding:40px 0 56px; }
    header { display:grid; grid-template-columns:1.4fr .9fr; gap:24px; align-items:end; border-bottom:1px solid var(--line); padding-bottom:28px; }
    h1 { margin:0 0 12px; font-size:clamp(30px,5vw,56px); line-height:1.05; letter-spacing:0; }
    h2 { margin:0 0 12px; font-size:22px; letter-spacing:0; }
    p { margin:0; color:var(--muted); }
    .eyebrow { color:var(--teal); font-weight:700; font-size:13px; margin-bottom:10px; }
    .status,.step,.panel { background:var(--panel); border:1px solid var(--line); border-radius:8px; }
    .status { display:grid; gap:10px; padding:18px; }
    .status div { display:flex; justify-content:space-between; gap:16px; border-bottom:1px solid #edf2f7; padding-bottom:8px; font-size:14px; }
    .status div:last-child { border-bottom:0; padding-bottom:0; }
    .section { padding-top:30px; }
    .grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:14px; }
    .step { padding:18px; min-height:190px; }
    .step b { display:inline-flex; width:32px; height:32px; align-items:center; justify-content:center; border-radius:999px; color:#fff; margin-bottom:14px; font-size:14px; }
    .blue{background:var(--blue)} .teal{background:var(--teal)} .amber{background:var(--amber)} .rose{background:var(--rose)}
    .step h3 { margin:0 0 8px; font-size:17px; letter-spacing:0; }
    code { font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:.92em; background:#eef2f7; border:1px solid #d8e1ec; border-radius:6px; padding:2px 5px; }
    .two { display:grid; grid-template-columns:1fr 1fr; gap:18px; }
    .panel { padding:20px; }
    ul { margin:0; padding-left:20px; color:var(--muted); }
    li + li { margin-top:8px; }
    .next { border-left:4px solid var(--teal); background:#ecfdf5; padding:18px 20px; border-radius:8px; }
    .idea { background:#f0fdfa; border:1px solid #99f6e4; border-radius:8px; padding:18px 20px; }
    .idea p { overflow-wrap:anywhere; color:#134e4a; }
    @media (max-width:860px){ main{width:min(100% - 24px,680px); padding-top:28px} header,.two{grid-template-columns:1fr} .grid{grid-template-columns:1fr} .step{min-height:auto} }
  </style>
</head>
<body>
  <main>
    <header>
      <div><div class="eyebrow">ShipGrade Workbench</div><h1>把想法变成可验证交付</h1><p>它不会替你自动做出伟大产品,但会让 AI 从第一步开始围绕目标、证据、质量门和接手点工作。</p></div>
      <aside class="status" aria-label="Project status"><div><span>当前阶段</span><strong>Brief first</strong></div><div><span>第一步</span><strong>填写 task brief</strong></div><div><span>完成标准</span><strong>证据优先</strong></div><div><span>可见产物</span><strong>4 个工作台文件</strong></div></aside>
    </header>
    <section class="section"><div class="idea"><h2>当前想法</h2><p>{{SHIPGRADE_IDEA_HTML}}</p></div></section>
    <section class="section"><h2>第一轮会输出什么</h2><div class="grid">
      <article class="step"><b class="blue">1</b><h3>任务 Brief</h3><p><code>task-brief.md</code> 把口语需求压成目标、非目标、证据、验收和第一刀。</p></article>
      <article class="step"><b class="teal">2</b><h3>质量门</h3><p><code>quality-gate.md</code> 要求测试、截图、日志、命令或人工检查点,拒绝假完成。</p></article>
      <article class="step"><b class="amber">3</b><h3>Agent 接线</h3><p><code>AGENTS.md</code>、<code>CLAUDE.md</code> 和 Cursor rules 让工具按同一套交付闭环工作。</p></article>
      <article class="step"><b class="rose">4</b><h3>交接单</h3><p><code>handoff.md</code> 记录结果、验证、风险和下一步,让下一位 agent 能接着做。</p></article>
    </div></section>
    <section class="section two"><div class="panel"><h2>对产品工作有什么帮助</h2><ul><li>把“做个很牛的东西”拆成用户能看到的第一版。</li><li>先定义验收标准,再让 agent 写代码或改设计。</li><li>每次交付都留下证据和下一步,减少返工。</li><li>把 Codex、Claude、Cursor 的行为对齐到同一套规则。</li></ul></div><div class="panel"><h2>它不会承诺什么</h2><ul><li>不会保证安装后自动产生市场成功。</li><li>不会把一个小 smoke 冒充完整质量证明。</li><li>不会复制 secret、cookie、session 或许可证不清的源码正文。</li><li>不会把模型草稿当成最终质量裁判。</li></ul></div></section>
    <section class="section"><div class="next"><h2>现在该做的第一步</h2><p>打开 <code>.shipgrade/task-brief.md</code>,粘贴用户原话,写清楚“用户完成后能看到什么”。然后让 agent 按 ShipGrade 规则实现最小可验证 slice。</p></div></section>
  </main>
</body>
</html>
""",
    ".shipgrade/task-brief.md": """# Task Brief

## 用户原话

{{SHIPGRADE_IDEA_MD}}

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


def normalize_idea(raw: str | None) -> str:
    if not raw:
        return ""
    lines = [line.strip() for line in raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    idea = "\n".join(line for line in lines if line)
    return idea[:500]


def quote_markdown(text: str) -> str:
    if not text:
        return "> 粘贴用户原始需求。不要急着改,先压成可验收任务。"
    return "\n".join(f"> {line}" for line in text.splitlines())


def render_template(text: str, idea: str) -> str:
    idea_md = quote_markdown(idea)
    idea_html = html.escape(idea) if idea else "尚未填写。可以重新运行 <code>shipgrade_init.py --idea \"...\"</code>,或直接编辑 <code>.shipgrade/task-brief.md</code>。"
    return text.replace("{{SHIPGRADE_IDEA_MD}}", idea_md).replace("{{SHIPGRADE_IDEA_HTML}}", idea_html)


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
    parser.add_argument("--idea", help="prefill .shipgrade/task-brief.md and product-map.html from a one-line user idea")
    args = parser.parse_args()

    root = Path(args.target).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    idea = normalize_idea(args.idea)
    print(f"shipgrade init: {root}")
    for rel, text in FILES.items():
        print(write_file(root, rel, render_template(text, idea), args.force))
    if args.pattern:
        print(render_pattern_brief(root, args.pattern, args.task_type, args.force))
    if not args.no_wire:
        print(upsert_block(root / "AGENTS.md", AGENTS_BLOCK, args.force))
        print(upsert_block(root / "CLAUDE.md", CLAUDE_BLOCK, args.force))
    print("visible=.shipgrade/product-map.html")
    print(f"idea_prefilled={str(bool(idea)).lower()}")
    if args.pattern:
        print("next: open .shipgrade/START_HERE.md, review .shipgrade/task-brief.md, cite .shipgrade/pattern-brief.md, run validation, then update .shipgrade/handoff.md")
    else:
        print("next: open .shipgrade/START_HERE.md, review .shipgrade/task-brief.md, optionally add --pattern on re-run, run validation, then update .shipgrade/handoff.md")


if __name__ == "__main__":
    main()
