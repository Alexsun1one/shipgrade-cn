# ShipGrade Transcript Evidence

## Result / 交付

- cases: `2`
- passed: `2/2`
- artifact directory: `outputs/shipgrade_transcript_cases/`

## Cases

| case | project | commands | status | artifact |
| --- | --- | --- | --- | --- |
| `enterprise-paperclip-api-smoke` | `local-project:enterprise` | 2 | pass | `outputs/shipgrade_transcript_cases/enterprise-paperclip-api-smoke.md` |
| `skillscn-release-proof` | `local-project:skills-cn-distill` | 4 | pass | `outputs/shipgrade_transcript_cases/skillscn-release-proof.md` |

## Validation / 验证证据

Each case file contains the exact command argv, exit code, and redacted output. Each case must pass `tools/shipgrade_doctor.py`.

## Source / License

- 来源: safe command outputs from local project refs.
- 许可证 / license: no private source bodies are redistributed in this public evidence package.

## Boundary / 风险边界

- This is stronger than structural gauntlet evidence because commands are actually executed.
- It still does not prove market adoption or future issue/PR quality.

## Forbidden / 禁止事项

- Do not copy secret, token, cookie, session, auth database, private key, browser profile, private config, database content, or private source body into a public transcript.
