from __future__ import annotations

import html
import re

SYMBOL = '<img class="brand-mark" src="/docs/assets/pernah-symbol.svg" alt="PERNAH" width="31" height="31">'

NAV = '''<nav class="nav" aria-label="PERNAH primary navigation">
<a href="/" class="nav-link {home}">Home</a>
<a href="/memory" class="nav-link {memory}">Memory</a>
<a href="/chronicle" class="nav-link {chronicle}">Chronicle</a>
<a href="/glossary" class="nav-link {glossary}">Glossary</a>
<a href="/settings" class="nav-link {settings}">Settings</a>
<a href="/about" class="nav-link {about}">About</a>
</nav>'''

STYLE = '''
:root{--bg:#F4F5EF;--surface:#fff;--surface-2:#ECEFE8;--text:#141414;--muted:#5F635F;--border:#D9DDD5;--accent:#176B1D;--accent-soft:#E4F4E5;--shadow:rgba(20,20,20,.10);--display:"LEMON MILK",Arial,sans-serif;--body:"Open Sans",ui-sans-serif,system-ui,sans-serif}
:root[data-theme="dark"]{--bg:#141414;--surface:#1C1C1C;--surface-2:#101010;--text:#F2F2F2;--muted:#A7A7A7;--border:#2B2B2B;--accent:#2BEE34;--accent-soft:#102A12;--shadow:rgba(0,0,0,.34)}
*{box-sizing:border-box}html{background:var(--bg);scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font-family:var(--body);line-height:1.65}a{color:inherit}button,textarea,input{font:inherit}button{cursor:pointer}.shell{width:min(1180px,100%);margin:auto;min-height:100vh;background:var(--surface);box-shadow:0 0 70px var(--shadow)}.sitebar{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:18px;min-height:64px;padding:0 24px;border-bottom:1px solid var(--border);background:var(--surface);backdrop-filter:blur(14px)}.brand{display:inline-flex;align-items:center;gap:10px;text-decoration:none;white-space:nowrap}.brand-mark{width:31px;height:31px;display:block;filter:none}.brand-word{font:600 16px/1 var(--display);letter-spacing:.18em}.nav{display:flex;gap:4px;align-items:center;flex-wrap:wrap}.nav-link{padding:9px 11px;border-radius:8px;text-decoration:none;color:var(--muted);font-size:13px}.nav-link:hover,.nav-link:focus-visible,.nav-link.active{color:var(--text);background:var(--surface-2);outline:none}.nav-link.active{box-shadow:inset 0 -2px 0 var(--accent)}.tools{margin-left:auto}.tool{width:38px;height:38px;border:1px solid var(--border);border-radius:9px;background:var(--surface);color:var(--text)}.main{padding:42px;max-width:1060px;margin:auto}.eyebrow{font:700 10px var(--body);letter-spacing:.18em;color:var(--accent);text-transform:uppercase}h1{margin:10px 0 12px;font:700 clamp(38px,7vw,68px)/.96 var(--display)}h2{margin:0 0 10px;font:700 18px var(--display)}.lead{max-width:720px;color:var(--muted);font-size:17px;margin:0 0 26px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.card{border:1px solid var(--border);border-radius:16px;padding:22px;background:var(--surface-2)}.card p{color:var(--muted);margin:7px 0}.card-link{display:block;text-decoration:none}.card-link:hover,.card-link:focus-visible{border-color:var(--accent);outline:2px solid var(--accent-soft);outline-offset:1px}.badge{display:inline-flex;border:1px solid var(--border);border-radius:999px;padding:5px 9px;color:var(--muted);font-size:11px;margin-bottom:12px}.footer{border-top:1px solid var(--border);padding:18px 24px;color:var(--muted);font-size:11px;display:flex;justify-content:space-between;gap:20px}.memory-form{border:1px solid var(--border);border-radius:16px;padding:24px;background:var(--surface-2)}label{display:block;font-weight:700;font-size:11px;letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px}textarea{display:block;width:100%;min-height:190px;resize:vertical;padding:15px;border:1px solid var(--border);border-radius:12px;background:var(--surface);color:var(--text);outline:0}textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}.file-input{display:block;width:100%;padding:12px;border:1px dashed var(--border);border-radius:10px;background:var(--surface);color:var(--text)}.attachment-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin-top:12px}.attachment-card{border:1px solid var(--border);border-radius:12px;padding:10px;min-width:0}.attachment-preview{display:block;width:100%;height:150px;object-fit:contain;background:var(--surface-2);border-radius:8px}.attachment-card a{display:block;overflow-wrap:anywhere;font-size:12px;margin-top:8px}.primary{margin-top:14px;border:1px solid var(--accent);border-radius:10px;padding:11px 16px;background:var(--accent);color:#061006;font-weight:800}.muted{color:var(--muted)}.settings-row{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:16px 0;border-bottom:1px solid var(--border)}.settings-row:last-child{border-bottom:0}.switch{border:1px solid var(--border);border-radius:999px;padding:7px 12px;background:var(--surface);color:var(--text)}
@media(max-width:780px){.sitebar{padding:10px 16px;align-items:flex-start;flex-wrap:wrap}.nav{order:3;width:100%;overflow:auto;flex-wrap:nowrap;padding-bottom:5px}.tools{margin-left:auto}.main{padding:30px 20px 70px}.grid{grid-template-columns:1fr}.footer{flex-direction:column}}
'''

