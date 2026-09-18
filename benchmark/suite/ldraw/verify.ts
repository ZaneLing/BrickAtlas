import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { splitMpd, normalize, reference, buildManifest, dependencyClosure, hash, type LDrawFile } from '../../../scripts/ldraw';
import { readZip } from '../../../scripts/readZip';
import { score, replay, solveActions } from '../../../src/benchmark/engine';
import type { AtlasManifest } from '../../../src/model/types';
import type { LDrawBundle, PublicLDrawTask } from '../../../src/benchmark/ldrawTypes';

const root = resolve(import.meta.dirname, '../../..');
const data = resolve(root, 'benchmark/ldraw-v1'), site = resolve(root, 'public/benchmark/ldraw');
const read = (file: string) => JSON.parse(readFileSync(file, 'utf8'));
const release = read(resolve(data, 'release.json'));
const lock = read(resolve(root, 'assets-source/library-lock.json'));
const releaseLockPath = resolve(data, 'dependency-lock.json');
const releaseLock: Record<string, string> = existsSync(releaseLockPath) ? read(releaseLockPath) : {};
let zipEntries: Map<string, Awaited<ReturnType<typeof readZip>>[number]> | undefined;
const colors = readFileSync(resolve(root, 'assets-source/ldraw-library/locked/LDConfig.ldr'), 'utf8');
let dependencies = new Set<string>(), instances = 0, tasks = 0, negative = 0, solved = 0;
const cases = [];
for (const entry of release.sources) {
  const file = resolve(root, entry.sourceFile), source = readFileSync(file);
  assert.equal(hash(source), entry.sourceHash);
  assert.equal(hash(readFileSync(resolve(site, 'sources', `${entry.id}.mpd`))), entry.sourceHash);
  const files = splitMpd(source.toString()), first = [...files.keys()][0], visited = new Set<string>();
  const collect = async (name: string): Promise<void> => {
    const normalized = normalize(name);
    const keys = [normalized, `parts/${normalized}`, `p/${normalized}`];
    let key = keys.find(k => files.has(k));
    if (!key) {
      key = keys.find(k => existsSync(resolve(root, 'assets-source/ldraw-library/locked', k)));
      assert.ok(key, `missing ${name}`);
      const bytes = readFileSync(resolve(root, 'assets-source/ldraw-library/locked', key));
      let expected = releaseLock[key] ?? lock[key];
      if (!expected) {
        if (!zipEntries) {
          const zip = readFileSync(resolve(root, 'assets-source/ldraw-library/complete.zip'));
          const provenance = read(resolve(root, 'assets-source/provenance.json'));
          assert.equal(hash(zip), provenance.resources.find((r: any) => r.file.endsWith('complete.zip')).sha256);
          zipEntries = new Map((await readZip(zip)).map(e => [normalize(e.entryName.replace(/^ldraw\//, '')), e]));
        }
        assert.ok(zipEntries.has(key), `No upstream dependency evidence: ${key}`);
        expected = hash(await zipEntries.get(key)!.getData());
      }
      assert.equal(hash(bytes), expected, `dependency changed: ${key}`);
      releaseLock[key] = expected;
      files.set(key, [...splitMpd(bytes.toString(), key).values()][0] as LDrawFile);
      dependencies.add(key);
    }
    if (visited.has(key)) return; visited.add(key);
    for (const l of files.get(key)!.lines) if (l.text.startsWith('1 ')) await collect(reference(l.text, l.line).file);
  };
  await collect(first); dependencyClosure(files, first);
  const fresh = buildManifest(files, first, colors, () => 'body');
  const manifest: AtlasManifest = read(resolve(root, 'public/models', entry.id, 'manifest.json'));
  assert.equal(fresh.instances.length, manifest.instances.length);
  const fields = (p: AtlasManifest['instances'][number]) =>
    [p.instanceId, p.index, p.partNumber, p.colorCode, p.originalMatrix, p.sourceFile, p.sourceLine, p.path, p.parentSubmodelId];
  assert.deepEqual(fresh.instances.map(fields), manifest.instances.map(fields), `source conversion changed ${entry.id}`);
  for (const chunk of manifest.chunks) assert.equal(hash(readFileSync(resolve(root, 'public/models', entry.id, chunk.url))), chunk.sha256);
  const bundle: LDrawBundle = read(resolve(site, 'models', `${entry.id}.json`));
  const input: { tasks: PublicLDrawTask[]; numberedInstances: unknown[] } = read(resolve(site, 'inputs', `${entry.id}.json`));
  assert.equal(hash(readFileSync(resolve(root, 'public/models', entry.id, 'manifest.json'))), bundle.audit.manifestSha256);
  assert.equal(bundle.parts.length, manifest.instances.length);
  assert.equal(new Set(bundle.parts.map(p => p.label)).size, bundle.parts.length);
  assert.ok(!bundle.instructions || bundle.instructions.provenance === 'source');
  const byId = new Map(bundle.parts.map(p => [p.id, p]));
  const correctByFamily: Record<string, number> = {};
  for (const [index, task] of bundle.tasks.entries()) {
    tasks++; assert.equal(score(task, task.answer).success, 1);
    correctByFamily[task.family] = (correctByFamily[task.family] ?? 0) + 1;
    for (const ref of task.references) assert.equal(ref.label, byId.get(ref.id)?.label);
    assert.equal(input.tasks[index].id, task.id);
    assert.ok(!('answer' in input.tasks[index]) && !('evidenceDetail' in input.tasks[index]));
    if (task.modality === 'visual') assert.deepEqual(task.input, {});
    if (task.format === 'actions') {
      assert.equal(score(task, solveActions(task)).success, 1); solved++;
      for (const ids of [[], ['unknown'], [...task.answer.actionIds, task.answer.actionIds[0]]]) {
        assert.equal(replay(task, ids).success, 0); negative++;
      }
      if (task.input.sourceWindow) {
        const refs = new Set(task.references.map(p => p.id));
        for (const step of task.input.sourceWindow) for (const id of step.instanceIds) assert.ok(refs.has(id));
      }
    } else if (task.format === 'single-choice') {
      for (const option of task.options!) if (option.id !== task.answer.choiceId) {
        assert.equal(score(task, { choiceId: option.id }).success, 0); negative++;
      }
    } else {
      assert.equal(score(task, { choiceIds: [...task.answer.choiceIds, task.answer.choiceIds[0]] }).success, 0); negative++;
    }
  }
  instances += manifest.instances.length;
  cases.push({ id: entry.id, sourceHashVerified: true, sourceInstancesReparsed: manifest.instances.length,
    geometryChunks: manifest.chunks.length, tasks: bundle.tasks.length, correctByFamily });
}
assert.equal(instances, release.parts); assert.equal(tasks, release.tasks);
const result = { version: release.version, sources: cases.length, instances, tasks, negativeControls: negative,
  publicPreconditionActionsSolved: solved, lockedDependencies: dependencies.size, cases };
writeFileSync(resolve(data, 'verification.json'), JSON.stringify(result, null, 2) + '\n');
writeFileSync(releaseLockPath, JSON.stringify(Object.fromEntries(Object.entries(releaseLock).sort()), null, 2) + '\n');
console.log(JSON.stringify({ ...result, cases: undefined }));
