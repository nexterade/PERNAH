# PERNAH — Changelog

## 0.2.0-dev.66 — Retrieval-first orchestration

- Added `orchestrate_retrieval()` that runs deterministic canonical retrieval before optional answer generation.
- Provider receives only bounded canonical evidence; empty retrieval does not call the provider.
- Answer output is accepted only through evidence-ID validation; provider failures preserve deterministic evidence and expose no exception message.
- No provider SDK, network calls, schema migration, or canonical writes were added.
- Parent artifact: `PERNAH-v0.2.0-dev.65.zip`.


## 0.2.0-dev.65 — Deterministic Extraction Orchestration

- Added `orchestrate_extraction()` as a provider-neutral orchestration boundary that always prepares the existing deterministic `normalize()` draft first.
- Provider absence, malformed output, validation failures, and provider exceptions fall back without blocking capture; exception messages are not copied into diagnostics.
- Valid provider proposals remain advisory and never replace the deterministic write-ready draft. Low-confidence or ambiguous proposals are explicitly marked for review; no automatic canonical writes were added.
- Added five orchestration regression tests covering no provider, valid advisory proposals, review-required proposals, malformed responses, and provider failure.
- No SDK, network call, schema migration, UI integration, or real provider added; schema remains v4.
- Parent artifact: `PERNAH-v0.2.0-dev.64.zip`.


## 0.2.0-dev.64 — AI Contracts + Structured Proposal Validation

- Added provider-neutral AI request/result contracts and explicit `ProviderUnavailable`, `ProviderFailure`, and `InvalidProposal` error types in `pernah/ai_layer.py`.
- Added strict validation for untrusted structured extraction proposals, exact original-input provenance, bounded sizes, allowed intent/language/entity/relationship fields, transaction/event invariants, and confidence review routing.
- Added answer-candidate validation that rejects memory references outside the retrieved canonical evidence set and requires uncertainty notes when evidence is insufficient.
- Added an offline-safe unconfigured provider contract; no SDK, network calls, provider credentials, canonical writes, or schema changes.
- Added 12 regression tests for valid/invalid proposals, evidence grounding, and deterministic fallback semantics.
- Parent artifact: `PERNAH-v0.2.0-dev.63.zip`.


## 0.2.0-dev.63 — Attachment Acceptance + AI Layer Plan

- Recorded Project Owner manual acceptance of image attachment capture, preview, and Backup & Recovery on the packaged `dev.62` artifact; all checks were reported PASS.
- Added `docs/AI-LAYER-PLAN.md` with staged delivery slices, non-goals, privacy boundaries, and acceptance criteria for Milestone 6.
- First implementation target is provider-neutral contracts and structured-output validation using fakes only; no real provider, network call, SDK, schema migration, or AI runtime behavior is introduced in this release.
- Kept **PERNAH CROSSOVER CATBOX (Coming Soon, Maybe 🤔)** parked and unimplemented.
- Documentation/plan-only release: runtime and canonical schema v4 are unchanged.
- Parent artifact: `PERNAH-v0.2.0-dev.62.zip`.

## 0.2.0-dev.62 — Roadmap Parking Lot: PERNAH CROSSOVER CATBOX

- Archived **PERNAH CROSSOVER CATBOX (Coming Soon, Maybe 🤔)** in the backlog as a future, non-committed concept.
- Captured potential use cases for transaction evidence and personal-life memories, plus future review items for privacy/public URLs, provider-neutral metadata, credential handling, deletion, and backup portability.
- Explicitly recorded that Catbox is **not implemented**, does not change current local SQLite attachment storage, and is not the active next gate.
- Documentation-only release: no runtime, database schema, dependencies, or attachment behavior changed.
- Parent artifact: `PERNAH-v0.2.0-dev.61.zip`.

## 0.2.0-dev.61 — Canonical Image Attachments

- Added schema v4 `attachments` table with an explicit foreign-key link to the owning Memory and SQLite BLOB storage.
- Extended the Local Web Interface Memory form to accept up to four JPEG, PNG, GIF, or WebP images alongside a note; validates byte signatures and enforces 8 MiB per image / 12 MiB per request limits.
- Added local attachment viewing and result-page previews; attachment content is never written to request logs or sent to external services.
- Included attachment bytes in `pernah-canonical-v1` backup/export as validated Base64, and preserved them through validation, import, and atomic restore.
- Added v3→v4 database migration and compatibility upgrade for existing v3 canonical JSON backups.
- Added storage, backup/restore, migration, web upload, invalid-image, and attachment-serving regression tests.
- Parent artifact: `PERNAH-v0.2.0-dev.60.zip`.
- Automated suite: **170 passed, 1 skipped** (171 discovered). Exact packaged-artifact validation is required before delivery.

## 0.2.0-dev.60 — Atomic Ingestion + Continuity Repair

- Made `ingest_draft()` atomic with a SQLite savepoint; failures roll back all rows written by that draft, including when the caller catches the exception inside a `Storage` context.
- Added regression tests for invalid transaction drafts and simulated downstream failures.
- Synchronized boot and machine-state snapshots, current release manifest, and continuation gates with authoritative state.
- Updated Chronicle and Glossary to record the atomic-ingestion contract and this material engineering change.
- Parent artifact: `PERNAH-v0.2.0-dev.59.zip`.
- Source-tree automated suite: **163 passed, 1 skipped** (164 discovered); exact packaged-artifact validation remains mandatory.

## 0.2.0-dev.59 — Chronicle Sidebar Scroll-Sync / Scrollspy

