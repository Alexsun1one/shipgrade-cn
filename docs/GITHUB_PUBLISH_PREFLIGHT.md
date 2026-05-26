# GitHub Publish Preflight

This is a local publish-readiness report for the standalone GitHub repository. It does not claim that remote GitHub Actions have run yet.

- passed: `32/32`
- remote CI boundary: `must be verified after the real GitHub repository exists`

| check | status | detail |
| --- | --- | --- |
| `required-files` | `pass` | 100 required files present |
| `readme-launch-surface` | `pass` | README has hook, proof, and preflight surface |
| `readme-english-surface` | `pass` | README.en.md has standalone onboarding surface |
| `shipgrade-zero-install-rule` | `pass` | SHIPGRADE.md is Chinese-first and zero-install |
| `skill-frontmatter` | `pass` | machine-readable frontmatter with name/description triggers |
| `world-class-skill-contract` | `pass` | SKILL.md encodes controller intelligence, source distillation, and completion audit |
| `github-workflow` | `pass` | validate workflow has PR/push and release check |
| `repo-metadata` | `pass` | topics=10 missing=[] |
| `public-evidence-manifest` | `pass` | evidence_files=17 |
| `repo-engineering-distillation-assets` | `pass` | summary=11/15/90/90 files={'repo_cards': 11, 'pattern_cards': 15, 'task_cards': 90, 'eval_cases': 90} |
| `patterns-tool` | `pass` | shipgrade-patterns-ok patterns=15 tasks=90 evals=90; show=command_topology_quality_gate; brief=pattern-brief-ok |
| `init-pattern-workbench` | `pass` | shipgrade_init --pattern writes pattern-brief and wires agent rules |
| `source-promotion-batch` | `pass` | selected=4 audited=4 runtime=2 static_smoke=2 |
| `source-promotion-sandbox-cases` | `pass` | cases=3/3 required=13/13 configured_tests=264 |
| `sandbox-runtime-matrix` | `pass` | cases=3/3 steps=12/12 |
| `social-preview` | `pass` | dimensions=(1672, 941) |
| `demo-gif` | `pass` | dimensions=(1200, 675) |
| `issue-pr-templates` | `pass` | issue and PR templates include validation language |
| `secret-and-metadata-scan` | `pass` | no generated metadata, local paths, or secret patterns |
| `doctor-fake-rejection` | `pass` | fake completion rejected |
| `demo-proof` | `pass` | demo proof captures init/reject/accept path |
| `zero-install-adoption-proof` | `pass` | SHIPGRADE.md-only adoption proof preserves existing rules and avoids target Python/service |
| `external-zero-install-trial` | `pass` | pypa/sampleproject zero-install trial has unit-test and doctor proof |
| `multi-repo-external-eval` | `pass` | 3 public repositories passed zero-install eval with doctor-reviewed handoffs |
| `real-repo-issue-case` | `pass` | pallets/click issue-style regression case passed validation and doctor review |
| `real-task-suite` | `pass` | 4 real task cases covered repair/migration/review/anti-pattern detection |
| `scored-eval-corpus` | `pass` | 4 scored eval cases separate chosen/rejected answers |
| `scored-holdout-replay` | `pass` | 12 holdout replay cases separate strong/weak answers with no base-repo overlap |
| `scored-model-output-replay` | `pass` | 16 candidate/model output replays pass target, fail lazy drafts, and stratify failure layers |
| `deterministic-judge-panel` | `pass` | 16 replay cases have deterministic controller/source/completion judge-panel votes |
| `blind-review-packet` | `pass` | 16 cases and 48 blinded candidates are ready for signed external review |
| `shipgrade-verify` | `pass` | shipgrade-verify-ok  |

## Publish Command Surface

```bash
python3 tools/github_publish_preflight.py --write-docs --run-verify
python3 tools/shipgrade_verify.py
python3 tools/shipgrade_zero_install_demo.py --clean
python3 tools/shipgrade_external_trial.py --clean
python3 tools/shipgrade_multi_repo_eval.py --clean
python3 tools/shipgrade_real_issue_case.py --clean
python3 tools/shipgrade_real_task_suite.py --clean
python3 tools/shipgrade_eval_corpus.py --clean
python3 tools/shipgrade_holdout_replay.py --clean
python3 tools/shipgrade_model_replay.py --clean
python3 tools/shipgrade_judge_panel.py --clean
python3 tools/shipgrade_review_packet.py --clean
python3 tools/shipgrade_demo.py
python3 tools/shipgrade_init.py /tmp/my-project --pattern command_topology_quality_gate
python3 tools/shipgrade_patterns.py validate
python3 tools/shipgrade_patterns.py brief command_topology_quality_gate --type engineering_plan --write .shipgrade/pattern-brief.md
python3 scripts/create-public-stage.py /tmp/shipgrade-cn-public --init-git
bash scripts/package.sh
```

## Boundary

- This report checks the local release artifact, not a remote GitHub repository.
- After publishing, verify the real Actions run, repository topics, social preview, release archive, and issue templates on GitHub.
