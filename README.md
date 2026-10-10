# PERNAH

**Personal Memory & Life Context System**

Canonical storage + deterministic Memory Engine + image attachments + rebuildable semantic retrieval foundation for PERNAH v0.2.0-dev.67.

## Runtime

- Python 3.10+
- SQLite (Python standard library)
- No third-party runtime dependency

## Quick start

```python
from pernah import Storage

with Storage("pernah.db") as db:
    source = db.add_source(source_type="manual", reference="user input")
    db.add_memory(
        memory_type="note",
        content="Passport ada di laci meja",
        source_id=source,
        confidence=1.0,
    )
```

The canonical database is local. Search indexes, embeddings, AI summaries, and caches are intentionally not part of this storage layer. Image attachments are canonical SQLite BLOBs linked to memories and included in `pernah-canonical-v1` backups as validated Base64. Existing schema v3 databases and v3 JSON backups remain compatible through migration/upgrade.

## Local Web Interface

Start the local Web Interface with:

```bash
python -m pernah.web --port 6772
```

On startup, PERNAH prints the local URL and automatically copies that URL to the first available local clipboard utility. If no supported clipboard utility is installed, startup continues normally and the URL remains available in the terminal for manual copy.

## Memory Engine v0.1

The first input-understanding layer is provider-neutral and deterministic. It preserves the original text and produces a normalized `MemoryDraft`. Multi-language handling is an architectural requirement; v0.1 currently contains focused Indonesian/Sundanese examples and a limited English keyword path.

Example supported input:

```text
Urang geus meli laptop hargana 2 jt tadi isuk
```

This can normalize into a purchase event, laptop entity, IDR 2,000,000 transaction, and a resolved relative time when a reference timestamp is supplied.


## Current implementation slice

The current deterministic core includes canonical SQLite storage, purchase ingestion/retrieval, exact memory search, bounded temporal query extraction for supported expressions, richer deterministic event/entity relationship extraction, entity deduplication, and a rebuildable semantic retrieval layer. Semantic retrieval is derived from canonical memories, expanded deterministic local concept normalization, and a concept-relevance boundary that reduces false positives; AI providers remain intentionally deferred.

## Documentation integrity

`docs/Glosarium.html` is maintained as a data-driven dictionary. Content-only
updates must preserve the approved presentation layer and must not inject global
content into every generated entry. The project CHECKPOINT contains the
**Generated UI Duplication Guard** and regression requirements for this class of
renderer defect.

## Cross-chat continuity

PERNAH treats the conversation as an **ephemeral workspace** and the project artifact as
the continuity layer. `PERNAH_BOOT.md` is the fast boot snapshot,
`PERNAH_PROJECT_STATE.json` is its machine-readable counterpart, and
`docs/RELEASE-MANIFEST.md` records release lineage. These files do not replace
`CHECKPOINT.md`, `STATE.md`, `BACKLOG.md`, `CHANGELOG.md`, the Glosarium, the Creation
Chronicle, source, or tests; they make continuation resilient when a chat ends or
context becomes limited.

## Development note — dev.20

PERNAH development now treats the AI as a Co-Developer and discussion partner: it should proactively surface better alternatives, trade-offs, and risks while respecting the Project Owner as the final decision maker. Resource constraints are first-class when explicitly stated, with free/local/offline/low-cost options preferred when sufficient.

## Local backup v0.1

```python
from pathlib import Path
from pernah import Storage

with Storage("pernah.db") as db:
    db.backup(Path("backup/pernah-canonical.json"))

Storage.validate_backup("backup/pernah-canonical.json")

with Storage("data/pernah.db") as db:
    db.import_json("backup/pernah-canonical.json")

Storage.restore("backup/pernah-canonical.json", "data/pernah.db")
```

Backup validation checks the canonical format/schema, exact table/row structure, and relational integrity in an isolated SQLite database. Restore remains a separate recovery gate.

Portable export is written atomically and creates missing parent directories. `Storage.import_json()` validates the canonical artifact, validates relational integrity in isolation, and only then imports it into the target storage. Import remains merge/dedup oriented; full replacement recovery is handled by `Storage.restore()`.


## Restore workflow v0.1

A validated `pernah-canonical-v1` backup can replace a target SQLite database atomically:

```python
Storage.restore("backup/pernah-canonical.json", "data/pernah.db")
```

Restore first validates the backup, builds a temporary target database, verifies that the restored canonical export matches the backup, then promotes the temporary database with an atomic filesystem replace. A failed or invalid restore leaves an existing target database unchanged. The backup file itself is never modified.

## Manual input v0.1

Manual input is the first explicit product-facing input boundary. It reuses the provider-neutral normalization and ingestion path, preserves the original text, and writes to local canonical SQLite storage without requiring an AI provider.

Python API:

