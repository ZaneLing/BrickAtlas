import { chromium } from '@playwright/test';
import assert from 'node:assert/strict';
import { writeFile, mkdir } from 'node:fs/promises';

const base = 'http://127.0.0.1:5173';
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
const page = await context.newPage();
const errors = [];
const results = [];
page.on('pageerror', error => errors.push(error.message));
try {
  await page.goto(base);
  await page.locator('h1').first().waitFor();
  assert.match(await page.title(), /Brick Atlas/);
  results.push({ route: '/', title: await page.title() });

  await page.goto(`${base}/benchmark/31028`);
  await page.waitForFunction(() => window.__ldrawBench?.().loadedInstances === 53);
  assert.equal(await page.locator('canvas').count() > 0, true);
  await page.getByLabel('基准展开程度').fill('0.6');
  await page.waitForFunction(() => window.__ldrawBench?.().requestedExplosion === 0.6);
  results.push({ route: '/benchmark/31028', loaded_instances: 53, explosion_control: 'passed' });

  await page.goto(`${base}/benchmark/evidence-v3/index.html`);
  await page.locator('#pair-images .observation[data-loaded="true"]').first().waitFor();
  results.push({ route: '/benchmark/evidence-v3/index.html', native_image: 'loaded' });

  await page.goto(`${base}/benchmark/visual-repair-v1/review.html`);
  await page.waitForFunction(() => document.querySelectorAll('#slot option').length === 6);
  assert.equal(await page.locator('#person').inputValue(), '');
  assert.equal(await page.locator('#export').isDisabled(), true);
  // Check the exact queued packet and PNG without recording a human judgment.
  const queue = await (await context.request.get(`${base}/benchmark/visual-repair-v1/qualification-queue.json`)).json();
  const ref = queue.assignments[0].items[0].packet;
  const packetResponse = await context.request.get(`${base}/${ref.path}`);
  assert.equal(packetResponse.ok(), true);
  const packet = await packetResponse.json();
  const png = await context.request.get(`${base}/${packet.images[0].path.replace(/^public\//, '')}`);
  assert.match(png.headers()['content-type'], /image\/png/);
  assert.ok((await png.body()).length > 1000);
  results.push({ route: '/benchmark/visual-repair-v1/review.html', reviewer_slots: 6,
    native_packet: ref.path, png: 'loaded', judgments_written: 0 });

  await page.goto(`${base}/paper/complex-render.html?model=omr-42004`);
  await page.getByText('Loaded', { exact: true }).waitFor({ timeout: 60000 });
  await page.getByRole('button', { name: 'Render source view', exact: true }).click();
  await page.getByText('Ready', { exact: true }).waitFor({ timeout: 30000 });
  results.push({ route: '/paper/complex-render.html', original_geometry_renderer: 'ready' });

  assert.deepEqual(errors, []);
  await mkdir('tem/verification/layout', { recursive: true });
  await page.screenshot({ path: 'tem/verification/layout/source-render.png' });
  await writeFile('tem/repository-layout-20260924/browser-verification.json',
    JSON.stringify({ status: 'passed', engine: 'headless Chrome', results, page_errors: errors }, null, 2) + '\n');
  console.log(JSON.stringify(results, null, 2));
} finally {
  await context.close();
  await browser.close();
}
