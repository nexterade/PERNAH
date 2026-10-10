## 0.2.0-dev.69 — Chronicle document-wide structural consistency (current)

- Audited all numbered sections in `docs/Creation-Chronicle.html`; each uses `h1` and a preceding divider. Section 0 remains an intentional `h2` introduction.
- Added document-wide regression checks for heading hierarchy, dividers, and recognizable body content.
- Documentation/editorial-only change; runtime and schema v4 unchanged.
- Parent artifact: `PERNAH-v0.2.0-dev.68.zip`.

## 0.2.0-dev.68 — Chronicle section style consistency

- Corrected section 44 to match the numbered milestone `h1` heading and divider pattern.
- Parent artifact: `PERNAH-v0.2.0-dev.67.zip`.

## 0.2.0-dev.67 — Canonical evidence projection hardening

- M6.3 now resolves event/purchase query rows through `Storage.event_memories(event_id)` before they can become provider evidence.
- Only memory-shaped records with stable IDs and non-empty canonical content are passed as evidence; event/transaction summaries without linked memories are excluded.
- Timeline nested memory rows are normalized to `memory_id`; duplicate IDs are removed and evidence remains bounded.
- Added regression tests for event-to-memory mapping, orphan events, and malformed memory rows.
- No provider SDK/network, canonical writes, or schema migration; schema remains v4.
- Next gate: test answer grounding and insufficiency/refinement behavior before considering any user-facing integration.
- Parent artifact: `PERNAH-v0.2.0-dev.66.zip`.

## 0.2.0-dev.65 — Deterministic Extraction Orchestration (current)

- M6.1/M6.2 contracts remain in `pernah/ai_layer.py`; M6.3 foundation adds `orchestrate_extraction()`.
- Deterministic `normalize()` runs first and remains the only write-ready draft. Provider proposals are validated and advisory only; review-required proposals never bypass deterministic fallback.
- Missing provider, invalid response, validation error, or provider exception returns the deterministic draft. Provider exception messages are not surfaced, reducing risk of secret leakage.
- Added five regression tests. No real provider, SDK, network call, UI integration, canonical write, or schema migration; schema v4 unchanged.
- Next gate: test/review the orchestration contract, then design deterministic retrieval-first orchestration with evidence-minimized provider context. Provider integration remains deferred.
- Catbox remains parked.
- Parent artifact: `PERNAH-v0.2.0-dev.64.zip`.

## 0.2.0-dev.64 — AI Contracts + Structured Proposal Validation (current)

- Implemented M6.1 provider-neutral contracts and M6.2 structured extraction validation in `pernah/ai_layer.py`.
- `UnconfiguredProvider` is offline-safe and raises an actionable `ProviderUnavailable`; there is no real provider, SDK, network behavior, or credential handling.
- Provider output is validated as an untrusted proposal; low-confidence or deterministic-routing intents require review. Proposals are not `MemoryDraft` objects and are not persisted automatically.
- Answer candidates must cite IDs from the exact supplied evidence set; insufficient evidence requires an uncertainty note.
- Added 12 AI boundary regression tests. Canonical schema remains v4; runtime capture/storage/retrieval paths are unchanged.
- Next gate: review the contract/failure semantics, then implement a deterministic fallback adapter that uses existing `normalize()` and only hands validated/reviewed proposals to the existing atomic ingestion boundary.
- Catbox remains parked.
- Parent artifact: `PERNAH-v0.2.0-dev.63.zip`.

## 0.2.0-dev.63 — Attachment Acceptance + AI Layer Plan (current)

- Project Owner reports all manual checks PASS on exact packaged `dev.62`: image capture, preview/reopen, backup, restore, refresh/restart persistence, and existing Memory/Backup UX.
- The supplied screenshot independently confirms saved memory + image preview; the complete checklist PASS is based on the Project Owner's report.
- Milestone 5 image attachment / Backup & Recovery acceptance gate is closed for the tested `dev.62` artifact.
- `docs/AI-LAYER-PLAN.md` defines the staged Milestone 6 plan; first slice is M6.1 provider-neutral contracts + M6.2 structured extraction validation, fake provider only.
- No runtime, schema, or provider behavior changed in dev.63; schema remains v4 and attachments remain local SQLite BLOBs.
- Catbox remains parked in the roadmap.
- Parent artifact: `PERNAH-v0.2.0-dev.62.zip`.

## 0.2.0-dev.62 — Roadmap Parking Lot: PERNAH CROSSOVER CATBOX

- Documentation-only release; no runtime, schema, attachment storage, or provider behavior changed.
- Archived **PERNAH CROSSOVER CATBOX (Coming Soon, Maybe 🤔)** in `docs/BACKLOG.md` as IDEA PARKED / NOT COMMITTED / NOT IMPLEMENTED.
- The concept covers optional external attachment hosting for both evidence and personal memories, with privacy, credentials, deletion, backup portability, and local-first constraints explicitly left for future design review.
- The current canonical attachment implementation remains local SQLite BLOB storage (schema v4); Catbox is not integrated and is not the current next gate.
- Historical gate: Project Owner browser acceptance of image capture and Backup & Recovery; accepted on the packaged dev.62 artifact and recorded in dev.63.
- Parent artifact: `PERNAH-v0.2.0-dev.61.zip`.

