import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

test('every mock tool name exists in the authoritative 35-tool snapshot', () => {
  const known = JSON.parse(readFileSync(new URL('./fixtures/tool-names.json', import.meta.url))).names;
  const mock = readFileSync(new URL('./mock-mcp.mjs', import.meta.url), 'utf8');
  const names = [...mock.matchAll(/^  \['([a-z_]+)',/gm)].map(m => m[1]);
  assert.equal(known.length, 35);
  assert.equal(names.length, 22);
  assert.equal(new Set(names).size, names.length);
  assert.deepEqual(names.filter(n => !known.includes(n)), []);
});
