/// <reference types="node" />
import { chromium } from '@playwright/test';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve } from 'node:path';
import type {} from './complex-render';

const root = resolve(import.meta.dirname, '..');
const output = resolve(root, 'paper/figures/complex-raw');
mkdirSync(output, { recursive: true });
const cases = JSON.parse(readFileSync(resolve(root, 'benchmark/complex-examples-v1/render-cases.json'), 'utf8'));
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const page = await browser.newPage({ viewport: { width: 1640, height: 1080 }, deviceScaleFactor: 1.5 });
const errors: string[] = [], frames: any[] = [];
page.on('pageerror', e => errors.push(e.message));
try {
  for (const model of ['omr-42004', 'omr-42061']) {
    await page.goto(`http://127.0.0.1:5173/paper/complex-render.html?model=${model}`);
    await page.waitForFunction(() => /^(Loaded|Error:)/.test(document.querySelector('#status')?.textContent ?? ''), undefined, { timeout: 60000 });
    if (await page.locator('#status').textContent() !== 'Loaded') throw new Error(await page.locator('#status').textContent() ?? 'Load failed');
    for (const [id, spec] of Object.entries(cases) as [string, any][]) {
      if (spec.model !== model) continue;
      await page.selectOption('#case', id);
      await page.getByRole('button', { name: 'Render source view', exact: true }).click();
      await page.waitForFunction(() => /^(Ready|Error:)/.test(document.querySelector('#status')?.textContent ?? ''));
      const data = await page.evaluate(() => window.__complexCapture?.());
      if (!data || data.metadata.id !== id || await page.locator('#status').textContent() !== 'Ready') throw new Error(`Capture failed: ${id}`);
      const bytes = Buffer.from(data.image.split(',')[1], 'base64');
      const file = `paper/figures/complex-raw/${id}.png`;
      writeFileSync(resolve(root, file), bytes);
      frames.push({ file, sha256: createHash('sha256').update(bytes).digest('hex'), ...data.metadata });
      writeFileSync(resolve(output, 'captures.json'), JSON.stringify({
        source: 'Original AtlasScene meshes, material colors and source poses; no physical fault rendering.',
        renderer_sha256: createHash('sha256').update(readFileSync(resolve(root, 'paper/complex-render.ts'))).digest('hex'),
        frames,
      }, null, 2) + '\n');
      console.log(`${id}: ${data.metadata.visibleCount} source parts captured`);
    }
  }
  if (errors.length) throw new Error(errors.join('\n'));
} finally { await page.close(); await browser.close(); }