## 0.2.0-dev.61 — Canonical Image Attachments (current)

- Schema v4 adds canonical `attachments` linked to `memories`; SQLite stores image bytes as BLOBs.
- Local Web Interface capture accepts JPEG, PNG, GIF, and WebP with 4-image / 8 MiB each / 12 MiB request limits and signature validation.
- Saved-memory view displays attached images through a same-origin route.
- Canonical JSON export/backup encodes image bytes as Base64; validation, import, and restore preserve them.
- Existing v3 SQLite databases migrate in place; v3 canonical JSON backups remain importable/restorable.
- AI/OCR interpretation, redaction, encryption-at-rest, and remote access are not implemented.
- Current gate: full automated suite and exact-artifact preflight, followed by Project Owner browser acceptance.

## 0.2.0-dev.60 — Atomic Ingestion + Continuity Repair

- `pernah.ingestion.ingest_draft()` now validates the transaction/event invariant before writing and wraps each draft in a SQLite savepoint.
- Any exception during ingestion rolls back source, memory, entity, event, event-entity, and transaction writes from that draft.
- Added regression coverage for invalid draft shape and downstream persistence failure.
- Continuity snapshots and release metadata are synchronized to `dev.60`; the original `dev.59` artifact remains immutable.
- Schema remained v3 in dev.60; no AI/provider runtime dependency was added in that release.

## 0.2.0-dev.59 — Chronicle Sidebar Scroll-Sync / Scrollspy

- Chronicle TOC now derives its active item from section position relative to the viewport instead of relying only on click/static state.
- Active TOC items auto-scroll within the sidebar when they move outside the sidebar viewport.
- Chronicle mobile sidebar now has backdrop and outside-pointer close behavior; taps inside the sidebar remain open.
- Parent artifact: `PERNAH-v0.2.0-dev.58.zip`.
- Baseline before patch: **160/160 PASS** (1 skipped).

## 0.2.0-dev.58 — Mobile Sidebar + Embedded Glossary Runtime Fix

- Fixed the embedded reference runtime so Glossary rendering no longer aborts when the standalone theme control is absent from the product shell.
- Hardened mobile Glossary outside-tap handling by explicitly binding the sidebar index element used by the pointer guard.
- Parent artifact: `PERNAH-v0.2.0-dev.57.zip`.

## 0.2.0-dev.57 — Chronicle: Obrolan Santai

- Documentation-only continuity update: Creation Chronicle section 42 records informal project conversation context.
- Runtime and canonical data behavior unchanged.

## 0.2.0-dev.56 — Hybrid Vocabulary + Glossary

- Canonical Glossary expanded from 133 to **153 entries**.
- New vocabulary includes `Failed to fetch`, `fetch`, `CSP`, `connect-src`, `python -m`, `--port`, `localhost`, `SPOK`, Product/UX/Engineering terms, and PERNAH internal vocabulary.
- Automated suite target: **current run pending packaging**.

## 0.2.0-dev.56 — Web UX Recovery Fixes

- Local Web restore fetch is now permitted by the dynamic page CSP through `connect-src 'self'`.
- Glossary rendering is hardened against unavailable localStorage.
- Mobile Glossary sidebar closes from backdrop, category selection, Escape, swipe, and any pointer/tap outside the open index.
- Automated suite: **158/158 PASS** (1 skipped).

## 0.2.0-dev.54 — CLI URL Auto-Copy

- `python -m pernah.web` now prints the local URL and best-effort copies the same URL to the system clipboard before serving requests.
- Clipboard integration is dependency-free and tries available local utilities for Termux, Wayland, X11, macOS, and Windows/WSL.
- Clipboard unavailability never blocks server startup.
- Automated suite: **158/158 PASS** (1 skipped).
- Exact artifact human acceptance: verify the URL lands in the clipboard on the target terminal environment.
- No canonical schema, storage semantics, AI/provider runtime dependency, or Secret Vault runtime changed.

## 0.2.0-dev.53 — Local Web Backup & Recovery UI

- Settings now exposes local Backup & Recovery controls.
- `GET /backup` downloads the canonical `pernah-canonical-v1` JSON state.
- `POST /restore` requires an explicit confirmation header, validates the backup, then delegates replacement to atomic `Storage.restore()`.
- Invalid restore payloads are rejected without mutating the existing canonical database.
- Automated suite: **156/156 PASS** (1 skipped).
- Exact artifact still requires the Project Owner's human Web Backup & Recovery browser test-drive.
- No canonical schema, storage semantics, AI/provider runtime dependency, or Secret Vault runtime changed.

## 0.2.0-dev.51 — Recovery Gate Automation + Exact Artifact Hygiene