- Added viewport-based Chronicle scroll synchronization so the sidebar active item follows the section currently reached in the viewport.
- Clicking a Chronicle index item immediately synchronizes the active state; the existing anchor smooth-scroll then lets scroll-sync reconfirm the target after navigation settles.
- Active Chronicle index items are automatically scrolled into view inside the sidebar when needed.
- Added Chronicle mobile backdrop + outside-pointer close behavior while preserving inside-sidebar taps, swipe-to-close, and Escape close.
- Added regression coverage for the scroll-sync and mobile outside-close contracts.
- No canonical schema, storage semantics, AI/provider runtime dependency, or Secret Vault behavior changed.

## 0.2.0-dev.58 — Mobile Sidebar + Embedded Glossary Runtime Fix

- Fixed embedded Glossary initialization: the reference script now safely skips the standalone theme-control DOM update when rendered inside the product shell, allowing the canonical 153-entry renderer to execute.
- Fixed the mobile outside-tap contract by explicitly binding `sidebarIndex` before the document-level pointer guard evaluates the event target.
- Added regression coverage for the embedded reference runtime guards.
- Automated suite: **160/160 PASS** (1 skipped).
- No canonical schema, storage semantics, AI/provider runtime dependency, or Secret Vault behavior changed.

## 0.2.0-dev.57 — Chronicle: Obrolan Santai

- Added Creation Chronicle section 42 documenting the project's informal conversation layer and recurring development jokes.
- Recorded the monetization running joke as **75% jokes, 25% bukan jokes**, without turning it into a product requirement or financial plan.
- No runtime, canonical schema, storage semantics, AI/provider dependency, or Secret Vault behavior changed.
- Documentation-only continuity update.

## 0.2.0-dev.56 — Hybrid Vocabulary + Glossary

- Expanded the canonical Glossary with 20 newly encountered vocabulary entries spanning language, product, UX, engineering, web, security, and CLI commands.
- Glossary now explicitly supports the Hybrid Vocabulary + Glossary direction: useful words, jargon, error messages, commands, abbreviations, and technical terms can all be documented with definitions and examples.
- Canonical dictionary size: **153 entries**.

## 0.2.0-dev.56 — Web UX Recovery Fixes

- Fixed the live Settings Content Security Policy to allow same-origin `fetch('/restore')`, resolving the browser-side `Failed to fetch` failure during restore.
- Hardened Glossary theme persistence with safe localStorage access so storage restrictions cannot prevent the dictionary from rendering.
- Added a document-level pointer/tap outside guard for the mobile Glossary index; tapping outside the index now closes it reliably.
- Added regression coverage for the restore CSP contract and the mobile outside-tap behavior.
- Automated suite: **158/158 PASS** (1 skipped).
- No canonical schema, storage semantics, AI/provider runtime dependency, or Secret Vault runtime changed.

## 0.2.0-dev.54 — CLI URL Auto-Copy

- Added best-effort automatic clipboard copy of the local Web Interface URL when `python -m pernah.web` starts the server.
- Supports common local clipboard utilities without adding a third-party runtime dependency: Termux, Wayland, X11, macOS, and Windows/WSL.
- Clipboard failure is non-fatal: the server still starts and the URL remains printed for manual copy.
- Added regression coverage for first-available clipboard selection and graceful no-clipboard environments.
- Automated suite: **158/158 PASS** (1 skipped).
- Human acceptance remains: run the exact artifact on the target terminal and confirm the printed URL is copied automatically.
- No canonical schema, storage semantics, AI/provider runtime dependency, or Secret Vault runtime changed.

## 0.2.0-dev.53 — Local Web Backup & Recovery UI

- Added Settings → Backup & Recovery to the local Web Interface.
- Added `GET /backup` to download the current canonical state as `pernah-canonical-v1` JSON.
- Added `POST /restore` for validated canonical recovery with an explicit `X-PERNAH-Confirm: restore` boundary.
- Restore validates the uploaded canonical backup before `Storage.restore()` atomically replaces the target database; invalid payloads leave the existing state unchanged.
- Added automated coverage for backup download, explicit restore confirmation, successful replacement, and invalid-backup non-mutation.
- Added browser-facing recovery copy and post-restore confirmation state in Settings.
- Automated suite: **155/155 PASS** (1 skipped).
- Human Web Backup & Recovery browser test-drive remains pending on the exact packaged artifact.
- No canonical schema, storage semantics, AI/provider runtime dependency, or Secret Vault runtime changed.

## 0.2.0-dev.51 — Recovery Gate Automation + Exact Artifact Hygiene

- Added automated Web Interface recovery coverage: capture through the local HTTP interface, create and validate a canonical backup, remove the live database, restore it atomically, restart the server, and verify the saved-memory route remains readable and refresh-safe.
- Hardened exact-artifact hygiene so `.pytest_cache/` is explicitly rejected alongside Python bytecode/cache artifacts.
- Release preflight and release-integrity checks now enforce this cache hygiene contract.
- Automated suite: **149/149 PASS** (1 skipped).
- Exact artifact still required the Project Owner's human restore/recovery browser test-drive before the product gate was considered complete.
- No canonical schema, storage semantics, AI/provider runtime dependency, or Secret Vault runtime changed.

## 0.2.0-dev.50 — Test Discovery + Language Boundary Hardening

- Converted Memory Engine regression tests to the canonical stdlib `unittest` discovery contract so all release tests are actually included in the official runner.
- Added a release-integrity guard preventing top-level `test_*` functions from silently bypassing unittest discovery in future changes.
- Hardened mixed Sundanese/Indonesian language detection for tied lexical scores when distinctive Sundanese markers are present.
- Updated the deterministic Sundanese retrieval regression expectation for the richer query payload.
- Parent artifact: `PERNAH-v0.2.0-dev.49.zip`.
- Automated suite: **148/148 PASS** (1 skipped).
- No canonical schema, storage semantics, AI/provider runtime dependency, or Secret Vault runtime changed.

## 0.2.0-dev.49 — Knowledge-Surface Impact Gate

