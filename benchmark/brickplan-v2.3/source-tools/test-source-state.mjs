import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { gunzipSync } from 'node:zlib';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { sourceState, legacyStatePath, archivedStatePath } from './source-state.mjs';

const tools = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(tools, '../../..');
const out = process.env.SOURCE_INTAKE_OUTPUT ?? '/tmp/brickplan-v23-work/source-intake';
const state = sourceState(root), archive = path.join(root, archivedStatePath);
const frozen = '3518c3357872225b0425ee6bcd2a0aa8350aca0791d7b83dd056d5baec081f0b';
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const json = file => JSON.parse(fs.readFileSync(file));
fs.mkdirSync(out, { recursive: true });
const fixture = fs.mkdtempSync(path.join(out, 'clean-checkout-test-'));
const checks = [], commands = [];
function run(command, args, cwd = root, output = out) {
  const result = spawnSync(command, args, { cwd, encoding: 'utf8', timeout: 120000,
    maxBuffer: 8 * 1024 * 1024,
    env: { ...process.env, SOURCE_INTAKE_OUTPUT: output, PYTHONDONTWRITEBYTECODE: '1' } });
  commands.push({ command, args, status: result.status, stdout: result.stdout, stderr: result.stderr });
  assert.equal(result.status, 0, result.error?.message || result.stderr || result.stdout);
  return result.stdout;
}

const resolutionRoot = path.join(fixture, 'resolution');
const pythonResolve = () => run('python3', ['-c',
  'import sys; from pathlib import Path; sys.path.insert(0,sys.argv[1]); from source_state import source_state; print(source_state(Path(sys.argv[2])))',
  tools, resolutionRoot]).trim();
function checkResolution(label, expected) {
  assert.equal(sourceState(resolutionRoot), path.join(resolutionRoot, expected));
  assert.equal(pythonResolve(), path.join(resolutionRoot, expected));
  checks.push(label);
}
checkResolution('Both languages select archive when legacy state is absent', archivedStatePath);
fs.mkdirSync(path.join(resolutionRoot, archivedStatePath), { recursive: true });
checkResolution('Both languages resolve an existing archive', archivedStatePath);
fs.mkdirSync(path.join(resolutionRoot, legacyStatePath), { recursive: true });
checkResolution('Both languages preserve legacy precedence, even when incomplete', legacyStatePath);

const registryBytes = fs.readFileSync(path.join(state, 'candidate-registry.frozen.json'));
assert.equal(sha(registryBytes), frozen);
const registry = JSON.parse(registryBytes);
const required = new Set(['candidate-registry.frozen.json', 'candidate-registry.frozen.sha256']);
const indexPages = new Set();
for (const candidate of registry.candidates) {
  required.add(`results/${candidate.id}.json`);
  required.add(`details/${candidate.kit}.json`);
  indexPages.add(candidate.indexPage);
  const token = new URL(candidate.sourceUrl).pathname.split('/').at(-1);
  for (const stem of [`index-${String(candidate.indexPage).padStart(2, '0')}`, `set-${token}`]) {
    required.add(`snapshots/${stem}.html`);
    required.add(`snapshots/${stem}.fetch.json`);
  }
}
const stateFiles = [...required].sort().map(relativePath => {
  const sourcePath = path.join(state, relativePath), archivePath = path.join(archive, relativePath);
  const sha256 = sha(fs.readFileSync(sourcePath));
  const present = fs.existsSync(archivePath);
  if (present) assert.equal(sha(fs.readFileSync(archivePath)), sha256, `Archived input changed ${relativePath}`);
  return { relativePath, sourcePath, archivePath, sha256, archiveStatus: present ? 'verified' : 'missing' };
});
checks.push(`All ${stateFiles.length} required frozen metadata files inventoried by byte hash`);
const requirements = { schema: 'brickplan-source-archive-requirements/1.0',
  candidateRegistrySha256: frozen, legacyStatePath, archivedStatePath,
  archiveReady: stateFiles.every(file => file.archiveStatus === 'verified'),
  counts: { candidates: registry.candidates.length, details: registry.candidates.length,
    indexHtml: indexPages.size, detailHtml: registry.candidates.length,
    fetchRecords: indexPages.size + registry.candidates.length, totalStateFiles: stateFiles.length },
  missingArchivedFiles: stateFiles.filter(file => file.archiveStatus === 'missing').map(file => file.relativePath),
  stateFiles };
fs.writeFileSync(path.join(out, 'archive-requirements.json'), JSON.stringify(requirements, null, 2) + '\n');

const checkout = path.join(fixture, 'checkout');
const fixtureTools = path.join(checkout, 'benchmark/brickplan-v2.3/source-tools');
fs.cpSync(tools, fixtureTools, { recursive: true });
for (const name of ['package.json', 'node_modules', 'scripts', 'src', 'atlas.config.ts',
  'assets-source', 'web', '.tools', '.git']) fs.symlinkSync(path.join(root, name), path.join(checkout, name));
for (const file of stateFiles) {
  const target = path.join(checkout, archivedStatePath, file.relativePath);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.copyFileSync(file.sourcePath, target);
}
assert(!fs.existsSync(path.join(checkout, 'tem')));
assert.equal(sourceState(checkout), path.join(checkout, archivedStatePath));
const output = path.join(fixture, 'output');
fs.mkdirSync(path.join(output, 'leaf-proofs'), { recursive: true });
let archivedProofs = 0;
for (const candidate of registry.candidates) {
  const intake = json(path.join(state, 'results', `${candidate.id}.json`));
  if (intake.status !== 'manifest-ready') continue;
  const name = `${candidate.id}.json`;
  const raw = gunzipSync(fs.readFileSync(path.join(archive, 'leaf-proofs', `${name}.gz`)));
  assert.equal(sha(raw), sha(fs.readFileSync(path.join(out, 'leaf-proofs', name))));
  fs.writeFileSync(path.join(output, 'leaf-proofs', name), raw);
  archivedProofs++;
}
assert.equal(archivedProofs, 96);
checks.push('All 96 archived gzip proofs preserve the exact uncompressed proof hashes');

