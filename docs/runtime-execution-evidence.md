# Runtime Execution Evidence

Generated: 2026-05-25

Purpose: record what was actually executed after the selective runtime audit, without pretending that every upstream repo has been fully tested.

Current status: this early execution record is superseded by `outputs/sandbox_runtime_cases.md`, which now proves a hydrated temporary sandbox for both `Yeachan-Heo/oh-my-claudecode` and `SuperClaude-Org/SuperClaude_Framework`.

## Executed Checks

| repo | command | result | meaning |
| --- | --- | --- | --- |
| `Yeachan-Heo/oh-my-claudecode` | `npm ci --ignore-scripts --dry-run --prefer-offline --no-audit --fund=false` | exit `0`; npm planned `318` packages; `node_modules` was not created | Dependency graph and lockfile are runnable enough for a future sandbox test, without running install lifecycle scripts. |
| `Yeachan-Heo/oh-my-claudecode` | `npm pkg get scripts dependencies devDependencies` | exit `0`; found `test:run`, `lint`, `bench:prompts`, multi-stage build scripts, 12 runtime deps and 14 dev deps | This repo has real executable validation surfaces: Vitest tests, prompt benchmarks, lint, build pipeline. |
| `SuperClaude-Org/SuperClaude_Framework` | `git ls-files` / package metadata inspection | exit `0`; tree shows `src`, `tests`, `.github`, `docs`, `AGENTS.md`, `CLAUDE.md`, `SECURITY.md`, `CONTRIBUTING.md` | Strong repo-shape signal; follow-up sandbox materialized `src/tests/plugins/scripts` and passed selected pytest tests. |

## Failed / Deferred Checks

| repo | attempted check | result | decision |
| --- | --- | --- | --- |
| `github/spec-kit` | refresh sparse clone | GitHub HTTPS timeout after about 75s | Keep API/tree evidence; retry clone later, do not block current skill improvement. |
| `SuperClaude-Org/SuperClaude_Framework` | early hydrate `src/tests/docs` sparse checkout | GitHub HTTPS timeout after about 75s | Superseded by later git-archive materialization in `outputs/sandbox_runtime_cases.md`; the later run passed editable install and selected pytest tests. |

## Skill Lessons

- Running everything is not the quality maximum; choosing what to run is part of the engineering skill.
- A repo earns runtime priority when it has tests/evals/benchmarks, package scripts, examples, and governance files, not merely a persuasive README.
- Safe runtime validation starts with `--ignore-scripts`, dry runs, static checks, and explicit logs before any arbitrary lifecycle script is allowed.
- If network or dependency hydration fails, preserve the evidence as a boundary instead of hallucinating that tests passed.
