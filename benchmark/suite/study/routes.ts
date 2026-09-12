import type http from 'node:http';
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { STUDY } from './protocol';
import { studyRuns, summarize } from './results';
import { apiTrace } from './trace';
import { localStatus } from './local-status';
import { localEvidenceRuns, localInferenceTrace } from './local-evidence';

export function handleStudy(url: URL, req: http.IncomingMessage, res: http.ServerResponse,
  json: (res: http.ServerResponse, status: number, data: unknown) => void) {
  const path = url.pathname;
  if (!path.startsWith('/api/study/')) return false;
  if (req.method !== 'GET') { json(res, 405, { error: 'Read-only' }); return true; }
  if (path === '/api/study/training') {
    json(res, 200, localStatus());
  } else if (path === '/api/study/runs') {
    json(res, 200, studyRuns().map(run => ({ id: run.id, status: run.status, error: run.error,
      completed: run.rows.length, expected: run.selection?.length ?? run.protocol.cases.length * 2,
      rows: summarize(run), cost: run.campaignAfter - run.campaignBefore }))
      .concat(localEvidenceRuns().map(run => ({ id: run.id, status: run.status, error: null,
        completed: run.completed, expected: run.expected, rows: summarize(run), cost: 0 }))));
  } else if (/^\/api\/study\/runs\/[\w.-]+\/cases$/.test(path)) {
    const run = [...studyRuns(), ...localEvidenceRuns()].find(r => r.id === path.split('/')[4]);
    if (!run) throw new Error('Unknown run');
    const page = Number(url.searchParams.get('page') ?? 0);
    if (!Number.isInteger(page) || page < 0) throw new Error('Invalid page');
    json(res, 200, { total: run.rows.length, items: run.rows.slice(page * 30, page * 30 + 30)
      .map((r: any, i: number) => ({ index: page * 30 + i, caseId: r.caseId, model: r.model ?? run.model,
        arm: r.arm ?? 'one-shot', verdict: r.verdict })) });
  } else if (/^\/api\/study\/runs\/[\w.-]+\/cases\/\d+\/trace$/.test(path)) {
    const id = path.split('/')[4], index = Number(path.split('/')[6]);
    const trace = id.startsWith('local-') ? localInferenceTrace(id, index) : apiTrace(id, index);
    if (url.searchParams.get('format') === 'jsonl') {
      const { events, ...manifest } = trace;
      res.writeHead(200, { 'Content-Type': 'application/x-ndjson', 'Content-Disposition': 'attachment; filename="study-trace.jsonl"' });
      res.end([JSON.stringify({ type: 'manifest', ...manifest }), ...events.map(e => JSON.stringify({ type: 'event', ...e }))].join('\n') + '\n');
    } else json(res, 200, trace);
  } else if (/^\/api\/study\/images\/[a-f0-9]{64}\.png$/.test(path)) {
    const file = resolve(STUDY, 'inputs/images', path.split('/').at(-1)!);
    if (!existsSync(file)) throw new Error('Missing image');
    res.writeHead(200, { 'Content-Type': 'image/png' }); res.end(readFileSync(file));
  } else json(res, 404, { error: 'Unknown study endpoint' });
  return true;
}
