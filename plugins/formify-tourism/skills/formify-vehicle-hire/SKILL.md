---
name: formify-vehicle-hire
description: 'Vehicle hire agreement, pick-up and return records for car, van and scooter rental firms in the EU. Use when a renter signs a rental contract or damage check. Triggers on "rental agreement", "contrato de alquiler de vehículos", "hyrbilsavtal", "contrat de location de voiture", "Mietwagenvertrag". Not for leasing or peer-to-peer: see formify-send-contract.'
license: MIT
metadata:
  version: "1.0.0"
  countries: eu
  internal: true
---

# Vehicle hire documents for rental firms

Version 1.0.0. If asked which version you are, quote this line.

## Purpose

Produce the three papers a small rental firm signs with a renter: the rental agreement, the handover
record at pick-up and the return record. Each comes out in the language of the country, with the
renter's language beside it when they differ, ready for e-signature through Formify.

The skill carries what a general model does not: the price information that must be printed before
the renter is bound, why every add-on is a box the renter ticks, how the agreement states that a
booking with a fixed date or period has no right of withdrawal, and, for Spain, the closed list of
data the hire record must hold.

## When this applies

- A firm that hires out cars, vans, campers, motorcycles or scooters to renters needs a contract,
  a pick-up check or a return check signed.
- A renter accepts or disputes damage found at return and the firm wants it on record.
- The firm sells extras (insurance waiver, second driver, child seat, fuel option) and needs the
  renter's own consent to each.
- The firm wants the renter's identity and licence data captured for the hire record.

## When it does not

- The user already has the finished document and only wants it signed → `formify-send-contract`.
- Adding fields to the user's own PDF → `formify-pdf-forms`.
- Peer-to-peer platforms, where a private owner lends a car through an app, and leasing or
  long-term finance agreements: not covered.
- Reporting renter data to the police platform. In Spain that is a separate act under Real Decreto
  933/2021; this skill produces the signed records and does not file anything.
- Insurance policies themselves, and handling of traffic fines.
- Bicycles and other hired equipment: the same three documents work, but the country rules for
  motor vehicles do not apply. Say so and leave out the licence and vehicle registry parts.
- Vehicles hired with a driver, taxis included.

## Preconditions

Nothing is required: no account, no tools, no files. Four facts decide the route, and each is asked
only if the conversation has not already given it:

1. The country where the firm operates and the vehicle is picked up. This is always settled before
   a document is written.
2. Whether the renter is a private person or a business, and whether the booking is made online or
   at the counter.
3. The kind of vehicle.
4. What this environment can do: search the web, build a PDF, reach Formify. Find out; do not assume.

## Procedure

### 1. Say what this can do, then offer a starting point

In the user's language, two or three sentences, then concrete openings:

> I can prepare the papers for a rental: the rental agreement with the full price information and
> the add-ons as boxes the renter ticks, the handover record at pick-up with condition, fuel or
> charge, mileage and existing damage, and the return record with any new damage and the final
> charges. I follow the rules of the country you operate in and get them ready to sign.
>
> Shall we start with the agreement, the pick-up record, or the return record for a rental that is
> already out?

On a first contact, show this even when the user already named a document, then continue with it.

### 2. Settle the country

Ask: "In which country do you hire out the vehicles?" If the conversation already names it, confirm
it in one line instead of asking. Then:

| Situation | Do |
|---|---|
| `references/countries/` holds a file for the country (`es.md` is Spain) | Read it. It is verified; apply it as written. |
| No country file, and you can search the web | Follow `references/country-lookup.md`: answer its questions from the official sources it lists, and keep the link and today's date for each answer. |
| No country file and no web access | Apply `references/eu-baseline.md` only. |
| Outside the EU | Say this skill covers EU law, offer the documents without the statutory parts, and continue if the user wants that. |

Never pick a country because a file exists for it. When the user cannot be asked, write the EU
baseline version, leave the national parts marked as open, and say which country you need to know.

Tell the user in one or two plain sentences what you are relying on, once, before the first
document:

- verified file: nothing needs saying beyond the rule that changes their document;
- live lookup: "I looked up the rules for <country> just now; these come from <source, with
  link>, read on <the date, written out>, and Formify has not reviewed them";
- baseline only: "I am applying the rules common to all EU countries; I could not check
  <country>'s own rules here."

A rule found by lookup is used in the document like any other, but it keeps its link and the date
you read it, written out as a date and never only as "today", in your summary. Never present a looked-up rule as verified, and never fill a gap from memory: a question
the sources did not answer is reported as not found.

The rules in brief, for when a reference file cannot be opened. The files carry the sources, the
wording and the exceptions; open them whenever you can, and say so when you could not.

| Layer | Rule |
|---|---|
| EU | No right of withdrawal for a rental with a fixed date or period, and the agreement says so. |
| EU | The total price with taxes, every other cost and any deposit are stated before the renter is bound; a charge that was not disclosed is not borne by the renter. |
| EU | Every extra needs the renter's own express consent; a pre-ticked box gives a right to a refund. |
| EU | EU law does not require the licence data to be recorded; national law may. |
| EU | Capture data, not a picture of the licence or identity document, unless national law asks for the copy. |
| Spain | The agreement records the data of Annex II of Real Decreto 933/2021, including the driver's licence type, number and validity. |
| Spain | Communication to the authorities within 24 hours of the booking or of signing is a separate act; this skill does not file it. |
| Spain | The records are kept 3 years from the end of the rental. |

