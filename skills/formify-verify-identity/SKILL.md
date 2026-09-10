---
name: formify-verify-identity
description: 'Verify a signer with BankID, ID scan, face liveness or company lookup. Use when a signature needs proof of who signed, for KYC or anti-money-laundering, when scanning an ID document, or when verifying a company registration number. Triggers on "BankID", "ID scan", "verify identity", "KYC", "AML", "face liveness", "legitimering", "identitetskontroll", "verificar identidad". Not for ordinary signing without identity checks: see formify-send-contract.'
license: MIT
metadata:
  version: "1.1.0"
---

# Verify who is signing

## Purpose

Bind a signature to a verified person or company. Formify can check an identity document,
match a live face against it, authenticate through Swedish BankID, look up a company
registration number, or require a one-time code before a document opens — and attach the
result to the signature rather than leaving it as a separate errand.

## When this applies

- A signature needs proof of **who** signed, not just that someone did.
- KYC or anti-money-laundering obligations apply.
- A company must be verified, or its board member or beneficial owner identified.
- An ID document must be scanned, or its data captured without storing the picture.

## When it does not

- **Ordinary signing with no identity requirement** → `formify-send-contract`.
- **Building the PDF fields themselves** → `formify-pdf-forms`. This skill decides *what*
  verification is needed; that one writes the fields it needs.

## Preconditions

**Every feature here is gated on the account, and you must check before offering.** Call
`get_account_capabilities` first. Offering BankID to an account that does not have it wastes
the user's time and ends the conversation badly.

The keys that matter here:

| Key | Unlocks |
|---|---|
| `signatureBankId` | BankID signing |
| `signatureIdScan` | ID-document scan as part of signing |
| `signatureFaceLiveness` | Live face check |
| `verificationEmail` / `verificationPhone` | One-time code before the document opens |
| `verificationToOpen` | Requiring that code to open at all |

If a needed capability is off, say what it would do and what it needs, then offer the
strongest option the account *does* have. Never silently downgrade.

## Two separate layers — do not confuse them

This is the distinction that causes the most expensive mistakes.

| Layer | What it is | Where it is set |
|---|---|---|
| **Signing method** | How the person signs and authenticates | On the signer, when the document is sent |
| **Document fields** | What is collected or verified *inside* the document | `tink-*` attributes in the PDF, built beforehand |

A company check inside a form is a **field**. BankID as the signing method is a **signer
setting**. They are configured in different places, at different times, and one does not
imply the other.

## Procedure

### 1. Ask what the user actually needs to prove

Not which feature they want — what they need to be true. There are four distinct answers,
and they lead to different places:

- *"I need to know this is really them."* → a signing method.
- *"I need their passport details in the document."* → document fields.
- *"I need to check the company is real and who can sign for it."* → company verification
  fields.
- *"I need a record for compliance."* → KYC, which is a specific variant, not a synonym.

One question at a time. If they name a regulation rather than a feature, translate it —
Swedish AML obligations under money-laundering rules usually mean company verification plus
retained identification, not a face check.

### 2. Choose the signing method

Four values. Each is gated as shown above. They differ in what they prove, not in a
ranking Formify publishes — do not tell a user that one satisfies a legal signature
class the others do not.

| Method | What the signer does |
|---|---|
| `digital_ink` | Draws a signature. Always available, no capability needed. |
| `bankid_identification` | Authenticates with Swedish BankID |
| `digital_ink_id_scan` | Photographs an identity document, then signs |
| `face_liveness` | Live face check bound to the signature |

**`digital_ink_id_scan` requires two boxes to be placed, not one:** the signature box and a
separate ID-scan box. Sending it with only the signature box configured is the single most
common failure in this area — see `formify-send-contract` for placement.

Methods are set per signer. Different signers on one document can use different methods.

### 3. Decide what goes inside the document

Only if data must live in the document itself. Read `references/tink-attributes.md` and
follow it exactly — the catalogue is closed and an unknown attribute fails silently.

**Company verification.** Three triggers: beneficial owner, board member, and the KYC
variant whose result is retained for compliance. Each must be paired, in the same field
name, with the field that receives the verified value — a trigger alone is a dead button.
Verified company name, address, postcode and city can all be auto-filled.

**Identity document capture.** Choose deliberately between the data and the picture:

- Trigger alone → the field is replaced by the **front-side image** of the document.
- Trigger combined with machine-readable-zone attributes → **no image is stored at all**;
  the fields receive name, document number, nationality, dates and so on as text.

The second is the data-minimisation pattern and it carries legal weight: keeping a copy of
an identity document needs its own legal basis. **When the user needs the details but not
the picture, say so and use it.** Most do not know it is an option.

**One-time codes.** Email or SMS verification before the document opens. Not indexed, and
gated on `verificationEmail` / `verificationPhone`.

### 4. Do not make them scan twice

If a signer will both scan a document and pass a face check, combine
`tink-scanned-id-allow-in-signature[index]` on the scan trigger. A **fully successful** scan
is then carried into the Live ID signature and the signer goes straight to the face check
without photographing anything again. The face check itself still runs.

An incomplete scan is never reusable. The index here is the scan group, not a signature
number.

### 5. Say what will happen, in the signer's terms

Before sending, tell the user what the person on the other end will experience:

> Maria will get an email, open the document, be asked to photograph her ID card, then take
> a short video selfie so we can confirm it is her. Then she signs. It takes about two
> minutes.

Identity checks are the step that makes recipients abandon a document. A sender who knows
what it looks like can warn them, and completion rates hold.

### 6. State the boundary honestly

Selecting a verification method configures a check. It does not, by itself, establish a
legal signature class, guarantee acceptance in a given jurisdiction, or constitute a
compliance programme. If the user asks whether this satisfies a specific regulation, say
what the product does and does not decide, and let them confirm with their own adviser.

Do not describe a document as "KYC compliant" because it carries a KYC trigger.

## Failure modes

| What you see | What it means | What to do |
|---|---|---|
| A method is not offered | The capability is off for this account | Say which one and what it does; offer the best available alternative. |
| ID-scan signing fails at send | The ID-scan box was not placed | Both boxes are required for that method. Place it and resend. |
| The verification button is not clickable | Trigger has no paired value field, or the field is not read-only | Pair it; set read-only on the widget itself. |
| The scan runs twice | Two triggers in one group, or the reuse modifier is missing | One trigger per person; add the modifier if a face check follows. |
| Fields never fill after a successful scan | Brackets missing, or indices renumbered when a person was inserted | Check the index on every field of that group. |
| An ID image appears when the user wanted only data | Trigger used alone | Combine with the machine-readable-zone attributes. |

## References

- **`references/tink-attributes.md`** — the complete catalogue of document markers, their
  combinations and required image shapes. Open it before writing any attribute; an invented
  one produces a document that looks correct and does nothing.
