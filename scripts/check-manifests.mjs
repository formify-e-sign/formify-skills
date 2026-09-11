#!/usr/bin/env node
/**
 * Manifest consistency check.
 *
 * Eight manifests describe one payload. Nothing keeps their versions, names and
 * skill lists in step except this script, and drift across them is the single
 * most common defect in published skill repositories.
 *
 * Run: node scripts/check-manifests.mjs
 */
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join } from "node:path";

const read = (p) => JSON.parse(readFileSync(p, "utf8"));
const problems = [];
const fail = (m) => problems.push(m);

const root = read("plugin.json");
const NAME = root.name;

// A sector skill is one whose frontmatter declares the countries it covers. The core
// plugin must never list one: a construction engineer installs the construction plugin
// and pays no context for real estate. Sector plugins bundle the capability skills so
// they still work on their own.
const isSector = (skill) => {
  const t = readFileSync(join("skills", skill, "SKILL.md"), "utf8");
  const fm = t.match(/^---\n([\s\S]*?)\n---\n/);
  return fm ? /^\s{2}countries:\s*\S/m.test(fm[1]) : false;
};

// 1. Every manifest agrees on the plugin name. Version agreement is checked by
// scripts/release.mjs --check, which owns every place a version is written.
const named = [
  ["plugin.json", root],
  [".claude-plugin/plugin.json", read(".claude-plugin/plugin.json")],
  [".codex-plugin/plugin.json", read(".codex-plugin/plugin.json")],
];
for (const [file, m] of named) {
  if (m.name !== NAME) fail(`${file}: name ${m.name} != ${NAME}`);
}

const market = read(".claude-plugin/marketplace.json");
const entry = market.plugins.find((p) => p.name === NAME);
if (!entry) fail(`.claude-plugin/marketplace.json: no entry named ${NAME}`);

// 2. Root plugin.json carries only the keys Agent Plugins 1.0.0 allows.
const ALLOWED = new Set(["$schema","name","version","description","author","homepage","repository","license","keywords","extensions"]);
for (const k of Object.keys(root)) {
  if (!ALLOWED.has(k)) fail(`plugin.json: "${k}" is not part of Agent Plugins 1.0.0 — skills and mcpServers belong in the per-harness manifests`);
}

// 3. Every skill on disk is reachable through some plugin, no plugin points at a skill
// that is not there, and the core plugin stays scoped to the capability layer.
//
// The shape is the one Anthropic's own `anthropics/skills` uses and the plugin-marketplace
// documentation describes: several entries share `"source": "./"`, and each entry lists the
// subdirectories it owns — "the listed paths are the complete set for that entry, and other
// directories in the shared skills/ folder don't load". An entry that lists nothing falls
// through to its plugin.json.
const onDisk = readdirSync("skills", { withFileTypes: true })
  .filter((d) => d.isDirectory())
  .map((d) => d.name)
  .sort();

const skillName = (p) => p.replace(/\/$/, "").split("/").pop();
const reachable = new Set();

