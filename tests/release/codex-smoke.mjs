// Native Codex smoke using project .agents/skills and only a synthetic MCP server.
import { mkdtempSync, mkdirSync, cpSync, readFileSync, writeFileSync, existsSync, rmSync, readdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { gradeWorkflow } from './grade.mjs';

const here = fileURLToPath(new URL('./', import.meta.url));
const root = fileURLToPath(new URL('../../', import.meta.url));
const temp = mkdtempSync(join(tmpdir(), 'formify-codex-smoke-'));
const reports = join(here, 'reports'); mkdirSync(reports, { recursive: true });
const skillsDir = join(temp, '.agents', 'skills'); mkdirSync(skillsDir, { recursive: true });
cpSync(join(root, 'skills'), skillsDir, { recursive: true });
const sourceHashes = Object.fromEntries(readdirSync(skillsDir).map(name => [name, createHash('sha256').update(readFileSync(join(skillsDir, name, 'SKILL.md'))).digest('hex')]));
const selected = process.argv.indexOf('--case');
const selectedCase = selected < 0 ? undefined : process.argv[selected + 1];
const fixtures = JSON.parse(readFileSync(join(here, 'fixtures/workflows.json'))).filter(f => ['prepare-only', 'resume-preserve'].includes(f.id) && (!selectedCase || f.id === selectedCase));
const report = { date: new Date().toISOString(), harness: 'Codex CLI', productionMcpConnected: false, sourceHashes, tests: [] };
const output = selectedCase ? `codex-smoke-${selectedCase}.json` : 'codex-smoke.json';
const save = () => writeFileSync(join(reports, output), JSON.stringify(report, null, 2) + '\n');
try {
  for (const f of fixtures) {
    const input = join(temp, f.id + '.json'), log = join(temp, f.id + '.calls.jsonl');
    writeFileSync(input, JSON.stringify({ responses: f.responses }));
    const mcpArgs = [join(here, 'mock-mcp.mjs'), input, log];
    const args = ['exec', '--ignore-user-config', '--ignore-rules', '--ephemeral', '--skip-git-repo-check', '--sandbox', 'read-only', '--json', '-C', temp,
      '--disable', 'apps', '--disable', 'plugins', '--disable', 'multi_agent',
      '-c', 'mcp_servers.formify.default_tools_approval_mode="approve"',
      '-c', `mcp_servers.formify.command=${JSON.stringify(process.execPath)}`,
      '-c', `mcp_servers.formify.args=${JSON.stringify(mcpArgs)}`, '-'];
    const run = await new Promise(resolve => {
      const child = spawn('codex', args, { cwd: temp, stdio: ['pipe', 'pipe', 'pipe'] });
      let stdout = '', stderr = '', timedOut = false;
      const timer = setTimeout(() => { timedOut = true; child.kill('SIGTERM'); setTimeout(() => child.kill('SIGKILL'), 5000).unref(); }, 120000);
      child.stdout.on('data', d => stdout += d); child.stderr.on('data', d => stderr += d);
      child.on('error', e => stderr += e.message);
      child.on('close', code => { clearTimeout(timer); resolve({ code, stdout, stderr, timedOut }); });
      child.stdin.end(f.prompt);
    });
    writeFileSync(join(reports, `codex-${f.id}.jsonl`), run.stdout);
    writeFileSync(join(reports, `codex-${f.id}.stderr.txt`), run.stderr);
    const events = run.stdout.split('\n').flatMap(line => { try { return [JSON.parse(line)]; } catch { return []; } });
    const answer = events.filter(e => e.type === 'item.completed' && e.item?.type === 'agent_message').map(e => e.item.text).join('\n');
    const calls = existsSync(log) ? readFileSync(log, 'utf8').trim().split('\n').filter(Boolean).map(JSON.parse) : [];
    const errors = gradeWorkflow(f, calls, answer);
    if (run.code !== 0 || run.timedOut || !events.some(e => e.type === 'turn.completed')) errors.push(`harness failed: code=${run.code}, timeout=${run.timedOut}`);
    // Codex reads SKILL.md through file tools instead of Claude's Skill invocation.
    // Record candidate read events for review; do not infer a successful read from a final answer.
    const skillReadEvidence = events.filter(e => e.type === 'item.completed' && e.item?.type === 'command_execution' && e.item.exit_code === 0 && e.item.command?.includes(f.skill + '/SKILL.md'));
    report.tests.push({ id: f.id, verdict: errors.length ? 'FAIL' : 'PASS', errors, calls, answer, skillReadEvidence, usage: events.findLast(e => e.type === 'turn.completed')?.usage });
    save(); console.log(`${f.id}: ${errors.length ? 'FAIL ' + errors.join('; ') : 'PASS'}; candidate native skill reads=${skillReadEvidence.length}`);
  }
} finally { rmSync(temp, { recursive: true, force: true }); save(); }
console.log(`Report: tests/release/reports/${output}`);
process.exitCode = report.tests.some(t => t.verdict === 'FAIL') ? 1 : 0;
