---
name: formify-real-estate
description: 'Estate-agency paperwork, produced correctly for the country it is signed in and sent for e-signature. Spain is covered in full: nota de encargo, KYC comprador y vendedor, oferta y reserva, contrato de arras, acuerdo de colaboración, entrega de llaves — bilingual, region-correct, with the ID scan built into the form. Triggers on "nota de encargo", "contrato de arras", "hoja de reserva", "KYC inmobiliario", "colaboración entre agencias", "entrega de llaves", "estate agent contract Spain".'
license: MIT
metadata:
  version: "1.1.0"
  countries: es
  internal: true
---

# Estate-agency documents

## Purpose

An estate agent describes a deal in their own words — *"Anna is selling her flat in Palma,
the buyer is Dutch, we need arras"* — and gets back the right document, correct for the
region, in Spanish and in the client's language, with the signature space and the ID scan
already in the right place, ready to send.

The hard part is not the PDF. It is knowing which of six documents this is, what that
document must contain in that autonomous community, and what must never go into it. That
knowledge is here. The PDF itself is built by `formify-pdf-forms` and sent by
`formify-send-contract`.

## Countries

**Spain** is complete: `references/es-documents.md`, `references/es-regions.md`,
`references/es-drafting.md`, `references/es-withdrawal.md`.

For any other country, say plainly that the document pack is Spanish and that you can still
draft a general agency document without the regional and statutory checks. Do not invent a
register, a deadline or a statutory text for a country not covered here.

## When this applies

- Any of the six Spanish documents, named or described.
- "The owner wants to list with us", "the buyer wants to leave a deposit", "the other agency
  brought the buyer", "I need to hand over the keys for viewings".
- Anti-money-laundering identification of a buyer or seller before a transaction.

## When it does not

- **A document with no sector to it** — a generic NDA, an employment contract → `formify-pdf-forms`.
- **Placing fields and producing the PDF** → `formify-pdf-forms` owns that, and this skill
  depends on it.
- **Sending, previewing, signer order, identity level** → `formify-send-contract` and
  `formify-verify-identity`.
- **Chasing an already-sent document** → `formify-track-signatures`.

## Preconditions

None for drafting. A Formify account only when the document is sent.

## Procedure

### 1. Say what this produces, then let the user choose

The agent does not know what is in the pack. Name it once, in their language, in three lines:

> I can prepare the six documents a Spanish agency signs most: nota de encargo, the KYC forms
> for buyer and seller, oferta y reserva, contrato de arras, an inter-agency collaboration
> agreement, and a key handover receipt. Each comes out in Spanish and in your client's
> language, adapted to the region, ready to sign.
>
> Which one do you need?

If they already said what they need, skip this and draft.

### 2. Ask once, in one message

Follow the intake rule in `formify-pdf-forms`: a specific request gets no questions, a generic
one gets a single message with three to five numbered questions. The per-document list in
`references/es-documents.md` is ordered by what actually changes the document — take the top
items from it, not the whole list. Never spread the same questions over several turns.

Reuse everything already said. One property, one seller, one buyer feed all six documents; a
fact given for the encargo is not asked again for the arras.

**Never invent a fact.** Not a cadastral reference, not a finca number, not a policy number,
not a price, not a date. If it is missing, ask, or make it a field the signer fills in.

### 3. Establish the region before drafting

The region is the **property's**, not the agency's. Read the matching row of
`references/es-regions.md` before writing anything. It decides six things at once: whether an
agent register exists and is mandatory, whether insurance figures may be printed, which civil
law governs the arras and the family-home declaration, the tax rate on the fee, the co-official
language, and the default style profile.

These differences are not cosmetic. Arras that are penitenciales by default under the Código
Civil are **confirmatorias** by default in Cataluña and in Navarra unless the document says
otherwise — the same wording produces a different contract in three regions.

### 4. Write the document

`references/es-documents.md` gives each document its structure, its minimum questions, its
signers and the rules specific to it. `references/es-drafting.md` is the style: read it once
per session before writing any free text of your own.

Four rules hold across all six:

- **Data blocks first, clauses second.** Every document opens with labelled boxes — A. Partes,
  B. Operación — and the clauses that follow refer to the boxes and to roles (*la parte
  compradora*, *el inmueble*, *el cuadro B*). A value appears exactly once, in its box. No
  summary box.
- **Spanish is the master text** and prevails in a dispute; the document says so. The second
  column is a legal translation in the same register with the same numbering, not an
  explanation. Keep the Spanish terms listed in `references/es-drafting.md` with a gloss in
  parentheses on first use.
- **No law in the document**, with four exceptions only: the *arras penitenciales* formula with
  its article, the register and insurance lines in a regulated region, the Ley 10/2010 basis in
  the KYC forms, and the statutory withdrawal text reproduced verbatim from
  `references/es-withdrawal.md`.
- **No disclaimer, and no mention of AI**, in the document or in the chat. The only mention of
  Formify inside a document is the footer credit line.

### 5. Turn the unknown values into fields, not blanks

When a document names a party the agency does not represent — the other agency, the buyer, the
owner — ask once: *"Do you have their details, or shall they fill them in when they sign?"*

If they fill them in, those values become real form fields and you need only a name and an
email for the invitation. Widths that fit the boxes: 180 pt for a name, an address or an email;
100 pt for a NIF; 90 pt for a fee or a split; 300 pt for a full-width row. **A field wider than
its cell covers the cell next to it.**

