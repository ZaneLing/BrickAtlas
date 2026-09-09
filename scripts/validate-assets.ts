import { readFile } from 'node:fs/promises';
import { gunzipSync } from 'node:zlib';
import { strict as assert } from 'node:assert';
import { Box3, Vector3 } from 'three';
import { hash, splitMpd, dependencyClosure, buildManifest, reference, resolveFile } from './ldraw';
import type { AtlasManifest } from '../src/model/types';
import { modelCatalog } from '../atlas.config';

for (const config of modelCatalog) {
  const base = `public/models/${config.id}/`;
  const manifest: AtlasManifest = JSON.parse(await readFile(`${base}manifest.json`, 'utf8'));
  const report = JSON.parse(await readFile(`assets-built/build-report-${config.id}.json`, 'utf8'));
  const source = await readFile(config.sourceFile);
  assert.equal(hash(source), config.sourceHash);
  assert.equal(hash(source), manifest.sourceHash);
  assert.equal(hash(JSON.stringify(manifest)), report.manifestHash);
  assert.equal(new Set(manifest.instances.map(p => p.instanceId)).size, manifest.instances.length);
  assert.deepEqual(manifest.instances.map(p => p.instanceId), manifest.instances.map((_, i) => `brick_${String(i + 1).padStart(6, '0')}`));
  const files = splitMpd(await readFile(`${base}model.packed.mpd`, 'utf8'));
  assert.equal(dependencyClosure(files, [...files.keys()][0]).length, report.dependencyFiles);
  const parsed = buildManifest(files, [...files.keys()][0], await readFile(`${base}LDConfig.ldr`, 'utf8'));
  const originalFiles = splitMpd(source.toString());
  for (const [i, part] of manifest.instances.entries()) {
    assert.equal(parsed.instances[i].instanceId, part.instanceId);
    assert.deepEqual(parsed.instances[i].originalMatrix, part.originalMatrix);
    assert(part.originalMatrix.every(Number.isFinite));
    assert([...part.bounds.min, ...part.bounds.max].every(Number.isFinite));
    assert(part.bounds.max.some((v, j) => v > part.bounds.min[j]));
    const sourceLine = originalFiles.get(part.sourceFile)!.lines.find(l => l.line === part.sourceLine)!;
    const ref = reference(sourceLine.text, sourceLine.line);
    assert.equal(resolveFile(files, ref.file).name.replace(/^parts\//, '').replace(/\.dat$/, ''), part.partNumber);
  }
  const membership = manifest.groups.flatMap(g => g.instanceIds);
  assert.equal(membership.length, manifest.instances.length);
  assert.equal(new Set(membership).size, membership.length);
  const instructionIds = manifest.instructions?.steps.flatMap(step => step.instanceIds) ?? [];
  assert.equal(instructionIds.length, manifest.instances.length);
  assert.equal(new Set(instructionIds).size, instructionIds.length);
  const renderIds = new Set<number>();
  let triangles = 0, bytes = 0;
  for (const chunk of manifest.chunks) {
    const compressed = await readFile(base + chunk.url);
    assert.equal(hash(compressed), chunk.sha256);
    assert.equal(compressed.length, chunk.bytes);
    bytes += compressed.length;
    const uncompressed = gunzipSync(compressed);
    const raw = uncompressed.buffer.slice(uncompressed.byteOffset, uncompressed.byteOffset + uncompressed.byteLength);
    for (const bucket of chunk.buckets) {
      const attrs = new Map<string, Float32Array>();
      for (const [name, attr] of Object.entries(bucket.attributes)) {
        const a = new Float32Array(raw, attr.offset, attr.count);
        assert(a.every(Number.isFinite), `Non-finite ${name}`);
        assert.equal(a.length % attr.itemSize, 0);
        attrs.set(name, a);
      }
      const positions = attrs.get('position')!, ids = attrs.get('instanceIndex')!;
      assert.equal(positions.length, ids.length * 3);
      if (bucket.kind === 'mesh') triangles += ids.length / 3;
      for (let i = 0; i < ids.length; i++) {
        const p = manifest.instances[ids[i]];
        assert(p && p.groupId === chunk.groupId, 'Lost instance ownership');
        renderIds.add(ids[i]);
        const point = new Vector3().fromArray(positions, i * 3);
        const box = new Box3(new Vector3(...p.bounds.min), new Vector3(...p.bounds.max)).expandByScalar(0.001);
        assert(box.containsPoint(point), 'Geometry outside semantic bounds');
      }
    }
  }
  assert.equal(renderIds.size, manifest.instances.length);
  assert.equal(triangles, report.triangles);
  assert.equal(bytes, report.compressedBytes);
  assert.equal(report.missingParts.length, 0);
  assert.equal(report.warnings.length, 0);
  console.log(`PASS ${config.id}: ${renderIds.size} identities, ${manifest.instructions?.steps.length} steps, ${triangles} triangles.`);
}
