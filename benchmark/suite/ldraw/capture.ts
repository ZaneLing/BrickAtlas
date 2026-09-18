import { chromium } from '@playwright/test';
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import type { LDrawEntry, LDrawBundle } from '../../../src/benchmark/ldrawTypes';
import type {} from '../../../src/benchmark/LDrawBenchmarkPage';

const root = resolve(import.meta.dirname, '../../..'), data = resolve(root, 'benchmark/ldraw-v1');
const out = resolve(root, 'benchmark/paper/figures/ldraw'); mkdirSync(out, { recursive: true });
const catalog: LDrawEntry[] = JSON.parse(readFileSync(resolve(data, 'catalog.json'), 'utf8'));
const file = resolve(data, 'capture.json');
const done: any[] = existsSync(file) ? JSON.parse(readFileSync(file, 'utf8')).models : [];
const numberedOnly = process.argv.includes('--numbered');
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const context = await browser.newContext({ viewport: { width: 1800, height: 1120 }, deviceScaleFactor: 1 });
const page = await context.newPage(); page.setDefaultTimeout(30000);
const errors: string[] = []; page.on('pageerror', error => errors.push(error.message));
const digest = (bytes: Uint8Array) => createHash('sha256').update(bytes).digest('hex');
try {
  for (const entry of catalog) {
    const previous = done.find(r => r.id === entry.id && r.sourceHash === entry.sourceHash);
    if (previous && (!numberedOnly || previous.numberedRenderVersion === 2)) continue;
    await page.goto(`http://127.0.0.1:5173/benchmark/${entry.id}`);
    await page.waitForFunction(n => window.__ldrawBench?.().loadedInstances === n && !!window.__ldrawCapture, entry.parts);
    const images = numberedOnly && previous ? previous.images.filter((i: any) => !i.taskId) : [];
    for (const [view, title] of numberedOnly && previous ? [] : [['iso', '自由视角'], ['front', '正视'], ['side', '侧视'], ['top', '俯视']]) {
      await page.getByRole('button', { name: title, exact: true }).click();
      await page.waitForFunction(() => window.__ldrawBench?.().cameraMoving === false);
      const encoded = await page.evaluate(() => window.__ldrawCapture!());
      const bytes = Buffer.from(encoded.split(',')[1], 'base64'), name = `${entry.id}-${view}.png`;
      writeFileSync(resolve(out, name), bytes); images.push({ file: name, sha256: digest(bytes) });
    }
    const bundle: LDrawBundle = JSON.parse(readFileSync(resolve(root, 'public/benchmark/ldraw/models', `${entry.id}.json`), 'utf8'));
    const visual = bundle.tasks.find(t => t.family === 'shape-match')!;
    await page.getByRole('button', { name: `${visual.title} · 待审核`, exact: true }).click();
    await page.getByRole('button', { name: '隔离题目编号', exact: true }).click();
    await page.waitForFunction(n => window.__ldrawBench?.().visibleInstances === n && !window.__ldrawBench?.().cameraMoving, visual.references.length);
    const metrics = await page.evaluate(() => window.__ldrawBench!());
    assert.equal(metrics.labels.length, visual.references.length);
    const encoded = await page.evaluate(() => window.__ldrawCapture!());
    const bytes = Buffer.from(encoded.split(',')[1], 'base64'), name = `${entry.id}-numbered.png`;
    writeFileSync(resolve(out, name), bytes); images.push({ file: name, sha256: digest(bytes), taskId: visual.id });
    assert.equal(metrics.contextLost, false);
    if (previous) done.splice(done.indexOf(previous), 1);
    done.push({ id: entry.id, sourceHash: entry.sourceHash, loadedInstances: metrics.loadedInstances,
      images, numberedTask: visual.id, numberedLabels: metrics.labels, numberedRenderVersion: 2, errors: [...errors] });
    writeFileSync(file, JSON.stringify({ version: 'brickatlas-ldraw-1', viewport: [1800, 1120], models: done, errors }, null, 2) + '\n');
    console.log(`${done.length}/${catalog.length} ${entry.id}: loaded ${metrics.loadedInstances}, captured 5 views`);
  }
  assert.deepEqual(errors, []);
} finally { await context.close(); await browser.close(); }
