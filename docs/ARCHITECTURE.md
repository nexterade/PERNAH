# PERNAH — Architecture & Canonical Data Model v0.1

Status: **IMPLEMENTED FOUNDATION + MEMORY ENGINE v0.1**

Dokumen ini mendefinisikan model logis sebelum pemilihan implementasi database dan kode. Tidak ada implementasi yang diklaim dari dokumen ini.

## 1. Tujuan

PERNAH harus mampu menyimpan memori kehidupan selama bertahun-tahun tanpa membuat data canonical bergantung pada model AI, provider, search index, embedding, atau cache tertentu.

## 2. Prinsip data

### Canonical data

Data yang menjadi sumber kebenaran utama:

- Memory
- Entity
- Event
- Relationship
- temporal history
- Commitment
- Decision
- Transaction
- Physical Object
- Location
- Source
- Confidence

### Derived data

Data yang boleh dihancurkan dan dibuat ulang:

- search index
- embeddings
- AI summaries
- semantic index (currently a deterministic in-memory TF-IDF index rebuilt from canonical memories)
- cached answers
- relationship suggestions
- statistics

AI tidak menjadi source of truth. Jika provider AI berubah atau tidak tersedia, canonical data tetap harus aman dan dapat digunakan.

## 3. Logical model

### Memory

Representasi informasi yang ditangkap PERNAH.

Atribut minimum:

- `id`
- `type`
- `content`
- `created_at`
- `occurred_at`
- `updated_at`
- `source_id`
- `confidence`
- `schema_version`

### Entity

Sesuatu yang dapat dirujuk dan dihubungkan dengan memori lain.

Contoh tipe:

- person
- object
- place
- organization
- document

Atribut minimum:

- `id`
- `type`
- `name`
- `created_at`
- `updated_at`

### Relationship

Hubungan antara entity atau record yang memiliki validitas temporal.

Atribut minimum:

- `id`
- `from_entity`
- `relation_type`
- `to_entity`
- `valid_from`
- `valid_until`
- `source_id`
- `confidence`

### Event

Sesuatu yang terjadi pada waktu tertentu. Physical table sudah diimplementasikan pada schema v2.

Atribut minimum:

- `id`
- `type`
- `occurred_at`
- `location_id`
- `source_id`

### Commitment

Janji atau kewajiban yang memiliki action, pihak terkait, deadline, dan status. Physical table sudah diimplementasikan pada schema v2.

### Decision

Keputusan yang menyimpan pilihan, alasan, waktu, dan konteks. Physical table sudah diimplementasikan pada schema v2.

### Transaction

Pergerakan uang yang dapat dihubungkan dengan event, person, kategori, dan konteks. Physical table sudah diimplementasikan pada schema v2.

### Physical Object & Location

Object merepresentasikan barang; Location merepresentasikan tempat. Perpindahan barang tidak menghapus lokasi lama, tetapi membentuk history state baru.

## 4. Temporal history

PERNAH tidak boleh melakukan overwrite destruktif pada informasi yang berubah.

Contoh:

```text
Passport
2026-10-05 → laci meja
2027-03-12 → safe
2028-01-08 → lemari dokumen
```

Query seperti "terakhir passport gue di mana?" mengambil state valid terbaru, sedangkan query historis tetap dapat mengakses state sebelumnya.

## 5. Source & confidence

Setiap informasi yang penting untuk retrieval harus memiliki provenance.

Contoh source:

- whatsapp
- web
- manual
- import
- ai_inference

Confidence membedakan fakta yang dinyatakan langsung dengan interpretasi atau inference.

## 6. Data flow

```text
INPUT
  ↓
RAW INPUT
  ↓
NORMALIZATION
  ↓
UNDERSTANDING
  ↓
ENTITY / EVENT / MEMORY
  ↓
RELATIONSHIPS
  ↓
CANONICAL DB
  ├── SEARCH INDEX
  ├── AI / EMBEDDING
  └── TIMELINE
```

## 7. Query examples

### Rahayu

> Gue pernah ketemu Rahayu kapan aja?

Supported deterministic temporal variants can constrain the same relationship query, for example:

