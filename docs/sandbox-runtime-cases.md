# Sandbox Runtime Cases

Generated: 2026-05-25T23:26:57Z

This evidence is produced in temporary copies with scrubbed environments. It does not mount user secrets, cookies, sessions, browser profiles, SSH keys, private keys, API tokens, or private project source.

## Summary

- cases: `3/3` passed
- steps: `12/12` passed
- temp_copy: `copy source to TemporaryDirectory; exclude .git, node_modules, .venv, __pycache__, .DS_Store, AppleDouble files; materialize selected public git paths without copying .git`
- env: `scrub env to PATH/system temp only; set HOME and tool caches to temp; no token/key/secret/cookie/session variables`

## Case: oh-my-claudecode-typescript-agent

- source: `Yeachan-Heo/oh-my-claudecode`
- runtime: `node/vitest/typescript`
- materialized paths: `package.json, src, agents, benchmarks, scripts, package-lock.json, tsconfig.json, vitest.config.ts`
- configured test discovery: `549` via `src/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}`

| step | command | exit | evidence |
| --- | --- | ---: | --- |
| npm-package-metadata | `npm pkg get scripts dependencies devDependencies` | `0` | {   "scripts": {     "build": "tsc && node scripts/build-skill-bridge.mjs && node scripts/build-mcp-server.mjs && node scripts/build-bridge-entry.mjs && npm run compose-docs && npm run build:runtime-cli && npm run build:team-server && npm run build:cli",     " |
| npm-ci-ignore-scripts | `npm ci --ignore-scripts --prefer-offline --no-audit --fund=false` | `0` |  added 318 packages in 16s  |
| typescript-noemit | `npx tsc --noEmit --pretty false` | `0` |  |
| vitest-configured-tests | `npx vitest run src/__tests__/agent-boundary-guidance.test.ts src/__tests__/agent-registry.test.ts src/__tests__/artifact-descriptor-handoff.test.ts` | `0` |   RUN  v4.0.18 $SANDBOX/oh-my-claudecode   ✓ src/__tests__/artifact-descriptor-handoff.test.ts (4 tests) 499ms  ✓ src/__tests__/agent-boundary-guidance.test.ts (3 tests) 6ms  ✓ src/__tests__/agent-registry.test.ts (12 tests) 76ms   Test Files  3 passed (3)     |

Distilled lesson: Agent skill repos need both source hydration and prompt/resource hydration; tests can fail falsely if prompts or agents are not materialized.

## Case: superclaude-python-pytest

- source: `SuperClaude-Org/SuperClaude_Framework`
- runtime: `python/pytest/uv`
- materialized paths: `src, tests, plugins, scripts, pyproject.toml, setup.py`
- configured test discovery: `25` via `tests/unit/test_confidence.py, tests/unit/test_token_budget.py`

| step | command | exit | evidence |
| --- | --- | ---: | --- |
| python-py-compile-selected | `python3 -m py_compile src/superclaude/cli/main.py src/superclaude/pm_agent/confidence.py src/superclaude/pm_agent/token_budget.py src/superclaude/execution/parallel.py tests/unit/test_confidence.py tests/unit/test_token_budget.py` | `0` |  |
| uv-venv-temp | `uv venv $SANDBOX/venv-superclaude` | `0` | Using CPython 3.14.3 interpreter at: /opt/homebrew/opt/python@3.14/bin/python3.14 Creating virtual environment at: $SANDBOX/venv-superclaude  |
| uv-pip-install-editable-test | `uv pip install --python $SANDBOX/venv-superclaude/bin/python -e .[test]` | `0` | Using Python 3.14.3 environment at: $SANDBOX/venv-superclaude Resolved 14 packages in 3.09s    Building superclaude @ file://$SANDBOX/superclaude Downloading pygments (1.2MiB) Downloading numpy (5.0MiB) Downloading scipy (19.4MiB)  Downloaded pygments  Downloa |
| pytest-selected-unit-tests | `$SANDBOX/venv-superclaude/bin/python -m pytest tests/unit/test_confidence.py tests/unit/test_token_budget.py -q --tb=short` | `0` | ============================= test session starts ============================== platform darwin -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0 SuperClaude: 4.3.0 rootdir: $SANDBOX/superclaude configfile: pyproject.toml plugins: cov-7.1.0, superclaude-4.3.0 coll |

Distilled lesson: Python skill frameworks need packaging-resource hydration (`plugins/` in this case), not just `src/` and `tests/`, before editable install evidence is meaningful.

## Case: spec-kit-python-sdd-cli

- source: `github/spec-kit`
- runtime: `python/pytest/spec-driven-cli`
- materialized paths: `pyproject.toml, src, tests/test_cli_version.py, tests/test_console_imports.py, tests/test_version_imports.py, tests/test_utils_assets_imports.py, templates`
- configured test discovery: `16` via `tests/test_cli_version.py, tests/test_console_imports.py, tests/test_version_imports.py, tests/test_utils_assets_imports.py`

| step | command | exit | evidence |
| --- | --- | ---: | --- |
| python-py-compile-spec-kit-selected | `python3 -m py_compile src/specify_cli/__init__.py src/specify_cli/_assets.py src/specify_cli/_console.py src/specify_cli/agents.py tests/test_cli_version.py tests/test_console_imports.py tests/test_version_imports.py tests/test_utils_assets_imports.py` | `0` |  |
| uv-venv-temp-spec-kit | `uv venv $SANDBOX/venv-spec-kit` | `0` | Using CPython 3.14.3 interpreter at: /opt/homebrew/opt/python@3.14/bin/python3.14 Creating virtual environment at: $SANDBOX/venv-spec-kit  |
| uv-pip-install-runtime-test-deps | `uv pip install --python $SANDBOX/venv-spec-kit/bin/python pytest>=7.0 typer>=0.24.0 click>=8.2.1 rich platformdirs readchar pyyaml>=6.0 packaging>=23.0 pathspec>=0.12.0 json5>=0.13.0` | `0` | Using Python 3.14.3 environment at: $SANDBOX/venv-spec-kit Resolved 17 packages in 3.51s Downloading pygments (1.2MiB)  Downloaded pygments Prepared 17 packages in 1.51s Installed 17 packages in 18ms  + annotated-doc==0.0.4  + click==8.4.1  + iniconfig==2.3.0  |
| pytest-spec-kit-import-assets | `$SANDBOX/venv-spec-kit/bin/python -m pytest tests/test_cli_version.py tests/test_console_imports.py tests/test_version_imports.py tests/test_utils_assets_imports.py -q --tb=short` | `0` | ============================= test session starts ============================== platform darwin -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0 rootdir: $SANDBOX/spec-kit configfile: pyproject.toml collected 16 items  tests/test_cli_version.py ......             |

Distilled lesson: Spec-first CLI repos need asset/import/version tests that prove templates and agent integrations are package-visible before heavier command execution.

## Distilled Lesson

- Runtime proof should start with dependency graph and package-script reality, then graduate to representative tests only when sandbox hydration is clean.
- `--ignore-scripts` is a hard default for untrusted Node repos; Python editable installs must use disposable virtualenvs and temp caches.
- Sparse/blobless clones are not enough for runtime proof. The sandbox must materialize the source, tests, and runtime resources that upstream tests actually require.
- A failed install, missing resource, or timed-out test is still useful evidence when it is recorded as a boundary instead of being hidden.
