import io
import json
import tempfile
from unittest.mock import patch
import threading
import unittest
from contextlib import redirect_stderr
from http.client import HTTPConnection
from urllib.parse import quote_plus
from pathlib import Path

from pernah.storage import Storage
from pernah.web import _copy_url_to_clipboard, create_server


class WebInterfaceTests(unittest.TestCase):
    def test_clipboard_copy_uses_first_available_command(self):
        url = "http://127.0.0.1:6772/"
        with patch("pernah.web.shutil.which", side_effect=lambda name: "/usr/bin/" + name if name == "wl-copy" else None), \
             patch("pernah.web.subprocess.run") as run:
            self.assertTrue(_copy_url_to_clipboard(url))
            run.assert_called_once_with(
                ["wl-copy"],
                input=url,
                text=True,
                check=True,
                stdout=__import__("subprocess").DEVNULL,
                stderr=__import__("subprocess").DEVNULL,
                timeout=2,
            )

    def test_clipboard_copy_is_best_effort_when_unavailable(self):
        with patch("pernah.web.shutil.which", return_value=None), patch("pernah.web.subprocess.run") as run:
            self.assertFalse(_copy_url_to_clipboard("http://127.0.0.1:6772/"))
            run.assert_not_called()

    def test_get_form(self):
        with tempfile.TemporaryDirectory() as td:
            server = create_server(Path(td) / "pernah.db", port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("GET", "/memory")
                response = conn.getresponse()
                body = response.read().decode("utf-8")
                self.assertEqual(response.status, 200)
                self.assertIn('name="text"', body)
            finally:
                server.shutdown()
                server.server_close()
                thread.join()

    def test_about_page_identifies_author(self):
        with tempfile.TemporaryDirectory() as td:
            server = create_server(Path(td) / "pernah.db", port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("GET", "/about")
                response = conn.getresponse()
                body = response.read().decode("utf-8")
                self.assertEqual(response.status, 200)
                self.assertIn("PERNAH · ABOUT", body)
                self.assertIn("@nexterade", body)
                self.assertEqual(response.getheader("X-Frame-Options"), "DENY")
            finally:
                server.shutdown()
                server.server_close()
                thread.join()

    def test_about_page_contains_author_profile_and_links(self):
        with tempfile.TemporaryDirectory() as td:
            server = create_server(Path(td) / "pernah.db", port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("GET", "/about")
                response = conn.getresponse()
                body = response.read().decode("utf-8")
                self.assertEqual(response.status, 200)
                for expected in (
                    "@nexterade",
                    "https://github.com/nexterade/pernah",
                    "nexterade@gmail.com",
                    "https://nexterade.github.io/",
                    "Skill Statistics",
                    "Python",
                    "SQLite",
                    "System Architecture",
                    "Product Thinking",
                    "Chat is ephemeral. Artifact is continuous.",
                ):
                    self.assertIn(expected, body)
                self.assertEqual(response.getheader("X-Frame-Options"), "DENY")
            finally:
                server.shutdown()
                server.server_close()
                thread.join()

    def test_post_uses_existing_capture_pipeline_and_persists(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "pernah.db"
            server = create_server(db_path, port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                body = "text=Passport+ada+di+laci+meja"
                conn.request("POST", "/capture", body=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
                response = conn.getresponse()
                html = response.read().decode("utf-8")
                self.assertEqual(response.status, 303)
                location = response.getheader("Location")
                self.assertIsNotNone(location)
                self.assertTrue(location.startswith("/?saved="))
                self.assertEqual(html, "")
                conn.request("GET", location)
                response = conn.getresponse()
                html = response.read().decode("utf-8")
                self.assertEqual(response.status, 200)
                self.assertIn("Tersimpan", html)
            finally:
                server.shutdown()
                server.server_close()
                thread.join()
            with Storage(db_path) as db:
                rows = db.list_memories()
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]["content"], "Passport ada di laci meja")
                source = db._conn.execute("SELECT source_type FROM sources").fetchone()[0]
                self.assertEqual(source, "web")

    def test_blank_post_is_rejected_without_persistence(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "pernah.db"
            server = create_server(db_path, port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("POST", "/capture", body="text=", headers={"Content-Type": "application/x-www-form-urlencoded"})
                response = conn.getresponse()
                response.read()
                self.assertEqual(response.status, 400)
            finally:
                server.shutdown()
                server.server_close()
                thread.join()
            with Storage(db_path) as db:
                self.assertEqual(db.list_memories(), [])



    def test_backup_endpoint_downloads_canonical_json(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "pernah.db"
            with Storage(db_path) as db:
                source = db.add_source("web", "backup-endpoint")
                db.add_memory(memory_type="note", content="Backup endpoint works", source_id=source, confidence=1.0)
            server = create_server(db_path, port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("GET", "/backup")
                response = conn.getresponse()
                body = response.read()
                self.assertEqual(response.status, 200)
                self.assertIn("application/json", response.getheader("Content-Type"))
                self.assertIn("attachment;", response.getheader("Content-Disposition"))
                payload = json.loads(body.decode("utf-8"))
                self.assertEqual(payload["format"], "pernah-canonical-v1")
                validation_path = Path(td) / "downloaded.json"
                validation_path.write_bytes(body)
                self.assertTrue(Storage.validate_backup(validation_path))
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_restore_endpoint_requires_explicit_confirmation(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "pernah.db"
            backup_path = Path(td) / "backup.json"
            with Storage(db_path) as db:
                source = db.add_source("web", "restore-endpoint")
                db.add_memory(memory_type="note", content="Restore target", source_id=source, confidence=1.0)
                db.backup(backup_path)
            payload = backup_path.read_bytes()
            server = create_server(db_path, port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("POST", "/restore", body=payload, headers={"Content-Type": "application/json"})
                response = conn.getresponse()
                body = response.read().decode("utf-8")
                self.assertEqual(response.status, 400)
                self.assertIn("konfirmasi eksplisit", body)
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_restore_endpoint_replaces_database_only_after_validated_backup(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "pernah.db"
            backup_path = Path(td) / "backup.json"
            with Storage(db_path) as db:
                source = db.add_source("web", "restore-endpoint")
                db.add_memory(memory_type="note", content="Restored canonical memory", source_id=source, confidence=1.0)
                db.backup(backup_path)
            payload = backup_path.read_bytes()
            with Storage(db_path) as db:
                source = db.add_source("web", "restore-endpoint-old")
                db.add_memory(memory_type="note", content="Old state", source_id=source, confidence=1.0)
            server = create_server(db_path, port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("POST", "/restore", body=payload, headers={"Content-Type": "application/json", "X-PERNAH-Confirm": "restore"})
                response = conn.getresponse()
                body = response.read().decode("utf-8")
                self.assertEqual(response.status, 200)
                self.assertEqual(json.loads(body)["restored"], True)
            finally:
                server.shutdown(); server.server_close(); thread.join()
            with Storage(db_path) as db:
                self.assertEqual(db.exact_search("Old state"), [])
                self.assertEqual(len(db.exact_search("Restored canonical memory")), 1)

    def test_restore_endpoint_rejects_invalid_backup_without_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "pernah.db"
            with Storage(db_path) as db:
                source = db.add_source("web", "restore-invalid")
                db.add_memory(memory_type="note", content="Keep me", source_id=source, confidence=1.0)
            server = create_server(db_path, port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("POST", "/restore", body=b"{broken", headers={"Content-Type": "application/json", "X-PERNAH-Confirm": "restore"})
                response = conn.getresponse()
                body = response.read().decode("utf-8")
                self.assertEqual(response.status, 400)
                self.assertIn("Backup tidak valid", body)
            finally:
                server.shutdown(); server.server_close(); thread.join()
            with Storage(db_path) as db:
                self.assertEqual(len(db.exact_search("Keep me")), 1)

    def test_cli_access_log_is_visible(self):
        with tempfile.TemporaryDirectory() as td:
            server = create_server(Path(td) / "pernah.db", port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                captured = io.StringIO()
                with redirect_stderr(captured):
                    conn.request("GET", "/health")
                    response = conn.getresponse()
                    response.read()
                self.assertEqual(response.status, 200)
                self.assertIn('"GET /health HTTP/1.1" 200', captured.getvalue())
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_favicon_uses_canonical_brand_symbol(self):
        with tempfile.TemporaryDirectory() as td:
            server = create_server(Path(td) / "pernah.db", port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("GET", "/favicon.svg")
                response = conn.getresponse()
                body = response.read()
                self.assertEqual(response.status, 200)
                self.assertEqual(response.getheader("Content-Type"), "image/svg+xml")
                self.assertTrue(body.startswith(b"<svg"))
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_docs_are_served_by_the_same_local_server(self):
        with tempfile.TemporaryDirectory() as td:
            server = create_server(Path(td) / "pernah.db", port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("GET", "/docs/Glosarium.html")
                response = conn.getresponse()
                body = response.read().decode("utf-8")
                self.assertEqual(response.status, 200)
                self.assertIn("Glosarium", body)
                self.assertIn("text/html", response.getheader("Content-Type"))
                self.assertEqual(response.getheader("X-Content-Type-Options"), "nosniff")
                self.assertEqual(response.getheader("X-Frame-Options"), "SAMEORIGIN")
                self.assertIn("frame-ancestors 'self'", response.getheader("Content-Security-Policy"))

                conn.request("GET", "/docs/assets/pernah-symbol.svg")
                response = conn.getresponse()
                body = response.read()
                self.assertEqual(response.status, 200)
                self.assertEqual(response.getheader("Content-Type"), "image/svg+xml")
                self.assertTrue(body.startswith(b"<svg"))
            finally:
                server.shutdown()
                server.server_close()
                thread.join()

    def test_docs_path_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            server = create_server(Path(td) / "pernah.db", port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("GET", "/docs/../README.md")
                response = conn.getresponse()
                response.read()
                self.assertEqual(response.status, 404)
            finally:
                server.shutdown()
                server.server_close()
                thread.join()

    def test_health_endpoint_reports_ok_and_security_headers(self):
        with tempfile.TemporaryDirectory() as td:
            server = create_server(Path(td) / "pernah.db", port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("GET", "/health")
                response = conn.getresponse()
                body = response.read().decode("utf-8")
                self.assertEqual(response.status, 200)
                self.assertEqual(body, '{"status":"ok"}')
                self.assertEqual(response.getheader("X-Content-Type-Options"), "nosniff")
                self.assertEqual(response.getheader("X-Frame-Options"), "DENY")
                self.assertEqual(response.getheader("Cache-Control"), "no-store")
            finally:
                server.shutdown()
                server.server_close()
                thread.join()

    def test_capture_rejects_wrong_content_type(self):
        with tempfile.TemporaryDirectory() as td:
            server = create_server(Path(td) / "pernah.db", port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("POST", "/capture", body="text=halo", headers={"Content-Type": "application/json"})
                response = conn.getresponse()
                response.read()
                self.assertEqual(response.status, 415)
            finally:
                server.shutdown()
                server.server_close()
                thread.join()

    def test_capture_rejects_duplicate_text_fields(self):
        with tempfile.TemporaryDirectory() as td:
            server = create_server(Path(td) / "pernah.db", port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("POST", "/capture", body="text=satu&text=dua", headers={"Content-Type": "application/x-www-form-urlencoded"})
                response = conn.getresponse()
                response.read()
                self.assertEqual(response.status, 400)
            finally:
                server.shutdown()
                server.server_close()
                thread.join()

    def test_capture_rejects_invalid_utf8(self):
        with tempfile.TemporaryDirectory() as td:
            server = create_server(Path(td) / "pernah.db", port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("POST", "/capture", body=b"text=" + bytes([0xFF]), headers={"Content-Type": "application/x-www-form-urlencoded", "Content-Length": "6"})
                response = conn.getresponse()
                response.read()
                self.assertEqual(response.status, 400)
            finally:
                server.shutdown()
                server.server_close()
                thread.join()

    def test_capture_rejects_oversized_body(self):
        with tempfile.TemporaryDirectory() as td:
            server = create_server(Path(td) / "pernah.db", port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                body = b"text=" + (b"x" * (64 * 1024))
                conn.request("POST", "/capture", body=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
                response = conn.getresponse()
                response.read()
                self.assertEqual(response.status, 413)
            finally:
                server.shutdown()
                server.server_close()
                thread.join()

    def test_capture_survives_backup_restore_and_server_restart(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "pernah.db"
            backup_path = Path(td) / "recovery.json"
            server = create_server(db_path, port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                text = "Recovery browser gate survives restore."
                body = "text=" + quote_plus(text)
                conn.request("POST", "/capture", body=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
                response = conn.getresponse()
                location = response.getheader("Location")
                response.read()
                self.assertEqual(response.status, 303)
                self.assertTrue(location.startswith("/?saved="))
                conn.request("GET", location)
                response = conn.getresponse()
                captured_page = response.read().decode("utf-8")
                self.assertEqual(response.status, 200)
                self.assertIn(text, captured_page)
                conn.close()

                with Storage(db_path) as store:
                    store.backup(backup_path)
                self.assertTrue(Storage.validate_backup(backup_path))
                server.shutdown()
                server.server_close()
                thread.join()
                db_path.unlink()
                self.assertFalse(db_path.exists())

                Storage.restore(backup_path, db_path)
                self.assertTrue(db_path.exists())

                server = create_server(db_path, port=0)
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("GET", location)
                response = conn.getresponse()
                restored_page = response.read().decode("utf-8")
                self.assertEqual(response.status, 200)
                self.assertIn(text, restored_page)
                conn.request("GET", location)
                response = conn.getresponse()
                refreshed_page = response.read().decode("utf-8")
                self.assertEqual(response.status, 200)
                self.assertIn(text, refreshed_page)
                conn.close()
            finally:
                server.shutdown()
                server.server_close()
                thread.join()

    def test_capture_uses_post_redirect_get_and_refresh_is_safe(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "pernah.db"
            server = create_server(db_path, port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                body = "text=Refresh+harus+aman"
                conn.request("POST", "/capture", body=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
                response = conn.getresponse()
                location = response.getheader("Location")
                response.read()
                self.assertEqual(response.status, 303)
                self.assertTrue(location.startswith("/?saved="))

                conn.request("GET", location)
                response = conn.getresponse()
                response.read()
                self.assertEqual(response.status, 200)

                conn.request("GET", location)
                response = conn.getresponse()
                response.read()
                self.assertEqual(response.status, 200)
            finally:
                server.shutdown()
                server.server_close()
                thread.join()
            with Storage(db_path) as db:
                rows = db.list_memories()
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]["content"], "Refresh harus aman")

    def test_saved_memory_query_does_not_accept_multiple_ids(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "pernah.db"
            server = create_server(db_path, port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("GET", "/?saved=missing&saved=also-missing")
                response = conn.getresponse()
                response.read()
                self.assertEqual(response.status, 404)
            finally:
                server.shutdown()
                server.server_close()
                thread.join()


    def test_root_favicon_is_served_from_canonical_symbol(self):
        with tempfile.TemporaryDirectory() as td:
            server = create_server(Path(td) / "pernah.db", port=0); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("GET", "/favicon.svg")
                response = conn.getresponse()
                body = response.read().decode("utf-8")
                self.assertEqual(response.status, 200)
                self.assertEqual(response.getheader("Content-Type"), "image/svg+xml")
                self.assertIn("#176B1D", body)
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_live_web_theme_uses_shared_theme_key_and_system_mode(self):
        with tempfile.TemporaryDirectory() as td:
            server = create_server(Path(td) / "pernah.db", port=0); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection("127.0.0.1", server.server_port)
                conn.request("GET", "/")
                response = conn.getresponse()
                body = response.read().decode("utf-8")
                self.assertEqual(response.status, 200)
                self.assertIn("localStorage.getItem('pernah-theme')", body)
                self.assertIn("connect-src 'self'", response.getheader("Content-Security-Policy", ""))
                self.assertIn("prefers-color-scheme: dark", body)
                self.assertIn("v==='system'", body)
            finally:
                server.shutdown(); server.server_close(); thread.join()


    def test_multipart_capture_saves_and_serves_image_attachment(self):
        import base64
        png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j3ioAAAAASUVORK5CYII=')
        boundary = '----pernah-test-boundary'
        body = (
            f'--{boundary}\r\nContent-Disposition: form-data; name="text"\r\n\r\nRahayu meminjam Rp200.000 tadi pagi\r\n'
            f'--{boundary}\r\nContent-Disposition: form-data; name="attachments"; filename="bukti transfer.png"\r\nContent-Type: image/png\r\n\r\n'
        ).encode() + png + f'\r\n--{boundary}--\r\n'.encode()
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / 'pernah.db'
            server = create_server(db_path, port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection('127.0.0.1', server.server_port)
                conn.request('POST', '/capture', body=body, headers={'Content-Type': f'multipart/form-data; boundary={boundary}'})
                response = conn.getresponse(); response.read()
                self.assertEqual(response.status, 303)
                location = response.getheader('Location')
                conn.request('GET', location)
                response = conn.getresponse(); saved_html = response.read().decode()
                self.assertEqual(response.status, 200)
                self.assertIn('bukti transfer.png', saved_html)
                self.assertIn('/attachments/', saved_html)
                with Storage(db_path) as db:
                    memory = db.list_memories()[0]
                    attachments = db.list_attachments(memory['id'])
                    self.assertEqual(memory['content'], 'Rahayu meminjam Rp200.000 tadi pagi')
                    self.assertEqual(len(attachments), 1)
                    attachment_id = attachments[0]['id']
                conn.request('GET', f'/attachments/{attachment_id}')
                response = conn.getresponse(); data = response.read()
                self.assertEqual(response.status, 200)
                self.assertEqual(response.getheader('Content-Type'), 'image/png')
                self.assertEqual(data, png)
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_multipart_rejects_fake_image_without_saving_memory(self):
        boundary = '----pernah-test-boundary'
        body = (
            f'--{boundary}\r\nContent-Disposition: form-data; name="text"\r\n\r\nThis must not persist\r\n'
            f'--{boundary}\r\nContent-Disposition: form-data; name="attachments"; filename="fake.png"\r\nContent-Type: image/png\r\n\r\nnot-image'
            f'\r\n--{boundary}--\r\n'
        ).encode()
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / 'pernah.db'
            server = create_server(db_path, port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                conn = HTTPConnection('127.0.0.1', server.server_port)
                conn.request('POST', '/capture', body=body, headers={'Content-Type': f'multipart/form-data; boundary={boundary}'})
                response = conn.getresponse(); body_out = response.read().decode()
                self.assertEqual(response.status, 400)
                self.assertIn('gambar', body_out)
            finally:
                server.shutdown(); server.server_close(); thread.join()
            with Storage(db_path) as db:
                self.assertEqual(db.list_memories(), [])


if __name__ == '__main__':
    unittest.main()
