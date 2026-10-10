from datetime import datetime, timezone
import unittest

from pernah.memory_engine import normalize
from pernah.ingestion import ingest_draft
from pernah.storage import Storage
from pernah.retrieval import retrieve, timeline

REF = datetime(2026, 10, 5, 2, 0, tzinfo=timezone.utc)


class NextGateTests(unittest.TestCase):
    def test_exact_search_returns_original_memory(self):
        with Storage() as db:
            ingest_draft(db, normalize('Passport ada di laci meja.', reference_time=REF))
            rows = db.exact_search('Passport ada di laci meja')
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['content'], 'Passport ada di laci meja.')

    def test_repeated_entity_capture_is_deduplicated(self):
        with Storage() as db:
            ingest_draft(db, normalize('Urang geus meli laptop hargana 2 jt tadi isuk', reference_time=REF))
            ingest_draft(db, normalize('Urang geus meli laptop hargana 3 jt tadi isuk', reference_time=REF))
            self.assertEqual(db._conn.execute("SELECT COUNT(*) FROM entities WHERE name='laptop'").fetchone()[0], 1)

    def test_temporal_query_extracts_yesterday_window(self):
        draft = normalize('Urang pernah meli laptop kemarin?', reference_time=REF)
        self.assertEqual(draft.query['occurred_after'], '2026-10-04T00:00:00Z')
        self.assertEqual(draft.query['occurred_before'], '2026-10-04T23:59:59Z')

    def test_broader_meeting_relationship_is_persisted(self):
        with Storage() as db:
            draft = normalize('Gue ketemu Rahayu kemarin.', reference_time=REF)
            self.assertEqual(draft.intent, 'record_event')
            result = ingest_draft(db, draft)
            row = db._conn.execute('''SELECT e.name, ee.role FROM event_entities ee
                                      JOIN entities e ON e.id=ee.entity_id WHERE ee.event_id=?''',
                                   (result['event_id'],)).fetchone()
            self.assertEqual(row['name'], 'Rahayu')
            self.assertEqual(row['role'], 'participant')

    def test_entity_relationship_query_resolves_to_timeline(self):
        with Storage() as db:
            first = normalize('Gue ketemu Rahayu kemarin.', reference_time=REF)
            second_ref = REF.replace(day=6)
            second = normalize('Gue ketemu Rahayu hari ini.', reference_time=second_ref)
            ingest_draft(db, first)
            ingest_draft(db, second)

            query = normalize('Gue pernah ketemu Rahayu kapan aja?', reference_time=REF)
            self.assertEqual(query.intent, 'entity_relationship_retrieval')
            self.assertEqual(query.query['entity'], 'Rahayu')
            rows = retrieve(db, query)
            self.assertEqual(len(rows), 2)
            self.assertEqual([r['event_type'] for r in rows], ['meeting', 'meeting'])
            self.assertEqual(rows[0]['entities'][0]['name'], 'Rahayu')
            self.assertEqual(rows[0]['matched_role'], 'participant')
            self.assertEqual(len(rows[0]['memories']), 1)

    def test_entity_relationship_query_can_filter_yesterday(self):
        with Storage() as db:
            ingest_draft(db, normalize('Gue ketemu Rahayu kemarin.', reference_time=REF))
            ingest_draft(db, normalize('Gue ketemu Rahayu hari ini.', reference_time=REF))
            query = normalize('Gue ketemu Rahayu kemarin?', reference_time=REF)
            rows = retrieve(db, query)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['occurred_at'], '2026-10-04T02:00:00Z')

    def test_timeline_direct_api_is_deterministic(self):
        with Storage() as db:
            result = ingest_draft(db, normalize('Gue ketemu Rahayu kemarin.', reference_time=REF))
            rows = timeline(db, 'Rahayu', relation_type='participant')
            self.assertEqual(rows[0]['event_id'], result['event_id'])
            self.assertEqual(rows[0]['entities'][0]['role'], 'participant')


if __name__ == '__main__':
    unittest.main()

class TemporalExpansionTests(unittest.TestCase):
    def test_relationship_query_extracts_last_week_window(self):
        query = normalize('Gue pernah ketemu Rahayu minggu lalu?', reference_time=REF)
        self.assertEqual(query.intent, 'entity_relationship_retrieval')
        self.assertEqual(query.query['occurred_after'], '2026-09-28T00:00:00Z')
        self.assertEqual(query.query['occurred_before'], '2026-10-04T23:59:59Z')

    def test_purchase_query_extracts_last_month_window(self):
        query = normalize('Gue pernah beli laptop bulan lalu?', reference_time=REF)
        self.assertEqual(query.intent, 'temporal_retrieval')
        self.assertEqual(query.query['occurred_after'], '2026-09-01T00:00:00Z')
        self.assertEqual(query.query['occurred_before'], '2026-09-30T23:59:59Z')

    def test_numeric_days_ago_extracts_exact_day_window(self):
        query = normalize('Gue pernah beli laptop 3 hari lalu?', reference_time=REF)
        self.assertEqual(query.query['occurred_after'], '2026-10-02T00:00:00Z')
        self.assertEqual(query.query['occurred_before'], '2026-10-02T23:59:59Z')

    def test_english_temporal_expression_is_supported(self):
        query = normalize('Did I meet Rahayu last week?', reference_time=REF)
        self.assertEqual(query.intent, 'entity_relationship_retrieval')
        self.assertEqual(query.query['occurred_after'], '2026-09-28T00:00:00Z')
        self.assertEqual(query.query['occurred_before'], '2026-10-04T23:59:59Z')

