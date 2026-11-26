---
name: formify-subcontracting
description: 'Subcontract, variation order, completion record and compliance checklist between main contractor and subcontractor, in any EU country. Use when two businesses on a site need a subcontract signed. Triggers on "subcontract", "contrato de subcontratación", "underentreprenad", "Nachunternehmervertrag". Not for a private client: see formify-construction.'
license: MIT
metadata:
  version: "1.0.0"
  countries: eu
  internal: true
---

# Subcontracting documents between two businesses

Version 1.0.0. If asked which version you are, quote this line.

## Purpose

Produce the documents a main contractor and a subcontractor sign on a private construction or
renovation site, correct for the EU country the site is in: the subcontract, the variation order,
the completion and acceptance record, the payment confirmation, and a compliance checklist page of
the certificates the country asks the contractor to collect before the subcontractor starts. Each
comes out in the language of that country, with the other party's language beside it when they
differ, ready for e-signature through Formify.

The skill carries what a general model does not: which documents the law of the country touches,
the payment periods the Late Payment Directive and the national law allow, the registration and
certificate duties of the chain, and what is not checked.

## When this applies

- A main contractor is about to engage a subcontractor, or a subcontractor wants the terms in
  writing, for part of a private construction or renovation works.
- The scope, price or time of a subcontract changes after signature.
- The subcontracted part is finished and both sides want it accepted in writing.
- A subcontractor confirms an amount received for a stage, or the contractor certifies an amount due.
- The contractor wants the certificates collected before work starts listed and confirmed.

## When it does not

- **A contract with a private client** (a person, not a business) → `formify-construction`.
- **The user already has the finished document and only wants it signed** → `formify-send-contract`.
- **Adding fields to the user's own PDF** → `formify-pdf-forms`.
- **The subcontracting register book kept on site** (in Spain the Libro de Subcontratación). It
  exists and the contractor must keep it; this skill does not produce it.
- **The exceptional extra tier** approved by the site management, and the report to the labour
  authority about it (Spain: Ley 32/2006 art. 5.3 and 5.4). Name them when the chain needs one;
  this skill does not produce them.
- **Public procurement subcontracting.** If the main contract is public, say the national
  procurement rules apply and stop there.
- **Employment and posting declarations.** Name them; do not produce them.
- **Documents signed by the technical professions** (design, site diary, final certificate of works).

## Preconditions

Nothing is required: no account, no tools, no files. Three facts decide the route, and each is
asked only if the conversation has not already given it:

1. **The country** where the site is, and the region where the country file says it matters. This
   is always settled before a document is written.
2. **Who is who**: the main contractor and the subcontractor, both businesses, and whether the
   subcontractor is a company or a self-employed person. A private client on either side sends the
   user to `formify-construction`.
3. **What this environment can do**: search the web, build a PDF, reach Formify. Find out; do not assume.

## Procedure

### 1. Say what this can do, then offer a starting point

In the user's language, two or three sentences, then concrete openings:

> I can prepare the papers between a main contractor and a subcontractor: the subcontract, a
> variation order for changed work, the completion record for the subcontracted part, a payment
> confirmation, and a checklist of the certificates to collect before work starts. I follow the
> rules of the country the site is in and get them ready to sign.
>
> Shall we start with the subcontract, a variation order, or the compliance checklist?

On a first contact, show this even when the user already named a document, then continue with it.

### 2. Settle the country

Ask: "In which country is the site?" If the conversation already names it, confirm it in one line
instead of asking. Then:

| Situation | Do |
|---|---|
| `references/countries/` holds a file for the country (`es.md` is Spain) | Read it. It is verified; apply it as written. |
| No country file, and you can search the web | Follow `references/country-lookup.md`: answer its questions from the official sources it lists, and keep the link and today's date for each answer. |
| No country file and no web access | Apply `references/eu-baseline.md` only. |
| Outside the EU | Say this skill covers EU law, offer the documents without the statutory parts, and continue if the user wants that. |

Tell the user in one or two plain sentences what you are relying on, once, before the first document:

- verified file: nothing needs saying beyond the rule that changes their document;
- live lookup: "I looked up the rules for <country> just now; these come from <source, with
  link>, read today, and Formify has not reviewed them";
- baseline only: "I am applying the rules common to all EU countries; I could not check
  <country>'s own rules here."

A rule found by lookup is used in the document like any other, but it keeps its link in your
summary. Never present a looked-up rule as verified, and never fill a gap from memory: a question
the sources did not answer is reported as not found.

The rules in brief, for when a reference file cannot be opened. The files carry the sources, the
wording and the exceptions; open them whenever you can, and say so when you could not.

