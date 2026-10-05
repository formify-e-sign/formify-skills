# Leaving room for a signature

Open this when designing a document that will be signed, to decide how much space to reserve
and where.

## A signature is never a form field

Do not create an AcroForm field for a signature. Do not draw a box, a line, or a row of
underscores where one goes.

Formify paints its signing overlay in that area when the document is sent. A widget or a
printed rule underneath collides with it, and the result is visible in the signed document
that the customer keeps.

Reserve the space with a caption and nothing else:

```
Buyer / Köpare

Seller / Säljare
```

## How much room to leave

The signature field placed at sending time is **219 × 58 points** at full size. Leave more
than that: the caption sits above it and the field must not touch the text beneath.

| Situation | Reserve |
|---|---|
| Handwritten signature or BankID | **~80 pt** per signer |
| Signing that includes an ID scan | **~220 pt** per signer |

The second figure is not padding. `digital_ink_id_scan` places a second field — an ID scan
placeholder of **218 × 138 points** — alongside the signature. Both are required for that
method, and both need clear space.

If the document may ever be signed with an ID scan, reserve for it. Adding the room later
means re-laying out the page.

## Where to put it

**A document that carries captions places its signatures under them**, on the existing page,
with placement *existing* and the rectangle under each caption. Asking for a new page for
such a document leaves the captions over empty space and puts the fields on a page of their
own. The new page at the end is the right default only for a document with no captions, or
when the caption's page has no room left.

When the signatures go on an existing page:

- Keep the block clear of anything the signer must read. A signature field is fully opaque
  and hides whatever is behind it.
- Keep several signers apart. An 80-point vertical step leaves a usable gap between
  58-point fields.
- Leave the bottom margin alone. A field flush against the page edge looks like an error
  even when it is technically valid.

## Do not put the amount in a field label

A label becomes part of the field's name. Writing an agreed figure into it — `Total EUR
65 000` — renames the field to something like `total_eur_65_000` for every system that reads
the document afterwards, and the name is then wrong the moment the figure changes.

There is no attribute that pre-fills a field with a value. An agreed amount belongs in the
document's printed text.

## Multi-language captions

Where a document serves two languages, write the caption once with both, the second in a
lighter treatment:

```
Köpare / Buyer
```

Do not create two separate signature areas for two languages. One person signs once.

## Finding the rectangle under a caption

Formify's coordinates have their origin at the top-left corner of the page, `y` increasing
downward, whole points, pages numbered from zero (`formify-send-contract` has the full
system). Text-extraction libraries report the caption's baseline from the bottom-left. The
box starts a small gap below the caption:

```python
from pypdf import PdfReader
CAPTIONS = ["VENDEDORA", "COMPRADORA"]     # the caption text as drawn, one per signer
W, H, GAP = 219, 58, 6                     # Formify signature field at full size
boxes = []
for pno, page in enumerate(PdfReader("document.pdf").pages):
    height = float(page.mediabox.height); hits = []
    def visit(text, cm, tm, font_dict, font_size):
        t = text.strip()
        for c in CAPTIONS:
            if t.startswith(c): hits.append((c, tm[4], tm[5]))   # x, baseline y (bottom-left)
    page.extract_text(visitor_text=visit)
    for c, x, y in hits:
        boxes.append({"caption": c, "page": pno, "x": round(x),
                      "y": round(height - y + GAP), "width": W, "height": H})
```

With `pdfplumber`, `page.search(caption)` returns `x0` and `bottom` already measured from the
top, so `y = round(bottom + GAP)`. Either way: whole numbers, one box per signer, an ID-scan
box of 218 × 138 beside the signature where the method needs it, and a look at the rendered
preview before sending.
