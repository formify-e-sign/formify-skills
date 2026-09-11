# The six Spanish documents

One file per document would scatter knowledge that is mostly shared. Read the section for the
document in hand; the four rules at the end apply to all of them.

Every document is laid out the same way: **labelled data boxes first** (A. Partes, B. Operación
and so on), **clauses second**, and the clauses refer to the boxes and to roles — *la parte
compradora*, *el inmueble*, *el cuadro B* — never repeating a value. A value appears exactly
once, in its box. There is no summary box.

Chains: **reserva → arras**, **encargo → llaves**, **KYC before reserva or arras**.

---

## 1. Nota de encargo y contrato de mediación

The mandate. It is what entitles the agency to advertise, show and receive money, and it is
what fixes the fee. Default profile: **oficial** in ES-IB, ES-CT, ES-VC; **profesional**
elsewhere.

**Boxes.** A client and agency side by side · B property · C mandate and fees · D insurance and
guarantee (optional) · E stipulations.

Box A carries the register line built as `references/es-regions.md` describes. The statutory
minimum content sits in A to D and the freely agreed terms in E, visibly separate — Baleares
requires that separation and it is good practice everywhere.

**The two things no market template has.** First, the **right of withdrawal** block with the
statutory text and the withdrawal form, reproduced verbatim from `references/es-withdrawal.md`,
plus the express request to start the service. Without it a private owner who signs remotely or
at home can withdraw up to twelve months later and the agency loses the fee even after finding
a buyer. Second, the consequence of a direct sale under an exclusive mandate written as
**proportionate compensation**, never as a penalty, and never using the word *penalización*.

**What to ask.**

1. Region of the property.
2. Owners: name, ID document, address, email, phone. Anyone acting as representative, and on
   what authority. Is this a private individual selling their own home, or a business? That
   decides whether they are a consumer.
3. Is it the family home of a married owner whose spouse is not on the title? If so, offer the
   spouse as a signer — optional here, mandatory in the arras.
4. Property: address, cadastral reference, Registro and finca, declared charges, protected
   regime, relevant legal situation (proceedings, occupation, an existing tenancy).
5. Transaction (sale or letting), price or rent, exclusive or not, start and end dates —
   three to six months is normal, never propose more than twelve.
6. Fee: percentage or amount; the tax and the total including it; when it is paid — usually at
   the deed, sometimes half at the arras.
7. The cap on deposits the agency may receive, as a percentage. Ten per cent is usual.
8. Consequence of a direct sale under exclusivity. Default: **half** the fee. If the user wants
   the whole fee, say in the chat that courts moderate clauses out of proportion to the work
   done and that half has held up best. They decide.
9. How often the client is reported to; tacit renewal (default no, with consumers).
10. *"Do you want the indemnity insurance and the guarantee in the document?"* — one question,
    every region, no explanation of who requires it. In Andalucía the question admits either a
    policy or a bank guarantee.
11. Is it signed remotely or at the client's home? An unsolicited home visit makes the
    withdrawal period **30 days instead of 14**.

**Signers.** Each owner (*Propietario/a*), the representative if any (*Representante*), the
non-owning spouse if wanted (*Cónyuge*), and the agent (*Agente inmobiliario*). ID scan for
owners and representative; the agent signs with a drawn signature. No signing order, unless the
user wants owners first.

**Its own rules.** Do not change a word of the withdrawal block or the form except its fields —
it is statutory text, the exception to the no-law rule. No *penalización*, no waiver of
withdrawal, no jurisdiction clause taking a consumer away from the courts of the property.

---

## 2. KYC — identification of buyer and seller

Once per person per transaction, before the reserva or the arras. The agency is a regulated
entity and must identify **both** sides. Two forms with the same identity box, one per person —
each co-owner, each buyer. Default profile: **oficial**.

