import type { CaseTrace, TraceEvent } from '../trace-types';
import type { Part } from '../shared';
import { decode, insertIssue, removeIssue } from '../geometry';
import { digest } from '../data';
import { SYSTEM } from '../storage';
import { differences } from '../traces';
import { taskForV2, type CaseSpec } from './cases';
import { evaluate } from './evaluate';

export function submissionTrace(runId: string, model: string, baseline: boolean,
  row: { spec: CaseSpec; answer: unknown; missing: boolean }, frames: string[]): CaseTrace {
  const task = taskForV2(row.spec), verdict = evaluate(task, row.answer);
  const disassemble = row.spec.kind === 'plan' && row.spec.variant === 'disassemble';
  const source = task.source?.parts ?? (row.spec.kind === 'relations' || disassemble ? task.target.parts : []);
  const reference = disassemble ? [] : task.target.parts;
  const trace: CaseTrace = {
    version: 'trace-v1', runId, caseIndex: 0, taskId: row.spec.id, model, kind: row.spec.kind,
    mode: baseline ? 'public-algorithm' : 'external-submission', input: task.public, frames,
    modelInput: { system: SYSTEM, user: JSON.stringify(task.public) }, source, reference, output: [], states: {}, events: [],
    differences: [], verdict, evidence: { scoreMatches: true, responseCount: 0, cost: 0, reusedFirstResponse: false,
      outputMeaning: row.spec.kind === 'plan' ? 'executed-plan' : row.spec.kind === 'relations' ? 'context-only'
        : row.spec.kind === 'parts' ? 'part-choice' : 'submitted-structure',
      referenceIsExample: row.spec.kind === 'generate' || row.spec.condition === 'ordinary',
      note: 'Recorded external submission or deterministic baseline. No provider response, token usage, latency or API receipt supplied. Cost is not measured; zero new API calls during offline replay.' } };
  let current = structuredClone(source);
  const state = (parts: Part[]) => { const hash = digest(parts); trace.states[hash] = structuredClone(parts); return hash; };
  const add = (actor: TraceEvent['actor'], kind: TraceEvent['kind'], title: string, payload: unknown, after = current) => {
    trace.events.push({ id: trace.events.length, actor, kind, title, payload, before: state(current), after: state(after),
      timestamp: null, callIndex: null, cost: 0, provenance: kind === 'response' ? 'recorded' : 'derived',
      visibility: kind === 'input' ? 'model-input' : 'posthoc' });
    current = structuredClone(after);
  };
  add('harness', 'input', '固定题目输入', trace.modelInput);
  add(baseline ? 'harness' : 'model', 'response', baseline ? '公开输入算法输出（非神经模型）' : '外部提交（未提供API调用日志）',
    { answer: row.answer, missing: row.missing, provenance: trace.evidence.note });
  if (row.spec.kind === 'plan') {
    const order = row.answer && typeof row.answer === 'object' && 'order' in row.answer ? row.answer.order : null;
    add('harness', 'decode', '按提交顺序执行，不重排', order, disassemble ? task.target.parts : []);
    const seen = new Set<string>();
    if (Array.isArray(order)) for (const id of order.slice(0, 128)) {
      const p = task.target.parts.find(p => p.id === id);
      const issue = !p || seen.has(id) ? 'unknown_or_duplicate_id'
        : disassemble ? removeIssue(current, id) : insertIssue(current, p);
      if (issue) { add('environment', 'reject', '非法计划步骤', { id, issue }); break; }
      seen.add(id); add('environment', 'execute', disassemble ? '移除' : '放置', { id },
        disassemble ? current.filter(p => p.id !== id) : [...current, p!]);
    }
  } else if (['relations', 'parts'].includes(row.spec.kind)) {
    add('harness', 'decode', '字段答案；场景为题目上下文', row.answer);
  } else {
    const raw = row.spec.kind === 'repair' && row.answer && typeof row.answer === 'object' && 'structure' in row.answer
      ? row.answer.structure : row.answer;
    const decoded = decode(raw);
    add('harness', 'decode', '结构集合展开，不是装配动作', row.answer, []);
    for (const p of decoded?.parts ?? []) add('harness', 'unfold', '展示提交零件', p, [...current, p]);
  }
  add('evaluator', 'score', '逐项指标与失败诊断', verdict);
  trace.output = current;
  trace.differences = ['parts', 'relations'].includes(row.spec.kind) || verdict.metrics.success === 1 && trace.evidence.referenceIsExample
    ? [] : differences(reference, current);
  return trace;
}
