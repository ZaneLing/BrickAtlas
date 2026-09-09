import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('WCAG 2 A/AA checks pass on the model and detail surfaces', async ({ page, isMobile, browserName }, testInfo) => {
  test.skip(browserName !== 'chromium', 'Run the automated accessibility audit in Chromium.');
  await page.goto('/explore/5867');
  await page.getByText('模型已就绪', { exact: true }).waitFor();
  const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
  await testInfo.attach('axe-model', { body: JSON.stringify(result.violations, null, 2), contentType: 'application/json' });
  expect(result.violations.map(v => ({ id: v.id, targets: v.nodes.map(n => n.target) }))).toEqual([]);
  if (isMobile) await page.getByRole('button', { name: '结构与零件' }).click();
  await page.getByLabel('搜索零件', { exact: true }).fill('3004');
  await page.locator('.part-row').first().click();
  const details = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
  await testInfo.attach('axe-details', { body: JSON.stringify(details.violations, null, 2), contentType: 'application/json' });
  expect(details.violations.map(v => ({ id: v.id, targets: v.nodes.map(n => n.target) }))).toEqual([]);
});

test('two-finger zoom never selects an instance', async ({ page, isMobile, browserName }) => {
  test.skip(!isMobile || browserName !== 'chromium', 'Native CDP touch on mobile Chromium.');
  await page.goto('/explore/5867');
  await page.getByText('模型已就绪', { exact: true }).waitFor();
  const canvas = (await page.locator('canvas').boundingBox())!;
  const x = canvas.x + canvas.width / 2, y = canvas.y + canvas.height / 2;
  const client = await page.context().newCDPSession(page);
  const cameraBefore = await page.evaluate(() => window.__atlas!().camera);
  await client.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x - 20, y, id: 1 }, { x: x + 20, y, id: 2 }] });
  for (let d = 24; d <= 70; d += 4) {
    await client.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x - d, y, id: 1 }, { x: x + d, y, id: 2 }] });
  }
  await client.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  expect(await page.evaluate(() => window.__atlas!().selected)).toEqual([]);
  expect(await page.evaluate(() => window.__atlas!().camera)).not.toEqual(cameraBefore);
});
