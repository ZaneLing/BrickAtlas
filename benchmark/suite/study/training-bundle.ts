import assert from 'node:assert/strict';
import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { gzipSync, gunzipSync } from 'node:zlib';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { BENCHMARK, SYSTEM } from '../storage';
import { digest } from '../data';
import { getSpec, taskForV2 } from '../v2/cases';
import { evaluateStrict } from './strict-evaluate';
import { STUDY, selection } from './protocol';

const hash = (data: Buffer) => createHash('sha256').update(data).digest('hex');
export function trainingBundle(mode: 'export' | 'verify' | 'restore' = 'verify') {
  const bundle = resolve(STUDY, 'training-data'), runtime = resolve(BENCHMARK, '.runtime/study-training');
  if (mode === 'export') {
    mkdirSync(resolve(bundle, 'images'), { recursive: true });
    const files: Record<string, string> = {};
    for (const split of ['train', 'validation']) {
      const raw = readFileSync(resolve(runtime, split + '.jsonl'));
      writeFileSync(resolve(bundle, split + '.jsonl.gz'), gzipSync(raw));
      files[split + '.jsonl'] = hash(raw);
      for (const row of raw.toString('utf8').trim().split('\n').map(l => JSON.parse(l))) {
        for (const path of row.images) {
          assert.match(path, /^images\/[a-f0-9]{64}\.png$/);
          const bytes = readFileSync(resolve(runtime, path));
          files[path] = hash(bytes); copyFileSync(resolve(runtime, path), resolve(bundle, path));
        }
      }
    }
    atomicJson(resolve(bundle, 'manifest.json'), { files, provenance: 'Procedural v2 oracle supervision; no human annotation',
      license: 'CC0-1.0', sourceManifest: JSON.parse(readFileSync(resolve(runtime, 'manifest.json'), 'utf8')) });
  }
  const manifest = JSON.parse(readFileSync(resolve(bundle, 'manifest.json'), 'utf8'));
  const test = new Set(selection().map(s => s.group)), train = new Set<string>(), validation = new Set<string>();
  const seen = new Set<string>(), images = new Set<string>();
  for (const split of ['train', 'validation']) {
    const raw = gunzipSync(readFileSync(resolve(bundle, split + '.jsonl.gz')));
    assert.equal(hash(raw), manifest.files[split + '.jsonl']);
    const rows = raw.toString('utf8').trim().split('\n').map(l => JSON.parse(l));
    assert.equal(rows.length, split === 'train' ? 672 : 168);
    for (const row of rows) {
      const spec = getSpec(row.caseId), task = taskForV2(spec);
      assert.ok(!seen.has(row.caseId)); seen.add(row.caseId);
      assert.equal(spec.split, split); assert.equal(row.split, split);
      assert.equal(row.group, spec.group); assert.equal(row.kind, spec.kind);
      assert.ok(!test.has(row.group));
      (split === 'train' ? train : validation).add(row.group);
      assert.equal(row.system, SYSTEM); assert.deepEqual(row.input, task.public);
      assert.deepEqual(row.answer, task.oracle);
      assert.equal(evaluateStrict(task, row.answer).metrics.success, 1);
      assert.equal(row.images.length, task.frames.length);
      for (const path of row.images) {
        assert.match(path, /^images\/[a-f0-9]{64}\.png$/); images.add(path);
        const bytes = readFileSync(resolve(bundle, path));
        assert.equal(hash(bytes), manifest.files[path]);
        assert.equal(path, `images/${digest(bytes.toString('base64'))}.png`);
      }
    }
    if (mode === 'restore') {
      mkdirSync(runtime, { recursive: true }); writeFileSync(resolve(runtime, split + '.jsonl'), raw);
    }
  }
  assert.equal(train.size, 96); assert.equal(validation.size, 24);
  assert.ok([...train].every(group => !validation.has(group))); assert.equal(images.size, 480);
  assert.deepEqual(Object.keys(manifest.files).sort(), ['train.jsonl', 'validation.jsonl', ...images].sort());
  if (mode === 'restore') {
    mkdirSync(resolve(runtime, 'images'), { recursive: true });
    for (const path of images) copyFileSync(resolve(bundle, path), resolve(runtime, path));
    atomicJson(resolve(runtime, 'manifest.json'), manifest.sourceManifest);
  }
  const evidence = { rows: seen.size, trainGroups: train.size, validationGroups: validation.size, images: images.size,
    oracleAndPublicInputExact: true, groupIsolation: true, hashesVerified: true, apiRequests: 0 };
  atomicJson(resolve(STUDY, 'training-bundle-verification.json'), evidence);
  return evidence;
}
