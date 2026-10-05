# Guide 03: Purchase offer and reservation document (v2: boxes A and B, terms that only refer to the boxes)

Use: every time a buyer wants to make an offer and leave a sum to "hold" the property. A single document with two phases: offer and reservation (buyer and agency) and acceptance (seller). Default profile: **professional**; **sencillo** if the user signs from a phone during the viewing.

## What this template solves that market models do not
- It says who holds the money (the agency, in a deposit account, on behalf of both parties) and when it is returned (five business days), which is the OCU's main complaint about reservations.
- It clearly distinguishes the offer phase (full refund if there is no acceptance) from the arras phase (forfeiture or double).
- It configures the arras as penitenciales with the express formula that case law requires; without that formula the money is presumed to be a simple advance payment.
- No cash (legal limit of €1,000 for payments to professionals and anti money laundering practice).
- Consumer's jurisdiction respected.

## Minimum questions (one per message; skip what is already known)
1. Buyer(s): "Do you have the buyer's details (name, ID document, address, email), or would you prefer that they fill them in when signing?" The same for the seller if not in memory or in a previous mandate. Several buyers: all sign.
2. Property: address, finca and Land Registry, cadastral reference, annexes (garage, storage room), public asking price. If the user has the nota simple, ask for the PDF for Anexo II.
3. Date of the viewing and date of the nota simple.
4. Offered price. Is furniture included? (optional row `muebles` and Anexo III).
5. Reservation amount (guidance: €1,000 to €6,000 or around 1 % of the price; never suggest figures above 5 %). Which account does the reservation go to: the agency's client account or another account? IBAN (from memory). Transfer receipt in PDF? Attached as Anexo I (see Annexes). If the transfer has not been made yet, warn in the chat that the reservation is not constituted until the money arrives.
6. Seller's response deadline: date and time (guidance: 3 to 10 calendar days).
7. Deadline for arras (guidance 7 to 15 days) and percentage (usually 10 %). Deadline for the deed (guidance 30 to 90 days).
8. Financing condition? If the buyer needs a mortgage, recommend block 7 bis and ask for the deadline and minimum amount. If paying cash, remove the block.
9. Does the buyer pay a fee to the agency? By default no. If yes, there is a separate purchase mandate and the sentence is added.
10. Proposed notary (optional).
11. Seller(s): name, ID document, address, email (for section D (acceptance) and the signature).
12. Client's language. Region of the property (for the variant of stipulation 7: CC, CCCat in Catalonia, FN in Navarre).

## Fields
| Field | Required | Note |
|---|---|---|
| referencia, lugar, fecha_larga, hora | yes | the time matters: it fixes the moment of the offer |
| comprador_nombres, comprador_docs, comprador_domicilio, comprador_email | yes | box A; several buyers separated by " y " (names) and "; " (documents); text or field if the user does not have them |
| vendedor_nombres, vendedor_docs, vendedor_domicilio, vendedor_email | yes | box A; text or field |
| agencia_email | yes | from memory |
| agente_*, agencia_* | yes | from memory; fecha_encargo = date of the nota de encargo with the seller |
| inmueble_direccion, inmueble_corto, finca, registro, refcat | yes | registro: "n.º 3 de Palma" / "no. 3 of Palma" |
| anejos_frase | no | ", con plaza de garaje n.º {{n}} y trastero n.º {{n}}" / ", together with parking space no. {{n}} and storage room no. {{n}}" |
| precio_publico_cifra(_tr), precio_cifra(_tr), precio_letras(_tr) | yes | Spanish: "250.000" and "doscientos cincuenta mil"; English: "250,000" and "two hundred and fifty thousand" |
| optional `muebles` | no | row in box B: furniture and fittings of Anexo III (then add the annex) |
| reserva_cifra(_tr), reserva_letras(_tr) | yes | |
| cuenta_destino(_tr) | yes | question when creating the reservation: "Which account does the reservation go to: the agency's client account or another account?". Agency: "la cuenta de depósito de la agencia con IBAN ES..." / "the agency's deposit account with IBAN ES..."; other: "la cuenta de la parte vendedora con IBAN ES..." / "the seller's account with IBAN ES...". Saved to memory if the user wishes |
| depositario, depositario_mayus, depositario_tr, depositario_mayus_tr | yes | who returns the money: "la agencia" / "La agencia" / "the agency" / "The agency", or "la parte vendedora" / "La parte vendedora" / "the seller" / "The seller" |

