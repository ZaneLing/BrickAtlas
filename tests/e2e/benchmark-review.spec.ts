import { expect, test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { readFile } from 'node:fs/promises';

test('Hierarchy-3 review workflow persists decisions and exports a correction batch', async ({ page }) => {
  await page.goto('/benchmark/review');
  await page.evaluate(() => localStorage.removeItem('brickatlas:hierarchy3:reviews:v1'));
  await page.reload();
  await expect(page.getByText('0 / 2304')).toBeVisible();
  await page.getByRole('link', { name: '继续逐题审核' }).click();
  await page.waitForFunction(() => window.__benchmark?.().modelId === 'camera-gimbal');
  await expect(page.getByText('本模型 0/48')).toBeVisible();
  await expect(page.locator('.bench-review-queue .current')).toHaveCount(1);

  await page.getByLabel('基准展开程度').fill('1');
  await expect.poll(() => page.evaluate(() => window.__benchmark?.().explosion)).toBe(1);

  const decisions = page.locator('.bench-review-decisions');
  await decisions.getByRole('button', { name: '不通过' }).click();
  await expect(page.getByRole('alert')).toContainText('必须填写理由');
  await page.getByLabel('审核意见').fill('题干与公开证据不一致，需要重新生成。');
  await decisions.getByRole('button', { name: '不通过' }).click();
  await expect.poll(() => page.evaluate(() =>
    JSON.parse(localStorage.getItem('brickatlas:hierarchy3:reviews:v1') ?? '[]').length)).toBe(1);
  await expect(page.getByText('本模型 1/48')).toBeVisible();

  await page.getByLabel('提交后自动进入下一道待审核题').uncheck();
  await decisions.getByRole('button', { name: '通过', exact: true }).click();
  await expect.poll(() => page.evaluate(() =>
    JSON.parse(localStorage.getItem('brickatlas:hierarchy3:reviews:v1') ?? '[]').length)).toBe(2);
  await expect(page.getByText('本模型 2/48')).toBeVisible();

  const downloadPromise = page.waitForEvent('download');
  await page.getByLabel('导出当前审核批次').click();
  const download = await downloadPromise;
  const path = await download.path();
  expect(path).not.toBeNull();
  const batch = JSON.parse(await readFile(path!, 'utf8'));
  expect(batch.benchmarkVersion).toBe('brickatlas-hierarchy-3');
  expect(batch.summary).toEqual({ totalTasks: 2304, reviewed: 2, passed: 1, failed: 1, pending: 2302 });
  expect(batch.records.find((row: any) => row.decision === 'fail').reason).toContain('公开证据不一致');

  await page.goto('/benchmark/review');
  await expect(page.getByText('2 / 2304')).toBeVisible();
  await expect(page.getByText('题干与公开证据不一致，需要重新生成。')).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  expect((await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()).violations).toEqual([]);
});

test('review dashboard and task panel remain usable on mobile', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/benchmark/review');
  await expect(page.getByRole('heading', { name: '按难度汇总' })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  await page.goto('/benchmark/camera-gimbal?review=1');
  await page.waitForFunction(() => window.__benchmark?.().modelId === 'camera-gimbal');
  await expect(page.getByLabel('审核意见')).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  expect((await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()).violations).toEqual([]);
});
