import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { gunzipSync } from 'node:zlib';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { getSpec } from '../v2/cases';
import { STUDY } from './protocol';

export interface Exposure { group: string; role: string; evidence: string }
export function exposureRecords(includeReplication = true): Exposure[] {
  const records: Exposure[] = [];
  const add = (groups: string[], role: string, evidence: string) => {
    for (const group of new Set(groups)) records.push({ group, role, evidence });
  };
  for (const split of ['train', 'validation']) {
    const path = `training-data/${split}.jsonl.gz`;
    const rows = gunzipSync(readFileSync(resolve(STUDY, path))).toString('utf8').trim().split('\n').map(l => JSON.parse(l));
    add(rows.map(r => r.group), split === 'train' ? 'training-supervision' : 'training-validation', path);
  }
  const protocol = JSON.parse(readFileSync(resolve(STUDY, 'protocol.json'), 'utf8'));
  add(protocol.cases.map((s: any) => s.group), 'published-pilot-test', 'protocol.json');
  const calibration = JSON.parse(readFileSync(resolve(STUDY, 'calibration/protocol.json'), 'utf8'));
  add(calibration.sourceGroups.map((s: any) => s.group), 'prepared-calibration', 'calibration/protocol.json');
  for (const path of ['model-validation/run.json', 'model-validation/ladder/run.json',
    'model-validation/ladder-normalized/run.json', 'pose-probes/run.json']) {
    if (!existsSync(resolve(STUDY, path))) continue;
    const run = JSON.parse(readFileSync(resolve(STUDY, path), 'utf8'));
    const groups = path === 'model-validation/run.json' ? run.rows.map((r: any) => getSpec(r.caseId).group)
      : path === 'pose-probes/run.json' ? run.rows.map((r: any) => r.group)
        : run.rows.length ? [JSON.parse(readFileSync(resolve(STUDY, path.replace('run.json', 'protocol.json')), 'utf8')).sourceGroup] : [];
    add(groups, 'adaptive-model-validation', path);
  }
  if (includeReplication && existsSync(resolve(STUDY, 'order-study/run.json'))) {
    const run = JSON.parse(readFileSync(resolve(STUDY, 'order-study/run.json'), 'utf8'));
    add(run.rows.map((r: any) => r.group), 'adaptive-model-replication', 'order-study/run.json');
  }
  return records;
}
export function observedGroups(records = exposureRecords()) {
  return new Set(records.filter(r => r.role !== 'prepared-calibration').map(r => r.group));
}
export function exposureAudit() {
  const records = exposureRecords(), observed = observedGroups(records);
  const trained = new Set(records.filter(r => r.role === 'training-supervision').map(r => r.group));
  assert.ok(records.filter(r => ['training-validation', 'published-pilot-test', 'adaptive-model-validation'].includes(r.role))
    .every(r => !trained.has(r.group)), 'Source leakage into supervised training');
  const roles = [...new Set(records.map(r => r.role))].map(role => ({ role,
    sourceGroups: new Set(records.filter(r => r.role === role).map(r => r.group)).size }));
  const result = { version: 'exposure-register-1', records, roles, observedGroups: [...observed].sort(),
    preparedOnlyGroups: [...new Set(records.filter(r => r.role === 'prepared-calibration' && !observed.has(r.group)).map(r => r.group))].sort(),
    sourceEvidenceHashes: Object.fromEntries([...new Set(records.map(r => r.evidence))].map(path =>
      [path, digest(readFileSync(resolve(STUDY, path)).toString('base64'))])),
    scope: 'Records explicit study use, not pretraining contamination or a claim unobserved public data is secret.',
    trainingIsolationPassed: true };
  atomicJson(resolve(STUDY, 'exposure-register.json'), result);
  return { roles, observedGroups: observed.size, preparedOnlyGroups: result.preparedOnlyGroups.length };
}
