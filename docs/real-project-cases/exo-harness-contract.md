# Real Project Gauntlet Case: exo harness contract and maintainer-facing proof

## Real Project Evidence

- project ref: `local-project:exo`
- expected handoff files found: `AGENTS.md`, `README.md`, `docs/coding-agent-harnesses.md`, `package.json`
- docs file signal count: `5`
- test/smoke file signal count: `14`
- validation script signals: `lint`, `lint:fix`, `test`, `typecheck`
- validation file signals: `tests/agent-harness-events.test.ts`

## ShipGrade Task

把 harness/CLI 改动拆成 maintainer 能审的最小 slice,保留运行命令、边界和后续协作入口。

## Expected Agent Output Contract

The skill must produce a delivery plan or final handoff that includes:

- harness command
- maintainer proof
- compatibility boundary
- handoff

It must also include:

- 交付 / result path or artifact path.
- 验证 / evidence command, screenshot, log, test, smoke, or probe.
- 风险边界 / known limits and rollback path.
- 来源 / source project path and license boundary.
- 禁止事项 / do not copy secret, token, cookie, session, auth database, private key, or private source body into a public package.

## Acceptance Checklist

- [ ] The agent reads the project-local AGENTS/CLAUDE/handoff entry before changing files.
- [ ] The agent chooses the smallest verifiable slice.
- [ ] The agent names the validation command or concrete manual smoke surface.
- [ ] The agent separates fact, inference, assumption, and remaining risk.
- [ ] The final handoff can be checked by `tools/shipgrade_doctor.py`.

## Public Package Boundary

This gauntlet stores safe structural evidence only. It does not export private source code, secrets, config values, database content, browser state, user text, or credentials.
