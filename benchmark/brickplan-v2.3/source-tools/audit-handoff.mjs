import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { sourceState } from './source-state.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const state = sourceState(root);
const out = process.env.SOURCE_INTAKE_OUTPUT ?? '/tmp/brickplan-v23-work/source-intake';
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const read = file => fs.readFileSync(file);
const json = file => JSON.parse(read(file));
function writeReport(name, text) {
  const file = path.join(out, name);
  if (fs.existsSync(file)) {
    const previous = read(file);
    if (sha(previous) !== sha(text)) {
      const history = path.join(out, 'handoff-history');
      fs.mkdirSync(history, { recursive: true });
      const archive = path.join(history, `${sha(previous)}-${name}`);
      if (fs.existsSync(archive)) assert.equal(sha(read(archive)), sha(previous));
      else fs.writeFileSync(archive, previous, { flag: 'wx' });
    }
  }
  fs.writeFileSync(file, text);
}
const frozen = read(path.join(state, 'candidate-registry.frozen.json'));
assert.equal(sha(frozen), '3518c3357872225b0425ee6bcd2a0aa8350aca0791d7b83dd056d5baec081f0b');
const registry = JSON.parse(frozen);
const summary = json(path.join(out, 'summary-final.json'));
const identities = json(path.join(out, 'identity-verification.json'));
const identityMap = new Map(identities.records.map(row => [row.id, row]));
const summaryMap = new Map(summary.rows.map(row => [row.id, row]));
const rows = [];
for (const candidate of registry.candidates) {
  const resultPath = path.join(state, 'results', `${candidate.id}.json`);
  const result = json(resultPath);
  const identity = identityMap.get(candidate.id);
  assert(identity && !['failed', 'pending'].includes(identity.status), `Identity evidence ${candidate.id}`);
  let proof = null, proofBytes = null, proofPath = null;
  if (result.status === 'manifest-ready') {
    proofPath = path.join(out, 'leaf-proofs', `${candidate.id}.json`);
    proofBytes = read(proofPath);
    proof = JSON.parse(proofBytes);
    assert.equal(proof.ordinaryLeafStatus, 'pass', candidate.id);
    assert.equal(proof.packedHierarchyStatus, 'pass', candidate.id);
    assert.equal(proof.manifestSha256, result.manifestSha256);
    assert.equal(proof.originalSha256, result.sourceHash);
    assert.equal(proof.instancesCompared, result.stats.instances);
    assert.equal(proof.leaves.length, proof.instancesCompared);
    assert.equal(identity.originalSha256, result.sourceHash);
  } else assert.equal(result.status, 'intake-failed');
  rows.push({
    id: candidate.id, kit: candidate.kit, title: candidate.title,
    intakeStatus: result.status, intakeError: result.error ?? null,
    intakeRecordPath: path.relative(root, resultPath), intakeRecordSha256: sha(read(resultPath)),
    originalFile: identity.originalPath ?? null, originalSha256: result.sourceHash,
    manifestFile: result.manifestFile ?? null, manifestSha256: result.manifestSha256 ?? null,
    packedHierarchyFile: proof?.packedHierarchyFile ?? null,
    ordinaryLeafStatus: proof?.ordinaryLeafStatus ?? 'not-run-intake-failed',
    fullHierarchyStatus: proof?.fullHierarchyStatus ?? 'not-run-intake-failed',
    packedHierarchyStatus: proof?.packedHierarchyStatus ?? 'not-run-intake-failed',
    instancesCompared: proof?.instancesCompared ?? 0,
    directGeometryOccurrences: proof?.directGeometry.length ?? null,
    proofPath, proofSha256: proofBytes ? sha(proofBytes) : null,
    sourceIdentity: identity,
    authorHeaderMatchesPage: identity.sourceAuthor ? identity.sourceAuthor === identity.pageAuthor : null,
    authorAttributionEvidence: identity.authorAttribution ?? null,
    lockedDependencyCompatible: summaryMap.get(candidate.id).lockedDependencyCompatible,
    sourceFidelityGatePass: result.status === 'manifest-ready' &&
      proof.fullHierarchyStatus === 'pass' && identity.status === 'pass' &&
      identity.manifestMetadataStatus === 'pass' &&
      summaryMap.get(candidate.id).lockedDependencyCompatible === true,
  });
}
assert.equal(rows.length, 100);
const countBy = key => rows.reduce((counts, row) =>
  ({ ...counts, [row[key]]: (counts[row[key]] ?? 0) + 1 }), {});
