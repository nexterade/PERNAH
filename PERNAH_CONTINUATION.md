# PERNAH — Continuation / Handoff State

> Dokumen ini dibuat agar pengembangan PERNAH dapat dilanjutkan jika percakapan, sesi, model, atau chat credit/limit terputus.


## 0.0 CURRENT KNOWLEDGE-SURFACE GATE

Current release: `0.2.0-dev.69`.

**Current implementation / next gate:** schema v4 canonical image attachments remain local SQLite BLOBs. Project Owner reports all attachment and Backup & Recovery browser checks PASS on packaged `dev.62`; this acceptance is recorded in `dev.63`. Catbox remains parked. M6.1 provider-neutral contracts and M6.2 strict extraction/answer proposal validation are implemented in `pernah/ai_layer.py`; no real provider/network/SDK or canonical writes. M6.3 retrieval-first orchestration and canonical event-to-memory evidence projection are implemented. Active next gate: harden answer grounding and explicit insufficient-evidence/refinement behavior. Provider proposals remain advisory and canonical writes remain deterministic.

For every material change, perform the lightweight Knowledge-Surface Impact Check:
`BOTH / GLOSSARY / CHRONICLE / NONE`. Glossary defines terminology; Creation Chronicle
records material historical decisions/events. Do not create entries for trivial edits,
but do not leave new recurring governance concepts undocumented.

## 0A. Authority and conflict resolution

This file is a **handoff/state aid**, not a replacement for CHECKPOINT.md.

Authority order:

1. `CHECKPOINT.md` — stable process/engineering rules and project governance.
2. `STATE.md` — actual current implementation state.
3. `BACKLOG.md` — planned work.
4. `CHANGELOG.md` — historical record.
5. `README.md` / `TUTORIAL.md` — user-facing overview and usage.
6. `PERNAH_CONTINUATION.md` — compact cross-session handoff and resume context.

If this file conflicts with `CHECKPOINT.md`, **CHECKPOINT wins**.
If this file conflicts with current `STATE.md`, **STATE wins for implementation status**.
If ambiguity remains and the decision changes scope or architecture, do not guess; ask the user.

This file may summarize decisions already present elsewhere, but it must not silently create a new governing rule.

## 🚨 0B. MANDATORY CONTINUATION ORDER

**WHEN A NEW CHAT STARTS WITH THE LATEST PERNAH ZIP, DO NOT IMPLEMENT FIRST.**

**CHECKPOINT → PERNAH_BOOT → README → STATE → BACKLOG → CHANGELOG → SOURCE + TESTS →
CREATION CHRONICLE + GLOSARIUM (WAJIB) → PLAN → IMPLEMENT → TEST →
DOCUMENT SYNC → PACKAGE → TEST EXACT ARTIFACT → DELIVER ACCESSIBLE ARTIFACT**

**THIS IS A MANDATORY GOVERNANCE RULE, NOT AN OPTIONAL CHECKLIST.** The latest ZIP
is the primary evidence. Prior chat memory, summaries, or handoff notes cannot replace
reading the latest artifact. Do not claim full project/state understanding until the
required documentation/context sweep has actually been completed.

## 0C. ARTIFACT CONTINUITY RULE

**CHAT IS EPHEMERAL. ARTIFACT IS CONTINUOUS.**

The conversation is a temporary workspace. Important project state must live in the
artifact so a new chat can recover without relying on old conversation memory.

Fast boot files:
- `PERNAH_BOOT.md` — human-readable orientation snapshot.
- `PERNAH_PROJECT_STATE.json` — machine-readable orientation snapshot.
- `docs/RELEASE-MANIFEST.md` — release lineage and validation record.

These files are derived/operational aids. They do not outrank `CHECKPOINT.md`,
`STATE.md`, or `BACKLOG.md`. If they drift, regenerate them during document sync.

## 1. Identity

**Project:** PERNAH  
**Expansion:** Personal Memory & Life Context System  
**Current project version:** 0.2.0-dev.69  
**Working concept:** External memory / life-context system  
**Core idea:** User speaks naturally; PERNAH understands the intent, extracts structured context, stores canonical memory, and retrieves it later.

