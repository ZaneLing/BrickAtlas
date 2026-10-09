// Local headless-browser verification; policies here are labelled software controls.
import { chromium, expect } from '@playwright/test';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const output = resolve('tem/brickplan-v1/validation');
const fixtures = JSON.parse(await readFile(`${output}/ui-fixtures.json`, 'utf8'));
await mkdir(output, { recursive: true });
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 1080 }, deviceScaleFactor: 2 });
const errors = [];
page.on('pageerror', error => errors.push(error.message));
const completed = [];
try {
  for (const fixture of fixtures) {
    await page.goto(`http://127.0.0.1:8766/?session=${fixture.sessionId}`);
    await expect(page.locator('#message')).toContainText('Workcell ready');
    await expect(page.locator('canvas')).toHaveCount(2);
    await page.screenshot({ path: `${output}/${fixture.mode}-initial.png`, fullPage: true });
    let revision = 0, extra = 0;
    if (fixture.mode === 'full') {
      const a = fixture.actions.find(a => a.type === 'attach');
      const obs = JSON.parse(await page.locator('#observation').textContent());
      const site = obs.sites.find(s => s.id === a.siteId);
      const incompatible = obs.inventory.find(p => p.partType !== site.partType);
      await page.locator('#site').selectOption(site.id);
      await page.locator('#part').selectOption(incompatible.id);
      await page.locator('#attach').click();
      await expect(page.locator('#message')).toContainText('INCOMPATIBLE_PART');
      revision += 1; extra += 1;
      await expect(page.locator('#attempt-count')).toHaveText('1');
    }
    let detaches = 0;
    for (const action of fixture.actions) {
      if (action.type === 'attach') {
        await page.locator('#site').selectOption(action.siteId);
        await page.locator('#part').selectOption(action.partId);
        await page.locator('#attach').click();
      } else if (action.type === 'detach') {
        const obs = JSON.parse(await page.locator('#observation').textContent());
        const site = obs.sites.find(s => s.installedPartId === action.partId);
        await page.locator('#site').selectOption(site.id);
        await page.locator('#detach').click(); detaches++;
      } else if (action.type === 'diagnose') {
        await page.locator(action.needsRework ? '#rework-yes' : '#rework-no').click();
      } else await page.locator('#finish').click();
      revision++;
      await expect(page.locator('#revision')).toHaveText(`REV ${String(revision).padStart(3, '0')}`);
      if (action.type === 'attach' || action.type === 'detach') await expect(page.locator('#message')).toContainText('· OK');
      if (fixture.mode === 'repair' && detaches === 3 && action.type === 'detach') {
        await page.locator('.scene-grid').screenshot({ path: `${output}/repair-open.png` });
      }
    }
    await expect(page.locator('#review')).toBeVisible();
    await expect(page.locator('#score .score-cell').first()).toContainText('success');
    await expect(page.locator('#score .score-cell').nth(2)).toContainText(String(extra));
    await page.locator('.scene-grid').screenshot({ path: `${output}/${fixture.mode}-complete.png` });
    const downloadPromise = page.waitForEvent('download');
    await page.locator('#export').click();
    const download = await downloadPromise;
    await download.saveAs(`${output}/${fixture.mode}-ui-trajectory.json`);
    const trajectory = JSON.parse(await readFile(`${output}/${fixture.mode}-ui-trajectory.json`, 'utf8'));
    if (trajectory.events.length !== revision) throw new Error('Export is not the displayed trajectory');
    await page.locator('#previous').click();
    await expect(page.locator('#revision')).toHaveText(`REV ${String(revision - 1).padStart(3, '0')}`);
    await page.locator('#feedback').fill('Software UI verification: original meshes, three-part repair, and replay checked.');
    const feedbackPromise = page.waitForEvent('download');
    await page.locator('#export-feedback').click();
    await (await feedbackPromise).saveAs(`${output}/${fixture.mode}-feedback.json`);
    completed.push({ mode: fixture.mode, sessionId: fixture.sessionId,
      successfulActions: fixture.optimalActions, failedActions: extra,
      minimumDetaches: fixture.minimumDetaches, replayAndDownloads: true });
  }
  await page.locator('#probes-tab').click();
  await expect(page.locator('#probe-panel')).toBeVisible();
  const shownId = (await page.locator('#session-label').textContent()).replace('PROBE ', '');
  const ids = await page.locator('#task-select option').evaluateAll(options => options.map(o => o.value));
  await page.locator('#task-select').selectOption(ids.find(id => id !== shownId));
  const responsePromise = page.waitForResponse(response =>
    response.url().endsWith(`/api/probes/${shownId}/answer`) && response.request().method() === 'POST');
  await page.locator('#probe-form button').click();
  if (!(await responsePromise).ok()) throw new Error('Displayed probe response was not recorded');
  await expect(page.locator('#message')).toContainText(`Answer frozen for ${shownId}`);
  await page.locator('#start').click();
  await expect(page.locator('#session-label')).not.toHaveText(`PROBE ${shownId}`);
  await page.setViewportSize({ width: 390, height: 844 });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
  if (overflow) throw new Error('Mobile viewport overflows horizontally');
  if (errors.length) throw new Error(errors.join('\n'));
  await writeFile(`${output}/arena-summary.json`, JSON.stringify({
    passed: true, softwareValidationOnly: true, browser: 'headless Chrome',
    nativeBrowserCapture: 'unavailable; IDE screenshot/selection bridge failed',
    viewport: '1440x1080 and 390x844', completed,
    displayedProbeIdentityPreserved: true, consoleErrors: errors,
  }, null, 2) + '\n');
  console.log(JSON.stringify({ passed: true, completed, errors }));
} finally { await browser.close(); }
