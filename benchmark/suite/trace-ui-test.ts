import { chromium } from '@playwright/test';
import { mkdirSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { PNG } from 'pngjs';
import { atomicJson } from '../core/budget';
import { ARTIFACTS, BENCHMARK, listRuns } from './storage';
import { VERSION } from './shared';

const { url } = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
const out = resolve(ARTIFACTS, 'trace-verification'); mkdirSync(out, { recursive: true });
const before = await (await fetch(url + '/api/status')).json();
const browser = await chromium.launch({ channel: process.env.CI ? undefined : 'chrome', headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const errors: string[] = []; let paid = 0;
  page.on('pageerror', e => errors.push(e.message));
  page.on('request', req => { if (req.url().endsWith('/api/run')) paid++; });
  await page.goto(url);
  await page.getByRole('button', { name: '模型结果', exact: true }).click();
  const run = listRuns().find(r => r.version === VERSION && r.mode === 'one-shot' && r.representation === 'absolute')!;
  const section = page.locator('.result-section').filter({ hasText: run.id });
  await section.getByRole('button', { name: '逐例查看', exact: true }).click();
  const index = run.results.findIndex(r => r.kind === 'reconstruct');
  await page.getByRole('combobox', { name: '结果样本' }).selectOption(String(index));
  await page.getByRole('heading', { name: '全步骤可视化', exact: true }).waitFor();
  await page.getByRole('button', { name: '最终事件', exact: true }).click();
  await page.waitForTimeout(250);
  assert.equal(await page.locator('.trace-scenes canvas').count(), 3);
  const image = PNG.sync.read(await page.locator('.trace-scenes canvas').nth(1).screenshot());
  const colors = new Set<string>();
  for (let i = 0; i < image.data.length; i += 16) colors.add(image.data.subarray(i, i + 3).toString('hex'));
  assert.ok(colors.size > 80);
  const beforeRotate = await page.locator('.trace-scenes canvas').nth(2).screenshot();
  const box = (await page.locator('.trace-scenes canvas').nth(1).boundingBox())!;
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  await page.mouse.down(); await page.mouse.move(box.x + box.width * 0.7, box.y + box.height * 0.65, { steps: 8 }); await page.mouse.up();
  assert.notDeepEqual(await page.locator('.trace-scenes canvas').nth(2).screenshot(), beforeRotate);
  await page.getByTitle('同步斜视', { exact: true }).click();
  await page.getByLabel('连接图', { exact: true }).check();
  await page.screenshot({ path: resolve(out, 'desktop.png'), fullPage: true });
  await page.getByRole('button', { name: '第一个事件', exact: true }).click();
  await page.getByRole('button', { name: '播放回放', exact: true }).click();
  await page.waitForTimeout(850);
  assert.ok(Number(await page.getByRole('slider', { name: '事件时间轴' }).inputValue()) > 0);
  await page.getByRole('button', { name: '暂停回放', exact: true }).click();
  await page.getByLabel('仅看模型原始输入').check();
  assert.equal(await page.locator('.trace-scenes canvas').count(), 0);
  assert.ok(await page.locator('.trace-inputs img').count() > 0);
  assert.equal(await page.locator('.trace-event-detail, .trace-transport, .response-grid').count(), 0);
  await page.getByLabel('仅看模型原始输入').uncheck();
  await page.setViewportSize({ width: 390, height: 844 });
  const mobileCanvas = PNG.sync.read(await page.locator('.trace-scenes canvas').nth(2).screenshot());
  const mobileColors = new Set<string>();
  for (let i = 0; i < mobileCanvas.data.length; i += 16) mobileColors.add(mobileCanvas.data.subarray(i, i + 3).toString('hex'));
  assert.ok(mobileColors.size > 80);
  await page.screenshot({ path: resolve(out, 'mobile.png'), fullPage: true });
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  let checked = 0;
  for (const run of listRuns()) for (let i = 0; i < run.results.length; i++) {
    const response = await fetch(`${url}/api/runs/${run.id}/cases/${i}/trace`);
    assert.equal(response.status, 200);
    const trace = await response.json();
    assert.equal(trace.evidence.scoreMatches, true); checked++;
  }
  const download = await fetch(`${url}/api/runs/${run.id}/cases/${index}/trace?format=jsonl`);
  const lines = (await download.text()).trim().split('\n').map(line => JSON.parse(line));
  assert.equal(lines[0].type, 'manifest'); assert.ok(lines.slice(1).every(line => line.type === 'event'));
  assert.equal((await (await fetch(url + '/api/status')).json()).budget.spent, before.budget.spent);
  assert.equal(paid, 0); assert.deepEqual(errors, []);
  const result = { checkedAt: new Date().toISOString(), casesAccessible: checked,
    syncedCameras: true, outputCanvasNonblank: true, playback: true, inputOnlyHidesJudgeScenes: true,
    mobileOverflow: false, mobileCanvasNonblank: true, jsonlExport: true, browserErrors: errors, paidRequests: paid };
  atomicJson(resolve(out, 'verification.json'), result); console.log(JSON.stringify(result, null, 2));
} finally { await browser.close(); }
