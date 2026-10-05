# Guide 02: Buyer and seller identification (KYC) forms

Use: once per client and transaction, before the reservation or the arras. The agency is an obliged entity under anti money laundering rules and must identify both parties (Ley 10/2010 art. 2.1.l and art. 3; from 10 July 2027, Reglamento (UE) 2024/1624 art. 19.6.c and art. 22). Two templates with the same identity block: `02_kyc_comprador.html` and `02_kyc_vendedor.html`. One form per person (each co-owner, each buyer). Default profile: **official**.

## What sets these templates apart
1. Fields aligned with the European Regulation that will apply in 2027 (date and place of birth, all nationalities, tax number, beneficial owner at 25 %, PEP including family members and close associates), which most agency forms do not collect.
2. A form for the seller with the same rigour as the buyer's: in Europe both parties are clients of the agency.
3. Signing with capture of the identity document performs the verification in the same act and leaves a copy on electronic medium, as the law requires.
4. Data protection information with the correct legal basis (legal obligation) and the ten year retention period.

## Template structure
Boxes A (identity), B (activity and transaction, or property and transaction for the seller), C (PEP), then representative and legal entity (optional), declarations and the client's signature; and on a separate page box D, "Comprobación y valoración por la agencia" (verification and assessment by the agency), which the agency fills in by hand after signing (checkboxes and blanks, no PDF fields). There is no internal use block: the risk assessment and the sanctions check live in the agency's file, never in the form the client signs (David, 2026-09-08). Each piece of data once only, in its box. No "Lo esencial" (key points) box.

**Box A is filled in by scanning the document.** The template carries the fixed fields (they are not `{{...}}`): on the right a 180×120 pt field `documento_scan|tink-scan-id[1]` (required) which at signing becomes a scan button and afterwards the image of the front of the document, and below the image three short items (NIF/NIE, phone, email) with the label above and the value or a 180 pt field below; on the left ten 135 pt fields `tink-scanned-id-mrz-*[1]` (first name, surnames, date and place of birth, nationality, number, issuing country, issue date, expiry, personal number) which Formify fills in on its own when the scan finishes. These data are never asked for in the chat nor printed: the client scans and the data arrive verified. The scan is mandatory: only the scan field carries the required mark (Formify reads it from the PDF and shows it in red), so signing without scanning is impossible; the ten data fields are not required, because the scan fills them in and not the client (David, 2026-09-08).

Below the image of the front there is an upload button `documento_reverso_subir|tink-upload-attachment[1]` (75×22 pt) with the instruction to photograph the back, and a read only field `documento_reverso_nombre|tink-uploaded-attachmentname[1]` where Formify writes the file name; the component accepts photographs. The rest of box A (address, tax residence, NIF/NIE, phone and email in full rows) and box B: ask "Do you have the client's details, or would you prefer that they fill them in when signing?". If the client fills them in, those values are passed as `{"field": "<nombre>", "width": <pt>}` (180 for nif, telefono and email, which go below the image; 300 for domicilio, residencia_fiscal and those in box B). A field wider than its cell covers the neighbouring cell: respect these widths; 

## Minimum questions (one per message; much of the data will come from the reservation or the mandate)
Buyer:
1. Name (for the invitation), email, and if available: NIF or NIE or foreign tax number, address, tax residence, phone. Nothing else about identity: the scan provides it.
2. Profession, purpose of the purchase (main residence, second home, investment, letting), origin of funds (savings, sale of another property, inheritance, loan, gift, company), planned bank financing (bank and approximate amount).
3. Acting on their own behalf? If on behalf of another: optional `representante` (and the represented person is the one in 1). If a company: optional `persona_juridica` with directors and beneficial owners.
4. PEP: yes or no; if yes, position, country and dates.

