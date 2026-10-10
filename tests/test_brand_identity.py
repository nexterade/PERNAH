import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHRONICLE = ROOT / "docs" / "Creation-Chronicle.html"
ASSETS = ROOT / "docs" / "assets"


class BrandIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = CHRONICLE.read_text(encoding="utf-8")

    def test_brand_assets_exist(self):
        for name in ("pernah-symbol.svg", "pernah-lockup.svg", "pernah-monochrome.svg", "BRAND.md"):
            self.assertTrue((ASSETS / name).is_file(), name)

    def test_core_palette_and_typography_are_declared(self):
        for value in ("#141414", "#2BEE34", "#F4F5EF", "#176B1D"):
            self.assertIn(value.lower(), self.html.lower())
        self.assertIn('"LEMON MILK"', self.html)
        self.assertIn('"Open Sans"', self.html)

    def test_theme_and_sidebar_controls_exist(self):
        self.assertIn('id="themeToggle"', self.html)
        self.assertIn('id="sidebarToggle"', self.html)
        self.assertIn('id="floatTop"', self.html)
        self.assertIn('localStorage.getItem(\'pernah-theme\')', self.html)
        self.assertIn('prefers-reduced-motion:reduce', self.html)

    def test_brand_identity_is_not_botanical(self):
        brand = (ASSETS / "BRAND.md").read_text(encoding="utf-8").lower()
        self.assertIn("continuity p", brand)
        self.assertIn("memory", brand)
        self.assertIn("knowledge", brand)
        self.assertIn("continuity", brand)
        self.assertIn("leaf", brand)
        self.assertNotIn("botanical imagery", brand.replace("without relying on literal brain, book, cloud, database, leaf, or botanical imagery", ""))

    def test_brand_header_uses_shared_symbol_asset(self):
        match = re.search(r'<a class="brand".*?</a>', self.html)
        self.assertIsNotNone(match)
        self.assertIn('src="assets/pernah-symbol.svg"', match.group(0))

    def test_standalone_reference_brand_links_home_not_readme(self):
        for name in ("Glosarium.html", "Creation-Chronicle.html"):
            html = (ROOT / "docs" / name).read_text(encoding="utf-8")
            self.assertIn('class="brand" href="../"', html)
            self.assertNotIn('class="brand" href="../README.md"', html)
            self.assertNotIn('id="sidebarClose"', html)

    def test_standalone_reference_supports_touch_sidebar_gesture(self):
        for name in ("Glosarium.html", "Creation-Chronicle.html"):
            html = (ROOT / "docs" / name).read_text(encoding="utf-8")
            self.assertIn("touchstart", html)
            self.assertIn("touchend", html)
            self.assertIn("sidebar-open", html)


    def test_static_favicon_exists_and_uses_explicit_brand_color(self):
        favicon = ROOT / "favicon.svg"
        self.assertTrue(favicon.is_file())
        text = favicon.read_text(encoding="utf-8")
        self.assertIn('#176B1D', text)
        self.assertNotIn('currentColor', text)

    def test_standalone_pages_have_favicon_and_shared_theme_contract(self):
        for name in ("Glosarium.html", "Creation-Chronicle.html"):
            html = (ROOT / "docs" / name).read_text(encoding="utf-8")
            self.assertIn('rel="icon"', html)
            self.assertIn("localStorage.getItem('pernah-theme')", html)
            self.assertIn("prefers-color-scheme: dark", html)
            self.assertIn("theme==='system'", html)


if __name__ == "__main__":
    unittest.main()
