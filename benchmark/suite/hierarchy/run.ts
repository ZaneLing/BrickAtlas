import { closeSync, mkdirSync, openSync, readFileSync, unlinkSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve } from 'node:path';
import { Budget, atomicJson } from '../../core/budget';
import { completion, MODELS, modelPricing, type Message } from '../../core/openrouter';
import { parseJSON } from '../score';
import { evaluateHierarchyTask } from './evaluate';
import { OUTPUT } from './release';
import { HIERARCHY_VERSION, hierarchyTasks, pilotSelection } from './tasks';

const BENCHMARK = resolve(import.meta.dirname, '../..');
const sha256 = (path: string) => createHash('sha256').update(readFileSync(path)).digest('hex');
const SYSTEM = `You are solving a controlled hierarchical brick-assembly benchmark.
Use the supplied rendered image, options, and structured evidence.
Return exactly one JSON object matching responseSchema.
Do not include markdown, explanations, chain-of-thought, or extra fields.`;

export async function runHierarchyPilot(
  selectedModels: string[] = MODELS.map(model => model.id),
  resumeId?: string,
) {
  if (!process.env.OPENROUTER_API_KEY) process.loadEnvFile(resolve(BENCHMARK, '../.env'));
  const key = process.env.OPENROUTER_API_KEY;
  if (!key) throw new Error('OPENROUTER_API_KEY is not configured');
  if (!selectedModels.length || selectedModels.some(id => !MODELS.some(model => model.id === id))) {
    throw new Error('Invalid low-cost model allowlist');
  }
  const lock = resolve(BENCHMARK, '.runtime/pilot.lock');
  const file = openSync(lock, 'wx', 0o600);
  writeFileSync(file, `${process.pid}\n`);
  closeSync(file);
  try {
    const budget = new Budget(resolve(BENCHMARK, '.runtime/campaign-ledger.json'));
    if (budget.blocked) throw new Error('Unsettled prior charge');
    const allTasks = hierarchyTasks(), tasks = pilotSelection(allTasks);
    const id = resumeId ?? `${new Date().toISOString().replace(/[:.]/g, '-')}-hierarchy`;
    const directory = resolve(OUTPUT, 'results', id);
    mkdirSync(directory, { recursive: true });
    const run: any = resumeId
      ? JSON.parse(readFileSync(resolve(directory, 'run.json'), 'utf8'))
      : {
        id,
        version: HIERARCHY_VERSION,
        status: 'running',
        error: null,
        models: selectedModels,
        cases: tasks.map(task => task.id),
        settings: {
          temperature: 0,
          maxTokens: 2200,
          retries: 0,
          sample: 'one fixed task per difficulty × task-layer cell',
          requests: tasks.length * selectedModels.length,
          maximumNewSpend: 0.12,
          protocolSha256: sha256(resolve(OUTPUT, 'frozen-protocol.json')),
          publicSha256: sha256(resolve(OUTPUT, 'public.json')),
          renderAuditSha256: sha256(resolve(OUTPUT, 'render-audit.json')),
        },
        pricing: await modelPricing(),
        campaignBefore: budget.spent,
        campaignAfter: budget.spent,
        results: [],
        startedAt: new Date().toISOString(),
        completedAt: null,
      };
    if (resumeId && (
      run.version !== HIERARCHY_VERSION
      || JSON.stringify(run.models) !== JSON.stringify(selectedModels)
      || JSON.stringify(run.cases) !== JSON.stringify(tasks.map(task => task.id))
    )) throw new Error('Resume protocol drift');
    run.status = 'running';
    run.error = null;
    run.completedAt = null;
    const before = run.campaignBefore;
    const persist = () => {
      run.campaignAfter = budget.spent;
      atomicJson(resolve(directory, 'run.json'), run);
      atomicJson(resolve(directory, 'ledger.json'), budget.ledger);
    };
    persist();
    try {
      for (const task of tasks) for (const model of selectedModels) {
        if (run.results.some((row: any) => row.taskId === task.id && row.model === model)) continue;
        if (budget.spent - before > 0.12) throw new Error('Hierarchy pilot allocation reached');
        if (run.results.length) await new Promise(resolveDelay => setTimeout(resolveDelay, 1_250));
        const image = readFileSync(resolve(OUTPUT, task.visualization.detailImage));
        const publicTask = {
          version: HIERARCHY_VERSION,
          id: task.id,
          difficulty: task.difficulty,
          layer: task.layer,
          format: task.format,
          capability: task.capability,
          question: task.question,
          options: task.options,
          input: task.input,
          responseSchema: task.responseSchema,
        };
        const content: Exclude<Message['content'], string> = [
          { type: 'text', text: JSON.stringify(publicTask) },
          { type: 'image_url', image_url: { url: `data:image/png;base64,${image.toString('base64')}` } },
        ];
        const call = await completion(key, model, [
          { role: 'system', content: SYSTEM },
          { role: 'user', content },
        ], budget);
        const answer = parseJSON(call.content);
        const verdict = evaluateHierarchyTask(task, answer);
        run.results.push({
          taskId: task.id,
          sourceGroup: task.sourceGroup,
          difficulty: task.difficulty,
          layer: task.layer,
          format: task.format,
          model,
          input: publicTask,
          image: task.visualization.detailImage,
          answer,
          verdict,
          call,
        });
        persist();
        console.log(JSON.stringify({
          completed: run.results.length,
          total: tasks.length * selectedModels.length,
          model,
          task: task.id,
          success: verdict.success,
          spent: budget.spent,
        }));
      }
      run.status = 'complete';
    } catch (error) {
      run.status = 'error';
      run.error = (error as Error).message;
    }
    run.completedAt = new Date().toISOString();
    persist();
    writeReport(run, directory);
    atomicJson(resolve(OUTPUT, 'results/latest.json'), {
      runId: id,
      path: `${id}/run.json`,
      status: run.status,
    });
    return run;
  } finally {
    unlinkSync(lock);
  }
}

