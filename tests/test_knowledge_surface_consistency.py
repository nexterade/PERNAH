import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class KnowledgeSurfaceConsistencyTests(unittest.TestCase):
    def test_impact_policy_and_canonical_surfaces_are_present(self):
        checkpoint = (ROOT / "docs/CHECKPOINT.md").read_text(encoding="utf-8")
        self.assertIn("3.34.2 KNOWLEDGE-SURFACE IMPACT CHECK", checkpoint)
        for token in ["BOTH", "GLOSSARY", "CHRONICLE", "NONE", "Glossary menjawab", "Chronicle menjawab"]:
            self.assertIn(token, checkpoint)
        self.assertTrue((ROOT / "docs/Glosarium.html").is_file())
        self.assertTrue((ROOT / "docs/Creation-Chronicle.html").is_file())

    def test_new_governance_terms_are_documented_in_glossary(self):
        html = (ROOT / "docs/Glosarium.html").read_text(encoding="utf-8")
        match = re.search(r"const entries = (\[.*?\]);\s*const dict", html, re.S)
        self.assertIsNotNone(match)
        entries = json.loads(match.group(1))
        names = {entry[0].casefold() for entry in entries}
        for term in [
            "artifact compliance gate", "behavioral policy", "concise", "human touch",
            "integrity contract", "invariant", "knowledge-surface impact check",
            "policy propagation", "prompt translation", "raw idea", "release preflight",
            "trigger policy", "test discovery contract", "regression guard",
            "mixed-language boundary", "web backup & recovery", "explicit restore confirmation", "grounded answer", "insufficient evidence", "evidence minimization",
        ]:
            self.assertIn(term, names)

    def test_current_change_is_recorded_in_chronicle(self):
        chronicle = (ROOT / "docs/Creation-Chronicle.html").read_text(encoding="utf-8")
        self.assertIn('id="section-43"', chronicle)
        self.assertIn("v0.2.0-dev.59", chronicle)
        self.assertIn("Parent: v0.2.0-dev.58", chronicle)
        self.assertIn("WEB BACKUP &amp; RECOVERY", chronicle)

if __name__ == "__main__":
    unittest.main()
