import { chromium } from '@playwright/test';
import assert from 'node:assert/strict';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { OUT } from './release';
const catalog = JSON.parse(readFileSync(resolve(OUT, 'catalog.json'), 'utf8'));
const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const results: any[] = [], errors: string[] = [];
const output = resolve(OUT, 'web-verification');
mkdirSync(output, { recursive: true });
if (process.argv.includes('--resume')) results.push(...JSON.parse(readFileSync(resolve(output, 'checkpoint.json'), 'utf8')));
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  page.on('pageerror', e => errors.push(e.message));
  await page.goto('http://127.0.0.1:5173/');
  await page.waitForSelector('[data-bench-model]');
  assert.equal(await page.locator('[data-bench-model]').count(), 48);
  for (const m of catalog) {
    if (results.some(r => r.id === m.id)) continue;
    await page.goto(`http://127.0.0.1:5173/benchmark/${m.id}`);
    await page.waitForFunction(id => (window as any).__benchmark?.().modelId === id, m.id);
    const read = () => page.evaluate(() => (window as any).__benchmark());
    const before = await read();
    assert.equal(before.parts, m.parts); assert.equal(before.modules, m.modules); assert.equal(before.contextLost, false);
    await page.getByLabel('基准展开程度').press('End');
    await page.waitForFunction(() => (window as any).__benchmark().explosion === 1);
    const expanded = await read();
    assert.notDeepEqual(before.camera, expanded.camera);
    await page.getByLabel('基准展开程度').press('Home');
    const canvas = await page.locator('.bench-canvas canvas').boundingBox(); assert.ok(canvas);
    const camera0 = (await read()).camera;
    await page.mouse.move(canvas.x + canvas.width * 0.5, canvas.y + canvas.height * 0.5);
    await page.mouse.down(); await page.mouse.move(canvas.x + canvas.width * 0.65, canvas.y + canvas.height * 0.6, { steps: 10 }); await page.mouse.up();
    const rotated = (await read()).camera;
    assert.notDeepEqual(camera0, rotated, `${m.id}: orbit interaction`);
    await page.getByLabel('选择基准题目').selectOption(`h3-${m.id}-assembly`);
    await page.getByRole('button', { name: '载入参考答案', exact: true }).click();
    await page.waitForFunction(() => (window as any).__benchmark().visibleModules.length === 0);
    const bundle = JSON.parse(readFileSync(resolve(OUT, 'models', `${m.id}.json`), 'utf8'));
    const root = bundle.model.modules.find((m: any) => m.anchored);
    await page.getByRole('button', { name: root.name, exact: true }).click();
    assert.equal((await read()).visibleModules.length, 0, `${m.id}: selection resurrected unbuilt modules`);
    await page.getByLabel(`隔离 ${root.id}`, { exact: true }).click();
    assert.equal((await read()).visibleModules.length, 0, `${m.id}: isolation resurrected unbuilt modules`);
    await page.getByRole('button', { name: root.name, exact: true }).click();
    await page.getByLabel('动作回放步骤').press('End');
    await page.waitForFunction(n => (window as any).__benchmark().visibleModules.length === n, m.modules);
    await page.getByRole('button', { name: '检查答案', exact: true }).click();
    assert.equal(await page.locator('p[role=status]').textContent(), '通过');
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    results.push({ id: m.id, parts: m.parts, orbit: true, explosion: true, replay: true, score: true });
    writeFileSync(resolve(output, 'checkpoint.json'), JSON.stringify(results, null, 2));
    if (results.length % 10 === 0) {
      console.log(`${results.length}/48 original-site models verified`);
      writeFileSync(resolve(output, 'checkpoint.json'), JSON.stringify(results, null, 2));
    }
  }
  await page.goto('http://127.0.0.1:5173/benchmark/rotary-excavator');
  await page.waitForFunction(() => (window as any).__benchmark?.().modelId === 'rotary-excavator');
  await page.screenshot({ path: resolve(output, 'desktop.png') });
  for (const id of ['camera-gimbal', 'scissor-service-lift', 'orbital-service-rover', 'automated-recycling-plant']) {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(`http://127.0.0.1:5173/benchmark/${id}`);
    await page.waitForFunction(id => (window as any).__benchmark?.().modelId === id, id);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, `${id}: mobile overflow`);
    assert.ok((await readFileSafe(page)).triangles > 0);
  }
  await page.screenshot({ path: resolve(output, 'mobile.png') });
  assert.deepEqual(errors, []);
  writeFileSync(resolve(output, 'report.json'), JSON.stringify({ desktopModels: results, mobileModels: 4, errors }, null, 2) + '\n');
} finally {
  const timeout = setTimeout(() => { console.error('Browser cleanup timeout'); process.exit(1); }, 10000);
  await browser.close(); clearTimeout(timeout);
}
async function readFileSafe(page: any) { return page.evaluate(() => (window as any).__benchmark()); }
