# Judge Panel Proof

This file is generated from a real local run of `python3 tools/shipgrade_judge_panel.py --output-dir docs/judge-panel` during release packaging.

It proves ShipGrade CN has a deterministic cross-review packet after candidate-output replay. The packet covers 16 replay cases and three judge lenses: `controller_quality`, `source_boundary`, and `completion_audit`.

This proof does not claim that an external model or human has already reviewed the outputs. It creates a public, CI-safe judge panel that can later be handed to human reviewers, Codex, Claude, or other reviewers without copying upstream source bodies.

## Captured Output

```text
shipgrade-judge-panel-ok
cases=16
profiles=3
judges=3
judge_lenses=controller_quality,source_boundary,completion_audit
target_unanimous_pass=16/16
lazy_majority_rejected=16/16
partial_majority_rejected=16/16
judge_panel_cases_path=docs/judge-panel/judge-panel-cases.jsonl
report_path=docs/judge-panel/judge-panel-report.json
cross_judge_packet_ready=true
deterministic_judge_panel=true
external_model_called=false
human_review_claimed=false
source_body_copied_to_public=false
secret_scan=pass
```

## Boundary

- This is a deterministic judge-panel proof, not an external benchmark or live human-review claim.
- Public judge files contain metadata, prompts, rubrics, path evidence, and synthetic candidate outputs only; no upstream source code bodies.
- Secret, cookie, session, private-key, auth database, browser profile, and private repository content remains forbidden.
