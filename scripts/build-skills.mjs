#!/usr/bin/env node
/**
 * Copy shared references into every skill that declares them.
 *
 * The Agent Skills specification defines no skill-to-skill references, and every
 * upload surface (claude.ai, ChatGPT, Manus, the Claude and OpenAI skills APIs)
 * takes exactly one self-contained skill per zip. A file needed by two skills is
 * therefore duplicated on disk — but authored once, here, and copied by this
 * script. `--check` fails instead of writing, which is what CI runs.
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";

const check = process.argv.includes("--check");
const map = JSON.parse(readFileSync("shared/shared.json", "utf8"));
const stale = [];
let copied = 0;

for (const [rel, skills] of Object.entries(map)) {
  if (rel === "//") continue;
  const src = join("shared", rel);
  const source = readFileSync(src, "utf8");
  const banner = `<!-- Generated from ${src} by scripts/build-skills.mjs. Edit the source, not this copy. -->\n`;
  const wanted = banner + source;

  for (const skill of skills) {
    const dest = join("skills", skill, rel);
    const current = existsSync(dest) ? readFileSync(dest, "utf8") : null;
    if (current === wanted) continue;
    if (check) { stale.push(`${dest} is out of date with ${src}`); continue; }
    mkdirSync(dirname(dest), { recursive: true });
    writeFileSync(dest, wanted);
    copied++;
  }
}

if (check && stale.length) {
  console.error("Shared references are stale:\n" + stale.map((s) => "  - " + s).join("\n") +
                "\nRun: node scripts/build-skills.mjs");
  process.exit(1);
}
console.log(check ? "Shared references up to date." : `Shared references written: ${copied} file(s).`);
