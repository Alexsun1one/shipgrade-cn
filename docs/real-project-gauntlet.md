# Real Project Gauntlet

Purpose: verify that ShipGrade CN can be judged against real local projects, not only synthetic README examples.

This gauntlet records safe structural evidence and expected output contracts for five existing projects. It intentionally does not copy private source code or sensitive configuration into the public package.

## Result

- cases: `5`
- passed structural readiness: `5/5`
- 交付: `outputs/real_project_gauntlet/real_project_gauntlet.md` plus one case markdown per project.
- 验证证据: generated case files are checked with `tools/shipgrade_doctor.py`.

## Cases

| case | project exists | found files | docs | tests/smoke | validation signals | status |
| --- | --- | --- | --- | --- | --- | --- |
| `enterprise-paperclip-runtime` | True | 4 | 1820 | 1378 | `build`, `lint`, `test`, `typecheck`, `apps/portal-web/src/api/actionsRoute.test.ts`, `apps/portal-web/src/api/agentsRoute.test.ts` | pass |
| `hardwrite-rewrite-safety` | True | 3 | 7 | 195 | `build`, `lint`, `test`, `typecheck`, `packages/cli/src/__tests__/analytics.test.ts`, `packages/cli/src/__tests__/cli-integration.test.ts` | pass |
| `silicoville-ledger-migration` | True | 5 | 307 | 895 | `build`, `build:claw`, `lint`, `tauri:android:build`, `scripts/build-admin-menu-i18n.mjs`, `scripts/build-and-sign-apk.sh` | pass |
| `exo-harness-contract` | True | 4 | 5 | 14 | `lint`, `lint:fix`, `test`, `typecheck`, `tests/agent-harness-events.test.ts` | pass |
| `skillscn-release-quality` | True | 4 | 1 | 25 | `scripts/validate_flagship_skill.py`, `scripts/validate_outputs.py` | pass |

## What This Proves

- The skill is tested against actual project shapes: SaaS runtime smoke, editorial pipeline safety, game/economy migration, CLI harness work, and the SkillsCN release itself.
- Each case has real handoff/rules/docs/test signals an agent must read before acting.
- The package now has a repeatable way to add public-safe case evidence without leaking private repo content.

## What It Does Not Prove

- It does not prove public adoption or GitHub stars.
- It does not prove every upstream repo is safe to run.
- It does not replace task-specific tests inside each private repo.

## Source / License Boundary

- 来源: local project paths and safe file-name/count signals only.
- 许可证 / license: this public package does not redistribute private project source bodies.
- 风险边界: case evidence is structural readiness, not proof that each future task is complete.

## Forbidden

- 禁止 copying secret, token, cookie, session, auth database, private key, browser profile, private config, database content, or private source body into a public case.

## Next Evidence Step

For each case, run one real task with ShipGrade CN, save a redacted transcript or screenshot, then rerun `tools/shipgrade_doctor.py` on the final handoff.
