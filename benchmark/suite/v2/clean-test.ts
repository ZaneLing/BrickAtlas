import assert from 'node:assert/strict';
import { cpSync, existsSync, mkdirSync, mkdtempSync, readdirSync, rmSync, symlinkSync } from 'node:fs';
import { resolve, relative } from 'node:path';
import { execFileSync } from 'node:child_process';
import { atomicJson } from '../../core/budget';
import { BENCHMARK } from '../storage';
import { DIRECTORY } from './build';

const temp = mkdtempSync(resolve(BENCHMARK, '.runtime/v2-clean-'));
try {
  const target = resolve(temp, 'benchmark'); mkdirSync(target);
  for (const entry of readdirSync(BENCHMARK).filter(n => !['.runtime', 'dist', 'dist-suite', 'node_modules'].includes(n))) {
    cpSync(resolve(BENCHMARK, entry), resolve(target, entry), { recursive: true,
      filter: file => !relative(BENCHMARK, file).endsWith('RESEARCH_ROADMAP.md') });
  }
  symlinkSync(resolve(BENCHMARK, '../node_modules'), resolve(temp, 'node_modules'), 'dir');
  assert.equal(existsSync(resolve(target, '.runtime')), false);
  const env = { ...process.env }; delete env.OPENROUTER_API_KEY;
  const cli = resolve(temp, 'node_modules/tsx/dist/cli.mjs');
  for (const command of ['verify', 'replay']) {
    execFileSync(process.execPath, [cli, resolve(target, 'suite/v2/cli.ts'), command],
      { cwd: target, env, encoding: 'utf8', maxBuffer: 8_000_000 });
    console.log(JSON.stringify({ cleanCommand: command, passed: true }));
  }
  const evidence = { checkedAt: new Date().toISOString(), originalRuntimeAvailable: false, apiKeyAvailable: false,
    sourceAndArtifactsCopied: true, fullCasebankVerified: true, allEvaluationsReplayed: true,
    dependencyMode: 'Existing pinned node_modules linked; not an independent install or second machine',
    apiRequests: 0 };
  atomicJson(resolve(DIRECTORY, 'clean-verification.json'), evidence); console.log(JSON.stringify(evidence, null, 2));
} finally { rmSync(temp, { recursive: true, force: true }); }
