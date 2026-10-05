# Guide 04 (v2: tables A and B, clauses that only cite the tables): Contrato de arras penitenciales (penitential deposit contract)

Use: when the seller has accepted the offer and the parties fix the price, the arras (deposit) and the deed date. It is the document with the most money at stake in the package. Default profile: **professional**. Read `references/regions-table.md` first (civil law of the region) and, if there is any doubt about the clause, `references/controls.json` (controls for art. 1454 CC, 621-8 CCCat and ley 467 of the Fuero Nuevo).

## What sets this template apart
1. Clause 3 meets the four conditions that case law requires for the arras to be penitential: it names them as such, cites the article, gives both parties the right to withdraw and spells out the consequence for each. A bare mention "según el artículo 1454" is not enough; the Supreme Court has treated it as an advance payment (STS 583/2018).
2. Variant for Catalonia with article 621-8 CCCat and the financing rule of 621-49, which applies by default in Catalonia if the contract mentions financing.
3. Financing clause as a condition with date, lender and minimum amount, and its express alternative (no financing), so it is never left open.
4. Non-owner spouse as a signer when the property is the family home, or a declaration that it is not. No model on the market covers this.
5. The agency as depositary with the seller's express authorisation and a delivery deadline, if the user wants it.
6. No cash, no mixed penalty clauses, no "a cuenta del precio" outside the final allocation.

## Minimum questions (one per message; reuse what is already in the conversation from the reservation or in memory)
1. Region of the property (variant CC, CCCat in Catalonia or FN in Navarre; family home article according to `references/regions-encargo.md`).
2. Sellers: all owners, with ID document and address, marital status and matrimonial property regime if married. Is the property the habitual family home of any married seller? If yes and the spouse is not an owner: spouse as signer (optional `conyuge`). If not: declaration that it is not. Tax resident in Spain? (optional `no_residente` or `residente`).
3. Buyers: all of them, with ID document (NIE if foreign; if they do not have one yet, warn in the chat that they will need it for the deed) and address.
4. Does anyone act under a power of attorney? Then the parties block with "en nombre y representación de ... según poder ..." and optional `poderes` with the annex.
5. Property: address, floor area (usable or built), Land Registry, finca (registered plot), tomo, libro, folio, cadastral reference, annexes, title of acquisition (purchase, inheritance, year), date of the nota simple (registry extract), charges according to the nota simple.
6. Price, arras (guideline 5 to 10 %), balance. Who receives the arras? The seller directly (default) or the agency as depositary (optional `depositaria`, with IBAN). Is there a seller's mortgage to be cancelled at the deed with the buyer's funds? (phrase `hipoteca_vendedor_frase`).
7. Does the buyer need a mortgage? Yes: optional `financiacion` with deadline, lender and minimum amount. No: optional `sin_financiacion`. Exactly one of the two.
8. Deed deadline (guideline 30 to 90 days; foreign buyers without NIE need more; in Catalonia with notarial deposit, six months maximum), place of the notary's office, days of notice (7), days to return the doubled arras (10 to 15).
9. Documentation: number and letter of the CEE (energy certificate); cédula de habitabilidad (habitability certificate; Catalonia, field `cedula_frase`); ITE (building inspection) if the building has one; furniture included (optional `muebles` with inventory).
10. Costs: by default the buyer pays ITP or IVA and AJD, notary fees for the sale and registry; the seller pays plusvalía and cancellation of charges. IBI (property tax) for the year: by default the seller pays it ("el impuesto sobre bienes inmuebles del año en curso"); alternative pro rata. If the user wants the seller to pay the notarial original (matriz), phrase `notaria_matriz_frase` in the negative (see fields).
11. Client's language.

