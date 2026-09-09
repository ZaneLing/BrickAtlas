import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { Matrix4, Box3 } from 'three';
import { atlasConfig } from '../atlas.config';
import type { AtlasManifest, GroupId, PartInstance, Vec3 } from '../src/model/types';

export const hash = (data: string | Uint8Array) => createHash('sha256').update(data).digest('hex');
export const normalize = (name: string) => name.trim().replaceAll('\\', '/').toLowerCase();
export interface LDrawFile { name: string; text: string; lines: { text: string; line: number }[] }
export interface Reference { color: string; matrix: Matrix4; file: string; line: number }

export function splitMpd(text: string, fallback = 'main.ldr'): Map<string, LDrawFile> {
  const files = new Map<string, LDrawFile>();
  let current: LDrawFile | null = null;
  const lines = text.replaceAll('\r', '').split('\n');
  const multi = lines.some(l => /^0 FILE /i.test(l.trim()));
  if (!multi) {
    current = { name: normalize(fallback), text, lines: [] };
    files.set(current.name, current);
  }
  lines.forEach((raw, i) => {
    const line = raw.trim();
    const match = /^0 FILE (.+)$/i.exec(line);
    if (match) {
      const name = normalize(match[1]);
      if (files.has(name)) throw new Error(`Duplicate FILE: ${name}`);
      current = { name, text: '', lines: [] };
      files.set(name, current);
    } else if (/^0 NOFILE$/i.test(line)) {
      current = null;
    } else if (current) {
      current.lines.push({ text: line, line: i + 1 });
      if (multi) current.text += raw + '\n';
    }
  });
  if (!files.size) throw new Error('No LDraw files');
  return files;
}

export function reference(text: string, line: number): Reference {
  const t = text.trim().split(/\s+/);
  if (t.length < 15 || t[0] !== '1') throw new Error(`Invalid reference at line ${line}`);
  const n = t.slice(2, 14).map(Number);
  if (n.some(v => !Number.isFinite(v))) throw new Error(`Non-finite matrix at line ${line}`);
  const [x, y, z, a, b, c, d, e, f, g, h, i] = n;
  const matrix = new Matrix4().set(a, b, c, x, d, e, f, y, g, h, i, z, 0, 0, 0, 1);
  if (Math.abs(matrix.determinant()) < 1e-10) throw new Error(`Singular matrix at line ${line}`);
  const file = normalize(t.slice(14).join(' '));
  if (file.startsWith('/') || file.split('/').includes('..')) throw new Error(`Unsafe reference ${file}`);
  // Some OMR exports serialize the inherited-color sentinel -1 as uint32.
  const color = t[1] === '4294967295' ? '16' : t[1];
  return { color, matrix, file, line };
}

export function header(file: LDrawFile, key: string) {
  return file.lines.find(l => l.text.toLowerCase().startsWith(`0 ${key.toLowerCase()}`))?.text.slice(key.length + 2).trim() ?? '';
}

export function assertLicensed(file: LDrawFile) {
  const license = header(file, '!LICENSE');
  if (!/CC BY (2\.0|4\.0)|CCAL version 2\.0|CC0/i.test(license))
    throw new Error(`Missing or unapproved license in ${file.name}: ${license}`);
  if (!header(file, 'Author:')) throw new Error(`Missing author in ${file.name}`);
}

export function resolveFile(files: Map<string, LDrawFile>, name: string) {
  const normalized = normalize(name);
  for (const key of [normalized, `parts/${normalized}`, `p/${normalized}`, `models/${normalized}`]) {
    if (files.has(key)) return files.get(key)!;
  }
  throw new Error(`Missing dependency: ${name}`);
}

export function dependencyClosure(files: Map<string, LDrawFile>, root: string) {
  const used = new Set<string>();
  const stack = new Set<string>();
  function visit(file: LDrawFile) {
    if (stack.has(file.name)) throw new Error(`Circular reference: ${[...stack, file.name].join(' -> ')}`);
    if (used.has(file.name)) return;
    assertLicensed(file);
    stack.add(file.name);
    for (const { text, line } of file.lines) {
      if (text.startsWith('1 ')) visit(resolveFile(files, reference(text, line).file));
      const kind = Number(text[0]);
      if ([2, 3, 4, 5].includes(kind) && text[1] === ' ') {
        const tokens = text.split(/\s+/);
        const expected = { 2: 8, 3: 11, 4: 14, 5: 14 }[kind];
        if (tokens.length !== expected || tokens.slice(2).some(t => !Number.isFinite(Number(t))))
          throw new Error(`Invalid geometry: ${file.name}:${line}`);
      }
      if (/^0 !TEXMAP/i.test(text)) throw new Error(`TEXMAP requires an explicit texture pipeline: ${file.name}`);
    }
    stack.delete(file.name);
    used.add(file.name);
  }
  visit(resolveFile(files, root));
  return [...used].sort();
}

interface ClassificationRule { groupId: GroupId; path?: string; name?: string; colors?: string[]; xMin?: number; xMax?: number; yMin?: number; yMax?: number }
const classification: { groups: AtlasManifest['groups']; rules: ClassificationRule[]; defaultGroup: GroupId } = JSON.parse(readFileSync(atlasConfig.classificationFile, 'utf8'));
export const groups: AtlasManifest['groups'] = classification.groups.map(group => ({ ...group, instanceIds: [] }));

