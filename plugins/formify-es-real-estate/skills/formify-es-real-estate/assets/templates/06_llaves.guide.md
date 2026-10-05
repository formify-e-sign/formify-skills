# Guide 06: Documento de entrega de llaves (key handover document)

Use: every time the owner leaves keys with the agency to show the property. It is the cheapest document in the package and the one signed most often. Default profile: **light**. Ideal for signing from the phone during the listing visit itself.

## Minimum questions (in this order, one per message)
Only what is not already in memory (`formify-memory.md`) or in the conversation.
1. Owner(s): «Do you have the owner's details (name, ID document, address) or would you rather they fill them in when signing?» If there are several, all sign (block `propietario_2`).
2. Property: full address. Registry details or cadastral reference only if the user has them at hand (optional here).
3. Transaction: sale or letting. Date of the mediation contract (if it does not exist yet, offer to generate the nota de encargo first, document 01).
4. Inventory: number of keys by type, remote controls, other.
5. Viewing log? (OPTIONAL block). By default yes for letting, no for sale.
6. Client's language.

## Fields
| Field | Required | Note |
|---|---|---|
| agencia_nombre, agencia_nif, agencia_direccion, agencia_email_datos | yes | from memory |
| agencia_registro_linea / agencia_registro_frase | no | only if the agency is registered: `<br>Registro {{nombre_registro}} n.º {{numero}}` and `, inscrita en el {{nombre_registro}} con el n.º {{numero}}` (English version: `, registered in the {{nombre_registro}} under no. {{numero}}`). Otherwise, empty string. |
| logo_html | no | `<img src="data:image/png;base64,...">` or empty |
| referencia | yes | the agency's format or `LLA-{{año}}-{{n}}` |
| lugar, fecha_larga | yes | "Palma, 5 de septiembre de 2026" (date in words, never 05/09/26) |
| propietario_1_nombre, propietario_1_doc, propietario_1_domicilio | yes | table B; text or field |
| propietario_2_* | with `propietario_2` | second owner |
| agente_nombre | yes | the signing agent, from memory; never their ID document (the agency is the party; identity is proven at signing when signature with ID document is used) |
| inmueble_direccion, inmueble_corto | yes | short: "el piso de Calle Ficticia 12, 3.º B" |
| inmueble_datos_registrales_frase | no | ", finca registral n.º {{finca}} del Registro de la Propiedad n.º {{n}} de {{ciudad}}, referencia catastral {{refcat}}" or empty |
| operacion / operacion_tr | yes | "venta" / "sale" or "arrendamiento" / "letting" |
| fecha_encargo | yes | date of the mediation contract |
| n_llaves_vivienda, n_llaves_portal, n_llaves_garaje, n_llaves_buzon, n_mandos, otros_llaves | yes | use "0" or "ninguna" when there are none; otros_llaves_tr translated |
| visitas_aviso_frase / _tr | no | if the owner wants prior notice: ", previo aviso a la parte propietaria con al menos {{horas}} horas de antelación" / ", with at least {{horas}} hours' prior notice to the owner". Otherwise, empty. |
| n_datos, n_idioma | yes | 9 and 10 if optional block 8 is present; 8 and 9 if it is removed |
| idioma_cliente_es / _tr | yes | "inglés" / "English", "neerlandés" / "Dutch", "sueco" / "Swedish", "alemán" / "German" |

## Structure (v2)
Tables A to E with bilingual labels and neutral values, then the conditions in two columns that only speak of «la parte propietaria» (the owner), «la agencia» (the agency) and the tables. It is the only version: there is no longer a layout question. Owner fields: `propietario_1_nombre`, `propietario_1_doc` (type and number, for example "NIE X1234567L"), `propietario_1_domicilio`; second owner with the optional block `propietario_2`. If the user does not have the owner's details, they are passed as `{"field": "...", "width": ...}` and the owner fills them in when signing. `propietarios_nombres`, `propietarios_bloque_*` and `inventario_resumen*` are no longer used.

## Optional blocks
- `propietario_2`: second owner in table B.
- `registro_visitas`: remove the two rows if the user does not want it, and renumber (n_datos, n_idioma).

## Rules for this document
- Never write alarm codes, entrance door codes or passwords, even if the user dictates them. Remind them that these are communicated separately (clause 5).
- The key handover presupposes a mediation contract. If there is none, propose generating the nota de encargo first; the user may insist, and then the date "este mismo día" (this same day) is used and a warning is given in the chat.
- Three or more owners: all sign. The document does not allow signing by representation without a power of attorney; if one owner signs for another, ask for the power of attorney and add "en nombre y representación de" in the parties block.
- Letting with a tenant already living in the property: add in clause 4 the phrase ", y previo consentimiento de la persona ocupante" in both columns. Ask.

## Signers and Formify
- Signers: each owner (role "Propietario/a") and the agent (role "Agente inmobiliario"). `id_scan: false` for all.
- Signature type: digital_ink. No signing order.
- Draft title: "Entrega de llaves {{inmueble_corto}}".
- Invitation message (personalMessage, 500 characters maximum, in the client's language or in Spanish): "Recibo de las llaves de {{inmueble_corto}} entregadas a {{agencia_nombre}} para las visitas. Firma en un minuto desde el móvil."

## Not in this version
- Photograph of the set of keys as an annex: it will come when the flow supports images (planned for version 1.2). Until then the inventory in clause 2 is the proof of what was handed over.

## Frequent errors this template avoids
- Network models that name the parent franchise as the recipient: here the receiving party is the agency that holds the keys, with its own NIF.
- No inventory: in case of loss nobody knows what was handed over.
- No return deadline and no consequence for loss.
- Alarm codes written in the document next to the address.
