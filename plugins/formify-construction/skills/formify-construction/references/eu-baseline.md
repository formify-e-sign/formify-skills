# EU baseline: works for a private client

What holds in every EU country, read on the consolidated EU texts on 2026-11-26. Sources and the
sentences to re-check are in `controls.json`. "CRD" is Directive 2011/83/EU on consumer rights,
consolidated version of 27 September 2026.

A country can be stricter or use one of the options in section 3. The country layer wins over this
file wherever it says something different.

## 1. Is the contract covered

| # | Rule | Source |
|---|---|---|
| 1 | Renovation, repair and building an annex (a garage, a veranda) for a consumer are covered by the consumer-contract rules. | CRD art. 3(3)(f), recital 26 |
| 2 | Building a new house and "substantial conversion" of an existing building are not covered. A substantial conversion is one comparable to a new building, for example where only the façade is kept. National law alone governs those. | CRD art. 3(3)(f), recital 26 |
| 3 | A contract concluded with both parties present somewhere that is not the contractor's business premises (the client's home, the site) is an off-premises contract. So is one concluded right after the client was approached in person away from the premises. | CRD art. 2(8) |

A contract concluded entirely at a distance (for example signed through a link, with no meeting)
is a distance contract: the same withdrawal right applies, and from 19 June 2026 a contract
concluded through an online interface must offer an online withdrawal function (Directive (EU)
2023/2673). A contract agreed in person at the client's home and then signed electronically remains
an off-premises contract.

## 2. What the documents must do

| # | Rule | Effect on the document | Source |
|---|---|---|---|
| 4 | The pre-contract information is given on paper or, if the consumer agrees, on another durable medium, legibly and in plain language. The consumer receives a copy of the signed contract the same way. | Field `agree_durable_medium` in the contract; the signed PDF is the copy | CRD art. 7(1)-(2) |
| 5 | The information includes the total price or how it is calculated, the time for performance, and the conditions, period and procedure for withdrawal with the model form. | Blocks C, D and H of the contract; document 3 attached | CRD art. 6(1)(e), (g), (h) |
| 6 | The model instructions, correctly filled in, satisfy the withdrawal information duty. | Use `withdrawal-form.md` word for word | CRD art. 6(4), Annex I(A) |
| 7 | The consumer has 14 days to withdraw, without giving a reason. For services the period runs from the day the contract is concluded. | Period printed in document 3 | CRD art. 9(1), 9(2)(a) |
| 8 | If the withdrawal information was not given, the period ends 12 months after the original period would have ended. | Never leave document 3 out when the right applies | CRD art. 10(1) |
| 9 | Works may start inside the period only if the consumer asks for it expressly on a durable medium and acknowledges that the right is lost once the contract is fully performed. | Field `start_during_withdrawal`, never pre-ticked | CRD art. 7(3) |
| 10 | After such a request, a consumer who withdraws pays in proportion to what was done. Without the request, or without the information, the consumer pays nothing for work done inside the period. | Instruction 6 sentence in document 3 | CRD art. 14(3), 14(4)(a) |
| 11 | No withdrawal right where the consumer specifically asked for a visit for urgent repair or maintenance. Anything extra done on that visit keeps the right. | Urgent repair: no document 3; extras: document 3 | CRD art. 16(h) |
| 12 | No withdrawal right once a service is fully performed, if performance began with the consumer's prior express consent and acknowledgement. | Same field as row 9 | CRD art. 16(a) |
| 13 | Goods made to the consumer's specifications or clearly personalised have no withdrawal right. Whether a made-to-measure kitchen or window counts is decided nationally. | Do not decide it; ask the contractor | CRD art. 16(c) |

## 3. Options each country decides: ask or look up

| # | Option | Baseline when unknown | Source |
|---|---|---|---|
| 14 | 30 days instead of 14 for contracts made during an unsolicited visit to the home or a sales excursion | 14 days | CRD art. 9(1a) |
| 15 | A ban on taking payment during the withdrawal period for off-premises contracts | No ban assumed; say it was not checked | CRD art. 9(3) |
| 16 | A lighter information regime for repairs or maintenance the consumer asked for, performed and paid at once, up to EUR 200 | Full information | CRD art. 7(4) |
| 17 | Exempting off-premises contracts up to EUR 50 (or a lower national figure) | No exemption | CRD art. 3(4) |
| 18 | The language the contract information must be in | The country's official language | CRD art. 6(7) |

## 4. What EU law does not set

| # | Point | Source |
|---|---|---|
| 19 | Warranty and liability periods for the works themselves, acceptance rules and retention are national. | Directive (EU) 2019/771 arts. 3, 8 |
| 20 | Goods sold and installed by the contractor (a boiler, windows) carry the two-year conformity guarantee for goods; incorrect installation by the seller counts as a defect of the goods. | Directive (EU) 2019/771 arts. 8, 10(1) |
| 21 | A reduced tax rate for renovating or repairing housing is something a country may allow. The rate, its conditions and any client declaration are national. Never print a rate the contractor did not give. | Directive 2006/112/EC art. 98, Annex III(10) |
| 22 | Contractor licences, registers, compulsory insurance, permits, deposit limits and statutory building-contract terms are national. | not harmonised |

## 5. Signature

| # | Rule | Source |
|---|---|---|
| 23 | An electronic signature cannot be denied legal effect or admissibility as evidence only because it is electronic. | Regulation (EU) 910/2014 art. 25(1) |
| 24 | A qualified electronic signature has the legal effect of a handwritten one. | Regulation (EU) 910/2014 art. 25(2) |
| 25 | Whether a document needs handwriting, a qualified signature or a notary is national law. | Regulation (EU) 910/2014 art. 2(3) |

Formify signatures are covered by row 23. Where a country asks for the form in row 24 or for
handwriting, say so and do not send that document for e-signature.
