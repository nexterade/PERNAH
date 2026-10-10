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

class ExtractionOrchestrationTests(unittest.TestCase):
    def setUp(self):
        from pernah.ai_layer import ExtractionRequest
        self.request = ExtractionRequest("Gue beli laptop baru kemarin.")
        self.raw = {
            "original_text": self.request.text,
            "normalized_text": self.request.text,
            "intent": "record_event", "detected_language": "id", "confidence": 0.91,
            "entities": [], "event": {"type": "purchase"},
            "transaction": None, "relationships": [],
        }

    def test_missing_provider_uses_deterministic_normalize(self):
        from pernah.ai_layer import orchestrate_extraction
        from pernah.memory_engine import normalize
        result = orchestrate_extraction(self.request.text)
        self.assertEqual(result.mode, "deterministic")
        self.assertEqual(result.draft, normalize(self.request.text))
        self.assertEqual(result.fallback_reason, "provider_not_configured")

    def test_valid_provider_proposal_is_advisory_only(self):
        from pernah.ai_layer import orchestrate_extraction
        class FakeProvider:
            name = "fake"
            def extract(self, request): return dict(self.raw)
            def answer(self, request): raise AssertionError("not used")
        provider = FakeProvider()
        provider.raw = dict(self.raw)
        result = orchestrate_extraction(self.request.text, provider)
        self.assertEqual(result.mode, "deterministic_with_candidate")
        self.assertIsNotNone(result.provider_candidate)
        self.assertEqual(result.draft.original_text, self.request.text)
        self.assertFalse(hasattr(result.provider_candidate.proposal, "memory_id"))

    def test_low_confidence_provider_candidate_requires_review(self):
        from pernah.ai_layer import orchestrate_extraction
        class FakeProvider:
            name = "fake"
            def extract(self, request): return dict(self.raw, confidence=0.2)
            def answer(self, request): raise AssertionError("not used")
        provider = FakeProvider()
        provider.raw = dict(self.raw)
        result = orchestrate_extraction(self.request.text, provider)
        self.assertEqual(result.mode, "deterministic_review_required")
        self.assertTrue(result.provider_candidate.requires_review)
        self.assertEqual(result.draft.original_text, self.request.text)

    def test_invalid_provider_output_falls_back_without_leaking_message(self):
        from pernah.ai_layer import orchestrate_extraction
        class FakeProvider:
            name = "fake"
            def extract(self, request): raise RuntimeError("secret-token-should-not-leak")
            def answer(self, request): raise AssertionError("not used")
        result = orchestrate_extraction(self.request.text, FakeProvider())
        self.assertEqual(result.mode, "deterministic_fallback")
        self.assertEqual(result.fallback_reason, "provider_error:RuntimeError")
        self.assertNotIn("secret-token", result.fallback_reason)
        self.assertEqual(result.draft.original_text, self.request.text)

    def test_malformed_provider_output_falls_back(self):
        from pernah.ai_layer import orchestrate_extraction
        class FakeProvider:
            name = "fake"
            def extract(self, request): return {"original_text": "forged"}
            def answer(self, request): raise AssertionError("not used")
        result = orchestrate_extraction(self.request.text, FakeProvider())
        self.assertEqual(result.mode, "deterministic_fallback")
        self.assertEqual(result.fallback_reason, "InvalidProposal")


