# Source Depth Dossier

这份 dossier 专门回应“只抓 README 有什么用”。它不复写源码正文,只看公开仓库的树结构、验证入口和治理文件,把强项目的真实工作方式压成 ShipGrade CN 的可执行动作。

## Reading Rule

- README 只回答“项目想怎么介绍自己”。
- 代码树回答“项目真实如何维护、测试、协作、演进”。
- 本 skill 只吸收结构和工作法,不复制实现源码。

## High-Signal Repo Patterns

| repo | stars | shape | evidence | distilled move |
| --- | --- | --- | --- | --- |
| `cline/cline` | 62301 | src | **design**: `assets/docs/demo.gif`<br>`docs/api/authentication.mdx`<br>+18 more<br>**tests**: `.github/scripts/tests/coverage_check_test.py`<br>`.github/workflows/ext-jb-test-integration.yml`<br>+18 more<br>**ci**: `.github/CODEOWNERS`<br>`.github/ISSUE_TEMPLATE/bug_report.yml`<br>+18 more | 把测试作为产品骨架: agent 接手时先找最小 test/e2e/smoke,再动代码。 |
| `google-gemini/gemini-cli` | 104597 | packages | **design**: `docs/CONTRIBUTING.md`<br>`docs/admin/enterprise-controls.md`<br>+18 more<br>**tests**: `.gemini/commands/introspect.toml`<br>`.gemini/skills/docs-changelog/references/latest_template.md`<br>+18 more<br>**ci**: `.gemini/skills/ci/SKILL.md`<br>`.gemini/skills/ci/scripts/ci.mjs`<br>+18 more | 把测试作为产品骨架: agent 接手时先找最小 test/e2e/smoke,再动代码。 |
| `promptfoo/promptfoo` | 21585 | src | **design**: `architecture/layers.json`<br>`docs/agents/AGENTS.md`<br>+18 more<br>**tests**: `.github/workflows/tusk-test-runner-app-vitest-unit-tests.yml`<br>`.github/workflows/tusk-test-runner-vitest-unit-tests.yml`<br>+18 more<br>**ci**: `.github/AGENTS.md`<br>`.github/CODEOWNERS`<br>+18 more | 把测试作为产品骨架: agent 接手时先找最小 test/e2e/smoke,再动代码。 |
| `davila7/claude-code-templates` | 27561 | docs/rules | **design**: `cli-tool/components/commands/design/web-design-reviewer.md`<br>`cli-tool/components/skills/ai-research/loki-mode/docs/COMPETITIVE-ANALYSIS.md`<br>+18 more<br>**tests**: `.claude/commands/test.md`<br>`api/__tests__/endpoints.test.js`<br>+18 more<br>**ci**: `.github/CODEOWNERS`<br>`.github/WORKFLOWS_REFERENCE.md`<br>+14 more | 把评测作为质量语言: examples 给入口,evals/benchmarks 给专业验收。 |
| `run-llama/llama_index` | 49659 | docs/rules | **design**: `docs/.gitignore`<br>`docs/DOCS_README.md`<br>+18 more<br>**tests**: `.github/workflows/llama_dev_tests.yml`<br>`.github/workflows/unit_test.yml`<br>+18 more<br>**ci**: `.github/ISSUE_TEMPLATE/config.yml`<br>`.github/ISSUE_TEMPLATE/docs-form.yml`<br>+18 more | 把设计文档前置: 先读 motivation/alternatives/compatibility,再写实现。 |
| `Yeachan-Heo/oh-my-claudecode` | 34818 | src | **design**: `docs/AGENTS.md`<br>`docs/ARCHITECTURE.md`<br>+18 more<br>**tests**: `.github/workflows/upgrade-test.yml`<br>`agents/document-specialist.md`<br>+18 more<br>**ci**: `.github/CLAUDE.md`<br>`.github/FUNDING.yml`<br>+10 more | 把测试作为产品骨架: agent 接手时先找最小 test/e2e/smoke,再动代码。 |
| `confident-ai/deepeval` | 15687 | docs/rules | **design**: `docs/.gitignore`<br>`docs/README.md`<br>+18 more<br>**tests**: `.github/workflows/full_test_core_for_pr.yml`<br>`.github/workflows/test_confident.yml`<br>+18 more<br>**ci**: `.github/ISSUE_TEMPLATE/bug_report.md`<br>`.github/ISSUE_TEMPLATE/feature_request.md`<br>+8 more | 把测试作为产品骨架: agent 接手时先找最小 test/e2e/smoke,再动代码。 |
| `UKGovernmentBEIS/inspect_ai` | 2126 | src | **design**: `design/acp/agent-acp-tui.md`<br>`design/acp/agent-acp.md`<br>+18 more<br>**tests**: `.github/workflows/test.yml`<br>`docs/evals/inspect-evals.mk`<br>+18 more<br>**ci**: `.github/dependabot.yml`<br>`.github/pull_request_template.md`<br>+9 more | 把测试作为产品骨架: agent 接手时先找最小 test/e2e/smoke,再动代码。 |
| `crewAIInc/crewAI` | 52173 | lib | **design**: `docs/ar/api-reference/inputs.mdx`<br>`docs/ar/api-reference/introduction.mdx`<br>+18 more<br>**tests**: `.env.test`<br>`.github/workflows/generate-tool-specs.yml`<br>+18 more<br>**ci**: `.github/CONTRIBUTING.md`<br>`.github/ISSUE_TEMPLATE/bug_report.yml`<br>+18 more | 把设计文档前置: 先读 motivation/alternatives/compatibility,再写实现。 |
| `UKGovernmentBEIS/inspect_evals` | 511 | src | **design**: `adr/0001-eval-metadata-location.md`<br>`adr/0002-versioning-metadata.md`<br>+18 more<br>**tests**: `.claude/skills/ensure-test-coverage/references/test-patterns.md`<br>`.claude/skills/investigate-dataset/references/inspect-dataset-patterns.md`<br>+18 more<br>**ci**: `.github/ISSUE_TEMPLATE/bug_report.yaml`<br>`.github/ISSUE_TEMPLATE/new_benchmark.yaml`<br>+18 more | 把测试作为产品骨架: agent 接手时先找最小 test/e2e/smoke,再动代码。 |
| `sourcegraph/CodeScaleBench` | 24 | lib | **design**: `docs/EVAL_KIT.md`<br>`docs/analysis/compare/README.md`<br>+18 more<br>**tests**: `benchmarks/backups/csb_org_compliance/ccx-compliance-051/tests/eval.sh`<br>`benchmarks/backups/csb_org_compliance/ccx-compliance-051/tests/ground_truth_meta.json`<br>+18 more<br>**ci**: `.github/workflows/docs-consistency.yml`<br>`.github/workflows/repo_health.yml`<br>+2 more | 把设计文档前置: 先读 motivation/alternatives/compatibility,再写实现。 |
| `microsoft/skills` | 2385 | docs/rules | **design**: `.github/docs/agent-integration.md`<br>`.github/docs/blog.wordpress.xml`<br>+18 more<br>**tests**: `.github/plugins/azure-sdk-python/skills/azure-cosmos-db-py/assets/conftest_template.py`<br>`.github/plugins/azure-sdk-python/skills/azure-cosmos-db-py/references/testing.md`<br>+18 more<br>**ci**: `.github/CODEOWNERS`<br>`.github/agents/backend.agent.md`<br>+18 more | 把协作规则仓库化: CONTRIBUTING/SECURITY/OWNERS/agent rules 必须可发现。 |
| `affaan-m/ECC` | 192139 | src | **design**: `.kiro/docs/longform-guide.md`<br>`.kiro/docs/security-guide.md`<br>+18 more<br>**tests**: `.cursor/rules/common-testing.md`<br>`.cursor/rules/golang-testing.md`<br>+18 more<br>**ci**: `.github/CODEOWNERS`<br>`.github/FUNDING.yml`<br>+18 more | 把设计文档前置: 先读 motivation/alternatives/compatibility,再写实现。 |
| `openai/openai-agents-python` | 26641 | src | **design**: `docs/agents.md`<br>`docs/assets/images/favicon-platform.svg`<br>+18 more<br>**tests**: `.agents/skills/final-release-review/scripts/find_latest_release_tag.sh`<br>`.github/workflows/tests.yml`<br>+18 more<br>**ci**: `.github/ISSUE_TEMPLATE/bug_report.md`<br>`.github/ISSUE_TEMPLATE/feature_request.md`<br>+13 more | 把设计文档前置: 先读 motivation/alternatives/compatibility,再写实现。 |
| `sst/opencode` | 165176 | packages | **design**: `packages/console/app/src/routes/docs/[...path].ts`<br>`packages/console/app/src/routes/docs/index.ts`<br>+18 more<br>**tests**: `.github/workflows/test.yml`<br>`packages/app/create-effect-simplification-spec.md`<br>+18 more<br>**ci**: `.github/CODEOWNERS`<br>`.github/ISSUE_TEMPLATE/bug-report.yml`<br>+18 more | 把设计文档前置: 先读 motivation/alternatives/compatibility,再写实现。 |
| `alirezarezvani/claude-skills` | 16165 | docs/rules | **design**: `docs/agents/content-strategist.md`<br>`docs/agents/cs-aeo.md`<br>+18 more<br>**tests**: `.github/AUTOMATION_TEST.md`<br>`agents/marketing/cs-demand-gen-specialist.md`<br>+18 more<br>**ci**: `.github/AUTOMATION_SETUP.md`<br>`.github/AUTOMATION_TEST.md`<br>+18 more | 把设计文档前置: 先读 motivation/alternatives/compatibility,再写实现。 |
| `continuedev/continue` | 33376 | packages | **design**: `core/indexing/docs/DocsService.skip.ts`<br>`core/indexing/docs/DocsService.ts`<br>+18 more<br>**tests**: `.continue/agents/test-coverage.md`<br>`.continue/prompts/core-unit-test.prompt`<br>+18 more<br>**ci**: `.github/CODEOWNERS`<br>`.github/ISSUE_TEMPLATE/bug_report.yml`<br>+18 more | 把测试作为产品骨架: agent 接手时先找最小 test/e2e/smoke,再动代码。 |
| `openai/openai-cookbook` | 73775 | docs/rules | **design**: `examples/agents_sdk/deployment_manager/docs/screenshots/app-details.png`<br>`examples/agents_sdk/deployment_manager/docs/screenshots/deployments.png`<br>+4 more<br>**tests**: `examples/Function_calling_with_an_OpenAPI_spec.ipynb`<br>`examples/Unit_test_writing_using_a_multi-step_prompt.ipynb`<br>+18 more<br>**ci**: `.github/ISSUE_TEMPLATE/feature_request.md`<br>`.github/ISSUE_TEMPLATE/get-help.md`<br>+8 more | 把示例当作 onboarding: 小白先跑样例,高手再审边界。 |

## What Changed In ShipGrade CN

- 新增 `tools/shipgrade_init.py`: 不再只教你怎么做,而是直接给项目生成 `.shipgrade/` 工作台、Codex/Claude/Cursor 入口和验收模板。
- 新增 `demo/`: 让用户 3 分钟看到一次完整交付闭环,而不是读完理论再猜。
- 新增 `START_HERE.md`: 把小白入口、进阶闭环、专业审计入口放在第一屏。
- 保留 `tools/shipgrade_doctor.py`: 交付文档必须能被机器检查,不是靠一句“看起来不错”。

## Distilled Standards

- 强项目一定有可发现入口: README、agent rules、contributing/security、examples、tests/evals。
- 强项目一定有验证语言: unit/e2e/smoke/bench/eval 至少一种能跑。
- 强项目一定有治理边界: owner、security、license、CI、release/rollback。
- 强项目不是把所有流程写很重,而是让下一位人或 agent 不需要猜。

## Boundary

- stars 是发现信号,不是质量证明。
- 树结构是强证据,但仍不等于代码质量结论。
- 真正执行上游代码必须进入无密钥、可丢弃 sandbox。