| optional `deposito_agencia` | if the agency holds the funds | deposit on behalf of both parties sentence in stipulation 2; remove when the money goes to another account |
| fecha_visita, fecha_nota_simple | yes | |
| hora_limite_respuesta, fecha_limite_respuesta(_tr) | yes | "18:00" and "12 de septiembre de 2026" / "12 September 2026" |
| dias_arras, porcentaje_arras, arras_total_cifra(_tr), dias_escritura | yes | arras_total = price × percentage |
| fecha_limite_financiacion(_tr), importe_financiacion_cifra(_tr) | if block 7 bis | |
| honorarios_comprador_frase/_tr | no | ", salvo los pactados en el encargo de búsqueda de fecha {{fecha}}" / ", except those agreed in the buyer's mandate dated {{fecha}}" |
| notario_propuesto_frase/_tr | no | "; las partes proponen la notaría de {{notaría}}" / "; the parties propose the notary office of {{notaría}}" |
| agencia_email_datos, idioma_cliente_es/_tr | yes | |

## Annexes
The document carries no empty annex pages. The transfer receipt is not an annex: the buyer uploads it at signing, in the "Justificante de la transferencia" (transfer receipt) row of box B (upload button `tink-upload-attachment[1]` and file name `tink-uploaded-attachmentname[1]`, required; fixed in the template). The nota simple (Anexo II) is a PDF the user provides, merged into the document with `merge_files` before creating the draft (see `references/formify.md`, 5b). If the user does not have them to hand, the document is generated anyway and they are told in the chat that they must add them before sending, or it is agreed with them to remove the reference.

## Variants
- **Catalonia**: replace stipulation 7 with the CCCat variant (commented in the template). Keep the rest.
- **Consumer buyer**: whenever they are a natural person. Stipulation 13 already protects their jurisdiction. There is no 14 day right of withdrawal in the reservation: contracts concerning real estate are excluded from that right, so no withdrawal block is added (unlike the nota de encargo).
- **Offer below the asking price**: normal; do not comment on it in the document.
- **Several sellers** (inheritance, marriage): all in section D (acceptance) and all sign. Ask whether the property is the family home of a married couple; if it is and only one is the owner, the non-owner spouse also signs the acceptance (explained in guide 04; here it is enough to add them as a signer with role "Cónyuge").

## Rules for this document
- Never suggest a cash reservation. If the user asks for it, explain the legal limit in the chat and propose a bank transfer.
- Do not remove stipulation 7 or change the formula "arras penitenciales conforme al artículo 1454 del Código Civil" (or 621-8 in Catalonia). It is one of the three exceptions in which the document cites the law.
- If the user wants the reservation to be "non-refundable in any case", explain that with a consumer buyer that clause is unfair and is not included.
- The seller's acceptance is their electronic signature; there are no boxes to fill in at signing. A counteroffer is a new document.

## Signers and Formify
- Signing order enabled (enableSigningOrder): buyers (signingOrder 1), agent (1), sellers (2). Formify notifies the seller when buyer and agency have signed.
- Roles: "Comprador/a", "Agente inmobiliario", "Vendedor/a". `id_scan: false` (identification is done in the KYC, document 02); if the user wants identification in this act, `id_scan: true` for buyers and sellers and signatureType digital_ink_id_scan.
- Draft title: "Oferta y reserva {{inmueble_corto}}".
- Invitation message for the seller (Spanish): "Ha recibido una oferta por {{inmueble_corto}}. Revise el documento y, si está conforme, firme para aceptarla antes del {{fecha_limite_respuesta}}."

## Frequent errors this template avoids
- Reservation "en concepto de señal" (as a deposit) without saying whether it is penitencial: presumed an advance payment and nobody can freely withdraw.
- Response deadline without consequence.
- Money in the agency's hands without saying on whose behalf or when it is returned.
- Citing Ley 28/1998 (instalment sales of movable goods) as if it governed the reservation: no law is cited in this document except art. 1454 CC.
- Imposing on the consumer buyer the courts of the agency's city.
