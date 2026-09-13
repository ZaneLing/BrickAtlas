import assert from 'node:assert/strict';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { digest } from '../data';
import { bom, canonicalGeometry, dims, key, validate } from '../geometry';
import { type Part, type Structure, type FrameSpec } from '../shared';
import { independentCheck } from '../research/independent-check';
import { surfaceSignature } from '../research/tasks';
import { parseJSON } from '../score';
import { type CaseTask, structureSchema } from '../v2/cases';
import { evaluateStrict } from './strict-evaluate';
import { calibrationSelection } from './calibration';
import { ladderTasks, normalizeOrigin } from './reconstruction-ladder';
import { validationCases } from './model-validation';
import { STUDY } from './protocol';
import { atomicJson } from '../../core/budget';
import { SuiteRenderer } from '../render';
import { imageEvidence } from './calibration-export';
import { VALIDATION_MODELS } from './validation-client';

export const POSE_DIR = resolve(STUDY, 'pose-probes');
export const POSE_ARMS = ['full-rgb', 'pose-rgb', 'choice-rgb', 'choice-permuted', 'choice-no-image', 'pose-symbolic'] as const;
export type PoseArm = typeof POSE_ARMS[number];
type Pose = Pick<Part, 'x' | 'y' | 'z' | 'turn'>;
const pose = (p: Part): Pose => ({ x: p.x, y: p.y, z: p.z, turn: p.turn });
export const CAMERA_CONVENTION = {
  projection: 'Orthographic; views recentered/rescaled to fit the structure.',
  origin: 'Minimum X/Y/Z of the entire structure are each 0.',
  position: 'Minimum body X/Z corner and bottom Y. X/Z are stud units; Y is plate-height units, 0.4 stud per unit.',
  front: 'Camera on positive Z, looking toward negative Z. Image right is +X, image up is +Y.',
  side: 'Camera on positive X, looking toward negative X. Image right is -Z, image up is +Y.',
  top: 'Camera on positive Y with tiny positive Z offset. Image right is +X, image down is +Z. Grid labels mark stud-cell centers.',
  turn: '0 or 2: catalog width along X, depth along Z. 1 or 3 swaps width and depth. Equivalent yaw footprints are accepted.',
};

export function poseScenes() {
  const excluded = new Set([...validationCases().chosen.map(o => o.group), ...ladderTasks().map(t => t.task.spec.group)]);
  const pool = calibrationSelection().objects.filter(o => !excluded.has(o.group))
    .sort((a, b) => digest(`pose-probe-1:${a.group}`).localeCompare(digest(`pose-probe-1:${b.group}`)));
  const seen = new Set<string>();
  const scenes: Array<{ group: string; policy: string; geometry: string; target: Structure; candidates: Pose[] }> = [];
  for (const source of pool) {
    const target = normalizeOrigin({ version: 1, parts: structuredClone(source.structure.parts.slice(0, 2)) });
    target.parts[0].id = 'base'; target.parts[0].color = 'gray';
    target.parts[1].id = 'query'; target.parts[1].color = 'blue';
    if (target.parts[0].x !== 0 || target.parts[0].y !== 0 || target.parts[0].z !== 0) continue;
    assert.deepEqual(validate(target.parts), []);
    assert.deepEqual(independentCheck(target.parts).issues, []);
    const geometry = canonicalGeometry(target.parts);
    if (seen.has(geometry)) continue;
    const base = target.parts[0], query = target.parts[1], d = dims(base);
    const alternatives: Part[] = [];
    // All distractors use the same part/yaw/height and are independently legal.
    for (let x = base.x; x < base.x + d.w; x++) for (let z = base.z; z < base.z + d.d; z++) {
      const p = { ...query, x, z };
      if (key(p) !== key(query) && !validate([base, p]).length) alternatives.push(p);
    }
    alternatives.sort((a, b) => digest(`distractor:${key(a)}`).localeCompare(digest(`distractor:${key(b)}`)));
    if (alternatives.length < 3) continue;
    const candidates = [query, ...alternatives.slice(0, 3)];
    const slot = scenes.length;
    const ordered = candidates.map((_, i) => candidates[(i - slot + 4) % 4]);
    for (const candidate of ordered) assert.deepEqual(independentCheck([base, candidate]).issues, []);
    assert.equal(new Set(ordered.map(p => key(p))).size, 4);
    assert.equal(new Set(ordered.map(p => digest([...surfaceSignature([base, p])].sort()))).size, 4);
    scenes.push({ group: source.group, policy: source.policy, geometry, target, candidates: ordered.map(pose) });
    seen.add(geometry);
    if (scenes.length === 4) break;
  }
  assert.equal(scenes.length, 4, 'Four distinct scene geometries are required');
  return scenes;
}

