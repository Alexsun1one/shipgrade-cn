# Review Packet Proof

This file is generated from a real local run of `python3 tools/shipgrade_review_packet.py --output-dir docs/review-packet` during release packaging.

It proves ShipGrade CN can turn replay outputs into a blind external-review handoff. The packet covers 16 cases and 48 candidate outputs, with profile labels separated from the review packet and stored in a separate answer key.

This proof does not claim that an external model or human has already reviewed the outputs. It creates a public, CI-safe review packet plus scorecard template for future Codex, Claude, human, or other reviewer passes.

## Captured Output

```text
shipgrade-review-packet-ok
cases=16
candidate_outputs=48
scorecard_rows=48
blind_profile_labels=true
answer_key_separate=true
scorecard_template_ready=true
signed_review_required_before_claim=true
external_model_called=false
human_review_claimed=false
source_body_copied_to_public=false
secret_scan=pass
review_packet_path=docs/review-packet/review-packet-cases.jsonl
report_path=docs/review-packet/review-packet-report.json
```

## Boundary

- This is a blind-review packet proof, not an external benchmark or live human-review claim.
- Public review files contain metadata, prompts, rubrics, path evidence, and synthetic candidate outputs only; no upstream source code bodies.
- The answer key is public for audit, but reviewers should record decisions before opening it.
- Secret, cookie, session, private-key, auth database, browser profile, and private repository content remains forbidden.