**Boxes.** A identity · B activity and transaction (for a seller: ownership and transaction) ·
C politically exposed person · then optional representative and legal-entity blocks ·
declarations · the client's signature. On a separate page, box D, *Comprobación y valoración por
la agencia*, which the agency completes **by hand after signing** — plain boxes and rules, not
PDF fields. The risk assessment and sanctions check live in the agency's file, never in the form
the client signs.

### Box A is scanned, not typed

This is the part that must be built exactly.

| Element | Field name | Size | Notes |
|---|---|---|---|
| Scan control, right-hand side | `documento_scan\|tink-scan-id[1]` | 180 × 120 pt | **The only required field in the form.** Becomes the scan button, then the image of the document front. |
| Ten MRZ values, left-hand side | `tink-scanned-id-mrz-*[1]` | 135 pt each | Given name, surname, date and place of birth, nationality, document number, issuing country, issue date, expiry date, personal number. Formify fills them when the scan completes. |
| Three short values under the image | NIF/NIE, phone, email | 180 pt each | Label above, value or field below. |
| Reverse-side upload | `documento_reverso_subir\|tink-upload-attachment[1]` | 75 × 22 pt | With the instruction to photograph the back. Accepts photographs. |
| Name of the uploaded file | `documento_reverso_nombre\|tink-uploaded-attachmentname[1]` | — | Read-only. Formify writes the file name here. |

Only the scan control is marked required — Formify reads that from the PDF and shows it in red,
so the form cannot be signed without scanning. **The ten MRZ fields are not required**, because
the scan fills them and the client does not.

Never ask for these details in the chat and never print them. The client scans; the data arrive
verified.

**What to ask.** Buyer: name and email for the invitation, and if they have them, NIF/NIE or
foreign tax number, address, tax residence, phone — nothing more about identity. Then
occupation, purpose of the purchase, source of funds, expected bank financing. Whether they act
for themselves; if for someone else, the representative block; if a company, the legal-entity
block with directors and beneficial owners at 25 %. PEP: yes or no, and if yes the office,
country and dates.

Seller: the same, plus marital status and property regime, spouse where relevant, registry data
of the property, how and when they acquired it and at what price, share of ownership, date of
the nota simple, and the account the price is to be paid into.

**Signers.** The client only, as *Comprador/a* or *Vendedor/a* (plus *Representante*). **No ID
scan on the signature** — the document is already scanned inside the form, so a second scan at
signing is pure friction. The agent does not sign. No signing order.

**Its own rules.** Never keep anything from this form in anything that persists between
conversations. If the seller's destination account is not in the seller's name, say so in the
chat — it is a risk indicator. If the source of funds is cash, crypto or an unidentified third
party, say so too, and that the agency should obtain evidence before continuing. The retention
period is ten years; remind the user not to delete it earlier.

---

## 3. Oferta de compra y documento de reserva

A buyer makes an offer and leaves money to hold the property. One document, two phases: offer
and reservation (buyer and agency), then acceptance (seller). Default profile: **profesional**,
or **sencillo** when it is signed on a phone during the viewing.

**What it solves that market templates do not.** It says who holds the money — the agency, in a
client account, on behalf of both parties — and when it is returned (five working days), which
is the single biggest complaint about reservations. It separates the offer phase, where the
money comes back in full if there is no acceptance, from the arras phase, where it is forfeited
or doubled. And it sets the arras out as **penitenciales** with the express formula the case law
requires; without that formula the money is presumed a simple advance.

**What to ask.** Buyers (all of them sign) and seller — details, or fields they fill at signing.
Property, finca and Registro, cadastral reference, annexes, asking price. Date of the viewing
and of the nota simple. Offered price; furniture included, if any. **The reservation amount** —
€1,000 to €6,000 or around 1 % is the usual range, never suggest more than 5 % — and which
account it goes to. Deadline for the seller's answer, date and time (3 to 10 calendar days).
Deadline for the arras (7 to 15 days) and its percentage, and for the deed (30 to 90 days). Is
the purchase conditional on financing? If so, the deadline, the minimum amount and the bank. Is
the buyer paying the agency a fee — default no. Proposed notary, optionally. Region, for the
arras variant.

