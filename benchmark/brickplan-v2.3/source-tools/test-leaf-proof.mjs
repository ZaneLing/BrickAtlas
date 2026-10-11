import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { compareLeaf } from './verify-leaves.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const out = process.env.SOURCE_INTAKE_OUTPUT ?? '/tmp/brickplan-v23-work/source-intake';
const proof = JSON.parse(fs.readFileSync(`${out}/leaf-proofs/v23-21004.json`));
const source = JSON.parse(fs.readFileSync(
  path.join(root, 'web/public/models/v23-21004/manifest.json')));
const expected = proof.leaves[0], original = source.instances[0];
assert.equal(compareLeaf(original, expected), 0);
const checks = ['unchanged real-source leaf accepted'];
for (const field of ['instanceId', 'partNumber', 'colorCode', 'sourceFile', 'parentSubmodelId']) {
  const changed = structuredClone(original);
  changed[field] += '-corrupted';
  assert.throws(() => compareLeaf(changed, expected));
  checks.push(`${field} mutation rejected`);
}
for (const field of ['index', 'sourceLine']) {
  const changed = structuredClone(original);
  changed[field]++;
  assert.throws(() => compareLeaf(changed, expected));
  checks.push(`${field} mutation rejected`);
}
for (const offset of [0, 4, 12]) {
  const changed = structuredClone(original);
  changed.originalMatrix[offset] += 0.01;
  assert.throws(() => compareLeaf(changed, expected));
  checks.push(`matrix element ${offset} mutation rejected`);
}
const changedPath = structuredClone(original);
changedPath.path.push('unoriginal.ldr');
assert.throws(() => compareLeaf(changedPath, expected));
checks.push('hierarchy path mutation rejected');
assert.throws(() => compareLeaf(source.instances[1], expected));
checks.push('leaf permutation rejected even with strict ordered source matching');
const omission = JSON.parse(fs.readFileSync(`${out}/leaf-proofs/v23-10261.json`));
assert.equal(omission.ordinaryLeafStatus, 'pass');
assert.equal(omission.fullHierarchyStatus, 'failed-direct-model-geometry');
assert(omission.directGeometry.length > 0);
checks.push('direct model geometry failure retained despite ordinary leaf match');
fs.writeFileSync(`${out}/leaf-proof-test-results.json`, JSON.stringify({
  status: 'pass', fixture: 'Real v23-21004 original leaf plus deliberate in-memory corruptions',
  sourceFilesModified: false, checks,
}, null, 2) + '\n');
console.log(`PASS ${checks.length} source-leaf proof tests`);
