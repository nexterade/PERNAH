from __future__ import annotations
from .memory_engine import MemoryDraft
from .storage import Storage, ValidationError


def ingest_draft(db: Storage, draft: MemoryDraft):
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
        if not draft.event:
            raise ValidationError('transaction draft requires an event')
        result['transaction_id'] = db.add_transaction(event_id=draft.event and result['event_id'], source_id=source_id, **draft.transaction)
    return result
