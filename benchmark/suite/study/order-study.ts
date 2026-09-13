import assert from 'node:assert/strict';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { atomicJson } from '../../core/budget';
import { digest } from '../data';
import { dataset } from '../v2/dataset';
import { canonicalGeometry, dims, key, validate, bom } from '../geometry';
import { independentCheck } from '../research/independent-check';
import { surfaceSignature } from '../research/tasks';
import { type Part, type FrameSpec, type Structure } from '../shared';
import { parseJSON } from '../score';
import { SuiteRenderer } from '../render';
import { STUDY } from './protocol';
import { observedGroups, exposureRecords } from './exposure';
import { normalizeOrigin } from './reconstruction-ladder';
import { CAMERA_CONVENTION, poseScenes } from './pose-probes';
import { imageEvidence } from './calibration-export';
import { VALIDATION_MODELS } from './validation-client';

export const ORDER_DIR = resolve(STUDY, 'order-study');
export const ORDER_ARMS = ['original', 'repeat', 'permuted', 'no-image'] as const;
type Candidate = Pick<Part, 'x' | 'y' | 'z' | 'turn'> & { label: string };
interface Scene { group: string; policy: string; target: Structure; candidates: Candidate[] }

export function orderScenes(): Scene[] {
  const excluded = observedGroups(exposureRecords(false)), usedGeometry = new Set(poseScenes().map(s => s.geometry));
  const pool = dataset().filter(s => s.split === 'validation' && !excluded.has(s.group));
  const policies = [...new Set(pool.map(s => s.policy))].sort(), scenes: Scene[] = [];
  assert.equal(policies.length, 6);
  for (const policy of policies) {
    let accepted = 0;
    const candidates = pool.filter(s => s.policy === policy)
      .sort((a, b) => digest(`order-v1:${a.group}`).localeCompare(digest(`order-v1:${b.group}`)));
    for (const source of candidates) {
      const target = normalizeOrigin({ version: 1, parts: structuredClone(source.structure.parts.slice(0, 2)) });
      const [base, query] = target.parts;
      if (base.x || base.y || base.z) continue;
      base.id = 'base'; base.color = 'gray'; query.id = 'query'; query.color = 'blue';
      const geometry = canonicalGeometry(target.parts);
      if (usedGeometry.has(geometry)) continue;
      const d = dims(base), alternatives: Part[] = [];
      for (let x = 0; x < d.w; x++) for (let z = 0; z < d.d; z++) {
        const p = { ...query, x, z };
        if (key(p) !== key(query) && !validate([base, p]).length) alternatives.push(p);
      }
      alternatives.sort((a, b) => digest(`order-distractor:${key(a)}`).localeCompare(digest(`order-distractor:${key(b)}`)));
      if (alternatives.length < 3) continue;
      const poses = [query, ...alternatives.slice(0, 3)];
      const correctSlot = scenes.length % 4;
      const ordered = poses.map((_, i) => poses[(i - correctSlot + 4) % 4]);
      for (const p of ordered) assert.deepEqual(independentCheck([base, p]).issues, []);
      assert.equal(new Set(ordered.map(p => digest([...surfaceSignature([base, p])].sort()))).size, 4);
      scenes.push({ group: source.group, policy, target, candidates: ordered.map((p, i) => ({
        label: 'ABCD'[i], x: p.x, y: p.y, z: p.z, turn: p.turn,
      })) });
      usedGeometry.add(geometry); accepted++;
      if (accepted === 2) break;
    }
    assert.equal(accepted, 2, `Two distinct geometries required for ${policy}`);
  }
  assert.equal(scenes.length, 12);
  return scenes;
}
export function orderQuestions() {
  return orderScenes().flatMap((scene, index) => {
    // Balance repeat/permutation temporal order rather than confounding them.
    const arms = index % 2 ? ['original', 'permuted', 'repeat', 'no-image'] as const : ORDER_ARMS;
    return arms.map(arm => {
      const query = scene.target.parts[1], ordered = arm === 'permuted'
        ? [...scene.candidates.slice(1), scene.candidates[0]].map((c, i) => ({ ...c, label: 'ABCD'[i] })) : scene.candidates;
      const frames: FrameSpec[] = arm === 'no-image' ? [] : (['iso', 'top', 'front', 'side'] as const)
        .map(view => ({ parts: scene.target.parts, view, layer: null, title: `Ordinary assembled ${view}` }));
      const input = {
        prompt: 'Select the candidate pose of the BLUE query piece. All candidates are legal. Exactly one matches the reference. Return only {"choice":"A"} with the selected label.',
        convention: CAMERA_CONVENTION, billOfMaterials: bom(scene.target.parts),
        query: { partId: query.partId, color: query.color }, candidates: ordered,
        ...(arm === 'no-image' ? { observation: 'Images withheld; guess one of the four candidates using the remaining public information.' } : {}),
      };
      const expected = ordered.find(p => key({ ...query, ...p }) === key(query))!.label;
      return { id: digest({ version: 'order-repeat-1', group: scene.group, arm }).slice(0, 24),
        group: scene.group, policy: scene.policy, arm, input, frames, expected, query };
    });
  });
}
export type OrderQuestion = ReturnType<typeof orderQuestions>[number];
export function orderScore(q: OrderQuestion, raw: string) {
  const parsed = parseJSON(raw) as any;
  const selected = parsed && typeof parsed === 'object' && !Array.isArray(parsed) && typeof parsed.choice === 'string'
    ? q.input.candidates.find(c => c.label === parsed.choice) : undefined;
  return { format: Number(!!selected), success: Number(!!selected && parsed.choice === q.expected),
    selectedKey: selected ? key({ ...q.query, ...selected }) : null };
}
export async function prepareOrderStudy(renderer: SuiteRenderer) {
  const qs = orderQuestions(), rows = [], cache = new Map<string, string>();
  mkdirSync(resolve(ORDER_DIR, 'images'), { recursive: true });
  for (const q of qs) {
    const images = [];
    for (const frame of q.frames) {
      const recipe = digest(frame);
      let path = cache.get(recipe);
      if (!path) {
        const image = await renderer.render(frame); imageEvidence(image.buffer);
        path = `images/${image.hash}.png`; writeFileSync(resolve(ORDER_DIR, path), image.buffer); cache.set(recipe, path);
      }
      images.push(path);
    }
    rows.push({ id: q.id, group: q.group, arm: q.arm, input: q.input, images });
  }
  const protocol = { version: 'order-repeat-1', rows, models: VALIDATION_MODELS, plannedCalls: 192, sourceGroups: 12,
    scope: '12 unused validation sources, two per seen policy, distinct normalized two-piece prefixes. Development replication, not a new hidden test.',
    endpoint: 'Permutation mismatch minus same-order-repeat mismatch relative to the original response, paired per source/model.',
    interpretation: 'Same-order repetition estimates resampling instability; reordered and repeated calls are temporally counterbalanced. Candidate identity is compared, not labels. Four-model per-source results remain separate.',
    statisticalPlan: 'Report paired source differences and fixed-seed 1000-resample source bootstrap intervals; no significant ranking or confirmatory claim with 12 sources.',
    newSpendCap: 0.7, sharedValidationCap: 2 };
  const file = resolve(ORDER_DIR, 'protocol.json');
  if (existsSync(file)) assert.deepEqual(JSON.parse(readFileSync(file, 'utf8')), protocol);
  atomicJson(file, protocol);
  return { sourceGroups: 12, tasks: rows.length, images: cache.size, plannedCalls: 192 };
}
