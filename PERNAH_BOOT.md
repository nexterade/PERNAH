# PERNAH BOOT STATE

> **BACA INI TERLEBIH DAHULU SAAT ZIP PERNAH BARU DIUPLOAD.**
>
> **CHAT IS EPHEMERAL. ARTIFACT IS CONTINUOUS.**
>
> Percakapan adalah workspace sementara. Artifact project adalah sumber kontinuitas.
> Jangan mengandalkan memory chat lama untuk menentukan state project.

## Current release

- **Project:** PERNAH
- **Expansion:** Personal Memory & Life Context System
- **Version:** `0.2.0-dev.63`
- **Schema:** `v4`
- **Status:** active development

## Current continuation point

- **Milestone:** Milestone 6 — AI Layer (plan accepted; implementation not yet started)
- **Current next gate:** Implement M6.1 provider-neutral contracts and M6.2 structured extraction validation using fake providers only, following `docs/AI-LAYER-PLAN.md`.
- **Current shell sub-gate:** shared shell now wraps Home, Memory, Chronicle, Glossary, Settings, and About; Chronicle/Glossary now embed content-only reference surfaces with one product navigation; standalone docs remain directly accessible
- **Completed immediately before this gate:** Warung Padang manual acceptance of the Local Web Interface on the packaged dev.31 artifact
- **Completed immediately before this release:** CLI Web Interface startup now auto-copies its printed local URL when a supported clipboard utility is available
- **AI/provider dependency:** none
- **Canonical data remains authoritative:** yes
- **Deployment concept:** `pernah.my.id` + OpenWrt / AmLogic HG680P candidate runtime; Cloudflare Tunnel candidate access layer; **not implemented**

## Last validated state

- `dev.61` adds canonical image attachments, v3→v4 migration, bounded upload validation, and attachment-preserving backup/restore.
- `dev.62` archived “PERNAH CROSSOVER CATBOX (Coming Soon, Maybe 🤔)” as a non-committed roadmap concept. Catbox is not integrated; attachments remain local SQLite BLOBs.
- `dev.63` records Project Owner PASS for all manual attachment + Backup & Recovery checks on the exact packaged dev.62 artifact and adds a staged Milestone 6 plan; no runtime/schema/provider behavior changes.
- Latest source-tree regression baseline from dev.62: **170 passed, 1 skipped (171 discovered)**. Re-run the full suite and exact-artifact preflight for dev.63 before delivery.
- Exact packaged-artifact validation must be completed for this release before delivery.

- Canonical test command: `python3 -m unittest discover -s tests -v`
- Expected release test result: **170 passed, 1 skipped (171 discovered); exact artifact must be revalidated**
- Exact artifact must be tested again after packaging. The package must contain no generated Python/test cache artifacts, including `.pytest_cache`.
- Release artifact must pass the executable Artifact Compliance Gate: valid version lineage, synchronized release metadata, required structure, flat-root packaging, documentation consistency including Chronicle + Glossary, provenance, and no generated Python cache artifacts.

## Mandatory context sweep

**CHECKPOINT → PERNAH_BOOT → README → STATE → BACKLOG → CHANGELOG → SOURCE + TESTS →
CREATION CHRONICLE + GLOSARIUM (WAJIB) → PLAN → IMPLEMENT → TEST →
DOCUMENT SYNC → PACKAGE → TEST EXACT ARTIFACT → DELIVER ACCESSIBLE ARTIFACT**

For a continuation, the full available `docs/` content must be inspected as required
by `docs/CHECKPOINT.md`. `docs/Glosarium.html`, `docs/Creation-Chronicle.html`, and `docs/SECURITY.md` are
mandatory context, not optional extras.

## Source-of-truth precedence

1. `docs/CHECKPOINT.md` — stable governance/process rules
2. `docs/STATE.md` — current implementation state
3. `docs/BACKLOG.md` — planned work / next gates
4. `docs/CHANGELOG.md` — historical record
5. `README.md` / `docs/TUTORIAL.md` — overview and usage
6. `PERNAH_CONTINUATION.md` — compact handoff aid
7. `PERNAH_BOOT.md` — boot snapshot; useful for fast orientation, **not a higher authority**
8. `PERNAH_PROJECT_STATE.json` — machine-readable boot snapshot, **not a higher authority**

If boot snapshot data conflicts with authoritative documents, authoritative documents
win and the snapshot must be regenerated during document sync.

## Continuation behavior

- **READ TO CONTINUE — NOT READ TO ASK.**
- If `STATE + BACKLOG` already determine the next gate, continue it without asking the
  user to choose a focus again.
- Ask the user only when a real scope/architecture/product decision cannot be resolved
  from the artifact and existing precedence rules.
- Do not restart completed work merely because the chat is new.
- Do not import assumptions, terminology, architecture, or decisions from another project.
- Use Bahasa Indonesia as the default interaction language: natural, santai, jelas,
  dan tidak kaku. Technical names/file names may remain in their canonical form.
- AI acts as a Co-Developer and discussion partner: proactively surface better options,
  risks, trade-offs, and root causes instead of behaving as a command executor or yes-man.
- Respect explicit resource constraints. Prefer free/local/offline/low-cost solutions when
  they satisfy the acceptance criteria; never infer or store personal financial status.
- Human touch is part of normal collaboration: occasionally use a relevant light joke,
  analogy, fun-fact, or human comment when context allows; never force it, and prioritize
  clarity for security, critical errors, data loss, privacy, or safety-sensitive work.

## Why this file exists

This file is a **fast boot snapshot**, not a replacement for CHECKPOINT, STATE, BACKLOG,
CHANGELOG, Glosarium, Chronicle, source, or tests. Its purpose is to make cross-chat
continuation resilient on limited-context/free-tier sessions while keeping authoritative
project state inside the artifact itself.
