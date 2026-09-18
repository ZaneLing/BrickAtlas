import { chromium } from '@playwright/test';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import type {} from '../../../src/benchmark/LDrawBenchmarkPage';
const root = resolve(import.meta.dirname, '../../..'), out = resolve(root, 'benchmark/paper/figures/ldraw');
const bundle = JSON.parse(readFileSync(resolve(root, 'public/benchmark/ldraw/models/omr-42102.json'), 'utf8'));
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const context = await browser.newContext({ viewport: { width: 1600, height: 1000 } });
const page = await context.newPage(), frames: any[] = [];
const capture = async (name: string, taskId: string) => {
  await page.waitForFunction(() => !window.__ldrawBench?.().cameraMoving);
  const encoded = await page.evaluate(() => window.__ldrawCapture!());
  const bytes = Buffer.from(encoded.split(',')[1], 'base64');
  writeFileSync(resolve(out, name + '.png'), bytes);
  frames.push({ file: name + '.png', taskId, sha256: createHash('sha256').update(bytes).digest('hex'),
    snapshot: await page.evaluate(() => { const s = window.__ldrawBench!(); return {
      visibleInstances: s.visibleInstances, labels: s.labels, taskId: s.taskId, offsets: s.offsets,
    }; }) });
};
try {
  const task = bundle.tasks.find((t: any) => t.family === 'source-sequence');
  await page.goto(`http://127.0.0.1:5173/benchmark/omr-42102?task=${task.id}`);
  await page.waitForFunction(() => window.__ldrawBench?.().loadedInstances === 129);
  await page.getByRole('button', { name: '载入参考答案', exact: true }).click();
  for (const n of [1, 3, 6]) {
    await page.getByLabel('操作回放步骤').fill(String(n));
    const count = new Set(task.input.sourceWindow.slice(0, n).flatMap((s: any) => s.instanceIds)).size;
    await page.waitForFunction(count => window.__ldrawBench?.().visibleInstances === count, count);
    await page.getByRole('button', { name: '聚焦题目编号', exact: true }).click();
    await capture(`sequence-${n}`, task.id);
  }
  const repair = bundle.tasks.find((t: any) => t.family === 'restore-instance');
  await page.getByRole('button', { name: `${repair.title} · 待审核`, exact: true }).click();
  await page.getByRole('button', { name: '聚焦题目编号', exact: true }).click();
  await capture('restore-before', repair.id);
  await page.getByRole('button', { name: '载入参考答案', exact: true }).click();
  await page.getByLabel('操作回放步骤').fill('1');
  await page.waitForFunction(() => window.__ldrawBench?.().visibleInstances === 129);
  await capture('restore-after', repair.id);
  await page.getByLabel('基准答案 JSON').fill('{"actionIds":["unknown"]}');
  await page.getByLabel('操作回放步骤').fill('1');
  await page.waitForFunction(() => window.__ldrawBench?.().visibleInstances === 128);
  await capture('restore-invalid', repair.id);
  writeFileSync(resolve(root, 'benchmark/ldraw-v1/worked-renders.json'), JSON.stringify({ frames }, null, 2) + '\n');
} finally { await context.close(); await browser.close(); }
