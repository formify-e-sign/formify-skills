---
name: formify-pdf-forms
description: 'Build fillable PDF forms and contract templates with signature fields. Use when creating a form or template, adding fillable fields to an existing PDF, replacing static text with fields, or preparing a document for e-signing. Triggers on "PDF form", "fillable PDF", "add fields to a PDF", "contract template", "skapa PDF-formulär", "PDF-mall", "fyllbart PDF", "formulario PDF". Not for sending a finished document: see formify-send-contract.'
license: MIT
metadata:
  version: "1.2.0"
---

# Build a PDF form

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

### 5. Produce the PDF — try in this order, never refuse

Use whatever this environment actually offers, in descending order of quality. Say which
one you used.

**If the user brought their own PDF, do not rebuild it.** Add fields to their file and change
nothing else — their wording was approved by someone, their letterhead is theirs, and a redrawn
lookalike is not the document they asked to sign. That path has traps that produce a file which
looks finished and carries no fields at all: open `references/existing-pdf.md` before starting.

For a document being written from scratch:

1. **A document-authoring capability available here** — use it, and set the field flags
   explicitly rather than trusting defaults.
2. **A PDF library, if code execution is available.** Write the code yourself against a
   **closed list**: `reportlab`, `pypdf`, `pdfplumber`, `pypdfium2`, `pillow`. Then render a
   page to an image and look at it; a PDF that opens is not a PDF that is correct.

   **Never run an installer.** Not `pip`, not `uv`, not `npm`, not `brew`, not a virtual
   environment — and not even when it would obviously succeed. Whatever you install exists
   only on the machine you happen to be on. The person this document is for is in a container
   with no internet, where nothing can be installed, so code that needed an install is code
   that fails for them with no error you will ever see. The same goes for a browser,
   WeasyPrint, wkhtmltopdf or any HTML-to-PDF converter.

   **`pymupdf` / `fitz` is forbidden** even where it is already present: it is not in that
   container, and its AGPL licence is not one this product can ship under.

   If something on the list is genuinely missing, go to option 3. Degrade; do not install.
3. **Hand over the document plus a complete field specification** — the text, and for every
   field its label, kind, options, required flag and any `tink-*` attributes. This is a real
   deliverable: someone else, or another tool, can finish it, and nothing has been lost.

Never end at "I cannot make a PDF here." End at the best artifact this environment can
produce, and name the one step that remains.

### 6. Leave the signature space empty

A signature is never a form field. Formify paints its signing overlay in that area, and a
widget or a printed line collides with it.

Reserve vertical space with a caption — `Buyer` / `Köpare` — and nothing else. No box, no
line, no underscores. Where the signature actually lands is decided when the document is
sent; see `references/signature-space.md` if the user wants it in a specific place.

### 7. Check it before handing it over

- Every field name unique.
- Every trigger and every auto-filled field marked read-only.
- Every image-capture field shaped correctly — a captured image is stretched to the
  rectangle exactly, so a portrait in a wide one-line box renders as a smeared face.
- No radio option containing `/` — the slash corrupts the stored value.
- Signature areas empty.

### 8. Offer the next step

A finished form is not the end of the job the user came for. Close on the offer:

> Do you want me to send this for signature? I can collect the signers and, if you need it,
> require BankID or an ID scan before they sign.

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
| Two fields fill at once | They share a name | Rename. Uniqueness is per document. |
| An accented character is missing from the page | The font lacks that glyph | Choose a family that covers the language, and say which. |
| No way to produce a PDF here | The environment has no renderer | Step 5, option 3. Deliver the specification; do not claim a PDF was made. |

## References

- **`references/tink-attributes.md`** — the complete closed catalogue of `tink-*`
  attributes, their combinations and the required image shapes. Open it whenever the user
  wants an ID scan, a company check, an attachment upload or a one-time code. Do not write
  an attribute from memory.
- **`references/signature-space.md`** — how much room a signature needs and how placement is
  chosen at sending time. Open it when the user wants the signature in a specific position.
- **`references/existing-pdf.md`** — adding fields to a PDF the user already has: the merging
  trap that silently drops every field, page-pointer repair, appearance streams, embedding a
  font that can hold Croatian or Polish characters, finding coordinates from the text, covering
  printed placeholders, and the field-behaviour flags. Open it whenever the input is the user's
  own file rather than a document being written here.
