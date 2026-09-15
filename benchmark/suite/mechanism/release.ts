import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { evaluateMechanismTask } from './evaluate';
import { mechanismModels } from './models';
import { mechanismTasks, MECHANISM_VERSION } from './tasks';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '../../..');
const rapierPackage = JSON.parse(readFileSync(resolve(root,
  'node_modules/@dimforge/rapier3d-compat/package.json'), 'utf8'));
export const OUTPUT = resolve(root, 'benchmark/mechanism-v1');
const hash = (data: string | Uint8Array) => createHash('sha256').update(data).digest('hex');
const write = (name: string, value: unknown) =>
  writeFileSync(resolve(OUTPUT, name), JSON.stringify(value, null, 2) + '\n');

export async function releaseMechanism() {
  mkdirSync(OUTPUT, { recursive: true });
  const models = mechanismModels();
  const tasks = await mechanismTasks();
  const publicRows = tasks.map(({ oracle, ...task }) => task);
  const oracleRows = tasks.map(task => ({ id: task.id, sourceGroup: task.sourceGroup,
    kind: task.kind, oracle: task.oracle }));
  const algorithmRows = tasks.map(task => {
    const answer = task.kind === 'active-inspection'
      ? { queryId: (task.oracle.queryIds as string[])[0] } : task.oracle;
    return { id: task.id, kind: task.kind,
      method: task.kind === 'active-inspection' ? 'finite-world-information-gain'
        : task.kind === 'multiobjective-design' || task.kind === 'inventory-substitution'
          ? 'constraint-enumerator' : 'Rapier-3D-oracle',
      result: evaluateMechanismTask(task, answer) };
  });
  assert.ok(algorithmRows.every(row => row.result.success === 1));
  const kinds = [...new Set(tasks.map(task => task.kind))];
  const byKind = Object.fromEntries(kinds.map(kind => [kind, tasks.filter(task => task.kind === kind).length]));
  const audit = {
    version: MECHANISM_VERSION,
    status: 'public-development-not-confirmatory',
    originalDesigns: models.length,
    tasks: tasks.length,
    byKind,
    visualParts: models.reduce((sum, model) => sum + model.parts.length, 0),
    visualPartsByModel: Object.fromEntries(models.map(model => [model.id, model.parts.length])),
    modules: models.reduce((sum, model) => sum + model.modules.length, 0),
    joints: models.reduce((sum, model) => sum + model.joints.length, 0),
    jointTypes: Object.fromEntries(['fixed', 'revolute', 'prismatic', 'spring'].map(type =>
      [type, models.flatMap(model => model.joints).filter(joint => joint.type === type).length])),
    shapeTypes: [...new Set(models.flatMap(model => model.parts.map(part => part.shape)))].sort(),
    physicsEngine: { name: '@dimforge/rapier3d-compat', version: rapierPackage.version,
      license: rapierPackage.license, timestepHz: 120, solverIterations: 12, internalPgsIterations: 2 },
    claimBoundary: [
      'Rigid-body dynamics and shape casts are simulator evidence, not calibrated LEGO clutch-force measurements.',
      'Slope and arch collision shapes use conservative cuboid envelopes.',
      'The six authored sources are public development objects, not an independent hidden confirmation set.',
      'Model scores must be reported by task family and source group; no pooled pseudo-replicated significance.',
    ],
  };
  const protocol = {
    version: MECHANISM_VERSION,
    frozenBeforeModelRuns: true,
    primaryEndpoint: 'exact structured answer per task family',
    taskFamilies: byKind,
    outputContracts: {
      'prefix-dynamics': '{validPlanId,invalidPlanFirstFailure}',
      'insertion-access': '{accessiblePathIds}',
      'fault-recovery': '{faultJointId,actions}',
      'inventory-substitution': '{alternativeId}',
      'dynamic-robustness': '{maxSafeImpulse}',
      'functional-kinematics': '{jointId,reachesTarget}',
      'active-inspection': '{queryId}',
      'multiobjective-design': '{paretoIds}',
    },
    reporting: [
      'Keep raw model, tool-assisted model, deterministic algorithm and physics oracle separate.',
      'Retain missing, malformed, truncated and unknown-ID failures in denominators.',
      'Group all eight tasks from one object into one source cluster.',
      'Do not call simulator thresholds real LEGO material or robot guarantees.',
    ],
  };
  write('models.json', models);
  write('public.json', publicRows);
  write('oracle-private.json', oracleRows);
  write('algorithm-results.json', algorithmRows);
  write('audit.json', audit);
  write('frozen-protocol.json', protocol);
  const files = ['README.md', 'models.json', 'public.json', 'oracle-private.json',
    'algorithm-results.json', 'audit.json', 'frozen-protocol.json',
    ...['render-audit.json', 'index.html', 'CASEBOOK.zh-CN.md', 'MODEL_REPORT.zh-CN.md',
      'ALL_MODELS.png', 'ALL_MODELS.pdf', 'TASK_MATRIX.png', 'TASK_MATRIX.pdf',
      'results/local-qwen3-0.6b.json', 'results/local-qwen3-0.6b.predictions.json',
      'results/local-qwen3-0.6b.scores.json', 'results/latest.json']
      .filter(name => existsSync(resolve(OUTPUT, name)))];
  const latest = existsSync(resolve(OUTPUT, 'results/latest.json'))
    ? JSON.parse(readFileSync(resolve(OUTPUT, 'results/latest.json'), 'utf8')) : null;
  if (latest?.path && existsSync(resolve(OUTPUT, 'results', latest.path))) {
    files.push(`results/${latest.path}`);
    const report = `results/${latest.path.replace('/run.json', '/REPORT.zh-CN.md')}`;
    if (existsSync(resolve(OUTPUT, report))) files.push(report);
    const reconciliation = `results/${latest.path.replace('/run.json', '/reconciliation.json')}`;
    if (existsSync(resolve(OUTPUT, reconciliation))) files.push(reconciliation);
  }
  const sourcePaths = ['types.ts', 'models.ts', 'physics.ts', 'tasks.ts', 'evaluate.ts',
    'score.ts', 'release.ts', 'render.ts', 'compose.ts', 'compose.py', 'run.ts', 'run_local.py'];
  write('manifest.json', {
    version: MECHANISM_VERSION,
    files: Object.fromEntries(files.map(name => [name, hash(readFileSync(resolve(OUTPUT, name)))])),
    sources: Object.fromEntries(sourcePaths.map(name => [name, hash(readFileSync(resolve(here, name)))])),
    rendererSource: hash(readFileSync(resolve(here, '../web/mechanism-render.ts'))),
  });
  console.log(JSON.stringify(audit));
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(fileURLToPath(import.meta.url))) {
  await releaseMechanism();
}
