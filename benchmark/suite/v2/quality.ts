import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { canonicalGeometry, cells, dims, edges } from '../geometry';
import { dataset, POLICIES } from './dataset';
import { DIRECTORY } from './build';

function hash32(text: string, seed: number) {
  let h = seed;
  for (let i = 0; i < text.length; i++) h = Math.imul(h ^ text.charCodeAt(i), 16777619);
  return h >>> 0;
}
export function qualityAudit() {
  const models = dataset(), signatures = models.map(m => canonicalGeometry(m.structure.parts).split('|'));
  const buckets = new Map<string, number[]>(), candidatePairs = new Set<string>(), matches = [];
  for (const [i, tokens] of signatures.entries()) {
    const mins = Array.from({ length: 32 }, (_, seed) => Math.min(...tokens.map(t => hash32(t, 2166136261 ^ (seed * 2654435761)))));
    for (let band = 0; band < 8; band++) {
      const key = band + ':' + mins.slice(band * 4, band * 4 + 4).join(',');
      for (const j of buckets.get(key) ?? []) if (models[i].split !== models[j].split) candidatePairs.add(`${j}:${i}`);
      buckets.set(key, [...(buckets.get(key) ?? []), i]);
    }
  }
  for (const pair of candidatePairs) {
    const [i, j] = pair.split(':').map(Number), a = new Set(signatures[i]), b = new Set(signatures[j]);
    const intersection = [...a].filter(t => b.has(t)).length, jaccard = intersection / (a.size + b.size - intersection);
    if (jaccard >= 0.8) matches.push({ a: models[i].id, b: models[j].id, splitA: models[i].split, splitB: models[j].split,
      jaccard, containment: intersection / Math.min(a.size, b.size) });
  }
  const policyRows = POLICIES.map(policy => {
    const rows = models.filter(m => m.policy === policy).map(m => {
      const p = m.structure.parts, links = edges(p), occupied = cells(p);
      const boxVolume = m.parameters.width * m.parameters.depth * m.parameters.height;
      const supports = p.map(a => p.filter(b => b.y + dims(b).h === a.y
        && links.some(e => e.a === a.id && e.b === b.id || e.b === a.id && e.a === b.id)).length);
      return { pieces: p.length, height: m.parameters.height, connections: links.length,
        multiSupported: supports.filter(n => n >= 2).length, fill: occupied.size / boxVolume };
    });
    return { policy, objects: rows.length, mean: Object.fromEntries(Object.keys(rows[0]).map(k =>
      [k, rows.reduce((n, r) => n + r[k as keyof typeof r], 0) / rows.length])) };
  });
  const exactGroups = new Map<string, Set<string>>();
  for (const m of models) {
    const geometry = canonicalGeometry(m.structure.parts);
    const splits = exactGroups.get(geometry) ?? new Set<string>(); splits.add(m.split); exactGroups.set(geometry, splits);
  }
  const result = { structures: models.length, policyRows, exactCrossSplitDuplicates: [...exactGroups.values()].filter(s => s.size > 1).length,
    approximateNearDuplicateAudit: { representation: 'colorless yaw/translation canonical part-position sets',
      minhashes: 32, bands: 8, threshold: 0.8, candidatePairs: candidatePairs.size,
      flagged: matches.sort((a, b) => b.jaccard - a.jaccard), exhaustive: false,
      warning: 'LSH can miss near duplicates; this is screening, not proof of no semantic or subassembly leakage.' } };
  atomicJson(resolve(DIRECTORY, 'quality-audit.json'), result);
  return { structures: models.length, candidates: candidatePairs.size, flagged: matches.length, policyRows };
}
