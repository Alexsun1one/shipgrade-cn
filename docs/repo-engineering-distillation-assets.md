# Repository Engineering Distillation Assets

中文名: 仓库工程蒸馏资产

这批产物把真实、公开、许可证已审查的仓库证据转成四类资产: Repo Card、Pattern Card、Task Card、Eval。它不是把 repo 直接塞给模型训练,也不复制源代码正文。

## Counts

- Repo Cards: `11`
- Pattern Cards: `15`
- Task Cards: `90`
- Eval Cases: `90`

## Asset Files

| asset | path | purpose |
| --- | --- | --- |
| Repo Card | `repo_cards.jsonl` | 仓库画像: 领域、语言、架构、入口、目录、命令、强项、迁移价值。 |
| Pattern Card | `pattern_cards.jsonl` | 合并雷同来源后的工程模式卡: 适用场景、问题、解法、证据、优点、代价。 |
| Task Card | `task_cards.jsonl` | 可训练/可评测任务: 规划、审查、修复、迁移、反模式、开项文档。 |
| Eval Case | `eval_cases.jsonl` | 评测输入、期望点、扣分点、judge rubric 和最低通过分。 |

## Top Repo Cards

| repo | domain | architecture | tests | evals | license |
| --- | --- | --- | ---: | ---: | --- |
| `affaan-m/ECC` | LLM eval / quality gate | Skill / Persona / Command layered / command-topology-first / CI-backed quality gate / docs-as-architecture-contract / eval-oriented validation / agent-facing contract surfaces | 302 | 85 | `MIT` |
| `github/spec-kit` | spec-driven development workflow | command-topology-first / CI-backed quality gate / docs-as-architecture-contract / agent-facing contract surfaces | 87 | 0 | `MIT` |
| `browser-use/browser-use` | browser automation agent runtime | frontmatter-driven skill pack / command-topology-first / CI-backed quality gate / eval-oriented validation / agent-facing contract surfaces | 104 | 4 | `MIT` |
| `addyosmani/agent-skills` | spec-driven development workflow | Skill / Persona / Command layered / CI-backed quality gate / docs-as-architecture-contract / agent-facing contract surfaces | 9 | 0 | `MIT` |
| `Yeachan-Heo/oh-my-claudecode` | LLM eval / quality gate | Skill / Persona / Command layered / command-topology-first / CI-backed quality gate / docs-as-architecture-contract / eval-oriented validation / agent-facing contract surfaces | 2735 | 83 | `MIT` |
| `VoltAgent/awesome-agent-skills` | spec-driven development workflow | structure-first repository | 0 | 0 | `MIT` |
| `SuperClaude-Org/SuperClaude_Framework` | AI coding agent skills / workflow system | frontmatter-driven skill pack / command-topology-first / CI-backed quality gate / docs-as-architecture-contract / agent-facing contract surfaces | 30 | 0 | `MIT` |
| `humanlayer/12-factor-agents` | AI coding agent skills / workflow system | command-topology-first / docs-as-architecture-contract / agent-facing contract surfaces | 22 | 0 | `Apache-2.0` |

## Merged Pattern Cards

