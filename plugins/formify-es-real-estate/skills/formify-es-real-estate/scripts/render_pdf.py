#!/usr/bin/env python3
"""
render_pdf.py: turns a document's HTML into an A4 PDF, adds the signature areas and writes
<document>.signatures.json with the coordinates Formify expects (create_draft: signatureBox and idScanBox
per signer, top-left origin, in points, 0-indexed page).

Usage:
  python3 render_pdf.py --html body.html --signers signers.json --out document.pdf
                        [--profile official|professional|light] [--css ../assets/base.css]
                        [--title "Deposit agreement"] [--ref "DEP-2026-0012"] [--lang sv]
                        [--credit-tr "..."] [--no-credit] [--signature-page] [--no-signatures]
                        [--config ../segment.json]

signers.json: list of objects {"name": "...", "role": "VENDEDORA", "role_tr": "Seller", "id_scan": true|false}
(role in the master language; role_tr the same role in the client's language, printed small after a slash so that a
 client who does not read the master language knows which block is theirs; omitted in single-language segments)
The list order is the order in which they appear.

Signature areas follow Formify's signature-box guide (references/signatures.md): a text heading above
(the role, then the name), nothing drawn, white space of at least 100 pt per standard signature and 261 pt
with an ID scan, two per row. By default the rows flow right after the text (or at <!-- SIGNATURES --> when
the template marks the place) and each row moves to the next page only if it does not fit. The exact
position is measured in the rendered PDF through an invisible marker, so the coordinates are always right.
Without pypdf the script falls back to a separate signature page with fixed coordinates.

Form fields: every <span class="pdf-field" data-name data-width> blank that fill.py inserted becomes a real PDF text
field (AcroForm, per Formify's pdf-forms recipe) at the measured position; the same name in two places becomes one
field with two widgets. Needs pypdf; pdfplumber gives the most reliable positions.

Footer on every page (CSS margin box): line 1 the title and reference; line 2 the credit line in the master
language and in the client's language, from segment.json ("footer"). No web address: addresses do not outlive documents.

PDF engines, in order: Chromium/Chrome headless, WeasyPrint, wkhtmltopdf. Without any of them the full
HTML is left next to the target and the script exits with code 2. Standard library only; pypdf optional.
"""
import argparse, json, os, re, shutil, subprocess, sys, glob, html

A4_W, A4_H = 595, 841
SIG_W, SIG_H = 219, 58
ID_W, ID_H = 218, 138
# Separate signature page (fallback only)
COL_X = [50, 326]
TOP0 = 90
ROW_H_ID = 268
ROW_H_SIMPLE = 112
ROWS_ID = 2
ROWS_SIMPLE = 6
# Inline signature rows (default)
IN_COLS = [0, 274]          # x offset inside the row (219 + 55 gap)
IN_HEAD = 46                # rule + heading (role) + translated role on its own line + subtitle (name) + 10 pt air
IN_ROW_SIMPLE = IN_HEAD + SIG_H + 20          # 124 pt
IN_ROW_ID = IN_HEAD + SIG_H + 15 + ID_H + 20  # 277 pt
MARK = "SIGMARK"
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG = os.path.join(HERE, "..", "segment.json")
DEFAULT_CSS = os.path.join(HERE, "..", "assets", "base.css")


def load_config(path):
    cfg = {"master_language": "en", "footer": {"credit": {"en": "Prepared with the Formify.eu e-signing solution"}}}
    if path and os.path.exists(path):
        try:
            cfg.update(json.load(open(path, encoding="utf-8")))
        except Exception as e:
            print(f"Notice: could not read {path}: {e}", file=sys.stderr)
    return cfg