- Added lightweight `KNOWLEDGE-SURFACE IMPACT CHECK` to CHECKPOINT with `BOTH / GLOSSARY / CHRONICLE / NONE` classification.
- Promoted Glossary + Creation Chronicle from presence/integrity-only checks into explicit knowledge-surface consistency workflow.
- Added 12 governance/communication terms to the canonical Glossary: Artifact Compliance Gate, Behavioral Policy, Concise, Human Touch, Integrity Contract, Invariant, Knowledge-Surface Impact Check, Policy Propagation, Prompt Translation, Raw Idea, Release Preflight, and Trigger Policy.
- Recorded the knowledge-surface governance change in Creation Chronicle section 34.
- Added regression coverage for knowledge-surface policy, terminology synchronization, and current Chronicle evidence.
- Parent artifact: `PERNAH-v0.2.0-dev.48.zip`.
- Automated suite target: **144/144 PASS**.

## 0.2.0-dev.48 — Human Touch Behavioral Policy

- Promoted FUN-FACT / HUMAN TOUCH from an optional permission into a soft behavioral policy for normal collaboration: relevant humor, analogy, fun-fact, or human comments may appear naturally without being forced into every response.
- Added explicit context triggers and focus/safety exceptions for debugging, milestones, security/privacy, critical errors, data loss/corruption, and safety-sensitive work.
- Propagated the policy into `PERNAH_BOOT.md` and `PERNAH_CONTINUATION.md`.
- Added regression coverage to verify policy definition and propagation without requiring fun-facts in every response.
- Parent artifact: `PERNAH-v0.2.0-dev.47-fixed.zip`.
- Automated suite target: **140/140 PASS**.

## 0.2.0-dev.47 — Release Integrity Gate + Prompt Translation

- Added an executable Artifact Compliance Gate covering version/lineage, source-of-truth consistency, required structure, flat-root packaging, artifact hygiene, documentation consistency, provenance, and exact-artifact validation.
- Added explicit documentation-consistency coverage for the canonical Creation Chronicle and Glossary surfaces; their historical/terminology contracts are validated without incorrectly requiring current release-version strings in historical documents.
- Added the `RAW IDEA → REQUIREMENT → PROMPT TRANSLATION` workflow to CHECKPOINT so unclear user ideas can be formalized before execution without inventing intent.
- Added release-integrity regression coverage for the new gate.
- Parent artifact: `PERNAH-v0.2.0-dev.46.zip`.
- Automated suite target: **TBD until exact artifact validation completes**.

## 0.2.0-dev.46 — Browser Visual Identity & Chronicle Index Fix

- **Chronicle index:** fixed the content-only `/chronicle` reader so its TOC generation runs again; the embedded fragment does not contain the standalone page's theme button, so the initialization code now guards that optional control.
- **Shell logo:** fixed the product shell CSP to allow same-origin SVG images, so the canonical `docs/assets/pernah-symbol.svg` can actually render.
- **Favicon:** kept `/favicon.svg` on the canonical symbol and added a shortcut-icon declaration to the shared shell for broader browser compatibility.
- **Regression coverage:** added checks for the logo CSP, favicon delivery, and embedded reference initialization.
- **Automated suite target:** **131/131 PASS**.
- **Canonical schema/storage:** unchanged.

## 0.2.0-dev.45 — Product Shell Reference Content Integration

- **Reference surfaces:** `/chronicle` and `/glossary` now render only the canonical document content inside the product shell; the standalone HTML page is no longer nested as an iframe.
- **Navigation:** the product shell remains the single primary navigation surface; embedded reference pages no longer duplicate their standalone navigation.
- **Interaction:** embedded Chronicle / Glossary keep their search, index, print, and sidebar behavior; a dedicated index toggle is provided for the embedded reference surface and the existing swipe behavior remains available on mobile.
- **Standalone:** `/docs/Creation-Chronicle.html` and `/docs/Glosarium.html` remain intact and are still reachable from the embedded surfaces.
- **Automated suite:** **129/129 PASS**.
- **Canonical schema/storage:** unchanged.

## 0.2.0-dev.44 — Browser Consistency & Theme Unification

- Fixed a real standalone Creation Chronicle JavaScript syntax regression that prevented the desktop index from being generated and the mobile sidebar button from opening.
- Hardened Chronicle / Glossary sidebar controls with explicit toggle state, accessible sidebar targets, swipe-open/close behavior, and Escape-to-close on mobile.
- Unified theme persistence across Product Home, Web Interface, Chronicle, and Glossary under the shared `pernah-theme` key. The default is **System**, following the device/browser `prefers-color-scheme`; explicit Light/Dark choices cycle back to System.
- Added cross-page theme synchronization for same-origin tabs through the browser storage event and system-theme change handling.
- Fixed the static-server brand path by adding a root `favicon.svg` and giving the canonical SVG explicit brand color instead of relying on `currentColor` through `<img>`.
- Added standalone favicon declarations and static Home theme support.
- Added regression coverage for favicon delivery, standalone theme contracts, shared shell theme defaults, and live Web Interface theme behavior.
- Automated suite: **127/127 PASS**.
- No canonical schema, storage semantics, AI/provider dependency, or OpenWrt deployment runtime changed.


- Fixed standalone Chronicle and Glossary navigation so the PERNAH brand returns to product Home instead of raw `README.md`.
- Added `index.html` as a static Home fallback for `python -m http.server` smoke tests; the unified Web Interface still owns `/` as the live product Home.
- Removed the desktop sidebar `X` affordance from standalone reference pages; desktop uses the existing toggle and mobile supports swipe gestures for opening/closing the index drawer.
- Added regression coverage for Home fallback, favicon content, standalone Home links, and sidebar gesture contracts.
- Preserved the canonical Visual Identity System and existing Chronicle / Glossary content.
- No canonical schema, storage semantics, AI/provider dependency, or OpenWrt deployment runtime changed.
- Automated suite target: **122/122 PASS**.

