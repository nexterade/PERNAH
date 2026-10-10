from __future__ import annotations

import uuid

from .memory_engine import MemoryDraft
from .storage import Storage, ValidationError


def ingest_draft(db: Storage, draft: MemoryDraft):
    """Persist one draft atomically; any failure leaves canonical tables unchanged."""
    # Reject the known invalid shape before opening a write scope.
    if draft.transaction and not draft.event:
        raise ValidationError('transaction draft requires an event')

    # A savepoint also works when the caller already has an open Storage transaction.
    savepoint = f"ingest_draft_{uuid.uuid4().hex}"
    db._conn.execute(f'SAVEPOINT {savepoint}')
    try:
        source_id = db.add_source(draft.source_type, draft.original_text)
        memory_id = db.add_memory('interaction', draft.original_text, source_id=source_id, confidence=draft.confidence, occurred_at=draft.occurred_at)
        result = {'source_id': source_id, 'memory_id': memory_id}
        entity_ids = []
        for entity in draft.entities:
            entity_ids.append((entity, db.add_entity(entity['type'], entity['name'])))
        if draft.event:
            event_id = db.add_event(draft.event['type'], draft.event.get('occurred_at'), source_id=source_id)
            result['event_id'] = event_id
            for entity, eid in entity_ids:
                role = next((r['relation_type'] for r in draft.relationships if r.get('entity', {}).get('name') == entity['name']), None)
                db.link_event_entity(event_id, eid, role=role)
        if draft.transaction:
            result['transaction_id'] = db.add_transaction(event_id=result['event_id'], source_id=source_id, **draft.transaction)
        db._conn.execute(f'RELEASE SAVEPOINT {savepoint}')
        return result
    except BaseException:
        db._conn.execute(f'ROLLBACK TO SAVEPOINT {savepoint}')
        db._conn.execute(f'RELEASE SAVEPOINT {savepoint}')
        raise
