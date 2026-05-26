# Scored Eval Corpus Proof

This file is generated from a real local run of `python3 tools/shipgrade_eval_corpus.py --output-dir docs/eval-corpus` during release packaging.

It proves ShipGrade CN has a machine-readable eval corpus before claiming training quality. The corpus contains four real-task cases across repair, migration, review, and anti-pattern detection. Each case records prompt, repository, revision, license, path evidence, rubric, must-include terms, must-avoid terms, and synthetic chosen/rejected answers.

The self-check uses a deterministic scorer: chosen answers must satisfy the rubric, while rejected answers must fail. The public package includes the generated JSONL corpus and scoring report under `docs/eval-corpus/`.

## Captured Output

```text
shipgrade-eval-corpus-ok
cases=4
task_types=anti_pattern_detection,migration,repair,review
repos=pallets/click,pallets/itsdangerous
licenses=BSD-3-Clause
chosen_passed=4/4
rejected_failed=4/4
eval_cases_path=docs/eval-corpus/real-task-eval-cases.jsonl
report_path=docs/eval-corpus/real-task-eval-report.json
chosen_rejected_samples=true
rubric_scored=true
source_body_copied_to_public=false
secret_scan=pass
```

## Boundary

- This is an eval-corpus proof, not a claim that a model has been trained or benchmarked on unseen tasks.
- Chosen/rejected answers are synthetic teaching/eval samples derived from public path-level evidence and rubrics.
- Public corpus files contain metadata, prompts, rubrics, path evidence, and synthetic answers only; no upstream source code bodies.
