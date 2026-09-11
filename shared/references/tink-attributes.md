# `tink-*` field attributes — the complete catalogue

Open this file whenever a PDF needs a Formify feature inside a field: an ID scan, a company
lookup, a one-time code, an attachment upload, or an auto-filled value.

## How a Formify field is configured

A Formify widget is configured entirely through its AcroForm field name (`/T`). Everything
before the first `|` is the human-readable label. Each `|`-separated segment after it is a
`tink-*` attribute.

```
firstname|tink-scanned-id-mrz-firstname[1]
photo|tink-scan-id[1]|tink-scanned-id-portrait[1]
scan|tink-scan-id[1]|tink-scanned-id-allow-in-signature[1]
```

**The catalogue below is closed.** An attribute that is not in it is not rejected — it is
silently ignored, or it locks the field read-only and never fills it. There is no error
message anywhere. Inventing a plausible-sounding attribute produces a PDF that opens
perfectly and quietly does nothing.

Three attributes that people invent and that **do not exist**: `tink-format-date`,
`tink-scanned-id-mrz-gender`, `tink-verified-orgnumber-ceo`. A date field takes a plain
name and no attribute at all.

## The index in brackets

`tink-scan-id[1]` is correct. `tink-scan-id1` is not — without brackets the index is
ignored and the fields are never linked to each other.

The index groups everything belonging to **one person**. Three signers means `[1]`, `[2]`,
`[3]`, each with its own trigger and its own capture fields. The index is a property of the
person's position in the document, so inserting a second applicant above the first
renumbers everything below.

---

## Company verification

| Attribute | What it does |
|---|---|
| `tink-orgnumber-verification[index]` | Verifies the beneficial owner through Swedish BankID |
| `tink-orgnumber-verification-boardmember[index]` | Verifies a board member |
| `tink-orgnumber-verification-kyc[index]` | KYC variant; the result is stored for compliance |

**A trigger on its own is a dead button.** Each of the three must be combined, in the same
field name, with `tink-verified-orgnumber[index]` or
`tink-verified-orgnumber-companyname[index]`. Without that pairing the field never becomes
clickable.

Auto-filled company data, all indexed: `tink-verified-orgnumber`,
`tink-verified-orgnumber-companyname`, `tink-verified-orgnumber-addressline1`,
`tink-verified-orgnumber-zipCode` (note the capital `C`), `tink-verified-orgnumber-city`.

## ID document scanning

Four triggers, no others:

| Attribute | Document |
|---|---|
| `tink-scan-id[index]` | ID card, full validation |
| `tink-scan-id-basic[index]` | ID card, partial validation, less strict |
| `tink-scan-id-passport[index]` | Passport, full validation |
| `tink-scan-id-passport-basic[index]` | Passport, partial validation |

**There is no driving-licence trigger.** A driving licence is scanned with `tink-scan-id`.

**One trigger per person, ever.** Putting the scan trigger on each capture field produces
one scan button per field — a real document once shipped three buttons for one passport,
and the signer is asked to scan the same document again for each.

### What the trigger field itself becomes

| Combination | Result |
|---|---|
| Trigger alone | The field is **replaced by the front-side image** of the document. Draw it landscape, about 3:2, and generously sized. |
| Trigger + `tink-scanned-id-portrait[index]` | The portrait replaces the front-side image. Shape 3:4 upright. |
| Trigger + any `tink-scanned-id-mrz-*[index]` | **No image at all.** The field receives that value as text. |
| Trigger + `tink-scanned-id-allow-in-signature[index]` | The scan is reused for a Live ID signature — see below. |

The third row is the **data-minimisation pattern**, and it carries legal weight:
reproducing a copy of an identity document requires its own legal basis. When the user
needs the data but not the picture, combine the trigger with the MRZ attributes and no
image is stored.

### Text captured from the machine-readable zone

All `tink-scanned-id-mrz-<name>[index]`, all auto-filled:

`firstname` · `lastname` · `personalnumber` · `documentid` · `nationality` ·
`nationalitycode` · `birthdate` · `expirydate` · `issuedate` · `issuingstatecode` ·
`issuingstatename` · `placeofbirth` · `placeofissue`

There is no `gender`.

### Images captured from the document

| Attribute | Shape | Note |
|---|---|---|
| `tink-scanned-id-portrait[index]` | 3:4 upright | Strict — the scan **fails** if the portrait cannot be extracted |
| `tink-scanned-id-ghostportrait[index]` | 3:4 upright | Field is removed if absent |
| `tink-scanned-id-signature[index]` | 4:1 wide and low | Field is removed if absent |
| `tink-scanned-id-documentrear[index]` | 3:2 landscape | Field is removed if absent |
| `tink-scanned-id-barcode[index]` | 4:1 wide and low | Field is removed if absent |

**A captured image is stretched to fill the field rectangle exactly.** It is not fitted and
not letterboxed. A 3:4 portrait dropped into a full-width single-line box renders as a face
smeared across the page. Give every image field the shape in the table.

When several image attributes are combined on one field, the last one wins.

### Reusing a scan for the face check

`tink-scanned-id-allow-in-signature[index]` is a modifier. Combine it on the scan trigger
and a **fully successful** scan is carried into a Live ID signature: the signer goes
straight to the biometric face check without photographing their document a second time.
The face check itself always runs.

