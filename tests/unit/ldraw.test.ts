import { describe, expect, it } from 'vitest';
import { Matrix4 } from 'three';
import { assertLicensed, buildManifest, dependencyClosure, reference, splitMpd } from '../../scripts/ldraw';

const license = '0 Author: Test Author\n0 !LICENSE Licensed under CC BY 4.0 : see CAreadme.txt';
const part = `0 FILE parts/brick.dat\n0 Brick 1 x 1\n${license}\n0 !LDRAW_ORG Part\n3 16 0 0 0 1 0 0 0 1 0`;
const colors = '0 !COLOUR Red    CODE 4   VALUE #B40000 EDGE #333333';
const ref = (file: string, color = '16') => `1 ${color} 10 -20 30 1 0 0 0 1 0 0 0 1 ${file}`;

describe('LDraw semantic parser', () => {
  it('preserves spaces, case-insensitive paths and source lines', () => {
    const files = splitMpd(`0 FILE Main Model.ldr\n${license}\n${ref('PARTS\\Brick.dat', '4')}\n${part}`);
    expect([...files.keys()]).toEqual(['main model.ldr', 'parts/brick.dat']);
    expect(reference(ref('some model.ldr'), 42).file).toBe('some model.ldr');
    expect(dependencyClosure(files, 'main model.ldr')).toHaveLength(2);
  });
  it('composes transforms, inherits colors and steps, retains duplicate instances', () => {
    const files = splitMpd(`0 FILE main.ldr\n${license}\n0 STEP\n${ref('sub.ldr', '4')}\n0 FILE sub.ldr\n${license}\n${ref('brick.dat')}\n${ref('brick.dat')}\n${part}`);
    const result = buildManifest(files, 'main.ldr', colors);
    expect(result.instances).toHaveLength(2);
    const p = result.instances[0];
    expect(p.originalMatrix.slice(12, 15)).toEqual([8, 16, -24]);
    expect(p.colorCode).toBe('4');
    expect(p.buildStep).toBe(2);
    expect(result.instances.map(i => i.instanceId)).toEqual(['brick_000001', 'brick_000002']);
    expect(buildManifest(files, 'main.ldr', colors)).toEqual(result);
  });
  it('does not fabricate STEP metadata', () => {
    const files = splitMpd(`0 FILE main.ldr\n${license}\n${ref('brick.dat', '4')}\n${part}`);
    expect(buildManifest(files, 'main.ldr', colors).instances[0].buildStep).toBeNull();
  });
  it('rejects cycles, missing files, unlicensed files, unsafe paths and malformed geometry', () => {
    expect(() => dependencyClosure(splitMpd(`0 FILE a.ldr\n${license}\n${ref('a.ldr')}`), 'a.ldr')).toThrow(/Circular/);
    expect(() => dependencyClosure(splitMpd(`0 FILE a.ldr\n${license}\n${ref('no.dat')}`), 'a.ldr')).toThrow(/Missing/);
    expect(() => assertLicensed([...splitMpd('0 no license').values()][0])).toThrow(/license/);
    expect(() => reference(ref('../secret'), 1)).toThrow(/Unsafe/);
    expect(() => dependencyClosure(splitMpd(`0 FILE a.ldr\n${license}\n3 16 0 NaN`), 'a.ldr')).toThrow(/geometry/);
  });
  it('rejects nonfinite and singular transforms, supports mirrors', () => {
    expect(() => reference(ref('x').replace('10', 'NaN'), 1)).toThrow(/Non-finite/);
    expect(() => reference('1 4 0 0 0 0 0 0 0 0 0 0 0 0 x', 1)).toThrow(/Singular/);
    const mirror = reference('1 4 0 0 0 -1 0 0 0 1 0 0 0 1 x', 1);
    expect(new Matrix4().copy(mirror.matrix).determinant()).toBe(-1);
  });
  it('respects NOFILE and rejects duplicate FILE declarations', () => {
    const files = splitMpd('0 FILE a.ldr\n0 body\n0 NOFILE\n0 ignored\n0 FILE b.ldr\n0 second');
    expect(files.get('a.ldr')!.text).not.toContain('ignored');
    expect(() => splitMpd('0 FILE a.ldr\n0 FILE A.ldr')).toThrow(/Duplicate/);
  });
});
