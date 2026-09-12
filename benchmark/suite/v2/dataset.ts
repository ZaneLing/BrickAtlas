import { CATALOG, type Color, type Part, type Split } from '../shared';
import { bounds, canonicalGeometry, contact, dims, edges, insertIssue } from '../geometry';
import { digest, models as oldModels, type ModelRecord } from '../data';
import { researchModels } from '../research/dataset';
import { independentCheck } from '../research/independent-check';

export const VERSION = 'brickatlas-casebank-2.0';
export const PER_POLICY = 640;
export const POLICIES = [
  'tip-walk', 'low-fan', 'shallow-terrace', 'plate-network',
  'column-field', 'alternating-beams', 'two-support-bridge', 'enclosed-shell',
] as const;
export type Policy = typeof POLICIES[number];
export interface RecordV2 extends ModelRecord {
  policy: Policy; seed: number; difficulty: 'small' | 'medium' | 'large';
  certificate: { insertionOrder: string[]; independent: boolean };
}
export function random(seed: number) {
  let state = seed >>> 0;
  return () => { state = (Math.imul(state, 1664525) + 1013904223) >>> 0; return state / 4294967296; };
}
const colors: Color[] = ['red', 'blue', 'green', 'yellow', 'gray', 'white'];
function generate(policy: Policy, seed: number): Part[] {
  const rng = random(seed), pick = <T>(a: T[]) => a[Math.floor(rng() * a.length)];
  const parts: Part[] = [];
  const add = (partId: string, x: number, y: number, z: number, turn = 0) => {
    const p = { id: `p${parts.length}`, partId, color: pick(colors), x, y, z, turn };
    if (x < 0 || z < 0 || y > 24 || x + dims(p).w > 24 || z + dims(p).d > 24 || insertIssue(parts, p)) return false;
    parts.push(p); return true;
  };
  add('3035', 8, 0, 8);
  if (policy === 'column-field') {
    // Independent height profiles on a common base; no lateral attachment moves.
    const positions = Array.from({ length: 32 }, (_, i) => [8 + i % 8, 8 + Math.floor(i / 8)]);
    for (let i = positions.length - 1; i; i--) {
      const j = Math.floor(rng() * (i + 1)); [positions[i], positions[j]] = [positions[j], positions[i]];
    }
    for (const [x, z] of positions.slice(0, 4 + seed % 6)) {
      let y = 1;
      for (let layer = 0, n = 2 + Math.floor(rng() * 4); layer < n; layer++) {
        const type = rng() < 0.5 ? '3005' : '3024'; add(type, x, y, z); y += CATALOG[type].h;
      }
    }
  } else if (policy === 'two-support-bridge') {
    // Two distinct tower supports are a construction prerequisite for every bridge.
    const zRows = [8, 10];
    for (const z of zRows) {
      const left = 8 + Math.floor(rng() * 2), right = 13 + Math.floor(rng() * 2);
      const height = 2 + Math.floor(rng() * 4);
      for (let level = 0; level < height; level++) {
        add(pick(['3005', '3004']), left, 1 + 3 * level, z, 1);
        add(pick(['3005', '3004']), right, 1 + 3 * level, z, 1);
      }
      add('3460', 8, 1 + height * 3, z);
      for (let k = 0; k < 4; k++) add(pick(['3024', '3005']), 8 + k * 2, 2 + height * 3, z);
    }
  } else if (policy === 'enclosed-shell') {
    // Closed perimeter and roof; varying internal supports create genuine occlusion.
    const levels = 1 + seed % 3;
    for (let level = 0; level < levels; level++) {
      const y = 1 + level * 3;
      add('3008', 8, y, 8); add('3008', 8, y, 11);
      add('3004', 8, y, 9, 1); add('3004', 15, y, 9, 1);
    }
    for (let x = 9; x < 15; x++) for (let z = 9; z <= 10; z++) {
      const height = Math.floor(rng() * (levels + 1));
      for (let k = 0; k < height; k++) add('3005', x, 1 + 3 * k, z);
    }
    add('3035', 8, 1 + levels * 3, 8);
    for (let k = 0; k < 2 + seed % 5; k++) add('3024', 8 + k, 2 + levels * 3, 8 + Math.floor(rng() * 4));
  } else {
    const goal = 10 + seed % 31;
    for (let attempt = 0; attempt < 2500 && parts.length < goal; attempt++) {
      let parents = parts;
      if (policy === 'tip-walk') parents = parts.slice(-1);
      if (policy === 'low-fan') parents = parts.filter(p => p.y <= 7);
      if (policy === 'shallow-terrace') parents = parts.filter(p => p.y + dims(p).h <= 4);
      const parent = pick(parents);
      const pool = policy === 'plate-network' ? ['3024', '3023', '3623', '3710', '3022', '3021', '3020']
        : policy === 'alternating-beams' ? ['3010', '3009', '3008', '3710', '3666', '3460']
          : policy === 'shallow-terrace' ? ['3024', '3023', '3022', '3005', '3004', '3003']
            : ['3005', '3004', '3622', '3010', '3003', '3002', '3001', '3024', '3023', '3022'];
      const partId = pick(pool), turn = policy === 'alternating-beams' ? 1 - parent.turn % 2 : Math.floor(rng() * 4);
      const pd = dims(parent), cd = dims({ partId, turn });
      const x = parent.x + Math.floor(rng() * (pd.w + cd.w - 1)) - cd.w + 1;
      const z = parent.z + Math.floor(rng() * (pd.d + cd.d - 1)) - cd.d + 1;
      if (policy === 'tip-walk' && parts.filter(p => p.y + dims(p).h === parent.y + pd.h
        && contact(p, { id: 'probe', partId, color: 'red', x, y: parent.y + pd.h, z, turn }) > 0).length !== 1) continue;
      add(partId, x, parent.y + pd.h, z, turn);
    }
  }
  const minX = Math.min(...parts.map(p => p.x)), minZ = Math.min(...parts.map(p => p.z));
  return parts.map(p => ({ ...p, x: p.x - minX, z: p.z - minZ }));
}