An incomplete scan is never reusable, even with the `-basic` triggers. The `[index]` here
is the scan group — it has no connection to any signature index.

## Attachments from the signer

`tink-upload-attachment[index]` opens the upload dialog. Pair it with
`tink-uploaded-attachmentname[index]`, usually carrying `tink-style-transparent`, or the
uploaded file's name appears nowhere in the document.

## One-time code verification

`tink-email-verification` and `tink-sms-verification`. **Neither takes an index.**

## Formatting and presentation

`tink-format-mobile` (Swedish mobile format) · `tink-format-email` ·
`tink-style-transparent` (draws no chrome). None take an index.

### Formatting is not verification — and they are usually wanted together

These two pairs look alike, sit next to each other in this catalogue, and do completely
different things. Confusing them is the most common way a "verified" field turns out not to be.

| The user asks for | Checks the value **looks** right | Checks the person **holds** it |
|---|---|---|
| A phone number | `tink-format-mobile` | `tink-sms-verification` |
| An email address | `tink-format-email` | `tink-email-verification` |

The formatting attribute shapes what is typed. The verification attribute sends a one-time code
to that address or number and requires it back before signing — proving the signer can actually
receive there.

When someone says "a verified phone number", ask which they mean, and offer both: they are
routinely combined on the same field, and each is useless as a substitute for the other.

Do not put `tink-style-transparent` on a field that nothing fills. It draws nothing and
stays empty, which is a blank space no one can explain.

## Everything else

| Attribute | What it does |
|---|---|
| `tink-date-now` | Auto-fills the signing date, ISO 8601 |
| `tink-input-fullname` | The name the signer types, which becomes the **visible signature name** on the document — not an ordinary name box |
| `tink-email-recipient` | The address that **receives the completed document** once everyone has signed. It is a delivery instruction, not a contact detail. |
| `tink-sign-and-pay-email[index]` | Prefills the email used for the Sign & Pay flow. The only indexed attribute that is not part of a scan group. |
| `tink-search-{label}` / `tink-search-firstname` / `tink-search-lastname` | Makes the value **findable in Formify's document overview**, so this document can later be located by what was typed here. `{label}` is the one customisable part of this entire catalogue. |
| `tink-share-sms-phonenumber` / `tink-share-email-emailaddress` | Prefills a public-sharing recipient. **This does not send an invitation** — invitations are configured when the document is sent, not in a field. |
| `tink-access-document` | Grants access to the document **before it is finalised**, and only through public links. It must be paired with `tink-email-verification` or `tink-sms-verification`; alone it opens the document to anyone holding the link. |

---

## Rules that produce a broken document silently

Each of these yields a PDF that opens correctly in every viewer and fails only in Formify,
or only when a signer reaches it.

1. **Brackets are mandatory.** `tink-scan-id1` is not an index; the fields never link.
2. **Two fields with the same name are one field to Formify.** Two boxes both named `Date`
   fill from a single keystroke. Every field name must be unique across the document.
3. **Set the read-only flag on the widget itself** for every trigger and every captured
   value. A scan trigger without the flag is an ordinary text box with a long name: the
   signer clicks in and types, and what should have been a scan button never reads as a
   control.

   **Exactly sixteen attributes forbid manual entry.** These, and no others:

   - the three company-verification triggers — `tink-orgnumber-verification[i]`,
     `-boardmember[i]`, `-kyc[i]`;
   - the four scan triggers — `tink-scan-id[i]`, `-basic[i]`, `-passport[i]`,
     `-passport-basic[i]`;
   - the five scanned **image** fields — `tink-scanned-id-portrait[i]`, `-signature[i]`,
     `-ghostportrait[i]`, `-documentrear[i]`, `-barcode[i]`;
   - the attachment pair — `tink-upload-attachment[i]`, `tink-uploaded-attachmentname[i]`;
   - the two one-time-code triggers — `tink-email-verification`, `tink-sms-verification`.

   Two groups that look like they belong here and do not: the **MRZ text fields**
   (`tink-scanned-id-mrz-*`) and the **`tink-verified-orgnumber-*` fields**. They are
   auto-populated, not manual-entry-forbidden. Marking them read-only is still the sensible
   default, but it is a choice, not a catalogue rule.

   Everything the signer types must stay writable: `tink-input-fullname`,
   `tink-email-recipient`, `tink-sign-and-pay-email[i]`, `tink-search-*`, both `tink-share-*`
   attributes and the two `tink-format-*` attributes. Read-only on one of those produces a
   field nobody can complete.
4. **A signature is never a form field.** Formify's signing overlay is painted in that
   zone; a widget or a printed line collides with it. Leave the space empty and let the
   signing configuration place the signature.
5. **A radio option containing `/` corrupts the file.** The export value becomes a PDF name
   object and `/` terminates it — a bilingual option like `Nej / No` once produced a file
   no reader could parse. Use a dash in the stored value; the visible label can keep the
   slash.
6. **What a signer types is limited to the WinAnsi character set.** `š ž å ä ö é` are fine;
   `č ć đ ł ř` are not. Page text has no such limit — this applies to values typed into a
   widget.
7. **A field cannot carry a pre-set value through an attribute.** There is no pre-fill
   attribute in this catalogue. An agreed amount belongs in printed text; writing it into a
   label renames the field for every downstream integration.
