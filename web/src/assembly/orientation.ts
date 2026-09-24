import type { AssemblyStep, PartInstance } from '../model/types';

export type QuarterTurn = 0 | 1 | 2 | 3;

export interface AssemblyMaterialGroup {
  key: string;
  partNumber: string;
  name: string;
  colorName: string;
  colorHex: string;
  quantity: number;
  instanceIds: string[];
  requiredTurn: QuarterTurn;
  rotationRelevant: boolean;
}

function normalizedQuarterTurn(angle: number): QuarterTurn {
  return ((Math.round(angle / (Math.PI / 2)) % 4 + 4) % 4) as QuarterTurn;
}

export function partQuarterTurn(part: Pick<PartInstance, 'originalMatrix'>): QuarterTurn {
  const matrix = part.originalMatrix;
  if (!Array.isArray(matrix) || matrix.length < 11) return 0;
  const localXLength = Math.hypot(matrix[0], matrix[2]);
  const localZLength = Math.hypot(matrix[8], matrix[10]);
  return localXLength >= localZLength
    ? normalizedQuarterTurn(Math.atan2(matrix[2], matrix[0]))
    : normalizedQuarterTurn(Math.atan2(matrix[8], matrix[10]));
}

export function partRotationIsRelevant(
  part: Pick<PartInstance, 'displayName' | 'tags'>,
) {
  return partTurnPeriod(part) > 1;
}

export function partTurnPeriod(
  part: Pick<PartInstance, 'displayName' | 'tags'>,
): 1 | 2 | 4 {
  const label = `${part.displayName} ${part.tags.join(' ')}`.toLowerCase();
  const directional = /(slope|wedge|clip|handle|stud on|bracket|hinge|wing|tail|bar|axle)/.test(label);
  if (directional) return 4;
  if (/(round|cone|dish|bush)/.test(label)) return 1;
  const dimensions = /\b(\d+)\s*x\s*(\d+)\b/.exec(label);
  if (dimensions?.[1] === dimensions?.[2]) return 1;
  return 2;
}

export function partOrientationMatches(
  part: Pick<PartInstance, 'originalMatrix' | 'displayName' | 'tags'>,
  turn: QuarterTurn,
) {
  const period = partTurnPeriod(part);
  return period === 1 || partQuarterTurn(part) % period === turn % period;
}

export function assemblyMaterialKey(
  part: Pick<PartInstance, 'partNumber' | 'colorCode'>,
) {
  return `${part.partNumber}:${part.colorCode}`;
}

export function equivalentAssemblyTargets(
  parts: PartInstance[],
  placedIds: ReadonlySet<string>,
  materialKey: string,
  sourceInstanceId: string | undefined,
  turn: QuarterTurn,
) {
  const candidates = parts.filter(part =>
    assemblyMaterialKey(part) === materialKey && !placedIds.has(part.instanceId));
  const source = parts.find(part => part.instanceId === sourceInstanceId) ?? candidates[0];
  if (!source) return [];
  const period = partTurnPeriod(source);
  const sourceTurn = partQuarterTurn(source);
  return candidates.filter(target => {
    if (period === 1) return true;
    const required = ((partQuarterTurn(target) - sourceTurn + 4) % 4) as QuarterTurn;
    return required % period === turn % period;
  });
}

export function nearestAssemblyTarget(
  parts: PartInstance[],
  position: [number, number, number],
) {
  let closest: PartInstance | null = null;
  let closestDistance = Infinity;
  for (const part of parts) {
    const distance = Math.hypot(
      (part.bounds.min[0] + part.bounds.max[0]) / 2 - position[0],
      (part.bounds.min[1] + part.bounds.max[1]) / 2 - position[1],
      (part.bounds.min[2] + part.bounds.max[2]) / 2 - position[2],
    );
    if (
      distance < closestDistance
      || distance === closestDistance && part.index < (closest?.index ?? Infinity)
    ) {
      closest = part;
      closestDistance = distance;
    }
  }
  return closest;
}

export function groupAssemblyMaterials(parts: PartInstance[]): AssemblyMaterialGroup[] {
  const groups = new Map<string, AssemblyMaterialGroup>();
  for (const part of parts) {
    const rotationRelevant = partRotationIsRelevant(part);
    const requiredTurn = rotationRelevant ? partQuarterTurn(part) : 0;
    const key = assemblyMaterialKey(part);
    const item = groups.get(key) ?? {
      key,
      partNumber: part.partNumber,
      name: part.displayName,
      colorName: part.colorName,
      colorHex: part.colorHex,
      quantity: 0,
      instanceIds: [],
      requiredTurn,
      rotationRelevant,
    };
    item.quantity++;
    item.instanceIds.push(part.instanceId);
    groups.set(key, item);
  }
  return [...groups.values()].sort((a, b) =>
    b.quantity - a.quantity
    || a.partNumber.localeCompare(b.partNumber)
    || a.requiredTurn - b.requiredTurn,
  );
}

export interface AssemblyStepAudit {
  ok: boolean;
  missingIds: string[];
  unexpectedIds: string[];
  wrongOrientationIds: string[];
  wrongPositionIds: string[];
}

export function auditAssemblyStep(
  step: AssemblyStep,
  parts: PartInstance[],
  placedIds: string[],
  placedTurns: Record<string, QuarterTurn>,
  placedPositions: Record<string, [number, number, number]> = {},
  assemblyPlaced = false,
): AssemblyStepAudit {
  if (step.kind === 'placement') {
    return {
      ok: assemblyPlaced,
      missingIds: assemblyPlaced ? [] : [step.id],
      unexpectedIds: [],
      wrongOrientationIds: [],
      wrongPositionIds: [],
    };
  }
  const expected = new Set(step.instanceIds);
  const placed = new Set(placedIds);
  const missingIds = step.instanceIds.filter(id => !placed.has(id));
  const unexpectedIds = [...placed].filter(id => !expected.has(id));
  const byId = new Map(parts.map(part => [part.instanceId, part]));
  const wrongOrientationIds = step.instanceIds.filter(id => {
    const part = byId.get(id);
    return !part || partRotationIsRelevant(part) && placedTurns[id] !== 0;
  });
  const wrongPositionIds = step.instanceIds.filter(id => {
    const part = byId.get(id);
    const position = placedPositions[id];
    if (!part || !position) return true;
    const target = [0, 1, 2].map(axis =>
      (part.bounds.min[axis] + part.bounds.max[axis]) / 2);
    return Math.hypot(
      position[0] - target[0],
      position[1] - target[1],
      position[2] - target[2],
    ) > 5;
  });
  return {
    ok: placed.size === placedIds.length
      && !missingIds.length
      && !unexpectedIds.length
      && !wrongOrientationIds.length
      && !wrongPositionIds.length,
    missingIds,
    unexpectedIds,
    wrongOrientationIds,
    wrongPositionIds,
  };
}
