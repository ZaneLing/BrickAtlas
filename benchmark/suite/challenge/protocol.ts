import { CHALLENGE_VERSION } from './models';
import { challengeTasks, type ChallengeKind } from './tasks';
import { RULES } from '../shared';
import { digest } from '../data';

export const METHOD_TRACKS = [
  { id: 'symbolic', methods: ['LLM', 'graph algorithm', 'tool-assisted solver'],
    tasks: ['support-counterfactual', 'compound-edit', 'graph-reasoning', 'module-transplant', 'step-selection', 'constrained-redesign'],
    information: 'public numeric geometry or constraints; no hidden target', status: 'implemented' },
  { id: 'disclosed-vision', methods: ['VLM', 'specialist reconstruction'],
    tasks: ['multi-fault-repair', 'distributed-completion', 'scene-reconstruction'],
    information: 'assembled plus all bottom-layer images; full-structure scoring', status: 'implemented' },
  { id: 'local-pose', methods: ['VLM', 'pose estimator'],
    tasks: ['pose-estimation'], information: 'reference images and current structure; yaw equivalence', status: 'implemented' },
  { id: 'open-loop-recovery', methods: ['LLM', 'search planner'],
    tasks: ['recovery-plan'], information: 'initial and target geometry; one action program, 256-action cap', status: 'implemented' },
  { id: 'inspection', methods: ['tool agent'],
    tasks: ['active-inspection'], information: 'one query, returned observation, final answer; cost separate', status: 'episode-api-implemented' },
  { id: 'robot-control', methods: ['OpenVLA', 'RT-2'],
    tasks: [], information: 'would need robot observations, embodiment, grasp/trajectory and force safety', status: 'not-implemented' },
] as const;

export function publicChallenge(task: ReturnType<typeof challengeTasks>[number]) {
  return { id: task.id, version: CHALLENGE_VERSION, kind: task.kind, rules: RULES,
    prompt: task.prompt, input: task.input, responseSchema: task.responseSchema,
    imageTitles: task.frames.map(f => f.title), maxActions: task.kind === 'recovery-plan' ? 256 : null };
}
export function challengeProtocol() {
  const tasks = challengeTasks();
  return { version: CHALLENGE_VERSION, status: 'public-development-not-confirmatory',
    selectionUsesModelOutcomes: false, modelResults: null, tracks: METHOD_TRACKS,
    cases: tasks.map(task => ({ id: task.id, group: task.model.id, kind: task.kind,
      inputHash: digest(publicChallenge(task)),
      track: METHOD_TRACKS.find(track => (track.tasks as readonly string[]).includes(task.kind as ChallengeKind))!.id })),
    reporting: { inferenceLatencyMs: null, renderLatencyMs: null, parseLatencyMs: null, inputTokens: null,
      outputTokens: null, billedUsd: null, peakDeviceMemoryBytes: null, repeats: null },
    rules: [
      'Same track, case IDs, image bytes, budgets and evaluator for every compared system.',
      'Report incompatible methods as unsupported, missing selected answers as failure.',
      'Do not remove images for text-only models and retain a visual score.',
      'Group intervals by source, not derived case. Repeats are paired, not new sources.',
      'Peak memory is unavailable for remote APIs; null is not zero.',
      'This is an openly reviewed development set; no pretraining-contamination guarantee.',
    ] };
}
