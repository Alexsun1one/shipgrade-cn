# First Run Demo

## 输入

用户说: “这个按钮点了没反应,你别讲道理,直接修好。”

## 执行

```bash
python3 tools/shipgrade_init.py /tmp/shipgrade-demo-project
```

生成:

- `/tmp/shipgrade-demo-project/.shipgrade/task-brief.md`
- `/tmp/shipgrade-demo-project/.shipgrade/quality-gate.md`
- `/tmp/shipgrade-demo-project/.shipgrade/handoff.md`
- `/tmp/shipgrade-demo-project/AGENTS.md`
- `/tmp/shipgrade-demo-project/CLAUDE.md`
- `/tmp/shipgrade-demo-project/.cursor/rules/shipgrade.mdc`

## 产物

把用户原话压成:

- 目标: 找到按钮无响应的最小原因并修复。
- 非目标: 不重构整页,不改设计系统。
- 验收: 测试或浏览器点击能证明按钮状态变化。
- 风险: 不覆盖未提交改动,不泄露 secret,验证跑不了要说明。

## 验收

```bash
python3 tools/shipgrade_doctor.py demo/demo-output.md
```

预期输出包含 `ship-grade-ok`。
