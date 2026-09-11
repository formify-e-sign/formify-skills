# Adding fields to a PDF that already exists

Open this when the user brings their own document — *"here is our standard contract, make it
signable"* — rather than asking for a new one to be written. It is the most common request and
the one where a good-looking result is most often silently broken.

This file assumes code execution is available. If it is not, go back to `SKILL.md` step 5 and
deliver the field specification instead; nothing here changes that ordering.

## The rule this file exists for

**Do not recreate their document.** A redrawn lookalike is not their contract: their lawyer
approved the original wording, their letterhead, their clause numbering. Re-typesetting it
introduces differences nobody asked for and nobody will proofread. Add fields to the file they
gave you and change nothing else.

Recreating is the right answer only when the user explicitly asks for a new version, or when
what they sent is a scan with no text layer and they agree to a rebuild.

## What the environment gives you

A closed list: `reportlab`, `pypdf`, `pdfplumber`, `pypdfium2`, `pillow`. Assume **no browser
and no network**. So:

- **Write the code yourself.** These libraries are enough to do everything below; you do not
  need a recipe to copy, you need to know which traps are there.
- **Never run an installer** — no `pip`, `uv`, `npm`, `brew` or virtual environment, and not
  even where it would succeed. What you install exists only on the machine you are on; the
  person receiving this document is in a container where nothing can be installed.
- **`pymupdf` / `fitz` is forbidden** even when already present: absent from that container,
  and AGPL.
- **No headless browser and no HTML-to-PDF converter.**
- Verify by **rendering a page to an image and looking at it**. A PDF that opens is not a PDF
  that is correct.

## The trap that ruins most attempts

Building widgets on a blank overlay page and merging that page into the original **loses every
field.** Page merging copies the content stream — the visible marks — and drops `/Annots`, which
is where form fields actually live. The result looks perfect: the boxes are drawn, the text is
positioned, nothing errors. There is simply no form.

The way through is to stop treating a field as something you draw. A field is a dictionary
registered in three places at once:

1. in the target page's `/Annots` array,
2. in the document catalog's `/AcroForm /Fields` array,
3. with its own `/P` entry pointing back at the page that holds it.

Miss any one of the three and the field is invisible, unfillable, or attached to the wrong page.

## Four failures that are worth knowing before you start

**`/P` pointing at the wrong page.** If widgets are created while the layout engine still
believes it is on page one — which happens whenever page output is deferred, for example to
number pages once the total is known — every widget on every later page carries page one's
reference. Formify's ingestion trusts `/P`, so a five-page contract arrives with all its fields
stacked on the first page. After building the document, walk every page and set each widget's
`/P` to the page whose `/Annots` actually contains it. It is a few lines and it is not optional.

**No appearance stream.** A widget with no `/AP /N` renders as nothing in many viewers. Either
build the appearance stream for each widget, or set the document-level flag that tells viewers
to generate appearances themselves. Setting that flag is the cheaper and more robust choice for
documents going into a signing flow.

**Missing font resource.** Text typed into a field is drawn with a font named in the AcroForm
default resources. If that dictionary has no usable face, typed characters vanish. Worse, the
standard built-in encoding covers only WinAnsi: `š ž å ä ö é` survive, `č ć đ ł ř ș` do not.
For any document in Croatian, Polish, Romanian, Turkish or Czech, embed a Unicode face and
reference it from the AcroForm default resources — the page text may look right while the
fields silently drop characters.

**An empty string as a value.** Setting a field's value to `""` is not the same as leaving it
unset, and it is rejected downstream. Omit the value entirely.

## Finding where to put a field

The user rarely knows coordinates. Read them off the document instead: extract the words with
their bounding boxes and look for the label the field belongs to — `Name:`, `Date:`, a row of
dots, an underscore run.

Two things to be careful about:

- **The vertical axes disagree.** Text-extraction libraries usually measure from the top of the
  page; the PDF coordinate system measures from the bottom. Convert with
  `pdf_y = page_height − top`, and confirm on a rendered image rather than trusting it.
- **A field sits under its label, not on it.** Place it at
  `label_y − label_font_size − gap − field_height`, with a gap of three to five points. A field
  drawn at the label's own baseline covers the label, and Formify's fields are opaque.

## Replacing text that is already printed

Sometimes a placeholder is already typed into the document — a name, a date, a fixed amount —
and the user wants a fillable field there instead. Rewriting the content stream to delete it is
fragile and rarely worth it.

Cover it instead: draw an opaque rectangle in the page background colour over the old text, one
to two points larger than its bounding box on each side, then place the field on top. Save and
restore the graphics state around the rectangle so it does not leak into the marks that follow.

Two cautions. The old text is still in the file and can be recovered by copy-paste or
extraction, so this hides, it does not redact — never use it for anything confidential. And the
rectangle must match the actual background; on a tinted band or a table cell, a white rectangle
is a visible patch.

## Field behaviour

Field behaviour is set by summing flag bits into one integer. The ones that matter here:

| Behaviour | Bit | When to use it |
|---|---|---|
| Read-only | 1 | Every `tink-*` trigger and every auto-filled field. Mandatory. |
| Required | 2 | Only where the user said the field is required. |
| No export | 4 | Rare; the field's value is not included in exported data. |
| Multiline | 4096 | A text box taller than about 1.5 lines. |
| Do not scroll | 8388608 | Hard-limits input to what fits the box. |
| Comb | 16777216 | Fixed-pitch character cells. Needs a maximum length set. |

They are summed: multiline **and** required is `2 + 4096 = 4098`.

A few defaults are worth setting deliberately rather than inheriting: auto-shrinking text (a
font size of zero) so a long answer stays inside its box; multiline wherever a box is tall
enough to suggest more than one line; and read-only left **off** for everything the signer is
meant to complete.

## Radio groups

Options belong to one group when they share a group identifier in the field name. Two blocks of
the same question — the same consent asked of two people — must use **different** identifiers,
or choosing an option for one person silently changes the other. And no option value may contain
a `/`; the slash corrupts the stored value.

## Before handing it over

- Render at least the first page and every page carrying fields to an image, and look at them.
- Confirm every widget's `/P` matches the page it is on.
- Confirm field names are unique, and that every `tink-*` name matches the catalogue exactly —
  see `references/tink-attributes.md`. There is no error path for a wrong attribute; silence is
  the failure.
- Confirm the signature areas are still empty. A widget in the signature space collides with
  Formify's signing overlay.
- Say which route produced the file, and name anything you could not verify.
