import { chromium } from '@playwright/test';
import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync, existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { PNG } from 'pngjs';
import { Environment } from '../core/environment';
import { makeTask, pilotTasks } from '../core/tasks';
import { RenderService } from '../core/render-service';
import { ROOT } from '../run';
import { atomicJson } from '../core/budget';
import type { View } from '../shared/types';

const info = JSON.parse(readFileSync(resolve(ROOT, '.runtime/server.json'), 'utf8')) as { url: string };
const url = info.url;
const output = resolve(ROOT, 'results/verification');
mkdirSync(output, { recursive: true });
const evidence: Record<string, unknown> = { measuredAt: new Date().toISOString(), url, tests: [] };
const checks: string[] = [];
const render = new RenderService(url);
let browser;
try {
  for (const seed of [41, 42]) for (const view of ['iso', 'top', 'front', 'back'] as View[]) {
    const a = new Environment(makeTask(seed, 0, 'none'));
    const b = new Environment(makeTask(seed, 1, 'none'));
    const af = await render.render(a.sceneParts(), view, a.visibleParts().map(p => p.id));
    const bf = await render.render(b.sceneParts(), view, b.visibleParts().map(p => p.id));
    assert.equal(af.hash, bf.hash, `${seed}:${view}: closed twins must be byte-identical`);
    const image = PNG.sync.read(af.buffer);
    const colors = new Set<string>();
    for (let i = 0; i < image.data.length; i += 16) colors.add(image.data.subarray(i, i + 3).toString('hex'));
    assert.ok(colors.size > 80, `${view}: blank frame`);
    if (seed === 41 && view === 'iso') writeFileSync(resolve(output, 'closed.png'), af.buffer);
  }
  checks.push('Closed twins are byte-identical for both seeds in all four allowed views; nonblank RGB');
  const a = new Environment(makeTask(41, 0, 'none'));
  const b = new Environment(makeTask(41, 1, 'none'));
  a.step({ type: 'detach', id: a.task.coverId });
  b.step({ type: 'detach', id: b.task.coverId });
  const af = await render.render(a.sceneParts(), 'top', a.visibleParts().map(p => p.id));
  const bf = await render.render(b.sceneParts(), 'top', b.visibleParts().map(p => p.id));
  assert.notEqual(af.hash, bf.hash);
  writeFileSync(resolve(output, 'opened-a.png'), af.buffer);
  writeFileSync(resolve(output, 'opened-b.png'), bf.buffer);
  checks.push('Intervention reveals different interiors');

  const status = await (await fetch(`${url}/api/status`)).json();
  const beforeCalls = status.budget.calls;
  const forbidden = await fetch(`${url}/api/pilot`, {
    method: 'POST', headers: { 'Content-Type': 'application/json', Origin: 'https://example.com' },
    body: JSON.stringify({ confirmPaid: true, models: ['openai/gpt-4.1-mini'] }),
  });
  assert.equal(forbidden.status, 403);
  const unconfirmed = await fetch(`${url}/api/pilot`, {
    method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Benchmark-Client': status.clientToken },
    body: JSON.stringify({ models: ['openai/gpt-4.1-mini'] }),
  });
  assert.equal(unconfirmed.status, 400);
  const invalidModels = await fetch(`${url}/api/pilot`, {
    method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Benchmark-Client': status.clientToken },
    body: JSON.stringify({ confirmPaid: true, models: ['expensive/unknown'] }),
  });
  assert.equal(invalidModels.status, 400);
  for (const path of [`/@fs/${ROOT}/../.env`, `/@fs/${ROOT}/core/tasks.ts`, `/@fs/${ROOT}/.runtime/campaign-ledger.json`, '/core/tasks.ts']) {
    const response = await fetch(`${url}${path}`);
    assert.ok(!response.ok, `Private source exposed: ${path}`);
  }
  checks.push('Private files denied; paid API rejects cross-origin, missing confirmation and unlisted models');

  browser = await chromium.launch({ channel: process.env.CI ? undefined : 'chrome', headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1050 } });
  const errors: string[] = [];
  let paidRequests = 0;
  page.on('pageerror', error => errors.push(error.message));
  page.on('request', r => { if (r.url().endsWith('/api/pilot')) paidRequests++; });
  await page.goto(url);
  await page.getByText('OpenRouter 已连接', { exact: true }).waitFor();
  await page.getByText('观察与拆解', { exact: true }).waitFor();
  await page.waitForFunction(() => {
    const c = document.querySelector<HTMLCanvasElement>('.scene-canvas');
    return !!c?.getContext('2d')?.getImageData(320, 240, 1, 1).data[3];
  });
  const before = await page.locator('.scene-canvas').screenshot();
  await page.getByRole('button', { name: '俯视', exact: true }).click();
  await page.waitForFunction(() => document.querySelector('.segmented .selected')?.textContent === '俯视');
  await page.waitForTimeout(250);
  assert.notDeepEqual(await page.locator('.scene-canvas').screenshot(), before);
  checks.push('Camera controls change real rendered canvas pixels');
  const task = pilotTasks()[0];
  await page.locator('.visible-list button').filter({ hasText: task.coverId }).click();
  await page.getByRole('spinbutton', { name: '预计新增可见零件数' }).fill('2');
  await page.getByRole('button', { name: '预测并拆卸', exact: true }).click();
  await page.locator('.visible-list button').filter({ hasText: task.hiddenIds[0] }).waitFor();
  await page.getByRole('textbox', { name: '蓝图 JSON' }).fill(JSON.stringify({ version: 1, parts: task.target }, null, 2));
  await page.getByRole('button', { name: '提交蓝图', exact: true }).click();
  await page.getByRole('button', { name: '执行蓝图', exact: true }).click();
  await page.waitForFunction(() => document.querySelectorAll('.visible-list button').length === 8);
  await page.getByRole('button', { name: '结束并评分', exact: true }).click();
  await page.getByText('PASS', { exact: true }).waitFor();
  checks.push('Manual inspect -> detach -> blueprint -> build -> score workflow');
  await page.screenshot({ path: resolve(output, 'desktop.png'), fullPage: true });
  if (!status.running && !status.budget.blocked) {
    await page.getByRole('button', { name: '运行付费 Pilot', exact: true }).click();
    await page.getByRole('dialog').waitFor();
    await page.getByRole('dialog').getByRole('button', { name: '取消', exact: true }).last().click();
    assert.equal(paidRequests, 0);
    checks.push('Opening/canceling paid confirmation never calls OpenRouter');
  }
  await page.setViewportSize({ width: 390, height: 844 });
  await page.screenshot({ path: resolve(output, 'mobile.png'), fullPage: true });
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
  const box = await page.locator('.scene-canvas').boundingBox();
  assert.ok(box && box.width > 300 && box.height > 200);
  checks.push('390px mobile layout: no horizontal overflow; visible stable-size scene');
  await page.setViewportSize({ width: 1440, height: 1050 });
  await page.getByRole('button', { name: '试验结果', exact: true }).click();
  if (await page.getByRole('button', { name: '逐步回放', exact: true }).count()) {
    await page.getByRole('button', { name: '逐步回放', exact: true }).first().click();
    await page.getByText('Episode 回放', { exact: true }).waitFor();
    await page.screenshot({ path: resolve(output, 'results.png'), fullPage: true });
    checks.push('Saved run table and step replay open successfully');
  }
  await page.getByRole('button', { name: '协议与边界', exact: true }).click();
  await page.getByRole('heading', { name: '协议与测量边界' }).waitFor();
  assert.deepEqual(errors, []);
  checks.push('Protocol view and browser runtime free of page errors');
  assert.equal((await (await fetch(`${url}/api/status`)).json()).budget.calls, beforeCalls);
  evidence.tests = checks;
  evidence.passed = checks.length;
  evidence.browser = browser.version();
  evidence.paidRequests = 0;
  atomicJson(resolve(output, 'verification.json'), evidence);
  if (existsSync(resolve(ROOT, 'results/latest.json'))) {
    const { id } = JSON.parse(readFileSync(resolve(ROOT, 'results/latest.json'), 'utf8'));
    atomicJson(resolve(ROOT, 'results', id, 'verification.json'), evidence);
  }
  console.log(JSON.stringify(evidence, null, 2));
} finally {
  await browser?.close();
  await render.close();
}
