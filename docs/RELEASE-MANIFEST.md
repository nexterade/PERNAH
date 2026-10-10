## 0.2.0-dev.62 — Roadmap Parking Lot: PERNAH CROSSOVER CATBOX

- **Version:** `0.2.0-dev.62`
- **Parent artifact:** `PERNAH-v0.2.0-dev.61.zip`
- **Scope:** documentation-only roadmap entry for a possible future Catbox attachment-hosting integration.
- **Status:** IDEA PARKED / NOT COMMITTED / NOT IMPLEMENTED.
- **Runtime/schema changes:** none; schema remains v4 and attachments remain stored in local SQLite BLOBs.
- **Validation:** run full suite and exact packaged-artifact preflight before delivery.
- **Artifact SHA-256:** record after packaging, outside the ZIP.

## 0.2.0-dev.61 — Canonical Image Attachments

- **Version:** `0.2.0-dev.61`
- **Parent artifact:** `PERNAH-v0.2.0-dev.60.zip`
- **Scope:** schema v4 image attachments linked to Memory, bounded local multipart capture, image preview/serving, and backup/restore compatibility.
- **Migration:** existing SQLite v3 databases migrate to v4; v3 canonical JSON backups are upgraded during validation/import/restore.
- **Security:** JPEG/PNG/GIF/WebP only; signature validation; max 4 attachments, 8 MiB each, 12 MiB per request; no remote exposure or external AI processing.
- **Automated suite:** **170 passed, 1 skipped** (171 discovered); exact packaged-artifact validation must also pass.
- **Artifact SHA-256:** record after packaging, outside the ZIP.

## 0.2.0-dev.60 — Atomic Ingestion + Continuity Repair

- **Version:** `0.2.0-dev.60`
- **Parent artifact:** `PERNAH-v0.2.0-dev.59.zip`
- **Scope:** atomic draft ingestion, failure-path regression coverage, and continuity/release metadata synchronization.
- **Schema:** v3 (unchanged).
- **Source-tree suite:** **163 passed, 1 skipped** (164 discovered).
- **Automated suite target:** full suite must pass against the exact packaged ZIP.
- **Artifact SHA-256:** recorded in delivery notes after packaging; not embedded here to avoid a self-referential ZIP hash.

## Current artifact

- **Project:** PERNAH
- **Version:** `0.2.0-dev.62`
- **Schema:** `v4`
- **Previous artifact:** `PERNAH-v0.2.0-dev.61.zip`
- **Current artifact SHA-256:** recorded in delivery notes after packaging; not embedded here to avoid a self-referential ZIP hash.

## 0.2.0-dev.59 — Chronicle Sidebar Scroll-Sync / Scrollspy

- **Version:** `0.2.0-dev.59`
- **Parent artifact:** `PERNAH-v0.2.0-dev.58.zip`
- **Scope:** Chronicle sidebar active-state synchronization and mobile outside-close behavior.
- **Automated suite target:** full suite must pass before delivery.
- **No changes:** canonical schema, storage semantics, AI/provider runtime dependency, Secret Vault runtime.

## 0.2.0-dev.58 — Mobile Sidebar + Embedded Glossary Runtime Fix

- **Version:** `0.2.0-dev.58`
- **Parent artifact:** `PERNAH-v0.2.0-dev.57.zip`
- **Automated suite target:** **160/160 PASS** (1 skipped).
- **Scope:** embedded Glossary initialization and mobile outside-tap event handling.
- **No changes:** canonical schema, storage semantics, AI/provider runtime dependency, Secret Vault runtime.

## 0.2.0-dev.57 — Chronicle: Obrolan Santai

- **Version:** `0.2.0-dev.57`
- **Parent artifact:** `PERNAH-v0.2.0-dev.56.zip`
- **Change:** documentation-only Chronicle update; added section 42 for informal project conversation context.
- **Automated suite target:** **158/158 PASS** (1 skipped).
- **No runtime changes:** canonical schema, storage semantics, AI/provider runtime dependency, and Secret Vault runtime remain unchanged.

