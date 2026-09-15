import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { mechanismTasks } from '../mechanism/tasks';
import { evaluateHierarchyTask } from './evaluate';
import { hierarchyModels } from './models';
import { hierarchyTasks, HIERARCHY_VERSION, pilotSelection } from './tasks';
import { ATOMIC_OPERATIONS, DIFFICULTIES, META_FAMILIES, TASK_LAYERS } from './types';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '../../..');
export const OUTPUT = resolve(root, 'benchmark/hierarchy-v1');
const hash = (data: string | Uint8Array) => createHash('sha256').update(data).digest('hex');
const write = (name: string, value: unknown) =>
  writeFileSync(resolve(OUTPUT, name), JSON.stringify(value, null, 2) + '\n');

function shortcutAnswer(task: ReturnType<typeof hierarchyTasks>[number]) {
  if (task.format === 'single-choice') return { choiceId: 'A' };
  if (task.format === 'multiple-choice') return { choiceIds: ['A'] };
  if (task.format === 'ordered-actions') {
    return { actionIds: [...(task.oracle.actionIds as string[])].reverse() };
  }
  return { planId: 'P1', verificationId: 'visual-only' };
}

export async function releaseHierarchy() {
  mkdirSync(OUTPUT, { recursive: true });
  const models = hierarchyModels(), tasks = hierarchyTasks();
  const mechanismExtension = await mechanismTasks();
  const publicRows = tasks.map(({ oracle, ...task }) => task);
  const oracleRows = tasks.map(task => ({
    id: task.id,
    sourceGroup: task.sourceGroup,
    difficulty: task.difficulty,
    layer: task.layer,
    oracle: task.oracle,
    oracleMethod: task.oracleMethod,
  }));
  const algorithmRows = tasks.map(task => ({
    id: task.id,
    oracle: evaluateHierarchyTask(task, task.oracle),
    firstChoiceOrReverse: evaluateHierarchyTask(task, shortcutAnswer(task)),
  }));
  assert.ok(algorithmRows.every(row => row.oracle.success === 1));
  const byDifficulty = Object.fromEntries(DIFFICULTIES.map(difficulty => [
    difficulty.id,
    {
      models: models.filter(model => model.difficulty === difficulty.id).length,
      questions: tasks.filter(task => task.difficulty === difficulty.id).length,
      visibleParts: models.filter(model => model.difficulty === difficulty.id)
        .reduce((sum, model) => sum + model.parts.length, 0),
    },
  ]));
  const byLayer = Object.fromEntries(TASK_LAYERS.map(layer => [
    layer.id,
    tasks.filter(task => task.layer === layer.id).length,
  ]));
  const byFormat = Object.fromEntries([...new Set(tasks.map(task => task.format))].map(format => [
    format,
    tasks.filter(task => task.format === format).length,
  ]));
  const audit = {
    version: HIERARCHY_VERSION,
    status: 'public-development-pilot',
    originalModels: models.length,
    coreQuestions: tasks.length,
    mechanismExtensionQuestions: mechanismExtension.length,
    totalUniqueQuestions: tasks.length + mechanismExtension.length,
    byDifficulty,
    byLayer,
    byFormat,
    atomicOperationCoverage: ATOMIC_OPERATIONS,
    metacognitiveFamilyCoverage: META_FAMILIES,
    visualParts: models.reduce((sum, model) => sum + model.parts.length, 0),
    modules: models.reduce((sum, model) => sum + model.modules.length, 0),
    joints: models.reduce((sum, model) => sum + model.joints.length, 0),
    pilotCases: pilotSelection(tasks).length,
    sourcePolicy: {
      originalGeometryOnly: true,
      omrLdrawRole: 'visual-complexity reference only',
      mechanism1Role: 'D3 library and 48-question advanced extension',
    },
    claimBoundary: [
      'The four difficulty levels are authored development strata, not yet human-calibrated psychometric bands.',
      'Rapier evidence is rigid-body simulation, not calibrated LEGO clutch-force or material deformation.',
      'The 16-case OpenRouter pilot validates the pipeline and heatmap schema; it is not a model ranking.',
      'A future confirmatory release must add hidden source-disjoint objects and human difficulty measurements.',
    ],
  };
  const protocol = {
    version: HIERARCHY_VERSION,
    frozenBeforePilot: true,
    difficulties: DIFFICULTIES,
    taskLayers: TASK_LAYERS,
    coreDesign: 'two atomic questions plus one metacognitive, procedural, and integrative question per object',
    primaryEndpoint: 'exact success reported by difficulty and task layer',
    clustering: 'all questions from one object form one source cluster',
    pilotSelection: pilotSelection(tasks).map(task => task.id),
    reporting: [
      'Never pool task variants as independent source objects.',
      'Retain malformed, missing, and unknown-ID answers in the denominator.',
      'Report the 90-question hierarchy core separately from the 48-question D3 extension.',
      'Report low-cost pilot cells as pipeline evidence with their small denominators.',
    ],
  };
  write('models.json', models);
  write('public.json', publicRows);
  write('oracle-private.json', oracleRows);
  write('algorithm-results.json', algorithmRows);
  write('audit.json', audit);
  write('frozen-protocol.json', protocol);
  const files = new Set([
    'README.md',
    'models.json',
    'public.json',
    'oracle-private.json',
    'algorithm-results.json',
    'audit.json',
    'frozen-protocol.json',
    'render-audit.json',
    'index.html',
    'QUESTION_BANK.zh-CN.md',
    'HIERARCHY_REPORT.zh-CN.md',
    'LIBRARY_OVERVIEW.png',
    'LIBRARY_OVERVIEW.pdf',
    'TASK_ABILITY_MATRIX.png',
    'TASK_ABILITY_MATRIX.pdf',
    'PILOT_HEATMAP.png',
    'PILOT_HEATMAP.pdf',
    'results/latest.json',
  ].filter(name => existsSync(resolve(OUTPUT, name))));
  const resultsRoot = resolve(OUTPUT, 'results');
  if (existsSync(resultsRoot)) {
    for (const entry of readdirSync(resultsRoot, { withFileTypes: true }).filter(entry => entry.isDirectory())) {
      for (const name of ['run.json', 'ledger.json', 'reconciliation.json', 'REPORT.zh-CN.md']) {
        const relative = `results/${entry.name}/${name}`;
        if (existsSync(resolve(OUTPUT, relative))) files.add(relative);
      }
    }
  }
  const latest = existsSync(resolve(OUTPUT, 'results/latest.json'))
    ? JSON.parse(readFileSync(resolve(OUTPUT, 'results/latest.json'), 'utf8')) : null;
  if (latest?.path && existsSync(resolve(OUTPUT, 'results', latest.path))) {
    files.add(`results/${latest.path}`);
    const report = `results/${latest.path.replace('/run.json', '/REPORT.zh-CN.md')}`;
    if (existsSync(resolve(OUTPUT, report))) files.add(report);
    const ledger = `results/${latest.path.replace('/run.json', '/ledger.json')}`;
    if (existsSync(resolve(OUTPUT, ledger))) files.add(ledger);
  }
  const sourcePaths = ['types.ts', 'models.ts', 'tasks.ts', 'evaluate.ts', 'score.ts',
    'release.ts', 'render.ts', 'compose.ts', 'compose.py', 'run.ts'];
  write('manifest.json', {
    version: HIERARCHY_VERSION,
    files: Object.fromEntries([...files].map(name => [name, hash(readFileSync(resolve(OUTPUT, name)))])),
    sources: Object.fromEntries(sourcePaths.filter(name => existsSync(resolve(here, name)))
      .map(name => [name, hash(readFileSync(resolve(here, name)))])),
    sharedRenderer: hash(readFileSync(resolve(here, '../web/mechanism-render.ts'))),
    mechanismExtension: {
      version: 'brickatlas-mechanism-1',
      questions: mechanismExtension.length,
      publicSha256: hash(readFileSync(resolve(root, 'benchmark/mechanism-v1/public.json'))),
    },
  });
  console.log(JSON.stringify(audit));
  return audit;
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(fileURLToPath(import.meta.url))) {
  await releaseHierarchy();
}
