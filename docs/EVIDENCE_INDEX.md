# Evidence Index

This file maps public README claims to repository-local evidence. It exists so ShipGrade CN does not ask readers to trust private `outputs/`, local `dist/`, or unpublished release folders.

## Claim Map

| claim | repository-local evidence |
| --- | --- |
| Runtime sandbox matrix is real | `docs/sandbox-runtime-cases.md` and `docs/evidence/sandbox_runtime_cases.json` |
| GitHub publish readiness was checked locally | `docs/GITHUB_PUBLISH_PREFLIGHT.md` and `docs/github-publish-preflight.json` |
| Runtime smoke covered 5 cloned repos | `docs/runtime-smoke-evidence.md` and `docs/evidence/runtime_smoke_evidence.json` |
| Real project gauntlet passed 5/5 | `docs/real-project-gauntlet.md`, `docs/real-project-cases/`, and `docs/evidence/real_project_gauntlet.json` |
| Transcript evidence passed 2/2 | `docs/transcript-evidence.md`, `docs/transcript-cases/`, and `docs/evidence/shipgrade_transcript_evidence.json` |
| Source structure was analyzed beyond README | `docs/source-depth-dossier.md`, `docs/code-structure-lessons.md`, and `docs/evidence/repo_structure_report.json` |
| High-signal source discovery stays current | `docs/high-signal-source-radar.md` and `docs/evidence/high_signal_source_radar.json` |
| Source discovery is converted into action | `docs/source-promotion-queue.md` and `docs/evidence/source_promotion_queue.json` |
| Source promotion queue is actually audited | `docs/source-promotion-batch.md` and `docs/evidence/source_promotion_batch.json` |
| Promoted runtime candidates are actually executed | `docs/source-promotion-sandbox-cases.md` and `docs/evidence/source_promotion_sandbox_cases.json` |
| Deep code case studies inspected runtime clones | `docs/deep-code-case-studies.md` and `docs/evidence/deep_code_case_studies.json` |
| Repo/Pattern/Task/Eval assets are generated from code evidence | `docs/repo-engineering-distillation-assets.md` and `docs/evidence/repo_engineering_distillation/*.jsonl` |
| Distilled patterns can initialize a real project workbench | `tools/shipgrade_init.py`, `tools/shipgrade_patterns.py`, and `docs/GITHUB_PUBLISH_PREFLIGHT.md` |
| Source overlap was compressed, not blindly merged | `docs/overlap-decisions.md` and `docs/evidence/source_overlap_report.json` |
| Adapter metrics are bounded execution evidence | `QUALITY_REPORT.md` and `docs/evidence/qwen_lora_quality_review.json` |
| Zero-install works on a small external public repo | `docs/EXTERNAL_TRIAL_PROOF.md` and `docs/external-trial-proof.json` |
| Zero-install generalizes across multiple small public repos | `docs/MULTI_REPO_EVAL_PROOF.md` and `docs/multi-repo-eval-proof.json` |
| ShipGrade can drive an issue-style real repo case | `docs/REAL_ISSUE_CASE_PROOF.md` and `docs/real-issue-case-proof.json` |
| ShipGrade covers multi-type real engineering tasks | `docs/REAL_TASK_SUITE_PROOF.md` and `docs/real-task-suite-proof.json` |
| ShipGrade has a scored real-task eval corpus | `docs/EVAL_CORPUS_PROOF.md`, `docs/eval-corpus-proof.json`, and `docs/eval-corpus/real-task-eval-cases.jsonl` |
| ShipGrade has an unseen-repo holdout replay gate | `docs/HOLDOUT_REPLAY_PROOF.md`, `docs/holdout-replay-proof.json`, and `docs/holdout-replay/holdout-replay-cases.jsonl` |
| ShipGrade can replay candidate/model outputs and stratify failure modes | `docs/MODEL_REPLAY_PROOF.md`, `docs/model-replay-proof.json`, and `docs/model-replay/model-output-replay-report.json` |
| Non-self release artifacts have stable hashes | `docs/public-evidence-manifest.json` |

## Verification

```bash
python3 tools/shipgrade_verify.py
python3 tools/shipgrade_release_check.py
python3 tools/shipgrade_init.py /tmp/shipgrade-demo-project --pattern command_topology_quality_gate
python3 scripts/create-public-stage.py /tmp/shipgrade-cn-public --init-git
```

## Boundary

The evidence here is redacted and public-safe. It does not include private source bodies, credentials, cookies, sessions, auth databases, browser profiles, private keys, or API tokens.
