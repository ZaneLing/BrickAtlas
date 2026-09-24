import type { MechanismModel } from '../../benchmark/suite/mechanism/types';
export type BenchModel = MechanismModel & { difficulty: string; family: string; lineage: string };
export type Layer = 'atomic' | 'metacognitive' | 'procedural' | 'integrative';
export interface Action {
  id: string;
  label: string;
  requires: string[];
  forbids?: string[];
  adds: string[];
  deletes: string[];
  cost: number;
  visual?: { moduleId: string; visible?: boolean; color?: string };
}
export interface Task {
  id: string;
  modelId: string;
  difficulty: string;
  layer: Layer;
  family: string;
  title: string;
  question: string;
  capabilities: string[];
  format: 'single-choice' | 'multiple-choice' | 'actions' | 'schedule' | 'policy';
  input: Record<string, any>;
  options?: Array<{ id: string; label: string; value: any }>;
  answer: Record<string, any>;
  targetModule: string;
  evidence: 'model-state' | 'support-graph' | 'Rapier' | 'finite-world' | 'state-machine' | 'resource-schedule';
}
export interface ReplayFrame {
  step: number; actionId: string | null; accepted: boolean; issue: string | null;
  facts: string[]; activeModules: string[]; colors: Record<string, string>; cost: number;
}