## 0.2.0-dev.42 — Browser Regression Hardening

- Recorded the first packaged-artifact browser regression findings from the `dev.41` manual test drive: Chronicle and Glossary embedding now verified **PASS** on the device/browser path.
- Fixed the release packaging layout so `dev.42.zip` is **flat-root**: project files are placed directly at archive root instead of inside an enclosing `PERNAH-v0.2.0-dev.42/` directory.
- Restored CLI HTTP access logging by keeping the standard `BaseHTTPRequestHandler` request log; starting the Web Interface now visibly records requests/responses in the terminal.
- Replaced the shell's duplicated inline logo geometry with the canonical `docs/assets/pernah-symbol.svg` asset and added a real `/favicon.svg` route, eliminating the browser globe fallback.
- Preserved the existing Visual Identity System as the source of truth; the shell logo was an implementation drift, not a new brand direction.
- No canonical schema, storage semantics, AI/provider dependency, or OpenWrt deployment runtime changed.
- Automated suite target: **120/120 PASS**.

## 0.2.0-dev.41 — Shared Reader Security + About Philosophy

- Fixed the `/chronicle` and `/glossary` shell reader surfaces: the canonical documents were blocked by the Web Interface security policy because the shell used an iframe while the global frame policy was `DENY`.
- Kept the security boundary strict: product/application responses remain `X-Frame-Options: DENY`, while same-origin static reference documents are explicitly `SAMEORIGIN` with `frame-ancestors 'self'` and the parent shell permits only same-origin frames.
- Updated the About philosophy surface with **“Karena yang berharga layak untuk dijaga 🫰”** while retaining the artifact-continuity principle as supporting copy.
- Added regression coverage for the reader security contract and About philosophy copy.
- No canonical schema, storage semantics, AI/provider dependency, or OpenWrt deployment runtime changed.
- Automated suite target: **117/117 PASS**.

## 0.2.0-dev.40 — Shared Product Shell Integration

- Integrated **Chronicle / Perjalanan** and **Glossary** into the shared product shell instead of redirecting the product routes directly to standalone documentation pages.
- Rendered the canonical Creation Chronicle and Glossary documents inside shell reader surfaces while preserving their standalone `/docs/` presentation and content contract.
- Moved the `/about` route onto the same shared shell so Home, Memory, Chronicle, Glossary, Settings, and About now use one product navigation/theme surface.
- Added regression coverage for shared-shell route rendering and embedded canonical reference targets.
- No canonical schema, storage semantics, AI/provider dependency, or OpenWrt deployment runtime changed.
- Automated suite: **116/116 PASS**.

## 0.2.0-dev.39 — Domain + OpenWrt Deployment Concept

- Documented a low-cost personal deployment concept using domain `pernah.my.id` with an OpenWrt-hosted PERNAH runtime.
- Recorded the current AmLogic HG680P / OpenWrt 24.10.4 environment as a candidate runtime, including the observed resource snapshot (~1.76 GB RAM, ~29.12 GB data mount, ~3% CPU, ~39°C).
- Recorded Cloudflare Tunnel as a candidate public-access layer and GitHub Pages as an optional static landing/docs surface.
- Explicitly marked the concept as **CONCEPT / NOT IMPLEMENTED**: no tunnel, authentication, public hostname, remote exposure, or OpenWrt deployment automation is included.
- Canonical SQLite storage and local-first architecture remain unchanged.
- Documentation-only release; automated suite remains **116/116 PASS**.

## 0.2.0-dev.38 — Web App Shell & Navigation

- Added the first product-facing application shell with Home, Memory, Chronicle, Glossary, Settings, and About navigation.
- Reframed `/` as the product Home instead of exposing `README.md` as the default user-facing index.
- Added `/memory` and `/settings` product routes; `/chronicle` and `/glossary` now have stable product routes that enter the existing reference surfaces.
- Preserved POST/Redirect/GET capture flow and returned saved-memory results inside the product shell.
- Added regression coverage for the shell routes, navigation, Home identity, and capture-result continuity.
- Automated suite: **116/116 PASS**.

## 0.2.0-dev.37 — About / Author Profile

- Expanded the product-facing `/about` surface from a minimal attribution page into an informative author profile for **@nexterade**.
- Added repository, email, and website links.
- Added transparent Skill Statistics as project-relevant focus areas rather than fabricated proficiency percentages.
- Added interests, builder profile, and the project philosophy **“Chat is ephemeral. Artifact is continuous.”**
- Preserved the local/offline-friendly runtime boundary; no canonical schema, storage semantics, AI/provider dependency, or Secret Vault runtime changed.
- Added regression coverage for the About profile content and links.
- Automated suite: **113/113 PASS**.

## 0.2.0-dev.36 — About / Author Surface

- Added a product-facing `/about` page to the localhost Web Interface.
- Identified the project author as **@nexterade**.
- Added a footer link from the current Web Interface to `/about`.
- This establishes **About** as a first-class item for the planned product navigation shell alongside Home, Memory, Chronicle, Glossary, and Settings.
- Added regression coverage for the About page and author attribution.
- No canonical schema, storage semantics, AI/provider dependency, or Secret Vault runtime changed.

## 0.2.0-dev.35 — Web Interface Static Documentation Serving

- Extended the same localhost Web Interface server to serve the project reference surfaces under `/docs/`, including `Glosarium.html`, `Creation-Chronicle.html`, and local design assets.
- Added `/docs/` redirect to the Glossary and `/README.md` serving so documentation navigation remains usable from the same local origin.
- Added a strict static-file allowlist (`.html`, `.css`, `.svg`, `.md`) with path-traversal protection and dedicated local CSP rules for documentation assets.
- Added regression coverage for documentation serving, asset MIME handling, security headers, and traversal rejection.
- Automated suite: **111/111 PASS**.
- No canonical schema, storage semantics, AI/provider dependency, or Secret Vault runtime changed.

