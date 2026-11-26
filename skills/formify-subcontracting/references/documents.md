# The five documents

One section per document: what it is for, its blocks in order, the fields, who signs and in which
order. Field names are short ASCII identifiers with no period, unique in the document. "Signer"
fields are left for the person signing; every other value is printed from what the parties said.

A value is printed once, in its block. Clauses refer to the block ("the price in block C") and never
repeat a figure. No date field next to a signature: Formify stamps date and time on each signature.
Both parties are businesses: print each one's legal name, tax number, registration number where the
country asks for one, full address, e-mail, and the person who signs for it.

The national layer (`countries/<cc>.md` or the lookup) can add a block, change a period or make an
optional block required. It never removes block A or the signatures. Nothing the parties did not
state is filled in: no price, no period, no percentage.

## 1. Subcontract

**For:** the agreement between the main contractor and the subcontractor for a defined part of the
works on a private site.

| Block | Content |
|---|---|
| A. Parties | main contractor and subcontractor as above; whether the subcontractor is a company or a self-employed person |
| B. Scope | the site address; the main works in one line; the subcontracted part, operation by operation, by reference to the main works or a list; exclusions; who supplies materials and equipment |
| C. Price | the price as the parties state it, with the tax treatment they state; stages and amounts if they state any |
| D. Payment terms | invoicing, the payment period the parties state, how payment is made, any acceptance or verification period they state. See `eu-baseline.md` rows 3 and 4 for the single note when a period is long |
| E. Time | start, duration or end date, what moves the dates |
| F. Changes | no change to scope, price or time without a signed variation order (document 2) |
| G. Site rules and safety | the subcontractor follows the site safety and health plan and the directions of the safety coordinator (offered clause, `eu-baseline.md` row 13); site access and working hours the parties state |
| H. Insurance | liability insurance of each side: insurer and policy number only if the party gives them |
| I. Defects and retention | only if the parties state them: period, start, amount or percentage retained, release. Left out when they state nothing |
| J. Further subcontracting | whether the subcontractor may subcontract, as the parties state it, within the limits the country layer lists |
| K. Compliance documents | the certificates the subcontractor supplies before starting, by reference to document 5 when it is used |
| L. Data protection | who the controller is, what the data are used for, contact for requests |

| Field | Kind | Required | Filled by |
|---|---|---|---|
| `contractor_signatory` | text: name and role of the person signing for the contractor | yes | contractor |
| `subcontractor_signatory` | text: name and role of the person signing for the subcontractor | yes | subcontractor |

**Signs:** contractor first, then subcontractor.

## 2. Variation order

**For:** any change to the scope, price or time of the subcontract after it is signed.

| Block | Content |
|---|---|
| A. Reference | the subcontract (date, parties) and the variation number |
| B. Change | what is added, removed or changed, and why |
| C. Price effect | the amount added or deducted and the new total, as the parties state them |
| D. Time effect | days added or removed, new end date |

| Field | Kind | Required | Filled by |
|---|---|---|---|
| `subcontractor_decision` | radio group: `accept`, `decline` | yes | subcontractor |

**Signs:** contractor, then subcontractor. Work on the change starts after the subcontractor has signed.

## 3. Completion and acceptance record

**For:** the moment the contractor takes over the subcontracted part, or a completed stage of it.

| Block | Content |
|---|---|
| A. Parties and subcontract | as in the subcontract |
| B. Part handed over | the whole subcontracted part or a stage; date of completion |
| C. Final price | the total including variation orders, as the parties state it |
| D. Acceptance | accepted without reservations, or accepted with the reservations listed |
| E. Reservations | each defect described objectively, with the date by which it will be fixed |
| F. Documents handed over | manuals, certificates, keys, as listed by the parties |

| Field | Kind | Required | Filled by |
|---|---|---|---|
| `acceptance` | radio group: `without_reservations`, `with_reservations` | yes | contractor |
| `reservations` | multi-line text | no | contractor |

**Signs:** contractor and subcontractor. A second short record signed by the same people closes the
reservations once they are fixed. Statutory handover rules of the country are in the country layer;
without them, print only what the parties agreed and say that statutory periods were not checked.

## 4. Payment confirmation

**For:** a written record of money for a stage. Two forms, chosen by the user.

| Block | Content |
|---|---|
| A. Reference | the subcontract, the stage or invoice number |
| B. Stage | what the amount is for |
| C. Amount | the amount, as the parties state it, and the date of payment or the date it falls due |
| D. Statement | form 1, receipt: "the subcontractor confirms it received the amount in block C for the stage in block B". Form 2, certification: "the contractor certifies that the amount in block C is due for the stage in block B" |

| Field | Kind | Required | Filled by |
|---|---|---|---|
| `amount_agreed` | checkbox: "I confirm the amount in block C" | yes | the party who signs second |
| `payment_comment` | multi-line text | no | the party who signs second |

**Signs:** form 1, the subcontractor first and the contractor after as acknowledgement; form 2, the
contractor first and the subcontractor after as acknowledgement. This record is evidence of what
the parties said. It does not set a payment period and states no interest.

## 5. Compliance checklist

**For:** the certificates the country asks the contractor to collect before the subcontractor
starts. The list comes from the country layer; with no country file the checklist is built only
from what the user names and says the country's list was not checked.

| Block | Content |
|---|---|
| A. Parties and subcontract | as in the subcontract |
| B. Certificates | one line each: name, issuing body, who requests it, validity as the country file gives it |

| Field | Kind | Required | Filled by |
|---|---|---|---|
| `cert_1`, `cert_2`, ... | checkbox per line: "I have supplied this certificate to the contractor" | yes | subcontractor |
| `cert_1_ref`, `cert_2_ref`, ... | text: reference or issue date of that certificate | no | subcontractor |

**Signs:** subcontractor, then contractor (who confirms receipt). Signing records that a
certificate was supplied. It does not show that the certificate is genuine or in force; say so in
the document.

## Chains

Subcontract, compliance checklist, variation orders during the works, payment confirmations per
stage, completion record. Offer the next document once, at the end of the current one.