Tagline sementara:

> Lu nggak perlu mengingat semuanya. PERNAH yang nyimpen.


## 1A. Collaborative AI working style

- AI is a Co-Developer and discussion partner, not only a command executor.
- Proactively surface materially better alternatives, risks, trade-offs, and root causes.
- Do not act as a yes-man; disagreement should be evidence-based and constructive.
- When the artifact already determines the next gate, continue without unnecessary confirmation.
- Treat explicit cost/resource limits as real constraints. Prefer free/local/offline/low-cost solutions when they satisfy the acceptance criteria.
- Never infer or store the user's personal financial condition as project state.
- Human touch is part of normal collaboration: occasionally use a relevant light joke,
  analogy, fun-fact, or human comment when context allows; never force it, and prioritize
  clarity for security, critical errors, data loss, privacy, or safety-sensitive work.

## 1C. Current Web App Shell

The shared product shell now owns the primary navigation and theme surface for Home, Memory, Chronicle, Glossary, Settings, and About. `/chronicle` and `/glossary` render shell reader surfaces containing the canonical standalone reference documents; `/docs/Creation-Chronicle.html` and `/docs/Glosarium.html` remain the canonical documentation presentations. `/about` now also uses the shared shell.

Next gate: Project Owner browser acceptance for image attachment capture and Backup & Recovery on the exact packaged dev.62 artifact. The Catbox concept is parked only; it is not approved for implementation.

## 1B. Low-cost deployment concept — Domain + OpenWrt

Current project concept: use `pernah.my.id` as the public domain identity and an
OpenWrt device as the candidate 24/7 personal runtime host. The current candidate
is an AmLogic HG680P running OpenWrt 24.10.4. The observed environment snapshot is
~1.76 GB RAM, ~29.12 GB data mount, ~3% CPU, and ~39°C; these figures are observations,
not deployment benchmarks.

Candidate public access: Cloudflare Tunnel. Optional static landing/docs: GitHub Pages.
Canonical storage remains SQLite on the local runtime. This is **CONCEPT / NOT IMPLEMENTED**:
no public hostname, tunnel, authentication, remote exposure, or OpenWrt deployment
automation is accepted yet.

## 2. Non-negotiable architecture principles

1. Local-first.
2. Canonical data is independent of any AI provider.
3. AI is an understanding/retrieval layer, NOT the source of truth.
4. Canonical memory persists until explicitly deleted.
5. Historical state should not be destroyed by updates.
6. Derived data must be rebuildable.
7. Export/import must remain possible.
8. Offline core must remain usable.
9. Natural language is the primary interface.
10. Multi-language is an architectural requirement.
11. Preserve original user input alongside normalized structure.
12. Do not claim tests, integrations, or runtime behavior that has not actually been tested.

## 3. Current architecture

INPUT
→ CAPTURE
→ MEMORY ENGINE
→ NORMALIZATION / UNDERSTANDING
→ VALIDATION
→ CANONICAL STORAGE
→ INDEX / RELATIONSHIPS
→ RETRIEVAL
→ OPTIONAL AI / INSIGHTS

Core storage:

- SQLite
- UUID4 identifiers
- UTC ISO 8601 timestamps
- Versioned schema + migrations
- Local canonical database
- JSON export/import

## 4. Canonical model

Core:

- Memory
- Entity
- Event
- Relationship
- Temporal history
- Source
- Confidence

Specialized canonical types:

- Commitment
- Decision
- Transaction
- Physical Object
- Location

Canonical data must survive AI provider changes.

Derived data may include:

- Search indexes
- Embeddings
- AI summaries
- Cached answers
- Statistics
- Relationship suggestions

Derived data must be rebuildable.

## 5. Current implementation status

### Visual Identity + Creation Chronicle Theme
DONE

- Symbol + Wordmark / Continuity P identity established.
- Brand assets added under `docs/assets/`.
- Chronicle now uses the PERNAH dark/light palette and LEMON MILK + Open Sans declarations.
- Theme toggle, responsive sidebar, primary navigation, and floating back-to-top are implemented.