export function poseQuestions() {
  return poseScenes().flatMap(scene => POSE_ARMS.map(arm => {
    const query = scene.target.parts[1], choice = arm.startsWith('choice');
    const candidates = arm === 'choice-permuted' ? [...scene.candidates.slice(1), scene.candidates[0]] : scene.candidates;
    const choices = candidates.map((p, i) => ({ label: 'ABCD'[i], ...p }));
    const imagesAllowed = !['choice-no-image', 'pose-symbolic'].includes(arm);
    const frames: FrameSpec[] = imagesAllowed ? (['iso', 'top', 'front', 'side'] as const).map(view => ({
      parts: scene.target.parts, view, layer: null, title: `Ordinary assembled ${view}`,
    })) : [];
    const id = digest({ version: 'pose-probe-1', group: scene.group, arm }).slice(0, 24);
    const input = {
      prompt: arm === 'full-rgb' ? 'Return the full two-piece structure matching the images and supplied known part identities.'
        : choice ? 'Select the candidate pose of the BLUE query piece. All candidates are legal. Exactly one matches the reference. Return only {"choice":"A"} with the selected label.'
          : 'Return only the BLUE query piece pose as {"x":0,"y":0,"z":0,"turn":0}, matching the reference.',
      convention: CAMERA_CONVENTION,
      billOfMaterials: bom(scene.target.parts),
      query: { partId: query.partId, color: query.color },
      responseSchema: arm === 'full-rgb' ? structureSchema : choice ? { choice: 'A|B|C|D' } : { x: 'integer', y: 'integer', z: 'integer', turn: '0|1|2|3' },
      ...(choice ? { candidates: choices } : {}),
      ...(arm === 'choice-no-image' ? { observation: 'Images withheld; no reference pose supplied. Guess one of the four candidates.' } : {}),
      ...(arm === 'pose-symbolic' ? { reference: scene.target } : {}),
    };
    const oracle = arm === 'full-rgb' ? scene.target : choice ? {
      choice: choices.find(c => key({ ...query, ...c }) === key(query))!.label,
    } : pose(query);
    const spec = { id, group: scene.group, modelId: scene.group, kind: 'reconstruct' as const, variant: 'full',
      condition: 'ordinary' as const, policy: scene.policy, difficulty: 'two-piece', split: 'validation' as const };
    const fullTask: CaseTask = { spec, target: scene.target, source: null, oracle: scene.target, changedIds: [], frames,
      public: { id, kind: 'reconstruct', split: 'validation', family: scene.policy, prompt: input.prompt,
        input: { billOfMaterials: input.billOfMaterials }, responseSchema: structureSchema, imageTitles: frames.map(f => f.title) } };
    return { id, group: scene.group, arm, input, oracle, frames, query, candidates: choices, fullTask };
  }));
}
export type PoseQuestion = ReturnType<typeof poseQuestions>[number];