- Added automated Web Interface recovery coverage: capture through the local HTTP interface, create and validate a canonical backup, remove the live database, restore it atomically, restart the server, and verify the saved-memory route remains readable and refresh-safe.
- Hardened exact-artifact hygiene so `.pytest_cache/` is explicitly rejected alongside Python bytecode/cache artifacts.
- Release preflight and release-integrity checks now enforce this cache hygiene contract.
- Automated suite: **149/149 PASS** (1 skipped).
- No canonical schema, storage semantics, AI/provider runtime dependency, or Secret Vault runtime changed.

## 0.2.0-dev.50 — Test Discovery + Language Boundary Hardening

- Converted the Memory Engine regression tests to the canonical stdlib `unittest` discovery contract; the three previously top-level pytest-style functions are now included in the release suite.
- Added a release-integrity regression guard that rejects top-level `test_*` functions in `tests/test_*.py`, preventing future tests from silently bypassing the canonical runner.
- Hardened lightweight language detection for mixed Sundanese/Indonesian input by allowing distinctive Sundanese markers to win an otherwise tied lexical score.
- Updated the Sundanese retrieval regression expectation to match the current deterministic query structure, including entity and original query text.
- Parent artifact: `PERNAH-v0.2.0-dev.49.zip`.
- Automated suite: **148/148 PASS** (1 skipped).
- No canonical schema, storage semantics, AI/provider runtime dependency, or Secret Vault runtime changed.

## 0.2.0-dev.49 — Knowledge-Surface Impact Gate

- Glossary and Creation Chronicle are now explicitly treated as canonical knowledge surfaces with distinct contracts.
- Added lightweight impact classification: `BOTH`, `GLOSSARY`, `CHRONICLE`, or `NONE`.
- Added 12 new canonical Glossary entries and Chronicle section 34.
- Added regression coverage for knowledge-surface consistency.
- Parent artifact: `PERNAH-v0.2.0-dev.48.zip`.
- Automated suite target: **144/144 PASS**.

## 0.2.0-dev.48 — Human Touch Behavioral Policy

- Human Touch policy is now explicit in CHECKPOINT, BOOT, and CONTINUATION: relevant humor, analogies, fun-facts, and human comments may appear naturally in normal collaboration, while critical/security/privacy/safety contexts prioritize clarity.
- Added regression coverage for behavioral-policy propagation.
- Parent artifact: `PERNAH-v0.2.0-dev.47-fixed.zip`.

## 0.2.0-dev.48 — Browser Visual Identity & Chronicle Index Fix

- Restored the embedded Creation Chronicle index by guarding the standalone-only theme control during content-fragment execution; the previous null theme-control exception prevented the Chronicle script from reaching TOC generation.
- Fixed the product shell Content Security Policy so same-origin `/docs/assets/pernah-symbol.svg` is allowed to render in the shell.
- Kept `/favicon.svg` backed by the canonical PERNAH symbol and added an explicit shortcut-icon declaration to the shared shell.
- Added regression coverage for same-origin brand-image CSP, favicon delivery, and content-only Chronicle script initialization.
- Automated suite target: **131/131 PASS**.
- Exact packaged artifact validation remains required after packaging.

## 0.2.0-dev.45 — Product Shell Reference Content Integration

- `/chronicle` and `/glossary` now load the canonical reference **content surface** inside the shared product shell instead of rendering the full standalone HTML page as an iframe.
- The product shell owns the only primary navigation; standalone reference pages retain their own full navigation only when opened directly.
- Embedded Chronicle / Glossary surfaces retain their content, search, index, print, and sidebar interactions, while the standalone document remains available through **Buka dokumen standalone →**.
- Added regression coverage to prevent duplicate primary navigation and iframe-based full-page embedding from returning.
- Automated suite: **129/129 PASS**.
- Next gate: packaged-artifact browser regression of dev.45.

## 0.2.0-dev.44 — Browser Consistency & Theme Unification

- Standalone reference pages now route the PERNAH brand back to product Home (`../`) rather than raw `README.md`.
- Added a static `index.html` Home fallback for simple static-server browser tests; the Python Web Interface continues to serve the live Home at `/`.
- Sidebar behavior: desktop uses the top toggle for collapse/expand; mobile uses the drawer toggle plus horizontal swipe gestures. The non-functional desktop `X` control was removed.
- Canonical symbol asset and favicon route remain the visual identity source of truth.
- Automated suite: **127/127 PASS**.
- Next gate: packaged-artifact browser regression of dev.44.

## 0.2.0-dev.42 — Browser Regression Hardening

