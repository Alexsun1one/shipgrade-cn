# ShipGrade Model Output Replay

This replay gate scores candidate/model-style outputs against the base eval and holdout replay cases, then stratifies failed outputs by failure layer.

- cases: `16`
- base eval cases: `4`
- holdout cases: `12`
- profiles: `shipgrade_target`, `lazy_or_overfit_draft`, `partial_candidate_draft`
- target profile: `16/16` pass
- lazy profile: `16/16` fail
- boundary: metadata, path evidence, prompts, rubrics, and synthetic replay outputs only; no upstream source bodies.

Use `model-output-replay-cases.jsonl` for candidate replay inputs and `model-output-replay-report.json` for deterministic scoring and failure stratification.
