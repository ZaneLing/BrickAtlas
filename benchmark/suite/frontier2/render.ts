import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { chromium } from '@playwright/test';
import { PNG } from 'pngjs';
import { maintenanceCases } from './maintenance';
import { insertion, removal } from '../frontier/geometry';
import type { PaperFrame } from '../web/paper-render';

const root = resolve(import.meta.dirname, '../..'), output = resolve(root, 'diagnostic-v2/images');
const config = JSON.parse(readFileSync(resolve(root, '.runtime/suite-server.json'), 'utf8'));
const browser = await chromium.launch({ headless: true, channel: 'chrome' });
const checks: unknown[] = [];
try {
  const page = await browser.newPage({ viewport: { width: 1000, height: 750 } });
  await page.goto(config.url + '/paper-render.html');
  await page.waitForFunction(() => typeof window.atlasPaperRender === 'function');
  for (const c of maintenanceCases().filter(c => c.context === 'full' && c.tier === 2)) {
    let state = structuredClone(c.current.parts);
    const render = async (step: string) => {
      const frame: PaperFrame = { parts: state, frameParts: c.target.parts, highlightIds: c.faultIds };
      const result = await page.evaluate(f => window.atlasPaperRender(f), frame);
      const png = Buffer.from(result.png.split(',')[1], 'base64'), image = PNG.sync.read(png);
      let foreground = 0, edge = 0;
      for (let i = 0; i < image.data.length; i += 4) if (image.data[i] < 235 || image.data[i+1] < 235 || image.data[i+2] < 235) {
        foreground++;
        const x = i/4 % image.width, y = Math.floor(i/4/image.width);
        if (x < 2 || y < 2 || x >= image.width-2 || y >= image.height-2) edge++;
      }
      assert.ok(foreground > 1000 && edge === 0);
      const name = `${c.id}-${step}.png`;
      writeFileSync(resolve(output, name), png);
      checks.push({ caseId: c.id, step, name, foreground, edge, parts: state.length });
    };
    await render('before');
    const inventory = new Map();
    for (const [i, action] of c.oracle.repair.actions.entries()) {
      if (action.op === 'remove') {
        assert.equal(removal(state, action.id), null);
        inventory.set(action.id, state.find(p => p.id === action.id));
        state = state.filter(p => p.id !== action.id);
      } else {
        const p = action.part ?? inventory.get(action.id);
        assert.equal(insertion(state, p), null); state.push(p); inventory.delete(action.id);
      }
      if (i + 1 === c.oracle.access.removeIds.length) await render('opened');
    }
    await render('repaired');
  }
} finally { await browser.close(); }
writeFileSync(resolve(root, 'diagnostic-v2/render-checks.json'), JSON.stringify(checks, null, 2) + '\n');
console.log(JSON.stringify({ replayFrames: checks.length, nonblankAndUnclipped: true }));
