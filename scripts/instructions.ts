import type { AtlasManifest, AssemblyStep, InstructionPlan, PartInstance, Vec3 } from '../src/model/types';
import { header, reference, resolveFile, type LDrawFile } from './ldraw';

const CONTACT_TOLERANCE = 2.05;
const CONTACT_OVERLAP = 1;
const accessory = /\b(tyre|tire|wheel|rim|propeller|rotor|minifig|figure|head|helmet)\b/i;
const connector = /\b(axle|bar|bracket|clip|hinge|pin|socket|towball|turntable|wheel|rim|tyre|tire)\b/i;
const groupRank = new Map([
  ['chassis', 0],
  ['body', 1],
  ['cockpit', 2],
  ['front', 3],
  ['rear', 4],
  ['wheels', 5],
]);

function axisOverlap(aMin: number, aMax: number, bMin: number, bMax: number) {
  return Math.max(0, Math.min(aMax, bMax) - Math.max(aMin, bMin));
}

function axisGap(aMin: number, aMax: number, bMin: number, bMax: number) {
  return Math.max(0, aMin - bMax, bMin - aMax);
}

function surfaceGap(aMin: number, aMax: number, bMin: number, bMax: number) {
  return Math.min(Math.abs(aMax - bMin), Math.abs(bMax - aMin));
}

function partLabel(part: PartInstance) {
  return `${part.displayName} ${part.category} ${part.tags.join(' ')}`;
}

export function partsConnect(a: PartInstance, b: PartInstance) {
  const overlap = [0, 1, 2].map(axis =>
    axisOverlap(a.bounds.min[axis], a.bounds.max[axis], b.bounds.min[axis], b.bounds.max[axis]));
  const gap = [0, 1, 2].map(axis =>
    axisGap(a.bounds.min[axis], a.bounds.max[axis], b.bounds.min[axis], b.bounds.max[axis]));
  const surfaceContact = [0, 1, 2].some(axis =>
    surfaceGap(
      a.bounds.min[axis],
      a.bounds.max[axis],
      b.bounds.min[axis],
      b.bounds.max[axis],
    ) <= CONTACT_TOLERANCE
    && [0, 1, 2].filter(other => other !== axis)
      .every(other => overlap[other] >= CONTACT_OVERLAP));
  if (surfaceContact || overlap.every(value => value >= CONTACT_OVERLAP)) return true;

  const mechanical = connector.test(partLabel(a)) || connector.test(partLabel(b));
  if (!mechanical || gap.some(value => value > CONTACT_TOLERANCE)) return false;
  return overlap.filter(value => value >= CONTACT_OVERLAP).length >= 2;
}

function rootOrder(a: PartInstance, b: PartInstance, minimum: number) {
  const score = (part: PartInstance) => {
    const isAccessory = accessory.test(partLabel(part));
    const heightBand = Math.max(0, Math.floor((part.bounds.min[1] - minimum + 0.01) / 8));
    const footprint = (part.bounds.max[0] - part.bounds.min[0])
      * (part.bounds.max[2] - part.bounds.min[2]);
    return { isAccessory, heightBand, footprint };
  };
  const left = score(a);
  const right = score(b);
  return Number(left.isAccessory) - Number(right.isAccessory)
    || left.heightBand - right.heightBand
    || right.footprint - left.footprint
    || a.bounds.min[1] - b.bounds.min[1]
    || (groupRank.get(a.groupId) ?? 99) - (groupRank.get(b.groupId) ?? 99)
    || a.index - b.index;
}

function supportedOrder(
  a: PartInstance,
  b: PartInstance,
  supportCounts: ReadonlyMap<string, number>,
) {
  return (groupRank.get(a.groupId) ?? 99) - (groupRank.get(b.groupId) ?? 99)
    || a.bounds.min[1] - b.bounds.min[1]
    || (supportCounts.get(b.instanceId) ?? 0) - (supportCounts.get(a.instanceId) ?? 0)
    || a.index - b.index;
}

