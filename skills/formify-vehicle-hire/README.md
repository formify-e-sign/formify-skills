# Formify Vehicle Hire (formify-vehicle-hire)

An agent skill for small car, van, camper, motorcycle and scooter rental firms anywhere in the EU. It prepares the three documents a rental needs and gets them ready for e-signature through [Formify](https://formify.eu):

1. Rental agreement, with the full price information, the deposit, and every add-on (insurance waiver, second driver, child seat, fuel option) as a box the renter ticks and never pre-ticked
2. Handover record at pick-up: condition, fuel or charge level, mileage, existing damage, accessories, with the renter's acknowledgement
3. Return record: the same items at return, new damage accepted or disputed, and the final charges

What makes it different: it always asks which country you operate in. For a country with a verified file (Spain today, including the closed list of data that Real Decreto 933/2021 asks the hire record to hold) it applies that file. For any other EU country it looks the rules up on the official legislation portal, quotes the source with a link and a date, and says plainly that the result was looked up and not reviewed. With no web access it applies the rules common to all EU countries and says so. The agreement states that a booking with a fixed date or period has no right of withdrawal, where that EU rule applies.

Renter identity and licence data are captured as data fields, not as a picture of the document, unless your country requires the picture.

Not covered: reporting renter data to the police platform (a separate act), insurance policies, traffic fines, leasing and long-term finance, and peer-to-peer rental platforms.

## Compatibility

Follows the open Agent Skills format (`SKILL.md` plus `references/` and `agents/`). No scripts, nothing to install. Building the PDF, sending it and tracking signatures are done by the Formify core skills shipped in the same plugin; signing needs the Formify MCP server.

## Install

From the Formify marketplace (`formify-e-sign/formify-skills`), install the **Formify for Tourism** plugin (`formify-tourism@formify`). It is opt-in: installing the core Formify plugin never pulls this skill.

## Legal note

The rules in this skill were read on the official EU and Spanish texts in November 2026 and carry their sources. They are not legal advice. Review the documents under your own guidelines and involve a lawyer where needed.

MIT licence.
