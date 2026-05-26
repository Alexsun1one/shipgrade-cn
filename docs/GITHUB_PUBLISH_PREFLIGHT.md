# GitHub Publish Preflight

This is a local publish-readiness report for the standalone GitHub repository. It does not claim that remote GitHub Actions have run yet.

- passed: `15/15`
- remote CI boundary: `must be verified after the real GitHub repository exists`

| check | status | detail |
| --- | --- | --- |
| `required-files` | `pass` | 38 required files present |
| `readme-launch-surface` | `pass` | README has hook, proof, and preflight surface |
| `skill-frontmatter` | `pass` | machine-readable frontmatter with name/description triggers |
| `github-workflow` | `pass` | validate workflow has PR/push and release check |
| `repo-metadata` | `pass` | topics=10 missing=[] |
| `public-evidence-manifest` | `pass` | evidence_files=12 |
| `source-promotion-batch` | `pass` | selected=4 audited=4 runtime=2 static_smoke=2 |
| `source-promotion-sandbox-cases` | `pass` | cases=2/2 required=9/9 configured_tests=225 |
| `sandbox-runtime-matrix` | `pass` | cases=3/3 steps=12/12 |
| `social-preview` | `pass` | dimensions=(1600, 900) |
| `issue-pr-templates` | `pass` | issue and PR templates include validation language |
| `secret-and-metadata-scan` | `pass` | no generated metadata or secret patterns |
| `doctor-fake-rejection` | `pass` | fake completion rejected |
| `demo-proof` | `pass` | demo proof captures init/reject/accept path |
| `shipgrade-verify` | `pass` | shipgrade-verify-ok  |

## Publish Command Surface

```bash
python3 tools/github_publish_preflight.py --write-docs --run-verify
python3 tools/shipgrade_verify.py
python3 tools/shipgrade_demo.py
python3 scripts/create-public-stage.py /tmp/shipgrade-cn-public --init-git
bash scripts/package.sh
```

## Boundary

- This report checks the local release artifact, not a remote GitHub repository.
- After publishing, verify the real Actions run, repository topics, social preview, release archive, and issue templates on GitHub.
