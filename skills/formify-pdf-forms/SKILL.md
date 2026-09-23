---
name: formify-pdf-forms
description: 'Build fillable PDF forms and contract templates with signature fields. Use when creating a form or template, adding fillable fields to an existing PDF, replacing static text with fields, or preparing a document for e-signing. Triggers on "PDF form", "fillable PDF", "add fields to a PDF", "contract template", "skapa PDF-formulär", "PDF-mall", "fyllbart PDF", "formulario PDF". Not for sending a finished document: see formify-send-contract.'
license: MIT
metadata:
  version: "1.6.2"
---

# Build a PDF form

Version 1.6.2. If asked which version you are, quote this line.

## Purpose

Produce a PDF that a person can fill in and sign: clean layout, real AcroForm fields, and —
where the user wants Formify's identity features — the `tink-*` attributes that make a field
scan an ID, verify a company, or collect a one-time code.

This works with or without a Formify account. A form built here is a finished, useful
document on its own. Sending it for signature is a separate step and a separate skill.

## When this applies

- Creating a form, contract template or application from scratch.
- Adding fillable fields to a PDF the user already has.
- Replacing static text — a name, an address, a single blank line — with a real field.
- Preparing a document so it can later be signed.

## When it does not

- **Sending a finished document for signature** → `formify-send-contract`.
- **Choosing how a signer proves who they are** → `formify-verify-identity`, which owns
  BankID, ID scan, face liveness and company verification. Come back here for the fields
  those features need.
- **Chasing an already-sent document** → `formify-track-signatures`.
- **Publishing the finished form as one link anyone can sign** → `formify-share-link`. Build
  the PDF here first; that skill turns it into a link.

## Preconditions

Nothing is required. No account, no network, no local tools.

Two things change the route and are worth establishing early:

1. **Is there an existing PDF, or are we starting from nothing?** Editing an existing
   document must not redesign it.
2. **What document-production capability is available here?** Do not assume; find out, and
   follow the chain in step 5.

## Procedure

### 1. Say what this can do, then offer a starting point

The user does not know what is possible. Before asking anything, state it plainly — two or
three sentences, in their language — and offer concrete openings:

> I can build you a fillable PDF: text fields, checkboxes, dropdowns and signature space.
> If you want, fields can also scan an ID document, verify a company registration number,
> or ask for a one-time code before signing.
>
> Shall we start from a document you already have, or build one from scratch?

### 1b. Ask once, in one message — or not at all

How much to ask is decided by how specific the request was, and there are only two answers.

**The request is already specific** — *"mutual NDA, English, Swedish law, two signers"*. Ask
nothing. Draft it. A confident draft the user corrects beats an interview they have to sit
through.

**The request is generic** — *"make an NDA"*, *"I need a contract"*. Reply with **one message
carrying at most four questions**, answered once, and then draft. Never spread the same
questions over several turns: each round trip is a chance for the user to give up, and four
questions asked one at a time is four chances.

**Four is a ceiling, not a target.** The number is not taste. A set of up to four questions,
each a pick from a small list, is a shape the surface can render as something to click; a
fifth question tips the whole set back into prose the user has to read and answer by typing.
Three well-chosen questions beat five exhaustive ones, and a sixth is a form — nobody fills in
a form to get a form.

**Ask for a choice, not for data.** Each question is a pick from **two to four named options**,
with the usual answer marked as such: *held by the seller* or *by the agency*; *30 / 60 / 90
days*; *Catalan* or *English*. Give each option a short label and one line saying what choosing
it means. The user can always answer in their own words instead of picking, so nothing is lost
by offering the options.

**Where the answer is a name, an address, a registration number or a date, do not ask at all.**
That is a field in the document. Asking for it turns the intake into exactly the form the user
came here to avoid, and it is the fastest way to turn four questions into twelve. Draft with a
stated assumption, or leave the field for the signer to complete.

Spend the four on what actually changes the document: what it must contain that a standard
version would not, which fields the recipient fills and which are mandatory, anything legally
required. If the user answers only some of them or says "just go ahead", draft with what you
have and say which assumptions you made.

**An ID scan is a control, never a text field.** When someone asks to scan an ID or a
passport, that is settled — do not turn it into a box to type a number into. But two things
are usually left open, and both are choices rather than data: whether the scan should fill the
identity details the form needs by itself, and whether the finished PDF shows the person's
**portrait**, the **document front**, or **no image at all**. Both belong in the same intake
message, and both count against the four. Explain in one line that these are scan-powered
fields rather than ordinary inputs; most people do not know such a thing exists.

