import { chromium } from '@playwright/test';
import { readFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { PNG } from 'pngjs';
import { atomicJson } from '../../core/budget';
import { BENCHMARK } from '../storage';
import { STUDY } from './protocol';
import { studyRuns } from './results';
import { localEvidenceRuns } from './local-evidence';

const { url } = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
const before = await (await fetch(url + '/api/status')).json(), out = resolve(STUDY, 'ui');
assert.equal(before.locked, false); mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ headless: true, channel: process.env.CI ? undefined : 'chrome' });
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } }), errors: string[] = [];
  page.on('pageerror', e => errors.push(e.message)); let paid = 0;
  page.on('request', r => { if (r.method() === 'POST' && r.url().endsWith('/run')) paid++; });
  await page.goto(url);
  await page.getByRole('button', { name: 'v2 模型实测', exact: true }).click();
  const main = studyRuns().find(r => r.id.endsWith('-api'));
  await page.getByRole('combobox', { name: 'study run' }).selectOption(main.id);
  await page.getByTitle('回放实测 0', { exact: true }).click();
  await page.getByRole('heading', { name: '全步骤可视化', exact: true }).waitFor();
  await page.getByTitle('最终事件', { exact: true }).click();
  assert.equal(await page.locator('.trace-scenes canvas').count(), 3);
  const png = PNG.sync.read(await page.locator('.trace-scenes canvas').nth(2).screenshot()), colors = new Set<string>();
  for (let i = 0; i < png.data.length; i += 20) colors.add(png.data.subarray(i, i + 3).toString('hex'));
  assert.ok(colors.size > 80);
  await page.locator('.trace-inspector').screenshot({ path: resolve(out, 'desktop.png') });
  await page.setViewportSize({ width: 390, height: 844 });
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  await page.locator('.trace-inspector').screenshot({ path: resolve(out, 'mobile.png') });
  await page.getByLabel('仅看模型原始输入').check();
  assert.equal(await page.locator('.trace-scenes canvas').count(), 0);
  let checked = 0;
  for (const run of studyRuns()) for (const [index, row] of run.rows.entries()) {
    const response = await fetch(`${url}/api/study/runs/${run.id}/cases/${index}/trace`);
    assert.equal(response.status, 200);
    const trace = await response.json();
    assert.deepEqual(trace.verdict, row.verdict);
    assert.equal(trace.evidence.responseCount, row.reusedFirstCall ? 2 : 1);
    assert.ok(Math.abs(trace.events.reduce((n: number, e: { cost: number }) => n + e.cost, 0) - row.call.cost) < 1e-9);
    for (let i = 1; i < trace.events.length; i++) assert.equal(trace.events[i].before, trace.events[i - 1].after);
    if (row.arm === 'no-image') assert.equal(trace.frames.length, 0);
    if (row.arm === 'reflection') assert.ok(trace.events.some((e: { title: string }) => e.title === '无新增信息的反思指令'));
    checked++;
  }
  let localChecked = 0;
  const locals = localEvidenceRuns();
  for (const run of locals) for (const [index, row] of run.rows.entries()) {
    const response = await fetch(`${url}/api/study/runs/${run.id}/cases/${index}/trace`);
    assert.equal(response.status, 200);
    const trace = await response.json();
    assert.deepEqual(trace.verdict, row.verdict);
    assert.equal(trace.mode, 'local-inference');
    assert.equal(trace.events.find((e: any) => e.kind === 'response').payload.content, row.call.content);
    assert.equal(trace.events.reduce((n: number, e: any) => n + e.cost, 0), 0);
    for (let i = 1; i < trace.events.length; i++) assert.equal(trace.events[i].before, trace.events[i - 1].after);
    localChecked++;
  }
  if (locals.length) {
    await page.getByRole('combobox', { name: 'study run' }).selectOption(locals[0].id);
    await page.getByTitle('回放实测 0', { exact: true }).click();
    await page.getByRole('heading', { name: '全步骤可视化', exact: true }).waitFor();
    await page.getByLabel('仅看模型原始输入').uncheck();
    await page.getByTitle('最终事件', { exact: true }).click();
    await page.getByText('本地模型原始输出', { exact: false }).first().waitFor();
    await page.locator('.trace-inspector').screenshot({ path: resolve(out, 'local-mobile.png') });
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  }
  assert.equal((await (await fetch(url + '/api/status')).json()).budget.spent, before.budget.spent);
  assert.equal(paid, 0); assert.deepEqual(errors, []);
  const report = { checkedAt: new Date().toISOString(), cases: checked, localCases: localChecked, allScoresMatch: true,
    paidReceiptsDisplayed: true, reusedChargesNotDuplicated: true, stateChainsContinuous: true,
    canvasNonblank: true, mobileNoOverflow: true, inputOnlyIsolation: true, apiRequests: 0, errors };
  atomicJson(resolve(out, 'verification.json'), report); console.log(JSON.stringify(report, null, 2));
} finally { await browser.close(); }