| pattern | source repos | core idea |
| --- | ---: | --- |
| `把 AGENTS / CLAUDE / Cursor 当作一等协作界面` | 10 | 把 AGENTS.md、CLAUDE.md、Cursor rules、skills、hooks 视为公开 API,并在 handoff 中同步引用。 |
| `把 CI 反写成本地质量门` | 9 | 抽取 workflow job 名称和 command hits,把可本地执行的部分写进 quality gate。 |
| `先读命令拓扑,再写验证计划` | 9 | 从 package scripts、pyproject、Makefile、workflow command hits 中抽出最小验证入口。 |
| `跨 harness 可移植规则` | 9 | 抽象共享规则,再为 AGENTS、CLAUDE、Cursor rule、skill frontmatter 提供薄适配层。 |
| `文档是架构契约,不是装饰` | 9 | 把 brief/RFC/ADR/spec 写成约束输入,让 agent 按文档往下做,并把未决问题显式留在 handoff。 |
| `先建 eval,再谈微调` | 6 | 把 Repo/Pattern/Task Card 转成 planning/review/repair/migration/anti-pattern eval,再比较模型输出。 |
| `用 examples 做用户分层入口` | 11 | 同时提供 30 秒 demo、5 分钟安装、真实证据、目录地图、贡献入口和专业边界。 |
| `开项文档栈` | 9 | 最小栈: README/START_HERE、task brief、architecture note、quality gate、handoff、ADR/decision log。 |
| `许可证和来源边界优先` | 11 | 每个资产记录 repo、commit、path、license、policy、生成时间和 public-safe 边界。 |
| `多 agent 并行,主 agent 合并` | 1 | 只把独立视角 fan-out,主 agent 统一合并 go/no-go、风险、回滚和验证结果。 |

## Sample Repo Card

```json
{
  "schema": "shipgrade.repo_card.v1",
  "repo": "affaan-m/ECC",
  "commit": "928076cc08cbb31e8549cea2883b4f51811de1c8",
  "generated_at": "2026-05-26T04:46:15Z",
  "domain": "LLM eval / quality gate",
  "language": [
    "Python",
    "TypeScript",
    "JavaScript",
    "Rust",
    "Markdown"
  ],
  "architecture": "Skill / Persona / Command layered / command-topology-first / CI-backed quality gate / docs-as-architecture-contract / eval-oriented validation / agent-facing contract surfaces",
  "license_spdx": "MIT",
  "source_policy": "allow_extract",
  "stars_snapshot": 192280,
  "runtime_tier": "runtime_candidate",
  "entrypoints": [
    ".opencode/package.json",
    "package.json",
    "pyproject.toml",
    "skills/skill-comply/pyproject.toml",
    ".github/workflows/ci.yml",
    ".github/workflows/maintenance.yml",
    ".github/workflows/monthly-metrics.yml",
    ".github/workflows/release.yml",
    ".github/workflows/reusable-release.yml",
    ".github/workflows/reusable-test.yml",
    ".github/workflows/reusable-validate.yml",
    ".github/workflows/supply-chain-watch.yml"
  ],
  "important_dirs": {
    "source": "核心实现入口: src",
    "tests": "验收语言和回归边界",
    "docs": "使用说明、设计材料、决策和迁移证据",
    ".github/workflows": "CI 质量门和远端验证入口",
    "agent_surfaces": "AGENTS/CLAUDE/Cursor/skills/hooks 等协作界面",
    "skills": "可安装技能、触发条件、references 和 examples",
    "evals": "模型或系统质量评测资产"
  },
  "build_commands": [
    "npm run build",
    "npm run build:opencode",
    "npm run catalog:check",
    "npm run command-registry:check",
    "npm run lint",
    "npm run test",
    "python -m pytest",
    "ruff check .",
    "mypy ."
  ],
  "design_strengths": [
    "把 Skill / Persona / Command 分层: skill 管 how, persona 管 who, command 管 when,避免大而全的混合提示词。",
    "把高频工程动作做成稳定 slash commands,先复用入口,再让 agent 展开细节。",
    "把 CI/workflow 里的真实 job 名称反写到本地 quality gate,避免本地验收和远端脱节。",
    "先读取 package scripts 再决定命令,不要凭经验猜 npm/pnpm/yarn gate。",
    "把 pyproject 的 pytest/ruff/mypy/coverage 配置当成 Python 项目的验证入口。",
    "CI/workflow 能反推本地 quality gate。",
    "包含 eval/benchmark 资产,适合抽象成模型质量评测任务。",
    "测试文件足够多,能学习项目自己的验收语言。"
  ],
  "reuse_for": [
    "技能包 anatomy、frontmatter、references/examples 组织",
    "slash command 生命周期和 agent 入口设计",
    "Codex / Claude Code / Cursor 规则同步",
    "本地 quality gate 与 GitHub Actions 对齐",
    "从项目配置推导验证命令",
    "规划、review、repair、迁移、反模式识别 eval",
    "项目开项文档、ADR、设计评审模板"
  ],
  "avoid_copying": [
    "不要复制源代码正文或长片段; 只迁移结构、边界、命令、验证语言和设计判断。",
    "许可证不清或 metadata-only 的信源只能做 radar 和 attribution,不能抽取正文。",
    "高 star 只作为发现信号,不能替代结构、测试、CI、docs 和 license 证据。"
  ],
  "repo_evidence": {
    "file_count": 2870,
    "source_file_count": 19,
    "test_file_count": 302,
    "eval_file_count": 85,
    "design_doc_file_count": 1387,
    "workflow_count": 8,
    "agent_surface_count": 2000,
    "skill_count": 246
  },
  "evidence_paths": [
    ".opencode/package.json",
    "package.json",
    "pyproject.toml",
    "skills/skill-comply/pyproject.toml",
    ".github/workflows/c
```

