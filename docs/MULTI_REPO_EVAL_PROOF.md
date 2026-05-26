# Multi-Repo External Eval Proof

This file is generated from a real local run of `python3 tools/shipgrade_multi_repo_eval.py --clean` during release packaging.

It proves ShipGrade CN can repeat the same zero-install workflow across multiple small, license-clear public repositories. Each case wires ShipGrade from `SHIPGRADE.md`, writes `.shipgrade/task-brief.md` and `.shipgrade/handoff.md`, runs lightweight repository-native validation, then checks the handoff with `shipgrade_doctor.py`.

The proof keeps only repository names, revisions, licenses, command labels, and pass/fail metadata. It does not copy upstream source bodies into this public package.

## Captured Output

```text
shipgrade-multi-repo-eval-ok
cases=3
passed=3
case=pypa/sampleproject revision=621e4974ca25ce531773def586ba3ed8e736b3fc license=MIT validations=2 doctor=ship-grade-ok
validation=pypa/sampleproject :: python -m py_compile src/sample/simple.py: ok exit 0
validation=pypa/sampleproject :: PYTHONPATH=src python -m unittest tests.test_simple: ok exit 0
case=pallets/click revision=6a141c3681027e8124ce5a3c70e608dbbebffafb license=BSD-3-Clause validations=2 doctor=ship-grade-ok
validation=pallets/click :: python -m py_compile src/click/core.py src/click/decorators.py src/click/testing.py: ok exit 0
validation=pallets/click :: PYTHONPATH=src python -c click CliRunner smoke: ok exit 0
case=pallets/itsdangerous revision=672971d66a2ef9f85151e53283113f33d642dabd license=BSD-3-Clause validations=2 doctor=ship-grade-ok
validation=pallets/itsdangerous :: python -m py_compile src/itsdangerous/serializer.py src/itsdangerous/url_safe.py src/itsdangerous/signer.py: ok exit 0
validation=pallets/itsdangerous :: PYTHONPATH=src python -c itsdangerous serializer roundtrip: ok exit 0
source=SHIPGRADE.md
python_helper_used_in_target=false
service_started=false
source_body_copied_to_public=false
target=$TMP/shipgrade-multi-repo-eval-ixz4sa7e
cleaned=true
```

## Boundary

- This is a maintainer-side external eval, not public adoption or a market traction claim.
- Target clones are under the system temp folder and are cleaned by `--clean`.
- Python runs only repository-native smoke checks and the maintainer-side doctor check; ShipGrade helper files are not installed into target repos.
- These cases become training/eval candidates only after their brief, validation, and handoff evidence pass the same gates.
