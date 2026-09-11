---
name: formify-track-signatures
description: 'Track who has signed, remind them, get notified automatically when they do, fix a wrong recipient, or cancel a send. Use after a document went out for signature, when contact details were wrong, or when the signed copy is needed. Triggers on "who has signed", "send a reminder", "notify me when signed", "wrong email address", "cancel the signing", "download the signed copy", "vem har signerat", "påminnelse", "återkalla", "quién ha firmado". Not for sending: see formify-send-contract.'
license: MIT
metadata:
  version: "1.1.0"
---

# After the document was sent

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

## When it does not

- **Sending a document in the first place** → `formify-send-contract`.
- **Building or editing the PDF** → `formify-pdf-forms`.

## Preconditions

A Formify account, connected. Every action here needs one.

**Always read current state before acting.** Call `get_document` before any reminder,
repair, cancellation or deletion. Never act on a status remembered from earlier in the
conversation — someone may have signed in the meantime, and several of these operations are
irreversible.

If the user does not know which document they mean, list recent documents and let them pick
by name. Never show internal IDs; those are for tool calls.

## Procedure

### 1. Read the document and report it in human terms

`get_document` returns the document's status and one entry per signer. Present it the way a
person would ask for it:

> **Rental agreement — Calle Mayor 14**
> Maria Sanchez — signed, yesterday 14:20
> Johan Berg — not yet signed
> Anna Lindqvist — not yet signed

Two different fields, and confusing them is the most common error here: the **document**
has a `status`; each signer has a `signatureStatus`. Read the second one per person.

Document statuses and what they permit:

| Status | Meaning | What is possible |
|---|---|---|
| `processing` | Still being prepared; invitations go out automatically when it finishes | Wait |
| `created` | Prepared, invitations not yet sent | No reminders yet |
| `awaiting_signatures` | Out with at least one person | Remind, repair, cancel |
| `completed` | Everyone signed | Download, delete |
| `revoked` | Cancelled | Delete |

### 2. Remind only the people who have not signed

Reminders are the most-asked and most-mishandled action.

- The document must be `awaiting_signatures`. **Any other status returns 403** — say why
  and stop rather than retrying.
- Include only signers whose `signatureStatus` shows they are still awaiting. Never include
  someone who has signed.
- **Maximum two reminders per signer per rolling 60 minutes.** Beyond that the call fails.
  Each signer's remaining cooldown is reported in seconds by `get_document` — read it, and
  tell the user how long is left instead of retrying.
- Show who will be reminded and get a yes before sending. If several people are
  outstanding, offer both: remind everyone, or pick.

### 3. Repair a recipient whose details were wrong

An unsigned signer's contact details can be corrected. Sending a fresh invitation and
revoking the old links happens automatically.

Two limits, and the first one surprises people:

- **An existing contact method can be changed, never added.** If someone was created with
  only a phone number, an email cannot be added to them afterwards, and the reverse is also
  true. When that is what the user needs, the honest answer is to cancel and resend.
- Contact details can be updated at most twice, then a 60-minute cooldown applies. The
  remaining time is reported by `get_document`.

Confirm the correction before sending it: a second wrong address costs another round of the
same cooldown.

**A corrected signer gets a new identifier.** Read the document again before any further
action on that person — a reminder sent to the identifier you held before the correction is
sent to someone who no longer exists.

### 4. Hand someone a link directly

When the signer is standing there, or reachable on a channel Formify does not send to, get
their personal signing link and give it to them.

Each link is **verification-locked**: opening it requires a one-time code that Formify sends
to the contact method already on file, never to a value the opener types. So a forwarded or
leaked link cannot be opened by anyone else. Say this to the user — it is the question they
ask next.

A signer with both an email and a phone comes back as two entries, one per channel. Offer
both and let the user choose. A signer with no contact method on file cannot be verified and
does not appear at all; that person cannot be repaired on a sent document.

This works only on a sent document, not a draft.

### 5. Correct a value before anyone has signed

Form field values can still be set on a sent document, and — unlike what older guidance
claimed — the values already filled in can be read at **any** status, not only after
completion. That is how you show the user what a signer has entered so far.

The window closes at the first signature. After that, values are fixed.

This changes field values only. It cannot change the contract text; that requires cancelling
and sending a corrected document.

### 6. Cancel, and delete

**Cancelling** is possible while a document is not yet fully signed. It is irreversible.
Show a summary — what the document is, who has already signed — and require an explicit yes.
Someone having already signed is worth naming out loud; their effort is about to be
discarded.

**Deleting** is only possible for a document that is completed or revoked, and it removes
the associated file. Confirm separately. Deleting is not archiving: if the user needs the
signed copy, retrieve it first.

### 7. Retrieve the signed document

Once complete, produce a download link for the finished PDF. **It expires after ten
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

1. **Where should it go?** It must be a public web address reachable over HTTPS — their own
   system, their site, or an automation service they already use. A private network address
   or a plain HTTP one will not be accepted. If they have none of these, say so plainly and
   leave it; do not send them off to build one.
2. **Which events?** Most people want completion only. Offer per-signer events when several
   people sign and they want progress, not just the end.
3. **Do they want a reminder set up too?** The two work together: one tells them, the other
   chases the signer.

Each subscription is created with a signing secret, which is how the receiving system knows a
message really came from Formify. Give the secret to the user once, tell them their system
must check it, and say that it can be rotated if it is ever exposed. Existing subscriptions can
be listed and removed the same way — worth checking before adding a second one that duplicates
the first.

**Say what this replaces.** After it is set up, tell the user they no longer need to ask you
whether it has been signed. That sentence is the whole value of the step.

## Failure modes

| What you see | What it means | What to do |
|---|---|---|
| Reminder returns 403 | The document is not `awaiting_signatures` | Report the actual status. Do not retry. |
| Reminder returns 429 | Two reminders already sent to that signer this hour | Read the remaining cooldown and tell the user how long is left. |
| Contact update rejected | Trying to add a method that was never there | Cannot be repaired on a sent document. Offer to cancel and resend. |
| A signer is missing from the link list | They have no contact method on file | Same as above. |
| Cancel refused | The document is already fully signed | Nothing to cancel. Offer the signed copy instead. |
| Delete refused | The document is still live | Only completed or revoked documents can be deleted. |
| The download link stopped working | The ten-minute window elapsed | Fetch a new one. |
| Field values will not change | Someone has signed | The window closed. A correction now needs a new document. |

## References

None. Everything here is in the procedure, because every step is a live account operation
whose current state must be read at the moment it runs.
