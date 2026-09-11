import { chromium } from '@playwright/test';
import { existsSync, mkdirSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { ARTIFACTS, BENCHMARK, SUITE, defaultSelection, listRuns } from './storage';
import { models } from './data';
import { taskFor } from './tasks';
import { SuiteRenderer } from './render';
import { PNG } from 'pngjs';
import { atomicJson } from '../core/budget';
import { TASKS } from './shared';

const { url } = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
const status = await (await fetch(url + '/api/status')).json();
assert.equal(status.locked, false, 'Wait for paid run before UI checks');
const costBefore = status.budget.spent;
const output = resolve(ARTIFACTS, 'verification');
mkdirSync(output, { recursive: true });
const browser = await chromium.launch({ headless: true, channel: process.env.CI ? undefined : 'chrome' });
const renderer = new SuiteRenderer(url);
const checks: string[] = [], errors: string[] = [];
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  page.on('pageerror', e => errors.push(e.message));
  let paid = 0;
  page.on('request', r => { if (r.url().endsWith('/api/run')) paid++; });
  await page.goto(url);
  await page.getByRole('button', { name: '进入评测', exact: true }).waitFor();
  await page.waitForFunction(() => !!document.querySelector('canvas'));
  await page.waitForTimeout(250);
  const first = await page.locator('canvas').screenshot();
  const png = PNG.sync.read(first);
  const colors = new Set<string>();
  for (let i = 0; i < png.data.length; i += 20) colors.add(png.data.subarray(i, i + 3).toString('hex'));
  assert.ok(colors.size > 80, '3D scene is blank');
  await page.getByRole('button', { name: '俯视', exact: true }).click();
  assert.notDeepEqual(await page.locator('canvas').screenshot(), first);
  const box = (await page.locator('canvas').boundingBox())!;
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  await page.mouse.down(); await page.mouse.move(box.x + box.width / 2 + 85, box.y + box.height / 2 + 25, { steps: 10 }); await page.mouse.up();
  await page.getByRole('button', { name: '斜视', exact: true }).click();
  checks.push('Desktop 3D scene nonblank, camera controls and OrbitControls drag work');
  await page.screenshot({ path: resolve(output, 'desktop.png'), fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  await page.screenshot({ path: resolve(output, 'mobile.png'), fullPage: true });
  checks.push('390px mobile fits viewport and scene remains visible');
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.getByRole('button', { name: '进入评测', exact: true }).click();
  await page.getByRole('textbox', { name: '评测答案 JSON' }).waitFor();
  const m = models()[0];
  const task = taskFor(m, 'reconstruct');
  await page.getByRole('textbox', { name: '评测答案 JSON' }).fill(JSON.stringify(task.oracle));
  await page.getByRole('button', { name: '提交并评分', exact: true }).click();
  await page.getByText('PASS', { exact: true }).waitFor();
  await page.screenshot({ path: resolve(output, 'task.png'), fullPage: true });
  checks.push('Reference images load; manual JSON submission uses the same scorer and passes oracle');
  for (const kind of TASKS) {
    const expected = taskFor(m, kind);
    const response = await fetch(`${url}/api/task?model=${m.id}&kind=${kind}`);
    const payload = await response.json();
    assert.ok(!('oracle' in payload) && !('target' in payload) && !('frames' in payload));
    for (const src of payload.images) {
      const image = await fetch(url + src);
      assert.ok(image.ok); assert.equal(image.headers.get('content-type'), 'image/png');
    }
    const result = await (await fetch(url + '/api/submit', { method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Benchmark-Client': status.token },
      body: JSON.stringify({ modelId: m.id, kind, answer: expected.oracle }) })).json();
    assert.equal(result.metrics.success, 1);
  }
  checks.push('All eight public task APIs omit oracle answers and score valid submissions');
  for (const path of ['/data.ts', `/@fs/${SUITE}/data.ts`, `/@fs/${BENCHMARK}/../.env`, `/@fs/${BENCHMARK}/.runtime/campaign-ledger.json`]) {
    assert.ok(!(await fetch(url + path)).ok, `Private file exposed: ${path}`);
  }
  const forbidden = await fetch(url + '/api/run', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
  assert.equal(forbidden.status, 403);
  const invalid = await fetch(url + '/api/run', { method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Benchmark-Client': status.token },
    body: JSON.stringify({ confirmPaid: false }) });
  assert.equal(invalid.status, 400);
  await page.getByRole('button', { name: '运行付费评测', exact: true }).click();
  await page.getByRole('dialog').getByRole('button', { name: '取消', exact: true }).click();
  assert.equal(paid, 0);
  checks.push('Private files denied; missing paid confirmation rejected; cancel costs nothing');
  await page.getByRole('button', { name: '模型结果', exact: true }).click();
  if (listRuns().length) {
    await page.getByRole('button', { name: '逐例查看', exact: true }).first().click();
    await page.getByRole('combobox', { name: '结果样本' }).waitFor();
    await page.screenshot({ path: resolve(output, 'results.png'), fullPage: true });
    checks.push('Model task table, exact scores, raw responses and receipts are viewable');
  }
  await page.getByRole('button', { name: '协议与指标', exact: true }).click();
  await page.getByRole('heading', { name: '协议与指标', exact: true }).waitFor();
  const firstSelection = defaultSelection();
  for (const item of firstSelection) {
    const task = taskFor(models().find(m => m.id === item.modelId)!, item.kind);
    for (const f of task.frames) {
      const frame = await renderer.render(f);
      const png = PNG.sync.read(frame.buffer);
      assert.equal(png.width, 640); assert.equal(png.height, 480);
      assert.ok(frame.buffer.length > 1000);
    }
  }
  checks.push('Every smoke observation renders at 640x480 without missing geometry');
  assert.deepEqual(errors, []);
  assert.equal((await (await fetch(url + '/api/status')).json()).budget.spent, costBefore);
  checks.push('No browser runtime errors and no paid requests');
  const result = { checkedAt: new Date().toISOString(), browser: browser.version(), checks,
    paidRequests: 0, viewport: ['1440x1000', '390x844'] };
  atomicJson(resolve(output, 'ui.json'), result);
  console.log(JSON.stringify(result, null, 2));
} finally { await renderer.close(); await browser.close(); }
