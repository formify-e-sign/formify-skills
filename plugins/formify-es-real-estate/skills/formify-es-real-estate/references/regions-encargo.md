# Regions: what the mandate note (encargo), the arras and the header take from the region

## Minimum content of the mandate note required by law

**Illes Balears (DA 13 point 17 Ley 3/2024, as worded by Ley 4/2026):** a) client details and the title that entitles them; b) agent: name and address, company, address and CIF, register number if registered; c) property with land register identification and cadastral reference; d) transaction and express indication of exclusivity; e) term with start and end, or indefinite until revocation with a communication mechanism; f) price or rent; g) fees with a breakdown of taxes and the form of payment; h) details of the liability policy and of the guarantee. The minimum content must be clearly distinguished from the freely agreed stipulations (17.3). That is why template 01 has boxes A to D and the stipulations in E.

**Cataluña (Llei 18/2007 art. 55.6):** a) identity of the agent and AICAT number; b) identity of the owners and, where applicable, representative; c) term; d) description of the transaction; e) identification of the property with land register data, charges, encumbrances and affectations; f) housing protection regime, where applicable; g) offer price; h) relevant legal aspects, in particular pending court proceedings, declared under the owner's responsibility; i) agent's remuneration (percentage or fixed amount) and form of payment; both parties may not be charged unless expressly agreed; j) rights and obligations of the parties and powers of the agent. The note is signed before the property is offered or advertised (55.5.b, 55.6). Art. 55.7: the agent verifies ownership and charges before signing documents with third parties.

**Comunitat Valenciana (Decreto 98/2022 art. 8, in force):** RAICV registration number and badge on contracts and advertising; identify the insurer or financial institution and the reference number of the guarantee (DA 6.ª Ley 2/2017). The minimum amounts in art. 3.c) are annulled: do not print them.

**Andalucía (Ley 5/2025 art. 53.3):** "Los agentes de intermediación inmobiliaria deberán facilitar a las personas interesadas, cuando así lo soliciten, el número de póliza y la denominación de la entidad aseguradora, o bien el número de aval y la entidad financiera correspondiente, en su caso. Esta información deberá incluirse igualmente en el contrato de mandato o la nota de encargo." (Agents must provide, on request, the policy number and insurer, or the guarantee number and financial institution, and this information must also be included in the mandate contract or mandate note.) While the register is not operating, the register line reads "Inscripción pendiente de desarrollo reglamentario" (registration pending regulatory development). The insurance block is offered with the usual question; the user decides.

**Rest of Spain:** there is no regional legal list. Apply the consumer pre-contractual information (identity and NIF of the trader, total price including taxes, duration, language of the contract, right of withdrawal) and the practice of template 01. The template is used in full all the same: it is easier to comply with more than with less.

## Register line in the header and in part A (field `registro_linea`)

- Registered: "<register name from the table>, n.º <number>" (ROAI n.º…, AICAT n.º…, RAICV n.º…, RAIN n.º…, RAIC n.º…, Registro de Agentes Inmobiliarios de Navarra n.º…).
- Not registered in a region with a voluntary register (Baleares, Madrid, Canarias, Navarra): "No inscrito (inscripción voluntaria en esta región)" (not registered, registration voluntary in this region).
- Not registered in a region with an operating mandatory register (Cataluña, Comunitat Valenciana): "Pendiente de inscripción" (registration pending), and one sentence in the chat: without registering they cannot legally offer the property. Once, nothing more.
- Andalucía: "Inscripción pendiente de desarrollo reglamentario (Ley 5/2025)".
- Regions without a register: the line is not printed.

## Family home (who signs and which article the declaration cites)

- Código Civil art. 1320 (all regions not listed below, including the Comunitat Valenciana): disposing of the family's habitual home requires the consent of both spouses even if it belongs to only one. Arras: the non-owner spouse signs. Mandate: only the owner signs; the spouse is optional (recommended in exclusive mandates).
- Cataluña art. 231-9 CCCat: the same, the consent cannot be given in general terms and a sale without it is voidable within four years.
- Illes Balears: Compilación art. 4.3 (Mallorca and Menorca) and art. 67.1 (Eivissa and Formentera), voidable within four years. The declaration cites "el artículo 4.3 de la Compilación de derecho civil de las Illes Balears" (or 67.1 in the Pitiusas).
- Aragón art. 190 of the Código del Derecho Foral de Aragón: consent of the other spouse; the sale extinguishes the expectant right of widowhood. The declaration cites that article.
- Navarra ley 81 of the Fuero Nuevo: consent of both, or assent of the other if the asset is separate property. The declaration cites "la ley 81 del Fuero Nuevo de Navarra".
- País Vasco and Galicia: Código Civil art. 1320 (their civil laws do not regulate the family home). In marriages under the Basque "comunicación foral" regime both spouses sign for any asset (art. 135 Ley 5/2015).
- If the property is not the family home, the arras document includes the declaration "el inmueble no constituye la vivienda habitual de la familia" (the property is not the family's habitual home) with the same article.

## Tax on fees and how it is printed

IVA 21 % on the mainland and in Baleares (Ley 37/1992 art. 90; there is no reduced rate for intermediation); IGIC 7 % in Canarias; IPSI 4 % in Ceuta and Melilla. The consumer must see the total price including taxes (TRLGDCU art. 60.2.c and 20.1.c): the fee row prints the percentage or amount, the tax with its rate and the total with the tax included (`honorarios_total`). Never a bare "IVA no incluido" (VAT not included).