## 0.2.0-dev.34 — Web Interface Hardening: Post/Redirect/Get

- Fixed the browser form-resubmission problem after successful Web Interface capture by adopting **Post/Redirect/Get (PRG)**.
- Successful `POST /capture` now persists once and returns `303` to a result `GET`; refreshing the result page no longer resubmits the capture form.
- Added regression coverage for redirect behavior, result retrieval, repeated refresh, and saved-memory lookup.
- Expanded the glossary with HTTP/Web fundamentals: HTTP, GET, POST, Request, Response, Redirect, Post/Redirect/Get (PRG), Endpoint, and Idempotency.
- Automated suite: **109/109 PASS**.
- No canonical schema, storage semantics, AI/provider dependency, or Secret Vault runtime changed.

## 0.2.0-dev.33 — Web Interface Hardening Slice

- Hardened the localhost Web Interface request boundary with strict form content-type validation, UTF-8 decoding, single-text-field enforcement, body-size limits, and malformed-input handling.
- Added `GET /health` as a lightweight local health check for the running interface and its SQLite path.
- Added baseline browser-facing security headers: no-store caching, MIME sniffing protection, frame denial, referrer suppression, and a restrictive local Content Security Policy.
- Added regression coverage for health status, security headers, wrong content type, duplicate fields, invalid UTF-8, and oversized bodies.
- Preserved the existing `capture_text()` boundary, canonical SQLite storage, localhost-only binding, and no-cloud/no-provider architecture.
- Automated suite: **107/107 PASS**.
- The next gate remains Web Interface hardening until the post-hardening **Warung Padang** regression is accepted.

## 0.2.0-dev.32 — Web Interface Warung Padang Acceptance

- Recorded the Project Owner's manual **Warung Padang** test drive of the Local Web Interface as **PASS**.
- Acceptance covered the real browser flow on the packaged `dev.31` artifact; the interface is accepted as usable for the current Milestone 5 slice.
- Promoted the Local Web Interface from **test drive gate** to **accepted initial product-facing input slice**.
- The next implementation gate is Web Interface hardening; WhatsApp and existing-data import remain separate future input slices.
- No canonical schema, storage semantics, AI/provider dependency, or Secret Vault runtime changed.
- Automated suite remains **102/102 PASS**; this release adds a manual acceptance record rather than changing runtime code.

## 0.2.0-dev.31 — PERNAH Visual Identity System

- Formalized the shared visual identity in `docs/assets/DESIGN-SYSTEM.md` and `pernah-design-tokens.css`.
- Extended the Symbol + Wordmark / Continuity P identity to the existing Glossary and Local Web Interface surfaces, not only Creation Chronicle.
- Standardized dark/light palette, LEMON MILK + Open Sans typography direction, navigation, theme controls, responsive interaction, provenance/status language, and floating action treatment.
- Removed the Glossary's external Google Fonts / CDN dependency to preserve local/offline-friendly operation.
- Refreshed `pernah.web` visually without changing its localhost-only capture pipeline or canonical storage behavior.
- Added cross-surface visual identity regression coverage.
- No canonical schema, storage, AI/provider, or Secret Vault behavior changed.

## 0.2.0-dev.30 — Visual Identity Foundation + Chronicle Theme System

- Established the **Symbol + Wordmark / Continuity P** visual identity direction for PERNAH.
- Added `docs/assets/pernah-symbol.svg`, `pernah-lockup.svg`, `pernah-monochrome.svg`, and `BRAND.md`.
- Refactored Creation Chronicle typography declarations toward **LEMON MILK + Open Sans** and the PERNAH dark/light palette.
- Added light/dark theme toggle with local persistence, responsive sidebar toggle, primary navigation, and floating back-to-top action.
- Added reduced-motion support and `tests/test_brand_identity.py`.
- Kept the feature state at v0.2.0-dev.28; no canonical schema, storage, Web Interface runtime, AI/provider, or Secret Vault behavior changed.
- Automated suite: **96/96 PASS** after exact artifact validation.

## 0.2.0-dev.29 — Creation Chronicle Integrity + Visual Refactor

- Refactored `docs/Creation-Chronicle.html` as a documentation-only release.
- Established the Chronicle contract: primary record, source discipline, chronology, current-state labeling, separation from CHANGELOG, and historical preservation.
- Reordered the late milestone history through dev.28 so documentation hygiene, data classification, and Web Interface appear in chronological order.
- Consolidated current handoff information into one final current-state section.
- Repaired duplicate section IDs and replaced the hardcoded TOC with a heading-driven dynamic index.
- Refreshed the standalone visual shell into an editorial/timeline-style archive while retaining search, print, mobile, and offline-friendly behavior.
- Added Chronicle integrity regression coverage.
- No canonical schema, storage, runtime, AI/provider, or Secret Vault behavior changed.

## 0.2.0-dev.28 — Local Web Interface

- Added `pernah.web` as a minimal localhost web input boundary using Python standard-library HTTP server.
- Reused `capture_text()` and the existing normalization/ingestion pipeline; no duplicate ingestion path.
- Recorded web provenance as `source_type="web"`.
- Added integration tests for form rendering, successful persistence, provenance, and blank-input rejection.
- Kept the server localhost-only by default; no authentication, cloud transport, remote exposure, or Secret Vault runtime was added.
- Added the glossary term **Web Interface** and updated the Creation Chronicle handoff.

- Added minimal localhost web input boundary via `python3 -m pernah.web`.
- Reused `capture_text()` and existing normalization/ingestion pipeline; no duplicate ingestion path.
- Recorded web provenance as `source_type="web"`.
- Added web integration tests for form rendering, persistence, provenance, and blank input.
- Kept server localhost-only by default; no auth, cloud, remote binding, or Secret Vault runtime.