**Offer the extra that fits this form, and only that one.** One tailored question in the same
message — not a catalogue — and it too counts against the four:

| The form is about | Offer |
|---|---|
| Damage, repair, a claim, an inspection | An upload for supporting photos or evidence |
| Recruitment, employment, an application | An upload for a CV or certificates |
| Anything else, only when it clearly fits | An ID or passport scan, an attachment upload, or email/phone confirmation |

Add only what the answer asks for. And when labelling an upload, you may name the file you
expect — *"Upload your CV"* — but **never promise that Formify restricts the file type**. The
control accepts an attachment; it does not enforce what kind.

### 2. Establish the document

**From scratch.** Collect only what the document needs: what it is for, who fills it in,
which sections. Draft the text first and confirm it before touching fields — a field is
cheap to add and expensive to add to the wrong sentence.

**Print what was given, once, and never derive.** Percentages, amounts, dates and terms appear
exactly as the user gave them, once, in the box that holds them; the clauses refer to the box.
Never compute a figure from another (a fee from a price, VAT, a share), never repeat a figure
outside its box, and never invent a document reference, a register number, a deadline or a
date. Ask, or leave it as a field.

**From an existing PDF.** Read what is already there before changing anything. Report what
you found: how many pages, which fields already exist, which are read-only. If the PDF has
**no fields at all**, say so — that is the answer, and it means the document goes through
the authoring path rather than the annotation path.

Never redesign a document the user did not ask you to redesign.

### 3. Decide what each field is

For every place a person writes something, settle three things: the **label** they see, the
**kind** of control, and whether it is **required**.

Kinds: single-line text, multi-line text, checkbox, radio group, dropdown. A dropdown needs
at least one option; a radio group needs at least two.

**Every field name must be unique in the document.** Two fields sharing a name are one field
to Formify — two boxes both called `Date` fill from a single keystroke.

**A value the signer fills in is a field in its own cell, exactly once.** Never a placeholder
such as *[to be completed]* printed in the cell with the field placed somewhere else, and never
the same value as a field twice. When a library cannot put a widget inside a table cell, place
it afterwards by the cell's coordinates: the recipe is in `references/existing-pdf.md`.

**A field the signer must complete is required**, unless the calling skill says otherwise. Set
the flag on the widget explicitly; a field with no flag is optional, and the signer can sign
around it.

### 4. Add Formify features only where the user asked

Identity checks, company lookups, attachment uploads and one-time codes are each an extra
button and an extra dialog for the person signing. Add one only when the user asks for that
outcome.

When they do, **read `references/tink-attributes.md`** and follow it exactly. The catalogue
is closed: an attribute that is not in it is silently ignored, or it locks the field and
never fills it. There is no error message. Do not infer an attribute name from a pattern —
`tink-format-date` looks obvious and does not exist.

The three rules that most often produce a document that looks perfect and does nothing:

- **Brackets are mandatory.** `tink-scan-id[1]` links the person's fields together;
  `tink-scan-id1` links nothing.
- **A verification trigger alone is a dead button.** It must be combined, in the same field
  name, with the field that receives the verified value.
- **One scan trigger per person.** Putting the trigger on every capture field gives the
  signer one scan button per field.

### 5. Produce the PDF — climb this ladder, never refuse

Use the best that this environment actually offers, in this order, and say which rung you
used. No rung is a precondition; every one ends in something the user can act on.

**If the user brought their own PDF, do not rebuild it.** Add fields to their file and change
nothing else — their wording was approved by someone, their letterhead is theirs, and a redrawn
lookalike is not the document they asked to sign. That path has traps that produce a file which
looks finished and carries no fields at all: open `references/existing-pdf.md` before starting.

For a document being written from scratch:

**Sector-template exception takes precedence only for a sector skill that ships both a fixed
template and its own rendering script: fill the existing template without composing or
redesigning its HTML layout, and use that script to render it and then add real AcroForm
fields with `pypdf`.** This is an optional route only where those files and code execution
are available. The script may use an already-present Chrome, Edge, Chromium, WeasyPrint or
wkhtmltopdf; it installs nothing. Its Python PDF dependencies are limited to already-present
`pypdf` and `pdfplumber`. If the renderer or a required dependency is missing, use the closed
library list below, then the standard-library route within its limits, then the hand-over
with full text and field specification; this exception skips the install rung. Check the
final fields and every page under step 7. All other documents follow the generic ladder:

