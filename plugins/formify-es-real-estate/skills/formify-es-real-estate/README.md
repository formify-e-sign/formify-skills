# ES Real Estate Formify (formify-es-real-estate)

An agent skill for estate agents in Spain who serve international clients; it works just as well for Spanish clients. It produces the six documents an agency signs most often, bilingual (Spanish master text plus the client's language, both in legal register), adapted to the autonomous community (all 17 plus Ceuta and Melilla, checked region by region against the official texts in September 2026), and sends them for identification and e-signature through [Formify](https://formify.eu).

1. Nota de encargo y contrato de mediación (mandate), with the statutory withdrawal information most templates forget
2. KYC identification forms for buyer and seller (Ley 10/2010 today, EU Regulation 2024/1624 fields from 2027)
3. Oferta de compra y documento de reserva, with the seller's acceptance in the same document
4. Contrato de arras penitenciales (Código Civil and Codi civil de Catalunya variants)
5. Acuerdo de colaboración between two agencies, one property, one client, signable from a phone
6. Documento de entrega de llaves

What makes it different: no set-up, you start with a document and the skill asks only what it does not know yet (and can send you all six documents as samples first), a memory file for the agency's own data and habits, a freshness check that reads the official text of every provision the documents rely on and warns when it changed, the parties and the deal in clear boxes on top of every document with the clauses below, the client's ID document scanned inside the KYC form with the identity data filled from it, a style checker that removes the tells of generated text, and a fixed signature page that gives Formify exact coordinates.

## Compatibility

Follows the open Agent Skills format (`SKILL.md` plus `scripts/`, `references/`, `assets/`, `agents/`). Works in any agent: with a document tool or code execution it produces the finished PDF (the scripts need only Python 3 and Chromium, WeasyPrint or wkhtmltopdf, whichever is installed); without either it hands over the document text and a complete field specification. Signing needs the Formify MCP server (Claude, Codex, ChatGPT, Cursor, Gemini CLI, Manus and others).

## Install

From the Formify marketplace (`formify-e-sign/formify-skills`), install the **Formify Spanish Real Estate** plugin (`formify-es-real-estate@formify`). It is opt-in: installing the core Formify plugin never pulls this skill.

Or copy this folder into your agent's skills directory (for example `~/.claude/skills/formify-es-real-estate`) and connect the Formify MCP server. Then say what you need, or ask for the sample pack first: "arras para el piso de Calle Mayor, comprador holandés".

## Legal note

The documents are built from a reference library of public Spanish models and verified statutory texts (September 2026), but they are not legal advice. Review them under your own guidelines and involve a lawyer where needed. Instructions and guides are in English; the documents are in Spanish plus the client's language.

MIT licence.
