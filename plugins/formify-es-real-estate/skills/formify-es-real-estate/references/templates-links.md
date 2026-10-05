<!-- generated from core/references/templates-links.md by build_vertical.py; edit the core file, not this copy -->
# Formify templates and public links

Formify MCP 1.3.0 added two things a vertical can use: a **template** (the uploaded PDF with its signature slots saved once, so a new draft needs no upload) and a **public link** (one reusable signing address that anyone holding it can open; each opener produces a separate document). Both are optional, both are the user's choice, and both fit only one kind of document.

## Which documents qualify
A document qualifies for a template when the PDF is the same for every client and only the form fields differ: the signer fills the fields in Formify, the organisation types nothing per case. In practice that is the identification form (KYC) for a client, and any similar blank the client completes alone. It does not qualify when the engine prints case data into the text (a mandate, a reservation, a deposit contract, a collaboration agreement): those stay drafts from a fresh file.

`segment.json["template_documents"]` lists the qualifying document types by their `document_types` key. A vertical without the key offers no templates.

A public link qualifies for the same documents, when the client fills in the form alone and the organisation wants one address to send to every new client instead of one draft per client.

## The rule: opt-in, once, remembered
1. After the first finished document of a qualifying type in a session (the preview has been shown, the draft exists), ask one question: "Do you want me to save this as a template in Formify, so the next client is two calls instead of an upload?" Never before the first document, never twice for the same type.
2. On yes: `create_template(fileId, name=<document title without client data>, sharingSetting="private", signeeDetails=<the signer list of the draft with the boxes, no names, no contacts>)`. Sharing "shared" needs the account's access levels; if it answers 403, create it private and say so in one line. Keep the `templateId`.
3. Write the id into `formify-memory.md`: on the document type's line, `template=<templateId>`. From then on, that document type starts with `create_draft(templateId=...)`: no engine run, no upload. Then continue at step 3 of `references/formify.md` with `update_draft` for the signer's name and contact (the complete configuration, as always) and the preview.
4. If the form's layout changes (a new template version, an own template), the saved Formify template is stale: create a new one, `delete_template` the old one, update the memory line.
5. The template question is asked after the memory question of `references/memory.md`, in the same message, never as a separate turn.

Public link, only after a template exists for the type and only when the user has said the client fills the form alone:
1. When the core skill `formify-share-link` is installed (`scripts/start.py` reports it), hand the link over to it: say that the identification form can become one link the agency sends to every new client, and let that skill ask its own cost question and create the link. It knows the billing rules; do not repeat its procedure here.
2. Without it, the same rule applies before any call: never create a link without an explicit yes that names the charge, both halves. Say: "That will create a live link, which is billed for the rest of this period and renews while it stays active. Each signature collected through it is charged separately, as it happens. Shall I go ahead?" A user told only about the link's own charge reads a month of signatures as a billing error.
3. On yes: `create_link(fileId=<the template's file>, name=<document title>, ...)` with the settings the tool describes; `get_link` afterwards for the `url` (one retry after five seconds if the first call answers 500). Put `link=<linkId>` on the memory line and show the url once. Insufficient credits or a suspended subscription fails the call cleanly: say so and stop, do not retry.
4. Documents produced through the link appear in `list_link_documents(linkId)`; the user follows them there, not in drafts.
5. To stop a link: `disable_link`, then `delete_link` (a live link answers 409 to delete). `update_link` is a full replacement: pass everything `get_link` returned except the fields that came back as null (`paymentLink`, `idScanBox`), which the schema does not accept.

## What is never done
- No template or link for a document whose text carries case data.
- No template or link created without the user's yes; no link without both halves of the cost named (the link per period, each signature as it happens).
- No client name, address or number in a template or link name.
- Templates and links are the organisation's; the memory file stores only their ids, never the documents made from them.
