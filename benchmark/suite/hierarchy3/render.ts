import { chromium } from '@playwright/test';
import { mkdirSync, readFileSync, writeFileSync, copyFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { PNG } from 'pngjs';
import assert from 'node:assert/strict';
import { OUT, WEB, sha } from './release';
const url = process.env.BRICKATLAS_URL ?? 'http://127.0.0.1:5173';
const catalog = JSON.parse(readFileSync(resolve(OUT, 'catalog.json'), 'utf8'));
const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const page = await browser.newPage({ viewport: { width: 1600, height: 1050 } });
const records: any[] = [];
mkdirSync(resolve(OUT, 'images'), { recursive: true }); mkdirSync(resolve(WEB, 'images'), { recursive: true });
try {
  for (const m of catalog) {
    await page.goto(`${url}/benchmark/${m.id}`);
    await page.waitForFunction(id => (window as any).__benchmark?.().modelId === id, m.id);
    // Capture canvas from the same renderer used in the original website.
    for (const view of ['iso', 'front', 'side', 'top']) {
      const encoded = await page.evaluate(view => (window as any).__benchmarkCapture(view), view);
      const path = resolve(OUT, 'images', `${m.id}-${view}.png`);
      const bytes = Buffer.from(encoded.split(',')[1], 'base64'); writeFileSync(path, bytes);
      const png = PNG.sync.read(bytes);
      let contrast = 0;
      for (let i = 0; i < png.data.length; i += 4)
        if (Math.abs(png.data[i] - png.data[i + 2]) > 25) contrast++;
      assert.ok(contrast > 100, `${m.id} ${view}: no colored geometry`);
      copyFileSync(path, resolve(WEB, 'images', `${m.id}-${view}.png`));
      records.push({ file: `images/${m.id}-${view}.png`, sha256: sha(path), contrast,
        width: png.width, height: png.height });
    }
    console.log(`rendered ${m.id}`);
  }
  writeFileSync(resolve(OUT, 'render-audit.json'), JSON.stringify({ frames: records }, null, 2) + '\n');
} finally {
  const timeout = setTimeout(() => { console.error('Browser cleanup timeout'); process.exit(1); }, 10000);
  await browser.close(); clearTimeout(timeout);
}
