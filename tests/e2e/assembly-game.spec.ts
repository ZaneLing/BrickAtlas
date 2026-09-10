import { expect, test } from '@playwright/test';

test('manual assembly rejects wrong steps, saves progress and marks completion', async ({ page }) => {
  test.setTimeout(120000);
  await page.goto('/');
  await page.evaluate(() => localStorage.removeItem('brick-atlas-assembly-game-v1'));
  await page.goto('/assemble/31028-sailboat');
  await expect(page.getByRole('main', { name: '手动拼装画布' })).toBeVisible();
  await expect.poll(
    () => page.evaluate(() => window.__assemblyGame?.().ready),
    { timeout: 30000 },
  ).toBe(true);
  await expect(page.locator('.assembly-loop-frame img')).toBeVisible({ timeout: 30000 });
  await expect(page.locator('.assembly-static-guide figure')).toHaveCount(2);
  expect(await page.evaluate(() => window.__assemblyGame?.().completedStep)).toBe(0);
  const camera = await page.evaluate(() => window.__assemblyGame?.().scene?.camera);
  await page.getByLabel('模型视角').selectOption('top');
  await expect.poll(() => page.evaluate(before => {
    const current = window.__assemblyGame?.().scene?.camera;
    return current && before
      ? Math.hypot(...current.map((value, index) => value - before[index]))
      : 0;
  }, camera)).toBeGreaterThan(1);
  await page.getByLabel('模型视角').selectOption('perspective');

  const steps = page.locator('.assembly-step-list > button');
  await steps.nth(1).click();
  const futurePart = page.locator('.assembly-material-card.future:not(:disabled)').first();
  await expect(futurePart).toBeVisible();
  await futurePart.dragTo(page.locator('.assembly-drop-zone'));
  await expect.poll(() => page.evaluate(() => window.__assemblyGame?.().feedback)).toBe('wrong');
  expect(await page.evaluate(() => window.__assemblyGame?.().placed)).toBe(0);

  await steps.nth(0).click();
  while ((await page.evaluate(() => window.__assemblyGame?.().completedStep ?? 0)) < 1) {
    await expect.poll(() => page.evaluate(() => window.__assemblyGame?.().advancing)).toBe(false);
    const material = page.locator('.assembly-material-card:not(.future):not(:disabled)').first();
    await expect(material).toBeVisible();
    await material.dragTo(page.locator('.assembly-drop-zone'));
    await expect.poll(() => page.evaluate(() => {
      const game = window.__assemblyGame?.();
      return Boolean(game?.placed || game?.advancing || game?.completedStep);
    })).toBe(true);
  }
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await page.reload();
  await expect.poll(
    () => page.evaluate(() => window.__assemblyGame?.().ready),
    { timeout: 30000 },
  ).toBe(true);
  expect(await page.evaluate(() => window.__assemblyGame?.().completedStep)).toBe(1);

  for (let guard = 0; guard < 60; guard++) {
    if (await page.evaluate(() => window.__assemblyGame?.().completed)) break;
    await expect.poll(() => page.evaluate(() =>
      window.__assemblyGame?.().completed || !window.__assemblyGame?.().advancing,
    )).toBe(true);
    if (await page.evaluate(() => window.__assemblyGame?.().completed)) break;
    const material = page.locator('.assembly-material-card:not(.future):not(:disabled)').first();
    await expect(material).toBeVisible();
    await material.dragTo(page.locator('.assembly-drop-zone'));
    await page.waitForTimeout(80);
  }
  await expect.poll(
    () => page.evaluate(() => window.__assemblyGame?.().completed),
    { timeout: 30000 },
  ).toBe(true);
  await expect(page.getByRole('heading', { name: '拼装完成' })).toBeVisible();

  await page.goto('/');
  const completedCard = page.locator('.model-card.game-completed').filter({ hasText: 'Sailboat' });
  await expect(completedCard.getByText('已拼完')).toBeVisible();
});

test('assembly hub exposes all five difficulty levels', async ({ page }) => {
  await page.goto('/assemble');
  await expect(page.getByRole('heading', { name: '选择一个模型开始挑战' })).toBeVisible();
  await expect(page.locator('.assembly-model-card')).toHaveCount(15);
  const levels = await page.locator('.assembly-difficulty').evaluateAll(elements =>
    [...new Set(elements.map(element => element.getAttribute('aria-label')?.split(' / ')[0]))].sort(),
  );
  expect(levels).toEqual(['1', '2', '3', '4', '5']);
});

test('placement steps accept one completed subassembly', async ({ page }) => {
  await page.goto('/');
  await page.evaluate(() => localStorage.setItem('brick-atlas-assembly-game-v1', JSON.stringify({
    '10159': {
      completedStep: 104,
      placedIds: [],
      completed: false,
      updatedAt: Date.now(),
    },
  })));
  await page.goto('/assemble/10159');
  await expect.poll(
    () => page.evaluate(() => window.__assemblyGame?.().ready),
    { timeout: 30000 },
  ).toBe(true);
  expect(await page.evaluate(() => window.__assemblyGame?.().activeStep)).toBe(105);
  expect(await page.evaluate(() => window.__assemblyGame?.().required)).toBe(1);
  await page.locator('.assembly-material-card').first().dragTo(page.locator('.assembly-drop-zone'));
  await expect.poll(
    () => page.evaluate(() => window.__assemblyGame?.().completedStep),
    { timeout: 10000 },
  ).toBe(105);
});
