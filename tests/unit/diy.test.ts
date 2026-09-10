import { describe, expect, it } from 'vitest';
import { existsSync } from 'node:fs';
import {
  canRemove, commitDiy, DIY_LIMIT, DiyIndex, diyCategories, diyRecipes, diyToLdraw, emptyDiyProject, footprint,
  parseDiyProject, redoDiy, rotateDiyBrick, stamp, stampSize, undoDiy, type DiyBrush, type DiyHistory,
} from '../../src/diy/diyModel';
import { createDiyGeometry } from '../../src/diy/diyGeometry';
import { diyParts } from '../../src/diy/diyModel';

const brush: DiyBrush = { recipeId: '3001', color: 'red', turn: 0 };
describe('DIY placement', () => {
  it('offers a broad, unique and traceable multi-category part library', () => {
    expect(diyParts.length).toBeGreaterThanOrEqual(70);
    expect(new Set(diyParts.map(part => part.id)).size).toBe(diyParts.length);
    for (const category of diyCategories) {
      expect(diyParts.filter(part => part.category === category.id).length, category.id).toBeGreaterThanOrEqual(4);
    }
    expect(diyParts.every(part => existsSync(`assets-source/ldraw-library/locked/parts/${part.id}.dat`))).toBe(true);
  });
  it('snaps rotations on an unbounded stud grid including negative and distant coordinates', () => {
    const parts = stamp({ ...brush, turn: 1 }, -1002, 0, 4096, 'a');
    expect(parts[0]).toMatchObject({ x: -1002, y: 0, z: 4096, turn: 1 });
    expect(footprint(parts[0])).toEqual({ width: 2, depth: 4 });
    expect(new DiyIndex([]).validate(parts, 0)).toBeNull();
  });
  it('rejects overlap, permits stacked bricks and blocks unsupported pieces', () => {
    const first = stamp(brush, 0, 0, 0, 'a');
    const index = new DiyIndex(first);
    expect(index.validate(stamp(brush, 0, 0, 0, 'b'), 1)).toBe('overlap');
    expect(index.validate(stamp(brush, 0, 3, 0, 'b'), 1)).toBeNull();
    expect(index.validate(stamp(brush, 10, 3, 0, 'b'), 1)).toBe('unsupported');
    expect(index.validate(stamp(brush, 0, 1, 0, 'b'), 1)).toBe('overlap');
  });
  it('does not allow attaching above smooth tiles or the low end of a slope', () => {
    const tile = stamp({ ...brush, recipeId: '3068b' }, 0, 0, 0);
    expect(new DiyIndex(tile).validate(stamp({ ...brush, recipeId: '3005' }, 0, 1, 0), 1)).toBe('unsupported');
    const slope = stamp({ ...brush, recipeId: '3039' }, 0, 0, 0);
    expect(new DiyIndex(slope).validate(stamp({ ...brush, recipeId: '3005' }, 0, 3, 0), 1)).toBeNull();
    expect(new DiyIndex(slope).validate(stamp({ ...brush, recipeId: '3005' }, 0, 3, 1), 1)).toBe('unsupported');
    const jumper = stamp({ ...brush, recipeId: '87580' }, 0, 0, 0);
    expect(new DiyIndex(jumper).validate(stamp({ ...brush, recipeId: '3005' }, 0, 1, 0), 1)).toBeNull();
    expect(new DiyIndex(jumper).validate(stamp({ ...brush, recipeId: '3005' }, 1, 1, 1), 1)).toBe('unsupported');
  });
  it('keeps all assembly recipes supported at every quarter turn', () => {
    for (const recipe of diyRecipes) for (const turn of [0, 1, 2, 3] as const) {
      const parts = stamp({ ...brush, recipeId: recipe.id, turn }, -3, 0, 5);
      expect(new DiyIndex([]).validate(parts, 0), `${recipe.id}:${turn}`).toBeNull();
    }
    expect(stampSize({ ...brush, recipeId: 'gateway', turn: 1 })).toEqual({ width: 2, depth: 6, height: 9 });
  });
  it('protects supporting bricks from deletion', () => {
    const bottom = stamp(brush, 0, 0, 0, 'a'), top = stamp(brush, 0, 3, 0, 'b');
    expect(canRemove([...bottom, ...top], bottom[0].id)).toBe(false);
    expect(canRemove([...bottom, ...top], top[0].id)).toBe(true);
  });
  it('rotates an already placed brick and rejects rotations that break support', () => {
    const project = {
      ...emptyDiyProject(),
      bricks: stamp(brush, 0, 0, 0, 'bottom'),
    };
    const rotated = rotateDiyBrick(project, project.bricks[0].id);
    expect(rotated.issue).toBeNull();
    expect(rotated.project.bricks[0].turn).toBe(1);

    const supported = {
      ...project,
      bricks: [
        ...project.bricks,
        ...stamp({ ...brush, recipeId: '3005' }, 3, 3, 0, 'top'),
      ],
    };
    const rejected = rotateDiyBrick(supported, supported.bricks[0].id);
    expect(rejected.issue).toBe('unsupported');
    expect(rejected.project).toBe(supported);
  });
  it('limits physical count without imposing a board boundary', () => {
    expect(new DiyIndex([]).validate(stamp(brush, 0, 0, 0), DIY_LIMIT)).toBe('limit');
    expect(new DiyIndex([]).validate(stamp(brush, NaN, 0, 0), 0)).toBe('limit');
  });
  it('undoes entire stamps and drops redo after a new edit', () => {
    const project = emptyDiyProject();
    const initial: DiyHistory = { past: [], present: project, future: [] };
    const next = { ...project, bricks: stamp({ ...brush, recipeId: 'table' }, 0, 0, 0) };
    const history = commitDiy(initial, next);
    expect(undoDiy(history).present.bricks).toHaveLength(0);
    expect(redoDiy(undoDiy(history)).present).toEqual(next);
    expect(commitDiy(undoDiy(history), project).future).toHaveLength(0);
  });
  it('round-trips project data and rejects corrupt or overlapping imported projects', () => {
    const project = { ...emptyDiyProject(), bricks: stamp(brush, -4, 0, 0, 'a') };
    expect(parseDiyProject(JSON.stringify(project))).toEqual(project);
    expect(() => parseDiyProject('{"version":1,"name":"x","bricks":[{}]}')).toThrow();
    expect(() => parseDiyProject(JSON.stringify({ ...project, bricks: [...project.bricks, ...stamp(brush, -4, 0, 0, 'b')] }))).toThrow();
  });
  it('exports physical top-face coordinates and excludes the infinite ground', () => {
    const project = { ...emptyDiyProject(), bricks: stamp(brush, 0, 0, 0, 'a') };
    const lines = diyToLdraw(project).split('\n').filter(line => line.startsWith('1 '));
    expect(lines).toEqual(['1 4 40 -24 -20 1 0 0 0 1 0 0 0 1 3001.dat']);
  });
  it('renders finite nonempty geometry for every part', () => {
    for (const part of diyParts) {
      const geometry = createDiyGeometry(part);
      const position = geometry.getAttribute('position');
      expect(position.count).toBeGreaterThan(30);
      expect([...position.array].every(Number.isFinite)).toBe(true);
      geometry.dispose();
    }
  });
});
