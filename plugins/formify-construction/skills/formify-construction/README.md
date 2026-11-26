# Formify Construction (formify-construction)

An agent skill for builders, renovation firms and tradespeople who work for private clients anywhere in the EU. It prepares the six documents such a job needs and gets them ready for e-signature through [Formify](https://formify.eu):

1. Quote, with accept and decline boxes
2. Works contract
3. Withdrawal information and the model withdrawal form, word for word from the official EU text
4. Variation order for extra or changed work
5. Handover record
6. Warranty note

What makes it different: it always asks which country the works are in. For a country with a verified file (Spain today) it applies that file. For any other EU country it looks the rules up on the official legislation portal, quotes the source with a link and a date, and says plainly that the result was looked up and not reviewed. With no web access it applies the rules common to all EU countries and says so.

## Compatibility

Follows the open Agent Skills format (`SKILL.md` plus `references/` and `agents/`). No scripts, nothing to install. Building the PDF, sending it and tracking signatures are done by the Formify core skills shipped in the same plugin; signing needs the Formify MCP server.

## Install

From the Formify marketplace (`formify-e-sign/formify-skills`), install the **Formify for Construction** plugin (`formify-construction@formify`). It is opt-in: installing the core Formify plugin never pulls this skill.

## Legal note

The rules in this skill were read on the official EU and Spanish texts in November 2026 and carry their sources. They are not legal advice. Review the documents under your own guidelines and involve a lawyer where needed.

MIT licence.
