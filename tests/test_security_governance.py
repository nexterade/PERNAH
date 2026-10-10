import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SecurityGovernanceTests(unittest.TestCase):
    def test_security_document_exists_and_defines_boundary(self):
        text = (ROOT / "docs" / "SECURITY.md").read_text(encoding="utf-8")
        for term in ["Normal Data", "Sensitive Data", "Secret Data", "Secret Vault"]:
            self.assertIn(term, text)
        self.assertIn("tidak boleh dihapus, dipangkas, atau dibuat kedaluwarsa secara otomatis", text)
        self.assertIn("tidak boleh disimpan plaintext sebagai Memory Core canonical data", text)

    def test_checkpoint_carries_security_boundary(self):
        text = (ROOT / "docs" / "CHECKPOINT.md").read_text(encoding="utf-8")
        self.assertIn("3.33.1 DATA CLASSIFICATION & PRIVACY BOUNDARY", text)
        self.assertIn("Source of truth untuk klasifikasi dan batas privasi adalah `docs/SECURITY.md`", text)

    def test_glossary_contains_security_terms_once(self):
        html = (ROOT / "docs" / "Glosarium.html").read_text(encoding="utf-8")
        match = re.search(r"const entries = (\[.*?\]);\s*const dict", html, re.S)
        self.assertIsNotNone(match)
        entries = json.loads(match.group(1))
        names = [entry[0].casefold() for entry in entries]
        for term in ["data classification", "normal data", "sensitive data", "secret data", "secret vault"]:
            self.assertEqual(names.count(term), 1, term)
        self.assertEqual(len(entries), 153)

    def test_web_backup_recovery_contract_is_explicit(self):
        checkpoint = (ROOT / "docs" / "CHECKPOINT.md").read_text(encoding="utf-8")
        for phrase in [
            "WEB BACKUP & RECOVERY CONTRACT",
            "Backup payloads MUST be validated",
            "Restore MUST require explicit confirmation",
            "`Storage.restore()` replacement contract",
            "localhost-only",
        ]:
            self.assertIn(phrase, checkpoint)

    def test_no_real_secret_examples_are_introduced(self):
        forbidden = ["-----BEGIN PRIVATE KEY-----", "sk-live-", "ghp_", "AKIA"]
        for rel in ["docs/SECURITY.md", "docs/CHECKPOINT.md", "README.md"]:
            text = (ROOT / rel).read_text(encoding="utf-8")
            for marker in forbidden:
                self.assertNotIn(marker, text)

    def test_security_doc_is_linked_in_continuity_state(self):
        state = json.loads((ROOT / "PERNAH_PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertIn("docs/SECURITY.md", state["source_of_truth"])
        self.assertIn("docs/SECURITY.md", state["mandatory_context"])


if __name__ == "__main__":
    unittest.main()
