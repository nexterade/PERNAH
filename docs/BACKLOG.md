# PERNAH — Backlog

Status roadmap: **Active implementation**

Current maintenance note (dev.71): M6.5 adds a default-deny external-processing policy for provider calls. Explicit authorization, disclosure acknowledgement, and allowlisted data categories are required; no consent UI or real provider is enabled. Next gate: review provider timeout/rate-limit/refusal semantics and disclosure/retention/cost requirements before any real integration.

## Current Gate — v0.2.0-dev.61: Canonical Image Attachments (Project Owner acceptance pending)

- [x] Add canonical attachment metadata and image bytes linked to Memory (schema v4).
- [x] Migrate v3 SQLite databases and preserve v3 canonical JSON backup compatibility.
- [x] Accept bounded JPEG/PNG/GIF/WebP attachments in Local Web Interface capture.
- [x] Preview and serve attachments through a same-origin local route.
- [x] Include attachment bytes in canonical JSON backup/restore.
- [x] Add validation, migration, persistence, web, and backup regression tests.
- [ ] Project Owner browser acceptance of image capture and backup/restore on exact packaged artifact.
- [ ] Add image OCR / automatic evidence interpretation only after explicit design and privacy review; not part of this release.


## Future Concept Parking Lot — Not Committed

### PERNAH CROSSOVER CATBOX (Coming Soon, Maybe 🤔)

**Status:** IDEA PARKED / NOT COMMITTED / NOT IMPLEMENTED. This is a discussion outcome only; it is not the next gate, a milestone commitment, or authorization to start implementation.

Concept: optionally use Catbox as an external attachment host while keeping PERNAH's canonical memory and attachment metadata provider-neutral. Intended use cases include transaction evidence (receipts, transfer/payment screenshots) and personal-life memories (family photos, relationship memories, trips, and meaningful moments).

If the idea is revisited, plan and review these decisions before implementation:

- [ ] Compare Catbox with local-only and hybrid storage; preserve local-first and offline core behavior.
- [ ] Document the public-access/privacy implications clearly, especially for family photos and financial evidence; never imply Catbox URLs are private.
- [ ] Design provider-neutral attachment metadata, upload state/failure recovery, and safe credential handling for optional API configuration.
- [ ] Define deletion semantics and what happens when remote files become unavailable.
- [ ] Define backup/export behavior so a backup is not merely a collection of external URLs; retain a portable recovery path where feasible.
- [ ] Decide whether sensitive attachments need local-only handling or client-side encryption, including the preview/recovery trade-offs.
- [ ] Write a beginner-friendly Catbox setup guide and test connection/upload/delete flows only after the privacy and architecture review is accepted.

Do not implement, add Catbox runtime dependencies, migrate attachment storage, or change the current local SQLite attachment behavior until the Project Owner explicitly reopens and approves this concept.


## Previous Gate — v0.2.0-dev.60 (historical; superseded by dev.61)

- [x] Close the test-discovery blind spot by bringing Memory Engine regression tests under canonical `unittest` discovery.
- [x] Add a regression guard against top-level `test_*` functions bypassing the release runner.
- [x] Harden mixed Sundanese/Indonesian language detection boundary.
- [x] Validate the exact packaged `PERNAH-v0.2.0-dev.56.zip` through the Artifact Compliance Gate.
- [x] Add automated Web Interface recovery coverage across backup, deletion, restore, restart, and refresh.
- [x] Add user-facing local Backup & Recovery controls in Settings with explicit restore confirmation and canonical validation.
- [x] Add dependency-free CLI URL auto-copy with graceful clipboard fallback.
- [x] Fix browser CSP for same-origin restore fetches.
- [x] Harden Glossary rendering against browser storage restrictions.
- [x] Make mobile Glossary index close on any outside tap/pointer.
- [ ] Complete the Project Owner's human Web Backup & Recovery browser test-drive gate on the exact packaged recovery artifact.
- [ ] Confirm CLI URL auto-copy manually on the target terminal environment using the exact dev.54 artifact.
- [x] Fix Chronicle sidebar active-state synchronization with viewport scrollspy.
- [x] Keep Chronicle mobile outside-tap/backdrop close behavior aligned with the Glossary sidebar contract.
- [x] Make draft ingestion atomic with SQLite savepoint rollback and add failure-path regression tests.
- [x] Synchronize continuity snapshots and release metadata for `dev.60`.

## Milestone 0 — Foundation

