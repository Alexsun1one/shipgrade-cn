# Demo Proof

This file is generated from a real local run of `python3 tools/shipgrade_demo.py --clean` during release packaging.

It proves the first-screen demo path does three things without private code, credentials, cookies, sessions, or browser profiles:

1. Initializes a demo project and wires `.shipgrade/`, `AGENTS.md`, `CLAUDE.md`, and Cursor rules.
2. Rejects a fake completion that says it merely looks done.
3. Accepts a handoff that contains concrete artifact paths, command evidence, source/license boundary, security boundary, and next handoff entry.

## Captured Output

```text
shipgrade-demo-ok
target=$TMP/shipgrade-demo-project-9hy1fj3i
created=.shipgrade/task-brief.md,.shipgrade/quality-gate.md,.shipgrade/handoff.md,AGENTS.md,CLAUDE.md,.cursor/rules/shipgrade.mdc,fake-completion.md,accepted-handoff.md
fake_rejection=$TMP/shipgrade-demo-project-9hy1fj3i/fake-completion.md: ship-grade-fail vague_or_unverified_language missing_concrete_artifact_path missing_command_or_browser_evidence
accepted=$TMP/shipgrade-demo-project-9hy1fj3i/accepted-handoff.md: ship-grade-ok
next=open $TMP/shipgrade-demo-project-9hy1fj3i/.shipgrade/task-brief.md
cleaned=true
```

## Boundary

- This proof is local and synthetic; it does not claim real GitHub Actions or external adoption.
- The demo target is under the system temp folder and is cleaned by `--clean`.
