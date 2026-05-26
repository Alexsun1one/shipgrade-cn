# Source Promotion Batch

This batch promotes the top source-promotion-queue targets into concrete review evidence: license probe, source boundary, sparse clone, structure counts, command topology, and safe static smoke where available.

## Snapshot

- generated at: `2026-05-26T00:00:37Z`
- selected targets: `4`
- audited targets: `4`
- runtime candidates: `2`
- static smoke pass count: `2`

## Batch Targets

| repo | license | clone | tier | files | tests | evals | scripts | next step |
| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `affaan-m/ECC` | MIT | audited | runtime_candidate | 2870 | 304 | 85 | build:opencode, catalog:check, command-registry:check, lint, test | promote to a disposable no-secret sandbox case after reviewing install lifecycle and test command scope |
| `addyosmani/agent-skills` | MIT | audited | deep_static_candidate | 77 | 11 | 0 | none | run deep-code case study first; defer executable sandbox |
| `browser-use/browser-use` | MIT | audited | runtime_candidate | 486 | 104 | 4 | none | inspect language/package files manually before sandbox execution |
| `VoltAgent/awesome-agent-skills` | MIT | audited | docs_or_metadata_candidate | 4 | 0 | 0 | none | keep as docs/metadata signal; executable sandbox is low priority |

## Per-Repo Notes

### affaan-m/ECC

- distill value: improve skill anatomy, progressive disclosure, examples, and installer ergonomics
- source boundary: allow_extract in source_manifest; body extraction remains provenance-tracked and excludes secrets/private/session/cookie/auth data
- GitHub license probe: `{"html_url": "https://github.com/affaan-m/ECC/blob/main/LICENSE", "name": "MIT License", "ok": true, "path": "LICENSE", "spdx_id": "MIT"}`
- static smoke: `{"python_py_compile": {"files_checked": 40, "returncode": 0, "stderr_tail": ""}}`
- command topology: `{"language_commands": {"python": ["python -m pytest", "python -m compileall"]}, "package_manager": "npm", "runtime_tier": "runtime_candidate", "script_names": ["build:opencode", "catalog:check", "command-registry:check", "lint", "test"]}`
- next step: promote to a disposable no-secret sandbox case after reviewing install lifecycle and test command scope

### addyosmani/agent-skills

- distill value: strengthen spec -> plan -> tasks -> implementation handoff
- source boundary: allow_extract in source_manifest; body extraction remains provenance-tracked and excludes secrets/private/session/cookie/auth data
- GitHub license probe: `{"html_url": "https://github.com/addyosmani/agent-skills/blob/main/LICENSE", "name": "MIT License", "ok": true, "path": "LICENSE", "spdx_id": "MIT"}`
- static smoke: `{}`
- command topology: `{"language_commands": {}, "package_manager": null, "runtime_tier": "deep_static_candidate", "script_names": []}`
- next step: run deep-code case study first; defer executable sandbox

### browser-use/browser-use

- distill value: improve skill anatomy, progressive disclosure, examples, and installer ergonomics
- source boundary: allow_extract in source_manifest; body extraction remains provenance-tracked and excludes secrets/private/session/cookie/auth data
- GitHub license probe: `{"html_url": "https://github.com/browser-use/browser-use/blob/main/LICENSE", "name": "MIT License", "ok": true, "path": "LICENSE", "spdx_id": "MIT"}`
- static smoke: `{"python_py_compile": {"files_checked": 40, "returncode": 0, "stderr_tail": ""}}`
- command topology: `{"language_commands": {"python": ["python -m pytest", "python -m compileall"]}, "package_manager": null, "runtime_tier": "runtime_candidate", "script_names": []}`
- next step: inspect language/package files manually before sandbox execution

### VoltAgent/awesome-agent-skills

- distill value: turn LLM quality into eval cases, red-team checks, and CI gates
- source boundary: allow_extract in source_manifest; body extraction remains provenance-tracked and excludes secrets/private/session/cookie/auth data
- GitHub license probe: `{"html_url": "https://github.com/VoltAgent/awesome-agent-skills/blob/main/LICENSE", "name": "MIT License", "ok": true, "path": "LICENSE", "spdx_id": "MIT"}`
- static smoke: `{}`
- command topology: `{"language_commands": {}, "package_manager": null, "runtime_tier": "docs_or_metadata_candidate", "script_names": []}`
- next step: keep as docs/metadata signal; executable sandbox is low priority

## Hard Boundary

- This batch still does not run arbitrary upstream code with local secrets.
- `npm/pnpm/yarn/pip/uv` install lifecycle execution is deferred until a dedicated disposable sandbox case is written.
- License probe is evidence for review, not final legal advice.
- No private repository body, secret, token, cookie, session, auth database, browser profile, SSH key, or private key is copied.
