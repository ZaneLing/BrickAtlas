import { createHash } from 'node:crypto';
import type { PartInstance } from '../../../src/model/types';

const hash = (value: unknown) => createHash('sha256').update(JSON.stringify(value)).digest('hex');
const q = (n: number) => +n.toFixed(5);
export function sourceFingerprint(parts: PartInstance[]) {
  const origin = [0,1,2].map(k => Math.min(...parts.map(p => p.originalMatrix[12+k])));
  // Remove labels, colors, ordering and global translation, retain part types
  // and exact local rotations. This is a duplicate screen, not independence.
  return hash(parts.map(p => [p.partNumber,
    ...p.originalMatrix.map((n,k) => q(k>=12 && k<=14 ? n-origin[k-12] : n))])
    .sort((a,b) => JSON.stringify(a).localeCompare(JSON.stringify(b))));
}
export function inventorySimilarity(a: PartInstance[], b: PartInstance[]) {
  const count = (parts: PartInstance[]) => {
    const map = new Map<string, number>();
    for (const part of parts) map.set(part.partNumber, (map.get(part.partNumber) ?? 0)+1);
    return map;
  };
  const x = count(a), y = count(b), keys = new Set([...x.keys(),...y.keys()]);
  let intersection = 0, union = 0;
  for (const key of keys) {
    intersection += Math.min(x.get(key)??0,y.get(key)??0);
    union += Math.max(x.get(key)??0,y.get(key)??0);
  }
  return intersection/union;
}
export function shapeSimilarity(a: PartInstance[], b: PartInstance[]) {
  const normalize = (ps: PartInstance[]) => {
    const lo = [0,1,2].map(k => Math.min(...ps.map(p => p.bounds.min[k])));
    const hi = [0,1,2].map(k => Math.max(...ps.map(p => p.bounds.max[k])));
    const size = Math.max(...hi.map((v,k) => v-lo[k]));
    return ps.map(p => p.bounds.min.map((v,k) => ((v+p.bounds.max[k])/2-(lo[k]+hi[k])/2)/size));
  };
  const x=normalize(a),y=normalize(b);
  const distance = (p:number[],q:number[]) => Math.hypot(...p.map((v,k)=>v-q[k]));
  const nearest = (x:number[][],y:number[][]) => x.reduce((s,p)=>s+Math.min(...y.map(q=>distance(p,q))),0)/x.length;
  // Conservative candidate screen: compare original axes after centering
  // and scale normalization. Shapes sharing an outline still need review.
  return Math.max(0,1-(nearest(x,y)+nearest(y,x))/2);
}
