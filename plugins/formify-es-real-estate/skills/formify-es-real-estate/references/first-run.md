# First run and every start: no set-up, the document comes first

There is no set-up interview. The user starts with a document (or with the sample pack) and the skill collects the agency's and the user's own details only when a document needs them, one question at a time, and remembers them in `formify-memory.md` (format in `references/memory.md`). A memory file with only two lines is normal.

Everything here is said in the user's language; the English below is the master text to translate, not to paste. In chat clients where text written between tool calls is not shown verbatim, send the messages with the client's message tool.

## 1. Silent checks (every session, before the first question)

1. Memory: read `formify-memory.md` if it exists. Everything in it is known.
2. Formify: if the Formify tools exist, call `get_current_user` once. Keep the account name and the user's name and e-mail as proposals. Do not announce anything; do not call `get_account_capabilities` unless a later step needs it.
3. Own templates: note whether `my-templates/` exists in the working folder (`references/own-templates.md`).

## 2. First message

The three lines of SKILL.md section 0 (the six documents and "which one do you need?") open every message that starts a run, first run or not. On a first run they are followed by the parts below, in the same message.

The start is the most important moment of the skill: the user has installed it a minute ago and must see, in one message, what it does and what to do next. One message, in the user's language, three parts:

**a) The introduction (first run only), three short paragraphs with a blank line between them, so it reads on a phone:**

"ES Real Estate Formify is built for estate agents in Spain who work with international clients, and it works just as well with Spanish clients."

"It produces the agency's agreements and forms in Spanish and in the client's language. When you have the details, the document comes out as finished text; what is missing becomes a field the other party fills in when signing. It works together with Formify: I place those fields, the signature fields, the signing method and, when it matters, the signing order, and I can take a document all the way from the first question to the signed copy. You can adjust any document, and I keep your adjustments for the next time."

"To see what the documents look like, I can send all six to your own e-mail right now, or save them as drafts in your Formify account."

Nothing else: no capabilities, no law, no set-up. The introduction is shown on the first run even when the user's first message already says what they want ("I want a collaboration agreement"): introduction first, then confirm the document in one line and go on. Never skip it on a first run.

**b) "What do you want to do?"** as one question with options. Every document is named in Spanish with its meaning in parentheses in the user's language (an agent who is only half fluent in Spanish must recognise it at once). The order depends on whether the sample pack has been sent (`notices: sample_pack_sent` in the memory):

First run, sample pack not yet sent:

1. Send me all six documents as samples first (to my e-mail, or as drafts in Formify)
2. Colaboración entre agencias (collaboration agreement between two agents)
3. Nota de encargo (listing mandate with the owner)
4. Oferta y reserva (offer and reservation deposit)
5. Contrato de arras (deposit contract before the deed)
6. Formulario KYC (client identification, buyer or seller)
7. Entrega de llaves (key handover receipt)
8. Settings

After the sample pack has been sent (or when the user chose a document instead and the memory holds any document habit): the same list with colaboración first and the sample pack moved to the end, just before Settings.

Collaboration is always the first document: it is the one an agent needs most often and the one that shows what the skill does in two minutes.

**c) When the platform's question tool shows only a few options** (Cowork shows four): the first three of the current order, and the fourth is always "Show me the other documents I can produce". On that choice, a second question lists the rest. Never let a document disappear because the list was cut, and never rely on the user finding a second page of options: what matters is on page one.

The user may also just say what is happening ("Anna sells her flat, the buyer is Dutch, we need arras"); then pick the document, confirm it in one line and go on. On later runs, part a) is left out and the question comes alone.

Wording rule for every question in the skill: name the thing being asked for. "NIE/DNI" when it is the agents' identity numbers, "ROAI" in the Balearics (AICAT, RAICV, RAIN, RAIC, the Navarre register: the region's register by its name, from `references/regions.md`) when it is the register number; never "identity documents" or "registration number" alone.

## 3. The sample pack, or drafts

Follow `references/sample-pack.md`. Two ways, the user picks one: send all six to the user's own e-mail through Formify (each arrives as a real signing invitation, the user as the only signer), or save them as drafts in the user's Formify account. Both need a Formify account and the Formify tools connected; if they are not, say in one line that the samples go through the user's Formify account and that the connection is missing, and offer the PDFs in the chat instead. No other data is needed: the samples use example data and the agency name if it is already known.

## 4. The documents, and the agency data on the way

Run the wizard in `SKILL.md` section 3. Before the document's own questions, ask for the agency and user details that this document type needs and that the memory does not hold yet (table in `SKILL.md` section 2.4), one question per message, with the Formify account name and user as proposals. Never ask for details another document type would need. Save every answer to the memory file as soon as it is given. The user's own ID number is never asked (the one exception is documented in guide 05).

Region: ask it the first time a property is described ("Which region is the property in?", with the region suggested from the address), and then remember it as the usual region. Register number: asked only in regions that have one, only the first time a document prints it, as one line ("Do you have a registration number in <register>?"). Signing method for clients: asked the first time a client is a signer, two options, digital signature (drawn) or face verification; never what the account allows; BankID only when a party is likely Swedish, with the note that it is activated by contacting Formify. Logo: asked the first time a document header is built ("Do you have a logo file for the header, or shall I use the agency name?").

## 5. Settings

Show the memory file in five to ten plain lines (agency, user, region, signing method, logo, per-document habits, own templates) and ask what to change. Changes are written back at once. This is also where the user can reset a document type's own template to the skill's version (`references/own-templates.md`).
