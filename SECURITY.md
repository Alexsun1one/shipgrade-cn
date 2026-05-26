# Security Policy

ShipGrade CN 的安全原则很简单: 工程能力不能靠牺牲用户边界获得。

## Do Not Include

- API keys, tokens, passwords, private keys.
- Cookies, browser profiles, auth/session databases.
- Private repository body text without explicit permission.
- Leaked source, leaked prompts, system prompt archives.
- Unclear-license body text.

## Safe To Include

- Public repo metadata.
- Public, license-reviewed file paths and structure signals.
- Redacted command transcripts.
- Source/license policy and checksum references.
- Templates, eval cases, and doctor checks.

## Reporting

If you find accidental secret exposure or unsafe source ingestion, remove the unsafe artifact first, then document:

- affected path
- exposure type
- cleanup command/result
- prevention rule added
