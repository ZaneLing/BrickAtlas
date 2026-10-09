// Actual DOM controls, shared executor and authoritative replay. No model trial.
import { chromium, firefox, expect } from '@playwright/test';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const output = resolve('tem/brickplan-v1.1/validation');
const { url, fixtures } = JSON.parse(await readFile(`${output}/ui-fixtures.json`, 'utf8'));
const figures = resolve('benchmark/brickplan-v1.1/figures');
await mkdir(figures, { recursive: true });
const browserName = process.env.BRICKPLAN_BROWSER || 'chrome';
if (!['chrome', 'firefox'].includes(browserName)) throw new Error('Unsupported browser');
console.log(`Launching ${browserName}`);
const browser = await (browserName === 'firefox'
  ? firefox.launch({ headless: true })
  : chromium.launch({ channel: 'chrome', headless: true }));
console.log(`Browser ready: ${browser.version()}`);
const page = await browser.newPage({ viewport: { width: 1440, height: 1080 }, deviceScaleFactor: 2 });
const errors = [], completed = [];
page.on('pageerror', error => errors.push(error.message));
try {
  for (const fixture of fixtures) {
    const key = `${fixture.case}-${fixture.mode}`;
    await page.goto(`${url}/?session=${fixture.sessionId}`);
    await expect(page.locator('#message')).toContainText('Workcell ready');
    await expect(page.locator('canvas')).toHaveCount(2);
    await expect(page.locator('.brand')).toContainText('1.1');
    await page.locator('.scene-grid').screenshot({ path: `${output}/${key}-initial.png` });
    let revision = 0, extra = 0, detaches = 0;
    if (fixture.mode === 'full') {
      const action = fixture.actions.find(a => a.type === 'attach');
      const obs = JSON.parse(await page.locator('#observation').textContent());
      const site = obs.sites.find(s => s.id === action.siteId);
      const wrong = obs.inventory.find(p => p.partType !== site.partType);
      await page.locator('#site').selectOption(site.id);
      await page.locator('#part').selectOption(wrong.id);
      await page.locator('#attach').click();
      await expect(page.locator('#message')).toContainText('INCOMPATIBLE_PART');
      revision++; extra++;
      await expect(page.locator('#attempt-count')).toHaveText('1');
    }
    for (const action of fixture.actions) {
      if (action.type === 'attach') {
        await page.locator('#site').selectOption(action.siteId);
        await page.locator('#part').selectOption(action.partId);
        await page.locator('#attach').click();
      } else if (action.type === 'detach') {
        const obs = JSON.parse(await page.locator('#observation').textContent());
        const site = obs.sites.find(s => s.installedPartId === action.partId);
        await page.locator('#site').selectOption(site.id);
        await page.locator('#detach').click();
        detaches++;
      } else if (action.type === 'diagnose') {
        await page.locator(action.needsRework ? '#rework-yes' : '#rework-no').click();
      } else {
        await page.locator('#finish').click();
      }
      revision++;
      await expect(page.locator('#revision')).toHaveText(`REV ${String(revision).padStart(3, '0')}`);
      if (['attach', 'detach'].includes(action.type)) {
        await expect(page.locator('#message')).toContainText('· OK');
      }
    }
    await expect(page.locator('#review')).toBeVisible();
    await expect(page.locator('#score .score-cell').first()).toContainText('success');
    await expect(page.locator('#score .score-cell').nth(2)).toContainText(String(extra));
    if (detaches !== fixture.minimumDetaches) throw new Error(`Wrong repair work: ${key}`);
    await page.locator('.scene-grid').screenshot({ path: `${output}/${key}-complete.png` });
    const exported = page.waitForEvent('download');
    await page.locator('#export').click();
    await (await exported).saveAs(`${output}/${key}-trajectory.json`);
    const trajectory = JSON.parse(await readFile(`${output}/${key}-trajectory.json`, 'utf8'));
    if (trajectory.events.length !== revision) throw new Error(`Export mismatch: ${key}`);
    await page.locator('#previous').click();
    await expect(page.locator('#revision')).toHaveText(`REV ${String(revision - 1).padStart(3, '0')}`);
    await page.locator('#feedback').fill('Software verification: assembly, repair, identity and replay.');
    const feedback = page.waitForEvent('download');
    await page.locator('#export-feedback').click();
    await (await feedback).saveAs(`${output}/${key}-feedback.json`);
    completed.push({ case: fixture.case, mode: fixture.mode, sessionId: fixture.sessionId,
      successfulActions: fixture.optimalActions, failedActions: extra,
      minimumDetaches: detaches, replayAndDownloads: true });
    if (fixture.case === 'airframe' && fixture.mode === 'repair') {
      const lastRemoval = fixture.actions.reduce((last, a, i) => a.type === 'detach' ? i + 1 : last, 0);
      const insertion = fixture.actions.findIndex((a, i) => i >= lastRemoval && a.type === 'attach');
      const revisions = [0, lastRemoval, insertion + 1, fixture.actions.length - 1];
      const inserted = fixture.actions[insertion];
      await page.locator('#site').selectOption(inserted.siteId);
      const frames = [];
      for (const [i, frameRevision] of revisions.entries()) {
        await page.locator('#replay').focus();
        await page.locator('#replay').press('Home');
        for (let j = 0; j < frameRevision; j++) await page.locator('#replay').press('ArrowRight');
        await expect(page.locator('#revision')).toHaveText(`REV ${String(frameRevision).padStart(3, '0')}`);
        const file = `repair-${i}.png`;
        await page.locator('#current-view').screenshot({ path: `${figures}/${file}` });
        frames.push({ revision: frameRevision, file });
      }
      await writeFile(`${figures}/provenance.json`, JSON.stringify({
        source: 'Authoritative airframe repair replay; original LDraw geometry',
        sessionId: fixture.sessionId, seed: 31, softwareValidationOnly: true,
        sourceGeometryModified: false, minimumDetaches: detaches,
        structuralActions: fixture.optimalActions,
        removedIds: fixture.actions.filter(a => a.type === 'detach').map(a => a.partId),
        inserted, frames,
      }, null, 2) + '\n');
    }
    console.log(JSON.stringify({ verified: key, revision, detaches }));
  }
  await page.locator('#probes-tab').click();
  await expect(page.locator('#probe-panel')).toBeVisible();
  const shown = (await page.locator('#session-label').textContent()).replace('PROBE ', '');
  const ids = await page.locator('#task-select option').evaluateAll(options => options.map(o => o.value));
  await page.locator('#task-select').selectOption(ids.find(id => id !== shown));
  const recorded = page.waitForResponse(r => r.url().endsWith(`/api/probes/${shown}/answer`) && r.request().method() === 'POST');
  await page.locator('#probe-form button').click();
  if (!(await recorded).ok()) throw new Error('Displayed probe was not recorded');
  await expect(page.locator('#message')).toContainText(`Answer frozen for ${shown}`);
  await page.locator('#start').click();
  await expect(page.locator('#session-label')).not.toHaveText(`PROBE ${shown}`);
  await page.setViewportSize({ width: 390, height: 844 });
  if (await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) {
    throw new Error('Mobile horizontal overflow');
  }
  await page.screenshot({ path: `${output}/mobile.png`, fullPage: true });
  if (errors.length) throw new Error(errors.join('\n'));
  await writeFile(`${output}/arena-summary.json`, JSON.stringify({
    passed: true, softwareValidationOnly: true,
    browser: `Playwright, headless ${browserName} ${browser.version()}`,
    viewport: '1440x1080 and 390x844', completed, displayedProbeIdentityPreserved: true,
    consoleErrors: errors,
  }, null, 2) + '\n');
} finally {
  await browser.close();
}
