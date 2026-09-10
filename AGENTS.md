# AGENTS.md

Contract for any agent working **on** this repository — Claude Code, Codex, or another
harness. Read it before changing anything under `skills/`.

If you are here to *use* Formify's skills rather than to change them, `README.md` is the
right file: this one is about how the skills are built and what makes one finished.

---

## 1. What this repository is

Formify is an electronic-signature and identity-verification platform. Its capabilities
reach AI agents through two surfaces:

- **The Formify MCP server** — the tool layer. Templates, drafts, documents, signees, files,
  field values, webhooks, reminders.
- **Formify skills** — the knowledge layer, and what this repository produces. Skills turn
  a set of tools into competence: when to reach for which tool, what a good contract looks
  like, how a signature field must be placed, what a `tink-*` attribute means.

### What a skill is judged on

Two things, in this order:

1. **Discoverability.** A skill that never activates has zero value regardless of its
   content. The `description` field is the only signal a model uses to decide whether to
   open a skill. Discoverability is a measurable property, not a matter of taste — see §6.
2. **Substance.** Once open, a skill must contain knowledge the model does not already
   have: real API shapes, real field-placement geometry, real validation rules. Generic
   advice is worse than no skill, because it costs context and returns nothing.

### Distribution

These skills are installed far beyond coding harnesses, so reach constrains how they are
written:

| Channel | Examples |
|---|---|
| Coding-agent harnesses | Claude Code, Codex, Cursor, and successors |
| Assistant products | Claude Desktop, ChatGPT, Manus |
| Skill and MCP marketplaces | public agent-skill directories |
| Package registries | the `npx` installer |

---

## 2. How a skill must be written

Four rules, all binding.

**Harness-neutral.** A skill body may not assume a tool name, a UI affordance, or a
slash-command mechanism that exists in only one runtime. Where a harness-specific capability
genuinely improves the result, it is declared as an optional enhancement with a stated
fallback, never as the main path.

**Environment-free.** Most people reach these skills through a chat product, not a terminal.
A skill may not assume a working directory, a repository, a shell, or the ability to read and
write local files. Anything the skill needs comes from the conversation or from the Formify
MCP server. A procedure that only works with a filesystem is a coding-agent enhancement, not
the main path.

**It makes its own capabilities visible.** The people using these skills do not read
documentation and do not know what a skill is. Discoverability is not only "does the model
open this skill" — it is also "does the person now understand what they can do". A skill that
works perfectly but leaves the user unaware of what was possible has failed at the thing that
actually matters.

**It is delightful on first contact, not merely correct.** A first interaction that explains,
offers concrete starting points, and produces a real document is the product demo.

The full authoring standard — line budgets, `description` design, what belongs in
`references/` — lives in the rules loaded alongside `skills/**`.

---

## 3. Language policy

- **Everything committed to this repository is written in English** — skill bodies,
  documentation, comments, identifiers, commit messages, file names.
- Non-English **trigger phrases** inside a skill's `description` are content, not
  language. Formify's users work in Swedish and other European languages; a skill that
  only triggers on English phrasing fails half its audience. Trigger phrases in any
  language are welcome and expected in `description`.
- Conversation between a human and an agent may be in any language. The artifact is not.

---

## 4. Repository layout

```
formify-skills/
├── AGENTS.md              # this file — the contract
├── README.md              # for people installing and using the skills
├── skills/                # the deliverable
├── shared/                # reference material authored once, copied at build
├── scripts/               # build, release, and manifest checks
├── tests/                 # eval suites and the release verification layer
├── assets/                # icons and brand artwork
├── demo/                  # recorded demonstrations
├── .agents/               # universal skill path and plugin marketplace
├── .claude-plugin/        # Claude Code plugin manifest
├── .codex-plugin/         # Codex plugin manifest
└── plugin.json, mcp.json, gemini-extension.json, skills.sh.json
```

Every manifest above claims the same MCP URL, the same skill list, and the same icons. They
drift silently, so `scripts/check-manifests.mjs` asserts they agree and that no manifest
points at a file the npm tarball does not publish. Run it before opening a pull request.

Two directories exist on disk and are deliberately not committed: `tasks/`, the agents' live
coordination file, and `docs/`, the working analysis behind the skills. Both name what could
not be verified about the API and what the platform cannot yet do, so they stay local. The
verification they record is claimed in `README.md`, where a reader of the product can act
on it.

---

## 5. Verification

Claims in a skill are verified, not remembered. A statement about the Formify API is checked
against the MCP server's own source before it ships; a claim that contradicts the server is a
bug, not a difference of opinion. The previous generation of these skills is a source of
questions worth re-asking, never of answers to copy.

What that verification currently proves, and what it does not, is stated in `README.md` and
implemented under `tests/`.

---

## 6. Definition of done for a skill

A skill is finished when all five hold:

1. **It activates.** Realistic user phrasings — in every language it claims to serve —
   cause the skill to be selected. Verified, not assumed.
2. **It fits its budget.** `SKILL.md` stays inside the line budget set by the authoring
   standard; anything larger lives in `references/` and is loaded on demand.
3. **Its claims are true.** Every statement about the Formify API is checked against the
   MCP server's source.
4. **It is harness-neutral.** No dependency on a mechanism that exists in only one agent
   runtime, except as a declared optional enhancement with a fallback.
5. **It carries knowledge.** Content a competent model would not already produce
   unprompted. Domain substance, not restated generalities.
