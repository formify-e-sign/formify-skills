import { mkdtempSync, mkdirSync, cpSync, readFileSync, writeFileSync, existsSync, rmSync, readdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { frontmatter } from './validate.mjs';
import { gradeWorkflow, gradeRouting } from './grade.mjs';

const here = fileURLToPath(new URL('./', import.meta.url));
const root = fileURLToPath(new URL('../../', import.meta.url));
const option = name => { const i = process.argv.indexOf(name); return i < 0 ? undefined : process.argv[i + 1]; };
const mode = option('--mode') ?? 'all';
if (!['all', 'routing', 'workflow'].includes(mode)) throw new Error('mode must be all, routing or workflow');
const reportDir = join(here, 'reports');
mkdirSync(reportDir, { recursive: true });
const sandbox = mkdtempSync(join(tmpdir(), 'formify-evaluation-'));
const plugin = join(sandbox, 'plugin');
const work = join(sandbox, 'work');
mkdirSync(work); mkdirSync(join(plugin, '.claude-plugin'), { recursive: true });
cpSync(join(root, 'skills'), join(plugin, 'skills'), { recursive: true });
// Do not copy the production manifests, .mcp.json, hooks, settings or project instructions.
writeFileSync(join(plugin, '.claude-plugin/plugin.json'), JSON.stringify({ name: 'formify', version: '1.0.0', description: 'Isolated evaluation of the current Formify skills', skills: './skills/' }));
const hashes = {};
function hashTree(dir, prefix = '') {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const rel = prefix + e.name;
    if (e.isDirectory()) hashTree(join(dir, e.name), rel + '/');
    else hashes['skills/' + rel] = createHash('sha256').update(readFileSync(join(dir, e.name))).digest('hex');
  }
}
hashTree(join(plugin, 'skills'));

function runClaude(prompt, mcp, nativeSkills) {
  const args = ['-p', '--output-format', 'stream-json', '--verbose', '--no-session-persistence',
    '--setting-sources', '', '--settings', JSON.stringify({ disableAllHooks: true, enabledPlugins: {} }),
    '--strict-mcp-config', '--mcp-config', JSON.stringify(mcp), '--no-chrome', '--permission-mode', 'dontAsk',
    '--tools', nativeSkills ? 'Skill' : '', '--max-budget-usd', '2'];
  if (nativeSkills) args.push('--plugin-dir', plugin, '--allowedTools', 'Skill,mcp__formify__*');
  else args.push('--disable-slash-commands');
  return new Promise(resolve => {
    const child = spawn('claude', args, { cwd: work, env: { ...process.env, CLAUDECODE: '' }, stdio: ['pipe', 'pipe', 'pipe'] });
    let stdout = '', stderr = '', timedOut = false;
    const timer = setTimeout(() => { timedOut = true; child.kill('SIGTERM'); setTimeout(() => child.kill('SIGKILL'), 5000).unref(); }, 120000);
    child.stdout.on('data', data => stdout += data); child.stderr.on('data', data => stderr += data);
    child.on('error', error => { stderr += error.message; });
    child.on('close', code => {
      clearTimeout(timer);
      const events = stdout.split('\n').flatMap(line => { try { return [JSON.parse(line)]; } catch { return []; } });
      const final = events.findLast(e => e.type === 'result');
      const invoked = events.flatMap(e => e.message?.content ?? []).filter(c => c.type === 'tool_use' && c.name === 'Skill').map(c => c.input?.skill);
      resolve({ code, timedOut, stderr, events, final, invoked, raw: stdout });
    });
    child.stdin.end(prompt);
  });
}

const report = { date: new Date().toISOString(), harness: 'Claude Code', model: 'CLI default (recorded in events)', sourceHashes: hashes, productionMcpConnected: false, tests: [] };
const save = () => writeFileSync(join(reportDir, `evaluation-${mode}.json`), JSON.stringify(report, null, 2) + '\n');
function record(id, kind, run, errors, details = {}) {
  if (run.code !== 0 || run.timedOut || !run.final || run.final.is_error) errors.push(`harness execution failed: code=${run.code}, timeout=${run.timedOut}, result=${run.final?.subtype ?? 'absent'}`);
  report.tests.push({ id, kind, verdict: errors.length ? 'FAIL' : 'PASS', errors, ...details, invoked: run.invoked, modelUsage: run.final?.modelUsage, usage: run.final?.usage, costUsd: run.final?.total_cost_usd });
  writeFileSync(join(reportDir, `${id}.jsonl`), run.raw);
  if (run.stderr) writeFileSync(join(reportDir, `${id}.stderr.txt`), run.stderr);
  save(); console.log(`${id}: ${errors.length ? 'FAIL ' + errors.join('; ') : 'PASS'}`);
}

try {
  if (mode !== 'workflow') {
    const fixtures = JSON.parse(readFileSync(join(here, 'fixtures/routing.json')));
    const descriptions = readdirSync(join(plugin, 'skills')).map(name => ({ name, description: frontmatter(readFileSync(join(plugin, 'skills', name, 'SKILL.md'), 'utf8')).data.description }));
    const prompt = `This is a description-routing evaluation, not a user task to execute. No tools are available. For each request choose the relevant skills from the catalogue. Multiple skills may compose. Choose none for unrelated requests. Mark clarify true when the request needs clarification. Return ONLY JSON: {"results":[{"id":"...","skills":["..."],"clarify":false}]}.\nCatalogue:\n${JSON.stringify(descriptions)}\nRequests:\n${JSON.stringify(fixtures.map(({ id, prompt }) => ({ id, prompt })))}`;
    const run = await runClaude(prompt, { mcpServers: {} }, false);
    let results = [];
    try { results = JSON.parse(run.final.result.replace(/^```(?:json)?\s*|\s*```$/g, '')).results; } catch {}
    for (const f of fixtures) {
      const result = results.find(r => r.id === f.id);
      record(f.id, 'description-routing-proxy; NOT native activation', run, result ? gradeRouting(f, result) : ['no parseable result'], { result });
    }
  }
  if (mode !== 'routing') {
    const fixtures = JSON.parse(readFileSync(join(here, 'fixtures/workflows.json'))).filter(f => !option('--case') || f.id === option('--case'));
    if (!fixtures.length) throw new Error('No matching workflow cases');
    for (const fixture of fixtures) {
      const fixturePath = join(sandbox, fixture.id + '.json');
      const logPath = join(sandbox, fixture.id + '.calls.jsonl');
      writeFileSync(fixturePath, JSON.stringify({ responses: fixture.responses }));
      const mcp = { mcpServers: { formify: { command: process.execPath, args: [join(here, 'mock-mcp.mjs'), fixturePath, logPath] } } };
      const run = await runClaude(fixture.prompt, mcp, true);
      const calls = existsSync(logPath) ? readFileSync(logPath, 'utf8').trim().split('\n').filter(Boolean).map(JSON.parse) : [];
      const errors = gradeWorkflow(fixture, calls, run.final?.result ?? '');
      if (!run.invoked.some(name => name === fixture.skill || name?.endsWith(':' + fixture.skill))) errors.push(`expected native Skill invocation: ${fixture.skill}`);
      record(fixture.id, 'native Skill invocation plus fixture MCP calls', run, errors, { calls, answer: run.final?.result, evidence: fixture.evidence });
    }
  }
} finally { rmSync(sandbox, { recursive: true, force: true }); save(); }
console.log(`Report: tests/release/reports/evaluation-${mode}.json`);
process.exitCode = report.tests.some(t => t.verdict === 'FAIL') ? 1 : 0;
