# Deep Code Case Studies

Generated: 2026-05-26T00:49:43Z

This report is the deeper pass after README and tree scans. It reads public, license-reviewed runtime/promotion clones and extracts command topology, workflow shape, test anatomy, agent surfaces, skill architecture, doc taxonomy, and code-symbol counts without copying source bodies.

## Summary

- case studies: `11`
- total files inspected: `17649`
- total tests/evals paths: `5381` / `786`
- total skill files inspected: `313`
- public boundary: `Public, license-reviewed runtime/promotion clones only; source bodies are not copied into the report.`

| repo | files | src | tests | evals | workflows | package scripts | agent surface | skill architecture | distilled signal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `SuperClaude-Org/SuperClaude_Framework` | 409 | 31 | 30 | 0 | 5 | 4 | 259 | 1 | 把 skill frontmatter、触发条件和验证清单当作可安装协作界面,而不是普通 Markdown。 |
| `UKGovernmentBEIS/inspect_ai` | 1725 | 776 | 579 | 104 | 9 | 0 | 257 | 0 | 把 CI/workflow 里的真实 job 名称反写到本地 quality gate,避免本地验收和远端脱节。 |
| `VoltAgent/awesome-agent-skills` | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 当前仓库主要提供结构 radar: 先识别验证入口,再决定是否进入 sandbox。 |
| `Yeachan-Heo/oh-my-claudecode` | 5621 | 1047 | 2735 | 83 | 7 | 32 | 1961 | 39 | 把 Skill / Persona / Command 分层: skill 管 how, persona 管 who, command 管 when,避免大而全的混合提示词。 |
| `addyosmani/agent-skills` | 77 | 0 | 9 | 0 | 1 | 0 | 61 | 23 | 把 Skill / Persona / Command 分层: skill 管 how, persona 管 who, command 管 when,避免大而全的混合提示词。 |
| `affaan-m/ECC` | 2870 | 19 | 302 | 85 | 8 | 30 | 2000 | 246 | 把 Skill / Persona / Command 分层: skill 管 how, persona 管 who, command 管 when,避免大而全的混合提示词。 |
| `browser-use/browser-use` | 486 | 0 | 104 | 4 | 10 | 0 | 78 | 4 | 把 skill frontmatter、触发条件和验证清单当作可安装协作界面,而不是普通 Markdown。 |
| `github/spec-kit` | 319 | 69 | 87 | 0 | 10 | 0 | 43 | 0 | 把 CI/workflow 里的真实 job 名称反写到本地 quality gate,避免本地验收和远端脱节。 |
| `humanlayer/12-factor-agents` | 499 | 15 | 22 | 0 | 0 | 9 | 146 | 0 | 先读取 package scripts 再决定命令,不要凭经验猜 npm/pnpm/yarn gate。 |
| `microsoft/code-with-engineering-playbook` | 391 | 0 | 61 | 1 | 2 | 0 | 1 | 0 | 把 CI/workflow 里的真实 job 名称反写到本地 quality gate,避免本地验收和远端脱节。 |
| `promptfoo/promptfoo` | 5248 | 1528 | 1452 | 509 | 11 | 15 | 615 | 0 | 把 CI/workflow 里的真实 job 名称反写到本地 quality gate,避免本地验收和远端脱节。 |

## Case Notes

### SuperClaude-Org/SuperClaude_Framework

- source lane: `runtime_repo_audit`; runtime tier: `runtime_candidate`; license: `MIT`; stars snapshot: `22982`
- line anatomy: source `4646`, tests `3396`, docs `61580`
- doc taxonomy: `{"design": 14, "governance": 4, "onboarding": 2, "reference": 107, "validation": 13}`
- workflow command hits: `['cargo', 'npm', 'pytest', 'ruff']`
- Python symbols: `{'files_sampled': 45, 'classes': 34, 'functions': 272, 'test_functions': 136, 'parse_errors': 0, 'sample_paths': ['scripts/ab_test_workflows.py', 'src/superclaude/__init__.py', 'src/superclaude/__version__.py', 'src/superclaude/agents/__init__.py', 'src/superclaude/cli/__init__.py', 'src/superclaude/cli/doctor.py', 'src/superclaude/cli/install_commands.py', 'src/superclaude/cli/install_mcp.py', 'src/superclaude/cli/install_skill.py', 'src/superclaude/cli/main.py']}`
- JS/TS symbols: `{'files_sampled': 1, 'export_symbols': 4, 'describe_blocks': 0, 'test_blocks': 0, 'sample_paths': ['src/superclaude/skills/confidence-check/confidence.ts']}`
- agent surfaces: `{'surface_count': 259, 'buckets': {'claude': 222, 'skills': 20, 'agents': 66, 'commands': 71, 'hooks': 4}, 'sample_paths': ['.claude/settings.json', '.claude/skills/confidence-check/SKILL.md', '.claude/skills/confidence-check/confidence.ts', 'AGENTS.md', 'CLAUDE.md', 'docs/Development/pm-agent-ideal-workflow.md', 'docs/Development/pm-agent-integration.md', 'docs/agents/pm-agent-guide.md', 'docs/architecture/PM_AGENT_COMPARISON.md', 'docs/architecture/SKILLS_CLEANUP.md', 'docs/architecture/pm-agent-auto-activation.md', 'docs/architecture/pm-agent-responsibility-cleanup.md', 'docs/mcp/mcp-integration-policy.md', 'docs/mcp/mcp-optional-design.md', 'docs/pm-agent-implementation-status.md', 'docs/reference/claude-code-history-management.md', 'docs/reference/commands-list.md', 'docs/reference/mcp-server-guide.md', 'docs/reference/pm-agent-autonomous-reflection.md', 'docs/reference/suggested-commands.md', 'docs/research/complete-python-skills-migration.md', 'docs/research/llm-agent-token-efficiency-2025.md', 'docs/research/mcp-installer-fix-summary.md', 'docs/research/pm-skills-migration-results.md']}`
- skill architecture: `{'skill_count': 1, 'skill_frontmatter_count': 1, 'skill_frontmatter_with_description': 1, 'skill_frontmatter_with_use_when': 0, 'claude_command_count': 0, 'gemini_command_count': 0, 'persona_count': 0, 'hook_file_count': 0, 'setup_doc_count': 0, 'reference_doc_count': 0, 'harness_surface_count': 2, 'command_lifecycle': [], 'sample_skill_paths': ['skills/confidence-check/SKILL.md'], 'sample_command_paths': [], 'sample_persona_paths': [], 'setup_docs': [], 'orchestration_signals': []}`

