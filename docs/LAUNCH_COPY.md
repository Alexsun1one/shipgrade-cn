# Launch Copy

Use this when publishing ShipGrade CN. Keep the promise sharp: this is not a prompt pack; it is a verified engineering workflow for Chinese agent users.

## GitHub Release Title

ShipGrade CN v0.1 - 中文 AI 工程交付系统

## GitHub Release Body

ShipGrade CN turns vague Chinese requests into verifiable engineering delivery for Codex, Claude Code, Cursor, and multi-agent teams. It is for people who are tired of "looks done" and want files, tests, evidence, and handoff.

What is inside:

- `shipgrade_init.py`: creates `.shipgrade/` and wires AGENTS/CLAUDE/Cursor rules into the target project.
- `shipgrade_init.py --pattern`: starts the project from a distilled engineering pattern instead of a blank brief.
- `shipgrade_doctor.py`: rejects fake completion unless there is a concrete artifact and command/browser evidence.
- Evidence backbone: 88 repo structure scans, 11 repos / 17649 files / 5381 test paths / 786 eval paths, 3/3 cases / 13/13 required steps / 264 configured upstream tests (`affaan-m/ECC`, `browser-use/browser-use`, `addyosmani/agent-skills`), and 3/3 cases and 12/12 steps across `Yeachan-Heo/oh-my-claudecode`, `SuperClaude-Org/SuperClaude_Framework`, `github/spec-kit`, with 590 configured upstream tests discovered.
- Public release kit: CI, license/notice/security/contributing, issue templates, publish preflight, staging script, and release package.

Run:

```bash
python3 tools/shipgrade_demo.py
python3 tools/shipgrade_init.py /tmp/my-project --pattern command_topology_quality_gate
python3 tools/github_publish_preflight.py --write-docs --run-verify
python3 tools/shipgrade_verify.py
```

Known boundary: v0.1 is a strong artifact, not market proof. Stars, issues, and user transcripts come next.

## V2EX / 即刻 Short Post

我做了一个中文 AI 工程 skill: ShipGrade CN。

它不是提示词合集,而是把“我想让 AI 帮我改点东西”压成一套可交付流程: 目标、非目标、证据、验收、风险、最小改动、验证、handoff。初始化后会直接接线 AGENTS/CLAUDE/Cursor,不是只给你一份说明书。

三个硬证据: doctor 会拒绝假完成; 11 个 deep-code case study; sandbox 真实安装/测试了 ECC 和 browser-use。

适合三类人: 中文小白能开工,进阶用户能养成验证习惯,专业工程师能审 provenance 和质量边界。欢迎 star、安装、跑 demo,然后拿你的真实项目来打它。

## One-Line English

ShipGrade CN is a Chinese engineering skill for Codex, Claude Code, and Cursor that turns vague requests into verifiable delivery.
