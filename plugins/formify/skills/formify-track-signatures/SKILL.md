---
name: formify-track-signatures
description: 'Track who has signed, remind them, get notified, fix a wrong recipient, change a field value or cancel a send. Use after sending for signature. Triggers: "who has signed", "send a reminder", "notify me when signed", "wrong email address", "cancel the signing", "signed copy", "vem har signerat", "påminnelse", "återkalla", "quién ha firmado". Not for sending: formify-send-contract.'
license: MIT
metadata:
  version: "1.8.0"
---

# After the document was sent

Version 1.8.0. If asked which version you are, quote this line.

## Purpose

Everything that happens between sending a document and having it signed: finding it,
seeing who is still outstanding, reminding only them, repairing a wrong email address,
handing someone a link in person, correcting a value before anyone signs, cancelling, and
retrieving the finished file.

This is the half of the job most agents never learn. Sending is one moment; waiting is the
following week.

## When this applies

- "Has anyone signed this yet?"
- "Remind the ones who haven't."
- "I typed his email wrong."
- "The client is in front of me — can I just give them the link?"
- "The amount is wrong and nobody has signed yet."
- "The deal is off, cancel it."
- "Send me the signed copy."
- "Just tell me when it's signed — I don't want to keep checking."
- "Has anyone filled in the form I shared?"

## When it does not

- **Sending a document in the first place** → `formify-send-contract`.
- **Building or editing the PDF** → `formify-pdf-forms`.
- **Managing the public link itself** — editing it, switching it off, what it costs →
  `formify-share-link`. Reading the documents it produced belongs here.

## Preconditions

A Formify account, connected. Every action here needs one.

**Always read current state before acting.** Call `get_document` before any reminder,
repair, cancellation or deletion. Never act on a status remembered from earlier in the
conversation — someone may have signed in the meantime, and several of these operations are
irreversible.

If the user does not know which document they mean, list recent documents and let them pick
by name. Never show internal IDs; those are for tool calls.

**Every list is paginated, and a short page does not mean the last page.** A listing returns
a `nextOffset`; keep asking with it until it comes back null. A page may hold fewer items than
the limit and still have more behind it — that is normal, not the end. Stopping at the first
short page is how "you have three documents out for signature" gets said to someone who has
eleven, and nothing about the answer looks wrong.

## Procedure

### 1. Read the document and report it in human terms

`get_document` returns the document's status and one entry per signer. Present it the way a
person would ask for it:

> **Rental agreement — Calle Mayor 14**
> Maria Sanchez — signed, yesterday 14:20
> Johan Berg — not yet signed
> Anna Lindqvist — not yet signed

Two different fields, and confusing them is the most common error here: the **document**
has a `status`; each signer has a `signatureStatus` (`awaiting_signature` or `signed`). Read
the second one per person.

Document statuses and what they permit:

| Status | Meaning | What is possible |
|---|---|---|
| `created` | Created and ready | No reminders (they need `awaiting_signatures`) |
| `processing` | The AI assistant is still preparing it | Wait |
| `error` | Processing failed | Report it; reminders, repair and download do not apply |
| `awaiting_signatures` | One or more signees have not signed | Remind, repair, cancel |
| `completed` | All signees have signed | Read field values, download, delete |
| `revoked` | Cancelled | Delete |
| `deleted` | Deleted | Nothing further |

**A document signed through a public link will not be in that list.** `list_documents` holds
what the user *sent* to named people. A public link — one reusable link anyone may open —
produces its own document per signer, and those live under the link. So when the user asks
"has anyone filled in my form yet?" and nothing turns up, do not report zero: ask whether it
went out as a link, then follow the path `list_links` → `list_link_documents(linkId)` →
`get_document` / `get_signed_document_url` / `get_document_field_values` on each entry's
document identifier. `list_links` needs the `publicLinks` capability.

**Only completed submissions are listed.** Someone who opened the link and abandoned it
half-filled leaves no trace, so "nobody has signed" and "nobody finished" are the same answer
here, and there is no way to tell them apart. Say it that way rather than implying nobody
looked. Follow `nextOffset` until it is null, never stopping at a short page. Everything about
the link itself — switching it off, editing it, what it costs — is `formify-share-link`.

### 2. Remind only the people who have not signed

Reminders are the most-asked and most-mishandled action.

