import unittest
from datetime import datetime, timezone

from pernah.memory_engine import detect_language, normalize

REF = datetime(2026, 10, 5, 2, 0, tzinfo=timezone.utc)


class MemoryEngineRegressionTests(unittest.TestCase):
    def test_sundanese_purchase_normalization(self):
        draft = normalize("Urang geus meli laptop hargana 2 jt tadi isuk", reference_time=REF)
        self.assertEqual(draft.detected_language, "su")
        self.assertEqual(draft.intent, "record_purchase")
        self.assertEqual(draft.entities, [{"type": "object", "name": "laptop"}])
        self.assertEqual(draft.transaction["amount"], 2_000_000)
        self.assertEqual(draft.occurred_at, "2026-10-05T07:00:00Z")
        self.assertTrue(draft.original_text.startswith("Urang geus"))

    def test_sundanese_retrieval_query(self):
        draft = normalize("Urang pernah meli laptop can nya?", reference_time=REF)
        self.assertEqual(draft.detected_language, "su")
        self.assertEqual(draft.intent, "temporal_retrieval")
        self.assertEqual(
            draft.query,
            {
                "action": "purchase",
                "temporal": "past",
                "text": "Urang pernah meli laptop can nya?",
                "entity": "laptop",
            },
        )

    def test_language_detection_mixed_input(self):
        self.assertEqual(detect_language("Urang pernah beli laptop teu?"), "su")
        self.assertEqual(detect_language("Gue pernah beli laptop gak?"), "id")


if __name__ == "__main__":
    unittest.main()
