#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "evidence" / "repo_engineering_distillation"
PATTERNS = ASSET_DIR / "pattern_cards.jsonl"
TASKS = ASSET_DIR / "task_cards.jsonl"
EVALS = ASSET_DIR / "eval_cases.jsonl"

TASK_TYPES = {
    "engineering_plan",
    "review",
    "repair",
    "migration",
    "anti_pattern",
    "kickoff_doc",
}


def fail(message: str) -> None:
    raise SystemExit(f"shipgrade-patterns-fail: {message}")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    rows: list[dict[str, Any]] = []
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"bad jsonl {path.relative_to(ROOT)}:{index}: {exc}")
        if not isinstance(value, dict):
            fail(f"jsonl row is not object: {path.relative_to(ROOT)}:{index}")
        rows.append(value)
    return rows


def load_assets() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    return load_jsonl(PATTERNS), load_jsonl(TASKS), load_jsonl(EVALS)


def pattern_key(value: dict[str, Any]) -> str:
    key = value.get("pattern_key")
    if isinstance(key, str) and key:
        return key
    pattern_id = value.get("pattern_id")
    if isinstance(pattern_id, str) and pattern_id.startswith("pattern:"):
        return pattern_id.split(":", 1)[1]
    return ""


def task_pattern_key(value: dict[str, Any]) -> str:
    task_id = value.get("task_id")
    if isinstance(task_id, str) and task_id.startswith("task:"):
        parts = task_id.split(":")
        if len(parts) >= 3:
            return parts[1]
    judge = value.get("judge_notes")
    source = judge.get("source_pattern_id") if isinstance(judge, dict) else None
    if isinstance(source, str) and source.startswith("pattern:"):
        return source.split(":", 1)[1]
    return ""


def task_type(value: dict[str, Any]) -> str:
    raw = value.get("task_type")
    return raw if isinstance(raw, str) else ""


def find_pattern(patterns: list[dict[str, Any]], key: str) -> dict[str, Any]:
    for pattern in patterns:
        if pattern_key(pattern) == key:
            return pattern
    known = ", ".join(sorted(pattern_key(pattern) for pattern in patterns if pattern_key(pattern)))
    fail(f"unknown pattern '{key}'. known: {known}")


def find_task(tasks: list[dict[str, Any]], key: str, wanted_type: str) -> dict[str, Any]:
    if wanted_type not in TASK_TYPES:
        fail(f"unknown task type '{wanted_type}'. choose one of: {', '.join(sorted(TASK_TYPES))}")
    for task in tasks:
        if task_pattern_key(task) == key and task_type(task) == wanted_type:
            return task
    available = sorted({task_type(task) for task in tasks if task_pattern_key(task) == key and task_type(task)})
    fail(f"no task for pattern '{key}' type '{wanted_type}'. available: {', '.join(available)}")


def evidence_paths(pattern: dict[str, Any], limit: int = 10) -> list[str]:
    paths: list[str] = []
    for evidence in pattern.get("code_evidence", []):
        if not isinstance(evidence, dict):
            continue
        repo = evidence.get("repo")
        for path in evidence.get("paths", []):
            if isinstance(repo, str) and isinstance(path, str):
                paths.append(f"{repo}:{path}")
            if len(paths) >= limit:
                return paths
    return paths


def print_wrapped(title: str, body: Any) -> None:
    if isinstance(body, list):
        print(f"{title}:")
        for item in body:
            print(f"- {item}")
        return
    text = "" if body is None else str(body)
    print(f"{title}:")
    print(textwrap.fill(text, width=88, subsequent_indent="  "))


def cmd_list(_: argparse.Namespace) -> None:
    patterns, tasks, _ = load_assets()
    task_counts: dict[str, int] = {}
    for task in tasks:
        key = task_pattern_key(task)
        if key:
            task_counts[key] = task_counts.get(key, 0) + 1
    print("pattern_key | name_cn | repos | tasks")
    print("--- | --- | ---: | ---:")
    for pattern in sorted(patterns, key=pattern_key):
        key = pattern_key(pattern)
        repos = len(pattern.get("source_repos", []) or [])
        print(f"{key} | {pattern.get('name_cn', '')} | {repos} | {task_counts.get(key, 0)}")


def cmd_show(args: argparse.Namespace) -> None:
    patterns, tasks, _ = load_assets()
    pattern = find_pattern(patterns, args.pattern_key)
    key = pattern_key(pattern)
    available_types = sorted({task_type(task) for task in tasks if task_pattern_key(task) == key and task_type(task)})
    print(f"# {pattern.get('name_cn', key)}")
    print()
    print(f"- key: `{key}`")
    print(f"- English: {pattern.get('name_en', '')}")
    print(f"- source repos: {', '.join(pattern.get('source_repos', [])[:8])}")
    print(f"- available task types: {', '.join(available_types)}")
    print()
    print_wrapped("适用场景", pattern.get("applicable_when", ""))
    print_wrapped("问题", pattern.get("problem", ""))
    print_wrapped("解法", pattern.get("solution", ""))
    print_wrapped("优点", pattern.get("strengths", []))
    print_wrapped("代价", pattern.get("tradeoffs", []))
    print_wrapped("迁移判断", pattern.get("migration_judgement_cn", ""))
    print("证据路径:")
    for path in evidence_paths(pattern, limit=args.evidence_limit):
        print(f"- {path}")


