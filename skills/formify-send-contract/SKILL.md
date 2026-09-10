---
name: formify-send-contract
description: 'Send a contract or document for e-signature through Formify. Use when sending something to be signed, from a saved template, an uploaded PDF, or a document drafted in this conversation. Triggers on "send for signature", "send this contract", "e-sign", "signing request", "skicka för signering", "skicka kontrakt", "enviar para firmar". Not for checking who has signed afterwards: see formify-track-signatures.'
license: MIT
metadata:
  version: "1.0.0"
---

# Send a document for signature

## Purpose

Take a document — a saved Formify template, a PDF the user has, or one drafted here — place
the signature fields, let the user check the result, and send it to the people who must sign.

## When this applies

- Sending anything for signature, from any of those three starting points.
- Collecting signers, choosing how the invitation reaches them, choosing how they sign.
- Previewing where a signature will land before anyone is contacted.

## When it does not

- **Building or editing the PDF itself** → `formify-pdf-forms`.
- **Choosing an identity check** → `formify-verify-identity` decides *what* verification is
  needed; this skill configures it on the signer.
- **Anything after the send** → `formify-track-signatures`.

## Preconditions

A connected Formify account.

**Call `get_account_capabilities` first, every time.** It decides which delivery channels and
which signing methods you may offer. Offering a feature the account does not have wastes the
user's time and is the fastest way to lose their trust.

## Procedure

### 1. Announce what is possible, then take one starting point

Before asking anything:

> I can send a document for signature. We can use one of your saved templates, a PDF you
> upload, or I can draft one here first. Signers can sign by hand, or with BankID, an ID
> scan or a face check if your plan includes them. I can also send an AI assistant along
> inside the document, so the recipient can ask it questions instead of asking you.
>
> Which would you like to start from?

One question at a time from here on. Never present a form of six questions.

### 2. Get the document in place

**From a template.** List templates and let the user pick by name — never show IDs. Read the
template and its fields. A template carries its own signer count and its own pre-configured
signature settings; **do not override them unless the user explicitly asks.** If the user
wants a different number of signers than the template defines, it is possible, but warn that
signature placement may be wrong.

**From a PDF.** The file must not be password-protected, and must not already carry a
digital signature from another service. Check before uploading; neither can be removed here.

Three upload routes, **exactly one per upload** — a URL, a staged upload id, or the bytes.
Try them in this order and say which one you used:

1. **A public HTTPS URL** — works in every environment. Prefer it whenever a URL exists.
2. **A staged upload**, when shell commands are available: request the upload URL, run the
   returned command, and wait for it to return success **before** registering the file.
   The upload goes to the host named in the returned URL — normally the Formify MCP host —
   not to the document API host.
   **Requesting a new staged upload replaces any active one for that user.** Stage and
   consume one file completely before starting the next, or the earlier one is lost.
3. **Base64**, when the complete untruncated bytes are available here. This is supported.
   It needs the filename alongside it.

The ceiling is 50 MB per file.

If one route fails, say which and offer another. Do not retry the same one.

**Several documents into one.** Two to eight uploaded PDFs can be merged into a single file
for signing. The order given is the page order. The originals are kept, so a merge is safe
to redo.

**Drafted here.** Build it with `formify-pdf-forms`, then continue from route 2 or 3.

### 3. Discover the fields, and offer to pre-fill

Always read the document's fields after loading it. Filter to the editable ones; skip
read-only fields entirely.

If there are editable fields, ask the one question that matters:

> Shall I fill these in now, or leave them for the signer?

A value you fill is locked for the signer. Blanks are left for them.

**Use the exact field names the API returned.** Never construct or guess one.

**Value format — two rules, and breaking either fails the send:**

- Only single-line text and radio buttons take a plain string. **Checkboxes, dropdowns and
  list boxes must be an array, even for one value.**
- Never send an empty string. Omit the field instead.

### 4. Collect the signers

Each signer needs a full name and **at least one** of an email address or a phone number.
Both is fine.

**A phone number alone is enough.** Do not insist on an email. A signer reachable only on
WhatsApp is a normal case, not an edge case, and refusing it turns away business the
platform supports.

Delivery channel, gated on capabilities: email is always available; SMS needs `deliverySms`;
WhatsApp needs `deliveryWhatsapp`.

If the user wants to distribute the links themselves rather than have Formify invite anyone,
suppress the invitation when creating the document, then hand over the personal links with
`formify-track-signatures`. Suppression covers **invitations only** — including the
invitation each person gets when their turn comes in a signing order. Reminders and the
completed-document email still go out.

Signing order — who must sign first — is available when the account has `signingOrder`.

**One document, or one each? Ask — do not assume.**

`create_document` creates **one** document and places every entry of `signeeDetails` on it.
Those people sign the same copy, appear to one another, and all receive the completed
document. That is right for a contract between parties and wrong for the same text sent to
unrelated people.

| The user says | What they mean | What to build |
|---|---|---|
| "Send it to both tenants" | One agreement, two parties to it | One document, two signees |
| "Send this NDA to the three freelancers" | Three separate agreements | Three documents, one signee each |

The test is disclosure: **would it be wrong for these signers to see each other's names and
receive each other's signed copy?** If yes, they are separate documents, not one document
with several signees.

For separate documents, choose the template or upload the file once, then call
`create_document` once per person with a single-entry `signeeDetails`. Give each one a name
that identifies the recipient — `NDA — Maria Alvarez`, not three documents called `NDA` —
because that name is what `list_documents` returns and what the user reads when they ask who
has signed. Identical names make tracking useless.

