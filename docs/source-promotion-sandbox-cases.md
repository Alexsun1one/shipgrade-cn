# Source Promotion Sandbox Cases

Generated: 2026-05-26T00:34:55Z

These cases take source-promotion-batch runtime candidates past static smoke into dedicated temporary sandbox execution. They are still public-source, no-secret, redacted command evidence, not market proof.

## Summary

- cases: `2/2` passed
- steps: `10/10` passed
- required steps: `9/9` passed
- configured upstream tests discovered: `225`
- temp_copy: `copy source to TemporaryDirectory; exclude .git, node_modules, .venv, __pycache__, .DS_Store, AppleDouble files; materialize selected public git paths`
- env: `scrub env to PATH/system temp only; HOME and package caches are temp; no token/key/secret/cookie/session variables`

## Case: ecc-agent-operating-system

- source: `affaan-m/ECC`
- license: `MIT`
- runtime: `node/npm/agent-skill-catalog`
- materialized paths: `package.json, README.md, .claude-plugin, .github, .codex, .cursor, .opencode, agents, commands, skills, hooks, rules, scripts/lib, tests, AGENTS.md, scripts/catalog.js, scripts/ci, README.zh-CN.md, .claude-plugin, docs/zh-CN, manifests, schemas, scripts`
- configured test discovery: `137` via `tests/**/*.test.js`

| step | required | command | exit | evidence |
| --- | --- | --- | ---: | --- |
| ecc-npm-package-metadata | `true` | `npm pkg get scripts dependencies devDependencies` | `0` | {   "scripts": {     "postinstall": "echo '\\n  ecc-universal installed!\\n  Run: npx ecc typescript\\n  Compat: npx ecc-install typescript\\n  Docs: https://github.com/affaan-m/ECC\\n'",     "catalog:check": "node scripts/ci/catalog.js --text",     "catalog:s |
| ecc-npm-install-ignore-scripts | `true` | `npm install --ignore-scripts --no-audit --fund=false` | `0` |  added 233 packages in 53s  |
| ecc-catalog-check | `true` | `npm run catalog:check` | `0` |  > ecc-universal@2.0.0-rc.1 catalog:check > node scripts/ci/catalog.js --text  Catalog counts: - agents: 61 - commands: 76 - skills: 246  Documentation counts match the repository catalog.  |
| ecc-command-registry-check | `true` | `npm run command-registry:check` | `0` |  > ecc-universal@2.0.0-rc.1 command-registry:check > node scripts/ci/generate-command-registry.js --check  Command registry is up to date.  |
| ecc-selected-catalog-tests | `true` | `node tests/scripts/catalog.test.js` | `0` |  === Testing catalog.js ===    ✓ shows help with no arguments   ✓ shows help with an explicit help flag   ✓ lists install profiles   ✓ filters components by family and emits JSON   ✓ shows a resolved component payload   ✓ fails on unknown subcommands   ✓ fails |

Distilled lesson: A high-signal agent-skill repo is valuable when it has machine-checkable catalog and registry gates, not just many prompt files or a glossy README.

## Case: browser-use-browser-agent

- source: `browser-use/browser-use`
- license: `MIT`
- runtime: `python/uv/pytest/browser-agent`
- materialized paths: `pyproject.toml, README.md, browser_use/llm, browser_use/skill_cli, tests/ci/test_markdown_chunking.py, tests/ci/test_variable_detection.py, tests/ci/test_doctor_command.py, tests/ci/conftest.py, browser_use/__init__.py, browser_use/agent, browser_use/browser, browser_use/dom, browser_use/filesystem, browser_use/tools, browser_use`
- configured test discovery: `88` via `tests/ci/*.py selected no-browser-or-local-only cases`

| step | required | command | exit | evidence |
| --- | --- | --- | ---: | --- |
| browser-use-py-compile-selected | `true` | `python3 -m py_compile browser_use/skill_cli/commands/doctor.py browser_use/dom/markdown_extractor.py browser_use/agent/variable_detector.py browser_use/agent/views.py browser_use/dom/views.py` | `0` |  |
| browser-use-uv-venv-temp | `true` | `uv venv $SANDBOX/venv-browser-use` | `0` | warning: The `tool.uv.dev-dependencies` field (used in `pyproject.toml`) is deprecated and will be removed in a future release; use `dependency-groups.dev` instead Using CPython 3.14.3 interpreter at: /opt/homebrew/opt/python@3.14/bin/python3.14 Creating virtu |
| browser-use-install-editable-with-test-deps | `true` | `uv pip install --python $SANDBOX/venv-browser-use/bin/python -e . pytest pytest-asyncio pytest-httpserver` | `0` | warning: The `tool.uv.dev-dependencies` field (used in `pyproject.toml`) is deprecated and will be removed in a future release; use `dependency-groups.dev` instead Using Python 3.14.3 environment at: $SANDBOX/venv-browser-use Resolved 109 packages in 4.98s     |
| browser-use-deterministic-pytest | `true` | `$SANDBOX/venv-browser-use/bin/python -m pytest tests/ci/test_markdown_chunking.py::TestChunkMarkdownBasic tests/ci/test_markdown_chunking.py::TestChunkMarkdownHeaders tests/ci/test_markdown_chunking.py::TestChunkMarkdownHeaderPreferred tests/ci/test_markdown_chunking.py::TestChunkMarkdownCodeFence tests/ci/test_markdown_chunking.py::TestChunkMarkdownTable tests/ci/test_markdown_chunking.py::TestChunkMarkdownListItems tests/ci/test_markdown_chunking.py::TestChunkMarkdownStartFromChar tests/ci/test_markdown_chunking.py::TestChunkMarkdownOverlap tests/ci/test_markdown_chunking.py::TestChunkMarkdownMixed tests/ci/test_markdown_chunking.py::TestHTMLToMarkdownChunking tests/ci/test_variable_detection.py -q --tb=short -o addopts=` | `0` | _code_fence_not_split PASSED [ 13%] tests/ci/test_markdown_chunking.py::TestChunkMarkdownCodeFence::test_unclosed_code_fence PASSED [ 15%] tests/ci/test_markdown_chunking.py::TestChunkMarkdownTable::test_table_not_split_mid_row PASSED [ 17%] tests/ci/test_mark |
| browser-use-doctor-boundary-probe | `false` | `$SANDBOX/venv-browser-use/bin/python -m pytest tests/ci/test_doctor_command.py -q --tb=short -o addopts=` | `0` |  tests/ci/test_doctor_command.py::test_doctor_handle_returns_valid_structure PASSED [ 11%] tests/ci/test_doctor_command.py::test_check_package_installed PASSED     [ 22%] tests/ci/test_doctor_command.py::test_check_browser_returns_valid_structure PASSED [ 33%] |

Distilled lesson: Browser-agent repos need a split between local deterministic tests and browser/network/cloud tests; ShipGrade should preserve that split in Chinese templates.

## Distilled Lesson

- Promotion is not a popularity contest. A repo graduates only when license, structure, command topology, and execution evidence all align.
- For Chinese beginner users, hide the upstream complexity behind one clean quality gate.
- For professional users, keep the exact upstream command, exit code, and boundary visible so the claim is auditable.

## Hard Boundary

- No private repository body, secret, token, cookie, session, auth database, browser profile, SSH key, or private key is copied.
- Dependency install happens only inside a temporary copy with a scrubbed environment and temp HOME/cache.
- Failing or deferred upstream commands must be recorded as evidence, not silently erased.
