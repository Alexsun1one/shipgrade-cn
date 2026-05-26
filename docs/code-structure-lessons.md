# Code Structure Lessons

这份报告回应一个关键要求: 不能只抓 README。README 说明一个项目想让别人怎么看它,代码结构才暴露它长期怎么工作。

本分析不复制源码正文,而是扫描仓库树结构,提取以下信号:

- `src/pkg/lib/packages`: 代码组织是否稳定。
- `tests/evals/benchmarks`: 验证是否一等公民。
- `.github/workflows`: CI 和交付门槛是否仓库化。
- `docs/design/rfcs/adrs/keps/specification`: 设计前文档是否存在。
- `CONTRIBUTING/SECURITY/OWNERS/AGENTS/CLAUDE`: 治理、协作和 agent 规则是否可发现。
- `examples/samples`: 小白是否能从可运行样例进入。

## Snapshot

- source count: `103`
- analyzed repos: `88`

## Strong Structure Signals

| repo | score | signals | design | tests | ci | gov | eval |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `cline/cline` | 285 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible, source_roots_explicit | 127 | 624 | 24 | 35 | 44 |
| `google-gemini/gemini-cli` | 285 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible, source_roots_explicit | 124 | 1118 | 72 | 73 | 45 |
| `promptfoo/promptfoo` | 285 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible, source_roots_explicit | 576 | 1397 | 21 | 57 | 142 |
| `davila7/claude-code-templates` | 280 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible | 129 | 183 | 16 | 35 | 1004 |
| `run-llama/llama_index` | 280 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible | 1884 | 1670 | 21 | 203 | 93 |
| `Yeachan-Heo/oh-my-claudecode` | 278 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible, source_roots_explicit | 38 | 2741 | 12 | 27 | 80 |
| `confident-ai/deepeval` | 275 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible | 522 | 677 | 10 | 11 | 127 |
| `UKGovernmentBEIS/inspect_ai` | 273 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible, source_roots_explicit | 200 | 626 | 11 | 17 | 16 |
| `crewAIInc/crewAI` | 273 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible, source_roots_explicit | 1234 | 958 | 21 | 22 | 30 |
| `UKGovernmentBEIS/inspect_evals` | 266 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible, source_roots_explicit | 48 | 660 | 49 | 54 | 202 |
| `sourcegraph/CodeScaleBench` | 248 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible, source_roots_explicit | 21068 | 9052 | 4 | 125 | 13936 |
| `microsoft/skills` | 235 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible | 20 | 310 | 1012 | 1014 | 21 |
| `affaan-m/ECC` | 234 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible, source_roots_explicit | 1357 | 267 | 47 | 55 | 3 |
| `openai/openai-agents-python` | 225 | design_docs, tests_visible, ci_visible, governance_visible, examples_visible, source_roots_explicit | 399 | 282 | 15 | 18 | 0 |
| `sst/opencode` | 219 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible, source_roots_explicit | 637 | 585 | 36 | 48 | 3 |
| `alirezarezvani/claude-skills` | 209 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible | 520 | 60 | 22 | 44 | 2 |
| `continuedev/continue` | 208 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, source_roots_explicit | 518 | 604 | 48 | 54 | 1 |
| `openai/openai-cookbook` | 208 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible | 6 | 68 | 10 | 13 | 97 |
| `github/awesome-copilot` | 207 | design_docs, tests_visible, ci_visible, governance_visible, examples_visible | 31 | 43 | 108 | 46 | 0 |
| `gsd-build/gsd-2` | 206 | design_docs, tests_visible, ci_visible, governance_visible, examples_visible, source_roots_explicit | 220 | 1323 | 23 | 26 | 0 |
| `SuperClaude-Org/SuperClaude_Framework` | 202 | design_docs, tests_visible, ci_visible, governance_visible, examples_visible, source_roots_explicit | 126 | 34 | 8 | 15 | 0 |
| `langchain-ai/langgraph` | 202 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible | 15 | 169 | 27 | 29 | 9 |
| `gsd-build/get-shit-done` | 200 | design_docs, tests_visible, ci_visible, governance_visible | 116 | 747 | 33 | 42 | 0 |
| `github/spec-kit` | 196 | design_docs, tests_visible, ci_visible, governance_visible, source_roots_explicit | 27 | 99 | 24 | 31 | 0 |
| `openai/evals` | 184 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible | 6 | 57 | 8 | 9 | 1687 |
| `google/googletest` | 182 | design_docs, tests_visible, ci_visible, governance_visible, examples_visible | 26 | 170 | 6 | 4 | 0 |
| `microsoft/code-with-engineering-playbook` | 173 | design_docs, tests_visible, ci_visible, governance_visible, examples_visible | 358 | 22 | 6 | 8 | 0 |
| `anthropics/anthropic-cookbook` | 172 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible | 2 | 27 | 18 | 25 | 45 |
| `anthropics/claude-cookbooks` | 172 | design_docs, tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible | 2 | 27 | 18 | 25 | 45 |
| `Mathews-Tom/armory` | 170 | tests_visible, ci_visible, governance_visible, bench_or_eval_visible, examples_visible | 0 | 27 | 12 | 14 | 132 |