Distilled moves:
- 把 skill frontmatter、触发条件和验证清单当作可安装协作界面,而不是普通 Markdown。
- 把 CI/workflow 里的真实 job 名称反写到本地 quality gate,避免本地验收和远端脱节。
- 先读取 package scripts 再决定命令,不要凭经验猜 npm/pnpm/yarn gate。
- 把 pyproject 的 pytest/ruff/mypy/coverage 配置当成 Python 项目的验证入口。
- 把 AGENTS/CLAUDE/Cursor/skills/hooks 视为一等协作界面,纳入 handoff。

### UKGovernmentBEIS/inspect_ai

- source lane: `runtime_repo_audit`; runtime tier: `runtime_candidate`; license: `MIT`; stars snapshot: `2126`
- line anatomy: source `201939`, tests `148814`, docs `1716`
- doc taxonomy: `{"design": 25, "governance": 1, "onboarding": 15, "reference": 28, "validation": 8}`
- workflow command hits: `['mypy', 'npm', 'pnpm', 'pytest', 'ruff', 'yarn']`
- Python symbols: `{'files_sampled': 80, 'classes': 97, 'functions': 783, 'test_functions': 0, 'parse_errors': 0, 'sample_paths': ['src/inspect_ai/__init__.py', 'src/inspect_ai/__main__.py', 'src/inspect_ai/_cli/_scanner.py', 'src/inspect_ai/_cli/acp.py', 'src/inspect_ai/_cli/cache.py', 'src/inspect_ai/_cli/common.py', 'src/inspect_ai/_cli/download.py', 'src/inspect_ai/_cli/eval.py', 'src/inspect_ai/_cli/info.py', 'src/inspect_ai/_cli/list.py']}`
- JS/TS symbols: `{'files_sampled': 7, 'export_symbols': 0, 'describe_blocks': 0, 'test_blocks': 19, 'sample_paths': ['src/inspect_ai/_view/dist/assets/chunk-DfAF0w94.js', 'src/inspect_ai/_view/dist/assets/index.js', 'src/inspect_ai/_view/dist/assets/lib-CBtriEt5.js', 'src/inspect_ai/_view/dist/assets/liteDOM-Cp0aN3bP.js', 'src/inspect_ai/_view/dist/assets/tex-svg-full-BI3fonbT.js', 'src/inspect_ai/_view/dist/assets/wgxpath.install-node-Csk64Aj9.js', 'src/inspect_ai/_view/dist/assets/xypic-DrMJn58R.js']}`
- agent surfaces: `{'surface_count': 257, 'buckets': {'claude': 5, 'agents': 192, 'commands': 9, 'hooks': 18, 'skills': 14, 'cursor': 1}, 'sample_paths': ['CLAUDE.md', 'design/acp/agent-acp-tui.md', 'design/acp/agent-acp.md', 'design/deepagents.md', 'docs/_agent_limits.md', 'docs/_extensions/meridianlabs-ai/inspect-docs/filters/reference/commands.py', 'docs/agent-bridge.qmd', 'docs/agent-custom.qmd', 'docs/agents.qmd', 'docs/deepagent.qmd', 'docs/human-agent.qmd', 'docs/images/inspect-human-agent-container.png', 'docs/images/inspect-human-agent.png', 'docs/multi-agent.qmd', 'docs/react-agent.qmd', 'docs/reference/inspect_ai.agent.qmd', 'docs/reference/inspect_ai.hooks.qmd', 'docs/tools-mcp.qmd', 'examples/bridge/agentsdk/README.md', 'examples/bridge/agentsdk/agent.py', 'examples/bridge/agentsdk/dataset.json', 'examples/bridge/agentsdk/task.py', 'examples/bridge/langchain/agent.py', 'examples/bridge/pydantic-ai/agent.py']}`
- skill architecture: `{'skill_count': 0, 'skill_frontmatter_count': 0, 'skill_frontmatter_with_description': 0, 'skill_frontmatter_with_use_when': 0, 'claude_command_count': 0, 'gemini_command_count': 0, 'persona_count': 0, 'hook_file_count': 0, 'setup_doc_count': 0, 'reference_doc_count': 0, 'harness_surface_count': 1, 'command_lifecycle': [], 'sample_skill_paths': [], 'sample_command_paths': [], 'sample_persona_paths': [], 'setup_docs': [], 'orchestration_signals': []}`

Distilled moves:
- 把 CI/workflow 里的真实 job 名称反写到本地 quality gate,避免本地验收和远端脱节。
- 先读取 package scripts 再决定命令,不要凭经验猜 npm/pnpm/yarn gate。
- 把 pyproject 的 pytest/ruff/mypy/coverage 配置当成 Python 项目的验证入口。
- 把 AGENTS/CLAUDE/Cursor/skills/hooks 视为一等协作界面,纳入 handoff。
- 设计文档不是装饰: brief/RFC/ADR 要把 motivation、alternatives、rollout 和 unresolved 写清。

### VoltAgent/awesome-agent-skills

