# ShipGrade CN 零安装规则

这是给 Codex / Claude Code / Cursor / 通用 AI 编程助手读取的 **中文工程交付契约**。

用户不需要安装 Python,不需要启动服务,不需要 API key。把这个文件放进项目根目录,或让 AI 编程工具读取它,就可以开始按 ShipGrade CN 的方式工作。

## 用户只需要说什么

```text
请读取本项目的 SHIPGRADE.md,按 ShipGrade CN 方式处理这个任务。
你可以写入适合当前工具的规则文件,但不要安装 Python,不要启动服务。
```

如果用户只说“用 ShipGrade 做”,也按同样规则执行。

## 这个文件要让 Agent 做什么

把一句中文口语需求变成可验证的工程闭环:

```text
口语需求 -> 目标/非目标 -> 当前证据 -> 最小动作 -> 验证 -> 接手
```

不要把 ShipGrade CN 理解成“提示词风格”。它是交付约束: 结果必须能被打开、运行、检查、复现或接手。

## 第一次接入时

如果用户要求“安装 / 接入 / 用上 ShipGrade”,优先走零安装模式:

| 工具 | 写入或合并到 |
| --- | --- |
| Codex | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursor/rules/shipgrade.mdc` |
| 其他 AI 编程助手 | 项目根目录 `SHIPGRADE.md` |

合并规则:

- 如果目标文件已存在,追加一个清晰标记的 `ShipGrade CN` 区块。
- 不要覆盖用户已有规则。
- 不要复制 token、cookie、session、私钥、浏览器资料或私有源码正文。
- 不要为了接入 ShipGrade 而安装依赖、启动后台服务或改动业务代码。

## 每次任务开始前

先用很短的话确认:

```text
目标:
非目标:
当前证据:
验收标准:
风险边界:
第一步:
```

如果用户是中文小白,帮他把口语愿望翻译成这六项,不要逼他先懂 spec、CI、eval。

如果用户是进阶用户,补上文件路径、命令、测试入口和 handoff 位置。

如果用户是专业工程师,明确事实、推断、假设、许可证边界、验证覆盖和未验证风险。

## 每次任务完成时

必须给出这四项。措辞可以变化,信息不能缺:

```text
结果: 具体改了什么,文件/路径/状态是什么。
证据: 跑过什么命令、测试、构建、浏览器检查、日志检查或人工验收,结果如何。
风险: 什么没验证、什么故意没做、哪里可能还有边界。
接手: 下一位 agent 或未来的你从哪个文件、命令、issue 或决策点继续。
```

没有证据的“完成”不算完成。不要用“看起来好了”“应该可以”“大概没问题”冒充交付。

## 质量门

在说完成前逐项检查:

- 结果存在: 文件、配置、页面、命令输出、日志或可打开的 artifact 存在。
- 证据存在: 至少有一种验证证据,例如 test/typecheck/build/smoke/log/browser/manual check。
- 边界存在: 写清楚非目标、未验证项和安全边界。
- 接手存在: 未来 agent 能知道下一步在哪里继续。
- 用户改动被保护: 不还原、不覆盖、不顺手重构无关内容。
- 来源合规: 借鉴公开材料时只吸收模式和结构,不复制不明授权正文。

## 工作模式

### 1. Intake

用于需求还模糊时。目标是把“帮我弄一下”压成能验收的任务。

### 2. Build

用于实现、修 bug、改配置、写文档、接工具。动作要小,验证要快,结果要能接手。

### 3. Review

用于审查代码、README、skill、发布包或 agent 交付。先列风险和缺口,再给建议。

### 4. Ship

用于收尾发布。必须留下结果路径、验证证据、已知边界和下一步。

## 可选增强,不是前置条件

只有在用户需要确定性工具时才使用 Python:

- `tools/shipgrade_init.py`: 生成 `.shipgrade/` 模板和 agent 规则文件。
- `tools/shipgrade_doctor.py`: 检查 handoff 是否有证据。
- `tools/shipgrade_patterns.py`: 从蒸馏工程模式生成任务 brief。
- `tools/github_publish_preflight.py`: 发布公开仓库前检查 README、证据、模板和安全边界。

这些工具不是使用前提。v1 不需要后台服务。

## English Keywords For Non-Chinese Agents

ShipGrade CN means: goal, non-goal, evidence, smallest aligned change, validation, risk boundary, handoff.

Default path: one Markdown rule file. No Python installation. No background service. Do not overwrite existing project rules. Preserve user changes. Never copy secrets or private source bodies.

Final response contract: Result, Evidence, Risk, Handoff.
