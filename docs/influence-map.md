# Influence Map

这份 skill 明确吸收世界级工程实践,但不崇拜名人或 stars。判断标准是: 是否能让真实交付更可验收、可复盘、可迁移。

## 面向谁

| 用户 | 能得到什么 | 入口 |
| --- | --- | --- |
| 中文小白 | 只要能说清目标、上下文、验收,就能用模板把任务交给 agent,避免陷入 prompt 玄学。 | 从 README 的一分钟上手和 templates/task-brief.md 开始。 |
| 进阶用户 | 能把需求、实现、验证、复盘串成闭环,并用 doctor/evals 检查交付是否缺证据。 | 使用 SKILL.md 的黄金闭环、templates/quality-gate.md 和 tools/shipgrade_doctor.py。 |
| 专业工程师 | 能看到来源归因、重合点压缩、许可证边界、eval 任务和多 agent 接手契约,可审计、可 fork、可持续改进。 | 审查 docs/influence-map.md、docs/overlap-decisions.md、docs/source-attribution.md 和 evals/ship_grade_eval.jsonl。 |

## 吸收与改造

| 人物/项目 | 为什么强 | 吸收了什么 | 为什么要改 | 来源边界 |
| --- | --- | --- | --- | --- |
| Andrej Karpathy | 把复杂模型训练拆成可读、可跑、可复现实验,强调少魔法、强反馈、保留指标和探针。 | 训练不只看 loss,必须保留数据、run config、metrics、probes 和失败记录。 | 改成中文团队能执行的训练交付模板,并明确小模型只是路由/检查/草稿层,不当最终老师。 | karpathy/nanoGPT: MIT / allow_extract<br>karpathy/llm.c: MIT / allow_extract<br>karpathy/minGPT: MIT / allow_extract |
| Google Engineering Practices / Styleguide | 把代码审查、可维护性、风格一致性变成团队制度,不是靠个人感觉。 | Review mode、质量门槛、事实/推断/假设分离、可维护性优先。 | 保留 CC-BY 归因边界,把英文 review 文化压成中文可执行清单和最终交付证据。 | google/eng-practices: CC-BY-3.0 / attribution_review<br>google/styleguide: CC-BY-3.0 / attribution_review |
| GitHub Spec Kit / OpenSpec / Agent OS | 把 AI 编程从一句话生成拉回 spec、计划、任务、验收的工程轨道。 | 先把愿望压成可验收目标,再做最小 slice,最后用证据收口。 | 去掉重型流程感,保留小白也能填的目标/非目标/验收/风险四格。 | github/spec-kit: MIT / allow_extract<br>Fission-AI/OpenSpec: MIT / allow_extract<br>buildermethods/agent-os: MIT / allow_extract |
| Matt Pocock / Real Engineer Skills | 面向真实工程师的技能组织方式,强调可读、可迁移、能直接改变工程动作。 | skill 要像专业 onboarding,而不是提示词堆叠。 | 加入中文解释、工具边界、国内网络/多机器/Windows+Mac 工作流。 | mattpocock/skills: MIT / allow_extract |
| OpenAI / Anthropic Cookbooks | 大量可运行 recipe 和 eval 思维,适合把 AI 产品能力落到测试和样例。 | 把提示词、agent、工具调用都绑定到 eval、样例和失败模式。 | 把 cookbook 式样例改成中文交付模板,强调复核、来源和许可证。 | openai/openai-cookbook: MIT / allow_extract<br>anthropics/claude-cookbooks: MIT / allow_extract<br>anthropics/anthropic-cookbook: MIT / allow_extract |
| Promptfoo / DeepEval | 把 LLM 输出质量变成可评测对象,不靠主观一句'效果不错'。 | 每个 skill 都要有 eval 任务、must_include 和 doctor 检查。 | 把评测降到仓库内 JSONL 和 Python doctor,小团队也能跑。 | promptfoo/promptfoo: MIT / allow_extract<br>confident-ai/deepeval: Apache-2.0 / allow_extract |
| Modern Coding Agents | 代表真实用户正在使用的 agent 产品形态: CLI、IDE、浏览器、工具调用和长任务。 | 多入口规则、工具可验收、浏览器/终端证据、长期任务 handoff。 | 适配 Codex/Claude/Cursor 共存,并加入不要复制 auth、sessions、cookie、私钥的硬边界。 | sst/opencode: MIT / allow_extract<br>google-gemini/gemini-cli: Apache-2.0 / allow_extract<br>cline/cline: Apache-2.0 / allow_extract<br>continuedev/continue: Apache-2.0 / allow_extract<br>browser-use/browser-use: MIT / allow_extract |
| Context Engineering / Agent Skill Frameworks | 把上下文、规则、记忆、hook、技能库组织成系统,不是单轮提示词。 | 找证据、写回、跨 agent handoff、技能可安装可审计。 | 加入 Obsidian/中文工作日志/局域网 worker/国内网络慢等真实团队约束。 | coleam00/context-engineering-intro: MIT / allow_extract<br>addyosmani/agent-skills: MIT / allow_extract<br>obra/superpowers: MIT / allow_extract<br>affaan-m/ECC: MIT / allow_extract |
| Design-First Engineering Repos | 这些项目把设计、提案、阶段门、ADR、兼容性和稳定性写成长期制度。 | 轻量 RFC、ADR、stage gate、owner、兼容/迁移/回滚/未决问题。 | 改成中文团队能承担的三档文档: 小改动 brief、中等变更 RFC、重大变更 ADR/上线门。 | microsoft/code-with-engineering-playbook: CC-BY-4.0 / attribution_review<br>golang/proposal: BSD-3-Clause / allow_extract<br>rust-lang/rfcs: Apache-2.0 / allow_extract<br>kubernetes/enhancements: Apache-2.0 / allow_extract<br>open-telemetry/opentelemetry-specification: Apache-2.0 / allow_extract<br>adr/madr: MIT OR CC0-1.0 / allow_extract |
| Agent And SWE Evaluation Benchmarks | 把 agent 能力放进真实任务、工具调用、可复现评测和 verifier 里。 | eval/task/scorer 分离、工具/沙箱边界、真实仓库任务、可审计快照。 | 改成 skill 评测三档: 小白入口是否可用、进阶闭环是否完整、专业验收是否有 verifier。 | UKGovernmentBEIS/inspect_ai: MIT / allow_extract<br>UKGovernmentBEIS/inspect_evals: MIT / allow_extract<br>openai/evals: MIT / allow_extract<br>sierra-research/tau2-bench: MIT / allow_extract<br>SWE-bench/SWE-bench: MIT / allow_extract<br>sourcegraph/CodeScaleBench: Apache-2.0 / allow_extract |

## 关键改造原则

- 英文项目多默认成熟 OSS/CI/英文团队语境; 本 skill 改成中文验收、中文复盘和国内网络现实。
- 高手实践往往隐含经验门槛; 本 skill 把它们压成小白能填的模板,同时保留专业用户可审计的 provenance/evals。
- GitHub stars 只作为发现信号,不作为质量或许可证证明。
- 本地小模型/LoRA adapter 只能做路由、草稿、缺项检查; 最终判断仍由强模型/人工和验证证据承担。
