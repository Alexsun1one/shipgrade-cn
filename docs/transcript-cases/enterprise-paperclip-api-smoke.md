# ShipGrade Transcript Case: Enterprise Paperclip API smoke with ShipGrade contract

## Result / 交付

- case id: `enterprise-paperclip-api-smoke`
- project ref: `local-project:enterprise`
- result: `pass`
- artifact: `outputs/shipgrade_transcript_cases/enterprise-paperclip-api-smoke.md`

## ShipGrade Goal

验证 Paperclip/local-tools 读路径具备真实测试入口,并把结果写成可交付 handoff 证据。

## Expected Contract

- route smoke
- field/read-model coverage
- read-only boundary
- handoff entry

## Validation / 验证证据

### 1. handoff and script surface

```bash
$ python3 -c import json, pathlib; required=['AGENTS.md','docs/CODEX_HANDOFF.md','docs/CODEX_START_HERE.md','package.json']; missing=[p for p in required if not pathlib.Path(p).exists()]; print('missing=' + ','.join(missing)); scripts=json.loads(pathlib.Path('package.json').read_text()).get('scripts',{}); print('validation_scripts=' + ','.join(k for k in sorted(scripts) if any(x in k for x in ['typecheck','lint','test','build','screenshots'])))
```

exit: `0`

```text
missing=
validation_scripts=build,lint,screenshots,test,typecheck
```
### 2. focused Paperclip/local-tools tests

```bash
$ pnpm --filter @enterprise-ai-hub/portal-web exec vitest run src/api/paperclipRuntime.test.ts src/api/localToolsRoute.test.ts --testTimeout 20000
```

exit: `0`

```text
RUN  v4.1.6 $PROJECT:enterprise/apps/portal-web


 Test Files  2 passed (2)
      Tests  12 passed (12)
   Start at  20:38:58
   Duration  3.19s (transform 1.61s, setup 3.60s, import 71ms, tests 159ms, environment 1.82s)
```

## Source / License

- 来源: `local-project:enterprise` plus command output shown above.
- 许可证 / license: this transcript records command outputs and safe structural evidence only; it does not redistribute private source bodies.

## Boundary / 风险边界

- This transcript proves the listed commands were executable and passed in this local workspace.
- It does not prove public adoption, GitHub stars, or every future task in the project.
- It is a redacted execution transcript, not a replacement for project-specific release gates.

## Forbidden / 禁止事项

- Do not copy secret, token, cookie, session, auth database, private key, browser profile, private config, database content, or private source body into a public case.
