---
name: formify-share-link
description: 'Publish one reusable signing link anyone can open and sign, with no named recipients. Use when a form, waiver or consent goes to people whose names are unknown, when a link belongs on a website or a QR code, or when reading what a link has collected. Triggers on "public link", "signing link", "link anyone can sign", "share a form", "put it on our website", "signeringslänk", "delningslänk", "enlace público", "enlace para firmar". Not for inviting named signers: see formify-send-contract.'
license: MIT
metadata:
  version: "1.6.2"
---

# Publish a document as one signing link

Version 1.6.2. If asked which version you are, quote this line.

## Purpose

Turn a PDF into a single link that anyone holding it can open, fill in and sign. There are no
recipients and no invitations: the user shares the link themselves, and every person who signs
produces their own separate document.

This is the shape a form takes when the sender does not know who will fill it in — an intake
form on a website, a waiver at a reception desk, a consent behind a QR code, an application
posted in a group chat.

## When this applies

- "I want one link I can put on our website."
- "Send me something I can print as a QR code."
- "Everyone who joins needs to sign this, but I don't know who they are yet."
- "How many people have filled in my form?"
- "Turn that link off."

## When it does not

- **Inviting people you can name** → `formify-send-contract`. One document, its signers
  invited by email, SMS or WhatsApp. If the user can list who signs, they want that skill.
- **One person's private way into a document already sent** → `formify-track-signatures`.
  That link is locked to one person by a one-time code. This one is public by definition.
- **Building or editing the PDF** → `formify-pdf-forms`. Build it there, publish it here.
- **Deciding which identity check is needed** → `formify-verify-identity`. This skill places
  whatever that one chose.

## Preconditions

A connected Formify account, and a PDF already uploaded.

**Call `get_account_capabilities` first, every time.** Three keys decide what is possible:
`publicLinks` to see links at all, `publicLinksCreate` to make one, `accessLevels` for
sharing a link with colleagues. `aiAssistant` and the signature-method keys are checked the
same way as anywhere else. Offering a feature the account does not have is the fastest way to
lose the user's trust.

**A live link is billed, and creating one is not reversible in the way users expect.** On the
credits pricing model every live link is a billed instance, charged pro rata for the rest of
the current period and renewed each period for as long as it stays active.

**The signatures it collects are charged separately, as they happen.** The link is a standing
cost; each person who signs through it is another. Users assume a link is paid for once, and
a busy link can cost far more than the link itself — say both parts whenever cost comes up.
Read the cost section below before creating anything.

## Procedure

### 1. Announce what this is, and check it is what they want

Before asking anything:

> I can publish this as one link that anyone can open and sign. You share the link yourself —
> nobody gets invited — and each person who signs ends up with their own signed copy that you
> can read back. It works on a website, in a QR code or pasted into a chat. Signers can sign
> by hand, or with BankID, an ID scan or a face check if your plan includes them.
>
> Shall I set one up?

Then confirm the shape, because the two products look alike from the outside and cost
differently:

| The user says | What they mean |
|---|---|
| "Send it to Maria and Johan" | Named signers — `formify-send-contract`, not this |
| "Put it on our booking page" | One public link — this skill |
| "Everyone in the club has to sign it" | A link, unless the club roster is short and known |

The test is whether they can name who signs. If they can, a send is cheaper and gives them
tracking per person. If they cannot, this is the only shape that works.

### 2. Get the PDF in place

A link is always created from an uploaded file. There is no template route.

Four upload routes, **exactly one per upload**. Try them in this order and say which you used:

1. **A file reference the host supplied**, when the user attached the file and this
   environment passes attachments to tools. Pass it exactly as given; never build one by hand.
   If a file was attached but no reference arrived, retry the call once.
2. **A public HTTPS URL** — works everywhere. Prefer it whenever a URL exists.
3. **A staged upload**, where shell commands are available: request the upload URL, run the
   returned command, wait for success, then register the file. A new staged upload replaces
   any active one, so finish one file before starting the next.
4. **Base64**, only with the complete untruncated bytes and the filename. The practical
   ceiling is roughly 30–50 kB of PDF; beyond that the payload cannot be emitted in one
   message, and a truncated one uploads a corrupt file that fails silently.

