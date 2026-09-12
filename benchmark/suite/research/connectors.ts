import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { CATALOG, type Part } from '../shared';
import { BENCHMARK, ARTIFACTS } from '../storage';
import { edges } from '../geometry';
import { researchModels } from './dataset';

export interface Connector {
  id: number; kind: string; subtype: string; polarity: string;
  positionLdu: [number, number, number]; pitchDeg: number | null; rollDeg: number | null;
}
let cached: Record<string, Connector[]> | undefined;
let aliases: { src: string; dst: string; final_matrix_3x4: number[] }[] | undefined;
export function connectorCatalog() {
  if (cached) return cached;
  const path = resolve(BENCHMARK, '.runtime/vendor/bricknet/normalized-connectors.json');
  if (!existsSync(path)) throw new Error('Run vendor_catalog.py first');
  cached = JSON.parse(readFileSync(path, 'utf8')) as Record<string, Connector[]>;
  return cached;
}
export function gridPorts(p: Part) {
  const d = CATALOG[p.partId];
  if (!d) throw new Error('Grid geometry unsupported');
  let annotations = connectorCatalog()[`${p.partId}.dat`];
  if (!annotations) {
    aliases ??= JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/vendor/bricknet/normalized-aliases.json'), 'utf8')).rows;
    const alias = aliases?.find(a => a.src === p.partId);
    const identity = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1];
    if (alias && alias.final_matrix_3x4.every((x, i) => x === identity[i])) annotations = connectorCatalog()[`${alias.dst}.dat`];
    else throw new Error('No supported identity alias');
  }
  if (!annotations) throw new Error('No upstream annotation');
  return annotations.filter(c => c.pitchDeg === 0 && c.rollDeg === 0
    && (c.kind === 'stud' && ['stud', 'open'].includes(c.subtype)
      || c.kind === 'hole' && c.subtype === 'hole')).map(c => {
    const [x, y, z] = c.positionLdu;
    const u = x / 20 + d.w / 2, v = z / 20 + d.d / 2;
    const rotated = [[u, v], [d.d - v, u], [d.w - u, d.d - v], [v, d.w - u]][p.turn];
    return { id: c.id, kind: c.kind as 'stud' | 'hole',
      position: [p.x + rotated[0], p.y + d.h - y / 8, p.z + rotated[1]] as [number, number, number] };
  });
}
export function portConnections(parts: Part[]) {
  const holes = new Map<string, { part: string; port: number }[]>();
  const key = (p: number[]) => p.map(x => x.toFixed(5)).join(':');
  const ports = parts.map(p => ({ p, ports: gridPorts(p) }));
  for (const { p, ports: entries } of ports) for (const port of entries) if (port.kind === 'hole') {
    const k = key(port.position);
    holes.set(k, [...(holes.get(k) ?? []), { part: p.id, port: port.id }]);
  }
  const result = [];
  for (const { p, ports: entries } of ports) for (const port of entries) if (port.kind === 'stud') {
    for (const other of holes.get(key(port.position)) ?? []) if (other.part !== p.id) {
      result.push({ a: p.id, aPort: port.id, b: other.part, bPort: other.port, position: port.position });
    }
  }
  return result;
}
export function auditConnectors() {
  const partChecks = [];
  for (const [partId, d] of Object.entries(CATALOG)) {
    const ports = gridPorts({ id: 'test', partId, color: 'gray', x: 0, y: 0, z: 0, turn: 0 });
    const expected = [];
    for (let x = 0; x < d.w; x++) for (let z = 0; z < d.d; z++) expected.push(`${x + 0.5}:${z + 0.5}`);
    const studs = ports.filter(c => c.kind === 'stud' && c.position[1] === d.h);
    const holes = ports.filter(c => c.kind === 'hole' && c.position[1] === 0);
    const footprints = (items: typeof ports) => items.map(p => `${p.position[0]}:${p.position[2]}`).sort();
    partChecks.push({ partId, studs: studs.length, holes: holes.length,
      agrees: JSON.stringify(footprints(studs)) === JSON.stringify(expected.sort())
        && JSON.stringify(footprints(holes)) === JSON.stringify(expected.sort()) });
  }
  const mismatches = [];
  for (const m of researchModels()) {
    const expected = edges(m.structure.parts).reduce((n, e) => n + e.studs, 0);
    const actual = portConnections(m.structure.parts).length;
    if (expected !== actual) mismatches.push({ model: m.id, expected, actual });
  }
  const result = { source: 'BrickNet MIT bundled annotations; attribution retained',
    testedGeometryDomain: '25 orthogonal rectangular brick/plate types; nominal stud-hole coordinates',
    partChecks, assembliesChecked: researchModels().length, mismatches,
    allAgree: partChecks.every(p => p.agrees) && mismatches.length === 0,
    notValidated: ['general hinge/axle/ball compatibility', 'force/clutch mechanics', 'arbitrary CAD collision meshes', 'independent human audit'] };
  atomicJson(resolve(ARTIFACTS, 'research/connector-audit.json'), result);
  return result;
}
