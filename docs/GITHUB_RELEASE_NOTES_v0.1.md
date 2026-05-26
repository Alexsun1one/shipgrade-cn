# ShipGrade CN v0.1

## What Changed

- First standalone GitHub-ready release.
- Includes Codex / Claude / Cursor agent entry files.
- Adds `shipgrade_init.py`, `install_skill.py`, `shipgrade_doctor.py`, `shipgrade_demo.py`, and `shipgrade_release_check.py`.
- Includes source-depth dossier, real-project gauntlet, transcript evidence, eval tasks, templates, and a 30-second init/reject/accept demo.
- Adds `docs/DEMO_PROOF.md`, `docs/demo-proof.json`, `PUBLISH_PROOF.md`, and `publish-proof.json` so people can inspect the demo and staging proof without trusting a claim.
- Adds high-signal source radar, source promotion queue, and source promotion batch evidence so discovery keeps turning into audited code review work.
- Local GitHub publish preflight is `15/15`, including `demo-proof`, fake-completion rejection, social preview dimensions, evidence manifest, workflow file, and secret/metadata scan.

## Validation

```bash
python3 tools/shipgrade_verify.py
python3 tools/shipgrade_demo.py --clean
python3 tools/github_publish_preflight.py --write-docs --run-verify
python3 tools/shipgrade_release_check.py
python3 tools/shipgrade_doctor.py demo/demo-output.md
python3 scripts/create-public-stage.py /tmp/shipgrade-cn-public --init-git
bash scripts/verify.sh
```

Expected high-signal outputs:

- `shipgrade-demo-ok`
- `github-publish-preflight-ok checks=15`
- `shipgrade-release-check-ok`
- staged publish proof contains both fake rejection and accepted handoff tails

## Known Limits

- v0.1 is a strong artifact, not market proof.
- The GitHub remote and Actions run prove publishability, not adoption.
- More public user transcripts, screenshots, and external issue/PR feedback are still needed before claiming world-class adoption.
