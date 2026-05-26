# Model Output Replay Proof

This file is generated from a real local run of `python3 tools/shipgrade_model_replay.py --output-dir docs/model-replay` during release packaging.

It proves ShipGrade CN can replay candidate or model-style outputs through the same base eval and holdout replay gates before making quality claims. The replay set contains 16 cases: 4 base eval cases and 12 holdout cases.

The self-check uses deterministic rubric scoring across three profiles: `shipgrade_target`, `lazy_or_overfit_draft`, and `partial_candidate_draft`. Target answers must pass 16/16, lazy drafts must fail 16/16, and partial drafts must expose stratified failure layers such as validation evidence gaps, source boundary gaps, and completion audit gaps.

## Captured Output

```text
shipgrade-model-replay-ok
cases=16
base_eval_cases=4
holdout_cases=12
profiles=3
target_passed=16/16
lazy_failed=16/16
partial_failed=16/16
failure_layers=completion_audit_gap,forbidden_behavior_hit,source_boundary_gap,validation_evidence_gap
model_replay_cases_path=docs/model-replay/model-output-replay-cases.jsonl
report_path=docs/model-replay/model-output-replay-report.json
candidate_outputs_replayed=true
failure_stratified=true
source_body_copied_to_public=false
secret_scan=pass
```

## Boundary

- This is a candidate-output replay proof, not a claim that a model has been trained, tuned, or judged by an external benchmark.
- Public replay files contain metadata, prompts, rubrics, path evidence, and synthetic candidate outputs only; no upstream source code bodies.
- Secret, cookie, session, private-key, auth database, browser profile, and private repository content remains forbidden.
