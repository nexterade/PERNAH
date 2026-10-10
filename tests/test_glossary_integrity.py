import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY = ROOT / "docs" / "Glosarium.html"


class GlossaryIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = GLOSSARY.read_text(encoding="utf-8")
        match = re.search(r"const entries = (\[.*?\]);\s*\n\s*const dict", cls.html, re.S)
        if not match:
            raise AssertionError("canonical glossary entries array not found")
        cls.entries = json.loads(match.group(1))

    def test_entry_names_are_unique(self):
        names = [entry[0].casefold() for entry in self.entries]
        self.assertEqual(len(names), len(set(names)))

    def test_known_terms_are_data_entries(self):
        names = {entry[0] for entry in self.entries}
        name_list = [entry[0].casefold() for entry in self.entries]
        self.assertIn("Exact Search", names)
        self.assertIn("Deterministic Ranking", names)
        self.assertIn("Generated UI Duplication Guard", names)
        self.assertIn("Disaster Recovery", names)
        self.assertIn("Manual Input", names)
        self.assertIn("Input Interface", names)
        self.assertIn("Secret Vault", names)
        self.assertIn("Secret Data", names)
        self.assertIn("Web Backup & Recovery", names)
        self.assertIn("Explicit Restore Confirmation", names)
        self.assertIn("Atomic Ingestion", names)
        self.assertIn("Vocabulary", names)
        self.assertIn("Product Owner", names)
        self.assertIn("Failed to fetch", names)
        self.assertIn("python -m", names)
        self.assertIn("SPOK", names)
        self.assertEqual(name_list.count("web interface"), 1)

    def test_renderer_does_not_inject_known_global_blocks(self):
        render_match = re.search(r"function render\(\) \{(.*?)\n  \}\n\n  const themeToggle", self.html, re.S)
        self.assertIsNotNone(render_match)
        render_source = render_match.group(1)
        self.assertNotIn("Exact Search", render_source)
        self.assertNotIn("Deterministic Ranking", render_source)

    def test_glossary_has_expected_latest_size(self):
        self.assertEqual(len(self.entries), 165)

    def test_glossary_has_pernah_identity_without_cross_project_branding(self):
        self.assertIn("PERNAH", self.html)
        self.assertNotIn("Project Genesis", self.html)

    def test_mobile_sidebar_has_tap_outside_backdrop_contract(self):
        self.assertIn('id="sidebarBackdrop"', self.html)
        self.assertIn('class="sidebar-backdrop"', self.html)
        self.assertIn("sidebarBackdrop.addEventListener('click', closeSidebar)", self.html)
        self.assertIn("document.addEventListener('pointerdown'", self.html)
        self.assertIn("!sidebarIndex.contains(target)", self.html)
        self.assertIn('.layout.sidebar-open .sidebar-backdrop', self.html)

    def test_temporal_window_is_unique(self):
        names = [entry[0].casefold() for entry in self.entries]
        self.assertEqual(names.count("temporal window"), 1)

    def test_glossary_is_utf8_and_free_of_mojibake_markers(self):
        raw = GLOSSARY.read_bytes()
        decoded = raw.decode("utf-8")
        self.assertNotRegex(decoded, r"[\u0080-\u009f]")
        self.assertNotRegex(decoded, r"[\u00c2\u00c3\u00e2\u00f0][\u0080-\u00bf]{1,3}")
        self.assertNotIn("�", decoded)


if __name__ == "__main__":
    unittest.main()
