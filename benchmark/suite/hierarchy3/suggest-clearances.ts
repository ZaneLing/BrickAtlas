// Offline authoring aid. It never changes release models automatically.
import { writeFileSync } from 'node:fs';
import { models } from './models';
import { build } from './physics';
const suggestions: Record<string, Record<string, number[]>> = {};
for (const model of models()) {
  const b = await build(model), moved: Record<string, number[]> = {};
  try {
    b.world.propagateModifiedBodyPositionsToColliders();
    const overlap = (a: string, c: string) => {
      const ba = b.bodies.get(a)!, bc = b.bodies.get(c)!;
      for (let u = 0; u < ba.numColliders(); u++) for (let v = 0; v < bc.numColliders(); v++) {
        const hit = ba.collider(u).contactCollider(bc.collider(v), 0);
        if (hit && hit.distance < -0.005) return true;
      }
      return false;
    };
    for (const m of [...model.modules].reverse().filter(m => !m.anchored)) {
      const others = model.modules.filter(o => o.id !== m.id);
      const collides = () => others.some(o => overlap(m.id, o.id));
      if (!collides()) continue;
      const body = b.bodies.get(m.id)!, origin = body.translation();
      let solved = false;
      search: for (let n = 1; n <= 60; n++) for (const axis of [1, 2, 0]) for (const sign of [1, -1]) {
        const delta = [0, 0, 0]; delta[axis] = n * 0.1 * sign;
        body.setTranslation({ x: origin.x + delta[0], y: origin.y + delta[1], z: origin.z + delta[2] }, false);
        b.world.propagateModifiedBodyPositionsToColliders();
        if (!collides()) { moved[m.id] = delta; solved = true; break search; }
      }
      if (!solved) throw new Error(`No local clearance: ${model.id}/${m.id}`);
      const delta = moved[m.id];
      body.setTranslation({ x: origin.x + delta[0], y: origin.y + delta[1], z: origin.z + delta[2] }, false);
      b.world.propagateModifiedBodyPositionsToColliders();
    }
    if (Object.keys(moved).length) { suggestions[model.id] = moved; console.log(model.id, JSON.stringify(moved)); }
  } finally { b.world.free(); }
}
writeFileSync('/tmp/brickatlas-clearance-suggestions.json', JSON.stringify(suggestions, null, 2) + '\n');