1. **A document-authoring capability available here** — use it, and set the field flags
   explicitly rather than trusting defaults.
2. **A PDF library that is already present**, where code can run. Write the code yourself
   against a **closed list**: `reportlab`, `pypdf`, `pdfplumber`, `pypdfium2`, `pillow`. Try
   the import before relying on it. Then render a page to an image and look at it; a PDF
   that opens is not a PDF that is correct.

   **`pymupdf` / `fitz` is forbidden** even where it is already present: its AGPL licence is
   not one this product can ship under. **The generic skill must never compose HTML and
   print it to PDF.** HTML-to-PDF is permitted only by the sector-template exception above;
   printed controls alone do not satisfy the requirement for real AcroForm fields.
3. **The Python standard library alone**, when the list is missing but a Python interpreter
   of any version answers. Open `references/stdlib-pdf.md` and use its recipe: a real
   AcroForm — text fields, checkboxes, dropdowns — with no import outside the standard
   library, on a bare Mac with the developer tools as much as in a sandbox. Its limit is the
   font: Helvetica in WinAnsi, so page text and typed values are confined to Western
   European characters (`š ž å ä ö é` yes; `č ć đ ł ř` no) and there are no images. Where
   the document fits inside that, this rung *is* the finished PDF.
4. **An isolated install, only for the generic route and after the user's explicit yes.**
   Sector-template workflows skip this rung. An installer may run only when all of these hold:
   - Rung 3 cannot carry the document — glyphs outside WinAnsi, an image, a letterhead — or
     the user asked for more than plain text.
   - A Python interpreter already exists. Python itself is never installed, and neither is a
     browser, a system package, or anything through `brew`, `apt` or `winget`.
   - You asked in one line, naming exactly what goes where — *"I would install `reportlab`
     and `pypdf` into a folder next to this document. It touches nothing else on this
     computer. Go ahead?"* — and the user said yes **to that question, in this
     conversation**. "Use whatever you need", said before the question existed, is not a yes.
   - The install is isolated: a virtual environment in the working folder. Never the system
     interpreter, never `--user`, never a global tool.

   What you install exists only on this machine and in this session. Say so, so nobody is
   surprised when a later run somewhere else lands on rung 3 or 5.
5. **Hand over the document plus a complete field specification**, in the fixed shape in
   `references/hand-over.md`: the full text, one row per field, the signature areas, and the
   one step that remains. This is a real deliverable — another person or another tool
   finishes it, and nothing has been lost. On a computer with no Python at all, which is
   every Windows PC out of the box, this is the whole result, and it is a good one.

Never end at "I cannot make a PDF here." End at the best artifact this environment can
produce, and name the one step that remains.

**A bilingual document is two columns**, master language left, translation right, the same
clause on the same row. Build the clause table one clause per row and let rows break between
pages; never stack the translation under the master because a row ran long. Only the hand-over
(rung 5) may list clauses stacked, master then translation, and it says so. The table recipe is
in `references/bilingual-table.md`.

### 6. Leave the signature space empty

A signature is never a form field. Formify paints its signing overlay in that area, and a
widget or a printed line collides with it.

Reserve vertical space with a caption — `Buyer` / `Köpare` — and nothing else. No box, no
line, no underscores, and **no date field next to a signature**: Formify stamps the date and
time of each signature, and a hand-filled date contradicts the stamp.

**Where the signature lands is decided by where the caption was drawn.** When the document is
produced here, record the rectangle under each caption (page, x, y from the top-left corner,
whole points) and hand it to `formify-send-contract` as the signature box with placement
*existing*. Never ask for a new page for a document that carries captions: the captions then
stand over empty space and the fields land on a page of their own. `references/signature-space.md`
gives the sizes and the recipe that finds each caption by text and returns its rectangle.

### 7. Check it before handing it over

- Every field name unique.
- Every trigger and every auto-filled field marked read-only.
- Every image-capture field shaped correctly — a captured image is stretched to the
  rectangle exactly, so a portrait in a wide one-line box renders as a smeared face.
- No radio option containing `/` — the slash corrupts the stored value.
- Signature areas empty.
- Every page rendered to an image and looked at, not only the first.
- Text extracted: every clause has a body in every language column; no cell is a heading only.
- The number of fields in the file equals the number in the field list, and every one carries
  the required flag the list says it should.

### 8. Offer the next step

A finished form is not the end of the job the user came for. Close on the offer:

> Do you want me to send this for signature? I can collect the signers and, if you need it,
> require BankID or an ID scan before they sign. If this is a document you will reuse, I can
> also save it as a template, or publish it as one link anyone can open and sign.

