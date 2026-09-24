import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { modelCatalog } from '../../atlas.config';
import { instructionPlan, partsConnect, supportAwareBatches } from '../../scripts/instructions';
import { groupStepParts } from '../../src/instructions/exportGuide';
import { buildManifest, splitMpd } from '../../scripts/ldraw';
import type { AtlasManifest, PartInstance } from '../../src/model/types';

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
    expect(plan.disclaimer).toContain('前序结构接触关系');
    expect(plan.disclaimer).toContain('不等同于实物承重认证');
    expect(plan.steps.flatMap(step => step.instanceIds)).toEqual(['brick_000001']);
  });

  it('delays upper parts until every part in a batch touches prior structure', () => {
    const files = splitMpd(`0 FILE main.ldr
${licensed}
1 4 0 -40 0 1 0 0 0 1 0 0 0 1 brick.dat
1 4 0 0 0 1 0 0 0 1 0 0 0 1 brick.dat
1 4 0 -20 0 1 0 0 0 1 0 0 0 1 brick.dat
1 4 20 -20 0 1 0 0 0 1 0 0 0 1 brick.dat
${part}`);
    const semantic = buildManifest(files, 'main.ldr', colors, () => 'body');
    const [top, base, left, right] = semantic.instances;
    top.bounds = { min: [0, 16, 0], max: [16, 25.6, 8] };
    base.bounds = { min: [0, 0, 0], max: [16, 9.6, 8] };
    left.bounds = { min: [0, 8, 0], max: [8, 17.6, 8] };
    right.bounds = { min: [8, 8, 0], max: [16, 17.6, 8] };

    const batches = supportAwareBatches([top, base, left, right]);
    expect(batches.map(batch => batch.map(item => item.instanceId))).toEqual([
      [base.instanceId],
      [left.instanceId, right.instanceId],
      [top.instanceId],
    ]);
    const committed = [base];
    expect(batches[1].every(item =>
      committed.some(previous => partsConnect(item, previous)))).toBe(true);
  });

  it('builds movable subassemblies before scene foundations and places them last', () => {
    const files = splitMpd(`0 FILE airport.ldr
${licensed}
1 16 0 0 0 1 0 0 0 1 0 0 0 1 airplane.ldr
1 16 0 0 0 1 0 0 0 1 0 0 0 1 runway.ldr
0 FILE airplane.ldr
0 Airplane
${licensed}
1 4 0 -24 0 1 0 0 0 1 0 0 0 1 brick.dat
1 4 20 0 0 1 0 0 0 1 0 0 0 1 brick.dat
0 FILE runway.ldr
0 Runway
${licensed}
1 4 0 0 0 1 0 0 0 1 0 0 0 1 brick.dat
${part}`);
    const semantic = buildManifest(files, 'airport.ldr', colors, () => 'body');
    semantic.instances.forEach((instance, index) => {
      instance.bounds = { min: [index * 8, index * 4, 0], max: [index * 8 + 8, index * 4 + 8, 8] };
    });
    const plan = instructionPlan(files, 'airport.ldr', { instances: semantic.instances, groups });
    expect(plan.steps.map(step => step.title)).toEqual([
      'Airplane · 子装配',
      'Airplane · 子装配',
      'Runway · 子装配',
      'Airplane · 放置总成',
    ]);
    expect(plan.steps.at(-1)).toMatchObject({
      kind: 'placement',
      instanceIds: [],
      motionInstanceIds: ['brick_000001', 'brick_000002'],
    });
    expect(plan.steps.flatMap(step => step.instanceIds)).toHaveLength(3);
  });

  it('keeps every editorial batch attached to prior structure or starts one isolated root', () => {
    for (const model of modelCatalog) {
      const manifest = JSON.parse(
        readFileSync(`public/models/${model.id}/manifest.json`, 'utf8'),
      ) as AtlasManifest;
      if (manifest.instructions?.provenance !== 'editorial') continue;
      const byId = new Map(manifest.instances.map(item => [item.instanceId, item]));
      const byAssembly = new Map<string, PartInstance[]>();
      const steps = manifest.instructions.steps.filter(step => step.kind !== 'placement');
      for (const step of steps) {
        const assemblyId = step.assemblyId ?? step.sourceFile;
        const previous = byAssembly.get(assemblyId) ?? [];
        const batch = step.instanceIds.map(id => byId.get(id)!);
        const future = steps
          .filter(candidate => (candidate.assemblyId ?? candidate.sourceFile) === assemblyId)
          .flatMap(candidate => candidate.instanceIds)
          .map(id => byId.get(id)!)
          .filter(part =>
            !previous.some(item => item.instanceId === part.instanceId)
            && !batch.some(item => item.instanceId === part.instanceId));
        if (!previous.length) {
          expect(batch, `${model.id}:${step.id}:root`).toHaveLength(1);
        } else if (batch.some(part =>
          !previous.some(support => partsConnect(part, support)))) {
          expect(batch, `${model.id}:${step.id}:isolated-root`).toHaveLength(1);
          expect(
            [batch[0], ...future].some(part =>
              previous.some(support => partsConnect(part, support))),
            `${model.id}:${step.id}:connected-part-was-delayed`,
          ).toBe(false);
        }
        byAssembly.set(assemblyId, [...previous, ...batch]);
      }
      expect(steps.flatMap(step => step.instanceIds)).toHaveLength(manifest.instances.length);
      expect(new Set(steps.flatMap(step => step.instanceIds)).size).toBe(manifest.instances.length);
    }
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