- source lane: `source_promotion_batch`; runtime tier: `docs_or_metadata_candidate`; license: `MIT`; stars snapshot: `23080`
- line anatomy: source `0`, tests `0`, docs `1768`
- doc taxonomy: `{"governance": 1, "reference": 1}`
- workflow command hits: `[]`
- Python symbols: `{'files_sampled': 0, 'classes': 0, 'functions': 0, 'test_functions': 0, 'parse_errors': 0, 'sample_paths': []}`
- JS/TS symbols: `{'files_sampled': 0, 'export_symbols': 0, 'describe_blocks': 0, 'test_blocks': 0, 'sample_paths': []}`
- agent surfaces: `{'surface_count': 0, 'buckets': {}, 'sample_paths': []}`
- skill architecture: `{'skill_count': 0, 'skill_frontmatter_count': 0, 'skill_frontmatter_with_description': 0, 'skill_frontmatter_with_use_when': 0, 'claude_command_count': 0, 'gemini_command_count': 0, 'persona_count': 0, 'hook_file_count': 0, 'setup_doc_count': 0, 'reference_doc_count': 0, 'harness_surface_count': 0, 'command_lifecycle': [], 'sample_skill_paths': [], 'sample_command_paths': [], 'sample_persona_paths': [], 'setup_docs': [], 'orchestration_signals': []}`

Distilled moves:
- 当前仓库主要提供结构 radar: 先识别验证入口,再决定是否进入 sandbox。

### Yeachan-Heo/oh-my-claudecode

- source lane: `runtime_repo_audit`; runtime tier: `runtime_candidate`; license: `MIT`; stars snapshot: `34818`
- line anatomy: source `141866`, tests `172347`, docs `35835`
- doc taxonomy: `{"design": 9, "governance": 3, "reference": 103, "validation": 25}`
- workflow command hits: `['npm']`
- Python symbols: `{'files_sampled': 0, 'classes': 0, 'functions': 0, 'test_functions': 0, 'parse_errors': 0, 'sample_paths': []}`
- JS/TS symbols: `{'files_sampled': 90, 'export_symbols': 0, 'describe_blocks': 13, 'test_blocks': 51, 'sample_paths': ['benchmarks/harsh-critic/scoring/__tests__/parser.test.ts', 'benchmarks/harsh-critic/scoring/__tests__/scorer.test.ts', 'benchmarks/harsh-critic/vitest.config.ts', 'dist/__tests__/agent-boundary-guidance.test.d.ts', 'dist/__tests__/agent-boundary-guidance.test.js', 'dist/__tests__/agent-registry.test.d.ts', 'dist/__tests__/agent-registry.test.js', 'dist/__tests__/artifact-descriptor-handoff.test.d.ts', 'dist/__tests__/artifact-descriptor-handoff.test.js', 'dist/__tests__/artifact-descriptor-integration.test.d.ts']}`
- agent surfaces: `{'surface_count': 1961, 'buckets': {'claude': 39, 'agents': 249, 'commands': 127, 'skills': 164, 'hooks': 1347}, 'sample_paths': ['.claude-plugin/marketplace.json', '.claude-plugin/plugin.json', '.github/CLAUDE.md', '.mcp.json', 'AGENTS.md', 'CLAUDE.md', 'agents/analyst.md', 'agents/architect.md', 'agents/code-reviewer.md', 'agents/code-simplifier.md', 'agents/critic.md', 'agents/debugger.md', 'agents/designer.md', 'agents/document-specialist.md', 'agents/executor.md', 'agents/explore.md', 'agents/git-master.md', 'agents/planner.md', 'agents/qa-tester.md', 'agents/scientist.md', 'agents/security-reviewer.md', 'agents/test-engineer.md', 'agents/tracer.md', 'agents/verifier.md']}`
- skill architecture: `{'skill_count': 39, 'skill_frontmatter_count': 39, 'skill_frontmatter_with_description': 39, 'skill_frontmatter_with_use_when': 0, 'claude_command_count': 0, 'gemini_command_count': 0, 'persona_count': 19, 'hook_file_count': 1, 'setup_doc_count': 0, 'reference_doc_count': 0, 'harness_surface_count': 4, 'command_lifecycle': [], 'sample_skill_paths': ['skills/ai-slop-cleaner/SKILL.md', 'skills/ask/SKILL.md', 'skills/autopilot/SKILL.md', 'skills/autoresearch/SKILL.md', 'skills/cancel/SKILL.md', 'skills/ccg/SKILL.md', 'skills/configure-notifications/SKILL.md', 'skills/debug/SKILL.md', 'skills/deep-dive/SKILL.md', 'skills/deep-interview/SKILL.md', 'skills/deepinit/SKILL.md', 'skills/external-context/SKILL.md'], 'sample_command_paths': [], 'sample_persona_paths': ['agents/analyst.md', 'agents/architect.md', 'agents/code-reviewer.md', 'agents/code-simplifier.md', 'agents/critic.md', 'agents/debugger.md', 'agents/designer.md', 'agents/document-specialist.md'], 'setup_docs': [], 'orchestration_signals': []}`

Distilled moves:
- 把 Skill / Persona / Command 分层: skill 管 how, persona 管 who, command 管 when,避免大而全的混合提示词。
- 把 CI/workflow 里的真实 job 名称反写到本地 quality gate,避免本地验收和远端脱节。
- 先读取 package scripts 再决定命令,不要凭经验猜 npm/pnpm/yarn gate。
- 把 AGENTS/CLAUDE/Cursor/skills/hooks 视为一等协作界面,纳入 handoff。
- 设计文档不是装饰: brief/RFC/ADR 要把 motivation、alternatives、rollout 和 unresolved 写清。

### addyosmani/agent-skills

