# Holdout Replay Proof

This file is generated from a real local run of `python3 tools/shipgrade_holdout_replay.py --output-dir docs/holdout-replay` during release packaging.

It proves ShipGrade CN has an unseen-repo replay gate before claiming training or distillation quality. The holdout set contains eight cases from repositories that do not overlap with the base scored eval corpus.

The self-check uses the same deterministic scoring style: strong answers must satisfy the rubric, weak answers must fail, and `base_overlap_repos` must be zero. The public package includes JSONL replay inputs and a scoring report under `docs/holdout-replay/`.

## Captured Output

```text
shipgrade-holdout-replay-ok
cases=8
task_types=anti_pattern_detection,engineering_plan,migration,repair,review,runtime_gate,skill_design
repos=SuperClaude-Org/SuperClaude_Framework,UKGovernmentBEIS/inspect_ai,addyosmani/agent-skills,affaan-m/ECC,browser-use/browser-use,github/spec-kit,humanlayer/12-factor-agents,promptfoo/promptfoo
licenses=Apache-2.0,MIT
base_overlap_repos=0
strong_passed=8/8
weak_failed=8/8
holdout_replay_cases_path=docs/holdout-replay/holdout-replay-cases.jsonl
report_path=docs/holdout-replay/holdout-replay-report.json
holdout_not_training=true
rubric_scored=true
source_body_copied_to_public=false
secret_scan=pass
```

## Boundary

- This is a holdout replay proof, not a claim that a model has been trained or benchmarked by an external judge.
- Strong/weak answers are synthetic teaching/eval samples derived from public path-level evidence and rubrics.
- Public holdout files contain metadata, prompts, rubrics, path evidence, and synthetic answers only; no upstream source code bodies.
