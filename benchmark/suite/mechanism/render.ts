import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { chromium } from '@playwright/test';
import { PNG } from 'pngjs';
import { mechanismModels } from './models';
import { mechanismTasks } from './tasks';
import { OUTPUT } from './release';

const url = process.env.BRICKATLAS_URL ?? 'http://127.0.0.1:5175';
const executablePath = process.env.CHROME_PATH ?? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const hash = (data: Uint8Array) => createHash('sha256').update(data).digest('hex');

function pixelAudit(data: Buffer) {
  const png = PNG.sync.read(data);
  let foreground = 0, alpha = 0;
  for (let i = 0; i < png.data.length; i += 4) {
    if (png.data[i + 3] > 0) alpha++;
    const distance = Math.abs(png.data[i] - 244) + Math.abs(png.data[i + 1] - 246) + Math.abs(png.data[i + 2] - 247);
    if (distance > 35) foreground++;
  }
  return { width: png.width, height: png.height, foreground, alpha };
}

export async function renderMechanism() {
  const models = mechanismModels(), tasks = await mechanismTasks();
  const modelDir = resolve(OUTPUT, 'images/models'), taskDir = resolve(OUTPUT, 'images/tasks');
  mkdirSync(modelDir, { recursive: true }); mkdirSync(taskDir, { recursive: true });
  const browser = await chromium.launch({ headless: true, executablePath });
  const page = await browser.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 1 });
  const rows: any[] = [];
  try {
    await page.goto(`${url}/mechanism-render.html`, { waitUntil: 'networkidle' });
    await page.waitForFunction(() => typeof (window as any).atlasMechanismRender === 'function');
    const render = async (relative: string, frame: unknown) => {
      const result = await page.evaluate(frame =>
        (window as any).atlasMechanismRender(frame), frame) as { png: string; parts: number; size: number[] };
      const data = Buffer.from(result.png.split(',')[1], 'base64');
      const path = resolve(OUTPUT, relative);
      writeFileSync(path, data);
      const pixels = pixelAudit(data);
      assert.equal(pixels.width, 1200); assert.equal(pixels.height, 900);
      assert.ok(pixels.foreground > 15_000, `${relative}: blank`);
      rows.push({ file: relative, sha256: hash(data), parts: result.parts, size: result.size, pixels });
    };
    for (const model of models) {
      await render(`images/models/${model.id}-iso.png`, { model, view: 'iso' });
      await render(`images/models/${model.id}-front.png`, { model, view: 'front' });
      await render(`images/models/${model.id}-side.png`, { model, view: 'side' });
      await render(`images/models/${model.id}-top.png`, { model, view: 'top' });
    }
    for (const task of tasks) {
      const model = models.find(m => m.id === task.sourceGroup)!;
      const frame: any = { model, view: task.visualization.view,
        highlightModules: task.visualization.highlightModules };
      if (task.kind === 'insertion-access') {
        const allowed = new Set(task.oracle.accessiblePathIds as string[]);
        frame.accessPaths = model.taskConfig.accessPaths.map(path => ({
          start: path.start, end: path.end, accessible: allowed.has(path.id),
        }));
      }
      if (task.kind === 'dynamic-robustness') {
        frame.force = { moduleId: model.taskConfig.loadModule, vector: [4, .7, 1.4] };
      }
      await render(`images/tasks/${model.id}-${task.kind}.png`, frame);
    }
  } finally {
    await browser.close();
  }
  writeFileSync(resolve(OUTPUT, 'render-audit.json'), JSON.stringify({
    version: 'brickatlas-mechanism-1',
    renderer: 'Three.js mechanism renderer',
    frames: rows,
  }, null, 2) + '\n');
  console.log(JSON.stringify({ frames: rows.length, models: models.length, tasks: tasks.length }));
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(import.meta.filename)) {
  await renderMechanism();
}
