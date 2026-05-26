# Real Project Gauntlet Case: SkillsCN release quality and provenance

## Real Project Evidence

- project ref: `local-project:skills-cn-distill`
- expected handoff files found: `AGENTS.md`, `README.md`, `scripts/validate_flagship_skill.py`, `dist/ship-grade-engineering-cn-v0.1/SKILL.md`
- docs file signal count: `1`
- test/smoke file signal count: `25`
- validation script signals: No validation script name detected; use repo-specific docs/tests.
- validation file signals: `scripts/validate_flagship_skill.py`, `scripts/validate_outputs.py`, `scripts/validate_project_kickoff_skill.py`, `scripts/validate_sft_dataset.py`

## ShipGrade Task

发布中文工程 skill 包时,同时证明来源、许可证、训练、runtime audit、doctor、eval 和多机器同步。

## Expected Agent Output Contract

The skill must produce a delivery plan or final handoff that includes:

- source attribution
- license boundary
- training probes
- release hash

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
