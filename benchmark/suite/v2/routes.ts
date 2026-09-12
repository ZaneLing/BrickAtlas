import type http from 'node:http';
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import type { SuiteRenderer } from '../render';
import { ARTIFACTS, BENCHMARK } from '../storage';
import { caseSpecs, getSpec, taskForV2 } from './cases';
import { groundTruth } from './ground-truth';
import { evaluateStrict, EVALUATOR_VERSION } from '../study/strict-evaluate';
import { strictTrace } from '../study/strict-trace';
import { DIRECTORY } from './build';
import { POLICIES } from './dataset';
import { jsonLines } from './verify';
import { submissionTrace } from './trace';
import { isDeepStrictEqual } from 'node:util';

interface Context {
  json: (res: http.ServerResponse, status: number, value: unknown) => void;
  body: (req: http.IncomingMessage) => Promise<any>;
  renderer: SuiteRenderer;
}
export async function handleV2(url: URL, req: http.IncomingMessage, res: http.ServerResponse, ctx: Context) {
  const path = url.pathname;
  if (!path.startsWith('/api/v2/')) return false;
  const { json, body, renderer } = ctx;
  if (req.method === 'GET' && path === '/api/v2/manifest') {
    const manifest = JSON.parse(readFileSync(resolve(DIRECTORY, 'manifest.json'), 'utf8'));
    json(res, 200, { ...manifest, policyNames: POLICIES });
  } else if (req.method === 'GET' && path === '/api/v2/cases') {
    const params = url.searchParams, page = Number(params.get('page') ?? 0);
    if (!Number.isInteger(page) || page < 0) throw new Error('Invalid page');
    const filtered = caseSpecs().filter(s => ['kind', 'condition', 'split', 'policy', 'difficulty'].every(k =>
      !params.get(k) || params.get(k) === 'all' || params.get(k) === s[k as keyof typeof s]));
    json(res, 200, { total: filtered.length, page, pageSize: 30, items: filtered.slice(page * 30, page * 30 + 30) });
  } else if (req.method === 'GET' && /^\/api\/v2\/cases\/[a-f0-9]{24}\/(input|truth)$/.test(path)) {
    const id = path.split('/')[4], task = taskForV2(getSpec(id));
    if (path.endsWith('/truth')) json(res, 200, groundTruth(task));
    else {
      const images = [], dir = resolve(BENCHMARK, '.runtime/casebank-frames');
      mkdirSync(dir, { recursive: true });
      for (const f of task.frames) {
        const rendered = await renderer.render(f), file = resolve(dir, rendered.hash + '.png');
        if (!existsSync(file)) writeFileSync(file, rendered.buffer);
        images.push(`/api/v2/frames/${rendered.hash}.png`);
      }
      json(res, 200, { ...task.public, images });
    }
  } else if (req.method === 'GET' && /^\/api\/v2\/frames\/[a-f0-9]{64}\.png$/.test(path)) {
    const file = resolve(BENCHMARK, '.runtime/casebank-frames', path.split('/').at(-1)!);
    if (!existsSync(file)) { json(res, 404, { error: 'Frame not rendered' }); return true; }
    res.writeHead(200, { 'Content-Type': 'image/png' }); res.end(readFileSync(file));
  } else if (req.method === 'POST' && path === '/api/v2/evaluate') {
    const b = await body(req);
    if (typeof b.caseId !== 'string') throw new Error('caseId required');
    json(res, 200, { ...evaluateStrict(taskForV2(getSpec(b.caseId)), b.answer), evaluatorVersion: EVALUATOR_VERSION });
  } else if (req.method === 'GET' && path === '/api/v2/evaluations') {
    const root = resolve(ARTIFACTS, 'evaluations-v2');
    const reports = existsSync(root) ? readdirSync(root).filter(n => /^[\w.-]+$/.test(n)).flatMap(n => {
      const file = resolve(root, n, 'summary.json');
      if (!existsSync(file)) return [];
      const r = JSON.parse(readFileSync(file, 'utf8'));
      return [{ id: r.id, model: r.model, baseline: r.baseline, cases: r.cases,
        evaluatorVersion: r.evaluatorVersion ?? 'legacy-v2',
        rows: r.rows.filter((g: { stratum: string }) => g.stratum.startsWith('task|')) }];
    }) : [];
    json(res, 200, reports);
  } else if (req.method === 'GET' && /^\/api\/v2\/evaluations\/[\w.-]+\/trace$/.test(path)) {
    const runId = path.split('/')[4], caseId = url.searchParams.get('caseId');
    const dir = resolve(ARTIFACTS, 'evaluations-v2', runId), summary = JSON.parse(readFileSync(resolve(dir, 'summary.json'), 'utf8'));
    if (summary.evaluatorVersion !== undefined && summary.evaluatorVersion !== EVALUATOR_VERSION) throw new Error('Unknown evaluator version');
    let found = false;
    for await (const row of jsonLines(resolve(dir, 'cases.jsonl.gz'))) if (row.spec.id === caseId) {
      const task = taskForV2(getSpec(caseId!)), images = [];
      const frameDir = resolve(BENCHMARK, '.runtime/casebank-frames'); mkdirSync(frameDir, { recursive: true });
      for (const f of task.frames) {
        const r = await renderer.render(f); writeFileSync(resolve(frameDir, r.hash + '.png'), r.buffer); images.push(`/api/v2/frames/${r.hash}.png`);
      }
      const trace = summary.evaluatorVersion === EVALUATOR_VERSION ? strictTrace(runId, summary.model, row, images)
        : submissionTrace(runId, summary.model, summary.baseline, row, images);
      if (!isDeepStrictEqual(trace.verdict, row.verdict)) throw new Error('Stored evaluation differs from replay');
      if (url.searchParams.get('format') === 'jsonl') {
        const { events, ...manifest } = trace;
        res.writeHead(200, { 'Content-Type': 'application/x-ndjson', 'Content-Disposition': 'attachment; filename="v2-trace.jsonl"' });
        res.end([JSON.stringify({ type: 'manifest', ...manifest }), ...events.map(e => JSON.stringify({ type: 'event', ...e }))].join('\n') + '\n');
      } else json(res, 200, trace);
      found = true; break;
    }
    if (!found) throw new Error('Case absent from evaluation');
  } else if (req.method === 'GET' && /^\/api\/v2\/evaluations\/[\w.-]+\/cases$/.test(path)) {
    const file = resolve(ARTIFACTS, 'evaluations-v2', path.split('/')[4], 'cases.jsonl.gz');
    if (!existsSync(file)) throw new Error('Unknown evaluation');
    const page = Number(url.searchParams.get('page') ?? 0), kind = url.searchParams.get('kind'), items = [];
    if (!Number.isInteger(page) || page < 0) throw new Error('Invalid page');
    let n = 0;
    for await (const row of jsonLines(file)) {
      if (kind && kind !== 'all' && row.spec.kind !== kind) continue;
      if (n >= page * 30 && n < page * 30 + 30) items.push(row); n++;
      if (n > page * 30 + 30) break;
    }
    json(res, 200, { page, hasNext: n > page * 30 + 30, items });
  } else if (req.method === 'GET' && /^\/api\/v2\/download\/[\w.-]+$/.test(path)) {
    const manifest = JSON.parse(readFileSync(resolve(DIRECTORY, 'manifest.json'), 'utf8'));
    const filename = path.split('/').at(-1)!;
    if (!manifest.shards.some((s: { filename: string }) => s.filename === filename)) throw new Error('Unknown artifact');
    res.writeHead(200, { 'Content-Type': 'application/gzip', 'Content-Disposition': `attachment; filename="${filename}"` });
    res.end(readFileSync(resolve(DIRECTORY, filename)));
  } else json(res, 404, { error: 'Unknown v2 endpoint' });
  return true;
}