## 0.2.0-dev.27 — Data Classification & Privacy Boundary

- Added `docs/SECURITY.md` as the source of truth for data classification and privacy boundaries.
- Defined Normal Data, Sensitive Data, and Secret Data classes.
- Defined the hard canonical-retention rule: maintenance, retrieval, indexing, backup, and optimization must not automatically prune or expire canonical records.
- Established that Secret Data must not be stored plaintext as Memory Core canonical data.
- Recorded Secret Vault as a separate future capability with encryption, key derivation, integrity/authentication, lock/unlock, and secure recovery requirements; no vault runtime was implemented.
- Added regression coverage for the new governance boundary.
- No canonical schema, storage, or AI/provider behavior changed.

## 0.2.0-dev.26 — Documentation & Artifact Hygiene

- Retired the legacy root `Readme.md` from the active release lineage; `README.md` remains the canonical project overview.
- Removed duplicated historical blocks from `docs/CHANGELOG.md` without rewriting the underlying release history.
- Corrected the manual-input API reference to `pernah.manual_input.capture_text()`.
- Synchronized stale glossary-count references from 99 to the actual **101 unique indexed terms**.
- Updated roadmap/current-state wording so the implemented manual CLI is not described as having no runtime at all; the remaining product-facing runtime gate is the Web Interface.
- Added a minimal `docs/TUTORIAL.md` usage guide for the currently implemented manual input path.
- Added documentation/artifact-hygiene regression coverage; no canonical schema, storage, or AI/provider behavior changed.

## 0.2.0-dev.25 — Manual Input Interface

- Added `pernah.manual_input.capture_text()` as an explicit provider-neutral manual input boundary.
- Added `python -m pernah.manual` with one-shot `--text` and interactive fallback for local SQLite capture.
- Preserved original input and existing normalization/ingestion semantics; no schema migration or AI/provider dependency.
- Added manual-input regression coverage.

## 0.2.0-dev.21 — Glossary UTF-8 integrity fix

- Fixed double-encoded UTF-8 punctuation in `docs/Glosarium.html` that rendered as mojibake such as `â...`.
- Root cause: glossary content contained UTF-8 bytes that had been decoded/re-encoded through an incompatible single-byte charset, producing valid-but-corrupted UTF-8 text. The HTML already declared UTF-8, so changing the browser/meta charset would not fix the stored data.
- Added a glossary regression test for UTF-8 decoding, C1 control characters, common mojibake markers, and replacement characters.
- Added an explicit glossary encoding-integrity rule to CHECKPOINT.
- No canonical schema, runtime, or provider dependency change.
- Canonical test suite: **48/48 PASS**.

## 0.2.0-dev.20 — Collaborative AI working style / resource-aware governance

- Updated CHECKPOINT with a stronger Co-Developer / discussion-partner character: proactive feedback, constructive disagreement, option comparison, and best-fit recommendations.
- Added resource-aware guidance for cost, usage limits, hardware, bandwidth, time, and complexity; free/local/offline/low-cost options are preferred when they satisfy the project requirements.
- Explicitly prohibited using or storing personal financial circumstances as hidden project rules.
- Preserved the rule that artifact evidence determines the next gate; unnecessary confirmation questions should not interrupt continuation.
- No schema or runtime behavior change.

## 0.2.0-dev.19 — Continuity Layer v1

- Added `PERNAH_BOOT.md` as the fast boot snapshot for cross-chat continuation.
- Added `PERNAH_PROJECT_STATE.json` as a machine-readable derived snapshot.
- Added `docs/RELEASE-MANIFEST.md` for release lineage and validation intent.
- Formalized **CHAT IS EPHEMERAL. ARTIFACT IS CONTINUOUS.** in the continuation workflow.
- Added regression coverage for continuity snapshot consistency.
- Added glossary entries **Ephemeral**, **Continuity Layer**, **Boot Snapshot**, and **Release Manifest**.
- No canonical schema change and no AI/provider dependency introduced.
- Canonical test command: `python3 -m unittest discover -s tests -v` — **45/45 PASS**.

## 0.2.0-dev.18 — Semantic concept vocabulary + ranking boundaries

- Expanded the deterministic local concept vocabulary across purchase, food, conversation, call, meeting, collaboration, device, passport, commitment, and decision concepts.
- Added a concept-relevance boundary so recognized semantic concepts are required to overlap before lexical ranking can produce a result, reducing false positives caused by shared generic tokens.
- Added regression coverage for concept normalization, phone synonyms, conversation ranking, and unrelated-person false positives.
- Promoted Creation Chronicle + Glosarium to mandatory continuation context in the top-level CHECKPOINT handoff order.
- Updated current-state/continuation documentation and glossary terminology for the semantic retrieval layer.
- Canonical test command: `python -m unittest discover -s tests -v` — **40/40 PASS**.
- No canonical schema change and no AI/provider dependency introduced.


## 0.2.0-dev.24 — Portable Export/Import Hardening + Disaster Recovery

- Hardened `Storage.export_json()` with atomic temporary-file promotion and automatic parent-directory creation.
- Added `Storage.import_json()` for validated file-based canonical import.
- Added relational preflight to `import_canonical()` so malformed references are rejected before target mutation.
- Preserved merge/dedup-oriented import semantics; full replacement remains `Storage.restore()`.
- Added a controlled disaster-recovery drill covering deletion of a temporary live database and reconstruction from validated backup, plus corrupted-backup failure safety.
- Added glossary term **Disaster Recovery**.
- Updated Creation Chronicle with the completed Milestone 4 handoff.
- Automated suite: **72/72 PASS**.



## 0.2.0-dev.23 — Restore Workflow + Chronicle Audit + Glossary Update

