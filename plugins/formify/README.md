<img src="assets/icon-128.png" alt="" width="72" align="left" hspace="16">

# Formify Core

**Ask an AI assistant to get something signed, and it knows how.**

Formify Core connects your assistant to [Formify](https://formify.eu), an electronic-signature
and identity-verification platform. With it, the assistant can build a contract or a fillable
form, place the signature fields where they belong, send it to the right people, verify who
signed with BankID or an ID scan, and follow up with the ones who have not.

It is not tied to any industry. You describe what you want signed and by whom; you never
learn a command.

## What is in the plugin

**Five skills**, which the assistant opens on its own when your request calls for them:

| Skill | What it does |
|---|---|
| `formify-pdf-forms` | Builds fillable PDF forms and contract templates: text fields, checkboxes, dropdowns, signature space, and markers for ID scans and company checks. |
| `formify-send-contract` | Sends a document for signature from a saved template, an uploaded PDF, or one drafted in the conversation. Shows where the signature will land before anyone is contacted. |
| `formify-verify-identity` | Verifies the signer: Swedish BankID, ID document scan, live face check, company registration lookup, KYC. |
| `formify-track-signatures` | Everything after sending: who has signed, reminders for only those who have not, fixing a mistyped email, cancelling, downloading the signed copy. |
| `formify-share-link` | One reusable public signing link anyone can open, for waivers, booking pages and open enrolment. |

**One connector**, the Formify MCP server at `https://mcp.formify.eu/mcp`, which lets the
assistant act on your Formify account.

## Setup

1. Install the plugin.
2. Connect your Formify account: open the plugin, go to **Connectors**, select **Connect**,
   and sign in to Formify in the browser window that opens. The assistant never sees your
   password, and it can do only what your account allows.

Building and structuring a document works without an account. Sending, signing, identity
checks and public links use your Formify account.

**Creating an account:** sign up at https://app.formify.eu/ with your email address, in
any country. Swedish users can also sign up with BankID.

### Cursor and Grok Bot

1. Install **Formify Core** from the Cursor Marketplace (or add the repository
   `https://github.com/formify-e-sign/formify-skills` as a plugin source).
2. The plugin registers the Formify MCP server at `https://mcp.formify.eu/mcp`. When the
   assistant first needs your account, Cursor opens a browser window: sign in to Formify
   there and approve access (OAuth). No API key or password is shared with the assistant.
3. If Cursor does not offer the sign-in on its own, open **Settings → MCP**, find
   `formify`, and select **Connect**.

Spanish estate agencies should install **Formify for Real Estate Agencies** instead. It
already includes everything in Core, so do not install both.

## Try it

Copy any of these into the chat:

```
What can you do for me with Formify?
```

```
Turn this PDF into a fillable form.
```

```
Send the contract in this PDF to anna@example.com for signature, and check her ID
with BankID before she signs.
```

```
Who still hasn't signed the contract I sent last week? Remind them.
```

```
Turn this waiver into one link anyone can open and sign.
```

## More

- Full documentation and install guides for other apps: [formify-skills on GitHub](https://github.com/formify-e-sign/formify-skills)
- Privacy policy: https://formify.eu/privacy/policy
- Terms of service: https://formify.eu/privacy/terms
- Support: https://app.formify.eu/

MIT licensed.
