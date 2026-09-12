import { submissionTrace } from '../v2/trace';
import { getSpec, taskForV2, type CaseSpec } from '../v2/cases';
import { evaluateStrict, EVALUATOR_VERSION } from './strict-evaluate';

export function strictTrace(runId: string, model: string, row: { spec: CaseSpec; answer: unknown; missing: boolean }, images: string[]) {
  const verdict = evaluateStrict(taskForV2(getSpec(row.spec.id)), row.answer);
  const trace = submissionTrace(runId, model, false, { ...row, answer: verdict.metrics.format ? row.answer : null }, images);
  trace.verdict = verdict;
  const response = trace.events.find(e => e.kind === 'response')!;
  response.payload = { answer: row.answer, missing: row.missing, evaluatorVersion: EVALUATOR_VERSION };
  trace.events.filter(e => e.kind === 'score').forEach(e => { e.payload = verdict; });
  trace.evidence.note += ` Strict evaluator ${EVALUATOR_VERSION}; rejected schemas are not unfolded.`;
  return trace;
}