- Added `Storage.restore()` for validated local canonical backups.
- Restore stages the database in a temporary SQLite file, verifies canonical round-trip equality, and atomically promotes the staged file with `os.replace()`.
- Invalid backups, broken relationships, failed staging, and backup/target path collisions are rejected without mutating an existing target database.
- Added six restore regression tests; automated suite is now **66/66 PASS**.
- Audited Creation Chronicle sessions 23–24 for language drift, preserving historical meaning while restoring Indonesian narrative consistency.
- Added a dedicated restore milestone and refreshed the current handoff in the Chronicle.
- Added glossary terms **Arsiparis**, **Restore**, **Recovery**, **Backup Validation**, and **Chronicle Editorial Consistency**.
- No canonical schema migration and no AI/provider dependency introduced.


## 0.2.0-dev.22 — Local Backup + Backup Validation

- Added `Storage.backup()` as a local preservation workflow over the existing `pernah-canonical-v1` JSON format.
- Made canonical JSON export ordering deterministic by table column order.
- Added strict canonical payload validation for format, schema version, table set, and exact row structure.
- Added isolated SQLite relational validation with foreign-key enforcement so broken references are rejected without mutating the source database.
- Added backup regression coverage for empty/full databases, deterministic output, malformed JSON, wrong format/schema, missing tables, extra row fields, broken foreign keys, and import round-trip compatibility.
- Updated README, architecture, state, backlog, release manifest, boot snapshots, and Creation Chronicle.
- No canonical schema change and no AI/provider dependency.
- Automated suite: **60/60 PASS**.

## 0.2.0-dev.17 — Rebuildable semantic retrieval

- Added a deterministic, rebuildable TF-IDF derived index over canonical memory content.
- Added a small local synonym/concept normalization layer without introducing an AI/provider dependency.
- Added semantic retrieval fallback behind canonical purchase retrieval so deterministic canonical hits remain authoritative.
- Added generic question routing to the semantic retrieval path for unsupported query intents.
- Added regression coverage for synonym matching, deterministic rebuilds, and canonical immutability; suite is **37/37 PASS**.


## 0.2.0-dev.16 — Richer deterministic entity relationships

- Added deterministic relationship/event patterns for conversation, call, and collaboration alongside the existing meeting path.
- Extended supported person extraction prefixes while preserving the canonical `event_entities` participant contract.
- Added deterministic event-type filtering to entity-scoped retrieval.
- Added regression coverage for richer relationship persistence, retrieval, and temporal filtering.
- No canonical schema change and no AI/provider dependency introduced.
- Canonical test command: `python -m unittest discover -s tests -v` — **34/34 PASS**.

## 0.2.0-dev.15 — Continuation rule prominence

- Promoted the mandatory new-chat ZIP continuation order to a **top-level, uppercase/bold rule** at the beginning of `docs/CHECKPOINT.md`.
- Kept the operational sequence explicit: CHECKPOINT → README → STATE → BACKLOG → CHANGELOG → source + tests → relevant Creation Chronicle / Glosarium → PLAN → IMPLEMENT → TEST → DOCUMENT SYNC → PACKAGE → TEST EXACT ARTIFACT → DELIVER ACCESSIBLE ARTIFACT.
- Clarified that this is a mandatory governance rule, not an optional checklist, and that the latest ZIP artifact is the primary evidence for continuation.
- Documentation/governance change only; no canonical schema or runtime behavior change.

## 0.2.0-dev.14 — Continuation context handshake

- Added an explicit mandatory document/context reading order to `docs/CHECKPOINT.md` for new-chat continuation from an uploaded ZIP.
- Locked the handoff sequence as CHECKPOINT → README → STATE → BACKLOG → CHANGELOG → source + tests → relevant Creation Chronicle / Glosarium → PLAN → IMPLEMENT → TEST → DOCUMENT SYNC → PACKAGE → TEST EXACT ARTIFACT → DELIVER ACCESSIBLE ARTIFACT.
- Clarified that "read the whole docs" means reading the available documentation contents under `docs/`, not merely filenames, metadata, or summaries.
- Added an anti-claim rule: AI must not claim to have read or understood the full current state before the relevant artifact/context sweep is actually completed.
- Clarified that the latest uploaded artifact is the primary evidence for continuation; prior chat memory, summaries, or handoff notes cannot replace reading the latest artifact.
- Documentation/governance change only; no canonical schema or runtime behavior change.

## 0.2.0-dev.13 — Deterministic temporal query expansion

- Expanded natural-language temporal query extraction beyond yesterday/today.
- Added numeric day offsets (`3 hari lalu` / `3 days ago`) and week/month windows for supported Indonesian/English forms.
- Reused the same inclusive UTC ISO 8601 window contract for purchase and entity-relationship retrieval.
- Expanded the relationship query classifier to support English meeting queries such as `Did I meet Rahayu last week?`.
- Added regression coverage; canonical suite is **30/30 PASS**.
- No canonical schema change and no AI provider dependency introduced.

## 0.2.0-dev.12 — PERNAH CHECKPOINT adaptation

- Replaced the project checkpoint with the uploaded starter governance baseline.
- Adapted `CHECKPOINT.md` Section 6 specifically for PERNAH without moving volatile
  implementation state or release history into the governance template.
- Recorded PERNAH-specific rules for canonical memory, provider independence,
  local/offline core, multilingual understanding, storage baseline, documentation
  sources of truth, and interface boundaries.
- Removed generated Python cache artifacts from the release package.
- Canonical artifact version: `0.2.0-dev.12`.

## 0.2.0-dev.10 — Deterministic retrieval + relationship gate

- Restored the executable `pernah/` package as the implementation layer for the documented v0.2 foundation.
- Added canonical SQLite storage at schema version 3 with source, memory, entity, relationship, event, commitment, decision, transaction, and event-entity records.
- Added exact memory search over canonical interaction content.
- Expanded supported temporal query extraction with deterministic yesterday/today windows.
- Expanded deterministic relationship extraction for meeting/participant events.
- Added entity find-or-create deduplication and duplicate event-entity protection.
- Added regression tests for the next implementation gate.
- Canonical test command: `python -m unittest discover -s tests -v` — **23/23 PASS**.
- AI provider integration remains deferred.

