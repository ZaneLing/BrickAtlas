import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';
import { copyFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { PNG } from 'pngjs';
import { BASE, OUT, WEB, read, write, sha } from './release';

const catalog = read(resolve(OUT, 'catalog.json'));
const url = process.env.BRICKATLAS_URL ?? 'http://127.0.0.1:5173';
const checkpoint = resolve(OUT, 'browser-checkpoint.json');
const records: any[] = process.argv.includes('--resume') && existsSync(checkpoint) ? read(checkpoint) : [];
const errors: string[] = [];
mkdirSync(resolve(OUT, 'images'), { recursive: true });
mkdirSync(resolve(OUT, 'web-verification'), { recursive: true });
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const context = await browser.newContext({ viewport: { width: 1600, height: 1050 } });
const page = await context.newPage();
page.setDefaultTimeout(15000);
page.on('pageerror', e => errors.push(e.message));
try {
  await page.goto(`${url}/benchmark`);
  await page.waitForSelector('[data-bench-model]');
  assert.equal(await page.locator('[data-bench-model]').count(), 144);
  for (const level of ['D1', 'D2', 'D3', 'D4']) {
    await page.getByLabel('基准难度筛选').selectOption(level);
    assert.equal(await page.locator('[data-bench-model]').count(), 36);
  }
  for (const m of catalog) {
    const hash = sha(resolve(OUT, 'models', `${m.id}.json`));
    if (records.some(r => r.id === m.id && r.modelHash === hash)) continue;
    await page.goto(`${url}/benchmark/${m.id}`);
    await page.waitForFunction(id => (window as any).__benchmark?.().modelId === id, m.id);
    const state = await page.evaluate(() => (window as any).__benchmark());
    assert.equal(state.parts, m.parts); assert.equal(state.modules, m.modules); assert.equal(state.contextLost, false);
    const frames: any[] = [];
    for (const view of ['iso', 'front', 'side', 'top']) {
      const filename = `${m.id}-${view}.png`, path = resolve(OUT, 'images', filename);
      if (m.retained) copyFileSync(resolve(BASE, 'images', filename), path);
      else {
        const encoded = await page.evaluate(view => (window as any).__benchmarkCapture(view), view);
        const { writeFileSync } = await import('node:fs');
        writeFileSync(path, Buffer.from(encoded.split(',')[1], 'base64'));
      }
      const png = PNG.sync.read(readFileSync(path));
      let contrast = 0;
      for (let i = 0; i < png.data.length; i += 4) if (Math.abs(png.data[i] - png.data[i + 2]) > 25) contrast++;
      assert.ok(contrast > 100, `${m.id}: blank capture`);
      copyFileSync(path, resolve(WEB, 'images', filename));
      frames.push({ file: `images/${filename}`, sha256: sha(path), width: png.width, height: png.height,
        contrast, source: m.retained ? 'retained-base48' : 'current-original-site-canvas' });
    }
    await page.getByLabel('基准展开程度').fill('1');
    await page.waitForFunction(() => (window as any).__benchmark().explosion === 1);
    await page.getByLabel('基准展开程度').fill('0');
    const rect = (await page.locator('.bench-canvas canvas').boundingBox())!;
    const before = (await page.evaluate(() => (window as any).__benchmark())).camera;
    await page.mouse.move(rect.x + rect.width / 2, rect.y + rect.height / 2);
    await page.mouse.down();
    await page.mouse.move(rect.x + rect.width * 0.65, rect.y + rect.height * 0.62, { steps: 6 });
    await page.mouse.up();
    assert.notDeepEqual((await page.evaluate(() => (window as any).__benchmark())).camera, before);
    await page.getByLabel('选择基准题目').selectOption(`h3-${m.id}-assembly`);
    await page.getByRole('button', { name: '载入参考答案', exact: true }).click();
    await page.waitForFunction(() => (window as any).__benchmark().visibleModules.length === 0);
    const bundle = read(resolve(OUT, 'models', `${m.id}.json`));
    const root = bundle.model.modules.find((x: any) => x.anchored);
    await page.getByLabel(`隔离 ${root.id}`, { exact: true }).click();
    assert.equal((await page.evaluate(() => (window as any).__benchmark())).visibleModules.length, 0);
    await page.locator('.bench-module').getByRole('button', { name: root.name, exact: true }).click();
    await page.getByLabel('动作回放步骤').fill(String(m.modules));
    await page.waitForFunction(n => (window as any).__benchmark().visibleModules.length === n, m.modules);
    await page.getByRole('button', { name: '检查答案', exact: true }).click();
    assert.equal(await page.locator('.bench-tasks > p[role=status]').textContent(), '通过');
    assert.equal(await page.getByLabel('选择基准题目').locator('option').count(), 49);
    records.push({ id: m.id, modelHash: hash, frames, orbit: true, explosion: true, replay: true, taskCount: 48 });
    write(checkpoint, records);
    if (records.length % 12 === 0) console.log(`Browser and views: ${records.length}/144`);
  }
  await page.goto(`${url}/benchmark/exp-d4-arm-2?review=1`);
  await page.waitForFunction(() => (window as any).__benchmark?.().modelId === 'exp-d4-arm-2');
  await page.screenshot({ path: resolve(OUT, 'web-verification/desktop.png') });
  for (const level of [1, 2, 3, 4]) {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(`${url}/benchmark/exp-d${level}-gripper-2?review=1`);
    await page.waitForFunction(id => (window as any).__benchmark?.().modelId === id, `exp-d${level}-gripper-2`);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    await page.getByLabel('审核意见').fill('自动化测试草稿，未提交人工审核');
  }
  await page.screenshot({ path: resolve(OUT, 'web-verification/mobile.png'), fullPage: true });
  assert.deepEqual(errors, []);
  write(resolve(OUT, 'render-audit.json'), { frames: records.flatMap(r => r.frames) });
  write(resolve(OUT, 'web-verification/report.json'), { desktopModels: records.map(({ frames, ...r }) => r),
    mobileModels: 4, errors, wroteHumanReviewDecisions: false });
} finally {
  const timer = setTimeout(() => process.exit(1), 10000);
  await context.close(); await browser.close(); clearTimeout(timer);
}
