# Stage332: Signed Execution Session

Stage332 adds cryptographic signatures to the execution session.

## What This Stage Adds

Stage331 produced an execution session.

Stage332 signs that session with:

- GPG
- Sigstore

## Audit Target

```text
docs/execution/execution_session.json
Public Evidence Files
docs/execution/execution_session.json
docs/execution/execution_session.json.sig
docs/execution/execution_session.json.bundle
docs/execution/public-key.asc
Why This Matters

Stage332 proves:

what execution session was generated
who generated it
whether the session was changed later
whether the evidence can be independently verified

This keeps QSP / VEP on the audit, evidence, verification, and transparency path.

Verify GPG Signature
gpg --import docs/execution/public-key.asc

gpg --verify \
  docs/execution/execution_session.json.sig \
  docs/execution/execution_session.json
Verify Sigstore Bundle
cosign verify-blob \
  --bundle docs/execution/execution_session.json.bundle \
  docs/execution/execution_session.json
Important

The local core is intentionally excluded from GitHub.

core/
local/

Only public audit evidence is published.

License

MIT License

Copyright (c) 2025 Motohiro Suzuki
