import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { PNG } from 'pngjs';

const root = resolve(import.meta.dirname, '../..');
const browser = await chromium.launch({ headless: true, channel: 'chrome' });
const errors: string[] = [], checks: unknown[] = [];
try {
  const page = await browser.newPage();
  page.on('pageerror', e => errors.push(e.message));
  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 900 });
    for (const name of ['index', 'courtyard-museum', 'four-storey-archive']) {
      await page.goto(`file://${root}/frontier-cases/${name}.html`);
      await page.locator('h1').waitFor();
      const state = await page.evaluate(async () => {
        const images = [...document.images]; images.forEach(i => { i.loading = 'eager'; });
        await Promise.all(images.map(i => i.decode()));
        return { overflow: document.documentElement.scrollWidth > innerWidth,
          broken: images.filter(i => !i.naturalWidth).length, images: images.length };
      });
      assert.equal(state.overflow, false); assert.equal(state.broken, 0);
      if (name !== 'index') {
        await page.locator('summary').first().click();
        assert.equal(await page.locator('details').first().getAttribute('open'), '');
      }
      await page.screenshot({ path: `${root}/.runtime/frontier-${name}-${width}.png` });
      checks.push({ width, name, ...state });
    }
  }
  const config = JSON.parse(readFileSync(`${root}/.runtime/suite-server.json`, 'utf8'));
  await page.goto(config.url + '/paper-render.html');
  await page.waitForFunction(() => typeof window.atlasPaperRender === 'function');
  const m = JSON.parse(readFileSync(`${root}/frontier-cases/four-storey-archive.json`, 'utf8'));
  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 900 });
    const results = [];
    for (const view of ['iso', 'front'] as const) {
      const r = await page.evaluate(f => window.atlasPaperRender(f), { parts: m.structure.parts, view });
      const image = PNG.sync.read(Buffer.from(r.png.split(',')[1], 'base64'));
      let count = 0;
      for (let j = 0; j < image.data.length; j += 4) if (image.data[j] < 235) count++;
      assert.ok(count > 1000); results.push(r.png);
    }
    assert.notEqual(results[0], results[1]);
    checks.push({ width, canvasNonblank: true, viewChangesPixels: true });
  }
  assert.deepEqual(errors, []);
} finally { await browser.close(); }
writeFileSync(`${root}/.runtime/frontier-ui.json`, JSON.stringify({ checks, errors }, null, 2) + '\n');
console.log(JSON.stringify({ checks: checks.length, errors }));
