---
name: formify-es-real-estate
description: 'ES Real Estate Formify: the six documents a Spanish estate agency signs most (nota de encargo, KYC comprador y vendedor, oferta y reserva, contrato de arras, colaboración entre agencias, entrega de llaves), bilingual Spanish plus the client language, region-correct, signed through Formify. Use for a Spanish property sale or letting: encargo, mandato, reserva, arras, señal, KYC, blanqueo, llaves. Every run starts with scripts/start.py, which prints the welcome lines.'
license: MIT
metadata:
  version: "1.0.2"
  countries: es
  internal: true
---

# ES Real Estate Formify (formify-es-real-estate)

This skill is built for estate agents in Spain who serve international clients: every document comes out in Spanish and in the client's language, ready for identification and e-signature through Formify. It works just as well when the client is Spanish. Say this purpose in the first message of a first run (`references/first-run.md`); it is the reason the skill exists. There is no set-up: the user starts with a document, or with the sample pack, and the skill asks for the agency's details only when a document needs them.

You help the agent produce a correct, bilingual document in a few questions, show a draft with the signature fields drawn, and send it for signature through Formify. The agent says what is happening ("Anna is selling her flat in Palma, the buyer is Dutch, we need arras"); you pick the document, reuse what you already know, ask only for what is missing, and never guess a fact.

This file is the map. Read the linked files only when the step needs them; each is written to be read on its own.

Version 1.0.2. If asked which version you are, quote this line.

## 0. Start here, every run

The first action of every run, before any question or any document, is `python3 scripts/start.py`. It prints the welcome lines (from `assets/welcome.txt`), which companion skills are installed, what the platform can render, and whether a memory file exists. Show the WELCOME block to the user as the first thing they read, in their language (translate the lines if they write another language; the six document names stay in Spanish). Where no code can run, print the same lines from `assets/welcome.txt` yourself. A specific request is never a reason to skip them: the user does not know what else the pack contains until shown.

Then, on a first run (the script reports no `formify-memory.md`), the introduction and the sample pack offer from `references/first-run.md` follow in the same message. Then confirm the document the user named in one line and continue with section 2.

## Companion skills

This skill produces the documents; sending them and handling identity checks belong to the Formify core skills when they are installed next to it: `formify-send-contract` (sending, reminders, signed copies), `formify-verify-identity` (BankID, ID scan, face liveness, company checks), `formify-pdf-forms` (fields in documents the user brings themselves), `formify-share-link` (one public signing link, with its cost question). `scripts/start.py` reports which companions are installed; where no code runs, look at the skill index the platform shows. If a companion is missing, say which one and that it is installed from the same package, and continue with what this skill can do on its own: `references/formify.md` covers the draft, the preview and the send question without the companions.

## Running on the user's own computer

Some platforms run the scripts on the user's own computer, not in a sandbox. The scripts therefore write only inside the working folder, never delete anything, make no network call except to mcp.formify.eu and to the official pages listed in `references/controls.json`, and never install anything. A renderer (Chrome, Chromium, Edge, WeasyPrint) is used only if it is already present; a browser is always started with its own temporary profile. When there is no Python at all, say so in one sentence and take route 1 or 3 of section 4.

## 1. The six documents

| # | Document | Template and guide (assets/templates/) | Default profile | Who signs |
|---|---|---|---|---|
| 1 | Nota de encargo y contrato de mediación (mandate) | `01_encargo.html`, `01_encargo.guide.md` | official in ES-IB, ES-CT, ES-VC; professional elsewhere | owners (ID scan), representative, optional spouse, agent |
| 2 | KYC identification forms, buyer and seller | `02_kyc_comprador.html`, `02_kyc_vendedor.html`, `02_kyc.guide.md` | official | the client; the document is scanned inside the form (box A, front scan plus a photo of the back) and the identity data are filled from it; box D on the last page is the agency's own verification and assessment record, filled in by hand after signing |
| 3 | Oferta de compra y documento de reserva | `03_reserva.html`, `03_reserva.guide.md` | professional (light on a phone) | buyer and agent first, then seller |
| 4 | Contrato de arras penitenciales | `04_arras.html`, `04_arras.guide.md` | professional | sellers and spouse (ID scan), buyers (ID scan), agency if escrow holder |
| 5 | Acuerdo de colaboración entre agencias | `05_colaboracion.html`, `05_colaboracion.guide.md` | professional | the two agents; the other agency may fill its own boxes when signing |
| 6 | Documento de entrega de llaves | `06_llaves.html`, `06_llaves.guide.md` | light | owners and agent |

