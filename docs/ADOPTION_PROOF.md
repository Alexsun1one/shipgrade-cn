# Zero-Install Adoption Proof

This file is generated from a real local run of `python3 tools/shipgrade_zero_install_demo.py --clean` during release packaging.

It proves the lowest-friction path does not require the target project to install Python, start a service, create an account, or use an API key. The maintenance script itself runs only inside this repository to produce proof.

The simulated target project starts with existing `AGENTS.md` and `CLAUDE.md` content. The demo reads `SHIPGRADE.md`, appends managed ShipGrade blocks, writes Cursor rules, and verifies existing user rules were preserved.

## Captured Output

```text
shipgrade-zero-install-demo-ok
target=$TMP/shipgrade-zero-install-demo-nu5p86_7
source=SHIPGRADE.md
created=SHIPGRADE.md,AGENTS.md,CLAUDE.md,.cursor/rules/shipgrade.mdc
preserved_existing_rules=true
python_helper_used_in_target=false
service_started=false
next=ask an AI coding agent: 用 ShipGrade 做这个任务
cleaned=true
```

## Boundary

- This proof is local and synthetic; it demonstrates zero-install adoption mechanics, not market adoption.
- The target project is under the system temp folder and is cleaned by `--clean`.
- Python is used only by the repository maintainer to generate this proof; target users can still adopt ShipGrade by giving `SHIPGRADE.md` to their AI coding tool.
