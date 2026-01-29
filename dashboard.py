#!/usr/bin/env python3
import csv
import html
import io
import json
import os
import re
import time
from urllib.parse import quote
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = Path(__file__).resolve().parent
SCRIPT_NAME = Path(__file__).name
EXCLUDE = {SCRIPT_NAME}
SECTION_FILES = {
    "living room": "living room",
    "bedroom": "bedrooms",
    "dining room": "dining-room",
    "recliner": "recliners",
}


def list_files():
    files = []
    for name in os.listdir(ROOT):
        if name.startswith('.'):
            continue
        path = ROOT / name
        if not path.is_file():
            continue
        if name in EXCLUDE:
            continue
        files.append(name)
    files.sort(key=lambda s: s.lower())
    return files


def render_index(files):
    files_json = json.dumps(files)
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>FDWEBSITE Preview Dashboard</title>
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\" />
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin />
  <link href=\"https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap\" rel=\"stylesheet\" />
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f4f0;
      --panel: #ffffff;
      --ink: #111827;
      --muted: #6b7280;
      --accent: #c08427;
      --line: #e5e7eb;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ height: 100%; margin: 0; }}
    body {{
      font-family: "Space Grotesk", "IBM Plex Sans", sans-serif;
      color: var(--ink);
      background: radial-gradient(1200px 700px at 20% -10%, #fff7e6, transparent),
                  radial-gradient(900px 600px at 100% 0%, #efe8ff, transparent),
                  var(--bg);
    }}
    .app {{ display: grid; grid-template-columns: 280px 1fr; height: 100%; gap: 16px; padding: 16px; }}
    .sidebar {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      box-shadow: 0 12px 30px rgba(17, 24, 39, 0.08);
    }}
    .title {{ font-size: 20px; font-weight: 700; }}
    .hint {{ color: var(--muted); font-size: 13px; }}
    .upload {{
      border: 1px dashed #d1d5db;
      border-radius: 12px;
      padding: 10px;
      background: #ffffff;
      display: grid;
      gap: 8px;
    }}
    .upload input[type=\"file\"] {{ font-size: 12px; }}
    .upload button {{
      border: 1px solid var(--line);
      background: #fffdf9;
      padding: 8px 10px;
      border-radius: 10px;
      font-weight: 600;
      color: var(--ink);
      font-size: 12px;
      cursor: pointer;
    }}
    .file-list {{
      display: grid;
      gap: 8px;
      overflow: auto;
      padding-right: 6px;
    }}
    .file-btn {{
      border: 1px solid var(--line);
      background: #fffaf2;
      color: var(--ink);
      padding: 10px 12px;
      border-radius: 12px;
      font-weight: 600;
      text-align: left;
      cursor: pointer;
      transition: transform 0.08s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }}
    .file-btn:hover {{ transform: translateY(-1px); border-color: #d6d3d1; box-shadow: 0 6px 16px rgba(17, 24, 39, 0.08); }}
    .file-btn.active {{ border-color: var(--accent); background: #fff2d6; }}
    .actions {{ display: flex; gap: 8px; flex-wrap: wrap; }}
    .action-link {{
      text-decoration: none;
      border: 1px solid var(--line);
      background: #ffffff;
      padding: 8px 10px;
      border-radius: 999px;
      font-weight: 600;
      color: var(--ink);
      font-size: 12px;
    }}
    .preview {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 16px;
      overflow: hidden;
      display: grid;
      grid-template-rows: auto 1fr;
      box-shadow: 0 12px 30px rgba(17, 24, 39, 0.08);
    }}
    .preview-header {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--line);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      background: #fffdf9;
    }}
    .current {{ font-weight: 700; }}
    iframe {{ width: 100%; height: 100%; border: 0; background: #f8fafc; }}

    @media (max-width: 900px) {{
      .app {{ grid-template-columns: 1fr; grid-template-rows: auto 1fr; }}
      .sidebar {{ flex-direction: column; }}
    }}
  </style>
</head>
<body>
  <div class=\"app\">
    <aside class=\"sidebar\">
      <div class=\"title\">FDWEBSITE Preview</div>
      <div class=\"hint\">Pick a file to render it inside a full HTML shell.</div>
      <div id=\"file-list\" class=\"file-list\"></div>
      <div class=\"upload\">
        <div class=\"hint\">Bulk update from CSV</div>
        <input id=\"csv-file\" type=\"file\" accept=\".csv,text/csv\" />
        <button id=\"upload-csv\">Upload + Update Pages</button>
        <div id=\"csv-status\" class=\"hint\"></div>
      </div>
      <div class=\"hint\">Note: links like /Content/... will 404 locally. Use this only for layout checks.</div>
    </aside>
    <section class=\"preview\">
      <div class=\"preview-header\">
        <div class=\"current\" id=\"current-file\">Select a file</div>
        <div class=\"actions\">
          <a id=\"open-tab\" class=\"action-link\" href=\"#\" target=\"_blank\">Open in new tab</a>
          <a id=\"open-raw\" class=\"action-link\" href=\"#\" target=\"_blank\">View raw</a>
        </div>
      </div>
      <iframe id=\"preview-frame\" title=\"Preview\"></iframe>
    </section>
  </div>

  <script>
    const files = {files_json};
    const list = document.getElementById('file-list');
    const frame = document.getElementById('preview-frame');
    const current = document.getElementById('current-file');
    const openTab = document.getElementById('open-tab');
    const openRaw = document.getElementById('open-raw');
    const csvFile = document.getElementById('csv-file');
    const uploadCsv = document.getElementById('upload-csv');
    const csvStatus = document.getElementById('csv-status');

    let activeFile = null;

    function loadFile(name) {{
      const url = '/render?file=' + encodeURIComponent(name);
      const raw = '/raw?file=' + encodeURIComponent(name);
      frame.src = url;
      current.textContent = name;
      openTab.href = url;
      openRaw.href = raw;
      activeFile = name;
      [...list.querySelectorAll('button')].forEach(btn => btn.classList.toggle('active', btn.dataset.file === name));
    }}

    files.forEach(name => {{
      const btn = document.createElement('button');
      btn.className = 'file-btn';
      btn.textContent = name;
      btn.dataset.file = name;
      btn.addEventListener('click', () => loadFile(name));
      list.appendChild(btn);
    }});

    uploadCsv.addEventListener('click', async () => {{
      if (!csvFile.files || !csvFile.files.length) {{
        csvStatus.textContent = 'Choose a CSV file first.';
        return;
      }}
      try {{
        const text = await csvFile.files[0].text();
        csvStatus.textContent = 'Uploading...';
        const res = await fetch('/upload-csv', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ csv: text }})
        }});
        if (!res.ok) throw new Error('Upload failed');
        const data = await res.json();
        const updated = data.updated || {{}};
        csvStatus.textContent = 'Updated: living room ' + (updated['living room'] || 0) +
          ', bedroom ' + (updated['bedroom'] || 0) +
          ', dining room ' + (updated['dining room'] || 0) +
          ', recliner ' + (updated['recliner'] || 0);
        if (activeFile) {{
          loadFile(activeFile);
        }}
      }} catch (err) {{
        csvStatus.textContent = 'Upload failed. Check server output.';
      }}
    }});

    if (files.length) loadFile(files[0]);
  </script>
