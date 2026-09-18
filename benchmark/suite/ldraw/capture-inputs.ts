import { chromium } from '@playwright/test';
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import type { LDrawBundle } from '../../../src/benchmark/ldrawTypes';
import type {} from '../../../src/benchmark/LDrawBenchmarkPage';
const root = resolve(import.meta.dirname, '../../..'), site = resolve(root, 'public/benchmark/ldraw');
const data = resolve(root, 'benchmark/ldraw-v1');
mkdirSync(resolve(site, 'inputs/views'), { recursive: true });
const catalog = JSON.parse(readFileSync(resolve(data, 'catalog.json'), 'utf8'));
const checkpoint = resolve(data, 'input-renders.json');
const done: any[] = existsSync(checkpoint) ? JSON.parse(readFileSync(checkpoint, 'utf8')).images.filter((r: any) => r.renderVersion === 2) : [];
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const context = await browser.newContext({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1 });
const page = await context.newPage(); page.setDefaultTimeout(30000);
try {
  for (const entry of catalog) {
    const bundle: LDrawBundle = JSON.parse(readFileSync(resolve(site, 'models', `${entry.id}.json`), 'utf8'));
    const tasks = bundle.tasks.filter(t => t.visualInput && !done.some(r => r.taskId === t.id));
    if (!tasks.length) continue;
    await page.goto(`http://127.0.0.1:5173/benchmark/${entry.id}`);
    await page.waitForFunction(n => window.__ldrawBench?.().loadedInstances === n, entry.parts);
    for (const task of tasks) {
      await page.getByRole('button', { name: `${task.title} · 待审核`, exact: true }).click();
      await page.getByRole('button', { name: '隔离题目编号', exact: true }).click();
      await page.getByRole('button', { name: '自由视角', exact: true }).click();
      await page.waitForFunction(n => window.__ldrawBench?.().visibleInstances === n && !window.__ldrawBench?.().cameraMoving, task.references.length).catch(async e => {
        console.error(JSON.stringify({ taskId: task.id, expected: task.references.length,
          observed: await page.evaluate(() => { const s = window.__ldrawBench?.(); return {
            visible: s?.visibleInstances, cameraMoving: s?.cameraMoving, taskId: s?.taskId,
            labels: s?.labels, alert: document.querySelector('[role=alert]')?.textContent,
          }; }) }));
        throw e;
      });
      const encoded = await page.evaluate(() => window.__ldrawCapture!());
      const bytes = Buffer.from(encoded.split(',')[1], 'base64');
      writeFileSync(resolve(root, 'public', task.visualInput!.numberedView), bytes);
      done.push({ taskId: task.id, sourceHash: entry.sourceHash, file: task.visualInput!.numberedView,
        sha256: createHash('sha256').update(bytes).digest('hex'), references: task.references,
        mode: 'isolated-original-poses-numbered', renderVersion: 2 });
    }
    writeFileSync(checkpoint, JSON.stringify({ version: 'brickatlas-ldraw-1', images: done }, null, 2) + '\n');
    console.log(`${entry.id}: ${tasks.length} visual inputs, ${done.length} total`);
  }
} finally { await context.close(); await browser.close(); }
