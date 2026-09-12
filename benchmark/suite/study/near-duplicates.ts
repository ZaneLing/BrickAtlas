import { atomicJson } from '../../core/budget';
import { resolve } from 'node:path';
import { canonicalGeometry } from '../geometry';
import { dataset } from '../v2/dataset';
import { STUDY } from './protocol';
import assert from 'node:assert/strict';

export function exactNearDuplicates(threshold = 0.8) {
  const models = dataset();
  const sets = models.map(m => [...new Set(canonicalGeometry(m.structure.parts).split('|'))]);
  const frequencies = new Map<string, number>();
  for (const s of sets) for (const token of s) frequencies.set(token, (frequencies.get(token) ?? 0) + 1);
  for (const s of sets) s.sort((a, b) => frequencies.get(a)! - frequencies.get(b)! || a.localeCompare(b));
  const sorted = sets.map((s, index) => ({ s, index })).sort((a, b) => a.s.length - b.s.length || a.index - b.index);
  const index = new Map<string, number[]>(), candidates = new Set<number>(), flagged = [];
  let comparisons = 0;
  // Lossless prefix filtering for Jaccard threshold joins under one global order.
  // Any qualifying pair must share a token in these prefixes.
  for (const entry of sorted) {
    candidates.clear();
    const prefix = entry.s.slice(0, entry.s.length - Math.ceil(threshold * entry.s.length) + 1);
    for (const token of prefix) for (const previous of index.get(token) ?? []) {
      if (models[previous].split !== models[entry.index].split
        && sets[previous].length >= threshold * entry.s.length) candidates.add(previous);
    }
    const current = new Set(entry.s);
    for (const previous of candidates) {
      comparisons++;
      const overlap = sets[previous].filter(t => current.has(t)).length;
      const score = overlap / (sets[previous].length + entry.s.length - overlap);
      if (score + 1e-12 >= threshold) flagged.push({ a: models[previous].id, b: models[entry.index].id,
        splits: [models[previous].split, models[entry.index].split], jaccard: score });
    }
    for (const token of prefix) index.set(token, [...index.get(token) ?? [], entry.index]);
  }
  const allSets = sets.map(s => new Set(s)), brute = new Set<string>();
  let crossSplitPairs = 0;
  for (let i = 0; i < models.length; i++) for (let j = i + 1; j < models.length; j++) {
    if (models[i].split === models[j].split) continue;
    crossSplitPairs++;
    if (Math.min(sets[i].length, sets[j].length) < threshold * Math.max(sets[i].length, sets[j].length)) continue;
    let intersection = 0;
    for (const t of sets[i]) if (allSets[j].has(t)) intersection++;
    if (intersection / (sets[i].length + sets[j].length - intersection) + 1e-12 >= threshold) {
      brute.add([models[i].id, models[j].id].sort().join(':'));
    }
  }
  assert.deepEqual(new Set(flagged.map(p => [p.a, p.b].sort().join(':'))), brute);
  const report = { objects: models.length, threshold, candidateComparisons: comparisons, flagged, crossSplitPairs,
    bruteForceCrossCheck: true,
    method: 'Lossless length/prefix-filtered exact Jaccard join of colorless canonical part-position sets.',
    exhaustiveForDeclaredRepresentation: true,
    limitations: ['Canonical orientation may change after a perturbation; not a best-aligned geometric near-duplicate metric.',
      'No semantic or subassembly containment guarantee; no statement about external pretraining overlap.'] };
  atomicJson(resolve(STUDY, 'exact-near-duplicates.json'), report);
  return report;
}