</body>
</html>"""


def render_wrapper(name, content):
    safe_name = html.escape(name)
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Preview - {safe_name}</title>
  <style>
    :root {{ color-scheme: light; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; padding: 24px; background: #f8fafc; }}
    img {{ max-width: 100%; height: auto; }}
    table {{ width: 100%; }}
    .row {{ display: flex; flex-wrap: wrap; margin: 0 -8px; }}
    .col-xs-12, .col-sm-6, .col-md-6 {{ width: 100%; padding: 0 8px; }}
    @media (min-width: 768px) {{ .col-sm-6 {{ width: 50%; }} }}
    @media (min-width: 992px) {{ .col-md-6 {{ width: 50%; }} }}
    .img-responsive {{ display: block; max-width: 100%; height: auto; }}
    .fd-h2 {{ font-weight: 900; font-size: 22px; margin: 20px 0 8px; color: #111827; }}
    .ms-nowline {{ font-size: 45px; font-weight: 900; color: #ffffff !important; letter-spacing: .02em; background: #b45309 !important; padding: 10px 14px; border-radius: 12px; display: inline-block; }}
  </style>
</head>
<body>
  <div id=\"fd-fragment\">
{content}
  </div>
</body>
</html>"""


def render_raw(content):
    return content


def extract_money(value):
    if not value:
        return ""
    match = re.search(r"\$\s*([0-9][0-9,]*)", value)
    if not match:
        return ""
    return match.group(1).replace(",", "")


