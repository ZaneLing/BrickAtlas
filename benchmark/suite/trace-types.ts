import type { Kind, Part, PublicTask, Verdict } from './shared';

export type TraceActor = 'model' | 'harness' | 'environment' | 'evaluator';
export interface TraceEvent {
  id: number;
  actor: TraceActor;
  kind: 'input' | 'response' | 'decode' | 'feedback' | 'unfold' | 'execute' | 'reject' | 'score' | 'error';
  provenance: 'recorded' | 'derived';
  timestamp: null;
  callIndex: number | null;
  title: string;
  payload: unknown;
  before: string;
  after: string;
  cost: number;
  visibility: 'model-input' | 'posthoc';
}
export interface PartDifference {
  kind: 'missing' | 'extra' | 'color' | 'pose';
  expectedId: string | null;
  actualId: string | null;
}
export interface CaseTrace {
  version: 'trace-v1';
  runId: string;
  caseIndex: number;
  taskId: string;
  model: string;
  kind: Kind;
  mode: string;
  input: PublicTask;
  modelInput: { system: string; user: string };
  frames: string[];
  source: Part[];
  reference: Part[];
  output: Part[];
  states: Record<string, Part[]>;
  events: TraceEvent[];
  differences: PartDifference[];
  verdict: Verdict;
  evidence: {
    scoreMatches: boolean;
    responseCount: number;
    cost: number;
    reusedFirstResponse: boolean;
    outputMeaning: 'submitted-structure' | 'executed-plan' | 'part-choice' | 'context-only';
    referenceIsExample: boolean;
    note: string;
  };
}
