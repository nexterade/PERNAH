import tempfile
import threading
import unittest
from http.client import HTTPConnection
from pathlib import Path

from pernah.web import create_server


class WebAppShellTests(unittest.TestCase):
    def _server(self, td):
        return create_server(Path(td) / "pernah.db", port=0)

    def _get(self, conn, path):
        conn.request("GET", path)
        response = conn.getresponse()
        body = response.read().decode("utf-8")
        return response, body

    def test_settings_exposes_backup_and_recovery_surface(self):
        with tempfile.TemporaryDirectory() as td:
            server = self._server(td); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                response, body = self._get(conn, "/settings")
                self.assertEqual(response.status, 200)
                for expected in ("Backup &amp; Recovery", "/backup", "/restore", "X-PERNAH-Confirm", "Restore selected backup"):
                    self.assertIn(expected, body)
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_home_is_product_shell_not_readme(self):
        with tempfile.TemporaryDirectory() as td:
            server = self._server(td); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                response, body = self._get(conn, "/")
                self.assertEqual(response.status, 200)
                for expected in ("Home", "Memory", "Chronicle", "Glossary", "Settings", "About", "Remember what matters."):
                    self.assertIn(expected, body)
                self.assertNotIn("Canonical storage is local.", body)
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_product_shell_routes_exist(self):
        with tempfile.TemporaryDirectory() as td:
            server = self._server(td); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                response, body = self._get(conn, "/memory")
                self.assertEqual(response.status, 200); self.assertIn('action="/capture"', body); self.assertIn('class="nav-link active"', body)
                response, body = self._get(conn, "/settings")
                self.assertEqual(response.status, 200); self.assertIn("Localhost-only Web Interface", body)
                for path, target, marker in (("/chronicle", "/docs/Creation-Chronicle.html", "Chronicle / Perjalanan"), ("/glossary", "/docs/Glosarium.html", "Glossary"), ("/about", None, "Built by @nexterade")):
                    response, body = self._get(conn, path)
                    self.assertEqual(response.status, 200)
                    self.assertIn(marker, body)
                    if target:
                        self.assertNotIn('<iframe', body)
                        self.assertIn(f'href="{target}"', body)
                        self.assertIn('class="reference-surface"', body)
                        self.assertIn('reference-index-toggle', body)
                        self.assertEqual(body.count('<nav class="nav"'), 1)
                        self.assertNotEqual(response.status, 303)
            finally:
                server.shutdown(); server.server_close(); thread.join()



    def test_reference_shell_embeds_content_not_standalone_document(self):
        with tempfile.TemporaryDirectory() as td:
            server = self._server(td); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                for path, marker in (("/glossary", "id=\"dictionary\""), ("/chronicle", "id=\"chronicle\"")):
                    response, body = self._get(conn, path)
                    self.assertEqual(response.status, 200)
                    self.assertIn(marker, body)
                    self.assertNotIn('<iframe', body)
                    self.assertIn('Buka dokumen standalone', body)
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_reference_shell_uses_single_product_navigation(self):
        with tempfile.TemporaryDirectory() as td:
            server = self._server(td); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                for path in ("/glossary", "/chronicle"):
                    response, body = self._get(conn, path)
                    self.assertEqual(response.status, 200)
                    self.assertEqual(body.count('<nav class="nav"'), 1)
                    self.assertIn('id="sidebarToggle"', body)
                    self.assertIn('id="floatTop"', body)
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_shell_csp_allows_same_origin_brand_image_and_favicon_route_serves_svg(self):
        with tempfile.TemporaryDirectory() as td:
            server = self._server(td); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                response, body = self._get(conn, "/")
                self.assertEqual(response.status, 200)
                self.assertIn("img-src 'self' data:", response.getheader("Content-Security-Policy"))
                self.assertIn('src="/docs/assets/pernah-symbol.svg"', body)
                response, body = self._get(conn, "/favicon.svg")
                self.assertEqual(response.status, 200)
                self.assertEqual(response.getheader("Content-Type"), "image/svg+xml")
                self.assertIn("#176B1D", body)
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_embedded_glossary_renderer_guards_absent_standalone_theme_control(self):
        with tempfile.TemporaryDirectory() as td:
            server = self._server(td); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                response, body = self._get(conn, "/glossary")
                self.assertEqual(response.status, 200)
                self.assertIn("if(themeToggle){themeToggle.textContent", body)
                self.assertIn("applyTheme(themeValue());", body)
                self.assertIn("function render()", body)
                self.assertIn("render();", body)
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_embedded_glossary_outside_tap_binds_sidebar_index_contract(self):
        with tempfile.TemporaryDirectory() as td:
            server = self._server(td); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                response, body = self._get(conn, "/glossary")
                self.assertEqual(response.status, 200)
                self.assertIn("const sidebarIndex = document.getElementById('sidebarIndex');", body)
                self.assertIn("!sidebarIndex.contains(target)", body)
                self.assertIn("sidebarBackdrop.addEventListener('click', closeSidebar)", body)
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_reference_shell_guards_absent_standalone_theme_control(self):
        with tempfile.TemporaryDirectory() as td:
            server = self._server(td); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                response, body = self._get(conn, "/chronicle")
                self.assertEqual(response.status, 200)
                self.assertIn("if(themeToggle){themeToggle.textContent", body)
                self.assertIn('id="toc"', body)
                self.assertIn("buildToc();", body)
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_shell_uses_canonical_symbol_asset_and_favicon(self):
        with tempfile.TemporaryDirectory() as td:
            server = self._server(td); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                response, body = self._get(conn, "/")
                self.assertEqual(response.status, 200)
                self.assertIn('src="/docs/assets/pernah-symbol.svg"', body)
                self.assertIn('href="/favicon.svg"', body)
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_about_contains_guarded_value_slogan(self):
        with tempfile.TemporaryDirectory() as td:
            server = self._server(td); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                response, body = self._get(conn, "/about")
                self.assertEqual(response.status, 200)
                self.assertIn("Karena yang berharga layak untuk dijaga", body)
            finally:
                server.shutdown(); server.server_close(); thread.join()


    def test_shell_uses_system_theme_as_shared_default(self):
        with tempfile.TemporaryDirectory() as td:
            server = self._server(td); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                response, body = self._get(conn, "/")
                self.assertEqual(response.status, 200)
                self.assertIn("localStorage.getItem('pernah-theme')", body)
                self.assertIn("prefers-color-scheme: dark", body)
                self.assertIn("v==='system'", body)
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_capture_result_returns_to_product_shell(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "pernah.db"
            server = create_server(db_path, port=0); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("POST", "/capture", body="text=Shell+capture", headers={"Content-Type":"application/x-www-form-urlencoded"})
                response = conn.getresponse(); location = response.getheader("Location"); response.read()
                self.assertEqual(response.status, 303)
                response, body = self._get(conn, location)
                self.assertEqual(response.status, 200)
                self.assertIn("Memory saved.", body); self.assertIn("Memory", body); self.assertIn("Chronicle", body); self.assertIn("About", body)
            finally:
                server.shutdown(); server.server_close(); thread.join()