## 0.2.0-dev.56 — Hybrid Vocabulary + Glossary

- **Version:** `0.2.0-dev.56`
- **Parent artifact:** `PERNAH-v0.2.0-dev.55.zip`
- **Change:** canonical Glossary expanded by 20 entries; hybrid vocabulary direction formalized.
- **Canonical dictionary size:** **153 entries**.
- **Automated suite target:** full suite must pass before delivery.

## 0.2.0-dev.56 — Web UX Recovery Fixes

- **Version:** `0.2.0-dev.56`
- **Parent artifact:** `PERNAH-v0.2.0-dev.54.zip`
- **Automated suite target:** **158/158 PASS** (1 skipped).
- **Restore UI:** fixed the live Settings CSP so same-origin `/restore` fetch requests are permitted instead of being blocked by browser policy.
- **Glossary:** hardened theme storage handling so an unavailable browser localStorage cannot abort glossary rendering; dictionary initialization remains usable.
- **Mobile index:** added a document-level outside-tap guard so tapping anywhere outside the open index closes it, in addition to the backdrop control.
- **Current product gate:** Project Owner human browser test-drive of Backup & Recovery, Glossary rendering, and mobile index close behavior on this exact artifact.

## 0.2.0-dev.54 — CLI URL Auto-Copy

- **Version:** `0.2.0-dev.54`
- **Parent artifact:** `PERNAH-v0.2.0-dev.53.zip`
- **Automated suite target:** **158/158 PASS** (1 skipped).
- **CLI startup:** the local Web Interface URL is printed and best-effort copied to the first available supported clipboard utility.
- **Fallback:** missing or failing clipboard utilities never prevent the server from starting.
- **Current product gate:** Project Owner manual confirmation of clipboard auto-copy on the target terminal, plus the existing human Web Backup & Recovery browser test-drive.

## 0.2.0-dev.53 — Local Web Backup & Recovery UI

- **Version:** `0.2.0-dev.53`
- **Parent artifact:** `PERNAH-v0.2.0-dev.52.zip`
- **Automated suite target:** **156/156 PASS** (1 skipped).
- **Backup UI:** Settings can download the canonical `pernah-canonical-v1` JSON state.
- **Restore UI:** selected JSON backups are validated and restored atomically after explicit confirmation.
- **Recovery safety:** invalid restore payloads are rejected without mutating the target database.
- **Current product gate:** Project Owner human Web Backup & Recovery browser test-drive on this exact artifact.

## 0.2.0-dev.51 — Recovery Gate Automation + Exact Artifact Hygiene

- **Version:** `0.2.0-dev.51`
- **Parent artifact:** `PERNAH-v0.2.0-dev.50.zip`
- **Automated suite target:** **149/149 PASS** (1 skipped).
- **Recovery coverage:** Web capture survives canonical backup, controlled live-database deletion, validated restore, server restart, and refresh.
- **Artifact hygiene:** `.pytest_cache/`, Python bytecode, and generated runtime/test caches are forbidden in the packaged ZIP.

## 0.2.0-dev.50 — Test Discovery + Language Boundary Hardening

- **Version:** `0.2.0-dev.50`
- **Parent artifact:** `PERNAH-v0.2.0-dev.49.zip`
- **Automated suite target:** **148/148 PASS** (1 skipped).
- **Test discovery:** all `tests/test_*.py` regression tests now use the canonical stdlib `unittest` discovery contract; a regression guard rejects top-level `test_*` functions.
- **Language boundary:** mixed Sundanese/Indonesian lexical ties now prefer distinctive Sundanese markers; retrieval regression expectation reflects the current deterministic query payload.
- **No changes:** canonical schema, storage semantics, AI/provider runtime dependency, Secret Vault runtime.

## 0.2.0-dev.49 — Knowledge-Surface Impact Gate

