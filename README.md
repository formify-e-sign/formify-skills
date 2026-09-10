<img src="assets/icon-128.png" alt="" width="72" align="left" hspace="16">

# Formify Skills

**Ask an AI assistant to get something signed, and it knows how.**

These are agent skills for [Formify](https://formify.eu) — electronic signatures and
identity verification. Install them once, and your assistant can build a contract or a
fillable form, place the signature fields where they belong, send it to the right people,
verify who signed with BankID or an ID scan, and chase the ones who have not.

You can also send an AI assistant along **inside the document itself**. The person receiving
your contract can ask it what a clause means and it highlights the passage it is answering
about, reads it aloud if they prefer, and answers in English, Swedish or Spanish — so nobody
has to paste your contract into another chatbot to understand what they are signing.

You do not need to be technical, and you never learn a command. You describe what you want
signed and by whom; everything below is what the assistant handles for you.

Works with Claude Code, Claude Desktop, Codex, ChatGPT, Cursor, Gemini CLI and around twenty
other agents.

## Contents

- [Why this exists](#why-this-exists)
- [The four skills](#the-four-skills)
- [The whole process, not one document](#the-whole-process-not-one-document)
- [What you can ask for](#what-you-can-ask-for)
- [What the agent can actually do](#what-the-agent-can-actually-do)
- [One of those, end to end](#one-of-those-end-to-end)
- [Install](#install) — [Claude Code](#claude-code) · [Any agent, via the skills installer](#any-agent-via-the-skills-installer) · [Codex CLI](#codex-cli) · [Gemini CLI](#gemini-cli) · [Claude Desktop and claude.ai](#claude-desktop-and-claudeai) · [In a repository, with no install at all](#in-a-repository-with-no-install-at-all) · [Manually, anywhere](#manually-anywhere)
- [Connect the Formify MCP server](#connect-the-formify-mcp-server)
- [Coming soon: skills for your niche](#coming-soon-skills-for-your-niche)
- [What is in this repository](#what-is-in-this-repository)
- [Contributing](#contributing)
- [License](#license)

---

## Why this exists

A small business does not have a contracts department. It has one person who also does
everything else, and a folder of documents that get retyped, mis-edited and emailed around
until somebody signs a scan of a printout.

The signature was never the hard part. Everything around it is:

- The same agreement rebuilt from scratch, because last month's version is buried in an inbox
- Details typed by hand into a PDF that was never made fillable in the first place
- Three people who have to sign in a particular order, coordinated over email
- An identity or company check that legally has to happen, done informally or not at all
- A week of *"has anyone signed yet?"*, answerable only by scrolling back through mail

None of that is a signing problem. It is a **document workflow** problem, and it is where
small businesses lose their week.

These skills give an assistant the knowledge to run that workflow properly — the field
geometry, the ordering rules, the verification options, the follow-up logic — instead of
attaching a file and pressing send.

---

## The four skills

| Skill | What it does |
|---|---|
| **`formify-pdf-forms`** | Builds fillable PDF forms and contract templates: text fields, checkboxes, dropdowns, signature space, and Formify's `tink-*` markers for ID scans and company checks. |
| **`formify-send-contract`** | Sends a document for electronic signature — from a saved template, an uploaded PDF, or one drafted in the conversation. Previews where the signature will land before anyone is contacted. |
| **`formify-verify-identity`** | Verifies the person signing: Swedish BankID, ID document scan, live face check, company registration lookup, KYC. |
| **`formify-track-signatures`** | Everything after the send: who has signed, remind only the ones who have not, repair a mistyped email, hand someone a link in person, cancel, download the signed copy. |

Building and structuring a document happens in the conversation. Sending, signing and
identity checks run through your Formify account.

The `tink-*` markers a document carries are read by Formify's signing client. In any other
PDF viewer they are ordinary empty fields, so the document stays valid and usable on its own.

---

## The whole process, not one document

Most e-signature integrations stop at *upload a PDF, add a signature box, send*. That is the
easy tenth of the job. A real document has a life around it, and an assistant carrying these
skills can run all of it:

1. **Draft** — from a saved template, an uploaded PDF, or written from scratch in the conversation
2. **Make it fillable** — text fields, checkboxes, dropdowns, with the constraints a signing client actually imposes
3. **Place the signature correctly** — signature space is not a form field, and getting that wrong is the most common way a document arrives broken
4. **Decide what must be proven** — BankID, ID document scan, live face check, company lookup, or a one-time code before the document even opens
5. **Route it** — several signers, in a set order or all at once, by email or SMS
6. **Preview** — see exactly where every field landed, before a single person is contacted
7. **Explain it, on the recipient's side** — attach an AI assistant that lives in the document, highlights the clause it is answering about, and speaks if asked
8. **Follow up** — who signed, who only opened it, who never looked; remind the ones who have not, never the ones who have
9. **Repair** — correct a mistyped address, hand someone a link in person, revoke the whole thing
10. **Hand off** — download the signed copy, or fire a webhook so the next system in your business picks it up

Ten steps. The assistant runs them because the skills describe how each one works — not
because you learned a tool name.

---

## What you can ask for

Say it the way you would say it to a colleague. You do not need to know which skill handles
it, and you never name a tool.

**You rebuild the same tenancy agreement every month**

> Take this tenancy agreement, add fields for the tenant's name, address and move-in date,
> and send it to both tenants. They sign in order — main tenant first.

**Onboarding a company client means a compliance file nobody enjoys assembling**

> New client, a limited company. I need their company details verified, the beneficial owner
> confirmed, and a KYC record I can keep. Set up the engagement letter for signature.

**One document, many recipients, and they must not see each other**

> Send this NDA to the three freelancers on this list. Same document, one each, not a group
> signing.

**The quote is written; turning it into something signable is the chore**

> Turn this quote into a contract with a deposit line and a signature block, then send it to
> the customer by SMS — I only have their mobile.

**Forty recipients and no way to tell who is missing**

> This consent form goes to forty parents. I need to know who has returned it and chase only
> the ones who have not.

**Every client emails you the same three questions before they sign**

> Send the tenancy agreement to both tenants, and turn on the in-document assistant in
> Swedish so they can ask it about the notice period instead of ringing me.

**You need the ID details but you must not keep the picture**

> Patient intake form, signed on the tablet at reception, with an ID document scanned but
> the picture not kept — only the name and document number.

That last one is a real capability most people never discover: an identity document can be
scanned and its data captured **without the image being stored at all**. Keeping a copy of
someone's passport needs its own legal basis; often the data is all you needed.

---

## What the agent can actually do

Connected to your Formify account, through the MCP server:

| | |
|---|---|
| **Documents** | Create from a template, from an uploaded PDF, or from something drafted in the conversation. Preview before anyone is contacted. Send, revoke, download the signed copy. |
| **Recipients** | Several signers, in a set order or all at once. Email or SMS. Correct a mistyped address. Hand someone a link in person. |
| **Identity** | Swedish BankID, ID document scan, live face check, company registration lookup, KYC. A one-time code before the document even opens. |
| **Inside the document** | An AI assistant that travels with the contract. The recipient asks it a question, it highlights the clause it is answering about, reads it aloud on request, and speaks English, Swedish or Spanish. |
| **Following up** | Who has signed, who has only opened it, who has not looked. Remind the ones who have not — never the ones who have. |
| **Files and templates** | Upload, merge several PDFs into one, read the fields a template expects, fill them. |
| **Automation** | Webhooks, so something else happens when a document completes. |

Everything runs with exactly the permissions your Formify account already has, and every
feature is checked against your plan before it is offered — so the agent never proposes
something your account cannot do.

---

## One of those, end to end

> **You:** Take this rental agreement and send it to Maria for signature. She needs to show
> ID first.
>
> **Agent:** Your account has ID scan enabled. I'll upload the PDF, place a signature box
> and an ID scan box at the bottom of the last page, and show you a preview before anything
> is sent to her.
>
> *(preview)*
>
> **Agent:** Maria will get an email, photograph her ID card, then sign. About two minutes.
> Send it?

Three days later:

> **You:** Has Maria signed yet?
>
> **Agent:** Not yet — sent Tuesday, opened Wednesday. Shall I send a reminder? She hasn't
> had one, so there's no cooldown.

---

## Install

### Claude Code

Two steps, run one after the other — not pasted together.

Add the marketplace:

```
/plugin marketplace add formify-e-sign/formify-skills
```

Then install the plugin:

```
/plugin install formify@formify
```

### Any agent, via the skills installer

```bash
npx skills add formify-e-sign/formify-skills
```

Installs into the agent's skill directory — `.agents/skills`, which around twenty agents
read directly, with Claude Code and Eve symlinked to it.

```bash
npx skills add formify-e-sign/formify-skills --list          # see what is in here first
npx skills add formify-e-sign/formify-skills --skill formify-pdf-forms
npx skills add formify-e-sign/formify-skills -g              # global, across projects
```

**These skills contain no executable code.** Every file is Markdown or YAML — no `scripts/`,
nothing that runs. A skill is instructions an agent reads, and the usual advice to inspect
`scripts/` before installing has nothing to inspect here.

### Codex CLI

Also two steps. Add the marketplace:

```bash
codex plugin marketplace add formify-e-sign/formify-skills
```

Then install the plugin:

```bash
codex plugin add formify@formify
```

### Gemini CLI

```bash
gemini extensions install https://github.com/formify-e-sign/formify-skills
```

Installs the skills and the MCP connection together.

### Claude Desktop and claude.ai

Skills are uploaded as a ZIP: **Settings → Capabilities** (enable code execution), then
**Customize → Skills → Create skill → Upload a skill**. Zip a single skill folder from
`skills/`. Connect the MCP server separately, as above.

### In a repository, with no install at all

Clone the repo and the skills are already where most agents look — `.agents/skills` is a
symlink to `skills/`, which Codex, Cursor, Gemini CLI, Amp, opencode and Zed scan
automatically.

### Manually, anywhere

Copy the folders inside `skills/` into whatever directory your agent reads. Each skill is
self-contained: a `SKILL.md` and, where it needs one, a `references/` folder.

---

## Connect the Formify MCP server

The skills describe *how* to work with Formify. The MCP server is what actually does it —
creating documents, sending them, collecting signatures.

**Server URL:** `https://mcp.formify.eu/mcp`

**Claude (web or desktop):** Settings → Connectors → Add Connector → paste the URL. You will
be asked to log in with your Formify account.

**Claude Code:**

```bash
claude mcp add --transport http formify https://mcp.formify.eu/mcp
```

**Anything reading a plugin manifest:** the server is already declared in `mcp.json` and in
both plugin manifests, so installing the plugin offers the connection.

You authorise with your own Formify account. The skills never see your password, and every
action runs with exactly the permissions that account already has.

---


## What is in this repository

```
skills/                        the four skills — the one canonical source
  formify-pdf-forms/
  formify-send-contract/
  formify-verify-identity/
  formify-track-signatures/
.agents/skills -> skills       symlink; most agents find the skills with no install
plugin.json  mcp.json          Agent Plugins 1.0.0
.mcp.json                      the MCP server, referenced by the manifests below
.claude-plugin/                Claude Code plugin and marketplace entry
.codex-plugin/                 Codex CLI plugin, with the marketplace listing block
.agents/plugins/               Codex and ChatGPT marketplace catalogue
gemini-extension.json          Gemini CLI
package.json  skills.sh.json   npm, npx, and the skills.sh gallery
scripts/check-manifests.mjs    keeps eight manifests from drifting apart
tests/release/                 what the skills do, not just what they say
```

Every manifest describes the same `skills/` directory. Nothing is copied, so no adapter can
drift from the source — and `npm run check` proves it, in CI on every push.

Every statement these skills make about the Formify API was checked against the server
before it shipped. Four hundred and fifty-one claims inherited from the previous generation
of these skills were re-verified one at a time; the ones that turned out to be wrong were
corrected here rather than carried forward, and the ones that could not be settled were
removed rather than repeated.

`tests/release/` checks behaviour rather than structure, and two details are the reason
it exists. References are re-checked **inside an actually extracted npm tarball** rather
than in the working tree, because a path that resolves in the repository and is missing
from the published package is a defect nobody sees until a stranger installs it. And the
routing cases score an **accepted set** of skills per request rather than one correct
answer, because a request can legitimately be served two ways and a test that insists
otherwise measures the test author, not the skills.

Sixteen requests across English, Swedish and Spanish cover activation, overlap and the
negative cases where no skill should fire. The workflow cases run against a synthetic MCP
server with no network and no credentials, so a send that should have been blocked fails
because there is nothing to send with. The suite's own README states its limits: it is a
description-routing proxy, not proof of native discovery, and it establishes nothing about
the live service.

The shape of the skills comes from the same exercise. Fifty-nine real user situations were
mapped against what the platform can actually do, and eight of them were served by no skill
at all — every one of those happening *after* a document is sent. That is why
`formify-track-signatures` exists, and why there are four skills here rather than two.

---

## Contributing

Issues and pull requests are welcome. Two rules keep the skills trustworthy:

1. **A claim about the Formify API is verified against the server, or it does not ship.**
   Cite what you checked.
2. **No skill may depend on a mechanism that exists in only one agent runtime.** Where a
   harness offers something better, it is an optional enhancement with a stated fallback.

### Cutting a release

Clients decide whether to update by comparing version numbers, not content. A
changed skill with an unchanged version reaches nobody except people who cloned the
repo. So every change that ships is a version bump, and one script writes all ten
places the version lives:

```bash
npm run release 1.1.0       # six manifests and four skill frontmatters
npm run check
git commit -am "release 1.1.0" && git tag v1.1.0 && git push --follow-tags
```

`npm run release --check` is part of `npm run check` and runs in CI, so drift fails
the build. `--audit` lists files carrying the version that `.version-bump.json` does
not declare — a file added later that needs adding there. Publishing happens on the
`v*` tag alone, and refuses if the tag and the manifests disagree.

---

## License

MIT. See [LICENSE](LICENSE).
