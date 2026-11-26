# Looking up a country that has no verified file

Use this when `countries/<cc>.md` does not exist and the web can be searched. The result is used for
one conversation and is always labelled as looked up today and not reviewed by Formify.

## Method

1. **Find the national law.** The guest duty comes from art. 45 of the Schengen Convention, which is
   not a directive, so the EUR-Lex national transposition pages do not list it, and Regulation (EU)
   2024/1028 is a regulation, which has none either. Search the country's portal (table below), in the
   country's language, for the law or decree on the register of guests or travellers in
   accommodation, and for the tourism or police rules that name the form.
2. **Read that law in the consolidated version in force today.** Search inside the text for the terms
   of the question.
3. **Answer each question in "Questions" with a quote.** Keep, for every answer: the law and
   article, the sentence, the address of the page, today's date.
4. **Check for scheduled changes** on the same page and give both versions with their dates when one
   is found.
5. **Report what was not found.** A question with no official answer stays open; apply the EU
   baseline for it and tell the user that point was not found.

What counts as a source: the official gazette or legislation portal, a ministry, police or regulator
page, the EU pages below. What does not: law-firm articles, blogs, vendor pages, comparison sites,
forums, machine-generated answers. They may help find the name of the law; the quote comes from the official text.
Filing systems such as SES.Hospedajes (Spain), eVisitor (Croatia) or Alloggiati Web (Italy) are named
as examples of the separate filing; whether and how a country requires one is a question below.

Regional law exists in Austria, Belgium, Germany, Italy and Spain, and accommodation registration is
often regional. Ask for the region or Land and say when regional rules were not checked.

## Questions

1. Which country and, where relevant, which region or Land? Which language must the document be in?
   Is a qualified electronic signature, handwriting, a notary or a registration needed for this
   document type?
2. Does the country apply art. 45 of the Schengen Convention, and is the duty extended to its own
   nationals, to children, to every guest?
3. Exact data fields the form must contain (name, birth date, nationality, document number, address,
   dates of stay, companions, signature) and who may sign for a group or for minors.
4. Is an electronic or paperless registration, or an electronic signature, accepted, or is paper
   mandatory?
5. Is a copy or photo of the ID document allowed, tolerated or forbidden (national data protection
   authority position)? May the document number be recorded?
6. Retention period, and the deadline and channel for sending the data to the police or the
   statistical office (online portal, daily or weekly).
7. Which accommodation types are covered (hotels, apartments, private rooms, campsites, boats) and
   the threshold for private hosts.
8. Any tourist tax or city tax declaration tied to the same form.
9. Short-term rental registration number under Regulation (EU) 2024/1028: does the country or city
   require one, in which register, with what penalties?
10. Language of the form, and whether a foreign-language version must be offered.

## Official portal per country

| Code | Country | Language | Portal | Address |
|---|---|---|---|---|
| AT | Austria | de | RIS | https://www.ris.bka.gv.at |
| BE | Belgium | nl, fr, de | Belgisch Staatsblad / Moniteur belge | https://www.ejustice.just.fgov.be/cgi/welcome.pl |
| BG | Bulgaria | bg | State Gazette | https://dv.parliament.bg |
| HR | Croatia | hr | Narodne novine | https://narodne-novine.nn.hr |
| CY | Cyprus | el | CyLaw (free database, not the gazette) | https://www.cylaw.org |
| CZ | Czechia | cs | e-Sbírka | https://e-sbirka.gov.cz |
| DK | Denmark | da | Retsinformation | https://www.retsinformation.dk |
| EE | Estonia | et | Riigi Teataja | https://www.riigiteataja.ee |
| FI | Finland | fi, sv | Finlex | https://www.finlex.fi |
| FR | France | fr | Légifrance | https://www.legifrance.gouv.fr |
| DE | Germany | de | Gesetze im Internet | https://www.gesetze-im-internet.de |
| GR | Greece | el | Government Gazette | https://www.et.gr |
| HU | Hungary | hu | Magyar Közlöny | https://magyarkozlony.hu |
| IE | Ireland | en, ga | Irish Statute Book | https://www.irishstatutebook.ie |
| IT | Italy | it | Normattiva | https://www.normattiva.it |
| LV | Latvia | lv | likumi.lv | https://likumi.lv |
| LT | Lithuania | lt | Teisės aktų registras | https://www.e-tar.lt |
| LU | Luxembourg | fr, de, lb | Legilux | https://legilux.public.lu |
| MT | Malta | mt, en | Laws of Malta | https://legislation.mt |
| NL | Netherlands | nl | wetten.overheid.nl | https://wetten.overheid.nl |
| PL | Poland | pl | ISAP | https://isap.sejm.gov.pl |
| PT | Portugal | pt | Diário da República | https://diariodarepublica.pt |
| RO | Romania | ro | Monitorul Oficial | https://monitoruloficial.ro |
| SK | Slovakia | sk | Slov-Lex | https://www.slov-lex.sk |
| SI | Slovenia | sl | PISRS | https://pisrs.si |
| ES | Spain | es | BOE | https://www.boe.es |
| SE | Sweden | sv | Svensk författningssamling | https://svenskforfattningssamling.se |

Every address was opened on 2026-11-26. The portals of France, Lithuania and Sweden refuse some
automated readers; when a page will not load, search for the law by name and number and open the
official result, or ask the user to paste the article.

## EU tools

| Purpose | Address |
|---|---|
| Search national law from one place | https://n-lex.europa.eu |
| Country pages on national law | https://e-justice.europa.eu |
| An EU act by ELI | `https://eur-lex.europa.eu/eli/<type>/<year>/<number>/oj/eng` (needs a browser) |
| An EU act as text, without a browser | `http://publications.europa.eu/resource/celex/<CELEX number>` |
| Data protection authorities and guidance | https://www.edpb.europa.eu |

The EUR-Lex pages need a browser; a plain fetch gets an empty answer. The Publications Office address
above serves the same text. Acts used here: Schengen Convention `42000A0922(02)`, GDPR
`02016R0679-20160504`, Regulation 2024/1028 `32024R1028`, eIDAS `02014R0910-20241018`.

## How to say it

One or two sentences, once, before the first document:

> I looked up <country>'s rules just now. The guest data fields and the retention come from <law,
> article> on <portal> (link), read on the date you state. Formify has not reviewed these, so treat them as a careful
> first reading. I could not find <open question>.

Then use the rules in the document without repeating the caveat on every line.
