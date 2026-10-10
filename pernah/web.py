from __future__ import annotations

import argparse
import html
import json
import mimetypes
import tempfile
import shutil
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from .manual_input import capture_text
from .storage import Storage, ValidationError
from .web_shell import about as shell_about, home as shell_home, memory as shell_memory, reader as shell_reader, saved_memory as shell_saved_memory, settings as shell_settings


_SYMBOL = '''<svg class="brand-mark" viewBox="0 0 96 96" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><path d="M19 79V30C19 17.85 28.85 8 41 8h15c12.7 0 23 10.3 23 23S68.7 54 56 54H35"/><path d="M35 54c10 0 17-6 17-16"/></g><circle cx="35" cy="30" r="6" fill="currentColor"/><circle cx="35" cy="54" r="6" fill="currentColor"/></svg>'''


_PAGE = """<!doctype html>
<html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#F4F5EF"><meta name="description" content="PERNAH Local Web Interface — capture memory ke canonical storage.">
<title>PERNAH · Web Interface</title>
<style>
:root{{--bg:#F4F5EF;--surface:#fff;--surface-2:#ECEFE8;--text:#141414;--muted:#5F635F;--border:#D9DDD5;--accent:#176B1D;--accent-soft:#E4F4E5;--shadow:rgba(20,20,20,.10);--display:"LEMON MILK","Lemon/Milk",Arial,sans-serif;--body:"Open Sans",ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}}
:root[data-theme="dark"]{{--bg:#141414;--surface:#1C1C1C;--surface-2:#101010;--text:#F2F2F2;--muted:#A7A7A7;--border:#2B2B2B;--accent:#2BEE34;--accent-soft:#102A12;--shadow:rgba(0,0,0,.34)}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;background:var(--bg)}}body{{margin:0;background:var(--bg);color:var(--text);font-family:var(--body);line-height:1.65}}button,textarea{{font:inherit}}button{{cursor:pointer}}::selection{{background:var(--accent);color:#061006}}
.shell{{width:min(1120px,100%);margin:auto;min-height:100vh;background:var(--surface);box-shadow:0 0 70px var(--shadow)}}
.sitebar{{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:20px;min-height:62px;padding:0 24px;border-bottom:1px solid var(--border);background:var(--surface);backdrop-filter:blur(14px)}}.brand{{display:inline-flex;align-items:center;gap:10px;color:var(--text);text-decoration:none}}.brand-mark{{width:31px;height:31px;color:var(--accent)}}.brand-word{{font:600 16px/1 var(--display);letter-spacing:.18em}}.nav-label{{color:var(--muted);font:700 10px var(--body);letter-spacing:.14em;text-transform:uppercase;margin-left:6px}}.nav-tools{{display:flex;gap:8px;margin-left:auto}}.nav-btn{{width:38px;height:38px;border:1px solid var(--border);border-radius:9px;background:var(--surface);color:var(--text);display:inline-flex;align-items:center;justify-content:center}}.nav-btn:hover,.nav-btn:focus-visible{{border-color:var(--accent);outline:2px solid color-mix(in srgb,var(--accent) 24%,transparent);outline-offset:1px}}
.hero{{padding:54px 42px 32px;border-bottom:1px solid var(--border);background:linear-gradient(180deg,var(--surface),var(--surface-2))}}.eyebrow{{font:700 10px var(--body);letter-spacing:.18em;color:var(--accent);text-transform:uppercase}}h1{{margin:9px 0 0;font:700 clamp(40px,7vw,68px)/.95 var(--display);letter-spacing:.01em}}.lead{{max-width:700px;margin:15px 0 0;color:var(--muted);font-size:16px}}
.main{{padding:34px 42px 90px;max-width:900px}}.status{{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--border);border-radius:999px;padding:6px 10px;color:var(--muted);font-size:11px;margin-bottom:20px}}.status::before{{content:"";width:7px;height:7px;border-radius:50%;background:var(--accent)}}.capture-card{{border:1px solid var(--border);border-radius:16px;background:var(--surface);padding:24px;box-shadow:0 16px 42px var(--shadow)}}label{{display:block;font:700 11px var(--body);letter-spacing:.1em;text-transform:uppercase;margin-bottom:9px}}textarea{{display:block;width:100%;min-height:190px;resize:vertical;padding:16px;border:1px solid var(--border);border-radius:12px;background:var(--surface-2);color:var(--text);line-height:1.65;outline:0}}textarea:focus{{border-color:var(--accent);box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 18%,transparent)}}textarea::placeholder{{color:var(--muted)}}.actions{{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-top:16px}}.hint{{color:var(--muted);font-size:12px}}.primary{{border:1px solid var(--accent);border-radius:10px;background:var(--accent);color:#061006;padding:11px 18px;font:800 12px var(--body);letter-spacing:.04em}}.primary:hover,.primary:focus-visible{{filter:brightness(1.04);outline:3px solid color-mix(in srgb,var(--accent) 22%,transparent);outline-offset:1px}}
.result{{margin-top:20px;border:1px solid var(--accent);border-left:5px solid var(--accent);border-radius:12px;padding:18px;background:var(--accent-soft)}}.result strong{{font:700 14px var(--display)}}.result p{{margin:7px 0;font-size:13px}}code{{word-break:break-all;background:var(--surface);border:1px solid var(--border);border-radius:5px;padding:2px 5px}}.footer{{border-top:1px solid var(--border);padding:22px 24px 30px;display:flex;justify-content:space-between;gap:20px;color:var(--muted);font-size:11px}}.footer b{{color:var(--text)}}.float-top{{position:fixed;right:22px;bottom:22px;width:48px;height:48px;border:1px solid var(--accent);border-radius:50%;background:var(--surface);color:var(--accent);font-weight:800;opacity:0;pointer-events:none;transform:translateY(12px);transition:.2s ease}}.float-top.visible{{opacity:1;pointer-events:auto;transform:none}}
@media(max-width:620px){{.sitebar{{padding:0 16px}}.hero{{padding:38px 20px 26px}}.lead{{font-size:14px}}.main{{padding:24px 20px 80px}}.capture-card{{padding:18px}}.actions{{align-items:stretch;flex-direction:column}}.primary{{width:100%;min-height:46px}}.footer{{padding:18px 20px;flex-direction:column}}.float-top{{right:16px;bottom:16px}}}}
@media(prefers-reduced-motion:reduce){{*,*::before,*::after{{scroll-behavior:auto!important;transition:none!important}}}}
</style></head><body><div class="shell">
<header class="sitebar" aria-label="PERNAH navigation">{symbol}<span class="brand-word">PERNAH</span><span class="nav-label">Web Interface</span><div class="nav-tools"><button class="nav-btn" id="themeToggle" type="button" aria-label="Ganti mode tampilan" aria-pressed="false">☾</button></div></header>
<section class="hero"><div class="eyebrow">MEMORY · KNOWLEDGE · CONTINUITY</div><div class="status">INPUT · LOCAL · CANONICAL</div><h1>Capture Memory</h1><p class="lead">Masukkan catatan secara natural. PERNAH akan melewatkannya melalui boundary input yang sama dengan manual input lalu menyimpannya ke canonical storage lokal.</p></section>
<main class="main"><div class="status">LOCALHOST · SOURCE TYPE: WEB</div><section class="capture-card"><form method="post" action="/capture"><label for="text">Catatan</label><textarea id="text" name="text" required autofocus placeholder="Contoh: Hari ini gue meeting dengan Rahayu jam 14.00…">{text}</textarea><div class="actions"><span class="hint">Original input tetap dipertahankan sebagai bagian dari provenance.</span><button class="primary" type="submit">Simpan ke PERNAH →</button></div></form></section>{result}</main>
<footer class="footer"><div><b>PERNAH / WEB INTERFACE</b><br>Local capture boundary · canonical storage.</div><div><a href="/about" style="color:inherit">About · @nexterade</a><br>Offline-friendly · localhost-only · no cloud</div></footer></div><button class="float-top" id="floatTop" type="button" aria-label="Kembali ke atas">↑</button>
<script>(()=>{{'use strict';const root=document.documentElement,t=document.getElementById('themeToggle'),top=document.getElementById('floatTop'),mq=matchMedia('(prefers-color-scheme: dark)');function get(){{const v=localStorage.getItem('pernah-theme');return v==='dark'||v==='light'||v==='system'?v:'system'}}function apply(v){{const d=v==='system'?mq.matches:v==='dark';root.dataset.theme=d?'dark':'light';t.textContent=v==='system'?'◐':d?'☀':'☾';t.setAttribute('aria-label',v==='system'?'Theme: system':d?'Theme: dark':'Theme: light');document.querySelector('meta[name="theme-color"]').content=d?'#141414':'#F4F5EF'}}apply(get());t.addEventListener('click',()=>{{const v=get(),n=v==='system'?'light':v==='light'?'dark':'system';localStorage.setItem('pernah-theme',n);apply(n)}});mq.addEventListener?.('change',()=>{{if(get()==='system')apply('system')}});addEventListener('storage',e=>{{if(e.key==='pernah-theme')apply(get())}});addEventListener('scroll',()=>top.classList.toggle('visible',scrollY>420),{{passive:true}});top.addEventListener('click',()=>scrollTo({{top:0,behavior:'smooth'}}))}})();</script>
</body></html>"""


