import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { readFile } from 'node:fs/promises';

test('numbered original geometry, author replay and review round trip preserve old feedback', async ({ page, request }) => {
  const catalog = await (await request.get('/benchmark/ldraw/catalog.json')).json();
  const total = catalog.reduce((s: number, m: any) => s + m.tasks, 0);
  const bundle = await (await request.get('/benchmark/ldraw/models/omr-42102.json')).json();
  const old = 'old feedback must stay byte identical';
  await page.addInitScript(value => {
    if (!localStorage.getItem('brickatlas:hierarchy3:reviews:v1')) localStorage.setItem('brickatlas:hierarchy3:reviews:v1', value);
  }, old);
  await page.goto('/benchmark/omr-42102?review=1');
  await page.waitForFunction(() => window.__ldrawBench?.().loadedInstances === 129);
  const task = bundle.tasks[0];
  await expect(page.getByRole('heading', { name: task.title })).toBeVisible();
  await expect.poll(() => page.evaluate(() => window.__ldrawBench?.().labels)).toContain(task.references[0].label);
  await page.locator('.ldraw-ref-list').getByRole('button', { name: task.references[0].label, exact: true }).click();
  await expect.poll(() => page.evaluate(() => window.__ldrawBench?.().visibleInstances)).toBe(1);
  await page.getByRole('button', { name: '取消隔离', exact: true }).click();
  await page.getByLabel('基准展开程度').fill('0.6');
  await expect.poll(() => page.evaluate(() => window.__ldrawBench?.().requestedExplosion)).toBe(.6);
  await page.getByLabel('保存后进入下一道待审核题').uncheck();
  await page.locator('.bench-review-decisions').getByRole('button', { name: '不通过', exact: true }).click();
  await expect(page.getByRole('alert')).toContainText('必须填写理由');
  await page.getByLabel('审核意见').fill('编号清楚，连接部位需要进一步复核');
  await page.locator('.bench-review-decisions').getByRole('button', { name: '不通过', exact: true }).click();
  await page.reload();
  await expect(page.getByLabel('审核意见')).toHaveValue('编号清楚，连接部位需要进一步复核');
  const downloadEvent = page.waitForEvent('download');
  await page.getByRole('button', { name: '导出本批次 JSON', exact: true }).click();
  const download = await downloadEvent;
  const batch = JSON.parse(await readFile((await download.path())!, 'utf8'));
  expect(batch.benchmarkVersion).toBe('brickatlas-ldraw-1');
  expect(batch.summary).toEqual({ totalTasks: total, reviewed: 1, passed: 0, failed: 1, pending: total - 1 });
  expect(batch.records[0].references).toEqual(task.references);
  expect(batch.records[0].sourceHash).toEqual(bundle.entry.sourceHash);
  expect(await page.evaluate(() => localStorage.getItem('brickatlas:hierarchy3:reviews:v1'))).toBe(old);
  await page.getByRole('button', { name: '播放作者步骤', exact: true }).click();
  await expect.poll(() => page.evaluate(() => window.__ldrawBench?.().buildStep)).toBeGreaterThan(0);
  await page.getByRole('button', { name: '暂停', exact: true }).click();
  await page.goto('/benchmark/review');
  await page.getByLabel('导入审核 JSON').setInputFiles({ name: 'batch.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(batch)) });
  await expect(page.getByText('已导入合并', { exact: true })).toBeVisible();
  await expect(page.getByText('编号清楚，连接部位需要进一步复核')).toBeVisible();
});

test('source instance restoration is visible and rejects invalid edits', async ({ page, request }) => {
  const bundle = await (await request.get('/benchmark/ldraw/models/31028.json')).json();
  const task = bundle.tasks.find((t: any) => t.family === 'restore-instance');
  await page.goto(`/benchmark/31028?task=${task.id}`);
  await page.waitForFunction(() => window.__ldrawBench?.().loadedInstances === 53);
  await expect.poll(() => page.evaluate(() => window.__ldrawBench?.().visibleInstances)).toBe(52);
  await page.getByRole('button', { name: '载入参考答案', exact: true }).click();
  await page.getByLabel('操作回放步骤').fill('1');
  await expect.poll(() => page.evaluate(() => window.__ldrawBench?.().visibleInstances)).toBe(53);
  await page.getByLabel('基准答案 JSON').fill('{"actionIds":["unknown"]}');
  await page.getByRole('button', { name: '检查答案', exact: true }).click();
  await expect(page.getByText('答案未通过', { exact: true })).toBeVisible();
  await expect.poll(() => page.evaluate(() => window.__ldrawBench?.().visibleInstances)).toBe(52);
  await page.getByRole('button', { name: '恢复完整源模型', exact: true }).click();
  await expect.poll(() => page.evaluate(() => window.__ldrawBench?.().visibleInstances)).toBe(53);
});

test('mobile inspection and dashboard fit and expose accessible controls', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/benchmark/review');
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  expect((await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze()).violations).toEqual([]);
  await page.goto('/benchmark/31028?review=1');
  await page.waitForFunction(() => window.__ldrawBench?.().loadedInstances === 53);
  await expect(page.getByLabel('审核意见')).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  expect((await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze()).violations).toEqual([]);
});
