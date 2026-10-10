import unittest

from pernah.ai_layer import (
    AnswerRequest, ExtractionRequest, InvalidProposal, ProviderUnavailable,
    UnconfiguredProvider, validate_answer, validate_extraction,
)


class AILayerContractTests(unittest.TestCase):
    def setUp(self):
        self.request = ExtractionRequest("Rahayu meminjam uang Rp200.000 tadi pagi.")
        self.raw = {
            "original_text": self.request.text,
            "normalized_text": "Rahayu meminjam uang Rp200.000 tadi pagi.",
            "intent": "record_transaction", "detected_language": "id", "confidence": 0.91,
            "entities": [{"type": "person", "name": "Rahayu"}],
            "event": {"type": "loan"},
            "transaction": {"amount": 200000, "currency": "IDR", "direction": "outgoing"},
            "relationships": [{"entity_name": "Rahayu", "relation_type": "counterparty"}],
        }

    def test_valid_proposal_is_candidate_not_memory_draft(self):
        result = validate_extraction(self.raw, self.request)
        self.assertEqual(result.proposal.original_text, self.request.text)
        self.assertFalse(result.requires_review)
        self.assertNotIn("memory_id", result.proposal.__dict__)

    def test_low_confidence_requires_review(self):
        raw = dict(self.raw, confidence=0.4)
        result = validate_extraction(raw, self.request)
        self.assertTrue(result.requires_review)
        self.assertIn("confidence_below_review_threshold", result.review_reasons)

    def test_original_input_must_match_exactly(self):
        with self.assertRaises(InvalidProposal):
            validate_extraction(dict(self.raw, original_text="changed"), self.request)

    def test_unknown_fields_are_rejected(self):
        with self.assertRaises(InvalidProposal):
            validate_extraction(dict(self.raw, execute_sql=True), self.request)

    def test_invalid_confidence_including_boolean_is_rejected(self):
        for value in (-0.1, 1.1, True, "0.9"):
            with self.subTest(value=value), self.assertRaises(InvalidProposal):
                validate_extraction(dict(self.raw, confidence=value), self.request)

    def test_transaction_without_event_is_rejected(self):
        with self.assertRaises(InvalidProposal):
            validate_extraction(dict(self.raw, event=None), self.request)

    def test_relationship_must_reference_declared_entity(self):
        raw = dict(self.raw, relationships=[{"entity_name": "Other", "relation_type": "counterparty"}])
        with self.assertRaises(InvalidProposal):
            validate_extraction(raw, self.request)

    def test_oversized_input_is_rejected(self):
        with self.assertRaises(ValueError):
            ExtractionRequest("x" * 20001)

    def test_default_provider_is_offline_and_actionable(self):
        provider = UnconfiguredProvider()
        with self.assertRaisesRegex(ProviderUnavailable, "deterministic normalize"):
            provider.extract(self.request)
        with self.assertRaisesRegex(ProviderUnavailable, "deterministic retrieval"):
            provider.answer(AnswerRequest("Apa yang gue catat?", ()))

    def test_answer_must_cite_supplied_canonical_memory(self):
        request = AnswerRequest("Apa yang terjadi?", ({"memory_id": "mem-1", "content": "Rahayu meminjam uang"},))
        answer = validate_answer({"text": "Rahayu meminjam uang.", "supporting_memory_ids": ["mem-1"], "evidence_sufficient": True}, request)
        self.assertEqual(answer.supporting_memory_ids, ("mem-1",))

    def test_answer_cannot_invent_evidence_reference(self):
        request = AnswerRequest("Apa yang terjadi?", ({"memory_id": "mem-1"},))
        with self.assertRaises(InvalidProposal):
            validate_answer({"text": "X", "supporting_memory_ids": ["mem-2"], "evidence_sufficient": True}, request)

    def test_insufficient_answer_requires_uncertainty_note(self):
        request = AnswerRequest("Apa yang terjadi?", ())
        with self.assertRaises(InvalidProposal):
            validate_answer({"text": "Tidak ditemukan.", "supporting_memory_ids": [], "evidence_sufficient": False}, request)


if __name__ == "__main__":
    unittest.main()
