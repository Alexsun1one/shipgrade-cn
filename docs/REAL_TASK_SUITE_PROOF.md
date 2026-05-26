# Real Task Suite Proof

This file is generated from a real local run of `python3 tools/shipgrade_real_task_suite.py --clean` during release packaging.

It proves ShipGrade CN can convert real public repository structure into multiple engineering task types, not just one smoke check. The suite uses `pallets/click` and `pallets/itsdangerous`, then generates repair, migration, review, and anti-pattern detection samples under `.shipgrade/task-suite/`.

The proof records repository metadata, task types, validation results, doctor-reviewed handoffs, and chosen/rejected sample evidence. It does not copy upstream source bodies into this public package and does not claim upstream maintainer adoption or merged changes.

## Captured Output

```text
shipgrade-real-task-suite-ok
repos=2
cases=4
passed=4
repo=pallets/click revision=6a141c3681027e8124ce5a3c70e608dbbebffafb license=BSD-3-Clause
repo=pallets/itsdangerous revision=672971d66a2ef9f85151e53283113f33d642dabd license=BSD-3-Clause
case=click_required_option_repair repo=pallets/click task_type=repair validation=PYTHONPATH=src python .shipgrade/task-suite/click_required_option_repair.py: ok exit 0
case=click_ci_local_gate_migration repo=pallets/click task_type=migration validation=card_terms migration-click-ci-local-gate.md: ok
case=itsdangerous_serializer_security_review repo=pallets/itsdangerous task_type=review validation=card_terms review-itsdangerous-serializer-security.md: ok
case=itsdangerous_vague_handoff_antipattern repo=pallets/itsdangerous task_type=anti_pattern_detection validation=shipgrade_doctor.py rejected-vague-handoff.md: expected fail ok
doctor_handoffs=2/2
task_types=repair,migration,review,anti_pattern_detection
controller_intelligence=true
eval_rubric=true
chosen_rejected_samples=true
python_helper_used_in_target=false
service_started=false
source_body_copied_to_public=false
target=$TMP/shipgrade-real-task-suite-ycoxp23u
cleaned=true
```

## Boundary

- This is a maintainer-side real task suite, not a market adoption or upstream merge claim.
- Target clones are under the system temp folder and are cleaned by `--clean`.
- Python runs generated focused checks, card-term checks, and the maintainer-side doctor check; ShipGrade helper files are not installed into target repos.
- Public evidence records metadata, task type labels, validation lines, and pass/fail metadata only, not upstream source code bodies.