Chains: reserva then arras; encargo then llaves; KYC before reserva or arras. When the user asks for one document in a chain, offer the next one at the end, once.

## 2. Every start: the document comes first

1. **Memory.** Look for `formify-memory.md` in the working folder and read it (`references/memory.md`). Everything it contains is known: never ask for it again. There is no set-up interview: the file starts almost empty and fills up as documents are made.
2. **Start.** Follow `references/first-run.md`: silent checks (memory, `get_current_user` if the Formify tools exist, `my-templates/`), then one message: on a first run three or four lines on what the skill is and that it works together with Formify (fields, signature fields, signing method and order, all the way to the signed copy), the offer to send all six documents to the user or save them as drafts, and the question "What do you want to do?" with the documents named in Spanish plus their meaning in parentheses in the user's language. On a first run the sample pack is option 1 and colaboración option 2; once the pack has been sent, colaboración is first and the pack last. When the question tool shows only four options, the fourth is "Show me the other documents I can produce". Nothing else is asked before the user has chosen. The start is the most important moment of the skill: `scripts/start.py` runs first on every run, the introduction and the sample pack offer follow on every first run, even when the user already said what they want.
3. **Sample pack.** If the user picks the samples, follow `references/sample-pack.md`: the six documents with example data, sent through the user's own Formify account to their own e-mail or saved as drafts there, no data asked. This is the fastest way to see the documents; offer it in the first message and as option 7.
4. **Agency and user details, on the way.** Each document type needs a few facts about the agency and the user. Ask only the missing ones, only for the document being made, before its own questions, one per message, with the Formify account and user as proposals; write each answer to the memory at once.

| Document | Agency and user details it needs |
|---|---|
| encargo | agency name, tax ID, address, e-mail, telephone; user name and e-mail; region (from the property); register number if the region has one; then the once-per-type offers (insurance, withdrawal) |
| KYC | agency name, tax ID, address; user name; data-protection e-mail (defaults to the agency e-mail, not asked) |
| reserva, arras | agency name, tax ID, address, e-mail; user name and e-mail; region; the deposit account (once per type) |
| colaboración | agency name, tax ID, address, e-mail; user name and e-mail; register number only if the user wants it in the contract (optional row) |
| llaves | agency name, address; user name and e-mail |

Signing method for clients (digital signature or face verification) is asked the first time a client is a signer; logo the first time a header is built; client languages are simply the language of the client in front of you. None of these is asked earlier.
5. **Not a policeman.** The skill knows what the law and the market templates contain, but the user decides what goes into their document. Never say that something is mandatory, never quote a law or a date in the chat, never explain registers, insurance amounts or civil-law variants, never describe what Formify or the account can or cannot do. Offer things as one short yes/no question ("Do you want to include the insurance details?"), accept the answer, move on. No disclaimer of any kind, in the chat or in a document: the skill never mentions AI, assistants, legal advice or lawyers.
6. **Region.** From memory once known; asked the first time a property is described and whenever the property is elsewhere. Read the matching row of `references/regions-table.md` before generating (index: `references/regions.md`): it decides the register line, the insurance block, the civil law variant (CC, CCCat in Cataluña, FN in Navarra), the family-home article, the tax on fees (IVA 21 %, IGIC 7 %, IPSI 4 %) and the co-official language. Every row was checked against primary sources on 2026-09-08; the table says what changed.
7. **Own templates.** If `my-templates/<template>` exists, that is the user's version and `fill.py` uses it by itself (`references/own-templates.md`). Any lasting change the user asks for goes there, never into `assets/templates/`.

## 3. The wizard

Ask one question per message, in the user's language, with the platform's question mechanism if it has one and otherwise in plain chat. Offer numbered options when the answer is a choice. Reuse every fact already given in the conversation: one property, one seller, one buyer feed all six documents. Never write a placeholder value and never invent a number, a name, a date or a registry detail; if it is missing, ask.

