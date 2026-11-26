# Spain (ES): vehicle hire

Verified pack. Every row was read on the official consolidated text of Real Decreto 933/2021 on
2026-11-26 (last update of the consolidated text 2025-12-20, no amendment since publication); the
links and the sentences to re-check are in `../controls.json`. The Interior FAQ quoted below is the
version updated on 10 August 2026, read from a local copy.

Language of the document: Spanish as master text, with the renter's language as a second column.
The rule that the information be at least in Spanish was read only for contracts concluded away from
the business premises (TRLGDCU art. 99.1); for a contract signed at the counter it was not checked.

## 1. Who is covered

| Situation | Result | Source |
|---|---|---|
| Hire of motor vehicles without driver, for a fixed time and for a price, by a rental firm | Covered | RD 933/2021 art. 2.2 |
| Tour operators that intermediate between rental firms and consumers, and digital platforms | Covered | RD 933/2021 art. 2.2 |
| Taxis and, in general, hire of vehicles with a driver | Excluded | RD 933/2021 art. 2.2 |
| Scooters, quads and e-scooters | Not checked whether they are "vehículos a motor" for this decree | |

The decree obliges "las personas físicas o jurídicas que desarrollen o intermedien" in the
activity (art. 2.3), whatever the legal form (art. 3). The firm is responsible for the accuracy of
the data, which must match the documents that prove the identity of the persons, shown by the users
(art. 4.3).

## 2. The hoja de servicios and the signature

Art. 4.2, second paragraph: «Igualmente, las personas arrendadoras deberán firmar las hojas de los
servicios en las actividades de alquiler de vehículos conforme al sistema y modelo que se
establezca.»

Two points. The literal word is "arrendadoras", which means lessors, while Annex II calls the
customer "arrendatario". Nothing in the text excludes either reading. Build the documents so that
the renter signs and keep the firm's own signature field, which is what `../documents.md` already
does. Second, the decree names no type of signature and delegates to "el sistema y modelo que se
establezca". No Interior model of the sheet was found. Never say that Interior accepts an electronic
signature on it.

What the sources do support: the register of the firm is electronic (art. 5.1), and Interior's FAQ
says «Los establecimientos pueden recabar la información mediante cualquier sistema que permita la
verificación de la exactitud de los datos, incluso sin que sea necesaria su presencia física y siempre
que se trate de un sistema compatible con el cumplimiento de la normativa vigente, especialmente en
materia de protección de datos.» Say that, and no more.

## 3. Annex II: the closed list of data

Annex II is titled «Datos a aportar en el ejercicio de la actividad de alquiler de vehículos». It
is a closed list; the agreement and the two records together must let the firm hold every item.
Verbatim:

1. Datos del arrendador/a: a) NIF/CIF. b) Nombre de la compañía. c) Municipio. d) Provincia. e) País. f) Dirección completa del arrendador/a. g) Teléfono fijo y/o móvil. h) Web de la empresa. i) E-mail.
2. Datos del arrendatario: a) Nombre o razón social. b) Primer apellido. c) Segundo apellido. d) Sexo. e) Numero de documento de identidad. f) Tipo de documento (DNI, pasaporte, TIE, NIF). g) Nacionalidad. h) Fecha de nacimiento. i) Lugar de residencia habitual: Dirección completa; Localidad; País. j) Teléfono fijo. k) Teléfono móvil. l) Correo electrónico.
3. Datos del conductor principal: a) Nombre. b) Primer apellido. c) Segundo apellido. d) Sexo. e) Numero de documento de identidad. f) Tipo de documento (DNI, pasaporte, TIE). g) Nacionalidad. h) Fecha de nacimiento. i) Lugar de residencia permanente: Dirección completa; Localidad; País. j) Teléfono fijo. k) Teléfono móvil. l) Correo electrónico. m) Carnet de conducir: Tipo; Validez; Número; Número de soporte.
4. Datos del segundo conductor (si procede): «Los mismos que el anterior.»
5. Datos de la transacción: a) Datos del contrato: Número de referencia; Fecha; Lugar; Firmas. b) Datos de la ejecución del contrato: Lugar de recogida; Fecha de y hora de recogida; Lugar de devolución; País de devolución; Fecha y hora de devolución. c) Datos del vehículo: Marca; Modelo; Matrícula; Número de bastidor; Color; Tipo (camión, furgoneta, turismo); Número de kilómetros a la recogida; Número de kilómetros a la devolución; Datos del GPS (si disponible). d) Datos del pago: Tipo (efectivo, tarjeta de crédito, plataforma de pago, transferencia...); Identificación del medio de pago: tipo de tarjeta y número, IBAN cuenta bancaria, solución de pago por móvil, otros; Titular del medio de pago; Fecha de caducidad de la tarjeta; Fecha del pago.