The file must not be password-protected and must not carry a digital signature from another
service. The ceiling is 50 MB.

Read the document's form fields after uploading. Whatever values the link carries are the
**starting point every signer sees**, not anyone's answers — a public link has no single set
of answers, because everyone who opens it fills it in independently. Pre-fill only what is
genuinely constant, such as the sender's own company details.

### 3. Design the signature slots

**A slot is a role, not a person.** There are no recipients, so a slot has no email, no phone
number, no delivery method and no signing order. What it has is a label on the signature line
— `Member`, `Guest`, `Patient` — which whoever signs can overwrite. Leave the label out
entirely to make the signer type their own name from scratch.

At least one slot is required. Most links need exactly one; a second is for a document where
two people sign together in front of the same screen, not for two different parties.

Four settings per slot matter:

- **Signature method.** Handwritten by default; BankID, ID scan and face check are each gated
  on the same capability as anywhere else. Every person who opens the link is verified the
  same way, which is usually the point of publishing it. An ID scan needs **two** boxes — the
  signature box and a separate ID-scan box — and must be placed on an existing page.
- **Coordinates are mandatory.** Unlike a document created from a template, a link has nothing
  to inherit them from, so every slot placed on an existing page must be given its page, x and
  y. See `references/signature-placement.md` before choosing them; the corner-of-the-page
  failure from a decimal coordinate is the same here as everywhere.
- **Name clarification** asks the signer to type their name beside the signature. It defaults
  to on, and on a public link that is almost always right, since the slot has no identity of
  its own. Leave it alone unless the user objects.
- **A payment before signing**, where the account has `signAndPay`. The payment link is set up
  in the Formify client, not here — never invent its identifier — and it **must be one that
  allows multiple use**, because a single public link is signed by many people. A single-use
  payment link works once and then silently blocks everyone after the first signer.

Ask which language signers should see. The choice is English, Swedish or Spanish, and it is a
closed list. The in-document AI assistant, where the account has it, is offered here as it is
on any document — and it is worth offering, because a public link has no sender standing by to
answer questions.

### 4. Confirm the cost before creating anything

**Never create a link without an explicit yes that names the charge.** This is not a
formality: a link is a recurring billed instance, and the user has no way of knowing that from
the request they made.

> That will create a live link, which is billed for the rest of this period and renews while
> it stays active. Each signature collected through it is charged separately, as it happens.
> Shall I go ahead?

Say both parts. A user told only about the link's own charge will read a month of signatures
as a billing error.

Insufficient credits fails the call and creates nothing. A suspended subscription fails it
too. Both are clean failures — say what happened and stop, rather than retrying.

### 5. Create it, then hand over the URL

The link is live the moment it is created. **Formify sends nothing to anyone** — the URL comes
back to you, and the user distributes it themselves. Say that plainly, because a user who has
sent documents before will assume invitations went out.

A new link may come back as `processing`, with no URL yet: the AI assistant is still reading
the document. Wait and read it again rather than reporting a failure. A link's statuses are
`active`, `disabled` and `processing` — deliberately not a document's vocabulary, because a
link is a source of documents rather than a signature request.

Hand over the URL itself, and say what to do with it: paste it on the page, put it behind a QR
code, send it in a message. Then close the loop:

> Whenever you want, I can tell you how many people have signed it, fetch any of their signed
> copies, or switch the link off.

### 6. Read what the link has collected

Each person who signs produces their own document, and those documents are **not** in the
ordinary document list. They live under the link. From there each one behaves normally: its
status, its field values and its signed copy all work as on any other document.

**Only completed submissions appear.** Someone who opened the link and gave up half-way leaves
no trace at all, so "nobody has signed" and "nobody finished" cannot be told apart. Report it
that way rather than implying nobody looked.

The listing paginates: follow `nextOffset` until it comes back null, and never stop at a short
page — a page with fewer items than the limit is not proof it is the last one.

Everything after that — reading a signed copy, checking field values — is
`formify-track-signatures`.

### 7. Edit a live link