class RetrievalOrchestrationTests(unittest.TestCase):
    def test_missing_provider_keeps_deterministic_results(self):
        from pernah.ai_layer import orchestrate_retrieval
        class DB:
            def exact_search(self, text):
                return [{"memory_id": "m1", "content": "Rahayu meminjam Rp200.000"}]
            def list_memories(self):
                return [{"id": "m1", "content": "Rahayu meminjam Rp200.000", "created_at": "2026-01-01T00:00:00Z"}]
        result = orchestrate_retrieval(DB(), "Rahayu meminjam Rp200.000")
        self.assertEqual(result.mode, "deterministic")
        self.assertEqual(result.evidence[0]["memory_id"], "m1")
        self.assertEqual(result.fallback_reason, "provider_not_configured")

    def test_provider_sees_only_deterministic_canonical_evidence(self):
        from pernah.ai_layer import orchestrate_retrieval
        class DB:
            def exact_search(self, text):
                return [{"memory_id": "m1", "content": "Catatan canonical"}]
            def list_memories(self):
                return [{"id": "m1", "content": "Catatan canonical", "created_at": "2026-01-01T00:00:00Z"}]
        class Provider:
            def answer(self, request):
                self.request = request
                return {"text": "Catatan ditemukan.", "supporting_memory_ids": ["m1"], "evidence_sufficient": True}
        provider = Provider()
        result = orchestrate_retrieval(DB(), "Apa catatannya?", provider)
        self.assertEqual(result.mode, "deterministic_with_grounded_candidate")
        self.assertEqual([e["memory_id"] for e in provider.request.evidence], ["m1"])
        self.assertEqual(result.answer_candidate.supporting_memory_ids, ("m1",))

    def test_no_evidence_never_calls_provider(self):
        from pernah.ai_layer import orchestrate_retrieval
        class DB:
            def exact_search(self, text): return []
            def list_memories(self): return []
        class Provider:
            def answer(self, request): raise AssertionError("must not call provider without evidence")
        result = orchestrate_retrieval(DB(), "Apa yang gue catat?", Provider())
        self.assertEqual(result.mode, "deterministic_no_evidence")
        self.assertEqual(result.fallback_reason, "no_canonical_evidence")

    def test_provider_failure_falls_back_without_leaking_exception(self):
        from pernah.ai_layer import orchestrate_retrieval
        class DB:
            def exact_search(self, text): return [{"memory_id": "m1", "content": "Catatan"}]
            def list_memories(self): return [{"id": "m1", "content": "Catatan", "created_at": "2026-01-01T00:00:00Z"}]
        class Provider:
            def answer(self, request): raise RuntimeError("private-api-key")
        result = orchestrate_retrieval(DB(), "Apa catatannya?", Provider())
        self.assertEqual(result.mode, "deterministic_fallback")
        self.assertNotIn("private-api-key", result.fallback_reason)
        self.assertEqual(result.evidence[0]["memory_id"], "m1")

    def test_event_result_resolves_to_linked_canonical_memory(self):
        from pernah.ai_layer import orchestrate_retrieval
        class DB:
            def exact_search(self, text): return []
            def find_purchase_events(self, **kwargs):
                return [{"event_id": "event-1", "transaction_id": "tx-1", "amount": 200000, "entity_name": "Laptop"}]
            def event_memories(self, event_id):
                self.requested_event = event_id
                return [{"id": "mem-1", "type": "event", "content": "Gue beli laptop seharga Rp200.000", "occurred_at": "2026-01-01T00:00:00Z"}]
        class Provider:
            def answer(self, request):
                self.request = request
                return {"text": "Ada catatan pembelian laptop.", "supporting_memory_ids": ["mem-1"], "evidence_sufficient": True}
        db, provider = DB(), Provider()
        result = orchestrate_retrieval(db, "Pernah beli laptop?", provider)
        self.assertEqual(db.requested_event, "event-1")
        self.assertEqual(result.evidence[0]["memory_id"], "mem-1")
        self.assertEqual(result.evidence[0]["matched_event_id"], "event-1")
        self.assertNotIn("transaction_id", provider.request.evidence[0])

    def test_event_without_linked_memory_is_not_evidence(self):
        from pernah.ai_layer import orchestrate_retrieval
        class DB:
            def exact_search(self, text): return []
            def find_purchase_events(self, **kwargs):
                return [{"event_id": "event-orphan", "transaction_id": "tx-1", "amount": 200000}]
            def event_memories(self, event_id): return []
        class Provider:
            def answer(self, request): raise AssertionError("unlinked event must not reach provider")
        result = orchestrate_retrieval(DB(), "Pernah beli laptop?", Provider())
        self.assertEqual(result.mode, "deterministic_no_evidence")
        self.assertEqual(result.evidence, ())

    def test_memory_rows_without_content_are_not_evidence(self):
        from pernah.ai_layer import orchestrate_retrieval
        class DB:
            def exact_search(self, text): return [{"id": "mem-1", "type": "note"}]
        result = orchestrate_retrieval(DB(), "catatan")
        self.assertEqual(result.evidence, ())

    def test_retrieval_limit_is_bounded(self):
        from pernah.ai_layer import orchestrate_retrieval
        class DB:
            def exact_search(self, text): return []
        for limit in (0, 51, True):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                orchestrate_retrieval(DB(), "tes", limit=limit)

