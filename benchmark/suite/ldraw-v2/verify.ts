import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import type { AtlasManifest } from '../../../src/model/types';
import type { InternalBundle, V2Task } from './types';
import { root, site, data, hash, loadPublicBundle, publicTask, serializeModelRequest, assertNoPrivateFields } from './publish';
import { score, scoreLDrawBatch } from './score';
import { deriveAnswer } from './oracle';

const read = (p: string) => JSON.parse(readFileSync(p, 'utf8'));
const write = (p: string, value: unknown) => writeFileSync(resolve(data, p), JSON.stringify(value, null, 2) + '\n');
execFileSync('python3', [resolve(import.meta.dirname, 'freeze.py'), '--verify']);
const catalog = read(resolve(data, 'catalog.json'));
const fresh = read(resolve(data, 'source-reparse-verification.json'));
const snapshotManifest = read(resolve(data, 'request-snapshots/manifest.json'));
const rows: any[] = [], sources: any[] = [], submissions: Array<{ id: string; answer: unknown }> = [];
let negativeControls = 0, visual = 0, actions = 0;
function semantic(t: any) {
  if (t.format === 'actions') return [...t.answer.actionIds];
  if (t.format === 'integer') return t.answer.value;
  if (t.format === 'single-choice') return t.options.find((o: any) => o.id === t.answer.choiceId).value;
  return t.options.filter((o: any) => t.answer.choiceIds.includes(o.id)).map((o: any) => o.value).sort();
}
for (const e of catalog) {
  const file = resolve(site, 'models', `${e.id}.json`), bundle: InternalBundle = read(file);
  const old = read(resolve(root, 'public/benchmark/ldraw/models', `${e.id}.json`));
  const input = loadPublicBundle(resolve(site, 'inputs', `${e.id}.json`));
  assert.equal(bundle.role, 'internal-scoring-review');
  assert.equal(bundle.tasks.length, input.tasks.length);
  assert.throws(() => loadPublicBundle(file), /only versioned inputs/);
  const manifest: AtlasManifest = read(resolve(root, 'public/models', e.id, 'manifest.json'));
  assert.equal(hash(readFileSync(resolve(root, 'public/models', e.id, 'manifest.json'))), bundle.audit.manifestSha256);
  const reparse = fresh.cases.find((s: any) => s.id === e.id);
  assert.equal(reparse.sourceInstancesReparsed, bundle.parts.length);
  const sourceEntry = read(resolve(root, 'benchmark/ldraw-v1/release.json')).sources.find((s: any) => s.id === e.id);
  assert.equal(hash(readFileSync(resolve(root, sourceEntry.sourceFile))), e.sourceHash);
  const byId = new Map(bundle.parts.map(p => [p.id, p]));
  for (const [i, t] of bundle.tasks.entries()) {
    const p = input.tasks[i];
    assert.equal(p.id, t.id);
    assert.deepEqual(p, publicTask(t));
    assert.deepEqual(semantic(t), semantic(old.tasks.find((v: any) => v.id === t.id.replace(/^ld2-/, 'ld1-'))), `Semantic drift: ${t.id}`);
    for (const r of t.references) assert.equal(r.label, byId.get(r.id)?.label);
    const oracle = deriveAnswer(p, manifest);
    assert.equal(score(t, oracle).success, 1, `Independent oracle: ${t.id}`);
    submissions.push({ id: t.id, answer: oracle });
    for (const bad of [null, {}, [], { choiceId: '__invalid__' }, { value: '4' }, { actionIds: [1] }]) {
      assert.equal(score(t, bad).success, 0, `Negative oracle: ${t.id}`);
      negativeControls++;
    }
    if (t.format === 'single-choice') for (const o of t.options!) {
      assert.equal(score(t, { choiceId: o.id }).success, Number(o.id === t.answer.choiceId));
      negativeControls += Number(o.id !== t.answer.choiceId);
    }
    if (t.format === 'multiple-choice') {
      assert.equal(score(t, { choiceIds: [...t.answer.choiceIds, t.answer.choiceIds[0]] }).success, 0);
      negativeControls++;
    }
    if (t.format === 'integer') {
      for (let n = 0; n <= t.numericDomain!.max + 1; n++)
        assert.equal(score(t, { value: n }).success, Number(n === t.answer.value));
    }
    if (t.format === 'actions') {
      actions++;
      assert.ok('actionIds' in oracle);
      for (const actionIds of [[], ['unknown'], [...oracle.actionIds, oracle.actionIds[0]]]) {
        assert.equal(score(t, { actionIds }).success, 0); negativeControls++;
      }
    }
    if (t.modality === 'visual') {
      visual++; assert.deepEqual(p.input, {});
      assert.ok(existsSync(resolve(root, 'public', p.visualInput!.numberedView)));
    }
    const canary = 'PRIVATE_CANARY_d094039b';
    const poisoned = structuredClone(t) as V2Task & { internalCanary: string };
    poisoned.internalCanary = canary;
    poisoned.answer = { ...poisoned.answer, canary };
    poisoned.input.canary = canary;
    const clean = publicTask(poisoned);
    assert.ok(!JSON.stringify(serializeModelRequest(clean)).includes(canary));
    const snapRow = snapshotManifest.requests.find((r: any) => r.taskId === t.id);
    const bytes = readFileSync(resolve(root, snapRow.file));
    assert.equal(hash(bytes), snapRow.sha256);
    const request = JSON.parse(bytes.toString()); assertNoPrivateFields(request);
    for (const m of request.messages) if (Array.isArray(m.content))
      for (const c of m.content) if (c.type === 'text') assertNoPrivateFields(JSON.parse(c.text));
    const derivation = { color: 'source colorName by rendered B-label; source oracle only',
      'shape-match': 'source partNumber equality across labeled candidates; source oracle only',
      distance: 'Euclidean norm from public rounded centers',
      interface: 'public connectorRecord.family equality', neighbors: 'public incident edge endpoint set',
      'graph-removal': 'union-find component count after public target deletion',
      coverage: 'public supported=false record', 'evidence-limit': 'fixed epistemic control label',
      'source-step': 'minimum public step index containing target',
      'source-sequence': 'public precondition solver', 'restore-instance': 'public precondition solver' }[t.family];
    const referenced = new Set(t.references.map(r => r.id));
    rows.push({
      id: t.id, sourceId: e.id, sourceSha256: e.sourceHash, family: t.family, modality: t.modality, layer: t.layer,
      operands: t.references, publicInput: p, referenceAnswer: t.answer, independentlyDerivedAnswer: oracle,
      oracleVerified: true, derivation, evidenceSource: t.modality === 'visual'
        ? { sourceManifest: `public/models/${e.id}/manifest.json`, render: p.visualInput!.numberedView }
        : { contract: t.modality, auditManifestSha256: bundle.audit.manifestSha256 },
      equivalence: t.family === 'shape-match' ? 'same source partNumber; ignore color and pose; perceptual equivalence pending'
        : t.format === 'multiple-choice' ? 'unordered exact set; duplicate IDs invalid'
        : t.format === 'actions' ? 'any legal sequence reaching all goals within budget; display-only semantics'
        : 'exact declared response',
      ambiguity: {
        humanVisualReview: t.modality === 'visual' ? 'pending' : 'not-applicable',
        nearIdenticalShape: t.family === 'shape-match' ? 'needs-human-adjudication' : 'not-applicable',
        colorDiscriminability: t.family === 'color' ? 'needs-human-adjudication' : 'not-applicable',
        unsupportedOperands: bundle.audit.unsupported.filter(p => referenced.has(p.instanceId)).map(p => p.instanceId),
        incidentIntersectionCandidates: bundle.audit.nonMatingCollisionPairs.filter(pair => pair.some(id => referenced.has(id))),
        graphEvidence: 'recognized-connectors-only; absent edges do not establish physical separation',
        physicalStability: 'not-established',
      },
    });
  }
  sources.push({ id: e.id, sourceFile: sourceEntry.sourceFile, sourceSha256: e.sourceHash,
    author: e.author, license: e.license, sourceUrl: e.sourceUrl,
    instances: bundle.parts.length, partTypes: new Set(bundle.parts.map(p => p.partNumber)).size,
    colors: new Set(bundle.parts.map(p => p.colorCode)).size,
    connectorRecordsByFamily: Object.fromEntries(['stud', 'axle', 'hinge', 'fixed', 'ball'].map(f =>
      [f, bundle.audit.edges.filter(edge => edge.family === f).length])),
    unsupportedInstances: bundle.audit.unsupported.length,
    nonMatingIntersectionCandidates: bundle.audit.nonMatingCollisionPairs.length,
    sourceSteps: e.sourceSteps, reparse: { status: 'passed', fields: ['type', 'color', 'transform', 'hierarchy'], ...reparse },
    connectedComponents: bundle.audit.components.length, physicalStatus: 'not-certified' });
}
assert.equal(rows.length, 617); assert.equal(visual, 140); assert.equal(actions, 75);
assert.equal(scoreLDrawBatch(submissions).success, 617);
assert.throws(() => scoreLDrawBatch([submissions[0], submissions[0]]), /Duplicate/);
write('task-audit.json', { version: 'brickatlas-ldraw-2', role: 'internal-scoring-review', tasks: rows });
write('source-audit.json', { sources });
write('verification.json', { status: 'passed', tasks: rows.length, sources: sources.length,
  independentSourceOracle: rows.length, publicActionSolver: actions, visualImages: visual, negativeControls,
  pathsRejected: catalog.length, canariesBlocked: rows.length, requestSnapshotsVerified: rows.length,
  visualHumanCertification: 'pending', physicalCertification: 'not-established' });
execFileSync('python3', [resolve(import.meta.dirname, 'freeze.py'), '--verify']);
console.log(JSON.stringify(read(resolve(data, 'verification.json'))));