## Fields
| Field | Required | Note |
|---|---|---|
| agencia_*, agente_* | yes | from memory (header and, if depositary, parties block) |
| referencia, lugar, fecha_larga | yes | |
| vendedor_nombres, vendedor_docs, vendedor_domicilio, vendedor_email | yes | table A; text or field if the user does not have them |
| conyuge_nombre, conyuge_doc, conyuge_de | if optional conyuge | row in table A |
| inmueble_direccion, inmueble_corto, superficie_frase(_tr), registro(_tr), finca, registro_detalle(_tr), refcat, titulo_adquisicion(_tr) | yes | floor area: "construida de 95 m²" / "of 95 m² built"; title: "compraventa en escritura de 12 de mayo de 2015" / "purchase by deed of 12 May 2015" |
| anejos_frase(_tr) | no | |
| fecha_nota_simple, cargas_frase(_tr) | yes | "se encuentra libre de cargas y gravámenes" / "is free of charges and encumbrances"; or "está gravado con hipoteca a favor de X, que la parte vendedora cancelará en el otorgamiento de la escritura" / "is encumbered by a mortgage in favour of X, which the seller shall cancel on execution of the deed" |
| vivienda_familiar_declaracion(_tr) | yes | If the spouse signs: "el inmueble constituye la vivienda habitual de la familia de la parte vendedora, por lo que comparece su cónyuge para prestar el consentimiento previsto en {{artículo}}." If not: "el inmueble no constituye la vivienda habitual de la familia de la parte vendedora, a los efectos de {{artículo}}." Article by region: "el artículo 1320 del Código Civil" (CC), "el artículo 231-9 del Código Civil de Cataluña" (ES-CT), "el artículo 190 del Código del Derecho Foral de Aragón" (ES-AR), "la ley 81 del Fuero Nuevo de Navarra" (ES-NC), "el artículo 4.3 de la Compilación de derecho civil de las Illes Balears" (ES-IB; "el artículo 67.1" in Eivissa and Formentera). Basque Country, Galicia and Comunitat Valenciana: el artículo 1320 del Código Civil. Unmarried seller or legal entity: "la parte vendedora no está casada y el inmueble no constituye vivienda familiar alguna." |
| estado_cargas_objeto(_tr) | yes | "libre de cargas, gravámenes, arrendatarios y ocupantes" / "free of charges, encumbrances, tenants and occupants" |
| precio_letras(_tr), precio_cifra(_tr), arras_letras(_tr), arras_cifra(_tr), arras_pct, resto_letras(_tr), resto_cifra(_tr) | yes | balance = price minus arras; if there was a prior reservation, today's arras include the reservation: say so in `recibi_frase` |
| hipoteca_vendedor_frase(_tr) | no | ", destinándose de esa cantidad la parte necesaria a la cancelación de la hipoteca que grava el inmueble, cuyo certificado de deuda aportará la parte vendedora" / ", the necessary portion of which shall be applied to cancelling the mortgage on the property, the seller providing the lender's debt certificate" |
| arras_depositario_resumen(_tr) | yes | " a la agencia, que las custodia" / " to the agency, which holds them"; or " al vendedor" / " to the seller" |
| iban_deposito | if depositaria | |
| fecha_escritura(_tr), dias_devolucion, lugar_notaria, dias_preaviso_notaria | yes | |
| deposito_notarial_frase(_tr) | no (CCCat only) | " Las arras se depositan ante el notario {{notario}} por un plazo de {{n}} meses y las partes solicitan la constancia del depósito en el Registro de la Propiedad conforme al artículo 621-8.3 del Código Civil de Cataluña." / " The deposit is lodged with notary {{notario}} for {{n}} months and the parties request that the deposit be recorded at the Land Registry under article 621-8.3 of the Civil Code of Catalonia." Six months maximum. Otherwise empty. |
| fecha_limite_financiacion(_tr), entidad_financiera, importe_financiacion_cifra(_tr) | if financiacion | |
| financiacion_cccat_frase(_tr) | CCCat with financing only | ", conforme al artículo 621-49 del Código Civil de Cataluña, y la parte compradora dejará a la vendedora en la situación en que se hallaría de no haberse celebrado el contrato" / ", under article 621-49 of the Civil Code of Catalonia, and the buyer shall leave the seller in the position it would have been in had the contract not been concluded". Elsewhere, empty. |
| muebles_frase(_tr) | no | " y con los muebles y enseres relacionados en el Anexo II" / " and with the furniture and fittings listed in Annex II" |
| cee_numero, cee_letra | yes | |
| cedula_frase(_tr) | no | "; la cédula de habitabilidad n.º {{n}} de fecha {{fecha}} (Anexo V)" / "; habitability certificate no. {{n}} dated {{fecha}} (Annex V)" |
| ite_frase(_tr) | no | "; el informe de la inspección técnica del edificio de fecha {{fecha}}" / "; the building technical inspection report dated {{fecha}}" |
| declaraciones_extra(_tr) | no | ", salvo {{lo que declare}}" / ", except {{...}}" |
| notaria_matriz_frase(_tr) | no | empty = the buyer pays all notary fees. If the user wants the legal rule: ", salvo la matriz, que corresponde a la parte vendedora" / ", except the original deed (matriz), which is borne by the seller" |
| ibi_frase(_tr) | yes | "el impuesto sobre bienes inmuebles del año en curso" / "the property tax (IBI) for the current year"; or "la parte proporcional del impuesto sobre bienes inmuebles del año en curso hasta la fecha de la escritura" / "the proportional part of the property tax for the current year up to the date of the deed" |
| ley_aplicable(_tr) | yes | "la ley española" / "Spanish law"; in Catalonia: "la ley española y, en particular, el Código Civil de Cataluña" / "Spanish law and, in particular, the Civil Code of Catalonia" |
| recibi_frase(_tr) | no | ". La parte vendedora declara recibir en este acto la cantidad indicada en la estipulación 2.a)" / ". The seller acknowledges receipt of the sum stated in clause 2.a)"; with depositary: ". La agencia declara recibir en depósito la cantidad indicada en la estipulación 2.a), en la que se incluye la reserva de {{n}} € entregada el {{fecha}}" |
| agencia_email_datos, idioma_cliente_es(_tr) | yes | |