- source lane: `source_promotion_batch`; runtime tier: `deep_static_candidate`; license: `MIT`; stars snapshot: `45641`
- line anatomy: source `0`, tests `803`, docs `8078`
- doc taxonomy: `{"design": 4, "governance": 4, "onboarding": 1, "reference": 40, "validation": 6}`
- workflow command hits: `['npm']`
- Python symbols: `{'files_sampled': 0, 'classes': 0, 'functions': 0, 'test_functions': 0, 'parse_errors': 0, 'sample_paths': []}`
- JS/TS symbols: `{'files_sampled': 0, 'export_symbols': 0, 'describe_blocks': 0, 'test_blocks': 0, 'sample_paths': []}`
- agent surfaces: `{'surface_count': 61, 'buckets': {'claude': 10, 'commands': 14, 'skills': 29, 'agents': 6, 'cursor': 1, 'hooks': 9}, 'sample_paths': ['.claude-plugin/marketplace.json', '.claude-plugin/plugin.json', '.claude/commands/build.md', '.claude/commands/code-simplify.md', '.claude/commands/plan.md', '.claude/commands/review.md', '.claude/commands/ship.md', '.claude/commands/spec.md', '.claude/commands/test.md', '.gemini/commands/build.toml', '.gemini/commands/code-simplify.toml', '.gemini/commands/planning.toml', '.gemini/commands/review.toml', '.gemini/commands/ship.toml', '.gemini/commands/spec.toml', '.gemini/commands/test.toml', '.opencode/skills', 'AGENTS.md', 'CLAUDE.md', 'agents/README.md', 'agents/code-reviewer.md', 'agents/security-auditor.md', 'agents/test-engineer.md', 'docs/cursor-setup.md']}`
- skill architecture: `{'skill_count': 23, 'skill_frontmatter_count': 23, 'skill_frontmatter_with_description': 23, 'skill_frontmatter_with_use_when': 23, 'claude_command_count': 7, 'gemini_command_count': 7, 'persona_count': 3, 'hook_file_count': 9, 'setup_doc_count': 5, 'reference_doc_count': 5, 'harness_surface_count': 19, 'command_lifecycle': ['build', 'code-simplify', 'plan', 'review', 'ship', 'spec', 'test'], 'sample_skill_paths': ['skills/api-and-interface-design/SKILL.md', 'skills/browser-testing-with-devtools/SKILL.md', 'skills/ci-cd-and-automation/SKILL.md', 'skills/code-review-and-quality/SKILL.md', 'skills/code-simplification/SKILL.md', 'skills/context-engineering/SKILL.md', 'skills/debugging-and-error-recovery/SKILL.md', 'skills/deprecation-and-migration/SKILL.md', 'skills/documentation-and-adrs/SKILL.md', 'skills/doubt-driven-development/SKILL.md', 'skills/frontend-ui-engineering/SKILL.md', 'skills/git-workflow-and-versioning/SKILL.md'], 'sample_command_paths': ['.claude/commands/build.md', '.claude/commands/code-simplify.md', '.claude/commands/plan.md', '.claude/commands/review.md', '.claude/commands/ship.md', '.claude/commands/spec.md', '.claude/commands/test.md', '.gemini/commands/build.toml', '.gemini/commands/code-simplify.toml', '.gemini/commands/planning.toml', '.gemini/commands/review.toml', '.gemini/commands/ship.toml', '.gemini/commands/spec.toml', '.gemini/commands/test.toml'], 'sample_persona_paths': ['agents/code-reviewer.md', 'agents/security-auditor.md', 'agents/test-engineer.md'], 'setup_docs': ['docs/copilot-setup.md', 'docs/cursor-setup.md', 'docs/gemini-cli-setup.md', 'docs/opencode-setup.md', 'docs/windsurf-setup.md'], 'orchestration_signals': ['anti-meta-orchestrator', 'main-agent-merge', 'parallel-fanout-ship', 'personas-do-not-call-personas', 'single-perspective-persona', 'skill-persona-command-layering']}`

Distilled moves:
- 把 Skill / Persona / Command 分层: skill 管 how, persona 管 who, command 管 when,避免大而全的混合提示词。
- 把 spec/plan/build/test/review/ship 做成稳定命令生命周期,让小白按入口走、高手按证据审。
- 多 agent 编排只在独立视角可并行时 fan-out,最终由主 agent 合并 go/no-go 与回滚计划。
- 把 CI/workflow 里的真实 job 名称反写到本地 quality gate,避免本地验收和远端脱节。
- 把 AGENTS/CLAUDE/Cursor/skills/hooks 视为一等协作界面,纳入 handoff。

### affaan-m/ECC

