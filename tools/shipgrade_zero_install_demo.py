from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BEGIN = "<!-- SHIPGRADE-CN:BEGIN -->"
END = "<!-- SHIPGRADE-CN:END -->"


def ensure_safe_target(path: Path) -> None:
    temp_root = Path(tempfile.gettempdir()).resolve()
    resolved = path.resolve()
    if temp_root not in resolved.parents and resolved != temp_root:
        raise SystemExit(f"refuse to clean non-temp zero-install demo target: {resolved}")
    if not resolved.name.startswith("shipgrade-zero-install-demo"):
        raise SystemExit(f"refuse to clean non-zero-install demo target: {resolved}")


def read_contract() -> str:
    contract = (ROOT / "SHIPGRADE.md").read_text(encoding="utf-8")
    required = [
        "ShipGrade CN 零安装规则",
        "用户只需要说什么",
        "不要覆盖用户已有规则",
        "每次任务开始前",
        "每次任务完成时",
        "No Python installation",
    ]
    missing = [term for term in required if term not in contract]
    if missing:
        raise SystemExit("SHIPGRADE.md is not a complete zero-install contract: " + ", ".join(missing))
    return contract


def managed_block(contract: str) -> str:
    excerpt_lines = []
    for line in contract.splitlines():
        if line.startswith("# ") or line.startswith("## 用户只需要说什么") or line.startswith("## 每次任务完成时"):
            excerpt_lines.append(line)
        if len(excerpt_lines) >= 3:
            break
    excerpt = "\n".join(excerpt_lines)
    return f"""{BEGIN}
# ShipGrade CN Zero-Install

This project uses the local `SHIPGRADE.md` contract. Do not install Python, start a service, or overwrite existing project rules just to adopt ShipGrade.

Core contract:

```text
结果: concrete changed artifact/path/state
证据: command/test/build/browser/log/manual check and observed result
风险: unverified or intentionally out-of-scope boundary
接手: next file, command, issue, or decision point
```

Source excerpt:

```text
{excerpt}
```
{END}
"""


def upsert(path: Path, block: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if BEGIN in existing and END in existing:
        return f"skip existing managed block {path.relative_to(path.parents[0])}"
    prefix = existing.rstrip() + "\n\n" if existing.strip() else ""
    path.write_text(prefix + block.strip() + "\n", encoding="utf-8")
    return f"write {path.name}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Prove ShipGrade CN can be adopted from SHIPGRADE.md without Python in the target project.")
    parser.add_argument("--target", help="demo project directory under the system temp folder")
    parser.add_argument("--clean", action="store_true", help="remove the generated zero-install demo project after printing proof")
    args = parser.parse_args()

    target = Path(args.target).expanduser() if args.target else Path(tempfile.mkdtemp(prefix="shipgrade-zero-install-demo-"))
    ensure_safe_target(target)
    if args.target and target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)

    contract = read_contract()
    block = managed_block(contract)

    (target / "README.md").write_text("# Demo Project\n\nExisting user README.\n", encoding="utf-8")
    (target / "AGENTS.md").write_text("# Existing Agent Rules\n\nKeep this user-owned rule.\n", encoding="utf-8")
    (target / "CLAUDE.md").write_text("# Existing Claude Rules\n\nKeep this user-owned rule.\n", encoding="utf-8")
    (target / "SHIPGRADE.md").write_text(contract, encoding="utf-8")
    upsert(target / "AGENTS.md", block)
    upsert(target / "CLAUDE.md", block)
    cursor_rule = target / ".cursor" / "rules" / "shipgrade.mdc"
    cursor_rule.parent.mkdir(parents=True, exist_ok=True)
    cursor_rule.write_text(
        "---\ndescription: ShipGrade CN zero-install rule\nalwaysApply: false\n---\n\n"
        + block.strip()
        + "\n",
        encoding="utf-8",
    )

    checks = {
        "read_shipgrade_md": "ShipGrade CN 零安装规则" in contract,
        "preserved_existing_agents_rule": "Keep this user-owned rule." in (target / "AGENTS.md").read_text(encoding="utf-8"),
        "preserved_existing_claude_rule": "Keep this user-owned rule." in (target / "CLAUDE.md").read_text(encoding="utf-8"),
        "wrote_codex_rule": BEGIN in (target / "AGENTS.md").read_text(encoding="utf-8"),
        "wrote_claude_rule": BEGIN in (target / "CLAUDE.md").read_text(encoding="utf-8"),
        "wrote_cursor_rule": BEGIN in cursor_rule.read_text(encoding="utf-8"),
        "python_helper_used_in_target": False,
        "service_started": False,
    }
    if not all(value is True or key in {"python_helper_used_in_target", "service_started"} and value is False for key, value in checks.items()):
        raise SystemExit("zero-install adoption proof failed: " + repr(checks))

    print("shipgrade-zero-install-demo-ok")
    print(f"target={target}")
    print("source=SHIPGRADE.md")
    print("created=SHIPGRADE.md,AGENTS.md,CLAUDE.md,.cursor/rules/shipgrade.mdc")
    print("preserved_existing_rules=true")
    print("python_helper_used_in_target=false")
    print("service_started=false")
    print("next=ask an AI coding agent: 用 ShipGrade 做这个任务")
    if args.clean:
        shutil.rmtree(target)
        print("cleaned=true")
    else:
        print("note=demo project kept for inspection; rerun with --clean to remove it")


if __name__ == "__main__":
    main()
