import json
import tempfile
import unittest
from pathlib import Path

from pernah.storage import Storage, ValidationError


class StorageTests(unittest.TestCase):
    def test_schema_initializes_and_is_versioned(self):
        with Storage() as db:
            self.assertEqual(db.schema_version, 4)

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


    def test_attachment_round_trip_and_memory_link(self):
        png = __import__('base64').b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j3ioAAAAASUVORK5CYII=')
        with Storage() as db:
            memory_id = db.add_memory('note', 'Rahayu meminjam Rp200.000')
            attachment_id = db.add_attachment(memory_id, '../bukti.png', 'image/png', png)
            attachment = db.get_attachment(attachment_id)
            self.assertEqual(attachment['memory_id'], memory_id)
            self.assertEqual(attachment['filename'], 'bukti.png')
            self.assertEqual(attachment['data'], png)
            self.assertEqual(db.list_attachments(memory_id)[0]['id'], attachment_id)

    def test_attachment_is_included_in_canonical_backup_and_restore(self):
        import base64
        png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j3ioAAAAASUVORK5CYII=')
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            backup, target = tmp / 'backup.json', tmp / 'restored.db'
            with Storage() as db:
                memory_id = db.add_memory('note', 'Bukti transfer Rahayu')
                db.add_attachment(memory_id, 'transfer.png', 'image/png', png)
                db.backup(backup)
            self.assertTrue(Storage.validate_backup(backup))
            Storage.restore(backup, target)
            with Storage(target) as restored:
                self.assertEqual(restored.get_attachment(restored.list_attachments(memory_id)[0]['id'])['data'], png)

    def test_v3_database_migrates_to_v4_without_losing_memory(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'legacy.db'
            with Storage(path) as db:
                db.add_memory('note', 'Existing v3 memory')
                db._conn.execute("UPDATE metadata SET value='3' WHERE key='schema_version'")
            with Storage(path) as migrated:
                self.assertEqual(migrated.schema_version, 4)
                self.assertEqual(migrated.exact_search('Existing v3 memory')[0]['content'], 'Existing v3 memory')

    def test_v3_canonical_backup_remains_restorable(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            backup = Path(tmp) / 'legacy-v3.json'
            with Storage() as db:
                memory_id = db.add_memory('note', 'Legacy backup survives migration')
                payload = db.export_canonical()
            payload.pop('attachments')
            payload['schema_version'] = 3
            for row in payload['memories']:
                row['schema_version'] = 3
            backup.write_text(json.dumps(payload), encoding='utf-8')
            self.assertTrue(Storage.validate_backup(backup))
            with Storage() as restored:
                restored.import_json(backup)
                self.assertEqual(restored.get_memory(memory_id)['content'], 'Legacy backup survives migration')

    def test_invalid_attachment_signature_is_rejected(self):
        with Storage() as db:
            memory_id = db.add_memory('note', 'No fake image')
            with self.assertRaises(ValueError):
                db.add_attachment(memory_id, 'fake.png', 'image/png', b'not a PNG')


if __name__ == '__main__':
    unittest.main()