### Documentation — Creation Chronicle Integrity
DONE

- Formal Chronicle contract established.
- Late milestone order repaired through v0.2.0-dev.28.
- Duplicate section IDs removed; TOC now derives from current headings.
- Standalone visual shell refactored without changing feature behavior.
- Chronicle regression tests added.

### Documentation / Glossary

- `docs/Glosarium.html` is a universal knowledge dictionary spanning domains, ecosystems, and audiences.
- Existing glossary terminology preserved.
- Current glossary build contains 107 unique indexed terms.
- Search, category filters, alphabet navigation, responsive layout, and print support are included.
- Existing CHANGELOG history was preserved; a new entry was appended for the redesign.


### Foundation
DONE

### Milestone 1 — Canonical Storage
DONE

Implemented:

- SQLite storage
- UUID4
- UTC timestamps
- Schema migration
- Memory
- Entity
- Relationship
- Temporal history
- Event
- Commitment
- Decision
- Transaction
- Export/import

Last reported test status:
**8/8 PASS** for canonical storage milestone.

### Milestone 2 — Memory Engine
IN PROGRESS

Implemented:

- Original text preservation
- Language detection
- Normalization
- Intent extraction
- Entity extraction
- Amount extraction
- Temporal expression extraction
- Confidence
- Provenance/source
- MemoryDraft contract

Last reported test status:
**14/14 PASS** for the Memory Engine + ingestion/retrieval stage.

IMPORTANT:
The current Memory Engine is intentionally limited. It has targeted Indonesian/Sundanese support and a limited English path. Do NOT claim universal multilingual understanding.

## 6. Important multilingual requirement

Example:

Input:
> Urang geus meli laptop hargana 2 jt tadi isuk

Expected conceptual normalization:

- language: Sundanese
- intent: record_purchase
- entity: laptop
- amount: Rp2.000.000
- action: purchase
- time expression: tadi isuk
- original_text preserved

Query:

> Urang pernah meli laptop can nya?

Expected conceptual interpretation:

- language: Sundanese
- intent: temporal_retrieval
- action: purchase
- entity: laptop
- temporal: past

PERNAH should answer from canonical data rather than string matching.

## 7. Product differentiation

Mainstream WhatsApp bot:

User → Message → Bot → Answer → Done

PERNAH:

User → Natural conversation → Understand → Extract context → Canonical memory → Relationships/timeline → Future retrieval

PERNAH is NOT merely a WhatsApp bot.

WhatsApp is one input interface. The PERNAH Core must remain usable independently.

### Web Interface Warung Padang Acceptance — dev.32

- Project Owner completed the real-browser Warung Padang test drive on the packaged dev.31 artifact.
- Manual acceptance: **PASS**.
- Initial Local Web Interface is accepted as a Milestone 5 product-facing input slice.
- Next slice: Web Interface hardening.

### PERNAH Visual Identity System — dev.31

- Shared identity contract: `docs/assets/DESIGN-SYSTEM.md`.
- Shared token reference: `docs/assets/pernah-design-tokens.css`.
- Continuity P brand applied to Creation Chronicle, Glossary, and Local Web Interface.
- Glossary remote font dependencies removed; all three existing user-facing surfaces use the same palette and typography direction.
- No canonical schema/storage/provider/Secret Vault behavior changed.

## 8. Current next milestone

### Immediate next task

Security & Privacy Foundation is defined as governance-only in dev.27; manual input remains implemented as the first explicit product-facing boundary. Next slice: local web interface. Continuity Layer v1 is complete and is not a replacement for backup/recovery.

Acceptance target:

A natural-language input can be transformed into a validated canonical record and persisted in SQLite without losing:

- original text
- language
- source
- confidence
- extracted entities
- temporal information
- transaction/event/commitment/etc. structure

Then add retrieval tests.

## 9. Do NOT jump to these yet

Until canonical ingestion + retrieval are stable, do not prematurely implement:

