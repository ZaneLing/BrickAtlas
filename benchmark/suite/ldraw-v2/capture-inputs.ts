import { chromium } from '@playwright/test';
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { parseArgs } from 'node:util';
import assert from 'node:assert/strict';
import { root, data, site, hash } from './publish';
import type { InternalBundle } from './types';
import type {} from '../../../src/benchmark-v2/render';
const { values } = parseArgs({ options: {
  help: { type: 'boolean' }, model: { type: 'string' }, limit: { type: 'string' },
  verify: { type: 'boolean' },
  url: { type: 'string', default: 'http://127.0.0.1:5173' },
}});
if (values.help) {
  console.log('Usage: tsx capture-inputs.ts [--model ID] [--limit N] [--verify] [--url http://127.0.0.1:5173]\nRenders 140 full/mask/crop/id/camera/wrong pairs plus 67 desaturated type images.\nCheckpoints each task; verifies saved hashes and skips completed task+mode keys.\n--verify rerenders selected tasks and compares bytes without replacing images.');
  process.exit(0);
}
const checkpoint = resolve(data, 'paired-renders.json');
const saved: any[] = existsSync(checkpoint) ? JSON.parse(readFileSync(checkpoint, 'utf8')).images.filter((r: any) => r.version === 2) : [];
for (const row of saved) assert.equal(hash(readFileSync(resolve(root, 'public', row.file))), row.sha256);
const catalog = JSON.parse(readFileSync(resolve(data, 'catalog.json'), 'utf8'));
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const context = await browser.newContext({ viewport: { width: 1320, height: 900 }, deviceScaleFactor: 1 });
const page = await context.newPage();
page.setDefaultTimeout(30000);
const errors: string[] = [];
page.on('pageerror', error => errors.push(error.message));
let doneTasks = 0;
const persist = () => writeFileSync(checkpoint, JSON.stringify({
  version: 'brickatlas-ldraw-2', rendering: 'Original geometry, source poses, canonical camera, white background, no shadows',
  rendererCodeSha256: hash(readFileSync(resolve(root, 'src/benchmark-v2/render.ts'))),
  images: saved, status: saved.length === 907 ? 'machine-rendered-human-review-pending' : 'in-progress',
}, null, 2) + '\n');
try {
  outer: for (const entry of catalog.filter((e: any) => !values.model || e.id === values.model)) {
    const bundle: InternalBundle = JSON.parse(readFileSync(resolve(site, 'models', `${entry.id}.json`), 'utf8'));
    const tasks = bundle.tasks.filter(t => t.visualInput && (values.verify || saved.filter(r => r.taskId === t.id).length < (t.family === 'shape-match' ? 7 : 6)));
    if (!tasks.length) continue;
    await page.goto(`${values.url}/ldraw-v2-render.html?model=${encodeURIComponent(entry.id)}`);
    await page.waitForFunction(() => document.querySelector('#status')?.textContent === 'Loaded'
      || document.querySelector('#status')?.textContent?.startsWith('Error:'));
    assert.equal(await page.locator('#status').textContent(), 'Loaded', errors.join('\n'));
    for (const task of tasks) {
      await page.selectOption('#task', task.id);
      for (const mode of ['full', 'mask', 'crop', 'id', 'camera', 'wrong', ...(task.family === 'shape-match' ? ['neutral'] : [])]) {
        if (!values.verify && saved.some(r => r.taskId === task.id && r.mode === mode)) continue;
        await page.selectOption('#condition', mode);
        await page.getByRole('button', { name: 'Prepare image', exact: true }).click();
        await page.waitForFunction(() => document.querySelector('#status')?.textContent === 'Ready'
          || document.querySelector('#status')?.textContent?.startsWith('Error:'));
        assert.equal(await page.locator('#status').textContent(), 'Ready');
        const result = await page.evaluate(() => window.__v2RenderCapture!());
        assert.equal(result.metadata.taskId, task.id); assert.equal(result.metadata.mode, mode);
        const bytes = Buffer.from(result.image.split(',')[1], 'base64');
        const file = `benchmark/ldraw-v2/inputs/views-${mode}/${task.id}.png`;
        if (values.verify) {
          const previous = saved.find(r => r.taskId === task.id && r.mode === mode);
          if (hash(bytes) !== previous?.sha256) {
            writeFileSync(resolve(data, 'render-reproduction-failure.png'), bytes);
            writeFileSync(resolve(data, 'render-reproduction-failure.json'), JSON.stringify({ previous, actual: result.metadata }, null, 2));
          }
          assert.equal(hash(bytes), previous?.sha256, `Non-reproducible pixels: ${task.id}/${mode}`);
        } else {
          mkdirSync(resolve(root, 'public', file, '..'), { recursive: true });
          writeFileSync(resolve(root, 'public', file), bytes);
          saved.push({ taskId: task.id, mode, file, sha256: hash(bytes), ...result.metadata });
        }
      }
      const full = saved.find(r => r.taskId === task.id && r.mode === 'full');
      const mask = saved.find(r => r.taskId === task.id && r.mode === 'mask');
      assert.deepEqual(full.camera, mask.camera, 'Background mask changed camera');
      assert.deepEqual(full.projections, mask.projections, 'Background mask changed label projections');
      assert.equal(full.visibleInstances, entry.parts);
      assert.equal(mask.visibleInstances, task.references.length);
      persist(); doneTasks++;
      console.log(`${task.id}: paired conditions verified; ${saved.length}/907 images`);
      if (values.limit && doneTasks >= Number(values.limit)) break outer;
    }
  }
  assert.equal(errors.length, 0, errors.join('\n'));
} finally {
  persist(); await context.close(); await browser.close();
}
