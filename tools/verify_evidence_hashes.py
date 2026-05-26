from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "evidence" / "hash_manifest.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not MANIFEST.exists():
        print("[ERROR] hash_manifest.json not found")
        sys.exit(1)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    evidence_hash_map = manifest.get("evidence_hash_map", {})

    ok = True

    for relative_path, expected_hash in evidence_hash_map.items():
        file_path = ROOT / relative_path

        if not file_path.exists():
            print(f"[FAIL] missing: {relative_path}")
            ok = False
            continue

        actual_hash = sha256_file(file_path)

        if actual_hash != expected_hash:
            print(f"[FAIL] hash mismatch: {relative_path}")
            print(f"  expected: {expected_hash}")
            print(f"  actual:   {actual_hash}")
            ok = False
        else:
            print(f"[OK] {relative_path}")

    if not ok:
        sys.exit(1)

    print("[OK] all evidence hashes verified")


if __name__ == "__main__":
    main()