def find_chromium():
    for env in ("CHROME_BIN", "CHROMIUM_BIN", "PUPPETEER_EXECUTABLE_PATH"):
        p = os.environ.get(env)
        if p and os.path.exists(p):
            return p
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome", "headless_shell", "microsoft-edge", "microsoft-edge-stable", "msedge"):
        p = shutil.which(name)
        if p:
            return p
    pats = [
        os.path.join(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"), "chromium*/chrome-linux/chrome"),
        os.path.join(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"), "chromium_headless_shell*/chrome-linux/headless_shell"),
        os.path.expanduser("~/.cache/ms-playwright/chromium*/chrome-linux/chrome"),
        os.path.expanduser("~/.cache/puppeteer/chrome/*/chrome-linux*/chrome"),
        # macOS: Chrome, Chromium, Edge in /Applications or the user's own Applications folder
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        # Windows: Chrome and Edge (Edge is present on every Windows machine), both Program Files folders and per-user installs
        os.path.join(os.environ.get("PROGRAMFILES", r"C:\Program Files"), "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"), "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.environ.get("LOCALAPPDATA", r"C:\Users\Default\AppData\Local"), "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"), "Microsoft", "Edge", "Application", "msedge.exe"),
        os.path.join(os.environ.get("PROGRAMFILES", r"C:\Program Files"), "Microsoft", "Edge", "Application", "msedge.exe"),
    ]
    for pat in pats:
        for p in sorted(glob.glob(pat)):
            if os.path.exists(p):
                return p
    return None


def valid_pdf(path):
    """A real, parseable PDF with at least one page; a stale or truncated file never counts as a result."""
    try:
        with open(path, "rb") as f:
            if f.read(5) != b"%PDF-":
                return False
        from pypdf import PdfReader  # type: ignore
        return len(PdfReader(path).pages) > 0
    except Exception:
        return os.path.exists(path) and os.path.getsize(path) > 1000


def render_with_chromium(bin_path, html_path, pdf_path):
    # --no-sandbox stays: skills run as root in agent sandboxes and Chromium refuses to start without it there.
    # A fresh, temporary profile keeps the user's browser state out of the render and avoids lock files.
    import tempfile
    with tempfile.TemporaryDirectory(prefix="formify-chrome-") as profile:
        for headless, nohf in (("--headless=new", "--no-pdf-header-footer"), ("--headless", "--print-to-pdf-no-header")):
            if os.path.exists(pdf_path):
                os.unlink(pdf_path)
            cmd = [bin_path, headless, "--disable-gpu", "--no-sandbox", nohf,
                   "--run-all-compositor-stages-before-draw", "--virtual-time-budget=4000",
                   "--no-first-run", "--no-default-browser-check", "--disable-background-networking",
                   "--user-data-dir=" + profile,
                   f"--print-to-pdf={pdf_path}", "file://" + os.path.abspath(html_path)]
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                RENDER_LOG.append("chromium %s exit %s: %s" % (headless, r.returncode, (r.stderr or "").strip().splitlines()[-1:] or ""))
            except subprocess.TimeoutExpired:
                RENDER_LOG.append("chromium %s: timeout after 120 s" % headless)
                continue
            except OSError as e:
                RENDER_LOG.append("chromium %s: could not start (%s)" % (headless, e))
                continue
            if valid_pdf(pdf_path):
                return True
    return False


def render_with_weasyprint(html_path, pdf_path):
    try:
        from weasyprint import HTML  # type: ignore
    except Exception:
        RENDER_LOG.append("weasyprint: not installed")
        return False
    try:
        HTML(filename=html_path).write_pdf(pdf_path)
    except Exception as e:
        RENDER_LOG.append("weasyprint: failed (%s)" % e)
        return False
    return os.path.exists(pdf_path)


def render_with_wkhtmltopdf(html_path, pdf_path):
    b = shutil.which("wkhtmltopdf")
    if not b:
        RENDER_LOG.append("wkhtmltopdf: not found")
        return False
    cmd = [b, "--quiet", "--page-size", "A4", "--margin-top", "0", "--margin-bottom", "0",
           "--margin-left", "0", "--margin-right", "0", "--enable-local-file-access", html_path, pdf_path]
    subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return os.path.exists(pdf_path)


RENDER_LOG = []   # one line per renderer tried: found or not, started or not, why it failed


def render(html_path, pdf_path):
    if os.path.exists(pdf_path):
        os.unlink(pdf_path)   # never let an old PDF pass as this run's result
    ch = find_chromium()
    if not ch:
        RENDER_LOG.append("chromium: no Chrome, Chromium or Edge found on this machine")
    elif render_with_chromium(ch, html_path, pdf_path):
        return "chromium"
    else:
        RENDER_LOG.append("chromium: found at %s but produced no PDF (blocked or crashed; see lines above)" % ch)
    if render_with_weasyprint(html_path, pdf_path):
        return "weasyprint"
    if render_with_wkhtmltopdf(html_path, pdf_path):
        return "wkhtmltopdf"
    return None


def count_pages(pdf_path):
    try:
        from pypdf import PdfReader  # type: ignore
        return len(PdfReader(pdf_path).pages)
    except Exception:
        pass
    data = open(pdf_path, "rb").read()
    n = len(re.findall(rb"/Type\s*/Page[^s]", data))
    return n if n > 0 else 1


def role_html(f):
    """Role heading: the role in the master language, then the client's-language role small after a slash."""
    out = html.escape(f.get("role") or "")
    if f.get("role_tr"):
        out += f' <span class="role-tr">/ {html.escape(f["role_tr"])}</span>'
    return out


def build_signature_pages(signers, title, ref, labels):
    """Returns (html, coords, n_pages) for one or more separate signature pages (fallback mode)."""
    pages, coords = [], []
    i = 0
    page_no = 0
    while i < len(signers):
        chunk_simple = signers[i:i + 2 * ROWS_SIMPLE]
        use_id = any(f.get("id_scan") for f in chunk_simple)
        if use_id:
            chunk = signers[i:i + 2 * ROWS_ID]; row_h = ROW_H_ID
        else:
            chunk = chunk_simple; row_h = ROW_H_SIMPLE
        blocks = []
        for k, f in enumerate(chunk):
            col, row = k % 2, k // 2
            x = COL_X[col]
            T = TOP0 + row * row_h
            b = (f'<div class="block" style="left:{x}pt;top:{T}pt;">'
                 f'<div class="role">{role_html(f)}</div>'
                 f'<div class="name">{html.escape(f.get("name") or "")}</div>'
                 f'<div class="label">{html.escape(labels["signature"])}</div>'
                 f'<div class="sig-area"></div>')
            c = {"name": f.get("name"), "role": f.get("role"),
                 "signatureBox": {"x": x, "y": T + 38, "page": page_no, "scale": 1.0}}
            if f.get("id_scan"):
                b += f'<div class="label" style="margin-top:6pt;">{html.escape(labels["id_document"])}</div><div class="id-area"></div>'
                c["idScanBox"] = {"x": x, "y": T + 113, "page": page_no, "scale": 1.0}
            b += "</div>"
            blocks.append(b); coords.append(c)
        sub = html.escape(f"{title}" + (f" · Ref. {ref}" if ref else ""))
        pages.append('<div class="sig-page">'
                     f'<div class="sp-title">{html.escape(labels["signatures"])}</div>'
                     f'<div class="sp-sub">{sub}. {html.escape(labels["signature_page_note"])}</div>'
                     + "".join(blocks) +
                     f'<div class="sp-footer">{sub}. {html.escape(labels["signatures"])} {page_no + 1}.</div>'
                     '</div>')
        i += len(chunk); page_no += 1
    return "".join(pages), coords, page_no


def build_inline_blocks(signers):
    """Signature rows that flow after the text, one row (two signers) per block so that each row can move to
    the next page on its own. Returns (html, relative coords per block)."""
    html_out, rel = [], []
    for i in range(0, len(signers), 2):
        chunk = signers[i:i + 2]
        use_id = any(f.get("id_scan") for f in chunk)
        height = IN_ROW_ID if use_id else IN_ROW_SIMPLE
        parts = [f'<div class="sig-inline" style="height:{height - 20}pt;">'
                 f'<span class="mark">{MARK}{len(rel)}</span>']
        coords = []
        for k, f in enumerate(chunk):
            dx = IN_COLS[k]
            parts.append(f'<div class="block" style="left:{dx}pt;top:0;">'
                         f'<div class="role">{role_html(f)}</div>'
                         f'<div class="name">{html.escape(f.get("name") or "")}</div></div>')
            c = {"name": f.get("name"), "role": f.get("role"), "dx": dx, "dy_sig": IN_HEAD}
            if f.get("id_scan"):
                c["dy_id"] = IN_HEAD + SIG_H + 15
            coords.append(c)
        parts.append("</div>")
        html_out.append("".join(parts)); rel.append(coords)
    return "".join(html_out), rel


def locate_marks(pdf_path, n, mark=MARK, right_edge=False):
    """Finds the <mark><k> markers in the PDF. Returns {k: (page, x_pt, y_baseline_pt)} or None.
    pdfplumber first (exact word positions); pypdf as fallback (text matrix).
    right_edge=True returns the marker's right edge instead of its left (pdfplumber only)."""
    found = {}
    try:
        import pdfplumber  # type: ignore
        with pdfplumber.open(pdf_path) as pdf:
            for pi, page in enumerate(pdf.pages):
                for w in page.extract_words(x_tolerance=1, y_tolerance=1):
                    if mark in w["text"]:
                        for m in re.finditer(mark + r"(\d+)", w["text"]):
                            found.setdefault(int(m.group(1)), (pi, float(w["x1"] if right_edge else w["x0"]), float(w["top"]) + 1.0))
        if len(found) == n:
            return found
        found = {}
    except Exception:
        found = {}
    if right_edge:
        return None
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return None
    try:
        reader = PdfReader(pdf_path)
        for pi, page in enumerate(reader.pages):
            h = float(page.mediabox.height)
            hits = []
            def visitor(text, cm, tm, fontdict, fontsize):
                if mark in text:
                    x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
                    y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
                    hits.append((text, x, y))
            page.extract_text(visitor_text=visitor)
            for text, x, y in hits:
                for m in re.finditer(mark + r"(\d+)", text):
                    found.setdefault(int(m.group(1)), (pi, x, h - y))
    except Exception:
        return None
    return found if len(found) == n else None


FIELD_MARK = "FIELDMARK"
FIELD_END = "FIELDEND"
FIELD_H = 13


def flags(c):
    return (1 if c.get("read_only") else 0) | (2 if c.get("required", True) and not c.get("read_only") else 0)


def add_form_fields(pdf_path, fields):
    """Creates one AcroForm text field per <span class="pdf-field"> blank (formify-pdf-forms recipe:
    widget + /AcroForm /Fields + /P, pre-built /AP /N appearance, /DR with Helvetica, NeedAppearances false).
    fields: list of {"name", "width", "height", "read_only", "required"} in marker order. Returns the created list or None.
    /Ff bit 1 = read only (scan buttons, images), bit 2 = required."""
    try:
        from pypdf import PdfReader, PdfWriter  # type: ignore
        from pypdf.generic import (ArrayObject, BooleanObject, DictionaryObject, FloatObject, NameObject,  # type: ignore
                                   NumberObject, RectangleObject, StreamObject, TextStringObject)
    except Exception:
        return None
    marks = locate_marks(pdf_path, len(fields), FIELD_MARK)
    if not marks:
        return None
    ends = locate_marks(pdf_path, len(fields), FIELD_END, right_edge=True) or {}   # right edge of the rendered blank, when present
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    writer.append(reader)
    root = writer._root_object
    if "/AcroForm" not in root:
        root[NameObject("/AcroForm")] = writer._add_object(DictionaryObject())
    acro = root["/AcroForm"].get_object()
    acro[NameObject("/DA")] = TextStringObject("/Helv 9 Tf 0 g")
    helv = DictionaryObject()
    helv[NameObject("/Type")] = NameObject("/Font"); helv[NameObject("/Subtype")] = NameObject("/Type1")
    helv[NameObject("/BaseFont")] = NameObject("/Helvetica"); helv[NameObject("/Encoding")] = NameObject("/WinAnsiEncoding")
    fonts = DictionaryObject(); fonts[NameObject("/Helv")] = writer._add_object(helv)
    dr = DictionaryObject(); dr[NameObject("/Font")] = fonts
    acro[NameObject("/DR")] = dr
    acro[NameObject("/NeedAppearances")] = BooleanObject(False)
    if "/Fields" not in acro:
        acro[NameObject("/Fields")] = ArrayObject()
    created = []
    parents = {}   # name -> parent dict when the same field has several widgets
    from collections import Counter
    repeated = {n for n, cnt in Counter(c["name"] for c in fields).items() if cnt > 1}
    for k, c in enumerate(fields):
        pg, x, y_top = marks[k]
        page = writer.pages[pg]
        h = float(page.mediabox.height)
        w = float(c.get("width", 160))
        if k in ends and ends[k][0] == pg and ends[k][1] > x + 10:
            w = min(w, ends[k][1] - x)   # never wider than the cell it sits in
        fh = float(c.get("height") or FIELD_H)
        x1, y2 = x, h - (y_top - 1.0)        # the marker sits at the top edge of the blank
        x2, y1 = x1 + w, y2 - fh
        ap = StreamObject()
        if fh > FIELD_H:   # tall field (scanned document image): white with a thin grey border
            ap.set_data(("q 1 1 1 rg 0 0 %.2f %.2f re f Q q 0.6 G 0.5 w 0.25 0.25 %.2f %.2f re S Q" % (w, fh, w - 0.5, fh - 0.5)).encode("latin-1"))
        else:
            ap.set_data(("q 1 1 1 rg 0 0 %.2f %.2f re f Q" % (w, fh)).encode("latin-1"))  # white background, no border: the document already prints the line
        ap[NameObject("/Type")] = NameObject("/XObject"); ap[NameObject("/Subtype")] = NameObject("/Form")
        ap[NameObject("/FormType")] = NumberObject(1)
        ap[NameObject("/BBox")] = ArrayObject([NumberObject(0), NumberObject(0), FloatObject(w), FloatObject(fh)])
        ap[NameObject("/Resources")] = DictionaryObject()
        apd = DictionaryObject(); apd[NameObject("/N")] = writer._add_object(ap)
        f = DictionaryObject()
        f[NameObject("/Type")] = NameObject("/Annot"); f[NameObject("/Subtype")] = NameObject("/Widget")
        f[NameObject("/F")] = NumberObject(4)
        f[NameObject("/Rect")] = RectangleObject([round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)])
        f[NameObject("/DA")] = TextStringObject("/Helv 9 Tf 0 g"); f[NameObject("/Q")] = NumberObject(0)
        mk = DictionaryObject(); mk[NameObject("/BG")] = ArrayObject([FloatObject(1.0)] * 3)
        f[NameObject("/MK")] = mk
        f[NameObject("/AP")] = apd
        f[NameObject("/P")] = page.indirect_reference
        label = c.get("label") or c["name"].split("|")[0].replace("_", " ")
        if c["name"] in repeated:
            if c["name"] not in parents:
                parent = DictionaryObject()
                parent[NameObject("/FT")] = NameObject("/Tx"); parent[NameObject("/T")] = TextStringObject(c["name"])
                parent[NameObject("/TU")] = TextStringObject(label)
                parent[NameObject("/Ff")] = NumberObject(flags(c))
                parent[NameObject("/V")] = TextStringObject(""); parent[NameObject("/DV")] = TextStringObject("")
                parent[NameObject("/DA")] = TextStringObject("/Helv 9 Tf 0 g")
                parent[NameObject("/Kids")] = ArrayObject()
                parents[c["name"]] = writer._add_object(parent)
                acro["/Fields"].append(parents[c["name"]])
            f[NameObject("/Parent")] = parents[c["name"]]
            f[NameObject("/Ff")] = NumberObject(flags(c))
            ref = writer._add_object(f)
            parents[c["name"]].get_object()["/Kids"].append(ref)
        else:
            f[NameObject("/FT")] = NameObject("/Tx"); f[NameObject("/T")] = TextStringObject(c["name"])
            f[NameObject("/TU")] = TextStringObject(label)
            f[NameObject("/Ff")] = NumberObject(flags(c))
            f[NameObject("/V")] = TextStringObject(""); f[NameObject("/DV")] = TextStringObject("")
            ref = writer._add_object(f)
            acro["/Fields"].append(ref)
        if "/Annots" not in page:
            page[NameObject("/Annots")] = ArrayObject()
        page["/Annots"].append(ref)
        created.append({"name": c["name"], "page": pg, "x": int(round(x1)), "y": int(round(y_top)), "width": int(w), "height": int(fh)})
    with open(pdf_path, "wb") as fh:
        writer.write(fh)
    return created


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True, help="body HTML (without <html>/<head>) or a full document")
    ap.add_argument("--signers", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--profile", default="professional", choices=["official", "professional", "light"])
    ap.add_argument("--css", default=DEFAULT_CSS)
    ap.add_argument("--config", default=DEFAULT_CONFIG, help="segment.json with the footer texts")
    ap.add_argument("--title", default="Document")
    ap.add_argument("--ref", default="")
    ap.add_argument("--no-signatures", action="store_true", help="no signature areas (e.g. a review draft)")
    ap.add_argument("--signature-page", action="store_true", help="signatures on a separate page instead of after the text")
    ap.add_argument("--lang", default="", help="client's language code for the footer credit line (from segment.json)")
    ap.add_argument("--credit-tr", default="", help="credit line in the client's language when it is not in segment.json")
    ap.add_argument("--no-credit", action="store_true", help="omit the Formify credit line")
    ap.add_argument("--no-fallback", action="store_true", help="do not fall back to the standard-library PDF when no renderer exists")
    a = ap.parse_args()

    cfg = load_config(a.config)
    footer = cfg.get("footer", {})
    credits = footer.get("credit", {})
    master = cfg.get("master_language", "en")
    labels = {"signature": "Signature", "id_document": "Identity document", "signatures": "Signatures",
              "signature_page_note": "Each signer signs in the space indicated. Signatures are collected electronically."}
    labels.update(cfg.get("signature_labels", {}))

    body = open(a.html, encoding="utf-8").read()
    css = open(a.css, encoding="utf-8").read()
    signers = json.load(open(a.signers, encoding="utf-8"))
    if isinstance(signers, dict):
        signers = signers.get("signers", [])
    m = re.search(r"<body[^>]*>(.*)</body>", body, re.S | re.I)
    if m:
        body = m.group(1)

    sig_html, coords, n_sig_pages = ("", [], 0)
    inline_rel = []
    if not a.no_signatures:
        if a.signature_page:
            sig_html, coords, n_sig_pages = build_signature_pages(signers, a.title, a.ref, labels)
        else:
            sig_html, inline_rel = build_inline_blocks(signers)

    # Footer in the bottom margin of every page (CSS margin boxes: Chromium 131+, WeasyPrint)
    lines = [a.title + (f" · Ref. {a.ref}" if a.ref else "")]
    if not a.no_credit:
        parts = [credits.get(master, "")]
        tr = a.credit_tr or (credits.get(a.lang.lower()[:2], "") if a.lang else "")
        if tr and tr != parts[0]:
            parts.append(tr)
        lines.append("  ·  ".join(p for p in parts if p))
    def css_str(t):
        return t.replace("\\", "\\\\").replace('"', '\\"')
    footer_css = ('@page { @bottom-center { content: "' + "\\A ".join(css_str(l) for l in lines) +
                  '"; white-space: pre; font-family: Arial, Helvetica, sans-serif; font-size: 6.5pt; line-height: 8.5pt; text-align: center; vertical-align: top; padding-top: 4pt; } }')

    def build_full(sig):
        # If the template marks where the signatures go (<!-- SIGNATURES -->, e.g. before an annex), insert
        # them there; otherwise right after the last paragraph.
        if "<!-- SIGNATURES -->" in body and "sig-inline" in sig:
            content = body.replace("<!-- SIGNATURES -->", sig); sig = ""
        else:
            content = body.replace("<!-- SIGNATURES -->", "")
        return (f'<!DOCTYPE html><html lang="{master}"><head><meta charset="utf-8"><title>{html.escape(a.title)}</title>'
                f"<style>{css}\n{footer_css}</style></head><body class=\"{a.profile}\">"
                f'<div class="content">{content}</div>{sig}</body></html>')
    full = build_full(sig_html)

    out_dir = os.path.dirname(os.path.abspath(a.out)) or "."
    os.makedirs(out_dir, exist_ok=True)
    full_html_path = os.path.splitext(os.path.abspath(a.out))[0] + ".html"
    open(full_html_path, "w", encoding="utf-8").write(full)

    engine = render(full_html_path, a.out)
    if not engine:
        print("No renderer could produce the PDF. What was tried:", file=sys.stderr)
        for line in RENDER_LOG:
            print("  " + line, file=sys.stderr)
        spec_path = os.path.splitext(os.path.abspath(a.out))[0] + "-spec.md"
        here = os.path.dirname(os.path.abspath(__file__))
        credit_line = "  \u00b7  ".join(p for p in ([credits.get(master, "")] + ([a.credit_tr or credits.get(a.lang.lower()[:2], "")] if a.lang or a.credit_tr else [])) if p) if not a.no_credit else ""
        cmd = [sys.executable, os.path.join(here, "stdlib_pdf.py"), "--html", a.html, "--signers", a.signers, "--out", a.out,
               "--title", a.title, "--ref", a.ref, "--footer", credit_line, "--labels", json.dumps(labels, ensure_ascii=False)]
        if a.no_signatures:
            cmd.append("--no-signatures")
        if a.no_fallback:
            rc = 2
        else:
            rc = subprocess.run(cmd, stdout=subprocess.DEVNULL).returncode
        subprocess.run([sys.executable, os.path.join(here, "handover.py"), "--html", a.html, "--signers", a.signers,
                        "--out", spec_path, "--title", a.title,
                        "--reason", ("Built with the standard library (route 3): same text and fields, plain layout. This specification lets anyone check it."
                                     if rc == 0 else "No renderer here and the text needs characters the standard-library route cannot carry, so this is the complete specification.")],
                       stdout=subprocess.DEVNULL)
        if rc == 0:
            print(f"Route 3: standard-library PDF written to {a.out} (plain one-column layout, same text, fields and signature areas). Hand-over specification next to it: {spec_path}. Tell the user which route produced the file.", file=sys.stderr)
            print(open(os.path.splitext(os.path.abspath(a.out))[0] + ".signatures.json", encoding="utf-8").read())
            sys.exit(0)
        print(f"Route 5: hand-over written to {spec_path} (document text plus field specification). Full HTML at: {full_html_path}.", file=sys.stderr)
        sys.exit(2)

    total = count_pages(a.out)
    # PDF form fields for <span class="pdf-field"> blanks (the other party fills them in when signing)
    fields_html = []
    for m in re.finditer(r'<span class="pdf-field[^"]*"([^>]*)>', body):
        attrs = dict(re.findall(r'data-(\w+)="([^"]*)"', m.group(1)))
        if "name" not in attrs:
            continue
        fields_html.append({"name": html.unescape(attrs["name"]), "width": int(attrs.get("width", 160)),
                            "height": int(attrs["height"]) if attrs.get("height") else FIELD_H,
                            "read_only": attrs.get("readonly") == "1", "required": attrs.get("required") != "0"})
    fields_pdf = []
    if fields_html:
        created = add_form_fields(a.out, fields_html)
        if created is None:
            print("Notice: form fields could not be created (pypdf missing or blanks not located).", file=sys.stderr)
        else:
            fields_pdf = created
    mode = "page"
    if inline_rel:
        marks = locate_marks(a.out, len(inline_rel))
        if marks:
            mode = "inline"
            coords = []
            for k, block in enumerate(inline_rel):
                pg, x0, y0 = marks[k]
                y0 = y0 - 1.0  # the marker is 1 pt high and its baseline sits 1 pt below the block's top edge
                for c in block:
                    d = {"name": c["name"], "role": c["role"],
                         "signatureBox": {"x": int(round(x0 + c["dx"])), "y": int(round(y0 + c["dy_sig"])), "page": pg, "scale": 1.0}}
                    if "dy_id" in c:
                        d["idScanBox"] = {"x": int(round(x0 + c["dx"])), "y": int(round(y0 + c["dy_id"])), "page": pg, "scale": 1.0}
                    coords.append(d)
        else:
            sig_html, coords, n_sig_pages = build_signature_pages(signers, a.title, a.ref, labels)
            full = build_full(sig_html)
            open(full_html_path, "w", encoding="utf-8").write(full)
            engine = render(full_html_path, a.out)
            total = count_pages(a.out)
            print("Notice: pypdf is not available; signatures on a separate page.", file=sys.stderr)
    if mode == "page":
        first_sig_page = total - n_sig_pages
        for c in coords:
            c["signatureBox"]["page"] += first_sig_page
            if "idScanBox" in c:
                c["idScanBox"]["page"] += first_sig_page

    result = {"pdf": os.path.abspath(a.out), "html": full_html_path, "engine": engine, "signature_mode": mode,
              "pages": total, "page_size_pt": [A4_W, A4_H], "signers": coords, "form_fields": fields_pdf}
    sig_path = os.path.splitext(os.path.abspath(a.out))[0] + ".signatures.json"
    json.dump(result, open(sig_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