- **Version:** `0.2.0-dev.49`
- **Parent artifact:** `PERNAH-v0.2.0-dev.48.zip`
- **Automated suite target:** **144/144 PASS**.
- **Knowledge-surface policy:** lightweight `BOTH / GLOSSARY / CHRONICLE / NONE` impact classification.
- **Glossary:** 12 new governance/communication terminology entries.
- **Chronicle:** section 34 records the knowledge-surface consistency gate and rationale.
- **Regression coverage:** added `tests/test_knowledge_surface_consistency.py`.
- **No changes:** canonical schema, storage semantics, AI/provider runtime dependency, OpenWrt deployment runtime.

## 0.2.0-dev.48 — Human Touch Behavioral Policy

- **Version:** `0.2.0-dev.48`
- **Parent artifact:** `PERNAH-v0.2.0-dev.47-fixed.zip`
- **Automated suite target:** **TBD until exact artifact validation completes**.
- **Behavioral policy:** FUN-FACT / HUMAN TOUCH is explicitly propagated through CHECKPOINT → BOOT → CONTINUATION with context-sensitive exceptions.
- **Regression coverage:** added `tests/test_human_touch.py`.
- **No changes:** canonical schema, storage semantics, AI/provider runtime dependency, OpenWrt deployment runtime.

## 0.2.0-dev.48 — Release Integrity Gate + Prompt Translation

- **Version:** `0.2.0-dev.48`
- **Parent artifact:** `PERNAH-v0.2.0-dev.46.zip`
- **Automated suite target:** **138/138 PASS**.
- **Artifact Compliance Gate:** validates SemVer/lineage, release metadata synchronization, required structure, flat-root packaging, documentation consistency, Chronicle + Glossary integrity coverage, provenance, and artifact hygiene.
- **Prompt workflow:** CHECKPOINT now formalizes `RAW IDEA → REQUIREMENT → PROMPT TRANSLATION` before execution planning.
- **No changes:** canonical schema, storage semantics, AI/provider runtime dependency, OpenWrt deployment runtime.

## 0.2.0-dev.46 — Browser Visual Identity & Chronicle Index Fix

- **Version:** `0.2.0-dev.46`
- **Parent artifact:** `PERNAH-v0.2.0-dev.45.zip`
- **Automated suite target:** **131/131 PASS**.
- **Chronicle:** embedded TOC/index initialization restored by guarding the absent standalone theme control.
- **Brand:** product shell CSP now permits same-origin SVG image rendering for the canonical PERNAH symbol.
- **Favicon:** `/favicon.svg` remains backed by the canonical symbol; shared shell declares both icon and shortcut-icon links.
- **No changes:** canonical schema, storage semantics, AI/provider dependency, OpenWrt deployment runtime.

## 0.2.0-dev.45 — Product Shell Reference Content Integration

- **Version:** `0.2.0-dev.45`
- **Parent artifact:** `PERNAH-v0.2.0-dev.44.zip`
- **Automated suite target:** **129/129 PASS**.
- **Reference integration:** Home shell `/chronicle` and `/glossary` render content fragments from the canonical standalone documents rather than full-page iframes.
- **Navigation contract:** one primary product navigation in shell; standalone navigation appears only on direct `/docs/*.html` access.
- **Standalone access:** embedded surfaces expose a direct standalone link.
- **No changes:** canonical schema, storage semantics, AI/provider dependency, OpenWrt deployment runtime.

## 0.2.0-dev.44 — Browser Consistency & Theme Unification

- **Version:** `0.2.0-dev.44`
- **Automated suite target:** **127/127 PASS**.
- **Navigation:** standalone Chronicle / Glossary brand links return to product Home; `README.md` remains documentation.
- **Sidebar:** desktop collapse/expand via toggle; mobile drawer supports horizontal swipe gestures; desktop-only `X` removed.
- **Static smoke test:** root `index.html` provides a lightweight Home fallback when using `python -m http.server`.
- **Brand:** canonical `docs/assets/pernah-symbol.svg` remains the shared asset; `/favicon.svg` remains the live-server favicon route.
- **No changes:** canonical schema, storage semantics, AI/provider dependency, OpenWrt deployment runtime.