def cmd_task(args: argparse.Namespace) -> None:
    patterns, tasks, _ = load_assets()
    pattern = find_pattern(patterns, args.pattern_key)
    task = find_task(tasks, pattern_key(pattern), args.type)
    print(f"# {task.get('title_cn', task.get('task_id', 'ShipGrade Task'))}")
    print()
    print_wrapped("任务上下文", task.get("context", ""))
    print("证据路径:")
    for path in task.get("repo_context", [])[: args.evidence_limit]:
        print(f"- {path}")
    expected = task.get("expected_answer") if isinstance(task.get("expected_answer"), dict) else {}
    print_wrapped("答案必须包含", expected.get("plan_should_include", []))
    print_wrapped("坏答案/反模式", expected.get("bad_answer_patterns", []))


def render_brief(pattern: dict[str, Any], task: dict[str, Any], evidence_limit: int) -> str:
    expected = task.get("expected_answer") if isinstance(task.get("expected_answer"), dict) else {}
    include = expected.get("plan_should_include", [])
    bad = expected.get("bad_answer_patterns", [])
    lines = [
        "# ShipGrade Pattern Brief",
        "",
        f"模式: {pattern.get('name_cn', pattern_key(pattern))}",
        f"Pattern Key: `{pattern_key(pattern)}`",
        "",
        "## 适用场景",
        str(pattern.get("applicable_when", "")),
        "",
        "## 当前任务",
        str(task.get("context", "")),
        "",
        "## 交付时必须包含",
    ]
    lines.extend(f"- {item}" for item in include)
    lines.extend(["", "## 坏答案 / 反模式"])
    lines.extend(f"- {item}" for item in bad)
    lines.extend(["", "## 证据路径"])
    for path in task.get("repo_context", [])[:evidence_limit]:
        lines.append(f"- {path}")
    lines.extend(
        [
            "",
            "## 验收标准",
            "- 输出要同时照顾中文小白、进阶用户和专业工程师。",
            "- 必须有具体文件路径、命令、截图、日志或人工检查点。",
            "- 不能复制上游源码正文; 只迁移模式、边界、验收语言和路径级证据。",
            "- 交付说明必须写清结果、验证、风险、安全边界和接手入口。",
            "",
            "## 来源边界",
            str(pattern.get("public_boundary", "Evidence paths and metrics only; no source-body copying.")),
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def cmd_brief(args: argparse.Namespace) -> None:
    patterns, tasks, _ = load_assets()
    pattern = find_pattern(patterns, args.pattern_key)
    task = find_task(tasks, pattern_key(pattern), args.type)
    brief = render_brief(pattern, task, args.evidence_limit)
    if args.write:
        out = Path(args.write)
        if not out.is_absolute():
            out = ROOT / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(brief, encoding="utf-8")
        display_path = out.relative_to(ROOT).as_posix() if ROOT in out.parents else f"<external>/{out.name}"
        print(f"shipgrade-pattern-brief-ok path={display_path}")
        return
    print(brief, end="")


def cmd_validate(_: argparse.Namespace) -> None:
    patterns, tasks, evals = load_assets()
    keys = {pattern_key(pattern) for pattern in patterns}
    if len(patterns) < 10:
        fail(f"too few patterns: {len(patterns)}")
    if len(tasks) < 50:
        fail(f"too few tasks: {len(tasks)}")
    if len(evals) != len(tasks):
        fail(f"task/eval mismatch: tasks={len(tasks)} evals={len(evals)}")
    missing_task_patterns = sorted({task_pattern_key(task) for task in tasks if task_pattern_key(task)} - keys)
    if missing_task_patterns:
        fail("tasks reference unknown patterns: " + ", ".join(missing_task_patterns))
    for required in ("agent_surface_contract", "command_topology_quality_gate", "eval_first_quality_loop"):
        if required not in keys:
            fail(f"missing core pattern: {required}")
    print(f"shipgrade-patterns-ok patterns={len(patterns)} tasks={len(tasks)} evals={len(evals)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Use ShipGrade CN distilled Repo/Pattern/Task/Eval assets.")
    sub = parser.add_subparsers(required=True)

    list_parser = sub.add_parser("list", help="List distilled engineering patterns.")
    list_parser.set_defaults(func=cmd_list)

    show_parser = sub.add_parser("show", help="Show one Pattern Card.")
    show_parser.add_argument("pattern_key")
    show_parser.add_argument("--evidence-limit", type=int, default=10)
    show_parser.set_defaults(func=cmd_show)

    task_parser = sub.add_parser("task", help="Show one Task Card for a pattern.")
    task_parser.add_argument("pattern_key")
    task_parser.add_argument("--type", default="engineering_plan", choices=sorted(TASK_TYPES))
    task_parser.add_argument("--evidence-limit", type=int, default=10)
    task_parser.set_defaults(func=cmd_task)

    brief_parser = sub.add_parser("brief", help="Render a project-ready pattern brief.")
    brief_parser.add_argument("pattern_key")
    brief_parser.add_argument("--type", default="engineering_plan", choices=sorted(TASK_TYPES))
    brief_parser.add_argument("--evidence-limit", type=int, default=10)
    brief_parser.add_argument("--write", help="Write the brief to a path, for example .shipgrade/pattern-brief.md")
    brief_parser.set_defaults(func=cmd_brief)

    validate_parser = sub.add_parser("validate", help="Validate distilled assets.")
    validate_parser.set_defaults(func=cmd_validate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