def extract_qty(value):
    if not value:
        return ""
    match = re.search(r"([0-9]+)", value)
    return match.group(1) if match else value.strip()


def parse_csv_sections(csv_text):
    sections = {key: [] for key in SECTION_FILES.keys()}
    current = None
    reader = csv.reader(io.StringIO(csv_text))
    for row in reader:
        row = [cell.strip() for cell in row]
        if not any(row):
            continue
        first = row[0].strip()
        name = first.lower()
        if name in {"living room", "bedroom", "dinning room", "dining room", "recliner"}:
            if name == "dinning room":
                name = "dining room"
            current = name
            continue
        if first.upper() == "NEW PRODUCT":
            continue
        if not current:
            continue
        while len(row) < 27:
            row.append("")
        item = {
            "includes": row[6].strip(),
            "name": row[7].strip(),
            "price": row[8].strip(),
            "reg": row[17].strip(),
            "qty": row[24].strip(),
            "badge": row[25].strip(),
            "img": row[26].strip(),
        }
        sections[current].append(item)
    return sections


def card_html(item):
    name = item.get("name") or item.get("sku") or "Item"
    includes = item.get("includes") or ""
    img = item.get("img") or ""
    now = extract_money(item.get("price", ""))
    reg = extract_money(item.get("reg", ""))
    qty = extract_qty(item.get("qty", ""))
    badge = item.get("badge", "").strip()
    search = quote(name)

    data_attrs = []
    if reg:
        data_attrs.append(f'data-reg="{reg}"')
    if now:
        data_attrs.append(f'data-now="{now}"')
    if qty:
        data_attrs.append(f'data-qty="{html.escape(str(qty))}"')
    if badge:
        data_attrs.append(f'data-badge="{html.escape(badge)}"')
    data_attrs_str = " ".join(data_attrs)

    includes_text = f"Includes: {html.escape(includes)}" if includes else ""
    qty_text = f"Qty Left: {html.escape(str(qty))}" if qty else ""

    return f"""
<table class="ms-card" {data_attrs_str} role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border: 1px solid #e5e7eb; border-radius: 12px; overflow: hidden;">
  <tbody>
    <tr>
      <td style="padding: 0;">
        <div style="position: relative;">
          <a href="/Product/SiteSearch?search={search}" style="text-decoration: none; color: inherit;">
            <img src="{html.escape(img)}" alt="{html.escape(name)}" style="width: 100%; height: auto; display: block; border: 0;" />
          </a>
          <div class="ms-badge" style="position: absolute; top: 10px; left: 10px; background: #111827; color: #fff; font-weight: 900; border-radius: 999px; padding: 6px 10px; font-size: 12px; letter-spacing: .04em;">Clearance</div>
          <div class="ms-offbadge" style="position: absolute; top: 10px; right: 10px; background: #b45309; color: #fff; font-weight: 900; border-radius: 999px; padding: 8px 14px; font-size: 14px; letter-spacing: .04em; box-shadow: 0 6px 14px rgba(0,0,0,.18);"></div>
          <div style="position: absolute; left: 0; bottom: 0; background: #ffffff; color: #111827; font-weight: 900; font-size: 14px; padding: 6px 10px; border-top-right-radius: 8px;">{html.escape(name)}</div>
        </div>
      </td>
    </tr>
    <tr>
      <td style="padding: 10px 12px 14px;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
          <tbody>
            <tr>
              <td valign="top" style="padding-right: 10px;">
                <div style="color: #6b7280; font-size: 12px;">{includes_text}</div>
                <div style="margin-top: 8px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                  <div class="ms-nowline" style="font-weight: 900; font-size: 13px; color: #111827;"></div>
                  <div style="color: #374151; font-size: 13px;">Was <span class="ms-regline" style="text-decoration: line-through;"></span></div>
                </div>
              </td>
              <td valign="top" style="text-align: right;">
                <div style="color: #6b7280; font-size: 12px;">{qty_text}</div>
                <a href="/Home/Locations" style="display: inline-block; margin-top: 8px; padding: 8px 12px; border-radius: 8px; background: #f3f4f6; color: #111827; text-decoration: none; font-weight: 800; font-size: 12px;">Check Store Stock</a>
              </td>
            </tr>
          </tbody>
        </table>
      </td>
    </tr>
  </tbody>
</table>
""".strip()


