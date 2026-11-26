# The three documents

One section per document: what it is for, its blocks in order, the fields, who signs and in which
order. Field names are short ASCII identifiers with no period, unique in the document. Fields are
left for the person signing; every other value is printed from what the firm said or what was
captured from the renter.

A value is printed once, in its block. Clauses refer to the block ("the price in block F") and never
repeat a figure. No date field next to a signature: Formify stamps date and time on each signature.

The national layer (`countries/<cc>.md` or the lookup) can add a block, add data fields or change a
period. It never removes the price information, the extras block or the signatures.

## 1. Rental agreement

**For:** the contract between the firm and the renter, signed before the renter takes the vehicle,
or at booking when the renter books at a distance.

| Block | Content |
|---|---|
| A. Lessor | name or company, tax number, full address of the business, telephone, e-mail, web address |
| B. Renter | name, sex where the country file lists it, identity document type and number, nationality, date of birth, address of habitual residence, telephone, e-mail |
| C. Drivers | main driver and, if any, second driver: name, date of birth, address, licence type, licence validity, licence number and, where the licence has one, its support number. State when the renter is also the main driver |
| D. Vehicle | make, model, plate, chassis number, colour, type, odometer at pick-up, GPS data if the vehicle has it |
| E. Period and places | pick-up place, date and time; return place, country, date and time |
| F. Price and payment | main characteristics of the hire; total price including taxes and every other cost the firm will charge; how the price is calculated where it cannot be fixed in advance; payment arrangements and means of payment; mileage allowance and the rate beyond it; fees for a means of payment, if any |
| G. Deposit and guarantee | amount, how it is held, when and how it is released |
| H. Fuel or charge, damage and excess | the firm's rules, stated by the firm: fuel or charge level at return, what is charged otherwise, the excess and when it is due, how damage is assessed |
| I. Extras | each extra on its own line with its price, each with its own box (fields below) |
| J. Withdrawal | for a booking with a fixed date or period: "There is no right of withdrawal from this booking." The firm's own cancellation terms, if any, follow as the firm's terms |
| K. Insurance and cover | what the firm states: cover included, waivers offered, restrictions on use abroad. Printed as the firm gave it |
| L. Fines, tolls and driver data | the firm's own clause on fines, tolls and any administration fee, and on passing the driver's details to an authority. Flag that the legal basis was not checked unless a country file covers it |
| M. Duration and termination | how the hire ends, early return, extension, late return |
| N. Complaints | how to complain to the firm and any out-of-court complaint mechanism the firm uses |
| O. Data protection | who the controller is, what each item of data is used for, how long it is kept, contact for requests, and that no picture of the renter's documents is kept unless block O says so |

| Field | Kind | Required | Filled by |
|---|---|---|---|
| `extra_waiver`, `extra_second_driver`, `extra_child_seat`, `extra_gps`, `extra_fuel_option` and one more `extra_<name>` per further extra | checkbox, one per extra, empty, with the extra's name and price in its label | no | renter |
| `terms_acknowledged` | checkbox: "I have received and read the price information and the rental terms in this document" | yes | renter |
| `renter_name`, `renter_birth_date`, `renter_nationality`, `renter_address`, `renter_phone`, `renter_email` | text | yes, only for data not already captured | renter |
| `renter_id_type` | radio group: `national_id`, `passport`, `residence_card`, `tax_id` | yes, only if not captured | renter |
| `renter_id_number` | text | yes, only if not captured | renter |
| `licence_type`, `licence_validity`, `licence_number`, `licence_support_number` | text | yes where the country asks for licence data, only if not captured | renter |
| `driver2_name`, `driver2_birth_date`, `driver2_address`, `driver2_licence_type`, `driver2_licence_validity`, `driver2_licence_number` | text | yes, only when the second driver extra is ticked | renter |

The extras are never pre-ticked and never grouped into a "select all". The firm's price for an
extra is printed in block I, once; the checkbox label names it without repeating the figure in the
clauses.

Block J is printed only when the booking fixes a date or period. A firm that allows cancellation
says so in its own words after the statement; the text must not suggest the law gives that right.

For an online booking that the renter confirms by signing, add the sentence "This booking obliges me
to pay" next to the signature block, and tell the user the button label was not checked
(`eu-baseline.md`, row 7).

**Signs:** renter and lessor. Order: lessor first, so the renter receives a signed offer.

## 2. Handover record at pick-up

**For:** fixing the state of the vehicle when the renter takes it, so that damage found later can be
told apart from damage that was already there.

| Block | Content |
|---|---|
| A. Reference | agreement reference, parties, vehicle make, model and plate |
| B. Handover | place, date and time of pick-up |
| C. Meter readings | odometer; fuel level or battery charge level |
| D. Existing damage | each mark described by position and kind, with the firm's photo reference if photos were taken |
| E. Accessories and documents | keys, vehicle papers, charging cable, safety items and any extra the renter ticked in the agreement, each with its own box |
| F. Renter's acknowledgement | accepts the condition as recorded, or accepts it with notes |

| Field | Kind | Required | Filled by |
|---|---|---|---|
| `odometer_pickup` | text | yes | lessor |
| `fuel_or_charge_pickup` | text | yes | lessor |
| `existing_damage` | multi-line text, "none" when there is none | yes | lessor |
| `acc_keys`, `acc_papers` and one `acc_<name>` per item | checkbox: handed over | no | lessor |
| `condition_ack` | radio group: `agree`, `agree_with_notes` | yes | renter |
| `renter_notes` | multi-line text | no | renter |

Whether a signed handover record, photographs or an inspection record is required by law was not
checked in the EU baseline; it is in the lookup questions. Offer the record as the firm's own good
practice, never as a legal duty.

**Signs:** lessor's staff member first, then the renter.

## 3. Return record

**For:** fixing the state of the vehicle at return, recording any new damage and the final charges.

| Block | Content |
|---|---|
| A. Reference | agreement reference, parties, vehicle, pick-up record reference |
| B. Return | place, date and time of return |
| C. Meter readings | odometer; fuel level or battery charge level; the figures from the pick-up record beside them |
| D. New damage | damage not in the pick-up record, each described by position and kind |
| E. Accessories and documents | the items of the pick-up record, each with its own box: returned |
| F. Final charges | each charge on its own line, each pointing to the block of the agreement that announced it: extra mileage, fuel or charge difference, late return, damage within the excess, fines and fees, deposit released |
| G. Renter's response | on damage: accepted or disputed; on charges: agreed or not agreed |

| Field | Kind | Required | Filled by |
|---|---|---|---|
| `odometer_return` | text | yes | lessor |
| `fuel_or_charge_return` | text | yes | lessor |
| `new_damage` | radio group: `none`, `listed` | yes | lessor |
| `new_damage_description` | multi-line text | yes when `new_damage` is `listed` | lessor |
| `acc_returned_keys` and one `acc_returned_<name>` per item | checkbox | no | lessor |
| `damage_decision` | radio group: `accepted`, `disputed` | yes when `new_damage` is `listed` | renter |
| `charges_decision` | radio group: `agree`, `do_not_agree` | yes | renter |
| `renter_comment` | multi-line text | no | renter |

A charge in block F that the agreement did not announce is flagged to the firm before the document
goes out (`eu-baseline.md`, row 5). A dispute is recorded as the renter's choice; the record does
not decide who is right.

When the renter is not present at return, the firm can issue the record for the renter to sign
later; the firm's own readings and damage description are then signed first.

**Signs:** lessor's staff member first, then the renter.

## Chains

Agreement, then the pick-up record on the day, then the return record. Offer the next document once,
at the end of the current one.
