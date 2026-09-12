import assert from 'node:assert/strict';
import { cpSync, existsSync, mkdirSync, mkdtempSync, readdirSync, rmSync, symlinkSync } from 'node:fs';
import { resolve, relative } from 'node:path';
import { execFileSync } from 'node:child_process';
import { ARTIFACTS, BENCHMARK } from '../storage';
import { atomicJson } from '../../core/budget';

const root = resolve(BENCHMARK, '.runtime'); mkdirSync(root, { recursive: true });
const temp = mkdtempSync(resolve(root, 'clean-replay-'));
try {
  const target = resolve(temp, 'benchmark');
  mkdirSync(target);
  for (const entry of readdirSync(BENCHMARK).filter(n => !['.runtime', 'dist', 'dist-suite', 'node_modules'].includes(n))) {
  cpSync(resolve(BENCHMARK, entry), resolve(target, entry), { recursive: true, filter: file => {
    const path = relative(BENCHMARK, file);
    return !['.runtime', 'dist', 'dist-suite', 'node_modules'].some(dir => path === dir || path.startsWith(dir + '/'))
      && !path.endsWith('RESEARCH_ROADMAP.md');
  } });
  }
  symlinkSync(resolve(BENCHMARK, '../node_modules'), resolve(temp, 'node_modules'), 'dir');
  assert.equal(existsSync(resolve(target, '.runtime')), false);
  assert.equal(existsSync(resolve(temp, '.env')), false);
  const cli = resolve(temp, 'node_modules/tsx/dist/cli.mjs');
  const env = { ...process.env }; delete env.OPENROUTER_API_KEY;
  const replay = execFileSync(process.execPath, [cli, resolve(target, 'suite/cli.ts'), 'replay'],
    { cwd: target, env, encoding: 'utf8' });
  const results = JSON.parse(replay);
  execFileSync(process.execPath, [resolve(temp, 'node_modules/typescript/bin/tsc'), '-p', resolve(target, 'tsconfig.json')],
    { cwd: target, env, encoding: 'utf8' });
  const status = execFileSync(process.execPath, [cli, '-e',
    `import {trainingStatus} from './suite/research/training-status.ts'; console.log(JSON.stringify(trainingStatus().map(j=>({name:j.name,status:j.status,steps:j.history.length}))))`],
  { cwd: target, env, encoding: 'utf8' });
  const jobs = JSON.parse(status);
  assert.equal(jobs.length, 5);
  assert.ok(jobs.every((j: { status: string }) => j.status === 'complete'));
  assert.equal(jobs.reduce((n: number, j: { steps: number }) => n + j.steps, 0), 480);
  const result = { checkedAt: new Date().toISOString(), copiedSourceAndArtifacts: true,
    originalRuntimeAvailable: false, apiKeyAvailable: false, apiRequests: 0, typecheck: true,
    replay: results, portableTrainingJobs: jobs, optimizerSteps: 480,
    connectorVendorPresent: false, dependencyMode: 'Existing pinned node_modules linked, not an independent npm installation',
    scope: 'Offline scoring and adapter hash reproduction, not rerunning stochastic API generation or training.' };
  atomicJson(resolve(ARTIFACTS, 'research/clean-replay.json'), result);
  console.log(JSON.stringify(result, null, 2));
} finally { rmSync(temp, { recursive: true, force: true }); }
