# Zero Install

ShipGrade CN should be useful before the user installs anything.

## Short Answer

- **Default:** one Markdown rule file: `SHIPGRADE.md`.
- **Optional:** Python helper scripts for deterministic initialization, doctor checks, demos, and release preflight.
- **Not needed for v1:** a background service.

The product should feel like this:

```text
User: Use ShipGrade CN on this project.
Agent: Reads SHIPGRADE.md, writes the right local rule file, then works through goal/non-goal/evidence/acceptance/risk/handoff.
```

## Why MD First

Markdown rules are the lowest-friction surface:

- readable by humans,
- readable by Codex, Claude Code, Cursor, and generic AI coding agents,
- easy to paste into locked-down company machines,
- no Python version mismatch,
- no package manager,
- no service lifecycle,
- no network required after the file is present.

This is the right beginner path.

## Why Keep Python

Python still matters, but only as an enhancer:

| Need | Python helper |
| --- | --- |
| Create `.shipgrade/` templates and agent rules automatically | `tools/shipgrade_init.py` |
| Reject vague "done" handoffs by script | `tools/shipgrade_doctor.py` |
| Show a reproducible demo | `tools/shipgrade_demo.py` |
| Use distilled Pattern/Task/Eval assets | `tools/shipgrade_patterns.py` |
| Check a public repo before release | `tools/github_publish_preflight.py` |

Do not make Python a prerequisite for understanding or using the skill.

## Why Not A Service Yet

A service adds accounts, ports, uptime, security, upgrades, and support burden. ShipGrade CN's v1 value is a rule contract and local delivery loop, not a hosted control plane.

A service becomes worth it only if the product later needs:

- team-shared rule catalogs,
- cloud eval dashboards,
- organization-wide policy sync,
- web UI for non-technical users,
- remote evidence collection across many repos,
- marketplace-style one-click install.

Until then, service-first would raise the adoption barrier.

## Recommended Product Shape

```text
Level 0: SHIPGRADE.md
  zero install, one file, agent-readable contract

Level 1: rule-file wiring
  AGENTS.md / CLAUDE.md / .cursor/rules/shipgrade.mdc

Level 2: optional Python helpers
  init / doctor / demo / patterns / preflight

Level 3: future service
  only for team sync, dashboards, marketplace, or hosted evals
```

## User-Facing One-Liner

```text
把 ShipGrade CN 接入这个项目,走零安装模式: 读取 SHIPGRADE.md,写入适合当前工具的规则文件,然后按它的工程交付闭环工作。
```

## Boundary

Zero install does not mean zero discipline. It still requires:

- concrete result paths,
- validation evidence,
- source/license boundaries,
- secret and private-data exclusion,
- a handoff another agent can continue from.
