# PERNAH — Tutorial

## Current supported path

The current product-facing input slice is the local manual input boundary. It writes through the existing provider-neutral pipeline into canonical SQLite storage.

```text
MANUAL TEXT
    ↓
pernah.manual_input.capture_text()
    ↓
normalize()
    ↓
MemoryDraft
    ↓
ingest_draft()
    ↓
CANONICAL STORAGE
```

## 1. One-shot input

From the project root:

```bash
python3 -m pernah.manual --db pernah.db --text "Gue beli laptop harga 2 jt tadi pagi"
```

The command prints the detected capture intent, canonical memory ID, resolved time when available, and extracted entities.

## 2. Interactive input

```bash
python3 -m pernah.manual --db pernah.db
```

Then enter one text input at the `PERNAH >` prompt.

## 3. Machine-readable output

Add `--json` when another local process needs structured output:

```bash
python3 -m pernah.manual --db pernah.db --text "Gue beli laptop" --json
```

## 4. Relative-time testing

Use `--reference-time` to make relative-time normalization deterministic:

```bash
python3 -m pernah.manual \
  --db pernah.db \
  --reference-time 2026-10-06T12:00:00+00:00 \
  --text "Gue beli laptop kemarin"
```

## 5. Important boundary

The input interface is **not** the source of truth. Canonical storage remains authoritative. Web, messaging, and import interfaces should converge on the same provider-neutral ingestion boundary rather than creating parallel canonical-write paths.

## Current limitation

This tutorial documents the implemented manual CLI and Local Web Interface, including local Backup & Recovery. The Web Interface has passed the earlier Warung Padang manual acceptance gate; the new Web Backup & Recovery surface still requires a fresh human browser acceptance on the exact packaged artifact before that gate is closed.


## 6. Web Backup & Recovery

From the local Web Interface, open **Settings → Backup & Recovery**.

1. **Download JSON** to create a canonical `pernah-canonical-v1` backup.
2. Keep the backup outside the live database directory when practical.
3. To recover, choose the JSON backup and press **Restore selected backup**.
4. Confirm the destructive replacement warning.
5. PERNAH validates the backup before atomically replacing the target database.
6. Open Memory or refresh the browser to verify the restored state.

Restore is intentionally local-only and does not provide authentication or remote access. Secret Data remains outside the Memory Core / Web Backup contract.
