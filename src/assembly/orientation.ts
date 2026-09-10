import type { PartInstance } from '../model/types';

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
  const label = `${part.displayName} ${part.tags.join(' ')}`.toLowerCase();
  const directional = /(slope|wedge|clip|handle|stud on|bracket|hinge|wing|tail|bar|axle)/.test(label);
  if (directional) return true;
  return !(
    /\b1\s*x\s*1\b/.test(label)
    || /\b2\s*x\s*2\b/.test(label)
    || /(round|cone|dish|bush)/.test(label)
  );
}

export function partOrientationMatches(
  part: Pick<PartInstance, 'originalMatrix' | 'displayName' | 'tags'>,
  turn: QuarterTurn,
) {
  return !partRotationIsRelevant(part) || partQuarterTurn(part) === turn;
}

export function assemblyMaterialKey(
  part: Pick<PartInstance, 'partNumber' | 'colorCode' | 'originalMatrix' | 'displayName' | 'tags'>,
) {
  const turn = partRotationIsRelevant(part) ? partQuarterTurn(part) : 0;
  return `${part.partNumber}:${part.colorCode}:${turn}`;
}

export function groupAssemblyMaterials(parts: PartInstance[]): AssemblyMaterialGroup[] {
  const groups = new Map<string, AssemblyMaterialGroup>();
  for (const part of parts) {
    const rotationRelevant = partRotationIsRelevant(part);
    const requiredTurn = rotationRelevant ? partQuarterTurn(part) : 0;
    const key = `${part.partNumber}:${part.colorCode}:${requiredTurn}`;
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