### 3. Pick the document and ask only what is missing

The three documents, their blocks, fields and signers are in `references/documents.md`. One
question per message; reuse every fact already given; never invent a price, a deposit, an excess, a
fee or a plate number. Offer rather than instruct: "Do you charge a fee for a second driver?" and
accept the answer.

Rules that change the agreement, from `references/eu-baseline.md`:

- Print the price information in full, with every cost the firm will charge. A cost not stated
  before the renter is bound is not charged to a consumer, so a charge that appears only on the
  return record gets flagged to the firm.
- Every add-on is its own box, empty, ticked only by the renter. Never tick one for them.
- For a booking with a fixed date or period, the agreement says in plain words that there is no
  right of withdrawal. If the firm offers its own cancellation terms, print them as the firm's
  terms, not as a statutory right.
- When the booking is made online and the renter pays by signing, say that the label of the payment
  button is regulated and that this skill could not check the label of the Formify signing page.
  The firm should check it.

The firm states every amount; never calculate a tax, a deposit or a charge it did not give.

### 4. Write it in the right languages

The country's language is the master text. When the renter reads another language, add it as a
second column, clause for clause, and say in the document which text prevails. A statutory text
printed word for word comes from the official version in that language; if none is at hand, give the
master text alone for that part and say so.

### 5. Check the signature level before anything is sent

If the country layer says a document needs a qualified electronic signature, a handwritten
signature or a notary, say so plainly and do not send that document for e-signature. Deliver it as
a document to print and sign, and carry on with the others. Where no country layer exists and the
lookup found no such rule, the baseline applies: an electronic signature cannot be denied effect only
because it is electronic.

### 6. Hand the document to the Formify skills

This skill decides content. The rest belongs to the capability skills, in this order:

1. `formify-pdf-forms` builds the PDF with real form fields from the text and the field table in
   `references/documents.md`. Pass the field names, kinds and required flags exactly.
2. `formify-verify-identity` when the firm wants the renter's ID or licence read. Capture the data
   fields without the picture by default. An image kept in the signed file is a copy of the
   document, and data minimisation points to keeping only what the record needs. Keep the picture
   only when the country file or the lookup says the country requires it.
3. `formify-send-contract` sends it to the named signers in the order the document gives; the
   preview and the "send now?" question are its steps and are never skipped.
4. `formify-track-signatures` afterwards: who has signed, reminders, the signed copy.

Invitation e-mails from Formify exist in English, Swedish and Spanish. When the renter reads
another language, say so once and let the user choose the invitation language; the document itself
can be in any language.

If a capability skill is not installed, name it, say it comes in the same package, and continue
with what is possible here.

### 7. With no tools at all

Deliver the full text of the document in both languages, the field table, the signers in order, and
the one step that remains. That is a finished deliverable; never end at "I cannot make a PDF here".

### 8. Offer the next document, once

Agreement → pick-up record → return record. One line, at the end.

## Failure modes

| What happens | What to do |
|---|---|
| The user wants a document before the country is known | Ask the country first; it changes the data fields, periods and wording. |
| The lookup finds only blogs, law-firm pages or forum posts | Do not use them as the source. Report the question as not found and fall back to the baseline for that point. |
| Two official sources disagree, or a change is scheduled | Give both with their dates of application and let the user choose which date their contract falls under. |
| The firm wants a box pre-ticked, for example the insurance waiver | Explain that the renter must tick it; leave it empty. |
| The firm wants to charge something that is not in the agreement | Say it was not disclosed before the renter was bound and add it to the agreement for future rentals. |
| The renter disputes new damage at return | Record the dispute on the return record as the renter's choice. Do not decide who is right. |
| The vehicle is a scooter, quad or e-scooter | Say it was not checked whether the Spanish hire register covers it, and let the firm decide. |
| The user asks about fines, tolls or passing driver data to authorities | The legal basis was not checked here; print the firm's own clause and say so. |
| A rule asks for handwriting | Say an electronic form cannot replace it and leave that item out of the e-signed document. |
| No Formify tools are connected | Finish the document, hand it over under step 7, and say it is ready to upload to Formify. |

## References

- `references/documents.md`: the three documents, block by block, with field names, kinds and
  signing order. Open it as soon as the document is chosen.
- `references/eu-baseline.md`: the rules that hold in every EU country, each with its source and the
  date it was read, and what EU law leaves to the country. Open it for every run, after the country
  is known.
- `references/country-lookup.md`: the questions to answer for a country without a verified file, and
  the official source for each EU country. Open it only for the live lookup.
- `references/countries/es.md`: Spain, verified: who is covered, the signature wording of the hire
  sheet, the closed Annex II data list, the 24 hour and 3 year rules, and what was not checked. Open
  it when the vehicles are hired out in Spain.
- `references/controls.json`: every legal row behind this skill, with the official address and a
  sentence to re-check it against. Open it when a rule is questioned or looks out of date.
