import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { isDeepStrictEqual } from 'node:util';
import { atomicJson } from '../core/budget';
import { CATALOG, COLORS, type Part } from './shared';
import { decode, dims, insertIssue, key, removeIssue } from './geometry';
import { digest, models } from './data';
import { taskFor } from './tasks';
import { legalityFeedback, parseJSON, score } from './score';
import { ARTIFACTS, SYSTEM, listRuns, type SuiteRun } from './storage';
import type { CaseTrace, PartDifference, TraceEvent } from './trace-types';
import { RESEARCH_VERSION, researchModels } from './research/dataset';
import { researchTaskFor, researchScore, type Condition } from './research/tasks';
import { PAIRED_VERSION, type PairedRun } from './research/paired';

export function differences(expected: Part[], actual: Part[]): PartDifference[] {
  const remaining = [...actual], unmatched: Part[] = [];
  for (const p of expected) {
    const index = remaining.findIndex(q => key(q) === key(p));
    if (index >= 0) remaining.splice(index, 1); else unmatched.push(p);
  }
  const result: PartDifference[] = [];
  for (const p of unmatched) {
    const samePosition = remaining.findIndex(q => q.partId === p.partId
      && q.x === p.x && q.y === p.y && q.z === p.z
      && dims(q).w === dims(p).w && dims(q).d === dims(p).d);
    if (samePosition >= 0) {
      result.push({ kind: 'color', expectedId: p.id, actualId: remaining.splice(samePosition, 1)[0].id });
      continue;
    }
    // Only label nearby unmatched same-type pieces as pose errors; other cases remain unmatched.
    const nearby = remaining.map((q, index) => ({ q, index,
      distance: Math.abs(q.x - p.x) + Math.abs(q.y - p.y) + Math.abs(q.z - p.z) }))
      .filter(({ q, distance }) => q.partId === p.partId && q.color === p.color && distance <= 2)
      .sort((a, b) => a.distance - b.distance)[0];
    if (nearby) result.push({ kind: 'pose', expectedId: p.id, actualId: remaining.splice(nearby.index, 1)[0].id });
    else result.push({ kind: 'missing', expectedId: p.id, actualId: null });
  }
  result.push(...remaining.map(p => ({ kind: 'extra' as const, expectedId: null, actualId: p.id })));
  return result;
}

