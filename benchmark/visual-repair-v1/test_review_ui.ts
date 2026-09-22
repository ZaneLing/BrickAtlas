/// <reference types="node" />
/** Synthetic UI canary only: no judgments, receipts, or human identities saved. */
import { chromium } from '@playwright/test';
import { spawn } from 'node:child_process';
import { resolve } from 'node:path';
import { writeFileSync } from 'node:fs';

const root = resolve(import.meta.dirname, '../..');
const port = process.env.CAPTURE_PORT ?? '5187';
const server = spawn(process.execPath, [resolve(root, 'node_modules/vite/bin/vite.js'),
  '--host', '127.0.0.1', '--port', port, '--strictPort'], { cwd: root });
await new Promise<void>((ready, reject) => {
  server.stdout.on('data', data => { if (String(data).includes(`127.0.0.1:${port}`)) ready(); });
  server.stderr.on('data', data => process.stderr.write(data));
  server.on('error', reject);
  server.on('exit', code => { if (code) reject(new Error(`Vite exit ${code}`)); });
});
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const page = await browser.newPage();
const errors: string[] = [];
page.on('pageerror', error => errors.push(error.message));
try {
  await page.goto(`http://127.0.0.1:${port}/benchmark/visual-repair-v1/review.html`);
  await page.waitForFunction(() => document.querySelector('#status')?.textContent?.includes('504 blinded assignments'));
  if (await page.locator('#slot option').count() !== 6) throw new Error('Wrong reviewer slot count');
  if (!await page.locator('#export').isDisabled()) throw new Error('Export enabled without real judgments');
  await page.locator('#person').fill('UI-CANARY-NOT-A-REVIEWER');
  await page.getByRole('button', { name: 'Start Assigned Queue' }).click();
  await page.waitForFunction(() => {
    const img = document.querySelector<HTMLImageElement>('#evidence');
    return img?.complete && img.naturalWidth === 1600 &&
      document.querySelector('#packet')?.textContent?.includes('fixed_terminals');
  });
  if (await page.locator('#binding option').count() !== 5) throw new Error('Binding options missing');
  if (await page.locator('#flags select').count() !== 4) throw new Error('Qualification flags missing');
  if (await page.locator('#binding').inputValue() !== '') throw new Error('Gold binding prefilled');
  for (const flag of await page.locator('#flags select').all()) {
    if (await flag.inputValue() !== '') throw new Error('Judgment prefilled');
  }
  if (errors.length) throw new Error(errors.join('\n'));
  const report = { status: 'passed', kind: 'synthetic-ui-test-not-human-evidence',
    checks: ['six slots', 'native 1600x900 PNG loaded', 'exact graph packet visible',
      'four quality flags unanswered', 'four binding options unanswered', 'export disabled'],
    judgments_recorded: 0, receipts_saved: 0, browser: browser.version() };
  writeFileSync(resolve(root, 'benchmark/visual-repair-v1/ui-verification.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(report);
} finally {
  await page.close(); await browser.close(); server.kill('SIGTERM');
}
