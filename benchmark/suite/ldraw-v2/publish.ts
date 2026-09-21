import { readFileSync, realpathSync } from 'node:fs';
import { resolve, dirname, basename } from 'node:path';
import { createHash } from 'node:crypto';
import type { Condition, ModelRequest, PublicBundle, PublicTask, V2Task } from './types';
import { conditions, labelPermutation, replaceLabels, alteredGraph } from './conditions';

export const root = resolve(import.meta.dirname, '../../..');
export const data = resolve(root, 'benchmark/ldraw-v2');
export const site = resolve(root, 'public/benchmark/ldraw-v2');
export const hash = (value: string | Buffer) => createHash('sha256').update(value).digest('hex');
export const SYSTEM_PROMPT = 'Solve the supplied item using only its declared evidence. Return exactly one JSON object: {"choiceId":"A"} for single choice; {"choiceIds":["A","B"]} for a set; {"value":1} for an integer; or {"actionIds":["action-id"]} for actions. Do not add prose. Display edits do not certify physical assembly or stability.';
const clone = <T>(v: T): T => JSON.parse(JSON.stringify(v));
const pick = (v: Record<string, any>, keys: string[]) => Object.fromEntries(keys.filter(k => k in v).map(k => [k, clone(v[k])]));
const inputKeys: Record<string, string[]> = {
  color: [], 'shape-match': [], distance: ['coordinateFrame', 'centers'],
  interface: ['connectorRecord', 'scope'], neighbors: ['edges', 'graphMeaning'],
  'graph-removal': ['edges', 'nodes', 'graphMeaning'], coverage: ['coverage'],
  'evidence-limit': ['available'], 'source-step': ['steps', 'provenance'],
  'source-sequence': ['initialFacts', 'goalFacts', 'absentFacts', 'budget', 'actions', 'editMode'],
  'restore-instance': ['initialFacts', 'goalFacts', 'absentFacts', 'budget', 'actions', 'editMode'],
};
export function publicInput(task: Pick<V2Task, 'family' | 'input'>) {
  if (!inputKeys[task.family]) throw new Error('Unknown family');
  const input = pick(task.input, inputKeys[task.family]);
  if (input.connectorRecord) input.connectorRecord = pick(input.connectorRecord, ['family', 'aConnector', 'bConnector']);
  if (input.coverage) input.coverage = input.coverage.map((r: any) => pick(r, ['label', 'supported']));
  if (input.steps) input.steps = input.steps.map((r: any) => pick(r, ['index', 'numbers']));
  if (input.actions) input.actions = input.actions.map((a: any) => pick(a, ['id', 'label', 'requires', 'forbids', 'adds', 'deletes', 'cost']));
  assertNoPrivateFields(input);
  return input;
}
export function publicTask(task: V2Task): PublicTask {
  const result: PublicTask = {
    id: task.id, modelId: task.modelId, family: task.family, modality: task.modality,
    format: task.format, promptEn: task.promptEn, input: publicInput(task),
  };
  if (task.options) result.options = task.options.map(o => ({ id: o.id, label: o.label }));
  if (task.visualInput) result.visualInput = { numberedView: task.visualInput.numberedView, isolationAllowed: true };
  assertNoPrivateFields(result);
  return result;
}
export function assertNoPrivateFields(value: unknown): void {
  if (!value || typeof value !== 'object') return;
  for (const [key, v] of Object.entries(value)) {
    if (/^(answer|evidenceDetail|references|targetModule|capabilities|evidence|canary|internalCanary)$/i.test(key))
      throw new Error(`Private field forbidden: ${key}`);
    assertNoPrivateFields(v);
  }
}
export function loadPublicBundle(file: string): PublicBundle {
  const actual = realpathSync(file), allowed = realpathSync(resolve(site, 'inputs'));
  if (dirname(actual) !== allowed || !/^[\w-]+\.json$/.test(basename(actual)))
    throw new Error('Runner accepts only versioned inputs/*.json, never internal scoring bundles');
  const bundle = JSON.parse(readFileSync(actual, 'utf8'));
  if (bundle.version !== 'brickatlas-ldraw-2' || bundle.role !== 'model-input') throw new Error('Wrong input role/version');
  assertNoPrivateFields(bundle);
  for (const t of bundle.tasks) {
    if (t.modelId !== bundle.modelId || !t.id.startsWith(`ld2-${bundle.modelId}-`)) throw new Error('Input task identity mismatch');
  }
  return bundle;
}

/** The only text/image request boundary. No spread of a task/bundle is allowed. */
export function serializeModelRequest(task: PublicTask, condition: Condition = 'standard',
  systemPrompt = SYSTEM_PROMPT, imageEncoder?: (path: string) => string): ModelRequest {
  if (!conditions.includes(condition)) throw new Error('Unknown condition');
  if (condition === 'graph-intervention') task = alteredGraph(task);
  const payload: Record<string, any> = { question: task.promptEn, format: task.format, input: publicInput(task) };
  if (task.options) payload.options = task.options.map(o => ({ id: o.id, label: o.label }));
  if (condition === 'graph-edges-withheld') delete payload.input.edges;
  if (condition === 'edge-order' && payload.input.edges) payload.input.edges.reverse();
  if (condition === 'choice-order' && payload.options) payload.options.reverse();
  if (condition === 'id-permutation') {
    Object.assign(payload, replaceLabels(payload, labelPermutation(payload)));
  }
  assertNoPrivateFields(payload);
  const content: Array<{ type: 'text'; text: string } | { type: 'image_url'; image_url: { url: string } }> =
    [{ type: 'text', text: JSON.stringify(payload) }];
  if (task.modality === 'visual' && condition !== 'text-without-image') {
    if (!task.visualInput) throw new Error('Missing visual input');
    let path = task.visualInput.numberedView;
    if (condition === 'full-scene') path = path.replace('/views/', '/views-full/');
    if (condition === 'background-mask') path = path.replace('/views/', '/views-mask/');
    if (condition === 'operand-only') path = path.replace('/views/', '/views-crop/');
    if (condition === 'id-permutation') path = path.replace('/views/', '/views-id/');
    if (condition === 'wrong-image') path = path.replace('/views/', '/views-wrong/');
    if (condition === 'camera-perturbation') path = path.replace('/views/', '/views-camera/');
    if (condition === 'color-nuisance') path = path.replace('/views/', '/views-neutral/');
    if (condition === 'multi-view') path = path.replace('/views/', '/views-crop/');
    if (!path.startsWith('benchmark/ldraw-v2/inputs/views') || path.includes('..')) throw new Error('Unsafe image reference');
    content.push({ type: 'image_url', image_url: { url: imageEncoder ? imageEncoder(path) : path } });
    if (condition === 'multi-view') {
      const second = path.replace('/views-crop/', '/views-camera/');
      content.push({ type: 'image_url', image_url: { url: imageEncoder ? imageEncoder(second) : second } });
    }
  }
  return { messages: [{ role: 'system', content: systemPrompt }, { role: 'user', content }] };
}
