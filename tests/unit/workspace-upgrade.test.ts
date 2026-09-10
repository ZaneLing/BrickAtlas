import { afterEach, describe, expect, it, vi } from 'vitest';
import { modelCatalog } from '../../atlas.config';
import { defaultCatalogFilter, filterCatalog, readFavorites } from '../../src/app/catalog';
import { changeHistory } from '../../src/app/useProjectHistory';
import { readSnapshots, removeSnapshot, saveSnapshot } from '../../src/app/projectSnapshots';
import { sanitizeBuildProgress } from '../../src/store/viewerStore';
import { createCompositionProject, createComposerItem, composerAssets, readCompositionProject, COMPOSITION_LIMIT } from '../../src/composer/compositionModel';
import { duplicateDiyBrick, emptyDiyProject, moveDiyBrick, stamp } from '../../src/diy/diyModel';
import { ASSEMBLY_PROGRESS_KEY, readAssemblyProgress } from '../../src/assembly/progress';
import { validateGlbBuffer } from '../../src/scene/gltfResources';

afterEach(() => vi.unstubAllGlobals());
function storage() {
  const data = new Map<string, string>();
  vi.stubGlobal('localStorage', { getItem: (key: string) => data.get(key) ?? null, setItem: (key: string, value: string) => data.set(key, value) });
  return data;
}

describe('workspace data boundaries', () => {
  it('filters models by all search terms, difficulty, favorites and progress', () => {
    expect(filterCatalog(modelCatalog, { ...defaultCatalogFilter, query: 'blue racer' }, [], {}).map(model => model.id)).toEqual(['31027']);
    expect(filterCatalog(modelCatalog, { ...defaultCatalogFilter, status: 'favorites' }, ['5867'], {}).map(model => model.id)).toEqual(['5867']);
    expect(filterCatalog(modelCatalog, { ...defaultCatalogFilter, status: 'started' }, [], { '31027': { completedStep: 1, placedIds: [], completed: false } })).toHaveLength(1);
    expect(filterCatalog(modelCatalog, { ...defaultCatalogFilter, query: 'nothing matches' }, [], {})).toHaveLength(0);
  });
  it('ignores corrupt favorites and filters unknown IDs', () => {
    const data = storage();
    data.set('brick-atlas-favorites-v1', '{"wrong":true}');
    expect(readFavorites()).toEqual([]);
    data.set('brick-atlas-favorites-v1', '["5867","5867","unknown"]');
    expect(readFavorites()).toEqual(['5867']);
  });
  it('restores only finite bounded integer build progress', () => {
    for (const value of [null, [], 'bad']) expect(sanitizeBuildProgress(value)).toEqual({});
    expect(sanitizeBuildProgress({ a: -1, b: '3', c: 1.5, d: Infinity, valid: 15, tooLarge: 10001 })).toEqual({ valid: 15 });
  });
  it('keeps undo/redo linear and no-ops at either boundary', () => {
    const history = { past: ['a', 'b'], present: 'c', future: [] };
    const undone = changeHistory(history, 'undo');
    expect(undone).toEqual({ past: ['a'], present: 'b', future: ['c'] });
    expect(changeHistory(undone, 'redo')).toEqual(history);
    expect(changeHistory(history, 'redo')).toBe(history);
  });
  it('bounds snapshots without silently evicting existing work', () => {
    storage();
    for (let i = 0; i < 8; i++) expect(saveSnapshot('snapshots', `Build ${i}`, '{}')).toBe(true);
    expect(saveSnapshot('snapshots', 'ninth', '{}')).toBe(false);
    const before = readSnapshots('snapshots');
    expect(before).toHaveLength(8);
    expect(removeSnapshot('snapshots', before[0].id)).toBe(true);
    expect(readSnapshots('snapshots')).toHaveLength(7);
  });
  it('normalizes duplicate placement IDs and contradictory zero-step completion', () => {
    const data = storage();
    data.set(ASSEMBLY_PROGRESS_KEY, JSON.stringify({
      '5867': { completedStep: 0, completed: true, placedIds: ['a', 'a'], updatedAt: 'bad', placedTurns: { a: 1, other: 2 }, placedPositions: { a: [0, 0, 0], other: [1, 2, 3] } },
    }));
    expect(readAssemblyProgress()['5867']).toEqual({
      completedStep: 0, completed: false, placedIds: ['a'], updatedAt: 0, placedTurns: { a: 1 }, placedPositions: { a: [0, 0, 0] },
    });
  });
});

