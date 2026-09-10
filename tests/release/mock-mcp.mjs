// Isolated fixture server: no HTTP client, credentials, shell execution or Formify connection.
// This deliberately implements a small test surface, not the complete Formify API schema.
import { createInterface } from 'node:readline';
import { readFileSync, appendFileSync } from 'node:fs';
import { updateDraftState } from './mock-state.mjs';

const [fixturePath, logPath] = process.argv.slice(2);
const fixture = JSON.parse(readFileSync(fixturePath, 'utf8'));
const str = { type: 'string' };
const array = { type: 'array', items: { type: 'object', additionalProperties: true } };
const box = { type: 'object', properties: { x: { type: 'number' }, y: { type: 'number' }, page: { type: 'integer' }, scale: { type: 'number', minimum: 0.25, maximum: 1.5 } }, required: ['x', 'y', 'page'], additionalProperties: false };
const signees = { type: 'array', items: { type: 'object', additionalProperties: false, properties: {
  fullName: str, emailAddress: str, phoneNumber: { type: 'string', description: 'Phone number with country code.' },
  phoneNumberDeliveryMethod: { enum: ['sms', 'whatsapp'] }, signaturePlacement: { enum: ['new_page', 'existing'] },
  signatureType: { enum: ['digital_ink', 'bankid_identification', 'digital_ink_id_scan', 'face_liveness'] },
  signingOrder: { type: 'integer' }, disableInvitationMessage: { type: 'boolean' }, signatureBox: box, idScanBox: box
} } };
const fields = { type: 'array', items: { type: 'object', properties: { name: str, value: { anyOf: [str, { type: 'array', items: str }] } }, required: ['name', 'value'], additionalProperties: false } };
const config = { fileId: str, name: str, userId: str, signeeDetails: signees, fields,
  fieldsReadonlyMode: { enum: ['keepOriginal', 'filled', 'all'] }, language: { enum: ['en', 'sv', 'es'] },
  sharingSetting: { enum: ['private', 'shared'] }, personalMessage: { type: 'string', maxLength: 500 }, enableSigningOrder: { type: 'boolean' },
  aiAssistant: { type: 'object', properties: { enabled: { type: 'boolean' }, language: str, textToSpeech: { type: 'boolean' } }, additionalProperties: false } };
const definitions = [
  ['get_account_capabilities', 'Get available account capabilities.', {}],
  ['list_templates', 'List saved templates.', {}],
  ['get_template', 'Read a template and its configured signees.', { templateId: str }, ['templateId']],
  ['get_template_fields', 'Read template form field definitions.', { templateId: str }, ['templateId']],
  ['get_file_fields', 'Read PDF field definitions, names, types and editability.', { fileId: str }, ['fileId']],
  ['create_draft', 'Create an unsent draft from an uploaded file.', config, ['fileId', 'name']],
  ['get_draft', 'Read current saved draft state.', { draftId: str }, ['draftId']],
  ['update_draft', 'Update a saved draft configuration.', { draftId: str, ...config }, ['draftId']],
  ['send_draft', 'Send a saved draft as a live signing document.', { draftId: str }, ['draftId']],
  ['create_document', 'Create and send a live signing document.', { templateId: str, ...config }],
  ['get_draft_file_url', 'Get a draft PDF preview URL.', { draftId: str }, ['draftId']],
  ['get_draft_file', 'Get a draft PDF preview.', { draftId: str }, ['draftId']],
  ['get_document', 'Read current document and signee state.', { documentId: str }, ['documentId']],
  ['send_reminder', 'Send a reminder to specified signees.', { documentId: str, signeeIds: { type: 'array', items: str } }, ['documentId', 'signeeIds']],
  ['update_signee', 'Correct existing signee contact details.', { documentId: str, signees: array }, ['documentId', 'signees']],
  ['get_document_fields', 'Read document field definitions.', { documentId: str }, ['documentId']],
  ['get_document_field_values', 'Read current document field values.', { documentId: str }, ['documentId']],
  ['set_document_field_values', 'Change editable document field values.', { documentId: str, fields: array }, ['documentId', 'fields']],
  ['revoke_document', 'Revoke a live document.', { documentId: str }, ['documentId']],
  ['delete_document', 'Delete a document and associated file.', { documentId: str }, ['documentId']],
  ['get_recipient_links', 'Get personal signing links for a sent document.', { documentId: str }, ['documentId']],
  ['get_signed_document_url', 'Get completed signed PDF URL.', { documentId: str }, ['documentId']]
];
const tools = definitions.map(([name, description, properties, required = []]) => ({ name, description, inputSchema: { type: 'object', properties, required, additionalProperties: false } }));
const defaults = { create_draft: { draftId: 'draft-test', status: 'draft' }, update_draft: { draftId: 'draft-test', status: 'draft' }, get_draft_file_url: { url: 'https://example.invalid/preview.pdf' } };

for await (const line of createInterface({ input: process.stdin })) {
  let request;
  try { request = JSON.parse(line); } catch { continue; }
  if (request.id === undefined) continue;
  let result;
  switch (request.method) {
    case 'initialize': result = { protocolVersion: request.params.protocolVersion, capabilities: { tools: {} }, serverInfo: { name: 'formify-fixture-only', version: '1.0.0' } }; break;
    case 'ping': result = {}; break;
    case 'tools/list': result = { tools }; break;
    case 'tools/call': {
      const { name, arguments: args = {} } = request.params;
      const known = tools.find(t => t.name === name);
      const missing = known?.inputSchema.required.filter(k => !(k in args)) ?? [];
      const extra = Object.keys(args).filter(k => !known?.inputSchema.properties[k]);
      const response = fixture.responses?.[name] ?? defaults[name];
      const error = !known || missing.length || extra.length || response === undefined;
      if (!error && name === 'update_draft') fixture.responses.get_draft = updateDraftState(fixture.responses.get_draft, args);
      if (!error && name === 'create_draft') fixture.responses.get_draft = { ...args, draftId: 'draft-test', status: 'draft' };
      result = { content: [{ type: 'text', text: JSON.stringify(error ? { error: 'Unscripted or invalid fixture call', missing, extra } : response) }], ...(error ? { isError: true } : {}) };
      appendFileSync(logPath, JSON.stringify({ tool: name, arguments: args, result, at: new Date().toISOString() }) + '\n');
      break;
    }
    default:
      process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id: request.id, error: { code: -32601, message: 'Method not implemented in test fixture' } }) + '\n');
      continue;
  }
  process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id: request.id, result }) + '\n');
}