> Gue pernah ketemu Rahayu minggu lalu?

The query layer normalizes supported relative-time expressions into inclusive UTC ISO 8601
windows before canonical retrieval.

PERNAH menelusuri Entity `Rahayu`, Event yang berhubungan, lalu menyusun timeline.

### Passport

> Terakhir passport gue di mana?

PERNAH mengambil relationship lokasi terbaru yang masih valid.

### Commitment

> Apa aja yang belum gue selesaikan?

PERNAH mengambil Commitment dengan status pending/open dan mengevaluasi deadline.

## 8. Edge cases

| Kasus | Perilaku |
|---|---|
| Informasi bertentangan | Pertahankan history; jangan overwrite destruktif |
| "Kayaknya..." | Confidence dapat diturunkan |
| AI inference | Tandai sebagai inference |
| Lokasi barang berubah | Buat state temporal baru |
| Nama orang sama | Jangan otomatis merge tanpa bukti cukup |
| User mengoreksi | Simpan koreksi dan history |
| Duplicate import | Jalankan deduplication |
| AI provider mati | Canonical data tetap usable |
| Search index rusak | Rebuild |
| Embedding berubah | Re-index |
| Schema berubah | Migration |
| Export | Canonical data wajib ikut |
| Import | Validate → migrate → import |

## 9. Acceptance criteria

- Canonical data tidak bergantung pada provider AI.
- Perubahan informasi tidak menghapus history.
- Fakta memiliki source dan confidence.
- Entity dapat saling berhubungan.
- Event dapat melibatkan banyak entity.
- Relationship memiliki validitas temporal.
- Object memiliki location history.
- Commitment memiliki status/deadline.
- Transaction dapat dikaitkan dengan event/person.
- Decision menyimpan reason/context.
- Derived data dapat direbuild.
- Schema dapat dimigrasikan tanpa kehilangan canonical data.

## 10. Physical storage decision — v0.1

- Storage engine: SQLite
- Runtime dependency: Python standard library only
- ID strategy: UUID4 string identifiers
- Time strategy: UTC ISO 8601 strings; user-facing timezone conversion belongs above storage
- Schema version: integer `schema_version` metadata with migration/version gate
- Portable export: JSON document with format `pernah-canonical-v1`
- Canonical storage tables implemented in this gate: `sources`, `entities`, `memories`, `relationships`, `events`, `event_entities`, `commitments`, `decisions`, `transactions`
- Derived indexes, embeddings, AI summaries, and caches remain outside the canonical store

The physical schema was completed in the current storage gate through schema version 3. Event-to-entity links are represented explicitly by `event_entities` so retrieval can scope an event to the entities actually involved.

## 11. Memory Engine v0.1

The first Memory Engine slice is provider-neutral and deterministic. It does not call an AI provider. It produces a `MemoryDraft`; the ingestion orchestration layer validates the supported draft shape and persists canonical records.

Input pipeline:

```text
RAW INPUT
  ↓
LANGUAGE DETECTION
  ↓
NORMALIZATION
  ↓
INTENT / ENTITY / TEMPORAL EXTRACTION
  ↓
MEMORY DRAFT
  ↓
INGESTION / VALIDATION
  ↓
CANONICAL STORAGE
```

### Multi-language requirement

The original user text is always preserved. Language detection and normalized meaning are separate fields. v0.1 includes deterministic examples for Indonesian, Sundanese, mixed Indonesian/Sundanese, and a small English keyword path; this is a foundation, not a claim of broad language coverage.

Example:

> Urang geus meli laptop hargana 2 jt tadi isuk

Normalizes to a purchase event with a laptop entity, IDR 2,000,000 transaction, and a resolved relative-time expression when a reference time is supplied.

Query example:

> Urang pernah meli laptop can nya?

Normalizes to a temporal retrieval intent for a past laptop purchase.

The engine keeps `original_text`, `detected_language`, normalized intent, extracted entities, temporal expression, confidence, and source type so downstream AI or retrieval layers do not need to reconstruct provenance.


### Entity relationship event patterns