- Fixed `/chronicle` and `/glossary` shell reader embedding so the canonical documents are frameable only by the same origin that serves the product shell.
- Product/application responses retain `X-Frame-Options: DENY`; static reference documents use `SAMEORIGIN` plus `frame-ancestors 'self'`.
- The parent shell CSP now allows `frame-src 'self'` only for this same-origin reader integration.
- Updated About philosophy copy with **“Karena yang berharga layak untuk dijaga 🫰”**.
- Automated suite target: **120/120 PASS**.
- Manual browser regression evidence: Chronicle and Glossary now render successfully in the packaged artifact; the previous embedded-content block is closed.
- Packaging contract: release ZIP must be flat-root (no enclosing version directory).
- Web CLI contract: access requests/responses are visible in the terminal via the standard HTTP server log.
- Brand contract: shell uses the canonical `docs/assets/pernah-symbol.svg`; `/favicon.svg` serves the same canonical symbol.
- Next gate: packaged-artifact browser regression of dev.42, specifically favicon/logo loading, CLI access logging, flat-root extraction, and shell navigation.

## 0.2.0-dev.39 — Domain + OpenWrt Deployment Concept

- Recorded **domain + OpenWrt** as the current low-cost personal deployment concept.
- Candidate domain: `pernah.my.id`.
- Candidate runtime: AmLogic HG680P running OpenWrt 24.10.4, available 24/7 in the current environment.
- Audit snapshot: ~1.76 GB RAM, ~29.12 GB data mount, ~3% CPU usage, ~39°C. These are observations, not benchmarks or deployment acceptance.
- Candidate public-access layer: Cloudflare Tunnel. GitHub Pages remains an optional static landing/docs surface, separate from the canonical runtime.
- SQLite remains the canonical local storage layer. No remote exposure, authentication, tunnel, domain routing, or OpenWrt deployment has been implemented yet.
- Automated suite remains **116/116 PASS** before and after this documentation-only change.
- Next gate remains Milestone 5 — Web App Shell & Navigation integration/hardening; deployment remains a documented future implementation track.

## 0.2.0-dev.38 — About / Author Profile

- Expanded `/about` from a minimal attribution page into an informative author profile for **@nexterade**.
- Added repository, email, and website links.
- Added project-relevant Skill Statistics focus areas without fabricated proficiency percentages.
- Added interests, builder profile, and the project philosophy **“Chat is ephemeral. Artifact is continuous.”**
- The planned product shell remains **Home · Memory · Chronicle/Perjalanan · Glossary · Settings · About**.
- Automated suite target: **113/113 PASS**.
- Next gate: browser regression of the About surface and continued Web App Shell & Navigation work.
- No canonical schema, storage semantics, AI/provider dependency, or Secret Vault runtime changed.

# PERNAH — Current State


## 0.2.0-dev.35 — Web Interface Static Documentation Serving

- The localhost Web Interface now serves the project reference library from the same server: `/docs/Glosarium.html`, `/docs/Creation-Chronicle.html`, `/docs/assets/...`, plus `/README.md`.
- `/docs/` redirects to the Glossary; static serving is restricted to `.html`, `.css`, `.svg`, and `.md` with path-traversal protection.
- Static documentation responses use a same-origin CSP while preserving the existing security baseline.
- Automated suite: **113/113 PASS**.
- Next gate: browser regression of the single-server documentation flow.

## 0.2.0-dev.34 — Web Interface Hardening: Post/Redirect/Get

- Changed successful web capture from direct POST response rendering to **Post/Redirect/Get (PRG)**: `POST /capture` persists once, returns `303`, then the browser renders the saved result through `GET /?saved=...`.
- Refreshing the result page now repeats a GET rather than resubmitting the capture form, eliminating the browser `Confirm Form Resubmission` flow for normal refreshes.
- Added regression coverage for the 303 redirect, result GET, repeated refresh, and saved-memory lookup behavior.
- Expanded `docs/Glosarium.html` with core HTTP/Web terms: HTTP, GET, POST, Request, Response, Redirect, Post/Redirect/Get (PRG), Endpoint, and Idempotency.
- Automated suite: **109/109 PASS**.
- No canonical schema, storage semantics, AI/provider dependency, or Secret Vault runtime changed.

## 0.2.0-dev.33 — Web Interface Hardening Slice

- Hardened the Local Web Interface request boundary without changing the canonical capture pipeline.
- Added strict form content-type validation, UTF-8 decoding, single-text-field enforcement, 64 KiB request-body limit, and explicit malformed-input handling.
- Added `GET /health` to verify the local SQLite-backed service is reachable and healthy.
- Added baseline security headers for browser responses: `Cache-Control: no-store`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, and a restrictive Content Security Policy.
- Added six Web Interface regression tests; automated suite is now **107/107 PASS**.
- No canonical schema, storage semantics, AI/provider dependency, or Secret Vault runtime changed.
- The next gate remains **Web Interface hardening**; the PRG fix now needs browser regression acceptance.

## 0.2.0-dev.32 — Web Interface Warung Padang Acceptance

- The Project Owner completed the real-browser **Warung Padang** test drive of the Local Web Interface on the packaged `v0.2.0-dev.31` artifact and marked it **PASS**.
- The initial Local Web Interface is therefore accepted as a product-facing input slice for Milestone 5.
- Browser capture and retrieval behavior remain backed by the existing provider-neutral capture/retrieval and canonical SQLite boundaries.
- No canonical schema, storage semantics, AI/provider dependency, or Secret Vault runtime changed.
- The next implementation gate is **Web Interface hardening**.

