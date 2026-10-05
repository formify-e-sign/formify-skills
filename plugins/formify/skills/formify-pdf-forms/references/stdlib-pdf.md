# A fillable PDF from the standard library alone

Step 5, rung 3. Use this when no already-present library from the closed list can complete
the selected route, but `python3` answers with
a version. Nothing is installed. The script below was run unchanged on Python 3.9.6 (a Mac
with the developer tools and nothing else) and on 3.12, produced byte-identical files, and
`pypdf` read every field back with the right type and flags. Preview, Chrome and Acrobat
draw the fields because the file asks the viewer to build appearances.

## What it can and cannot do

| Can | Cannot |
|---|---|
| Text fields, multi-line text, checkboxes, dropdowns | Radio groups — use a dropdown or one checkbox per option |
| Required and read-only flags | Images, logos, letterheads |
| Any number of pages, plain paragraphs and headings | Typeset layout: the wrap is by character count |
| `tink-*` attributes: they are only a field name | Fonts other than Helvetica |
| Western European characters: `š ž å ä ö é ü ñ` | `č ć đ ł ř ő` — Helvetica in WinAnsi has no glyph, and the file replaces them with `?` |

That last line decides. Croatian, Polish, Czech or Hungarian page text needs an embedded
font, which is rung 4 with the user's yes or rung 5. Do not ship a document with `?` in it.

## Rules the script already follows — keep them when you change it

- **Field names are ASCII** and unique; the `tink-*` catalogue goes in the name with its
  brackets. Labels, headings and paragraphs may carry any WinAnsi character.
- **Signature space is empty**: a gap and a caption, no box, no line, no widget. The gap is
  70 points; 58 is the minimum Formify's signature field needs.
- `NeedAppearances true` is what makes viewers draw fields that have no appearance stream.
  Checkboxes do carry one, shared, because most viewers will not invent a tick mark.
- Flags: `/Ff 2` required, `4096` multi-line, `131072` combo box. Read-only is `1`, and
  every trigger and auto-filled field gets it.
- `(`, `)` and `\` are escaped in every string; nothing else needs escaping.

## The script

```python
"""Write a fillable PDF with nothing outside the Python standard library (3.6 or newer).

Edit the example at the bottom, then:  python3 make_form.py out.pdf
"""
import sys

PAGE_W, PAGE_H = 595, 842      # A4 in points. US Letter is 612 x 792.
MARGIN = 56                    # 20 mm
SIZE, LEAD = 11, 16            # font size and line height
FIELD_H = 20                   # height of a one-line field
SIGN_H = 70                    # empty space reserved per signature (58 pt is the minimum)
LABEL_W = 150                  # label column; the field starts to its right


def esc(s):
    """Escape the three characters that break a PDF string."""
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def wrap(text, width_chars=88):
    """Word-wrap for 11 pt Helvetica across the A4 text width. Good enough, not typeset."""
    lines, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > width_chars:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + [cur] if cur else lines


