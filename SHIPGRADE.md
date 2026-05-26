# ShipGrade CN Zero-Install Rule

Use this file when a user wants ShipGrade CN without installing Python, running a service, or setting up a package manager.

## What This Rule Does

Turn a vague Chinese engineering request into a verifiable delivery loop:

```text
request -> goal/non-goal -> evidence -> smallest change -> validation -> handoff
```

This is enough for Codex, Claude Code, Cursor, or another AI coding agent to start working. Python helper tools are optional.

## Required Output Contract

Every substantive engineering response should end with these facts, even if the exact wording changes:

```text
Result: concrete artifact path, behavior, or state changed
Evidence: command/browser/log/manual check and observed result
Risk: what remains unverified or intentionally out of scope
Handoff: next file, command, or decision point for the next agent
```

## Before Editing

1. Restate the user's real goal in one concrete sentence.
2. Name non-goals: files, modules, data, configs, refactors, or deployments that should not be touched.
3. Gather current evidence from local rules, relevant files, tests, logs, browser state, or user-provided context.
4. Choose the smallest aligned change that can be verified.

## Quality Gate

Do not call a task complete unless:

- There is a concrete artifact path, command result, browser observation, log line, or explicit manual check.
- User changes were not overwritten or reverted.
- Secrets, tokens, cookies, sessions, private keys, browser profiles, and private source bodies were not copied into outputs.
- Source/license boundaries are preserved when borrowing from public material.
- A future agent can continue from the handoff.

## Work Modes

### Intake

Use when the request is vague:

```text
Goal:
Non-goals:
Current evidence:
Acceptance:
Risks:
First slice:
```

### Build

Use when implementation is clear:

- Read nearest `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, README, schemas, and existing patterns.
- Make the smallest correct change.
- Run the fastest meaningful validation.
- Update handoff if the task is substantive.

### Review

Use when judging quality:

- Check whether the result solves the user's real goal.
- Prefer bugs, regressions, missing tests, security risks, license risks, and handoff gaps over style nits.
- Separate facts, inferences, and assumptions.

### Ship

Use when finishing:

```text
Result:
Validation:
Known boundary:
Next handoff point:
```

## Tool Landing Files

If you are asked to "install" this rule without Python:

| Tool | Write or merge into |
| --- | --- |
| Codex | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursor/rules/shipgrade.mdc` |
| Generic AI coding agent | `SHIPGRADE.md` |

If a target file already exists, append a clearly marked `ShipGrade CN` block instead of replacing user rules.

## Optional Enhancements

Use Python only when the user wants deterministic helpers:

- `tools/shipgrade_init.py`: create `.shipgrade/` templates and rule files.
- `tools/shipgrade_doctor.py`: script-check a handoff for evidence.
- `tools/shipgrade_patterns.py`: generate a task brief from distilled engineering patterns.
- `tools/github_publish_preflight.py`: check a public repository before release.

No background service is required for v1.