## 蒸馏出的规律

- 强仓库不是只有漂亮 README; 它们把代码、测试、CI、设计文档、治理文件和示例放在 agent 能自动发现的位置。
- 设计文档强的项目会留下动机、替代方案、兼容性、迁移/回滚、未决问题和 owner。
- 代码规范强的项目会把 review 口径、API 设计、错误语义、测试策略写成可复用文件。
- Agent/LLM 项目强的标志是 examples 与 evals 并存: examples 降低小白门槛, evals 支撑专业验收。
- 中文团队版本要把这些压成轻量 RFC、ADR、quality gate、repo doctor 和 handoff,不能搬运源码。

## Selective Runtime Audit

“把代码拉下来跑”只对一部分仓库有价值。本项目新增 selective runtime lane: 先按许可证白名单 shallow/sparse clone,只拉 README/docs/tests/evals/src/package metadata; 再做 no-install 静态 smoke; 真正执行 tests/examples 必须进无密钥、可丢弃 sandbox。

| repo | tier | files | source | tests | evals | safe_smoke |
| --- | --- | --- | --- | --- | --- | --- |
| `github/spec-kit` | runtime_candidate | 319 | 69 | 87 | 0 | yes |
| `microsoft/code-with-engineering-playbook` | runtime_candidate | 391 | 0 | 61 | 1 | no |
| `humanlayer/12-factor-agents` | runtime_candidate | 499 | 152 | 23 | 0 | no |
| `promptfoo/promptfoo` | runtime_candidate | 5248 | 1835 | 1452 | 509 | yes |
| `UKGovernmentBEIS/inspect_ai` | runtime_candidate | 1725 | 845 | 579 | 104 | yes |
| `vercel-labs/skills` | skipped | 0 | 0 | 0 | 0 | no |
| `SuperClaude-Org/SuperClaude_Framework` | runtime_candidate | 409 | 122 | 30 | 0 | yes |
| `Yeachan-Heo/oh-my-claudecode` | runtime_candidate | 5621 | 1207 | 2735 | 83 | yes |

## Known Boundary / 已知边界

- 本报告只分析仓库树结构和公开文件路径,不证明代码质量一定高。
- Runtime audit 只证明仓库具备可继续运行验证的结构信号,不等于已安全执行所有代码。
- Runtime smoke evidence 记录低副作用检查的 exit code,用于学习命令拓扑和验证面,不冒充完整测试通过。
- `tree_truncated=true` 的仓库只适合作为结构信号,不能当作完整计数。
- 许可证不清、metadata-only 或私有来源不进入正文抽取。

## Forbidden

- 不复制 secret/token/cookie/session/auth/private key。
- 不吸收泄漏源码或系统提示词归档。
- 不把 stars、README 文案或目录规模当成最终质量证明。