## 0.2.0-dev.42 — Browser Regression Hardening

- **Version:** `0.2.0-dev.42`
- **Automated suite target:** **120/120 PASS**.
- **Manual regression:** Chronicle and Glossary reader surfaces verified rendered in the packaged browser test; the `dev.40` embedded-content block is closed.
- **Packaging:** flat-root ZIP; no enclosing version directory.
- **CLI:** standard HTTP access logging visible during runtime.
- **Brand:** shared shell references canonical `docs/assets/pernah-symbol.svg`; `/favicon.svg` uses the same source.
- **No changes:** canonical schema, storage semantics, AI/provider dependency, OpenWrt deployment runtime.

## 0.2.0-dev.41 — Shared Reader Security + About Philosophy

- **Version:** `0.2.0-dev.41`
- **Scope:** Fix same-origin reader embedding for Chronicle / Glossary and update About philosophy copy.
- **Security contract:** application routes remain `X-Frame-Options: DENY`; static reference documents use `SAMEORIGIN` with `frame-ancestors 'self'`; parent shell permits `frame-src 'self'`.
- **Automated suite:** **117/117 PASS**.
- **Manual status:** browser regression pending on the exact packaged artifact.
- **Canonical schema/storage:** unchanged.
- **Deployment/OpenWrt:** unchanged; concept remains not implemented.

## 0.2.0-dev.40 — Shared Product Shell Integration

- Parent artifact: `PERNAH-v0.2.0-dev.39.zip`
- Scope: product shell integration only.
- `/chronicle` and `/glossary` now render inside the shared shell while preserving canonical standalone docs under `/docs/`.
- `/about` now uses the same shared shell.
- Automated suite: **116/116 PASS**.
- ZIP checksum is recorded only in the delivery record after packaging.

# PERNAH — Release Manifest

## 0.2.0-dev.39 — Domain + OpenWrt Deployment Concept

- Documentation-only release.
- Recorded `pernah.my.id` + OpenWrt / AmLogic HG680P as a candidate low-cost personal runtime pattern.
- Recorded Cloudflare Tunnel as a candidate public-access mechanism and GitHub Pages as an optional static landing/docs layer.
- Preserved SQLite as canonical local storage and explicitly kept remote exposure/authentication/tunnel deployment out of the current runtime.
- Automated suite: **116/116 PASS**.

## What changed

### Web App Shell & Navigation

- Added the first product-facing application shell with Home, Memory, Chronicle, Glossary, Settings, and About navigation.
- Reframed `/` as the product Home instead of exposing `README.md` as the default user-facing index.
- Added `/memory` and `/settings` product routes; `/chronicle` and `/glossary` now have stable product routes entering the existing reference surfaces.
- Preserved POST/Redirect/GET capture flow and returned saved-memory results inside the product shell.
- Added regression coverage for the shell routes, navigation, Home identity, and capture-result continuity.
- Automated suite: **116/116 PASS**.


### About / Author Profile

- Expanded `/about` into a product-facing author profile for **@nexterade**.
- Added repository, email, and website links.
- Added project-relevant skill focus areas, interests, builder profile, and the philosophy “Chat is ephemeral. Artifact is continuous.”
- Added regression coverage for profile content and links.
- Automated suite is **113/113 PASS**.
- No canonical schema, storage, provider, or Secret Vault runtime change.


### About / Author Surface

- Added product-facing `/about` route to the localhost Web Interface.
- Author attribution: **@nexterade**.
- Added About link to the current Web Interface footer.
- Established About as part of the planned product shell: Home, Memory, Chronicle/Perjalanan, Glossary, Settings, About.
- Added regression coverage for About route and author attribution.
- No canonical schema, storage, provider, or Secret Vault runtime change.

## What changed

### Web Interface Static Documentation Serving

- Single localhost server now serves `/docs/` reference pages and local assets.
- Static file surface is allowlisted and traversal-protected.
- Automated suite is **111/111 PASS**.