The deterministic relationship layer currently supports `meeting`, `conversation`, `call`, and `collaboration` events. Each supported person link uses the existing `event_entities` role `participant`; retrieval may additionally filter the entity-scoped timeline by deterministic event type. This is a narrow pattern contract, not semantic understanding.

## 12. Ingestion and retrieval v0.1

Supported purchase capture follows:

```text
MemoryDraft
  ↓
Source provenance
  ↓
Entity find-or-create
  ↓
Event + event_entities
  ↓
Transaction
  ↓
Interaction memory
```

The current deterministic retrieval path supports a temporal purchase query by object entity. It is intentionally narrow and does not yet represent general semantic search.

## 13. Rebuildable semantic retrieval

The current semantic retrieval layer is deliberately derived-only. It builds an in-memory TF-IDF index from canonical `memories` at query time and applies deterministic local concept/synonym normalization. Recognized query concepts also act as a relevance boundary: a candidate must share at least one recognized concept when the query contains one, preventing generic token overlap (such as a shared person name) from producing an unrelated semantic hit. The index is not persisted, does not modify canonical records, and can be rebuilt from the same SQLite data.

Retrieval precedence is:

1. Existing deterministic canonical query path.
2. Semantic derived fallback when the canonical path returns no result.

A canonical deterministic hit therefore cannot be silently overridden by a semantic score. No external AI provider or embedding service is required by this layer.

## 14. Local Backup & Validation v0.1

Local backup is a preservation layer over the existing canonical JSON contract, not a new
parallel data format. `Storage.backup()` writes the current canonical SQLite state as
`pernah-canonical-v1` JSON. Export ordering is deterministic by canonical table columns so
the same logical state produces the same serialized bytes.

`Storage.validate_backup()` validates the backup without mutating the project database. It
checks the format/schema contract and exact canonical row structure, then inserts the
backup into an isolated in-memory SQLite database with foreign-key enforcement enabled.
Relational integrity failures are therefore rejected before the artifact is considered
valid.

The backup boundary is intentionally separate from restore: dev.22 validates preservation
artifacts; a later recovery gate will perform mutation/restore. Backup is not cache, derived
index, presentation export, or AI-generated content.

## 15. Continuity Layer v1

PERNAH memperlakukan conversation sebagai workspace **ephemeral**. Continuity project
disimpan di artifact agar new-chat continuation tidak bergantung pada memory percakapan.

The continuity layer terdiri dari:

- `PERNAH_BOOT.md` — fast human-readable boot snapshot.
- `PERNAH_PROJECT_STATE.json` — machine-readable derived snapshot.
- `PERNAH_CONTINUATION.md` — compact handoff/context aid.
- `docs/RELEASE-MANIFEST.md` — release lineage and validation contract.

These files are operational/derived aids. Authoritative project state remains governed by
`CHECKPOINT.md`, `STATE.md`, `BACKLOG.md`, and the other source-of-truth documents defined
by the project. Continuity snapshots must be regenerated when current state changes.

**Recovery path:** BOOT → CHECKPOINT → README → STATE → BACKLOG → CHANGELOG → SOURCE +
TESTS → GLOSARIUM + CREATION CHRONICLE → NEXT GATE.


## Restore workflow

Restore is a recovery operation over the existing `pernah-canonical-v1` backup contract. `Storage.restore()` validates the backup before mutation, stages the canonical records into a temporary SQLite database with foreign-key enforcement, verifies that the staged canonical export exactly matches the backup payload, and only then atomically replaces the target path.

The workflow deliberately separates validation from mutation:

```text
validated backup
      ↓
temporary target DB
      ↓
canonical round-trip equality
      ↓
atomic promotion
```

An invalid backup or failed staging operation must not modify an existing target. Cloud recovery, scheduling, merge semantics, and disaster-recovery automation remain outside this slice.

## 16. Portable export/import hardening + disaster recovery

Portable canonical JSON remains the single `pernah-canonical-v1` contract. `Storage.export_json()` now writes the document atomically through a temporary file and creates missing parent directories, so an interrupted export cannot intentionally replace a previously valid artifact with a partial write.

