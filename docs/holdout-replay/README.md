# ShipGrade Holdout Replay

This holdout set replays strong and weak answers on repositories that are not part of the scored real-task eval corpus.

- cases: `8`
- base overlap repos: `0`
- strong answers: `8/8` pass
- weak answers: `8/8` fail
- boundary: metadata, path evidence, prompts, rubrics, and synthetic replay answers only; no upstream source bodies.

Use `holdout-replay-cases.jsonl` for replay inputs and `holdout-replay-report.json` for the deterministic self-check result.
