import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
CHRONICLE = ROOT / "docs" / "Creation-Chronicle.html"
GLOSSARY = ROOT / "docs" / "Glosarium.html"
WEB = ROOT / "pernah" / "web.py"


class VisualIdentitySystemTests(unittest.TestCase):
    def test_design_system_contract_and_tokens_exist(self):
        system = (ASSETS / "DESIGN-SYSTEM.md").read_text(encoding="utf-8")
        tokens = (ASSETS / "pernah-design-tokens.css").read_text(encoding="utf-8")
        for value in ("Memory", "Knowledge", "Continuity", "#141414", "#2BEE34", "#F4F5EF", "#176B1D", "LEMON MILK", "Open Sans"):
            self.assertIn(value, system)
        for value in ("--bg:#F4F5EF", "--accent:#176B1D", "--bg:#141414", "--accent:#2BEE34", '"LEMON MILK"', '"Open Sans"'):
            self.assertIn(value, tokens)

    def test_existing_user_facing_surfaces_use_shared_identity(self):
        for path in (CHRONICLE, GLOSSARY, WEB):
            text = path.read_text(encoding="utf-8").lower()
            self.assertIn("#141414".lower(), text, path.name)
            self.assertIn("#2bee34".lower(), text, path.name)
            self.assertIn("#f4f5ef".lower(), text, path.name)
            self.assertIn("#176b1d".lower(), text, path.name)
            self.assertIn("lemon milk", text, path.name)
            self.assertIn("open sans", text, path.name)

    def test_glossary_has_no_remote_font_dependency(self):
        text = GLOSSARY.read_text(encoding="utf-8")
        self.assertNotIn("fonts.googleapis.com", text)
        self.assertNotIn("fonts.cdnfonts.com", text)

    def test_glossary_has_brand_navigation_theme_and_floating_action(self):
        text = GLOSSARY.read_text(encoding="utf-8")
        for marker in ('assets/pernah-symbol.svg', 'id="themeToggle"', 'id="sidebarToggle"', 'id="floatTop"', 'touchstart', 'touchend'):
            self.assertIn(marker, text)

    def test_web_interface_has_identity_and_theme_controls(self):
        text = WEB.read_text(encoding="utf-8")
        lowered = text.lower()
        for marker in ('id="themetoggle"', 'id="floattop"', "memory", "knowledge", "continuity"):
            self.assertIn(marker, lowered)
        self.assertIn("#2BEE34", text)
        self.assertIn("#141414", text)

    def test_chronicle_uses_shared_symbol_asset(self):
        text = CHRONICLE.read_text(encoding="utf-8")
        self.assertIn('src="assets/pernah-symbol.svg"', text)
        self.assertNotIn('fonts.googleapis.com', text)


if __name__ == "__main__":
    unittest.main()
