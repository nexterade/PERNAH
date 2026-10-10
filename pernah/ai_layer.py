"""Provider-neutral AI contracts; intentionally contains no network or SDK code.

All provider responses are untrusted data. This module validates proposals but does
not persist them to canonical memory or select a provider automatically.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol, Sequence

from .memory_engine import MemoryDraft, normalize


MAX_INPUT_CHARS = 20_000
MAX_OUTPUT_CHARS = 20_000
MAX_ENTITIES = 50
MAX_RELATIONSHIPS = 100
MAX_CONFIDENCE = 1.0
MIN_CONFIDENCE = 0.0


class AIError(RuntimeError):
    """Base class for expected AI boundary failures."""


class ProviderUnavailable(AIError):
    """No provider is configured or available; callers should use deterministic fallback."""


class ProviderFailure(AIError):
    """A configured provider failed; callers should use deterministic fallback."""


class InvalidProposal(AIError, ValueError):
    """A provider proposal is malformed or outside the accepted contract."""


@dataclass(frozen=True)
class ExtractionRequest:
    text: str
    language_hint: str | None = None
    source_type: str = "manual"

    def __post_init__(self) -> None:
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("text must be a non-empty string")
        if len(self.text) > MAX_INPUT_CHARS:
            raise ValueError(f"text exceeds {MAX_INPUT_CHARS} characters")
        if not isinstance(self.source_type, str) or not self.source_type.strip() or len(self.source_type) > 64:
            raise ValueError("source_type must be a non-empty string of at most 64 characters")
        if self.language_hint is not None and (not isinstance(self.language_hint, str) or len(self.language_hint) > 16):
            raise ValueError("language_hint must be at most 16 characters")


@dataclass(frozen=True)
class ExtractionProposal:
    """Untrusted structured proposal; never a MemoryDraft by construction."""
    original_text: str
    normalized_text: str
    intent: str
    detected_language: str
    confidence: float
    entities: tuple[Mapping[str, str], ...] = ()
    event: Mapping[str, Any] | None = None
    transaction: Mapping[str, Any] | None = None
    relationships: tuple[Mapping[str, Any], ...] = ()
    occurred_at: str | None = None
    temporal_expression: str | None = None


@dataclass(frozen=True)
class ValidatedExtraction:
    """Validated candidate awaiting review/fallback; not yet canonical data."""
    proposal: ExtractionProposal
    requires_review: bool
    review_reasons: tuple[str, ...]


@dataclass(frozen=True)
class AnswerRequest:
    question: str
    evidence: tuple[Mapping[str, Any], ...]
    max_answer_chars: int = 4_000

    def __post_init__(self) -> None:
        if not isinstance(self.question, str) or not self.question.strip():
            raise ValueError("question must be a non-empty string")
        if len(self.question) > MAX_INPUT_CHARS:
            raise ValueError(f"question exceeds {MAX_INPUT_CHARS} characters")
        if not isinstance(self.evidence, tuple):
            raise ValueError("evidence must be a tuple of retrieved canonical records")
        if not isinstance(self.max_answer_chars, int) or not 1 <= self.max_answer_chars <= MAX_OUTPUT_CHARS:
            raise ValueError(f"max_answer_chars must be between 1 and {MAX_OUTPUT_CHARS}")


@dataclass(frozen=True)
class AnswerCandidate:
    text: str
    supporting_memory_ids: tuple[str, ...]
    evidence_sufficient: bool
    uncertainty_note: str | None = None


def validate_extraction(raw: Mapping[str, Any], request: ExtractionRequest, *, review_threshold: float = 0.65) -> ValidatedExtraction:
    """Validate provider JSON without coercing arbitrary values or trusting its source text."""
    if not isinstance(raw, Mapping):
        raise InvalidProposal("proposal must be an object")
    allowed = {
        "original_text", "normalized_text", "intent", "detected_language", "confidence",
        "entities", "event", "transaction", "relationships", "occurred_at", "temporal_expression",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise InvalidProposal("proposal contains unsupported fields")

    original = raw.get("original_text")
    normalized = raw.get("normalized_text")
    intent = raw.get("intent")
    language = raw.get("detected_language")
    confidence = raw.get("confidence")
    if original != request.text:
        raise InvalidProposal("original_text must exactly match the submitted input")
    if not isinstance(normalized, str) or not normalized.strip() or len(normalized) > MAX_OUTPUT_CHARS:
        raise InvalidProposal("normalized_text must be non-empty and within the size limit")
    if not isinstance(intent, str) or intent not in {"record_event", "record_transaction", "record_fact", "retrieval", "unknown"}:
        raise InvalidProposal("intent is not supported")
    if not isinstance(language, str) or language not in {"id", "su", "en", "unknown"}:
        raise InvalidProposal("detected_language is not supported")
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not MIN_CONFIDENCE <= confidence <= MAX_CONFIDENCE:
        raise InvalidProposal("confidence must be a number between 0 and 1")

    entities = raw.get("entities", [])
    relationships = raw.get("relationships", [])
    if not isinstance(entities, list) or len(entities) > MAX_ENTITIES:
        raise InvalidProposal("entities must be a list within the size limit")
    clean_entities: list[dict[str, str]] = []
    entity_names: set[str] = set()
    for entity in entities:
        if not isinstance(entity, Mapping) or set(entity) != {"type", "name"}:
            raise InvalidProposal("each entity must contain only type and name")
        etype, name = entity["type"], entity["name"]
        if not isinstance(etype, str) or etype not in {"person", "place", "object", "organization", "other"}:
            raise InvalidProposal("entity type is not supported")
        if not isinstance(name, str) or not name.strip() or len(name) > 200:
            raise InvalidProposal("entity name must be non-empty and at most 200 characters")
        clean_entities.append({"type": etype, "name": name.strip()})
        entity_names.add(name.strip().casefold())

    if not isinstance(relationships, list) or len(relationships) > MAX_RELATIONSHIPS:
        raise InvalidProposal("relationships must be a list within the size limit")
    clean_relationships: list[dict[str, Any]] = []
    for relation in relationships:
        if not isinstance(relation, Mapping) or set(relation) != {"entity_name", "relation_type"}:
            raise InvalidProposal("each relationship must contain entity_name and relation_type only")
        name, relation_type = relation["entity_name"], relation["relation_type"]
        if not isinstance(name, str) or name.casefold() not in entity_names:
            raise InvalidProposal("relationship must reference a declared entity")
        if not isinstance(relation_type, str) or relation_type not in {"participant", "owner", "counterparty", "location", "other"}:
            raise InvalidProposal("relationship type is not supported")
        clean_relationships.append({"entity_name": name, "relation_type": relation_type})

    event = raw.get("event")
    transaction = raw.get("transaction")
    if event is not None:
        if not isinstance(event, Mapping) or set(event) - {"type", "occurred_at"} or not isinstance(event.get("type"), str) or not event["type"].strip():
            raise InvalidProposal("event must contain a non-empty type and optional occurred_at")
    if transaction is not None:
        if not isinstance(transaction, Mapping) or set(transaction) - {"amount", "currency", "direction", "counterparty", "description"}:
            raise InvalidProposal("transaction fields are unsupported")
        amount = transaction.get("amount")
        if amount is not None and (isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount < 0):
            raise InvalidProposal("transaction amount must be a non-negative number")
        for key, value in transaction.items():
            if value is not None and not isinstance(value, (str, int, float)):
                raise InvalidProposal(f"transaction {key} has an invalid value")
    if transaction is not None and event is None:
        raise InvalidProposal("transaction proposal requires an event")

    optional_strings = ("occurred_at", "temporal_expression")
    for key in optional_strings:
        if raw.get(key) is not None and (not isinstance(raw[key], str) or len(raw[key]) > 128):
            raise InvalidProposal(f"{key} must be a string of at most 128 characters")

    proposal = ExtractionProposal(
        original_text=original, normalized_text=normalized, intent=intent,
        detected_language=language, confidence=float(confidence),
        entities=tuple(clean_entities), event=dict(event) if event is not None else None,
        transaction=dict(transaction) if transaction is not None else None,
        relationships=tuple(clean_relationships), occurred_at=raw.get("occurred_at"),
        temporal_expression=raw.get("temporal_expression"),
    )
    reasons = []
    if proposal.confidence < review_threshold:
        reasons.append("confidence_below_review_threshold")
    if proposal.intent in {"unknown", "retrieval"}:
        reasons.append("intent_requires_deterministic_routing")
    return ValidatedExtraction(proposal, bool(reasons), tuple(reasons))


def validate_answer(raw: Mapping[str, Any], request: AnswerRequest) -> AnswerCandidate:
    """Validate answer provenance against the exact retrieved evidence set."""
    if not isinstance(raw, Mapping) or set(raw) - {"text", "supporting_memory_ids", "evidence_sufficient", "uncertainty_note"}:
        raise InvalidProposal("answer must be an object with supported fields")
    text = raw.get("text")
    ids = raw.get("supporting_memory_ids")
    sufficient = raw.get("evidence_sufficient")
    note = raw.get("uncertainty_note")
    if not isinstance(text, str) or not text.strip() or len(text) > request.max_answer_chars:
        raise InvalidProposal("answer text is empty or exceeds the size limit")
    if not isinstance(ids, list) or any(not isinstance(value, str) or not value for value in ids):
        raise InvalidProposal("supporting_memory_ids must be a list of non-empty strings")
    available = {str(item.get("memory_id")) for item in request.evidence if isinstance(item, Mapping) and item.get("memory_id") is not None}
    if any(memory_id not in available for memory_id in ids):
        raise InvalidProposal("answer cites a memory that was not provided as evidence")
    if not isinstance(sufficient, bool):
        raise InvalidProposal("evidence_sufficient must be boolean")
    if sufficient and not ids:
        raise InvalidProposal("sufficient evidence requires at least one supporting memory ID")
    if not sufficient and not isinstance(note, str):
        raise InvalidProposal("insufficient evidence requires an uncertainty note")
    if note is not None and (not isinstance(note, str) or len(note) > 500):
        raise InvalidProposal("uncertainty_note must be at most 500 characters")
    return AnswerCandidate(text.strip(), tuple(dict.fromkeys(ids)), sufficient, note)


class AIProvider(Protocol):
    """Provider interface only; concrete integrations are deliberately out of scope."""
    name: str

    def extract(self, request: ExtractionRequest) -> Mapping[str, Any]: ...
    def answer(self, request: AnswerRequest) -> Mapping[str, Any]: ...


class UnconfiguredProvider:
    """Offline-safe default. It never performs network I/O."""
    name = "unconfigured"

    def extract(self, request: ExtractionRequest) -> Mapping[str, Any]:
        raise ProviderUnavailable("No AI provider configured; use deterministic normalize() fallback.")

    def answer(self, request: AnswerRequest) -> Mapping[str, Any]:
        raise ProviderUnavailable("No AI provider configured; use deterministic retrieval fallback.")


@dataclass(frozen=True)
class ExtractionOutcome:
    """Safe orchestration result; deterministic draft is the only write-ready value.

    A validated provider proposal is advisory and is never converted into a MemoryDraft
    automatically. Callers may show it for review, while canonical capture remains on
    the deterministic path unless a later, explicit review workflow is implemented.
    """
    draft: MemoryDraft
    mode: str
    provider_candidate: ValidatedExtraction | None = None
    fallback_reason: str | None = None


def orchestrate_extraction(
    text: str,
    provider: AIProvider | None = None,
    *,
    reference_time=None,
    source_type: str = "manual",
) -> ExtractionOutcome:
    """Use deterministic normalization as the authoritative fallback.

    Provider absence, provider errors, malformed proposals, or low-confidence/review
    candidates never block capture and never mutate canonical storage. Even a valid
    provider proposal remains advisory; the returned write-ready draft is deterministic.
    """
    # Normalize first so capture has a ready, provider-independent result even if the
    # optional provider fails or returns invalid data.
    draft = normalize(text, reference_time=reference_time, source_type=source_type)
    if provider is None:
        return ExtractionOutcome(draft=draft, mode="deterministic", fallback_reason="provider_not_configured")

    request = ExtractionRequest(text=text, source_type=source_type)
    try:
        raw = provider.extract(request)
        candidate = validate_extraction(raw, request)
    except (AIError, ValueError, TypeError) as exc:
        return ExtractionOutcome(
            draft=draft,
            mode="deterministic_fallback",
            fallback_reason=type(exc).__name__,
        )
    except Exception as exc:
        # Third-party providers may surface transport/timeouts using their own exception
        # types. Fail closed without leaking exception messages that may contain secrets.
        return ExtractionOutcome(
            draft=draft,
            mode="deterministic_fallback",
            fallback_reason=f"provider_error:{type(exc).__name__}",
        )

    if candidate.requires_review:
        return ExtractionOutcome(
            draft=draft,
            mode="deterministic_review_required",
            provider_candidate=candidate,
            fallback_reason="proposal_requires_review",
        )
    return ExtractionOutcome(
        draft=draft,
        mode="deterministic_with_candidate",
        provider_candidate=candidate,
    )


@dataclass(frozen=True)
class RetrievalResult:
    """Deterministic canonical candidates plus an optional grounded answer candidate."""
    query: str
    evidence: tuple[Mapping[str, Any], ...]
    mode: str
    answer_candidate: AnswerCandidate | None = None
    fallback_reason: str | None = None


def orchestrate_retrieval(db: Any, question: str, provider: Any | None = None, *, limit: int = 10) -> RetrievalResult:
    """Run deterministic retrieval first; AI may only see bounded canonical evidence.

    This function never writes canonical data. Provider failures return the exact
    deterministic candidates without exposing provider exception messages.
    """
    if not isinstance(question, str) or not question.strip():
        raise ValueError("question must be a non-empty string")
    if len(question) > MAX_INPUT_CHARS:
        raise ValueError(f"question exceeds {MAX_INPUT_CHARS} characters")
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 50:
        raise ValueError("limit must be an integer between 1 and 50")

    from .memory_engine import normalize
    from .retrieval import retrieve

    draft = normalize(question)
    rows = retrieve(db, draft)
    # If intent routing returns no rows, preserve deterministic exact search as a
    # safe secondary path; never ask a provider to invent absent personal facts.
    if not rows and hasattr(db, "exact_search"):
        rows = db.exact_search(question)
    # Canonical retrieval outputs vary by query type. Only mappings with stable
    # memory IDs can be passed as answer evidence; timeline/event rows are
    # reduced to their referenced canonical memory records.
    candidates: list[Mapping[str, Any]] = []
    seen: set[str] = set()
    for row in rows or []:
        if not isinstance(row, Mapping):
            continue
        if row.get("memory_id", row.get("id")) is not None:
            item = dict(row)
            key = str(item.get("memory_id", item.get("id")))
            item["memory_id"] = key
            if key not in seen:
                candidates.append(item)
                seen.add(key)
        elif isinstance(row.get("memories"), (list, tuple)):
            for memory in row["memories"]:
                if not isinstance(memory, Mapping) or memory.get("memory_id", memory.get("id")) is None:
                    continue
                item = dict(memory)
                key = str(item.get("memory_id", item.get("id")))
                item["memory_id"] = key
                if key not in seen:
                    candidates.append(item)
                    seen.add(key)
    evidence = tuple(candidates[:limit])
    if provider is None:
        return RetrievalResult(question, evidence, "deterministic", fallback_reason="provider_not_configured")
    if not evidence:
        # Never ask a model to invent a personal fact when canonical retrieval found nothing.
        return RetrievalResult(question, (), "deterministic_no_evidence", fallback_reason="no_canonical_evidence")
    request = AnswerRequest(question, evidence)
    try:
        raw = provider.answer(request)
        candidate = validate_answer(raw, request)
    except Exception as exc:
        return RetrievalResult(question, evidence, "deterministic_fallback", fallback_reason=f"provider_error:{type(exc).__name__}")
    if not candidate.evidence_sufficient:
        return RetrievalResult(question, evidence, "deterministic_review_required", answer_candidate=candidate,
                               fallback_reason="evidence_insufficient")
    return RetrievalResult(question, evidence, "deterministic_with_grounded_candidate", answer_candidate=candidate)
