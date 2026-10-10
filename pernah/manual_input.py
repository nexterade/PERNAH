from __future__ import annotations

from datetime import datetime

from .ingestion import ingest_draft
from .memory_engine import normalize
from .storage import Storage


def capture_text(
    db: Storage,
    text: str,
    *,
    reference_time: datetime | None = None,
    source_type: str = "manual",
):
    """Capture one manually supplied text input into canonical storage."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")
    draft = normalize(text, reference_time=reference_time, source_type=source_type)
    result = ingest_draft(db, draft)
    return {"draft": draft, "result": result}
