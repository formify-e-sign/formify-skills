import { isDeepStrictEqual } from 'node:util';
const at = (object, path) => path.split('.').reduce((v, k) => v?.[k], object);

export function gradeWorkflow(fixture, calls, answer) {
  const errors = [];
  const names = calls.map(c => c.tool);
  const expected = fixture.expect;
  for (const t of expected.required ?? []) if (!names.includes(t)) errors.push(`missing ${t}`);
  for (const t of expected.forbidden ?? []) if (names.includes(t)) errors.push(`forbidden ${t} attempted`);
  for (const [first, second] of expected.before ?? []) if (names.includes(second) && (names.indexOf(first) < 0 || names.indexOf(first) > names.indexOf(second))) errors.push(`${first} must precede ${second}`);
  for (const [tool, values] of Object.entries(expected.arguments ?? {})) {
    const matches = calls.filter(c => c.tool === tool);
    if (!matches.length) errors.push(`no ${tool} payload to inspect`);
    for (const c of matches) for (const [path, value] of Object.entries(values)) if (!isDeepStrictEqual(at(c.arguments, path), value)) errors.push(`${tool}.${path} expected ${JSON.stringify(value)}, got ${JSON.stringify(at(c.arguments, path))}`);
  }
  for (const [tool, paths] of Object.entries(expected.absent ?? {})) for (const c of calls.filter(c => c.tool === tool)) for (const path of paths) if (at(c.arguments, path) !== undefined) errors.push(`${tool}.${path} should be absent`);
  if (expected.preserve) for (const c of calls.filter(c => c.tool === 'update_draft')) {
    for (const [key, value] of Object.entries(fixture.responses.get_draft)) {
      if (['draftId', 'status', 'fileId', 'personalMessage'].includes(key)) continue;
      if (!isDeepStrictEqual(c.arguments[key], value)) errors.push(`update_draft lost or changed ${key}`);
    }
    if (c.arguments.fileId !== undefined && c.arguments.fileId !== fixture.responses.get_draft.fileId) errors.push('update_draft changed fileId');
  }
  if (expected.prefill) for (const c of calls.filter(c => c.tool === 'create_draft')) {
    const fields = c.arguments.fields ?? [];
    for (const [name, value] of [['Consent', ['Yes']], ['Plan', ['Basic']]]) if (!isDeepStrictEqual(fields.find(f => f.name === name)?.value, value)) errors.push(`incorrect ${name} field value`);
    if (fields.some(f => f.name === 'Notes' || f.value === '')) errors.push('blank field was sent instead of omitted');
  }
  for (const word of expected.answer_contains ?? []) if (!answer.toLowerCase().includes(word.toLowerCase())) errors.push(`answer omits ${word}`);
  // A regional variant is only proved by what the answer does NOT say. Citing the default
  // Codigo Civil article in Catalonia or Navarra is the exact failure this catches.
  for (const word of expected.answer_excludes ?? []) if (answer.toLowerCase().includes(word.toLowerCase())) errors.push(`answer wrongly cites ${word}`);
  for (const call of calls) if (call.result?.isError) errors.push(`fixture rejected ${call.tool}`);
  return errors;
}

export function gradeRouting(fixture, result) {
  const got = [...new Set(result.skills ?? [])].sort();
  const errors = [];
  if (!fixture.accepted_sets.some(set => isDeepStrictEqual([...set].sort(), got))) errors.push(`unexpected skills ${JSON.stringify(got)}`);
  if (fixture.clarification_required && result.clarify !== true) errors.push('ambiguous request requires clarification');
  return errors;
}