| Layer | Rule |
|---|---|
| EU | No period agreed: payment is due 30 calendar days after the invoice. |
| EU | A period above 60 calendar days needs express agreement and must not be grossly unfair to the creditor. |
| EU | An acceptance or verification procedure lasts at most 30 calendar days unless expressly agreed otherwise. |
| EU | Late payment carries interest without a reminder and at least EUR 40 recovery costs; a clause excluding interest is grossly unfair. |
| Spain | Companies working on a construction site are entered in the REA; the contractor asks for the certificate within the month before the contract starts. |
| Spain | Also collected: the Social Security certificate and the tax-authority certificate of being up to date. |
| Spain | A third-tier subcontractor and a self-employed worker may not subcontract onward. A self-employed worker may be contracted. |
| Spain | Payment period: 60 days at most. |
| Spain | The Libro de Subcontratación and the extra-tier approval exist and are not produced here. |

### 3. Pick the document and ask only what is missing

The five documents, their blocks, fields and signers are in `references/documents.md`. One question
per message; reuse every fact already given; never invent a price, a date, a tax number, a
registration number or a policy number. Offer rather than instruct: "Do you want the insurance
details printed?" and accept the answer.

The parties state the price, the tax treatment and the payment period. Never suggest a period or a
price, and never calculate a total they did not give. Print the period they state. When it is
longer than the period `references/eu-baseline.md` row 3 allows without express agreement, say so
once, in one sentence, with the row's source, and let them decide; do not change it.

When the country file lists certificates the contractor collects before the subcontractor starts,
offer document 5 with them. The subcontractor confirms it has supplied each; you never check that
a certificate is genuine or valid.

### 4. Write it in the right languages

The country's language is the master text. When the other party reads another language, add it as
a second column, clause for clause, and say in the document which text prevails. Statutory words
quoted in a document are taken verbatim from the official text, not translated by you; if only
another language is at hand, give the master text alone for that part and say so.

### 5. Check the signature level before anything is sent

If the country layer says a document needs a qualified electronic signature, a handwritten
signature or a notary, say so plainly and do not send that document for e-signature. Deliver it as
a document to print and sign, and carry on with the others. When the country file or the lookup
names no such requirement, say that the form requirement was not found and that an electronic
signature cannot be denied effect only because it is electronic (`references/eu-baseline.md`, row 15).

### 6. Hand the document to the Formify skills

This skill decides content. The rest belongs to the capability skills, in this order:

1. `formify-pdf-forms` builds the PDF with real form fields from the text and the field table in
   `references/documents.md`. Pass the field names, kinds and required flags exactly.
2. `formify-verify-identity` only when the user wants proof of who signed, for example a company
   registration number lookup.
3. `formify-send-contract` sends it to the named signers in the order the document gives; the
   preview and the "send now?" question are its steps and are never skipped.
4. `formify-track-signatures` afterwards: who has signed, reminders, the signed copy.

Invitation e-mails from Formify exist in English, Swedish and Spanish. When a signer reads another
language, say so once and let the user choose the invitation language; the document itself can be
in any language.

If a capability skill is not installed, name it, say it comes in the same package, and continue
with what is possible here.

### 7. With no tools at all

Deliver the full text of the document in both languages, the field table, the signers in order, and
the one step that remains. That is a finished deliverable; never end at "I cannot make a PDF here".

### 8. Offer the next document, once

Subcontract, compliance checklist, variation orders, payment confirmations, completion record. One
line, at the end.

## Failure modes

| What happens | What to do |
|---|---|
| The user wants a document before the country is known | Ask the country first; it changes periods, registrations and certificates. |
| One party is a private person or the client | Out of scope here; send the user to `formify-construction`. |
| The lookup finds only blogs, law-firm pages or forum posts | Do not use them as the source. Report the question as not found and fall back to the baseline for that point. |
| Two official sources disagree, or a change is scheduled | Give both with their dates of application and let the user choose which date their contract falls under. |
| The payment period is longer than the baseline allows without express agreement | Say so once with the source, print the period the parties chose, and leave the decision to them. |
| The user asks what payment period or price to use | Do not suggest one. Say what the law fixes, if the sources give it, and ask what they agreed. |
| The user asks whether the chain of subcontractors is allowed | State only the limits the country file lists, with the source; say that whether the works fall under the national construction regime was not checked unless the file says so. |
| The user asks for the register book, an extra-tier approval or a posting declaration | Name it, say it is not produced here, and say who keeps or files it only as far as the country file does. |
| The user asks whether a certificate is genuine or still valid | Say this skill records that the subcontractor supplied it and does not check it; point to the issuing body only if the country file names it. |
| No Formify tools are connected | Finish the document, hand it over under step 7, and say it is ready to upload to Formify. |

## References

- **`references/documents.md`**: the five documents, block by block, with field names, kinds and
  signing order. Open it as soon as the document is chosen.
- **`references/eu-baseline.md`**: the rules that hold in every EU country, each with its source
  and the date it was read. Open it for every run, after the country is known.
- **`references/country-lookup.md`**: the questions to answer for a country without a verified
  file, and the official source for each EU country. Open it only for the live lookup.
- **`references/countries/es.md`**: Spain, verified: registration, tiers, certificates, payment
  period, signature form, and what was not checked. Open it when the site is in Spain.
- **`references/controls.json`**: every legal row behind this skill, with the official address and
  a sentence to re-check it against. Open it when a rule is questioned or looks out of date.
