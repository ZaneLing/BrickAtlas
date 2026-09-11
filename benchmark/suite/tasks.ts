import { CATALOG, TASKS, type Color, type FrameSpec, type Kind, type Part, type PublicTask, type Structure } from './shared';
import { bom, bounds, cells, components, contact, dims, relative } from './geometry';
import { digest, type ModelRecord } from './data';

export interface Task {
  public: PublicTask;
  frames: FrameSpec[];
  target: Structure;
  oracle: unknown;
  source: Structure | null;
  changedIds: string[];
}
export function volumeSpec(parts: Part[]) {
  const box = bounds(parts), occupied = cells(parts);
  const layers: { fromY: number; toY: number; rows: string[] }[] = [];
  for (let y = 0; y < box.y; y++) {
    const rows = Array.from({ length: box.z }, (_, z) =>
      Array.from({ length: box.x }, (_, x) => occupied.has(`${x},${y},${z}`) ? '#' : '.').join(''));
    const previous = layers.at(-1);
    if (previous && JSON.stringify(previous.rows) === JSON.stringify(rows)) previous.toY = y + 1;
    else layers.push({ fromY: y, toY: y + 1, rows });
  }
  return { bounds: box, layers, maxPieces: 64 };
}
function revealFrames(parts: Part[]): FrameSpec[] {
  const frames: FrameSpec[] = [{ parts, view: 'iso', layer: null, title: 'Reference: assembled isometric' }];
  for (const y of [...new Set(parts.map(p => p.y))].sort((a, b) => a - b)) {
    frames.push({ parts: parts.filter(p => p.y === y), view: 'top', layer: y,
      title: `Reference layer inspection: only parts with bottom y=${y}. All other layers removed.` });
  }
  return frames;
}
const structureSchema = { version: 1, parts: [{ id: 'local1', partId: '3005', color: 'red', x: 0, y: 0, z: 0, turn: 0 }] };
export function taskFor(model: ModelRecord, kind: Kind, representation: 'absolute' | 'relative' = 'absolute'): Task {
  const target = structuredClone(model.structure);
  // Opaque, nonordinal IDs avoid teaching a reference sequence through handles.
  target.parts = target.parts.map((p, i) => ({ ...p, id: 'p' + digest(`${model.group}:${i}`).slice(0, 7) }));
  const parts = target.parts;
  const encode = (s: Structure) => representation === 'relative' ? relative(s) : s;
  let prompt = '', input: Record<string, unknown> = {}, oracle: unknown = target;
  let source: Structure | null = null, frames: FrameSpec[] = [], changedIds: string[] = [];
  let responseSchema: Record<string, unknown> = structureSchema;
  const n = parseInt(model.id.slice(0, 8), 16);
  if (kind === 'parts') {
    const entries = Object.keys(CATALOG).sort();
    const partId = entries[n % entries.length];
    const p: Part = { id: 'query', partId, color: parts[n % parts.length].color, x: 0, y: 0, z: 0, turn: 0 };
    frames = ['iso', 'top'].map(view => ({ parts: [p], view: view as 'iso' | 'top', layer: null, title: `Query ${view}` }));
    prompt = 'Identify this isolated part from the public catalog. Return its partId, color, and number of top studs. Do not copy the example answer.';
    oracle = { partId, color: p.color, studs: dims(p).w * dims(p).d };
    responseSchema = { partId: 'string', color: 'string', studs: 'integer' };
  } else if (kind === 'relations') {
    const a = parts[n % parts.length], b = parts[(n + 1) % parts.length];
    prompt = 'Use the supplied complete structure. Is a directly stud-connected to b? Is the entire body of a at or above the top of b? How many stud-connected components exist?';
    input = { structure: encode(target), a: a.id, b: b.id };
    oracle = { connected: contact(a, b) > 0, above: a.y >= b.y + dims(b).h, components: components(parts) };
    responseSchema = { connected: 'boolean', above: 'boolean', components: 'integer' };
  } else if (kind === 'reconstruct') {
    prompt = 'Reconstruct all reference pieces and their exact colors/poses from the assembled and layer-inspection images. Layer views explicitly reveal hidden geometry; this is NOT single-view reconstruction. IDs may be arbitrary.';
    input = { billOfMaterials: bom(parts), coordinateFrame: 'minimum x/z corner at 0,0; bottom y=0' };
    frames = revealFrames(parts);
  } else if (kind === 'generate') {
    prompt = `Generate a ${model.family}-shaped structure matching the occupied volume below. '#' means occupied, '.' empty. Rows index z, columns x; fromY inclusive, toY exclusive. Any catalog tiling with exactly that volume is valid. Use only the listed colors. This is controlled shape-conditioned generation, not unconstrained aesthetic text generation.`;
    input = { description: model.description, volume: volumeSpec(parts), allowedColors: [...new Set(parts.map(p => p.color))] };
  } else if (kind === 'complete') {
    const removeCount = Math.max(1, Math.floor(parts.length / 4));
    source = { version: 1, parts: structuredClone(parts.slice(0, -removeCount)) };
    changedIds = parts.slice(-removeCount).map(p => p.id);
    prompt = 'Complete the supplied partial structure to match the reference layer-inspection images. Return the FULL final structure. Existing pieces must remain in exactly their current poses and colors; output IDs may change.';
    input = { current: encode(source), billOfMaterials: bom(parts) };
    frames = revealFrames(parts);
  } else if (kind === 'edit') {
    source = structuredClone(target);
    if (n % 3 === 0) {
      const oldColor = parts[n % parts.length].color;
      const replacement: Color = oldColor === 'blue' ? 'green' : 'blue';
      changedIds = parts.filter(p => p.color === oldColor).map(p => p.id);
      for (const p of parts) if (p.color === oldColor) p.color = replacement;
      prompt = `Recolor every ${oldColor} piece to ${replacement}. Preserve all part types, poses, counts and other colors. Return the full final structure.`;
      input = { current: encode(source), operation: { type: 'recolor', from: oldColor, to: replacement } };
    } else {
      const top = [...parts].sort((a, b) => (b.y + dims(b).h) - (a.y + dims(a).h))[0];
      if (n % 3 === 1) {
        prompt = `Add one exact copy of ${top.id} directly on its top studs. Preserve its orientation and color, align its minimum x/z, and preserve every existing piece. Return the full final structure.`;
        parts.push({ ...top, id: 'added', y: top.y + dims(top).h });
        input = { current: encode(source), operation: { type: 'stack-copy', reference: top.id } };
      } else {
        prompt = `Remove only piece ${top.id}, leaving every other piece unchanged. Return the full remaining structure.`;
        changedIds = [top.id];
        parts.splice(parts.findIndex(p => p.id === top.id), 1);
        input = { current: encode(source), operation: { type: 'remove', id: top.id } };
      }
    }
  } else if (kind === 'plan') {
    const direction = n % 2 ? 'assemble' : 'disassemble';
    const shuffled = [...parts].sort((a, b) => digest(a.id).localeCompare(digest(b.id)));
    prompt = `Return every piece ID exactly once in a valid ${direction} order. Check support, no body overlap and unobstructed vertical insertion/removal. Any legal order is accepted, not only the source order.`;
    input = { target: representation === 'relative' ? encode(target) : { version: 1, parts: shuffled }, direction };
    oracle = { order: (direction === 'assemble' ? parts : [...parts].reverse()).map(p => p.id) };
    responseSchema = { order: ['part ID strings'] };
  } else if (kind === 'repair') {
    source = structuredClone(target);
    const damaged = source.parts[n % source.parts.length];
    const fault = n % 4;
    if (fault === 1) { damaged.color = damaged.color === 'blue' ? 'red' : 'blue'; changedIds = [damaged.id]; }
    if (fault === 2) { damaged.x += 1; changedIds = [damaged.id]; }
    if (fault === 3) { source.parts.push({ ...parts[0], id: 'extra', x: 18, y: 0 }); changedIds = ['extra']; }
    prompt = 'Compare the supplied current structure against the reference layer-inspection images. Return the full corrected structure and faultIds identifying wrong or extra CURRENT pieces. There may be no fault: then return an empty list. Do not modify correct pieces.';
    input = { current: encode(source), billOfMaterials: bom(parts) };
    frames = revealFrames(parts);
    oracle = { structure: target, faultIds: changedIds };
    responseSchema = { structure: structureSchema, faultIds: ['current piece ID strings; or empty array'] };
  }
  return { public: {
    id: digest(`${model.id}:${kind}:${representation}`).slice(0, 24), kind, split: model.split, family: model.family,
    prompt, input, responseSchema, imageTitles: frames.map(f => f.title),
  }, frames, target, oracle, source, changedIds };
}
export function taskList(model: ModelRecord) { return TASKS.map(kind => taskFor(model, kind)); }
