# Real Project Gauntlet Case: HardWrite rewrite safety and editorial gate

## Real Project Evidence

- project ref: `local-project:AutoW/Autow-source`
- expected handoff files found: `CLAUDE.md`, `README.md`, `package.json`
- docs file signal count: `7`
- test/smoke file signal count: `195`
- validation script signals: `build`, `lint`, `test`, `typecheck`
- validation file signals: `packages/cli/src/__tests__/analytics.test.ts`, `packages/cli/src/__tests__/cli-integration.test.ts`, `packages/cli/src/__tests__/interact-command.test.ts`, `packages/cli/src/__tests__/localization.test.ts`, `packages/cli/src/__tests__/progress-text.test.ts`, `packages/cli/src/__tests__/publish-package.test.ts`, `packages/cli/src/__tests__/revision-command.test.ts`, `packages/cli/src/__tests__/studio-runtime.test.ts`

## ShipGrade Task

定位章节改写质量门失败时,先保护已有正文和 truth files,再给出最小可验证修复。

## Expected Agent Output Contract

The skill must produce a delivery plan or final handoff that includes:

- truth-file check
- non-destructive rewrite
- chapter evidence
- rollback

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
