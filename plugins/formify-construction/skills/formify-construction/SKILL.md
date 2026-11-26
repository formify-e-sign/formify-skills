---
name: formify-construction
description: 'Renovation contract, quote, change order and handover record for a contractor, in any EU country. Use when a builder or tradesperson needs a quote, works contract, withdrawal form or variation order for a private client. Triggers on "works contract", "contrato de obra", "Bauvertrag", "devis travaux", "hantverkaravtal". Not for subcontracts: see formify-subcontracting.'
license: MIT
metadata:
  version: "1.0.0"
  countries: eu
  internal: true
---

# Renovation and construction documents for private clients

Version 1.0.0. If asked which version you are, quote this line.

## Purpose

Produce the documents a contractor signs with a private client, correct for the EU country the
works are in: the quote, the works contract, the withdrawal information and form, the variation
order, the handover record and the warranty note. Each comes out in the language of that country,
with the client's language beside it when they differ, ready for e-signature through Formify.

The skill carries what a general model does not: which of these documents the law of the country
asks for, the periods and wording it fixes, and the statutory withdrawal text word for word.

## When this applies

- A builder, renovation firm or tradesperson is about to quote, contract, change or hand over
  works for a private client.
- A contract is being signed at the client's home, and the right to withdraw may apply.
- The client asks for extra work mid-project and it must be agreed in writing.
- The contractor wants the reduced tax rate for renovation recorded with the client's declaration.

## When it does not

- **A contract between two businesses on a site** → `formify-subcontracting`.
- **The user already has the finished document and only wants it signed** →
  `formify-send-contract`.
- **Adding fields to the user's own PDF** → `formify-pdf-forms`.
- **Documents signed by the technical professions** (design, site diary, final certificate of
  works, energy certificate): many countries ask for a qualified signature or a professional stamp.
  Say so and stop there for that document.
- **Public works and tenders.**
- **Property sale and letting in Spain** → `formify-es-real-estate`, when it is installed.

## Preconditions

Nothing is required: no account, no tools, no files. Three facts decide the route, and each is
asked only if the conversation has not already given it:

1. **The country** where the works take place, and the region where the country file says it
   matters. This is always settled before a document is written.
2. **Whether the client is a private person**, and **where the contract is signed** (the client's
   home, the contractor's premises, at a distance). Together they decide the withdrawal pages.
3. **What this environment can do**: search the web, build a PDF, reach Formify. Find out; do not
   assume.

## Procedure

### 1. Say what this can do, then offer a starting point

In the user's language, two or three sentences, then concrete openings:

> I can prepare the papers for a job with a private client: the quote, the works contract with the
> withdrawal form where the law asks for it, a change order for extra work, and the handover
> record. I follow the rules of the country the works are in and get them ready to sign.
>
> Shall we start with a quote, a contract for a job you have already agreed, or a change order?

On a first contact, show this even when the user already named a document, then continue with it.

### 2. Settle the country

Ask: "In which country are the works?" If the conversation already names it, confirm it in one
line instead of asking. Then:

| Situation | Do |
|---|---|
| `references/countries/` holds a file for the country (`es.md` is Spain) | Read it. It is verified; apply it as written. |
| No country file, and you can search the web | Follow `references/country-lookup.md`: answer its questions from the official sources it lists, and keep the link and today's date for each answer. |
| No country file and no web access | Apply `references/eu-baseline.md` only. |
| Outside the EU | Say this skill covers EU law, offer the documents without the statutory parts, and continue if the user wants that. |

Tell the user in one or two plain sentences what you are relying on, once, before the first
document:

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
| EU | Renovation, repair and annexes for a consumer are covered; a new building or a conversion comparable to one is not. |
| EU | Signed away from the contractor's premises (the client's home): 14 days to withdraw, from the day the contract is concluded. |
| EU | Withdrawal information and model form not given: the period runs 12 months longer. |
| EU | Works start inside the period only on the client's own express request; then a client who withdraws pays for what was done, otherwise nothing. |
| EU | An urgent repair the client asked for has no withdrawal right; extras on the same visit do. |
| EU | The contract and the information go electronic only if the client agrees. |
| Spain | 14 calendar days; 30 for an unsolicited visit to the home. |
| Spain | Catalonia: a written quote with itemised costs, validity, start and duration, two equal spaces to accept or refuse; copies kept 6 months. |
| Spain | Reduced VAT on dwelling renovation: the client signs a three-point declaration; from 1 December 2026 payment must be by card, transfer, nominative cheque or bank deposit. The contractor decides the rate. |
| Spain | The 1, 3 and 10 year periods apply to building works under the building act, not to a kitchen or bathroom refit. |

