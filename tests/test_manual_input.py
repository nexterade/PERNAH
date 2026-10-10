from datetime import datetime, timezone
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pernah import Storage, capture_text

REF = datetime(2026, 10, 6, 2, 0, tzinfo=timezone.utc)


class ManualInputTests(unittest.TestCase):
    def test_capture_text_preserves_original_input_and_ingests(self):
        text = "Passport ada di laci meja."
        with Storage() as db:
            captured = capture_text(db, text, reference_time=REF)
            self.assertEqual(captured["draft"].original_text, text)
            self.assertEqual(captured["draft"].source_type, "manual")
            self.assertEqual(db.get_memory(captured["result"]["memory_id"])["content"], text)

    def test_capture_text_rejects_blank_input(self):
        with Storage() as db:
            with self.assertRaises(ValueError):
                capture_text(db, "   ")

    def test_capture_text_uses_existing_normalization_and_relative_time(self):
        with Storage() as db:
            captured = capture_text(db, "Gue ketemu Rahayu kemarin.", reference_time=REF)
            self.assertEqual(captured["draft"].intent, "record_event")
            self.assertEqual(captured["draft"].occurred_at, "2026-10-05T02:00:00Z")
            self.assertIsNotNone(captured["result"]["event_id"])

    def test_manual_cli_captures_to_file_database(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "pernah.db"
            cmd = [
                sys.executable,
                "-m",
                "pernah.manual",
                "--db",
                str(db_path),
                "--text",
                "Catatan manual bro",
                "--json",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["intent"], "capture_memory")
            self.assertTrue(payload["result"]["memory_id"])
            with Storage(db_path) as db:
                self.assertEqual(db.list_memories()[0]["content"], "Catatan manual bro")


if __name__ == "__main__":
    unittest.main()
