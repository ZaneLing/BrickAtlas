import { describe, expect, it } from 'vitest';
import { instructionPlan } from '../../scripts/instructions';
import { groupStepParts } from '../../src/instructions/exportGuide';
import { buildManifest, splitMpd } from '../../scripts/ldraw';
import type { AtlasManifest } from '../../src/model/types';

const licensed = '0 Author: Test\n0 !LICENSE Licensed under CC BY 4.0';
const part = `0 FILE parts/brick.dat\n0 Brick\n${licensed}\n0 !LDRAW_ORG Part\n3 16 0 0 0 1 0 0 0 1 0`;
const colors = '0 !COLOUR Red CODE 4 VALUE #C91A09 EDGE #333333';
const groups: AtlasManifest['groups'] = [{ id: 'body', name: 'Body', color: '#f00', direction: [0, 1, 0], instanceIds: [] }];

describe('instruction plans', () => {
  it('preserves source STEP batches with complete brick coverage', () => {
    const files = splitMpd(`0 FILE main.ldr\n${licensed}\n1 4 0 0 0 1 0 0 0 1 0 0 0 1 brick.dat\n0 STEP\n1 4 0 -20 0 1 0 0 0 1 0 0 0 1 brick.dat\n${part}`);
    const semantic = buildManifest(files, 'main.ldr', colors, () => 'body');
    const plan = instructionPlan(files, 'main.ldr', { instances: semantic.instances, groups });
    expect(plan.provenance).toBe('source');
    expect(plan.steps.map(step => step.instanceIds)).toEqual([['brick_000001'], ['brick_000002']]);
  });

  it('labels generated spatial batches as editorial', () => {
    const files = splitMpd(`0 FILE main.ldr\n${licensed}\n1 4 0 0 0 1 0 0 0 1 0 0 0 1 brick.dat\n${part}`);
    const semantic = buildManifest(files, 'main.ldr', colors, () => 'body');
    semantic.instances[0].bounds = { min: [0, 0, 0], max: [8, 8, 8] };
    const plan = instructionPlan(files, 'main.ldr', { instances: semantic.instances, groups });
    expect(plan.provenance).toBe('editorial');
    expect(plan.disclaimer).toContain('未验证实物可拼搭性');
    expect(plan.steps.flatMap(step => step.instanceIds)).toEqual(['brick_000001']);
  });

  it('groups instruction callouts by part and color', () => {
    const files = splitMpd(`0 FILE main.ldr\n${licensed}\n1 4 0 0 0 1 0 0 0 1 0 0 0 1 brick.dat\n1 4 20 0 0 1 0 0 0 1 0 0 0 1 brick.dat\n${part}`);
    const semantic = buildManifest(files, 'main.ldr', colors, () => 'body');
    const groups = groupStepParts(semantic.instances);
    expect(groups).toHaveLength(1);
    expect(groups[0]).toMatchObject({ partNumber: 'brick', colorHex: '#C91A09', quantity: 2 });
    expect(groups[0].instanceIds).toEqual(['brick_000001', 'brick_000002']);
  });
});
