# ShipGrade Judge Panel

This deterministic judge panel turns model replay cases into a cross-review packet. It does not claim that an external model or human has already reviewed the outputs.

- cases: `16`
- profiles: `3`
- judge lenses: `controller_quality`, `source_boundary`, `completion_audit`
- target profile: `16/16` unanimous pass
- lazy profile: `16/16` majority rejected
- partial profile: `16/16` majority rejected
- boundary: metadata, prompts, rubrics, path evidence, and synthetic candidate outputs only; no upstream source bodies.

Use `judge-panel-cases.jsonl` as a human/Codex/Claude review packet and `judge-panel-report.json` as the deterministic CI gate.