**Signers, with order.** Signing order is **on**: buyers and agent at position 1, sellers at
position 2. Formify notifies the seller once the buyer and agency have signed. No ID scan by
default — identification happens in the KYC — unless the user wants it in this act.

**Its own rules.** Never suggest a cash reservation; if asked, explain the legal ceiling and
propose a transfer. Never remove the *arras penitenciales* formula with its article. If the user
wants the reservation to be "non-refundable in any case", say that with a consumer buyer such a
clause is unfair and is not included. The seller's acceptance is their signature — there are no
boxes to tick. A counter-offer is a new document. If the transfer has not been made yet, say in
the chat that the reservation does not exist until the money arrives.

---

## 4. Contrato de arras penitenciales

The seller has accepted; the parties now fix the price, the deposit and the date of the deed.
The document with the most money at stake in the pack. Default profile: **profesional**.

**Why the deposit clause is written the way it is.** Four conditions must all be met for the
arras to be penitenciales: the document names them so, cites the article, gives **both** parties
the right to withdraw, and writes the consequence for each. A bare mention of the article is not
enough — the Supreme Court has read one as a simple advance. Regional variants: art. 1454 CC by
default, **art. 621-8 CCCat in Cataluña** (together with the financing rule of 621-49, which
applies by default there once the contract mentions financing), **ley 467 of the Fuero Nuevo in
Navarra**.

**What to ask.** Region. All sellers, with document and address, marital status and property
regime if married; whether the property is a married seller's family home, and if so the spouse
as a signer, or the declaration that it is not. Tax residence in Spain. All buyers, with their
NIE — if a foreign buyer does not have one yet, say in the chat that they will need it for the
deed. Anyone acting under a power of attorney. The property in full: address, floor area,
Registro, finca, tomo, libro, folio, cadastral reference, annexes, how it was acquired, date of
the nota simple, charges per the nota simple. Price, the deposit (5 to 10 %) and the balance.
Who receives the deposit — the seller directly by default, or the agency as escrow holder. Any
seller mortgage to be cancelled at the deed out of the buyer's funds. Whether the buyer needs
financing: **exactly one** of the financing block or the no-financing block, never neither and
never both. Deadline for the deed (30 to 90 days; foreign buyers without a NIE need longer; in
Cataluña with a notarial deposit, six months maximum), the notary's town, days of notice, days
to return the doubled deposit (10 to 15). Documentation: energy certificate number and letter,
habitability certificate where the region uses one, building inspection if there is one,
furniture inventory if included. Costs: by default the buyer pays transfer tax and stamp duty,
the deed and the registration; the seller pays the municipal land value tax and the cancellation
of charges; the seller pays the current year's IBI unless the user wants it apportioned.

**Signers, with order.** Sellers and spouse at position 1, buyers at 2, the escrow-holding
agency at 3 if it is involved. ID scan for sellers, spouse and buyers; the agency signs with a
drawn signature.

**Its own rules.** Do not touch the deposit clause outside its fields. Do not add *"a cuenta del
precio"* to the deposit clause — the crediting against the price is already at the end of it.
Do not mix penalties or liquidated damages into arras: if the user wants confirmatorias or
penales, say that this is a penitenciales document and that the other kinds need their own
drafting. **Check the arithmetic yourself** — balance = price − deposit, and the percentage
agrees — and write it in the chat. A nota simple older than a month deserves a warning. When the
seller is not resident in Spain, the buyer's 3 % withholding obligation clause is never removed.

---

## 5. Acuerdo de colaboración entre agencias

One deal, two agencies: one holds the mandate, the other brought the buyer. Default profile:
**profesional**, or **sencillo** from a phone. For a framework covering a whole portfolio this
is the wrong document — say so and offer a per-deal agreement.

**Boxes.** A the two agencies side by side · B the transaction · then the conditions, which
speak only of *la agencia titular*, *la agencia colaboradora*, *el cliente presentado*, *los
inmuebles del cuadro B*. There is no client registration date — signing this contract **is** the
registration — and no viewing rule. The template is written from the mandate-holder's side; if
the user is the collaborator, their details go in the collaborator column.

