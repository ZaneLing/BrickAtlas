/** Reproducible scientific stimulus capture; never writes an earlier release. */
import { chromium } from '@playwright/test';
import { readFileSync, writeFileSync, mkdirSync, existsSync, copyFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve } from 'node:path';
import { parseArgs } from 'node:util';
import assert from 'node:assert/strict';
import type {} from '../../../src/evidence-v2/render';
const root = resolve(import.meta.dirname, '../../..');
const data = resolve(root, 'benchmark/ldraw-evidence-v2');
const pub = resolve(root, 'public/benchmark/evidence-v2');
const hash = (b: Buffer | string) => createHash('sha256').update(b).digest('hex');
const read = (p: string) => JSON.parse(readFileSync(p, 'utf8'));
const { values } = parseArgs({ options: { limit: { type: 'string' }, model: { type: 'string' },
  verify: { type: 'boolean' }, url: { type: 'string', default: 'http://127.0.0.1:5173' } } });
const manifest = read(resolve(data, 'visual-manifest.json'));
const checkpoint = resolve(data, 'renders.json');
const saved: any[] = existsSync(checkpoint) ? read(checkpoint).images : [];
const codeHash = hash(readFileSync(resolve(root, 'src/evidence-v2/render.ts')));
for (const r of saved) {
  assert.equal(hash(readFileSync(resolve(root, r.file))), r.sha256);
  if (r.kind !== 'preserved-render') assert.equal(r.renderer_sha256, codeHash, 'Renderer changed; create new stimuli version');
}
mkdirSync(resolve(pub, 'images'), { recursive: true });
mkdirSync(resolve(data, 'body-masks'), { recursive: true });
for (const o of manifest.observations.filter((o: any) => o.render_spec.kind === 'preserved-render')) {
  const spec = o.render_spec, bytes = readFileSync(resolve(root, spec.source_file));
  assert.equal(hash(bytes), spec.source_sha256);
  if (saved.some(r => r.observation_id === o.observation_id)) continue;
  const file = `public/benchmark/evidence-v2/images/${o.observation_id}.png`;
  copyFileSync(resolve(root, spec.source_file), resolve(root, file));
  saved.push({ observation_id: o.observation_id, kind: spec.kind, file, sha256: hash(bytes),
    source_file: spec.source_file, source_sha256: spec.source_sha256, metadata: spec });
}
function persist() {
  writeFileSync(checkpoint, JSON.stringify({ dataset: manifest.dataset,
    status: saved.length === manifest.observations.length ? 'rendered-human-qa-pending' : 'in-progress',
    images: saved }, null, 2) + '\n');
}
persist();
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const context = await browser.newContext({ viewport: { width: 1320, height: 900 }, deviceScaleFactor: 1 });
const page = await context.newPage(); page.setDefaultTimeout(30000);
const errors: string[] = []; page.on('pageerror', e => errors.push(e.message));
let count = 0;
try {
  outer: for (const model of [...new Set<string>(manifest.observations.map((o: any) => o.source_id))]) {
    if (values.model && values.model !== model) continue;
    const tasks = manifest.observations.filter((o: any) => o.source_id === model
      && o.render_spec.kind !== 'preserved-render'
      && (values.verify || !saved.some(r => r.observation_id === o.observation_id)));
    if (!tasks.length) continue;
    await page.goto(`${values.url}/evidence-v2-render.html?model=${encodeURIComponent(model)}`);
    await page.waitForFunction(() => /^(Loaded|Error:)/.test(document.querySelector('#status')?.textContent ?? ''));
    assert.equal(await page.locator('#status').textContent(), 'Loaded', errors.join('\n'));
    for (const o of tasks) {
      await page.selectOption('#job', o.observation_id);
      await page.getByRole('button', { name: 'Prepare image', exact: true }).click();
      await page.waitForFunction(() => /^(Ready|Error:)/.test(document.querySelector('#status')?.textContent ?? ''));
      assert.equal(await page.locator('#status').textContent(), 'Ready', errors.join('\n'));
      const result = await page.evaluate(() => window.__evidenceV2Capture!());
      assert.ok(result); assert.equal(result.metadata.observation_id, o.observation_id);
      const bytes = Buffer.from(result.image.split(',')[1], 'base64');
      const file = `public/benchmark/evidence-v2/images/${o.observation_id}.png`;
      const mask = result.mask ? Buffer.from(result.mask.split(',')[1], 'base64') : null;
      if (values.verify) {
        const previous = saved.find(r => r.observation_id === o.observation_id);
        assert.equal(hash(bytes), previous.sha256, `Reproduction failed: ${o.observation_id}`);
        if (mask) assert.equal(hash(mask), previous.mask_sha256);
      } else {
        assert.ok(!existsSync(resolve(root, file)));
        writeFileSync(resolve(root, file), bytes);
        const maskFile = mask ? `benchmark/ldraw-evidence-v2/body-masks/${o.observation_id}.png` : null;
        if (mask) writeFileSync(resolve(root, maskFile!), mask);
        saved.push({ observation_id: o.observation_id, kind: o.render_spec.kind,
          file, sha256: hash(bytes), mask_file: maskFile, mask_sha256: mask ? hash(mask) : null,
          renderer_sha256: codeHash, metadata: result.metadata });
        persist();
      }
      count++;
      console.log(JSON.stringify({ observation: o.observation_id, completed: saved.length, verified: count, total: 347 }));
      if (values.limit && count >= Number(values.limit)) break outer;
    }
  }
  assert.equal(errors.length, 0, errors.join('\n'));
} finally { await context.close(); await browser.close(); }
