# Quality Report

## Result

Ship-Grade Engineering CN v0.1 has a GitHub-ready artifact: README, SKILL, agent rules, templates, examples, evals, source attribution, manifest, and doctor tool.

## Evidence

- required files present: yes
- templates: `6`
- examples: `3`
- demos: `3`
- release files: `12`
- standalone release check: `yes`
- GitHub Actions workflow: `yes`
- evals: `12`
- source refs: `103`
- source snapshot: `103` sources / `128` artifacts / `12` overlap themes
- repo structure scan: `88` repos
- high-signal source radar: `87` candidates / `64` new / `65` green-license candidates / `8` off-scope search noise
- source promotion queue: `87` rows / `12` next deep-sandbox targets / `18` license-review targets
- source promotion batch: `4` selected / `4` audited / `2` runtime candidates / `2` static smoke passed
- source promotion sandbox cases: `2/2` cases / `9/9` required steps / `225` configured upstream tests discovered
- deep code case studies: `11` repos / `17649` files / `5381` test paths / `786` eval paths
- audience tiers: 中文小白 / 进阶用户 / 专业工程师
- influence profiles: `10`
- primary adapter probe: `3/3` semantic (`2/3` raw literal checker)
- primary adapter review: `accept_as_primary_execution_adapter`
- real project gauntlet: `5/5` structural cases
- transcript evidence: `2/2` executed cases
- sandbox runtime matrix: `3/3` cases, `12/12` steps, `590` configured upstream tests discovered

## Judgment

This is a GitHub-ready v0.1 flagship skill: focused, installable, evidence-backed, and aligned with Chinese engineering delivery.

It is not yet proven to be world-class in the market. That requires public usage, issues, examples, and repeated real-task evals.

## Why It Is Strong

- It compresses repeated signals from high-trust engineering sources instead of copying long passages.
- It goes beyond README: repo tree structure is analyzed for source roots, tests, CI, governance files, design docs, examples, and eval/benchmark surfaces.
- It goes beyond tree counts: `docs/deep-code-case-studies.md` extracts package scripts, pyproject sections, workflow command hits, test anatomy, agent surfaces, doc taxonomy, and code-symbol counts from public runtime clones.
- It includes a project initializer through `tools/shipgrade_init.py`, so the package creates a real workspace instead of only describing one.
- It includes a runnable demo through `demo/demo-output.md` and `tools/shipgrade_doctor.py`.
- It includes standalone open-source release checks through `tools/shipgrade_release_check.py` and `.github/workflows/validate.yml`.
- It includes `LICENSE.md`, `NOTICE.md`, `CONTRIBUTING.md`, `SECURITY.md`, issue templates, and a PR template.
- It is checked against five real project shapes through `docs/real-project-gauntlet.md`, while keeping private project bodies out of the public package.
- It includes real command transcripts through `docs/transcript-evidence.md`, including an Enterprise Paperclip API smoke and the SkillsCN release proof.
- It includes a true sandbox runtime matrix through `docs/sandbox-runtime-cases.md`: no secrets, no auth state, Node `npm ci --ignore-scripts`, TypeScript `tsc --noEmit`, selected upstream Vitest files, Python `uv` temp venv, editable install where safe, dependency-only install where package assets are incomplete, and selected pytest unit tests.
- It names the influence map: Karpathy, Google engineering practices, spec-driven systems, real engineer skills, AI cookbooks, eval frameworks, and modern coding agents.
- It explains why those sources were modified for Chinese users: lower entry friction for 小白, stronger habits for 进阶用户, auditable provenance/evals for 专业工程师.
- It keeps source/license boundaries visible, including metadata-only sources.

## Known Boundary / 已知边界

- 这是交付级工程 skill,不是最终法律/安全审查结论。
- 来源为公开仓库引用和许可证策略,不复制私有内容。
- 14B adapter 只作为执行层证据,不是最终老师。
- Transcript evidence 是脱敏本地执行证据,不是市场采用证明。
- Sandbox runtime matrix 只跑低副作用代表样本,不是声称已完整验证所有上游测试文件。

## Forbidden

- 不复制 secret/token/cookie/session/auth/private key。
- 不吸收泄漏源码或系统提示词归档。
- 不把 stars 当许可证或质量证明。

## Next Quality Move

- Run it on 5 real projects.
- Add more redacted transcripts and screenshots from real user-facing tasks.
- Add a tiny `ship-grade doctor` CLI or checker.
- Translate only the README summary, not the core Chinese workflow.