Order:
1. Which document (or which chain), from the question in section 2.
1b. The agency and user details this document type still lacks (table in section 2.4), then region if unknown or different.
3. Client's language for the second column (English, Swedish, Dutch, German are curated; any other language is generated with the same rules).
4. Style profile, only the first time a document of this type is made (then remembered per type; in the chat call them profesional, oficial, sencillo; the script flag is professional, official, light): 1 professional (agency letterhead, running clauses; the default), 2 official (structured like the Balearic official form; meaningful mainly for encargo and KYC), 3 light (a simplified version with few fields). Present them in that order.
5. The document-specific questions in the guide's "Preguntas mínimas" list, in that order, skipping anything known. Three of them are one-line offers, asked once per document type and remembered: encargo, "include the insurance and guarantee details?" and "include the withdrawal information? (recommended when the owner is a private person)"; reserva and arras, "which account does the money go to: the agency's client account or another account?".
5b. Counterparty details. When a document names a party the agency does not represent (the other agency in colaboración, the buyer or seller in reserva and arras, the owner in encargo and llaves, the client in KYC), ask once: "Do you have the other party's details, or should they fill them in themselves when signing?" If they fill them in, write those fields in `data.json` as form-field objects (section 4.1b) and ask only for the name and e-mail needed for the invitation. The client the document is about (the introduced client in colaboración, the property, the price) is always given by the user, never left as a field. Then one short question, "Anything else to add, for example a register number?", and no technical explanation of how fields work.
6. Signers, e-mail addresses and, where the guide says so, identity level. Signing methods offered: digital signature (drawn) and face verification; BankID only when a party is likely Swedish, with the note that it is activated by contacting Formify. Never say what the account allows.

Colaboración and llaves must be finished in five questions or fewer when the memory holds the agency data.

## 4. How a document is built

The document is fully described by its template in `assets/templates/` (the fixed text in both columns, the boxes, the `{{fields}}`, the optional and variant blocks) and its guide (which fields, which questions, who signs, which fields are form fields with which `tink-*` attributes). That description is the main path: it must be enough to produce the document wherever this skill runs. Produce it in this order, and say which route you used:

