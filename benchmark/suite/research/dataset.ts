import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { CATALOG, type Color, type Part, type Split } from '../shared';
import { bounds, canonicalGeometry, contact, dims, edges, insertIssue } from '../geometry';
import { digest, type ModelRecord } from '../data';
import { ARTIFACTS, BENCHMARK } from '../storage';
import { independentCheck } from './independent-check';

export const RESEARCH_VERSION = 'composition-grammar-v1';
export const RULES = [
  'vertical-chain', 'offset-chain', 'branching-frame', 'low-terraces', 'cross-beams', 'plate-stack',
  'alternating-columns', 'mixed-grid', 'stepped-frame', 'wide-canopy', 'narrow-lattice', 'forked-canopy',
];
export interface ResearchRecord extends ModelRecord {
  release: typeof RESEARCH_VERSION;
  topology: string;
  seed: number;
  certificate: { insertionOrder: string[]; independent: boolean };
}
function rng(seed: number) {
  let state = seed >>> 0;
  return () => { state = (Math.imul(state, 1664525) + 1013904223) >>> 0; return state / 4294967296; };
}
export function topologySignature(parts: Part[]) {
  let labels = new Map(parts.map(p => [p.id, p.partId]));
  for (let i = 0; i < 3; i++) {
    labels = new Map(parts.map(p => [p.id, digest([labels.get(p.id),
      parts.filter(q => q.id !== p.id && contact(p, q)).map(q => [labels.get(q.id), contact(p, q)]).sort()]).slice(0, 16)]));
  }
  return digest([...labels.values()].sort()).slice(0, 20);
}
function grow(seed: number, rule: number): Part[] {
  const random = rng(seed), select = <T>(items: T[]) => items[Math.floor(random() * items.length)];
  const colors: Color[] = ['red', 'blue', 'green', 'yellow'];
  const parts: Part[] = [{ id: 'p0', partId: '3035', color: 'gray', x: 8, y: 0, z: 8, turn: 0 }];
  const brickPool = ['3005', '3004', '3622', '3010', '3003', '3002', '3001'];
  const platePool = ['3024', '3023', '3623', '3710', '3022', '3021', '3020'];
  const goal = 8 + seed % 21;
  for (let attempt = 0; attempt < 3500 && parts.length < goal; attempt++) {
    let candidates = parts;
    if (rule <= 1) candidates = parts.slice(-Math.min(4, parts.length));
    if (rule === 3 || rule === 9) candidates = parts.filter(p => p.y < 8);
    if (rule === 5) candidates = parts.slice(-Math.min(6, parts.length));
    const parent = select(candidates);
    const pool = rule === 5 ? platePool : rule === 10 ? ['3005', '3004', '3023']
      : rule === 4 || rule === 11 ? ['3010', '3710', '3001', '3020'] : [...brickPool, ...platePool];
    const partId = select(pool), turn = rule === 6 ? parts.length % 2 : Math.floor(random() * 4);
    const pd = dims(parent), cd = dims({ partId, turn });
    const x = parent.x + Math.floor(random() * (pd.w + cd.w - 1)) - cd.w + 1;
    const z = parent.z + Math.floor(random() * (pd.d + cd.d - 1)) - cd.d + 1;
    const p: Part = { id: `p${parts.length}`, partId, color: colors[(parts.length + rule) % colors.length],
      x, y: parent.y + pd.h, z, turn };
    if (p.y + cd.h > 23 || x < 0 || z < 0 || x + cd.w > 24 || z + cd.d > 24) continue;
    if (insertIssue(parts, p)) continue;
    parts.push(p);
  }
  const minX = Math.min(...parts.map(p => p.x)), minZ = Math.min(...parts.map(p => p.z));
  return parts.map(p => ({ ...p, x: p.x - minX, z: p.z - minZ }));
}

let cached: ResearchRecord[] | undefined;
export function researchModels(): ResearchRecord[] {
  if (cached) return cached;
  const records: ResearchRecord[] = [], seen = new Set<string>();
  for (let rule = 0; rule < RULES.length; rule++) for (let sample = 0; sample < 48; sample++) {
    const seed = 7001 + rule * 1009 + sample * 53;
    const parts = grow(seed, rule);
    if (parts.length < 8) continue;
    const group = digest(canonicalGeometry(parts)).slice(0, 20);
    if (seen.has(group)) continue;
    seen.add(group);
    const independent = independentCheck(parts);
    if (independent.issues.length) throw new Error(`Independent checker rejected ${group}: ${independent.issues}`);
    const topology = topologySignature(parts), box = bounds(parts);
    const bucket = parseInt(group.slice(0, 8), 16) % 10;
    const split: Split = rule >= 10 ? 'test_ood' : bucket < 7 ? 'train' : bucket === 7 ? 'validation' : 'test_id';
    records.push({
      id: 'r' + digest({ seed, group }).slice(0, 19), group, family: RULES[rule], split,
      description: `An open ${RULES[rule]} structure with ${parts.length} interlocking pieces, ${box.x} by ${box.z} studs and ${box.y} plate layers.`,
      parameters: { width: box.x, depth: box.z, height: box.y, palette: rule % 4 },
      structure: { version: 1, parts }, connections: edges(parts),
      provenance: { source: 'procedural', license: 'CC0-1.0', generator: RESEARCH_VERSION },
      release: RESEARCH_VERSION, topology, seed,
      certificate: { insertionOrder: parts.map(p => p.id), independent: true },
    });
  }
  const heldOutTopologies = new Set(records.filter(r => r.split === 'test_ood').map(r => r.topology));
  for (const r of records) if (heldOutTopologies.has(r.topology)) r.split = 'test_ood';
  cached = records;
  return records;
}
export function prepareResearchData() {
  const data = researchModels(), splits: Record<string, number> = {}, families: Record<string, number> = {};
  for (const m of data) { splits[m.split] = (splits[m.split] ?? 0) + 1; families[m.family] = (families[m.family] ?? 0) + 1; }
  const topologyCrossings = [...new Set(data.map(m => m.topology))].filter(t =>
    new Set(data.filter(m => m.topology === t).map(m => m.split)).size > 1).length;
  const manifest = { version: RESEARCH_VERSION, count: data.length, geometryGroups: new Set(data.map(m => m.group)).size,
    topologyGroups: new Set(data.map(m => m.topology)).size, topologyCrossings, splits, families,
    parts: { min: Math.min(...data.map(m => m.structure.parts.length)), max: Math.max(...data.map(m => m.structure.parts.length)),
      vocabulary: [...new Set(data.flatMap(m => m.structure.parts.map(p => p.partId)))].sort() },
    sha256: digest(data), independentHumanModels: 0, independentCheckerPassed: data.length,
    humanAudit: 'not performed; queued separately', physicalClaims: 'integer-cell geometry and stud support only',
    provenance: 'Own procedural composition grammar. Not the BrickNet model dataset.' };
  const output = resolve(ARTIFACTS, 'research'); mkdirSync(output, { recursive: true });
  atomicJson(resolve(output, 'dataset-manifest.json'), manifest);
  atomicJson(resolve(output, 'dataset-examples.json'), RULES.map(family => data.find(m => m.family === family)).filter(Boolean));
  const dir = resolve(BENCHMARK, '.runtime/research'); mkdirSync(dir, { recursive: true });
  writeFileSync(resolve(dir, 'models.jsonl'), data.map(m => JSON.stringify(m)).join('\n') + '\n');
  return manifest;
}
