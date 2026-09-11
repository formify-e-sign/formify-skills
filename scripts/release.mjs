#!/usr/bin/env node
// The version lives in several manifests and in every skill's frontmatter.
// This is the only thing that writes them, so they cannot drift.
//
//   node scripts/release.mjs 1.1.0   bump every declared place
//   node scripts/release.mjs --check every declared place agrees (runs in CI)
//   node scripts/release.mjs --audit find files carrying the version that are not declared
//
// It stops at the working tree: no commit, no tag, no publish. Those stay human.

import { readFileSync, writeFileSync, existsSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { execFileSync } from "node:child_process";

const CONFIG = ".version-bump.json";
const cfg = JSON.parse(readFileSync(CONFIG, "utf8"));

const problems = [];
const note = (m) => problems.push(m);

// --- reading and writing one declared place -------------------------------

const dig = (obj, path) =>
  path.split(".").reduce((o, k) => (o == null ? o : o[/^\d+$/.test(k) ? Number(k) : k]), obj);

function setDeep(obj, path, value) {
  const keys = path.split(".").map((k) => (/^\d+$/.test(k) ? Number(k) : k));
  const last = keys.pop();
  const parent = keys.reduce((o, k) => o[k], obj);
  parent[last] = value;
}

const jsonPlace = ({ path, field }) => ({
  path,
  where: field,
  read() {
    if (!existsSync(path)) return null;
    return dig(JSON.parse(readFileSync(path, "utf8")), field) ?? null;
  },
  write(v) {
    const data = JSON.parse(readFileSync(path, "utf8"));
    setDeep(data, field, v);
    writeFileSync(path, JSON.stringify(data, null, 2) + "\n");
  },
});

// A skill's frontmatter, matched inside the --- block so a body mention is never touched.
const skillPlace = (path, field) => {
  const leaf = field.split(".").pop();
  const re = new RegExp(`(^---\\n[\\s\\S]*?^\\s*${leaf}:\\s*")([^"]*)(")`, "m");
  return {
    path,
    where: field,
    read() {
      const m = readFileSync(path, "utf8").match(re);
      return m ? m[2] : null;
    },
    write(v) {
      const text = readFileSync(path, "utf8");
      if (!re.test(text)) { note(`${path}: no quoted ${field} in frontmatter`); return; }
      writeFileSync(path, text.replace(re, `$1${v}$3`));
    },
  };
};

// A field may carry one `*` segment, which fans out over an array. Every marketplace entry
// has its own version, and a list would silently miss the next one added.
function expand(entry) {
  if (!entry.field.includes("*")) return [entry];
  if (!existsSync(entry.path)) return [entry];
  const [before] = entry.field.split(".*.");
  const arr = dig(JSON.parse(readFileSync(entry.path, "utf8")), before);
  if (!Array.isArray(arr)) return [entry];
  return arr.map((_, i) => ({ ...entry, field: entry.field.replace(".*.", `.${i}.`) }));
}

function places() {
  const out = cfg.files.flatMap(expand).map(jsonPlace);
  if (cfg.skills) {
    const [dir, , file] = cfg.skills.glob.split("/");
    for (const d of readdirSync(dir, { withFileTypes: true })) {
      if (!d.isDirectory()) continue;
      const p = join(dir, d.name, file);
      if (existsSync(p)) out.push(skillPlace(p, cfg.skills.field));
      else note(`${p}: declared by ${CONFIG} but missing`);
    }
  }
  return out;
}

// --- the three modes -------------------------------------------------------

const SEMVER = /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/;
const cmp = (a, b) => {
  const p = (v) => v.split("-")[0].split(".").map(Number);
  const [x, y] = [p(a), p(b)];
  for (let i = 0; i < 3; i++) if (x[i] !== y[i]) return x[i] - y[i];
  return 0;
};

const current = () => {
  const v = jsonPlace(cfg.files[0]).read();
  if (!v) { console.error(`error: no version in ${cfg.files[0].path}`); process.exit(1); }
  return v;
};

function check(quiet = false) {
  const want = current();
  const all = places();
  for (const p of all) {
    const got = p.read();
    if (got === null) note(`${p.path}: no ${p.where}`);
    else if (got !== want) note(`${p.path}: ${p.where} is ${got}, expected ${want}`);
  }
  if (problems.length) {
    console.error(`Version drift (expected ${want}):`);
    for (const m of problems) console.error(`  ${m}`);
    process.exit(1);
  }
  if (!quiet) console.log(`Version ${want} agrees across ${all.length} places.`);
}

function audit() {
  const want = current();
  const declared = new Set(places().map((p) => p.path));
  const exclude = new Set(cfg.audit?.exclude ?? []);
  const tracked = execFileSync("git", ["ls-files"], { encoding: "utf8" }).trim().split("\n");
  const stray = [];
  for (const f of tracked) {
    if (declared.has(f) || exclude.has(f) || !existsSync(f)) continue;
    if (exclude.has(f.split("/")[0])) continue;
    let text;
    try { text = readFileSync(f, "utf8"); } catch { continue; }
    if (text.includes(want)) stray.push(f);
  }
  console.log(`Version ${want} is declared in ${declared.size} places.`);
  if (!stray.length) { console.log("No undeclared file carries it."); return; }
  console.log(`\nCarrying ${want} but not declared in ${CONFIG}:`);
  for (const f of stray) console.log(`  ${f}`);
  console.log(`\nEach is either prose (fine) or a place that must be declared.`);
}

function bump(next) {
  if (!SEMVER.test(next)) { console.error(`error: "${next}" is not a semver version`); process.exit(1); }
  const now = current();
  if (cmp(next, now) <= 0) { console.error(`error: ${next} is not newer than ${now}`); process.exit(1); }

  const dirty = execFileSync("git", ["status", "--porcelain"], { encoding: "utf8" }).trim();
  if (dirty) { console.error("error: working tree is not clean — commit or stash first, so a failed bump can be reverted with git checkout"); process.exit(1); }

  // Read everything before writing anything: a file that cannot be parsed
  // stops the bump while the tree is still untouched.
  const all = places();
  for (const p of all) if (p.read() === null) note(`${p.path}: no ${p.where}`);
  if (problems.length) {
    console.error("Refusing to bump:");
    for (const m of problems) console.error(`  ${m}`);
    process.exit(1);
  }

  for (const p of all) p.write(next);
  if (problems.length) {
    console.error("Bump failed partway; run: git checkout -- .");
    for (const m of problems) console.error(`  ${m}`);
    process.exit(1);
  }

  check(true);
  console.log(`${now} → ${next} in ${all.length} places.\n`);
  for (const p of all) console.log(`  ${p.path}`);
  console.log(`\nNothing was committed. Next:\n  npm run check\n  git commit -am "release ${next}" && git tag v${next} && git push --follow-tags`);
}

const arg = process.argv[2];
if (arg === "--check") check();
else if (arg === "--audit") audit();
else if (arg && !arg.startsWith("-")) bump(arg);
else { console.error("usage: release.mjs <version> | --check | --audit"); process.exit(1); }