### Web Interface Hardening: Post/Redirect/Get

- Fixed successful capture refresh resubmission by changing `POST /capture` to return `303` and rendering the saved result through `GET /?saved=...`.
- Added regression coverage for PRG, repeated refresh, and saved-memory lookup.
- Expanded the canonical glossary with core HTTP/Web terms used by the interface and hardening work.
- Automated suite is **109/109 PASS**.
- No canonical schema, storage, provider, or Secret Vault runtime change.

### Web Interface Hardening Slice

- Hardened the localhost request boundary with strict form content-type validation, UTF-8 decoding, single-text-field enforcement, a 64 KiB body limit, and malformed-input handling.
- Added `GET /health` for local service/SQLite health verification.
- Added baseline browser security headers and a restrictive local Content Security Policy.
- Added six Web Interface regression tests; automated suite is **107/107 PASS**.
- Post-fix browser regression remains the acceptance gate before the hardening item is closed.
- No canonical schema, storage, provider, or Secret Vault runtime change.

### Web Interface Warung Padang Acceptance

- Recorded the Project Owner's manual browser test drive of the packaged dev.31 Local Web Interface as **PASS**.
- Accepted the initial Local Web Interface as a product-facing Milestone 5 input slice.
- Moved the next implementation gate to **Web Interface hardening**.
- No runtime, schema, storage, provider, or Secret Vault behavior changed.

### PERNAH Visual Identity System

- Formalized the shared visual identity contract and design tokens under `docs/assets/`.
- Applied the Continuity P brand language to Creation Chronicle, Glossary, and Local Web Interface surfaces.
- Standardized dark/light palette, typography direction, navigation, theme controls, responsive behavior, status/provenance language, and floating actions.
- Removed remote font dependencies from the Glossary.
- Preserved the existing Web Interface capture and canonical ingestion behavior.
- Added cross-surface visual identity regression coverage.
- No canonical schema or product runtime behavior changed.

### Visual Identity Foundation + Chronicle Theme System

- Established the **Symbol + Wordmark / Continuity P** direction for the PERNAH identity.
- Added symbol, lockup, monochrome, and identity guidance assets under `docs/assets/`.
- Applied the PERNAH palette and LEMON MILK + Open Sans typography direction to Creation Chronicle.
- Added light/dark theme toggle, responsive sidebar control, primary navigation, and floating back-to-top action.
- Added reduced-motion support and brand identity regression coverage.
- No canonical schema or product runtime behavior changed; feature state remains v0.2.0-dev.28.

### Creation Chronicle Integrity + Visual Refactor

- Established the formal Chronicle contract and preserved historical/source-of-truth boundaries.
- Reordered late milestones through v0.2.0-dev.28 into chronological order and consolidated the current handoff.
- Repaired duplicate section IDs and made the TOC derive from current Chronicle headings.
- Refactored the standalone visual shell into an editorial/timeline-style archive.
- Added Chronicle integrity regression coverage.
- No canonical schema or product runtime behavior changed.

### Data Classification & Privacy Boundary

- Added `docs/SECURITY.md` as the source of truth for Normal Data, Sensitive Data, and Secret Data classification.
- Defined canonical retention with no automatic pruning or expiry.
- Established that Secret Data must not be stored plaintext in Memory Core.
- Recorded Secret Vault as a future capability only; no vault runtime or cryptographic implementation was added.

### Documentation & artifact hygiene

- Retired the legacy root `Readme.md`; `README.md` remains canonical.
- Removed duplicated blocks from `docs/CHANGELOG.md` and corrected the manual-input API name.
- Synchronized the glossary count to 101 indexed terms.
- Clarified current runtime status and added `docs/TUTORIAL.md`.
- No canonical schema or runtime behavior changed.

### Manual input interface

- Added provider-neutral `pernah.manual_input.capture_text()` as the first explicit product-facing input boundary.
- Added a local CLI entry point via `python -m pernah.manual`.
- Reused existing normalization and ingestion semantics without schema or provider changes.
- Added regression coverage for API and CLI manual capture.

