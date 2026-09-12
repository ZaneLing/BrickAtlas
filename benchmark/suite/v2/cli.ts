import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { ARTIFACTS, BENCHMARK } from '../storage';
import { buildCasebank } from './build';
import { readPredictions, scoreBatch, selectCases, type Selection } from './batch';
import { verifyCasebank } from './verify';
import { exportInputs } from './export';
import { SuiteRenderer } from '../render';
import { replayEvaluations } from './replay';

const [command, ...args] = process.argv.slice(2);
const option = (name: string, fallback = '') => args.find(a => a.startsWith(`--${name}=`))?.slice(name.length + 3) ?? fallback;
let result: unknown;
if (command === 'build') {
  const m = await buildCasebank(); result = { structures: m.structures, cases: m.cases, splits: m.splits, audit: m.audit };
} else if (command === 'verify') result = await verifyCasebank();
else if (command === 'replay') result = await replayEvaluations();
else if (command === 'select') {
  const selection = selectCases(option('split', 'test_id'), option('condition', 'all'),
    option('objects') ? Number(option('objects')) : undefined);
  const path = resolve(ARTIFACTS, 'casebank-v2/selections', selection.id + '.json');
  atomicJson(path, selection); result = { path, cases: selection.caseIds.length, hash: selection.hash };
} else if (['score', 'baseline', 'export'].includes(command)) {
  if (!option('selection')) throw new Error('Require frozen --selection=path.json');
  const selection = JSON.parse(readFileSync(resolve(option('selection')), 'utf8')) as Selection;
  if (command === 'export') {
    const info = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
    const renderer = new SuiteRenderer(info.url);
    try { result = await exportInputs(selection, renderer); } finally { await renderer.close(); }
  } else {
    if (command === 'score' && (!option('predictions') || !option('model'))) throw new Error('Require --predictions=path.jsonl and --model=name');
    result = await scoreBatch(selection, command === 'baseline' ? new Map() : await readPredictions(resolve(option('predictions'))),
      command === 'baseline' ? 'public-symbolic-algorithm' : option('model'), command === 'baseline');
  }
} else throw new Error('Commands: build | verify | select [--split=test_id --condition=all --objects=N] | export --selection=... | baseline --selection=... | score --selection=... --predictions=... --model=...');
console.log(JSON.stringify(result, null, 2));
