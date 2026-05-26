import json
import sys
from pathlib import Path

ALLOWED_TYPES = {
    "prompt-injection",
    "sensitive-information-disclosure",
    "supply-chain",
    "insecure-output-handling",
    "excessive-agency",
    "model-denial-of-service",
    "training-data-poisoning",
    "model-theft",
    "overreliance",
    "misinformation",
    "other",
}

ALLOWED_RESULTS = {
    "reproduced",
    "not-reproduced",
    "partial",
    "inconclusive",
}

REQUIRED = [
    "vulnerability_type",
    "target",
    "ai_claim_id",
    "reproduction_id",
    "result",
    "evidence_files",
    "sha256",
]


def fail(message):
    print(f"REJECT: {message}")
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        fail("Usage: python tools/validate_reproduction_evidence.py <json-file>")

    path = Path(sys.argv[1])
    if not path.exists():
        fail(f"file not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))

    for key in REQUIRED:
        if key not in data:
            fail(f"missing required field: {key}")

    if data["vulnerability_type"] not in ALLOWED_TYPES:
        fail(f"invalid vulnerability_type: {data['vulnerability_type']}")

    if data["result"] not in ALLOWED_RESULTS:
        fail(f"invalid result: {data['result']}")

    if not isinstance(data["evidence_files"], list) or not data["evidence_files"]:
        fail("evidence_files must be a non-empty list")

    if not isinstance(data["sha256"], dict):
        fail("sha256 must be an object")

    for filename in data["evidence_files"]:
        if filename not in data["sha256"]:
            fail(f"missing sha256 for evidence file: {filename}")

        digest = data["sha256"][filename]
        if not isinstance(digest, str) or len(digest) != 64:
            fail(f"invalid sha256 length for: {filename}")

    print("ACCEPT: reproduction evidence schema is valid")
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