- source lane: `source_promotion_batch`; runtime tier: `runtime_candidate`; license: `MIT`; stars snapshot: `192280`
- line anatomy: source `1356`, tests `91282`, docs `344922`
- doc taxonomy: `{"design": 3, "governance": 11, "reference": 116, "validation": 10}`
- workflow command hits: `['npm', 'pnpm', 'yarn']`
- Python symbols: `{'files_sampled': 37, 'classes': 60, 'functions': 306, 'test_functions': 181, 'parse_errors': 0, 'sample_paths': ['integrations/aura/tests/__init__.py', 'integrations/aura/tests/fixtures.py', 'integrations/aura/tests/test_adapter.py', 'skills/continuous-learning-v2/scripts/test_parse_instinct.py', 'skills/skill-comply/tests/test_grader.py', 'skills/skill-comply/tests/test_parser.py', 'skills/skill-comply/tests/test_runner.py', 'src/llm/__init__.py', 'src/llm/__main__.py', 'src/llm/cli/__init__.py']}`
- JS/TS symbols: `{'files_sampled': 90, 'export_symbols': 10, 'describe_blocks': 0, 'test_blocks': 1892, 'sample_paths': ['.opencode/tools/run-tests.ts', 'tests/ci/agent-instruction-safety.test.js', 'tests/ci/agent-yaml-surface.test.js', 'tests/ci/catalog.test.js', 'tests/ci/code-reviewer-false-positive-guard.test.js', 'tests/ci/codex-skill-surface.test.js', 'tests/ci/command-registry.test.js', 'tests/ci/mle-workflow-coverage.test.js', 'tests/ci/no-personal-paths.test.js', 'tests/ci/scan-supply-chain-iocs.test.js']}`
- agent surfaces: `{'surface_count': 2000, 'buckets': {'agents': 442, 'skills': 1020, 'claude': 68, 'commands': 392, 'cursor': 69, 'hooks': 202}, 'sample_paths': ['.agents/plugins/marketplace.json', '.agents/skills/agent-introspection-debugging/SKILL.md', '.agents/skills/agent-introspection-debugging/agents/openai.yaml', '.agents/skills/agent-sort/SKILL.md', '.agents/skills/agent-sort/agents/openai.yaml', '.agents/skills/api-design/SKILL.md', '.agents/skills/api-design/agents/openai.yaml', '.agents/skills/article-writing/SKILL.md', '.agents/skills/article-writing/agents/openai.yaml', '.agents/skills/backend-patterns/SKILL.md', '.agents/skills/backend-patterns/agents/openai.yaml', '.agents/skills/brand-voice/SKILL.md', '.agents/skills/brand-voice/agents/openai.yaml', '.agents/skills/brand-voice/references/voice-profile-schema.md', '.agents/skills/bun-runtime/SKILL.md', '.agents/skills/bun-runtime/agents/openai.yaml', '.agents/skills/coding-standards/SKILL.md', '.agents/skills/coding-standards/agents/openai.yaml', '.agents/skills/content-engine/SKILL.md', '.agents/skills/content-engine/agents/openai.yaml', '.agents/skills/crosspost/SKILL.md', '.agents/skills/crosspost/agents/openai.yaml', '.agents/skills/deep-research/SKILL.md', '.agents/skills/deep-research/agents/openai.yaml']}`
- skill architecture: `{'skill_count': 246, 'skill_frontmatter_count': 80, 'skill_frontmatter_with_description': 80, 'skill_frontmatter_with_use_when': 24, 'claude_command_count': 3, 'gemini_command_count': 0, 'persona_count': 61, 'hook_file_count': 4, 'setup_doc_count': 0, 'reference_doc_count': 0, 'harness_surface_count': 76, 'command_lifecycle': ['add-language-rules', 'database-migration', 'feature-development'], 'sample_skill_paths': ['skills/accessibility/SKILL.md', 'skills/agent-architecture-audit/SKILL.md', 'skills/agent-eval/SKILL.md', 'skills/agent-harness-construction/SKILL.md', 'skills/agent-introspection-debugging/SKILL.md', 'skills/agent-payment-x402/SKILL.md', 'skills/agent-sort/SKILL.md', 'skills/agentic-engineering/SKILL.md', 'skills/agentic-os/SKILL.md', 'skills/ai-first-engineering/SKILL.md', 'skills/ai-regression-testing/SKILL.md', 'skills/android-clean-architecture/SKILL.md'], 'sample_command_paths': ['.claude/commands/add-language-rules.md', '.claude/commands/database-migration.md', '.claude/commands/feature-development.md'], 'sample_persona_paths': ['agents/a11y-architect.md', 'agents/architect.md', 'agents/build-error-resolver.md', 'agents/chief-of-staff.md', 'agents/code-architect.md', 'agents/code-explorer.md', 'agents/code-reviewer.md', 'agents/code-simplifier.md'], 'setup_docs': [], 'orchestration_signals': []}`

Distilled moves:
- 把 Skill / Persona / Command 分层: skill 管 how, persona 管 who, command 管 when,避免大而全的混合提示词。
- 把高频工程动作做成稳定 slash commands,先复用入口,再让 agent 展开细节。
- 把 CI/workflow 里的真实 job 名称反写到本地 quality gate,避免本地验收和远端脱节。
- 先读取 package scripts 再决定命令,不要凭经验猜 npm/pnpm/yarn gate。
- 把 pyproject 的 pytest/ruff/mypy/coverage 配置当成 Python 项目的验证入口。

### browser-use/browser-use