export function supportAwareBatches(
  parts: PartInstance[],
  alreadyPlaced: PartInstance[] = [],
  maxBatchSize = 6,
) {
  if (!Number.isInteger(maxBatchSize) || maxBatchSize < 1) {
    throw new Error('Instruction batch size must be a positive integer');
  }
  const remaining = new Map(parts.map(part => [part.instanceId, part]));
  const committedIds = new Set(alreadyPlaced.map(part => part.instanceId));
  const neighbors = new Map(parts.map(part => [part.instanceId, [] as PartInstance[]]));
  for (const part of parts) {
    for (const previous of alreadyPlaced) {
      if (partsConnect(part, previous)) neighbors.get(part.instanceId)!.push(previous);
    }
  }
  for (let left = 0; left < parts.length; left++) {
    for (let right = left + 1; right < parts.length; right++) {
      if (!partsConnect(parts[left], parts[right])) continue;
      neighbors.get(parts[left].instanceId)!.push(parts[right]);
      neighbors.get(parts[right].instanceId)!.push(parts[left]);
    }
  }
  const supportCounts = new Map(parts.map(part => [
    part.instanceId,
    neighbors.get(part.instanceId)!.reduce(
      (count, neighbor) => count + Number(committedIds.has(neighbor.instanceId)),
      0,
    ),
  ]));
  const batches: PartInstance[][] = [];
  while (remaining.size) {
    const pool = [...remaining.values()];
    const supported = pool.filter(part => (supportCounts.get(part.instanceId) ?? 0) > 0);
    const structural = pool.filter(part => !accessory.test(partLabel(part)));
    const minimum = Math.min(...(structural.length ? structural : pool)
      .map(part => part.bounds.min[1]));
    const batch = supported.length
      ? supported.sort((a, b) => supportedOrder(a, b, supportCounts)).slice(0, maxBatchSize)
      : [pool.sort((a, b) => rootOrder(a, b, minimum))[0]];
    batches.push(batch);
    for (const part of batch) {
      remaining.delete(part.instanceId);
      committedIds.add(part.instanceId);
      for (const neighbor of neighbors.get(part.instanceId) ?? []) {
        if (!remaining.has(neighbor.instanceId)) continue;
        supportCounts.set(
          neighbor.instanceId,
          (supportCounts.get(neighbor.instanceId) ?? 0) + 1,
        );
      }
    }
  }
  return batches;
}

