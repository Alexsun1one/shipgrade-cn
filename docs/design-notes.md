# Design Notes

## 为什么这是一个 skill,不是提示词

提示词通常只影响一次回答。本 skill 约束的是完整工程行为:

- 如何定义目标。
- 如何选择上下文。
- 如何拆最小闭环。
- 如何验证。
- 如何写回。
- 如何让其他 agent 接手。

## 蒸馏方法

来源被分成几类:

- spec-driven: 需求、计划、任务和验收。
- agent rules: AGENTS/CLAUDE/Cursor/Copilot 规则。
- engineering practice: review、style、test、可维护性。
- context engineering: 记忆、上下文选择、handoff。
- ML training: 数据、训练、探针、实验记录。
- SRE/security: 长期运行、安全边界、恢复。

本 skill 不复写来源正文,只吸收工程结构和质量门槛。

## 三层用户设计

- 小白层: 给一句话入口和可填模板,避免一上来讲抽象方法论。
- 进阶层: 给黄金闭环、doctor、quality gate,让用户能自检。
- 专业层: 给 influence map、overlap decisions、source attribution、eval JSONL,让高手能审计并继续改。

## 为什么要中文化改造

很多英文资料默认用户已经熟悉 GitHub、CI、英文 issue、许可证和 review 文化。中文团队常见问题不同: 需求口语化、证据意识弱、多端机器混用、网络慢、知识沉淀分散、协作工具不统一。

所以本 skill 不是直译,而是把强实践压成: 中文可验收模板、最小验证、Obsidian/项目写回、多 agent handoff、国内网络和 Windows/Mac 混合边界。

## 取舍

吸收:

- 可验证流程。
- 输入/输出契约。
- 失败模式。
- 来源和许可证边界。

丢弃:

- persona 堆叠。
- 神奇效率承诺。
- 高星即权威。
- 泄漏/私有/许可证不清正文。