- source lane: `source_promotion_batch`; runtime tier: `runtime_candidate`; license: `MIT`; stars snapshot: `95508`
- line anatomy: source `0`, tests `25634`, docs `6699`
- doc taxonomy: `{"governance": 2, "onboarding": 11, "reference": 42, "validation": 1}`
- workflow command hits: `['playwright', 'pytest', 'ruff']`
- Python symbols: `{'files_sampled': 80, 'classes': 130, 'functions': 941, 'test_functions': 702, 'parse_errors': 0, 'sample_paths': ['browser_use/llm/tests/test_anthropic_cache.py', 'browser_use/llm/tests/test_chat_models.py', 'browser_use/llm/tests/test_gemini_image.py', 'browser_use/llm/tests/test_groq_loop.py', 'browser_use/llm/tests/test_mistral_schema.py', 'browser_use/llm/tests/test_single_step.py', 'browser_use/tokens/tests/test_cost.py', 'tests/ci/browser/test_cdp_headers.py', 'tests/ci/browser/test_cloud_browser.py', 'tests/ci/browser/test_cross_origin_click.py']}`
- JS/TS symbols: `{'files_sampled': 0, 'export_symbols': 0, 'describe_blocks': 0, 'test_blocks': 0, 'sample_paths': []}`
- agent surfaces: `{'surface_count': 78, 'buckets': {'claude': 3, 'agents': 32, 'skills': 37, 'commands': 6}, 'sample_paths': ['.github/workflows/claude.yml', 'AGENTS.md', 'CLAUDE.md', 'browser_use/agent/cloud_events.py', 'browser_use/agent/gif.py', 'browser_use/agent/judge.py', 'browser_use/agent/message_manager/service.py', 'browser_use/agent/message_manager/utils.py', 'browser_use/agent/message_manager/views.py', 'browser_use/agent/prompts.py', 'browser_use/agent/service.py', 'browser_use/agent/system_prompts/__init__.py', 'browser_use/agent/system_prompts/system_prompt.md', 'browser_use/agent/system_prompts/system_prompt_anthropic_flash.md', 'browser_use/agent/system_prompts/system_prompt_browser_use.md', 'browser_use/agent/system_prompts/system_prompt_browser_use_flash.md', 'browser_use/agent/system_prompts/system_prompt_browser_use_no_thinking.md', 'browser_use/agent/system_prompts/system_prompt_flash.md', 'browser_use/agent/system_prompts/system_prompt_flash_anthropic.md', 'browser_use/agent/system_prompts/system_prompt_no_thinking.md', 'browser_use/agent/variable_detector.py', 'browser_use/agent/views.py', 'browser_use/mcp/.dxtignore', 'browser_use/mcp/__init__.py']}`
- skill architecture: `{'skill_count': 4, 'skill_frontmatter_count': 4, 'skill_frontmatter_with_description': 4, 'skill_frontmatter_with_use_when': 2, 'claude_command_count': 0, 'gemini_command_count': 0, 'persona_count': 0, 'hook_file_count': 0, 'setup_doc_count': 0, 'reference_doc_count': 0, 'harness_surface_count': 2, 'command_lifecycle': [], 'sample_skill_paths': ['skills/browser-use/SKILL.md', 'skills/cloud/SKILL.md', 'skills/open-source/SKILL.md', 'skills/remote-browser/SKILL.md'], 'sample_command_paths': [], 'sample_persona_paths': [], 'setup_docs': [], 'orchestration_signals': []}`

Distilled moves:
- 把 skill frontmatter、触发条件和验证清单当作可安装协作界面,而不是普通 Markdown。
- 把 CI/workflow 里的真实 job 名称反写到本地 quality gate,避免本地验收和远端脱节。
- 把 pyproject 的 pytest/ruff/mypy/coverage 配置当成 Python 项目的验证入口。
- 把 AGENTS/CLAUDE/Cursor/skills/hooks 视为一等协作界面,纳入 handoff。
- 从测试命名和 test block 学项目的验收语言,再写自己的最小验证。

### github/spec-kit

- source lane: `runtime_repo_audit`; runtime tier: `runtime_candidate`; license: `MIT`; stars snapshot: `105805`
- line anatomy: source `22467`, tests `29709`, docs `8057`
- doc taxonomy: `{"design": 23, "governance": 4, "onboarding": 3, "reference": 63, "validation": 9}`
- workflow command hits: `['npm', 'pnpm', 'pytest', 'ruff', 'yarn']`
- Python symbols: `{'files_sampled': 80, 'classes': 133, 'functions': 804, 'test_functions': 174, 'parse_errors': 0, 'sample_paths': ['src/specify_cli/__init__.py', 'src/specify_cli/_assets.py', 'src/specify_cli/_console.py', 'src/specify_cli/_github_http.py', 'src/specify_cli/_utils.py', 'src/specify_cli/_version.py', 'src/specify_cli/agents.py', 'src/specify_cli/authentication/__init__.py', 'src/specify_cli/authentication/azure_devops.py', 'src/specify_cli/authentication/base.py']}`
- JS/TS symbols: `{'files_sampled': 0, 'export_symbols': 0, 'describe_blocks': 0, 'test_blocks': 0, 'sample_paths': []}`
- agent surfaces: `{'surface_count': 43, 'buckets': {'agents': 7, 'skills': 3, 'commands': 25, 'claude': 3, 'cursor': 2, 'hooks': 5}, 'sample_paths': ['.github/ISSUE_TEMPLATE/agent_request.yml', '.github/skills/add-community-extension/SKILL.md', 'AGENTS.md', 'extensions/git/commands/speckit.git.commit.md', 'extensions/git/commands/speckit.git.feature.md', 'extensions/git/commands/speckit.git.initialize.md', 'extensions/git/commands/speckit.git.remote.md', 'extensions/git/commands/speckit.git.validate.md', 'extensions/selftest/commands/selftest.md', 'extensions/template/commands/example.md', 'media/bootstrap-claude-code.gif', 'presets/lean/commands/speckit.constitution.md', 'presets/lean/commands/speckit.implement.md', 'presets/lean/commands/speckit.plan.md', 'presets/lean/commands/speckit.specify.md', 'presets/lean/commands/speckit.tasks.md', 'presets/scaffold/commands/speckit.myext.myextcmd.md', 'presets/scaffold/commands/speckit.specify.md', 'presets/self-test/commands/speckit.specify.md', 'presets/self-test/commands/speckit.wrap-test.md', 'presets/self-test/templates/agent-file-template.md', 'src/specify_cli/agents.py', 'src/specify_cli/integrations/claude/__init__.py', 'src/specify_cli/integrations/cursor_agent/__init__.py']}`
- skill architecture: `{'skill_count': 0, 'skill_frontmatter_count': 0, 'skill_frontmatter_with_description': 0, 'skill_frontmatter_with_use_when': 0, 'claude_command_count': 0, 'gemini_command_count': 0, 'persona_count': 0, 'hook_file_count': 0, 'setup_doc_count': 0, 'reference_doc_count': 0, 'harness_surface_count': 1, 'command_lifecycle': [], 'sample_skill_paths': [], 'sample_command_paths': [], 'sample_persona_paths': [], 'setup_docs': [], 'orchestration_signals': []}`