Editing is safe and free: **the public URL survives**, so anyone already holding the link
keeps a working one, and nothing is billed again.

**But an edit is a full replace.** Read the link first and send its complete configuration
back with your change applied. Every property round-trips, so nothing is lost by doing it that
way — and a name, a language or a slot left out of the call is gone. The one exception is the
document: omit it to keep the file the link already has.

Two limits worth naming before the user asks:

- **A disabled link cannot be edited.** The call fails. Duplicating it is the only way back,
  and that is billed as a new link.
- **Only the owner may edit.** A colleague can read a shared link and switch it off, but not
  change it.

### 8. Switch it off, and delete it

**Disabling is permanent and there is no way back.** The link stops accepting signers and its
URL stops working. Confirm first, naming the link, and say what it does and does not touch:

- Documents the link already produced are unaffected and stay accessible.
- Someone who had already finished keeps their completed document.
- Someone part-way through signing is cut off immediately.
- The billed instance is released, with no refund for the current period.
- To have the link back, it must be duplicated — a new URL, and a new charge.

Anyone on the account may disable a link shared with the account; it is not owner-only.

**Deleting is separate, and it comes second.** A link must be disabled before it can be
deleted; deleting a live one fails. That order exists because deleting does not close the link
— a live link that was deleted would keep serving with nothing left behind it to stop. Deleting
permanently removes the link's generated PDFs, thumbnails and any AI assistant data, and it is
owner-only. Documents the link produced are **not** deleted.

Most users who say "turn it off" mean disable and nothing more. Do not offer deletion in the
same breath; it destroys data and the link is already dead.

### 9. Duplicate, when a copy is genuinely wanted

A duplicate carries the same document, slots, language, print setting and assistant, and gets
its **own** URL. The source keeps working.

**A duplicate is billed exactly like a new link** — its own instance, charged pro rata. Confirm
it the same way. This is also the only way to bring back a disabled link, and it is worth
saying out loud that the old URL will not work again: anything already printed or published
pointing at it is dead.

Give the copy its own name. Defaulting leaves the user with two links of the same name and no
way to tell them apart.

## Failure modes

| What you see | What it means | What to do |
|---|---|---|
| Creation refused, insufficient credits | The wallet cannot cover the charge | 402. Say so plainly and stop — nothing was created. Offer a named send instead. |
| Creation refused, subscription suspended | The account is suspended | 403. Nothing was created. Say what it needs; do not retry. |
| The user is surprised by the bill | Only the link's own charge was explained | Two charges exist: the live link, and every signature collected through it. Say both, every time. |
| Creation refused, capability missing | The account has no `publicLinksCreate` | Name what it would do and offer a named send instead. Never downgrade silently. |
| The link has no URL yet | Status is `processing`; the assistant is still reading the document | Wait and read it again. This is not a failure. |
| The edit was rejected | The link is disabled, or the caller is not its owner | A disabled link cannot be edited — duplicate it, and say it will be billed. For ownership, the owner must make the change. |
| Slots or a name vanished after an edit | An edit is a full replace and they were left out | Read the link, send the complete configuration back. |
| Delete rejected | The link is still live | Disable first, then delete. Confirm both separately. |
| The signature landed in the corner of a page | A decimal coordinate was discarded | Send whole numbers. Coordinates are mandatory on a link — nothing is inherited. |
| The signature covers the text | Fields are opaque and overlap is never detected | Move it to clear space, or shrink it with a scale factor between 0.25 and 1.5. |
| Nobody appears in the link's documents | Either nobody finished, or the listing stopped at a short page | Follow `nextOffset` to the end first. Then say that no one has completed it — an abandoned form leaves no trace. |
| The user expected invitations to go out | A link invites nobody by design | Say the link is live and hand them the URL to share. |
| Everyone after the first signer is blocked at payment | The payment link is single-use | A public link needs a multiple-use payment link. It is changed in the Formify client. |

## References

- **`references/signature-placement.md`** — the coordinate system, field sizes, page-size
  arithmetic, ID-scan box placement and stacking several boxes. Open it before placing any
  slot, since a link never inherits coordinates and every one must be computed.
