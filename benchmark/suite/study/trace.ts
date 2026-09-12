import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import type { CaseTrace } from '../trace-types';
import { submissionTrace } from '../v2/trace';
import { getSpec } from '../v2/cases';
import { SYSTEM } from '../storage';
import { STUDY } from './protocol';
import type { StudyRow } from './results';
import { parseJSON } from '../score';

export function apiTrace(runId: string, caseIndex: number): CaseTrace {
  const run = JSON.parse(readFileSync(resolve(STUDY, 'runs', runId, 'run.json'), 'utf8'));
  const row = run.rows[caseIndex] as StudyRow;
  if (!row) throw new Error('Unknown study case');
  const frames = (row.images ?? []).map(file => `/api/study/images/${file.slice(7)}`);
  const trace = submissionTrace(runId, row.model ?? run.model, false,
    { spec: getSpec(row.caseId), answer: row.answer, missing: false }, frames);
  trace.caseIndex = caseIndex;
  trace.mode = row.arm ?? 'one-shot';
  trace.input = row.input;
  trace.modelInput = { system: SYSTEM, user: JSON.stringify(row.input) };
  trace.events[0].payload = trace.modelInput;
  const response = trace.events.find(e => e.kind === 'response')!;
  response.title = '模型原始 API 响应';
  response.payload = row.call;
  response.cost = row.call.cost;
  response.callIndex = row.reusedFirstCall ? 1 : 0;
  trace.evidence.responseCount = row.reusedFirstCall ? 2 : 1;
  trace.evidence.cost = row.call.cost;
  trace.evidence.reusedFirstResponse = !!row.reusedFirstCall;
  trace.evidence.note = 'Real recorded API receipt; geometry playback is derived, not hidden model reasoning. Reused first answers incur no new charge.';
  if (row.reusedFirstCall) {
    const first = submissionTrace(runId, row.model ?? run.model, false, {
      spec: getSpec(row.caseId), answer: parseJSON(row.reusedFirstCall.content), missing: false,
    }, frames);
    const firstResponse = first.events.find(e => e.kind === 'response')!;
    firstResponse.payload = { ...row.reusedFirstCall, reusedHistoricalReceipt: true };
    firstResponse.title = '复用原始首答（历史收据，不重复收费）';
    firstResponse.callIndex = 0;
    Object.assign(trace.states, first.states);
    const before = first.events.at(-1)!.after, after = trace.events[0].before;
    const bridge = { ...trace.events[0], actor: 'harness' as const, kind: 'feedback' as const,
      title: row.arm === 'reflection' ? '无新增信息的反思指令' : '目标盲合法性反馈',
      payload: row.feedback, provenance: 'recorded' as const, before, after, callIndex: 1 };
    trace.events = [...first.events, bridge, ...trace.events.slice(1)].map((e, id) => ({ ...e, id }));
  }
  return trace;
}
