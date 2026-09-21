/** Native canvas figures, replayed through the existing application and scorer. */
import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve, relative } from 'node:path';
import { createHash } from 'node:crypto';
import { replay } from '../../src/benchmark/engine';
import type { Task } from '../../src/benchmark/types';

const root = resolve(import.meta.dirname, '../..');
const output = resolve(import.meta.dirname, 'figures/publication-frames');
mkdirSync(output, { recursive: true });
const hash = (p: string) => createHash('sha256').update(readFileSync(p)).digest('hex');
const source = resolve(root, 'benchmark/hierarchy-v3-expanded/models/exp-d1-arm-2.json');
const bundle = JSON.parse(readFileSync(source, 'utf8'));
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const context = await browser.newContext({ viewport: { width: 1900, height: 1200 }, deviceScaleFactor: 2 });
const page = await context.newPage();
page.setDefaultTimeout(15000);
const errors: string[] = [], frames: any[] = [];
page.on('pageerror', e => errors.push(e.message));
try {
  await page.goto(`${process.env.BRICKATLAS_URL ?? 'http://127.0.0.1:5173'}/benchmark/${bundle.model.id}`);
  await page.waitForFunction(id => (window as any).__benchmark?.().modelId === id, bundle.model.id);
  for (const family of ['disassembly', 'service-repair']) {
    const task = bundle.tasks.find((t: Task) => t.family === family) as Task;
    const result = replay(task, task.answer.actionIds);
    assert.equal(result.success, 1);
    await page.getByLabel('选择基准题目').selectOption(task.id);
    await page.getByRole('button', { name: '载入参考答案', exact: true }).click();
    for (const frame of result.frames) {
      await page.getByLabel('动作回放步骤').fill(String(frame.step));
      await page.waitForFunction(ids => JSON.stringify((window as any).__benchmark().visibleModules.sort()) === JSON.stringify(ids), frame.activeModules);
      const encoded = await page.evaluate(() => (window as any).__benchmarkCapture('iso'));
      const file = resolve(output, `${family}-${frame.step}.png`);
      writeFileSync(file, Buffer.from(encoded.split(',')[1], 'base64'));
      frames.push({ family, taskId: task.id, ...frame, file: relative(root, file), sha256: hash(file) });
    }
    const invalidIds = family === 'disassembly' ? ['remove:foundation'] : ['remove:cell-0-tool'];
    const invalid = replay(task, invalidIds);
    assert.equal(invalid.success, 0);
    await page.getByLabel('基准答案 JSON').fill(JSON.stringify({ actionIds: invalidIds }));
    await page.getByLabel('动作回放步骤').fill('1');
    await page.waitForFunction(ids => JSON.stringify((window as any).__benchmark().visibleModules.sort()) === JSON.stringify(ids), invalid.frames[1].activeModules);
    const encoded = await page.evaluate(() => (window as any).__benchmarkCapture('iso'));
    const file = resolve(output, `${family}-invalid.png`);
    writeFileSync(file, Buffer.from(encoded.split(',')[1], 'base64'));
    frames.push({ family, taskId: task.id, ...invalid.frames[1], file: relative(root, file), sha256: hash(file) });
    console.log(`${family}: ${result.frames.length} states and one rejected transition captured`);
  }
  assert.deepEqual(errors, []);
  const sources = [source, import.meta.filename, resolve(root, 'src/benchmark/Scene.ts'), resolve(root, 'src/benchmark/engine.ts')];
  writeFileSync(resolve(import.meta.dirname, 'publication-capture.json'), JSON.stringify({
    method: 'Existing application canvas; reference and rejected programs executed by the shared replay interpreter',
    wroteHumanReviews: false, errors, sources: Object.fromEntries(sources.map(p => [relative(root, p), hash(p)])), frames,
  }, null, 2) + '\n');
} finally {
  await context.close();
  await browser.close();
}