for (const p of market.plugins) {
  const src = typeof p.source === "string" ? p.source : p.source?.path;
  if (!src) { fail(`.claude-plugin/marketplace.json: entry "${p.name}" has no usable source`); continue; }
  const rootDir = (src.replace(/^\.\//, "") || ".");
  const manifestPath = join(rootDir, ".claude-plugin", "plugin.json");
  const manifest = existsSync(manifestPath) ? read(manifestPath) : null;

  // Strict mode, per the documentation: with `strict: false` the entry is the whole
  // definition, and a plugin.json that also declares components is a conflict that stops
  // the plugin loading. With the default `strict: true` the two are merged, so an entry
  // may legitimately add skills on top.
  if (p.strict === false && manifest) {
    for (const k of ["skills", "mcpServers", "commands", "agents", "hooks"]) {
      if (k in manifest) {
        fail(`.claude-plugin/marketplace.json: entry "${p.name}" sets "strict": false while ${manifestPath} declares "${k}" — that is a conflict and the plugin fails to load`);
      }
    }
  }

  const declared = [...(p.skills ?? []), ...(p.strict === false ? [] : manifest?.skills ?? [])];
  if (declared.length === 0) fail(`.claude-plugin/marketplace.json: entry "${p.name}" resolves to no skills at all`);

  for (const rel of declared) {
    const s = skillName(rel);
    if (!onDisk.includes(s)) { fail(`entry "${p.name}": lists ${rel}, which is not a directory under skills/`); continue; }
    reachable.add(s);
    if (p.name === NAME && isSector(s)) {
      fail(`entry "${p.name}": the core plugin resolves the sector skill "${s}" — sector skills belong to their own entry, or every user carries every vertical`);
    }
  }
}

for (const s of onDisk) {
  if (!reachable.has(s)) fail(`skills/${s} is listed by no plugin in .claude-plugin/marketplace.json — it would never be installed`);
  // A vertical must be opt-in on the npx channel: `npx skills add owner/repo` collects every
  // plugin's skills/ directory regardless of what the manifests scope, and metadata.internal
  // is the only switch (vercel-labs/skills, src/skills.ts).
  const t = readFileSync(join("skills", s, "SKILL.md"), "utf8");
  const fm = t.match(/^---\n([\s\S]*?)\n---\n/);
  const internal = fm ? /^\s{2}internal:\s*true\s*$/m.test(fm[1]) : false;
  if (isSector(s) && !internal) {
    fail(`${s}: a sector skill must carry "internal: true" in its frontmatter metadata, or a bare \`npx skills add\` installs it for every user of every other vertical`);
  }
  if (!isSector(s) && internal) {
    fail(`${s}: a capability skill must not be internal — it is what a bare \`npx skills add\` is meant to deliver`);
  }
}

// 4. Every skill has the files it promises.
for (const s of onDisk) {
  const skillFile = join("skills", s, "SKILL.md");
  if (!existsSync(skillFile)) { fail(`${s}: no SKILL.md`); continue; }
  const text = readFileSync(skillFile, "utf8");
  const fm = text.match(/^---\n([\s\S]*?)\n---\n/);
  if (!fm) { fail(`${s}: no YAML frontmatter`); continue; }

  // Every plain scalar carrying ": " must be quoted. A strict YAML parser reads the
  // colon as a nested mapping and rejects the whole file — the skills.sh installer
  // does exactly that, and skipped all four skills before the quotes went in.
  for (const line of fm[1].split("\n")) {
    const kv = line.match(/^([A-Za-z0-9_-]+):[ \t]+(.+)$/);
    if (kv && !/^['"]/.test(kv[2]) && /:[ \t]/.test(kv[2])) {
      fail(`${s}: frontmatter "${kv[1]}" holds an unquoted value containing ": " — strict YAML parsers reject the file; wrap the value in single quotes`);
    }
  }

  const unquote = (v) => v?.replace(/^'(.*)'$/s, "$1").replace(/^"(.*)"$/s, "$1");
  const name = unquote(fm[1].match(/^name:\s*(.+)$/m)?.[1]?.trim());
  const desc = unquote(fm[1].match(/^description:\s*(.+)$/m)?.[1]?.trim());
  if (name !== s) fail(`${s}: frontmatter name "${name}" does not match its directory`);
  if (!desc) { fail(`${s}: no description`); continue; }

  // The authoring standard: 500 hard, and the first 60 characters must still work.
  if (desc.length > 500) fail(`${s}: description ${desc.length} chars, limit 500`);
  const body = text.slice(fm[0].length);
  const lines = body.split("\n").length;
  if (lines > 500) fail(`${s}: SKILL.md body ${lines} lines, limit 500`);

  // Every referenced file exists.
  for (const m of body.matchAll(/`references\/([A-Za-z0-9._-]+\.md)`/g)) {
    if (!existsSync(join("skills", s, "references", m[1]))) {
      fail(`${s}: references/${m[1]} is named in SKILL.md but not present`);
    }
  }

  // No skill may point at another skill's files. The Agent Skills specification has
  // no skill-to-skill references, and every upload surface takes one skill per zip,
  // so such a pointer dangles the moment the skill is installed on its own.
  for (const m of body.matchAll(/`(formify-[a-z-]+)\/(references|scripts|assets)\//g)) {
    if (m[1] !== s) fail(`${s}: points at ${m[1]}/${m[2]}/ — cross-skill references do not survive a single-skill install; add the file to shared/shared.json instead`);
  }
}

// 4b. Every skill carries the per-harness files the others carry. A skill added without
// them is not broken, it is quietly less installable than its siblings — which is exactly
// the kind of drift nobody notices until a listing looks wrong.
for (const s of onDisk) {
  if (!existsSync(join("skills", s, "agents", "openai.yaml"))) {
    fail(`${s}: no agents/openai.yaml — every other skill has one, and it is what names the skill on OpenAI surfaces`);
  }
  if (!existsSync(join("tests", "evals", s, "evals.json"))) {
    fail(`${s}: no tests/evals/${s}/evals.json — a skill ships with its trigger and behaviour evals or it ships unverified`);
  }
}

// 5. One MCP endpoint, spelled per-harness, never two different URLs.
const URL = "https://mcp.formify.eu/mcp";
const urls = [
  ["mcp.json", read("mcp.json").mcpServers.formify.url],
  [".mcp.json", read(".mcp.json").mcpServers.formify.url],
];
for (const p of market.plugins) {
  const src = typeof p.source === "string" ? p.source : p.source?.path;
  const f = join((src ?? ".").replace(/^\.\//, "") || ".", ".mcp.json");
  if (f !== ".mcp.json" && existsSync(f)) urls.push([f, read(f).mcpServers.formify.url]);
}
for (const [file, u] of urls) if (u !== URL) fail(`${file}: MCP url ${u} != ${URL}`);

// 6. Every file a manifest points at is inside the npm allowlist. A path that
// resolves in the repository but is missing from the published tarball is a
// broken icon or a missing context file for anyone installing from npm.
const allow = read("package.json").files ?? [];
const packed = (rel) => allow.some((a) => rel === a || rel.startsWith(a.replace(/\/$/, "") + "/"));
const pointed = [
  [".codex-plugin/plugin.json", read(".codex-plugin/plugin.json").interface?.iconSmall],
  [".codex-plugin/plugin.json", read(".codex-plugin/plugin.json").interface?.iconLarge],
];
for (const [file, ref] of pointed) {
  if (!ref) continue;
  const rel = ref.replace(/^\.\//, "");
  if (!existsSync(rel)) fail(`${file}: points at ${ref}, which does not exist`);
  else if (!packed(rel)) fail(`${file}: points at ${ref}, which package.json "files" does not publish — it would dangle for anyone installing from npm`);
}

// 7. No manifest may resolve a path through a symlink. npm silently drops symlinks when it
// packs, so anything reached through one works from a git clone and is simply absent for
// every npm and npx install — with no error on either side. Verified by packing the tarball.
//
// `.agents/skills` is the one deliberate exception and is allowlisted below: nothing in any
// manifest resolves through it. It exists so that a cloned checkout already has its skills
// where the ~22 agents that scan `.agents/skills` will find them, which is a git-clone
// affordance by definition.
const SYMLINK_OK = new Set([join(".agents", "skills")]);
for (const dir of ["skills", ".claude-plugin", ".codex-plugin", ".agents", "assets"]) {
  const walk = (d) => {
    for (const e of readdirSync(d, { withFileTypes: true })) {
      const full = join(d, e.name);
      if (e.isSymbolicLink() && !SYMLINK_OK.has(full)) fail(`${full} is a symbolic link — npm drops symlinks when packing, so it would be missing for every npm and npx install`);
      else if (e.isDirectory()) walk(full);
    }
  };
  if (existsSync(dir)) walk(dir);
}

if (problems.length) {
  console.error("Manifest check failed:\n" + problems.map((p) => "  - " + p).join("\n"));
  process.exit(1);
}
console.log(`Manifests consistent: ${market.plugins.length} plugins (${market.plugins.map((p) => p.name).join(", ")}), ${onDisk.length} skills (${onDisk.join(", ")})`);
