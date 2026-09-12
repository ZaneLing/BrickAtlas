import { CATALOG } from '../shared';
import { bom, bounds, dims, edges } from '../geometry';
import { digest } from '../data';
import { independentCheck } from '../research/independent-check';
import { metricNames, evaluate } from './evaluate';
import { type CaseTask } from './cases';
import { VERSION } from './dataset';

export function groundTruth(task: CaseTask) {
  const ordered = [...task.target.parts].sort((a, b) => a.y - b.y || a.id.localeCompare(b.id));
  const check = independentCheck(ordered);
  if (check.issues.length) throw new Error(`Invalid target ${task.spec.id}: ${check.issues}`);
  const connections = edges(ordered);
  const studs = connections.reduce((n, e) => n + e.studs, 0);
  if (studs !== check.contacts.reduce((n, e) => n + e.studs, 0)) throw new Error('Independent connection count differs');
  const vertexMap = new Map(ordered.map(p => [p.id, p]));
  const ports = connections.flatMap(e => {
    const a = vertexMap.get(e.a)!, b = vertexMap.get(e.b)!;
    const lower = a.y < b.y ? a : b, upper = lower === a ? b : a;
    const ld = dims(lower), ud = dims(upper), points = [];
    for (let x = Math.max(lower.x, upper.x); x < Math.min(lower.x + ld.w, upper.x + ud.w); x++) {
      for (let z = Math.max(lower.z, upper.z); z < Math.min(lower.z + ld.d, upper.z + ud.d); z++) {
        points.push({ lower: lower.id, upper: upper.id, position: [x + 0.5, upper.y, z + 0.5] });
      }
    }
    return points;
  });
  return {
    version: VERSION, caseId: task.spec.id, inputHash: digest(task.public), spec: task.spec,
    answerSemantics: task.spec.kind === 'generate' ? 'nonunique-constraint-witness'
      : task.spec.kind === 'plan' ? 'nonunique-executable-order'
        : task.spec.condition === 'ordinary' && ['reconstruct', 'complete', 'repair'].includes(task.spec.kind)
          ? 'nonunique-visible-surface-with-bom' : 'exact-fields-or-symmetric-parts',
    oracle: task.oracle, target: task.target, source: task.source,
    billOfMaterials: bom(ordered), extents: bounds(ordered), connections,
    nominalStudMates: ports, changedIds: task.changedIds,
    preservedIds: task.source?.parts.filter(p => !task.changedIds.includes(p.id)).map(p => p.id) ?? [],
    symmetry: Object.fromEntries([...new Set(ordered.map(p => p.partId))].map(id =>
      [id, CATALOG[id].w === CATALOG[id].d ? [0, 1, 2, 3] : [0, 2]])),
    assemblyWitness: ordered.map(p => p.id), disassemblyWitness: ordered.map(p => p.id).reverse(),
    independentCheck: check, metrics: metricNames(task.spec.kind), oracleEvaluation: evaluate(task, task.oracle),
    annotationProvenance: 'Procedural construction plus independent integer-cell checker. Not human annotation or force simulation.',
    humanReviewed: false,
  };
}
