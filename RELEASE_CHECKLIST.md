# Release Checklist

Use this before publishing a GitHub release.

## Required Commands

```bash
python3 tools/shipgrade_release_check.py
python3 tools/shipgrade_doctor.py demo/demo-output.md
python3 tools/shipgrade_init.py /tmp/shipgrade-release-proof
python3 tools/shipgrade_demo.py
```

## Required Human Checks

- README first screen explains what, why, quickstart, proof, and boundary.
- `START_HERE.md` works for 小白 / 进阶 / 专业三类用户。
- `LICENSE.md`, `NOTICE.md`, `SECURITY.md`, `CONTRIBUTING.md`, and `.github/` templates exist.
- `docs/source-depth-dossier.md` and `docs/deep-code-case-studies.md` contain structure/code-shape evidence, not just README summaries.
- `docs/transcript-evidence.md` includes redacted command evidence.
- No secret/token/cookie/session/auth/private key or private source body appears in the release.
- Tarball has no `.DS_Store` or `._*` metadata.

## Release Note Minimum

- What changed.
- Why it matters.
- Validation commands and exact result.
- Known limits.
- Hash of the release archive.
