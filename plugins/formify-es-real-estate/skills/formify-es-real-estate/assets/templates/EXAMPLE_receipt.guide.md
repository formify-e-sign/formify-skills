<!-- generated from core/templates/EXAMPLE_receipt.guide.md by build_vertical.py; edit the core file, not this copy -->
# Guide: EXAMPLE receipt (copy this structure for every document type)

One guide per template, same headings every time. The agent reads only the guide of the document it is building.

## Minimum questions (in this order, one per message)
Only what is not already in the memory (`formify-memory.md`) or in the conversation.
1. Giver: full name, ID document type and number, address.
2. Receiver: same.
3. Purpose and the items with their counts.
4. Return rule: standard (days after request) or fixed date (variant FIXEDDATE).
5. Loss clause? (OPTIONAL block `loss`). Default yes.
6. Client's language.

## Fields
| Field | Required | Rule |
|---|---|---|
| logo_html | no | `<img src="data:...">` or empty |
| org_name, org_address, org_tax_id, org_data_email | yes | from memory |
| reference | yes | organisation's own reference: document type, year, running number (REC-2026-0001) |
| place, date_long | yes | date written out in the master language ("6 September 2026") |
| what / what_tr | yes | one sentence, both languages, plain words |
| giver_block / _tr, receiver_block / _tr | yes | party formula from the style guide: "Full Name, of legal age, holding <ID type> <number>, domiciled at <address>" |
| giver_name, giver_id, giver_address, giver_email, receiver_name, receiver_id, receiver_address, receiver_email | yes | box A; text, or `{"field": ..., "width": ...}` when the other party fills it in at signing |
| purpose / purpose_tr | yes | noun phrase |
| n_item_a, n_item_b | yes | numbers as digits; 0 allowed |
| return_days | if STANDARD | digits |
| return_date | if FIXEDDATE | date written out |
| until / until_tr | yes | one sentence |
| n_data, n_language | yes | clause numbers after removing optional rows (4 and 5 with `loss`, 3 and 4 without... recount) |
| client_language / _tr | yes | language name in the master language and in the client's language |

## Optional blocks
- `loss`: remove the row if the user does not want it, and renumber (n_data, n_language).

## Variants
- `STANDARD` (default) or `FIXEDDATE` (`--variant FIXEDDATE`).

## Rules for this document
- Never write access codes, passwords or similar secrets into the document, even if the user dictates them.
- Two or more givers: all sign; list them in the party block and add one signer per person.

## Signers and Formify
- Signers: giver and receiver, `role` in the master language (uppercase, as the heading prints it) and `role_tr` the same role in the client's language (omit it in a single-language segment). `id_scan: false` for both unless the segment rule says otherwise.
- Signature type: digital_ink. No signing order.
- Draft title: "Receipt {{what}}".
- Invitation message (personalMessage, max 500 characters, client's language when possible): "Receipt for {{what}} handed over to {{org_name}}. Sign in a minute from your phone."

## Outside this version
- Photos as annexes: only when the flow supports images.

## Frequent errors this template avoids
- No inventory: in case of loss nobody knows what was handed over.
- No return deadline and no consequence for loss.