```python
from pernah import Storage, capture_text

with Storage("pernah.db") as db:
    captured = capture_text(db, "Gue ketemu Rahayu kemarin.")
```

Local CLI:

```text
python3 -m pernah.manual --db pernah.db --text "Passport ada di laci meja"
```

Omit `--text` for a single interactive prompt. Use `--json` for machine-readable capture metadata. Web, messaging, and existing-data import remain separate input-interface slices.

## Web Interface v0.1

Local web input is available through the standard-library HTTP server and reuses the same `capture_text()` boundary as the CLI. It binds to localhost by default and writes `source_type="web"` into canonical provenance.

```text
python3 -m pernah.web --db pernah.db
```

Open the printed localhost address in a browser. This slice is intentionally local-only: no authentication, cloud transport, remote binding, or Secret Vault capability is included.

Settings now exposes local **Backup & Recovery**: download the canonical `pernah-canonical-v1` JSON and restore a selected validated backup through the same `Storage.restore()` atomic replacement contract. Restore requires an explicit browser confirmation and never treats an unvalidated payload as canonical state.

## Data classification boundary

PERNAH membedakan Normal Data, Sensitive Data, dan Secret Data. Canonical data tidak auto-prune; Secret Data tidak boleh masuk plaintext ke Memory Core. Detail governance ada di `docs/SECURITY.md`. Secret Vault masih roadmap dan belum diimplementasikan.


## Deployment concept — Domain + OpenWrt

PERNAH tetap mempertahankan **local-first** sebagai prinsip runtime. Untuk deployment pribadi
berbiaya rendah, project sekarang mencatat konsep **domain + OpenWrt** sebagai kandidat
lingkungan runtime, bukan sebagai implementasi production yang sudah aktif.

Target yang sedang dievaluasi:

- Domain: `pernah.my.id`
- Runtime candidate: OpenWrt 24.10.4 pada AmLogic HG680P yang tersedia 24/7
- Canonical storage: SQLite tetap lokal pada runtime OpenWrt
- Public access candidate: Cloudflare Tunnel, tanpa mengubah canonical storage menjadi cloud
- GitHub Pages: opsi terpisah untuk landing/docs statis jika dibutuhkan nanti

Audit awal perangkat menunjukkan sekitar **1.76 GB RAM**, sekitar **29.12 GB** pada
mount data yang terlihat, CPU sekitar **3%**, dan suhu sekitar **39°C** pada saat observasi.
Angka ini adalah snapshot observasi, bukan benchmark atau acceptance deployment.

Status: **CONCEPT / NOT IMPLEMENTED**. Jangan menganggap domain, tunnel, authentication,
atau remote exposure sudah tersedia hanya karena konsep ini terdokumentasi.

## Visual Identity

The project-facing UI uses the **PERNAH Visual Identity System**: Symbol + Wordmark / Continuity P, Memory · Knowledge · Continuity, LEMON MILK + Open Sans, restrained green signal accents, and dark/light themes. See `docs/assets/DESIGN-SYSTEM.md`.


## Image attachments

The Local Web Interface Memory form can attach up to four JPEG, PNG, GIF, or WebP images to one note (8 MiB each; 12 MiB per request). This is intended for receipts, transfer/payment screenshots, warranty evidence, and other visual context. Images remain local and are preserved by canonical backup/restore. The current implementation does not OCR images or transmit them to an AI provider.


## Roadmap note — dev.62

“PERNAH CROSSOVER CATBOX (Coming Soon, Maybe 🤔)” is a parked, non-committed idea in `docs/BACKLOG.md`. Catbox is not integrated; image attachments continue to use local SQLite storage.


## Roadmap note — dev.63

Milestone 6 — AI Layer is planned in `docs/AI-LAYER-PLAN.md`. The first slice will define provider-neutral contracts and validate structured extraction with fake providers only; no real AI provider or network dependency is included yet.


## AI Layer contracts — dev.64

PERNAH now defines provider-neutral contracts and strict validation for untrusted structured extraction and evidence-grounded answer candidates in `pernah/ai_layer.py`. The default provider is offline-safe and makes no network calls. No real provider, SDK, API key, automatic canonical write, or schema change is included; the next gate is deterministic fallback orchestration and contract review.


## AI extraction orchestration — dev.65

`pernah.ai_layer.orchestrate_extraction()` provides an offline-safe orchestration boundary. It prepares the deterministic `normalize()` draft first and may validate a provider proposal as advisory context. Missing/failed providers and invalid proposals fall back to the deterministic draft. Provider proposals are never written to canonical memory automatically; low-confidence proposals require review. No real provider, SDK, network call, or schema change is included.


Milestone 6 current gate: dev.67 hardens canonical event-to-memory evidence projection for retrieval-first orchestration. See `docs/AI-LAYER-PLAN.md`; no real provider/network is enabled.
