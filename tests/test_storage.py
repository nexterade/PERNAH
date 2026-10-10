import json
import tempfile
import unittest
from pathlib import Path

from pernah.storage import Storage, ValidationError


class StorageTests(unittest.TestCase):
    def test_schema_initializes_and_is_versioned(self):
        with Storage() as db:
            self.assertEqual(db.schema_version, 3)

    def test_memory_has_source_and_confidence(self):
        with Storage() as db:
            source = db.add_source(source_type="manual", reference="test")
            mid = db.add_memory(
                memory_type="note",
                content="Passport ada di laci meja",
                source_id=source,
                confidence=0.95,
            )
            row = db.get_memory(mid)
            self.assertEqual(row["source_id"], source)
            self.assertEqual(row["confidence"], 0.95)

    def test_confidence_is_validated(self):
        with Storage() as db:
            with self.assertRaises(ValidationError):
                db.add_memory(memory_type="note", content="x", confidence=1.5)

    def test_temporal_location_history_preserves_old_state(self):
        with Storage() as db:
            passport = db.add_entity(entity_type="object", name="Passport")
            drawer = db.add_entity(entity_type="location", name="Laci meja")
            safe = db.add_entity(entity_type="location", name="Safe")
            old = db.add_location_state(object_entity=passport, location_entity=drawer, valid_from="2026-10-05T00:00:00Z")
            db.close_location_state(old, "2027-03-11T23:59:59Z")
            db.add_location_state(object_entity=passport, location_entity=safe, valid_from="2027-03-12T00:00:00Z")
            latest = db.latest_location(passport)
            self.assertEqual(latest["location_name"], "Safe")
            self.assertEqual(latest["valid_from"], "2027-03-12T00:00:00Z")
            history = db._conn.execute("SELECT COUNT(*) FROM relationships WHERE from_entity=?", (passport,)).fetchone()[0]
            self.assertEqual(history, 2)

    def test_file_database_persists_between_connections(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "pernah.db"
            with Storage(db_path) as db:
                db.add_memory(memory_type="note", content="Persisten", confidence=1.0)
            with Storage(db_path) as db:
                self.assertEqual(db.list_memories()[0]["content"], "Persisten")

    def test_export_import_round_trip(self):
        with tempfile.TemporaryDirectory() as td:
            export_path = Path(td) / "pernah.json"
            with Storage() as source:
                entity = source.add_entity(entity_type="person", name="Rahayu")
                source.add_memory(memory_type="relationship", content="Rahayu is beloved", confidence=1.0)
                source.export_json(export_path)

            payload = json.loads(export_path.read_text(encoding="utf-8"))
            with Storage() as target:
                target.import_canonical(payload)
                self.assertEqual(target.list_memories()[0]["content"], "Rahayu is beloved")
                self.assertEqual(target._conn.execute("SELECT name FROM entities WHERE id=?", (entity,)).fetchone()[0], "Rahayu")

    def test_event_commitment_decision_transaction_round_trip(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "pernah.db"
            with Storage(path) as db:
                source = db.add_source(source_type="manual", reference="test")
                rahayu = db.add_entity(entity_type="person", name="Rahayu")
                place = db.add_entity(entity_type="location", name="Cafe")
                event = db.add_event(event_type="meeting", occurred_at="2026-10-05T12:00:00Z", location_id=place, source_id=source)
                db.link_event_entity(event_id=event, entity_id=rahayu, role="participant")
                commitment = db.add_commitment(action="kirim invoice", person_id=rahayu, deadline="2026-10-09T17:00:00Z", source_id=source)
                decision = db.add_decision(decision="Batal beli laptop X", reason="Terlalu mahal", occurred_at="2026-10-05T13:00:00Z", source_id=source)
                transaction = db.add_transaction(amount=85000, currency="IDR", direction="expense", occurred_at="2026-10-05T12:30:00Z", category="food", event_id=event, person_id=rahayu, source_id=source)
                payload = db.export_canonical()
                self.assertEqual({"events","commitments","decisions","transactions"}, set(payload) & {"events","commitments","decisions","transactions"})
            with Storage() as restored:
                restored.import_canonical(payload)
                self.assertEqual(restored._conn.execute("SELECT COUNT(*) FROM events").fetchone()[0], 1)
                self.assertEqual(restored._conn.execute("SELECT COUNT(*) FROM event_entities").fetchone()[0], 1)
                self.assertEqual(restored._conn.execute("SELECT COUNT(*) FROM commitments").fetchone()[0], 1)
                self.assertEqual(restored._conn.execute("SELECT COUNT(*) FROM decisions").fetchone()[0], 1)
                self.assertEqual(restored._conn.execute("SELECT amount FROM transactions").fetchone()[0], 85000)

    def test_transaction_rejects_negative_amount(self):
        with Storage() as db:
            with self.assertRaises(ValidationError):
                db.add_transaction(amount=-1)


if __name__ == "__main__":
    unittest.main()
