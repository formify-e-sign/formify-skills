import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { checkRoot } from './validate.mjs';

const root = fileURLToPath(new URL('../../', import.meta.url));
const reportDir = join(root, 'tests/release/reports');
mkdirSync(reportDir, { recursive: true });
const report = { date: new Date().toISOString(), node: process.version, source: checkRoot(root), commands: [], package: null };
function command(executable, args, cwd = root) {
  const r = spawnSync(executable, args, { cwd, encoding: 'utf8', timeout: 60000 });
  report.commands.push({ executable, args, status: r.status, stdout: r.stdout ?? '', stderr: r.stderr ?? '', error: r.error?.message });
  return r;
}
command('npm', ['run', 'check']);
command('claude', ['plugin', 'validate', join(root, '.claude-plugin/plugin.json')]);
command('claude', ['plugin', 'validate', join(root, '.claude-plugin/marketplace.json')]);
const temp = mkdtempSync(join(tmpdir(), 'formify-package-check-'));
try {
  const packed = command('npm', ['pack', '--ignore-scripts', '--json', '--pack-destination', temp]);
  if (packed.status === 0) {
    const info = JSON.parse(packed.stdout)[0];
    const extracted = command('tar', ['-xzf', join(temp, info.filename), '-C', temp]);
    if (extracted.status === 0) report.package = { filename: info.filename, shasum: info.shasum, integrity: info.integrity, ...checkRoot(join(temp, 'package')), files: info.files.map(f => f.path) };
  }
} catch (e) { report.package = { failures: [{ message: e.message }] }; }
finally { rmSync(temp, { recursive: true, force: true }); }
const failures = report.source.failures.length + (report.package?.failures.length ?? 1) + report.commands.filter(c => c.status !== 0).length;
report.verdict = failures ? 'FAIL' : 'PASS';
writeFileSync(join(reportDir, 'static.json'), JSON.stringify(report, null, 2) + '\n');
console.log(`${report.verdict}: source=${report.source.failures.length}, package=${report.package?.failures.length ?? 'not checked'}, command failures=${report.commands.filter(c => c.status !== 0).length}`);
for (const [scope, result] of [['source', report.source], ['package', report.package]]) for (const f of result?.failures ?? []) console.log(`${scope}: ${f.path ?? ''}: ${f.message}`);
for (const c of report.commands.filter(c => c.status !== 0)) console.log(`${c.executable} ${c.args.join(' ')}: ${c.stdout}${c.stderr}${c.error ?? ''}`);
console.log('Report: tests/release/reports/static.json');
process.exitCode = failures ? 1 : 0;
