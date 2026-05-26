# Repository Engineering Distillation Pipeline

中文名: 仓库工程蒸馏流水线

ShipGrade CN 的核心目标不是让模型背代码,而是把优秀仓库里的工程判断沉淀成可检索、可评测、可训练、可人工审查的资产。

## One-Line Route

```text
Repository -> Engineering Knowledge -> Task Data -> Eval -> RAG / SFT / DPO
```

先 RAG / 知识库化,再做任务集和 eval,最后才考虑 SFT、LoRA 或 DPO。没有 eval,不要急着训练。

## What To Distill

### Repo Card

Repo Card 是仓库画像,回答“这个仓库是什么,为什么值得学,哪里值得迁移”。

```json
{
  "repo": "owner/name",
  "domain": "agent system / web framework / data pipeline",
  "language": ["TypeScript", "Python"],
  "architecture": "plugin-based / layered / event-driven",
  "entrypoints": ["src/main.ts", "server/app.py"],
  "important_dirs": {
    "core": "核心抽象",
    "adapters": "外部系统适配",
    "tests": "测试策略"
  },
  "build_commands": ["pnpm test", "pnpm build"],
  "design_strengths": ["模块边界清晰", "插件接口稳定", "测试夹具可复用"],
  "reuse_for": ["CLI 插件系统", "多 provider adapter 设计", "配置加载模式"]
}
```

### Pattern Card

Pattern Card 是工程模式卡,只抽象可迁移的设计,不复制实现代码。

```markdown
# Pattern: Provider Adapter Registry

## 适用场景
系统需要支持多个外部 provider,例如 OpenAI、Anthropic、local model、custom API。

## 问题
不同 provider 的鉴权、参数、错误格式、streaming 行为不一致。

## 解法
定义统一接口 ProviderAdapter,把 provider-specific 逻辑隔离到 adapter 层。

## 代码证据
- src/providers/base.ts
- src/providers/openai.ts
- tests/providers/*.test.ts

## 优点
- 新增 provider 不影响核心调度逻辑。
- 测试可以 mock adapter。
- 错误处理统一。

## 代价
- 初期抽象成本更高。
- 接口不稳定时会频繁调整。

## 适合迁移到我的项目吗
适合,如果系统也有多个模型、多个数据源或多个执行后端。
```

### Task Card

Task Card 把仓库知识转成工程判断任务,用于训练、检索增强或评测。

```json
{
  "task_type": "engineering_plan",
  "context": "项目已有 provider adapter 层,现在要新增 local vLLM provider。",
  "repo_context": [
    "src/providers/base.ts",
    "src/providers/openai.ts",
    "tests/providers/openai.test.ts"
  ],
  "expected_answer": {
    "plan_should_include": [
      "新增 LocalVLLMProvider",
      "复用 ProviderAdapter interface",
      "补 streaming 和 non-streaming 测试",
      "增加 baseURL/modelName 配置项",
      "不要改核心 scheduler"
    ],
    "bad_answer_patterns": [
      "直接在 scheduler 里硬编码 vLLM",
      "绕过 provider 抽象",
      "不补测试"
    ]
  }
}
```

### Eval

Eval 用来判断模型、agent、prompt 或 skill 是否真的学会了工程判断。每个 eval 至少要有:

- 输入。
- 期望点。
- 扣分点。
- 可执行测试命令或可检查证据。
- 人工或模型 judge rubric。

推荐 eval 类型:

| 类型 | 输入 | 期望输出 |
| --- | --- | --- |
| 规划类 | issue + repo map | 实现计划、边界、验证点 |
| Review 类 | diff + 相关结构 | 架构问题、测试缺口、兼容性风险 |
| Repair 类 | failing test + 相关代码 | 修复路径和最小补丁计划 |
| 迁移类 | 一个 repo 的设计模式 | 是否适合迁移,迁移到哪里,代价是什么 |
| 反模式识别 | 一段不良实现 | 为什么不适合,如何改回架构边界 |

## Machine Roles

| 机器 | 角色 |
| --- | --- |
| 主控 Mac / Codex | 整合、校验、README、发布包、Obsidian 写回。 |
| mac-alex / Claude Code | 并行审查、模式卡复核、规划模板和文档质量检查。 |
| win-awesun / GPU | repo indexing、embedding、本地模型批跑、LoRA/SFT/DPO、eval 跑分。 |

## Source Selection

第一批不要超过 20 个仓库。优先选择:

1. 技术栈接近。
2. tests 清晰。
3. CI 清晰。
4. 有 docs、ADR 或 design docs。
5. commit history 比较干净。
6. issue / PR 讨论质量高。
7. license 明确。
8. 不是纯 demo。

不要只按 star 选仓库。高 star 只能说明传播,不能自动说明设计值得迁移。

## License Boundary

训练、再分发或商用前必须过滤 license。没有明确许可证的仓库只能做 metadata-only 记录,不能复制正文、代码或派生内容。

Reference links:

- GitHub licensing guide: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository
- OpenAI evals guide: https://platform.openai.com/docs/guides/evals

## Pipeline Commands In This Repo

```bash
python3 scripts/collect_sources.py
python3 scripts/fetch_curated_artifacts.py
python3 scripts/analyze_repo_structure.py
python3 scripts/analyze_source_overlap.py
python3 scripts/build_seed_pack.py
python3 scripts/build_teacher_dataset.py
python3 scripts/build_sft_dataset.py
python3 scripts/validate_outputs.py
python3 scripts/validate_training_data.py
python3 scripts/validate_sft_dataset.py
```

Runtime and promotion lanes:

```bash
python3 scripts/discover_high_signal_sources.py
python3 scripts/build_source_promotion_queue.py
python3 scripts/run_source_promotion_batch.py
python3 scripts/run_source_promotion_sandbox_cases.py
python3 scripts/analyze_deep_code_case_studies.py
python3 scripts/build_repo_engineering_distillation.py
python3 scripts/validate_repo_engineering_distillation.py
```

Current generated assets: 11 Repo Cards / 15 Pattern Cards / 90 Task Cards / 90 Eval Cases.

## Hard Rule

如果一个产物不能指出来源、文件证据、设计取舍、验证方式和许可证边界,它就不是合格蒸馏结果。