### 3. Pick the document and ask only what is missing

The six documents, their blocks, fields and signers are in `references/documents.md`. One question
per message; reuse every fact already given; never invent a price, a date, a tax number or a
policy number. Offer rather than instruct: "Do you want the insurance details printed?" and accept
the answer.

Decide the withdrawal pages from the facts in Preconditions 2 with `references/eu-baseline.md`
and the country layer. When they apply, the text comes from `references/withdrawal-form.md`,
word for word, in the language of the contract.

The contractor states prices and tax rates; never calculate tax, a share or a total they did not
give. When a national rule ties a tax rate to conditions, offer the document that records them and
leave the judgement to the contractor.

### 4. Write it in the right languages

The country's language is the master text. When the client reads another language, add it as a
second column, clause for clause, and say in the document which text prevails. Statutory texts
(the withdrawal information and form) are taken from the official version in each language, not
translated by you; if no official version of a language is at hand, give the master text alone for
that part and say so.

### 5. Check the signature level before anything is sent

If the country layer says a document needs a qualified electronic signature, a handwritten
signature or a notary, say so plainly and do not send that document for e-signature. Deliver it as
a document to print and sign, and carry on with the others.

### 6. Hand the document to the Formify skills

This skill decides content. The rest belongs to the capability skills, in this order:

1. `formify-pdf-forms` builds the PDF with real form fields from the text and the field table in
   `references/documents.md`. Pass the field names, kinds and required flags exactly.
2. `formify-verify-identity` only when the user wants proof of who signed.
3. `formify-send-contract` sends it to the named signers in the order the document gives; the
   preview and the "send now?" question are its steps and are never skipped.
4. `formify-track-signatures` afterwards: who has signed, reminders, the signed copy.

Invitation e-mails from Formify exist in English, Swedish and Spanish. When the client reads
another language, say so once and let the user choose the invitation language; the document itself
can be in any language.

If a capability skill is not installed, name it, say it comes in the same package, and continue
with what is possible here.

### 7. With no tools at all

Deliver the full text of the document in both languages, the field table, the signers in order,
and the one step that remains. That is a finished deliverable; never end at "I cannot make a PDF
here".

### 8. Offer the next document, once

Quote → contract → variation orders → handover record → warranty note. One line, at the end.

## Failure modes

| What happens | What to do |
|---|---|
| The user wants a document before the country is known | Ask the country first; it changes periods, wording and required blocks. |
| The lookup finds only blogs, law-firm pages or forum posts | Do not use them as the source. Report the question as not found and fall back to the baseline for that point. |
| Two official sources disagree, or a change is scheduled | Give both with their dates of application and let the user choose which date their contract falls under. |
| Unclear whether the job is a substantial conversion (outside the withdrawal rules) | Say it is unclear in one sentence; attaching the withdrawal pages is the cautious choice; the contractor decides. |
| The client wants works to start at once | Add the express-request checkbox of document 2; never tick it for them. |
| The contractor asks which tax rate applies | State the conditions the country file lists, with the source; do not pick the rate. |
| A rule asks for handwriting (for example a waiver) | Say an electronic form cannot replace it and leave that item out of the e-signed document. |
| The user asks for a design, a site diary or a final certificate | Out of scope: these belong to the technical professions and often need a qualified signature. |
| No Formify tools are connected | Finish the document, hand it over under step 7, and say it is ready to upload to Formify. |

## References

- **`references/documents.md`**: the six documents, block by block, with field names, kinds and
  signing order. Open it as soon as the document is chosen.
- **`references/eu-baseline.md`**: the rules that hold in every EU country, each with its source
  and the date it was read. Open it for every run, after the country is known.
- **`references/withdrawal-form.md`**: the withdrawal information and the model form, word for
  word. Open it whenever the withdrawal pages are attached.
- **`references/country-lookup.md`**: the questions to answer for a country without a verified
  file, and the official source for each EU country. Open it only for the live lookup.
- **`references/countries/es.md`**: Spain, verified: withdrawal periods, the reduced tax rate and
  the client's declaration, the Catalan quote rules, handover and liability periods. Open it when
  the works are in Spain.
- **`references/controls.json`**: every legal row behind this skill, with the official address and
  a sentence to re-check it against. Open it when a rule is questioned or looks out of date.
