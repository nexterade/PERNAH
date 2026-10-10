import json
import tempfile
import unittest
from pathlib import Path

from pernah.storage import SCHEMA_VERSION, Storage, ValidationError


class BackupTests(unittest.TestCase):
    def _populate(self, db: Storage):
        source = db.add_source('test', 'backup-suite')
        person = db.add_entity('person', 'Rahayu')
        laptop = db.add_entity('object', 'Laptop')
        event = db.add_event('purchase', '2026-10-05T02:00:00Z', location_id=None, source_id=source)
        db.link_event_entity(event, laptop, 'object')
        db.link_event_entity(event, person, 'buyer')
        db.add_memory('purchase', 'Meli laptop', source_id=source, confidence=0.9, occurred_at='2026-10-05T02:00:00Z')
        db.add_transaction(2000000, event_id=event, person_id=person, source_id=source, occurred_at='2026-10-05T02:00:00Z')
        db.add_relationship(laptop, 'owned_by', person, source_id=source, confidence=1.0)
        db.add_commitment('Cek laptop', person_id=person, source_id=source)
        db.add_decision('Pilih laptop', 'Kebutuhan kerja', source_id=source)

    def test_backup_writes_canonical_json_and_validates(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'backup.json'
            with Storage() as db:
                self._populate(db)
                result = db.backup(path)
                before = db.export_canonical()
            self.assertEqual(result, path)
            self.assertTrue(path.is_file())
            payload = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(payload['format'], 'pernah-canonical-v1')
            self.assertEqual(payload['schema_version'], SCHEMA_VERSION)
            self.assertTrue(Storage.validate_backup(path))
            self.assertEqual(payload, before)

    def test_empty_database_backup_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'empty.json'
            with Storage() as db:
                db.backup(path)
            self.assertTrue(Storage.validate_backup(path))

    def test_backup_is_deterministic_for_same_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            first, second = Path(tmp) / 'a.json', Path(tmp) / 'b.json'
            with Storage() as db:
                self._populate(db)
                db.backup(first)
                db.backup(second)
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_missing_backup_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValidationError):
                Storage.validate_backup(Path(tmp) / 'missing.json')

    def test_invalid_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'broken.json'
            path.write_text('{broken', encoding='utf-8')
            with self.assertRaises(ValidationError):
                Storage.validate_backup(path)

    def test_wrong_format_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'wrong-format.json'
            with Storage() as db:
                payload = db.export_canonical()
            payload['format'] = 'not-pernah'
            path.write_text(json.dumps(payload), encoding='utf-8')
            with self.assertRaises(ValidationError):
                Storage.validate_backup(path)

    def test_wrong_schema_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'wrong-schema.json'
            with Storage() as db:
                payload = db.export_canonical()
            payload['schema_version'] = 999
            path.write_text(json.dumps(payload), encoding='utf-8')
            with self.assertRaises(ValidationError):
                Storage.validate_backup(path)

    def test_missing_table_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'missing-table.json'
            with Storage() as db:
                payload = db.export_canonical()
            del payload['events']
            path.write_text(json.dumps(payload), encoding='utf-8')
            with self.assertRaises(ValidationError):
                Storage.validate_backup(path)

    def test_broken_foreign_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'broken-fk.json'
            with Storage() as db:
                payload = db.export_canonical()
            payload['relationships'].append({
                'id': 'broken-relationship',
                'from_entity': 'missing-entity',
                'relation_type': 'owned_by',
                'to_entity': 'missing-entity-2',
                'valid_from': None,
                'valid_until': None,
                'source_id': None,
                'confidence': 1.0,
            })
            path.write_text(json.dumps(payload), encoding='utf-8')
            with self.assertRaises(ValidationError):
                Storage.validate_backup(path)

    def test_invalid_canonical_values_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'invalid-values.json'
            with Storage() as db:
                payload = db.export_canonical()
                source = db.add_source('test', 'validation')
                payload = db.export_canonical()
            payload['memories'] = [{
                'id': 'bad-memory', 'type': 'note', 'content': 'x',
                'created_at': '2026-10-05T00:00:00Z', 'occurred_at': None,
                'updated_at': '2026-10-05T00:00:00Z', 'source_id': source,
                'confidence': 2.0, 'schema_version': SCHEMA_VERSION,
            }]
            path.write_text(json.dumps(payload), encoding='utf-8')
            with self.assertRaises(ValidationError):
                Storage.validate_backup(path)

    def test_extra_row_field_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'extra-field.json'
            with Storage() as db:
                payload = db.export_canonical()
            payload['entities'].append({
                'id': 'extra', 'type': 'person', 'name': 'X',
                'created_at': '2026-10-05T00:00:00Z',
                'updated_at': '2026-10-05T00:00:00Z',
                'extra': 'must-not-be-ignored',
            })
            path.write_text(json.dumps(payload), encoding='utf-8')
            with self.assertRaises(ValidationError):
                Storage.validate_backup(path)

    def test_import_round_trip_remains_validated(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'round-trip.json'
            with Storage() as source:
                self._populate(source)
                source.backup(path)
            payload = json.loads(path.read_text(encoding='utf-8'))
            with Storage() as restored:
                restored.import_canonical(payload)
                self.assertEqual(restored.export_canonical(), payload)


if __name__ == '__main__':
    unittest.main()

class RestoreTests(unittest.TestCase):
    def _populate(self, db: Storage):
        source = db.add_source('test', 'restore-suite')
        person = db.add_entity('person', 'Rahayu')
        laptop = db.add_entity('object', 'Laptop')
        event = db.add_event('purchase', '2026-10-05T02:00:00Z', source_id=source)
        db.link_event_entity(event, laptop, 'object')
        db.link_event_entity(event, person, 'buyer')
        db.add_memory('purchase', 'Meli laptop', source_id=source, confidence=0.9, occurred_at='2026-10-05T02:00:00Z')
        db.add_transaction(2000000, event_id=event, person_id=person, source_id=source, occurred_at='2026-10-05T02:00:00Z')
        db.add_relationship(laptop, 'owned_by', person, source_id=source, confidence=1.0)

    def test_restore_recreates_empty_database(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            backup = tmp / 'empty.json'
            target = tmp / 'restored.db'
            with Storage() as db:
                db.backup(backup)
            self.assertEqual(Storage.restore(backup, target), target.resolve())
            with Storage(target) as restored:
                self.assertEqual(restored.export_canonical(), json.loads(backup.read_text(encoding='utf-8')))

    def test_restore_round_trip_matches_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            backup = tmp / 'state.json'
            target = tmp / 'restored.db'
            with Storage() as db:
                self._populate(db)
                db.backup(backup)
                expected = db.export_canonical()
            Storage.restore(backup, target)
            with Storage(target) as restored:
                self.assertEqual(restored.export_canonical(), expected)

    def test_restore_replaces_existing_target_only_after_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            backup = tmp / 'state.json'
            target = tmp / 'target.db'
            with Storage() as db:
                self._populate(db)
                db.backup(backup)
            with Storage(target) as db:
                db.add_memory('note', 'old state')
            Storage.restore(backup, target)
            with Storage(target) as restored:
                self.assertEqual(restored.exact_search('old state'), [])
                self.assertEqual(len(restored.list_memories()), 1)

    def test_invalid_backup_does_not_modify_existing_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            backup = tmp / 'broken.json'
            target = tmp / 'target.db'
            with Storage(target) as db:
                db.add_memory('note', 'must survive')
            backup.write_text('{broken', encoding='utf-8')
            with self.assertRaises(ValidationError):
                Storage.restore(backup, target)
            with Storage(target) as db:
                self.assertEqual(db.exact_search('must survive')[0]['content'], 'must survive')

    def test_broken_backup_does_not_modify_existing_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            backup = tmp / 'broken-fk.json'
            target = tmp / 'target.db'
            with Storage() as db:
                payload = db.export_canonical()
            payload['relationships'].append({
                'id': 'broken', 'from_entity': 'missing', 'relation_type': 'owned_by',
                'to_entity': 'missing-2', 'valid_from': None, 'valid_until': None,
                'source_id': None, 'confidence': 1.0,
            })
            backup.write_text(json.dumps(payload), encoding='utf-8')
            with Storage(target) as db:
                db.add_memory('note', 'must survive')
            with self.assertRaises(ValidationError):
                Storage.restore(backup, target)
            with Storage(target) as db:
                self.assertEqual(db.exact_search('must survive')[0]['content'], 'must survive')

    def test_backup_and_target_must_differ(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'same.json'
            with Storage() as db:
                db.backup(path)
            with self.assertRaises(ValidationError):
                Storage.restore(path, path)

class PortableExportImportTests(unittest.TestCase):
    def test_export_json_creates_parent_and_replaces_atomically(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'nested' / 'backup' / 'pernah.json'
            with Storage() as db:
                db.add_memory(memory_type='note', content='portable', confidence=1.0)
                self.assertEqual(db.export_json(path), path)
            self.assertTrue(path.is_file())
            self.assertTrue(Storage.validate_backup(path))
            self.assertFalse(any(path.parent.glob('.*.export-*.json')))

    def test_import_json_validates_before_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            backup = Path(td) / 'backup.json'
            with Storage() as source:
                source.add_memory(memory_type='note', content='valid payload', confidence=1.0)
                source.backup(backup)

            payload = json.loads(backup.read_text(encoding='utf-8'))
            payload['memories'][0]['confidence'] = 2.0
            backup.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')

            with Storage() as target:
                target.add_memory(memory_type='note', content='must survive', confidence=1.0)
                with self.assertRaises(ValidationError):
                    target.import_json(backup)
                self.assertEqual(target.list_memories()[0]['content'], 'must survive')

    def test_import_json_round_trip_is_portable(self):
        with tempfile.TemporaryDirectory() as td:
            backup = Path(td) / 'portable.json'
            with Storage() as source:
                source.add_memory(memory_type='note', content='Halo dunia 👋', confidence=1.0)
                source.backup(backup)
                expected = source.export_canonical()

            with Storage() as target:
                self.assertIs(target.import_json(backup), target)
                self.assertEqual(target.export_canonical(), expected)

    def test_import_json_rejects_broken_relationship_without_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            backup = Path(td) / 'broken.json'
            with Storage() as source:
                entity = source.add_entity(entity_type='person', name='Rahayu')
                target = source.add_entity(entity_type='person', name='Budi')
                source.add_relationship(entity, 'knows', target)
                payload = source.export_canonical()
            payload['relationships'][0]['to_entity'] = 'missing-entity'
            backup.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')

            with Storage() as target:
                target.add_memory(memory_type='note', content='unchanged', confidence=1.0)
                with self.assertRaises(ValidationError):
                    target.import_json(backup)
                self.assertEqual(target.list_memories()[0]['content'], 'unchanged')


class DisasterRecoveryTests(unittest.TestCase):
    def test_full_disaster_recovery_drill_recreates_deleted_database(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source_path = root / 'live.db'
            backup_path = root / 'backup' / 'pernah-canonical.json'

            with Storage(source_path) as db:
                source = db.add_source('manual', 'drill')
                person = db.add_entity('person', 'Rahayu')
                event = db.add_event('meeting', '2026-10-05T12:00:00Z', source_id=source)
                db.link_event_entity(event, person, role='participant')
                db.add_memory(memory_type='note', content='disaster recovery drill', source_id=source, confidence=1.0)
                expected = db.export_canonical()
                db.backup(backup_path)

            source_path.unlink()
            self.assertFalse(source_path.exists())

            Storage.restore(backup_path, source_path)
            with Storage(source_path) as recovered:
                self.assertEqual(recovered.export_canonical(), expected)
                self.assertEqual(recovered.list_memories()[0]['content'], 'disaster recovery drill')
                self.assertEqual(recovered._conn.execute('SELECT COUNT(*) FROM event_entities').fetchone()[0], 1)

    def test_corrupted_backup_cannot_complete_disaster_recovery(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            target = root / 'live.db'
            backup = root / 'backup.json'
            with Storage(target) as db:
                db.add_memory(memory_type='note', content='safe state', confidence=1.0)
                db.backup(backup)

            backup.write_text('{not valid json', encoding='utf-8')
            with self.assertRaises(ValidationError):
                Storage.restore(backup, target)

            with Storage(target) as intact:
                self.assertEqual(intact.list_memories()[0]['content'], 'safe state')

