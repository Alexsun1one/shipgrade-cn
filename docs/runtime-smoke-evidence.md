# Runtime Smoke Evidence

Generated: 2026-05-25T23:25:35Z

This report extends the earlier runtime audit with low-side-effect checks on cloned source trees. It intentionally avoids dependency install lifecycle scripts, secrets, auth state, and private source.

## Checks

| repo | check | exit | evidence | lesson |
| --- | --- | ---: | --- | --- |
| `SuperClaude-Org/SuperClaude_Framework` | `tree_inventory` | `0` | files=409, tests=30, evals_or_benchmarks=0, ci=6, docs=138 | Structure first: count tests/evals/CI/docs before deciding whether runtime execution is worth the risk. |
| `SuperClaude-Org/SuperClaude_Framework` | `npm_metadata` | `0` | scripts=[lint, postinstall, test, update], deps=0, devDeps=0 | Package metadata exposes the real validation surface without running install scripts. |
| `SuperClaude-Org/SuperClaude_Framework` | `python_py_compile` | `0` | files_checked=40 | Syntax-only checks are useful smoke tests because they do not import dependencies or execute app code. |
| `SuperClaude-Org/SuperClaude_Framework` | `make_dry_run` | `0` | echo "🔧 Installing SuperClaude Framework (development mode)..." uv pip install -e ".[dev]" echo "" echo "✅ Installation complete!" echo "   Run 'make verify' to check installation" | A dry-run Makefile is enough to learn command topology; full execution still belongs in a sandbox. |
| `UKGovernmentBEIS/inspect_ai` | `tree_inventory` | `0` | files=1725, tests=579, evals_or_benchmarks=104, ci=9, docs=197 | Structure first: count tests/evals/CI/docs before deciding whether runtime execution is worth the risk. |
| `UKGovernmentBEIS/inspect_ai` | `python_py_compile` | `0` | files_checked=40 | Syntax-only checks are useful smoke tests because they do not import dependencies or execute app code. |
| `UKGovernmentBEIS/inspect_ai` | `make_dry_run` | `0` | pre-commit install  | A dry-run Makefile is enough to learn command topology; full execution still belongs in a sandbox. |
| `Yeachan-Heo/oh-my-claudecode` | `tree_inventory` | `0` | files=5621, tests=2735, evals_or_benchmarks=83, ci=7, docs=80 | Structure first: count tests/evals/CI/docs before deciding whether runtime execution is worth the risk. |
| `Yeachan-Heo/oh-my-claudecode` | `npm_metadata` | `0` | scripts=[bench:prompts, bench:prompts:compare, bench:prompts:save, build, build:bridge, build:bridge-entry, build:cli, build:runtime-cli], deps=12, devDeps=14 | Package metadata exposes the real validation surface without running install scripts. |
| `github/spec-kit` | `tree_inventory` | `0` | files=319, tests=87, evals_or_benchmarks=0, ci=13, docs=37 | Structure first: count tests/evals/CI/docs before deciding whether runtime execution is worth the risk. |
| `github/spec-kit` | `python_py_compile` | `0` | files_checked=40 | Syntax-only checks are useful smoke tests because they do not import dependencies or execute app code. |
| `humanlayer/12-factor-agents` | `tree_inventory` | `0` | files=499, tests=22, evals_or_benchmarks=0, ci=0, docs=22 | Structure first: count tests/evals/CI/docs before deciding whether runtime execution is worth the risk. |
| `humanlayer/12-factor-agents` | `npm_metadata` | `0` | scripts=[build, dev], deps=6, devDeps=6 | Package metadata exposes the real validation surface without running install scripts. |
| `humanlayer/12-factor-agents` | `npm_metadata` | `0` | scripts=[test, test:watch], deps=6, devDeps=3 | Package metadata exposes the real validation surface without running install scripts. |
| `humanlayer/12-factor-agents` | `npm_metadata` | `0` | scripts=[build, dev], deps=3, devDeps=4 | Package metadata exposes the real validation surface without running install scripts. |
| `humanlayer/12-factor-agents` | `npm_metadata` | `0` | scripts=[build, dev], deps=5, devDeps=6 | Package metadata exposes the real validation surface without running install scripts. |
| `humanlayer/12-factor-agents` | `npm_metadata` | `0` | scripts=[build, dev], deps=2, devDeps=4 | Package metadata exposes the real validation surface without running install scripts. |
| `humanlayer/12-factor-agents` | `npm_metadata` | `0` | scripts=[build, dev], deps=3, devDeps=4 | Package metadata exposes the real validation surface without running install scripts. |
| `humanlayer/12-factor-agents` | `npm_metadata` | `0` | scripts=[build, dev], deps=3, devDeps=4 | Package metadata exposes the real validation surface without running install scripts. |
| `humanlayer/12-factor-agents` | `npm_metadata` | `0` | scripts=[build, dev], deps=3, devDeps=4 | Package metadata exposes the real validation surface without running install scripts. |
| `humanlayer/12-factor-agents` | `make_dry_run` | `0` | echo "Setting up project..." npm install // bun install // yarn install echo "Setup complete!"  | A dry-run Makefile is enough to learn command topology; full execution still belongs in a sandbox. |
| `microsoft/code-with-engineering-playbook` | `tree_inventory` | `0` | files=391, tests=61, evals_or_benchmarks=1, ci=3, docs=359 | Structure first: count tests/evals/CI/docs before deciding whether runtime execution is worth the risk. |
| `microsoft/code-with-engineering-playbook` | `npm_metadata` | `0` | scripts=[], deps=2, devDeps=0 | Package metadata exposes the real validation surface without running install scripts. |
| `promptfoo/promptfoo` | `tree_inventory` | `0` | files=5248, tests=1451, evals_or_benchmarks=509, ci=11, docs=307 | Structure first: count tests/evals/CI/docs before deciding whether runtime execution is worth the risk. |
| `promptfoo/promptfoo` | `npm_metadata` | `0` | scripts=[build, dev, package, test, tsc, tsc:watch], deps=5, devDeps=4 | Package metadata exposes the real validation surface without running install scripts. |
| `promptfoo/promptfoo` | `npm_metadata` | `0` | scripts=[test], deps=1, devDeps=3 | Package metadata exposes the real validation surface without running install scripts. |
| `promptfoo/promptfoo` | `npm_metadata` | `0` | scripts=[test], deps=1, devDeps=0 | Package metadata exposes the real validation surface without running install scripts. |
| `promptfoo/promptfoo` | `npm_metadata` | `0` | scripts=[server], deps=3, devDeps=0 | Package metadata exposes the real validation surface without running install scripts. |
| `promptfoo/promptfoo` | `npm_metadata` | `0` | scripts=[eval, eval-schema, view], deps=3, devDeps=2 | Package metadata exposes the real validation surface without running install scripts. |
| `promptfoo/promptfoo` | `npm_metadata` | `0` | scripts=[test, test:jest, test:vitest], deps=0, devDeps=5 | Package metadata exposes the real validation surface without running install scripts. |
| `promptfoo/promptfoo` | `npm_metadata` | `0` | scripts=[], deps=2, devDeps=0 | Package metadata exposes the real validation surface without running install scripts. |
| `promptfoo/promptfoo` | `npm_metadata` | `0` | scripts=[eval, view], deps=2, devDeps=0 | Package metadata exposes the real validation surface without running install scripts. |
| `promptfoo/promptfoo` | `python_py_compile` | `0` | files_checked=24 | Syntax-only checks are useful smoke tests because they do not import dependencies or execute app code. |

## Distillation Moves

- Do not treat a persuasive README as proof. A strong repo must reveal how it tests, evaluates, releases, and handles failures.
- Prefer no-install metadata and syntax checks before running upstream code.
- Convert runtime evidence into ShipGrade gates: command topology, proof files, expected exit codes, and clear deferred boundaries.
- If a check fails or is dry-run only, record the boundary. That honesty is part of the skill.