- production WhatsApp integration
- cloud infrastructure
- realtime multi-device sync
- autonomous agent behavior
- subscriptions
- social/family sharing
- fancy UI
- provider-specific AI lock-in

## 10. Key product examples

### Memory

> Passport gue di laci meja.

Later:

> Passport gue di mana?

Expected:
Latest known valid location.

### Finance

> 25 ribu makan sama Rahayu.

Later:

> Bulan ini gue habis berapa buat makan sama Rahayu?

Expected:
Query transaction/event relationships.

### Commitment

> Gue janji Rahayu kirim invoice Jumat.

Later:

> Apa yang gue janjikan minggu ini?

Expected:
Pending commitment retrieval.

### Decision

> Gue batal beli laptop X karena terlalu mahal.

Later:

> Kenapa dulu gue nggak jadi beli laptop X?

Expected:
Decision + reason retrieval.

## 11. Naming

Official project name:

**PERNAH**

Do not revert to LIFE MEMORY as the product name.

LIFE MEMORY is only an internal working/concept description if needed.

Example person used in conceptual examples:

**Rahayu ❤️**

## 12. Resume protocol

When starting a new conversation/session:

1. Load the latest project ZIP.
2. Read `CHECKPOINT.md` first.
3. Read the latest `STATE.md`.
4. Read `PERNAH_CONTINUATION.md` as a compact handoff aid.
5. Read `BACKLOG.md` / `CHANGELOG.md` when the task needs planned or historical context.
6. Inspect the actual repository before changing anything.
6. Treat implementation/test results as authoritative only when verified from the current files/runtime.
6. Continue from the "Current next milestone" section.
7. Update STATE / CHANGELOG / BACKLOG according to the project's documentation rules.
8. Run tests after implementation.
9. Never assume previous unverified claims are still true.

## 13. Recovery principle

If the original chat disappears:

**The project files are the memory.**

The fastest recovery path is:

`CHECKPOINT → PERNAH_BOOT → README → STATE → BACKLOG → CHANGELOG → SOURCE + TESTS → GLOSARIUM + CHRONICLE → CONTINUE`.

The conversation is useful context, but it must not be the only place where architectural decisions live.

Current artifact baseline: 0.2.0-dev.28

Generated: 2026-10-05


## Retrieval expansion — 0.2.0-dev.1
- Purchase retrieval can run without an object entity constraint.
- Canonical purchase retrieval accepts inclusive `occurred_after` / `occurred_before` ISO 8601 filters.
- Entity-scoped retrieval uses an existence constraint to avoid duplicate purchase rows from multiple event-entity links.
- `pytest`: 16/16 PASS.


## Documentation milestone

Creation Chronicle official presentation is now `docs/Creation-Chronicle.html`; Markdown remains a working/source representation, while the HTML is the canonical project-facing format.


## Latest documentation fix — 0.2.0-dev.8

- Fixed the glossary renderer duplication pattern: global/static terminology is no longer injected into every entry.
- `Exact Search` and `Deterministic Ranking` are normal glossary entries.
- Added 13 user-maintained networking/infrastructure terms without removing existing terminology.
- Added CHECKPOINT rule 3.37: Generated UI Duplication Guard.
- Added glossary integrity smoke validation.

## Latest governance + glossary sync — 0.2.0-dev.9
- Upgraded CHECKPOINT governance baseline merged into the PERNAH project checkpoint.
- Added context handshake, validation/release contract, change-impact classification, evidence integrity, reproducibility, security baseline, documentation sync matrix, artifact traceability, and project adaptation guidance.
- Preserved the Generated UI Duplication Guard and the PERNAH-specific glossary presentation invariants.
- User-maintained networking/infrastructure glossary entries synchronized; canonical glossary count is 86 unique terms.

## Latest governance adaptation — 0.2.0-dev.12

- Uploaded starter CHECKPOINT is now the governance baseline for PERNAH.
- CHECKPOINT Section 6 was adapted with PERNAH-specific stable rules only.
- Implementation state remains in STATE/ARCHITECTURE; planning remains in BACKLOG;
  history remains in CHANGELOG.
