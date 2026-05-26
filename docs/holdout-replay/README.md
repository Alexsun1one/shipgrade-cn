# ShipGrade Holdout Replay

This holdout set replays strong and weak answers on repositories that are not part of the scored real-task eval corpus.

- cases: `12`
- base overlap repos: `0`
- strong answers: `12/12` pass
- weak answers: `12/12` fail
- boundary: metadata, path evidence, prompts, rubrics, and synthetic replay answers only; no upstream source bodies.

Use `holdout-replay-cases.jsonl` for replay inputs and `holdout-replay-report.json` for the deterministic self-check result.