def _page(result: str = "", text: str = "") -> bytes:
    return _PAGE.format(result=result, text=html.escape(text), symbol=_SYMBOL).encode("utf-8")


def _result_html(captured) -> str:
    draft = captured["draft"]
    result = captured["result"]
    entities = ", ".join(html.escape(e["name"]) for e in draft.entities) or "—"
    return (
        '<section class="result" aria-live="polite"><strong>Tersimpan ke canonical storage.</strong>'
        f'<p>Intent: <code>{html.escape(draft.intent)}</code></p>'
        f'<p>Language: <code>{html.escape(draft.detected_language)}</code></p>'
        f'<p>Memory ID: <code>{html.escape(result["memory_id"])}</code></p>'
        f'<p>Entities: {entities}</p></section>'
    )


def _saved_result_html(memory: dict) -> str:
    return (
        '<section class="result" aria-live="polite"><strong>Tersimpan ke canonical storage.</strong>'
        f'<p>Memory type: <code>{html.escape(str(memory["type"]))}</code></p>'
        f'<p>Memory ID: <code>{html.escape(str(memory["id"]))}</code></p>'
        f'<p>Catatan: {html.escape(str(memory["content"]))}</p></section>'
    )


class WebInputHandler(BaseHTTPRequestHandler):
    server_version = "PERNAHWeb/0.2"

    def do_GET(self):  # noqa: N802
        path = urlparse(self.path).path
        if path == "/about":
            self._send(200, shell_about())
            return
        if path == "/memory":
            self._send(200, shell_memory())
            return
        if path == "/settings":
            query = parse_qs(urlparse(self.path).query, keep_blank_values=False)
            restored = query.get("restored", [""])[0] == "1"
            self._send(200, shell_settings(restored=restored))
            return
        if path == "/backup":
            try:
                with Storage(self.server.db_path) as db:
                    payload = db.export_canonical()
                body = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
            except Exception:
                self._send_json(500, {"status": "error", "message": "Backup gagal dibuat."})
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="pernah-canonical-v1.json"')
            self._security_headers()
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if path == "/chronicle":
            self._send(200, shell_reader("Chronicle / Perjalanan", "chronicle", "/docs/Creation-Chronicle.html", "Rekam historis dan perjalanan perkembangan PERNAH, ditampilkan sebagai reference surface di dalam product shell.", self.server.docs_root / "Creation-Chronicle.html"))
            return
        if path == "/glossary":
            self._send(200, shell_reader("Glossary", "glossary", "/docs/Glosarium.html", "Knowledge dictionary PERNAH untuk istilah, konsep, dan bahasa lintas domain yang dipakai sepanjang project.", self.server.docs_root / "Glosarium.html"))
            return
        if path == "/":
            query = parse_qs(urlparse(self.path).query, keep_blank_values=False)
            saved_ids = query.get("saved", [])
            if saved_ids:
                memory_id = saved_ids[0]
                with Storage(self.server.db_path) as db:
                    memory = db.get_memory(memory_id)
                if memory is None:
                    self._send(404, _page('<section class="result" aria-live="polite"><strong>Memory tidak ditemukan.</strong></section>'))
                    return
                self._send(200, shell_saved_memory(memory))
                return
            self._send(200, shell_home())
            return
        if path == "/index.html":
            self._send(200, shell_home())
            return
        if path == "/favicon.svg":
            self._serve_file(self.server.docs_root, "assets/pernah-symbol.svg")
            return
        if path == "/health":
            try:
                with Storage(self.server.db_path) as db:
                    db._conn.execute("SELECT 1").fetchone()
            except Exception:
                self._send_json(503, {"status": "error"})
                return
            self._send_json(200, {"status": "ok"})
            return
        if path == "/docs" or path == "/docs/":
            self._redirect(303, "/docs/Glosarium.html")
            return
        if path.startswith("/docs/"):
            self._serve_static(path[len("/docs/"):])
            return
        if path == "/README.md":
            self._serve_root_file("README.md")
            return
        self.send_error(404)

    def do_POST(self):  # noqa: N802
        path = urlparse(self.path).path
        if path == "/restore":
            self._restore_backup()
            return
        if path != "/capture":
            self._send(404, _page('<section class="result" aria-live="polite"><strong>Halaman tidak ditemukan.</strong></section>'))
            return
        content_type = self.headers.get("Content-Type", "")
        if not content_type.lower().split(";", 1)[0].strip() == "application/x-www-form-urlencoded":
            self._send(415, _page('<section class="result" aria-live="polite"><strong>Format input tidak didukung.</strong></section>'))
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send(400, _page('<section class="result" aria-live="polite"><strong>Content-Length tidak valid.</strong></section>'))
            return
        if length < 0:
            self._send(400, _page('<section class="result" aria-live="polite"><strong>Content-Length tidak valid.</strong></section>'))
            return
        if length > 64 * 1024:
            self._send(413, _page('<section class="result" aria-live="polite"><strong>Input terlalu besar.</strong></section>'))
            return
        try:
            raw = self.rfile.read(length)
            fields = parse_qs(raw.decode("utf-8"), keep_blank_values=True, max_num_fields=16)
        except (UnicodeDecodeError, ValueError):
            self._send(400, _page('<section class="result" aria-live="polite"><strong>Format input tidak valid.</strong></section>'))
            return
        values = fields.get("text", [])
        if len(values) != 1:
            self._send(400, _page('<section class="result" aria-live="polite"><strong>Input teks harus tepat satu field.</strong></section>'))
            return
        text = values[0]
        if not text.strip():
            self._send(400, _page('<section class="result" aria-live="polite"><strong>Input tidak boleh kosong.</strong></section>', text))
            return
        try:
            with Storage(self.server.db_path) as db:
                captured = capture_text(db, text, source_type="web")
        except (ValueError, UnicodeDecodeError) as exc:
            self._send(400, _page(f'<section class="result" aria-live="polite"><strong>Input ditolak.</strong><p>{html.escape(str(exc))}</p></section>', text))
            return
        memory_id = captured["result"]["memory_id"]
        self._redirect(303, f"/?saved={memory_id}")

    def _restore_backup(self):
        content_type = self.headers.get("Content-Type", "")
        if content_type.lower().split(";", 1)[0].strip() != "application/json":
            self._send_json(415, {"status": "error", "message": "Restore hanya menerima application/json."})
            return
        if self.headers.get("X-PERNAH-Confirm", "") != "restore":
            self._send_json(400, {"status": "error", "message": "Restore membutuhkan konfirmasi eksplisit."})
            return
        try:
            length = int(self.headers.get("Content-Length", "-1"))
        except ValueError:
            self._send_json(400, {"status": "error", "message": "Content-Length tidak valid."})
            return
        if length < 0:
            self._send_json(411, {"status": "error", "message": "Content-Length wajib untuk restore."})
            return
        max_restore = 64 * 1024 * 1024
        if length > max_restore:
            self._send_json(413, {"status": "error", "message": "Backup terlalu besar untuk restore lokal."})
            return
        raw = self.rfile.read(length)
        if len(raw) != length:
            self._send_json(400, {"status": "error", "message": "Payload restore tidak lengkap."})
            return
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(prefix=".pernah-restore-", suffix=".json", delete=False) as temp:
                temp.write(raw)
                temp_path = Path(temp.name)
            Storage.validate_backup(temp_path)
            Storage.restore(temp_path, self.server.db_path)
        except ValidationError:
            self._send_json(400, {"status": "error", "message": "Backup tidak valid atau tidak memenuhi canonical contract."})
            return
        except Exception:
            self._send_json(400, {"status": "error", "message": "Restore gagal. Canonical state tidak diubah oleh payload yang gagal."})
            return
        finally:
            if temp_path is not None:
                try:
                    temp_path.unlink()
                except OSError:
                    pass
        self._send_json(200, {"status": "ok", "restored": True})

    def _serve_static(self, relative_path: str):
        self._serve_file(self.server.docs_root, relative_path)

    def _serve_root_file(self, filename: str):
        self._serve_file(self.server.project_root, filename)

    def _serve_file(self, root: Path, relative_path: str):
        try:
            relative = unquote(relative_path)
            candidate = (root / relative).resolve()
            candidate.relative_to(root.resolve())
        except (ValueError, OSError):
            self.send_error(404)
            return
        if not candidate.is_file() or candidate.suffix.lower() not in {".html", ".css", ".svg", ".md"}:
            self.send_error(404)
            return
        try:
            body = candidate.read_bytes()
        except OSError:
            self.send_error(404)
            return
        suffix = candidate.suffix.lower()
        content_types = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".svg": "image/svg+xml",
            ".md": "text/markdown; charset=utf-8",
        }
        self.send_response(200)
        self.send_header("Content-Type", content_types.get(suffix, mimetypes.types_map.get(suffix, "application/octet-stream")))
        self._security_headers(static=True)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _redirect(self, status: int, location: str):
        self.send_response(status)
        self.send_header("Location", location)
        self._security_headers()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _send(self, status: int, body: bytes):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self._security_headers()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, payload: dict):
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._security_headers()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _security_headers(self, static: bool = False):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN" if static else "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        csp = (
            "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; base-uri 'none'; form-action 'self'; frame-ancestors 'self'"
            if static else
            "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; "
            "connect-src 'self'; img-src 'self' data:; frame-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'"
        )
        self.send_header("Content-Security-Policy", csp)

    # Keep the standard BaseHTTPRequestHandler access log so CLI runs expose
    # request/response activity instead of silently swallowing it.


