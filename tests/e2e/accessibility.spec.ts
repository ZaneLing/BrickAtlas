import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('WCAG 2 A/AA checks pass on the model and detail surfaces', async ({ page, browserName }, testInfo) => {
  test.skip(browserName !== 'chromium', 'Run the automated accessibility audit in Chromium.');
  await page.goto('/');
  const landing = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
  await testInfo.attach('axe-landing', { body: JSON.stringify(landing.violations, null, 2), contentType: 'application/json' });
  expect(landing.violations.map(v => ({ id: v.id, targets: v.nodes.map(n => n.target) }))).toEqual([]);
  await page.goto('/explore/5867');
  await page.getByText('模型已就绪', { exact: true }).waitFor();
  const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
  await testInfo.attach('axe-model', { body: JSON.stringify(result.violations, null, 2), contentType: 'application/json' });
  expect(result.violations.map(v => ({ id: v.id, targets: v.nodes.map(n => n.target) }))).toEqual([]);
  await page.getByLabel('搜索零件', { exact: true }).fill('3004');
  await page.locator('.part-row').first().click();
  const details = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
  await testInfo.attach('axe-details', { body: JSON.stringify(details.violations, null, 2), contentType: 'application/json' });
  expect(details.violations.map(v => ({ id: v.id, targets: v.nodes.map(n => n.target) }))).toEqual([]);
});