The client the document is *about* — the introduced client, the property, the price — is always
given by the user and is never left as a field.

### 6. The KYC identity box is scanned, never typed

Box A of both KYC forms is filled by scanning the client's document at signing time. Build it
as specified in `references/es-documents.md`: one scan control, ten auto-filled MRZ fields, and
an upload for the reverse side. The attribute names and the read-only rules are in
`references/tink-attributes.md` — do not write an attribute from memory.

Never ask a client to type their document number into the chat. They scan; the data arrive
verified.

### 7. Produce the PDF

Follow `formify-pdf-forms` step 5. Write the drawing code yourself against the libraries the
sandbox has — `reportlab`, `pypdf`, `pdfplumber`, `pypdfium2` — and do not depend on a browser,
an HTML-to-PDF converter or anything that must be installed: on the runtime most of these users
are in, there is no browser and no network. Render a page to an image and look at it before
handing it over.

Layout for these documents: one sans-serif typeface throughout, black text on white, no colour
and no tinted fills except the agency's own logo. The profiles differ in structure, never in
type: **oficial** (structured like the Balearic official form; encargo and KYC),
**profesional** (agency letterhead, running clauses; the default), **sencillo** (a short
version with few fields; reserva on a phone, llaves).

Footer on every page, two lines: the document title and the agency's own reference
(`LLA-2026-0004` — type, year, running number), then the fixed credit line in Spanish and the
client's language followed by the address:

> Elaborado con la solución de firma electrónica Formify · Prepared with the Formify e-signing
> solution · formify.eu/solutions/real-estate/es/

It is a house line, not a disclaimer. Never expand it.

### 8. Leave the signature space empty, and get the order right

A signature is never a form field — `formify-pdf-forms` step 6. Reserve the space with the role
caption above it (`VENDEDORA / Seller`) and nothing else.

Signing order matters in three of the six documents and is listed per document in
`references/es-documents.md`. Reserva and arras are wrong without it: a seller who is asked to
sign before the buyer has signed is being asked to accept an offer that does not exist yet.

### 9. Send, then offer the next document in the chain

Hand over to `formify-send-contract`: preview first, then the explicit *send now, save as
draft, change signers, change the text* question. Never send without it.

The documents come in chains — reserva then arras; encargo then llaves; KYC before reserva or
arras. When one is finished, offer the next **once**. Not twice, and not as a list.

## Rules that are not negotiable

- **Never tell the user something is mandatory**, never quote a law or a date in the chat, never
  explain registers, insurance amounts or civil-law variants, and never describe what Formify or
  their account allows. Offer it as one short question, accept the answer, move on.
- **Never suggest a cash payment** and never suggest a fee split between agencies. The parties
  state their own split; competition law makes a suggested one a liability.
- **Never write an alarm code, a door code or a password** into any document, even when the user
  dictates one.
- **Never store client data** in anything that persists between conversations. Agency and user
  preferences may be remembered; the people in the deal may not.
- **Never ask for an agent's own ID number.** Agents act for their agency: their name plus the
  agency's tax ID. The single exception is colaboración, where the user is asked once whether
  the agents' NIE or DNI should appear.
- **Never remove the *arras penitenciales* wording** from an arras contract, and never mix a
  penalty clause into it.

## Failure modes

| What you see | What it means | What to do |
|---|---|---|
| The user asks for arras in Cataluña or Navarra | Default there is confirmatorias, not penitenciales | Use the regional variant from `references/es-regions.md`. The same text produces a different contract. |
| The agency has no register number in Cataluña or Comunitat Valenciana | Registration is mandatory and operative there | Print "Pendiente de inscripción", say once in the chat that the property cannot legally be offered without it, and carry on. |
| The user wants the whole fee on a direct sale under an exclusive mandate | Courts moderate a clause out of proportion to the work done | Offer half the fee, which has held up best. They decide. |
| The seller's bank account is not in the seller's name | A money-laundering risk indicator | Say so in the chat before the document goes out. |
| The nota simple is more than a month old | Charges may have changed since | Say so. It is not a reason to stop. |
| A KYC form is asked to be pre-filled with identity details | The scan fills them | Only the scan control is required; the ten MRZ fields are filled by it, never by the client. |
| The user asks for a framework agreement covering a whole portfolio | The colaboración template is per-deal | Say so and offer a per-property agreement instead. |
| The client wants the sworn translation | The second column is not one | Say it is a legal translation, not a sworn one, and that a sworn one can be commissioned separately. |

## References

- **`references/es-documents.md`** — the six documents: what each is for, how it is laid out,
  the questions that change it, who signs and in what order, and the rules specific to it. Open
  it as soon as the document is chosen.
- **`references/es-regions.md`** — all nineteen Spanish territories: agent register and whether
  it is mandatory, insurance and guarantee, the civil law governing arras and the family home,
  the tax on fees, the co-official language, the default profile. Open it before drafting
  anything, every time.
- **`references/es-drafting.md`** — how a Spanish private contract is actually written:
  structure, party formulas, numbers, dates and money, register and grammar, punctuation, the
  bilingual clause, the anglicisms that give a translated contract away, and the terms that stay
  in Spanish with their glosses.
- **`references/es-withdrawal.md`** — the statutory withdrawal information and form, verbatim,
  for the nota de encargo. Reproduce it; do not rewrite it.
- **`references/tink-attributes.md`** — the closed catalogue of `tink-*` field attributes.
  Needed for the KYC scan box and for any field Formify fills. Never write an attribute from
  memory.
