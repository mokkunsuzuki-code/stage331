from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

SAMPLE_FILES = [
    ROOT / "samples" / "prompt.txt",
    ROOT / "samples" / "response.txt",
    ROOT / "samples" / "run.log",
]

EVIDENCE_DIR = ROOT / "docs" / "evidence"
REPORT_DIR = ROOT / "docs" / "report"

HASH_MANIFEST = EVIDENCE_DIR / "hash_manifest.json"
HASH_MANIFEST_SHA256 = EVIDENCE_DIR / "hash_manifest.sha256"
REPRODUCTION_EVIDENCE = EVIDENCE_DIR / "reproduction_evidence.json"
AUDIT_REPORT_JSON = REPORT_DIR / "audit_report.json"
AUDIT_REPORT_HTML = REPORT_DIR / "audit_report.html"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    evidence_hash_map = {}

    for file_path in SAMPLE_FILES:
        if not file_path.exists():
            raise FileNotFoundError(f"Missing evidence file: {file_path}")

        relative_path = file_path.relative_to(ROOT).as_posix()
        evidence_hash_map[relative_path] = sha256_file(file_path)

    hash_manifest = {
        "stage": 330,
        "name": "Evidence Hash Auto Builder",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "algorithm": "SHA256",
        "evidence_hash_map": evidence_hash_map,
    }

    HASH_MANIFEST.write_text(
        json.dumps(hash_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    manifest_digest = sha256_file(HASH_MANIFEST)
    HASH_MANIFEST_SHA256.write_text(manifest_digest + "  hash_manifest.json\n", encoding="utf-8")

    reproduction_evidence = {
        "stage": 330,
        "ai_claim_id": "demo-ai-claim-001",
        "reproduction_id": "demo-reproduction-001",
        "vulnerability_type": "prompt-injection",
        "target": {
            "type": "model-output",
            "name": "demo-target",
            "commit": "demo",
            "file": "samples/response.txt",
        },
        "result": "reproduced",
        "evidence_files": list(evidence_hash_map.keys()),
        "sha256": evidence_hash_map,
        "stage328_ready": True,
    }

    REPRODUCTION_EVIDENCE.write_text(
        json.dumps(reproduction_evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    audit_report = {
        "stage": 330,
        "title": "Stage330 Evidence Hash Auto Builder Audit Report",
        "decision_layer": "Stage328 Evidence Match Gate Ready",
        "evidence_hash_map": evidence_hash_map,
        "hash_manifest_sha256": manifest_digest,
        "created_at": hash_manifest["created_at"],
    }

    AUDIT_REPORT_JSON.write_text(
        json.dumps(audit_report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    rows = "\n".join(
        f"<tr><td>{path}</td><td><code>{digest}</code></td></tr>"
        for path, digest in evidence_hash_map.items()
    )

    AUDIT_REPORT_HTML.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Stage330 Evidence Hash Auto Builder</title>
</head>
<body>
  <h1>Stage330 Evidence Hash Auto Builder</h1>
  <p>Automatically generated SHA256 hashes for reproduction evidence files.</p>

  <h2>Stage328 Ready</h2>
  <p>This evidence package can be passed to the Stage328 Evidence Match Gate.</p>

  <h2>Evidence Hash Map</h2>
  <table border="1" cellpadding="8">
    <tr><th>Evidence File</th><th>SHA256</th></tr>
    {rows}
  </table>

  <h2>Hash Manifest SHA256</h2>
  <p><code>{manifest_digest}</code></p>
</body>
</html>
""",
        encoding="utf-8",
    )

    print("[OK] wrote docs/evidence/hash_manifest.json")
    print("[OK] wrote docs/evidence/hash_manifest.sha256")
    print("[OK] wrote docs/evidence/reproduction_evidence.json")
    print("[OK] wrote docs/report/audit_report.json")
    print("[OK] wrote docs/report/audit_report.html")


if __name__ == "__main__":
    main()
