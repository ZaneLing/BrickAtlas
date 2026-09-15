import assert from 'node:assert/strict';
import { dims, key } from '../geometry';
import { maintenanceCases, publicMaintenance } from './maintenance';
import { parseStructure, exact } from '../frontier/geometry';
import { sameSet } from '../frontier/tasks';

export function poseCases() {
  return maintenanceCases().filter(c => c.context === 'full' && c.tier === 0).map(c => {
    const target = c.target;
    const candidates = [...target.parts].filter(p => dims(p).w !== dims(p).d).sort((a, b) => b.y - a.y);
    const chosen = [candidates[0], candidates.find(p => p.id !== candidates[0].id)!,
      target.parts.find(p => ![candidates[0].id, candidates[1].id].includes(p.id))!];
    const current = { version: 1 as const, parts: target.parts.map(p =>
      p.id === chosen[0].id ? { ...p, x: p.x + 1 } :
      p.id === chosen[1].id ? { ...p, turn: (p.turn + 1) % 4 } :
      p.id === chosen[2].id ? { ...p, color: p.color === 'red' ? 'blue' as const : 'red' as const } : p) };
    assert.equal(new Set(current.parts.map(p => key(p))).size, current.parts.length, 'ambiguous_duplicate_current_pose');
    const oracle = { faultIds: chosen.map(p => p.id), replacements: chosen };
    return { ...c, id: c.id.replace('-maintenance-0-full', '-pose-patch'), current, target, faultIds: oracle.faultIds, oracle };
  });
}

export function publicPose(c: ReturnType<typeof poseCases>[number], condition: 'symbolic' | 'layers') {
  const source = maintenanceCases().find(m => m.sourceGroup === c.sourceGroup && m.context === 'full' && m.tier === 0)!;
  const pub = publicMaintenance(source, condition);
  return { ...pub, id: c.id + '-' + condition, kind: 'pose-patch', input: { ...pub.input, current: c.current },
    prompt: `Return {faultIds,replacements:[Part]} to correct ALL translation, quarter-turn or color faults.
Reference is the supplied full JSON or calibrated bottom-Y layer images. Preserve every other current part.
Current geometry may be invalid; the corrected structure must be nominally valid and exact.
Replacement IDs must address current instances. This is a structural patch, NOT a physical repair trace.
Position is minimum X/Z corner and bottom Y; X right and Z down in layer images. Unknown yaw symmetries
are resolved by rectangular footprints; equivalent 180-degree rotations are accepted.` };
}
export function scorePose(c: ReturnType<typeof poseCases>[number], raw: any) {
  const patches = parseStructure({ version: 1, parts: raw?.replacements });
  const faultCorrect = sameSet(raw?.faultIds, c.oracle.faultIds);
  if (!patches || !faultCorrect || !sameSet(patches.parts.map(p => p.id), c.oracle.faultIds))
    return { success: 0, faultCorrect: Number(faultCorrect), correctedExact: 0 };
  const final = c.current.parts.map(p => patches.parts.find(q => q.id === p.id) ?? p);
  const correctedExact = exact(c.target.parts, final)
    && c.target.parts.every(p => final.some(q => q.id === p.id && key(q) === key(p)));
  return { success: Number(correctedExact), faultCorrect: 1, correctedExact: Number(correctedExact) };
}
