# Good First Issues

These are intentionally small so contributors can improve ShipGrade CN without touching private data or changing the core quality promise.

## Documentation

- Add a one-page Windows quick start using PowerShell.
- Add a bilingual one-paragraph summary for international readers.
- Improve `docs/DEMO_SCRIPT.md` with a real terminal recording checklist.

## Validation

- Add one more low-side-effect runtime smoke check for a public Python repo.
- Add a validator check that every launch doc is referenced from the README.
- Add more negative demo outputs and confirm `shipgrade_doctor.py` rejects each failure mode.

## Templates

- Add a stricter rollback section to `templates/quality-gate.md`.
- Add a `small-bugfix.md` task brief for beginner users.
- Add a short "handoff to next agent" template for team projects.

## Rules

- Keep all examples public and synthetic.
- Do not add secrets, tokens, cookies, browser profiles, session databases, or private repository content.
- Every change should be verifiable with `python3 tools/shipgrade_verify.py`.
