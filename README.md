# ShipGrade CN

> 给 Codex、Claude Code、Cursor 用的中文工程交付技能包: 把一句模糊需求变成可执行、可验证、可接手的交付流程。

英文版: [README.en.md](README.en.md)

[![本地验证](https://img.shields.io/badge/本地验证-shipgrade__verify.py-2ea44f)](#发布前自检)
[![适用工具](https://img.shields.io/badge/适用-Codex%20%7C%20Claude%20Code%20%7C%20Cursor-111827)](START_HERE.md)
[![代码许可证](https://img.shields.io/badge/代码-MIT-blue)](LICENSE.md)
[![文档许可证](https://img.shields.io/badge/文档-CC%20BY%204.0-blue)](NOTICE.md)

![ShipGrade CN hero](assets/shipgrade-hero-cn.png)

## 这是什么

ShipGrade CN 是一套仓库工程蒸馏流水线和中文 AI 编程助手交付技能包。它不是提示词合集,也不是把英文最佳实践翻译一遍。它解决一个很常见的问题:

> 你对 AI 说“帮我把这个弄好”,它回你“好了”,但你不知道它到底改了什么、验证了什么、哪里还能接着干。

ShipGrade CN 会把这种口语需求压成五件事:

1. 目标: 这次到底要交付什么。
2. 非目标: 哪些东西这次不碰。
3. 证据: 当前有什么文件、日志、截图、命令输出或外部来源。
4. 验收: 什么结果才算完成。
5. 接手: 下一位 agent 或未来的你怎么继续。

## 仓库工程蒸馏流水线

ShipGrade CN 的核心路线不是“把一堆 repo 直接塞给模型训练”。更合适的方法是:

```text
Repo -> 工程知识 -> 任务数据 -> 评测 -> RAG / SFT / DPO
```

先知识库化,再构建任务集和评测集,最后才考虑微调。模型不应该背代码,而应该学习工程判断:

- 这个仓库为什么这样分层。
- 模块边界怎么定。
- 新增功能应该从哪里切入。
- 测试应该补在哪里。
- 哪些设计值得迁移。
- 哪些坑应该避免。

完整方法论见 `docs/repository-engineering-distillation-pipeline.md`。

![仓库工程蒸馏流水线](assets/shipgrade-proof-map-cn.png)

## 30 秒看懂差异

```bash
python3 tools/shipgrade_demo.py
```

你会看到一个完整闭环:

- 初始化一个临时项目。
- 生成 `.shipgrade/` 工作台、`AGENTS.md`、`CLAUDE.md` 和 Cursor 规则。
- 拒绝“看起来好了”的假完成。
- 接受包含文件路径、命令证据、来源边界、安全边界和下一步的合格交付说明。

```text
shipgrade-demo-ok
fake_rejection=... ship-grade-fail vague_or_unverified_language ...
accepted=... ship-grade-ok
```

演示证据在 `docs/DEMO_PROOF.md`,动画在下面这张图里。

![ShipGrade CN demo](assets/shipgrade-demo.gif)

## 5 分钟装进你的项目

要求: Python 3.10+。不需要 API key,不需要联网。

```bash
python3 tools/shipgrade_init.py /path/to/your-project
cd /path/to/your-project
sed -n '1,160p' .shipgrade/task-brief.md
sed -n '1,160p' AGENTS.md
```

然后按这个顺序用:

1. 在 `.shipgrade/task-brief.md` 填清楚目标、非目标、验收标准和风险边界。
2. 让 Codex、Claude Code 或 Cursor 读取项目规则,按 ShipGrade 流程工作。
3. 交付前把结果写进 `.shipgrade/handoff.md`。
4. 用质量检查器检查交付说明是不是有证据。

```bash
python3 tools/shipgrade_doctor.py .shipgrade/handoff.md
```

如果要装成 Codex skill:

```bash
python3 tools/install_skill.py --force
```

## 它会生成什么

```text
.shipgrade/
  task-brief.md       # 把口语需求压成目标、非目标、证据、验收和第一刀
  quality-gate.md     # 每次交付前必须过的质量门
  handoff.md          # 下一位 agent 或未来自己的接手入口
  AGENTS.snippet.md   # 可追加到项目 AGENTS.md 的规则片段
AGENTS.md             # ShipGrade 托管规则块,给 Codex 读
CLAUDE.md             # ShipGrade 托管规则块,给 Claude Code 读
CLAUDE.shipgrade.md   # Claude Code 的独立协作说明
.cursor/rules/shipgrade.mdc
```

![ShipGrade terminal demo](assets/shipgrade-terminal-demo.png)

## 四类蒸馏资产

ShipGrade CN 真正产出的不是代码复制件,而是四类可以被检索、评测、训练和人工审查的工程资产:

| 资产 | 作用 |
| --- | --- |
| Repo Card（仓库画像） | 记录领域、语言、架构、入口、目录、命令、强项和适用迁移场景。 |
| Pattern Card（工程模式卡） | 记录适用场景、问题、解法、证据、优点、代价和迁移判断。 |
| Task Card（任务卡） | 给模型或 AI 编程助手使用的规划、审查、修复、迁移和反模式识别任务。 |
| Eval（评测集） | 记录输入、期望点、扣分点、命令、人工或模型裁判标准。 |

![四类蒸馏资产](assets/shipgrade-audience-cn.png)

## 怎么用

### 给中文小白

你只需要填 `.shipgrade/task-brief.md`,把“我要什么”和“怎样算完成”写清楚。之后让 AI 读项目规则,它就会按目标、验证、交付说明的方式干活,不是随口说“已完成”。

### 给进阶用户

把 ShipGrade 当成项目工作台。每次开工先写 brief,做完跑测试或检查,最后写 handoff。这样 Codex、Claude Code、Cursor 之间不会各说各话。

### 给专业工程师

你可以审它的规则、来源、许可证、验证命令、发布前检查和证据索引。它不是要求你相信一个 README,而是把每条关键 claim 都落到文件、命令或报告里。

## 里面有什么

| 路径 | 用途 |
| --- | --- |
| `SKILL.md` | AI 编程助手真正会读取的核心技能说明。 |
| `START_HERE.md` | 第一次打开项目时的路线图。 |
| `tools/shipgrade_init.py` | 给任意项目生成 `.shipgrade/`、`AGENTS.md`、`CLAUDE.md` 和 Cursor 规则。 |
| `tools/shipgrade_doctor.py` | 检查交付说明是否包含结果、验证、来源、风险、安全边界和接手入口。 |
| `tools/shipgrade_demo.py` | 30 秒演示初始化、拒绝假完成、接受合格交付。 |
| `tools/github_publish_preflight.py` | 发布前检查 README、证据、模板、工作流、图片和安全边界。 |
| `docs/repository-engineering-distillation-pipeline.md` | 仓库画像、工程模式卡、任务卡、评测集的工程蒸馏方法论。 |
| `docs/EVIDENCE_INDEX.md` | 所有公开 claim 对应到哪些证据文件。 |
| `docs/source-depth-dossier.md` | 信源不是只看 README,而是看结构、脚本、测试、命令和 agent 入口。 |
| `docs/deep-code-case-studies.md` | 对高信源项目的代码级案例研究。 |
| `docs/source-promotion-sandbox-cases.md` | 候选项目进入临时沙箱后的真实运行记录。 |
| `docs/LAUNCH_COPY.md` | 发布文案和首发说明。 |

## 工作流结构

![ShipGrade CN workflow](assets/shipgrade-loop.png)

1. 需求进入: 先把口语需求变成 brief。
2. 规则接线: 让 Codex、Claude Code、Cursor 都看到同一套质量门。
3. 最小交付: 只做当前目标需要的最小正确改动。
4. 证据验证: 用测试、构建、浏览器冒烟检查、日志或人工检查证明结果。
5. 接手沉淀: 写 handoff,保留下一步、风险和验证结果。

## 为什么不是提示词合集

| 问题 | ShipGrade CN 怎么回答 |
| --- | --- |
| 新手能不能用 | 可以。先跑 `shipgrade_init.py`,再填 `.shipgrade/task-brief.md`。 |
| 初始化后 agent 真能看到吗 | 可以。默认接入 `AGENTS.md`、`CLAUDE.md` 和 Cursor rule。 |
| 会不会放过假完成 | 不会只看好听的话。doctor 要求具体产物路径和命令或浏览器证据。 |
| 是不是只抓 README | 不是。先做仓库画像、工程模式卡、任务卡、评测集,结构扫描覆盖 88 个仓库,代码级案例研究覆盖 11 个仓库。 |
| 有没有真实运行 | 有。临时沙箱记录覆盖 `affaan-m/ECC`、`browser-use/browser-use`、`addyosmani/agent-skills`。 |
| 能不能发布 | 可以。仓库内有发布前检查、GitHub Actions、模板、许可证、发布包和校验脚本。 |

## 证据快照

- 信源总数: 103
- 抽取产物: 128
- 仓库结构扫描: 88
- 高信号信源雷达: 87 candidates / 64 new / 65 green-license / 8 off-scope search-noise
- 信源晋级队列: 87 rows / 12 next deep-sandbox / 18 license-review targets
- 信源批量审计: 4 selected / 4 audited / 2 runtime candidates / 2 static smoke passed (`affaan-m/ECC`, `addyosmani/agent-skills`, `browser-use/browser-use`, `VoltAgent/awesome-agent-skills`)
- 晋级信源沙箱: 3/3 cases / 13/13 required steps / 264 configured upstream tests (`affaan-m/ECC`, `browser-use/browser-use`, `addyosmani/agent-skills`)
- 代码级案例研究: 11 repos / 17649 files / 5381 test paths / 786 eval paths
- 评测任务: 12
- 运行冒烟检查: 33 passed checks / 33 checks on 7 cloned repos
- 沙箱运行矩阵: 3/3 cases and 12/12 steps across `Yeachan-Heo/oh-my-claudecode`, `SuperClaude-Org/SuperClaude_Framework`, `github/spec-kit`, with 590 configured upstream tests discovered
- 真实项目 gauntlet: 5/5
- 交付记录证据: 2/2
- GitHub 发布前检查: 已内置本地报告

## 吸收了谁的经验

ShipGrade CN 吸收的是工程结构,不是名人光环:

- Karpathy 系列训练仓库: 极简、可复现、指标和探针。
- Google engineering practices/styleguide: review、可维护性和团队一致性。
- GitHub Spec Kit / OpenSpec / Agent OS: spec-first、任务化、验收化。
- Matt Pocock skills: 面向真实工程师的 skill 组织方式。
- OpenAI / Anthropic cookbooks: recipe、eval 和失败模式。
- promptfoo / DeepEval: 把模型质量变成可评测对象。
- Cline / Gemini CLI / opencode / Continue / browser-use: 真实 agent 产品工作流。
- Microsoft playbook / Rust RFCs / Kubernetes KEPs / OpenTelemetry spec: 设计前文档和阶段门。

## 资料地图

- 快速入口: `START_HERE.md`
- 证据索引: `docs/EVIDENCE_INDEX.md`
- 蒸馏流水线: `docs/repository-engineering-distillation-pipeline.md`
- 信源地图: `docs/source-attribution.md`
- 深度研究: `docs/source-depth-dossier.md`
- 代码案例: `docs/deep-code-case-studies.md`
- 运行证据: `docs/runtime-smoke-evidence.md`、`docs/sandbox-runtime-cases.md`
- 晋级队列: `docs/high-signal-source-radar.md`、`docs/source-promotion-queue.md`、`docs/source-promotion-batch.md`
- 发布检查: `docs/GITHUB_PUBLISH_PREFLIGHT.md`
- 演示证明: `docs/DEMO_PROOF.md`
- 路线图: `docs/ROADMAP.md`

## 发布前自检

```bash
python3 tools/github_publish_preflight.py --write-docs --run-verify
python3 tools/shipgrade_verify.py
python3 scripts/create-public-stage.py /tmp/shipgrade-cn-public
bash scripts/verify.sh
bash scripts/package.sh
```

## 安全边界

ShipGrade CN 不接收、不训练、不发布:

- secret、token、API key、private key
- cookie、browser profile、auth database、session database
- 私有仓库正文
- 泄漏源码、泄漏提示词、系统提示词归档
- 许可证不清的正文搬运

## 发布信息

- 推荐仓库名: `shipgrade-cn`
- 推荐描述: `中文工程 skill for Codex / Claude Code / Cursor: turn vague Chinese requests into verifiable engineering delivery.`
- 推荐社交预览图: `assets/shipgrade-hero-cn.png`
- 推荐主题标签: 见 `.github/repo-metadata.json`

## 许可证

- `tools/` 中的代码: MIT
- 文档、模板、示例、评测和 skill 内容: CC BY 4.0
- 详见 `LICENSE.md`、`NOTICE.md`、`docs/source-attribution.md`
