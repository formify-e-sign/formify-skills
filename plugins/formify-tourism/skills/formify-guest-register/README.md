# Formify Guest Register (formify-guest-register)

An agent skill for hosts, small hotels, hostels, campsites and property managers anywhere in the EU. It prepares the papers needed at check-in and gets them ready for e-signature through [Formify](https://formify.eu):

1. Guest registration form, one per guest who must sign
2. House rules acknowledgement
3. Property-manager mandate, so an owner can authorise a manager to register guests and run check-in

What makes it different: it always asks which country the property is in. For a country with a verified file (Spain today) it applies that file, including the closed list of data fields and who must sign. For any other EU country it looks the rules up on the official legislation portal, quotes the source with a link and a date, and says plainly that the result was looked up and not reviewed. With no web access it applies the rules common to all EU countries and says so.

The registration form can be published as one reusable signing link, for example behind a QR code at the door, through the Formify share-link skill. By default the form captures the identity data without keeping a picture of the ID document.

## What it does not do

It does not file guest data with the police or a statistics platform, prepare tourist tax returns, handle short-term-rental registration numbers, or draft tenancy agreements.

## Compatibility

Follows the open Agent Skills format (`SKILL.md` plus `references/` and `agents/`). No scripts, nothing to install. Building the PDF, sending it and tracking signatures are done by the Formify core skills shipped in the same plugin; signing needs the Formify MCP server.

## Install

From the Formify marketplace (`formify-e-sign/formify-skills`), install the **Formify for Tourism** plugin (`formify-tourism@formify`). It is opt-in: installing the core Formify plugin never pulls this skill.

## Legal note

The rules in this skill were read on the official EU and Spanish texts in November 2026 and carry their sources. They are not legal advice. Review the documents under your own guidelines and involve a lawyer where needed.

MIT licence.