// Model-specific editorial classification. Submodels take priority; the remaining
// flat root is classified by source-space position and the official part name.
export function classify(part: Pick<PartInstance, 'path' | 'displayName' | 'originalMatrix' | 'colorCode'>): GroupId {
  const path = part.path.join(' ').toLowerCase();
  const x = part.originalMatrix[12], y = part.originalMatrix[13];
  for (const rule of classification.rules) {
    if (rule.path && !new RegExp(rule.path, 'i').test(path)) continue;
    if (rule.name && !new RegExp(rule.name, 'i').test(part.displayName)) continue;
    if (rule.colors && !rule.colors.includes(part.colorCode)) continue;
    if (rule.xMin !== undefined && x <= rule.xMin) continue;
    if (rule.xMax !== undefined && x >= rule.xMax) continue;
    if (rule.yMin !== undefined && y <= rule.yMin) continue;
    if (rule.yMax !== undefined && y >= rule.yMax) continue;
    return rule.groupId;
  }
  return classification.defaultGroup;
}

export function parseColors(text: string) {
  const colors = new Map<string, { name: string; hex: string }>();
  for (const line of text.split('\n')) {
    const m = /0\s+!COLOUR\s+(\S+)\s+CODE\s+(\d+)\s+VALUE\s+(#[a-f\d]{6})/i.exec(line);
    if (m) colors.set(m[2], { name: m[1].replaceAll('_', ' '), hex: m[3] });
  }
  return colors;
}

export function buildManifest(files: Map<string, LDrawFile>, root: string, colorText: string, classifier = classify) {
  const colors = parseColors(colorText);
  const instances: PartInstance[] = [];
  const submodels: AtlasManifest['submodels'] = [];
  const axis = new Matrix4().makeScale(0.4, -0.4, -0.4);
  const stack = new Set<string>();
  function visit(file: LDrawFile, parent: Matrix4, color: string, path: string[], address: string, parentId: string | null, inheritedStep: number | null) {
    if (stack.has(file.name)) throw new Error(`Circular reference: ${file.name}`);
    stack.add(file.name);
    const id = `s-${hash(address).slice(0, 16)}`;
    submodels.push({ id, name: header(file, '') || file.name, parentId, sourceFile: file.name });
    const hasSteps = file.lines.some(l => /^0 (STEP|ROTSTEP)( |$)/.test(l.text));
    let step = hasSteps ? 1 : inheritedStep;
    let ordinal = 0;
    for (const { text, line } of file.lines) {
      if (/^0 (STEP|ROTSTEP)( |$)/.test(text)) { step = (step ?? 1) + 1; continue; }
      if (!text.startsWith('1 ')) continue;
      const ref = reference(text, line);
      const child = resolveFile(files, ref.file);
      const world = parent.clone().multiply(ref.matrix);
      const resolvedColor = ref.color === '16' ? color : ref.color;
      const childAddress = `${address}/${ordinal++}:${child.name}`;
      if (child.name.endsWith('.ldr') || /(?:^|_)Model\b/.test(header(child, '!LDRAW_ORG'))) {
        visit(child, world, resolvedColor, [...path, child.name], childAddress, id, step);
      } else {
        const matrix = axis.clone().multiply(world);
        const colorInfo = colors.get(resolvedColor) ?? (/^0x2[\da-f]{6}$/i.test(resolvedColor)
          ? { name: 'Direct color', hex: `#${resolvedColor.slice(3)}` } : null);
        if (!colorInfo) throw new Error(`Unknown color: ${resolvedColor}`);
        const displayName = child.lines.find(l => l.text.startsWith('0 ') && !/^0 (!|Name:|Author:)/.test(l.text))?.text.slice(2) ?? child.name;
        const part: PartInstance = {
          instanceId: `brick_${String(instances.length + 1).padStart(6, '0')}`, index: instances.length,
          partNumber: child.name.replace(/^parts\//, '').replace(/\.dat$/, ''),
          displayName, colorCode: resolvedColor, colorName: colorInfo.name, colorHex: colorInfo.hex,
          sourceFile: file.name, sourceLine: line, parentSubmodelId: id, path,
          buildStep: step, originalMatrix: matrix.toArray(), bounds: { min: [0, 0, 0], max: [0, 0, 0] },
          category: header(child, '!CATEGORY') || displayName.replace(/^[~_=]/, '').split(' ')[0],
          tags: header(child, '!KEYWORDS').split(',').map(t => t.trim()).filter(Boolean),
          groupId: 'body',
        };
        part.groupId = classifier(part);
        instances.push(part);
      }
    }
    stack.delete(file.name);
  }
  visit(resolveFile(files, root), new Matrix4(), '7', [root], root, null, null);
  if (!instances.length) throw new Error('Empty model');
  return { instances, submodels };
}

export function boundsJSON(box: Box3) {
  if (box.isEmpty() || [...box.min.toArray(), ...box.max.toArray()].some(v => !Number.isFinite(v))) throw new Error('Invalid bounds');
  return { min: box.min.toArray() as Vec3, max: box.max.toArray() as Vec3 };
}

export function referenceLine(instance: PartInstance) {
  const axisInverse = new Matrix4().makeScale(2.5, -2.5, -2.5);
  const e = axisInverse.multiply(new Matrix4().fromArray(instance.originalMatrix)).elements;
  return `1 ${instance.colorCode} ${[e[12], e[13], e[14], e[0], e[4], e[8], e[1], e[5], e[9], e[2], e[6], e[10]].join(' ')} ${instance.partNumber}.dat`;
}