- Release ZIP is flat-root and excludes Python cache artifacts.


### Current continuation point — dev.18
Deterministic temporal and relationship retrieval is implemented through the supported event/entity contracts. Semantic retrieval is a rebuildable derived layer with deterministic TF-IDF ranking, expanded local concept normalization, and a deterministic concept-relevance boundary for recognized concepts. Next planned gate: Milestone 5 — Web Interface hardening. Manual input is already implemented through the provider-neutral capture boundary; web, WhatsApp, and existing-data import remain separate slices.


## dev.25 handoff

Manual input slice completed via `pernah.manual_input.capture_text()` and `python -m pernah.manual`. Next gate: Milestone 5 — Web Interface hardening.


## dev.27 handoff

Local Web Interface is implemented over the existing capture boundary and its request boundary now has the first hardening slice. Data Classification & Privacy Boundary remains defined in `docs/SECURITY.md`. PERNAH distinguishes Normal Data, Sensitive Data, and Secret Data. Canonical data has an explicit no-auto-prune/no-auto-expire rule. Secret Data must not be stored plaintext in Memory Core. Secret Vault is roadmap-only and not implemented. The initial localhost input boundary has passed the Warung Padang manual acceptance gate; the next product gate is Web Interface hardening.

## Previous Focus — dev.59
Chronicle Sidebar Scroll-Sync / Scrollspy is the current runtime UX slice. Active Chronicle index state follows viewport section position; mobile sidebar retains backdrop/outside close and swipe/Escape behavior.


Hybrid Vocabulary + Glossary: the canonical dictionary accepts useful vocabulary, jargon, command snippets, abbreviations, error messages, and technical terms when useful to understand the project journey. Current canonical size: **153 entries**.


## dev.60 handoff — Atomic Ingestion + Continuity Repair

- `ingest_draft()` prevalidates the transaction/event invariant and uses a unique SQLite savepoint so any exception rolls back all writes from that draft.
- Regression tests cover malformed transaction drafts and a simulated downstream persistence failure.
- `VERSION`, boot snapshot, machine state, STATE, BACKLOG, CHANGELOG, and release manifest are synchronized to `0.2.0-dev.62`; this is a documentation-only roadmap update.
- Current product gate remains Project Owner human acceptance for Web Backup & Recovery and remaining exact-artifact UX checks. Milestone 6 readiness should be reassessed only after those gates are closed.


## Current handoff — dev.61 image attachments

Current implementation adds canonical image attachments linked to Memory records. SQLite schema v4 stores image BLOBs; portable canonical JSON encodes them as Base64. Local Web capture accepts JPEG/PNG/GIF/WebP (maximum 4 images, 8 MiB each, 12 MiB total), validates byte signatures, previews attachments on the saved-memory page, and preserves them through backup/restore. Existing schema v3 databases and v3 canonical JSON backups have compatibility paths. OCR, AI image interpretation, redaction, encryption-at-rest, and remote access are not implemented. Run the full suite and exact packaged-artifact preflight, then request human browser acceptance.


## Roadmap concept parked — dev.62

**PERNAH CROSSOVER CATBOX (Coming Soon, Maybe 🤔)** is an idea-only backlog entry. It is not implemented or committed. Any future plan must review public URL/privacy implications, local-first fallback, provider-neutral metadata, credential handling, remote deletion behavior, and backup portability before the Project Owner explicitly authorizes implementation.


**dev.67:** Retrieval orchestration now resolves event/purchase rows through linked canonical memories before forming provider evidence; orphan summaries are excluded. Next: test answer grounding and insufficient-evidence/refinement behavior; no real provider or network behavior yet.


**dev.68:** Section 44 heading/divider repair. **dev.69:** Audited all numbered Chronicle sections and expanded regression checks to enforce `h1` + preceding divider for every numbered milestone, with section 0 explicitly exempted as `h2`; tests also check section body content. Documentation-only; runtime/schema v4 unchanged.
