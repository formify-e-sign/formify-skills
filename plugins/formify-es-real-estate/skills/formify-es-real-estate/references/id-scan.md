<!-- generated from core/references/id-scan.md by build_vertical.py; edit the core file, not this copy -->
# The ID-scan pattern: the client scans the document, the data fills itself

Verified against Formify on 2026-09-07 (`get_file_fields` lists every field), mandatory scan added 2026-09-08. Use it for any identification or KYC form, and for any document where a party's identity data should come from the document rather than from typing.

## What the template carries (fixed fields in the HTML, not `{{...}}`)

One table with class `form identity`. Left: one row per identity value, each with a text field named `<name>|tink-scanned-id-mrz-<attribute>[1]|tink-style-transparent`, width 135 pt, all with `data-required="0"`: the scan fills them, the signer never types them, so they carry no required mark. Right: a cell `td.image` with `rowspan` over those rows, holding a label, the scan field `document_scan|tink-scan-id[1]` (180 × 120 pt, `data-height="120" data-required="1"`, class `pdf-field image`), and under it up to three short values with a label above and a 180 pt field or printed value below (tax number, telephone, e-mail). Below the table, full-width rows for what no document contains (address, tax residence).

MRZ attributes available: firstname, lastname, birthdate, placeofbirth, nationality, nationalitycode, documentid, issuingstatename, issuingstatecode, issuedate, expirydate, placeofissue, personalnumber. Variants of the trigger: `tink-scan-id-basic` (accepts incomplete data), `tink-scan-id-passport` (passports only), `-passport-basic`. Combine the trigger with an MRZ attribute on the same field when no image of the document is wanted (data minimisation).

Field markup (fill.py numbers the markers):
```html
<span class="pdf-field" data-name="first_name|tink-scanned-id-mrz-firstname[1]|tink-style-transparent" data-width="135" data-required="0" style="width:135pt"><span class="field-mark">FIELDMARK</span></span>
<span class="pdf-field image" data-name="document_scan|tink-scan-id[1]" data-width="180" data-height="120" data-required="1" style="width:180pt !important;height:120pt !important"><span class="field-mark">FIELDMARK</span></span>
```

## The scan is mandatory

An identification form that can be signed without scanning is worthless to the organisation (David, 2026-09-08). The scan trigger is a required field (Ff 2), never read-only; Formify reads the flag from the PDF and marks the field in red, and the signing client refuses to finish until a document has been scanned. The MRZ fields stay optional: the scan fills them, so a required mark on them would only confuse the signer (David, 2026-09-08). Formify's own KYC form does the same (trigger Ff 4098). Tell the user nothing about it; the form simply cannot be signed empty.

## No internal-use block

Identification forms carry no "internal use" section (PEP check, risk class, verified by). Those judgements belong in the organisation's own file, not in a document the client signs (David, 2026-09-08).

## Rules

- Fields are opaque in the signing client: a field wider than its cell covers the neighbouring cell. Measure the cell (page width 493 pt of content; label column 24 %; image column 196 pt) and keep the field inside it. 135 pt for the left column, 180 pt under the image.
- Keep the image 3:2 (180 × 120 pt) so it sits beside the rows without stretching the page; Formify replaces the field with the front side of the document.
- Never ask for these values in the chat: the client scans, and the data arrives verified. Values no document contains are typed by the client or printed by the user.
- The signer of such a form does not need a second ID scan in the signature field; the default signing method of the memory is enough.
- Retention: the signed PDF with the embedded document image, sealed by Formify, is the electronic copy an AML-obliged organisation must keep; say so in the document's data-protection text, not in the chat.
- In the sample pack these fields stay empty; the user sees the scan button when opening the sample on a phone.
