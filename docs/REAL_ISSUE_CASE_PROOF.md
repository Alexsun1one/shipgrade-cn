# Real Repository Issue Case Proof

This file is generated from a real local run of `python3 tools/shipgrade_real_issue_case.py --clean` during release packaging.

It proves ShipGrade CN can drive an issue-style workflow inside a real public repository, not only wire rules or run synthetic temp projects. The case uses `pallets/click`, writes a ShipGrade task brief, creates a focused CLI required-option regression check under `.shipgrade/issue-case/`, runs repository-local validation with `PYTHONPATH=src`, and checks the handoff with `shipgrade_doctor.py`.

The proof records repository metadata, task intent, generated proof paths, command results, and pass/fail metadata. It does not copy upstream source bodies into this public package and does not claim an upstream issue was fixed, submitted, or merged.

## Captured Output

```text
shipgrade-real-issue-case-ok
repo=pallets/click
url=https://github.com/pallets/click
revision=6a141c3681027e8124ce5a3c70e608dbbebffafb
license=BSD-3-Clause
issue=click-required-option-regression
source=SHIPGRADE.md
created=SHIPGRADE.md,AGENTS.md,CLAUDE.md,.cursor/rules/shipgrade.mdc,.shipgrade/task-brief.md,.shipgrade/issue-case/test_click_required_option.py,.shipgrade/handoff.md
validation=python -m py_compile .shipgrade/issue-case/test_click_required_option.py: ok exit 0
validation=PYTHONPATH=src python .shipgrade/issue-case/test_click_required_option.py: ok exit 0
doctor=.shipgrade/handoff.md: ship-grade-ok
controller_intelligence=true
evidence_matrix=true
completion_audit=true
python_helper_used_in_target=false
service_started=false
source_body_copied_to_public=false
target=$TMP/shipgrade-real-issue-case-e_ugg3hx
cleaned=true
```

## Boundary

- This is an issue-style real repository case, not a claim of upstream maintainer adoption or merged contribution.
- The target clone is under the system temp folder and is cleaned by `--clean`.
- Python runs only a generated focused regression check, repository-local imports, and the maintainer-side doctor check; ShipGrade helper files are not installed into the target repo.
- Public evidence records metadata, generated proof paths, task intent, and command outcomes only, not upstream source code bodies.
