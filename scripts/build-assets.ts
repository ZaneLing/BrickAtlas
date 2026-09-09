import { readFile, writeFile, mkdir, unlink } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import AdmZip from 'adm-zip';
import { gzipSync } from 'node:zlib';
import { Box3, BufferAttribute, Matrix3, Matrix4, Mesh, Vector3, type Material } from 'three';
import { LDrawLoader } from 'three/addons/loaders/LDrawLoader.js';
import { LDrawConditionalLineMaterial } from 'three/addons/materials/LDrawConditionalLineMaterial.js';
import { splitMpd, reference, normalize, dependencyClosure, resolveFile, buildManifest, hash, groups as carGroups, classify, boundsJSON, header } from './ldraw';
import { instructionPlan } from './instructions';
import type { AtlasManifest, GeometryBucket, MaterialRecord, GroupId } from '../src/model/types';
import { modelCatalog } from '../atlas.config';

const requestedId = process.argv.slice(2).find(argument => !argument.startsWith('--'));
if (!requestedId) {
  for (const model of modelCatalog) {
    execFileSync(process.execPath, [...process.execArgv, process.argv[1], model.id], { stdio: 'inherit' });
  }
  process.exit(0);
}
const atlasConfig = modelCatalog.find(model => model.id === requestedId);
if (!atlasConfig) throw new Error(`Unknown model ${requestedId}`);
const out = `public/models/${atlasConfig.id}`;
await mkdir(out, { recursive: true });
await mkdir('assets-built', { recursive: true });
const previousManifest: AtlasManifest | null = existsSync(`${out}/manifest.json`) ? JSON.parse(await readFile(`${out}/manifest.json`, 'utf8')) : null;
const source = await readFile(atlasConfig.sourceFile, 'utf8');
const libraryProvenance = JSON.parse(await readFile('assets-source/provenance.json', 'utf8'));
if (hash(source) !== atlasConfig.sourceHash) throw new Error(`Source hash differs from lock for ${atlasConfig.id}`);
const libraryResource = libraryProvenance.resources.find((resource: { file: string }) => resource.file.endsWith('complete.zip'));
if (!libraryResource) throw new Error('LDraw library lock is missing');
const provenance = {
  acquiredAt: '2026-09-08',
  model: { title: `${atlasConfig.setNumber} ${atlasConfig.title}`, author: atlasConfig.author, license: atlasConfig.license, page: atlasConfig.sourceUrl },
  library: libraryProvenance.library,
  resources: [{ file: atlasConfig.sourceFile, url: atlasConfig.sourceUrl, sha256: atlasConfig.sourceHash }, libraryResource],
  changes: ['Dependency closure packed without modifying original files', 'Geometry converted to millimetres (+Y up)', 'Deterministic brick IDs and functional groups', 'Geometry batching and lossless gzip; no decimation'],
};
const files = splitMpd(source);
const rootName = [...files.keys()][0];
const libraryRoot = 'assets-source/ldraw-library/locked';
const zipPath = 'assets-source/ldraw-library/complete.zip';
const zip = existsSync(zipPath) && !process.argv.includes('--offline') ? new AdmZip(zipPath) : null;
if (zip && hash(await readFile(zipPath)) !== libraryResource.sha256) throw new Error('Library hash differs from lock');
const entries = new Map(zip?.getEntries().map(e => [normalize(e.entryName.replace(/^ldraw\//, '')), e]) ?? []);
const libraryLockPath = 'assets-source/library-lock.json';
const libraryLock: Record<string, string> = existsSync(libraryLockPath) ? JSON.parse(await readFile(libraryLockPath, 'utf8')) : {};

async function libraryFile(name: string) {
  const path = `${libraryRoot}/${name}`;
  if (existsSync(path)) {
    const text = await readFile(path, 'utf8');
    const expected = libraryLock[name] ?? (entries.has(normalize(name)) ? hash(entries.get(normalize(name))!.getData()) : null);
    if (!expected || expected !== hash(text)) throw new Error(`Library lock mismatch: ${name}`);
    libraryLock[name] = expected;
    return text;
  }
  const entry = entries.get(normalize(name));
  if (!entry) throw new Error(`Missing library file ${name}; run npm run acquire`);
  const text = entry.getData().toString('utf8');
  libraryLock[name] = hash(text);
  await mkdir(path.slice(0, path.lastIndexOf('/')), { recursive: true });
  await writeFile(path, text);
  return text;
}
const colorText = await libraryFile('LDConfig.ldr');
for (const name of ['CAreadme.txt', 'CAlicense.txt', 'CAlicense4.txt', 'Readme.txt']) {
  await writeFile(`assets-source/license/${name}`, await libraryFile(name));
  await writeFile(`${out}/${name}`, await libraryFile(name));
}

async function loadDependency(name: string) {
  const candidates = [name, `parts/${name}`, `p/${name}`, `models/${name}`].map(normalize);
  const found = candidates.find(n => files.has(n));
  if (found) return files.get(found)!;
  const key = candidates.find(n => entries.has(n) || existsSync(`${libraryRoot}/${n}`));
  if (!key) throw new Error(`Missing dependency ${name}`);
  const text = await libraryFile(key);
  const file = splitMpd(text, key).get(key)!;
  files.set(key, file);
  return file;
}
const visited = new Set<string>();
async function collect(name: string) {
  const file = await loadDependency(name);
  if (visited.has(file.name)) return;
  visited.add(file.name);
  for (const line of file.lines) if (line.text.startsWith('1 ')) await collect(reference(line.text, line.line).file);
}
await collect(rootName);
const closure = dependencyClosure(files, rootName);
const genericGroups: AtlasManifest['groups'] = [
  { id: 'body', name: '主体结构', color: '#e45252', direction: [0, 55, 0], instanceIds: [] },
  { id: 'chassis', name: '基础与承重', color: '#848d95', direction: [0, -35, 0], instanceIds: [] },
  { id: 'wheels', name: '轮组与活动件', color: '#b392e0', direction: [0, 0, 65], instanceIds: [] },
  { id: 'cockpit', name: '座舱与角色', color: '#59b3c0', direction: [0, 90, 0], instanceIds: [] },
  { id: 'front', name: '前部与附件', color: '#dfb744', direction: [-75, 25, 0], instanceIds: [] },
  { id: 'rear', name: '后部与外装', color: '#64ac84', direction: [75, 25, 0], instanceIds: [] },
];
const modelGroups = atlasConfig.id === '5867' ? carGroups : genericGroups;
const genericClassify = (part: Parameters<typeof classify>[0]): GroupId => {
  const text = `${part.displayName} ${part.path.join(' ')}`.toLowerCase();
  if (/\b(tyre|tire|wheel|propell|rotor|hinge|turntable)\b/.test(text)) return 'wheels';
  if (/\b(seat|windscreen|window|cockpit|figure|torso|head|helmet|astronaut)\b/.test(text)) return 'cockpit';
  const y = part.originalMatrix[13];
  const x = part.originalMatrix[12];
  if (y < 10) return 'chassis';
  if (x < -55) return 'front';
  if (x > 55) return 'rear';
  return 'body';
};
const semantic = buildManifest(files, rootName, colorText, atlasConfig.id === '5867' ? classify : genericClassify);
const rewrite = (text: string) => text.split('\n').map(line => {
  if (!line.trim().startsWith('1 ')) return line;
  const tokens = line.trim().split(/\s+/);
  return `${tokens.slice(0, 14).join(' ')} ${resolveFile(files, tokens.slice(14).join(' ')).name}`;
}).join('\n');
const packed = [rootName, ...closure.filter(n => n !== rootName)].map(name => `0 FILE ${name}\n${rewrite(files.get(name)!.text)}`).join('\n');
await writeFile(`${out}/model.packed.mpd`, packed);
await writeFile(`${out}/LDConfig.ldr`, colorText);

// Only Three.js's official LDrawLoader interprets geometry, BFC and conditional edges.
// Flattening here is semantic, with one identity-space object per physical instance.
const loader = new LDrawLoader();
loader.setConditionalLineMaterial(LDrawConditionalLineMaterial);
const references = semantic.instances.map(p => `1 ${p.colorCode} 0 0 0 1 0 0 0 1 0 0 0 1 ${resolveFile(files, `${p.partNumber}.dat`).name}`);
const geometryText = [
  '0 FILE atlas-flat.ldr', '0 Atlas build model', '0 !LDRAW_ORG Model', colorText,
  ...references, ...closure.filter(n => n.endsWith('.dat')).map(n => `0 FILE ${n}\n${rewrite(files.get(n)!.text)}`),
].join('\n');
const warnings: string[] = [];
const oldWarn = console.warn;
console.warn = (...args) => { warnings.push(args.map(String).join(' ')); oldWarn(...args); };
const loaded = await new Promise<import('three').Group>((resolve, reject) => loader.parse(geometryText, resolve, reject));
console.warn = oldWarn;
if (warnings.length) throw new Error(`LDrawLoader warnings must be resolved:\n${warnings.join('\n')}`);
if (loaded.children.length !== semantic.instances.length) throw new Error(`Identity count mismatch: ${loaded.children.length} vs ${semantic.instances.length}`);
loaded.updateMatrixWorld(true);

type Bucket = { kind: GeometryBucket['kind']; material: MaterialRecord; attributes: Record<string, number[]> };
const buckets = new Map<GroupId, Map<string, Bucket>>(modelGroups.map(g => [g.id, new Map()]));
const allBounds = new Box3();
let triangleCount = 0;
const vec = new Vector3();
for (const part of semantic.instances) {
  const object = loaded.children[part.index];
  if (normalize(object.name) !== resolveFile(files, `${part.partNumber}.dat`).name) throw new Error(`Loader order mismatch for ${part.instanceId}`);
  const partBox = new Box3();
  const original = new Matrix4().fromArray(part.originalMatrix);
  object.traverse(node => {
    const mesh = node as Mesh;
    if (!mesh.geometry) return;
    const geometry = mesh.geometry.index ? mesh.geometry.toNonIndexed() : mesh.geometry;
    const transform = original.clone().multiply(node.matrixWorld);
    const normalMatrix = new Matrix3().getNormalMatrix(transform);
    const rotation = new Matrix3().setFromMatrix4(transform);
    const materials = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
    const ranges = geometry.groups.length ? geometry.groups : [{ start: 0, count: geometry.attributes.position.count, materialIndex: 0 }];
    for (const range of ranges) {
      const count = Math.min(range.count, geometry.attributes.position.count - range.start);
      const material = materials[range.materialIndex ?? 0] as Material & { color: import('three').Color; roughness?: number; metalness?: number; isLDrawConditionalLineMaterial?: boolean };
      const kind = material.isLDrawConditionalLineMaterial ? 'conditional' : (mesh.isMesh ? 'mesh' : 'line');
      const record: MaterialRecord = { color: `#${material.color.getHexString()}`, opacity: material.opacity, roughness: material.roughness ?? 0.32, metalness: material.metalness ?? 0 };
      // Transparent instances are kept in separate buckets for object-level depth sorting.
      const key = `${kind}:${JSON.stringify(record)}${material.opacity < 1 ? `:${part.index}` : ''}`;
      const groupBuckets = buckets.get(part.groupId)!;
      let bucket = groupBuckets.get(key);
      if (!bucket) {
        bucket = { kind, material: record, attributes: { position: [], instanceIndex: [] } };
        for (const attr of kind === 'mesh' ? ['normal'] : kind === 'conditional' ? ['control0', 'control1', 'direction'] : []) bucket.attributes[attr] = [];
        groupBuckets.set(key, bucket);
      }
      const mirrored = transform.determinant() < 0;
      for (let offset = 0; offset < count; offset++) {
        const localOffset = kind === 'mesh' && mirrored ? offset - offset % 3 + [0, 2, 1][offset % 3] : offset;
        const index = range.start + localOffset;
        for (const [name, array] of Object.entries(bucket.attributes)) {
          if (name === 'instanceIndex') { array.push(part.index); continue; }
          const attr = geometry.getAttribute(name) as BufferAttribute;
          vec.fromBufferAttribute(attr, index);
          if (name === 'normal') vec.applyMatrix3(normalMatrix).normalize();
          else if (name === 'direction') vec.applyMatrix3(rotation);
          else vec.applyMatrix4(transform);
          if (name === 'position') partBox.expandByPoint(vec);
          array.push(vec.x, vec.y, vec.z);
        }
      }
      if (kind === 'mesh') triangleCount += count / 3;
    }
  });
  part.bounds = boundsJSON(partBox);
  allBounds.union(partBox);
}
const chunks: AtlasManifest['chunks'] = [];
for (const group of modelGroups) {
  const groupBuckets = [...buckets.get(group.id)!.values()];
  const parts: Buffer[] = [];
  let offset = 0;
  const metadata = groupBuckets.map(bucket => {
    const attributes: GeometryBucket['attributes'] = {};
    for (const [name, values] of Object.entries(bucket.attributes)) {
      const array = new Float32Array(values);
      parts.push(Buffer.from(array.buffer));
      attributes[name] = { offset, count: array.length, itemSize: name === 'instanceIndex' ? 1 : 3 };
      offset += array.byteLength;
    }
    return { kind: bucket.kind, material: bucket.material, attributes };
  });
  const compressed = gzipSync(Buffer.concat(parts), { level: 9 });
  const digest = hash(compressed);
  const file = `${group.id}.${digest.slice(0, 12)}.bin`;
  await writeFile(`${out}/${file}`, compressed);
  chunks.push({ groupId: group.id, url: file, bytes: compressed.byteLength, sha256: digest, buckets: metadata });
}
const manifest: AtlasManifest = {
  version: 1,
  model: {
    id: atlasConfig.id, title: atlasConfig.title, author: provenance.model.author, sourceUrl: provenance.model.page,
    license: atlasConfig.license, year: atlasConfig.year,
    notes: atlasConfig.notes,
  },
  sourceHash: hash(source), ...semantic,
  groups: modelGroups.map(g => ({ ...g, instanceIds: semantic.instances.filter(p => p.groupId === g.id).map(p => p.instanceId) })),
  bounds: boundsJSON(allBounds), chunks,
  stats: {
    instances: semantic.instances.length, uniqueParts: new Set(semantic.instances.map(p => p.partNumber)).size,
    colors: new Set(semantic.instances.map(p => p.colorCode)).size,
    triangles: triangleCount, compressedBytes: chunks.reduce((s, c) => s + c.bytes, 0),
  },
  instructions: instructionPlan(files, rootName, {
    instances: semantic.instances,
    groups: modelGroups.map(g => ({ ...g, instanceIds: semantic.instances.filter(p => p.groupId === g.id).map(p => p.instanceId) })),
  }),
};
const attribution = {
  model: provenance.model, library: provenance.library, changes: provenance.changes,
  files: closure.map(name => ({ file: name, author: header(files.get(name)!, 'Author:'), license: header(files.get(name)!, '!LICENSE'), sha256: hash(files.get(name)!.text) })),
};
await writeFile(`${out}/credits.json`, JSON.stringify(attribution, null, 2));
await writeFile(`${out}/provenance.json`, JSON.stringify(provenance, null, 2));
await writeFile(`${out}/attribution.txt`, [
  'Brick Atlas is an unofficial community project, not affiliated with the LEGO Group.',
  `${provenance.model.title} by ${provenance.model.author}, CC BY 2.0, ${provenance.model.page}`,
  'LDraw.org Parts Library. Per-file authors and licenses: credits.json and original packed MPD.',
  'Licenses: https://creativecommons.org/licenses/by/2.0/ and https://creativecommons.org/licenses/by/4.0/',
  `Changes: ${provenance.changes.join('; ')}.`, '',
  ...attribution.files.map(f => `${f.file} | ${f.author} | ${f.license}`),
].join('\n'));
const report = {
  sourceHash: manifest.sourceHash, libraryHash: libraryResource.sha256,
  classificationHash: atlasConfig.classificationFile
    ? hash(await readFile(atlasConfig.classificationFile)) : hash(JSON.stringify(modelGroups)),
  ...manifest.stats, dependencyFiles: closure.length, missingParts: [], warnings,
  manifestHash: hash(JSON.stringify(manifest)), chunks: chunks.map(c => ({ file: c.url, sha256: c.sha256, bytes: c.bytes })),
  limitations: manifest.model.notes,
};
await writeFile(`${out}/manifest.json`, JSON.stringify(manifest));
await writeFile(`assets-built/build-report-${atlasConfig.id}.json`, JSON.stringify(report, null, 2) + '\n');
if (atlasConfig.id === '5867') await writeFile('assets-built/build-report.json', JSON.stringify(report, null, 2) + '\n');
await writeFile(`${out}/build-report.json`, JSON.stringify(report, null, 2) + '\n');
await writeFile(libraryLockPath, JSON.stringify(Object.fromEntries(Object.entries(libraryLock).sort(([a], [b]) => a.localeCompare(b))), null, 2) + '\n');
for (const chunk of previousManifest?.chunks ?? []) {
  if (!chunks.some(c => c.url === chunk.url)) await unlink(`${out}/${chunk.url}`).catch(() => {});
}
console.log(JSON.stringify(report, null, 2));
