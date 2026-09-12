import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { dataset } from '../v2/dataset';
import { portConnections } from '../research/connectors';
import { independentGeometry } from './independent';
import { STUDY } from './protocol';
import { BENCHMARK } from '../storage';
import { digest } from '../data';

export function auditV2Connectors() {
  const rows = [];
  for (const m of dataset()) {
    const expected = independentGeometry(m.structure.parts).links.reduce((n, e) => n + e.studs, 0);
    const actual = portConnections(m.structure.parts);
    assert.equal(actual.length, expected, m.id);
    rows.push({ modelId: m.id, studs: actual.length });
  }
  const result = { assemblies: rows.length, allAgree: true, rows,
    sourceHash: digest(readFileSync(resolve(BENCHMARK, '.runtime/vendor/bricknet/normalized-connectors.json'), 'utf8')),
    scope: 'Nominal grid stud-hole positions for supported catalog only; not general hinges/axles/balls or forces.',
    upstream: 'BrickNet bundled MIT annotations, original attribution retained.' };
  atomicJson(resolve(STUDY, 'connector-audit.json'), result); return { assemblies: rows.length, allAgree: true };
}
