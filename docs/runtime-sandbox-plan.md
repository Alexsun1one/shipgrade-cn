# Runtime Sandbox Plan

Generated: 2026-05-25T22:53:12Z

Purpose: define exactly which upstream repos are worth executing, and how to run them without leaking local secrets or polluting the main machine.

## Hard Rules

- Run only repositories already allowed by `source_manifest.json` license policy.
- Run in a disposable sandbox, not the main login shell.
- Start with no API keys, no browser cookies, no SSH agent, no private key mount, and no inherited `.env`.
- Use `npm ci --ignore-scripts` first for Node projects; do not allow install lifecycle scripts until reviewed.
- Capture command, exit code, stdout/stderr tail, and what the result changes in the skill.

## github/spec-kit

- Local path: `$PROJECT:skills-cn-distill/sources/runtime_repos/github__spec-kit`
- Why run: source `69`, tests `87`, evals `0`, docs `134`, governance `7`.
- Current safe static smoke: `{"python_py_compile": {"files_checked": 40, "returncode": 0, "stderr_tail": ""}}`
- Candidate sandbox commands:

```bash
python -m compileall .
```
```bash
python -m pytest
```

- Skill-learning target: extract test/eval shape, command ergonomics, repo-local agent rules, and failure-mode handling; do not copy implementation code.

## microsoft/code-with-engineering-playbook

- Local path: `$PROJECT:skills-cn-distill/sources/runtime_repos/microsoft__code-with-engineering-playbook`
- Why run: source `0`, tests `61`, evals `1`, docs `359`, governance `15`.
- Current safe static smoke: `{}`
- Candidate sandbox commands:

```bash
find . -maxdepth 3 -type f | sort | sed -n '1,200p'
```

- Skill-learning target: extract test/eval shape, command ergonomics, repo-local agent rules, and failure-mode handling; do not copy implementation code.

## humanlayer/12-factor-agents

- Local path: `$PROJECT:skills-cn-distill/sources/runtime_repos/humanlayer__12-factor-agents`
- Why run: source `152`, tests `23`, evals `0`, docs `24`, governance `4`.
- Current safe static smoke: `{}`
- Candidate sandbox commands:

```bash
find . -maxdepth 3 -type f | sort | sed -n '1,200p'
```

- Skill-learning target: extract test/eval shape, command ergonomics, repo-local agent rules, and failure-mode handling; do not copy implementation code.

## promptfoo/promptfoo

- Local path: `$PROJECT:skills-cn-distill/sources/runtime_repos/promptfoo__promptfoo`
- Why run: source `1835`, tests `1452`, evals `509`, docs `924`, governance `114`.
- Current safe static smoke: `{"python_py_compile": {"files_checked": 40, "returncode": 0, "stderr_tail": ""}}`
- Candidate sandbox commands:

```bash
npm ci --ignore-scripts
```
```bash
npm test
```
```bash
npm run lint
```

- Skill-learning target: extract test/eval shape, command ergonomics, repo-local agent rules, and failure-mode handling; do not copy implementation code.

## UKGovernmentBEIS/inspect_ai

- Local path: `$PROJECT:skills-cn-distill/sources/runtime_repos/UKGovernmentBEIS__inspect_ai`
- Why run: source `845`, tests `579`, evals `104`, docs `1064`, governance `8`.
- Current safe static smoke: `{"python_py_compile": {"files_checked": 40, "returncode": 0, "stderr_tail": ""}}`
- Candidate sandbox commands:

```bash
python -m compileall .
```
```bash
python -m pytest
```

- Skill-learning target: extract test/eval shape, command ergonomics, repo-local agent rules, and failure-mode handling; do not copy implementation code.

## SuperClaude-Org/SuperClaude_Framework

- Local path: `$PROJECT:skills-cn-distill/sources/runtime_repos/SuperClaude-Org__SuperClaude_Framework`
- Why run: source `122`, tests `30`, evals `0`, docs `144`, governance `13`.
- Current safe static smoke: `{"python_py_compile": {"files_checked": 31, "returncode": 0, "stderr_tail": ""}}`
- Candidate sandbox commands:

```bash
npm run lint
```
```bash
python -m compileall .
```
```bash
python -m pytest
```

- Skill-learning target: extract test/eval shape, command ergonomics, repo-local agent rules, and failure-mode handling; do not copy implementation code.

## Yeachan-Heo/oh-my-claudecode

- Local path: `$PROJECT:skills-cn-distill/sources/runtime_repos/Yeachan-Heo__oh-my-claudecode`
- Why run: source `1207`, tests `2735`, evals `83`, docs `92`, governance `33`.
- Current safe static smoke: `{"python_py_compile": {"files_checked": 1, "returncode": 0, "stderr_tail": ""}}`
- Candidate sandbox commands:

```bash
npm ci --ignore-scripts
```
```bash
npm run test:run
```
```bash
npm run lint
```
```bash
npm run bench:prompts
```

- Skill-learning target: extract test/eval shape, command ergonomics, repo-local agent rules, and failure-mode handling; do not copy implementation code.
