---
name: formify-guest-register
description: 'Guest registration form, house rules acknowledgement and manager mandate for hosts, hotels and campsites, ready to e-sign. Use when guests must register at check-in or an owner hands check-in to a manager. Triggers on "guest registration", "parte de entrada", "gästregistrering", "Meldeschein". Not for tenancy agreements: see formify-send-contract.'
license: MIT
metadata:
  version: "1.0.0"
  countries: eu
  internal: true
---

# Guest registration and check-in documents for hosts

Version 1.0.0. If asked which version you are, quote this line.

## Purpose

Produce the papers a host, small hotel, hostel, campsite or property manager signs at check-in,
correct for the EU country of the property: the guest registration form (one per guest who must
sign), the house rules acknowledgement, and the mandate by which an owner lets a manager register
guests and run check-in. Each comes out in the language of that country, with the guest's language
beside it when they differ, ready for e-signature through Formify.

The skill carries what a general model does not: who must sign, which data fields a country fixes,
how long the record is kept, which part is a separate filing this skill does not perform, and what
the EU text says and does not say about electronic signing.

## When this applies

- A host or manager wants guests to register and sign at or before check-in.
- Guests should fill the registration themselves, for example from a QR code at the door.
- A guest must acknowledge house rules in writing.
- An owner wants to authorise a manager, agency or co-host to register guests and handle check-in.

## When it does not

- **Filing the guest data with the police or a statistics platform** (SES.Hospedajes in Spain,
  eVisitor, Alloggiati Web and similar). That is a separate act with its own deadline. This skill
  prepares the signed record and never files anything.
- **Tourist tax returns and the short-term-rental registration number procedure.**
- **Tenancy agreements for residential letting, and booking contracts.**
- **The user already has the finished document and only wants it signed** → `formify-send-contract`.
- **Adding fields to the user's own PDF** → `formify-pdf-forms`.
- **Checking who a signer is, on its own** → `formify-verify-identity`.

## Preconditions

Nothing is required: no account, no tools, no files. Three facts decide the route, each asked only
if the conversation has not already given it:

1. **The country** of the property, and the region where the country file says it matters. Settled
   before any document is written.
2. **Who the host is**: a professional operator (hotel, hostel, campsite, registered tourist
   accommodation), a private person letting a home, or a manager acting for an owner. Some national
   duties differ between professional and non-professional hosts.
3. **What this environment can do**: search the web, build a PDF, reach Formify. Find out; do not
   assume.

## Procedure

### 1. Say what this can do, then offer a starting point

In the user's language, two or three sentences, then concrete openings:

> I can prepare the papers for check-in: a guest registration form that each guest signs, a house
> rules acknowledgement, and a mandate that lets a manager register guests for an owner. I follow
> the rules of the country the property is in and get them ready to sign.
>
> Shall we start with the registration form, the house rules, or the manager mandate?

For the registration form, mention that one reusable signing link can go on a QR code at the door,
so each arriving guest fills in and signs on their own phone. On a first contact show this even
when the user already named a document, then continue with it.

### 2. Settle the country

Ask: "In which country is the property?" If the conversation already names it, confirm it in one
line. Then:

| Situation | Do |
|---|---|
| `references/countries/` holds a file for the country (`es.md` is Spain) | Read it. It is verified; apply it as written. |
| No country file, and you can search the web | Follow `references/country-lookup.md`: answer its questions from the official sources it lists, and keep the link and today's date for each answer. |
| No country file and no web access | Apply `references/eu-baseline.md` only. |
| Outside the EU | Say this skill covers EU law, offer the documents without the statutory parts, and continue if the user wants that. |

Never pick a country because a file exists for it. When the user cannot be asked, write the EU
baseline version, leave the national parts marked as open, and say which country you need to know.

Tell the user in one or two plain sentences what you are relying on, once, before the first document:

- verified file: nothing needs saying beyond the rule that changes their document;
- live lookup: "I looked up the rules for <country> just now; these come from <source, with link>,
  read on <the date, written out>, and Formify has not reviewed them";
- baseline only: "I am applying the rules common to all EU countries; I could not check
  <country>'s own rules here."

A rule found by lookup is used like any other but keeps its link and the date you read it, written
out as a date and never only as "today", in your summary. Never present a
looked-up rule as verified, and never fill a gap from memory: a question the sources did not answer
is reported as not found. The EU text fixes no list of data fields; where the country's list is not
found, ask the host which fields their authority told them to collect and print only those.

The rules in brief, for when a reference file cannot be opened. The files carry the sources, the
wording and the exceptions; open them whenever you can, and say so when you could not.

