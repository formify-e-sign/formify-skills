# Guide 05: Acuerdo de colaboración puntual entre agencias (one-off collaboration agreement between agencies) (v2)

Use: one agent has a client for one or more properties of another agent and they want to put the fee split and client protection in writing before the viewing. One client, one or more properties, two agencies, a single contract. Default profile: **professional** (sencillo if the user asks for it). Goal: five questions or fewer when memory has the agency data; three pages; no data repeated in the text.

For framework collaborations (the whole portfolio, several months) this template does not work; say so and offer a one-off agreement per property.

## Template structure
Table A (the two agencies, side by side), table B (the transaction), conditions in two columns that only speak of «la agencia titular» (the listing agency), «la agencia colaboradora» (the collaborating agency), «el cliente presentado» (the introduced client), «los inmuebles del cuadro B» (the properties in table B) and «el cuadro B» (table B). There is no client registration date (the signing of this contract is the registration) and no viewing rule. The template is drafted from the listing agency's side; if the user is the collaborating agency, its data go in the collaborating column and the other agency's data in the listing column. No «Lo esencial» table.

## Two scenarios, one template
1. The user knows all the data: everything printed, no fields.
2. Data are missing: the missing values are written in `data.json` as objects `{"field": "<nombre>", "width": <pt>}` and the other agency fills them in when signing. Each item is a field only once, always in tables A or B, never in the text. Guideline widths: name and address 180, e-mail 180, NIF 100, registry 100, fees and split 90.

## Non-negotiable rule
**The template does not propose any split or any fee.** They are written exactly as the user states them, or they are left as a field for the other agency. If the user asks «¿qué es lo habitual?» (what is usual?), answer in the chat that equal splits are seen and also splits in favour of the listing agency; the split is for them to decide.

## Minimum questions (one per message; skip what is in memory or in the conversation)
1. Who are you in this transaction: listing agency (you hold the mandate) or collaborating agency (you have the client)?
2. Do you have the other agency's data (company name, NIF, address, e-mail, signing agent) or would you rather they fill them in when signing? If they have them: ask for them. If not: only the agent's name and e-mail for the invitation; the rest are fields. Then a single question: «Do you want to add any other detail, for example the ROAI number?» (name the region's registry according to `references/regions-table.md`: ROAI in the Balearic Islands, AICAT in Catalonia, RAICV in Valencia, RAIN in Madrid, RAIC in the Canary Islands, Registro de Agentes Inmobiliarios de Navarra; in the other regions do not ask) (OPTIONAL row `registro`).
2b. Only the first time a collaboration is made (and saved in memory as `agent_id_document=yes|no`): «Do you want the agents' NIE or DNI to appear in the contract?» (say NIE/DNI, never plain «documento de identidad»). If yes: OPTIONAL row `documento_agente` with the user's document (asked for then, once, and saved in `usuario`) and the other agency's as text or field. This is the only situation in which the agent's document is requested, and only because the user has chosen it.
3. Properties and transaction: free text, one or more addresses, with price if the user wants (`inmuebles`, for example "Carrer Inventat 128, 3.º A, Palma, 650.000 €; Carrer Inventat 10, Palma"). Several addresses separated by «;» or by `<br>`. Never create one contract per property. Transaction (sale or letting); the listing agency's mandate in one line (date, term, exclusive or not). If the user is the collaborating agency and does not know it, the mandate can be a field.
4. Introduced client: always stated by the user, never a field. Only first name and surnames (`cliente_nombre`), several clients separated by « y ». Do not ask for an ID document or its numbers; do not ask for the date, time or channel of registration.
5. **Fees agreed with the owner** (those of the listing agency, as a percentage or an amount, excluding IVA). This question is always asked: if the user knows them, they are printed; if not, «Shall we leave it as a field for the listing agency to fill in?». Never omitted.
6. **Split**: «What share does the collaborating agency receive: 50 %, 60/40, another figure, or shall we leave it as a field?». Written as stated (for example «50 %», «40 %», «1.500 € fijos»), plus IVA in the text of condition 4.
7. Payment term after collection (guideline 8 to 15 days). Language of the other agent.

## Fields
| Field | Required | Note |
|---|---|---|
| titular_nombre, titular_nif, titular_direccion, titular_email, titular_agente | yes | listing agency; text or field |
| colaboradora_nombre, colaboradora_nif, colaboradora_direccion, colaboradora_email, colaboradora_agente | yes | collaborating agency; text or field |
| titular_registro, colaboradora_registro | with `registro` | registry number or empty |
| titular_agente_doc, colaboradora_agente_doc | with `documento_agente` | "NIE X0000000Y"; text or field |
| agencia_nombre, agencia_direccion, agencia_nif, agencia_registro_linea | yes | document header: always the user's agency, from memory |
| referencia, lugar, fecha_larga | yes | |
| inmuebles | yes | free text: one or more addresses, optional price ("Carrer Inventat 128, Palma, 650.000 €; Carrer Inventat 10, Palma") |
| operacion / operacion_tr | yes | "venta" / "sale", "alquiler" / "letting" |
| encargo_resumen / _tr | yes | "Contrato de mediación en exclusiva de 1 de julio de 2026, vigente hasta el 31 de diciembre de 2026" / English; or field |
| cliente_nombre | yes | "Jan de Vries" or "Olga Ivanova y Liam Byrne" (names only) |
| honorarios_titular | yes | "5 % del precio" or field; always present |
| reparto_colaboradora | yes | "50 %" or field |
| dias_pago | yes | digits |
| mediacion_frase / _tr | no | ", acudiendo a mediación si lo acuerdan" / ", through mediation if they so agree", or empty |
| idioma_cliente_es / _tr | yes | "inglés" / "English" |

## Rules for this document
- No data from table A or B is repeated in the conditions; if a condition needs changing, change the reference to the table, do not copy the data.
- Do not ask for the agents' ID document unless the user has chosen to include it (question 2b): they sign on behalf of their agency.
- Letting: replace «venta» with «alquiler» in table B; the text of the conditions works as is.
- Several properties with the same client: a single contract, all addresses in the row «Inmueble o inmuebles».

## Signers and Formify
- Signers: the listing agency's agent (role "Agencia titular") and the collaborating agency's agent (role "Agencia colaboradora"), `id_scan: false`, digital_ink. If there are fields for the other agency, signing order: the other agency first (fills in and signs), the user afterwards.
- Draft title: "Colaboración {{cliente_nombre}}".
- Invitation message (500 characters maximum, in the other agent's language): "Acuerdo de colaboración para {{cliente_nombre}}: reparto y respeto de clientes. Revise los cuadros A y B, complete lo que falte y firme desde el móvil."

## Frequent errors this template avoids
- Forgetting to ask what fees the listing agency has with the owner: question 5 is always asked and the data is in table B.
- Split agreed verbally with nothing in writing: the signing of this contract is the client registration.
- Models that prescribe an equal split for a whole network: here the parties write it.
