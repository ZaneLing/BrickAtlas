import { execFileSync } from 'node:child_process';
import { mkdirSync, readdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { BENCHMARK } from '../storage';
import { DIRECTORY } from './build';

const root = resolve(BENCHMARK, '..'), tsx = resolve(root, 'node_modules/tsx/dist/cli.mjs');
const logs = resolve(BENCHMARK, '.runtime/v2-check'); mkdirSync(logs, { recursive: true });
const commands = [
  { name: 'benchmark-tests', args: [tsx, '--test', '--test-reporter=spec', ...readdirSync(resolve(BENCHMARK, 'tests'))
    .filter(n => n.endsWith('.test.ts')).map(n => resolve(BENCHMARK, 'tests', n))] },
  { name: 'typecheck', args: [resolve(root, 'node_modules/typescript/bin/tsc'), '-p', resolve(BENCHMARK, 'tsconfig.json')] },
  { name: 'suite-build', args: [resolve(root, 'node_modules/vite/bin/vite.js'), 'build', '--config', resolve(BENCHMARK, 'suite/vite.config.ts')] },
  { name: 'original-unit-tests', args: [resolve(root, 'node_modules/vitest/vitest.mjs'), 'run'] },
  { name: 'historical-replay', args: [tsx, resolve(BENCHMARK, 'suite/cli.ts'), 'replay'] },
  { name: 'evaluation-contract', args: [tsx, resolve(BENCHMARK, 'suite/v2/evidence-test.ts')] },
  { name: 'export-integrity', args: [tsx, resolve(BENCHMARK, 'suite/v2/export-test.ts')] },
  { name: 'casebank-ui', args: [tsx, resolve(BENCHMARK, 'suite/v2/ui-test.ts')] },
  { name: 'historical-trace-ui', args: [tsx, resolve(BENCHMARK, 'suite/trace-ui-test.ts')] },
];
const evidence: { name: string; passed: boolean; seconds: number; detail?: string }[] = [];
for (const c of commands) {
  const start = Date.now();
  try {
    const output = execFileSync(process.execPath, c.args, { cwd: root, encoding: 'utf8', maxBuffer: 8_000_000 });
    writeFileSync(resolve(logs, c.name + '.log'), output);
    evidence.push({ name: c.name, passed: true, seconds: (Date.now() - start) / 1000,
      detail: output.match(/tests \d+|Tests.*passed/)?.[0]?.replace(/\u001b\[[0-9;]*m/g, '') });
  } catch (error) {
    const e = error as Error & { stdout?: string; stderr?: string };
    writeFileSync(resolve(logs, c.name + '.log'), (e.stdout ?? '') + (e.stderr ?? '') + e.message);
    evidence.push({ name: c.name, passed: false, seconds: (Date.now() - start) / 1000 });
    process.exitCode = 1;
  }
  atomicJson(resolve(DIRECTORY, 'engineering-verification.json'), { checkedAt: new Date().toISOString(), checks: evidence, apiRequests: 0 });
  console.log(JSON.stringify(evidence.at(-1)));
  if (process.exitCode) break;
}
