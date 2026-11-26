# The three documents

One section per document: what it is for, its blocks in order, the fields, who signs and in which
order. Field names are short ASCII identifiers with no period, unique in the document. "Signer"
fields are left for the person signing; every other value is printed from what the host said.

A value is printed once, in its block. No date field next to a signature: Formify stamps date and
time on each signature.

The national layer (`countries/<cc>.md` or the lookup) fixes the data fields, the signers and the
retention. It never removes block A or the signature.

## 1. Guest registration form

**For:** the record each guest completes and signs on arrival, one per guest who must sign. Who must
sign, which fields, how long it is kept and whether an electronic form is accepted are national:
`eu-baseline.md`, then the country layer.

| Block | Content |
|---|---|
| A. Host and property | name or company, tax number if the host gives it, address of the property, contact e-mail or telephone. Registration code of the property only if the host states one; never invent it |
| B. Stay | arrival date and time, departure date and time, number of guests, kinship of any minor to the adults when the country asks for it |
| C. Guest data | exactly the fields the country fixes. Spain: `countries/es.md`. Country not verified: only the fields the host says their authority asked for, and a line saying the list was not checked |
| D. Identity document | document type and number, read from the document by the host or by `formify-verify-identity`. No image kept by default |
| E. Data notice | controller, purpose, legal basis as the country file states it, retention period from the country file, contact for requests. Host's own statement; whether more is required was not checked |
| F. Signature | the guest signs; an adult signs the data of a young child where the country file says so |

| Field | Kind | Required | Filled by |
|---|---|---|---|
| `guest_name` | text | yes | guest, or read from the ID document |
| `guest_doc_type` | text | per country | guest |
| `guest_doc_number` | text | per country | guest |
| `guest_nationality` | text | per country | guest |
| `guest_birth_date` | date | per country | guest |
| `guest_residence` | multi-line text | per country | guest |
| `guest_contact` | text | per country | guest |
| `data_notice_read` | checkbox | yes | guest |
| `guest_signature` | signature | yes | guest |

Add or drop the `guest_*` fields to match the country list exactly; the table is the usual set, not a
statutory one. For a group, the document is repeated per signing guest, with the same stay block.
With a public link, each guest opens the same link and fills in their own copy (`formify-share-link`).

**Spain variant for tourist homes.** In Andalucia and the Canary Islands a second, contract-like
document is signed for tourist or vacation homes. Its content and conditions are in `countries/es.md`
section 6; it is an addition to this document, not a separate EU document.

**Signs:** the guest; the host's side is recorded by the data the host prints, not by a signature,
unless the host asks to countersign.

## 2. House rules acknowledgement

**For:** the guest's written confirmation that they received the house rules. No statutory text on its
form is carried by this skill. The rules are the host's own words.

| Block | Content |
|---|---|
| A. Host and property | as in document 1 |
| B. Rules | the host's rules, numbered, as given; the skill adds none |
| C. Acknowledgement | one box: the guest has read and accepts the rules |

| Field | Kind | Required | Filled by |
|---|---|---|---|
| `rules_accepted` | checkbox: "I have read the house rules and accept them" | yes | guest |
| `guest_name` | text | yes | guest |
| `guest_signature` | signature | yes | guest |

Do not state that a rule is enforceable or that a deposit or charge may be kept: that was not checked.
Reproduce the host's wording; if a rule looks like a legal statement, ask the host where it comes from.

**Signs:** the guest. One acknowledgement per adult guest, or one for the lead guest if the host says
so; the choice is the host's.

## 3. Property-manager mandate

**For:** an owner authorising a manager, agency or co-host to register guests and run check-in. It is
a private agreement; no national rule on its form is carried by this skill.

| Block | Content |
|---|---|
| A. Owner | name or company, tax number, address, contact |
| B. Manager | name or company, tax number, address, contact |
| C. Property | address, and the registration code only if the owner states one |
| D. Scope | what the manager may do, as the owner chooses: collect guest data and signatures, check identity documents, hand over keys, apply the house rules |
| E. Filing | whether the manager may file the guest data with the authority for the owner. Spain: filing through an authorised third party is allowed when the obligated party authorises it (`countries/es.md`, section 4). Other countries: not checked |
| F. Data | who decides the purposes of the guest data, how long the manager keeps copies, return or deletion at the end. Owner's statement; processor terms under the GDPR were not checked |
| G. Term | start date, end date or notice period, how either side ends it |

| Field | Kind | Required | Filled by |
|---|---|---|---|
| `mandate_scope_filing` | checkbox: "The manager may file guest data with the authority on my behalf" | no | owner |
| `owner_signature` | signature | yes | owner |
| `manager_signature` | signature | yes | manager |

Never print a fee, a share or a liability allocation the parties did not give. Whether the mandate moves
any legal duty away from the owner was not checked; say so in one sentence.

**Signs:** owner first, then manager.

## Chains

Registration form, house rules, mandate. For a new property the order is usually the mandate first
(once), then the house rules and the registration form for every stay. Offer the next document once, at
the end of the current one.
