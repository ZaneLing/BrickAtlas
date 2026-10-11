import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { Matrix4 } from 'three';
import { LDrawLoader } from 'three/addons/loaders/LDrawLoader.js';
import { LDrawConditionalLineMaterial } from 'three/addons/materials/LDrawConditionalLineMaterial.js';
import { sourceState } from './source-state.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const STATE = sourceState(ROOT);
const OUT = process.env.SOURCE_INTAKE_OUTPUT ?? '/tmp/brickplan-v23-work/source-intake';
const FROZEN = '3518c3357872225b0425ee6bcd2a0aa8350aca0791d7b83dd056d5baec081f0b';
const sha = data => crypto.createHash('sha256').update(data).digest('hex');
const read = file => fs.readFileSync(path.resolve(ROOT, file));
const json = file => JSON.parse(read(file));
const norm = name => name.trim().replaceAll('\\', '/').toLowerCase();
const tolerance = 1e-8;
const identity = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
const axis = [0.4, 0, 0, 0, 0, -0.4, 0, 0, 0, 0, -0.4, 0, 0, 0, 0, 1];
const transpose = a => a.map((_, k) => a[(k % 4) * 4 + Math.floor(k / 4)]);
const maxError = (a, b) => Math.max(...a.map((v, i) => Math.abs(v - b[i])));
const multiply = (a, b) => a.map((_, k) =>
  [0, 1, 2, 3].reduce((v, n) => v + a[Math.floor(k / 4) * 4 + n] * b[n * 4 + k % 4], 0));
const header = (file, key) => file.lines.find(line =>
  line.text.toLowerCase().startsWith(`0 ${key.toLowerCase()}`))?.text.slice(key.length + 2).trim() ?? '';

// This index records original source addresses; no production LDraw helper is imported.
function sections(text, fallback) {
  const files = new Map();
  const lines = text.replaceAll('\r', '').split('\n');
  const isMpd = lines.some(line => /^0 FILE /i.test(line.trim()));
  let current = isMpd ? null : { name: norm(fallback), text, lines: [] };
  if (current) files.set(current.name, current);
  lines.forEach((raw, index) => {
    const clean = raw.trim(), match = /^0 FILE (.+)$/i.exec(clean);
    if (match) {
      const name = norm(match[1]);
      assert(!files.has(name), `Duplicate source section ${name}`);
      current = { name, text: '', lines: [] };
      files.set(name, current);
    } else if (/^0 NOFILE$/i.test(clean)) current = null;
    else if (current) {
      current.lines.push({ text: clean, line: index + 1 });
      if (isMpd) current.text += raw + '\n';
    }
  });
  assert(files.size);
  return files;
}

function resolveFile(files, ref) {
  const key = norm(ref);
  assert(!key.startsWith('/') && !key.split('/').includes('..'), 'Unsafe reference');
  const found = [key, `parts/${key}`, `p/${key}`, `models/${key}`].find(name => files.has(name));
  assert(found, `Unresolved source dependency ${ref}`);
  return files.get(found);
}

function parseReference(line) {
  const tokens = line.text.split(/\s+/);
  assert(tokens.length >= 15 && tokens[0] === '1');
  const values = tokens.slice(2, 14).map(Number);
  assert(values.every(Number.isFinite), 'Non-finite source matrix');
  const [x, y, z, a, b, c, d, e, f, g, h, i] = values;
  return { file: tokens.slice(14).join(' '), color: tokens[1],
    rowMatrix: [a, b, c, x, d, e, f, y, g, h, i, z, 0, 0, 0, 1] };
}

export function compareLeaf(actual, expected) {
  for (const key of ['instanceId', 'index', 'partNumber', 'colorCode', 'sourceFile',
    'sourceLine', 'parentSubmodelId']) assert.equal(actual[key], expected[key], `Leaf ${expected.instanceId}:${key}`);
  assert.deepEqual(actual.path, expected.path, `Leaf path ${expected.instanceId}`);
  assert.equal(actual.originalMatrix.length, 16);
  assert(actual.originalMatrix.every(Number.isFinite));
  const error = maxError(actual.originalMatrix, expected.originalMatrix);
  assert(error < tolerance, `Leaf matrix ${expected.instanceId}: ${error}`);
  return error;
}