## Sample Pattern Card

```json
{
  "schema": "shipgrade.pattern_card.v1",
  "pattern_id": "pattern:agent_surface_contract",
  "pattern_key": "agent_surface_contract",
  "generated_at": "2026-05-26T04:46:15Z",
  "name_cn": "把 AGENTS / CLAUDE / Cursor 当作一等协作界面",
  "name_en": "Agent Surface Contract",
  "source_repos": [
    "affaan-m/ECC",
    "github/spec-kit",
    "browser-use/browser-use",
    "addyosmani/agent-skills",
    "Yeachan-Heo/oh-my-claudecode",
    "SuperClaude-Org/SuperClaude_Framework",
    "humanlayer/12-factor-agents",
    "promptfoo/promptfoo",
    "microsoft/code-with-engineering-playbook",
    "UKGovernmentBEIS/inspect_ai"
  ],
  "applicable_when": "一个项目要让 Codex、Claude Code、Cursor 或其他 agent 共享规则。",
  "problem": "多个 agent 各读各的上下文,术语、路径、验收标准和禁止事项容易漂移。",
  "solution": "把 AGENTS.md、CLAUDE.md、Cursor rules、skills、hooks 视为公开 API,并在 handoff 中同步引用。",
  "code_evidence": [
    {
      "repo": "affaan-m/ECC",
      "license_spdx": "MIT",
      "paths": [
        ".agents/plugins/marketplace.json",
        ".agents/skills/agent-introspection-debugging/SKILL.md",
        ".agents/skills/agent-introspection-debugging/agents/openai.yaml",
        ".agents/skills/agent-sort/SKILL.md",
        ".agents/skills/agent-sort/agents/openai.yaml",
        ".agents/skills/api-design/SKILL.md",
        ".agents/skills/api-design/agents/openai.yaml",
        ".agents/skills/article-writing/SKILL.md",
        ".agents/skills/article-writing/agents/openai.yaml",
        ".agents/skills/backend-patterns/SKILL.md",
        ".agents/skills/backend-patterns/agents/openai.yaml",
        ".agents/skills/brand-voice/SKILL.md"
      ],
      "detail": "agent-facing files are explicit collaboration contracts"
    },
    {
      "repo": "github/spec-kit",
      "license_spdx": "MIT",
      "paths": [
        ".github/ISSUE_TEMPLATE/agent_request.yml",
        ".github/skills/add-community-extension/SKILL.md",
        "AGENTS.md",
        "extensions/git/commands/speckit.git.commit.md",
        "extensions/git/commands/speckit.git.feature.md",
        "extensions/git/commands/speckit.git.initialize.md",
        "extensions/git/commands/speckit.git.remote.md",
        "extensions/git/commands/speckit.git.validate.md",
        "extensions/selftest/commands/selftest.md",
        "extensions/template/commands/example.md",
        "media/bootstrap-claude-code.gif",
        "presets/lean/commands/speckit.constitution.md"
      ],
      "detail": "agent-facing files are explicit collaboration contracts"
    },
    {
      "repo": "browser-use/browser-use",
      "license_spdx": "MIT",
      "paths": [
        ".github/workflows/claude.yml",
        "AGENTS.md",
        "CLAUDE.md",
        "browser_use/agent/cloud_events.py",
        "browser_use/agent/gif.py",
        "browser_use/agent/judge.py",
        "browser_use/agent/message_manager/service.py",
        "browser_use/agent/message_manager/utils.py",
        "browser_use/agent/message_manager/views.py",
        "browser_use/agent/prompts.py",
      
```

