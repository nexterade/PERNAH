import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHRONICLE = ROOT / "docs" / "Creation-Chronicle.html"


class ChronicleIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = CHRONICLE.read_text(encoding="utf-8")

    def test_section_numbers_are_sequential_and_unique(self):
        headings = re.findall(r'<h[12] id="section-(\d+)">\s*(\d+)\.\s+', self.html)
        ids = [int(a) for a, _ in headings]
        numbers = [int(b) for _, b in headings]
        self.assertEqual(ids, list(range(len(ids))))
        self.assertEqual(numbers, list(range(len(numbers))))

    def test_numbered_milestone_headings_share_h1_style_and_divider(self):
        sections = list(re.finditer(r'<h([1-6]) id="section-(\d+)">(.*?)</h\1>', self.html))
        self.assertTrue(sections, "no section headings discovered")
        for index, match in enumerate(sections):
            level, section_id, title = match.group(1), int(match.group(2)), match.group(3)
            if section_id == 0:
                self.assertEqual(level, "2", "introductory Chronicle contract is intentionally h2")
                self.assertIn("CHRONICLE CONTRACT", title)
                continue
            self.assertEqual(level, "1", f"numbered milestone section {section_id} must use h1")
            prefix = self.html[max(0, match.start() - 16):match.start()]
            self.assertRegex(prefix, r'<hr\s*/?>\s*$', f"section {section_id} is missing its divider")
            self.assertTrue(title.strip(), f"section {section_id} has an empty heading")

        self.assertRegex(self.html, r'<h1 id="section-44">44\. ATOMIC INGESTION DAN CONTINUITY REPAIR')
        self.assertRegex(self.html, r'<h2 id="section-0">0\. CHRONICLE CONTRACT')

    def test_every_numbered_section_has_content_before_next_section(self):
        sections = list(re.finditer(r'<h[12] id="section-(\d+)">', self.html))
        for index, match in enumerate(sections):
            section_id = int(match.group(1))
            end = sections[index + 1].start() if index + 1 < len(sections) else self.html.find('<div class="no-results"', match.end())
            if end < 0:
                end = len(self.html)
            body = self.html[match.end():end]
            self.assertRegex(body, r'<(?:p|pre|ul|ol|div|table)\b', f"section {section_id} has no recognizable body content")

    def test_section_ids_are_unique(self):
        ids = re.findall(r'id="(section-\d+)"', self.html)
        self.assertEqual(len(ids), len(set(ids)))

    def test_chronicle_contract_is_present(self):
        self.assertIn("CHRONICLE CONTRACT", self.html)
        for phrase in (
            "Primary record",
            "Source discipline",
            "Chronology",
            "Current state",
            "CHANGELOG mencatat perubahan",
            "CHAT IS EPHEMERAL. ARTIFACT IS CONTINUOUS.",
        ):
            self.assertIn(phrase, self.html)

    def test_late_milestones_follow_release_chronology(self):
        order = [
            "MANUAL INPUT",
            "DOCUMENTATION &amp; ARTIFACT HYGIENE",
            "DATA CLASSIFICATION &amp; PRIVACY BOUNDARY",
            "FINAL NOTE — REFLECTION BEFORE THE WEB GATE",
            "LOCAL WEB INTERFACE",
            "CURRENT DOCUMENTED STATE — v0.2.0-dev.28",
        ]
        positions = [self.html.index(item) for item in order]
        self.assertEqual(positions, sorted(positions))

    def test_historical_snapshot_is_marked_as_historical(self):
        self.assertIn("HISTORICAL SNAPSHOT", self.html)
        self.assertRegex(self.html, r"milestone terakhir pada chronicle")
        self.assertNotIn("Latest documented artifact:\nPERNAH-v0.2.0-dev.24.zip", self.html)

    def test_toc_is_generated_from_current_headings(self):
        self.assertIn('id="toc"', self.html)
        self.assertIn("root.querySelectorAll('h1[id],h2[id]')", self.html)
        self.assertNotIn('<nav class="toc" id="toc"><a href="#section-', self.html)

    def test_toc_has_scroll_sync_and_active_item_contract(self):
        for marker in (
            "let activeSectionId=null;",
            "function setActiveSection(id)",
            "function syncActiveSection()",
            "window.addEventListener('scroll'",
            "setActiveSection(link.getAttribute('href').slice(1))",
            "nav.querySelectorAll('a.active')",
        ):
            self.assertIn(marker, self.html)

    def test_mobile_chronicle_sidebar_has_outside_close_contract(self):
        self.assertIn('id="sidebarBackdrop"', self.html)
        self.assertIn("sidebarBackdrop.addEventListener('click',closeSidebar)", self.html)
        self.assertIn("if(!sidebarIndex.contains(target)&&target!==sidebarToggle&&!sidebarToggle.contains(target))closeSidebar()", self.html)


if __name__ == "__main__":
    unittest.main()
