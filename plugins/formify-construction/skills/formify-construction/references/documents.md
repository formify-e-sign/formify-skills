# The six documents

One section per document: what it is for, its blocks in order, the fields, who signs and in which
order. Field names are short ASCII identifiers with no period, unique in the document. "Signer"
fields are left for the person signing; every other value is printed from what the contractor said.

A value is printed once, in its block. Clauses refer to the block ("the price in block C") and never
repeat a figure. No date field next to a signature: Formify stamps date and time on each signature.

The national layer (`countries/<cc>.md` or the lookup) can add a block, change a period or make an
optional block required. It never removes block A or the signatures.

## 1. Quote

**For:** the price and scope the client accepts or declines before any work starts.

| Block | Content |
|---|---|
| A. Contractor | name or company, tax number, full address of the business, e-mail, telephone |
| B. Client | name, address of the works, e-mail |
| C. Works | what will be done, operation by operation; what is excluded |
| D. Price | labour, materials and other costs as separate lines; tax rate and amount; total; payment schedule |
| E. Dates | date of the quote, how long it is valid, planned start, planned duration |
| F. Decision | two equal boxes: accept, decline |

| Field | Kind | Required | Filled by |
|---|---|---|---|
| `client_decision` | radio group: `accept`, `decline` | yes | client |
| `client_comment` | multi-line text | no | client |

**Signs:** contractor first (so the client receives a signed offer), then the client.

## 2. Works contract

**For:** the agreement itself. Built from an accepted quote when there is one.

| Block | Content |
|---|---|
| A. Parties | contractor and client as in the quote; whether the client is a private person |
| B. Works | address, scope by reference to the quote or listed in full, exclusions, who obtains permits |
| C. Price and payment | total, tax, instalments tied to stages, how payment is made |
| D. Time | start date, duration or end date, what moves the dates (weather, changes, late client decisions) |
| E. Changes | no extra work without a signed variation order (document 4) |
| F. Handover and defects | handover by signed record (document 5); how defects are reported and fixed |
| G. Insurance and safety | contractor's liability insurance: insurer and policy number if the contractor wants them printed |
| H. Withdrawal | only when the right applies: see document 3, attached as the last pages |
| I. Data protection | who the controller is, what the data are used for, contact for requests |

| Field | Kind | Required | Filled by |
|---|---|---|---|
| `start_during_withdrawal` | checkbox: "I ask for the works to start before the withdrawal period ends, and I know that I lose the right to withdraw once the works are fully performed and must pay for what has been done if I withdraw before that" | no | client |
| `client_private_person` | checkbox | no | client |
| `agree_durable_medium` | checkbox: "I agree to receive this contract and the information in it as an electronic document instead of on paper" | yes, when the withdrawal right applies | client |

`agree_durable_medium` exists because the information and the copy of the signed contract may be
given electronically only if the client agrees (`eu-baseline.md`, row 4).

The checkbox `start_during_withdrawal` is printed only when the withdrawal right applies and the
contractor wants to start inside the period. Its wording follows `withdrawal-form.md`, in the
contract's language. It is never ticked in advance.

**Signs:** client and contractor. Order: contractor first.

## 3. Withdrawal information and form

**For:** a contract concluded away from the contractor's business premises (typically at the
client's home) or at a distance, with a private person. Whether the right applies and how long the
period is: `eu-baseline.md`, then the national layer.

Two parts, both reproduced from `withdrawal-form.md` in the language of the contract, word for
word, with only the bracketed choices resolved:

1. **Information on the right of withdrawal** (the period, how to withdraw, what is refunded, the
   proportional payment when works started early at the client's request).
2. **The model withdrawal form**, addressed to the contractor (name, full address, e-mail printed
   in), which the client fills in only to withdraw.

No fields and no signature when it is attached to the contract: the client signs the contract, and
the form stays blank for later use. When the contractor wants proof that the client received it, add
one checkbox to the contract, `withdrawal_info_received`, required.

Never translate the model text yourself when an official language version exists: take it from the
official version for that language (`country-lookup.md` says where).

## 4. Variation order

**For:** any change to scope, price or time after the contract is signed.

| Block | Content |
|---|---|
| A. Reference | contract date and parties, variation number |
| B. Change | what is added, removed or changed, and why |
| C. Price effect | amount added or deducted, tax, new total |
| D. Time effect | days added or removed, new end date |

| Field | Kind | Required | Filled by |
|---|---|---|---|
| `client_decision` | radio group: `accept`, `decline` | yes | client |

**Signs:** contractor, then client. Work on the change starts after the client has signed.

## 5. Handover record

**For:** the moment the client takes over the works. It starts the warranty and defect periods.

| Block | Content |
|---|---|
| A. Parties and contract | as in the contract |
| B. Works handed over | the whole works or a completed stage; date of completion |
| C. Final price | total including variation orders |
| D. Acceptance | accepted without reservations, or accepted with the reservations listed |
| E. Reservations | each defect described objectively, with the date by which it will be fixed |
| F. Documents handed over | manuals, certificates, keys |

| Field | Kind | Required | Filled by |
|---|---|---|---|
| `acceptance` | radio group: `without_reservations`, `with_reservations` | yes | client |
| `reservations` | multi-line text | no | client |

**Signs:** client and contractor. A second, short record signed by the same people closes the
reservations once they are fixed.

## 6. Warranty note

**For:** telling the client in one page what is covered, for how long, counted from the handover
date, and how to report a defect. The periods come from the national layer; when none was found the
note states the periods the contractor chooses to give and nothing else.

No fields. **Signs:** contractor only.

## Chains

Quote, then works contract (with the withdrawal pages when they apply), variation orders during the
works, handover record, warranty note. Offer the next document once, at the end of the current one.
