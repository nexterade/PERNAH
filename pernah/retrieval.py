from __future__ import annotations
from .memory_engine import MemoryDraft
from .storage import Storage
from .semantic import semantic_search


def _timeline_from_events(db: Storage, events):
    timeline = []
    for event in events:
        timeline.append({
            'event_id': event['event_id'],
            'event_type': event['event_type'],
            'occurred_at': event['occurred_at'],
            'location_name': event.get('location_name'),
            'matched_role': event.get('matched_role'),
            'entities': db.event_entities(event['event_id']),
            'memories': db.event_memories(event['event_id']),
        })
    return timeline


def timeline(db: Storage, entity_name: str, relation_type: str | None = None,
             occurred_after: str | None = None, occurred_before: str | None = None):
    events = db.find_entity_events(
        entity_name=entity_name,
        relation_type=relation_type,
        occurred_after=occurred_after,
        occurred_before=occurred_before,
    )
    return _timeline_from_events(db, events)


def retrieve(db: Storage, query: MemoryDraft):
    if query.query and query.query.get('action') == 'purchase':
        rows = db.find_purchase_events(
            entity_name=query.query.get('entity'),
            occurred_after=query.query.get('occurred_after'),
            occurred_before=query.query.get('occurred_before'),
        )
        if rows:
            return rows
        # Derived semantic fallback must never override a canonical deterministic hit.
        return semantic_search(db, query.query.get('text', query.original_text))
    if query.query and query.query.get('action') == 'entity_relationship':
        return timeline(
            db,
            entity_name=query.query['entity'],
            relation_type=query.query.get('relation_type'),
            occurred_after=query.query.get('occurred_after'),
            occurred_before=query.query.get('occurred_before'),
        )
    if query.intent == 'exact_search':
        return db.exact_search(query.query.get('text',''))
    if query.intent == 'semantic_retrieval':
        return semantic_search(db, query.query.get('text', ''))
    return []
