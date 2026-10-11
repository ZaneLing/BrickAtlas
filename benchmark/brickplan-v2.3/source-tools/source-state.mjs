import { existsSync } from 'node:fs';
import { resolve } from 'node:path';

export const legacyStatePath = 'tem/research/20261010-brickplan-v23-diversity/source-intake';
export const archivedStatePath = 'benchmark/brickplan-v2.3/data/source-intake';

export function sourceState(root) {
  const legacy = resolve(root, legacyStatePath);
  return existsSync(legacy) ? legacy : resolve(root, archivedStatePath);
}