const toolDir = path.dirname(fileURLToPath(import.meta.url));
const report = {
  schema: 'brickplan-source-audit-handoff/1.0', generatedAt: new Date().toISOString(),
  candidateRegistrySha256: sha(frozen), denominator: 100,
  intakeStatuses: countBy('intakeStatus'), fullHierarchyStatuses: countBy('fullHierarchyStatus'),
  ordinaryLeavesCompared: rows.reduce((total, row) => total + row.instancesCompared, 0),
  admissionStateIncluded: false,
  fullHierarchyFailures: rows.filter(row =>
    row.intakeStatus === 'manifest-ready' && row.fullHierarchyStatus !== 'pass').map(row => row.id),
  identityConflicts: rows.filter(row => row.sourceIdentity.originalIdentityStatus === 'conflict')
    .map(row => ({ id: row.id, rootFile: row.sourceIdentity.rootFile,
      issues: row.sourceIdentity.issues })),
  authorAttributionDifferences: rows.filter(row => row.authorHeaderMatchesPage === false).map(row => ({
    id: row.id, sourceAuthor: row.sourceIdentity.sourceAuthor, pageAuthor: row.sourceIdentity.pageAuthor,
    evidence: row.authorAttributionEvidence, history: row.sourceIdentity.sourceHistory,
  })),
  semantics: {
    ordinaryLeaves: 'Every original ordinary leaf is bound to an exact manifest ID, source chain, matrix, part and color.',
    fullHierarchy: 'Fails if direct model geometry is omitted; passing ordinary leaves never overrides this failure.',
    identity: 'Hash-bound official OMR index/detail snapshots and actual MPD authors/licenses, including contributor history.',
    inventory: 'Full selected MPD-root inventory, not official LEGO retail BOM or complete physical-set certification.',
    ownership: 'Main owns admission, sourceAudit integration and bank decisions; no benchmark data written by this tool.',
    admissionState: 'Excluded: no admission records are read or hashed, and source gate results do not assert taskbank inclusion.',
  },
  evidenceFiles: ['summary-final.json', 'dependency-lock-final.json', 'full-source-verification.json',
    'identity-verification.json', 'leaf-proof-test-results.json', 'unit-test-results.json',
    'protected-byte-verification.json',
    ...['archive-requirements.json', 'source-state-test-results.json']
      .filter(file => fs.existsSync(path.join(out, file)))]
    .map(file => ({ path: path.join(out, file), sha256: sha(read(path.join(out, file))) })),
  durableTools: fs.readdirSync(toolDir).filter(file => /\.(py|ts|mjs|mts)$/.test(file)).sort()
    .map(file => ({ path: path.relative(root, path.join(toolDir, file)), sha256: sha(read(path.join(toolDir, file))) })),
  rows,
};
writeReport('source-audit-handoff.json', JSON.stringify(report, null, 2) + '\n');
const lines = [
  '# V23 Source Intake And Original-Hierarchy Audit', '',
  '## Inventory', '',
  `All ${rows.length} frozen candidates have final intake result records. Registry SHA256: \`${sha(frozen)}\`.`,
  `Ordinary leaves compared: ${report.ordinaryLeavesCompared}. Mutable admission state is deliberately excluded.`, '',
  '| Intake status | Count |', '| --- | ---: |',
  ...Object.entries(report.intakeStatuses).map(([key, value]) => `| ${key} | ${value} |`), '',
  '## Gate Findings', '',
  `Full-hierarchy failures among prepared sources: ${report.fullHierarchyFailures.join(', ') || 'none'}.`,
  `Original/catalog identity conflicts: ${report.identityConflicts.map(row => row.id).join(', ') || 'none'}.`,
  'Ordinary-leaf equality does not certify omitted direct geometry, physical support or official retail-set completeness.',
  'Page/header author differences remain explicit; normalized display names and MPD contributor history are evidence, not literal equality.', '',
  '## Per-Candidate Results', '',
  '| Model | Intake | Leaves | Full hierarchy | Identity |',
  '| --- | --- | ---: | --- | --- |',
  ...rows.map(row => `| ${row.id} | ${row.intakeStatus} | ${row.instancesCompared} | ${row.fullHierarchyStatus} | ${row.sourceIdentity.status} |`), '',
  '## Evidence And Limitations', '',
  'The machine-readable `source-audit-handoff.json` binds each source URL, local original, manifest, detailed leaf proof and dependency proof to SHA256 hashes. Admission records and counts are intentionally absent.',
  'Official evidence comes from OMR index pages, detail pages and original MPD headers within one publisher; it is not three independent publishers or LEGO endorsement.',
  'The `leaf-proofs/` records retain full reference chains and inventories. Direct geometry is recorded separately and receives no invented part IDs.',
  'Source tools resolve the registered intake directory first, then `benchmark/brickplan-v2.3/data/source-intake` only when the registered directory is absent. Registry bytes and frozen path declarations are never rewritten.',
  'Clean-checkout metadata requirements are enumerated by raw SHA256 in `archive-requirements.json`; the source-tools README lists the exact details/snapshots set. `source-state-test-results.json` distinguishes an isolated restored-fixture pass from actual archive readiness.',
  'Original poses, source colors, source leaf IDs and tracked historical bytes were not repaired or replaced. No qualification, benchmark bank, commit or push was performed by source intake.', '',
];
writeReport('REPORT.md', lines.join('\n'));
console.log(JSON.stringify({ results: rows.length, intake: report.intakeStatuses,
  hierarchy: report.fullHierarchyStatuses, leaves: report.ordinaryLeavesCompared,
  admissionStateIncluded: report.admissionStateIncluded,
  gateFailures: report.fullHierarchyFailures, identityConflicts: report.identityConflicts }, null, 2));