## 0.2.0-dev.31 — PERNAH Visual Identity System

- Formalized the shared visual identity in `docs/assets/DESIGN-SYSTEM.md` and `pernah-design-tokens.css`.
- Extended the Symbol + Wordmark / Continuity P identity beyond Creation Chronicle to the Glossary and Local Web Interface surfaces.
- Standardized the core dark/light palette, LEMON MILK + Open Sans typography direction, navigation, theme control, responsive interaction, status/provenance language, and floating action treatment.
- Removed the Glossary's remote font dependency so the project-facing HTML remains offline-friendly.
- Refreshed `pernah.web` with the same visual language while preserving its existing localhost capture and canonical ingestion behavior.
- Added shared visual-system regression coverage.
- No canonical schema, storage semantics, AI/provider dependency, or Secret Vault runtime changed.
- Feature state remains **v0.2.0-dev.28 — Local Web Interface**; this release is a cross-surface visual/brand layer.

## 0.2.0-dev.30 — Visual Identity Foundation + Chronicle Theme System

- Established the **Symbol + Wordmark / Continuity P** visual identity direction for PERNAH: Memory · Knowledge · Continuity.
- Added standalone brand assets under `docs/assets/` for symbol-only, lockup, monochrome, and identity guidance.
- Refactored the Creation Chronicle visual shell to use the PERNAH palette (`#141414` / `#2BEE34` with a restrained light-theme counterpart) and LEMON MILK + Open Sans typography declarations.
- Added light/dark theme toggle with local persistence, responsive sidebar toggle, primary navigation, and a floating back-to-top action.
- Added reduced-motion support and kept the Chronicle standalone/offline-friendly.
- No canonical schema, storage, Web Interface runtime, AI/provider, or Secret Vault behavior changed.
- Feature state remains **v0.2.0-dev.28 — Local Web Interface**; this release is a visual/brand layer over that feature state.
- Added `tests/test_brand_identity.py`.

## 0.2.0-dev.29 — Creation Chronicle Integrity + Visual Refactor

- Refactored `docs/Creation-Chronicle.html` as a documentation-only release; canonical implementation behavior is unchanged.
- Established an explicit Chronicle contract covering primary record, source discipline, chronology, current-state labeling, separation from CHANGELOG, and preservation of historical facts.
- Reordered late milestones into chronological sequence through the v0.2.0-dev.28 Web Interface state and consolidated the current handoff into one final section.
- Repaired duplicate/ambiguous section IDs and moved the table of contents to a heading-driven dynamic index so navigation cannot silently drift from the document structure.
- Refreshed the visual presentation into an editorial/timeline-style archive while preserving standalone, mobile, print, and search behavior.
- Added `tests/test_chronicle_integrity.py` for section numbering, IDs, chronology, contract, historical labeling, and dynamic TOC guards.
- No canonical schema, storage, Web Interface runtime, AI/provider, or Secret Vault behavior changed.

## 0.2.0-dev.28 — Local Web Interface

- Added `pernah.web` as a minimal local web input interface using Python standard-library HTTP server.
- Web POST `/capture` reuses `capture_text()` and the existing provider-neutral normalization/ingestion path.
- Web provenance is recorded as `source_type="web"`; canonical storage remains SQLite.
- Server binds to localhost by default; no remote exposure, authentication, cloud transport, or Secret Vault runtime was added.
- Added integration coverage for GET form, successful persistence, provenance, and blank-input rejection.


## 0.2.0-dev.27 — Data Classification & Privacy Boundary

- Added `docs/SECURITY.md` as the source of truth for Normal Data, Sensitive Data, and Secret Data classification.
- Established the canonical retention rule: canonical data is not automatically pruned or expired by maintenance, retrieval, indexing, backup, or optimization.
- Established the boundary that Secret Data must not be stored plaintext as Memory Core canonical data.
- Recorded Secret Vault as a separate future capability; no encryption, key-management, or vault runtime was implemented in this release.
- No canonical schema or storage behavior changed.


## 0.2.0-dev.26 — Documentation & Artifact Hygiene

- Retired the legacy root `Readme.md`; `README.md` remains the canonical project overview.
- Cleaned duplicated historical blocks from `docs/CHANGELOG.md` and corrected the manual-input API reference.
- Synchronized the documented glossary count to **101 unique indexed terms**.
- Clarified that the manual CLI is already a user-facing runtime slice; the remaining product-facing runtime gate is the Web Interface.
- Added a minimal manual-input tutorial.
- No canonical schema, storage, or AI/provider behavior changed.
- Documentation/artifact hygiene test coverage is included.

## 0.2.0-dev.25 — Manual Input Interface