How the list lands in the documents:

| Annex II | Where |
|---|---|
| 1 | Block A of the agreement |
| 2 | Block B of the agreement, with sex added because the list names it |
| 3 and 4 | Block C of the agreement, with the licence type, validity, number and support number |
| 5.a | Reference and date from the agreement, place of signing added to block A, signatures from the signature fields |
| 5.b | Block E of the agreement |
| 5.c | Block D of the agreement; the odometer at pick-up and at return also in the two records |
| 5.d | Block F of the agreement: type of payment, means of payment, holder, expiry and date |

Capture the data fields, not a picture of the documents (`../eu-baseline.md`, rows 19 and 21). The
decree lists data to hold; whether a copy of the document may be kept was not checked, and no
position of the Spanish data protection authority was read on its own page.

## 4. Deadlines, retention and sanctions

| Rule | Value | Source |
|---|---|---|
| Data of Annex II point 1 | Communicated before starting the activity, within ten days of completing the administrative steps | RD 933/2021 art. 6.1 and 6.2 |
| Data of Annex II points 2, 3, 4 and 5 | Communicated immediately and in any case within 24 hours of the reservation or the signing of the contract, or its cancellation, and within 24 hours of the start of the services | RD 933/2021 art. 6.3 |
| Channel | Telematic procedures | RD 933/2021 art. 6.4 |
| Retention | Three years from the end of the service or the contracted benefit | RD 933/2021 art. 5.3 |
| Register | Electronic register holding the Annex data | RD 933/2021 art. 5.1 |
| Sanctions | Missing registers and omitted communications are serious: fine of 601 to 30,000 euros. Irregularities or deficiencies in filling the registers, and communications outside the deadline, are minor: fine of 100 to 600 euros | RD 933/2021 art. 8.2 and 8.3; LO 4/2015 art. 39.1 |

The filing to the authorities is a separate act. It is made by the firm through the electronic
procedure of the Ministry of the Interior, or through a third party the firm has authorised (FAQ Q22).
The signed records are the source of the data; this skill does not file anything.

A change of data means a new communication (FAQ Q26).

## 5. Signature

The decree names no type of signature for the hoja de servicios. Nothing read in the texts for this
skill asks for a qualified electronic signature or a notary for the three documents.

## 6. Not in this pack

- The Spanish rule that transposes the withdrawal exemption for car rental: not read. The EU rule in
  `../eu-baseline.md`, row 2, is the one to apply, and the Spanish article was not checked.
- Spanish rules on cancellation before pick-up, minimum age, years of licence, deposits, excess,
  compulsory insurance, fines and tolls, and the Spanish list of unfair terms: not checked.
- Regional rules: not checked.
- Whether a draft or adopted Interior order changes the annexes: not verified; none appears in the
  consolidated record.
- A Spanish data protection authority position on copying documents: not read on the authority's own
  page; do not state one.

Never state these, because the sources do not support them: that the communication duty became
enforceable on 2 December 2024 (the decree gives effect from 2 January 2023); that Catalonia and the
Basque Country keep separate systems; that Interior accepts an electronic signature on the hoja.
