// Export original-mesh replay frames, never synthetic depictions of an assembly.
import { chromium, expect } from '@playwright/test';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const out = resolve('benchmark/brickplan-v1/figures');
await mkdir(out, { recursive: true });
const fixtures = JSON.parse(await readFile('tem/brickplan-v1/validation/ui-fixtures.json', 'utf8'));
const fixture = fixtures.find(f => f.mode === 'repair');
const browser = await chromium.launch({ channel: 'chrome', headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1500, height: 1100 }, deviceScaleFactor: 2 });
  await page.goto(`http://127.0.0.1:8766/?session=${fixture.sessionId}`);
  await expect(page.locator('#review')).toBeVisible();
  await page.locator('#site').selectOption('S008');
  const frames = [{ revision: 0, file: 'repair-0.png', label: 'Repair start: three removals are necessary' },
    { revision: 4, file: 'repair-1.png', label: 'Remove P005, P008, and P018' },
    { revision: 5, file: 'repair-2.png', label: 'Insert P003 at S008' },
    { revision: 8, file: 'repair-3.png', label: 'Restore the closures: target assembled' }];
  for (const frame of frames) {
    await page.locator('#replay').focus();
    await page.locator('#replay').press('Home');
    for (let i = 0; i < frame.revision; i++) await page.locator('#replay').press('ArrowRight');
    await expect(page.locator('#revision')).toHaveText(`REV ${String(frame.revision).padStart(3, '0')}`);
    await page.locator('#current-view').screenshot({ path: `${out}/${frame.file}` });
  }
  await writeFile(`${out}/provenance.json`, JSON.stringify({
    sessionId: fixture.sessionId, source: 'Authoritative kart-deck repair replay, original LDraw meshes',
    seed: 31, softwareValidationOnly: true, sourceGeometryModified: false,
    minimumDetaches: 3, structuralActions: 7, frames,
  }, null, 2) + '\n');
} finally { await browser.close(); }
