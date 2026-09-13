import assert from 'node:assert/strict';

export interface SourceAsset {
  id: string;
  origin: 'procedural' | 'external';
  url: string;
  revision: string;
  license: string | null;
  permissionEvidence: string | null;
  permittedUses: string[];
  contentSha256: string | null;
  objects: number;
  independentSourceFamilies: number;
}
export function sourceGate(asset: SourceAsset) {
  assert.match(asset.id, /^[a-z0-9_-]+$/);
  assert.ok(Number.isInteger(asset.objects) && asset.objects >= 0);
  assert.ok(Number.isInteger(asset.independentSourceFamilies) && asset.independentSourceFamilies >= 0);
  assert.ok(asset.independentSourceFamilies <= asset.objects);
  const missing = [];
  if (!asset.url || !asset.revision) missing.push('provenance');
  if (!asset.license) missing.push('license');
  if (!asset.permissionEvidence) missing.push('permission-evidence');
  if (!asset.permittedUses.includes('redistribute-derived-data')) missing.push('redistribution-scope');
  if (!asset.contentSha256 || !/^[a-f0-9]{64}$/.test(asset.contentSha256)) missing.push('content-hash');
  if (!asset.objects || !asset.independentSourceFamilies) missing.push('actual-assets');
  return { id: asset.id, readyForRelease: missing.length === 0, missing,
    note: 'Checks declared provenance fields, not legal advice or independent verification of permission authenticity.' };
}

export const EXTERNAL_SOURCE_CANDIDATES: SourceAsset[] = [
  { id: 'bricknet-human-designs', origin: 'external', url: 'https://kulits.github.io/BrickNet/',
    revision: 'CVPR-2026-paper', license: null, permissionEvidence: null, permittedUses: [],
    contentSha256: null, objects: 0, independentSourceFamilies: 0 },
  { id: 'stabletext2brick', origin: 'external', url: 'https://huggingface.co/datasets/AvaLovelace/StableText2Brick',
    revision: 'ICCV-2025-paper', license: null, permissionEvidence: null, permittedUses: [],
    contentSha256: null, objects: 0, independentSourceFamilies: 0 },
];
