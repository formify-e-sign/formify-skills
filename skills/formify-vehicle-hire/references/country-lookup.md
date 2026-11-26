# Looking up a country that has no verified file

Use this when `countries/<cc>.md` does not exist and the web can be searched. The result is used for
one conversation and is always labelled as looked up today and not reviewed by Formify.

## Method

1. **Find the national law that transposes the EU act.** Open the national transposition measures
   page for the directive (section "EU tools") and take the name and number of the country's law.
   For this skill the acts are Directive 2011/83/EU (consumer rights) and Directive 93/13/EEC (unfair
   terms).
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

Common to every country:

1. Which country and, where relevant, which region or Land?
2. Which language must the document be in, and must a foreign-language version be offered?
3. Does any of these documents need handwriting, a qualified electronic signature, a notary or a
   registration?
4. Which national law transposes each directive, and does the country use stricter consumer
   protection for unfair terms?

Specific to vehicle hire:

5. Is the withdrawal exemption for car rental with a fixed date or period transposed as it stands?
   Is there a statutory right to cancel or to change the booking before pick-up?
6. Minimum age, minimum years of licence held, young-driver or senior-driver limits, and whether
   foreign licences, non-EU licences or an international driving permit are accepted.
7. Must the lessor check and record the licence, and may a copy be made? What is the data
   protection authority's position?
8. Deposit and card-hold rules, limits on excess or damage charges, accepted means of payment and
   fee caps.
9. Compulsory insurance, and what the contract must disclose about excess, waivers and third-party
   cover; restrictions on taking the vehicle abroad.
10. Fines and tolls: the legal basis for passing driver data to authorities and for administration
    fees.
11. Who is liable for traffic offences, the lessor or the hirer, and must the hirer declare the
    driver?
12. Is there a national list of unfair terms, for example on damage, fuel or cancellation, and
    mandatory contract language?
13. Is a signed handover protocol, photographs or an inspection record required or customary?

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
| National laws transposing the consumer rights directive | https://eur-lex.europa.eu/legal-content/EN/NIM/?uri=CELEX:32011L0083 |
| The same for another directive: replace the number | `https://eur-lex.europa.eu/legal-content/EN/NIM/?uri=CELEX:<number>` |
| Search national law from one place | https://n-lex.europa.eu |
| Country pages on national law | https://e-justice.europa.eu |
| Plain-language summary: withdrawal rights | https://europa.eu/youreurope/citizens/consumers/shopping/returns/index_en.htm |
| Plain-language summary: selling off-premises | https://europa.eu/youreurope/business/selling-in-eu/selling-goods-services/ecommerce-distance-selling/index_en.htm |
| Plain-language summary: car rental abroad | https://europa.eu/youreurope/citizens/travel/driving-abroad/car-rental-abroad/index_en.htm |
| Commission page on the car-rental commitments | https://commission.europa.eu/topics/consumers/consumer-rights-and-complaints/enforcement-consumer-protection/coordinated-actions/other-travel-services_en |
| European Data Protection Board | https://www.edpb.europa.eu |

The EUR-Lex pages need a browser; a plain fetch gets an empty answer. The consolidated text of an
EU act can be read without one at `http://publications.europa.eu/resource/celex/<consolidated
number>`; the exact addresses used for this skill are in `controls.json`. The Commission page
answers some automated readers with an error; open it in a browser.

## How to say it

One or two sentences, once, before the first document:

> I looked up <country>'s rules just now. The rules on the contract and the data come from <law,
> article> on <portal> (link), read today. Formify has not reviewed these, so treat them as a
> careful first reading. I could not find <open question>.

Then use the rules in the document without repeating the caveat on every line.
