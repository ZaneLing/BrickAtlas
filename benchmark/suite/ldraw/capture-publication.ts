/** Captionless publication pixels. UI actions only; canvas/snapshot reads are read-only. */
import { chromium } from '@playwright/test';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import type {} from '../../../src/benchmark/LDrawBenchmarkPage';

const root = resolve(import.meta.dirname, '../../..');
const out = resolve(root, 'benchmark/paper/figures/ldraw');
const bundle = JSON.parse(readFileSync(resolve(root, 'public/benchmark/ldraw/models/omr-42102.json'), 'utf8'));
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const page = await browser.newPage({ viewport: { width: 2000, height: 1300 }, deviceScaleFactor: 2 });
const frames: any[] = [];
const capture = async (name: string, taskId: string, expected: number, focus = '聚焦题目编号') => {
  await page.waitForFunction(n => window.__ldrawBench?.().visibleInstances === n, expected);
  // A visibility transition requests auto-fit; reapply the same public focus
  // after every transition so captures share one camera region.
  await page.getByRole('button', { name: focus, exact: true }).click();
  await page.waitForFunction(() => !window.__ldrawBench?.().cameraMoving);
  const encoded = await page.locator('.ldraw-canvas canvas').first().evaluate(
    canvas => (canvas as HTMLCanvasElement).toDataURL('image/png'));
  const bytes = Buffer.from(encoded.split(',')[1], 'base64');
  writeFileSync(resolve(out, name + '.png'), bytes);
  const snapshot = await page.evaluate(() => {
    const s = window.__ldrawBench!();
    return { visibleInstances: s.visibleInstances, taskId: s.taskId, offsets: s.offsets, camera: s.camera, target: s.target };
  });
  frames.push({ file: name + '.png', taskId, sha256: createHash('sha256').update(bytes).digest('hex'), snapshot });
  console.log(JSON.stringify({ frame: name, visible: snapshot.visibleInstances, completed: frames.length }));
};
try {
  const task = bundle.tasks.find((t: any) => t.family === 'source-sequence');
  await page.goto(`http://127.0.0.1:5173/benchmark/omr-42102?task=${task.id}`);
  await page.waitForFunction(() => window.__ldrawBench?.().loadedInstances === 129);
  await page.getByRole('button', { name: '载入参考答案', exact: true }).click();
  // Stable key: action number. Completion: six recorded counts 3,5,8,10,12,14.
  for (let n = 1; n <= 6; n++) {
    await page.getByLabel('操作回放步骤').fill(String(n));
    const count = new Set(task.input.sourceWindow.slice(0, n).flatMap((s: any) => s.instanceIds)).size;
    await capture(`clean-sequence-${n}`, task.id, count);
  }
  const repair = bundle.tasks.find((t: any) => t.family === 'restore-instance');
  await page.getByRole('button', { name: `${repair.title} · 待审核`, exact: true }).click();
  await page.locator('.ldraw-inventory').getByRole('button', { name: 'B0094', exact: true }).click();
  await capture('clean-restore-before', repair.id, 128, '聚焦所选');
  await page.getByRole('button', { name: '载入参考答案', exact: true }).click();
  await page.getByLabel('操作回放步骤').fill('1');
  await capture('clean-restore-after', repair.id, 129, '聚焦所选');
  await page.getByLabel('基准答案 JSON').fill('{"actionIds":["unknown"]}');
  await page.getByLabel('操作回放步骤').fill('1');
  await capture('clean-restore-invalid', repair.id, 128, '聚焦所选');
  for (const group of [frames.slice(0, 6), frames.slice(6)]) {
    for (const frame of group) {
      for (const key of ['camera', 'target']) {
        if (frame.snapshot[key].some((v: number, i: number) => Math.abs(v - group[0].snapshot[key][i]) > .05))
          throw new Error(`Camera framing differs for ${frame.file}`);
      }
    }
  }
  writeFileSync(resolve(root, 'benchmark/ldraw-v1/publication-renders.json'), JSON.stringify({
    modelId: bundle.entry.id, sourceHash: bundle.entry.sourceHash,
    capture: 'Raw renderer canvas only; no text overlay; camera fixed within each sequence; source poses preserved.',
    frames,
  }, null, 2) + '\n');
} finally {
  await page.close();
  await browser.close();
}
