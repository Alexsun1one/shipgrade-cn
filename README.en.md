# ShipGrade CN

> An agent skill for Codex, Claude Code, and Cursor that turns vague requests into verified engineering delivery for Chinese-speaking teams.

Chinese version: [README.md](README.md)

[![Local verify](https://img.shields.io/badge/local%20verify-shipgrade__verify.py-2ea44f)](#release-preflight)
[![Agents](https://img.shields.io/badge/agents-Codex%20%7C%20Claude%20Code%20%7C%20Cursor-111827)](START_HERE.md)
[![Code license](https://img.shields.io/badge/code-MIT-blue)](LICENSE.md)
[![Docs license](https://img.shields.io/badge/docs-CC%20BY%204.0-blue)](NOTICE.md)

## What It Does

ShipGrade CN installs a verifiable delivery workbench into any repository. Codex, Claude Code, and Cursor then work from the same goal, boundary, validation, and handoff rules.

| Feature | What you get |
| --- | --- |
| Project workbench initialization | `.shipgrade/task-brief.md`, `quality-gate.md`, and `handoff.md`. |
| Multi-agent rule wiring | `AGENTS.md`, `CLAUDE.md`, and Cursor rules generated from the same contract. |
| Vague request compression | Goal, non-goal, evidence, acceptance criteria, risks, and the first implementation slice. |
| Fake-completion rejection | `shipgrade_doctor.py` requires artifact paths and command or browser evidence. |
| Handoff after delivery | Result, validation proof, remaining risks, security boundary, and next action. |
| Release preflight | `github_publish_preflight.py`, `shipgrade_verify.py`, GitHub Actions, and package scripts. |

## Problem It Solves

ShipGrade CN is not a prompt pack. It helps a user move from "please fix this" to a concrete delivery contract:

1. goal
2. non-goal
3. current evidence
4. acceptance criteria
5. validation proof
6. handoff for the next agent or future maintainer

The project is written for Chinese-speaking workflows, but this file explains the package in English for reviewers, contributors, and global users.

## Quick Demo

Requirements: Python 3.10+. No API key and no network access are required.

```bash
python3 tools/shipgrade_demo.py
```

The demo proves three things:

- `shipgrade_init.py` creates a project workbench and wires agent rules.
- `shipgrade_doctor.py` rejects a fake completion that only says the work looks done.
- The same doctor accepts a handoff with concrete artifact paths, command evidence, source and license boundaries, security boundaries, and a next-step entry.

Expected signal:

```text
shipgrade-demo-ok
fake_rejection=... ship-grade-fail vague_or_unverified_language ...
accepted=... ship-grade-ok
```

See `docs/DEMO_PROOF.md` for the captured proof.

## Install Into A Project

```bash
python3 tools/shipgrade_init.py /path/to/your-project
cd /path/to/your-project
sed -n '1,160p' .shipgrade/task-brief.md
sed -n '1,160p' AGENTS.md
```

Then use it like this:

1. Fill `.shipgrade/task-brief.md`.
2. Ask Codex, Claude Code, or Cursor to read the project rules.
3. Make the smallest verified change.
4. Write the result and evidence into `.shipgrade/handoff.md`.
5. Run the doctor.

```bash
python3 tools/shipgrade_doctor.py .shipgrade/handoff.md
```

Install as a Codex skill:

```bash
python3 tools/install_skill.py --force
```

## Generated Structure

```text
.shipgrade/
  task-brief.md
  quality-gate.md
  handoff.md
  AGENTS.snippet.md
AGENTS.md
CLAUDE.md
CLAUDE.shipgrade.md
.cursor/rules/shipgrade.mdc
```

## Why It Is Credible: Repository Engineering Distillation Pipeline

The repository-engineering layer behind ShipGrade CN does not dump repositories into a model and hope it learns architecture. It treats repositories as engineering evidence and turns them into structured assets first:

```text
Repository -> Engineering Knowledge -> Task Data -> Eval -> RAG / SFT / DPO
```

The model should not memorize source code. It should learn engineering judgment:

- why a repository is layered the way it is
- where module boundaries live
- where a new feature should enter
- where tests should be added
- which designs are worth reusing
- which failure modes should be avoided

The full method is documented in `docs/repository-engineering-distillation-pipeline.md`.

## Distilled Asset Types

ShipGrade CN turns repository evidence into four reviewable asset types:

| Asset | Purpose |
| --- | --- |
| Repo Card | Repository profile: domain, language, architecture, entrypoints, directories, commands, strengths, and reuse scenarios. |
| Pattern Card | Engineering pattern: scenario, problem, solution, code evidence, benefits, tradeoffs, and migration judgment. |
| Task Card | Task data for planning, review, repair, migration, and anti-pattern recognition. |
| Eval | Evaluation cases with inputs, expected points, deductions, commands, and judge rubrics. |

Current generated assets: 11 Repo Cards / 15 Pattern Cards / 90 Task Cards / 90 Eval Cases. See `docs/repo-engineering-distillation-assets.md` and `docs/evidence/repo_engineering_distillation/`.

## What Is Inside

| Path | Purpose |
| --- | --- |
| `SKILL.md` | The actual skill instructions consumed by agents. |
| `START_HERE.md` | The first navigation file for new users. |
| `tools/shipgrade_init.py` | Generates the project workbench and agent-rule wiring. |
| `tools/shipgrade_doctor.py` | Checks whether a handoff contains result, validation, source, risk, security, and next-step evidence. |
| `tools/shipgrade_demo.py` | Runs the quick proof path. |
| `tools/github_publish_preflight.py` | Checks the repository before release. |
| `docs/repository-engineering-distillation-pipeline.md` | The Repo Card / Pattern Card / Task Card / Eval methodology. |
| `docs/repo-engineering-distillation-assets.md` | Generated Repo/Pattern/Task/Eval assets from real repository evidence. |
| `docs/EVIDENCE_INDEX.md` | Maps public claims to evidence files. |
| `docs/source-depth-dossier.md` | Explains how sources were studied beyond README files. |
| `docs/deep-code-case-studies.md` | Code-level case studies from high-signal repositories. |
| `docs/source-promotion-sandbox-cases.md` | Runtime sandbox evidence for promoted source candidates. |

## Workflow

ShipGrade CN gives agents a repeatable loop:

1. Turn a vague request into a brief.
2. Wire the same rules into Codex, Claude Code, and Cursor.
3. Ship the smallest aligned change.
4. Validate with tests, builds, browser smoke checks, logs, or explicit manual checks.
5. Write a handoff with result, proof, boundaries, residual risk, and next steps.

## Evidence Snapshot

- Sources: 103
- Extracted artifacts: 128
- Repository structure scans: 88
- High-signal source radar: 87 candidates / 64 new / 65 green-license / 8 off-scope search-noise
- Source promotion queue: 87 rows / 12 next deep-sandbox / 18 license-review targets
- Source promotion batch: 4 selected / 4 audited / 2 runtime candidates / 2 static smoke passed (`affaan-m/ECC`, `addyosmani/agent-skills`, `browser-use/browser-use`, `VoltAgent/awesome-agent-skills`)
- Source promotion sandbox cases: 3/3 cases / 13/13 required steps / 264 configured upstream tests (`affaan-m/ECC`, `browser-use/browser-use`, `addyosmani/agent-skills`)
- Deep code case studies: 11 repos / 17649 files / 5381 test paths / 786 eval paths
- Repository engineering distillation assets: 11 Repo Cards / 15 Pattern Cards / 90 Task Cards / 90 Eval Cases
- Evaluation tasks: 12
- Runtime smoke checks: 33 passed checks / 33 checks on 7 cloned repos
- Sandbox runtime matrix: 3/3 cases and 12/12 steps across `Yeachan-Heo/oh-my-claudecode`, `SuperClaude-Org/SuperClaude_Framework`, `github/spec-kit`, with 590 configured upstream tests discovered
- Real project gauntlet: 5/5
- Transcript evidence: 2/2

## Why It Is Not Just Prompts

| Question | Answer |
| --- | --- |
| Can a beginner use it? | Yes. Run `shipgrade_init.py`, fill the brief, then follow the quality gate. |
| Does the agent actually see the rules? | Yes. The initializer wires `AGENTS.md`, `CLAUDE.md`, and Cursor rules. |
| Can it reject fake completion? | Yes. The doctor requires artifact paths and validation evidence. |
| Is the research README-only? | No. It generates 11 Repo Cards / 15 Pattern Cards / 90 Task Cards / 90 Eval Cases. Structure scans cover 88 repositories, and deep code case studies cover 11 repositories. |
| Is there runtime evidence? | Yes. Runtime and sandbox evidence live under `docs/`. |
| Can the repo be released independently? | Yes. It includes local preflight, GitHub Actions, release packaging, issue templates, and license files. |

## Source Influences

ShipGrade CN borrows engineering structure, not celebrity branding:

- Karpathy-style minimal reproducible training repos
- Google engineering practices and style guides
- GitHub Spec Kit, OpenSpec, and Agent OS
- Matt Pocock-style skill organization
- OpenAI and Anthropic cookbooks
- promptfoo and DeepEval
- Cline, Gemini CLI, opencode, Continue, and browser-use
- Microsoft playbooks, Rust RFCs, Kubernetes KEPs, and OpenTelemetry specs

## Document Map

- Start here: `START_HERE.md`
- Evidence index: `docs/EVIDENCE_INDEX.md`
- Distillation pipeline: `docs/repository-engineering-distillation-pipeline.md`
- Distillation assets: `docs/repo-engineering-distillation-assets.md`
- Source attribution: `docs/source-attribution.md`
- Deep source study: `docs/source-depth-dossier.md`
- Code case studies: `docs/deep-code-case-studies.md`
- Runtime evidence: `docs/runtime-smoke-evidence.md`, `docs/sandbox-runtime-cases.md`
- Source promotion: `docs/high-signal-source-radar.md`, `docs/source-promotion-queue.md`, `docs/source-promotion-batch.md`
- Release preflight: `docs/GITHUB_PUBLISH_PREFLIGHT.md`
- Demo proof: `docs/DEMO_PROOF.md`
- Roadmap: `docs/ROADMAP.md`

## Release Preflight

```bash
python3 tools/github_publish_preflight.py --write-docs --run-verify
python3 tools/shipgrade_verify.py
python3 scripts/create-public-stage.py /tmp/shipgrade-cn-public
bash scripts/verify.sh
bash scripts/package.sh
```

## Security Boundary

ShipGrade CN must not ingest, train on, or publish:

- secrets, tokens, API keys, or private keys
- cookies, browser profiles, auth databases, or session databases
- private repository bodies
- leaked source, leaked prompts, or archived system prompts
- unclear-license body text

## License

- Code in `tools/`: MIT
- Docs, templates, examples, evals, and skill content: CC BY 4.0
- See `LICENSE.md`, `NOTICE.md`, and `docs/source-attribution.md`