**The rule that is not negotiable.** The template proposes **no split and no fee**. Both are
written exactly as the user states them, or left as fields for the other agency. If the user
asks what is usual, say in the chat that equal splits are seen and so are splits favouring the
agency that took the listing, and that it is their decision.

**What to ask.**

1. Which side are you on — the agency with the mandate, or the one with the client?
2. Do you have the other agency's details, or shall they fill them in when they sign? If not,
   only the signing agent's name and email are needed; the rest become fields. Then one
   question: *"Anything else to add, for example a register number?"* — naming the region's
   actual register, and only in regions that have one.
3. First time only, remembered: *"Do you want the agents' NIE or DNI in the contract?"* Say
   NIE/DNI, never "identity document". This is the only situation in which an agent's own
   document is asked for, and only because the user chose it.
4. Properties and transaction, free text, one or several addresses with prices if wanted.
   Several properties with the same client is **one** contract, never one per property.
5. The introduced client: given by the user, never a field. Name only — no document, no figures,
   no date, no channel.
6. **The fee agreed with the owner** (the mandate-holder's, percentage or amount, before tax).
   This is always asked: printed if known, left as a field for the mandate-holder if not. Never
   omitted.
7. **The split**: 50 %, 60/40, another figure, or a field. Written exactly as said, plus tax.
8. Payment deadline after the fee is collected (8 to 15 days). The other agent's language.

**Signers.** The mandate-holder's agent (*Agencia titular*) and the collaborator's (*Agencia
colaboradora*), drawn signature, no ID scan. If there are fields for the other agency, put them
first in the signing order so they fill in and sign before the user does.

**Its own rules.** No value from box A or B is repeated in the conditions; change the reference
to the box, never copy the value. Do not ask for the agents' ID documents unless question 3 was
answered yes. For a letting, *venta* becomes *alquiler* in box B and the conditions stand.

---

## 6. Documento de entrega de llaves

A receipt for the keys handed to the agency for viewings. Small, fast, and the one most often
done from a phone. Default profile: **sencillo**. With the agency's details already known it
must be finished in **five questions or fewer** — as must colaboración.

**Boxes.** A to E with bilingual labels, then the conditions in two columns.

**What to ask.** Owners — details or fields; several owners all sign. The property address;
registry data or cadastral reference only if the user has them to hand. Sale or letting, and the
date of the mandate: if there is no mandate yet, offer to produce the nota de encargo first. The
inventory: how many keys of each kind, remotes, anything else. A viewing log — default yes for a
letting, no for a sale. The client's language.

**Signers.** Each owner (*Propietario/a*) and the agent (*Agente inmobiliario*), drawn
signature, no ID scan, no signing order.

**Its own rules.** **Never write an alarm code, an entryphone code or a password**, even when
the user dictates one; remind them these are communicated separately. Three or more owners: all
sign. The document does not allow one owner to sign for another without a power of attorney —
ask for it and add the representation wording. For a letting with a tenant already in the
property, add *", y previo consentimiento de la persona ocupante"* to the access clause in both
columns, and ask first.

---

## Draft titles and invitation messages

Titles are short and identify the deal: *Nota de encargo {property}*, *Identificación comprador
{name}*, *Oferta y reserva {property}*, *Arras {property}*, *Colaboración {client}*, *Entrega de
llaves {property}*.

The invitation message is at most 500 characters, written in the recipient's language, and says
what to look at before signing — not what the document is in the abstract. *"Ha recibido una
oferta por {property}. Revise el documento y, si está conforme, firme para aceptarla antes del
{deadline}."* For the KYC form it must warn them to have their document to hand, because it is
photographed during signing.

Invitation emails themselves exist only in Spanish, English and Swedish. When the client speaks
another language, say so — and offer the in-document AI assistant instead, which speaks whatever
language the signer does.
