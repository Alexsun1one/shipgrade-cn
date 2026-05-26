# Source Promotion Queue

This queue is the step after high-signal source discovery. It decides what deserves license review, deep-code analysis, or no-secret sandbox runtime work next.

## Snapshot

- generated at: `2026-05-25T23:53:42Z`
- radar candidates: `87`
- promotion rows: `87`
- next deep/sandbox: `17`
- manual license review: `42`
- metadata-only watchlist: `16`
- off-scope search noise: `8`

## Next Deep-Code / Sandbox Targets

| rank | repo | score | policy | status | distill value | next action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `affaan-m/ECC` | 378 | allow_extract | not_yet_deep_run | improve skill anatomy, progressive disclosure, examples, and installer ergonomics | clone sparse, inspect package/workflow/test topology, then run no-secret sandbox smoke |
| 2 | `addyosmani/agent-skills` | 353 | allow_extract | not_yet_deep_run | strengthen spec -> plan -> tasks -> implementation handoff | clone sparse, inspect package/workflow/test topology, then run no-secret sandbox smoke |
| 3 | `browser-use/browser-use` | 324 | allow_extract | not_yet_deep_run | improve skill anatomy, progressive disclosure, examples, and installer ergonomics | clone sparse, inspect package/workflow/test topology, then run no-secret sandbox smoke |
| 4 | `VoltAgent/awesome-agent-skills` | 323 | allow_extract | not_yet_deep_run | turn LLM quality into eval cases, red-team checks, and CI gates | clone sparse, inspect package/workflow/test topology, then run no-secret sandbox smoke |
| 5 | `obra/superpowers` | 314 | allow_extract | not_yet_deep_run | improve skill anatomy, progressive disclosure, examples, and installer ergonomics | clone sparse, inspect package/workflow/test topology, then run no-secret sandbox smoke |
| 6 | `wshobson/agents` | 305 | allow_extract | not_yet_deep_run | improve AGENTS/CLAUDE/Cursor portability without duplicating rules | clone sparse, inspect package/workflow/test topology, then run no-secret sandbox smoke |
| 7 | `alirezarezvani/claude-skills` | 304 | allow_extract | not_yet_deep_run | improve AGENTS/CLAUDE/Cursor portability without duplicating rules | clone sparse, inspect package/workflow/test topology, then run no-secret sandbox smoke |
| 8 | `promptfoo/promptfoo` | 296 | allow_extract | already_in_deep_code_case_studies | turn LLM quality into eval cases, red-team checks, and CI gates | consider upgrading from deep-code to disposable sandbox if package commands are stable |
| 9 | `openai/evals` | 291 | allow_extract | not_yet_deep_run | turn LLM quality into eval cases, red-team checks, and CI gates | clone sparse, inspect package/workflow/test topology, then run no-secret sandbox smoke |
| 10 | `karpathy/micrograd` | 282 | allow_extract | not_yet_deep_run | keep training/eval examples minimal, legible, and probe-driven | clone sparse, inspect package/workflow/test topology, then run no-secret sandbox smoke |
| 11 | `Shubhamsaboo/awesome-llm-apps` | 281 | allow_extract | not_yet_deep_run | improve skill anatomy, progressive disclosure, examples, and installer ergonomics | clone sparse, inspect package/workflow/test topology, then run no-secret sandbox smoke |
| 12 | `mattpocock/skills` | 274 | allow_extract | not_yet_deep_run | improve skill anatomy, progressive disclosure, examples, and installer ergonomics | clone sparse, inspect package/workflow/test topology, then run no-secret sandbox smoke |

## License Review Queue

