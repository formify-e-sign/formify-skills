<!-- generated from core/references/attachments.md by build_vertical.py; edit the core file, not this copy -->
# The attachment pattern: the signer uploads a document at signing

Verified against Formify 2026-09-08 (Formify's own KYC form uses it for the proof of residence; es-real-estate-formify uses it for the proof of the deposit transfer). Use it whenever a document must be accompanied by a file the counterparty holds (a payment receipt, a proof of residence, a licence, a certificate) instead of an annex page or a chat question.

## What the template carries (fixed fields in the HTML, not `{{...}}`)

One row in the data box, label left, and on the right a cell `td.attachment` with two fields: the upload button `<value>_upload|tink-upload-attachment[1]|tink-style-transparent` (75 × 22 pt, class `pdf-field button`; Formify draws its own upload control over it) and the file-name field `<value>_name|tink-uploaded-attachmentname[1]` (250 pt, read-only; Formify writes the name of the uploaded file into it, so the signed PDF shows which file belongs to the document). A short label above the name field ("Uploaded document" with its translation) tells the signer what the empty line is.

```html
<tr><td class="k">Proof of transfer <span class="tr-lbl">/ Justificante de la transferencia</span></td>
<td colspan="3" class="attachment"><span class="pdf-button"><span class="pdf-field button" data-name="proof_upload|tink-upload-attachment[1]|tink-style-transparent" data-width="75" data-height="22" style="width:75pt !important;height:22pt !important"><span class="field-mark">FIELDMARK</span></span></span><span class="attachment-name">Uploaded document <span class="tr-lbl">/ Documento subido</span><span class="pdf-field" data-name="proof_name|tink-uploaded-attachmentname[1]" data-width="250" data-readonly="1" style="width:250pt"><span class="field-mark">FIELDMARK</span></span></span></td></tr>
```

The clause that refers to the file says "the document uploaded in box B" (and nothing about annexes). The uploaded file travels with the signed document in Formify; it is not merged into the PDF.

## Making the upload mandatory

Two ways, both through the /Ff flags `render_pdf.py` writes: `data-required="1"` on the button (required, Ff 2) makes the signing client refuse to finish without a file; Formify's own form instead sets the name field read-only + required (Ff 3) so that the upload is the only way to fill it. Use the first for a plain "must upload"; use the second when the document must show the file name. Never both required and read-only on the button itself.

## Rules

- Fields are opaque in the signing client: keep the button at 75 × 22 pt and the name field at 250 pt so neither covers a neighbouring cell; the name field wraps under the button when the cell is narrower than 340 pt.
- One attachment row per file. Several files: several rows, each with its own `[1]`, `[2]`... index on both fields.
- The sample pack shows the row empty; the user sees the upload control when opening the sample on a phone.
- Never ask for the file in the chat and never leave an empty annex page for it; the row replaces both.
