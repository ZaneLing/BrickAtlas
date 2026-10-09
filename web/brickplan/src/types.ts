export type Bi = { zh: string; en: string };
export type Action = { type: string; partId?: string; siteId?: string; view?: string; avoidableError?: boolean; answer?: Record<string, number | null> };
export type Raster = { url?: string; base64?: string; mime: string; width: number; height: number };
export type Images = Record<string, Raster>;
export type Observation = {
  taskId: string; sessionId: string; revision: number; view: string; track: string;
  attempts: number; actionBudget: number; remainingActions: number; remainingViews: number; remainingDiagnoses: number;
  terminated: boolean; termination: string | null;
  rack: { capacity: number; occupiedHolders: number; rule: string };
  partIds: string[]; siteIds: string[]; registration: { partId: string; siteId: string }[];
  workOrders: { partId: string; completed: boolean; operation: string }[];
  inspectionHistory: { frameId: string; atRevision: number; view: string; images?: Images }[];
  images?: Images; completion: string; identityRule: string; fixture: string; diagnosisQuestion: string;
};
export type Question = { id: string; stableId: string; category: string; form: string; kind: string; source: string; profile: string; split: string; tier: string; lengthBin: string };
export type Family = { id: string; number: string; name: Bi; question: Bi; given: Bi; answer: Bi; score: Bi; count: number };
export type Catalogue = { questions: Question[]; taxonomy: Family[]; counts: { episodes: number; probes: number; pairs: number; sources: number }; lengthNotice: Bi };
export type Preview = {
  id: string; kind: string; observation: Observation; question: string; revision?: number; answered?: boolean;
  candidates?: Action[]; proposedPlan?: Action[];
  repairContext?: { checkpointObservation: Observation; executedHistory: Action[]; lagAfterError: number; rule: string };
};
export type Frame = { assembly: number; done: number };
export type SceneData = {
  scope: string; parts: { partNumber: string; colorHex: string; rawMatrix: number[][] }[];
  mutable: number[]; fixed: number[]; meshes: Record<string, Record<string, number[]>>;
  partIds: Record<string, string>; siteIds: Record<string, string>; fixedIds: Record<string, string>;
  goal: number; revision: number; frames: Frame[]; current: Frame; grayscale: boolean;
};
export type Event = { revision: number; attempt: number; action: Action; code: string };
export type Score = { success: boolean; operations: number; optimal: number; regret: number | null; [key: string]: unknown };
export type Step = {
  index: number; status: string; input: { observation: Observation; prompt: string; imageOrder: string[] };
  rawOutput?: string; explanation?: string; parseError?: string; action?: Action; feedback?: { code: string; revision?: number };
  after?: Observation; usage?: { inputTokens?: number; outputTokens?: number }; latencySeconds?: number;
};
export type ModelRun = {
  id: string; taskId: string; model: string; status: string; steps: Step[]; maxCalls: number; provider: string;
  initialObservation: Observation; finalObservation?: Observation; score?: Score; stopReason?: string; scope: string; systemPrompt: string;
};
export type Models = {
  providers: { id: string; name: string; available: boolean; cost: string }[];
  runs: { id: string; taskId: string; model: string; status: string }[];
  cases: { id: string; title: string }[];
};
export type TaskInfo = { study: boolean; track: string; tasks: { id: string; sessions: string[]; tier?: string; profile?: string }[] };
