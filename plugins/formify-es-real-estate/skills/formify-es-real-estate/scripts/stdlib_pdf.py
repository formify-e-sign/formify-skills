#!/usr/bin/env python3
"""Route 3 of the PDF ladder: a fillable PDF from the Python standard library alone.

Used by render_pdf.py when no renderer (browser, WeasyPrint, wkhtmltopdf) exists on the machine.
Same text, same form fields, same signature areas as the rendered document; plainer layout
(Helvetica, one column, tables as label: value lines). Nothing is installed, nothing outside the
standard library is imported. The writer follows the developer's recipe (formify-pdf-forms,
references/stdlib-pdf.md): NeedAppearances, /Ff flags, WinAnsi text, empty signature space.

    python3 scripts/stdlib_pdf.py --html body.html --signers signers.json --out "<title>.pdf" \
        --title "<title>" --ref "<ref>" [--footer "credit line"]

Writes <title>.pdf and <title>.signatures.json (same shape as render_pdf.py, engine "stdlib").
Exit 3 when the text needs characters outside WinAnsi (the file would carry "?"): then only the
hand-over (scripts/handover.py) is the deliverable.
"""
import argparse
import html as htmlmod
import json
import os
import re
import sys
from html.parser import HTMLParser

PAGE_W, PAGE_H = 595, 842
MARGIN = 56
SIZE, LEAD = 10, 14
FIELD_H = 18
LABEL_W = 150
SIGN_W, SIGN_H = 219, 58
ID_W, ID_H = 218, 138
TEXT_W = PAGE_W - 2 * MARGIN
# Helvetica average glyph width at 10 pt is close to 5.0 pt: 483 pt of text width holds about 95 chars.
WRAP_CHARS = int(TEXT_W / (SIZE * 0.5))