class RicherRelationshipPatternTests(unittest.TestCase):
    def test_conversation_relationship_is_persisted(self):
        with Storage() as db:
            draft = normalize('Gue ngobrol sama Rahayu kemarin.', reference_time=REF)
            self.assertEqual(draft.event['type'], 'conversation')
            self.assertEqual(draft.relationships[0]['relation_type'], 'participant')
            result = ingest_draft(db, draft)
            row = db._conn.execute('''SELECT e.type, en.name, ee.role
                                      FROM events e
                                      JOIN event_entities ee ON ee.event_id=e.id
                                      JOIN entities en ON en.id=ee.entity_id
                                      WHERE e.id=?''', (result['event_id'],)).fetchone()
            self.assertEqual((row['type'], row['name'], row['role']), ('conversation', 'Rahayu', 'participant'))

    def test_call_relationship_is_retrievable(self):
        with Storage() as db:
            ingest_draft(db, normalize('Gue telepon Rahayu kemarin.', reference_time=REF))
            query = normalize('Gue telepon Rahayu kemarin?', reference_time=REF)
            self.assertEqual(query.query['event_type'], 'call')
            rows = retrieve(db, query)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['event_type'], 'call')
            self.assertEqual(rows[0]['matched_role'], 'participant')

    def test_collaboration_relationship_is_retrievable(self):
        with Storage() as db:
            ingest_draft(db, normalize('Gue kerja bareng Rahayu kemarin.', reference_time=REF))
            query = normalize('Gue kerja bareng Rahayu kapan aja?', reference_time=REF)
            self.assertEqual(query.query['event_type'], 'collaboration')
            rows = retrieve(db, query)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['event_type'], 'collaboration')

    def test_richer_relationship_query_keeps_temporal_filter(self):
        with Storage() as db:
            ingest_draft(db, normalize('Gue ngobrol sama Rahayu kemarin.', reference_time=REF))
            ingest_draft(db, normalize('Gue ngobrol sama Rahayu hari ini.', reference_time=REF))
            query = normalize('Gue ngobrol sama Rahayu kemarin?', reference_time=REF)
            rows = retrieve(db, query)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['occurred_at'], '2026-10-04T02:00:00Z')

class SemanticRetrievalTests(unittest.TestCase):
    def test_semantic_search_matches_synonymous_concept(self):
        with Storage() as db:
            ingest_draft(db, normalize('Gue beli laptop baru kemarin.', reference_time=REF))
            rows = retrieve(db, normalize('Gue pernah membeli komputer?', reference_time=REF))
            self.assertEqual(len(rows), 1)
            self.assertGreater(rows[0]['score'], 0)
            self.assertEqual(rows[0]['content'], 'Gue beli laptop baru kemarin.')

    def test_semantic_index_is_rebuildable_and_deterministic(self):
        with Storage() as db:
            ingest_draft(db, normalize('Gue ngobrol sama Rahayu kemarin.', reference_time=REF))
            ingest_draft(db, normalize('Gue telepon Rahayu hari ini.', reference_time=REF))
            first = retrieve(db, normalize('Kapan gue bicara dengan Rahayu?', reference_time=REF))
            second = retrieve(db, normalize('Kapan gue bicara dengan Rahayu?', reference_time=REF))
            self.assertEqual(first, second)
            self.assertEqual(first[0]['content'], 'Gue ngobrol sama Rahayu kemarin.')

    def test_semantic_search_does_not_modify_canonical_memory(self):
        with Storage() as db:
            result = ingest_draft(db, normalize('Passport ada di laci meja.', reference_time=REF))
            before = db.get_memory(result['memory_id'])
            retrieve(db, normalize('Di mana paspor gue?', reference_time=REF))
            after = db.get_memory(result['memory_id'])
            self.assertEqual(before, after)


    def test_semantic_concept_vocabulary_resolves_bicara_to_conversation(self):
        with Storage() as db:
            ingest_draft(db, normalize('Gue ngobrol sama Rahayu kemarin.', reference_time=REF))
            ingest_draft(db, normalize('Gue telepon Rahayu hari ini.', reference_time=REF))
            rows = retrieve(db, normalize('Kapan gue berbicara dengan Rahayu?', reference_time=REF))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['content'], 'Gue ngobrol sama Rahayu kemarin.')

    def test_semantic_concept_boundary_blocks_unrelated_shared_person(self):
        with Storage() as db:
            ingest_draft(db, normalize('Gue ngobrol sama Rahayu kemarin.', reference_time=REF))
            ingest_draft(db, normalize('Gue telepon Rahayu hari ini.', reference_time=REF))
            ingest_draft(db, normalize('Gue ketemu Rahayu minggu lalu.', reference_time=REF))
            rows = retrieve(db, normalize('Gue makan sama Rahayu kapan?', reference_time=REF))
            self.assertEqual(rows, [])

    def test_semantic_concept_vocabulary_supports_phone_synonym(self):
        with Storage() as db:
            ingest_draft(db, normalize('Gue beli handphone baru kemarin.', reference_time=REF))
            rows = retrieve(db, normalize('Gue pernah beli smartphone?', reference_time=REF))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['content'], 'Gue beli handphone baru kemarin.')
