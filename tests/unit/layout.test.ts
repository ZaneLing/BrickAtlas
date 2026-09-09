import { describe, expect, it } from 'vitest';
import manifestJSON from '../../public/models/5867/manifest.json';
import type { AtlasManifest } from '../../src/model/types';
import { initialState, searchInstances, visibleInstances } from '../../src/model/types';
import { explosionOffset, inventoryLayout, groupOffset } from '../../src/explosion/layout';

const manifest = manifestJSON as unknown as AtlasManifest;
describe('two-stage explosion', () => {
  for (const aspect of [0.45, 0.75, 1, 1.8, 2.5]) {
    it(`packs every instance without cell overlap at aspect ${aspect}`, () => {
      const layout = inventoryLayout(manifest.instances, aspect);
      expect(layout.cells.length).toBe(278);
      layout.cells.forEach((a, i) => {
        for (const b of layout.cells.slice(i + 1)) {
          const overlap = a.x < b.x + b.width - 1e-8 && a.x + a.width > b.x + 1e-8 &&
            a.y < b.y + b.height - 1e-8 && a.y + a.height > b.y + 1e-8;
          expect(overlap).toBe(false);
        }
      });
      expect(inventoryLayout(manifest.instances, aspect)).toEqual(layout);
    });
  }
  it('has exact, reversible endpoints and finite intermediate offsets', () => {
    const layout = inventoryLayout(manifest.instances, 1.6);
    for (const part of manifest.instances) {
      expect(explosionOffset(part, 0, manifest, layout)).toEqual([0, 0, 0]);
      expect(explosionOffset(part, 0.45, manifest, layout)).toEqual(groupOffset(part, manifest));
      explosionOffset(part, 1, manifest, layout).forEach((v, i) => expect(v).toBeCloseTo(layout.offsets.get(part.instanceId)![i], 8));
      for (const e of [0.13, 0.44, 0.451, 0.72, 0.999]) expect(explosionOffset(part, e, manifest, layout).every(Number.isFinite)).toBe(true);
    }
  });
  it('recomputes only the chosen visible set and handles an empty set', () => {
    expect(inventoryLayout([], 1).cells).toEqual([]);
    const subset = manifest.instances.slice(0, 3);
    expect(inventoryLayout(subset, 0.6).offsets.size).toBe(3);
  });
});
describe('queries and visibility', () => {
  it('searches identifiers, names, colors, submodels and Chinese functional groups', () => {
    for (const query of ['3004', 'plate', 'red', 'rear', '轮胎', '红色', '透明玻璃']) expect(searchInstances(manifest, query).length).toBeGreaterThan(0);
    expect(searchInstances(manifest, 'not-a-part')).toEqual([]);
  });
  it('composes hidden groups and isolation without mutating the manifest', () => {
    const part = manifest.instances[0];
    expect(visibleInstances(manifest, { ...initialState, isolation: [part.instanceId] })).toEqual([part]);
    expect(visibleInstances(manifest, { ...initialState, isolation: [part.instanceId], hiddenGroups: [part.groupId] })).toEqual([]);
    expect(visibleInstances(manifest, initialState)).toHaveLength(278);
  });
});