Distilled moves:
- 把 CI/workflow 里的真实 job 名称反写到本地 quality gate,避免本地验收和远端脱节。
- 把 pyproject 的 pytest/ruff/mypy/coverage 配置当成 Python 项目的验证入口。
- 把 AGENTS/CLAUDE/Cursor/skills/hooks 视为一等协作界面,纳入 handoff。
- 设计文档不是装饰: brief/RFC/ADR 要把 motivation、alternatives、rollout 和 unresolved 写清。
- 从测试命名和 test block 学项目的验收语言,再写自己的最小验证。

### humanlayer/12-factor-agents

- source lane: `runtime_repo_audit`; runtime tier: `runtime_candidate`; license: `Apache-2.0`; stars snapshot: `22309`
- line anatomy: source `1186`, tests `1144`, docs `4935`
- doc taxonomy: `{"design": 1, "reference": 49, "validation": 2}`
- workflow command hits: `[]`
- Python symbols: `{'files_sampled': 0, 'classes': 0, 'functions': 0, 'test_functions': 0, 'parse_errors': 0, 'sample_paths': []}`
- JS/TS symbols: `{'files_sampled': 18, 'export_symbols': 27, 'describe_blocks': 5, 'test_blocks': 20, 'sample_paths': ['packages/create-12-factor-agent/template/src/a2h.ts', 'packages/create-12-factor-agent/template/src/agent.ts', 'packages/create-12-factor-agent/template/src/cli.ts', 'packages/create-12-factor-agent/template/src/index.ts', 'packages/create-12-factor-agent/template/src/server.ts', 'packages/create-12-factor-agent/template/src/state.ts', 'packages/walkthroughgen/examples/typescript/walkthrough/01-index.ts', 'packages/walkthroughgen/examples/typescript/walkthrough/02-cli.ts', 'packages/walkthroughgen/examples/typescript/walkthrough/02-index.ts', 'packages/walkthroughgen/jest.config.js']}`
- agent surfaces: `{'surface_count': 146, 'buckets': {'claude': 2, 'agents': 144, 'hooks': 2}, 'sample_paths': ['CLAUDE.md', 'content/factor-10-small-focused-agents.md', 'img/025-agent-dag.png', 'img/026-agent-dag-lines.png', 'img/027-agent-loop-animation.gif', 'img/027-agent-loop-animation.mp4', 'img/027-agent-loop-dag.png', 'img/027-agent-loop.png', 'img/028-micro-agent-dag.png', 'img/175-outer-loop-agents.png', 'img/1a0-small-focused-agents.png', 'img/1a5-agent-scope-grow.gif', 'img/1c5-agent-foldl.png', 'packages/create-12-factor-agent/template/.gitignore', 'packages/create-12-factor-agent/template/README.md', 'packages/create-12-factor-agent/template/baml_src/agent.baml', 'packages/create-12-factor-agent/template/baml_src/clients.baml', 'packages/create-12-factor-agent/template/baml_src/generators.baml', 'packages/create-12-factor-agent/template/baml_src/tool_calculator.baml', 'packages/create-12-factor-agent/template/package-lock.json', 'packages/create-12-factor-agent/template/package.json', 'packages/create-12-factor-agent/template/src/a2h.ts', 'packages/create-12-factor-agent/template/src/agent.ts', 'packages/create-12-factor-agent/template/src/cli.ts']}`
- skill architecture: `{'skill_count': 0, 'skill_frontmatter_count': 0, 'skill_frontmatter_with_description': 0, 'skill_frontmatter_with_use_when': 0, 'claude_command_count': 0, 'gemini_command_count': 0, 'persona_count': 0, 'hook_file_count': 0, 'setup_doc_count': 0, 'reference_doc_count': 0, 'harness_surface_count': 1, 'command_lifecycle': [], 'sample_skill_paths': [], 'sample_command_paths': [], 'sample_persona_paths': [], 'setup_docs': [], 'orchestration_signals': []}`

Distilled moves:
- 先读取 package scripts 再决定命令,不要凭经验猜 npm/pnpm/yarn gate。
- 把 pyproject 的 pytest/ruff/mypy/coverage 配置当成 Python 项目的验证入口。
- 把 AGENTS/CLAUDE/Cursor/skills/hooks 视为一等协作界面,纳入 handoff。
- 设计文档不是装饰: brief/RFC/ADR 要把 motivation、alternatives、rollout 和 unresolved 写清。
- 从测试命名和 test block 学项目的验收语言,再写自己的最小验证。

### microsoft/code-with-engineering-playbook

- source lane: `runtime_repo_audit`; runtime tier: `runtime_candidate`; license: `CC-BY-4.0`; stars snapshot: `2663`
- line anatomy: source `0`, tests `4128`, docs `16078`
- doc taxonomy: `{"design": 36, "governance": 3, "onboarding": 2, "reference": 73, "validation": 26}`
- workflow command hits: `[]`
- Python symbols: `{'files_sampled': 0, 'classes': 0, 'functions': 0, 'test_functions': 0, 'parse_errors': 0, 'sample_paths': []}`
- JS/TS symbols: `{'files_sampled': 0, 'export_symbols': 0, 'describe_blocks': 0, 'test_blocks': 0, 'sample_paths': []}`
- agent surfaces: `{'surface_count': 1, 'buckets': {'skills': 1}, 'sample_paths': ['docs/ml-and-ai-projects/images/ml-tpm-skills.png']}`
- skill architecture: `{'skill_count': 0, 'skill_frontmatter_count': 0, 'skill_frontmatter_with_description': 0, 'skill_frontmatter_with_use_when': 0, 'claude_command_count': 0, 'gemini_command_count': 0, 'persona_count': 0, 'hook_file_count': 0, 'setup_doc_count': 0, 'reference_doc_count': 0, 'harness_surface_count': 0, 'command_lifecycle': [], 'sample_skill_paths': [], 'sample_command_paths': [], 'sample_persona_paths': [], 'setup_docs': [], 'orchestration_signals': []}`

