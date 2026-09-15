import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';
import { resolve } from 'node:path';
import { writeFileSync } from 'node:fs';

const root = resolve(import.meta.dirname, '..');
const browser = await chromium.launch({ headless: true, channel: 'chrome' });
const checks: unknown[] = [], errors: string[] = [];
try {
  const page = await browser.newPage();
  page.on('pageerror', e => errors.push(e.message));
  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 900 });
    for (const name of ['index', 'courtyard-museum', 'four-storey-archive']) {
      await page.goto(`file://${root}/diagnostic-v2/${name}.html`);
      await page.locator('h1').waitFor();
      const result = await page.evaluate(async () => {
        const images = [...document.images]; images.forEach(i => { i.loading = 'eager'; });
        await Promise.all(images.map(i => i.decode()));
        return { images: images.length, broken: images.filter(i => !i.naturalWidth).length,
          overflow: document.documentElement.scrollWidth > innerWidth };
      });
      assert.equal(result.broken, 0); assert.equal(result.overflow, false);
      if (name !== 'index') {
        await page.locator('summary').first().click();
        assert.equal(await page.locator('details').first().getAttribute('open'), '');
        await page.evaluate(() => window.scrollTo(0, 0));
      }
      await page.screenshot({ path: `${root}/.runtime/diagnostic-${name}-${width}.png` });
      checks.push({ width, name, ...result });
    }
  }
  assert.deepEqual(errors, []);
} finally { await browser.close(); }
writeFileSync(`${root}/.runtime/diagnostic-ui.json`, JSON.stringify({ checks, errors }, null, 2) + '\n');
console.log(JSON.stringify({ checks: checks.length, errors }));