- Added `pernah.manual_input.capture_text()` as the first explicit product-facing input boundary over the existing provider-neutral normalization and ingestion pipeline.
- Added `python -m pernah.manual` for one-shot or interactive local manual capture into SQLite.
- Manual capture preserves original input through the existing `MemoryDraft`/ingestion path and does not introduce an AI/provider dependency.
- Added regression coverage for direct capture, blank-input rejection, relative-time normalization, and CLI persistence.
- Automated suite: **77/77 PASS** before documentation/package validation.

## Project identity

- **Name:** PERNAH
- **Expansion:** Personal Memory & Life Context System
- **Status:** Active implementation; `v0.2.0-dev.34` is the current Web Interface hardening slice


## 0.2.0-dev.24 — Portable Export/Import Hardening + Disaster Recovery

- Hardened `Storage.export_json()` as an atomic portable export that creates missing parent directories before promotion.
- Added `Storage.import_json()` as a file-oriented import path with canonical and isolated relational validation before mutation.
- Tightened `import_canonical()` with relational preflight while preserving its merge/dedup-oriented conflict handling.
- Added a local disaster-recovery drill that removes a temporary live database and reconstructs it from a validated canonical backup, plus corrupted-backup safety coverage.
- Added the glossary term **Disaster Recovery**.
- Automated suite: **72/72 PASS**.

## 0.2.0-dev.23 — Restore Workflow + Chronicle Audit + Glossary Update

- Added `Storage.restore()` for safe replacement of a target SQLite database from a validated `pernah-canonical-v1` backup.
- Restore validates the backup first, stages the recovered database in a temporary file, compares the restored canonical export with the source backup, then atomically promotes the staged file.
- Invalid or failed restore attempts do not mutate an existing target database.
- Updated Creation Chronicle sessions 23–24 to restore Indonesian historical language consistency, added the restore milestone, and refreshed the current handoff.
- Added glossary entries for Arsiparis, Restore, Recovery, Backup Validation, and Chronicle Editorial Consistency.
- Automated suite: **66/66 PASS**.

## 0.2.0-dev.22 — Local Backup + Backup Validation

- Added `Storage.backup()` over the existing canonical `pernah-canonical-v1` JSON contract.
- Made canonical export deterministic by ordering each table by its full column set.
- Added strict backup validation for format, schema, exact canonical table set, and exact row columns.
- Added isolated SQLite relational validation with foreign-key enforcement; invalid references and constraint violations are rejected before a backup is considered valid.
- Preserved the existing import round-trip contract while tightening canonical payload validation.
- No schema migration and no AI/provider dependency.
- Automated suite: **60/60 PASS**.

## 0.2.0-dev.19 — Continuity Layer v1

- Added `PERNAH_BOOT.md` as a fast, human-readable cross-chat boot snapshot.
- Added `PERNAH_PROJECT_STATE.json` as a machine-readable boot snapshot; it is derived
  state and does not outrank CHECKPOINT/STATE/BACKLOG.
- Added `docs/RELEASE-MANIFEST.md` for explicit release lineage and validation contract.
- Strengthened continuation documentation around the principle **CHAT IS EPHEMERAL.
  ARTIFACT IS CONTINUOUS.**
- Added the glossary term **Ephemeral** for the new continuity vocabulary.
- Automated suite: **45/45 PASS**.
- No canonical schema change and no AI/provider dependency introduced.

## 0.2.0-dev.18 — Semantic concept vocabulary + ranking boundaries

- Expanded deterministic local concept normalization across purchase, food, conversation, call, meeting, collaboration, device, passport, commitment, and decision concepts.
- Added a deterministic concept-relevance boundary so a recognized query concept cannot be answered solely by shared generic tokens such as a person's name.
- Added ranking/false-positive regression coverage for conversation, phone, and unrelated food queries.
- Updated continuation governance so Creation Chronicle and Glosarium are mandatory in the initial context sweep.
- Automated suite: **40/40 PASS**.

## 0.2.0-dev.17 — Rebuildable deterministic semantic retrieval

- Added `pernah/semantic.py` as a derived-only in-memory TF-IDF index over canonical memory content.
- Added deterministic local concept normalization for supported synonym groups (for example purchase/buy and laptop/computer).
- Added semantic retrieval as a fallback behind canonical deterministic purchase retrieval: canonical hits always win; the derived index is used only when the deterministic path returns no result.
- Added generic natural-language question routing to `semantic_retrieval` for queries outside the existing deterministic purchase/relationship contracts.
- The derived index is rebuilt from canonical SQLite memories on demand and is never persisted as canonical state.
- No schema migration or external AI/provider dependency was introduced.
- Automated suite: **37/37 PASS**.

## 0.2.0-dev.16 — Richer deterministic entity relationships

- Added deterministic relationship/event patterns for conversation, call, and collaboration in addition to meeting.
- Extended person extraction for the supported relationship prefixes without changing canonical schema.
- Extended entity-scoped retrieval to apply an optional deterministic event-type filter.
- Added regression coverage for persistence, retrieval, and temporal filtering of the richer relationship patterns.
- Canonical test suite: **34/34 PASS**.


