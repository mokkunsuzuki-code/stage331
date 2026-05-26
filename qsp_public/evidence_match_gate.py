"""
Stage328: QSP Evidence Match Gate - Public Safe Layer

This public layer checks whether an AI security claim and reproduction evidence
are sufficiently bound together as verifiable evidence.

It does NOT reproduce vulnerabilities.
It does NOT contain private scoring logic.
It does NOT contain exploit logic.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: str | Path) -> Dict[str, Any]:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_same_target(ai_claim: Dict[str, Any], reproduction: Dict[str, Any]) -> bool:
    return ai_claim.get("target") == reproduction.get("target")


def check_evidence_files_present(reproduction: Dict[str, Any], base_dir: Path) -> bool:
    files = reproduction.get("evidence_files", [])
    if not files:
        return False

    for item in files:
        file_path = base_dir / item.get("path", "")
        if not file_path.exists() or not file_path.is_file():
            return False

    return True


def check_sha256_bound(reproduction: Dict[str, Any], base_dir: Path) -> bool:
    files = reproduction.get("evidence_files", [])
    if not files:
        return False

    for item in files:
        file_path = base_dir / item.get("path", "")
        expected_sha256 = item.get("sha256")

        if not expected_sha256:
            return False

        if not file_path.exists():
            return False

        actual_sha256 = sha256_file(file_path)
        if actual_sha256 != expected_sha256:
            return False

    return True


def check_signature_present(reproduction: Dict[str, Any], base_dir: Path) -> bool:
    signature_path = reproduction.get("signature")

    if not signature_path:
        return False

    sig_file = base_dir / signature_path
    return sig_file.exists() and sig_file.is_file()


def decide(checks: Dict[str, bool]) -> str:
    """
    Public decision rule:

    accept  = all checks true
    pending = same_target and evidence exists, but sha/signature incomplete
    reject  = target mismatch or evidence missing
    """

    if all(checks.values()):
        return "accept"

    if checks["same_target"] and checks["evidence_files_present"]:
        return "pending"

    return "reject"


def run_gate(ai_claim_path: str, reproduction_path: str, base_dir: str = ".") -> Dict[str, Any]:
    base = Path(base_dir)
    ai_claim = load_json(ai_claim_path)
    reproduction = load_json(reproduction_path)

    checks = {
        "same_target": check_same_target(ai_claim, reproduction),
        "evidence_files_present": check_evidence_files_present(reproduction, base),
        "sha256_bound": check_sha256_bound(reproduction, base),
        "signature_present": check_signature_present(reproduction, base),
    }

    decision = decide(checks)

    return {
        "stage": 328,
        "engine": "QSP Evidence Match Gate",
        "purpose": "AI Claim vs Reproduction Evidence trust decision",
        "checks": checks,
        "decision": decision,
        "note": "This gate verifies evidence binding. It does not reproduce vulnerabilities.",
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Stage328 QSP Evidence Match Gate")
    parser.add_argument("--claim", required=True, help="Path to AI claim JSON")
    parser.add_argument("--reproduction", required=True, help="Path to reproduction evidence JSON")
    parser.add_argument("--base-dir", default=".", help="Base directory for evidence files")
    parser.add_argument("--output", default="stage328_decision.json", help="Output decision JSON")

    args = parser.parse_args()

    result = run_gate(args.claim, args.reproduction, args.base_dir)

    output_path = Path(args.output)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[OK] wrote {output_path}")