export function instructionPlan(files: Map<string, LDrawFile>, root: string, manifest: Pick<AtlasManifest, 'instances' | 'groups'>): InstructionPlan {
  const hasSteps = [...files.values()].some(f => !f.name.endsWith('.dat') && f.lines.some(l => /^0 (STEP|ROTSTEP)( |$)/.test(l.text)));
  const steps: AssemblyStep[] = [];
  const add = (ids: string[], file: string, sourceStep: number | null, title: string, extra: Partial<AssemblyStep> = {}) => {
    if (ids.length || extra.kind === 'placement') {
      steps.push({ id: `step-${steps.length + 1}`, title, sourceFile: file, sourceStep, instanceIds: ids, ...extra });
    }
  };
  if (hasSteps) {
    let index = 0;
    const visit = (file: LDrawFile) => {
      let ids: string[] = [], local = 1;
      const stepped = file.lines.some(l => /^0 (STEP|ROTSTEP)( |$)/.test(l.text));
      const flush = () => { add(ids, file.name, stepped ? local : null, header(file, '') || file.name); ids = []; };
      for (const line of file.lines) {
        if (/^0 (STEP|ROTSTEP)( |$)/.test(line.text)) { flush(); local++; continue; }
        if (!line.text.startsWith('1 ')) continue;
        const child = resolveFile(files, reference(line.text, line.line).file);
        if (child.name.endsWith('.ldr') || /(?:^|_)Model\b/.test(header(child, '!LDRAW_ORG'))) {
          flush();
          visit(child);
        } else {
          const part = manifest.instances[index++];
          if (!part || part.sourceFile !== file.name || part.sourceLine !== line.line) throw new Error('Instruction/source traversal mismatch');
          ids.push(part.instanceId);
        }
      }
      flush();
    };
    visit(resolveFile(files, root));
  } else {
    const assemblies = new Map<string, PartInstance[]>();
    for (const part of manifest.instances) {
      const key = part.path[1] ?? root;
      if (!assemblies.has(key)) assemblies.set(key, []);
      assemblies.get(key)!.push(part);
    }
    const cleanName = (name: string) => (header(resolveFile(files, name), '') || name)
      .replace(/\.(ldr|mpd)$/i, '')
      .replace(/^\d+\s*-\s*/, '');
    const foundation = /runway|airport|base|ground|platform|station|building|road|track/i;
    const mobile = /airplane|plane|helicopter|train|car|truck|trailer|vehicle|boat|ship|minifig|figure/i;
    const isScene = [...assemblies.keys()].some(name => foundation.test(cleanName(name)));
    const rank = (name: string) => {
      const label = cleanName(name);
      if (!isScene) return name === root ? 0 : 1;
      if (/airplane|plane/i.test(label)) return 0;
      if (/helicopter/i.test(label)) return 1;
      if (/train|car|truck|trailer|vehicle|boat|ship/i.test(label)) return 2;
      if (/minifig|figure/i.test(label)) return 3;
      if (/runway|base|ground|platform|road|track/i.test(label)) return 5;
      if (/airport|station|building/i.test(label)) return 6;
      return 4;
    };
    const orderedAssemblies = [...assemblies.entries()].sort(([a, aParts], [b, bParts]) =>
      isScene
        ? rank(a) - rank(b) || a.localeCompare(b)
        : bParts.length - aParts.length || a.localeCompare(b),
    );
    const movableAssemblies = orderedAssemblies.filter(([name]) => isScene && mobile.test(cleanName(name)));
    const extentX = Math.max(...manifest.instances.map(part => part.bounds.max[0]))
      - Math.min(...manifest.instances.map(part => part.bounds.min[0]));
    const extentZ = Math.max(...manifest.instances.map(part => part.bounds.max[2]))
      - Math.min(...manifest.instances.map(part => part.bounds.min[2]));
    const distance = Math.min(180, Math.max(70, Math.max(extentX, extentZ) * 0.2));
    const offsets = new Map<string, Vec3>(movableAssemblies.map(([name], index) => {
      const angle = -Math.PI * 0.7 + index / Math.max(1, movableAssemblies.length - 1) * Math.PI * 1.4;
      return [name, [Math.cos(angle) * distance, 28 + index % 2 * 18, Math.sin(angle) * distance] as Vec3];
    }));
    for (const [name, parts] of orderedAssemblies) {
      for (const batch of supportAwareBatches(parts)) {
        const ids = new Set(batch.map(part => part.groupId));
        const group = ids.size === 1
          ? manifest.groups.find(candidate => candidate.id === batch[0].groupId)
          : null;
        const title = name === root && group ? group.name : cleanName(name);
        add(batch.map(part => part.instanceId), batch[0].sourceFile, null, `${title} · 子装配`, {
          kind: 'parts',
          assemblyId: name,
          stagingOffset: offsets.get(name),
        });
      }
    }
    for (const [name, parts] of movableAssemblies) {
      add([], parts[0].sourceFile, null, `${cleanName(name)} · 放置总成`, {
        kind: 'placement',
        assemblyId: name,
        motionInstanceIds: parts.map(part => part.instanceId),
        stagingOffset: offsets.get(name),
      });
    }
  }
  const ids = steps.flatMap(s => s.instanceIds);
  if (ids.length !== manifest.instances.length || new Set(ids).size !== manifest.instances.length) throw new Error('Incomplete instruction coverage');
  return {
    provenance: hasSteps ? 'source' : 'editorial',
    disclaimer: hasSteps
      ? 'OMR 作者步骤，按源层级展开子装配；非官方说明书页码，入位动画不模拟碰撞。'
      : '源模型无 STEP：以下按前序结构接触关系构建独立子装配，再构建场景基础并完成总装；这是编辑演示，不等同于实物承重认证。',
    steps,
  };
}
