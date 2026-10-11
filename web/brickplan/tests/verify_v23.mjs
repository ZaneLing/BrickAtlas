import { firefox, expect as baseExpect } from '@playwright/test';
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { downloadedJSON, evidence, root, out } from './evidence.mjs';

const tested = await evidence();
const urls = JSON.parse(await readFile(path.join(out, 'services.json')));
const workflow = JSON.parse(await readFile(path.join(out, 'workflow-validation.json')));
const apiReport = JSON.parse(await readFile(path.join(out, 'api-validation.json')));
const expect = baseExpect.configure({ timeout: 30000 });
const browser = await firefox.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1480, height: 1050 } });
page.setDefaultTimeout(30000);
const checks = [], errors = [], timings = {};
const integration = { historicalCaseReplay: false, staticMultiview: false, activeAcquisition: false,
  studyIsolation: false, staticSubpath: false, newModelInference: false };
page.on('pageerror', error => errors.push(error.message));
const check = name => { checks.push(name); console.log('PASS', name); };
const idle = () => expect(page.getByRole('status')).not.toContainText('Working');
async function nativeImages() {
  await expect.poll(() => page.locator('[data-render-mode="raster"] img').evaluateAll(
    images => images.length === 2 && images.every(img => img.complete && img.naturalWidth === 1920))).toBe(true);
}
async function inspectPiece(targetPage, touch = false) {
  const canvas = targetPage.locator('canvas').first();
  await canvas.scrollIntoViewIfNeeded();
  const box = await canvas.boundingBox();
  // Sample only visible canvas coordinates; no renderer/framework internals.
  for (const [x, y] of [[.5, .62], [.5, .5], [.4, .5], [.6, .5], [.5, .4]]) {
    if (touch) await targetPage.touchscreen.tap(box.x + box.width * x, box.y + box.height * y);
    else await targetPage.mouse.move(box.x + box.width * x, box.y + box.height * y);
    if (await targetPage.locator('.scene-tooltip:visible').count()) break;
  }
  await expect(targetPage.locator('.scene-tooltip:visible')).toHaveCount(1);
  await expect(targetPage.locator('.scene-tooltip:visible')).toContainText(/LDraw/);
}
let bankHash, status = 'failed';
try {
  expect(workflow.status).toBe('passed');
  expect(workflow.errors).toEqual([]);
  for (const key of ['bankHash', 'bankFileSha256', 'frontendFiles']) expect(workflow[key]).toEqual(tested[key]);
  expect(apiReport.status).toBe('passed');
  expect(apiReport.bankHash).toBe(tested.bankHash);
  const cat = await (await page.request.get(urls.practice + '/api/catalogue')).json();
  bankHash = cat.bankHash;
  expect(bankHash).toBe(tested.bankHash);
  expect(bankHash).toBe(urls.bankHash);
  expect(cat.release).toBe('2.3');
  expect(cat.questions).toHaveLength(cat.counts.episodes + cat.counts.probes);
  const episode = cat.questions.find(q => q.stableId === 'kart-deck-08').id;
  await page.goto(`${urls.practice}/#q=${episode}`);
  await expect(page.locator('[class*="families"] > button')).toHaveCount(cat.taxonomy.length);
  await expect(page.locator('[class*="_census_"]')).toContainText(String(cat.counts.episodes));
  await expect(page.locator('[class*="_census_"]')).toContainText(String(cat.counts.probes));
  await expect(page.locator('[class*="_census_"]')).toContainText(String(cat.counts.sources));
  await expect(page.locator('[data-scene-ready="true"]')).toHaveCount(2);
  check('Current-bank census and all task families render in the v2.3 workbench');
  await expect(page.locator('.scene-labels')).toHaveCount(0);
  await expect(page.locator('.scene-tooltip:visible')).toHaveCount(0);
  await inspectPiece(page);
  await page.getByRole('heading', { level: 1 }).hover();
  await expect(page.locator('.scene-tooltip:visible')).toHaveCount(0);
  await page.locator('canvas').first().focus();
  await page.keyboard.press('ArrowRight');
  await expect(page.locator('.scene-tooltip:visible')).toHaveCount(1);
  await page.keyboard.press('Escape');
  await expect(page.locator('.scene-tooltip:visible')).toHaveCount(0);
  check('No persistent part IDs; raycast hover and keyboard inspection show and dismiss one detail card');
  await expect(page.locator('[class*="_previewFooter_"]')).toContainText('registered pieces');
  const started = performance.now();
  await page.getByRole('button', { name: '高清图 HD', exact: true }).click();
  await nativeImages();
  timings.hdSwitchMs = Math.round(performance.now() - started);
  expect(timings.hdSwitchMs).toBeLessThan(1500);
  await page.getByRole('button', { name: '放大 当前结构 Current', exact: true }).click();
  await page.getByRole('button', { name: '原生像素 1:1', exact: true }).click();
  expect(await page.getByRole('dialog').locator('img').evaluate(img => [img.naturalWidth, img.clientWidth])).toEqual([1920, 1920]);
  await page.getByRole('button', { name: '关闭 Close', exact: true }).click();
  check('Fast preloaded HD switch and 1920-pixel native image zoom');
  await page.getByRole('button', { name: '自由 3D', exact: true }).click();
  for (const cohort of cat.cohorts) {
    await page.locator('[class*="families"] > button').nth(cat.taxonomy.findIndex(f => f.id === 'geometry')).click();
    await page.getByLabel('Geometry cohort', { exact: true }).selectOption(cohort.id);
    await expect(page.locator('[class*="_listCaption_"]')).toContainText(`${cohort.probes} questions`);
    await page.locator('[class*="_questionRow_"]').first().click();
    await expect(page.locator(`[data-cohort="${cohort.id}"]`)).toContainText(cohort.label.en);
    await expect(page.locator('[data-provenance]')).toContainText('Practice provenance');
    await expect(page.locator('[data-scene-ready="true"]')).toHaveCount(2);
    await page.screenshot({ path: path.join(out, `${cohort.id}.png`), fullPage: true });
  }
  integration.cohorts = cat.cohorts;
  check('Primary matched and historical unmatched geometry are separately counted, filtered and labeled');
  await page.goto(`${urls.practice}/play?probe=${urls.probe}`);
  await expect(page.getByLabel('Probe answer', { exact: true })).toBeEnabled();
  await expect(page.getByRole('button', { name: '获取并记录 Acquire', exact: true })).toHaveCount(0);
  const observation = await (await page.request.get(`${urls.practice}/api/probes/${urls.probe}`)).json();
  const views = observation.observation.inspectionHistory;
  expect(observation.observation.observationProtocol.initialViews).toEqual(['isometric', 'left', 'rear', 'right']);
  await expect(page.getByLabel('View history').locator('li')).toHaveCount(views.length);
  check('Four-digit probe loads initial history and static protocol without an acquisition control');
  for (let i = 0; i < views.length; i++) {
    expect(views[i].atRevision).toBe(0);
    await page.getByLabel('Saved view', { exact: true }).selectOption(String(i));
    await nativeImages();
    await expect(page.getByLabel('Probe answer', { exact: true })).toBeEnabled();
    expect(await page.locator('[data-render-mode="raster"] img').first().getAttribute('src')).toContain(views[i].images.current.url);
  }
  await page.screenshot({ path: path.join(out, 'static-multiview.png'), fullPage: true });
  integration.staticMultiview = { probe: urls.probe, initialViews: ['isometric', ...views.map(v => v.view)], acquisitionCost: 0 };
  check('Supplied left/rear/right images switch without spending budget or blocking answers');
  await expect(page.getByRole('button', { name: /放大 Pre-error checkpoint/ })).toHaveCount(1);
  const checkpointImage = page.getByRole('button', { name: /放大 Pre-error checkpoint/ }).locator('img');
  expect(await checkpointImage.getAttribute('src')).toContain(observation.repairContext.checkpointObservation.inspectionHistory.at(-1).images.current.url);
  check('Repair checkpoint switches to the matching supplied view');
  await page.getByLabel('Probe answer', { exact: true }).selectOption('0');
  await page.getByRole('button', { name: '提交答案 Submit', exact: true }).click();
  await idle();
  await expect(page.getByText('答案已冻结 / Answer frozen', { exact: true })).toBeVisible();
  const reviewed = await (await page.request.get(`${urls.practice}/api/probes/${urls.probe}/review`)).json();
  expect(['calibration', 'discriminative']).toContain(reviewed.scoringRole);
  await page.reload();
  await expect(page.getByText('答案已冻结 / Answer frozen', { exact: true })).toBeVisible();
  check('Answer submits while a supplied view is selected, freezes, and exposes scoring role only in review');
  await page.goto(`${urls.active}/play?probe=${urls.probe}`);
  await expect(page.getByLabel('Probe answer', { exact: true })).toBeEnabled();
  await expect(page.locator('header')).toContainText('image-id-active');
  const before = await (await page.request.get(`${urls.active}/api/probes/${urls.probe}`)).json();
  expect(before.observation.inspectionHistory).toHaveLength(0);
  await page.getByLabel('Acquisition view', { exact: true }).selectOption('left');
  await page.getByRole('button', { name: '获取并记录 Acquire', exact: true }).click();
  await idle();
  const after = await (await page.request.get(`${urls.active}/api/probes/${urls.probe}`)).json();
  expect(after.observation.remainingViews).toBe(before.observation.remainingViews - 1);
  expect(after.observation.observationProtocol.acquiredViews).toBe(1);
  expect(after.observation.inspectionHistory[0].atRevision).toBe(1);
  expect(after.observation.inspectionHistory[0].frameId).toBe('view-1-left');
  await page.getByLabel('Saved view', { exact: true }).selectOption('0');
  await expect(page.getByLabel('Probe answer', { exact: true })).toBeDisabled();
  await page.getByRole('button', { name: '返回当前 Return to live', exact: true }).click();
  await expect(page.getByLabel('Probe answer', { exact: true })).toBeEnabled();
  integration.activeAcquisition = { track: after.observation.track, acquiredViews: 1, cost: 1 };
  check('Active condition starts isometric and charges exactly one unit for an acquired view');
  await page.goto(`${urls.study}/play?probe=${urls.probe}`);
  await expect(page.getByLabel('Probe answer', { exact: true })).toBeEnabled();
  await page.getByLabel('Saved view', { exact: true }).selectOption('1');
  await nativeImages();
  await expect(page.locator('canvas')).toHaveCount(0);
  await expect(page.getByRole('button', { name: '自由 3D', exact: true })).toHaveCount(0);
  await expect(page.locator('[data-cohort], [data-provenance]')).toHaveCount(0);
  const denied = ['/api/catalogue', `/api/preview/${urls.probe}`, `/api/scene/preview/${urls.probe}`,
    '/api/models', '/api/model-runs/case-local', '/download/brickplan-v2.3-release.zip'];
  for (const endpoint of denied) expect((await page.request.get(urls.study + endpoint)).ok()).toBe(false);
  integration.studyIsolation = { denied, canvasCount: 0, nativeImageWidth: 1920 };
  check('Controlled study retains native multiview images and blocks practice/model/download routes');
  await page.goto(urls.practice + '/#case');
  const trace = JSON.parse(await readFile(path.join(root, 'benchmark/brickplan-v2.3/cases/local-vlm.json')));
  await expect(page.getByLabel('Model call timeline').locator('button')).toHaveCount(trace.steps.length);
  await expect(page.getByText(/Historical BrickPlan 2.1 trace/)).toBeVisible();
  await page.getByRole('button', { name: 'Next model step', exact: true }).click();
  await page.getByRole('button', { name: '执行后 After', exact: true }).click();
  await expect(page.locator('[class*="_callDetail_"]')).toContainText('INVALID_ACTION');
  await expect(page.locator('[data-scene-ready="true"]')).toHaveCount(2);
  integration.historicalCaseReplay = { release: '2.1', calls: trace.steps.length, newMeasurement: false };
  check('Historical 2.1 case label, exact recorded calls, raw output and after-state replay');
  await page.goto(urls.static);
  const samples = await (await page.request.get(urls.static + 'samples.json')).json();
  expect((await (await page.request.get(urls.static + 'catalogue.json')).json()).bankHash).toBe(bankHash);
  expect(samples.find(s => s.category === 'geometry').evaluationCohort).toBe('primary-matched');
  for (const sample of samples) {
    await page.locator('[class*="families"] > button').nth(cat.taxonomy.findIndex(f => f.id === sample.category)).click();
    await expect(page.locator('[class*="_brief_"]')).toContainText(sample.id);
    await expect(page.locator('[data-scene-ready="true"]')).toHaveCount(2);
  }
  check('All exported family samples render original 3D scenes under a static subpath');
  await page.getByRole('button', { name: /模型运行/ }).click();
  await expect(page.getByLabel('Model call timeline').locator('button')).toHaveCount(trace.steps.length);
  await expect(page.getByRole('button', { name: '创建运行 Create', exact: true })).toBeDisabled();
  await page.getByRole('button', { name: '高清图 HD', exact: true }).click();
  await nativeImages();
  const hostedTrace = await (await page.request.get(urls.static + 'cases/local-vlm.json')).body();
  expect(hostedTrace.equals(await readFile(path.join(root, 'benchmark/brickplan-v2.3/cases/local-vlm.json')))).toBe(true);
  expect(await downloadedJSON(page, page.getByRole('button', { name: '导出', exact: true }))).toEqual(trace);
  integration.staticSubpath = { base: urls.static, families: samples.length, historicalTraceBytesUnchanged: true, nativeImageWidth: 1920 };
  check('Static historical trace stays byte-identical while its native image URLs resolve');
  await page.getByRole('button', { name: /论文与下载/ }).click();
  const portable = await page.getByRole('link', { name: 'Portable runtime ZIP', exact: true }).getAttribute('href');
  expect(portable).toBe(urls.static + 'brickplan-v2.3-release.zip');
  await expect(page.getByRole('link', { name: /公开题库 JSONL/ })).toContainText(String(cat.questions.length));
  check('Release page derives counts and v2.3 download paths from the current catalogue');
  const touch = await browser.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true });
  await touch.goto(`${urls.practice}/#q=${episode}`);
  await expect(touch.locator('[data-scene-ready="true"]')).toHaveCount(2);
  await inspectPiece(touch, true);
  expect(await touch.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await touch.screenshot({ path: path.join(out, 'touch-details.png'), fullPage: true });
  await touch.close();
  check('Touch inspection reveals one original-piece detail card without horizontal overflow');
  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole('button', { name: '打开导航 Open navigation', exact: true }).click();
  await page.getByRole('dialog').getByRole('button', { name: /题目库/ }).click();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await page.screenshot({ path: path.join(out, 'mobile.png'), fullPage: true });
  check('Mobile navigation and catalogue fit without horizontal overflow');
  await page.locator('[class*="families"] > button').nth(cat.taxonomy.findIndex(f => f.id === 'geometry')).click();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  expect(await evidence()).toEqual(tested);
  expect(errors).toEqual([]);
  status = 'passed';
} catch (error) {
  errors.push(error.message);
  console.error('FAILED', error.message, page.url());
  await page.screenshot({ path: path.join(out, 'failure.png'), fullPage: true }).catch(() => {});
  process.exitCode = 1;
} finally {
  await writeFile(path.join(out, 'workbench-validation.json'), JSON.stringify({ status, browser: 'Firefox',
    ...tested, bankHash, checks: [...apiReport.checks, ...workflow.checks, ...checks], errors, timings,
    testedAt: new Date().toISOString() }, null, 2));
  await writeFile(path.join(out, 'workbench-integration.json'), JSON.stringify({ status, ...tested, bankHash, errors,
    ...integration, finalDownloadsVerified: false, note: 'Final PDF/Overleaf/runtime archives are pending main-agent publication; URL wiring verified.' }, null, 2));
  await browser.close();
}
