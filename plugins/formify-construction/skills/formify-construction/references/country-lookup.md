# Looking up a country that has no verified file

Use this when `countries/<cc>.md` does not exist and the web can be searched. The result is used for
one conversation and is always labelled as looked up today and not reviewed by Formify.

## Method

1. **Find the national law that transposes the EU act.** Open the national transposition measures
   page for the directive (section "EU tools") and take the name and number of the country's law.
2. **Read that law on the country's official portal** (table below), in the consolidated version
   in force today. Search inside the text for the terms of the question, in the country's language.
3. **Answer each question in "Questions" with a quote.** Keep, for every answer: the law and
   article, the sentence, the address of the page, today's date.
4. **Check for scheduled changes** on the same page (a consolidated text usually marks future
   versions). Give both versions with their dates when one is found.
5. **Report what was not found.** A question with no official answer stays open; apply the EU
   baseline for it and tell the user that point was not found.

What counts as a source: the official gazette or legislation portal, a ministry or regulator page,
the EU pages below. What does not: law-firm articles, blogs, comparison sites, forums, machine-generated answers.
They may help find the name of the law; the quote comes from the official text.

Regional law exists in Austria, Belgium, Germany, Italy and Spain. Ask for the region or Land and
say when regional rules were not checked.

## Questions

1. How does the country draw the line for "substantial conversion", which falls outside the
   consumer withdrawal rules?
2. Is the withdrawal period 30 days for contracts made during an unsolicited visit to the home?
3. May the contractor take payment or a deposit during the withdrawal period? Is there a limit on
   deposits or a statutory payment schedule?
4. Does the lighter regime for small repairs (up to EUR 200) apply, and the exemption for small
   off-premises contracts (EUR 50 or less)?
5. Must a building or works contract with a consumer be in writing, and what must it contain
   (price, completion date, plans, permits)? Is there a statutory consumer building-contract law or
   mandatory standard terms?
6. Must a written quote be given before the works, with what content, and can the client waive it?
7. Which language must the contract be in?
8. Acceptance: is there a statutory handover procedure, and is acceptance presumed after a period?
9. Warranty and liability periods for defects in the works, and from when they run.
10. Must the contractor hold a licence, registration or insurance that the contract has to state?
11. Reduced tax rate for housing renovation: does it exist, on what conditions, and what does the
    client sign?
12. Does any of these documents need handwriting, a qualified electronic signature or a notary?
13. Does the country publish its own version of the withdrawal information and form, and where?

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

The addresses were checked on 2026-11-26. The portals of France, Lithuania and Sweden refuse some
automated readers; when a page will not load, search for the law by name and number and open the
official result, or ask the user to paste the article.

## EU tools

| Purpose | Address |
|---|---|
| National laws transposing the consumer rights directive | https://eur-lex.europa.eu/legal-content/EN/NIM/?uri=CELEX:32011L0083 |
| The same for another directive: replace the number | `https://eur-lex.europa.eu/legal-content/EN/NIM/?uri=CELEX:<number>` |
| Search national law from one place | https://n-lex.europa.eu |
| Country pages on national law | https://e-justice.europa.eu |
| Plain-language summary: withdrawal rights | https://europa.eu/youreurope/citizens/consumers/shopping/returns/index_en.htm |
| Plain-language summary: selling off-premises | https://europa.eu/youreurope/business/selling-in-eu/selling-goods-services/ecommerce-distance-selling/index_en.htm |

The EUR-Lex pages need a browser; a plain fetch gets an empty answer. The consolidated text of an
EU act can be read without one at `http://publications.europa.eu/resource/celex/<consolidated
number>` (see `withdrawal-form.md`).

## How to say it

One or two sentences, once, before the first document:

> I looked up <country>'s rules just now. The withdrawal period and the quote rules come from
> <law, article> on <portal> (link), read today. Formify has not reviewed these, so treat them as a
> careful first reading. I could not find <open question>.

Then use the rules in the document without repeating the caveat on every line.