- The document must be `awaiting_signatures`. **Any other status returns 403** — say why
  and stop rather than retrying.
- Include only signers whose `signatureStatus` is `awaiting_signature`. Never include
  someone who has signed.
- **Maximum two reminders per signer per rolling 60 minutes.** Hitting the limit is not an
  error: the call returns 200 and lists that signer in `remindersNotSentTo` with a
  `reminderCooldown`. Always read `remindersSentTo` and `remindersNotSentTo` to see who
  actually got one. Check `signeeDetails[].reminders.reminderCooldown` from `get_document`
  (seconds left, 0 when allowed) before calling, and tell the user how long is left instead
  of retrying. Example: reminders at 10:00 and 10:20 go out; one at 10:40 returns 200 but
  lands in `remindersNotSentTo` with `reminderCooldown` ≈ 1200 (allowed again at 11:00, when
  the 10:00 one leaves the window). Say plainly "not sent, wait 20 minutes", never "sent".
- Show who will be reminded and get a yes before sending. If several people are
  outstanding, offer both: remind everyone, or pick.

### 3. Repair a recipient whose details were wrong

A signer whose `signatureStatus` is `awaiting_signature` can have contact details corrected
(`update_signee`). A fresh invitation goes out and the old links are revoked automatically. A
signer who has signed cannot be changed, and neither can a completed document (403).

Limits, and the first one surprises people:

- **An existing contact method can be changed, never added** (400). If someone was created
  with only a phone number, an email cannot be added afterwards, and the reverse is also true.
  An invalid email or phone number, or a request that changes nothing, is also 400. When
  a method must be added, the honest answer is to cancel and resend.
- Contact details can be updated at most twice, then a 60-minute cooldown applies and further
  updates return 400. Read `signeeDetails[].updates.updateCooldown` from `get_document`
  (seconds left) before calling, and tell the user how long is left.
- Adding a phone number can also return 403 when the account's phone-channel lock applies.
- A request that changes nothing comes back as 400 "Invalid request parameters: emailAddress,
  phoneNumber, fullName". It does not mean the address is wrong: compare with what is on file
  and tell the user it is already set.

Confirm the correction before sending it: a second wrong address costs another round of the
same cooldown.

**A successful update creates a new `signeeId`.** Read the document again before any further
action on that person — a reminder sent to the identifier you held before the correction is
sent to someone who no longer exists.

### 4. Hand someone a link directly

When the signer is standing there, or reachable on a channel Formify does not send to, call
`get_recipient_links` and give them their personal signing link. It also serves signees
created with `disableInvitationMessage: true` (Formify never invited them) and any case where
the user distributes links themselves. It is idempotent: later calls return the same links.

Each link is **verification-locked**: opening it requires a one-time code that Formify sends
to the contact method already on file, never to a value the opener types. So a forwarded or
leaked link cannot be opened by anyone else. Say this to the user — it is the question they
ask next.

A signer with both an email and a phone comes back as two entries (same `signeeId`, one per
channel). Offer both and let the user choose. A signer with no contact method on file is
omitted entirely, and `update_signee` cannot fix that on a sent document (it changes a
contact method, never adds one): revoke and resend with an email or phone for them.

This works only on a sent document, not a draft.

**This is not a public link, and the word is the trap.** What you hand over here is one
person's private way into one document, locked to the contact method already on file. A
public link is the opposite: no named recipient, anyone who holds it may sign, and each one
who does gets their own document. If the user says "just give me a link I can put on our
website", they mean the other thing — `formify-share-link`.

### 5. Correct a value before anyone has signed

Form field values can still be set on a sent document with `set_document_field_values`, but
only on editable fields and only before anyone has signed. The window closes at the first
signature; after that, values are fixed.

**Values cannot be read back before completion.** `get_document_field_values` works only once
the status is `completed`; every other status returns 403 by design, and retrying will not
help. `get_document_fields` returns field definitions and predefined defaults only, so there is
no way to show the user what a signer has entered so far or what was pre-filled.

This changes field values only. It cannot change the contract text; that requires cancelling
and sending a corrected document. The cheapest way to do that is `duplicate_document`: it
copies the file, fields, signers and settings into a new draft and sends nothing, so the
correction is made there and sent with `formify-send-contract`. Nothing is charged until that
draft is sent.

### 6. Cancel, and delete

