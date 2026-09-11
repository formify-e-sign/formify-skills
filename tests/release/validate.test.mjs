import test from 'node:test';
import assert from 'node:assert/strict';
import { frontmatter, validateSkill, localReferences } from './validate.mjs';

const body = ['Purpose', 'When this applies', 'When it does not', 'Preconditions', 'Procedure', 'Failure modes', 'References'].map(x => `## ${x}\nContent.`).join('\n');
const sample = desc => `---\nname: formify-example\ndescription: ${desc}\nmetadata:\n  version: "1.0.0"\n---\n${body}\n`;
test('accepts folded descriptions with a real YAML parser', () => {
  assert.deepEqual(validateSkill('formify-example', sample('>\n  Build a form.\n  Not for sending.')), []);
});
test('rejects duplicate YAML keys', () => assert.throws(() => frontmatter(sample('"Not for sending."').replace('metadata:', 'name: hidden\nmetadata:')), /unique|duplicate/i));
test('rejects a syntactically invalid unquoted colon', () => assert.throws(() => frontmatter(sample('Build a form. Not for sending: use send'))));
test('counts the entire SKILL.md, including frontmatter', () => assert.ok(validateSkill('formify-example', sample('"Not for sending."') + '\n'.repeat(490) + 'last').some(x => x.includes('500 total'))));
test('rejects malformed names, and nested but not scalar metadata', () => {
  assert.ok(validateSkill('formify--example', sample('"Not for sending."')).some(x => x.includes('name')));
  // A boolean is legal: the skills installer documents metadata.internal: true, and the
  // harnesses treat metadata as a free-form map they do not act on.
  assert.ok(!validateSkill('formify-example', sample('"Not for sending."').replace('"1.0.0"', 'true')).some(x => x.includes('metadata')));
  assert.ok(!validateSkill('formify-example', sample('"Not for sending."').replace('"1.0.0"', '42')).some(x => x.includes('metadata')));
  // Nesting is not: no consumer reads it and it is what an upload is most likely to reject.
  assert.ok(validateSkill('formify-example', sample('"Not for sending."').replace('"1.0.0"', '{ a: b }')).some(x => x.includes('metadata')));
});
test('finds markdown and code-span local references', () => assert.deepEqual(localReferences('Read `references/a.md` and [B](references/b.md#section).'), ['references/a.md', 'references/b.md']));
