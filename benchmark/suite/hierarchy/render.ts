import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { chromium } from '@playwright/test';
import { PNG } from 'pngjs';
import { hierarchyModels } from './models';
import { OUTPUT } from './release';
import { hierarchyTasks } from './tasks';

const url = process.env.BRICKATLAS_URL ?? 'http://127.0.0.1:5175';
const executablePath = process.env.CHROME_PATH
  ?? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const hash = (data: Uint8Array) => createHash('sha256').update(data).digest('hex');

function pixelAudit(data: Buffer) {
  const png = PNG.sync.read(data);
  let foreground = 0;
  for (let index = 0; index < png.data.length; index += 4) {
    const distance = Math.abs(png.data[index] - 244)
      + Math.abs(png.data[index + 1] - 246)
      + Math.abs(png.data[index + 2] - 247);
    if (distance > 35 && png.data[index + 3] > 0) foreground++;
  }
  return { width: png.width, height: png.height, foreground };
}

export async function renderHierarchy() {
  const models = hierarchyModels(), tasks = hierarchyTasks();
  mkdirSync(resolve(OUTPUT, 'images/models'), { recursive: true });
  mkdirSync(resolve(OUTPUT, 'images/tasks'), { recursive: true });
  const browser = await chromium.launch({ headless: true, executablePath });
  const page = await browser.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 1 });
  const frames: Array<Record<string, unknown>> = [];
  try {
    await page.goto(`${url}/mechanism-render.html`, { waitUntil: 'networkidle' });
    await page.waitForFunction(() => typeof (window as any).atlasMechanismRender === 'function');
    const render = async (relative: string, frame: unknown, metadata: Record<string, unknown>) => {
      const result = await page.evaluate(payload =>
        (window as any).atlasMechanismRender(payload), frame) as {
          png: string;
          parts: number;
          size: number[];
        };
      const data = Buffer.from(result.png.split(',')[1], 'base64');
      const path = resolve(OUTPUT, relative);
      writeFileSync(path, data);
      const pixels = pixelAudit(data);
      assert.equal(pixels.width, 1200);
      assert.equal(pixels.height, 900);
      assert.ok(pixels.foreground > 10_000, `${relative}: blank`);
      frames.push({
        file: relative,
        sha256: hash(data),
        parts: result.parts,
        size: result.size,
        pixels,
        ...metadata,
      });
    };
    for (const model of models) {
      for (const view of ['iso', 'front', 'side', 'top'] as const) {
        await render(`images/models/${model.id}-${view}.png`, { model, view },
          { type: 'model', sourceGroup: model.id, difficulty: model.difficulty, view });
      }
    }
    for (const task of tasks) {
      const model = models.find(candidate => candidate.id === task.sourceGroup)!;
      await render(task.visualization.detailImage, {
        model,
        view: task.visualization.view,
        highlightModules: task.visualization.highlightModules,
        accessPaths: task.visualization.accessPaths,
        force: task.visualization.force,
      }, {
        type: 'task',
        taskId: task.id,
        sourceGroup: task.sourceGroup,
        difficulty: task.difficulty,
        layer: task.layer,
      });
    }
  } finally {
    await browser.close();
  }
  writeFileSync(resolve(OUTPUT, 'render-audit.json'), JSON.stringify({
    version: 'brickatlas-hierarchy-1',
    renderer: 'Three.js shared mechanism renderer',
    frames,
  }, null, 2) + '\n');
  console.log(JSON.stringify({
    frames: frames.length,
    modelFrames: models.length * 4,
    taskFrames: tasks.length,
  }));
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(import.meta.filename)) {
  await renderHierarchy();
}
