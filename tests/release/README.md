# First-release verification

Run from the repository root (Node.js 22 or newer):

```sh
npm ci --prefix tests/release --ignore-scripts
npm test --prefix tests/release
node tests/release/check.mjs
node tests/release/evaluate.mjs --mode routing
node tests/release/evaluate.mjs --mode workflow
node tests/release/codex-smoke.mjs
```

`check.mjs` runs the existing checks without changing their files, validates YAML with a real parser, checks the whole SKILL.md line budget and local references, validates the Claude manifests with the installed CLI, then creates and extracts an actual npm tarball in a temporary directory. It checks references again inside that distribution artifact. It never publishes or installs the package into a user's harness. A nonzero exit is a failing check, including an unavailable Claude executable. JSON results go to `reports/static.json`.

The name/frontmatter checks implement a subset of the [Agent Skills specification](https://agentskills.io/specification), plus Formify's stricter 500-character description and 500-total-line limits. YAML parsing uses the documented [yaml v2 parser](https://eemeli.org/yaml/). This is not a claim of complete marketplace-schema certification. The 60-character prefixes are recorded for human review; semantic usefulness is not proved by character counting.

`evaluate.mjs --mode routing` gives the model the actual four descriptions and sixteen English, Swedish, Spanish, overlapping and unrelated requests. It scores allowed sets, not one fixed skill per request. **This is a batched description-routing proxy, not proof of native discovery or independent trials.** It disables skills and all built-in tools and configures zero MCP servers. It uses the installed Claude CLI's default model.

`evaluate.mjs --mode workflow` runs each fixture as a separate Claude session. The actual four skill directories are copied into a temporary plugin. The production manifests, MCP configuration and hooks are not copied. Only the built-in `Skill` tool and the local fixture MCP are offered; no shell, browser or real Formify connector is available. The runner records actual `Skill` invocations and MCP calls, and scores payloads and forbidden attempts deterministically. Use `--case prepare-only` to run one scenario. Each completed case is saved immediately.

The fixture server is deliberately smaller than the real API: 22 tool names, simplified descriptions and partial input schemas, with synthetic responses. It cannot establish backend behavior, production OAuth, complete tool-schema compliance, renderer correctness, competing installed-skill behavior or all 35-tool selection. No network client or Formify credentials exist in the server. Unscripted calls return errors and are still recorded, so a forbidden send attempt fails even though nothing was sent. These tests need authenticated Claude model access and consume model quota. Each model invocation has a 120-second timeout and a $2 API-budget ceiling; that is not a total-suite budget.

`fixtures/workflows.json` cites the source of each expected rule. `MCP/src/tools.ts` refers to the separately maintained Formify MCP server; its source is not bundled or required to run these fixtures. These expectations are a dated contract snapshot, not generated truth. Recheck them when the server changes. Mock responses are synthetic examples, not a guaranteed backend response schema.

Reports include model usage, native skill invocations, tool arguments, fixture responses and SHA-256 hashes of the exact skill snapshot tested. `reports/` and `node_modules/` are ignored locally. Never commit real account data into fixtures or reports. Inspect `docs/release-readiness.md` for the human handoff and remaining coverage.

## Remaining release evidence

- Native positive, negative and overlap activation across all claimed languages, repeated trials, and comparison with a no-skill baseline. Current native fixtures primarily exercise send/track/identity; PDF activation and visual PDF output need separate evidence.
- Complete signature-method and delivery combinations, authentication failure, preview failure, signee ID changes, reminder cooldown execution, upload routes and recipient correction. Current fixtures cover a selected first-release risk set, not this entire list.
- Fresh-install tests in Claude Code, Codex, OpenCode and Cursor. A manifest passing validation is not an installation test.
- Controlled real-account send/sign/retrieve checks using explicitly approved test recipients and spending. No such sends are performed by this suite.

Release status must remain unverified where those checks have not run. Do not turn a passing fixture trace into a claim that all harnesses or the live Formify service pass.

## Codex smoke

`codex-smoke.mjs` copies the skill snapshot into a temporary `.agents/skills` directory and runs two native CLI cases. It ignores user configuration, disables apps/plugins/subagents, retains a read-only shell sandbox, and configures only the local synthetic MCP server. Approval is granted to that server only through command-line overrides; no user's settings are written. See [the official MCP configuration options](https://developers.openai.com/codex/mcp). The CLI default model is retained. Native skill read commands are retained as evidence for human review; a model claiming to have used a skill is not sufficient evidence. Reports distinguish workflow grading from skill-read evidence. This is not a Codex plugin marketplace installation test.