function writeReport(run: any, directory: string) {
  const cells = ['D1', 'D2', 'D3', 'D4'].flatMap(difficulty =>
    ['atomic', 'metacognitive', 'procedural', 'integrative'].map(layer => {
      const selected = run.results.filter((row: any) =>
        row.difficulty === difficulty && row.layer === layer);
      return {
        difficulty,
        layer,
        n: selected.length,
        success: selected.filter((row: any) => row.verdict.success).length,
      };
    }));
  const models = run.models.map((model: string) => {
    const selected = run.results.filter((row: any) => row.model === model);
    return { model, n: selected.length, success: selected.filter((row: any) => row.verdict.success).length };
  });
  const text = `# Hierarchy-1 低成本流程试跑

- 状态：${run.status}
- 错误：${run.error ?? '无'}
- 固定样本：16 题（每个难度 × 任务层一个）
- 请求：${run.results.length}
- 本轮费用：$${(run.campaignAfter - run.campaignBefore).toFixed(6)}
- 累计费用：$${run.campaignAfter.toFixed(6)} / $4.50

| 模型 | 完成 | Exact Success |
|---|---:|---:|
${models.map((row: { model: string; n: number; success: number }) =>
    `| ${row.model} | ${row.n} | ${row.success} |`).join('\n')}

| 难度 | 任务层 | 样本 | Exact Success |
|---|---|---:|---:|
${cells.map(row => `| ${row.difficulty} | ${row.layer} | ${row.n} | ${row.success} |`).join('\n')}

这是流程与可视化管线检查，不是模型排名。每个单模型单元格只有 1 题。
`;
  writeFileSync(resolve(directory, 'REPORT.zh-CN.md'), text);
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(import.meta.filename)) {
  const args = process.argv.slice(2);
  const resume = args.find(argument => argument.startsWith('--resume='));
  const models = args.filter(argument => !argument.startsWith('--resume='));
  const run = await runHierarchyPilot(models.length ? models : undefined, resume?.slice('--resume='.length));
  console.log(JSON.stringify({
    id: run.id,
    status: run.status,
    completed: run.results.length,
    error: run.error,
    campaignAfter: run.campaignAfter,
  }));
}