SCRIPT = '''<script>(()=>{const r=document.documentElement,b=document.getElementById('theme'),m=document.querySelector('meta[name="theme-color"]'),mq=matchMedia('(prefers-color-scheme: dark)');function get(){const v=localStorage.getItem('pernah-theme');return v==='dark'||v==='light'||v==='system'?v:'system'}function resolved(v){return v==='system'?(mq.matches?'dark':'light'):v}function apply(v){const d=resolved(v)==='dark';r.dataset.theme=d?'dark':'light';if(b){b.textContent=v==='system'?'◐':d?'☀':'☾';b.setAttribute('aria-label',v==='system'?'Theme: system':d?'Theme: dark':'Theme: light');b.title=b.getAttribute('aria-label')}if(m)m.content=d?'#141414':'#F4F5EF'}function cycle(){const v=get();const n=v==='system'?'light':v==='light'?'dark':'system';localStorage.setItem('pernah-theme',n);apply(n)}apply(get());if(b)b.addEventListener('click',cycle);mq.addEventListener?.('change',()=>{if(get()==='system')apply('system')});addEventListener('storage',e=>{if(e.key==='pernah-theme')apply(get())})})();</script>'''



def page(title: str, active: str, content: str, main_class: str = "main") -> bytes:
    nav = NAV.format(**{k: ('active' if k == active else '') for k in ('home','memory','chronicle','glossary','settings','about')})
    doc = f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="shortcut icon" href="/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#141414"><meta name="description" content="PERNAH · Memory, Knowledge, Continuity"><title>PERNAH · {html.escape(title)}</title><style>{STYLE}</style></head><body><div class="shell"><header class="sitebar">{SYMBOL}<a class="brand" href="/"><span class="brand-word">PERNAH</span></a>{nav}<div class="tools"><button class="tool" id="theme" type="button" aria-label="Toggle theme">☾</button></div></header><main class="{main_class}">{content}</main><footer class="footer"><div><strong>PERNAH</strong> · Memory · Knowledge · Continuity</div><div><a href="/about">Built by @nexterade</a></div></footer></div>{SCRIPT}</body></html>'''
    doc = doc.replace('{main_class}', html.escape(main_class, quote=True))
    return doc.encode('utf-8')


def home() -> bytes:
    return page('Home','home','''<div class="eyebrow">PERSONAL MEMORY &amp; LIFE CONTEXT SYSTEM</div><h1>Remember what matters.</h1><p class="lead">PERNAH membantu menangkap, menjaga, dan memahami konteks personal melalui local-first memory, canonical storage, dan deterministic processing.</p><div class="grid"><a class="card card-link" href="/memory"><span class="badge">INPUT · LOCAL · CANONICAL</span><h2>Memory</h2><p>Capture catatan secara natural dan simpan ke canonical storage lokal.</p></a><a class="card card-link" href="/chronicle"><span class="badge">CONTINUITY · JOURNEY</span><h2>Chronicle / Perjalanan</h2><p>Lihat perjalanan pembentukan PERNAH sebagai artifact yang terus hidup.</p></a><a class="card card-link" href="/glossary"><span class="badge">REFERENCE LIBRARY</span><h2>Glossary</h2><p>Pahami istilah, konsep, dan bahasa yang dipakai sepanjang project.</p></a><a class="card card-link" href="/settings"><span class="badge">PREFERENCES</span><h2>Settings</h2><p>Atur preferensi pengalaman lokal seperti tema tampilan.</p></a></div>''')


def memory(text: str = '') -> bytes:
    safe = html.escape(text)
    return page('Memory','memory',f'''<div class="eyebrow">MEMORY · CAPTURE</div><h1>Memory</h1><p class="lead">Catat kejadian, transaksi, keputusan, atau hal penting lainnya. Tambahkan gambar sebagai bukti atau konteks visual bila diperlukan.</p><div class="memory-form"><form method="post" action="/capture" enctype="multipart/form-data"><label for="text">Catatan</label><textarea id="text" name="text" maxlength="60000" required placeholder="Contoh: Rahayu meminjam uang Rp200.000 tadi pagi.">{safe}</textarea><label for="attachments" style="margin-top:18px">Lampiran gambar (opsional)</label><input class="file-input" id="attachments" name="attachments" type="file" accept="image/jpeg,image/png,image/gif,image/webp" multiple><p class="muted">JPEG, PNG, GIF, atau WebP · maksimal 4 gambar · 8 MiB per gambar · 12 MiB total. Gambar disimpan lokal dan terhubung ke catatan ini.</p><button class="primary" type="submit">Simpan catatan + lampiran →</button></form><p class="muted">Original input tetap dipertahankan sebagai provenance. Lampiran bukan pengganti catatan.</p></div>''')


def saved_memory(memory_row: dict, attachments: list[dict] | None = None) -> bytes:
    content = html.escape(str(memory_row.get('content','')))
    mid = html.escape(str(memory_row.get('id','')))
    attachment_html = ''
    items = attachments or []
    if items:
        cards = []
        for item in items:
            aid = html.escape(str(item.get('id','')), quote=True)
            filename = html.escape(str(item.get('filename','Gambar')))
            mime = html.escape(str(item.get('mime_type','image/jpeg')), quote=True)
            size = int(item.get('size_bytes', 0))
            cards.append(f'<article class="attachment-card"><a href="/attachments/{aid}" target="_blank" rel="noopener"><img class="attachment-preview" src="/attachments/{aid}" alt="Lampiran: {filename}" loading="lazy"></a><a href="/attachments/{aid}" target="_blank" rel="noopener">{filename}</a><p class="muted">{mime} · {size:,} byte</p></article>')
        attachment_html = '<h2 style="margin-top:20px">Bukti &amp; lampiran</h2><div class="attachment-grid">' + ''.join(cards) + '</div>'
    return page('Memory saved','memory',f'''<div class="eyebrow">MEMORY · SAVED</div><h1>Memory saved.</h1><p class="lead">Catatan dan lampirannya tersimpan di canonical storage lokal.</p><section class="card"><strong>Tersimpan ke canonical storage.</strong><p>Memory ID: <code>{mid}</code></p><p>Catatan: {content}</p>{attachment_html}<p style="margin-top:20px"><a href="/memory">Capture another memory →</a></p></section>''')


def settings(restored: bool = False) -> bytes:
    notice = '<section class="card" style="border-color:var(--accent);margin-bottom:18px"><strong>Recovery selesai.</strong><p>Canonical storage sudah dipulihkan dari backup yang tervalidasi. Coba buka Memory atau refresh halaman untuk memastikan state tetap terbaca.</p></section>' if restored else ''
    content = '''<div class="eyebrow">SETTINGS · LOCAL EXPERIENCE</div><h1>Settings</h1><p class="lead">Preferensi tampilan tersimpan di browser lokal. Backup dan restore bekerja pada canonical SQLite lokal.</p><section class="card"><div class="settings-row"><div><strong>Theme</strong><div class="muted">Light / Dark</div></div><button class="switch" id="settings-theme" type="button">Toggle theme</button></div><div class="settings-row"><div><strong>Runtime</strong><div class="muted">Localhost-only Web Interface</div></div><span class="badge">LOCAL</span></div><div class="settings-row"><div><strong>Storage</strong><div class="muted">Canonical SQLite</div></div><span class="badge">CANONICAL</span></div></section><section class="card" style="margin-top:18px"><h2>Backup &amp; Recovery</h2><p>Backup menyimpan canonical state dalam format <code>pernah-canonical-v1</code>. Restore mengganti canonical database secara atomic setelah backup divalidasi.</p><div class="settings-row"><div><strong>Download backup</strong><div class="muted">Salinan canonical untuk recovery lokal.</div></div><a class="switch" href="/backup">Download JSON</a></div><div style="padding-top:16px"><label for="restore-file">Restore backup</label><input id="restore-file" type="file" accept="application/json,.json"><p class="muted">Restore bersifat destruktif terhadap state database target: state saat ini diganti oleh backup. Pastikan backup yang dipilih benar.</p><button class="primary" id="restore-btn" type="button">Restore selected backup →</button><p id="restore-status" class="muted" aria-live="polite"></p></div></section><p class="muted" style="margin-top:18px"><a href="/about">About @nexterade →</a></p><script>document.getElementById('settings-theme').addEventListener('click',()=>document.getElementById('theme').click());const f=document.getElementById('restore-file'),b=document.getElementById('restore-btn'),s=document.getElementById('restore-status');b.addEventListener('click',async()=>{if(!f.files.length){s.textContent='Pilih file backup JSON terlebih dahulu.';return}const file=f.files[0];if(!confirm('Restore akan mengganti canonical database dengan backup yang dipilih. Lanjutkan?'))return;b.disabled=true;s.textContent='Memvalidasi dan memulihkan backup…';try{const r=await fetch('/restore',{method:'POST',headers:{'Content-Type':'application/json','X-PERNAH-Confirm':'restore'},body:await file.arrayBuffer()});const data=await r.json();if(!r.ok)throw new Error(data.message||'Restore gagal.');location.href='/settings?restored=1'}catch(err){s.textContent=err.message||'Restore gagal.';b.disabled=false}})</script>'''
    return page('Settings','settings',notice + content)


def about() -> bytes:
    return page('About', 'about', '''<div class="eyebrow">PERNAH · ABOUT</div><h1>Built by @nexterade</h1><p class="lead">PERNAH lahir dari gagasan bahwa memory seharusnya membantu memahami apa yang penting, bukan sekadar mengingat apa yang terjadi.</p><div class="grid"><section class="card"><h2>Author</h2><p><strong>Builder · Experimenter · Lifelong Learner</strong></p><p>PERNAH dibangun dengan prinsip local-first, canonical storage, deterministic processing, dan continuity.</p></section><section class="card"><h2>Connect</h2><p><a href="https://github.com/nexterade/pernah">Repository ↗</a></p><p><a href="mailto:nexterade@gmail.com">nexterade@gmail.com</a></p><p><a href="https://nexterade.github.io/">nexterade.github.io ↗</a></p></section><section class="card"><h2>Skill Statistics</h2><p>Python · SQLite · Web · System Architecture · Data &amp; Storage · AI / LLM · Product Thinking · Documentation</p></section><section class="card"><h2>Interests</h2><p><strong>Building things. Understanding systems. Exploring ideas.</strong></p><p>Ngoprek sistem, belajar hal baru, membangun sesuatu dari nol, dan mencari cara sederhana untuk membuat hal yang rumit menjadi lebih masuk akal.</p><p><strong>“Karena yang berharga layak untuk dijaga 🫰”</strong></p><p class="muted">“Chat is ephemeral. Artifact is continuous.”</p></section></div>''')


def _scope_reference_css(css: str) -> str:
    """Scope standalone reference CSS so it cannot overwrite the product shell."""
    def split_selectors(text: str):
        out, start, depth = [], 0, 0
        for i, ch in enumerate(text):
            if ch in '([':
                depth += 1
            elif ch in ')]':
                depth = max(0, depth - 1)
            elif ch == ',' and depth == 0:
                out.append(text[start:i].strip()); start = i + 1
        out.append(text[start:].strip())
        return [x for x in out if x]

    def prefix_selector(sel: str) -> str:
        sel = sel.strip()
        if sel.startswith(':root[data-theme="dark"]'):
            return 'html[data-theme="dark"] .reference-surface' + sel[len(':root[data-theme="dark"]'):]
        if sel == ':root' or sel == 'html' or sel == 'body':
            return '.reference-surface'
        if sel.startswith('html[data-theme="dark"]'):
            return 'html[data-theme="dark"] .reference-surface' + sel[len('html[data-theme="dark"]'):]
        if sel.startswith('body '):
            return '.reference-surface ' + sel[len('body '):]
        if sel.startswith('html '):
            return '.reference-surface ' + sel[len('html '):]
        if sel == '*':
            return '.reference-surface *'
        if sel.startswith('::selection'):
            return '.reference-surface::selection' + sel[len('::selection'):]
        return '.reference-surface ' + sel

    def process_block(text: str) -> str:
        out, pos = [], 0
        while pos < len(text):
            brace = text.find('{', pos)
            if brace == -1:
                out.append(text[pos:]); break
            header = text[pos:brace].strip()
            depth, i = 1, brace + 1
            while i < len(text) and depth:
                if text[i] == '{': depth += 1
                elif text[i] == '}': depth -= 1
                i += 1
            body = text[brace + 1:i - 1]
            if header.startswith('@'):
                if header.lower().startswith(('@media', '@supports', '@container', '@layer', '@document')):
                    out.append(header + '{' + process_block(body) + '}')
                else:
                    out.append(header + '{' + body + '}')
            else:
                selectors = ','.join(prefix_selector(x) for x in split_selectors(header))
                out.append(selectors + '{' + body + '}')
            pos = i
        return ''.join(out)
    return process_block(css)


def _reference_fragment(doc_path: Path, sidebar_label: str) -> tuple[str, str, str]:
    raw = doc_path.read_text(encoding='utf-8')
    style_match = re.search(r'<style>(.*?)</style>', raw, re.S)
    script_match = re.search(r'<script>(.*?)</script>\s*</body>', raw, re.S)
    fragment_match = re.search(r'(<header class="masthead">.*?</header>\s*<div class="layout">.*?)(?=<footer class="footer">)', raw, re.S)
    if not (style_match and script_match and fragment_match):
        raise RuntimeError(f'Invalid reference document structure: {doc_path.name}')
    fragment = fragment_match.group(1)
    fragment = fragment.replace(
        '<div class="toolbar">',
        '<div class="toolbar"><button class="tool-btn reference-index-toggle" id="sidebarToggle" type="button" aria-label="Toggle ' + html.escape(sidebar_label, quote=True) + ' index" aria-controls="sidebarIndex" aria-pressed="false">☰ INDEX</button>',
        1,
    )
    fragment += '<button class="float-top" id="floatTop" type="button" aria-label="Kembali ke atas">↑</button>'
    script = script_match.group(1)
    # The standalone reference document owns its theme button, but the embedded
    # product shell intentionally reuses the shell-level theme control. Do not
    # let the reference script abort before its data renderer runs when that
    # standalone button is absent from the embedded fragment.
    script = re.sub(
        r"(function applyTheme\(theme\)\{.*?const dark=resolved==='dark';)(.*?)(document\.querySelector\('meta\[name=\"theme-color\"\]'\).*?;\})",
        lambda m: m.group(1) + "if(themeToggle){" + m.group(2) + "}" + m.group(3),
        script,
        count=1,
        flags=re.S,
    )
    script = script.replace("themeToggle.addEventListener('click',()=>{", "if(themeToggle)themeToggle.addEventListener('click',()=>{")
    if "const sidebarIndex = document.getElementById('sidebarIndex');" not in script:
        script = script.replace(
            "const sidebarToggle = document.getElementById('sidebarToggle');",
            "const sidebarToggle = document.getElementById('sidebarToggle');\n  const sidebarIndex = document.getElementById('sidebarIndex');",
            1,
        )
    return fragment, _scope_reference_css(style_match.group(1)), script


def reader(title: str, active: str, source: str, description: str, doc_path: Path) -> bytes:
    safe_title = html.escape(title)
    safe_source = html.escape(source, quote=True)
    safe_description = html.escape(description)
    fragment, ref_css, ref_script = _reference_fragment(doc_path, title)
    content = '<div class="reference-surface"><style>' + ref_css + '</style>' + fragment + '<p class="muted" style="margin:14px 42px 28px"><a href="' + safe_source + '">Buka dokumen standalone →</a></p><script>' + ref_script + '</script></div>'
    return page(safe_title, active, content, main_class='main reference-main')
