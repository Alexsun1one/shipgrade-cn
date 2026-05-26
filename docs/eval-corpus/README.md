# ShipGrade Real Task Eval Corpus

This corpus turns real public repository evidence into evaluation tasks for ShipGrade CN.

- cases: `4`
- task types: `repair`, `migration`, `review`, `anti_pattern_detection`
- repos: `pallets/click`, `pallets/itsdangerous`
- boundary: metadata, path evidence, prompts, rubrics, and synthetic chosen/rejected answers only; no upstream source bodies.

Use `real-task-eval-cases.jsonl` for eval inputs and `real-task-eval-report.json` for the deterministic self-check result.