## Documentation / continuation workflow update — 2026-10-06

Strengthened `docs/CHECKPOINT.md` with a **top-level, uppercase/bold mandatory continuation rule** so the required reading/implementation order is immediately visible when a new chat starts from a ZIP handoff. The order remains: CHECKPOINT → README → STATE → BACKLOG → CHANGELOG → source + tests → relevant Creation Chronicle / Glosarium → plan → implement → test → document sync → package → test exact artifact → deliver accessible artifact. The rule also prohibits claiming full context/state understanding before the relevant artifact sweep is actually completed.

## Documentation / governance adaptation update — 2026-10-06

Applied the uploaded starter CHECKPOINT as the current PERNAH governance baseline and
completed the project adaptation pass in Section 6. The adaptation records PERNAH's
stable identity, canonical-memory principles, local/offline core, runtime/storage
baseline, multilingual understanding contract, documentation sources of truth, and
interface boundary without moving volatile implementation state into CHECKPOINT.


## Documentation / glossary update — 2026-10-05

`docs/Glosarium.html` is a universal knowledge dictionary designed for long-term growth toward hundreds/thousands of entries across domains, ecosystems, and audiences. Existing glossary terminology was preserved; the current build contains 107 unique indexed terms. Search, category filtering, alphabet navigation, responsive layout, print behavior, two-font typography (LEMON MILK + Open Sans), and a persistent Night/Day theme toggle are implemented in the standalone HTML.

The redesign is documentation/UI scope only and does not change canonical storage, Memory Engine behavior, or product data. The current glossary build contains 107 unique indexed terms after adding the continuity/recovery terminology and the data-classification/privacy boundary terms.



## Documentation / governance integrity update — 2026-10-06

`docs/CHECKPOINT.md` now includes explicit content-update procedures and regression guards for `docs/Glosarium.html` and `docs/Creation-Chronicle.html`. Content-only updates must preserve approved presentation/UI invariants and existing historical/content records unless the user explicitly requests structural changes.

## 0.2.0-dev.21 — Glossary UTF-8 integrity fix

- Fixed double-encoded UTF-8 punctuation in `docs/Glosarium.html` that rendered as mojibake such as `â...` in the browser.
- Confirmed the root cause is corrupted character encoding in the canonical glossary data, not a missing HTML charset declaration.
- Added a regression test that validates UTF-8 decoding and rejects C1 control / common UTF-8 mojibake markers.
- Added an explicit CHECKPOINT encoding-integrity rule so future glossary edits cannot silently reintroduce the defect.
- No canonical schema change and no runtime/provider dependency change.

## 0.2.0-dev.20 — Collaborative AI working style / resource-aware governance

- Strengthened CHECKPOINT Section 2 and PERNAH-specific collaboration rules so the AI acts as a Co-Developer and discussion partner, not only a command executor.
- Added explicit expectations for proactive technical/product feedback, constructive disagreement, option comparison, and recommendation of the best-fit solution under current project constraints.
- Added cost/resource-aware guidance: when no paid service is required, prefer free-tier, local-first, offline, open-source, or low-cost options; do not assume or store personal financial circumstances as project rules.
- Preserved continuation autonomy: when artifact evidence already determines the next gate, the AI should continue rather than ask for unnecessary confirmation.
- No canonical schema change. No AI provider dependency introduced.

## Current collaboration model

PERNAH treats the AI as a **Co-Developer + Partner Diskusi**, not merely a command executor. The AI should proactively surface better alternatives, risks, trade-offs, and root causes while respecting the Project Owner as the final decision maker. Explicit resource constraints are treated as real constraints; when paid services are not required, free/local/offline/low-cost options are preferred.

## Current milestone

**Milestone 5 — Input Interfaces**

Milestone 4 is complete through local backup, validation, restore, portable export/import hardening, and a controlled disaster-recovery drill. The next product-facing slice is input interfaces; the manual input slice is now implemented and the next slice is the local web interface.

## Completed

- Product concept consolidated under one system.
- Local-first + optional encrypted online backup architecture selected as direction.
- Canonical vs derived data separation defined.
- Historical/temporal persistence model defined.
- Canonical Data Model v0.1 reviewed.
- Core logical entities defined: Memory, Entity, Event, Relationship, Commitment, Decision, Transaction, Physical Object, Location, Source, Confidence.
- SQLite canonical storage foundation implemented with schema version 1.
- UUID4 identifiers and UTC ISO 8601 timestamps selected for v0.1.
- Core storage implemented for Source, Entity, Memory, and temporal Relationship records.
- Canonical JSON export/import implemented.
- Physical Event, Commitment, Decision, and Transaction tables implemented with schema migration v1→v2.
- Deterministic Memory Engine foundation implemented without AI provider dependency.
- Multi-language input foundation preserves original text and detects supported language patterns.
- MemoryDraft normalization supports purchase capture and temporal retrieval examples.
- Automated suite: 40/40 PASS via the canonical stdlib unittest discovery command.