1. **A document-authoring capability this environment offers** (a PDF or document tool): build the document from the template text and the guide, set every form field with its kind, required flag and attributes explicitly (only names from `references/tink-attributes.md`), leave the signature areas as labelled empty space (`references/signatures.md`).
2. **Code execution is available**: run the scripts below. They give the exact PDF, the form fields, the signature coordinates and the style and law checks, and they are the tested reference for everything a document must look like. Prefer this route whenever it exists. When no renderer exists on the machine (no browser, no WeasyPrint, no wkhtmltopdf), `render_pdf.py` falls back by itself to a standard-library PDF (`scripts/stdlib_pdf.py`, the developer's rung 3 recipe): same text, same form fields, same signature areas, plain one-column layout, and writes the hand-over specification next to it. Say which route produced the file; never install a renderer.
3. **Neither, or the text needs characters the standard-library route cannot carry**: the hand-over, `scripts/handover.py` when code runs or written by hand in the same shape: the document text with `{{field}}` at each field, the field table (name, label, kind, required, options, read-only, page, anchor, size), the signature areas, and the one step that remains. The shape is the developer's own hand-over shape (the formify-pdf-forms skill) so that any assistant or colleague can finish it. That is a real deliverable; never end at "I cannot make a PDF here".

Route 2, step by step. Work in the user's working folder. All scripts use only the Python standard library.

1. Write `data.json` with every field the guide lists, in Spanish; for each `_tr` field, the same content in the client's language in legal register. Names, amounts and dates follow `references/terms.md` (numbers and dates section).
1b. Form fields for the other party: any field in `data.json` may be an object instead of a string, `{"field": "agencia_colaboradora_nif", "width": 90}` (name of the PDF field, width in pt; optional `"attributes": "tink-..."` for Formify attributes, `"height"` for a tall field, `"read_only": true` for scan buttons and images, `"required": false` when the signer may leave it empty). `fill.py` prints a blank line there and `render_pdf.py` turns it into a real PDF form field that the signer fills in Formify. Templates may also carry fixed fields in their HTML (the KYC identity box: an ID-scan button `tink-scan-id[1]` plus `tink-scanned-id-mrz-*[1]` fields that Formify fills from the scanned document); `fill.py` numbers all markers in order. `<title>.signatures.json` lists the fields created under `form_fields`; Formify picks them up from the uploaded file (`get_file_fields`), nothing else to configure.
2. `python3 scripts/fill.py --template assets/templates/<doc>.html --data data.json --out body.html [--optional a,b] [--variant CCCat|FN|NOEXCLUSIVA]`. The script removes unused optional blocks, activates the variant and lists any field left unfilled.
3. If the client's language is not English: `python3 scripts/translate.py extract body.html cells.json`, then edit the `text` field of every entry in `cells.json` (the right-hand cells, with their inner HTML kept intact, and the bilingual labels "Español / English", where only the English half changes, and the label halves `<span class="tr-lbl">/ English</span>` in the data boxes) with a translation of the Spanish text in that language, same register, same numbering, keeping the Spanish terms listed in `references/terms.md` with a gloss in parentheses on first use; then `python3 scripts/translate.py insert body.html cells.json body.html`. Never edit the right-hand cells by hand with search and replace: several contain nested tables and a partial replacement breaks the whole page layout. The Spanish column is never touched.
4. `python3 scripts/check_style.py body.html --doc <encargo|kyc|reserva|arras|colaboracion|llaves>`. Fix every warning before continuing; the checks are explained inside the script. Read `references/style-structure.md` and `references/style-drafting.md` once per session before writing any free text of your own (`references/style.md` is the index; `style-bilingual.md` when you translate) (party formulas, optional phrases, invitation text).
5. Take the temperature: `python3 scripts/check_law.py --doc <doc> [--region ES-xx]`. See section 6.
6. Write `signers.json` (list of `{"name","role","role_tr","id_scan"}` in signing order, per the guide; `role` in Spanish, `role_tr` its meaning in the client's language, printed small on its own line under it, and always the same term as the one used for that role in box A of the document: "VENDEDORA / Seller") and run `python3 scripts/render_pdf.py --html body.html --signers signers.json --out "<title>.pdf" --profile <official|professional|light> --title "<title>" --ref "<reference>"`. The script renders A4, places the signature areas right after the last paragraph following Formify's own rules in `references/signatures.md` (heading with the role above, white space below, nothing drawn, two per row, each row moves to the next page only if it does not fit) and the page footer and writes `<title>.signatures.json` with the exact Formify coordinates for every signer. Never hand-compute coordinates. `--signature-page` puts the signatures on a separate page instead; without pypdf the script falls back to that mode by itself.
7. Show the user the PDF (your file presentation tool) and a five-line summary of what it contains, and offer in one line to share the PDF with someone before it is sent (a colleague, the other party, the buyer's adviser) without saying why anyone would. Then continue with Formify (section 7).

Keep documents tight: no empty annex pages, no placeholder pages for photos or files. Annexes are the user's own PDFs merged after the document (see `references/formify.md`, 5b); images are not supported in this version.

Never edit the fixed Spanish clause text of a template in `assets/templates/`. Fields, optional blocks and variants are the moving parts for one document. When the user wants a lasting change (a clause added or removed, a wording of their own, a row taken out), it goes into their own copy in `my-templates/` following `references/own-templates.md`, in both columns, and is remembered; a one-off change for a single document is made in `body.html` and not saved.

## 5. Language and style rules

- Spanish is the master text and prevails in a dispute; every document says so. The second column is a legal translation, not an explanation; both columns keep the same register and numbering.
- No summary box. Every document opens with the data blocks (A. Partes, B. Operación or the equivalent): the parties side by side, then what the document is about, with bilingual labels and neutral values. The clauses that follow speak only of the roles ("la agencia titular", "la parte compradora", "el inmueble", "el cuadro B") and never repeat a value. When a counterparty's details are unknown, only their cells in block A (and the figures they must supply in block B) become form fields, each exactly once.
- No dashes as punctuation anywhere (a Formify house rule); split the sentence or use a colon. No wording that reads as generated text. No bold on stray words. The style checker enforces this.
- One typeface in every profile (sans-serif, Arial/Helvetica); the profiles differ in structure, not in type. Design: everything black and white, an administrative look. Black text, black rules, white paper; no colours, no grey or blue fills, no logo colours except in the agency's own logo image. `assets/base.css` carries this; do not add colour anywhere.
- Footer on every page, written by `render_pdf.py` into the page margin: line 1 the document title and reference (the agency's own reference, for example `LLA-2026-0004`: document type, year, running number); line 2 the fixed credit line in Spanish and in the client's language, no web address ("Elaborado con la solución de firma electrónica Formify.eu  ·  Prepared with the Formify.eu e-signing solution"). Two lines only. Pass `--lang xx` (en, sv, nl, de, fr, ca) or `--credit-tr "..."` for another language. The credit line names the Formify e-signing solution and nothing else: no "AI", no slogan; it is a fixed house line, not a disclaimer, and it is never expanded.
- No law text and no article citations inside a document, with these exceptions only: the words "arras penitenciales" with article 1454 CC (621-8 CCCat in Cataluña, ley 467 of the Fuero Nuevo in Navarra) in arras and reserva; the register number, insurer and guarantee in the mandate in regulated regions; the reference to Ley 10/2010 as the legal basis in the KYC forms; the family-home declaration with its article in arras; and the statutory withdrawal information and form in the mandate, which is reproduced verbatim from `references/withdrawal.md`.
- In Catalonia a consumer may ask for the document in Catalan: offer it, and then the second column is Catalan.
- Fee splits between agencies are never suggested by you or by the template; the parties state them (competition law, see guide 05).

## 6. Taking the temperature (freshness check)

The documents rest on a small set of legal provisions listed in `references/controls.json` with a key sentence from each and the date it was last verified. Before every document run `check_law.py`. It prints one line per control:
- UNCHANGED: nothing to do, and nothing to say to the user.
- REVIEW: the key sentence is no longer on the official page. Tell the user in one plain sentence, without article numbers or dates, that the rule behind a named clause seems to have changed since the template was checked and that they may want to read that clause before sending; then continue. Give the provision only if they ask.
- NOT CHECKED: the sandbox could not reach the site. Check the URL with your web tool yourself; if that fails too, say nothing unless the user asks whether the check ran.
Never stop the flow for the check.

## 7. Formify: preview, link, "send now?"

Follow `references/formify.md` exactly. The three rules the user cares about: the draft is always shown in the chat as the Formify-rendered preview with the signature fields drawn (never the source PDF); a link to the document in the Formify app is shown next to the preview whenever the API gives one; and the question "send now, save as draft, change signers, move a field, change the text" is always asked before anything is sent. The upload path follows the client, in the order `references/formify.md` gives (a file reference from the host, an https address, the staged curl command, base64 only as the last resort for a small file); a path that fails is named, never repeated. Invitation e-mails exist only in Spanish, English and Swedish; say so when the client speaks another language. The identification forms qualify for a Formify template and a public link (`references/templates-links.md`): offer the template once after the first KYC of a session, and the link only when the client fills the form alone; both need the user's yes, the link is billed.

If no Formify tools are available in this environment, deliver the PDF and `firmas.json` and say the document is ready to upload in Formify.

## 8. After the document

1. Ask: "Do you want me to save these settings as your default for this document type?" On yes, update `formify-memory.md` (format in `references/memory.md`). Only agency and user preferences are stored; never client data. If the user changed the text of the document, ask separately whether that change should apply to all future documents of this type (`references/own-templates.md`).
2. If the document is part of a chain, offer the next document once.
3. If a REVIEW result was reported, repeat the one-sentence warning in the closing message.

## 9. Things you never do

- Mention AI, assistants, disclaimers, legal advice or lawyers, in a document or in the chat. The only mention of Formify in a document is the fixed footer credit line.
- Tell the user what is mandatory, quote a law or a date, explain registers, insurance or civil-law variants, or describe what Formify or the account allows. Offer, ask, accept.
- Ask for the agent's own ID number, or the counterparty agent's. Agents act for their agency: name plus the agency's tax ID. The only exception is colaboración, where the user is asked once whether the agents' ID documents should appear in the contract (remembered as `documento_agente`); only if they say yes are the documents asked for and printed.
- Invent registry details, cadastral references, policy numbers, prices or dates.
- Write alarm codes, passwords or door codes into any document.
- Store client data in the memory file.
- Suggest cash payments, or a fee split between agencies.
- Remove the "arras penitenciales" wording from arras. (The withdrawal block in a mandate is offered and recommended; the user decides.)
- Calculate an amount (a fee from a price, VAT, a share) or repeat a figure outside its box; print percentages, amounts and terms exactly as given, once, and let the clauses refer to the box.
- Add a date field next to a signature: Formify stamps the date and time of each signature.
- Print a placeholder text in a cell that is meant to be a field, or the same value twice; a field sits in its cell, once, required unless the guide says otherwise.
- Use paper wording ("signed in duplicate", "en dos ejemplares"); the closing line is the template's.
- Give the signature captions a translation other than the one used for the same role in the data boxes.
- Send anything through Formify without the preview step and the user's explicit "send now".
- Show a docs-api download URL to the user, or call `get_draft_file`.

## 10. File map

```
SKILL.md                      this file
README.md                     short description for catalogues
agents/openai.yaml            display name, default prompt and the Formify MCP dependency (Codex, ChatGPT)
references/regions.md        index; regions-table.md (the row per region), regions-encargo.md (what encargo and arras take from it)
references/regions-table.md  region table checked row by row (2026-09-08): registers, insurance, civil law variants, tax, language, default profile
references/style.md          index; style-structure.md, style-drafting.md, style-bilingual.md: Spanish drafting style, both columns
references/terms.md        terms that stay in Spanish, glosses in en, sv, nl, de; number and date formats
references/controls.json     legal provisions, key sentences, URLs, what to review if changed
references/withdrawal.md   statutory withdrawal information and form, verbatim, with adaptation notes
references/formify.md         upload, draft, preview, send, archive
references/signatures.md          Formify's signature area rules (dimensions, spacing, heading pattern) and how the renderer applies them
references/memory.md         memory file format and rules
references/first-run.md          every start: silent checks, the one opening question, details collected on the way
references/sample-pack.md         the sample pack: six documents sent to the user's own e-mail through Formify
references/own-templates.md         the user's own templates in my-templates/: how changes are kept and carried over
references/id-scan.md          the ID-scan pattern used in the KYC forms: scan trigger required, MRZ fields filled by Formify
references/attachments.md      the upload row for files the counterparty supplies (receipts, the back of an ID document)
references/templates-links.md  Formify templates and public links for the identification forms: opt-in, remembered in formify-memory.md
references/formify-errors.md   which Formify errors heal with one retry and which need a reconnect
references/kyc-pattern.md      the identification-form pattern: scan, back photo, declarations, the agency's box D
references/tink-attributes.md  the complete catalogue of Formify's tink-* field attributes (the developer's file, mirrored)
assets/base.css               layout, the three profiles, signature page
assets/templates/            six templates with their guides (boxes A, B… on top, clauses below)
assets/samples/               example data and signers for every document (sample pack and tests)
assets/welcome.txt            the welcome lines printed by start.py on every run
scripts/start.py             step 0: welcome lines, companion skills, platform and renderer, memory file
scripts/fill.py           fills a template (or the user's own copy) from data.json, handles optional blocks and variants
scripts/sample_pack.py            renders the sample pack and writes sample_pack.json for sending
scripts/translate.py           extracts the translatable cells and labels to JSON and puts the translations back
scripts/check_style.py   style and safety checks on the HTML
scripts/check_law.py      freshness check against the official sources
scripts/render_pdf.py         HTML to A4 PDF, signature page, <title>.signatures.json with Formify coordinates; falls back to stdlib_pdf.py
scripts/stdlib_pdf.py         route 3: fillable PDF from the standard library alone (plain layout, same text, fields and signature areas)
scripts/handover.py           route 5: the hand-over, document text plus field specification, in the developer's fixed shape
tests/                        run_all.py and documents.json: builds every document from assets/samples and checks it
```

## Network

Every outbound call this skill makes, and nothing else: law_check: the official URLs in references/controls.json (BOE and regional gazettes; read only, at document time); formify: https://mcp.formify.eu (MCP tools) and the presigned upload URL from request_file_upload_url (curl PUT); other: none. No hooks, no telemetry.
