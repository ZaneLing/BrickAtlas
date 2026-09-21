/** UI smoke check without creating any human judgments. */
import { chromium } from '@playwright/test';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
const root = resolve(import.meta.dirname, '../../..');
const queue = JSON.parse(readFileSync(resolve(root, 'benchmark/ldraw-evidence-v2/qa/initial/reviewer-1/queue.json'), 'utf8'));
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const context = await browser.newContext({ viewport: { width: 1460, height: 1000 }, acceptDownloads: true });
const page = await context.newPage();
const errors: string[] = []; page.on('pageerror', e => errors.push(e.message));
try {
  await page.goto('http://127.0.0.1:5173/benchmark/ldraw-evidence-v2/qa/initial/reviewer-1/index.html');
  await page.waitForFunction(() => document.querySelector('#progress')?.textContent?.includes('/ 347'));
  assert.equal(await page.locator('#token').textContent(), queue.queue[0].review_id);
  const image = await page.locator('#stimulus').evaluate((img: HTMLImageElement) => ({
    width: img.naturalWidth, height: img.naturalHeight, displayedWidth: img.width, displayedHeight: img.height,
    src: img.src,
  }));
  assert.deepEqual([image.width, image.height, image.displayedWidth, image.displayedHeight], [1280, 800, 1280, 800]);
  assert.equal(createHash('sha256').update(image.src).digest('hex'),
    createHash('sha256').update(queue.queue[0].image).digest('hex'));
  assert.equal(await page.locator('#question').textContent(), queue.queue[0].payload.question);
  await page.getByRole('button', { name: 'Next', exact: true }).click();
  assert.equal(await page.locator('#token').textContent(), queue.queue[1].review_id);
  await page.getByRole('button', { name: 'Previous', exact: true }).click();
  assert.equal(await page.locator('#token').textContent(), queue.queue[0].review_id);
  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Export feedback JSON', exact: true }).click();
  const download = await downloadPromise;
  const file = await download.path(); assert.ok(file);
  const feedback = JSON.parse(readFileSync(file, 'utf8'));
  assert.equal(feedback.reviews.length, 0, 'UI test must not fabricate a human judgment');
  assert.equal(feedback.queue_sha256, createHash('sha256').update(readFileSync(
    resolve(root, 'benchmark/ldraw-evidence-v2/qa/initial/reviewer-1/queue.json'))).digest('hex'));
  assert.equal(errors.length, 0, errors.join('\n'));
  writeFileSync(resolve(root, 'benchmark/ldraw-evidence-v2/qa/ui-validation.json'), JSON.stringify({
    status: 'passed', checks: ['loads all 347 blinded units', 'native image dimensions and exact source',
      'question matches observation', 'next and previous', 'hash-bound JSON export'],
    human_judgments_created: 0, browser_errors: errors,
  }, null, 2) + '\n');
  console.log('QA UI passed; no human judgments created.');
} finally { await context.close(); await browser.close(); }
