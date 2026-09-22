/// <reference types="node" />
import { chromium } from '@playwright/test';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '../..');
const here = resolve(root, 'benchmark/visual-repair-v1');
const assets = resolve(root, 'public/benchmark/visual-repair-v1');
const hash = (x: Buffer | string) => createHash('sha256').update(x).digest('hex');
const specs = JSON.parse(readFileSync(resolve(here, 'render-specs.json'), 'utf8'));
const rendererHash = hash(readFileSync(resolve(here, 'render.ts')));
const specsHash = hash(readFileSync(resolve(here, 'render-specs.json')));
mkdirSync(resolve(assets, 'images'), { recursive: true });
mkdirSync(resolve(assets, 'provenance'), { recursive: true });
const capturePath = resolve(here, 'captures.json');
const previous = existsSync(capturePath) && !process.argv.includes('--restart')
  ? JSON.parse(readFileSync(capturePath, 'utf8')) : null;
if (previous && (previous.renderer_sha256 !== rendererHash || previous.specs_sha256 !== specsHash)) {
  throw new Error('Capture inputs changed; remove only new-version captures explicitly before rerendering.');
}
const frames: any[] = previous?.frames ?? [];
const done = new Set(frames.filter(f => f.id.startsWith('construction-')).map(f => f.id));
const limitArg = process.argv.find(v => v.startsWith('--limit='));
const limit = limitArg ? Number(limitArg.split('=')[1]) : Infinity;
const port = process.env.CAPTURE_PORT ?? '5187';
const modelFor = (cid: unknown) => (Object.values(specs).find((s: any) => s.construction_id === cid) as any).model;
const constructions = [...new Set(Object.values(specs).map((s: any) => s.construction_id))]
  .filter(c => !done.has(c)).sort((a, b) => modelFor(a).localeCompare(modelFor(b))).slice(0, limit);
const server = spawn(process.execPath, [resolve(root, 'node_modules/vite/bin/vite.js'),
  '--host', '127.0.0.1', '--port', port, '--strictPort'], { cwd: root });
await new Promise<void>((ready, reject) => {
  server.stdout.on('data', data => { if (String(data).includes(`127.0.0.1:${port}`)) ready(); });
  server.stderr.on('data', data => process.stderr.write(data));
  server.on('error', reject);
  server.on('exit', code => { if (code) reject(new Error(`Vite exit ${code}`)); });
});
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const page = await browser.newPage({ viewport: { width: 1100, height: 700 }, deviceScaleFactor: 1 });
const errors: string[] = [];
page.on('pageerror', e => errors.push(e.message));
let loaded = '';
try {
  for (const cid of constructions) {
    const spec = Object.values(specs).find((s: any) => s.construction_id === cid) as any;
    if (loaded !== spec.model) {
      await page.goto(`http://127.0.0.1:${port}/benchmark/visual-repair-v1/render.html?model=${spec.model}`);
      await page.waitForFunction(() => /^(Loaded|Error:)/.test(document.querySelector('#status')?.textContent ?? ''),
        undefined, { timeout: 120000 });
      if (await page.locator('#status').textContent() !== 'Loaded') throw new Error('Source load failed');
      const font = await page.evaluate(() => (window as any).__visualRepairFont());
      writeFileSync(resolve(assets, 'font-calibration.png'), Buffer.from(font.split(',')[1], 'base64'));
      loaded = spec.model;
    }
    await page.selectOption('#construction', String(cid));
    await page.getByRole('button', { name: 'Render construction', exact: true }).click();
    await page.waitForFunction(() => /^(Ready|Error:)/.test(document.querySelector('#status')?.textContent ?? ''),
      undefined, { timeout: 60000 });
    if (await page.locator('#status').textContent() !== 'Ready') {
      throw new Error(await page.locator('#status').textContent() ?? 'Capture failed');
    }
    const images = await page.evaluate(() => (window as any).__visualRepairCapture());
    if (!images || images.length !== 7) throw new Error(`Incomplete construction ${cid}`);
    for (const frame of images) {
      const bytes = Buffer.from(frame.image.split(',')[1], 'base64');
      const folder = frame.id.startsWith('construction-') ? 'provenance' : 'images';
      const file = `public/benchmark/visual-repair-v1/${folder}/${frame.id}.png`;
      writeFileSync(resolve(root, file), bytes);
      frames.push({ id: frame.id, file, sha256: hash(bytes), ...frame.metadata });
    }
    writeFileSync(capturePath, JSON.stringify({
      version: 'visual-repair-v1', renderer_sha256: rendererHash, specs_sha256: specsHash,
      browser: browser.version(), frames,
    }, null, 2) + '\n');
    done.add(cid);
    console.log(`${done.size}/84 captured ${cid}, ${frames.length} frames`);
    if (errors.length) throw new Error(errors.join('\n'));
  }
} finally {
  await page.close(); await browser.close();
  server.kill('SIGTERM');
}
