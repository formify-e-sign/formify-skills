# The two-column clause table

Open this for any document with a translation column. The rule from `SKILL.md` step 5: two
columns, master language left, translation right, the same clause on the same row, rows
breaking between pages. Stacking the translation under the master is allowed only in the
hand-over, and it is announced there.

## Why rows, not paragraphs

A clause and its translation are one unit. When they are laid out as separate paragraphs, the
two columns drift apart the moment one language runs longer, and the numbering stops lining
up. A table with one clause per row keeps them level, and a row is the unit that moves to
the next page as a whole.

## The reportlab recipe

`reportlab` breaks a table between rows and keeps a row together. Give every clause its own
row of two `Paragraph` cells and let the table split itself:

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

W, H = A4
MARGIN = 56
cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=9.5, leading=12.5)

# (id, master text, translation) — the id stays inside the text as its printed number
CLAUSES = [("COL-01", "1. Objeto. La colaboración se limita ...", "1. Purpose. The collaboration is limited ..."),
           ("COL-02", "2. Cliente presentado. ...", "2. Introduced client. ...")]

rows = [[Paragraph(es, cell), Paragraph(tr, cell)] for _, es, tr in CLAUSES]
col = (W - 2 * MARGIN) / 2
table = Table(rows, colWidths=[col, col], repeatRows=0, splitByRow=1)
table.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
doc = SimpleDocTemplate("document.pdf", pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                        topMargin=MARGIN, bottomMargin=MARGIN)
doc.build([table])
```

Two consequences to handle deliberately:

- **A single clause taller than a page cannot be split by row.** Split that clause's text at a
  paragraph boundary into two rows carrying the same number, in both languages, and say so
  in the check. Do not let the library fall back to stacking.
- **No grid lines.** The table is a layout device, not a visible frame; the style above draws
  none. Keep the caption-only rule for signatures below the table.

This recipe follows the library's documented behaviour and has not been rendered in this
repository's own test run; look at every page of the result, as step 7 requires.

## Where fields sit in a bilingual table

A value the signer fills in belongs to the data boxes above the clauses, once, never inside a
clause cell. If a clause needs a field, the field goes into the box the clause refers to, and
the clause refers to the box.