## 0.2.0-dev.9 — Governance merge + glossary integrity sync

- Merged the upgraded CHECKPOINT governance baseline into the PERNAH project checkpoint without carrying over cross-project branding or implementation assumptions.
- Added context handshake, validation/release contract, change-impact classification, evidence/claim integrity, reproducibility, security baseline, documentation sync matrix, artifact traceability, and project adaptation guidance.
- Preserved the PERNAH-specific glossary invariants and strengthened the Generated UI Duplication Guard for the Exact Search / Deterministic Ranking regression.
- Synchronized the user-maintained networking/infrastructure glossary entries and retained the renderer-fix terminology as normal glossary data entries.
- Canonical glossary count: 86 unique terms.

## 0.2.0-dev.8 — Glossary renderer duplication guard

- Fixed the glossary renderer regression pattern where global/static text such as `Exact Search` and `Deterministic Ranking` could be injected into every generated glossary entry.
- Kept those terms as normal glossary terminology instead of renderer-level repeated content.
- Merged the user-maintained glossary additions for networking/infrastructure terminology while preserving existing PERNAH entries and the approved dictionary presentation layer.
- Added the **Generated UI Duplication Guard** to `docs/CHECKPOINT.md` with source-level and generated-output regression requirements.
- Added a glossary integrity smoke test covering entry uniqueness and renderer injection guards.

## 0.2.0-dev.7.1 — Chronicle validation fix

- Fixed the malformed JavaScript regular expression in `docs/Creation-Chronicle.html` discovered while applying the new documentation integrity validation.
- This is a correctness fix required by the newly merged Chronicle content-integrity guardrail.

## 0.2.0-dev.7 — Documentation integrity guardrails

- Merged the approved glossary entry-integrity rules into `docs/CHECKPOINT.md`.
- Added an explicit read → identify → duplicate-check → update → preserve → validate workflow for glossary entry changes.
- Added UI invariants and regression guards to prevent content-only glossary updates from removing approved typography, theme, search, index/filter, responsive, print, or universal-dictionary behavior.
- Added Creation Chronicle content-integrity rules covering chronological preservation, evidence discipline, and presentation-layer preservation during content-only updates.

## 0.2.0-dev.6 — Glossary regression fix

- Restored the v0.2.0-dev.4 universal glossary data and typography/theme shell that regressed in v0.2.0-dev.5.
- Restored the universal knowledge entries, including the broader temporal-query terminology.
- Added `Creation Chronicle` as the new dev.5 terminology entry without breaking the glossary script.
- Fixed the malformed JavaScript string that caused the glossary to render **0 istilah tampil / 0 istilah terdaftar**.
- Restored the documented two-font typography (LEMON MILK + Open Sans) and Night/Day theme toggle.

## 0.2.0-dev.5 — Creation Chronicle HTML

- Added `docs/Creation-Chronicle.html` as the official standalone HTML presentation.
- Updated CHECKPOINT rule 3.27 from Markdown presentation to HTML.
- Added `Creation Chronicle` to the glossary.

## Unreleased — Foundation

### Added

- Product name locked as **PERNAH**.
- Project identity: **Personal Memory & Life Context System**.
- Canonical Data Model v0.1 blueprint.
- Architecture blueprint covering canonical/derived data, temporal history, provenance, confidence, and rebuildable indexes.
- Initial product backlog.
- Current-state documentation.

### Design decisions

- Local-first is the core storage direction.
- Online backup is optional and encrypted.
- AI is not the canonical source of truth.
- Historical states are preserved instead of destructively overwritten.
- Derived search/AI artifacts must be rebuildable.


## 2026-10-05 — Canonical Storage v0.1 foundation

- Selected SQLite for local canonical storage.
- Selected UUID4 identifiers and UTC ISO 8601 timestamps.
- Implemented schema version gate and initial migration.
- Implemented Source, Entity, Memory, and temporal Relationship storage.
- Implemented canonical JSON export/import.
- Added validation and persistence/round-trip tests.
- Deferred Event, Commitment, Decision, and Transaction physical tables to the next storage slice.

## 2026-10-05 — Canonical types v0.1

- Menambahkan physical tables dan storage methods untuk Event, Commitment, Decision, dan Transaction.
- Menaikkan schema version dari 1 ke 2 dengan migration gate v1→v2.
- Memperluas canonical JSON export/import untuk empat tipe baru.
- Menambahkan validasi amount Transaction agar tidak negatif.
- Menambahkan test round-trip dan validation; seluruh suite menjadi 8/8 PASS.


## 2026-10-05 — Memory Engine v0.1 foundation

- Added deterministic, provider-neutral `MemoryDraft` contract.
- Preserved original input text as first-class provenance.
- Added lightweight language detection foundation for Indonesian, Sundanese, mixed input, and limited English keyword recognition.
- Added normalization for purchase capture, basic entity extraction, IDR amount parsing, and selected relative-time expressions.
- Added temporal retrieval intent detection for supported “pernah/can” query patterns.
- Added Memory Engine tests; suite is now **11/11 PASS**.
- Deliberately deferred AI provider integration, broad language coverage, full relationship extraction, and persistence orchestration.


## 2026-10-05 — Memory ingestion + retrieval slice

- Added deterministic `MemoryDraft` persistence orchestration for supported purchase capture.
- Preserved original input and language/intent provenance through `Source` metadata.
- Added event-to-entity canonical links via `event_entities` and schema migration v2→v3.
- Added deterministic purchase retrieval for supported temporal query drafts.
- Added ingestion/retrieval tests; suite is now **14/14 PASS**.
- Kept AI provider integration deferred.