export function scorePose(q: PoseQuestion, raw: string) {
  const a = parseJSON(raw) as any;
  if (q.arm === 'full-rgb') {
    const v = evaluateStrict(q.fullTask, a);
    return { format: v.metrics.format, success: v.metrics.success, x: null, y: null, z: null, orientation: null,
      selectedPose: null as Pose | null, metrics: v.metrics };
  }
  const object = !!a && typeof a === 'object' && !Array.isArray(a);
  if (q.arm.startsWith('choice')) {
    const selected = object && typeof a.choice === 'string' ? q.candidates.find(c => c.label === a.choice) : undefined;
    return { format: Number(!!selected), success: Number(!!selected && key({ ...q.query, ...selected }) === key(q.query)),
      x: null, y: null, z: null, orientation: null, selectedPose: selected ? pose({ ...q.query, ...selected }) : null, metrics: null };
  }
  const format = object && ['x', 'y', 'z', 'turn'].every(k => typeof a[k] === 'number' && Number.isInteger(a[k]))
    && [0, 1, 2, 3].includes(a.turn) && ['x', 'y', 'z'].every(k => a[k] >= 0 && a[k] <= 24);
  const d = dims(q.query);
  const orientation = Number(!!format && (d.w === d.d || a.turn % 2 === q.query.turn % 2));
  const x = Number(!!format && a.x === q.query.x), y = Number(!!format && a.y === q.query.y), z = Number(!!format && a.z === q.query.z);
  return { format: Number(!!format), success: Number(!!format && x && y && z && orientation),
    x, y, z, orientation, selectedPose: format ? pose({ ...q.query, ...a }) : null, metrics: null };
}

export async function preparePoseProbes(renderer: SuiteRenderer) {
  const questions = poseQuestions(), rows = [], cache = new Map<string, string>();
  mkdirSync(resolve(POSE_DIR, 'images'), { recursive: true });
  for (const q of questions) {
    const images = [];
    for (const frame of q.frames) {
      const recipe = digest(frame);
      let path = cache.get(recipe);
      if (!path) {
        const image = await renderer.render(frame); imageEvidence(image.buffer);
        path = `images/${image.hash}.png`; cache.set(recipe, path);
        writeFileSync(resolve(POSE_DIR, path), image.buffer);
      }
      images.push(path);
    }
    assert.equal(scorePose(q, JSON.stringify(q.oracle)).success, 1);
    rows.push({ id: q.id, group: q.group, arm: q.arm, input: q.input, images });
  }
  const protocol = { version: 'pose-probe-1', models: VALIDATION_MODELS, rows, plannedCalls: 96,
    sourceGroups: poseScenes().map(s => s.group), temperature: 0, maxTokens: 2200,
    newSpendCap: 0.6, pairedUnits: 4,
    scope: 'Four distinct normalized two-piece prefixes from four unused calibration sources. Colors canonicalized to gray base/blue query; part identities supplied. Adaptive development diagnosis, not independent confirmatory testing.',
    caveats: ['Choice alternatives add candidate information, so choice vs generation is not an information-matched causal comparison.',
      'Permutation consistency does not imply correctness; no-image is a guessing control with chance expectation 25%, not a guaranteed score.',
      'Correct labels are balanced over four scenes; candidate poses differ and all are legal.',
      'Top/front/side conventions are declared, but no new camera calibration algorithm or human observability study is claimed.',
      'Full-structure output is only two pieces here: do not call differences a demonstrated long-output bottleneck.'] };
  const file = resolve(POSE_DIR, 'protocol.json');
  if (existsSync(file)) assert.deepEqual(JSON.parse(readFileSync(file, 'utf8')), protocol);
  atomicJson(file, protocol);
  atomicJson(resolve(POSE_DIR, 'oracle-audit.json'), { cases: questions.length, oraclesPass: true, sourceGroups: 4,
    distinctGeometry: 4, allCandidatesLegal: true, candidateChanceExpectation: 0.25,
    note: 'Evaluator-only evidence; no oracles or generator metadata are added to model inputs.' });
  return { cases: rows.length, images: cache.size, plannedCalls: 96 };
}