## Sample Task Card

```json
{
  "schema": "shipgrade.task_card.v1",
  "task_id": "task:agent_surface_contract:engineering_plan",
  "generated_at": "2026-05-26T04:46:15Z",
  "task_type": "engineering_plan",
  "title_cn": "把 AGENTS / CLAUDE / Cursor 当作一等协作界面 - 规划任务",
  "context": "你在为中文 AI 工程 skill 提炼 `把 AGENTS / CLAUDE / Cursor 当作一等协作界面`。 该模式来自 affaan-m/ECC, github/spec-kit, browser-use/browser-use, addyosmani/agent-skills, Yeachan-Heo/oh-my-claudecode 等仓库。 模式问题: 多个 agent 各读各的上下文,术语、路径、验收标准和禁止事项容易漂移。 解法: 把 AGENTS.md、CLAUDE.md、Cursor rules、skills、hooks 视为公开 API,并在 handoff 中同步引用。",
  "repo_context": [
    "affaan-m/ECC:.agents/plugins/marketplace.json",
    "affaan-m/ECC:.agents/skills/agent-introspection-debugging/SKILL.md",
    "affaan-m/ECC:.agents/skills/agent-introspection-debugging/agents/openai.yaml",
    "affaan-m/ECC:.agents/skills/agent-sort/SKILL.md",
    "affaan-m/ECC:.agents/skills/agent-sort/agents/openai.yaml",
    "affaan-m/ECC:.agents/skills/api-design/SKILL.md",
    "affaan-m/ECC:.agents/skills/api-design/agents/openai.yaml",
    "affaan-m/ECC:.agents/skills/article-writing/SKILL.md",
    "affaan-m/ECC:.agents/skills/article-writing/agents/openai.yaml",
    "affaan-m/ECC:.agents/skills/backend-patterns/SKILL.md"
  ],
  "expected_answer": {
    "plan_should_include": [
      "引用模式卡名称和来源 repo",
      "指出应改哪些层和不应改哪些层",
      "给出最小验证命令或人工检查点",
      "写出风险和下一步",
      "不能复制上游源码正文",
      "保留 source repo / path / license / policy",
      "输出要同时照顾中文小白、进阶用户、专业工程师"
    ],
    "bad_answer_patterns": [
      "只复述 README",
      "不引用证据路径",
      "直接要求训练模型",
      "没有验证标准",
      "声称已经训练出世界级模型但没有 eval",
      "把 metadata-only 或许可证不清内容当成可抽取正文"
    ]
  },
  "judge_notes": {
    "source_pattern_id": "pattern:agent_surface_contract",
    "rubric_hint": "优先奖励证据引用、边界意识、验证命令、可接手 handoff; 惩罚空泛口号和无证据完成。"
  },
  "public_boundary": "Task data references path-level evidence only."
}
```

## Sample Eval Case

