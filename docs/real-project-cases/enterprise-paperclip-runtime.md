# Real Project Gauntlet Case: Enterprise AI Hub Paperclip runtime closure

## Real Project Evidence

- project ref: `local-project:enterprise`
- expected handoff files found: `AGENTS.md`, `docs/CODEX_HANDOFF.md`, `docs/CODEX_START_HERE.md`, `package.json`
- docs file signal count: `1820`
- test/smoke file signal count: `1378`
- validation script signals: `build`, `lint`, `test`, `typecheck`
- validation file signals: `apps/portal-web/src/api/actionsRoute.test.ts`, `apps/portal-web/src/api/agentsRoute.test.ts`, `apps/portal-web/src/api/localToolRegistrationRoute.test.ts`, `apps/portal-web/src/api/localToolsRoute.test.ts`, `apps/portal-web/src/api/paperclipRuntime.test.ts`, `apps/portal-web/src/api/policyPermissionsVerificationApi.test.ts`, `apps/portal-web/src/api/readRoutes.test.ts`, `apps/portal-web/src/api/securityAuditTokenLedgerVerificationApi.test.ts`

## ShipGrade Task

验证 Paperclip/Core/local-tools 读模型是否真实进入前端,并给出可复烟的 release gate。

## Expected Agent Output Contract

The skill must produce a delivery plan or final handoff that includes:

- route smoke
- field coverage
- read-only boundary
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
