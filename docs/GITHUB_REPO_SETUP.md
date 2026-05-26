# GitHub Repo Setup

This file is for the human who publishes ShipGrade CN.

## Repository Fields

- Repository name: `shipgrade-cn`
- Description: `中文工程 skill for Codex / Claude Code / Cursor: turn vague Chinese requests into verifiable engineering delivery.`
- Social preview: `assets/shipgrade-loop.png`
- Topics: copy from `.github/repo-metadata.json`

## Publish Preflight

```bash
python3 tools/github_publish_preflight.py --write-docs --run-verify
python3 tools/shipgrade_verify.py
python3 tools/shipgrade_demo.py
python3 scripts/create-public-stage.py /tmp/shipgrade-cn-public --init-git
cd /tmp/shipgrade-cn-public
git status --short
```

The staged repo must contain `PUBLISH_PROOF.md` and no `.DS_Store`, `._*`, `__pycache__`, `.pyc`, tokens, cookies, sessions, auth databases, browser profiles, or private keys.

## First Release

```bash
bash scripts/package.sh
```

Attach `.release/shipgrade-cn-v0.1.tar.gz` and its `.sha256` to the first GitHub release.
