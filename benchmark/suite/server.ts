import http from 'node:http';
import { randomUUID } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createServer } from 'vite';
import { Budget, atomicJson } from '../core/budget';
import { MODELS } from '../core/openrouter';
import { models, summary } from './data';
import { taskFor } from './tasks';
import { score } from './score';
import { TASKS, type Kind } from './shared';
import { runSuite, type Progress } from './runner';
import { SuiteRenderer } from './render';
import { ARTIFACTS, BENCHMARK, SUITE, groupResults, listRuns } from './storage';

if (!process.env.OPENROUTER_API_KEY && existsSync(resolve(BENCHMARK, '../.env'))) process.loadEnvFile(resolve(BENCHMARK, '../.env'));
const token = randomUUID(), data = models();
let progress: Progress = { running: false, completed: 0, total: 0 }, url = '';
let renderer: SuiteRenderer;
const pictures = new Map<string, Buffer>();
const server = http.createServer();
const vite = await createServer({ configFile: resolve(SUITE, 'vite.config.ts'),
  appType: 'mpa', server: { middlewareMode: true, hmr: { server } } });
function json(res: http.ServerResponse, status: number, value: unknown) {
  res.writeHead(status, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' });
  res.end(JSON.stringify(value));
}
async function body(req: http.IncomingMessage) {
  const chunks: Buffer[] = []; let size = 0;
  for await (const chunk of req) { size += chunk.length; if (size > 96_000) throw new Error('Request too large'); chunks.push(chunk); }
  return JSON.parse(Buffer.concat(chunks).toString('utf8'));
}
server.on('request', async (req, res) => {
  try {
    const request = new URL(req.url ?? '/', 'http://localhost'), path = request.pathname;
    if (!['127.0.0.1', 'localhost'].includes((req.headers.host ?? '').split(':')[0])) { json(res, 403, { error: 'Host denied' }); return; }
    if (!path.startsWith('/api/')) { vite.middlewares(req, res, () => { res.writeHead(404); res.end('Not found'); }); return; }
    if (req.headers.origin && req.headers.origin !== url) { json(res, 403, { error: 'Origin denied' }); return; }
    if (req.method === 'POST' && req.headers['x-benchmark-client'] !== token) { json(res, 403, { error: 'Client token required' }); return; }
    if (path === '/api/status' && req.method === 'GET') {
      const ledgerFile = resolve(BENCHMARK, '.runtime/campaign-ledger.json');
      const ledger = existsSync(ledgerFile) ? JSON.parse(readFileSync(ledgerFile, 'utf8')) : { charges: [], cap: 4.5 };
      const spent = ledger.charges.reduce((n: number, c: { actual: number | null }) => n + (c.actual ?? 0), 0);
      json(res, 200, { title: 'BrickAtlas Multitask', token, models: MODELS, keyPresent: !!process.env.OPENROUTER_API_KEY,
        progress, locked: existsSync(resolve(BENCHMARK, '.runtime/pilot.lock')), budget: { cap: ledger.cap, spent,
          uncertain: ledger.charges.some((c: { status: string }) => c.status === 'uncertain') } });
    } else if (path === '/api/dataset' && req.method === 'GET') {
      json(res, 200, { summary: summary(), items: data.map(m => ({ id: m.id, group: m.group,
        family: m.family, split: m.split, parts: m.structure.parts.length, description: m.description })) });
    } else if (/^\/api\/models\/[a-f0-9]{20}$/.test(path) && req.method === 'GET') {
      const m = data.find(m => m.id === path.split('/').at(-1));
      if (!m) { json(res, 404, { error: 'Unknown model' }); return; }
      json(res, 200, m);
    } else if (path === '/api/task' && req.method === 'GET') {
      const m = data.find(m => m.id === request.searchParams.get('model'));
      const kind = request.searchParams.get('kind') as Kind;
      if (!m || !TASKS.includes(kind)) { json(res, 400, { error: 'Unknown model/task' }); return; }
      const t = taskFor(m, kind);
      const images = [];
      for (const f of t.frames) {
        const frame = await renderer.render(f);
        pictures.set(frame.hash, frame.buffer);
        while (pictures.size > 150) pictures.delete(pictures.keys().next().value!);
        images.push(`/api/frame/${frame.hash}.png`);
      }
      json(res, 200, { ...t.public, images });
    } else if (/^\/api\/frame\/[a-f0-9]{64}\.png$/.test(path) && req.method === 'GET') {
      const frame = pictures.get(path.split('/').at(-1)!.slice(0, -4));
      if (!frame) { json(res, 404, { error: 'Frame expired' }); return; }
      res.writeHead(200, { 'Content-Type': 'image/png' }); res.end(frame);
    } else if (path === '/api/submit' && req.method === 'POST') {
      const b = await body(req), m = data.find(m => m.id === b.modelId);
      if (!m || !TASKS.includes(b.kind)) { json(res, 400, { error: 'Unknown model/task' }); return; }
      json(res, 200, score(taskFor(m, b.kind), b.answer));
    } else if (path === '/api/runs' && req.method === 'GET') {
      json(res, 200, listRuns().map(r => ({ id: r.id, status: r.status, mode: r.mode,
        representation: r.representation, completed: r.results.length, rows: groupResults(r),
        cost: r.results.flatMap(x => x.calls).reduce((s, c) => s + c.cost, 0) })));
    } else if (/^\/api\/runs\/[\w.-]+(?:\/report|\/frames\/[a-f0-9]{64}\.png)?$/.test(path) && req.method === 'GET') {
      const id = path.split('/')[3], run = listRuns().find(r => r.id === id);
      if (!run) { json(res, 404, { error: 'Unknown run' }); return; }
      const dir = resolve(ARTIFACTS, 'runs', id);
      if (path.endsWith('/report')) {
        const file = resolve(dir, 'REPORT.md');
        if (!existsSync(file)) { json(res, 404, { error: 'Report pending' }); return; }
        res.writeHead(200, { 'Content-Type': 'text/markdown; charset=utf-8',
          'Content-Disposition': 'attachment; filename="BrickAtlas-multitask-report.md"' });
        res.end(readFileSync(file));
      } else if (path.includes('/frames/')) {
        const file = resolve(dir, 'frames', path.split('/').at(-1)!);
        if (!existsSync(file)) { json(res, 404, { error: 'Missing frame' }); return; }
        res.writeHead(200, { 'Content-Type': 'image/png' }); res.end(readFileSync(file));
      } else json(res, 200, run);
    } else if (path === '/api/run' && req.method === 'POST') {
      const b = await body(req);
      if (b.confirmPaid !== true) { json(res, 400, { error: 'Explicit paid confirmation required' }); return; }
      if (!Array.isArray(b.models) || !b.models.length || b.models.length > 2
        || new Set(b.models).size !== b.models.length || b.models.some((s: string) => !MODELS.some(m => m.id === s))
        || !['one-shot', 'validator-once'].includes(b.mode)) { json(res, 400, { error: 'Invalid run configuration' }); return; }
      if (!process.env.OPENROUTER_API_KEY) { json(res, 400, { error: 'Server-side API key missing' }); return; }
      if (progress.running || existsSync(resolve(BENCHMARK, '.runtime/pilot.lock'))) { json(res, 409, { error: 'Campaign busy' }); return; }
      if (new Budget(resolve(BENCHMARK, '.runtime/campaign-ledger.json')).blocked) { json(res, 409, { error: 'Unsettled charge' }); return; }
      progress = { running: true, completed: 0, total: b.models.length * 16 };
      void runSuite(renderer, { models: b.models, mode: b.mode }, p => { progress = p; })
        .catch(e => { progress = { ...progress, running: false, error: e.message }; });
      json(res, 202, progress);
    } else json(res, 404, { error: 'Not found' });
  } catch (e) { json(res, 400, { error: (e as Error).message }); }
});
for (let port = Number(process.env.SUITE_PORT ?? 5175); port < Number(process.env.SUITE_PORT ?? 5175) + 20; port++) {
  try {
    await new Promise<void>((ok, no) => {
      const fail = (e: Error) => no(e); server.once('error', fail);
      server.listen(port, '127.0.0.1', () => { server.off('error', fail); ok(); });
    });
    url = `http://127.0.0.1:${port}`; break;
  } catch (e) { if ((e as NodeJS.ErrnoException).code !== 'EADDRINUSE') throw e; }
}
if (!url) throw new Error('No free suite port');
renderer = new SuiteRenderer(url);
atomicJson(resolve(BENCHMARK, '.runtime/suite-server.json'), { url, pid: process.pid });
console.log(`BrickAtlas Multitask: ${url}`);
async function close() { await renderer.close(); await vite.close(); server.close(); process.exit(0); }
process.once('SIGTERM', () => void close()); process.once('SIGINT', () => void close());
