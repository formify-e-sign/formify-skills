# Formify Subcontracting (formify-subcontracting)

An agent skill for main contractors and their subcontractors working on a private construction or renovation site anywhere in the EU. It prepares the five documents two businesses exchange and gets them ready for e-signature through [Formify](https://formify.eu):

1. Subcontract, with scope tied to the main works, price and payment terms as the parties state them, time, site rules, insurance and further subcontracting
2. Variation order between the two businesses
3. Completion and acceptance record for the subcontracted part
4. Payment confirmation, either the subcontractor confirming an amount received for a stage or the contractor certifying an amount due
5. Compliance checklist of the certificates the country asks the contractor to collect before the subcontractor starts, which the subcontractor confirms it has supplied

What makes it different: it always asks which country the site is in. For a country with a verified file (Spain today) it applies that file. For any other EU country it looks the rules up on the official legislation portal, quotes the source with a link and a date, and says plainly that the result was looked up and not reviewed. With no web access it applies the rules common to all EU countries and says so. It never suggests a price or a payment period; it prints what the parties state and says once when a period is longer than EU law allows without express agreement.

It does not produce the site subcontracting register, approvals or reports to labour authorities, posting declarations, public procurement documents or documents signed by the technical professions. Contracts with a private client belong to `formify-construction`.

## Compatibility

Follows the open Agent Skills format (`SKILL.md` plus `references/` and `agents/`). No scripts, nothing to install. Building the PDF, sending it and tracking signatures are done by the Formify core skills shipped in the same plugin; signing needs the Formify MCP server.

## Install

From the Formify marketplace (`formify-e-sign/formify-skills`), install the **Formify for Construction** plugin (`formify-construction@formify`). It is opt-in: installing the core Formify plugin never pulls this skill.

## Legal note

The rules in this skill were read on the official EU and Spanish texts in November 2026 and carry their sources. They are not legal advice. Review the documents under your own guidelines and involve a lawyer where needed.

MIT licence.