## Not implemented yet

- The initial Local Web Interface is implemented and manually accepted; hardening remains the next product-facing runtime slice.
- Restore workflow is implemented for validated local canonical backups; cloud recovery, scheduling, and disaster-recovery automation remain deferred.
- Backup service remains local-only; no cloud sync or scheduler.
- No WhatsApp integration.
- No AI provider integration.
- No cloud sync.

## Source of truth

- `CHECKPOINT.md` — stable project rules.
- `docs/STATE.md` — current implementation state.
- `docs/BACKLOG.md` — planned work.
- `docs/CHANGELOG.md` — history.
- `docs/ARCHITECTURE.md` — current architecture blueprint.
- `docs/Glosarium.html` — terminology.
- `README.md` — project overview.
- `PERNAH_BOOT.md` — fast boot snapshot; not authoritative over CHECKPOINT/STATE.
- `PERNAH_PROJECT_STATE.json` — machine-readable boot snapshot; not authoritative over CHECKPOINT/STATE.
- `PERNAH_CONTINUATION.md` — compact handoff aid; CHECKPOINT/STATE remain authoritative.
- `docs/RELEASE-MANIFEST.md` — release lineage/validation record.

## Next implementation gate

Current gate (dev.61): validate canonical image attachments against the full suite and exact packaged artifact, then obtain Project Owner browser acceptance for image capture and existing Backup & Recovery / clipboard UX checks. Schema v4 adds canonical image attachments and preserves v3 database and backup compatibility. After product-facing Milestone 5 gates are accepted, reassess Milestone 6 — AI Layer; do not introduce provider coupling before deterministic capture/retrieval and attachment contracts are stable.

The manual input and initial Local Web Interface slices are implemented, and the latter passed the earlier Warung Padang manual acceptance gate. Milestone 4 — Backup & Recovery is implemented through local backup, validation, restore, portable export/import hardening, and a controlled disaster-recovery drill. Continuity Layer v1 remains the cross-chat recovery mechanism. AI provider integration remains deferred until the deterministic contract is stable.

## Milestone 1 update — 2026-10-05

Canonical storage schema version pada milestone awal adalah **3**. Physical storage untuk Event, Commitment, Decision, dan Transaction sudah tersedia, termasuk migration v1→v2→v3, event-entity links, dan canonical JSON export/import. Automated suite: **8/8 PASS**. Memory Engine, retrieval, AI, dan WhatsApp belum diimplementasikan.


## Milestone 2 update — 2026-10-05

Implemented `pernah/memory_engine.py` as a deterministic, provider-neutral normalization layer. It currently supports explicit Indonesian/Sundanese examples, preserves original input, detects language, extracts laptop entities, parses common IDR amounts, resolves selected relative-time expressions against a supplied reference time, and distinguishes purchase capture from temporal retrieval queries. Automated suite: **11/11 PASS**.


## Milestone 2 persistence update — 2026-10-05

Implemented `pernah/ingestion.py` and `pernah/retrieval.py`. Supported purchase MemoryDrafts now persist source provenance, object entity, purchase event, transaction, and original interaction memory. Events can be explicitly linked to entities through `event_entities`. Supported temporal retrieval queries can return persisted purchase records by object entity. Automated suite: **14/14 PASS**.


## Retrieval expansion update — 2026-10-06

Implemented the first broader deterministic retrieval slice. Purchase retrieval can now return all matching purchases when the query omits an object, and the canonical storage retrieval method accepts inclusive `occurred_after` / `occurred_before` ISO 8601 filters. Entity-scoped purchase retrieval now uses an existence constraint so multiple event-entity links do not duplicate the same purchase row. The deterministic query contract remains provider-neutral.


## Milestone 3 temporal expansion update — 2026-10-06

Expanded deterministic natural-language temporal query extraction beyond yesterday/today.
Supported query windows now include numeric day offsets such as `3 hari lalu` / `3 days ago`,
`minggu lalu` / `last week`, `minggu ini` / `this week`, `bulan lalu` / `last month`, and
`bulan ini` / `this month`. English meeting queries now resolve through the same entity
relationship retrieval path. Query windows are normalized to inclusive UTC ISO 8601 boundaries;
the canonical data model remains unchanged. Automated suite: 30/30 PASS.

## Creation Chronicle HTML

- Canonical presentation: `docs/Creation-Chronicle.html`.
- Creation Chronicle remains a historical derived record; raw conversation export remains the primary record.
- Markdown source may remain as working source, but official project presentation is standalone HTML.


## Milestone 3 retrieval update — 2026-10-06

Implemented the first entity-scoped relationship retrieval and timeline slice. Supported queries such as `Gue pernah ketemu Rahayu kapan aja?` resolve the named entity, retrieve related canonical events through `event_entities`, preserve participant roles, and return a deterministic chronological timeline with related entities and source memories. Temporal day filtering reuses the deterministic yesterday/today contract. Automated suite: 26/26 PASS.