### Portable export/import hardening + disaster recovery

- Hardened portable JSON export with atomic filesystem promotion and automatic parent-directory creation.
- Added `Storage.import_json()` with canonical and relational validation before mutation.
- Added relational preflight to `import_canonical()` while preserving merge/dedup-oriented import semantics.
- Added a controlled disaster-recovery drill that reconstructs a deleted temporary live database from validated backup, plus corrupted-backup safety coverage.
- Added glossary term **Disaster Recovery** and updated the Chronicle handoff.

### Restore workflow

- Added atomic restore from validated `pernah-canonical-v1` backup to a target SQLite database.
- Restore stages and validates a temporary database before promotion, protecting an existing target from invalid or failed restores.
- Added round-trip equality checks and failure-safety regression coverage.

### Chronicle + glossary audit

- Reworked Chronicle sessions 23–24 for Indonesian historical language consistency without changing their historical claims.
- Added the restore milestone and refreshed the current handoff.
- Added glossary entries for Arsiparis, Restore, Recovery, Backup Validation, and Chronicle Editorial Consistency.


### Local backup + backup validation

- Added local canonical backup using `pernah-canonical-v1`.
- Added deterministic serialization and strict structural validation.
- Added isolated SQLite relational integrity validation without mutating source storage.
- Restore is now implemented as the next recovery layer.

### Glossary UTF-8 integrity fix

- Repaired double-encoded UTF-8 punctuation in `docs/Glosarium.html` without removing or rewriting glossary entries.
- Added a regression test rejecting C1 control characters and common UTF-8 mojibake markers.
- Added explicit CHECKPOINT encoding-integrity governance for future glossary updates.


### Collaborative AI working style / resource-aware governance

- Strengthened CHECKPOINT collaboration rules so the AI acts as a Co-Developer and discussion partner, not only a command executor.
- Added proactive feedback, constructive disagreement, option comparison, and best-fit recommendation behavior.
- Added cost/resource-aware guidance with free/local/offline/low-cost defaults when sufficient.
- Explicitly avoided storing personal financial circumstances as project state.

### Continuity Layer v1

- Added `PERNAH_BOOT.md` as the fast boot snapshot for new-chat continuation.
- Added `PERNAH_PROJECT_STATE.json` as a machine-readable boot snapshot.
- Added this release manifest to record release lineage and validation intent.
- Strengthened `PERNAH_CONTINUATION.md` so chat is treated as ephemeral workspace and
  artifact state as the continuity layer.
- Added explicit CHECKPOINT governance for artifact continuity and cross-chat recovery.
- Added glossary entries **Ephemeral**, **Continuity Layer**, **Boot Snapshot**, and **Release Manifest**.

## Current continuation point

- **Milestone:** Milestone 5 — Input Interfaces
- **Next gate:** Milestone 5 — Web Interface hardening
- **Security/privacy gate:** classification boundary defined; Secret Vault not implemented
- **AI/provider dependency:** none
- **Canonical schema change:** none

## Validation contract

- Canonical command: `python3 -m unittest discover -s tests -v`
- Expected suite: **107/107 PASS**
- Exact ZIP must be extracted and tested after packaging.
- No `__pycache__/`, `.pyc`, or `.pyo` files may be included in the delivered ZIP.
- The exact delivered artifact checksum must be recorded outside the ZIP at delivery time.

## Parent/lineage rule

`dev.32` records manual acceptance of `dev.31` and continues directly from `dev.31` as a visual/brand release over the v0.2.0-dev.28 feature state. The v0.2.0-dev.28 artifact remains the feature-state parent. The `dev.20` artifact remains part of the
release lineage for historical traceability. A new chat must treat the latest uploaded
artifact as the primary evidence and must not reconstruct project state from conversation
memory alone.

Historical parent artifact: `PERNAH-v0.2.0-dev.20.zip`.
