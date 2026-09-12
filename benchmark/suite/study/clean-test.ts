import assert from 'node:assert/strict';
import { cpSync, existsSync, mkdirSync, mkdtempSync, rmSync, symlinkSync } from 'node:fs';
import { resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { atomicJson } from '../../core/budget';
import { BENCHMARK } from '../storage';
import { STUDY } from './protocol';

const temporary = mkdtempSync(resolve(BENCHMARK, '.runtime/study-clean-'));
try {
  const target = resolve(temporary, 'benchmark'); mkdirSync(target);
  for (const entry of ['suite', 'core', 'package.json', 'tsconfig.json']) {
    cpSync(resolve(BENCHMARK, entry), resolve(target, entry), {
      recursive: true, filter: file => !file.endsWith('RESEARCH_ROADMAP.md'),
    });
  }
  symlinkSync(resolve(BENCHMARK, '../node_modules'), resolve(temporary, 'node_modules'), 'dir');
  assert.equal(existsSync(resolve(target, '.runtime')), false);
  const env = { ...process.env }; delete env.OPENROUTER_API_KEY;
  const commands = ['replay', 'verify-training', 'replay-local', 'local-statistics'];
  for (const command of commands) {
    execFileSync(process.execPath, [resolve(temporary, 'node_modules/tsx/dist/cli.mjs'),
      resolve(target, 'suite/study/cli.ts'), command], { cwd: target, env, encoding: 'utf8', maxBuffer: 8_000_000 });
    console.log(JSON.stringify({ command, passed: true }));
  }
  const result = { checkedAt: new Date().toISOString(), commands, passed: true,
    runtimeCopied: false, apiKeyAvailable: false, apiRequests: 0,
    limitation: 'Pinned installed Node dependencies shared; no independent OS install or repeated stochastic training.' };
  atomicJson(resolve(STUDY, 'clean-verification.json'), result);
  console.log(JSON.stringify(result));
} finally { rmSync(temporary, { recursive: true, force: true }); }
