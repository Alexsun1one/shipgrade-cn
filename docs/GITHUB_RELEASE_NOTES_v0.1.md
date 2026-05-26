# ShipGrade CN v0.1

## What Changed

- First standalone GitHub-ready release.
- Includes Codex / Claude / Cursor agent entry files.
- Adds `shipgrade_init.py`, `install_skill.py`, `shipgrade_doctor.py`, and `shipgrade_release_check.py`.
- Includes source-depth dossier, real-project gauntlet, transcript evidence, eval tasks, templates, and demo.
- Adds high-signal source radar, source promotion queue, and source promotion batch evidence so discovery keeps turning into audited code review work.

## Validation

```bash
python3 tools/shipgrade_verify.py
python3 tools/shipgrade_release_check.py
python3 tools/shipgrade_doctor.py demo/demo-output.md
bash scripts/verify.sh
```

## Known Limits

- v0.1 is a strong artifact, not market proof.
- More public user transcripts, screenshots, and external issue/PR feedback are still needed before claiming world-class adoption.
