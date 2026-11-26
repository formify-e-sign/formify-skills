# Spain (ES): renovation works for a private client

Verified pack. Every row was read on the official consolidated text on 2026-11-26; the links and
the sentences to re-check are in `../controls.json`. Language of the document: Spanish at least
(the pre-contract information must be "al menos en castellano"); offer the client's language as a
second column, and Catalan in Catalonia.

Ask for the region when the works are in Catalonia: it adds the quote rules in section 4.

## 1. Does the withdrawal right apply

| Situation | Result | Source |
|---|---|---|
| Contract signed at the client's home or anywhere that is not the contractor's premises, client is a consumer | Withdrawal right applies; attach document 3 | TRLGDCU art. 92.2 |
| New building, or "transformación sustancial" of an existing one | Outside these rules: no withdrawal pages | TRLGDCU art. 93.f |
| The client specifically asked for a visit for urgent repair or maintenance | No withdrawal for that repair; it does apply to anything extra done on the visit | TRLGDCU art. 103.h |
| Signed at the contractor's premises | No statutory withdrawal right | TRLGDCU art. 92 |

"Substantial" is not defined in the law. When it is unclear whether a job is a substantial
conversion, say so in one sentence and let the contractor decide whether to attach the pages;
attaching them is the cautious choice.

## 2. Periods and what goes in the documents

| Rule | Value | Source |
|---|---|---|
| Withdrawal period | 14 calendar days from the day the contract is concluded | TRLGDCU arts. 102.1, 104.a |
| Unsolicited visit to the home, or a sales excursion | 30 calendar days | TRLGDCU art. 102.1 |
| Information on withdrawal not given | The period ends 12 months after the original period would have ended | TRLGDCU art. 105.1 |
| Copy for the client | A copy of the signed contract, on paper or, if the client agrees, on another durable medium | TRLGDCU art. 99.2 |
| Works to start inside the period | The client asks for it expressly on a durable medium and declares they know the right is lost once the contract is fully performed | TRLGDCU art. 99.3 |
| Client withdraws after such a request | Pays the proportion already performed | TRLGDCU art. 108.4 |
| Client did not make the request, or was not informed | Pays nothing for what was done inside the period | TRLGDCU art. 108.5.a |
| Clause penalising withdrawal | Void | TRLGDCU art. 102.2 |

The model information text and the model form are in Anexo I, parts A and B, of the TRLGDCU. The
Spanish law prints its own version, which differs from the EU Spanish text in `../withdrawal-form.md`
in two places: the periods read "catorce/treinta días naturales", and the consumer is "consumidor y
usuario". Read Anexo I on the BOE page given in `../controls.json` and use that text for Spain; when
the page cannot be reached, use the Spanish section of `../withdrawal-form.md` with "días naturales"
after each period, and say which text was used.

**Scheduled change.** From 2027-01-25 (Real Decreto-ley 44/2026) note 3 of part A gains a sentence
for businesses that offer an online withdrawal function. A contract signed at the client's home is
not an online contract, so the text in `../withdrawal-form.md` stays correct for it. The decree was
still awaiting the vote of Congress on 2026-11-26.

## 3. Reduced VAT on renovation of a dwelling (10 %)

The quote and the contract print the rate the contractor states. When the contractor says the
reduced rate applies, offer the client declaration below; do not work out the rate yourself.

Conditions (Ley 37/1992 art. 91.Uno.2.10º):

| Condition | Until 2026-11-30 | From 2026-12-01 |
|---|---|---|
| Client | A private person using the dwelling for their own use, or a community of owners | Also a dwelling let as a habitual residence, whoever the landlord is |
| Age of the dwelling | Built or rehabilitated at least two years before the works start | Same |
| Materials supplied by the contractor | Not more than 40 % of the taxable amount | Same |
| Payment | No condition | Paid by card, bank transfer, nominative cheque or deposit into the contractor's bank account |

The second column comes from Real Decreto-ley 29/2026 art. 7, confirmed by Congress on 2026-11-12.

**Client declaration** (Reglamento del IVA art. 26): a written statement signed by the client and
addressed to the contractor, saying under their own responsibility that (1) they do not act as a
business or professional, (2) they use the dwelling for private use, (3) its construction or
rehabilitation ended at least two years before the works start. It is a permitted proof, not a
required form. It does not cover the materials limit or the payment method; print the payment
method in block C of the contract.

Fields: `not_business` checkbox, `private_use` checkbox, `dwelling_two_years` checkbox, all
required, filled by the client. Signs: the client only.

## 4. Catalonia: the quote

Applies to services provided in Catalonia to a consumer (Codi de consum, Llei 22/2010, arts.
251-1 to 251-5).

| Rule | Value | Source |
|---|---|---|
| A quote is handed over before the service when the client cannot work out the price themselves | Unless the client waives it in their own handwriting, with a signature | art. 251-3.2 |
| Content of the quote | Provider's name, tax number and full address of a physical establishment; the purpose and the operations; costs itemised, with parts and goods; validity period; planned start and duration; date and signature of a person responsible at the provider; date of acceptance or refusal with **two signature spaces of equal size**, one for each | art. 251-3.3 |
| Copies kept | At least six months from refusal or from the end of the service | art. 251-3.4 |
| Invoice | Not higher than the quote | art. 251-4.1 |
| New items during the works | A written extension or change that the client accepts, on record | art. 251-4.2 |
| Minimum guarantee of a service | Six months from the last act, when no specific rule applies | art. 251-5.2 |

Effect on the documents: document 1 takes exactly the content above and block F keeps the two equal
boxes; document 4 is the extension of art. 251-4.2. The handwritten waiver cannot be given through
an electronic form: when the client wants to waive the quote, say that the law asks for handwriting.

## 5. Handover and liability periods

For building works within the Ley de Ordenación de la Edificación (new buildings, and works that
alter the architectural configuration of an existing one):

| Rule | Value | Source |
|---|---|---|
| Handover record | Signed at least by the developer (the client) and the builder; states the parties, the date of the final certificate, the final cost, acceptance with or without reservations and the term to fix them, and any guarantees | LOE art. 6.2 |
| When | Within 30 days of completion unless agreed otherwise; acceptance is presumed after 30 days without written reservations | LOE art. 6.4 |
| Structural defects | 10 years | LOE art. 17.1.a |
| Habitability defects | 3 years | LOE art. 17.1.b |
| Finishing defects (builder) | 1 year | LOE art. 17.1.b |
| Start of the periods | The date the record is signed, or presumed acceptance | LOE art. 6.5 |

A kitchen or bathroom refit that changes neither façade, volume, structure nor use is not within
that wording. For such works print the periods the contractor gives in document 6 (in Catalonia not
less than the six months of section 4) and do not print the 1, 3 and 10 years as if they applied.

The final certificate of works is signed by the site director and the director of execution. It is
their document: this skill does not produce it.

## 6. Signature

None of the provisions above asks for a qualified electronic signature or a notary. The exception
is the handwritten waiver in section 4.

## 7. Not in this pack

- Regional consumer rules outside Catalonia: not checked.
- Which civil-law rule governs defects in minor works: not checked.
- Building permits and municipal notices.