let cached: RecordV2[] | undefined;
export function dataset(): RecordV2[] {
  if (cached) return cached;
  const seen = new Set([...oldModels(), ...researchModels()].map(m => canonicalGeometry(m.structure.parts)));
  const output: RecordV2[] = [];
  for (const [policyIndex, policy] of POLICIES.entries()) {
    let accepted = 0;
    for (let attempt = 0; accepted < PER_POLICY && attempt < PER_POLICY * 30; attempt++) {
      const seed = 410003 + policyIndex * 100003 + attempt * 97, parts = generate(policy, seed);
      if (parts.length < 8 || parts.length > 64) continue;
      const geometry = canonicalGeometry(parts);
      if (seen.has(geometry)) continue;
      const independent = independentCheck(parts);
      if (independent.issues.length) throw new Error(`${policy}/${seed}: ${independent.issues}`);
      seen.add(geometry);
      const group = digest(geometry), box = bounds(parts);
      const bucket = parseInt(group.slice(0, 8), 16) % 10;
      const split: Split = policyIndex >= 6 ? 'test_ood' : bucket < 7 ? 'train' : bucket === 7 ? 'validation' : 'test_id';
      output.push({ id: 'v' + group.slice(0, 19), group, family: policy, policy, seed, split,
        description: `A ${policy} construction with ${parts.length} pieces, extents ${box.x} x ${box.z} studs and ${box.y} plate layers.`,
        parameters: { width: box.x, depth: box.z, height: box.y, palette: seed % 6 },
        structure: { version: 1, parts }, connections: edges(parts),
        difficulty: parts.length <= 16 ? 'small' : parts.length <= 28 ? 'medium' : 'large',
        provenance: { source: 'procedural', license: 'CC0-1.0', generator: VERSION },
        certificate: { insertionOrder: parts.map(p => p.id), independent: true } });
      accepted++;
    }
    if (accepted !== PER_POLICY) throw new Error(`Insufficient unique ${policy} samples: ${accepted}`);
  }
  cached = output;
  return output;
}