describe('editing validation', () => {
  const asset = composerAssets.find(asset => asset.id === 'brick-2x4')!;
  it('rejects invalid composition imports without returning a replacement empty project', () => {
    expect(() => readCompositionProject('{"version":1,"items":[{}]}')).toThrow();
    const project = createCompositionProject();
    const item = createComposerItem(project, asset)!;
    for (const update of [{ x: 100 }, { x: 0.5 }, { level: -1 }]) {
      expect(() => readCompositionProject(JSON.stringify({ ...project, items: [{ ...item, ...update }] }))).toThrow();
    }
    expect(() => readCompositionProject(JSON.stringify({ ...project, items: [item, { ...item, id: 'copy' }] }))).toThrow();
    expect(readCompositionProject(JSON.stringify({ ...project, items: [item] })).items).toHaveLength(1);
  });
  it('enforces the total composition budget, including the baseplate', () => {
    const project = createCompositionProject();
    expect(createComposerItem(project, asset, Array.from({ length: COMPOSITION_LIMIT }, () => asset.bricks![0]))).toBeNull();
  });
  it('moves and duplicates DIY bricks only when the entire structure remains valid', () => {
    const bottom = stamp({ recipeId: '3001', color: 'red', turn: 0 }, 0, 0, 0, 'base');
    const top = stamp({ recipeId: '3005', color: 'blue', turn: 0 }, 0, 3, 0, 'top');
    const project = { ...emptyDiyProject(), bricks: [...bottom, ...top] };
    expect(moveDiyBrick(project, bottom[0].id, { x: 10 }).issue).toBe('unsupported');
    expect(moveDiyBrick(project, top[0].id, { x: 1 }).issue).toBeNull();
    expect(moveDiyBrick(project, top[0].id, { y: 1 }).issue).toBe('overlap');
    const copy = duplicateDiyBrick(project, top[0].id);
    expect(copy.issue).toBeNull();
    expect(copy.project.bricks).toHaveLength(3);
    expect(new Set(copy.project.bricks.map(brick => brick.id)).size).toBe(3);
  });
});

function glb(json: object) {
  const encoded = new TextEncoder().encode(JSON.stringify(json));
  const length = Math.ceil(encoded.length / 4) * 4;
  const buffer = new ArrayBuffer(20 + length);
  const view = new DataView(buffer);
  [0x46546c67, 2, buffer.byteLength, length, 0x4e4f534a].forEach((value, i) => view.setUint32(i * 4, value, true));
  new Uint8Array(buffer, 20).fill(32);
  new Uint8Array(buffer, 20, encoded.length).set(encoded);
  return buffer;
}
describe('GLB boundary', () => {
  it('accepts embedded GLB data and rejects external assets and malformed headers', () => {
    expect(() => validateGlbBuffer(glb({ asset: { version: '2.0' }, buffers: [{ byteLength: 0 }] }))).not.toThrow();
    expect(() => validateGlbBuffer(glb({ asset: { version: '2.0' }, images: [{ uri: 'https://example.com/image.png' }] }))).toThrow('external');
    expect(() => validateGlbBuffer(glb({ asset: { version: '2.0' }, buffers: [{ uri: '../mesh.bin', byteLength: 4 }] }))).toThrow('external');
    expect(() => validateGlbBuffer(glb({ asset: { version: '2.0' }, buffers: [{ byteLength: 1e12 }] }))).toThrow('120 MB');
    expect(() => validateGlbBuffer(new ArrayBuffer(25))).toThrow('header');
  });
});
