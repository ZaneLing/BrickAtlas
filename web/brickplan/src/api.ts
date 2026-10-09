import type { Action, Catalogue, ModelRun, Models, Preview, SceneData, TaskInfo } from './types';

export const staticMode = document.querySelector('meta[name="brickplan-mode"]')?.getAttribute('content') === 'static';
const base = new URL('./', location.href);
export function asset(path: string) { return new URL(path.replace(/^\//, ''), base).href; }
export async function read<T>(path: string, payload?: unknown): Promise<T> {
  const response = await fetch(asset(path), payload === undefined ? {} : {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || `Request failed (${response.status})`);
  }
  return response.json();
}
const immutable = new Map<string, Promise<unknown>>();
function cached<T>(path: string): Promise<T> {
  const hit = immutable.get(path);
  if (hit) {
    immutable.delete(path); immutable.set(path, hit);
    return hit as Promise<T>;
  }
  const request = read<T>(path).catch(error => { immutable.delete(path); throw error; });
  immutable.set(path, request);
  if (immutable.size > 24) immutable.delete(immutable.keys().next().value!);
  return request;
}
let samples: { id: string; preview: string; scene: string }[] | undefined;
async function sample(id: string) {
  samples ??= await read('samples.json');
  const found = samples!.find(s => s.id === id);
  if (!found) throw new Error('此题需下载完整运行包；静态站提供每类一个可旋转示例。 Download the runtime for this question.');
  return found;
}
export const api = {
  info: () => staticMode ? Promise.resolve<TaskInfo>({ study: false, track: 'image-id', tasks: [] }) : read<TaskInfo>('api/tasks'),
  catalogue: () => read<Catalogue>(staticMode ? 'catalogue.json' : 'api/catalogue'),
  preview: async (id: string) => cached<Preview>(staticMode ? (await sample(id)).preview : `api/preview/${id}`),
  scene: async (id: string) => cached<SceneData>(staticMode ? (await sample(id)).scene : `api/scene/preview/${id}`),
  models: () => staticMode ? Promise.resolve<Models>({ providers: [], runs: [], cases: [{ id: 'case-local', title: 'SmolVLM-256M' }] }) : read<Models>('api/models'),
  run: (id: string) => read<ModelRun>(staticMode ? 'cases/local-vlm.json' : `api/model-runs/${id}`),
  runScene: (id: string) => read<SceneData>(staticMode ? 'cases/scene.json' : `api/model-runs/${id}/scene`),
  sampleIds: async () => staticMode ? (await read<{ id: string }[]>('samples.json')).map(s => s.id) : [],
};
export function describe(a?: Action) {
  if (!a) return 'Initial state';
  if (a.type === 'attach') return `安装 Attach ${a.partId} → ${a.siteId}`;
  if (a.type === 'detach') return `拆卸 Detach ${a.partId}`;
  if (a.type === 'audit') return `离架检修 Audit ${a.partId}`;
  if (a.type === 'inspect') return `获取视角 Camera · ${a.view}`;
  if (a.type === 'diagnose') return `诊断 Diagnosis · ${a.avoidableError ? 'error' : 'no error'}`;
  if (a.type === 'finish') return '结束 Finish';
  return a.type;
}
export function download(name: string, data: unknown) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' }));
  const link = document.createElement('a'); link.href = url; link.download = name; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
export function publicJSON(value: unknown) {
  return JSON.stringify(value, (key, item) => key === 'base64' ? '[image bytes]' : item, 2);
}
