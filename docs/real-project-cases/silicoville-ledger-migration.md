# Real Project Gauntlet Case: SilicoVille ledger and migration discipline

## Real Project Evidence

- project ref: `local-project:cursor_0311`
- expected handoff files found: `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/ARCHITECTURE.md`, `docs/DB_SCHEMA.md`
- docs file signal count: `307`
- test/smoke file signal count: `895`
- validation script signals: `build`, `build:claw`, `lint`, `tauri:android:build`, `test`, `test:watch`
- validation file signals: `scripts/build-admin-menu-i18n.mjs`, `scripts/build-and-sign-apk.sh`, `scripts/build-android.sh`, `scripts/test-lianlu-sign.mjs`, `videos/silicoville-intro/.tts-venv/lib/python3.14/site-packages/dateutil/zoneinfo/rebuild.py`, `videos/silicoville-intro/.tts-venv/lib/python3.14/site-packages/flatbuffers/builder.py`, `videos/silicoville-intro/.tts-venv/lib/python3.14/site-packages/jsonschema/benchmarks/json_schema_test_suite.py`, `videos/silicoville-intro/.tts-venv/lib/python3.14/site-packages/jsonschema/tests/__init__.py`

## ShipGrade Task

处理经济账本或 SQL 迁移时,把 live DB 证据、迁移脚本、回滚和产品文档对齐。

## Expected Agent Output Contract

The skill must produce a delivery plan or final handoff that includes:

- migration proof
- ledger invariant
- rollback
- architecture docs

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