Distilled moves:
- 把 CI/workflow 里的真实 job 名称反写到本地 quality gate,避免本地验收和远端脱节。
- 先读取 package scripts 再决定命令,不要凭经验猜 npm/pnpm/yarn gate。
- 把 AGENTS/CLAUDE/Cursor/skills/hooks 视为一等协作界面,纳入 handoff。
- 设计文档不是装饰: brief/RFC/ADR 要把 motivation、alternatives、rollout 和 unresolved 写清。

### promptfoo/promptfoo

- source lane: `runtime_repo_audit`; runtime tier: `runtime_candidate`; license: `MIT`; stars snapshot: `21585`
- line anatomy: source `297769`, tests `491531`, docs `129742`
- doc taxonomy: `{"design": 3, "governance": 4, "onboarding": 103, "reference": 27, "validation": 3}`
- workflow command hits: `['go test', 'npm', 'ruff', 'vitest']`
- Python symbols: `{'files_sampled': 32, 'classes': 45, 'functions': 179, 'test_functions': 71, 'parse_errors': 0, 'sample_paths': ['examples/compare-agentic-sdks/test-codebase/payment_processor.py', 'examples/compare-agentic-sdks/test-codebase/user_service.py', 'examples/config-python-test-cases/test_cases.py', 'examples/integration-google-adk/provider_test.py', 'examples/integration-inspect-osworld/osworld_tests.py', 'examples/openai-agents/agent_provider_test.py', 'examples/openai-agents/promptfoo_tracing_test.py', 'examples/provider-amazon-sagemaker/deploy-test-model.py', 'src/python/persistent_wrapper.py', 'src/python/persistent_wrapper_test.py']}`
- JS/TS symbols: `{'files_sampled': 90, 'export_symbols': 127, 'describe_blocks': 81, 'test_blocks': 389, 'sample_paths': ['examples/config-javascript-test-cases/dynamicTests.ts', 'examples/config-javascript-test-cases/staticTests.ts', 'examples/config-node-module-package/node_modules/testpackage/main.js', 'examples/config-retry-testing/errorProvider.js', 'examples/config-websockets/basic/test-server/server.js', 'examples/integration-jest/index.test.ts', 'examples/integration-jest/vitest.config.js', 'examples/provider-amazon-sagemaker/test-sagemaker-provider.js', 'examples/redteam-cyberseceval/loadTests.js', 'examples/redteam-medical-agent/src/test-agent.js']}`
- agent surfaces: `{'surface_count': 615, 'buckets': {'agents': 287, 'skills': 103, 'claude': 100, 'cursor': 1, 'hooks': 55, 'commands': 114}, 'sample_paths': ['.agents/AGENTS.md', '.agents/plugins/marketplace.json', '.agents/skills/redteam-plugin-development/SKILL.md', '.agents/skills/search-params/SKILL.md', '.claude-plugin/marketplace.json', '.claude/settings.json', '.claude/skills/promptfoo-evals/SKILL.md', '.claude/skills/promptfoo-evals/references/cheatsheet.md', '.claude/skills/redteam-plugin-development/SKILL.md', '.claude/skills/search-params/SKILL.md', '.cursor/mcp.json', '.github/AGENTS.md', 'AGENTS.md', 'CLAUDE.md', 'code-scan-action/AGENTS.md', 'docs/agents/AGENTS.md', 'docs/agents/codex-app-server-provider-notes.md', 'docs/agents/coding-agent-provider-taxonomy.md', 'docs/agents/database-security.md', 'docs/agents/dependency-management.md', 'docs/agents/git-workflow.md', 'docs/agents/logging.md', 'docs/agents/pr-conventions.md', 'docs/agents/python.md']}`
- skill architecture: `{'skill_count': 0, 'skill_frontmatter_count': 0, 'skill_frontmatter_with_description': 0, 'skill_frontmatter_with_use_when': 0, 'claude_command_count': 0, 'gemini_command_count': 0, 'persona_count': 0, 'hook_file_count': 0, 'setup_doc_count': 0, 'reference_doc_count': 0, 'harness_surface_count': 4, 'command_lifecycle': [], 'sample_skill_paths': [], 'sample_command_paths': [], 'sample_persona_paths': [], 'setup_docs': [], 'orchestration_signals': []}`

Distilled moves:
- 把 CI/workflow 里的真实 job 名称反写到本地 quality gate,避免本地验收和远端脱节。
- 先读取 package scripts 再决定命令,不要凭经验猜 npm/pnpm/yarn gate。
- 把 pyproject 的 pytest/ruff/mypy/coverage 配置当成 Python 项目的验证入口。
- 把 AGENTS/CLAUDE/Cursor/skills/hooks 视为一等协作界面,纳入 handoff。
- 设计文档不是装饰: brief/RFC/ADR 要把 motivation、alternatives、rollout 和 unresolved 写清。

## What ShipGrade CN Absorbs

- Command topology is extracted before commands are guessed.
- Workflow files become local quality-gate candidates.
- Test/eval names become the project's acceptance language.
- Agent-facing files become handoff surfaces, not incidental docs.
- Skill / Persona / Command are separated so workflows keep clear how/who/when boundaries.
- Parallel agent fan-out is reserved for independent review/security/test perspectives, with one main agent merging the final go/no-go.
- Documentation taxonomy decides whether a task needs brief, RFC, ADR, eval, or release note.

## Boundary

- This report does not copy implementation bodies or long source passages.
- It does not claim every upstream test suite passed.
- It records static and low-side-effect evidence before any executable sandbox case is promoted.
- Stars and file counts remain discovery signals, not quality proof.
