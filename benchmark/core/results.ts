import type { Action, EpisodeScore, Fault, Observation, Protocol } from '../shared/types';
import type { CallResult } from './openrouter';
import type { Ledger } from './budget';

export interface TraceStep {
  index: number;
  context: 'inspector' | 'builder';
  observation: Observation;
  image: string;
  action: Action | null;
  response: CallResult;
  feedback: string;
}
export interface EpisodeResult {
  id: string;
  model: string;
  taskId: string;
  seed: number;
  variant: number;
  fault: Fault;
  protocol: Protocol;
  status: 'complete' | 'error';
  error?: string;
  score: EpisodeScore;
  trace: TraceStep[];
  finalImage: string;
}
export interface RunResult {
  version: 'care-mini-v1';
  id: string;
  startedAt: string;
  completedAt: string | null;
  status: 'running' | 'complete' | 'error';
  error?: string;
  split: 'public-pilot';
  observation: 'RGB+visible-part-identities';
  actionSpace: 'grid-edits+ordered-batches';
  models: string[];
  plannedEpisodes: number;
  pricing: unknown;
  protocolHash: string;
  taskHash: string;
  sourceHash: string;
  sourceFiles: Record<string, string>;
  episodes: EpisodeResult[];
  ledger: Ledger;
}

export function wilson(success: number, n: number): [number, number] | null {
  if (!n) return null;
  const z = 1.959964, p = success / n, d = 1 + z * z / n;
  const mid = (p + z * z / (2 * n)) / d;
  const radius = z * Math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d;
  return [Math.max(0, mid - radius), Math.min(1, mid + radius)];
}
export function summaries(run: RunResult) {
  return run.models.flatMap(model => (['active', 'passive'] as const).map(protocol => {
    const all = run.episodes.filter(e => e.model === model && e.protocol === protocol);
    const episodes = all.filter(e => e.status === 'complete');
    const n = episodes.length;
    const avg = (fn: (e: EpisodeResult) => number) => n ? episodes.reduce((s, e) => s + fn(e), 0) / n : null;
    const successes = episodes.filter(e => e.score.lifecycleSuccess).length;
    const eligible = episodes.filter(e => e.score.recoverySuccess !== null);
    return {
      model, protocol, n, errors: all.length - n,
      successes, successRate: n ? successes / n : null, ci95: wilson(successes, n),
      anatomyF1: avg(e => e.score.anatomy.partF1),
      edgeF1: avg(e => e.score.construction.edgeF1),
      finalF1: avg(e => e.score.construction.partF1),
      blueprintExecutable: avg(e => Number(e.score.blueprintExecutable)),
      recoverySuccesses: eligible.filter(e => e.score.recoverySuccess).length,
      recoveryEligible: eligible.length,
      invalidActions: episodes.reduce((s, e) => s + e.score.invalidActions, 0),
      averageActions: avg(e => e.score.actions),
      calls: all.reduce((s, e) => s + e.trace.length, 0),
      cost: all.reduce((s, e) => s + e.trace.reduce((v, t) => v + t.response.cost, 0), 0),
    };
  }));
}