- [x] Tetapkan nama produk: PERNAH
- [x] Tetapkan positioning: Personal Memory & Life Context System
- [x] Tetapkan prinsip local-first
- [x] Tetapkan canonical vs derived data
- [x] Tetapkan historical/temporal model secara konseptual
- [x] Tetapkan Canonical Data Model v0.1
- [x] Review final Canonical Data Model sebelum implementasi

## Milestone 1 — Canonical Storage

- [x] Pilih storage engine lokal untuk v0.1 — SQLite via Python standard library
- [x] Rancang physical schema dari logical model untuk core storage v0.1
- [x] Tetapkan ID strategy — UUID4 string
- [x] Tetapkan timestamp/timezone strategy — UTC ISO 8601
- [x] Tetapkan serialization/export format — JSON canonical v1
- [x] Implementasikan database initialization
- [x] Implementasikan core CRUD/read canonical records
- [x] Implementasikan temporal history untuk relationship/location state
- [x] Implementasikan validation dasar
- [x] Implementasikan migration/version gate dasar
- [x] Implementasikan persistence dan export/import round-trip
- [x] Lengkapi physical tables untuk Commitment, Decision, Transaction, Event sebelum Memory Engine

## Milestone 2 — Memory Engine

- [x] Define provider-neutral MemoryDraft contract
- [x] Preserve original input text
- [x] Lightweight language detection foundation
- [x] Normalisasi input mentah untuk supported patterns
- [x] Basic entity extraction
- [x] Basic event extraction
- [x] Basic temporal-expression resolution
- [x] Basic transaction extraction
- [x] Intent classification for capture/retrieval examples
- [x] Source/provenance tracking in draft output
- [x] Confidence handling in draft output
- [x] Relationship extraction for event-to-entity links in supported ingestion path
- [x] Persistence orchestration from MemoryDraft to canonical records for supported purchase capture
- [x] Broader relationship extraction (supported meeting/participant path)
- [x] Deduplication (entity find-or-create + canonical relationship/event guards)

## Documentation / Knowledge Glossary

- [x] Define glossary as a universal knowledge dictionary across domains, ecosystems, and audiences
- [x] Preserve PERNAH-specific terminology as one knowledge category rather than the glossary boundary
- [x] Seed cross-domain entries such as Meme, ISO, Polaroid, Aurora, and Gmail Dot Trick
- [ ] Expand knowledge glossary coverage systematically by domain

## Milestone 3 — Retrieval

- [x] Deterministic purchase retrieval for supported MemoryDraft queries
- [x] Broadened purchase retrieval when the object is omitted
- [x] Temporal window filtering at the canonical retrieval layer
- [x] Exact search
- [x] Broader natural-language temporal query extraction (yesterday/today, numeric day offsets, week/month windows, Indonesian/English supported forms)
- [x] Entity relationship query for supported event/entity paths
- [x] Timeline generation for entity-scoped event retrieval
- [x] Richer entity relationship patterns beyond supported meeting/participant paths
- [x] Semantic retrieval sebagai derived layer
- [x] Expand semantic concept vocabulary and ranking/false-positive evaluation

## Continuity Layer v1

- [x] Fast boot snapshot (`PERNAH_BOOT.md`)
- [x] Machine-readable boot snapshot (`PERNAH_PROJECT_STATE.json`)
- [x] Release lineage manifest (`docs/RELEASE-MANIFEST.md`)
- [x] Cross-chat continuity rule: chat is ephemeral; artifact is continuous
- [x] Continuity regression tests

## Low-cost deployment concept — Domain + OpenWrt

- [x] Record `pernah.my.id` as the domain candidate.
- [x] Record OpenWrt / AmLogic HG680P as the candidate 24/7 runtime host.
- [x] Record the local SQLite + OpenWrt runtime boundary.
- [x] Record Cloudflare Tunnel as the candidate public-access mechanism.
- [x] Record GitHub Pages as an optional static landing/docs surface, separate from runtime.
- [ ] Audit OpenWrt runtime capabilities: architecture, Python, SQLite CLI/runtime, storage paths, process supervision, and package availability.
- [ ] Prototype PERNAH runtime on OpenWrt without changing canonical data semantics.
- [ ] Design authentication and remote-exposure security before public access.
- [ ] Test domain → tunnel → PERNAH flow.
- [ ] Define backup/recovery behavior for the OpenWrt-hosted canonical database.
- [ ] Accept or reject OpenWrt as the production personal runtime target based on measured tests.

**Status:** CONCEPT / NOT IMPLEMENTED.

## Next gate

Project Owner manual acceptance for image attachments and the existing Web Backup & Recovery flow on packaged `dev.62`: **PASS** (reported by Project Owner; screenshot confirms saved-memory attachment preview). This closes the current Milestone 5 acceptance gate for that artifact.

