import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { gradeWorkflow, gradeRouting } from './grade.mjs';
import { updateDraftState } from './mock-state.mjs';
const fixtures = JSON.parse(readFileSync(new URL('./fixtures/workflows.json', import.meta.url)));
test('draft grader catches lost AI, readonly mode and owner, not just signees', () => {
  const f = fixtures.find(f => f.id === 'resume-preserve');
  const result = gradeWorkflow(f, [{ tool: 'get_draft' }, { tool: 'update_draft', arguments: { draftId: 'draft-test', personalMessage: 'Thank you', signeeDetails: f.responses.get_draft.signeeDetails } }], '');
  for (const key of ['aiAssistant', 'fieldsReadonlyMode', 'userId']) assert.ok(result.some(e => e.includes(key)));
});
test('draft grader accepts complete preservation without forcing redundant fileId', () => {
  const f = fixtures.find(f => f.id === 'resume-preserve');
  const { status, fileId, ...args } = f.responses.get_draft;
  assert.deepEqual(gradeWorkflow(f, [{ tool: 'get_draft' }, { tool: 'update_draft', arguments: { ...args, personalMessage: 'Thank you' } }], ''), []);
});
test('attempted forbidden send fails even when mock rejects it', () => {
  const f = fixtures.find(f => f.id === 'prepare-only');
  assert.ok(gradeWorkflow(f, [{ tool: 'send_draft', arguments: { draftId: 'draft-test' }, result: { isError: true } }], '').some(e => e.includes('forbidden')));
});
test('prefill grader catches scalar checkbox and unlocked values', () => {
  const f = fixtures.find(f => f.id === 'prefill-lock');
  const errors = gradeWorkflow(f, [{ tool: 'get_file_fields' }, { tool: 'create_draft', arguments: { fields: [{ name: 'Consent', value: 'Yes' }] } }], '');
  assert.ok(errors.some(e => e.includes('Consent')));
  assert.ok(errors.some(e => e.includes('fieldsReadonlyMode')));
});
test('routing accepts composed send plus identity, rejects send alone', () => {
  const f = { accepted_sets: [['formify-send-contract', 'formify-verify-identity']] };
  assert.deepEqual(gradeRouting(f, { skills: [...f.accepted_sets[0]].reverse() }), []);
  assert.equal(gradeRouting(f, { skills: ['formify-send-contract'] }).length, 1);
});
test('mock readback reflects update, preserving fileId but exposing omitted configuration', () => {
  const previous = { draftId: 'd', fileId: 'f', language: 'sv', personalMessage: 'old' };
  assert.deepEqual(updateDraftState(previous, { draftId: 'd', personalMessage: 'new' }), { draftId: 'd', status: 'draft', fileId: 'f', personalMessage: 'new' });
});
