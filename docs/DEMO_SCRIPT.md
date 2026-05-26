# Demo Script

Goal: record a 3 minute demo that makes the repository feel immediately useful and professionally verifiable.

## Scene 1 - First Contact

Show the README first screen:

- `assets/shipgrade-hero-cn.png`
- `assets/shipgrade-loop.png`
- `assets/shipgrade-proof-map-cn.png`
- `assets/shipgrade-audience-cn.png`
- 30 second quick proof command
- Evidence snapshot

Say: "This is not a prompt collection. It gives AI agents a delivery contract."

Run:

```bash
python3 tools/shipgrade_demo.py
```

Show `shipgrade-demo-ok`, `fake_rejection=...ship-grade-fail`, and `accepted=...ship-grade-ok`.

## Scene 2 - Generate A Project Workbench

Run:

```bash
python3 tools/shipgrade_init.py /tmp/shipgrade-demo-project --pattern command_topology_quality_gate
find /tmp/shipgrade-demo-project -maxdepth 3 -type f | sort
```

Open `.shipgrade/task-brief.md`, `.shipgrade/pattern-brief.md`, `.shipgrade/quality-gate.md`, and `.shipgrade/handoff.md`.

## Scene 3 - Verify The Package

Run:

```bash
python3 tools/shipgrade_verify.py
python3 scripts/create-public-stage.py /tmp/shipgrade-cn-public --init-git
```

Show `PUBLISH_PROOF.md` and `publish-proof.json`.

## Scene 4 - Why It Is Different

Open:

- `docs/source-depth-dossier.md`
- `docs/deep-code-case-studies.md`
- `docs/sandbox-runtime-cases.md`
- `docs/real-project-gauntlet.md`
- `docs/source-attribution.md`

Say: "README is the poster. These files are the evidence."