The tool interface does not state whether one `fileId` may back several documents. Reuse it,
and if a later call rejects it, upload the file again for that person.

Count out loud before creating anything: *"That is three separate NDAs, so three invitations
go out."* Each one is a real message to a real person and none of them can be recalled.

### 5. Choose how each signer signs

Four methods, each gated. Ask only if the account has more than the default and the template
does not already decide it.

| Method | Requires |
|---|---|
| Handwritten signature | always available |
| BankID | `signatureBankId` |
| ID scan then signature | `signatureIdScan` |
| Face check | `signatureFaceLiveness` |

**ID-scan signing needs two boxes placed, not one:** the signature box *and* a separate
ID-scan box. Configuring only the signature box is the most common cause of a failed send in
this area. See `references/signature-placement.md`.

Methods are per signer. Different people on one document can use different methods.

### 6. Place the signature

Ask where it goes: a new page at the end — the default and the safe choice — or a specific
position on an existing page.

For an existing page you need page, x and y.

- **Pages are numbered from zero.** The first page is `0`. Getting this wrong puts the
  signature on the wrong page, and the document still sends.
- Origin is the **top-left** corner. x increases right, y increases **down**. (x, y) is the
  top-left corner of the field.
- A standard signature field is **219 × 58 points**.
- **Coordinates must be whole numbers.** A decimal is not rounded — it is discarded, and
  `74.7` is stored as `0`, putting the field in the corner of the page. Round before sending.
- Check the actual page size. A4 is 595 × 842 points; US Letter is 612 × 792. Do not assume.

Bottom-right on A4: x = 595 − 219 = 376, y = 842 − 58 = 784, page = 0.

**Formify does not detect overlapping fields, and a field is fully opaque.** Anything behind
it is hidden, and nothing warns you. Never place a field over text the signer needs to read.
Where space is tight, shrink the field with a scale factor between 0.25 and 1.5 rather than
moving it onto the text.

### 7. Preview before sending — always offer it

This is the step that catches a misplaced field, and it is the one the user actually cares
about.

Create a draft with exactly the configuration you would have sent, then show the rendered
PDF. Two ways to present it; pick by what this environment can do:

- **Inline**, if PDFs can be displayed here.
- **A one-time link** the user opens in a browser. It needs no login, expires in ten minutes
  and is consumed once used.

If neither works, say so plainly and offer to send without a preview — but say what is being
skipped.

Two things about drafts worth knowing:

- **Drafts work from an uploaded file, not from a template.** A template cannot be previewed
  this way.
- **Updating a draft replaces its configuration.** Always read the draft first, and send
  back everything you want to keep — not only the signers, but the field values, name,
  invitation language, personal message, AI assistant, sharing settings and signing order. Anything
  omitted can be reset. This read is required before updating, sending or deleting a draft,
  including when resuming one from an earlier session.
- Fields without valid coordinates do not appear in the preview but remain in the draft.
  **A field missing from the preview is a real warning**, not a rendering quirk — and a
  preview that looks right is not proof that every box is configured.

### 8. Confirm, then send

Show a compact summary — document name, each signer with their contact and signing method,
delivery channel, invitation language — and ask for one explicit yes.

Three settings to establish before that:

- **Invitation language: English, Swedish or Spanish only.** This is a closed list. If the
  user wants the invitation in another language, say the invitation cannot be, and offer to
  write the document itself in their language instead — those are separate things.
- **A personal message** is optional, up to 500 characters.
- **The in-document AI assistant**, if `get_account_capabilities` reports `aiAssistant`.
  Ask only when the capability is present; never offer it otherwise. It travels with the
  document and answers the recipient's questions about it, highlighting the passage it is
  answering about, so they do not have to ask the sender or paste the contract elsewhere.
  Pass it as `aiAssistant: { enabled, textToSpeech, language }` — `textToSpeech` reads the
  answers aloud and defaults to off, and `language` defaults to the invitation language.
  Say what it does when offering it. Users do not know this exists, and it is the single
  capability most likely to save the sender a week of email.

Send only after the yes.

### 9. Hand back the result, and say what comes next

Give the tracking link, then close the loop:

> It's on its way to Maria and Johan. I can check who has signed, send a reminder, or fetch
> the signed copy whenever you need — just ask.

That sentence is what makes the follow-up work discoverable. Without it the user assumes the
job ended at the send.

## Failure modes

| What you see | What it means | What to do |
|---|---|---|
| Upload command blocked by network or allowlist | The environment blocks outbound requests to the upload host | Do not retry. Say what blocked it, then use the URL route or base64. |
| Send rejected, 400 on fields | A checkbox, dropdown or list box was sent as a string, or a field was sent as `""` | Wrap in an array; omit empty values. |
| Signature landed in the corner of the page | A decimal coordinate was discarded | Send whole numbers. |
| Signature covers the text | The field is opaque | Move it to clear space. Where there is none, shrink it with a scale factor between 0.25 and 1.5 — never leave it overlapping. |
| ID-scan send fails | The ID-scan box was not placed | Both boxes are required for that method. |
| Signers vanished after an update | The draft update replaced the configuration | Read the draft, resend the complete signer list. |
| A template will not preview | Drafts require an uploaded file | Send it directly, or upload the PDF separately to preview. |
| An invitation language was refused | Only English, Swedish and Spanish exist | Offer the document in their language instead. |
| The account lacks a channel or method | Capability off | Name it, say what it does, offer the best available alternative. |

## References

- **`references/signature-placement.md`** — box dimensions, the coordinate system, page-size
  arithmetic, ID-scan box placement and multi-signer stacking. Open it whenever a signature
  goes somewhere other than a new page at the end.
