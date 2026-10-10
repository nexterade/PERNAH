# Milestone 6 — AI Layer: Execution Plan

**Status:** IN PROGRESS — M6.1/M6.2 and extraction orchestration foundation implemented through dev.65  
**Planning baseline:** `0.2.0-dev.63`; updated through `0.2.0-dev.65`  
**Architecture guardrail:** AI is an optional interpretation/answering capability. Canonical memory and deterministic capture/retrieval remain authoritative.

## Outcome

Add a provider-neutral AI boundary that can improve extraction and answer composition without binding PERNAH Core to a vendor, requiring a network connection for ordinary operation, or allowing model output to write unvalidated canonical records.

## Non-goals for the first slice

- No provider selected or API key required yet.
- No automatic cloud calls, background uploads, or hidden transmission of memory/attachments.
- No embeddings/vector database, schema migration, or canonical data model change without a separately reviewed plan.
- No AI-generated claim may be presented as a retrieved fact without supporting canonical memory references.
- No Secret Data or credential storage in canonical memory.

## Delivery slices

### M6.1 — Provider-neutral contract and deterministic fallback

- Define a narrow provider interface for structured extraction and answer generation.
- Define typed request/result/error contracts and explicit capability/configuration status.
- Keep the default implementation unavailable/offline-safe; missing configuration produces a typed, actionable result rather than a crash.
- Provider implementations must not become required dependencies of canonical storage, ingestion, or deterministic retrieval.
- No provider SDK dependency in Core.

### M6.2 — Structured extraction contract

- Model output is an untrusted proposal, never a `MemoryDraft` trusted by construction.
- Validate required fields, allowed intent/type values, confidence range, size limits, and references to the original input.
- Preserve original input and provenance; reject malformed output and fall back to existing deterministic `normalize()` behavior.
- No automatic canonical write until validated and routed through the existing atomic `ingest_draft()` boundary.
- Ambiguous or low-confidence proposals must be returned for review, not silently committed.

### M6.3 — Retrieval orchestration

- Deterministic retrieval runs first and remains available without AI.
- AI may help interpret a query or rerank candidates, but receives only the minimum context needed.
- Answer candidates retain IDs/provenance for canonical memories supporting them.
- Empty retrieval must not be filled with invented personal facts.

### M6.4 — Grounded answer generation

- Compose answers only from retrieved canonical records and distinguish stored facts from inference/uncertainty.
- Include supporting memory IDs or equivalent traceable references in the internal result contract.
- If evidence is insufficient, say so and offer deterministic search/refinement rather than guessing.

### M6.5 — Provider failure and privacy behavior

- Timeout, network failure, invalid response, rate limit, missing configuration, and refusal fail closed to deterministic functionality.
- No secrets or full attachment bytes in logs.
- External processing must be explicit and disclosed; no AI transmission by default.
- Provider retention/training terms and cost must be reviewed before enabling a real provider.

## Cross-cutting constraints

- Canonical SQLite remains the source of truth; AI outputs, summaries, rankings, and indexes are derived/rebuildable.
- Local-first, offline-capable operation remains the baseline.
- Do not prune canonical records automatically.
- Reuse normalization → `MemoryDraft` → atomic ingestion.
- No schema migration unless required and separately planned with migration/backup/restore tests.
- Fake providers cover behavior; tests require neither internet nor real credentials.

## Acceptance criteria

1. Core imports and all existing tests work with no AI SDK and no network.
2. Missing provider configuration does not break capture, storage, or deterministic retrieval.
3. Malformed/oversized/untrusted model output is rejected before canonical mutation.
4. Failed extraction/answer requests fall back without data loss or fabricated memory.
5. Every generated answer candidate carries traceable canonical evidence or explicitly indicates insufficient evidence.
6. Privacy and external-processing boundaries are documented and tested.
7. Full test suite and exact packaged-artifact preflight pass.
8. Project Owner manually accepts new user-facing AI behavior before dependent work proceeds.

## First implementation target

Start with **M6.1 + M6.2 contracts and tests only**, using fake providers and no real network provider. Review the API and failure semantics before adding provider integrations or changing the Web UI.

## Implementation note — dev.64

`pernah/ai_layer.py` now implements provider-neutral contracts, an offline-safe `UnconfiguredProvider`, strict extraction-proposal validation, and evidence-bound answer validation. Tests use local fixtures only. This module intentionally does not call providers, write canonical data, or construct a `MemoryDraft`; deterministic orchestration remains the next gate.


## Implementation note — dev.65

`orchestrate_extraction()` prepares the deterministic `normalize()` draft first, then optionally validates provider output. Missing providers, malformed proposals, and provider exceptions return the deterministic draft. Provider proposals remain advisory and are not converted into `MemoryDraft` or persisted; low-confidence proposals are marked review-required. The provider exception message is intentionally not exposed. Five regression tests cover these branches. This is orchestration groundwork, not retrieval orchestration or a real provider integration.


## Implementation note — dev.66

`orchestrate_retrieval()` runs the existing deterministic `normalize()` → `retrieve()` path first. Only bounded canonical memory candidates with stable memory IDs are eligible as provider evidence. A provider is not called when retrieval is empty. A valid answer is accepted only through `validate_answer()` and must cite IDs in the supplied evidence set. Provider errors preserve deterministic evidence and return a sanitized error class. This layer is advisory and performs no canonical writes.

Known limitation: deterministic retrieval returns different shapes for event/timeline queries; orchestration only forwards rows that can be tied to stable canonical memory IDs. Broader event-to-memory projection should be added only with tests grounded in actual storage return contracts.
