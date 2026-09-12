import http from 'node:http';
import { randomUUID } from 'node:crypto';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { createServer } from 'vite';
import { Budget, atomicJson } from '../core/budget';
import { MODELS } from '../core/openrouter';
import { digest, models, summary } from './data';
import { taskFor } from './tasks';
import { score } from './score';
import { CATALOG, TASKS, type Kind } from './shared';
import { runSuite, type Progress } from './runner';
import { SuiteRenderer } from './render';
import { ARTIFACTS, BENCHMARK, SUITE, groupResults, listRuns } from './storage';
import { buildTrace } from './traces';
import { RESEARCH_VERSION, researchModels } from './research/dataset';
import { researchTaskFor, researchScore, type Condition } from './research/tasks';
import { runResearch, researchSelection, groupResearch, type ResearchRun } from './research/run';
import { portConnections } from './research/connectors';
import { reviewQueue, reviewSummary, submitReview } from './research/review';
import { PAIRED_VERSION } from './research/paired';
import { trainingStatus } from './research/training-status';
import { handleV2 } from './v2/routes';
import { handleStudy } from './study/routes';

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
    if (handleStudy(request, req, res, json)) return;
    if (await handleV2(request, req, res, { json, body, renderer })) return;
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
    } else if (path === '/api/research/reviews' && req.method === 'GET') {
      json(res, 200, { summary: reviewSummary(), items: reviewQueue().map(m => ({ id: m.id, family: m.family, structure: m.structure })) });
    } else if (path === '/api/research/reviews' && req.method === 'POST') {
      const review = submitReview(await body(req));
      json(res, 200, { recorded: true, sampleId: review.sampleId });
    } else if (path === '/api/research/training' && req.method === 'GET') {
      json(res, 200, { jobs: trainingStatus() });
    } else if (path === '/api/research/dataset' && req.method === 'GET') {
      const records = researchModels(), families: Record<string, number> = {}, splits: Record<string, number> = {};
      for (const m of records) { families[m.family] = (families[m.family] ?? 0) + 1; splits[m.split] = (splits[m.split] ?? 0) + 1; }
      json(res, 200, { summary: { version: RESEARCH_VERSION, digest: digest(records), models: records.length, groups: records.length,
        tasks: records.length * 8, families, splits, catalogParts: Object.keys(CATALOG).length },
        items: records.map(m => ({ id: m.id, group: m.group, family: m.family, split: m.split,
          parts: m.structure.parts.length, description: m.description })) });
    } else if (/^\/api\/research\/models\/r[a-f0-9]{19}$/.test(path) && req.method === 'GET') {
      const m = researchModels().find(m => m.id === path.split('/').at(-1));
      if (!m) { json(res, 404, { error: 'Unknown research model' }); return; }
      let ports: unknown = null;
      try { ports = portConnections(m.structure.parts); } catch { /* Optional upstream catalog may not be installed. */ }
      json(res, 200, { ...m, ports, portsSource: 'BrickNet bundled MIT annotations; grid-domain audit only' });
    } else if (/^\/api\/models\/[a-f0-9]{20}$/.test(path) && req.method === 'GET') {
      const m = data.find(m => m.id === path.split('/').at(-1));
      if (!m) { json(res, 404, { error: 'Unknown model' }); return; }
      json(res, 200, m);
    } else if (['/api/task', '/api/research/task'].includes(path) && req.method === 'GET') {
      const research = path.startsWith('/api/research/');
      const m = (research ? researchModels() : data).find(m => m.id === request.searchParams.get('model'));
      const kind = request.searchParams.get('kind') as Kind;
      if (!m || !TASKS.includes(kind)) { json(res, 400, { error: 'Unknown model/task' }); return; }
      const condition = (request.searchParams.get('condition') ?? 'ordinary') as Condition;
      if (!['ordinary', 'layers', 'symbolic'].includes(condition)) { json(res, 400, { error: 'Unknown condition' }); return; }
      const t = research ? researchTaskFor(researchModels().find(r => r.id === m.id)!, kind, condition) : taskFor(m, kind);
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
      const b = await body(req), research = typeof b.modelId === 'string' && b.modelId.startsWith('r');
      const m = (research ? researchModels() : data).find(m => m.id === b.modelId);
      if (!m || !TASKS.includes(b.kind)) { json(res, 400, { error: 'Unknown model/task' }); return; }
      const condition = b.condition ?? 'ordinary';
      if (!['ordinary', 'layers', 'symbolic'].includes(condition)) { json(res, 400, { error: 'Unknown condition' }); return; }
      json(res, 200, research ? researchScore(researchTaskFor(researchModels().find(r => r.id === m.id)!, b.kind, condition), b.answer)
        : score(taskFor(m, b.kind), b.answer));
    } else if (path === '/api/runs' && req.method === 'GET') {
      json(res, 200, listRuns().map(r => ({ id: r.id, status: r.status, mode: r.mode,
        representation: r.representation, version: r.version, completed: r.results.length,
        rows: r.version === RESEARCH_VERSION || r.version === PAIRED_VERSION
          ? groupResearch(r as ResearchRun).map(g => ({ ...g, cost: r.results.filter(row => row.model === g.model
            && row.kind === g.kind && (r as ResearchRun).cases.find(c => c.taskId === row.taskId)?.condition === g.condition)
            .flatMap(row => r.version === PAIRED_VERSION ? row.calls.slice(1) : row.calls).reduce((s, c) => s + c.cost, 0) }))
          : groupResults(r),
        cost: r.results.flatMap(x => r.version === PAIRED_VERSION ? x.calls.slice(1) : x.calls).reduce((s, c) => s + c.cost, 0) })));
    } else if (/^\/api\/runs\/[\w.-]+\/cases\/\d+\/trace$/.test(path) && req.method === 'GET') {
      const [, , , id, , index] = path.split('/');
      const run = listRuns().find(r => r.id === id);
      if (!run || !run.results[Number(index)]) { json(res, 404, { error: 'Unknown run/case' }); return; }
      const trace = buildTrace(run, Number(index));
      if (request.searchParams.get('format') === 'jsonl') {
        const { events, ...manifest } = trace;
        res.writeHead(200, { 'Content-Type': 'application/x-ndjson',
          'Content-Disposition': 'attachment; filename="brickatlas-trace.jsonl"' });
        res.end([JSON.stringify({ type: 'manifest', ...manifest }),
          ...events.map(event => JSON.stringify({ type: 'event', ...event }))].join('\n') + '\n');
      } else json(res, 200, trace);
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
    } else if (path === '/api/research/run' && req.method === 'POST') {
      const b = await body(req);
      if (b.confirmPaid !== true) { json(res, 400, { error: 'Explicit paid confirmation required' }); return; }
      if (!Array.isArray(b.models) || !b.models.length || b.models.length > 2
        || new Set(b.models).size !== b.models.length || b.models.some((id: string) => !MODELS.some(m => m.id === id))) {
        json(res, 400, { error: 'Invalid model selection' }); return;
      }
      if (!process.env.OPENROUTER_API_KEY) { json(res, 400, { error: 'API key missing' }); return; }
      if (progress.running || existsSync(resolve(BENCHMARK, '.runtime/pilot.lock'))) { json(res, 409, { error: 'Campaign busy' }); return; }
      if (new Budget(resolve(BENCHMARK, '.runtime/campaign-ledger.json')).blocked) { json(res, 409, { error: 'Unsettled charge' }); return; }
      progress = { running: true, completed: 0, total: researchSelection().length * b.models.length };
      void runResearch(renderer, p => { progress = { running: true, ...p }; }, b.models)
        .then(run => { progress = { ...progress, completed: run.results.length, running: false, error: run.error }; })
        .catch(e => { progress = { ...progress, running: false, error: e.message }; });
      json(res, 202, progress);
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
