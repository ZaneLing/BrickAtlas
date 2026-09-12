import { chromium } from '@playwright/test';
import { mkdirSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { atomicJson } from '../../core/budget';
import { ARTIFACTS, BENCHMARK } from '../storage';
import { researchModels } from './dataset';
import { researchTaskFor } from './tasks';
import { reviewSummary } from './review';
import { PNG } from 'pngjs';

const { url } = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
const start = await (await fetch(url + '/api/status')).json();
assert.equal(start.locked, false, 'Wait for paid campaign to finish');
const reviewed = reviewSummary().submissions;
const output = resolve(ARTIFACTS, 'research/ui'); mkdirSync(output, { recursive: true });
const browser = await chromium.launch({ headless: true, channel: process.env.CI ? undefined : 'chrome' });
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1050 } });
  const errors: string[] = [];
  page.on('pageerror', e => errors.push(e.message));
  let paid = 0;
  page.on('request', r => { if (r.url().endsWith('/api/run') || r.url().endsWith('/api/research/run')) paid++; });
  await page.goto(url);
  await page.getByRole('combobox', { name: '数据版本', exact: true }).selectOption('research');
  await page.locator('.metrics-strip').getByText('576', { exact: true }).first().waitFor();
  await page.getByRole('heading', { name: 'vertical-chain', exact: true }).waitFor();
  await page.waitForTimeout(150);
  const colored = async () => {
    const image = PNG.sync.read(await page.locator('canvas').first().screenshot());
    const colors = new Set<string>();
    for (let i = 0; i < image.data.length; i += 20) colors.add(image.data.subarray(i, i + 3).toString('hex'));
    assert.ok(colors.size > 80);
  };
  await colored();
  await page.screenshot({ path: resolve(output, 'dataset.png'), fullPage: true });
  await page.getByRole('button', { name: '进入评测', exact: true }).click();
  await page.getByRole('textbox', { name: '评测答案 JSON', exact: true }).waitFor();
  const m = researchModels()[0], task = researchTaskFor(m, 'reconstruct', 'ordinary');
  await page.getByRole('textbox', { name: '评测答案 JSON', exact: true }).fill(JSON.stringify(task.oracle));
  await page.getByRole('button', { name: '提交并评分', exact: true }).click();
  await page.getByText('PASS', { exact: true }).waitFor();
  await page.getByRole('combobox', { name: '输入信息条件', exact: true }).selectOption('symbolic');
  await page.waitForFunction(() => document.querySelector('.task-prompt')?.textContent?.includes('SYMBOLIC'));
  assert.equal(await page.locator('.observation-grid img').count(), 0);
  await page.getByRole('button', { name: '训练与验证', exact: true }).click();
  await page.getByRole('heading', { name: '本地训练与验证', exact: true }).waitFor();
  await page.getByText('base-seed17', { exact: true }).first().waitFor();
  await page.screenshot({ path: resolve(output, 'training.png'), fullPage: true });
  await page.getByRole('button', { name: '人工审核', exact: true }).click();
  await page.getByRole('heading', { name: '独立审核队列', exact: true }).waitFor();
  assert.equal(await page.getByRole('button', { name: '提交人工审核', exact: true }).isDisabled(), true);
  await page.screenshot({ path: resolve(output, 'review.png'), fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  await colored();
  await page.screenshot({ path: resolve(output, 'mobile.png'), fullPage: true });
  const invalid = await fetch(url + '/api/research/reviews', { method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Benchmark-Client': start.token }, body: '{}' });
  assert.equal(invalid.status, 400);
  assert.equal(reviewSummary().submissions, reviewed);
  assert.equal((await (await fetch(url + '/api/status')).json()).budget.spent, start.budget.spent);
  assert.deepEqual(errors, []); assert.equal(paid, 0);
  await page.setViewportSize({ width: 1440, height: 1050 });
  await page.getByRole('button', { name: '模型结果', exact: true }).click();
  const runs = await (await fetch(url + '/api/runs')).json();
  for (const arm of ['reflection', 'validation']) {
    const run = runs.find((r: { mode: string }) => r.mode === `paired-${arm}`);
    assert.ok(run);
    const section = page.locator('.result-section').filter({ hasText: run.id });
    await section.getByRole('button', { name: '逐例查看', exact: true }).click();
    await page.getByText('首答复用 · 不重复计费', { exact: true }).waitFor();
    const label = arm === 'reflection' ? '无新增信息的反思指令' : '目标盲合法性反馈';
    await page.locator('.trace-event-list').getByRole('button').filter({ hasText: label }).click();
    await page.locator('.trace-event-detail').getByRole('heading', { name: label, exact: true }).waitFor();
    const raw = await (await fetch(`${url}/api/runs/${run.id}`)).json();
    const cost = raw.results.flatMap((r: { calls: { cost: number }[] }) => r.calls.slice(1))
      .reduce((n: number, c: { cost: number }) => n + c.cost, 0);
    assert.ok(Math.abs(cost - run.cost) < 1e-8);
  }
  const result = { checkedAt: new Date().toISOString(), releaseSwitch: true, ordinaryOraclePass: true,
    symbolicConditionExplicit: true, trainingDashboard: true, reviewRequiresManualInput: true,
    pairedArmsVisible: true, pairedCostsNotDuplicated: true, canvasNonblankDesktopMobile: true,
    realHumanRecordsCreated: 0, paidRequests: 0, mobileOverflow: false, browserErrors: errors };
  atomicJson(resolve(output, 'verification.json'), result); console.log(JSON.stringify(result, null, 2));
} finally { await browser.close(); }
