# Memory: the agency profile and the user's habits

The skill remembers the agency and the user's preferences in one plain text file, `formify-memory.md`, in the user's working folder (the folder where the documents are generated; if the platform has a project or workspace folder, that one). It works the same in every agent that can read and write files. If you cannot write files, show the text and ask the user to save it as `formify-memory.md` and to attach it next time.

## Rules
1. Read the file before asking anything. Never ask for something it already contains. The file grows as documents are made: there is no set-up, so a file with only the agency name and the user's e-mail is normal. Every line below is optional until a document needs it; write each answer the moment it is given.
2. Write to it only what the user confirmed, and only about the agency, the user and their preferences. Never write client data: no names of buyers or sellers, no property addresses, no ID numbers, no bank accounts, no offers. Client data lives in the documents and in Formify.
3. After each finished document, ask one question: "Do you want me to save these settings as your default for this document type?" If yes, write the document-type block. If the user says "this is how I want it" at any point, treat it as a yes for that setting.
4. Update in place; do not duplicate blocks. Keep the file short.
5. Never store anything about the skill itself except the flags below.
6. Own templates (`references/own-templates.md`): `own_template=yes` on the document type's line, and one line in `notices` per own template saying what was changed.

## Format
```markdown
# formify-memory (formify-es-real-estate)
updated: 2026-09-06

## organisation
name: Inmobiliaria Ejemplo, S.L.
tax_id: B00000000
address: Calle Ficticia 1, 07000 Palma
email: info@example.com
phone: +34 971 000 000
data_protection_email: datos@example.com
region: ES-IB
register: ROAI n.º 0000   (or empty; only if the user gave a number)
liability_insurance: Aseguradora Ejemplo, S.A. | tax_id: A00000000 | policy: RC-000000   (only if the user gave it while making a mandate note)
guarantee_provider: Caución Ejemplo, S.A. | tax_id: A11111111 | number: G-000000   (same)
deposit_account: agency | ES00 0000 0000 0000 0000 0000   (agency or other, with IBAN; only if the user gave it while making a reservation or arras)
logo: logo.png   (relative path; embedded as a data URI; "none" if there is none: the header shows the name)
formify_logo_in_invitations: yes   (capability companyLogo)
style_profile: official   (official | professional | light, default according to region)
usual_languages: en, sv, de

## user
name: María López García
email: maria@example.com
default_signature_type: digital_ink_id_scan
id_document: NIE X0000000Y   (only if the user chose agent_id_document=yes in colaboración; never asked for in the initial set-up)

## documents
encargo: profile=professional; insurance=yes; withdrawal=yes; exclusive=yes; term=6 months; fee=5 %; payment=at deed; direct_sale_consequence=half; report=15 days; extension=no; notice=15
reserva: profile=professional; account=agency; reservation=1 % of the price (min. 3,000 €); reply=7 days; arras=10 %; arras_days=10; deed_days=60; financing=ask
arras: profile=professional; escrow=yes; refund_days=10; notary_notice=7; ibi=seller current year; signing_order=sellers, buyers, agency
colaboracion: profile=light; payment_days=10; agent_id_document=no
llaves: profile=light; visit_log=rental only; own_template=yes
kyc: profile=official

## notices
welcome_shown: 2026-09-06
sample_pack_sent: 2026-09-06
own_template llaves: without the garage remote row; clause 5 added (alarm company)
```

## What each block feeds
- `organisation` and `user` fill the header, the agency column of box A in every document, box D of the mandate, the deposit IBAN and the data protection contact in every document. The user's own ID number is never asked for and is not printed: the agent acts for the agency, and when a signing method with an identity document is used, Formify captures the document in the signature itself. The one exception is the user's own choice `agent_id_document=yes` for colaboración (asked the first time that document is made); then `user.id_document` is stored and printed in box A of that document only.
- `documents` sets the defaults the wizard proposes; the user can always override for one document without changing the memory. `profile` (professional | official | light) is asked the first time a document type is made and remembered here; the same for `insurance` and `withdrawal` (encargo), and `account` (reserva, arras).
- `notices` prevents repeating the welcome text and the sample-pack offer, and lists what each own template changes.

## Several users in one agency
One file per user. If the agency shares a folder, name the file `formify-memory-<name>.md` and read the one that matches the user; the `organisation` block may be copied between them.