Seller: same as 1, 3, 4, plus marital status and matrimonial property regime, spouse where applicable, Land Registry details of the property, title of acquisition with date and price, ownership percentage, date of the nota simple, account receiving the price (must be in the seller's name; if it is not, warn in the chat: it is a risk signal).


## Fields
| Field | Required | Note |
|---|---|---|
| agencia_*, agente_nombre, agencia_email_datos | yes | from memory |
| referencia, lugar, fecha_larga, inmueble_corto | yes | reference "KYC-C-..." or "KYC-V-..." |
| nombre_completo, fecha_nacimiento, lugar_nacimiento, nacionalidades, documento_tipo, documento_numero, documento_pais, documento_caducidad, nif, domicilio, residencia_fiscal, telefono, email | yes | date in words or in the format 5-9-2026; if there is no NIF or NIE, "pendiente de obtención" (pending) and warn that it will be needed for the deed |
| profesion | yes | |
| finalidad(_tr), origen_fondos(_tr), financiacion(_tr), nombre_propio(_tr) | yes (buyer) | "Vivienda habitual" / "Main residence"; "Ahorros y venta de vivienda en Utrecht" / "Savings and sale of a home in Utrecht"; "Sí, Banco X, aprox. 250.000 €" / "Yes, Bank X, approx. €250,000"; "Sí" / "Yes" |
| pep_no_marca, pep_si_marca, pep_detalle(_tr) | yes | one of the two marks is " checked" (with a leading space) and the other "" ; detail "" if none |
| rep_* | if representative | rep_poder: "Escritura de poder de fecha X ante el notario Y, n.º de protocolo Z / Power of attorney dated X before notary Y, protocol no. Z" |
| pj_* | if legal entity | pj_titulares_reales with one line per person; pj_fiduciarios "Ninguno" / "None"; pj_documentos "Escritura de constitución y certificado del Registro Mercantil de fecha X" / "Deed of incorporation and Commercial Register certificate dated X" |
| estado_civil(_tr), conyuge, inmueble_registral, titulo_adquisicion(_tr), porcentaje_titularidad, fecha_nota_simple, iban_destino | yes (seller) | conyuge "No procede / Not applicable" if single or separation of property with no family home |

## Rules for this document
- Never save any data from this form in the skill's memory. It is client information; it lives in Formify and in the agency's file.
- Do not ask the client to paste the account number or the document into the chat if it can be avoided; the document is captured at signing. The seller's destination IBAN is written in the form.
- If the client declares being a PEP, the agency documents the enhanced measures in its file; the form does not change and the chat does not explain the law.
- If the origin of funds is cash, crypto assets or an unidentified third party, warn in the chat that it is a risk indicator and that the agency must request supporting documents before continuing.
- The citation of Ley 10/2010 in the declarations block is one of the permitted exceptions: do not remove it.
- Date note: from 10 July 2027 the European retention period becomes five years and verification may take place after acceptance of the offer. Until then the Spanish rule applies (identify before any transaction, retain for ten years). The law checker has a control with that date.

## Signers and Formify
- Signer: the client, role "Comprador/a" or "Vendedor/a" (and "Representante" if any). `id_scan: false` (no scan box next to the signature: the document is already scanned inside the form, box A). Signature type ALWAYS `face_liveness` (video selfie) for the client, preselected without asking, regardless of `default_signature_type` in memory. Only if `get_account_capabilities` returns `signatureFaceLiveness: false`, use `digital_ink` and tell the user in one sentence.
- The agent does not sign. No signing order.
- Draft title: "Identificación comprador {{nombre_completo}}" or "Identificación vendedor ...".
- Invitation message: "Formulario de identificación que la ley obliga a la agencia a recoger antes de la operación de {{inmueble_corto}}. Tenga a mano su documento de identidad: se fotografía al firmar."
- Archive: the signed document is kept in Formify. Remind the user not to delete it before ten years have passed.
- Formify template and public link (`references/templates-links.md`): this is the one document type that qualifies, when the client fills in box A and B alone (the "fill in when signing" answer). After the first identification form of a session, ask once whether to save it as a Formify template (one per form: comprador, vendedor); on yes, `create_template` from the draft's file with the client's signature slot and no names, and write `template=<id>` on the `kyc` line of the memory file. From then on a new client starts with `create_draft(templateId=...)`, then `update_draft` with the client's name and contact, then the preview. Offer a public link only after the template exists and only if the agency wants one address for every new client; say it is billed. Never a template when the agency pre-fills the client's data: that draft is made from a fresh file.

## Frequent errors these templates avoid
- Photocopying the DNI and nothing more: without purpose, origin of funds or PEP there is no due diligence.
- Identifying only the buyer.
- Destination account in a third party's name without explanation.
- Beneficial owner not identified in purchases through a company.
- Forms without data protection information or with the wrong legal basis (consent instead of legal obligation).

## Box D: verification and assessment by the agency
- It is the agency's part: checkboxes to tick and blanks to write in, after printing or in the PDF with a reader that annotates. No PDF fields, no question in the chat, nothing the client sees filled in. Rows: status (data collected, identity verified, due diligence assessed), identity verification (in person with the original document, or another procedure the agency describes in its own words), date, document checked and validity, checked by, representation, beneficial owner, purpose and nature, PEP, risk factors, risk classification, origin of funds, special examination, decision, follow up.
- The form does not say how identity is verified nor which remote procedure is valid: the agency decides that. The scan and the photograph in box A are the evidence the client provides; the verification is the agency's. Never explain this in the chat unless the user asks, and then in one sentence.
- The PEP row contains one sentence: OpenSanctions is a service that can be used to consult registers of persons with public responsibility. Only that, no link and no instructions; the agency decides whether to use it or another service. There is no setting or question about it.
- If the user asks what to do with box D: the agency fills it in once it has seen the client and made its decision; the client's electronic signature covers boxes A to C and the declarations, and box D stays in the file.