## Annexes
No empty annex pages. The proof of the arras transfer is not an annex: the buyer uploads it when signing, in the row «Justificante de la transferencia» of table B (upload button `tink-upload-attachment[1]` and file name, required; fixed in the template). The other annexes cited (II inventory, III nota simple, IV CEE, V cédula, VI powers of attorney) are PDFs that the user provides and that are joined with `merge_files` before the draft (`references/formify.md`, 5b). The optionals `muebles`, `cedula` and `poderes` only add the mention in the text.

## Variants and optionals
- `--variant FN` for properties in Navarre: clause 3 cites ley 467 of the Fuero Nuevo (without an express agreement the arras would be confirmatory, as in Catalonia); `ley_aplicable` "la ley española y, en particular, el Fuero Nuevo de Navarra"; `financiacion_cccat_frase` empty; family home with ley 81.
- `--variant CCCat` for properties in Catalonia. With it: Catalan `ley_aplicable`, `financiacion_cccat_frase` if there is financing, `deposito_notarial_frase` if the user wants a notarial deposit and registration (explain in the chat: six months maximum, the notary hands the arras to whoever is entitled, it protects the buyer against a sale to a third party).
- Exactly one of `financiacion` / `sin_financiacion`, and exactly one of `no_residente` / `residente`.
- `conyuge` when there is a family home and a non-owner spouse. In Catalonia consent cannot be given generically in advance: that is why the spouse signs this specific contract.
- `depositaria` when the agency holds the arras.
- `muebles` according to the documentation; cédula and powers of attorney go through the fields `cedula_frase` and `poderes_frase`.

## Rules for this document
- Do not touch clause 3 outside the fields. Do not add "a cuenta del precio" in clause 2.a); the allocation to the price is already at the end of clause 3.
- Do not mix penalties, damages or penalty clauses with the arras. If the user wants confirmatory or penal arras, say that this template is for penitential arras and that other types require specific drafting; do not improvise.
- Check that balance = price minus arras and that arras_pct is consistent. The style checker does no arithmetic: do it yourself and write it in the chat.
- Nota simple less than one month old; if it is older, warn.
- Non-resident seller: the 3 % withholding is the buyer's obligation; never remove clause 9 when the seller does not reside in Spain.

## Signers and Formify
- Signing order enabled: sellers and spouse (signingOrder 1), buyers (2), depositary agency (3) if involved. Roles: "Vendedor/a", "Cónyuge", "Comprador/a", "Agencia depositaria".
- Identity: `id_scan: true` for sellers, spouse and buyers (digital_ink_id_scan); face_liveness if the account has it and the user prefers it. Agency with digital_ink.
- Draft title: "Arras {{inmueble_corto}}".
- Invitation message (buyer, in their language or in Spanish): "Contrato de arras de {{inmueble_corto}}. Revise el precio, las arras, la fecha de escritura y la estipulación 3 antes de firmar."
- Bilingual with foreign clients. If the buyer wants a sworn translation, say that the translated column is not one and that it can be ordered separately; it is not mandatory.

## Frequent errors this template avoids
- Bare citation of art. 1454 without a right to withdraw or consequences: arras reclassified as an advance payment (STS 583/2018).
- "Art. 1254" by copying error in popular models.
- Financing agreed orally or without date, lender and amount: no protection for the buyer.
- Non-owner spouse missing: the deed gets stuck at the notary's office.
- Deed deadline too short for foreign buyers without NIE.
- Non-resident seller without the 3 % withholding.
