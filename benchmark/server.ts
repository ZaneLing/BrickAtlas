import http from 'node:http';
import { randomUUID } from 'node:crypto';
import { createServer as createViteServer } from 'vite';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { Environment } from './core/environment';
import { HARD_CAP_USD, atomicJson, type Ledger } from './core/budget';
import { RenderService, type Frame } from './core/render-service';
import { MODELS } from './core/openrouter';
import { pilotTasks, taskSummary } from './core/tasks';
import { summaries, type RunResult } from './core/results';
import { ROOT, loadKey, runPilot, type PilotProgress } from './run';

const keyPresent = Boolean(loadKey());
const clientToken = randomUUID();
const tasks = pilotTasks();
const sessions = new Map<string, { env: Environment; touched: number }>();
const images = new Map<string, Buffer>();
let progress: PilotProgress = { status: 'idle', completed: 0, total: 0 };
let url = '';
let render: RenderService;
const vite = await createViteServer({
  configFile: resolve(ROOT, 'vite.config.ts'),
  server: { middlewareMode: true, hmr: false },
  appType: 'mpa',
});

const json = (response: http.ServerResponse, status: number, value: unknown) => {
  response.writeHead(status, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff' });
  response.end(JSON.stringify(value));
};
async function body(request: http.IncomingMessage) {
  const chunks: Buffer[] = [];
  let bytes = 0;
  for await (const chunk of request) {
    bytes += chunk.length;
    if (bytes > 64_000) throw new Error('Request too large');
    chunks.push(chunk);
  }
  return JSON.parse(Buffer.concat(chunks).toString('utf8'));
}
function budgetSummary() {
  const path = resolve(ROOT, '.runtime/campaign-ledger.json');
  if (!existsSync(path)) return { cap: HARD_CAP_USD, spent: 0, committed: 0, calls: 0, blocked: false };
  const ledger = JSON.parse(readFileSync(path, 'utf8')) as Ledger;
  return { cap: ledger.cap, spent: ledger.charges.reduce((s, c) => s + (c.actual ?? 0), 0),
    committed: ledger.charges.reduce((s, c) => s + (c.actual ?? c.reserved), 0),
    calls: ledger.charges.length, blocked: ledger.charges.some(c => c.status !== 'settled') };
}
function remember(frame: Frame) {
  images.set(frame.hash, frame.buffer);
  while (images.size > 256) images.delete(images.keys().next().value!);
  return `/api/images/${frame.hash}.png`;
}
async function observation(env: Environment) {
  const frame = await render.render(env.sceneParts(), env.view, env.visibleParts().map(p => p.id));
  return { ...env.observe(), imageUrl: remember(frame), score: env.phase === 'done' ? env.score() : null };
}
function resultIds() {
  return existsSync(resolve(ROOT, 'results'))
    ? readdirSync(resolve(ROOT, 'results'), { withFileTypes: true })
      .filter(e => e.isDirectory() && /^[\w.-]{1,100}$/.test(e.name)
        && existsSync(resolve(ROOT, 'results', e.name, 'run.json'))).map(e => e.name).sort().reverse()
    : [];
}

const server = http.createServer(async (request, response) => {
  const path = new URL(request.url ?? '/', 'http://localhost').pathname;
  try {
    if (!path.startsWith('/api/')) {
      vite.middlewares(request, response, () => {
        response.writeHead(404);
        response.end('Not found');
      });
      return;
    }
    const origin = request.headers.origin;
    if (origin && origin !== url) { json(response, 403, { error: 'Cross-origin request denied' }); return; }
    if (!['127.0.0.1', 'localhost'].includes((request.headers.host ?? '').split(':')[0])) {
      json(response, 403, { error: 'Host denied' }); return;
    }
    if (request.method === 'POST' && request.headers['x-benchmark-client'] !== clientToken) {
      json(response, 403, { error: 'Missing same-origin client token' }); return;
    }
    if (request.method === 'GET' && path === '/api/status') {
      json(response, 200, { title: 'Brick Atlas Benchmark', version: 'CARE-mini v1',
        keyPresent, clientToken, models: MODELS, budget: budgetSummary(), progress,
        running: progress.status === 'running' || existsSync(resolve(ROOT, '.runtime/pilot.lock')) });
    } else if (request.method === 'GET' && path === '/api/tasks') {
      json(response, 200, tasks.map(taskSummary));
    } else if (request.method === 'POST' && path === '/api/sessions') {
      const data = await body(request);
      const task = tasks.find(t => t.id === data.taskId);
      if (!task || !['active', 'passive'].includes(data.protocol ?? 'active')) {
        json(response, 400, { error: 'Invalid task/protocol' }); return;
      }
      for (const [id, s] of sessions) if (Date.now() - s.touched > 3_600_000) sessions.delete(id);
      if (sessions.size >= 40) { json(response, 429, { error: 'Session limit reached' }); return; }
      const id = randomUUID();
      const env = new Environment(task, data.protocol ?? 'active');
      sessions.set(id, { env, touched: Date.now() });
      json(response, 200, { id, observation: await observation(env) });
    } else if (request.method === 'POST' && /^\/api\/sessions\/[\w-]+\/actions$/.test(path)) {
      const session = sessions.get(path.split('/')[3]);
      if (!session) { json(response, 404, { error: 'Session expired' }); return; }
      session.env.step(await body(request));
      session.touched = Date.now();
      json(response, 200, await observation(session.env));
    } else if (request.method === 'GET' && /^\/api\/images\/[a-f0-9]{64}\.png$/.test(path)) {
      const buffer = images.get(path.split('/').at(-1)!.slice(0, -4));
      if (!buffer) { json(response, 404, { error: 'Frame expired' }); return; }
      response.writeHead(200, { 'Content-Type': 'image/png', 'Cache-Control': 'no-store' });
      response.end(buffer);
    } else if (request.method === 'GET' && path === '/api/results') {
      json(response, 200, resultIds().map(id => {
        const run = JSON.parse(readFileSync(resolve(ROOT, 'results', id, 'run.json'), 'utf8')) as RunResult;
        return { id, status: run.status, startedAt: run.startedAt, summaries: summaries(run),
          episodes: run.episodes.length, plannedEpisodes: run.plannedEpisodes };
      }));
    } else if (request.method === 'GET' && /^\/api\/results\/[\w.-]+(?:\/report)?$/.test(path)) {
      const id = path.split('/')[3];
      if (!resultIds().includes(id)) { json(response, 404, { error: 'Unknown run' }); return; }
      if (path.endsWith('/report')) {
        const file = resolve(ROOT, 'results', id, 'REPORT.zh-CN.md');
        if (!existsSync(file)) { json(response, 404, { error: 'Report not ready' }); return; }
        response.writeHead(200, { 'Content-Type': 'text/markdown; charset=utf-8',
          'Content-Disposition': 'attachment; filename="CARE-mini-v1-report.md"' });
        response.end(readFileSync(file));
      } else json(response, 200, JSON.parse(readFileSync(resolve(ROOT, 'results', id, 'run.json'), 'utf8')));
    } else if (request.method === 'GET' && /^\/api\/results\/[\w.-]+\/observations\/[a-f0-9]{64}\.png$/.test(path)) {
      const segments = path.split('/');
      if (!resultIds().includes(segments[3])) { json(response, 404, { error: 'Unknown run' }); return; }
      const file = resolve(ROOT, 'results', segments[3], 'observations', segments[5]);
      if (!existsSync(file)) { json(response, 404, { error: 'Missing frame' }); return; }
      response.writeHead(200, { 'Content-Type': 'image/png', 'X-Content-Type-Options': 'nosniff' });
      response.end(readFileSync(file));
    } else if (request.method === 'POST' && path === '/api/pilot') {
      const data = await body(request);
      if (data.confirmPaid !== true || !keyPresent) {
        json(response, 400, { error: 'Paid confirmation and server-side API key required' }); return;
      }
      if (progress.status === 'running' || existsSync(resolve(ROOT, '.runtime/pilot.lock'))) {
        json(response, 409, { error: 'A pilot is already running' }); return;
      }
      if (!Array.isArray(data.models) || !data.models.length || data.models.length > 2
        || new Set(data.models).size !== data.models.length
        || data.models.some((id: string) => !MODELS.some(m => m.id === id))) {
        json(response, 400, { error: 'Select one or two allowlisted models' }); return;
      }
      if (budgetSummary().blocked) { json(response, 409, { error: 'Unsettled charge; reconcile first' }); return; }
      progress = { status: 'running', completed: 0, total: data.models.length * 6 };
      void runPilot(render, data.models, value => { progress = value; }).catch(error => {
        progress = { ...progress, status: 'error', error: error.message };
      });
      json(response, 202, progress);
    } else json(response, 404, { error: 'Not found' });
  } catch (error) {
    json(response, 400, { error: error instanceof Error ? error.message : 'Request failed' });
  }
});

const startPort = Number(process.env.BENCHMARK_PORT ?? 5174);
for (let port = startPort; port < startPort + 20; port++) {
  try {
    await new Promise<void>((resolve, reject) => {
      const onError = (e: Error) => reject(e);
      server.once('error', onError);
      server.listen(port, '127.0.0.1', () => { server.off('error', onError); resolve(); });
    });
    url = `http://127.0.0.1:${port}`;
    break;
  } catch (e) {
    if ((e as NodeJS.ErrnoException).code !== 'EADDRINUSE') throw e;
  }
}
if (!url) throw new Error('No free benchmark port');
render = new RenderService(url);
atomicJson(resolve(ROOT, '.runtime/server.json'), { url, pid: process.pid });
console.log(`Brick Atlas Benchmark: ${url} (OpenRouter configured: ${keyPresent})`);
async function close() {
  await render.close();
  await vite.close();
  server.close();
  process.exit(0);
}
process.once('SIGINT', () => void close());
process.once('SIGTERM', () => void close());
