import assert from 'node:assert/strict';
import { existsSync, readFileSync, openSync, closeSync, unlinkSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { Budget, atomicJson } from '../../core/budget';
import type { Message } from '../../core/openrouter';
import { BENCHMARK, SYSTEM } from '../storage';
import { digest } from '../data';
import { clusterBootstrap } from '../v2/batch';
import { imageEvidence } from './calibration-export';
import { VALIDATION_MODELS, validationPricing, validationCeiling, validationCompletion } from './validation-client';
import { VALIDATION_DIR } from './model-validation';
import { ORDER_DIR, ORDER_ARMS, orderQuestions, orderScore } from './order-study';

function sources() {
  return Object.fromEntries(['order-study.ts', 'order-run.ts', 'exposure.ts', 'validation-client.ts'].map(p =>
    [p, digest(readFileSync(resolve(BENCHMARK, 'suite/study', p), 'utf8'))]));
}
function inputs() {
  const protocol = JSON.parse(readFileSync(resolve(ORDER_DIR, 'protocol.json'), 'utf8')), questions = orderQuestions();
  assert.equal(protocol.version, 'order-repeat-1'); assert.deepEqual(protocol.models, VALIDATION_MODELS);
  assert.equal(protocol.plannedCalls, 192); assert.equal(protocol.newSpendCap, 0.7);
  assert.deepEqual(protocol.rows.map((r: any) => r.id), questions.map(q => q.id));
  for (const [i, row] of protocol.rows.entries()) {
    assert.equal(row.group, questions[i].group); assert.equal(row.arm, questions[i].arm);
    assert.deepEqual(row.input, questions[i].input); assert.equal(row.images.length, questions[i].frames.length);
  }
  return { protocol, questions };
}
function messages(row: any): Message[] {
  const content: Exclude<Message['content'], string> = [{ type: 'text', text: JSON.stringify(row.input) }];
  for (const path of row.images) {
    assert.match(path, /^images\/[a-f0-9]{64}\.png$/);
    const bytes = readFileSync(resolve(ORDER_DIR, path)); assert.equal(imageEvidence(bytes).hash, path.slice(7, -4));
    content.push({ type: 'image_url', image_url: { url: `data:image/png;base64,${bytes.toString('base64')}` } });
  }
  return [{ role: 'system', content: SYSTEM }, { role: 'user', content }];
}
export async function runOrderStudy() {
  const { protocol, questions } = inputs(), path = resolve(ORDER_DIR, 'run.json');
  assert.ok(!existsSync(path), 'Preserve existing experiment; no automatic rerun');
  if (!process.env.OPENROUTER_API_KEY) process.loadEnvFile(resolve(BENCHMARK, '../.env'));
  const apiKey = process.env.OPENROUTER_API_KEY; assert.ok(apiKey);
  const lock = resolve(BENCHMARK, '.runtime/pilot.lock'), fd = openSync(lock, 'wx', 0o600); closeSync(fd);
  try {
    const budget = new Budget(resolve(BENCHMARK, '.runtime/campaign-ledger.json'));
    assert.equal(budget.blocked, false);
    const original = JSON.parse(readFileSync(resolve(VALIDATION_DIR, 'run.json'), 'utf8'));
    const run = { status: 'running', protocolHash: digest(protocol), sourceHashes: sources(), pricing: await validationPricing(),
      campaignBefore: budget.spent, campaignAfter: budget.spent, error: null as string | null, rows: [] as any[] };
    const save = () => { run.campaignAfter = budget.spent; atomicJson(path, run); atomicJson(resolve(ORDER_DIR, 'ledger.json'), budget.ledger); };
    save();
    try {
      for (const [i, row] of protocol.rows.entries()) for (let j = 0; j < VALIDATION_MODELS.length; j++) {
        const model = VALIDATION_MODELS[(i + j) % VALIDATION_MODELS.length], request = messages(row);
        const ceiling = validationCeiling(model.id, request);
        if (budget.spent - run.campaignBefore + ceiling > protocol.newSpendCap
          || budget.spent - original.campaignBefore + ceiling > 2) throw new Error('Validation allocation reached');
        const call = await validationCompletion(apiKey, model.id, request, budget);
        run.rows.push({ id: row.id, group: row.group, arm: row.arm, model: model.id,
          requestHash: digest(request), call, score: orderScore(questions[i], call.content) });
        save(); console.log(JSON.stringify({ completed: run.rows.length, planned: 192, newCost: budget.spent - run.campaignBefore }));
      }
      run.status = 'complete';
    } catch (error) { run.status = 'stopped'; run.error = (error as Error).message; }
    save(); return { status: run.status, responses: run.rows.length, error: run.error };
  } finally { unlinkSync(lock); }
}
export function pairedOrderEffect(a: string | null, repeat: string | null, permuted: string | null) {
  if (a === null || repeat === null || permuted === null) return null;
  return { repeatMismatch: Number(a !== repeat), permutationMismatch: Number(a !== permuted),
    excessMismatch: Number(a !== permuted) - Number(a !== repeat) };
}
export function replayOrderStudy() {
  const { protocol, questions } = inputs(), run = JSON.parse(readFileSync(resolve(ORDER_DIR, 'run.json'), 'utf8'));
  assert.equal(run.protocolHash, digest(protocol)); assert.deepEqual(run.sourceHashes, sources());
  const ledger = JSON.parse(readFileSync(resolve(ORDER_DIR, 'ledger.json'), 'utf8')), seen = new Set(), receipts = new Set();
  let cost = 0;
  for (const row of run.rows) {
    const i = questions.findIndex(q => q.id === row.id); assert.ok(i >= 0);
    assert.equal(row.group, questions[i].group); assert.equal(row.arm, questions[i].arm);
    assert.ok(VALIDATION_MODELS.some(m => m.id === row.model));
    const k = `${row.id}:${row.model}`; assert.ok(!seen.has(k)); seen.add(k);
    assert.ok(!receipts.has(row.call.id)); receipts.add(row.call.id);
    assert.equal(row.requestHash, digest(messages(protocol.rows[i])));
    assert.deepEqual(row.score, orderScore(questions[i], row.call.content));
    const charge = ledger.charges.find((c: any) => c.generationId === row.call.id);
    assert.equal(charge?.status, 'settled'); assert.equal(charge.model, row.model); assert.equal(charge.actual, row.call.cost);
    cost += row.call.cost;
  }
  if (run.status === 'complete') assert.equal(run.rows.length, 192);
  assert.ok(Math.abs(cost - run.campaignAfter + run.campaignBefore) < 1e-8);
  const groups = [...new Set<string>(questions.map(q => q.group))];
  const byModel = VALIDATION_MODELS.map(model => {
    const rows = run.rows.filter((r: any) => r.model === model.id);
    const paired = groups.map(group => {
      const arms = Object.fromEntries(ORDER_ARMS.map(arm => [arm, rows.find((r: any) => r.group === group && r.arm === arm)]));
      return { group, effect: pairedOrderEffect(arms.original?.score.selectedKey ?? null,
        arms.repeat?.score.selectedKey ?? null, arms.permuted?.score.selectedKey ?? null),
      sameProvider: arms.original && arms.repeat && arms.permuted
        ? new Set([arms.original.call.provider, arms.repeat.call.provider, arms.permuted.call.provider]).size === 1 : null };
    });
    const valid = paired.filter(p => p.effect !== null);
    return { model: model.id, arms: Object.fromEntries(ORDER_ARMS.map(arm => {
      const selected = rows.filter((r: any) => r.arm === arm);
      return [arm, { successes: selected.reduce((n: number, r: any) => n + r.score.success, 0),
        returned: selected.length, missing: groups.length - selected.length,
        formatAccepted: selected.reduce((n: number, r: any) => n + r.score.format, 0) }];
    })), paired, pairedGroups: valid.length,
    repeatMismatch: valid.reduce((n, p) => n + p.effect!.repeatMismatch, 0),
    permutationMismatch: valid.reduce((n, p) => n + p.effect!.permutationMismatch, 0),
    excessMismatchInterval: clusterBootstrap(valid.map(p => p.effect!.excessMismatch)) };
  });
  const result = { version: 'order-repeat-analysis-1', status: run.status, responses: run.rows.length,
    sourceGroups: groups.length, newCost: cost, campaignAfter: run.campaignAfter, byModel, apiRequests: 0,
    runHash: digest(readFileSync(resolve(ORDER_DIR, 'run.json'), 'utf8')),
    caveat: 'Bootstrap resamples source groups within this tiny selected grid sample, not the population of real structures. Provider/time and sampling remain possible causes. No causal or stable model-ranking claim.' };
  atomicJson(resolve(ORDER_DIR, 'analysis.json'), result);
  const models = VALIDATION_MODELS.map(m => m.id);
  writeFileSync(resolve(ORDER_DIR, 'REPORT.zh-CN.md'), `# 候选换序与重复采样对照\n\n状态：${result.status}，${result.responses}/192次调用，12个来源对象；新增费用$${cost.toFixed(6)}。\n\n` +
    '| 模型 | 首答 | 同顺序重复 | 换序 | 无图 | 重复不一致 | 换序不一致 | 超额不一致均值及95%区间 |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |\n' +
    byModel.map(m => `| ${m.model} | ${ORDER_ARMS.map(a => `${m.arms[a].successes}/${m.arms[a].returned}`).join(' | ')} | ${m.repeatMismatch}/${m.pairedGroups} | ${m.permutationMismatch}/${m.pairedGroups} | ${m.excessMismatchInterval ? [m.excessMismatchInterval.mean, m.excessMismatchInterval.low, m.excessMismatchInterval.high].map(x => x.toFixed(3)).join(' / ') : 'N/A'} |`).join('\n') +
    '\n\n同顺序重复与换序交错，比较实际位姿而非标签。超额不一致=换序不一致-重复不一致；区间包含0时不能把换序波动可靠归因于选项顺序。' +
    '原4对象实验不能排除重复采样，本对照专门补此缺口。12个小型来源仍是开发集，不代表充分确认性研究。缺失/坏格式的配对不编造数值；分母单列。\n' +
    `\n模型：${models.join(', ')}。所有条件图片与输入按协议冻结；只有无图组移除图片。全部候选合法、标签平衡。\n`);
  return { status: result.status, responses: result.responses, sourceGroups: groups.length, byModel };
}
