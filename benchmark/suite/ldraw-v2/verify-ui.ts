import { chromium } from '@playwright/test';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { VERSION, emptyBatch, makeRecord, mergeBatch, validateBatch, type ReviewIndex } from '../../../src/benchmark-v2/reviews';
import type {} from '../../../src/benchmark-v2/App';

if (process.argv.includes('--help')) {
  console.log('Usage: tsx verify-ui.ts [--base-url http://127.0.0.1:5173]\nUses a temporary browser context; does not save real human approvals.');
  process.exit(0);
}
const root = resolve(import.meta.dirname, '../../..'), data = resolve(root, 'benchmark/ldraw-v2');
const arg = process.argv.indexOf('--base-url'), base = arg > -1 ? process.argv[arg + 1] : 'http://127.0.0.1:5173';
const read = (p: string) => JSON.parse(readFileSync(resolve(root, p), 'utf8'));
const catalog = read('public/benchmark/ldraw-v2/catalog.json');
const index: ReviewIndex = read('public/benchmark/ldraw-v2/review-index.json');
const blank = emptyBatch(index), unit = index.units[0];
const fixture = { ...blank, records: [makeRecord(unit, 'SOFTWARE-FIXTURE', 'uncertain', 'Temporary implementation test; not human review')] };
assert.equal(validateBatch(fixture, index).records.length, 1);
assert.equal(mergeBatch(fixture, fixture, index).records.length, 1);
const other = { ...fixture, records: [{ ...fixture.records[0], reviewer: 'SECOND-FIXTURE', decision: 'fail' }] };
assert.equal(mergeBatch(fixture, other, index).records.length, 2);
for (const bad of [
  { ...fixture, version: 'brickatlas-ldraw-1' }, { ...fixture, releaseHash: 'stale' },
  { ...fixture, records: [{ ...fixture.records[0], sourceHash: 'stale' }] },
  { ...fixture, records: [{ ...fixture.records[0], contentHash: 'stale' }] },
  { ...fixture, records: [{ ...fixture.records[0], id: 'unknown' }] },
  { ...fixture, records: [{ ...fixture.records[0], rationale: '' }] },
  { ...fixture, records: [{ ...fixture.records[0], operands: [] }] },
  { ...fixture, records: [fixture.records[0], fixture.records[0]] },
]) assert.throws(() => validateBatch(bad, index));
assert.throws(() => mergeBatch(fixture, { ...fixture, records: [{ ...fixture.records[0], rationale: 'Conflicting edit' }] }, index));
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const context = await browser.newContext({ viewport: { width: 1500, height: 1000 }, deviceScaleFactor: 1 });
const page = await context.newPage(), errors: string[] = [], checks: Record<string, unknown> = {};
page.on('pageerror', e => errors.push(String(e)));
const status = async () => page.evaluate(() => {
  const v = window.__ldraw2?.();
  return v ? { modelId: v.modelId, ready: v.ready, unitId: v.unitId, labels: v.labels,
    loaded: v.scene.loadedInstances, visible: v.scene.visibleInstances, explosion: v.scene.actualExplosion,
    moving: v.scene.cameraMoving, camera: v.scene.camera, buildStep: v.scene.buildStep } : null;
});
async function open(model: string, id = '') {
  await page.goto(`${base}/ldraw-v2.html?model=${model}&unit=${id}`);
  await page.waitForFunction(() => window.__ldraw2?.().ready, undefined, { timeout: 30000 });
}
try {
  await open('31028', 'ld2-31028-graph-removal-1');
  await page.getByRole('button', { name: '载入参考答案', exact: true }).click();
  await page.getByRole('button', { name: '检查答案', exact: true }).click();
  assert.equal(await page.locator('.task-panel [role=status]').textContent(), '答案通过');
  await page.getByLabel('答案 JSON', { exact: true }).fill('{"value":1.5}');
  await page.getByRole('button', { name: '检查答案', exact: true }).click();
  assert.match(await page.locator('.task-panel [role=status]').textContent() ?? '', /格式无效/);
  checks.integerScoring = true;
  await page.getByRole('button', { name: '隔离 B0001', exact: true }).click();
  await page.waitForFunction(() => window.__ldraw2?.().scene.visibleInstances === 1);
  assert.deepEqual((await status())!.labels, ['B0001']);
  await page.getByRole('button', { name: '显示全部', exact: true }).click();
  await page.getByLabel('展开程度').focus();
  await page.getByLabel('展开程度').press('End');
  await page.waitForFunction(() => (window.__ldraw2?.().scene.actualExplosion ?? 0) > .89);
  await page.getByLabel('展开程度').press('Home');
  await page.getByRole('button', { name: '正视', exact: true }).click();
  await page.waitForFunction(() => window.__ldraw2?.().scene.cameraMoving === false);
  const cameraA = (await status())!.camera;
  await page.getByRole('button', { name: '侧视', exact: true }).click();
  await page.waitForFunction(() => window.__ldraw2?.().scene.cameraMoving === false);
  assert.notDeepEqual((await status())!.camera, cameraA);
  const canvas = page.locator('.canvas canvas').first(), box = (await canvas.boundingBox())!;
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  await page.mouse.wheel(0, -220);
  await page.waitForFunction(() => window.__ldraw2?.().scene.cameraMoving === false);
  checks.isolationExplosionCameraZoom = true;

  await open('omr-42102', 'ld2-omr-42102-restore-instance-1');
  const initial = (await status())!.visible;
  await page.getByRole('button', { name: '载入参考答案', exact: true }).click();
  await page.getByRole('button', { name: '播放操作', exact: true }).click();
  await page.waitForFunction(n => window.__ldraw2?.().scene.visibleInstances === n + 1, initial);
  const restored = (await status())!.visible;
  await page.getByLabel('答案 JSON', { exact: true }).fill('{"actionIds":["unknown"]}');
  await page.getByRole('button', { name: '播放操作', exact: true }).click();
  await page.waitForFunction(() => document.querySelector('[aria-label="操作回放"]')?.getAttribute('value') === '1');
  assert.equal((await status())!.visible, initial);
  checks.restoration = { initial, restored, rejected: initial };
  await page.getByLabel('选择审核项目').selectOption('ld2-omr-42102-source-sequence-1');
  await page.getByRole('button', { name: '载入参考答案', exact: true }).click();
  await page.getByLabel('操作回放').focus();
  await page.getByLabel('操作回放').press('End');
  await page.getByRole('button', { name: '检查答案', exact: true }).click();
  assert.equal(await page.locator('.task-panel [role=status]').textContent(), '答案通过');
  assert.ok((await status())!.visible > 0);
  checks.sixStepReplay = true;
  await page.getByRole('button', { name: '播放作者步骤', exact: true }).click();
  await page.waitForFunction(() => (window.__ldraw2?.().scene.buildStep ?? 0) >= 1);
  await page.getByRole('button', { name: '暂停作者步骤', exact: true }).click();
  checks.authorReplay = true;

  await open('10156', 'ld2-10156-pair-0001');
  await page.getByRole('button', { name: '隔离当前编号', exact: true }).click();
  await page.waitForFunction(() => window.__ldraw2?.().scene.visibleInstances === 2);
  assert.deepEqual(new Set((await status())!.labels), new Set(['B0082', 'B0094']));
  await page.getByRole('button', { name: '仍待确认', exact: true }).click();
  assert.match(await page.locator('.message').textContent() ?? '', /必须/);
  await page.getByLabel('审核人', { exact: true }).fill('SOFTWARE-FIXTURE');
  await page.getByLabel('判定理由', { exact: true }).fill('Temporary UI fixture; not a human adjudication.');
  await page.getByRole('button', { name: '仍待确认', exact: true }).click();
  await page.reload();
  await page.waitForSelector('.record');
  const downloadWait = page.waitForEvent('download');
  await page.getByRole('button', { name: '导出反馈 JSON', exact: true }).click();
  const downloaded = await downloadWait, exportPath = (await downloaded.path())!;
  const exported = JSON.parse(readFileSync(exportPath, 'utf8'));
  assert.equal(exported.version, VERSION);
  assert.equal(exported.records.length, 1);
  await page.getByRole('button', { name: '撤销此记录', exact: true }).click();
  await page.getByLabel('导入反馈 JSON', { exact: true }).setInputFiles(exportPath);
  await page.waitForSelector('.record');
  assert.match(await page.locator('.message').textContent() ?? '', /合并反馈/);
  await page.getByRole('button', { name: '撤销此记录', exact: true }).click();
  checks.physicalPairAndFeedbackRoundTrip = true;
  checks.reviewValidationCases = 12;
  const models = [];
  for (const m of catalog) {
    await open(m.id);
    const s = (await status())!;
    assert.equal(s.loaded, m.parts);
    assert.equal(s.visible, m.parts);
    models.push({ id: m.id, loaded: s.loaded });
    if (models.length % 4 === 0) console.log(`Verified model loading: ${models.length}/24`);
  }
  checks.models = models;
  await open('omr-42004', 'ld2-omr-42004-shape-match-1');
  for (const c of ['views', 'views-full', 'views-mask', 'views-crop', 'views-camera']) {
    const width = readFileSync(resolve(root, `public/benchmark/ldraw-v2/inputs/${c}/ld2-omr-42004-shape-match-1.png`)).readUInt32BE(16);
    await page.getByLabel('图像条件').selectOption(c);
    await page.waitForFunction(({ width, mode }) => {
      const img = document.querySelector('.frozen img') as HTMLImageElement;
      return img?.complete && img.naturalWidth === width && img.currentSrc.includes(`/${mode}/`);
    }, { width, mode: c });
  }
  mkdirSync(resolve(data, 'ui-captures'), { recursive: true });
  await page.screenshot({ path: resolve(data, 'ui-captures/desktop.png'), fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
  await page.screenshot({ path: resolve(data, 'ui-captures/mobile.png'), fullPage: true });
  checks.pairedImagesAndMobileLayout = true;
  assert.deepEqual(errors, []);
  writeFileSync(resolve(data, 'ui-verification.json'), JSON.stringify({
    status: 'passed', baseUrl: base, checks, pageErrors: errors,
    fixturePolicy: 'Temporary isolated browser context; exported fixture automatically deleted with context. No human review claimed.',
  }, null, 2) + '\n');
  console.log('V2 UI verification passed.');
} catch (error) {
  writeFileSync(resolve(data, 'ui-verification-failure.json'), JSON.stringify({
    status: 'failed', checksCompleted: checks, error: String(error), pageErrors: errors, url: page.url(),
  }, null, 2) + '\n');
  throw error;
} finally {
  await context.close();
  await browser.close();
}