**Cancelling** (`revoke_document`) is possible while a document is not yet fully signed. It is
irreversible.
Show a summary — what the document is, who has already signed — and require an explicit yes.
Someone having already signed is worth naming out loud; their effort is about to be
discarded.

**Deleting** (`delete_document`) is only possible for a document that is `completed` or
`revoked`; on a live one it returns 403 "The document must be revoked first". So "delete the
contract he never signed" is two steps, cancel and then delete, each with its own yes. A revoked
document is deleted together with its file. A completed document is removed from the account
at once, but it is permanently deleted with its signed file only after every signer has also
deleted their own copy. Confirm separately. Deleting is not archiving: if the user needs the
signed copy, retrieve it first.

### 7. Retrieve the signed document

Once complete, produce a download link for the finished PDF (`get_signed_document_url`). **It expires after ten
minutes**, so fetch it when the user is ready to use it, not earlier in the conversation.

Offer it before it is asked for. A completed signature that nobody downloaded is a job left
half done.

### 8. Stop checking — have Formify say when it happens

Everything above is the user asking. Formify can tell them instead, and nothing in this skill
is more worth offering, because it is the difference between a person remembering to check and
a person being told.

Formify can call a web address of the user's whenever something happens to a document. Six
things can be reported: the document was **created**, **opened** by a signer, **signed** by
someone, **completed** by everyone, **revoked**, or **deleted**. A subscription can ask for
any combination of them.

Offer this the moment someone says any version of *"let me know when it's signed"*, *"I keep
having to check"*, or *"can this land in our system automatically"*. Three questions settle it:

1. **Where should it go?** `register_webhook` needs a public web address reachable over HTTPS — their own
   system, their site, or an automation service they already use. A private network address
   or a plain HTTP one will not be accepted. If they have none of these, say so plainly and
   leave it; do not send them off to build one.
2. **Which events?** Most people want completion only. Offer per-signer events when several
   people sign and they want progress, not just the end.
3. **Do they want reminders too?** There is no scheduled or automatic reminder: reminders go
   out only when someone calls `send_reminder`, so say that rather than promising a chase.

A signing secret is how the receiving system knows a message really came from Formify.
`list_webhooks` shows per subscription whether it has one (`hasSigningSecret`), and older
subscriptions often do not. `rotate_webhook_secret` returns a new HMAC secret: give it to the
user once, tell them their system must check it, and use the same call if a secret is ever
exposed. Call `list_webhooks` before adding one, so as not to duplicate an existing
subscription, and offer a secret for any listed one that lacks it; `delete_webhook` stops
delivery immediately.

**Say what this replaces.** After it is set up, tell the user they no longer need to ask you
whether it has been signed. That sentence is the whole value of the step.

## Failure modes

| What you see | What it means | What to do |
|---|---|---|
| Reminder returns 403 | The document is not `awaiting_signatures` | Report the actual status. Do not retry. |
| Reminder returns 200 but the signer is in `remindersNotSentTo` | Two reminders already sent to that signer in the last 60 minutes | Read the `reminderCooldown` and tell the user how long is left. |
| Contact update returns 400 | Adding a method that was never there, an invalid value, no change, or the two-update cooldown | Adding is impossible on a sent document: offer to cancel and resend. Otherwise read `updateCooldown`. |
| Contact update returns 403 | Document completed, or the phone-channel lock applies to an added phone | Report it; do not retry. |
| Field values read returns 403 | The document is not `completed` | Values are readable only after completion. |
| A signer is missing from the link list | They have no contact method on file | Same as above. |
| Cancel refused | The document is already fully signed | Nothing to cancel. Offer the signed copy instead. |
| Delete refused, 403 "must be revoked first" | The document is still live | Cancel it first (with its own yes), then delete. |
| Contact update returns 400 naming every field | The request changed nothing | The value is already on file; say so. |
| The download link stopped working | The ten-minute window elapsed | Fetch a new one. |
| Field values will not change | Someone has signed | The window closed. A correction now needs a new document. |
| A document the user swears they sent is not in the list | Either the listing stopped at a short page, or it went out as a public link | Follow `nextOffset` to the end first; then check their links and read that link's documents. |
| A link's form was opened but nothing is listed | Only completed submissions are recorded | Say that nobody has finished. An abandoned half-filled form leaves no trace either way. |

## References

None. Everything here is in the procedure, because every step is a live account operation
whose current state must be read at the moment it runs.
