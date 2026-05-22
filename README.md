# REMEDA Stage330

## Stage329 Audit Submission Package + Stage330 Evidence Hash Auto Builder

Stage330 extends the Stage329 audit submission workflow by adding automatic SHA256 evidence hash generation.

This stage does not replace Stage329.

It adds:

- automatic evidence hash generation
- hash manifest generation
- SHA256 verification support
- Stage328-ready reproduction evidence binding

---

# Architecture

AI Claim
↓
Reproduction Evidence
↓
Stage328 Evidence Match Gate
↓
accept / pending / reject
↓
Stage329 Signed Audit Report
↓
Stage330 Evidence Hash Auto Builder

---

# Stage330 Features

## Core Features

### 1. Read Evidence Files

Reads:

- prompt.txt
- response.txt
- run.log

---

### 2. Automatic SHA256 Generation

Automatically calculates SHA256 hashes for evidence files.

---

### 3. Automatic SHA256 Map

Builds an evidence hash map automatically.

---

### 4. reproduction_evidence.json Integration

Automatically embeds generated hashes into:

docs/evidence/reproduction_evidence.json

---

### 5. Stage328 Gate Compatibility

Generated evidence is directly usable by:

- Stage328 Evidence Match Gate

---

# Extended Features

## 6. hash_manifest.json Generation

Generated file:

docs/evidence/hash_manifest.json

---

## 7. hash_manifest.sha256 Generation

Generated file:

docs/evidence/hash_manifest.sha256

---

## 8. Audit Report Integration

Evidence hash maps are integrated into:

- audit_report.json
- audit_report.html

---

## 9. verify_evidence_hashes.py

Verification tool:

tools/verify_evidence_hashes.py

Verifies:

- file existence
- SHA256 integrity
- evidence consistency

---

# Generated Files

## Evidence

- docs/evidence/hash_manifest.json
- docs/evidence/hash_manifest.sha256
- docs/evidence/reproduction_evidence.json

## Reports

- docs/report/audit_report.json
- docs/report/audit_report.html

---

# Security Model

Stage330 keeps core logic private.

The following remain excluded from GitHub:

- tools/
- local verification core
- private signing logic
- secrets / keys

This repository only exposes public verification artifacts.

---

# Public Verification

## Japanese Page

https://mokkunsuzuki-code.github.io/stage330/

## English Page

https://mokkunsuzuki-code.github.io/stage330/en/

---

# License

MIT License

Copyright (c) 2025 Motohiro Suzuki

