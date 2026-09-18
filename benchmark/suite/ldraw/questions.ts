import { createHash } from 'node:crypto';
import type { AtlasManifest, PartInstance } from '../../../src/model/types';
import type { Action, Layer } from '../../../src/benchmark/types';
import { numberedPart, type LDrawAudit, type LDrawTask } from '../../../src/benchmark/ldrawTypes';

const digest = (s: string) => createHash('sha256').update(s).digest('hex');
const order = <T>(items: T[], key: string) => [...items].sort((a, b) =>
  digest(key + JSON.stringify(a)).localeCompare(digest(key + JSON.stringify(b))));
const center = (p: PartInstance) => p.bounds.min.map((n, k) => (n + p.bounds.max[k]) / 2);
export function generateQuestions(manifest: AtlasManifest, audit: LDrawAudit, difficulty: string) {
  const parts = manifest.instances, modelId = manifest.model.id;
  const byId = new Map(parts.map(p => [p.instanceId, p]));
  const label = (id: string) => numberedPart(byId.get(id)!).label;
  const sampleCount = Math.min(5, 2 + Math.floor(parts.length / 400));
  const selected = order(parts, modelId).slice(0, sampleCount);
  const tasks: LDrawTask[] = [], counters: Record<string, number> = {};
  function base(family: string, layer: Layer, title: string, question: string, promptEn: string,
    refs: string[], modality: LDrawTask['modality'], input: Record<string, unknown>, evidenceDetail: string): LDrawTask {
    const serial = counters[family] = (counters[family] ?? 0) + 1;
    return {
      id: `ld1-${modelId}-${family}-${serial}`, modelId, difficulty, layer, family, title,
      question, promptEn, modality, references: [...new Set(refs)].map(id => ({ id, label: label(id) })),
      capabilities: [family], format: 'single-choice', input, answer: {}, targetModule: refs[0] ?? '',
      evidence: 'model-state', evidenceDetail,
    };
  }
  function choice(task: LDrawTask, values: Array<{ label: string; value: unknown }>, correct: unknown) {
    const shuffled = order(values, task.id);
    task.options = shuffled.map((v, i) => ({ id: String.fromCharCode(65 + i), ...v }));
    task.answer = { choiceId: task.options.find(o => JSON.stringify(o.value) === JSON.stringify(correct))!.id };
    tasks.push(task);
  }
  const numbers = (n: number) => [...new Set([n, Math.max(0, n - 1), n + 1, n + 2])].map(value => ({ label: String(value), value }));
  for (const p of selected) {
    const id = p.instanceId, name = label(id);
    const colors = [...new Map(parts.map(x => [x.colorCode, x.colorName])).entries()];
    const alternatives = order(colors.filter(([code]) => code !== p.colorCode), id).slice(0, 3);
    if (alternatives.length) choice(base('color', 'atomic', `颜色识别 · ${name}`,
      `查看原模型中 ${name} 的颜色。可按编号隔离查看。`, `Identify the original color of ${name}; numbered isolation is allowed.`,
      [id], 'visual', {}, `Source color code: ${p.colorCode}.`),
    [[p.colorCode, p.colorName], ...alternatives].map(([value, label]) => ({ value, label })), p.colorCode);

    const same = order(parts.filter(x => x.instanceId !== id && x.partNumber === p.partNumber), id)[0];
    const different = order(parts.filter(x => x.partNumber !== p.partNumber), id).slice(0, 3);
    if (same && different.length >= 2) {
      const candidates = [same, ...different];
      choice(base('shape-match', 'atomic', `同型零件 · ${name}`,
        `忽略颜色与朝向，哪个编号与 ${name} 使用同一个 LDraw 零件型号？`,
        `Ignoring color and pose, which numbered instance has the same LDraw part type as ${name}?`,
        [id, ...candidates.map(x => x.instanceId)], 'visual', {}, `Part type: ${p.partNumber}.`),
      candidates.map(x => ({ label: label(x.instanceId), value: x.instanceId })), same.instanceId);
    }
    const nearby = order(parts.filter(x => x.instanceId !== id), id + 'position').slice(0, 3);
    if (nearby.length === 3) {
      const candidates = nearby.map(x => x.instanceId);
      const coords = Object.fromEntries([p, ...nearby].map(x => [label(x.instanceId), center(x).map(n => +n.toFixed(6))]));
      const distances = nearby.map(x => ({ id: x.instanceId, d: Math.hypot(...center(x).map((v, k) => v - center(p)[k])) }))
        .sort((a, b) => a.d - b.d);
      if (distances[1].d - distances[0].d > .01) choice(base('distance', 'atomic', `三维距离 · ${name}`,
        `使用输入中的几何包围盒中心坐标，哪个编号距离 ${name} 最近？`,
        `Using the supplied geometry bounding-box centers, which candidate is nearest to ${name}?`,
        [id, ...candidates], 'source-data', { coordinateFrame: 'Viewer world, millimeters, Euclidean distance', centers: coords },
        'Centers come from the rendered source meshes; these are not mass centers.'),
      nearby.map(x => ({ label: label(x.instanceId), value: x.instanceId })), distances[0].id);
    }
  }

  const adjacency = new Map(parts.map(p => [p.instanceId, new Set<string>()]));
  for (const e of audit.edges) { adjacency.get(e.a)!.add(e.b); adjacency.get(e.b)!.add(e.a); }
  const families = [...new Set(audit.edges.map(e => e.family))].sort();
  for (const family of families) {
    const e = order(audit.edges.filter(e => e.family === family), modelId)[0];
    choice(base('interface', 'metacognitive', `接口证据 · ${label(e.a)} / ${label(e.b)}`,
      `给定连接器审计记录，${label(e.a)} 与 ${label(e.b)} 的接口属于哪一类？这不表示已验证承载力。`,
      `Classify the supplied connector record for ${label(e.a)} and ${label(e.b)}. This does not certify load capacity.`,
      [e.a, e.b], 'connector-graph', { connectorRecord: { family: e.family, aConnector: e.aConnector, bConnector: e.bConnector },
        scope: audit.scope }, `BrickNet recognized ${family}; original source poses are unchanged.`),
    [...new Set([family, 'fixed', 'axle', 'hinge', 'ball'])].map(value => ({ label: value, value })), family);
  }
  const graphNodes = order(parts.filter(p => adjacency.get(p.instanceId)!.size >= 2 && adjacency.get(p.instanceId)!.size <= 6), modelId + 'graph')
    .slice(0, sampleCount);
  for (const p of graphNodes) {
    const id = p.instanceId, neighbors = [...adjacency.get(id)!];
    const distractors = order(parts.filter(p => p.instanceId !== id && !neighbors.includes(p.instanceId)), id).slice(0, 2).map(p => p.instanceId);
    const refs = [id, ...neighbors, ...distractors];
    const localEdges = audit.edges.filter(e => refs.includes(e.a) && refs.includes(e.b))
      .map(e => [label(e.a), label(e.b)]);
    const input = { edges: localEdges, graphMeaning: 'Undirected recognized connector pairs only; absence is not proof of physical separation.' };
    const task = base('neighbors', 'metacognitive', `连接邻居 · ${label(id)}`,
      `根据给定连接图，选出所有与 ${label(id)} 有直接接口证据的候选编号。`,
      `Select every candidate directly adjacent to ${label(id)} in the supplied connector graph.`,
      refs, 'connector-graph', input, 'Exact one-hop neighbors in the recognized graph.');
    task.format = 'multiple-choice';
    task.options = order([...neighbors, ...distractors], task.id).map((v, i) => ({ id: String.fromCharCode(65 + i), label: label(v), value: v }));
    task.answer = { choiceIds: task.options.filter(o => neighbors.includes(o.value)).map(o => o.id) };
    tasks.push(task);

    const countComponents = (removed: string | null) => {
      const nodes = refs.filter(v => v !== removed), seen = new Set<string>(); let count = 0;
      for (const v of nodes) {
        if (seen.has(v)) continue;
        count++; const queue = [v]; seen.add(v);
        while (queue.length) for (const w of adjacency.get(queue.shift()!)!) {
          if (nodes.includes(w) && !seen.has(w)) { seen.add(w); queue.push(w); }
        }
      }
      return count;
    };
    const count = countComponents(id);
    choice(base('graph-removal', 'integrative', `移除后的连接图 · ${label(id)}`,
      `仅在给定局部图中删除 ${label(id)} 及其关联边，剩余多少个连通分量？不推断实际可拔出性。`,
      `Delete ${label(id)} and its incident edges from this local graph. How many connected components remain? Do not infer physical extractability.`,
      refs, 'connector-graph', { ...input, nodes: refs.map(label) }, `Induced local graph after vertex deletion: ${count} components.`), numbers(count), count);
  }

  const unsupported = new Set(audit.unsupported.map(p => p.instanceId));
  const unknown = parts.find(p => unsupported.has(p.instanceId));
  if (unknown) {
    const known = order(parts.filter(p => !unsupported.has(p.instanceId)), modelId).slice(0, 3);
    const refs = [unknown, ...known].map(p => p.instanceId);
    choice(base('coverage', 'metacognitive', '连接覆盖边界',
      '根据审计覆盖记录，哪个编号没有连接器定义，不能据此认定它悬空？',
      'Which numbered instance lacks a connector definition in the coverage record, so this audit cannot establish that it is floating?',
      refs, 'source-data', { coverage: refs.map(id => ({ label: label(id), supported: !unsupported.has(id) })) },
      'Unsupported means unknown, not disconnected.'), refs.map(id => ({ label: label(id), value: id })), unknown.instanceId);
  }
  choice(base('evidence-limit', 'metacognitive', '力学结论边界',
    '当前提供源模型与连接器、网格交叠审计，但没有材料、摩擦、质量或动力学试验。能否得出该模型在重力下稳定的结论？',
    'Only source geometry, connector matching and mesh intersection audits are available. Without mass, friction, material or dynamic tests, is gravitational stability established?',
    [], 'source-data', { available: ['Original CAD', 'Connector inference', 'Inset-mesh intersection candidates'] },
    'No force or dynamics validation was performed.'),
  [{ label: 'Established', value: 'yes' }, { label: 'Not established by this evidence', value: 'unknown' }], 'unknown');

  if (manifest.instructions?.provenance === 'source') {
    const steps = manifest.instructions.steps;
    const sampled = order(steps.map((s, i) => ({ s, i })).filter(({ s }) => s.instanceIds.length > 0), modelId).slice(0, sampleCount);
    for (const { s, i } of sampled) {
      const id = s.instanceIds[0], other = steps.find((x, j) => j !== i && x.instanceIds.length)?.instanceIds[0];
      if (!other) continue;
      const refs = [id, other];
      const record = steps.map((s, j) => ({ index: j + 1, sourceFile: s.sourceFile, sourceStep: s.sourceStep,
        numbers: s.instanceIds.filter(id => refs.includes(id)).map(label) })).filter(s => s.numbers.length);
      choice(base('source-step', 'procedural', `作者步骤 · ${label(id)}`,
        `根据给定作者步骤表，${label(id)} 首次出现于第几个展开步骤？这是源文件顺序，不是碰撞自由装配证明。`,
        `At which expanded author step does ${label(id)} first appear in the supplied source-step table? Source order is not a collision-free assembly proof.`,
        refs, 'source-data', { steps: record, provenance: 'source' }, `Expanded source step ${i + 1}.`), numbers(i + 1), i + 1);
    }
    // Sequence validation uses existing author steps, never a synthetic support graph.
    const useful = steps.filter(s => s.instanceIds.length).slice(0, Math.min(6, steps.length));
    if (useful.length >= 3) {
      const ids = useful.flatMap(s => s.instanceIds);
      const task = base('source-sequence', 'procedural', '作者步骤序列',
        '在给定局部步骤窗口中，按作者顺序依次显示各步新增零件。动作只控制显示，不模拟插入轨迹。',
        'Reveal the supplied source-step window in author order. Actions change visibility only, without simulating insertion trajectories.',
        ids, 'scene-edit', {}, 'Preconditions encode the supplied source STEP order, not mechanical prerequisites.');
      const actions: Action[] = useful.map((_, i) => ({
        id: `step-${i + 1}`, label: `Source step ${i + 1}`,
        requires: [i ? `done-${i}` : 'start'], forbids: [`done-${i + 1}`],
        adds: [`done-${i + 1}`], deletes: [], cost: 1,
      }));
      task.format = 'actions';
      task.input = { initialFacts: ['start'], initialModules: [], goalFacts: [`done-${useful.length}`],
        absentFacts: [], budget: useful.length, actions: order(actions, task.id),
        sourceWindow: useful.map((s, i) => ({ actionId: `step-${i + 1}`, instanceIds: s.instanceIds, labels: s.instanceIds.map(label) })),
        editMode: 'source-window' };
      task.answer = { actionIds: actions.map(a => a.id) }; tasks.push(task);
    }
  }
  // A scene restoration task is deliberately an editor operation, not a claim
  // that an arbitrary part can be inserted while every neighbor stays fixed.
  for (const p of selected.slice(0, 3)) {
    const target = p.instanceId, distractor = parts.find(x => x.instanceId !== target)!.instanceId;
    const task = base('restore-instance', 'procedural', `补全实例 · ${label(target)}`,
      `展示副本暂时隐藏了 ${label(target)}。仅恢复这个编号，保持其余实例可见；所有位置沿用源文件。`,
      `The display copy hides ${label(target)}. Restore only that numbered instance, preserving all other instances and source poses.`,
      [target, distractor], 'scene-edit', {}, 'Visibility restoration at the original pose; no insertion feasibility is asserted.');
    const actions: Action[] = [target, distractor].map(id => ({
      id: `restore-${label(id)}`, label: `Restore ${label(id)}`, requires: [`missing-${id}`],
      adds: [`present-${id}`], deletes: [`missing-${id}`], cost: 1, visual: { moduleId: id, visible: true },
    }));
    task.format = 'actions';
    task.input = { initialFacts: [`missing-${target}`, `present-${distractor}`], initialModules: parts.filter(p => p.instanceId !== target).map(p => p.instanceId),
      goalFacts: [`present-${target}`, `present-${distractor}`], absentFacts: [`missing-${target}`], budget: 1,
      actions: order(actions, task.id), editMode: 'visibility', missingInstanceIds: [target] };
    task.answer = { actionIds: [`restore-${label(target)}`] }; tasks.push(task);
  }
  for (const task of tasks) if (task.modality === 'visual') task.visualInput = {
    numberedView: `benchmark/ldraw/inputs/views/${task.id}.png`,
    isolationAllowed: true,
  };
  return tasks;
}