# ---------------------------------------------------------------------------------------------
# HTML -> blocks. The body HTML the templates produce is tables (header, form, terms) plus h1/h2/p.
# ---------------------------------------------------------------------------------------------
class Blocks(HTMLParser):
    """Linear reading order: ('h', level, text) | ('p', text) | ('row', [cells]) | ('sig',)
    A cell is {'text': str, 'fields': [field dicts], 'k': bool}. Field tokens {{name}} sit in the text."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = []
        self.fields = []
        self._h = None
        self._p = None
        self._row = None
        self._cell = None
        self._in_field = None
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "")
        if tag in ("style", "script"):
            self._skip += 1
            return
        if tag in ("h1", "h2", "h3", "h4"):
            self._h = [int(tag[1]), ""]
        elif tag in ("p", "li", "div"):
            if self._cell is None and self._row is None:
                self._p = "" if tag != "li" else "• "
        elif tag == "tr":
            self._row = []
        elif tag in ("td", "th"):
            self._cell = {"text": "", "fields": [], "k": "k" in cls.split() or tag == "th", "cab": "cab" in cls.split()}
        elif tag == "span" and "pdf-field" in cls:
            name = htmlmod.unescape(a.get("data-name", ""))
            f = {"name": name, "width": int(a.get("data-width", 160) or 160),
                 "height": int(a["data-height"]) if a.get("data-height") else FIELD_H,
                 "read_only": a.get("data-readonly") == "1", "required": a.get("data-required") != "0"}
            if self._cell is not None:
                hint = re.split(r"\{\{[^}]*\}\}", self._cell["text"])[-1]
                f["label_hint"] = norm(hint)
            self._in_field = f
            self._append("{{" + name + "}}")
            if self._cell is not None:
                self._cell["fields"].append(f)
            self.fields.append(f)
        elif tag == "br":
            self._append(" ")

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self._skip = max(0, self._skip - 1)
            return
        if tag in ("h1", "h2", "h3", "h4") and self._h:
            t = norm(self._h[1])
            if t:
                self.blocks.append(("h", self._h[0], t))
            self._h = None
        elif tag in ("p", "li", "div") and self._p is not None and self._cell is None and self._row is None:
            t = norm(self._p)
            if t and t != "•":
                self.blocks.append(("p", t))
            self._p = None
        elif tag in ("td", "th") and self._cell is not None:
            self._cell["text"] = norm(self._cell["text"])
            if self._row is not None:
                self._row.append(self._cell)
            self._cell = None
        elif tag == "tr" and self._row is not None:
            if any(c["text"] or c["fields"] for c in self._row):
                self.blocks.append(("row", self._row))
            self._row = None
        elif tag == "span" and self._in_field:
            self._in_field = None

    def handle_comment(self, data):
        if "SIGNATURES" in data:
            self.blocks.append(("sig",))

    def handle_data(self, data):
        if self._skip or self._in_field:
            return
        self._append(data)

    def _append(self, s):
        if self._h is not None:
            self._h[1] += s
        elif self._cell is not None:
            self._cell["text"] += s
        elif self._p is not None:
            self._p += s


def norm(s):
    return re.sub(r"\s+", " ", s.replace(" ", " ")).strip()


def parse_blocks(body_html):
    m = re.search(r"<body[^>]*>(.*)</body>", body_html, re.S | re.I)
    if m:
        body_html = m.group(1)
    p = Blocks()
    p.feed(body_html)
    p.close()
    return p.blocks, p.fields


# ---------------------------------------------------------------------------------------------
# PDF writer (standard library only)
# ---------------------------------------------------------------------------------------------
def esc(s):
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def wrap(text, width_chars=WRAP_CHARS):
    lines, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > width_chars:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + [cur] if cur else lines


class Form:
    def __init__(self, footer_lines):
        self.pages = [[]]
        self.annots = [[]]
        self.y = PAGE_H - MARGIN
        self.footer_lines = footer_lines
        self.widgets = []      # (name, page, x, y_top, w, h) in top-origin coordinates
        self.signers = []      # dicts for signatures.json

    @property
    def page(self):
        return len(self.pages) - 1

    def _need(self, h):
        if self.y - h < MARGIN + 24:   # 24 pt reserved for the footer
            self.pages.append([])
            self.annots.append([])
            self.y = PAGE_H - MARGIN

    def _text(self, x, y, s, size=SIZE, bold=False):
        self.pages[-1].append("BT /%s %d Tf %d %d Td (%s) Tj ET" % ("F2" if bold else "F1", size, x, y, esc(s)))

    def heading(self, text, level):
        size = {1: SIZE + 5, 2: SIZE + 2}.get(level, SIZE + 1)
        self._need(LEAD * 2)
        self.y -= LEAD // 2
        for line in wrap(text, int(TEXT_W / (size * 0.55))):
            self._need(size + 4)
            self._text(MARGIN, self.y - size, line, size, bold=True)
            self.y -= size + 4
        self.y -= LEAD // 2

    def para(self, text, indent=0, bold=False):
        for line in wrap(text, WRAP_CHARS - indent // 5):
            self._need(LEAD)
            self._text(MARGIN + indent, self.y - SIZE, line, bold=bold)
            self.y -= LEAD
        self.y -= LEAD // 3

    def text_field(self, f, label):
        """Label on its own line, the field box below it, never wider than the text column."""
        h = max(f["height"], FIELD_H)
        w = min(max(f["width"], 60), TEXT_W)
        lines = wrap(label)[:2]
        self._need(len(lines) * LEAD + h + LEAD)
        for line in lines:
            self._text(MARGIN, self.y - SIZE, line, SIZE - 1)
            self.y -= LEAD - 2
        top = self.y - 2
        bottom = top - h
        ff = (2 if f["required"] and not f["read_only"] else 0) | (1 if f["read_only"] else 0)
        x0 = MARGIN
        self.annots[-1].append(
            "<< /Type /Annot /Subtype /Widget /FT /Tx /T (%s) /V () /Ff %d /F 4 /P {P} 0 R "
            "/Rect [%d %d %d %d] /DA (/Helv %d Tf 0 g) /MK << /BC [0.6 0.6 0.6] /BG [0.96 0.96 0.96] >> >>"
            % (esc(f["name"]), ff, x0, bottom, x0 + w, top, SIZE - 1))
        # a light box in the page content too, so the blank is visible in viewers that draw no appearances
        self.pages[-1].append("q 0.7 G 0.5 w %d %d %d %d re S Q" % (x0, bottom, w, h))
        self.widgets.append({"name": f["name"], "page": self.page, "x": x0, "y": PAGE_H - top, "w": w, "h": h})
        self.y = bottom - LEAD // 2

    def signature(self, signer, labels):
        """Empty space plus captions. No box, no line, no widget: Formify paints the signature here."""
        id_scan = bool(signer.get("id_scan"))
        gap = (ID_H if id_scan else SIGN_H) + 12
        caption = signer.get("role", "")
        if signer.get("role_tr") and signer["role_tr"] != caption:
            caption2 = signer["role_tr"]
        else:
            caption2 = ""
        need = gap + LEAD * 3
        self._need(need)
        self._text(MARGIN, self.y - SIZE, caption, bold=True)
        self.y -= LEAD
        if caption2:
            self._text(MARGIN, self.y - SIZE + 2, caption2, SIZE - 2)
            self.y -= LEAD - 2
        if id_scan:
            self._text(MARGIN + SIGN_W + 16, self.y - SIZE, labels.get("id_document", "Identity document"), SIZE - 1)
        top = self.y - 4
        d = {"name": signer.get("name", ""), "role": caption,
             "signatureBox": {"x": MARGIN, "y": int(PAGE_H - top), "page": self.page, "scale": 1.0}}
        if id_scan:
            d["idScanBox"] = {"x": MARGIN + SIGN_W + 16, "y": int(PAGE_H - top), "page": self.page, "scale": 1.0}
        self.signers.append(d)
        self.y = top - gap
        self._text(MARGIN, self.y - 2, labels.get("signature", "Signature"), SIZE - 2)
        self.y -= LEAD * 2

    def write(self, path):
        objs = {}
        objs[3] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
        objs[4] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
        next_id, page_ids, widget_ids = 5, [], []
        n_pages = len(self.pages)
        for i, (content, annots) in enumerate(zip(self.pages, self.annots)):
            foot = list(self.footer_lines) + ["%d / %d" % (i + 1, n_pages)]
            y = MARGIN - 14
            for line in foot:
                content = content + ["BT /F1 6.5 Tf %d %d Td (%s) Tj ET" % (MARGIN, y, esc(line))]
                y -= 8
            pid, cid = next_id, next_id + 1
            wids = list(range(cid + 1, cid + 1 + len(annots)))
            next_id = cid + 1 + len(annots)
            page_ids.append(pid)
            widget_ids += wids
            stream = "\n".join(content).encode("cp1252", "strict")
            objs[cid] = b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream"
            objs[pid] = ("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] "
                         "/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents %d 0 R /Annots [%s] >>"
                         % (PAGE_W, PAGE_H, cid, " ".join("%d 0 R" % w for w in wids))).encode("latin-1")
            for w, a in zip(wids, annots):
                objs[w] = a.replace("{P}", str(pid)).encode("cp1252", "strict")
        objs[1] = ("<< /Type /Catalog /Pages 2 0 R /AcroForm << /Fields [%s] /DA (/Helv 0 Tf 0 g) "
                   "/DR << /Font << /Helv 3 0 R >> >> /NeedAppearances true >> >>"
                   % " ".join("%d 0 R" % w for w in widget_ids)).encode("latin-1")
        objs[2] = ("<< /Type /Pages /Kids [%s] /Count %d >>"
                   % (" ".join("%d 0 R" % p for p in page_ids), len(page_ids))).encode("latin-1")
        out = bytearray(b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n")
        offsets = {}
        for i in sorted(objs):
            offsets[i] = len(out)
            out += b"%d 0 obj\n" % i + objs[i] + b"\nendobj\n"
        xref, n = len(out), len(objs) + 1
        out += b"xref\n0 %d\n0000000000 65535 f \n" % n
        for i in range(1, n):
            out += b"%010d 00000 n \n" % offsets[i]
        out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (n, xref)
        with open(path, "wb") as fh:
            fh.write(out)
        return len(out)


# ---------------------------------------------------------------------------------------------
def winansi_problems(text):
    bad = set()
    for ch in text:
        try:
            ch.encode("cp1252")
        except UnicodeEncodeError:
            bad.add(ch)
    return sorted(bad)


def field_label(row, f, headers):
    """The label printed beside a field: the row's key cell plus the column heading when the table has one."""
    key = next((c["text"] for c in row if c["k"] and c["text"]), "") or f["name"].split("|")[0].replace("_", " ")
    if f.get("label_hint"):
        key = f["label_hint"][-90:]
    col = next((i for i, c in enumerate(row) if f in c["fields"]), None)
    if col is not None and col < len(headers) and headers[col]:
        return key + " (" + headers[col] + ")"
    return key


