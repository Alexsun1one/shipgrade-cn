# External Zero-Install Trial Proof

This file is generated from a real local run of `python3 tools/shipgrade_external_trial.py --clean` during release packaging.

It proves ShipGrade CN is not only tested against a self-made temporary project. The trial clones the small MIT-licensed public repository `pypa/sampleproject`, wires ShipGrade from `SHIPGRADE.md`, writes a task brief and handoff, runs the repository's existing Python unit test, and then checks the handoff with `shipgrade_doctor.py`.

The proof keeps only repository metadata, paths, command results, and a redacted output transcript. It does not copy upstream source bodies into this public package.

## Captured Output

```text
shipgrade-external-trial-ok
repo=pypa/sampleproject
url=https://github.com/pypa/sampleproject
revision=621e4974ca25ce531773def586ba3ed8e736b3fc
license=MIT
tracked_files=12
source=SHIPGRADE.md
created=SHIPGRADE.md,AGENTS.md,CLAUDE.md,.cursor/rules/shipgrade.mdc,.shipgrade/task-brief.md,.shipgrade/handoff.md
validation=python -m py_compile src/sample/simple.py: ok exit 0
validation=PYTHONPATH=src python -m unittest tests.test_simple: ok exit 0
doctor=.shipgrade/handoff.md: ship-grade-ok
python_helper_used_in_target=false
service_started=false
source_body_copied_to_public=false
target=$TMP/shipgrade-external-trial-jjdmepyc
cleaned=true
```

## Boundary

- This proof demonstrates external-repository adoption mechanics and one existing unit-test path; it does not claim public user adoption or GitHub stars.
- The target clone is under the system temp folder and is cleaned by `--clean`.
- Python runs only to execute the external repository's own test and the maintainer-side doctor check; ShipGrade helper files are not installed into the target project.
- Public evidence records metadata and command outcomes only, not upstream source code bodies.
