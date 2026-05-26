<div align="center">

# ShipGrade CN

**A Chinese-first engineering delivery workbench for Codex, Claude Code, and Cursor.**

[中文](README.md) · [Zero Install](#zero-install-one-md-file) · [External Trial](docs/EXTERNAL_TRIAL_PROOF.md) · [Multi-Repo Eval](docs/MULTI_REPO_EVAL_PROOF.md) · [Real Case](docs/REAL_ISSUE_CASE_PROOF.md) · [Task Suite](docs/REAL_TASK_SUITE_PROOF.md) · [Eval Corpus](docs/EVAL_CORPUS_PROOF.md) · [Holdout Replay](docs/HOLDOUT_REPLAY_PROOF.md) · [Model Replay](docs/MODEL_REPLAY_PROOF.md) · [Judge Panel](docs/JUDGE_PANEL_PROOF.md) · [Review Packet](docs/REVIEW_PACKET_PROOF.md) · [Quick Demo](#quick-demo) · [Install](#two-install-paths) · [Evidence Index](docs/EVIDENCE_INDEX.md)

[![Local verify](https://img.shields.io/badge/local%20verify-shipgrade__verify.py-2ea44f)](#release-preflight)
[![Agents](https://img.shields.io/badge/agents-Codex%20%7C%20Claude%20Code%20%7C%20Cursor-111827)](START_HERE.md)
[![Code license](https://img.shields.io/badge/code-MIT-blue)](LICENSE.md)
[![Docs license](https://img.shields.io/badge/docs-CC%20BY%204.0-blue)](NOTICE.md)

</div>

![ShipGrade CN function map](assets/shipgrade-hero-cn.png)

## What It Does

ShipGrade CN is a Chinese-first engineering delivery skill for AI coding agents. It is not a prompt pack. It installs repo-local files, quality gates, and verification scripts so Codex, Claude Code, and Cursor can work from the same contract.

Generated workbench:

```text
.shipgrade/task-brief.md   # goal, non-goal, evidence, acceptance
.shipgrade/quality-gate.md # delivery constraints before completion
.shipgrade/handoff.md      # result, proof, risk, next step
AGENTS.md / CLAUDE.md / .cursor/rules/shipgrade.mdc
```

| Problem | What ShipGrade CN adds |
| --- | --- |
| Users should not install anything first | `SHIPGRADE.md` gives a one-file, zero-install rule surface for Codex, Claude Code, Cursor, or any AI coding agent. |
| The request is just "please fix this" | `.shipgrade/task-brief.md`: goal, non-goal, evidence, acceptance criteria, risk boundary, and first slice. |
| Different agents read different rules | `AGENTS.md`, `CLAUDE.md`, and Cursor rules are generated from the same quality gate. |
| The agent says "done" without proof | The MD contract requires proof first; optional `shipgrade_doctor.py` rejects handoffs without artifact paths and command or browser evidence. |
| You want to reuse strong engineering patterns | `shipgrade_patterns.py` turns real-repository Pattern/Task/Eval assets into a task brief. |
| The next agent cannot continue | `.shipgrade/handoff.md` records result, validation proof, residual risk, security boundary, and next action. |
| The repo needs to be public-ready | `github_publish_preflight.py`, `shipgrade_verify.py`, GitHub Actions, and evidence docs check the launch surface. |

## Engineering Constraints

ShipGrade CN gives agents delivery constraints, not tone preferences:

| Constraint | Requirement |
| --- | --- |
| Goal | Define what this task must deliver before implementation starts. |
| Non-goal | Name the modules, data, configs, and refactors that are out of scope. |
| Evidence | Bind completion to file paths, commands, tests, browser checks, logs, or explicit manual checks. |
| Safety | Do not copy secrets, tokens, cookies, sessions, private keys, browser profiles, or private source bodies. |
| Source | Preserve source, license, applicability, and non-applicability when borrowing from public repos. |
| Handoff | Leave enough result, proof, risk, and next-step context for another agent to continue. |

## Why It Is Advanced

| Prompt-pack habit | ShipGrade CN behavior |
| --- | --- |
| Longer instructions inside one chat | A one-file MD contract first; repo-local workbench files only when useful. |
| Trust the model to self-police | The MD contract requires proof; optional `shipgrade_doctor.py` rejects unsupported completion claims. |
| Works only in one agent session | Shared rules for Codex, Claude Code, and Cursor. |
| Hard for beginners to apply | Chinese task briefs turn scope, risk, and acceptance into fillable structure. |
| Hard for senior engineers to trust | Public claims map to evidence files, commands, and validation scripts. |
| Copy surface patterns from famous repos | Convert strong practices into Pattern Briefs, Task Cards, and Evals. |

## What It Borrows From

| Source family | Borrowed idea | ShipGrade CN form |
| --- | --- | --- |
| GitHub Spec Kit / OpenSpec / Agent OS | spec-first, planning, tasks, acceptance gates | task brief + quality gate + pattern brief |
| Addy Osmani Agent Skills / Matt Pocock skills | lifecycle skills, anti-rationalization, command surfaces | cross-agent skill structure |
| Google Engineering Practices | review discipline, maintainability, testing | non-goals, evidence, validation, review boundary |
| Karpathy-style training repos | minimal reproducibility, probes, metrics | demo, verify, release check |
| OpenAI / Anthropic cookbooks | recipes, failure modes, eval thinking | Task Cards, Evals, doctor checks |
| promptfoo / DeepEval | measurable model behavior | script-checkable handoff quality |
| Rust RFC / Kubernetes KEP / OpenTelemetry spec | design docs, compatibility, stage gates | handoff, ADR habits, architecture constraints |

## Problem It Solves

ShipGrade CN is not a prompt pack. It helps Chinese-speaking teams turn everyday requests into a concrete engineering loop:

```text
vague request -> task brief -> smallest change -> validation proof -> handoff -> next agent
```

The delivery contract has six parts:

1. goal
2. non-goal
3. current evidence
4. acceptance criteria
5. validation proof
6. handoff for the next agent or future maintainer

## Zero Install: One MD File

**No Python, no background service, no API key.** The lowest-friction version is the Chinese-first [SHIPGRADE.md](SHIPGRADE.md). Put it in a project or ask Codex, Claude Code, or Cursor to read it.

You can tell an AI coding tool:

```text
Read https://github.com/Alexsun1one/shipgrade-cn/blob/main/SHIPGRADE.md,
wire ShipGrade CN into this project, and use the zero-install path.
Only write the rule file that fits this tool. Do not install Python or start a service.
```

Recommended landing files:

| Tool | File |
| --- | --- |
| Codex | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursor/rules/shipgrade.mdc` |
| Generic AI coding agent | project-root `SHIPGRADE.md` |

Python tools are optional enhancers: `shipgrade_init.py` creates the workbench, `shipgrade_doctor.py` checks handoffs, and `github_publish_preflight.py` checks public release readiness. A hosted service is not needed for v1; it only becomes useful later for shared team dashboards, cloud evals, or remote rule sync.

See [docs/zero-install.md](docs/zero-install.md).

Zero install is tested, not just described. The release package runs a maintainer-side proof command that reads `SHIPGRADE.md`, wires `AGENTS.md`, `CLAUDE.md`, and Cursor rules into a temporary project, preserves existing user rules, and does not install Python or start a service in the target project:

```bash
python3 tools/shipgrade_zero_install_demo.py --clean
```

See [docs/ADOPTION_PROOF.md](docs/ADOPTION_PROOF.md).

To avoid proving the workflow only on a self-made temporary project, the release package also runs a small external-repo trial. It clones `pypa/sampleproject`, wires ShipGrade from `SHIPGRADE.md`, writes `.shipgrade/task-brief.md` and `.shipgrade/handoff.md`, runs the repo's existing Python unit test, then checks the handoff with `shipgrade_doctor.py`:

```bash
python3 tools/shipgrade_external_trial.py --clean
```

See [docs/EXTERNAL_TRIAL_PROOF.md](docs/EXTERNAL_TRIAL_PROOF.md).

The stronger layer is a multi-repo eval. The release package repeats the same zero-install workflow across `pypa/sampleproject`, `pallets/click`, and `pallets/itsdangerous`: `SHIPGRADE.md` wiring, task brief, handoff, lightweight repository-native validation, and doctor review.

```bash
python3 tools/shipgrade_multi_repo_eval.py --clean
```

See [docs/MULTI_REPO_EVAL_PROOF.md](docs/MULTI_REPO_EVAL_PROOF.md).

The next proof is an issue-style real repository case. The release package clones `pallets/click`, reads real project structure, uses the ShipGrade controller contract to write a task brief, adds a focused `click.option(required=True)` regression check under `.shipgrade/issue-case/`, runs `PYTHONPATH=src` validation, then doctor-checks the handoff.

```bash
python3 tools/shipgrade_real_issue_case.py --clean
```

See [docs/REAL_ISSUE_CASE_PROOF.md](docs/REAL_ISSUE_CASE_PROOF.md).

The next layer is a multi-type real task suite. The release package uses `pallets/click` and `pallets/itsdangerous` to generate and validate four engineering task types: repair, migration, review, and anti-pattern detection. This is not code memorization; it is a way to turn real project structure into task cards, eval rubrics, and chosen/rejected samples.

```bash
python3 tools/shipgrade_real_task_suite.py --clean
```

See [docs/REAL_TASK_SUITE_PROOF.md](docs/REAL_TASK_SUITE_PROOF.md).

Before training or distillation, the task suite becomes a scored eval corpus. The release package writes JSONL cases with prompt, repo, revision, license, evidence paths, rubric, must-include terms, must-avoid terms, and chosen/rejected answers. A deterministic scorer proves chosen answers pass 4/4 and rejected answers fail 4/4.

```bash
python3 tools/shipgrade_eval_corpus.py --clean
```

See [docs/EVAL_CORPUS_PROOF.md](docs/EVAL_CORPUS_PROOF.md), with machine-readable corpus files under [docs/eval-corpus/](docs/eval-corpus/).

To avoid rewarding only samples already represented in the base eval corpus, the release package also includes a holdout replay gate. It uses 12 cases from repositories outside the base eval repos, then proves strong answers pass 12/12, weak answers fail 12/12, and base-overlap is 0.

```bash
python3 tools/shipgrade_holdout_replay.py --clean
```

See [docs/HOLDOUT_REPLAY_PROOF.md](docs/HOLDOUT_REPLAY_PROOF.md), with machine-readable holdout files under [docs/holdout-replay/](docs/holdout-replay/).

## Model / Candidate Output Replay

Beyond the holdout set, the release package combines the 4 base eval cases and 12 holdout cases, then replays three candidate-output profiles: `shipgrade_target`, `lazy_or_overfit_draft`, and `partial_candidate_draft`. This is not a remote model benchmark. It is a deterministic replay gate: the target profile must pass 16/16, lazy drafts must fail 16/16, and partial drafts are stratified into failure layers such as validation evidence, source boundary, and completion audit gaps.

```bash
python3 tools/shipgrade_model_replay.py --clean
```

See [docs/MODEL_REPLAY_PROOF.md](docs/MODEL_REPLAY_PROOF.md), with replay inputs and reports under [docs/model-replay/](docs/model-replay/).

## Judge Panel

After candidate-output replay, the release package also generates a deterministic judge panel. It does not claim that an external model or human has already reviewed the outputs. Instead, it packages the 16 replay cases for later human / Codex / Claude review and runs three CI-safe lenses: `controller_quality`, `source_boundary`, and `completion_audit`.

```bash
python3 tools/shipgrade_judge_panel.py --clean
```

See [docs/JUDGE_PANEL_PROOF.md](docs/JUDGE_PANEL_PROOF.md), with judge packets and reports under [docs/judge-panel/](docs/judge-panel/).

## Blind Review Packet

For real Codex / Claude / human review, the release package still does not claim that external review already happened. It first generates a blind review packet: 16 cases, 48 candidate outputs, a separate answer key, and a scorecard template. Reviewers inspect `candidate A/B/C` first, record signed decisions, then compare against the answer key.

```bash
python3 tools/shipgrade_review_packet.py --clean
```

See [docs/REVIEW_PACKET_PROOF.md](docs/REVIEW_PACKET_PROOF.md), with review packet files under [docs/review-packet/](docs/review-packet/).

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

## Two Install Paths

### Path A: Zero-install MD

Best for first-time users, locked-down company laptops, and Chinese-speaking beginners:

```text
Wire ShipGrade CN into this project using the zero-install path.
Read SHIPGRADE.md from the repo, then write the matching AGENTS.md / CLAUDE.md / Cursor rule.
After that, deliver every task with goal, non-goal, evidence, acceptance, risk, and handoff.
```

### Path B: Python helper tools

Best for maintainers and power users. Requirements: Python 3.10+. No API key and no network access are required.

```bash
python3 tools/shipgrade_init.py /path/to/your-project --idea "Build an operations workbench that shows order risk, inventory gaps, and the next action."
cd /path/to/your-project
open .shipgrade/product-map.html
sed -n '1,120p' .shipgrade/START_HERE.md
sed -n '1,160p' .shipgrade/task-brief.md
sed -n '1,160p' AGENTS.md
```

Then use it like this:

1. Open `.shipgrade/product-map.html` to see the first visible workbench and confirm the `--idea` prefill is visible.
2. Review `.shipgrade/task-brief.md`, then tighten the goal, non-goal, acceptance, and risk boundary.
3. Ask Codex, Claude Code, or Cursor to read the project rules.
4. Make the smallest verified change.
5. Write the result and evidence into `.shipgrade/handoff.md`, then run the doctor.

```bash
python3 tools/shipgrade_doctor.py .shipgrade/handoff.md
```

Install as a Codex skill:

```bash
python3 tools/install_skill.py --force
```

## Use A Distilled Pattern

If you are not starting from a blank brief, initialize the project with an engineering pattern distilled from real repositories:

```bash
python3 tools/shipgrade_init.py /path/to/your-project --pattern command_topology_quality_gate
```

Or write the pattern brief into an existing project:

```bash
python3 tools/shipgrade_patterns.py list
python3 tools/shipgrade_patterns.py show command_topology_quality_gate
python3 tools/shipgrade_patterns.py brief command_topology_quality_gate --type engineering_plan --write .shipgrade/pattern-brief.md
```

The generated `pattern-brief.md` is ready for Codex, Claude Code, or Cursor. It contains the scenario, task context, required points, bad-answer patterns, evidence paths, and acceptance criteria.

## Generated Structure

```text
.shipgrade/
  task-brief.md
  pattern-brief.md
  quality-gate.md
  handoff.md
  AGENTS.snippet.md
AGENTS.md
CLAUDE.md
CLAUDE.shipgrade.md
.cursor/rules/shipgrade.mdc
```

![ShipGrade terminal demo](assets/shipgrade-terminal-demo.png)

## How Different Users Use It

| User | Short path | Advanced path |
| --- | --- | --- |
| Chinese-speaking beginner | Fill `.shipgrade/task-brief.md`, then ask the agent to follow project rules. | Run `shipgrade_doctor.py` before accepting the handoff. |
| Builder | Use ShipGrade as the project workbench for every task. | Start common work from `--pattern` briefs distilled from stronger repositories. |
| Senior reviewer | Review `SKILL.md`, quality gates, evidence docs, licenses, and preflight scripts. | Extend Pattern Cards, Task Cards, and Evals for the team. |

![ShipGrade CN workflow](assets/shipgrade-loop.png)

## Source Backbone: Repository Engineering Distillation Pipeline

The distillation process is not the product promise; it is the sourcing discipline behind the skill. ShipGrade CN does not dump repositories into a model and hope it learns architecture. It turns public, license-reviewed repositories into reviewable engineering assets:

```text
Repository -> Engineering Knowledge -> Task Data -> Eval -> RAG / SFT / DPO
```

The output is what matters to users: task briefs, quality gates, doctor checks, pattern briefs, handoffs, and evals. The full method is documented in `docs/repository-engineering-distillation-pipeline.md`.

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
| `tools/shipgrade_init.py` | Generates the project workbench and agent-rule wiring; `--idea` prefills the first brief and visible workbench. |
| `tools/shipgrade_zero_install_demo.py` | Proves `SHIPGRADE.md` can wire a target project without Python or a service in that target. |
| `tools/shipgrade_external_trial.py` | Runs a zero-install trial against a small public MIT repository and doctor-checks the resulting handoff. |
| `tools/shipgrade_multi_repo_eval.py` | Repeats zero-install wiring, lightweight validation, and doctor review across multiple small public repositories. |
| `tools/shipgrade_real_issue_case.py` | Runs an issue-style regression case inside `pallets/click`, proving the controller contract can drive a real repository task slice. |
| `tools/shipgrade_real_task_suite.py` | Generates repair, migration, review, and anti-pattern detection task samples inside `pallets/click` and `pallets/itsdangerous`. |
| `tools/shipgrade_eval_corpus.py` | Exports real-task samples as JSONL eval cases and proves chosen/rejected answers are separated by the rubric scorer. |
| `tools/shipgrade_holdout_replay.py` | Replays strong/weak answers on 12 repositories outside the base eval corpus to catch overfit quality claims. |
| `tools/shipgrade_model_replay.py` | Replays candidate/model outputs across 16 base + holdout cases and stratifies failures by validation, boundary, and completion gaps. |
| `tools/shipgrade_judge_panel.py` | Generates a three-lens judge packet for the 16 replay cases, ready for later human/Codex/Claude cross-review. |
| `tools/shipgrade_review_packet.py` | Generates a 16-case / 48-candidate blind review packet, separate answer key, and scorecard template for real reviewer handoff. |
| `tools/shipgrade_doctor.py` | Checks whether a handoff contains result, validation, source, risk, security, and next-step evidence. |
| `tools/shipgrade_demo.py` | Runs the quick proof path. |
| `tools/shipgrade_patterns.py` | Lists distilled patterns and writes `.shipgrade/pattern-brief.md`. |
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
- External zero-install trial: `pypa/sampleproject` handoff doctor pass
- Multi-repo external eval: 3/3 public repos passed zero-install eval
- Real repository issue case: `pallets/click` required-option regression case pass
- Real task suite: 4/4 cases across repair/migration/review/anti-pattern detection
- Scored real-task eval corpus: 4 cases, chosen 4/4 pass, rejected 4/4 fail
- Model/candidate output replay: 16 candidate replays with failure stratification
- Judge panel: 16 replay cases, 3 deterministic judge lenses
- Blind review packet: 16 replay cases, 48 blinded candidate outputs

## Why It Is Not Just Prompts

| Question | Answer |
| --- | --- |
| Can a beginner use it? | Yes. Run `shipgrade_init.py`, fill the brief, then follow the quality gate. |
| Does the agent actually see the rules? | Yes. The initializer wires `AGENTS.md`, `CLAUDE.md`, and Cursor rules. |
| Can it reject fake completion? | Yes. The doctor requires artifact paths and validation evidence. |
| Is the research README-only? | No. It generates 11 Repo Cards / 15 Pattern Cards / 90 Task Cards / 90 Eval Cases. Structure scans cover 88 repositories, and deep code case studies cover 11 repositories. |
| Is there runtime evidence? | Yes. Runtime and sandbox evidence live under `docs/`. |
| Has it touched an external repo? | Yes. `docs/EXTERNAL_TRIAL_PROOF.md` records a zero-install trial against `pypa/sampleproject`, including existing unit test evidence and doctor-reviewed handoff. |
| Is there repeated eval evidence? | Yes. `docs/MULTI_REPO_EVAL_PROOF.md` records 3 public repositories passing the same zero-install eval loop. |
| Is there a real issue-style case? | Yes. `docs/REAL_ISSUE_CASE_PROOF.md` records a `pallets/click` CLI behavior regression case with validation and doctor-reviewed handoff. |
| Is there multi-type engineering task evidence? | Yes. `docs/REAL_TASK_SUITE_PROOF.md` records repair, migration, review, and anti-pattern detection samples from real public repositories. |
| Is there a scored eval corpus? | Yes. `docs/EVAL_CORPUS_PROOF.md` records 4 real-task eval cases with chosen 4/4 pass and rejected 4/4 fail. |
| Is there a holdout gate? | Yes. `docs/HOLDOUT_REPLAY_PROOF.md` records 12 non-base-repo replay cases with strong 12/12 pass, weak 12/12 fail, and base overlap 0. |
| Can it replay model/candidate outputs? | Yes. `docs/MODEL_REPLAY_PROOF.md` records 16 base + holdout candidate-output replays and stratifies failures into validation, boundary, and completion gaps. |
| Can outputs be cross-reviewed? | The repo now includes a deterministic judge panel. `docs/JUDGE_PANEL_PROOF.md` records controller/source/completion lenses for 16 replay cases without claiming external model or human review already happened. |
| Can external reviewers blind-review outputs? | Yes. `docs/REVIEW_PACKET_PROOF.md` records a 16-case / 48-candidate blind review packet, separate answer key, and scorecard template without claiming external model or human review already happened. |
| Can the repo be released independently? | Yes. It includes local preflight, GitHub Actions, release packaging, issue templates, and license files. |

## How Those Ideas Become Actions

The source influences land as runnable repository artifacts, not decorative citations:

- spec-first practice becomes `.shipgrade/task-brief.md`
- review and test discipline becomes `.shipgrade/quality-gate.md`
- eval thinking becomes `shipgrade_doctor.py`
- multi-agent collaboration becomes shared `AGENTS.md`, `CLAUDE.md`, and Cursor rules
- design-doc stage gates become `.shipgrade/handoff.md`
- strong repository patterns become `tools/shipgrade_patterns.py brief`

## Document Map

- Start here: `START_HERE.md`
- Evidence index: `docs/EVIDENCE_INDEX.md`
- Distillation pipeline: `docs/repository-engineering-distillation-pipeline.md`
- Distillation assets: `docs/repo-engineering-distillation-assets.md`
- Source attribution: `docs/source-attribution.md`
- Deep source study: `docs/source-depth-dossier.md`
- Code case studies: `docs/deep-code-case-studies.md`
- Runtime evidence: `docs/runtime-smoke-evidence.md`, `docs/sandbox-runtime-cases.md`
- External trial: `docs/EXTERNAL_TRIAL_PROOF.md`
- Multi-repo eval: `docs/MULTI_REPO_EVAL_PROOF.md`
- Real issue case: `docs/REAL_ISSUE_CASE_PROOF.md`
- Real task suite: `docs/REAL_TASK_SUITE_PROOF.md`
- Eval corpus: `docs/EVAL_CORPUS_PROOF.md`, `docs/eval-corpus/`
- Holdout replay: `docs/HOLDOUT_REPLAY_PROOF.md`, `docs/holdout-replay/`
- Model replay: `docs/MODEL_REPLAY_PROOF.md`, `docs/model-replay/`
- Judge panel: `docs/JUDGE_PANEL_PROOF.md`, `docs/judge-panel/`
- Review packet: `docs/REVIEW_PACKET_PROOF.md`, `docs/review-packet/`
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