run(process.execPath, [path.join(root, 'node_modules/typescript/bin/tsc'),
  '--pretty', 'false', '--noEmit', '--strict', '--skipLibCheck', '--module', 'ESNext',
  '--moduleResolution', 'Bundler', '--target', 'ES2022', '--allowImportingTsExtensions',
  '--resolveJsonModule', '--esModuleInterop',
  ...['intake.ts', 'summarize.ts', 'verify-hierarchy.ts', 'test-intake.ts'].map(file => path.join(tools, file))]);
checks.push('Strict TypeScript compile passes with repository Bundler module resolution and .d.mts declarations');
run(process.execPath, ['--import', 'tsx', path.join(fixtureTools, 'test-intake.ts')], checkout, output);
checks.push('Sixteen parser/write tests pass from the checkout without tem');
run(process.execPath, ['--import', 'tsx', path.join(fixtureTools, 'intake.ts'), '--range=1:100'], checkout, output);
checks.push('Archived intake resolves all 100 existing results without redownloading originals');
run(process.execPath, ['--import', 'tsx', path.join(fixtureTools, 'verify-hierarchy.ts'), '--id=v23-21004'],
  checkout, output);
assert.equal(json(path.join(output, 'hierarchy-checks/v23-21004.json')).status, 'pass');
checks.push('Independent hierarchy parser passes using archived intake records');
run(process.execPath, [path.join(fixtureTools, 'verify-leaves.mjs'), '--id=v23-21004'], checkout, output);
assert.equal(sha(fs.readFileSync(path.join(output, 'leaf-proofs/v23-21004.json'))),
  sha(fs.readFileSync(path.join(out, 'leaf-proofs/v23-21004.json'))));
checks.push('Regenerated original-leaf proof is byte-identical through archive fallback');
run(process.execPath, [path.join(fixtureTools, 'test-leaf-proof.mjs')], checkout, output);
checks.push('Fourteen real-leaf/corruption tests pass with gzip-restored proofs');
run('python3', ['-c', [
  'import sys,runpy,subprocess',
  'sys.path.insert(0,sys.argv[1])',
  'def deny_network(*args, **kwargs): raise RuntimeError("Network forbidden in offline metadata test")',
  'subprocess.check_output = deny_network',
  'runpy.run_path(sys.argv[2],run_name="__main__")',
].join('\n'), fixtureTools, path.join(fixtureTools, 'verify-identities.py')], checkout, output);
const identity = json(path.join(output, 'identity-verification.json'));
const expectedIdentity = json(path.join(out, 'identity-verification.json'));
assert.deepEqual(identity.records.map(row => [row.id, row.status, row.manifestSha256, row.originalSha256]),
  expectedIdentity.records.map(row => [row.id, row.status, row.manifestSha256, row.originalSha256]));
checks.push('All 100 identities retain outcomes and source hashes using only archived HTML/fetch metadata');
fs.cpSync(path.join(out, 'hierarchy-checks'), path.join(output, 'hierarchy-checks'), { recursive: true });
run(process.execPath, ['--import', 'tsx', path.join(fixtureTools, 'summarize.ts'), '--label=clean-checkout'],
  checkout, output);
const summary = json(path.join(output, 'summary-clean-checkout.json'));
assert.equal(summary.frozenCandidates, 100);
assert.equal(summary.manifestReady, 96);
assert.equal(summary.sourceFidelityReady, 91);
checks.push('Summary resolves all frozen candidates and preserves whole-hierarchy failure counts without tem');
for (const name of ['summary-final.json', 'dependency-lock-final.json', 'full-source-verification.json',
  'protected-byte-verification.json', 'archive-requirements.json'])
  fs.copyFileSync(path.join(out, name), path.join(output, name));
run(process.execPath, [path.join(fixtureTools, 'audit-handoff.mjs')], checkout, output);
const handoff = json(path.join(output, 'source-audit-handoff.json'));
assert.equal(handoff.admissionStateIncluded, false);
assert.equal(handoff.rows.length, 100);
assert.equal(handoff.ordinaryLeavesCompared, 54978);
assert(handoff.rows.every(row => row.intakeRecordPath.startsWith(archivedStatePath + '/')));
for (const tool of handoff.durableTools)
  assert.equal(sha(fs.readFileSync(path.join(checkout, tool.path))), tool.sha256);
checks.push('Source-only handoff resolves archived results and binds all current tools, including .d.mts');
for (const file of stateFiles) assert.equal(sha(fs.readFileSync(file.sourcePath)), file.sha256);
checks.push('Every original state input remains byte-identical');
const report = { schema: 'brickplan-source-state-test/1.0', status: 'pass',
  fixture, fixtureUsesTem: false, liveStateModified: false, archiveReady: requirements.archiveReady,
  missingArchivedFiles: requirements.missingArchivedFiles.length, archivedProofs, checks, commands };
fs.writeFileSync(path.join(out, 'source-state-test-results.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({ status: report.status, checks: checks.length, fixture,
  archivedProofs, archiveReady: report.archiveReady, missingArchivedFiles: report.missingArchivedFiles }, null, 2));