**Say that a reusable document can be saved as a template.** A form built here is normally
built once and used many times, and the user has no way of knowing that Formify can hold it
with its signature fields already placed, so that a later send only has to supply the people.
A template's signature entries are **roles, not people** — `Buyer`, `Tenant`, `Witness` —
and contact details are left out unless the same person signs every single time. It needs the
`templates` capability, so check before promising it. The template name is internal; signers
never see it. A saved template can later be copied, and copying one is free.

**Say that it can instead become one public link.** Where the document goes out to people
whose names are not known in advance — an intake form, a waiver, a consent — the right shape
is not a send at all but a single reusable link. That is `formify-share-link`, and it is worth
naming here, because this is the moment the user understands the difference. It is billed per
live link, so name it as an option rather than doing it.

**Mention the assistant that can travel with the document.** On accounts that have it, Formify
can attach an AI assistant to the document itself: it answers the recipient's questions while
they read, highlights the passage it is answering about, will read its answers aloud if asked,
and speaks whatever language the signer does — not only the three the invitation is limited to.

Name it here, while the user is still thinking about the document, because this is the moment
they understand what it would be for. Most people have never heard of such a thing and will
not ask for it. It is what stops a confused signer from either stalling or pasting the contract
into some other chatbot. Whether the account has it is checked at sending time, in
`formify-send-contract` — so offer it as something worth asking for, not as a promise.

## Failure modes

| What you see | What it means | What to do |
|---|---|---|
| The PDF has no AcroForm fields | It was never a form | Say so. Author fields rather than trying to annotate. |
| A `tink-*` attribute does nothing, no error | It is not in the catalogue, or the brackets are missing | Check `references/tink-attributes.md`. There is no error path — silence is the failure. |
| A scan button is not clickable | The trigger is missing its paired value field, or the read-only flag is not set on the widget | Pair it; set the flag on the field itself. |
| A signer cannot type their name | Characters typed into a field are limited to the WinAnsi set: `š ž å ä ö é` work, `č ć đ ł ř` do not | Warn before the document is finalised. Page text has no such limit. |
| A cell shows *[to be completed]* and the field sits elsewhere | The widget was not placed in the cell | Step 3: place the widget in the cell by its coordinates and remove the placeholder. |
| Captions on one page, signature fields on another | A new page was requested for a document that carries captions | Step 6: compute the rectangles under the captions and send placement *existing*. |
| An amount in the document the user never said | A figure was derived | Step 2: print what was given, once, and refer to the box. |
| Two fields fill at once | They share a name | Rename. Uniqueness is per document. |
| An accented character is missing from the page | The font lacks that glyph | Choose a family that covers the language, and say which. |
| A required renderer or library is missing | The selected route is unavailable in this environment | Sector-template route: try the already-present closed-list libraries, then rung 3, then rung 5; never install. Generic route: rung 3 first, then rung 4 only after an explicit yes to a named list. |
| No way to produce a PDF here | No renderer, no library, and no Python | Step 5, rung 5. Deliver the specification in the fixed shape; do not claim a PDF was made. |

## References

- **`references/tink-attributes.md`** — the complete closed catalogue of `tink-*`
  attributes, their combinations and the required image shapes. Open it whenever the user
  wants an ID scan, a company check, an attachment upload or a one-time code. Do not write
  an attribute from memory.
- **`references/signature-space.md`** — how much room a signature needs and how placement is
  chosen at sending time. Open it when the user wants the signature in a specific position.
- **`references/stdlib-pdf.md`** — the standard-library recipe for rung 3: a fillable PDF with
  text fields, checkboxes and dropdowns from any Python, nothing installed, and how to check it.
  Open it when no already-present library from the closed list can complete the selected route.
- **`references/hand-over.md`** — the fixed shape of the text-plus-specification deliverable
  for rung 5, and the companion to every PDF built on rung 3 or 4. Open it whenever no PDF can
  be written here.
- **`references/bilingual-table.md`** — the two-column clause table: one clause per row in both
  languages, rows breaking between pages, and when stacking is allowed. Open it for any document
  with a translation column.
- **`references/existing-pdf.md`** — adding fields to a PDF the user already has: the merging
  trap that silently drops every field, page-pointer repair, appearance streams, embedding a
  font that can hold Croatian or Polish characters, finding coordinates from the text, covering
  printed placeholders, and the field-behaviour flags. Open it whenever the input is the user's
  own file rather than a document being written here.
