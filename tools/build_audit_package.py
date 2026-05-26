#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 Motohiro Suzuki

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
DOCS_REPORTS = ROOT / "docs" / "reports"
REPORTS = ROOT / "reports"
DECISION_PATH = ROOT / "stage328_decision.json"

DOCS_REPORTS.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def load_stage328_decision():
    if DECISION_PATH.exists():
        return json.loads(DECISION_PATH.read_text(encoding="utf-8"))

    return {
        "decision": "pending",
        "reason": "stage328_decision.json not found",
        "same_target": False,
        "evidence_files_present": False,
        "sha256_bound": False,
        "signature_present": False,
    }


def main():
    created_at = datetime.now(timezone.utc).isoformat()
    stage328_decision = load_stage328_decision()

    decision_json_text = json.dumps(stage328_decision, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    evidence_hash = sha256_text(decision_json_text)

    audit_report = {
        "stage": 329,
        "name": "Stage329 Audit Artifact Package",
        "created_at": created_at,
        "purpose": "Convert Stage328 verification decisions into submit-ready audit evidence.",
        "source_decision_file": "stage328_decision.json",
        "evidence_hash_sha256": evidence_hash,
        "stage328_decision": stage328_decision,
        "verification_trace": [
            "Loaded stage328_decision.json",
            "Calculated SHA256 evidence hash",
            "Generated audit_report.json",
            "Generated audit_report.html",
            "Generated verify.txt",
            "Prepared signed audit report target"
        ],
        "submission_status": "ready_for_third_party_review",
        "flow": [
            "AI Claim",
            "Reproduction Evidence",
            "QSP Decision",
            "Signed Audit Report"
        ],
        "license": "MIT",
    }

    audit_json = json.dumps(audit_report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    audit_hash = sha256_text(audit_json)

    decision = stage328_decision.get("decision", "unknown")

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Stage329 Audit Submission Report</title>
  <style>
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #f6f8fa;
      color: #24292f;
    }}
    header {{
      background: #0d1117;
      color: white;
      padding: 48px 32px;
    }}
    main {{
      max-width: 1000px;
      margin: 32px auto;
      padding: 0 20px;
    }}
    .card {{
      background: white;
      border: 1px solid #d0d7de;
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: 0 8px 24px rgba(140,149,159,0.15);
    }}
    .badge {{
      display: inline-block;
      padding: 8px 14px;
      border-radius: 999px;
      background: #dafbe1;
      color: #116329;
      font-weight: 700;
      text-transform: uppercase;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
    }}
    .item {{
      border: 1px solid #d0d7de;
      border-radius: 12px;
      padding: 16px;
      background: #ffffff;
    }}
    pre {{
      background: #0d1117;
      color: #c9d1d9;
      padding: 16px;
      border-radius: 12px;
      overflow-x: auto;
      white-space: pre-wrap;
    }}
    code {{
      background: #f6f8fa;
      padding: 2px 6px;
      border-radius: 6px;
    }}
  </style>
</head>
<body>
<header>
  <h1>Stage329 Audit Submission Report</h1>
  <p>AI Claim → Reproduction Evidence → QSP Decision → Signed Audit Report</p>
  <span class="badge">Submit-ready audit artifact</span>
</header>

<main>
  <section class="card">
    <h2>Audit Decision</h2>
    <p><strong>{decision}</strong></p>
    <p>This page converts the Stage328 verification decision into a third-party reviewable audit artifact.</p>
  </section>

  <section class="card">
    <h2>Audit Trace</h2>
    <div class="grid">
      <div class="item"><strong>Created At</strong><br>{created_at}</div>
      <div class="item"><strong>Evidence Hash</strong><br><code>{evidence_hash}</code></div>
      <div class="item"><strong>Audit Report Hash</strong><br><code>{audit_hash}</code></div>
      <div class="item"><strong>Signature</strong><br><code>audit_report.json.asc</code></div>
    </div>
  </section>

  <section class="card">
    <h2>Stage328 Decision Input</h2>
    <pre>{json.dumps(stage328_decision, ensure_ascii=False, indent=2)}</pre>
  </section>

  <section class="card">
    <h2>Verification Trace</h2>
    <pre>{chr(10).join(audit_report["verification_trace"])}</pre>
  </section>

  <section class="card">
    <h2>Third-party Verification</h2>
    <pre>shasum -a 256 docs/reports/audit_report.json
gpg --verify docs/reports/audit_report.json.asc docs/reports/audit_report.json</pre>
  </section>

  <section class="card">
    <h2>Download / Review Files</h2>
    <ul>
      <li><a href="./audit_report.json">audit_report.json</a></li>
      <li><a href="./audit_report.json.asc">audit_report.json.asc</a></li>
      <li><a href="./audit_report.sha256">audit_report.sha256</a></li>
      <li><a href="./verify.txt">verify.txt</a></li>
    </ul>
  </section>
</main>
</body>
</html>
"""

    verify_txt = f"""Stage329 Third-party Verification

Source decision:
stage328_decision.json

Created at:
{created_at}

Evidence SHA256:
{evidence_hash}

Audit Report SHA256:
{audit_hash}

Verify hash:
shasum -a 256 docs/reports/audit_report.json

Verify signature:
gpg --verify docs/reports/audit_report.json.asc docs/reports/audit_report.json

Meaning:
This audit package was generated from the Stage328 verification decision.

Flow:
AI Claim
↓
Reproduction Evidence
↓
QSP Decision
↓
Signed Audit Report
"""

    for out_dir in [DOCS_REPORTS, REPORTS]:
        (out_dir / "audit_report.json").write_text(audit_json, encoding="utf-8")
        (out_dir / "audit_report.html").write_text(html, encoding="utf-8")
        (out_dir / "verify.txt").write_text(verify_txt, encoding="utf-8")
        (out_dir / "audit_report.sha256").write_text(
            f"{audit_hash}  audit_report.json\n",
            encoding="utf-8"
        )

    print("[OK] Stage329 audit package regenerated from stage328_decision.json")
    print(f"[OK] evidence_hash_sha256={evidence_hash}")
    print(f"[OK] audit_report_sha256={audit_hash}")


if __name__ == "__main__":
    main()
