# ShipGrade Transcript Case: SkillsCN release proof with flagship validator

## Result / 交付

- case id: `skillscn-release-proof`
- project ref: `local-project:skills-cn-distill`
- result: `pass`
- artifact: `outputs/shipgrade_transcript_cases/skillscn-release-proof.md`

## ShipGrade Goal

验证 ShipGrade CN 发布包包含来源、训练、runtime evidence、real project gauntlet、high-signal source radar、source promotion queue、source promotion batch、source promotion sandbox cases 和 GitHub publish preflight。

## Expected Contract

- source attribution
- license boundary
- training probes
- real-project evidence
- source radar
- source promotion queue
- source promotion batch
- source promotion sandbox cases
- GitHub publish preflight

## Validation / 验证证据

### 1. flagship package validator

```bash
$ python3 scripts/validate_flagship_skill.py
```

exit: `0`

```text
flagship-validation-ok templates=6 examples=3 demos=2 evals=12 source_refs=103
```
### 2. real project case doctor

```bash
$ python3 dist/ship-grade-engineering-cn-v0.1/tools/shipgrade_doctor.py dist/ship-grade-engineering-cn-v0.1/docs/real-project-gauntlet.md dist/ship-grade-engineering-cn-v0.1/docs/real-project-cases/enterprise-paperclip-runtime.md dist/ship-grade-engineering-cn-v0.1/docs/real-project-cases/exo-harness-contract.md dist/ship-grade-engineering-cn-v0.1/docs/real-project-cases/hardwrite-rewrite-safety.md dist/ship-grade-engineering-cn-v0.1/docs/real-project-cases/silicoville-ledger-migration.md dist/ship-grade-engineering-cn-v0.1/docs/real-project-cases/skillscn-release-quality.md
```

exit: `0`

```text
dist/ship-grade-engineering-cn-v0.1/docs/real-project-gauntlet.md: ship-grade-ok
dist/ship-grade-engineering-cn-v0.1/docs/real-project-cases/enterprise-paperclip-runtime.md: ship-grade-ok
dist/ship-grade-engineering-cn-v0.1/docs/real-project-cases/exo-harness-contract.md: ship-grade-ok
dist/ship-grade-engineering-cn-v0.1/docs/real-project-cases/hardwrite-rewrite-safety.md: ship-grade-ok
dist/ship-grade-engineering-cn-v0.1/docs/real-project-cases/silicoville-ledger-migration.md: ship-grade-ok
dist/ship-grade-engineering-cn-v0.1/docs/real-project-cases/skillscn-release-quality.md: ship-grade-ok
```
### 3. standalone GitHub repo validator

```bash
$ python3 scripts/validate_github_repo.py
```

exit: `0`

```text
github-repo-validation-ok files=94
```
### 4. source radar evidence

```bash
$ python3 -c import json
from pathlib import Path
for p in ['outputs/high_signal_source_radar.json','outputs/source_promotion_queue.json','outputs/source_promotion_batch.json','outputs/source_promotion_sandbox_cases.json','dist/github/shipgrade-cn/docs/evidence/high_signal_source_radar.json','dist/github/shipgrade-cn/docs/evidence/source_promotion_queue.json','dist/github/shipgrade-cn/docs/evidence/source_promotion_batch.json','dist/github/shipgrade-cn/docs/evidence/source_promotion_sandbox_cases.json','dist/github/shipgrade-cn/docs/github-publish-preflight.json']:
    data=json.loads(Path(p).read_text())
    print(p, data.get('candidate_count'), data.get('new_candidate_count'), data.get('green_license_candidate_count'), data.get('row_count'), len(data.get('top_deep_or_sandbox_targets', [])), len(data.get('license_review_targets', [])), data.get('selected_count'), data.get('audited_count'), data.get('runtime_candidate_count'), data.get('static_smoke_pass_count'), data.get('case_count'), data.get('passed_case_count'), data.get('required_step_count'), data.get('passed_required_step_count'), data.get('configured_test_count'), data.get('passed'), data.get('total'))
```

exit: `0`

```text
outputs/high_signal_source_radar.json 87 64 65 None 0 0 None None None None None None None None None None None
outputs/source_promotion_queue.json None None None 87 12 18 None None None None None None None None None None None
outputs/source_promotion_batch.json None None None None 0 0 4 4 2 2 None None None None None None None
outputs/source_promotion_sandbox_cases.json None None None None 0 0 None None None None 2 2 9 9 225 None None
dist/github/shipgrade-cn/docs/evidence/high_signal_source_radar.json 87 64 65 None 0 0 None None None None None None None None None None None
dist/github/shipgrade-cn/docs/evidence/source_promotion_queue.json None None None 87 12 18 None None None None None None None None None None None
dist/github/shipgrade-cn/docs/evidence/source_promotion_batch.json None None None None 0 0 4 4 2 2 None None None None None None None
dist/github/shipgrade-cn/docs/evidence/source_promotion_sandbox_cases.json None None None None 0 0 None None None None 2 2 9 9 225 None None
dist/github/shipgrade-cn/docs/github-publish-preflight.json None None None None 0 0 None None None None None None None None None 12 12
```

## Source / License

- 来源: `local-project:skills-cn-distill` plus command output shown above.
- 许可证 / license: this transcript records command outputs and safe structural evidence only; it does not redistribute private source bodies.

## Boundary / 风险边界

- This transcript proves the listed commands were executable and passed in this local workspace.
- It does not prove public adoption, GitHub stars, or every future task in the project.
- It is a redacted execution transcript, not a replacement for project-specific release gates.

## Forbidden / 禁止事项

- Do not copy secret, token, cookie, session, auth database, private key, browser profile, private config, database content, or private source body into a public case.