| Layer | Rule |
|---|---|
| EU | Foreign guests, including nationals of other EU countries, personally complete and sign the registration form and show a valid identity document. |
| EU | Accompanying spouses, accompanying minors and members of travel groups are exempt from completing and signing. |
| EU | The EU text is silent on electronic form, electronic signature, copies of the document, retention and what is sent to the police. Those are national. |
| EU | Collect the data the form needs, not a picture of the document, unless national law asks for the copy. |
| Spain | Every guest over 14 signs. The data of a child under 14 are given by the accompanying adult. |
| Spain | The register is kept 3 years from the end of the stay. |
| Spain | Communication to the authorities within 24 hours is a separate act; this skill does not file it. |
| Spain | The decree does not say an electronic signature is accepted on the form; never claim it does. |
| Spain | Holiday lets in Andalusia and the Canary Islands also have a signed admission document. |

### 3. Pick the document and ask only what is missing

The three documents, their blocks, fields and signers are in `references/documents.md`. One question
per message; reuse every fact already given; never invent a name, an address, a registration code, a
price or a date. Offer rather than instruct, and accept the answer.

House rules and the manager mandate are private agreements: their content is the host's, and this
skill carries no national rule on their form. Say so in one sentence and structure what the host
gives you rather than adding clauses of your own.

### 4. Write it in the right languages

The country's language is the master text. When guests read another language, add it as a second
column, clause for clause, and say in the document which text prevails. A statutory field list is
printed in the language of the law it comes from; do not re-translate its wording, label it beside
the guest's language instead.

### 5. Check the signature level before anything is sent

An electronic signature cannot be refused as evidence only because it is electronic, and the Schengen
text is silent on paper or electronic form, so whether a country accepts an electronic register is a
national question: read it in the country file or lookup. If the country says paper or handwriting is
required for a document, say so plainly and deliver that document to print and sign; carry on with
the others. Never claim that an electronic signature is accepted on a registration form unless a
source you read says so.

### 6. Hand the document to the Formify skills

This skill decides content. The rest belongs to the capability skills, in this order:

1. `formify-pdf-forms` builds the PDF with real form fields from the text and the field table in
   `references/documents.md`. Pass names, kinds and required flags exactly.
2. `formify-verify-identity` when the guest should not type the identity data: it can read the ID
   document. Default to capturing the data without keeping the picture, because the signed file would
   otherwise hold a copy of the ID, and the data fields are what the registration needs
   (`references/eu-baseline.md`, section 2). Keep the picture only when the country file says it is
   required.
3. `formify-send-contract` for named signers (the mandate, a guest known in advance). For the
   registration form on a QR code or a booking confirmation, `formify-share-link` publishes one
   reusable link anyone can sign; it owns the link and the cost question, so do not answer cost here.
4. `formify-track-signatures` afterwards: who has signed, reminders, the signed copy.

Invitation e-mails from Formify exist in English, Swedish and Spanish. When a guest reads another
language, say so once; the document itself can be in any language.

The preview and the "send now?" question belong to the capability skills and are never skipped. If a
capability skill is not installed, name it, say it comes in the same package, and continue with what
is possible here.

### 7. With no tools at all

Deliver the full text in both languages, the field table, the signers in order, and the one step that
remains. That is a finished deliverable; never end at "I cannot make a PDF here".

### 8. Offer the next document, once

Registration form, then house rules, then the manager mandate. One line, at the end.

## Failure modes

| What happens | What to do |
|---|---|
| The user wants a document before the country is known | Ask the country first; it changes the fields, the signers and the retention. |
| The lookup finds only blogs, vendor pages or forum posts | Do not use them as the source. Report the question as not found and fall back to the baseline for that point. |
| The user believes signing the form also reports the guest to the police | Say plainly it does not: the filing is a separate act this skill does not perform. |
| A guest is a minor or part of a travel group | The EU text exempts accompanying spouses, minors and travel-group members from completing and signing; whether their data is still recorded is national. Read the country file. |
| The host asks to store a photo or copy of the ID | Explain the data-minimisation default and that the EU text asks only for the document to be produced; keep the picture only if the country file requires it. |
| The host quotes a rule from a blog or a vendor | Treat it as unverified; look it up on the official portal or report it as not found. |
| A region has its own check-in document and no file covers it | Say regional rules were not checked; ask the host whether their region requires one. |
| The owner is not the operator who files | Use the mandate, and say that whether it moves any duty away from the owner was not checked. |
| No Formify tools are connected | Finish the document, hand it over under step 7, and say it is ready to upload to Formify. |

## References

- **`references/documents.md`**: the three documents, block by block, with field names, kinds and
  signing order, and the Spain regional variant. Open it as soon as the document is chosen.
- **`references/eu-baseline.md`**: the rules that hold in every EU country, each with its source and
  the date it was read. Open it for every run, after the country is known.
- **`references/country-lookup.md`**: the questions to answer for a country without a verified file,
  and the official source for each EU country. Open it only for the live lookup.
- **`references/countries/es.md`**: Spain, verified: who signs, the closed field list of Annex I,
  retention, the separate filing, the Andalusian and Canarian documents, and what is not checked.
  Open it when the property is in Spain.
- **`references/controls.json`**: every legal row behind this skill, with the official address and a
  sentence to re-check it against. Open it when a rule is questioned or looks out of date.