M6.1–M6.4 contracts, deterministic orchestration, canonical evidence projection, grounded answer validation, and refinement are implemented through dev.70. M6.5 dev.71 adds a deny-by-default authorization contract for external provider calls. Next gate: strengthen provider timeout/rate-limit/refusal semantics and define disclosure/retention/cost review; no real provider, SDK, network behavior, schema migration, or AI UI yet.

Catbox remains parked as **PERNAH CROSSOVER CATBOX (Coming Soon, Maybe 🤔)** and must not be implemented unless explicitly reopened by the Project Owner.

### Product shell direction

- [ ] Home — product landing / entry point (not `README.md`)
- [ ] Memory — capture and memory interaction surface
- [x] Chronicle / Perjalanan — product-facing continuity narrative
- [x] Glossary — reference library
- [x] Settings — local interface settings
- [x] About — author surface with **@nexterade** attribution


## Milestone 4 — Backup & Recovery

- [x] Local backup
- [x] Backup validation
- [x] Restore workflow
- [x] Portable export hardening
- [x] Import validation
- [x] Disaster recovery test


## Security & Privacy Foundation

- [x] Define Normal Data / Sensitive Data / Secret Data classification
- [x] Define canonical retention rule: no automatic pruning/expiry
- [x] Define Secret Data boundary for Memory Core
- [x] Record Secret Vault as a separate future capability
- [ ] Design Secret Vault threat model
- [ ] Design encryption/key derivation/key lifecycle for Secret Vault
- [ ] Implement Secret Vault only after security design and failure/recovery tests are accepted

## Milestone 5 — Input Interfaces

- [x] Browser regression hardening: flat-root artifact packaging, CLI access logs, canonical shell logo asset, and favicon

- [x] About — author profile surface with author, links, skill focus, interests, and project philosophy

- [x] Manual input — local CLI + provider-neutral capture API
- [x] Web interface — local standard-library HTTP boundary
- [x] Web interface — Warung Padang manual acceptance
- [x] Web interface hardening — post-hardening browser regression closed for dev.46 artifact; browser visual identity and Chronicle index fixes covered by automated checks
- [x] Shared reader security — same-origin Chronicle / Glossary embedding fixed
- [x] Shared reference surfaces — Chronicle / Glossary content-only integration with one product navigation
- [ ] WhatsApp integration design
- [ ] Import existing data

## Milestone 6 — AI Layer

Detailed plan and acceptance criteria: [`docs/AI-LAYER-PLAN.md`](AI-LAYER-PLAN.md).

- [x] M6.1 — Provider-neutral request/result/error contracts; unconfigured provider is offline-safe
- [x] M6.2 — Structured extraction contract and untrusted-output validation
- [x] M6.3 — Retrieval-first orchestration with bounded canonical event/timeline evidence projection (dev.67)
- [ ] M6.4 — Grounded answer generation and insufficient-evidence/refinement behavior
- [ ] M6.4 — Memory-grounded answer generation with traceable evidence
- [ ] M6.5 — Provider failure, privacy, and external-processing boundaries

## Milestone 7 — Optional Online Backup / Sync

- [ ] Encrypted remote backup
- [ ] Sync model
- [ ] Conflict resolution
- [ ] Multi-device support

## Explicitly out of scope for v0.1

- Realtime multi-device sync
- Social/family sharing
- Marketplace
- Subscription system
- Autonomous agent kompleks
- Wearable integration
- Production WhatsApp integration
- Final cloud infrastructure


## Visual Identity System

- [x] Define Symbol + Wordmark / Continuity P direction
- [x] Establish dark/light core palette
- [x] Establish LEMON MILK + Open Sans typography direction
- [x] Add reusable brand assets and identity guidance
- [x] Apply first shared theme system to Creation Chronicle
- [ ] Apply the shared visual system to Glossary and future product-facing interfaces


## Documentation — Creation Chronicle HTML

- [x] Convert Creation Chronicle from Markdown presentation to standalone HTML.
- [x] Add searchable TOC and print-friendly presentation.
- [x] Update CHECKPOINT rule 3.27 to make HTML the official presentation format.


## Completed visual identity gate — dev.30

PERNAH Symbol + Wordmark identity and the shared theme system are established across the current project-facing surfaces. The initial Local Web Interface has passed the Warung Padang manual acceptance gate; hardening is the current product gate.

### Hybrid Vocabulary + Glossary
- [x] Accept vocabulary, jargon, command snippets, abbreviations, and technical error messages as valid Glossary candidates.
- [x] Add the 20 newly identified entries from the current development conversation.