def build_cards_table(items):
    rows = []
    for i in range(0, len(items), 2):
        left = card_html(items[i])
        right = card_html(items[i + 1]) if i + 1 < len(items) else ""
        right_cell = right or ""
        rows.append(f"""
<tr>
  <td width="50%" valign="top" style="padding: 8px;">{left}</td>
  <td width="50%" valign="top" style="padding: 8px;">{right_cell}</td>
</tr>
""".strip())
    tbody = "\n".join(rows)
    return f"""
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin: 6px 0;">
  <tbody>
{tbody}
  </tbody>
</table>
""".strip()


def replace_cards_section(content, new_table):
    start = content.find("<!-- Cards -->")
    if start == -1:
        return None
    logic = content.find("<!-- Logic -->", start)
    if logic == -1:
        return None
    return content[: start + len("<!-- Cards -->")] + "\n" + new_table + "\n" + content[logic:]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            files = list_files()
            body = render_index(files)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
            return

        if parsed.path in {"/render", "/raw"}:
            qs = parse_qs(parsed.query)
            name = qs.get("file", [""])[0]
            if not name or "/" in name or "\\" in name:
                self.send_error(400, "Invalid file")
                return
            path = ROOT / name
            if name in EXCLUDE or name.startswith(".") or not path.is_file():
                self.send_error(404, "File not found")
                return
            content = path.read_text(encoding="utf-8", errors="replace")
            if parsed.path == "/raw":
                body = render_raw(content)
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
            else:
                body = render_wrapper(name, content)
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
            return

        self.send_error(404, "Not found")

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/save":
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                self.send_error(400, "Invalid length")
                return

            payload = self.rfile.read(length).decode("utf-8", errors="replace")
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return

            name = str(data.get("file", ""))
            html_content = str(data.get("html", ""))
            if not name or "/" in name or "\\" in name:
                self.send_error(400, "Invalid file")
                return

            path = ROOT / name
            if name in EXCLUDE or name.startswith(".") or not path.is_file():
                self.send_error(404, "File not found")
                return

            ts = time.strftime("%Y%m%d-%H%M%S")
            base = path.stem
            suffix = path.suffix
            new_name = f"{base}-{ts}{suffix}"
            new_path = ROOT / new_name
            counter = 1
            while new_path.exists():
                new_name = f"{base}-{ts}-{counter}{suffix}"
                new_path = ROOT / new_name
                counter += 1

            new_path.write_text(html_content, encoding="utf-8")
            body = json.dumps({"ok": True, "file": new_name}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if parsed.path == "/upload-csv":
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                self.send_error(400, "Invalid length")
                return

            payload = self.rfile.read(length).decode("utf-8", errors="replace")
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return

            csv_text = str(data.get("csv", ""))
            if not csv_text:
                self.send_error(400, "Missing csv")
                return

            sections = parse_csv_sections(csv_text)
            updated = {}
            updated_files = []
            ts = time.strftime("%Y%m%d-%H%M%S")

            for section, items in sections.items():
                filename = SECTION_FILES.get(section)
                if not filename:
                    continue
                path = ROOT / filename
                if not path.is_file():
                    continue
                original = path.read_text(encoding="utf-8", errors="replace")
                table = build_cards_table(items)
                replaced = replace_cards_section(original, table)
                if replaced is None:
                    continue
                backup = ROOT / f"{filename}.bak-{ts}"
                backup.write_text(original, encoding="utf-8")
                path.write_text(replaced, encoding="utf-8")
                updated[section] = len(items)
                updated_files.append(filename)

            body = json.dumps({"ok": True, "updated": updated, "files": updated_files}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_error(404, "Not found")
        return


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), Handler)
    print("FDWEBSITE dashboard running at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
