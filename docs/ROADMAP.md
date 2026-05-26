# Roadmap

ShipGrade CN v0.1 is GitHub-ready. The next milestones are about external proof, better evals, and safer automation.

## v0.2 - External Proof

- Add 10 public, redacted real-user transcripts.
- Add screenshots or terminal recordings for the demo path.
- Add a bilingual README summary while keeping the core workflow Chinese-first.
- Run the skill on at least 10 unrelated public repos.

## v0.3 - Stronger Evaluation

- Add a small promptfoo-compatible eval export.
- Add negative tests for fake evidence, missing validation, and unsafe secret handling.
- Add cross-agent handoff fixtures for Codex, Claude Code, Cursor, and CLI-only environments.

## v0.4 - Installer Polish

- Add a tiny `shipgrade` CLI wrapper.
- Add upgrade checks for existing `.shipgrade/` folders.
- Add Windows PowerShell examples where Bash is unavailable.

## Non-Goals

- Do not ingest private repos or leaked prompts.
- Do not claim market adoption from local validation.
- Do not train a tiny model to replace strong review; small models can route, check, and draft only.