function verify(candidate, intake) {
  const base = path.join(ROOT, 'web/public/models', candidate.id);
  const manifestBytes = read(path.join(base, 'manifest.json'));
  const provenanceBytes = read(path.join(base, 'provenance.json'));
  assert.equal(sha(manifestBytes), intake.manifestSha256);
  assert.equal(sha(provenanceBytes), intake.provenanceSha256);
  const manifest = JSON.parse(manifestBytes), provenance = JSON.parse(provenanceBytes);
  assert.equal(manifest.candidateRegistrySha256, FROZEN);
  const original = read(manifest.sourceFile);
  assert.equal(sha(original), intake.sourceHash);
  assert.equal(sha(original), manifest.sourceHash);
  const originalText = original.toString('utf8');
  assert.equal(sha(Buffer.from(originalText)), sha(original));
  const files = sections(originalText, path.basename(manifest.sourceFile));
  const root = files.keys().next().value;
  assert.equal(root, manifest.rootFile);
  const dependencies = new Map();
  const externalText = [];
  for (const dep of provenance.dependencyFiles) {
    const bytes = read(dep.path);
    assert.equal(sha(bytes), dep.sha256, `Dependency changed ${dep.path}`);
    dependencies.set(dep.file, dep);
    if (dep.origin === 'Historical hash-locked LDraw library') {
      assert(!files.has(dep.file), `Library shadows source section ${dep.file}`);
      files.set(dep.file, sections(bytes.toString('utf8'), dep.file).get(dep.file));
      externalText.push(`0 FILE ${dep.file}\n${bytes.toString('utf8')}`);
    } else {
      assert.equal(sha(files.get(dep.file).text), dep.sha256, `Embedded section ${dep.file}`);
      assert.equal(dep.containerSha256, sha(original));
    }
  }
  const packedPath = path.join(base, 'model.packed.mpd');
  const packedBytes = read(packedPath);
  const packed = sections(packedBytes.toString('utf8'), 'packed.mpd');
  assert.deepEqual([...packed.keys()].sort(), [...dependencies.keys()].sort(), 'Packed dependency closure');
  const canonicalLines = file => file.lines.filter(line => line.text).map(line => {
    if (!/^1\s/.test(line.text)) return line.text;
    const tokens = line.text.split(/\s+/);
    return [...tokens.slice(0, 14), resolveFile(files, tokens.slice(14).join(' ')).name].join(' ');
  });
  for (const name of dependencies.keys()) {
    assert.deepEqual(canonicalLines(packed.get(name)), canonicalLines(files.get(name)),
      `Packed section differs from original dependency ${name}`);
  }
  const colorBytes = read(path.join(base, 'LDConfig.ldr'));
  assert.equal(sha(colorBytes), provenance.colorConfig.sha256);
  const loader = new LDrawLoader();
  loader.setConditionalLineMaterial(LDrawConditionalLineMaterial);
  const fileMap = {};
  for (const file of files.values()) for (const line of file.lines) {
    if (!/^1\s/.test(line.text)) continue;
    const ref = parseReference(line);
    // Unused embedded definitions may reference unavailable files; they are not root instances.
    try { fileMap[ref.file.replaceAll('\\', '/')] = resolveFile(files, ref.file).name; }
    catch (error) { if (dependencies.has(file.name)) throw error; }
  }
  loader.setFileMap(fileMap);
  const warnings = [], previousWarn = console.warn;
  let rootInfo, palette;
  try {
    console.warn = (...args) => warnings.push(args.map(String).join(' '));
    palette = loader.partsCache.parseCache.parse(colorBytes.toString('utf8')).materials;
    loader.setMaterials(Object.values(palette));
    rootInfo = loader.partsCache.parseCache.parse(originalText + '\n' + externalText.join('\n'));
  } finally { console.warn = previousWarn; }
  const cache = loader.partsCache.parseCache;
  for (const [key, value] of Object.entries(cache._cache)) {
    const normalized = norm(key);
    assert(!cache._cache[normalized] || cache._cache[normalized] === value, `Parser namespace ${key}`);
    cache._cache[normalized] = value;
  }
  assert.equal(warnings.length, 0, `Parser warnings: ${warnings.join('; ')}`);
  const leaves = [], modelOccurrences = [], directGeometry = [];
  const inventory = new Map(), submodels = new Map(manifest.submodels.map(s => [s.id, s]));
  let maximumMatrixError = 0, maximumArithmeticError = 0;
  function visit(name, info, world, rows, color, chain, address, sourcePath, parentId, ancestors) {
    assert(!ancestors.has(name), `Original hierarchy cycle ${name}`);
    const file = files.get(name);
    assert(file && info);
    const submodelId = `s-${sha(address).slice(0, 16)}`;
    const submodel = submodels.get(submodelId);
    assert(submodel && submodel.sourceFile === name && submodel.parentId === parentId);
    const lines = file.lines.filter(line => /^1\s/.test(line.text));
    assert.equal(lines.length, info.subobjects.length, `Parser reference coverage ${name}`);
    const geometryLines = file.lines.filter(line => /^[2-5]\s/.test(line.text));
    modelOccurrences.push({ address, submodelId, parentId, sourceFile: name,
      referenceCount: lines.length, directGeometryPrimitives: geometryLines.length });
    if (geometryLines.length || info.faces.length + info.lineSegments.length + info.conditionalSegments.length) {
      directGeometry.push({ address, sourceFile: name, sourceLines: geometryLines.map(line => line.line),
        sourcePrimitiveCount: geometryLines.length, parserFaces: info.faces.length,
        parserLines: info.lineSegments.length, parserConditionalLines: info.conditionalSegments.length,
        originalMatrix: new Matrix4().makeScale(0.4, -0.4, -0.4).multiply(world).toArray(),
        reason: 'Direct model geometry is not representable by the ordinary-part manifest; no invented part ID assigned.' });
    }
    const next = new Set([...ancestors, name]);
    lines.forEach((line, ordinal) => {
      const ref = parseReference(line), parsed = info.subobjects[ordinal];
      const child = resolveFile(files, ref.file);
      assert.equal(norm(parsed.fileName), child.name);
      assert.equal(parsed.colorCode, ref.color);
      assert(maxError(parsed.matrix.toArray(), transpose(ref.rowMatrix)) < tolerance);
      const childWorld = world.clone().multiply(parsed.matrix);
      const childRows = multiply(rows, ref.rowMatrix);
      const arithmeticError = maxError(childWorld.toArray(), transpose(childRows));
      maximumArithmeticError = Math.max(maximumArithmeticError, arithmeticError);
      assert(arithmeticError < tolerance);
      const childColor = ['16', '4294967295'].includes(parsed.colorCode) ? color : parsed.colorCode;
      const childAddress = `${address}/${ordinal}:${child.name}`;
      const childChain = [...chain, { sourceFile: name, sourceLine: line.line, ordinal,
        referencedFile: child.name, originalReference: line.text,
        referenceColor: ref.color, inheritedColor: color, resolvedColor: childColor,
        localMatrix: parsed.matrix.toArray() }];
      if (child.name.endsWith('.ldr') || /(?:^|_)Model\b/.test(header(child, '!LDRAW_ORG'))) {
        const childInfo = cache.getData(child.name, false);
        assert(childInfo && !(childInfo instanceof Promise), `Missing parser data ${child.name}`);
        visit(child.name, childInfo, childWorld, childRows, childColor, childChain, childAddress,
          [...sourcePath, child.name], submodelId, next);
        return;
      }
      const index = leaves.length;
      const expected = { instanceId: `brick_${String(index + 1).padStart(6, '0')}`, index,
        partNumber: child.name.replace(/^parts\//, '').replace(/\.dat$/, ''),
        colorCode: childColor, sourceFile: name, sourceLine: line.line,
        parentSubmodelId: submodelId, path: sourcePath,
        originalMatrix: new Matrix4().makeScale(0.4, -0.4, -0.4).multiply(childWorld).toArray() };
      const actual = manifest.instances[index];
      assert(actual, `Missing manifest leaf ${expected.instanceId}`);
      const error = compareLeaf(actual, expected);
      maximumMatrixError = Math.max(maximumMatrixError, error);
      assert(maxError(actual.originalMatrix, transpose(multiply(axis, childRows))) < tolerance);
      const dep = dependencies.get(child.name);
      assert(dep && actual.sourcePartSha256 === dep.sha256);
      const material = loader.getMaterial(childColor);
      assert(material, `Unknown color ${childColor}`);
      assert.equal(actual.colorHex.toLowerCase(), `#${material.color.getHexString()}`);
      const key = `${expected.partNumber}\0${childColor}`;
      const item = inventory.get(key) ?? { partNumber: expected.partNumber, colorCode: childColor,
        colorHex: actual.colorHex, count: 0, instanceIds: [] };
      item.count++;
      item.instanceIds.push(expected.instanceId);
      inventory.set(key, item);
      leaves.push({ ...expected, originalReferenceAddress: childAddress, chain: childChain,
        sourceWorldMatrixLdu: childWorld.toArray(), colorHex: actual.colorHex,
        sourcePartSha256: dep.sha256, dependencyPath: dep.path, maximumMatrixError: error });
    });
  }
  visit(root, rootInfo, new Matrix4(), identity, '7', [], root, [root], null, new Set());
  assert.equal(leaves.length, manifest.instances.length, 'Complete ordinary-part coverage');
  assert.equal(modelOccurrences.length, manifest.submodels.length, 'Complete submodel occurrence coverage');
  assert.equal(new Set(leaves.map(leaf => leaf.instanceId)).size, leaves.length);
  assert.equal(new Set(leaves.map(leaf => leaf.originalReferenceAddress)).size, leaves.length);
  const flat = sections(read(path.join(base, 'assembly.ldr')).toString(), 'assembly.ldr')
    .values().next().value.lines.filter(line => /^1\s/.test(line.text));
  assert.equal(flat.length, leaves.length);
  flat.forEach((line, index) => {
    const ref = parseReference(line), leaf = leaves[index];
    assert.equal(norm(ref.file), `${leaf.partNumber}.dat`);
    assert.equal(ref.color, leaf.colorCode);
    assert(maxError(transpose(ref.rowMatrix), leaf.sourceWorldMatrixLdu) < tolerance);
  });
  return { schema: 'brickplan-original-hierarchy-leaf-proof/1.0', id: candidate.id,
    candidateRegistrySha256: FROZEN, originalSha256: sha(original), manifestSha256: sha(manifestBytes),
    originalSourceFile: manifest.sourceFile, rootFile: root,
    packedHierarchyFile: path.relative(ROOT, packedPath), packedHierarchySha256: sha(packedBytes),
    packedSectionsCompared: packed.size, packedHierarchyStatus: 'pass',
    provenanceSha256: sha(provenanceBytes), parser: 'Three.js 0.180.0 LDrawParsedCache, original MPD + locked dependencies',
    independentArithmetic: 'Separate row-major scalar matrix composition checked against Three.js at every reference.',
    matching: 'Strict ordered source-address bijection, exact instance IDs; no nearest-pose matching or substitution.',
    transformConvention: 'Column-major diag(0.4,-0.4,-0.4,1) * original source world matrix (LDU).',
    ordinaryLeafStatus: 'pass', fullHierarchyStatus: directGeometry.length ? 'failed-direct-model-geometry' : 'pass',
    instancesCompared: leaves.length, modelOccurrencesCompared: modelOccurrences.length,
    maximumMatrixError, maximumArithmeticError, tolerance, warnings,
    directGeometry, modelOccurrences, inventory: [...inventory.values()], leaves,
    limitations: ['Source inventory only; not an independent official LEGO bill-of-materials audit.',
      'No pose repair, part substitution, spacer insertion, mesh qualification or physical completeness claim.',
      'Direct geometry is recorded separately and never converted into invented ordinary parts.'] };
}

if (process.argv[1] && fs.realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  assert.equal(sha(read(path.join(STATE, 'candidate-registry.frozen.json'))), FROZEN);
  const registry = json(path.join(STATE, 'candidate-registry.frozen.json'));
  fs.mkdirSync(path.join(OUT, 'leaf-proofs'), { recursive: true });
  const requested = process.argv.find(arg => arg.startsWith('--id='))?.slice(5);
  const summaries = [];
  for (const candidate of registry.candidates) {
    if (requested && requested !== candidate.id) continue;
    const resultPath = path.join(STATE, 'results', `${candidate.id}.json`);
    if (!fs.existsSync(resultPath)) continue;
    const intake = json(resultPath);
    if (intake.status !== 'manifest-ready') continue;
    let report;
    try { report = verify(candidate, intake); }
    catch (error) { report = { id: candidate.id, ordinaryLeafStatus: 'failed',
      fullHierarchyStatus: 'failed', error: error.message, stack: error.stack }; }
    const output = path.join(OUT, 'leaf-proofs', `${candidate.id}.json`);
    fs.writeFileSync(output, JSON.stringify(report) + '\n');
    const { leaves, inventory, modelOccurrences, ...summary } = report;
    summaries.push({ ...summary, proofPath: output, proofSha256: sha(read(output)) });
    console.log(candidate.id, report.ordinaryLeafStatus, report.fullHierarchyStatus,
      report.instancesCompared ?? report.error);
  }
  fs.writeFileSync(path.join(OUT, requested ? `leaf-summary-${requested}.json` : 'leaf-summary.json'),
    JSON.stringify(summaries, null, 2) + '\n');
}