| repo | stars | license | why | next action |
| --- | --- | --- | --- | --- |
| `openai/codex` | 85589 | Apache-2.0 | Authoritative Codex CLI and AGENTS.md-adjacent implementation surface; useful for agent rule contracts and validation ergonomics. | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `garrytan/gstack` | 102433 | MIT | Use Garry Tan's exact Claude Code setup: 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `msitarzewski/agency-agents` | 105048 | MIT | A complete AI agency at your fingertips - From frontend wizards to Reddit community ninjas, from whimsy injectors to reality checkers. Each agent is a specialized expert with personality, processes, and proven deliverables. | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `punkpeye/awesome-mcp-servers` | 87878 | MIT | A collection of MCP servers. | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `safishamsi/graphify` | 53687 | MIT | AI coding assistant skill (Claude Code, Codex, OpenCode, Cursor, Gemini CLI, and more). Turn any folder of code, SQL schemas, R scripts, shell scripts, docs, papers, images, or videos into a queryable knowledge graph. App code + database schema + infrastructure in one graph. | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `Priivacy-ai/spec-kitty` | 1262 | MIT | Spec-driven development loop with explicit artifact flow; useful as a fresh candidate for spec-first comparison. | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `sickn33/antigravity-awesome-skills` | 38682 | MIT | Antigravity skills discovery feeder; useful for broader skill-market taxonomy. | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `ultraworkers/claw-code` | 192496 | MIT | The repo is finally unlocked. enjoy the party! The fastest repo in history to surpass 100K stars ⭐. Join Discord: https://discord.gg/5TUQKqFWd Built in Rust using oh-my-codex. | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `bytedance/deer-flow` | 69534 | MIT | An open-source long-horizon SuperAgent harness that researches, codes, and creates. With the help of sandboxes, memories, tools, skill, subagents and message gateway, it handles different levels of tasks that could take minutes to hours. | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `farion1231/cc-switch` | 80688 | MIT | A cross-platform desktop All-in-One assistant for Claude Code, Codex, OpenCode, OpenClaw, Gemini CLI & Hermes Agent. Only official website: ccswitch.io | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `colbymchenry/codegraph` | 24837 | MIT | Pre-indexed code knowledge graph for Claude Code, Codex, Cursor, OpenCode, and Hermes Agent — fewer tokens, fewer tool calls, 100% local | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `paperclipai/paperclip` | 67619 | MIT | The open-source app everyone uses to manage agents at work | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `JuliusBrussee/caveman` | 64699 | MIT | 🪨 why use many token when few token do trick — Claude Code skill that cuts 65% of tokens by talking like caveman | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `jnMetaCode/agency-agents-zh` | 12918 | MIT | 🎭 211 个即插即用的 AI 专家角色 — 支持 Hermes Agent/Claude Code/Cursor/Copilot 等 16 种工具，覆盖工程/设计/营销/金融等 18 个部门。含 46 个中国市场原创智能体（小红书/抖音/微信/飞书/钉钉等） | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `microsoft/playwright` | 89397 | Apache-2.0 | Playwright is a framework for Web Testing and Automation. It allows testing Chromium, Firefox and WebKit with a single API.  | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `taishi-i/awesome-ChatGPT-repositories` | 3040 | CC0-1.0 | A curated list of resources dedicated to open source GitHub repositories related to ChatGPT, OpenAI API, and Codex. Searchable via Claude Code skills. | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `mem0ai/mem0` | 56698 | Apache-2.0 | Universal memory layer for AI Agents | verify LICENSE file and source boundaries; add to seed_sources only after review |
| `VoltAgent/awesome-design-md` | 84022 | MIT | A collection of DESIGN.md files analysis by popular brand design systems. Drop one into your project and let coding agents generate a matching UI. | verify LICENSE file and source boundaries; add to seed_sources only after review |

## Hard Rules

- Do not promote a repo because of stars alone.
- Do not extract body text until the repo has an explicit compatible license and source-policy review.
- Discovery indexes are taxonomy sources; each downstream repo still needs its own review.
- Sandbox execution is allowed only in disposable, no-secret environments.
- The promotion queue must feed concrete downstream work: source whitelist edits, deep-code case studies, or sandbox runtime cases.
