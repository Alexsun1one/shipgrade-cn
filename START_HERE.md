# Start Here

ShipGrade CN 是一套中文工程 skill,目标是让 AI 编程从“会回答”进入“能交付、能验证、能接手”。

## 3 分钟真实首用链路

```bash
python3 tools/shipgrade_demo.py
python3 tools/shipgrade_init.py /tmp/shipgrade-demo-project
sed -n '1,120p' /tmp/shipgrade-demo-project/.shipgrade/task-brief.md
sed -n '1,120p' /tmp/shipgrade-demo-project/AGENTS.md
python3 tools/shipgrade_doctor.py demo/demo-output.md
```

这条链路会证明三件事:

- 项目里真的生成 `.shipgrade/` 工作台。
- `AGENTS.md` / `CLAUDE.md` 被接线,后续 agent 会看到规则。
- `shipgrade_doctor.py` 不只看关键词,会拒绝没有命令/浏览器证据的假完成,也会接受合格 handoff。

## 你是哪类用户

| 你是谁 | 先打开 | 你要做什么 |
| --- | --- | --- |
| 中文小白 | `demo/demo-task.md` | 照着填目标、非目标、验收和风险。 |
| 进阶用户 | `tools/shipgrade_init.py` | 给当前项目生成 `.shipgrade/` 工作台。 |
| 专业工程师 | `docs/source-depth-dossier.md` + `docs/deep-code-case-studies.md` | 审计来源结构、验证门槛、命令拓扑和取舍。 |

## 不是计划

这个包必须提供可打开的 artifact:

- agent 入口: `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, `cursor-rules.mdc`
- 可填模板: `templates/`
- 可跑工具: `tools/shipgrade_demo.py`, `tools/shipgrade_init.py`, `tools/shipgrade_doctor.py`
- 可审证据: `QUALITY_REPORT.md`, `manifest.json`, `docs/transcript-evidence.md`
- 可继续深挖: `docs/source-depth-dossier.md`, `docs/deep-code-case-studies.md`, `docs/source-attribution.md`

## 最重要的一句话

没有验证证据的“完成”不算完成;没有接手入口的“聪明”不算工程。
