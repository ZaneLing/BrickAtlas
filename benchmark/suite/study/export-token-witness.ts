import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { BENCHMARK } from '../storage';
import { getSpec, taskForV2 } from '../v2/cases';
import { STUDY } from './protocol';

// Private diagnostics only: never append these answers to model input files.
const rows = readFileSync(resolve(STUDY, 'inputs/public.jsonl'), 'utf8').trim().split('\n').map(line => {
  const row = JSON.parse(line), task = taskForV2(getSpec(row.caseId));
  return { caseId: row.caseId, kind: task.spec.kind, answer: task.oracle };
});
atomicJson(resolve(BENCHMARK, '.runtime/study-test-token-witness.json'), rows);
console.log(JSON.stringify({ witnesses: rows.length, modelInputModified: false }));
