import { readFile, readdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { resolve, dirname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { hash, header, splitMpd, normalize } from '../../../scripts/ldraw.ts';
import { readZip } from '../../../scripts/readZip.ts';
import { LDrawLoader } from 'three/addons/loaders/LDrawLoader.js';
import { LDrawConditionalLineMaterial } from 'three/addons/materials/LDrawConditionalLineMaterial.js';
import { writeNew } from './intake.ts';
import { sourceState } from './source-state.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../../..');
const HERE = sourceState(ROOT);
const OUTPUT = process.env.SOURCE_INTAKE_OUTPUT ?? '/tmp/brickplan-v23-work/source-intake';
const suffix = process.argv.find(a => a.startsWith('--label='))?.slice(8) ?? 'final';
assert(/^[a-z0-9-]+$/.test(suffix));
const registryBytes = await readFile(resolve(HERE, 'candidate-registry.frozen.json'));
const frozenHash = (await readFile(resolve(HERE, 'candidate-registry.frozen.sha256'), 'utf8')).split(' ')[0];
assert.equal(hash(registryBytes), frozenHash);
const registry = JSON.parse(registryBytes.toString());
const previousHashes = new Set(registry.previousModels.map((m: any) => m.sourceHash));
const rows: any[] = [], dependencyFiles = new Map<string, any>();
const authorName = (text: string) => text.replace(/\s*\[.*\]\s*$/, '').normalize('NFKD')
  .replace(/\p{Diacritic}/gu, '').trim().toLowerCase();
const exactProfiles = new Map<string, string[]>(), translatedProfiles = new Map<string, string[]>();
function add(map: Map<string, string[]>, key: string, id: string) {
  map.set(key, [...(map.get(key) ?? []), id]);
}
function profile(instances: any[], translationInvariant = false) {
  const offset = translationInvariant ? [12, 13, 14].map(
    i => Math.min(...instances.map(p => p.originalMatrix[i]))) : [0, 0, 0];
  const records = instances.map(p => [p.partNumber, p.colorCode, p.originalMatrix.map(
    (n: number, i: number) => Math.round((n - (i >= 12 && i <= 14 ? offset[i - 12] : 0)) * 1e9) / 1e9)]);
  return hash(JSON.stringify(records.map(r => JSON.stringify(r)).sort()));
}
for (const previous of registry.previousModels) {
  const bytes = await readFile(resolve(ROOT, 'web/public/models', previous.modelId, 'manifest.json'));
  assert.equal(hash(bytes), previous.sha256);
  const model = JSON.parse(bytes.toString());
  add(exactProfiles, profile(model.instances), previous.modelId);
  add(translatedProfiles, profile(model.instances, true), previous.modelId);
}
const libraryLock = JSON.parse(await readFile(resolve(ROOT, 'assets-source/library-lock.json'), 'utf8'));
const licenseDocuments = [];
for (const name of ['CAreadme.txt', 'CAlicense.txt', 'CAlicense4.txt']) {
  const originalPath = resolve(ROOT, 'assets-source/ldraw-library/locked', name);
  const bytes = await readFile(originalPath);
  assert.equal(hash(bytes), libraryLock[name]);
  const target = resolve(ROOT, 'assets-source/brickplan-v23/licenses', name);
  await writeNew(target, bytes);
  licenseDocuments.push({ file: relative(ROOT, target), sha256: hash(bytes),
    copiedUnchangedFrom: relative(ROOT, originalPath) });
}
for (const candidate of registry.candidates) {
  const resultPath = resolve(HERE, 'results', `${candidate.id}.json`);
  const checkPath = resolve(OUTPUT, 'hierarchy-checks', `${candidate.id}.json`);
  const result = existsSync(resultPath) ? JSON.parse(await readFile(resultPath, 'utf8')) : null;
  const hierarchy = existsSync(checkPath) ? JSON.parse(await readFile(checkPath, 'utf8')) : null;
  const detailPath = resolve(HERE, 'details', `${candidate.kit}.json`);
  const detail = existsSync(detailPath) ? JSON.parse(await readFile(detailPath, 'utf8')) : null;
  const chosen = detail && (detail.models.find((m: any) => m.pageModelLabel === 'Main Model')
    ?? [...detail.models].sort((a: any, b: any) => a.downloadUrl.localeCompare(b.downloadUrl))[0]);
  let original: any = null, manifest: any = null, provenanceChecks: any = null;
  if (chosen && result) {
    const filename = decodeURIComponent(new URL(chosen.downloadUrl).pathname.split('/').at(-1)!);
    const sourcePath = resolve(ROOT, 'assets-source/brickplan-v23/original', filename);
    if (existsSync(sourcePath)) {
      const bytes = await readFile(sourcePath);
      const sections = splitMpd(bytes.toString('utf8'), filename);
      const root = sections.values().next().value!;
      original = {
        id: candidate.id, kit: candidate.kit, sourceFile: relative(ROOT, sourcePath),
        downloadUrl: chosen.downloadUrl, sourceUrl: candidate.sourceUrl,
        sourceHash: hash(bytes), bytes: bytes.length, author: header(root, 'Author:'),
        license: header(root, '!LICENSE'), pageAuthor: chosen.pageAuthor,
        pageSha256: detail.pageSha256, completeness: chosen.completeness,
        candidateRegistrySha256: frozenHash,
      };
      assert(!previousHashes.has(original.sourceHash), `Repeated historical original: ${candidate.id}`);
      assert.equal(detail.setNumber, candidate.setNumber);
      assert.equal(detail.sourceUrl, candidate.sourceUrl);
      assert.equal(detail.title, candidate.title);
      assert(filename.startsWith(candidate.setNumber), `Download identity mismatch: ${candidate.id}`);
      const rootNameMatchesKit = new RegExp(`^${candidate.kit}[ ._-]`).test(root.name);
      assert(original.author && /CC BY (2\.0|4\.0)|CCAL version 2\.0|CC0/i.test(original.license));
      const indexPath = resolve(HERE, 'snapshots', `index-${String(candidate.indexPage).padStart(2, '0')}.html`);
      const pagePath = resolve(HERE, 'snapshots', `set-${candidate.sourceUrl.split('/').at(-1)}.html`);
      assert.equal(hash(await readFile(indexPath)), candidate.indexSha256);
      assert.equal(hash(await readFile(pagePath)), detail.pageSha256);
      const history = root.lines.filter(l => l.text.startsWith('0 !HISTORY')).map(l => l.text);
      const attribution = original.author === original.pageAuthor ? 'exact-match'
        : authorName(original.author) === authorName(original.pageAuthor) ? 'display-name-match-with-header-spelling-retained'
          : history.some(line => line.includes(original.pageAuthor)) ? 'original-author-and-OMR-contributor-in-history'
            : 'unresolved';
      assert.notEqual(attribution, 'unresolved', `Unexplained author/page discrepancy: ${candidate.id}`);
      provenanceChecks = {
        status: rootNameMatchesKit ? 'pass' : 'root-name-conflict',
        officialSetAndDownloadIdentity: true, rootFile: root.name, rootNameMatchesKit,
        rootIdentityIssue: rootNameMatchesKit ? null
          : 'Official catalog/download kit conflicts with original MPD root name; original bytes retained.',
        indexSnapshotSha256: candidate.indexSha256, detailSnapshotSha256: detail.pageSha256,
        authorAttribution: attribution, sourceAuthor: original.author, pageAuthor: original.pageAuthor,
        sourceHistory: history, licenseHeaderPreserved: true, license: original.license,
        sourceCustomColorDeclarations: root.lines.filter(l => /^0\s+!COLOUR\b/.test(l.text)).length,
      };
      assert.equal(provenanceChecks.sourceCustomColorDeclarations, 0, 'Custom model colors require separate handling');
      await writeNew(resolve(ROOT, 'assets-source/brickplan-v23/provenance', `${candidate.id}.json`),
        JSON.stringify(original, null, 2) + '\n');
    }
  }
  if (result?.status === 'manifest-ready') {
    const base = resolve(ROOT, 'web/public/models', candidate.id);
    const bytes = await readFile(resolve(base, 'manifest.json'));
    assert.equal(hash(bytes), result.manifestSha256);
    manifest = JSON.parse(bytes.toString());
    assert.equal(manifest.sourceHash, original.sourceHash);
    assert.equal(manifest.model.id, candidate.id);
    assert.equal(manifest.model.setNumber, candidate.setNumber);
    assert.equal(manifest.model.author, original.author);
    assert.equal(manifest.model.license, original.license);
    assert.equal(manifest.model.downloadUrl, chosen.downloadUrl);
    assert.equal(manifest.candidateRegistrySha256, frozenHash);
    assert.equal(manifest.instances.length, manifest.stats.instances);
    assert.equal(new Set(manifest.instances.map((p: any) => p.instanceId)).size, manifest.instances.length);
    const provenanceBytes = await readFile(resolve(base, 'provenance.json'));
    assert.equal(hash(provenanceBytes), result.provenanceSha256);
    const provenance = JSON.parse(provenanceBytes.toString());
    const colorBytes = await readFile(resolve(base, 'LDConfig.ldr'));
    assert.equal(hash(colorBytes), provenance.colorConfig.sha256);
    const colorLoader = new LDrawLoader();
    colorLoader.setConditionalLineMaterial(LDrawConditionalLineMaterial);
    const palette = (colorLoader as any).partsCache.parseCache.parse(colorBytes.toString()).materials;
    colorLoader.setMaterials(Object.values(palette) as any[]);
    for (const part of manifest.instances) {
      const material: any = colorLoader.getMaterial(part.colorCode);
      assert(material, `Unknown source color ${part.colorCode}`);
      assert.equal(part.colorHex.toLowerCase(), `#${material.color.getHexString()}`, `Color mismatch ${candidate.id}:${part.instanceId}`);
    }
    provenanceChecks.manifestAuthorAndLicenseMatchOriginal = true;
    provenanceChecks.colorHexVerifiedWithIndependentThreeParser = manifest.instances.length;
    for (const dep of provenance.dependencyFiles) {
      if (!dependencyFiles.has(dep.path)) {
        const actual = hash(await readFile(resolve(ROOT, dep.path)));
        assert.equal(actual, dep.sha256, `Dependency hash mismatch ${dep.path}`);
        dependencyFiles.set(dep.path, dep);
      } else assert.equal(dependencyFiles.get(dep.path).sha256, dep.sha256);
    }
    const flat = (await readFile(resolve(base, 'assembly.ldr'), 'utf8')).split(/\r?\n/).filter(l => /^1\s/.test(l));
    assert.equal(flat.length, manifest.instances.length);
    add(exactProfiles, profile(manifest.instances), candidate.id);
    add(translatedProfiles, profile(manifest.instances, true), candidate.id);
    if (hierarchy?.status === 'pass') {
      assert.equal(hierarchy.manifestSha256, result.manifestSha256);
      assert.equal(hierarchy.instancesCompared, manifest.instances.length);
    }
  }
  rows.push({
    id: candidate.id, kit: candidate.kit, intakeStratum: candidate.intakeStratum,
    title: candidate.title, theme: candidate.theme, original,
    provenanceChecks,
    selectedSourceProfileLabel: chosen?.pageModelLabel ?? null,
    sourceDisplayTitle: chosen?.pageModelLabel === 'Main Model' ? candidate.title : chosen?.pageModelLabel ?? null,
    lockedDependencyCompatible: result?.status === 'manifest-ready'
      ? result.embeddedPartLockedPathConflicts.length === 0 : null,
    intakeStatus: result?.status ?? 'pending', intakeError: result?.error ?? null,
    manifestFile: result?.manifestFile ?? null, manifestSha256: result?.manifestSha256 ?? null,
    instances: manifest?.instances.length ?? null,
    hierarchyStatus: hierarchy?.status ?? (result?.status === 'intake-failed' ? 'not-run-intake-failed' : 'pending'),
    hierarchyError: hierarchy?.error ?? null,
    sourceFidelityReady: result?.status === 'manifest-ready' && hierarchy?.status === 'pass',
    omrDeclaresNoMissingParts: chosen?.completeness['Missing Parts'] === 'No',
    geometryQualification: null,
  });
}
const originals = rows.filter(r => r.original);
assert.equal(new Set(originals.map(r => r.original.sourceHash)).size, originals.length, 'Duplicate new originals');
for (const previous of registry.previousModels) {
  const path = resolve(ROOT, 'web/public/models', previous.modelId, 'manifest.json');
  assert.equal(hash(await readFile(path)), previous.sha256, `Historical manifest changed: ${previous.modelId}`);
}
const protectedFiles = ['atlas.config.ts', 'assets-source/provenance.json', 'assets-source/library-lock.json',
  'scripts/ldraw.ts', 'scripts/build-assets.ts', 'scripts/acquire-model.ts', 'scripts/verify-reference.ts'];
const protectedRecords = protectedFiles.map(file => {
  const expected = execFileSync('git', ['show', `HEAD:${file}`], { cwd: ROOT, maxBuffer: 16 * 1024 * 1024 });
  return { file, headSha256: hash(expected) };
});
for (const record of protectedRecords) {
  assert.equal(hash(await readFile(resolve(ROOT, record.file))), record.headSha256, `Protected file changed: ${record.file}`);
}
const newLockedFiles = execFileSync('git', ['ls-files', '--others', '--exclude-standard', '-z',
  '--', 'assets-source/ldraw-library/locked'], { cwd: ROOT }).toString().split('\0').filter(Boolean);
if (newLockedFiles.length) {
  const globalProvenance = JSON.parse(await readFile(resolve(ROOT, 'assets-source/provenance.json'), 'utf8'));
  const archiveRecord = globalProvenance.resources.find((r: any) => r.file.endsWith('complete.zip'));
  const archive = await readFile(resolve(ROOT, archiveRecord.file));
  assert.equal(hash(archive), archiveRecord.sha256);
  const entries = new Map((await readZip(archive)).map(e => [normalize(e.entryName.replace(/^ldraw\//, '')), e]));
  const originsByHash = new Map([...dependencyFiles.values()].map(d => [d.sha256, d]));
  for (const path of newLockedFiles) {
    const bytes = await readFile(resolve(ROOT, path)), sha256 = hash(bytes);
    const key = normalize(path.slice('assets-source/ldraw-library/locked/'.length));
    const entry = entries.get(key);
    const origin = originsByHash.get(sha256);
    if (entry && hash(await entry.getData()) === sha256) {
      const file = splitMpd(bytes.toString('utf8'), key).values().next().value!;
      dependencyFiles.set(path, {
        file: key, path, sha256, author: header(file, 'Author:'), license: header(file, '!LICENSE'),
        origin: 'Historical hash-locked LDraw library', archiveSha256: archiveRecord.sha256,
        introducedInV23: true,
      });
    } else {
      assert(origin?.containerSha256, `New locked file lacks verified archive or MPD origin: ${path}`);
      dependencyFiles.set(path, {
        ...origin, path, embeddedSectionPath: origin.path, introducedInV23: true,
      });
    }
  }
}
const countBy = (key: string) => Object.fromEntries([...new Set(rows.map(r => r[key]))]
  .sort().map(value => [value, rows.filter(r => r[key] === value).length]));
const summary = {
  schema: 'brickplan-v23-source-intake-summary/1.0',
  candidateRegistrySha256: frozenHash, frozenCandidates: registry.count,
  downloadedOriginals: originals.length, manifestReady: rows.filter(r => r.intakeStatus === 'manifest-ready').length,
  sourceFidelityReady: rows.filter(r => r.sourceFidelityReady).length,
  independentKitCount: rows.filter(r => r.sourceFidelityReady).length,
  fidelityReadyAndOMRDeclaresNoMissingParts: rows.filter(
    r => r.sourceFidelityReady && r.omrDeclaresNoMissingParts).length,
  omrMissingPartsDeclarations: rows.filter(r => r.original?.completeness['Missing Parts'] === 'Yes').map(r => r.id),
  fidelityReadyAuthors: [...new Set(rows.filter(r => r.sourceFidelityReady).map(r => r.original.author))].sort(),
  normalizedSourceAuthorDisplayNames: [...new Set(originals.map(r => authorName(r.original.author)))].sort(),
  authorNormalizationCaveat: 'Display-name deduplication only, not verified personal identity; exact source/page headers and contribution history retained per source.',
  rawSourceAuthors: [...new Set(originals.map(r => r.original.author))].sort(),
  rawSourceLicenses: [...new Set(originals.map(r => r.original.license))].sort(),
  strata: countBy('intakeStratum'), themes: countBy('theme'),
  intakeStatuses: countBy('intakeStatus'), hierarchyStatuses: countBy('hierarchyStatus'),
  duplicateExactProfiles: [...exactProfiles.values()].filter(ids => ids.length > 1 && ids.some(id => id.startsWith('v23-'))),
  duplicateTranslationInvariantProfiles: [...translatedProfiles.values()].filter(ids => ids.length > 1 && ids.some(id => id.startsWith('v23-'))),
  duplicateProfileScope: 'Full part/type/color/pose multisets, exact and translation-normalized, across new and historical manifests; not a design-genealogy or rotation-invariance proof.',
  licenseDocuments,
  dependenciesChecked: dependencyFiles.size, protectedRecords,
  newLockedFilesVerified: newLockedFiles.length,
  historicalManifestsChecked: registry.previousModels.length,
  geometryQualification: null, taskOrOracleOrPolicyResults: null,
  selectionCaveat: 'Metadata-stratified convenience intake; kit count does not establish statistical independence or R5 closure.',
  rows,
};
if (suffix === 'final') {
  assert(rows.length === 100 && rows.every(r => r.intakeStatus !== 'pending' && r.hierarchyStatus !== 'pending'),
    'Final report requires all frozen candidates accounted for');
}
await writeNew(resolve(OUTPUT, `summary-${suffix}.json`), JSON.stringify(summary, null, 2) + '\n');
await writeNew(resolve(OUTPUT, `dependency-lock-${suffix}.json`),
  JSON.stringify([...dependencyFiles.values()].sort((a, b) => a.path.localeCompare(b.path)), null, 2) + '\n');
if (suffix === 'final') {
  await writeNew(resolve(OUTPUT, 'full-source-verification.json'), JSON.stringify({
    candidateRegistrySha256: frozenHash, denominator: registry.count,
    method: 'Independent Three.js original-hierarchy parser pose/part/color audit; unprepared candidates explicitly not run',
    statuses: countBy('hierarchyStatus'),
    candidates: rows.map(r => ({
      id: r.id, kit: r.kit, sourceHash: r.original?.sourceHash ?? null,
      manifestSha256: r.manifestSha256, status: r.hierarchyStatus,
      error: r.hierarchyError ?? r.intakeError, sourceFidelityReady: r.sourceFidelityReady,
      lockedDependencyCompatible: r.lockedDependencyCompatible,
      omrDeclaresNoMissingParts: r.omrDeclaresNoMissingParts,
      selectedSourceProfileLabel: r.selectedSourceProfileLabel,
      provenanceChecks: r.provenanceChecks,
      report: r.hierarchyStatus === 'not-run-intake-failed' ? `results/${r.id}.json`
        : `hierarchy-checks/${r.id}.json`,
    })),
  }, null, 2) + '\n');
}
console.log(JSON.stringify({
  frozen: summary.frozenCandidates, raw: summary.downloadedOriginals, manifests: summary.manifestReady,
  fidelityReady: summary.sourceFidelityReady, statuses: summary.intakeStatuses,
  hierarchy: summary.hierarchyStatuses, authors: summary.rawSourceAuthors.length,
  historicalManifestsUnchanged: summary.historicalManifestsChecked,
}, null, 2));