export function buildTrace(run: SuiteRun | PairedRun, caseIndex: number): CaseTrace {
  const row = run.results[caseIndex];
  if (!row || !Number.isInteger(caseIndex)) throw new Error('Unknown case');
  const paired = run.version === PAIRED_VERSION;
  const research = run.version === RESEARCH_VERSION || paired;
  const model = (research ? researchModels() : models()).find(m => m.id === row.modelId);
  if (!model) throw new Error('Dataset version unavailable');
  const condition = (run as SuiteRun & { cases?: { taskId: string; condition: Condition }[] }).cases?.find(c => c.taskId === row.taskId)?.condition ?? 'ordinary';
  const task = research ? researchTaskFor(researchModels().find(m => m.id === row.modelId)!, row.kind, condition)
    : taskFor(model, row.kind, row.representation);
  const evaluate = (answer: unknown) => research ? researchScore(task as ReturnType<typeof researchTaskFor>, answer) : score(task, answer);
  if (!isDeepStrictEqual(task.public, row.input)) throw new Error('Task version differs from recorded input');
  const disassembly = row.kind === 'plan' && row.input.input.direction === 'disassemble';
  const source = task.source?.parts ?? decode(task.public.input.reference)?.parts
    ?? (row.kind === 'relations' || disassembly ? task.target.parts : []);
  const reference = row.kind === 'parts' ? task.frames[0].parts : disassembly ? [] : task.target.parts;
  const trace: CaseTrace = {
    version: 'trace-v1', runId: run.id, caseIndex, taskId: row.taskId, model: row.model,
    kind: row.kind, mode: row.mode, input: row.input, frames: row.frames,
    modelInput: { system: SYSTEM, user: JSON.stringify(run.version === 'local-text-training-v1'
      ? { prompt: row.input.prompt, input: row.input.input, responseSchema: row.input.responseSchema, imageTitles: [] }
      : row.input) },
    source, reference, output: [], states: {}, events: [], differences: [], verdict: row.verdict,
    evidence: {
      scoreMatches: false, responseCount: row.calls.length,
      cost: row.calls.reduce((n, c, i) => n + (paired && i === 0 ? 0 : c.cost), 0),
      reusedFirstResponse: paired,
      outputMeaning: row.kind === 'plan' ? 'executed-plan' : row.kind === 'parts' ? 'part-choice'
        : row.kind === 'relations' ? 'context-only' : 'submitted-structure',
      referenceIsExample: row.kind === 'generate' || typeof row.verdict.metrics.visibleSurfaceSuccess === 'number',
      note: 'Historical replay. Responses are recorded; decoding, feedback reconstruction and geometry playback are derived. No internal thoughts or historical timestamps were recorded. Collection unfolding is not a model assembly plan. Difference labels beyond exact matches are diagnostic, not the scorer.',
    },
  };
  const state = (parts: Part[]) => {
    const id = digest(parts); trace.states[id] = structuredClone(parts); return id;
  };
  let current: Part[] = structuredClone(source);
  const add = (actor: TraceEvent['actor'], kind: TraceEvent['kind'], title: string, payload: unknown,
    after = current, callIndex: number | null = null, cost = 0, provenance: TraceEvent['provenance'] = 'derived') => {
    const beforeHash = state(current), afterHash = state(after);
    trace.events.push({ id: trace.events.length, actor, kind, title, payload,
      before: beforeHash, after: afterHash, timestamp: null, callIndex, cost, provenance,
      visibility: kind === 'input' || kind === 'feedback' ? 'model-input' : 'posthoc' });
    current = structuredClone(after);
  };
  add('harness', 'input', '固定模型输入', { messages: trace.modelInput, framePaths: row.frames,
    note: 'User serialization reconstructed from frozen runner; local Python JSON escapes Unicode. Same semantic payload.' }, current, null, 0, 'derived');
  for (const [callIndex, call] of row.calls.entries()) {
    if (callIndex > 0) add('harness', 'feedback',
      paired ? (run.mode === 'paired-reflection' ? '无新增信息的反思指令' : '目标盲合法性反馈') : '固定合法性反馈（由历史版本重建）',
      paired ? (row as PairedRun['results'][number]).refinementPrompt : legalityFeedback(row.answers[callIndex - 1]),
      current, callIndex, 0, paired ? 'recorded' : 'derived');
    add('model', 'response', `模型响应 ${callIndex + 1}`, {
      raw: call.content, generationId: call.id, provider: call.provider,
      tokens: { input: call.provider.startsWith('local ') ? null : call.promptTokens, output: call.completionTokens }, latencyMs: call.latencyMs,
      billing: paired && callIndex === 0 ? 'Historical first response reused; no new charge.' : call.provider.startsWith('local ') ? 'No API bill; local compute is not free. Prompt token count was not recorded.' : 'OpenRouter usage receipt',
      originalReceiptCost: call.cost,
      finishReason: call.finishReason,
    }, current, callIndex, paired && callIndex === 0 ? 0 : call.cost, 'recorded');
    const answer = parseJSON(call.content);
    if (!isDeepStrictEqual(answer, row.answers[callIndex])) throw new Error('Recorded parsed answer differs from response');
    if (row.kind === 'plan') {
      const assemble = row.input.input.direction === 'assemble';
      const initial = assemble ? [] : structuredClone(task.target.parts);
      add('harness', 'decode', '按原始计划执行；不重新排序', answer, initial, callIndex);
      const order = answer && typeof answer === 'object' && 'order' in answer ? answer.order : null;
      const seen = new Set<string>();
      if (Array.isArray(order) && order.length <= 64) for (const id of order) {
        const p = typeof id === 'string' ? task.target.parts.find(p => p.id === id) : undefined;
        const issue = !p || seen.has(String(id)) ? 'unknown_or_duplicate_id'
          : assemble ? insertIssue(current, p) : removeIssue(current, p.id);
        if (issue) {
          add('environment', 'reject', '原计划在此被拒绝', { id, issue, direction: assemble ? 'assemble' : 'disassemble' }, current, callIndex);
          break;
        }
        const next = assemble ? [...current, p!] : current.filter(q => q.id !== id);
        seen.add(String(id));
        add('environment', 'execute', assemble ? '执行计划：放置' : '执行计划：移除', { id }, next, callIndex);
      } else add('harness', 'error', '计划无法解析', answer, current, callIndex);
    } else if (row.kind === 'parts') {
      const a = answer as { partId?: string; color?: string } | null;
      const parts: Part[] = a && a.partId && a.color && Object.hasOwn(CATALOG, a.partId) && Object.hasOwn(COLORS, a.color)
        ? [{ ...reference[0], partId: a.partId, color: a.color as Part['color'], id: 'predicted' }] : [];
      add('harness', 'decode', '将型号选择转换为候选零件', answer, parts, callIndex);
    } else if (row.kind === 'relations') {
      add('harness', 'decode', '关系答案；场景仅为题目上下文', answer, source, callIndex);
    } else {
      const raw = row.kind === 'repair' && answer && typeof answer === 'object' && 'structure' in answer ? answer.structure : answer;
      const program = decode(raw);
      add('harness', 'decode', program ? '结构集合展开，不代表装配计划' : '结构无法解析', answer, [], callIndex);
      if (program) for (const p of program.parts) add('harness', 'unfold', '展示输出集合中的零件', p, [...current, p], callIndex);
    }
    const verdict = evaluate(answer);
    add('evaluator', 'score', `第 ${callIndex + 1} 次输出的事后评分`, verdict, current, callIndex);
  }
  trace.output = structuredClone(current);
  if (row.status === 'error') add('harness', 'error', '运行错误', row.error ?? 'Unknown error');
  const recomputed = evaluate(row.answers.at(-1));
  trace.evidence.scoreMatches = isDeepStrictEqual(recomputed, row.verdict);
  if (row.status === 'complete' && !trace.evidence.scoreMatches) throw new Error('Scoring version mismatch');
  trace.differences = row.kind === 'relations' || (row.verdict.metrics.success === 1
    && (row.kind === 'generate' || row.verdict.metrics.visibleSurfaceSuccess === 1)) ? [] : differences(reference, trace.output);
  return trace;
}

export function migrateTraces() {
  const dir = resolve(ARTIFACTS, 'traces'); mkdirSync(dir, { recursive: true });
  const rows = [];
  for (const run of listRuns()) for (let index = 0; index < run.results.length; index++) {
    const trace = buildTrace(run, index), filename = `${run.id}-${index}.json`;
    atomicJson(resolve(dir, filename), trace);
    rows.push({ runId: run.id, caseIndex: index, taskId: trace.taskId, model: trace.model, kind: trace.kind,
      events: trace.events.length, responses: trace.evidence.responseCount, scoreMatches: trace.evidence.scoreMatches,
      file: filename, sha256: digest(trace) });
  }
  const report = { version: 'trace-v1', cases: rows.length, events: rows.reduce((n, r) => n + r.events, 0),
    calls: rows.reduce((n, r) => n + r.responses, 0), paidRequests: 0, allScoresMatch: rows.every(r => r.scoreMatches), rows };
  atomicJson(resolve(dir, 'index.json'), report);
  return report;
}
