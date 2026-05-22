# Stage331: Execution Integrity (REMEDA)

Stage331 extends Stage330 by introducing:

## Execution Integrity

This stage verifies not only file integrity, but whether multiple evidence files belong to the same execution session.

## What Stage331 Adds

Stage330 verified:

- prompt.txt hash
- response.txt hash
- run.log hash

Stage331 additionally verifies:

- same execution session
- evidence order
- evidence count
- session identity
- execution timestamp

## Execution Session

Stage331 generates:

- `execution_session.json`

Example:

```json
{
  "session_id": "run-2026-05-22T06-40-23Z",
  "created_at": "2026-05-22T06:40:23Z",
  "evidence_order": [
    "prompt.txt",
    "response.txt",
    "run.log"
  ],
  "evidence_count": 3,
  "sha256_map": {
    "prompt.txt": "...",
    "response.txt": "...",
    "run.log": "..."
  }
}
Verification

Stage331 verifies:

same session
same hashes
same evidence order
same evidence count

This evolves REMEDA from:

file integrity
→ to
execution session integrity
Public Verification Files
docs/report/execution_session.json
docs/report/audit_report.json
docs/report/audit_report.html
URL

GitHub Pages:

https://mokkunsuzuki-code.github.io/stage331/

License

MIT License