def create_server(db_path: str | Path = "pernah.db", host: str = "127.0.0.1", port: int = 8765):
    server = ThreadingHTTPServer((host, port), WebInputHandler)
    server.db_path = Path(db_path)
    server.project_root = Path(__file__).resolve().parent.parent
    server.docs_root = server.project_root / "docs"
    return server


def _copy_url_to_clipboard(url: str) -> bool:
    """Best-effort system clipboard copy without adding a runtime dependency.

    PERNAH remains fully usable when no clipboard utility is installed; the CLI
    simply reports that automatic copy was unavailable. Commands are invoked
    without a shell so the URL is never interpreted as shell syntax.
    """
    commands = [
        ["termux-clipboard-set"],
        ["wl-copy"],
        ["xclip", "-selection", "clipboard"],
        ["xsel", "--clipboard", "--input"],
        ["pbcopy"],
        ["clip.exe"],
    ]
    for command in commands:
        if shutil.which(command[0]) is None:
            continue
        try:
            subprocess.run(
                command,
                input=url,
                text=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2,
            )
            return True
        except (OSError, subprocess.SubprocessError):
            continue
    return False


def main(argv=None):
    parser = argparse.ArgumentParser(description="PERNAH local web interface for manual input")
    parser.add_argument("--db", default="pernah.db", help="SQLite database path")
    parser.add_argument("--host", default="127.0.0.1", help="bind address (default: localhost only)")
    parser.add_argument("--port", type=int, default=8765, help="HTTP port")
    args = parser.parse_args(argv)
    if args.host not in {"127.0.0.1", "localhost", "::1"}:
        parser.error("web interface defaults to localhost; use a deliberate local address only")
    server = create_server(args.db, args.host, args.port)
    url = f"http://{args.host}:{server.server_port}/"
    print(f"PERNAH Web Interface: {url}")
    if _copy_url_to_clipboard(url):
        print("URL copied to clipboard.")
    else:
        print("Clipboard auto-copy unavailable; copy the URL above manually.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
