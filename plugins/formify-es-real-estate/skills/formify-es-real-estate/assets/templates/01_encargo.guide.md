# Guide 01: Nota de encargo (listing mandate) and real estate brokerage contract

Use: every time an owner instructs the agency to sell or let a property. It is the document that authorises the agency to advertise, show and receive sums, and the one that sets the fee. In Catalonia and the Balearic Islands there is a legal minimum content; in the Valencian Community, mandatory identifiers; elsewhere, good practice and consumer law. Default profile: **official** in ES-IB, ES-CT, ES-VC; **profesional** elsewhere.

Read `references/regions-table.md` (the row for the region) and `references/regions-encargo.md` first and `references/withdrawal.md`.

## Template structure
Box A (client and agency, side by side), B (property), C (mandate and fee), D (insurance and guarantee, optional `seguro`) and E (stipulations), which only refer to "el cliente" (the client), "la agencia" (the agency), "el inmueble" (the property) and the boxes. Each piece of data once only, in its box. If the user does not have the client's details: ask "Do you have the client's details, or would you prefer that they fill them in when signing?" and pass the missing ones as fields (name 180, ID document 120, address 180, email 180, phone 100 pt). No "Lo esencial" (key points) box.

## What sets this template apart
1. Part A (minimum data) separated from part B (freely agreed terms), as the Balearic Islands require (DA 13.17.3) and as is advisable everywhere.
2. **Right of withdrawal** block with the legal text and the form (Anexo I), plus the **express request to start the service**. Without this, a consumer owner who signs remotely or at home can withdraw up to twelve months later and the agency loses the fee even if it has found a buyer (STS 167/2021). No template on the market includes it.
3. Consequence of a direct sale under exclusivity worded as proportionate compensation, not as a fine; without the word "penalización".
4. Fee accrual defined (conclusion with a person introduced by the agency) and a twelve month tail with evidence (visit log).
5. Agent's insurance and guarantee identified, as the three regulated regions require.