class Form:
    def __init__(self):
        self.pages = [[]]      # per page: content-stream lines
        self.annots = [[]]     # per page: widget dictionaries, "{P}" stands for the page id
        self.y = PAGE_H - MARGIN

    # ---- layout -------------------------------------------------------------------
    def _need(self, h):
        if self.y - h < MARGIN:
            self.pages.append([])
            self.annots.append([])
            self.y = PAGE_H - MARGIN

    def _text(self, x, y, s, size=SIZE):
        self.pages[-1].append("BT /F1 %d Tf %d %d Td (%s) Tj ET" % (size, x, y, esc(s)))

    def heading(self, text):
        self._need(LEAD * 2)
        self._text(MARGIN, self.y - 4, text, SIZE + 4)
        self.y -= LEAD * 2

    def para(self, text):
        for line in wrap(text):
            self._need(LEAD)
            self._text(MARGIN, self.y, line)
            self.y -= LEAD
        self.y -= LEAD // 2

    # ---- fields -------------------------------------------------------------------
    def text_field(self, name, label, required=False, multiline=False, lines=1):
        h = LEAD * lines + 8 if multiline else FIELD_H
        self._need(h + LEAD // 2)
        top, bottom = self.y, self.y - h
        self._text(MARGIN, top - SIZE - 3, label)
        ff = (2 if required else 0) | (4096 if multiline else 0)
        self.annots[-1].append(
            "<< /Type /Annot /Subtype /Widget /FT /Tx /T (%s) /V () /Ff %d /F 4 /P {P} 0 R "
            "/Rect [%d %d %d %d] /DA (/Helv %d Tf 0 g) /MK << /BC [0.6 0.6 0.6] >> >>"
            % (esc(name), ff, MARGIN + LABEL_W, bottom, PAGE_W - MARGIN, top, SIZE))
        self.y = bottom - LEAD // 2

    def checkbox(self, name, label, required=False):
        self._need(20 + LEAD // 2)
        top, bottom = self.y, self.y - 20
        self.annots[-1].append(
            "<< /Type /Annot /Subtype /Widget /FT /Btn /T (%s) /V /Off /AS /Off /Ff %d /F 4 /P {P} 0 R "
            "/Rect [%d %d %d %d] /MK << /BC [0 0 0] >> /AP << /N << /Yes 4 0 R /Off 5 0 R >> >> >>"
            % (esc(name), 2 if required else 0, MARGIN, bottom, MARGIN + 20, top))
        self._text(MARGIN + 28, bottom + 5, label)
        self.y = bottom - LEAD // 2

    def dropdown(self, name, label, options, required=False):
        self._need(FIELD_H + LEAD // 2)
        top, bottom = self.y, self.y - FIELD_H
        self._text(MARGIN, top - SIZE - 3, label)
        opts = " ".join("(%s)" % esc(o) for o in options)
        ff = 131072 | (2 if required else 0)          # combo box
        self.annots[-1].append(
            "<< /Type /Annot /Subtype /Widget /FT /Ch /T (%s) /Ff %d /Opt [%s] /V () /F 4 /P {P} 0 R "
            "/Rect [%d %d %d %d] /DA (/Helv %d Tf 0 g) /MK << /BC [0.6 0.6 0.6] >> >>"
            % (esc(name), ff, opts, MARGIN + LABEL_W, bottom, PAGE_W - MARGIN, top, SIZE))
        self.y = bottom - LEAD // 2

    def signature(self, caption):
        """Empty space plus a caption. No box, no line, no widget: Formify paints the signature here."""
        self._need(SIGN_H + LEAD * 2)
        self.y -= SIGN_H
        self._text(MARGIN, self.y, caption)
        self.y -= LEAD * 2

    # ---- serialisation ------------------------------------------------------------
    def write(self, path):
        objs = {}
        objs[3] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
        on = b"q 0 g 1 w 0.5 0.5 19 19 re S 3 3 m 17 17 l S 3 17 m 17 3 l S Q"
        off = b"q 0 g 1 w 0.5 0.5 19 19 re S Q"
        for i, ap in ((4, on), (5, off)):
            objs[i] = (b"<< /Type /XObject /Subtype /Form /BBox [0 0 20 20] /Length %d >>\nstream\n"
                       % len(ap) + ap + b"\nendstream")
        next_id, page_ids, widget_ids = 6, [], []
        for content, annots in zip(self.pages, self.annots):
            pid, cid = next_id, next_id + 1
            wids = list(range(cid + 1, cid + 1 + len(annots)))
            next_id = cid + 1 + len(annots)
            page_ids.append(pid)
            widget_ids += wids
            stream = "\n".join(content).encode("cp1252", "replace")
            objs[cid] = b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream"
            objs[pid] = ("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] "
                         "/Resources << /Font << /F1 3 0 R >> >> /Contents %d 0 R /Annots [%s] >>"
                         % (PAGE_W, PAGE_H, cid, " ".join("%d 0 R" % w for w in wids))).encode("latin-1")
            for w, a in zip(wids, annots):
                objs[w] = a.replace("{P}", str(pid)).encode("cp1252", "replace")
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


if __name__ == "__main__":
    f = Form()
    f.heading("Photo consent")
    f.para("I consent to photographs taken of me at the event named below being used by the "
           "organiser for the purpose selected. I can withdraw this consent at any time by "
           "writing to the organiser; use before the withdrawal remains lawful.")
    f.text_field("full_name", "Full name", required=True)
    f.text_field("email", "Email", required=True)
    f.text_field("event", "Event")
    f.dropdown("purpose", "Purpose", ["Website", "Print", "Social media"], required=True)
    f.checkbox("agree", "I have read the text above and agree to it", required=True)
    f.text_field("notes", "Notes", multiline=True, lines=3)
    f.signature("Participant")
    print("wrote", f.write(sys.argv[1] if len(sys.argv) > 1 else "form.pdf"), "bytes")
```

## Check it before handing it over

1. The file starts with `%PDF` and is a few kilobytes, not a few bytes.
2. If `pypdf` happens to exist, read the fields back and compare with the table you planned:

   ```python
   from pypdf import PdfReader
   for name, f in PdfReader("out.pdf").get_fields().items():
       print(name, f.get("/FT"), f.get("/Ff"))
   ```

3. If nothing can render a page here, say so and ask the user to open the file: every field
   should show a border, the dropdown an arrow, the checkbox a square, and the signature
   caption should sit under empty space.

Say which rung produced the file, and — if the document is going to a language outside
WinAnsi — say that this file cannot carry it and offer rung 4 or the hand-over.
