import { closeSync, mkdirSync, openSync, readFileSync, unlinkSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { Budget, atomicJson } from '../../core/budget';
import { completion, MODELS, modelPricing, type Message } from '../../core/openrouter';
import { parseJSON } from '../score';
import { evaluateMechanismTask } from './evaluate';
import { mechanismTasks, MECHANISM_VERSION } from './tasks';
import { OUTPUT } from './release';

const BENCHMARK = resolve(import.meta.dirname, '../..');
const SYSTEM = `You are solving a controlled brick-assembly benchmark.
Use the supplied image and structured evidence. Return exactly one JSON object matching responseSchema.
Do not include markdown, explanations, hidden chain-of-thought, or fields outside the schema.
The physics values and candidate IDs in the prompt are authoritative.`;

function schema(kind: string) {
  if (kind === 'prefix-dynamics') return { validPlanId: 'string', invalidPlanFirstFailure: 'zero-based integer' };
  if (kind === 'insertion-access') return { accessiblePathIds: ['string'] };
  if (kind === 'fault-recovery') return { faultJointId: 'string', actions: ['string in exact execution order'] };
  if (kind === 'inventory-substitution') return { alternativeId: 'string' };
  if (kind === 'dynamic-robustness') return { maxSafeImpulse: 'number from candidates, or 0' };
  if (kind === 'functional-kinematics') return { jointId: 'string', reachesTarget: 'boolean' };
  if (kind === 'active-inspection') return { queryId: 'string' };
  return { paretoIds: ['string'] };
}

export async function runMechanismModels(selectedModels: string[] = MODELS.map(model => model.id), resumeId?: string) {
  if (!process.env.OPENROUTER_API_KEY) process.loadEnvFile(resolve(BENCHMARK, '../.env'));
  const key = process.env.OPENROUTER_API_KEY;
  if (!key) throw new Error('OPENROUTER_API_KEY is not configured');
  if (!selectedModels.length || selectedModels.some(id => !MODELS.some(model => model.id === id)))
    throw new Error('Invalid model allowlist');
  const lock = resolve(BENCHMARK, '.runtime/pilot.lock'), fd = openSync(lock, 'wx', 0o600);
  writeFileSync(fd, `${process.pid}\n`); closeSync(fd);
  try {
    const budget = new Budget(resolve(BENCHMARK, '.runtime/campaign-ledger.json'));
    if (budget.blocked) throw new Error('Unsettled prior charge');
    const tasks = await mechanismTasks();
    const id = resumeId ?? new Date().toISOString().replace(/[:.]/g, '-') + '-mechanism';
    const dir = resolve(OUTPUT, 'results', id); mkdirSync(dir, { recursive: true });
    const run: any = resumeId ? JSON.parse(readFileSync(resolve(dir, 'run.json'), 'utf8')) : {
      id, version: MECHANISM_VERSION, status: 'running', error: null,
      models: selectedModels, cases: tasks.map(task => task.id),
      settings: { temperature: 0, maxTokens: 2200, retries: 0, images: 'one task render per case' },
      pricing: await modelPricing(), campaignBefore: budget.spent, campaignAfter: budget.spent,
      results: [], startedAt: new Date().toISOString(), completedAt: null,
    };
    if (resumeId && (run.version !== MECHANISM_VERSION
      || JSON.stringify(run.models) !== JSON.stringify(selectedModels)
      || JSON.stringify(run.cases) !== JSON.stringify(tasks.map(task => task.id)))) throw new Error('Resume protocol drift');
    run.status = 'running'; run.error = null; run.completedAt = null;
    const before = run.campaignBefore;
    const persist = () => {
      run.campaignAfter = budget.spent;
      atomicJson(resolve(dir, 'run.json'), run);
      atomicJson(resolve(dir, 'ledger.json'), budget.ledger);
    };
    persist();
    try {
      for (const task of tasks) for (const model of selectedModels) {
        if (run.results.some((row: any) => row.taskId === task.id && row.model === model)) continue;
        if (budget.spent - before > .70) throw new Error('Mechanism experiment allocation reached');
        const image = readFileSync(resolve(OUTPUT, task.visualization.detailImage));
        const publicTask = {
          version: MECHANISM_VERSION,
          id: task.id,
          kind: task.kind,
          capability: task.capability,
          question: task.question,
          input: task.input,
          responseSchema: schema(task.kind),
        };
        const content: Exclude<Message['content'], string> = [
          { type: 'text', text: JSON.stringify(publicTask) },
          { type: 'image_url', image_url: { url: `data:image/png;base64,${image.toString('base64')}` } },
        ];
        const call = await completion(key, model, [
          { role: 'system', content: SYSTEM },
          { role: 'user', content },
        ], budget);
        const answer = parseJSON(call.content), verdict = evaluateMechanismTask(task, answer);
        run.results.push({ taskId: task.id, sourceGroup: task.sourceGroup, kind: task.kind,
          model, input: publicTask, image: task.visualization.detailImage, answer, verdict, call });
        persist();
        console.log(JSON.stringify({ completed: run.results.length, total: tasks.length * selectedModels.length,
          model, task: task.id, success: verdict.success, spent: budget.spent }));
      }
      run.status = 'complete';
    } catch (error) {
      run.status = 'error'; run.error = (error as Error).message;
    }
    run.completedAt = new Date().toISOString(); persist();
    writeReport(run, dir);
    atomicJson(resolve(OUTPUT, 'results/latest.json'), { runId: id, path: `${id}/run.json`, status: run.status });
    return run;
  } finally {
    unlinkSync(lock);
  }
}

function writeReport(run: any, dir: string) {
  const kinds = [...new Set(run.results.map((row: any) => row.kind))] as string[];
  const rows = run.models.flatMap((model: string) => kinds.map(kind => {
    const selected = run.results.filter((row: any) => row.model === model && row.kind === kind);
    return { model, kind, n: selected.length, success: selected.filter((row: any) => row.verdict.success).length,
      format: selected.filter((row: any) => row.verdict.format).length,
      cost: selected.reduce((sum: number, row: any) => sum + row.call.cost, 0) };
  }));
  const text = `# Mechanism-1 模型实测

- 状态：${run.status}
- 错误：${run.error ?? '无'}
- 模型：${run.models.join('、')}
- 请求：${run.results.length}
- 本轮费用：$${(run.campaignAfter - run.campaignBefore).toFixed(6)}
- 累计费用：$${run.campaignAfter.toFixed(6)} / $4.50

| 模型 | 任务 | 完成 | 格式正确 | Exact Success | 费用 |
|---|---|---:|---:|---:|---:|
${rows.map((row: { model: string; kind: string; n: number; format: number; success: number; cost: number }) =>
    `| ${row.model} | ${row.kind} | ${row.n} | ${row.format} | ${row.success} | $${row.cost.toFixed(6)} |`).join('\n')}

结果是固定最小 Harness 下的描述性开发集表现。六个对象、每类六题，不支持显著性排名。
物理 Oracle、原始模型回答和评分结果分别保留在 \`run.json\`。
`;
  writeFileSync(resolve(dir, 'REPORT.zh-CN.md'), text);
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(import.meta.filename)) {
  const args = process.argv.slice(2), resume = args.find(arg => arg.startsWith('--resume='));
  const models = args.filter(arg => !arg.startsWith('--resume='));
  const run = await runMechanismModels(models.length ? models : undefined, resume?.slice('--resume='.length));
  console.log(JSON.stringify({ id: run.id, status: run.status, completed: run.results.length,
    error: run.error, campaignAfter: run.campaignAfter }));
}