## Minimum questions (one per message; skip whatever is in memory)
1. Region of the property (only the region; the regions table decides the rest without commenting on it).
2. Owner(s): name, ID document, address, email, phone. Is anyone acting as representative? If yes: name, ID document and means of accreditation (power of attorney deed dated X before notary Y). Is it a natural person selling their own home, or a business? (determines whether they are a consumer).
3. Is it the family home of a married couple where the other spouse is not an owner? If yes, offer to add them as a signer (optional here; in the arras it will be mandatory).
4. Property: address, cadastral reference, Land Registry and finca (tomo, libro, folio, inscripción if available), declared charges (mortgage, attachments, easements), protection regime (VPO or unrestricted), relevant legal situation (proceedings, occupation, current tenancy).
5. Transaction (sale or letting), price or rent, exclusive or not, start and end dates (guidance: three to six months; never propose more than twelve).
6. Fee: percentage or amount; tax (IVA 21 %; IGIC 7 % in the Canary Islands; IPSI 4 % in Ceuta and Melilla) and the total with tax included, which consumer law requires to be shown (for example, "el 5 % más IVA" is also printed as "6,05 % del precio, IVA incluido"); when it is paid (usual: at signing of the deed; alternative: half at arras and the rest at the deed).
7. Authority to receive arras: cap as a percentage (usually 10 %).
8. Consequence of a direct sale under exclusivity: by default "la mitad de los honorarios del cuadro C" (half of the fee in box C); the user may set a different proportion. If they ask for the full fee, explain in the chat that courts moderate these clauses when they are not proportionate to the work done and that half is the formula that has held up best.
9. Frequency of the report to the client (fifteen days, one month).
10. Tacit extension? By default no with consumers. If yes: "una sola vez, por igual plazo, salvo preaviso de quince días" (once, for the same term, unless fifteen days' notice is given) (OPTIONAL block prorroga).
11. "Do you want to include the civil liability insurance and the guarantee (insurer, NIF and policy number)?" Yes: OPTIONAL block `seguro` with the details the user gives, saved to memory if they wish. No: no block, no comments. Never say it is mandatory or in which region. (Previously: mandatory in ES-IB, ES-CT, ES-VC; elsewhere "si procede" (where applicable), and if the agency has none, write "No exigido en esta región" and mention in the chat that in three regions it is required).
12. How is it signed? Remotely (Formify link) or at the client's home. If at the home and the visit was not requested by the client, the withdrawal period is 30 days instead of 14.
13. Client's language.

## Fields
| Field | Required | Note |
|---|---|---|
| agencia_*, agente_*, agencia_email, agencia_telefono, agencia_email_datos | yes | from memory |
| agencia_registro_linea | no | header: "<br>ROAI n.º 0000" or empty |
| registro_linea | yes | per `references/regions-encargo.md`, section "Register line": "Registro Oficial de Agentes Inmobiliarios de las Illes Balears (ROAI), n.º 0000", "AICAT n.º…", "RAICV n.º…", "RAIN n.º…", "RAIC n.º…", "Registro de Agentes Inmobiliarios de Navarra n.º…"; "No inscrito (inscripción voluntaria en esta región)"; "Pendiente de inscripción" (Catalonia, Valencia); "Inscripción pendiente de desarrollo reglamentario" (Andalusia); empty in regions without a register / English version follows after " / " |
| establecimiento_linea | yes | "Establecimiento abierto al público en {{dirección}}; atención de consultas y reclamaciones en la misma dirección" or "Servicios por internet; dirección postal para reclamaciones: {{dirección}}" (plus English version) |
| cliente_nombres, cliente_docs, cliente_domicilio | yes | box A, client column: names of all owners; ID documents ("NIE X0000000Y; DNI 00000000A"); address. Text or field `{"field": ..., "width": ...}` if the user does not have the data |
| titulo_habilitante(_tr) | yes | "Pleno dominio" / "Full ownership"; "Nuda propiedad y usufructo" / "Bare ownership and usufruct"; "Herederos, según escritura de aceptación de herencia de fecha X" / "Heirs, per deed of acceptance of inheritance dated X" |
| representante_bloque | with `representante` | "D. X, DNI Y, según escritura de poder de fecha Z ante el notario W / per power of attorney dated Z before notary W"; without a representative the row does not appear |
| cliente_email, cliente_telefono | yes | text or field |
| garantia_frase(_tr) | yes | with `seguro`: ", cubierta por la garantía del cuadro D" / ", covered by the guarantee stated in box D"; without seguro: "" |
| inmueble_direccion, inmueble_corto, refcat, registro, finca | yes | |
| registro_detalle | no | ", tomo X, libro Y, folio Z, inscripción N" or empty |
| cargas_declaradas(_tr), regimen_proteccion(_tr), situacion_juridica(_tr) | yes | "Libre de cargas" / "Free of charges"; "Hipoteca a favor de X" / "Mortgage in favour of X"; "Vivienda libre" / "Unrestricted housing"; "Ninguna" / "None" |
| operacion(_tr), operacion_mayus(_tr) | yes | "venta"/"sale", "VENTA"/"SALE"; "arrendamiento"/"letting" |
| exclusiva_si_no(_tr), exclusiva_resumen(_tr) | yes | "SÍ"/"YES"; summary: "Sí, hasta el {{fecha_fin}}: no se puede encargar a otra agencia ni vender por cuenta propia sin compensar a la agencia." |
| precio_cifra(_tr), precio_letras | yes | |
| precio_nota | no | "; renta mensual" / ", monthly rent" for lettings |
| fecha_inicio(_tr), fecha_fin(_tr), plazo_resumen(_tr) | yes | |
| honorarios_detalle(_tr), honorarios_resumen(_tr) | yes | "El 5 % del precio de venta" / "5 % of the sale price" |
| impuesto_nombre(_tr), impuesto_tipo | yes | "IVA"/"VAT", 21; Canary Islands "IGIC", 7; Ceuta and Melilla "IPSI", 4 |
| honorarios_total(_tr) | yes | the total with tax included: "el 6,05 % del precio de venta" / "6.05 % of the sale price", or "6.050 €" / "€6,050" |
| honorarios_pago_detalle(_tr), honorarios_pago_resumen(_tr) | yes | "Se devengan al perfeccionarse la venta y se pagan en el otorgamiento de la escritura pública, por transferencia" / "Accrue on conclusion of the sale and are paid on execution of the public deed, by bank transfer"; summary: "en la escritura" / "at the deed" |
| rc_aseguradora, rc_nif, rc_poliza, garantia_entidad, garantia_nif, garantia_numero | only if the user wanted the `seguro` block | If they only have one of the two (policy or bank guarantee), "n/a" in the other. In regions without a guarantee: "No exigido en esta región / Not required in this region" in the entity field and "n/a" in NIF and number |
| max_arras_pct | yes | "10" |
| consecuencia_venta_directa(_tr) | yes (exclusive) | "la mitad de los honorarios del cuadro C" / "half of the fee stated in box C" |
| informe_periodicidad(_tr) | yes | "quince días" / "fifteen days" |
| prorroga_frase(_tr) | no | " y se prorrogará una sola vez por igual plazo si ninguna de las partes comunica a la otra su voluntad de no prorrogarlo con quince días de antelación" / " and shall be extended once for the same term unless either party notifies the other fifteen days in advance that it does not wish to extend it" |
| preaviso_dias | yes | "15" |
| dias_desistimiento | yes (consumer) | "14" or "30" |
| fecha_larga_tr | yes | "5 September 2026" |
| idioma_cliente_es(_tr) | yes | |

## Variants and optional blocks
- `--variant NOEXCLUSIVA` when there is no exclusivity. Then `consecuencia_venta_directa` is not used.
- Optional `desistimiento` and `desistimiento_anexo`: offered with a single question, "Do you want to include the information on the right of withdrawal? (recommended when the owner is a private individual)". Yes: both blocks. No: neither, with no further comment. The user decides. (Context for you, not for the chat: it applies when the client is a consumer, which includes someone selling their own home. Remove both only if the client is a company or a professional selling a business asset, and say so in the chat. The style checker warns if they are missing.
- Optional `prorroga`: it does not exist as a block; it is handled with the `prorroga_frase` field.
- Catalonia: a consumer client may request the document in Catalan. If they do, the second column is Catalan in legal register (not English) and clause 11 reads "en español y en catalán". The Catalan minimum content is already covered by boxes A to C (charges, protection regime, legal situation, powers).
- Letting: replace "venta" with "arrendamiento", the price with the monthly rent, and stipulation 5 reads the same (conclusion = signing of the tenancy agreement). Fees for letting a home are paid by the landlord; charge nothing to the tenant.

## Rules for this document
- Do not modify the text of the "Derecho de desistimiento" block or Anexo I except for the fields. It is legal text (exception to the general rule).
- No "penalización", no waiver of withdrawal, no submission to courts other than those of the property's location for consumers.
- Legal citation allowed in this document: none in the stipulations; the withdrawal block is an official model and cites no articles.
- Registration is mandatory in Catalonia and the Valencian Community: if the user has no number, warn in the chat that they cannot legally offer the property without registering, and keep generating the document with "Pendiente de inscripción". In Andalusia it is mandatory by law but the register is not yet operational: "Inscripción pendiente de desarrollo reglamentario", no warning.
- Voluntary registration: Balearic Islands (insurance and guarantee mandatory for everyone), Madrid, Canary Islands and Navarre. The other regions have no operational register (`references/regions.md`).
- The `seguro` block is always the user's choice, in every region, with question 11 and nothing more: no "required", no mention of which region demands it. In Andalusia the question allows a policy or a bank guarantee ("Insurer and policy number, or entity and guarantee number?"); if they say no, no block and no comment.
- Valencian Community: identify policy and guarantee, never print minimum amounts (annulled).
- Co-official language: in Catalonia the consumer may request the document in Catalan (right column in Catalan); in the Balearic Islands, Valencia, Galicia and the Basque Country, at the client's request, the right column is in the co-official language instead of English. One question only if the client is from the region and their language has not been stated.

## Signers and Formify
- Signers: each owner (role "Propietario/a"), the representative if any (role "Representante"), the non-owner spouse if the user wants (role "Cónyuge"), and the agent (role "Agente inmobiliario").
- Identity: `id_scan: true` for owners and representative, signatureType digital_ink_id_scan if the account allows it; face_liveness if the user prefers and it is enabled. The agent signs with digital_ink.
- No signing order (or owners first if the user asks).
- Draft title: "Nota de encargo {{inmueble_corto}}".
- Invitation message: "Nota de encargo para la {{operacion}} de {{inmueble_corto}}. Revise los cuadros A a C, las estipulaciones y la información sobre su derecho de desistimiento. Firme cuando esté conforme."
- After signing, the copy Formify sends by email meets the requirement of a copy on a durable medium.

## Frequent errors this template avoids
- Mandate signed at the seller's home without withdrawal information: fee lost (STS 167/2021, SAP Sevilla 2020).
- Disproportionate fine for direct sale: void (SAP Madrid 361/2024).
- No defined accrual: disputes over whether the fee is due when the sale falls through after arras.
- No Land Registry or cadastral data: breaches Balearic Islands and Catalonia rules.
- Slipping in exclusivity with a checkbox without explaining the consequence.
