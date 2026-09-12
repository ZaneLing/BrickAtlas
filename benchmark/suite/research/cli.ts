import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { BENCHMARK } from '../storage';
import { SuiteRenderer } from '../render';
import { migrateTraces } from '../traces';
import { prepareResearchData } from './dataset';
import { auditConnectors } from './connectors';
import { importLocalResults } from './local-results';
import { runResearch } from './run';
import { runPaired } from './paired';
import { writeStatistics } from './statistics';
import { exportResearchInputs, scoreResearchPredictions } from './external';
import { researchBaselines } from './baselines';

const [command, ...args] = process.argv.slice(2);
let result: unknown;
if (command === 'prepare') result = prepareResearchData();
else if (command === 'connectors') result = auditConnectors();
else if (command === 'import-local') result = importLocalResults();
else if (command === 'statistics') result = writeStatistics();
else if (command === 'baselines') result = researchBaselines();
else if (command === 'score') {
  const path = args.find(a => a.startsWith('--predictions='))?.slice('--predictions='.length);
  if (!path) throw new Error('Provide --predictions=/absolute/path.jsonl');
  result = scoreResearchPredictions(path);
} else if (command === 'export') {
  const info = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
  const renderer = new SuiteRenderer(info.url);
  try { result = await exportResearchInputs(renderer); } finally { await renderer.close(); }
}
else if (command === 'traces') {
  const { rows, ...summary } = migrateTraces(); result = summary;
} else if (command === 'run' || command === 'paired') {
  if (!args.includes('--paid')) throw new Error('Explicit --paid required; reuses the persistent budget');
  if (command === 'paired') {
    const runs = await runPaired();
    result = runs.map(r => ({ id: r.id, status: r.status, error: r.error }));
    if (runs.some(r => r.status !== 'complete')) process.exitCode = 1;
  } else {
    const info = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
    const renderer = new SuiteRenderer(info.url);
    try {
      const run = await runResearch(renderer, p => console.log(JSON.stringify(p)));
      result = { id: run.id, status: run.status, error: run.error };
      if (run.status !== 'complete') process.exitCode = 1;
    } finally { await renderer.close(); }
  }
} else throw new Error('Commands: prepare | connectors | import-local | statistics | traces | export | score --predictions=... | run --paid | paired --paid');
console.log(JSON.stringify(result, null, 2));