```json
{
  "schema": "shipgrade.eval_case.v1",
  "eval_id": "eval:agent_surface_contract:engineering_plan",
  "generated_at": "2026-05-26T04:46:15Z",
  "task_id": "task:agent_surface_contract:engineering_plan",
  "task_type": "engineering_plan",
  "input": {
    "instruction": "你在为中文 AI 工程 skill 提炼 `把 AGENTS / CLAUDE / Cursor 当作一等协作界面`。 该模式来自 affaan-m/ECC, github/spec-kit, browser-use/browser-use, addyosmani/agent-skills, Yeachan-Heo/oh-my-claudecode 等仓库。 模式问题: 多个 agent 各读各的上下文,术语、路径、验收标准和禁止事项容易漂移。 解法: 把 AGENTS.md、CLAUDE.md、Cursor rules、skills、hooks 视为公开 API,并在 handoff 中同步引用。",
    "repo_context": [
      "affaan-m/ECC:.agents/plugins/marketplace.json",
      "affaan-m/ECC:.agents/skills/agent-introspection-debugging/SKILL.md",
      "affaan-m/ECC:.agents/skills/agent-introspection-debugging/agents/openai.yaml",
      "affaan-m/ECC:.agents/skills/agent-sort/SKILL.md",
      "affaan-m/ECC:.agents/skills/agent-sort/agents/openai.yaml",
      "affaan-m/ECC:.agents/skills/api-design/SKILL.md",
      "affaan-m/ECC:.agents/skills/api-design/agents/openai.yaml",
      "affaan-m/ECC:.agents/skills/article-writing/SKILL.md",
      "affaan-m/ECC:.agents/skills/article-writing/agents/openai.yaml",
      "affaan-m/ECC:.agents/skills/backend-patterns/SKILL.md"
    ],
    "answer_language": "Chinese first; concise English aliases are allowed when they help tooling."
  },
  "expected_points": [
    "引用模式卡名称和来源 repo",
    "指出应改哪些层和不应改哪些层",
    "给出最小验证命令或人工检查点",
    "写出风险和下一步",
    "不能复制上游源码正文",
    "保留 source repo / path / license / policy",
    "输出要同时照顾中文小白、进阶用户、专业工程师"
  ],
  "deductions": [
    "只复述 README",
    "不引用证据路径",
    "直接要求训练模型",
    "没有验证标准",
    "声称已经训练出世界级模型但没有 eval",
    "把 metadata-only 或许可证不清内容当成可抽取正文"
  ],
  "validation_command": "python3 scripts/validate_repo_engineering_distillation.py",
  "judge_rubric": {
    "max_score": 1.0,
    "scoring": [
      {
        "points": 0.3,
        "criterion": "引用具体 repo/path/license/policy 证据"
      },
      {
        "points": 0.25,
        "criterion": "给出可执行工程步骤和明确非目标"
      },
      {
        "points": 0.2,
        "criterion": "包含测试、CI、eval 或人工验收标准"
      },
      {
        "points": 0.15,
        "criterion": "识别风险、反模式和适用边界"
      },
      {
        "points": 0.1,
        "criterion": "适合中文小白、进阶用户和专业工程师三层读者"
      }
    ]
  },
  "min_score": 0.78,
  "public_boundary": "Rubric-level eval only; no source bodies."
}
```

## Why This Matters

- 先知识库化,再任务化,再评测,最后才微调或 DPO。
- Pattern Card 先合并雷同来源,避免把相同 README 口号堆成噪声。
- Task/Eval 让 Windows GPU 节点可以批量跑本地模型,但质量由 rubric 和强模型/人工审查兜底。
- 所有资产都保留来源、路径、许可证和 public-safe 边界。

## Next GPU Work

1. 对 `eval_cases.jsonl` 跑本地 7B/14B/32B 模型基线。
2. 用 Codex/Claude 审 chosen/rejected,不要让小模型自我打分闭环。
3. 只有当 eval 能稳定区分好坏答案时,再把高质量 Task Card 转 SFT/LoRA 数据。

## Boundary

- 不复制源码正文。
- 不抽取 metadata-only 或许可证不清的正文。
- 不声称模型已经学会,除非 eval 真实跑过并留存分数。