`Storage.import_json()` is the file-oriented import path. It reads and validates the canonical artifact before mutating target storage, including isolated relational validation with foreign-key enforcement. `import_canonical()` applies the same relational preflight. Existing import semantics remain merge/dedup oriented through conflict-safe inserts; replacement recovery remains the responsibility of `Storage.restore()`.

The disaster-recovery boundary is exercised as a local recovery drill: a live SQLite database is backed up, the live database is removed in a controlled temporary environment, and the database is recreated from the validated artifact. The recovered canonical export must equal the pre-loss canonical state. Corrupted artifacts must fail before recovery and must never be able to mutate an existing target.

```text
CANONICAL SQLITE
      ↓
atomic portable export
      ↓
pernah-canonical-v1
      ↓
validate + relational preflight
      ↓
import / restore
      ↓
recovered canonical state
```

## Input interface boundary

Milestone 5 begins with a deliberately thin manual input boundary. `pernah.manual_input.capture_text()` accepts user-supplied text, reuses the existing provider-neutral `normalize()` → `MemoryDraft` → `ingest_draft()` pipeline, and writes through the canonical storage layer. `python -m pernah.manual` provides a local one-shot or interactive CLI over that boundary.
The Local Web Interface adds a localhost-only HTTP boundary over the same capture pipeline; its hardened request boundary validates form content type, UTF-8, field cardinality, and body size, and exposes `GET /health` for local service checks.

The interface is not canonical truth and does not introduce an AI/provider dependency. Future web, messaging, and existing-data import interfaces should converge on the same provider-neutral ingestion boundary rather than creating parallel canonical-write paths.



## 17. Data classification & privacy boundary

PERNAH now defines a governance-only data classification boundary before expanding input interfaces. The classes are Normal Data, Sensitive Data, and Secret Data. The detailed rules live in `docs/SECURITY.md`.

The canonical retention rule is explicit: maintenance, retrieval, indexing, backup, or optimization must not automatically delete, prune, or expire canonical records. Derived indexes, embeddings, summaries, caches, and AI outputs remain rebuildable and may be discarded without deleting their canonical source.

Secret Data is outside the current Memory Core contract. Passwords, API keys/tokens, PINs, recovery codes, private keys, seed phrases, and TOTP/GAuth secrets must not be stored as plaintext canonical memory. A future Secret Vault is a separate capability and requires encryption/decryption, key derivation, integrity/authentication, lock/unlock lifecycle, secure backup/recovery, and a threat model before production use.

## Deployment concept — Domain + OpenWrt

PERNAH mempertahankan pemisahan antara **canonical runtime** dan **public access layer**.
Untuk deployment pribadi berbiaya rendah, project mencatat pola berikut sebagai kandidat:

```text
                    pernah.my.id
                         │
                    public access
                         │
                Cloudflare Tunnel
                         │
                         ▼
                OpenWrt / PERNAH
                         │
                    SQLite canonical
```

### Candidate environment

- Domain candidate: `pernah.my.id`
- Runtime candidate: AmLogic HG680P / OpenWrt 24.10.4
- Observed RAM: ~1.76 GB
- Observed data mount: ~29.12 GB
- Observed CPU usage: ~3%
- Observed temperature: ~39°C
- Device availability: 24/7 according to current project-owner environment

These values are an environment snapshot, not a performance benchmark or deployment
acceptance result.

### Architectural rules

1. OpenWrt is a **candidate runtime host**, not yet an accepted production target.
2. SQLite remains the canonical local storage layer; public exposure must not turn a
   remote service into the canonical source of truth.
3. A tunnel is an access mechanism, not a replacement for application authentication,
   authorization, backup, or security hardening.
4. The domain is an addressing/identity layer and is independent from the canonical
   storage model.
5. GitHub Pages may be used later for static landing/docs; it is not the PERNAH canonical
   runtime.
6. No VPS is required by this concept.
7. Remote exposure, authentication, TLS/tunnel configuration, backup policy, and failure
   recovery must each pass their own implementation and test gates before being called
   production-ready.

### Current status

**CONCEPT / NOT IMPLEMENTED.** No tunnel, public hostname, remote binding, authentication,
or OpenWrt deployment automation is part of this release.
