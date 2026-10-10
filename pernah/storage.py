from __future__ import annotations

import json
import sqlite3
import tempfile
import uuid
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 3

class ValidationError(ValueError):
    pass


def _id() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _validate_ts(value: str | None) -> str | None:
    if value is None:
        return None
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise ValidationError(f'invalid timestamp: {value}') from exc
    if dt.tzinfo is None:
        raise ValidationError('timestamp must include timezone')
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


class Storage:
    def __init__(self, path: str | Path = ':memory:'):
        self.path = str(path)
        self._conn = sqlite3.connect(self.path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute('PRAGMA foreign_keys = ON')
        self._initialize()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self._conn.rollback()
        else:
            self._conn.commit()
        self.close()

    def close(self):
        if getattr(self, '_conn', None) is not None:
            self._conn.close()
            self._conn = None

    @property
    def schema_version(self) -> int:
        row = self._conn.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()
        return int(row['value'])

    def _initialize(self):
        self._conn.executescript('''
        CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS sources (
            id TEXT PRIMARY KEY, source_type TEXT NOT NULL, reference TEXT, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS entities (
            id TEXT PRIMARY KEY, type TEXT NOT NULL, name TEXT NOT NULL,
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
            UNIQUE(type, name COLLATE NOCASE)
        );
        CREATE TABLE IF NOT EXISTS memories (
            id TEXT PRIMARY KEY, type TEXT NOT NULL, content TEXT NOT NULL,
            created_at TEXT NOT NULL, occurred_at TEXT, updated_at TEXT NOT NULL,
            source_id TEXT, confidence REAL NOT NULL, schema_version INTEGER NOT NULL,
            FOREIGN KEY(source_id) REFERENCES sources(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id TEXT PRIMARY KEY, from_entity TEXT NOT NULL, relation_type TEXT NOT NULL,
            to_entity TEXT NOT NULL, valid_from TEXT, valid_until TEXT,
            source_id TEXT, confidence REAL NOT NULL,
            FOREIGN KEY(from_entity) REFERENCES entities(id), FOREIGN KEY(to_entity) REFERENCES entities(id),
            FOREIGN KEY(source_id) REFERENCES sources(id)
        );
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY, type TEXT NOT NULL, occurred_at TEXT,
            location_id TEXT, source_id TEXT,
            FOREIGN KEY(location_id) REFERENCES entities(id), FOREIGN KEY(source_id) REFERENCES sources(id)
        );
        CREATE TABLE IF NOT EXISTS event_entities (
            event_id TEXT NOT NULL, entity_id TEXT NOT NULL, role TEXT,
            PRIMARY KEY(event_id, entity_id, role),
            FOREIGN KEY(event_id) REFERENCES events(id) ON DELETE CASCADE,
            FOREIGN KEY(entity_id) REFERENCES entities(id)
        );
        CREATE TABLE IF NOT EXISTS commitments (
            id TEXT PRIMARY KEY, action TEXT NOT NULL, person_id TEXT,
            deadline TEXT, status TEXT NOT NULL DEFAULT 'open', source_id TEXT,
            FOREIGN KEY(person_id) REFERENCES entities(id), FOREIGN KEY(source_id) REFERENCES sources(id)
        );
        CREATE TABLE IF NOT EXISTS decisions (
            id TEXT PRIMARY KEY, decision TEXT NOT NULL, reason TEXT,
            occurred_at TEXT, source_id TEXT,
            FOREIGN KEY(source_id) REFERENCES sources(id)
        );
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY, amount INTEGER NOT NULL, currency TEXT NOT NULL,
            direction TEXT NOT NULL, occurred_at TEXT, category TEXT,
            event_id TEXT, person_id TEXT, source_id TEXT,
            FOREIGN KEY(event_id) REFERENCES events(id), FOREIGN KEY(person_id) REFERENCES entities(id),
            FOREIGN KEY(source_id) REFERENCES sources(id)
        );
        CREATE INDEX IF NOT EXISTS idx_memories_content ON memories(content);
        CREATE INDEX IF NOT EXISTS idx_events_occurred_at ON events(occurred_at);
        CREATE INDEX IF NOT EXISTS idx_transactions_occurred_at ON transactions(occurred_at);
        ''')
        row = self._conn.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()
        if row is None:
            self._conn.execute("INSERT INTO metadata(key,value) VALUES('schema_version',?)", (str(SCHEMA_VERSION),))
        elif int(row['value']) != SCHEMA_VERSION:
            raise RuntimeError(f'unsupported schema version {row["value"]}; expected {SCHEMA_VERSION}')
        self._conn.commit()

    def add_source(self, source_type: str, reference: str | None = None, source_id: str | None = None) -> str:
        sid = source_id or _id()
        self._conn.execute('INSERT INTO sources(id,source_type,reference,created_at) VALUES(?,?,?,?)', (sid, source_type, reference, _now()))
        return sid

    def add_memory(self, memory_type: str, content: str, source_id: str | None = None,
                   confidence: float = 1.0, occurred_at: str | None = None,
                   memory_id: str | None = None) -> str:
        if not 0 <= confidence <= 1:
            raise ValidationError('confidence must be between 0 and 1')
        mid = memory_id or _id(); now = _now()
        self._conn.execute('''INSERT INTO memories(id,type,content,created_at,occurred_at,updated_at,source_id,confidence,schema_version)
                              VALUES(?,?,?,?,?,?,?,?,?)''',
                           (mid, memory_type, content, now, _validate_ts(occurred_at), now, source_id, confidence, SCHEMA_VERSION))
        return mid

    def get_memory(self, memory_id: str):
        row = self._conn.execute('SELECT * FROM memories WHERE id=?', (memory_id,)).fetchone()
        return dict(row) if row else None

    def list_memories(self):
        return [dict(r) for r in self._conn.execute('SELECT * FROM memories ORDER BY created_at, id')]

    def add_entity(self, entity_type: str, name: str, entity_id: str | None = None) -> str:
        existing = self._conn.execute('SELECT id FROM entities WHERE type=? AND name=? COLLATE NOCASE', (entity_type, name)).fetchone()
        if existing:
            return existing['id']
        eid = entity_id or _id(); now = _now()
        self._conn.execute('INSERT INTO entities(id,type,name,created_at,updated_at) VALUES(?,?,?,?,?)', (eid, entity_type, name.strip(), now, now))
        return eid

    def find_entity(self, name: str, entity_type: str | None = None):
        if entity_type:
            row = self._conn.execute('SELECT * FROM entities WHERE type=? AND name=? COLLATE NOCASE', (entity_type, name)).fetchone()
        else:
            row = self._conn.execute('SELECT * FROM entities WHERE name=? COLLATE NOCASE ORDER BY id LIMIT 1', (name,)).fetchone()
        return dict(row) if row else None

    def add_relationship(self, from_entity: str, relation_type: str, to_entity: str,
                         valid_from: str | None = None, valid_until: str | None = None,
                         source_id: str | None = None, confidence: float = 1.0) -> str:
        if not 0 <= confidence <= 1: raise ValidationError('confidence must be between 0 and 1')
        vf, vu = _validate_ts(valid_from), _validate_ts(valid_until)
        if vf and vu and vf > vu: raise ValidationError('valid_from cannot be after valid_until')
        existing = self._conn.execute('''SELECT id FROM relationships
            WHERE from_entity=? AND relation_type=? AND to_entity=? AND valid_from IS ? AND valid_until IS ?''',
            (from_entity, relation_type, to_entity, vf, vu)).fetchone()
        if existing: return existing['id']
        rid = _id()
        self._conn.execute('INSERT INTO relationships VALUES(?,?,?,?,?,?,?,?)', (rid, from_entity, relation_type, to_entity, vf, vu, source_id, confidence))
        return rid

    def add_location_state(self, object_entity: str, location_entity: str, valid_from: str, source_id: str | None = None, confidence: float = 1.0) -> str:
        return self.add_relationship(object_entity, 'located_at', location_entity, valid_from=valid_from, source_id=source_id, confidence=confidence)

    def close_location_state(self, relationship_id: str, valid_until: str):
        self._conn.execute('UPDATE relationships SET valid_until=? WHERE id=?', (_validate_ts(valid_until), relationship_id))

    def latest_location(self, object_entity: str):
        row = self._conn.execute('''SELECT r.*, e.name AS location_name FROM relationships r
            JOIN entities e ON e.id=r.to_entity WHERE r.from_entity=? AND r.relation_type='located_at'
            ORDER BY r.valid_from DESC, r.id DESC LIMIT 1''', (object_entity,)).fetchone()
        return dict(row) if row else None

    def add_event(self, event_type: str, occurred_at: str | None = None, location_id: str | None = None, source_id: str | None = None, event_id: str | None = None) -> str:
        eid = event_id or _id()
        self._conn.execute('INSERT INTO events(id,type,occurred_at,location_id,source_id) VALUES(?,?,?,?,?)', (eid, event_type, _validate_ts(occurred_at), location_id, source_id))
        return eid

    def link_event_entity(self, event_id: str, entity_id: str, role: str | None = None):
        self._conn.execute('INSERT OR IGNORE INTO event_entities(event_id,entity_id,role) VALUES(?,?,?)', (event_id, entity_id, role))

    def add_commitment(self, action: str, person_id: str | None = None, deadline: str | None = None, source_id: str | None = None, status: str = 'open', commitment_id: str | None = None) -> str:
        cid = commitment_id or _id()
        self._conn.execute('INSERT INTO commitments(id,action,person_id,deadline,status,source_id) VALUES(?,?,?,?,?,?)', (cid, action, person_id, _validate_ts(deadline), status, source_id))
        return cid

    def add_decision(self, decision: str, reason: str | None = None, occurred_at: str | None = None, source_id: str | None = None, decision_id: str | None = None) -> str:
        did = decision_id or _id()
        self._conn.execute('INSERT INTO decisions(id,decision,reason,occurred_at,source_id) VALUES(?,?,?,?,?)', (did, decision, reason, _validate_ts(occurred_at), source_id))
        return did

    def add_transaction(self, amount: int, currency: str = 'IDR', direction: str = 'expense', occurred_at: str | None = None,
                        category: str | None = None, event_id: str | None = None, person_id: str | None = None,
                        source_id: str | None = None, transaction_id: str | None = None) -> str:
        if amount < 0: raise ValidationError('amount cannot be negative')
        tid = transaction_id or _id()
        self._conn.execute('INSERT INTO transactions(id,amount,currency,direction,occurred_at,category,event_id,person_id,source_id) VALUES(?,?,?,?,?,?,?,?,?)',
                           (tid, amount, currency, direction, _validate_ts(occurred_at), category, event_id, person_id, source_id))
        return tid

    def find_purchase_events(self, entity_name: str | None = None, occurred_after: str | None = None, occurred_before: str | None = None):
        clauses = ["e.type='purchase'", "t.direction='expense'"]
        params: list[Any] = []
        if entity_name:
            clauses.append("EXISTS (SELECT 1 FROM event_entities ee2 JOIN entities en2 ON en2.id=ee2.entity_id WHERE ee2.event_id=e.id AND en2.name=? COLLATE NOCASE)")
            params.append(entity_name)
        if occurred_after:
            clauses.append('e.occurred_at >= ?'); params.append(_validate_ts(occurred_after))
        if occurred_before:
            clauses.append('e.occurred_at <= ?'); params.append(_validate_ts(occurred_before))
        sql = '''SELECT t.id AS transaction_id, t.amount, t.currency, t.direction, e.id AS event_id, e.occurred_at,
                        en.name AS entity_name, en.type AS entity_type
                 FROM events e JOIN transactions t ON t.event_id=e.id
                 JOIN event_entities ee ON ee.event_id=e.id JOIN entities en ON en.id=ee.entity_id
                 WHERE ''' + ' AND '.join(clauses) + ' ORDER BY e.occurred_at, t.id'
        return [dict(r) for r in self._conn.execute(sql, params)]

    def find_entity_events(self, entity_name: str, relation_type: str | None = None,
                           occurred_after: str | None = None, occurred_before: str | None = None):
        entity = self.find_entity(entity_name)
        if not entity:
            return []
        clauses = [
            'EXISTS (SELECT 1 FROM event_entities ee2 WHERE ee2.event_id=e.id AND ee2.entity_id=?)'
        ]
        params: list[Any] = [entity['id']]
        if relation_type:
            clauses.append('EXISTS (SELECT 1 FROM event_entities ee3 WHERE ee3.event_id=e.id AND ee3.entity_id=? AND ee3.role=?)')
            params.extend([entity['id'], relation_type])
        if occurred_after:
            clauses.append('e.occurred_at >= ?'); params.append(_validate_ts(occurred_after))
        if occurred_before:
            clauses.append('e.occurred_at <= ?'); params.append(_validate_ts(occurred_before))
        rows = self._conn.execute('''SELECT e.id AS event_id, e.type AS event_type, e.occurred_at,
                                            e.location_id, loc.name AS location_name, e.source_id,
                                            (SELECT ee4.role FROM event_entities ee4
                                             WHERE ee4.event_id=e.id AND ee4.entity_id=?
                                             ORDER BY ee4.role LIMIT 1) AS matched_role
                                     FROM events e
                                     LEFT JOIN entities loc ON loc.id=e.location_id
                                     WHERE ''' + ' AND '.join(clauses) + '''
                                     ORDER BY e.occurred_at IS NULL, e.occurred_at ASC, e.id ASC''',
                                   [entity['id'], *params]).fetchall()
        return [dict(r) for r in rows]

    def event_entities(self, event_id: str):
        rows = self._conn.execute('''SELECT en.id, en.type, en.name, ee.role
                                     FROM event_entities ee
                                     JOIN entities en ON en.id=ee.entity_id
                                     WHERE ee.event_id=?
                                     ORDER BY en.type, en.name COLLATE NOCASE, ee.role''', (event_id,)).fetchall()
        return [dict(r) for r in rows]

    def event_memories(self, event_id: str):
        row = self._conn.execute('SELECT source_id FROM events WHERE id=?', (event_id,)).fetchone()
        if not row or not row['source_id']:
            return []
        rows = self._conn.execute('''SELECT id, type, content, occurred_at, confidence
                                     FROM memories WHERE source_id=?
                                     ORDER BY created_at, id''', (row['source_id'],)).fetchall()
        return [dict(r) for r in rows]

    def exact_search(self, text: str, limit: int = 50):
        q = text.strip()
        if not q: return []
        like = f'%{q}%'
        rows = self._conn.execute('''SELECT id,type,content,occurred_at,confidence FROM memories
                                     WHERE content LIKE ? ORDER BY occurred_at DESC, created_at DESC LIMIT ?''', (like, limit)).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def _canonical_tables():
        return ['sources','entities','memories','relationships','events','event_entities','commitments','decisions','transactions']

    def export_canonical(self):
        tables = self._canonical_tables()
        payload = {'format': 'pernah-canonical-v1', 'schema_version': SCHEMA_VERSION}
        for table in tables:
            columns = [r['name'] for r in self._conn.execute(f'PRAGMA table_info({table})')]
            order = ', '.join(f'"{column}"' for column in columns)
            rows = self._conn.execute(f'SELECT * FROM {table} ORDER BY {order}').fetchall()
            payload[table] = [dict(r) for r in rows]
        return payload

    def export_json(self, path: str | Path):
        """Atomically write the current canonical state as portable JSON."""
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(self.export_canonical(), ensure_ascii=False, indent=2)
        fd, temp_name = tempfile.mkstemp(prefix=f'.{target.name}.export-', suffix='.json', dir=target.parent)
        os.close(fd)
        temp_path = Path(temp_name)
        try:
            temp_path.write_text(payload, encoding='utf-8')
            os.replace(temp_path, target)
        except Exception:
            if temp_path.exists():
                temp_path.unlink()
            raise
        return target

    def backup(self, path: str | Path):
        """Write the current canonical state to a portable local backup artifact."""
        return self.export_json(path)

    @classmethod
    def _validate_canonical_payload(cls, payload: Any):
        if not isinstance(payload, dict):
            raise ValidationError('canonical payload must be an object')
        expected = {'format', 'schema_version', *cls._canonical_tables()}
        if set(payload) != expected:
            missing = sorted(expected - set(payload))
            extra = sorted(set(payload) - expected)
            detail = []
            if missing:
                detail.append(f'missing keys: {", ".join(missing)}')
            if extra:
                detail.append(f'unexpected keys: {", ".join(extra)}')
            raise ValidationError('invalid canonical payload structure' + (f' ({"; ".join(detail)})' if detail else ''))
        if payload.get('format') != 'pernah-canonical-v1':
            raise ValidationError('unsupported export format')
        try:
            schema_version = int(payload.get('schema_version'))
        except (TypeError, ValueError) as exc:
            raise ValidationError('invalid schema version') from exc
        if schema_version != SCHEMA_VERSION:
            raise ValidationError('unsupported schema version')

        schema = cls(':memory:')
        try:
            for table in cls._canonical_tables():
                rows = payload[table]
                if not isinstance(rows, list):
                    raise ValidationError(f'{table} must be a list')
                expected_columns = {r['name'] for r in schema._conn.execute(f'PRAGMA table_info({table})')}
                for row in rows:
                    if not isinstance(row, dict) or set(row) != expected_columns:
                        raise ValidationError(f'invalid row structure in {table}')
        finally:
            schema.close()
        timestamp_fields = {
            'sources': ['created_at'],
            'entities': ['created_at', 'updated_at'],
            'memories': ['created_at', 'occurred_at', 'updated_at'],
            'relationships': ['valid_from', 'valid_until'],
            'events': ['occurred_at'],
            'commitments': ['deadline'],
            'decisions': ['occurred_at'],
            'transactions': ['occurred_at'],
        }
        for table, fields in timestamp_fields.items():
            for row in payload[table]:
                for field in fields:
                    _validate_ts(row[field])
        for row in payload['memories']:
            if row['schema_version'] != SCHEMA_VERSION:
                raise ValidationError('memory row has unsupported schema version')
            if not 0 <= row['confidence'] <= 1:
                raise ValidationError('memory confidence must be between 0 and 1')
        for row in payload['relationships']:
            if not 0 <= row['confidence'] <= 1:
                raise ValidationError('relationship confidence must be between 0 and 1')
            if row['valid_from'] and row['valid_until'] and row['valid_from'] > row['valid_until']:
                raise ValidationError('relationship valid_from cannot be after valid_until')
        for row in payload['transactions']:
            if row['amount'] < 0:
                raise ValidationError('transaction amount cannot be negative')

        return True

    @classmethod
    def _read_backup(cls, path: str | Path):
        target = Path(path)
        if not target.is_file():
            raise ValidationError(f'backup file not found: {target}')
        try:
            payload = json.loads(target.read_text(encoding='utf-8'))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ValidationError(f'invalid backup JSON: {target}') from exc
        cls._validate_canonical_payload(payload)
        return payload

    @classmethod
    def _validate_relational_payload(cls, payload: dict):
        # Relational validation happens in an isolated in-memory SQLite database.
        with cls(':memory:') as temp:
            try:
                temp._insert_canonical(payload, ignore_conflicts=False)
            except sqlite3.IntegrityError as exc:
                raise ValidationError(f'canonical relational integrity failed: {exc}') from exc

    @classmethod
    def validate_backup(cls, path: str | Path):
        """Validate a local canonical backup without mutating project storage."""
        payload = cls._read_backup(path)
        cls._validate_relational_payload(payload)
        return True

    @classmethod
    def restore(cls, backup_path: str | Path, target_path: str | Path):
        """Atomically replace a target database with a validated canonical backup."""
        backup = Path(backup_path).resolve()
        target = Path(target_path).resolve()
        if backup == target:
            raise ValidationError('backup and restore target must be different paths')

        payload = cls._read_backup(backup)
        parent = target.parent
        parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(prefix=f'.{target.name}.restore-', suffix='.db', dir=parent)
        os.close(fd)
        temp_path = Path(temp_name)
        try:
            with cls(temp_path) as restored:
                try:
                    restored._insert_canonical(payload, ignore_conflicts=False)
                    restored._conn.commit()
                except sqlite3.IntegrityError as exc:
                    raise ValidationError(f'restore relational integrity failed: {exc}') from exc
                if restored.export_canonical() != payload:
                    raise ValidationError('restored canonical state does not match backup')
            os.replace(temp_path, target)
        except Exception:
            if temp_path.exists():
                temp_path.unlink()
            raise
        return target

    def _insert_canonical(self, payload: dict, ignore_conflicts: bool = True):
        for table in self._canonical_tables():
            columns = [r['name'] for r in self._conn.execute(f'PRAGMA table_info({table})')]
            placeholders = ','.join('?' for _ in columns)
            verb = 'INSERT OR IGNORE' if ignore_conflicts else 'INSERT'
            for row in payload[table]:
                vals = [row[c] for c in columns]
                self._conn.execute(
                    f'{verb} INTO {table}({",".join(columns)}) VALUES({placeholders})',
                    vals,
                )

    def import_json(self, path: str | Path):
        """Validate and import a portable canonical JSON artifact into this storage."""
        payload = self._read_backup(path)
        self._validate_relational_payload(payload)
        self.import_canonical(payload)
        return self

    def import_canonical(self, payload: dict):
        self._validate_canonical_payload(payload)
        self._validate_relational_payload(payload)
        self._conn.execute('BEGIN')
        try:
            self._insert_canonical(payload, ignore_conflicts=True)
            self._conn.commit()
        except Exception:
            self._conn.rollback(); raise
