import { readFileSync, readdirSync, existsSync, realpathSync, statSync } from 'node:fs';
import { resolve, relative, dirname, join } from 'node:path';
import { parseDocument } from 'yaml';

export function frontmatter(text) {
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!match) throw new Error('missing YAML frontmatter');
  const doc = parseDocument(match[1], { uniqueKeys: true });
  if (doc.errors.length) throw new Error(doc.errors.map(e => e.message).join('; '));
  const data = doc.toJS({ maxAliasCount: 20 });
  if (!data || typeof data !== 'object' || Array.isArray(data)) throw new Error('frontmatter must be a mapping');
  return { data, body: text.slice(match[0].length) };
}

export function validateSkill(name, text) {
  const errors = [];
  let parsed;
  try { parsed = frontmatter(text); } catch (e) { return [e.message]; }
  const { data, body } = parsed;
  if (data.name !== name || !/^formify-[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name) || name.length > 64) errors.push('invalid or mismatched name');
  if (typeof data.description !== 'string' || !data.description.trim() || [...data.description].length > 500) errors.push('description must contain 1–500 characters (Formify limit)');
  if (typeof data.description === 'string' && !/Not for /i.test(data.description)) errors.push('description has no negative boundary');
  if (data.compatibility !== undefined && (typeof data.compatibility !== 'string' || !data.compatibility.length || data.compatibility.length > 500)) errors.push('invalid compatibility');
  for (const key of ['license', 'allowed-tools']) if (data[key] !== undefined && typeof data[key] !== 'string') errors.push(`${key} must be a string`);
  if (data.metadata !== undefined && (!data.metadata || Array.isArray(data.metadata) || typeof data.metadata !== 'object' || Object.values(data.metadata).some(v => typeof v !== 'string'))) errors.push('metadata must map strings to strings');
  if (text.trimEnd().split(/\r?\n/).length > 500) errors.push('SKILL.md exceeds 500 total lines');
  if (!body.trim()) errors.push('empty skill body');
  for (const marker of ['Purpose', 'When this applies', 'When it does not', 'Preconditions', 'Procedure', 'Failure modes', 'References']) {
    if (!new RegExp(`^## ${marker}$`, 'm').test(body)) errors.push(`missing section: ${marker}`);
  }
  // A lint signal only; optional harness instructions need human review, not an automatic ban.
  if (/\/(?:Users|home|mnt\/data)\//.test(body)) errors.push('absolute user or sandbox path in body');
  return errors;
}

export function localReferences(text) {
  return [...new Set([
    ...[...text.matchAll(/`((?:references|scripts|assets)\/[^`]+)`/g)].map(m => m[1]),
    ...[...text.matchAll(/\]\(((?:\.\/)?(?:references|scripts|assets)\/[^)#\s]+)(?:#[^)]*)?\)/g)].map(m => m[1])
  ])];
}

export function checkRoot(root) {
  const failures = [];
  const fail = (path, message) => failures.push({ path, message });
  const read = p => readFileSync(join(root, p), 'utf8');
  const json = p => JSON.parse(read(p));
  const confined = (base, path) => {
    const target = resolve(base, path);
    if (relative(base, target).startsWith('..')) return false;
    return existsSync(target) && !relative(realpathSync(base), realpathSync(target)).startsWith('..');
  };
  const skills = readdirSync(join(root, 'skills'), { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name).sort();
  const inventory = [];
  for (const skill of skills) {
    const file = `skills/${skill}/SKILL.md`;
    if (!existsSync(join(root, file))) { fail(file, 'missing'); continue; }
    const text = read(file);
    validateSkill(skill, text).forEach(message => fail(file, message));
    let parsed;
    try { parsed = frontmatter(text); } catch { continue; }
    inventory.push({ skill, lines: text.trimEnd().split(/\r?\n/).length, descriptionCharacters: [...String(parsed.data.description)].length, prefix60: String(parsed.data.description).slice(0, 60) });
    const base = join(root, 'skills', skill);
    for (const ref of localReferences(text)) if (!confined(base, ref)) fail(file, `missing or escaping reference: ${ref}`);
    if (existsSync(join(base, 'commands'))) fail(file, 'commands/ is forbidden by the Formify authoring standard');
  }
  // Check actual path targets, including storefront assets and extension context files.
  for (const manifest of ['.claude-plugin/plugin.json', '.codex-plugin/plugin.json', 'gemini-extension.json']) {
    try {
      const data = json(manifest);
      const declared = Array.isArray(data.skills) ? data.skills : data.skills ? [data.skills] : [];
      for (const p of [...declared, ...(typeof data.mcpServers === 'string' ? [data.mcpServers] : []), ...(data.contextFileName ? [data.contextFileName] : [])]) {
        if (!confined(root, p)) fail(manifest, `missing or escaping target: ${p}`);
      }
      if (Array.isArray(data.skills)) {
        const listed = data.skills.map(p => p.replace(/^\.\/skills\//, '').replace(/\/$/, '')).sort();
        if (JSON.stringify(listed) !== JSON.stringify(skills)) fail(manifest, 'skill list differs from payload');
      }
      for (const [key, value] of Object.entries(data.interface ?? {})) {
        const paths = Array.isArray(value) ? value : [value];
        for (const p of paths) if (typeof p === 'string' && p.startsWith('./') && !confined(root, p)) fail(manifest, `missing interface.${key}: ${p}`);
      }
    } catch (e) { fail(manifest, e.message); }
  }
  return { failures, inventory };
}
