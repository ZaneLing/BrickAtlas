import { firefox, expect as baseExpect } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const out = path.join(root, 'tem/research/20261009-react-workbench');
const practice = process.env.BRICKPLAN_TEST_URL || 'http://127.0.0.1:8771';
const study = process.env.BRICKPLAN_STUDY_URL || 'http://127.0.0.1:8772';
const site = process.env.BRICKPLAN_STATIC_URL || 'http://127.0.0.1:8781/static-site/';
const expect = baseExpect.configure({ timeout: 30000 });
const report = { status: 'running', errors: [], liveLocalCall: false, studyIsolation: false, staticSubpath: false };
await mkdir(out, { recursive: true });
const browser = await firefox.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1480, height: 1050 } });
page.setDefaultTimeout(30000);
page.on('pageerror', e => report.errors.push(e.message));
try {
  await page.goto(practice + '/#case');
  await expect(page.getByRole('button', { name: '创建运行 Create', exact: true })).toBeEnabled();
  const previous = await (await page.request.get(practice + '/api/models')).json();
  await page.getByLabel('Maximum calls', { exact: true }).fill('1');
  await page.getByRole('button', { name: '创建运行 Create', exact: true }).click();
  await expect(page.getByRole('button', { name: '单步 Step', exact: true })).toBeEnabled();
  const created = await (await page.request.get(practice + '/api/models')).json();
  const id = created.runs.find(r => !previous.runs.some(p => p.id === r.id)).id;
  const initial = await (await page.request.get(`${practice}/api/model-runs/${id}`)).json();
  expect(initial.status).toBe('paused'); expect(initial.steps).toHaveLength(0);
  await page.getByRole('button', { name: '单步 Step', exact: true }).click();
  await expect(page.getByLabel('Model call timeline').locator('button')).toHaveCount(1);
  // One bounded assertion follows a real asynchronous local inference request.
  await expect(page.locator('[class*="_raw_"]')).not.toContainText(/等待模型返回|尚无输出/, { timeout: 170000 });
  await expect(page.getByRole('button', { name: '执行后 After', exact: true })).toBeEnabled();
  const run = await (await page.request.get(`${practice}/api/model-runs/${id}`)).json();
  expect(run.steps).toHaveLength(1); expect(run.steps[0].status).toBe('executed');
  expect(run.steps[0].rawOutput.length).toBeGreaterThan(0);
  expect(run.steps[0].input.imageOrder).toHaveLength(5);
  expect(run.steps[0].usage.inputTokens).toBeGreaterThan(0);
  expect(run.modelWeightsSHA256).toHaveLength(64);
  expect(run.status).toBe('ended'); expect(run.stopReason).toBe('call-budget');
  await expect(page.locator('[class*="_runSidebar_"] button[aria-pressed="true"]')).toContainText('ended');
  await page.getByRole('button', { name: '执行后 After', exact: true }).click();
  await expect(page.locator('canvas')).toHaveCount(2);
  await page.screenshot({ path: path.join(out, 'workbench-live-call.png'), fullPage: true });
  report.liveLocalCall = { runId: id, model: run.model, calls: run.steps.length,
    feedback: run.steps[0].feedback.code, usage: run.steps[0].usage,
    latencySeconds: run.steps[0].latencySeconds, weightsSHA256: run.modelWeightsSHA256,
    scope: 'Integration acceptance only; no aggregate performance claim.' };
  console.log('PASS real local model created without inference, stepped once, ended at budget and exposed evidence');

  await page.goto(study);
  await expect(page.getByRole('button', { name: '开始作答 Start', exact: true })).toBeEnabled();
  await expect(page.locator('nav button')).toHaveCount(1);
  await page.getByRole('button', { name: '开始作答 Start', exact: true }).click();
  await expect(page.getByRole('button', { name: '安装 Attach', exact: true })).toBeEnabled();
  await expect(page.locator('canvas')).toHaveCount(0);
  await expect(page.getByRole('button', { name: '自由 3D', exact: true })).toHaveCount(0);
  const sid = new URL(page.url()).searchParams.get('session');
  const state = await (await page.request.get(`${study}/api/sessions/${sid}`)).json();
  expect(state.observation.images.current.width).toBe(1920);
  const tasks = await (await page.request.get(study + '/api/tasks')).json();
  const denied = ['/api/catalogue', `/api/preview/${tasks.tasks[0].id}`,
    `/api/scene/preview/${tasks.tasks[0].id}`, `/api/sessions/${sid}/scene`,
    '/api/model-runs/case-local/scene', '/api/model-runs/case-local', '/api/models',
    '/download/brickplan-cvpr-overleaf.zip', '/download/brickplan-v2.1-release.zip'];
  for (const endpoint of denied) expect((await page.request.get(study + endpoint)).ok()).toBe(false);
  await page.screenshot({ path: path.join(out, 'workbench-study.png'), fullPage: true });
  report.studyIsolation = { denied, rasterWidth: 1920, canvasCount: 0 };
  console.log('PASS controlled-study native raster UI and blocked scene/demo/download routes');

  await page.goto(site);
  await expect(page.locator('[class*="families"] > button')).toHaveCount(7);
  await expect(page.locator('canvas')).toHaveCount(2);
  const samples = await (await page.request.get(site + 'samples.json')).json();
  for (let i = 0; i < 7; i++) {
    await page.locator('[class*="families"] > button').nth(i).click();
    await expect(page.locator('[class*="_brief_"]')).toContainText(samples[i].id);
    await expect(page.locator('canvas')).toHaveCount(2);
    await expect(page.locator('[data-scene-ready="true"]')).toHaveCount(2);
  }
  await page.getByRole('button', { name: /模型运行/ }).click();
  await expect(page.getByLabel('Model call timeline').locator('button')).toHaveCount(4);
  await expect(page.getByRole('button', { name: '创建运行 Create', exact: true })).toBeDisabled();
  await page.getByRole('button', { name: '高清图 HD', exact: true }).click();
  const images = page.locator('[data-render-mode="raster"] img');
  await expect(images).toHaveCount(2);
  await expect.poll(() => images.evaluateAll(items => items.every(img => img.complete && img.naturalWidth === 1920))).toBe(true);
  await page.getByRole('button', { name: /论文与下载/ }).click();
  for (const label of ['Overleaf ZIP', 'Portable runtime ZIP']) {
    const href = await page.getByRole('link', { name: label, exact: true }).getAttribute('href');
    expect(href.startsWith(site)).toBe(true);
    expect((await page.request.get(href)).ok()).toBe(true);
  }
  await page.screenshot({ path: path.join(out, 'workbench-static.png'), fullPage: true });
  report.staticSubpath = { base: site, families: 7, caseCalls: 4, nativeImageWidth: 1920, downloads: 2 };
  console.log('PASS static deployment under subpath, seven 3D samples, case images and independent downloads');
  expect(report.errors).toEqual([]);
  report.status = 'passed';
} catch (error) {
  report.status = 'failed'; report.errors.push(error.message);
  console.log('FAILED', error.message, page.url());
  await page.screenshot({ path: path.join(out, 'workbench-integration-failure.png'), fullPage: true }).catch(() => {});
  process.exitCode = 1;
} finally {
  await writeFile(path.join(out, 'workbench-integration.json'), JSON.stringify(report, null, 2));
  await browser.close();
}
