# Overlap Decisions

本报告回答用户真正关心的问题: 不是把很多高星项目粘到一起,而是找它们反复重合的强信号,重复处合并,冲突处取舍,缺口处为中文团队补齐。

## Snapshot

- source count: `103`
- artifact count: `128`
- overlap themes: `12`

## 合并规则

- 多个来源都强调的内容: 收敛成黄金闭环和质量门槛。
- 只有少数高手项目强调、但对中文团队关键的内容: 保留为硬边界或模板。
- 只适合英文/大厂/成熟 CI 的内容: 改写成小团队可执行版本。
- 许可证不清或 metadata-only 来源: 只保留发现信号,不吸收正文。

## Core Merge Table

| 重合主题 | 命中仓库数 | 处理方式 | 代表来源 |
| --- | --- | --- | --- |
| 上线、监控、恢复和长期运行是交付的一部分 | 72 | 合并进 Ship mode,把上线和恢复视为交付一部分。 | sst/opencode, airbnb/javascript, Shubhamsaboo/awesome-llm-apps, microsoft/generative-ai-for-beginners, mattpocock/skills, google-gemini/gemini-cli |
| 工具调用必须可安装、可验收、可回滚 | 69 | 合并成工具可安装、可验收、可回滚原则。 | sst/opencode, airbnb/javascript, Shubhamsaboo/awesome-llm-apps, microsoft/generative-ai-for-beginners, mattpocock/skills, google-gemini/gemini-cli |
| 先把愿望压成可验收规格 | 64 | 合并进黄金闭环第 1 步: 先定义可验收结果。 | sst/opencode, airbnb/javascript, Shubhamsaboo/awesome-llm-apps, microsoft/generative-ai-for-beginners, mattpocock/skills, google-gemini/gemini-cli |
| 用测试、评测、日志和探针证明完成 | 63 | 合并进黄金闭环第 4 步和 Done Means Evidence。 | sst/opencode, airbnb/javascript, Shubhamsaboo/awesome-llm-apps, microsoft/generative-ai-for-beginners, mattpocock/skills, google-gemini/gemini-cli |
| 代码审查和可维护性是默认门槛 | 59 | 合并成 Review mode 和质量门槛。 | sst/opencode, airbnb/javascript, Shubhamsaboo/awesome-llm-apps, microsoft/generative-ai-for-beginners, mattpocock/skills, google-gemini/gemini-cli |
| 上下文工程比单次提示词更重要 | 58 | 合并进找证据和写回,避免只靠一次提示词。 | airbnb/javascript, Shubhamsaboo/awesome-llm-apps, microsoft/generative-ai-for-beginners, mattpocock/skills, google-gemini/gemini-cli, browser-use/browser-use |
| secret、私有数据、许可证和供应链风险必须前置 | 57 | 前置为硬 gate,不进入普通建议流。 | sst/opencode, airbnb/javascript, Shubhamsaboo/awesome-llm-apps, microsoft/generative-ai-for-beginners, mattpocock/skills, google-gemini/gemini-cli |
| 多 agent 需要主控、分工、合并和证据 | 56 | 合并成主控/worker/本地 adapter 三层分工。 | sst/opencode, Shubhamsaboo/awesome-llm-apps, microsoft/generative-ai-for-beginners, mattpocock/skills, google-gemini/gemini-cli, browser-use/browser-use |
| 把 agent 行为写成仓库规则而不是口头约定 | 53 | 合并成 AGENTS/CLAUDE/Cursor 三入口规则。 | airbnb/javascript, microsoft/generative-ai-for-beginners, google-gemini/gemini-cli, browser-use/browser-use, dair-ai/Prompt-Engineering-Guide, cline/cline |
| 训练要保留数据、配置、指标、探针和失败记录 | 50 | 合并为训练实验模板和坏 run 不算成果。 | sst/opencode, Shubhamsaboo/awesome-llm-apps, microsoft/generative-ai-for-beginners, mattpocock/skills, google-gemini/gemini-cli, browser-use/browser-use |
| 小步迭代,每步都能回滚和验证 | 48 | 合并成最小可验证 slice,丢弃大而全计划。 | sst/opencode, airbnb/javascript, Shubhamsaboo/awesome-llm-apps, microsoft/generative-ai-for-beginners, mattpocock/skills, browser-use/browser-use |
| 关键判断保留人工/强模型复核 | 44 | 保留为强模型/人工最终判断,本地 adapter 不当老师。 | airbnb/javascript, Shubhamsaboo/awesome-llm-apps, browser-use/browser-use, cline/cline, crewAIInc/crewAI, Fission-AI/OpenSpec |