class GroundedAnswerRefinementTests(unittest.TestCase):
    def test_insufficient_answer_requires_nonblank_uncertainty_note(self):
        from pernah.ai_layer import AnswerRequest, InvalidProposal, validate_answer
        request = AnswerRequest("Apa yang terjadi?", ({"memory_id": "mem-1", "content": "Catatan"},))
        for note in (None, "", "   "):
            with self.subTest(note=note), self.assertRaises(InvalidProposal):
                validate_answer({
                    "text": "Buktinya belum cukup.", "supporting_memory_ids": [],
                    "evidence_sufficient": False, "uncertainty_note": note,
                }, request)

    def test_insufficient_answer_is_preserved_with_refinement_guidance(self):
        from pernah.ai_layer import orchestrate_retrieval
        class DB:
            def exact_search(self, text):
                return [{"id": "m1", "content": "Catatan singkat", "private_metadata": "must-not-leak"}]
            def list_memories(self):
                return [{"id": "m1", "content": "Catatan singkat", "private_metadata": "must-not-leak"}]
        class Provider:
            def answer(self, request):
                return {
                    "text": "Catatan ini belum cukup untuk menjawab detailnya.",
                    "supporting_memory_ids": [], "evidence_sufficient": False,
                    "uncertainty_note": "Catatan yang ditemukan tidak memuat detail yang ditanyakan.",
                }
        result = orchestrate_retrieval(DB(), "Detailnya apa?", Provider())
        self.assertEqual(result.mode, "deterministic_review_required")
        self.assertEqual(result.fallback_reason, "evidence_insufficient")
        self.assertIsNotNone(result.answer_candidate)
        self.assertFalse(result.answer_candidate.evidence_sufficient)
        self.assertTrue(result.refinement_suggestions)

    def test_provider_evidence_is_minimized_and_drops_unrelated_fields(self):
        from pernah.ai_layer import orchestrate_retrieval
        class DB:
            def exact_search(self, text):
                return [{
                    "id": "m1", "content": "Catatan canonical", "created_at": "2026-01-01T00:00:00Z",
                    "secret_token": "do-not-forward", "attachment_bytes": b"private-image",
                    "internal_notes": "not for provider", "source_type": "manual",
                }]
            def list_memories(self):
                return [{
                    "id": "m1", "content": "Catatan canonical", "created_at": "2026-01-01T00:00:00Z",
                    "secret_token": "do-not-forward", "attachment_bytes": b"private-image",
                    "internal_notes": "not for provider", "source_type": "manual",
                }]
        class Provider:
            def answer(self, request):
                self.evidence = request.evidence
                return {"text": "Catatan ditemukan.", "supporting_memory_ids": ["m1"], "evidence_sufficient": True}
        provider = Provider()
        result = orchestrate_retrieval(DB(), "Apa catatannya?", provider)
        self.assertEqual(result.mode, "deterministic_with_grounded_candidate")
        self.assertEqual(set(provider.evidence[0]), {"memory_id", "content", "created_at", "source_type"})
        self.assertNotIn("secret_token", provider.evidence[0])
        self.assertNotIn("attachment_bytes", provider.evidence[0])
        self.assertNotIn("internal_notes", provider.evidence[0])

    def test_no_evidence_returns_deterministic_refinement_suggestions_without_provider_call(self):
        from pernah.ai_layer import orchestrate_retrieval
        class DB:
            def exact_search(self, text): return []
            def list_memories(self): return []
        class Provider:
            def answer(self, request): raise AssertionError("must not be called without evidence")
        result = orchestrate_retrieval(DB(), "Laptop?", Provider())
        self.assertEqual(result.mode, "deterministic_no_evidence")
        self.assertGreaterEqual(len(result.refinement_suggestions), 2)
        self.assertLessEqual(len(result.refinement_suggestions), 3)
        self.assertTrue(all(isinstance(item, str) and item.strip() for item in result.refinement_suggestions))