def lay_out(blocks, signers, labels, footer_lines, no_signatures=False):
    form = Form(footer_lines)
    sig_done = False
    headers = []
    for b in blocks:
        kind = b[0]
        if kind == "h":
            form.heading(b[2], b[1])
        elif kind == "p":
            form.para(b[1])
        elif kind == "sig" and not no_signatures and not sig_done:
            for s in signers:
                form.signature(s, labels)
            sig_done = True
        elif kind == "row":
            cells = b[1]
            if any(c.get("cab") for c in cells):
                headers = [c["text"] for c in cells]
                form.para(" \u00b7 ".join(t for t in headers if t), bold=True)
                continue
            key = next((c for c in cells if c["k"]), None)
            others = [c for c in cells if not c["k"]]
            fields_in_row = [f for c in cells for f in c["fields"]]
            texts = []
            for c in others:
                t = re.sub(r"\{\{[^}]*\}\}", "", c["text"]).strip()
                if c["fields"] and t and all(t.startswith(f.get("label_hint", "\0")) or t == f.get("label_hint") for f in c["fields"]) and len(t) <= 90:
                    continue      # the text is the field's own label: printed with the field, not as a row line
                if t:
                    texts.append(t)
            long = any(len(t) > 80 for t in texts) or (key and len(key["text"]) > 80)
            if long:
                if key and key["text"]:
                    form.para(key["text"], bold=True)
                for t in texts:
                    form.para(t, indent=12)
            elif texts or not fields_in_row:
                line = " · ".join(texts)
                if key and key["text"]:
                    line = key["text"] + (": " + line if line else "")
                if line:
                    form.para(line)
            for f in fields_in_row:
                form.text_field(f, field_label(cells, f, headers))
    if not no_signatures and not sig_done:
        form.para("")
        for s in signers:
            form.signature(s, labels)
    return form


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--signers", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="Document")
    ap.add_argument("--ref", default="")
    ap.add_argument("--footer", default="", help="credit line(s), separated by ' | '")
    ap.add_argument("--labels", default="", help="JSON with signature/id_document labels")
    ap.add_argument("--no-signatures", action="store_true")
    a = ap.parse_args()

    body = open(a.html, encoding="utf-8").read()
    signers = json.load(open(a.signers, encoding="utf-8"))
    if isinstance(signers, dict):
        signers = signers.get("signers", [])
    labels = {"signature": "Signature", "id_document": "Identity document"}
    if a.labels:
        labels.update(json.loads(a.labels))
    blocks, fields = parse_blocks(body)

    all_text = " ".join(x for b in blocks for x in (b[1:] if b[0] != "row" else [c["text"] for c in b[1]]) if isinstance(x, str))
    all_text += " ".join(s.get("role", "") + s.get("role_tr", "") for s in signers)
    bad = winansi_problems(all_text)
    if bad:
        print("stdlib route cannot carry these characters (Helvetica WinAnsi): " + " ".join(bad), file=sys.stderr)
        print("The file would print '?' for them. Use the hand-over (scripts/handover.py) instead.", file=sys.stderr)
        sys.exit(3)

    footer_lines = [a.title + (" · Ref. " + a.ref if a.ref else "")]
    if a.footer:
        footer_lines.append(a.footer)
    form = lay_out(blocks, signers, labels, footer_lines, a.no_signatures)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    size = form.write(a.out)

    result = {"pdf": os.path.abspath(a.out), "html": os.path.abspath(a.html), "engine": "stdlib",
              "signature_mode": "inline", "pages": len(form.pages), "page_size_pt": [PAGE_W, PAGE_H],
              "signers": form.signers,
              "form_fields": [{"name": w["name"], "page": w["page"], "x": w["x"], "y": w["y"], "width": w["w"], "height": w["h"]}
                              for w in form.widgets],
              "note": "Standard-library PDF (route 3): same text and fields, plain one-column layout."}
    sig_path = os.path.splitext(os.path.abspath(a.out))[0] + ".signatures.json"
    json.dump(result, open(sig_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("wrote %d bytes" % size, file=sys.stderr)


if __name__ == "__main__":
    main()
