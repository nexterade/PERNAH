from datetime import datetime, timezone
import unittest

from pernah.ingestion import ingest_draft
from pernah.memory_engine import normalize
from pernah.retrieval import retrieve
from pernah.storage import Storage


REF = datetime(2008, 4, 29, 2, 0, tzinfo=timezone.utc)


class IngestionTests(unittest.TestCase):
    def test_purchase_draft_persists_canonical_records(self):
        draft = normalize("Urang geus meli laptop hargana 2 jt tadi isuk", reference_time=REF)
        with Storage() as db:
            result = ingest_draft(db, draft)
            self.assertIsNotNone(result["source_id"])
            self.assertIsNotNone(result["event_id"])
            self.assertIsNotNone(result["transaction_id"])
            self.assertIsNotNone(result["memory_id"])
            self.assertEqual(db._conn.execute("SELECT COUNT(*) FROM entities WHERE name='laptop'").fetchone()[0], 1)
            self.assertEqual(db._conn.execute("SELECT amount FROM transactions").fetchone()[0], 2_000_000)
            self.assertEqual(db._conn.execute("SELECT COUNT(*) FROM event_entities").fetchone()[0], 1)

    def test_entity_is_not_duplicated_on_repeat_ingestion(self):
        draft = normalize("Urang geus meli laptop hargana 2 jt tadi isuk", reference_time=REF)
        with Storage() as db:
            ingest_draft(db, draft)
            ingest_draft(db, draft)
            self.assertEqual(db._conn.execute("SELECT COUNT(*) FROM entities WHERE type='object' AND name='laptop'").fetchone()[0], 1)

    def test_retrieval_finds_recorded_purchase(self):
        purchase = normalize("Urang geus meli laptop hargana 2 jt tadi isuk", reference_time=REF)
        query = normalize("Urang pernah meli laptop can nya?", reference_time=REF)
        with Storage() as db:
            ingest_draft(db, purchase)
            rows = retrieve(db, query)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["amount"], 2_000_000)
            self.assertEqual(rows[0]["entity_name"], "laptop")
            self.assertEqual(rows[0]["occurred_at"], "2008-04-29T07:00:00Z")

    def test_retrieval_finds_all_purchases_when_object_is_omitted(self):
        laptop = normalize("Urang geus meli laptop hargana 2 jt tadi isuk", reference_time=REF)
        phone = normalize("Urang geus meli handphone hargana 3 jt tadi isuk", reference_time=REF)
        query = normalize("Urang pernah meli can nya?", reference_time=REF)
        self.assertEqual(query.query["action"], "purchase")
        with Storage() as db:
            ingest_draft(db, laptop)
            ingest_draft(db, phone)
            rows = retrieve(db, query)
            self.assertEqual(len(rows), 2)

    def test_storage_purchase_retrieval_supports_temporal_window(self):
        first = normalize("Urang geus meli laptop hargana 2 jt tadi isuk", reference_time=REF)
        second_ref = REF.replace(day=30)
        second = normalize("Urang geus meli laptop hargana 3 jt tadi isuk", reference_time=second_ref)
        with Storage() as db:
            ingest_draft(db, first)
            ingest_draft(db, second)
            rows = db.find_purchase_events(
                entity_name="laptop",
                occurred_after="2008-04-29T00:00:00Z",
                occurred_before="2008-04-29T23:59:59Z",
            )
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["amount"], 2_000_000)
