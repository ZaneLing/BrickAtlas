import { expect, test, type Locator, type Page } from '@playwright/test';

async function dragMaterialToCanvas(page: Page, material: Locator, correct = true) {
  const transfer = await page.evaluateHandle(() => new DataTransfer());
  await material.dispatchEvent('dragstart', { dataTransfer: transfer });
  const stage = (await page.locator('.assembly-game-stage').boundingBox())!;
  const assembly = await material.locator('.assembly-swatch-group').count() > 0;
  let target = { x: stage.width / 2, y: stage.height / 2 };
  if (!assembly && correct) {
    await expect.poll(() => page.evaluate(() => window.__assemblyGame?.().heldId)).not.toBeNull();
    const projected = await page.evaluate(() => {
      const game = window.__assemblyGame?.();
      return game?.scene?.projected.find(part => part.id === game.heldId) ?? null;
    });
    if (!projected) throw new Error('Selected material has no projected target');
    target = projected;
  } else if (!assembly) {
    target = { x: stage.width - 24, y: stage.height - 24 };
  }
  const event = {
    dataTransfer: transfer,
    clientX: stage.x + target.x,
    clientY: stage.y + target.y,
  };
  const canvas = page.locator('.assembly-game-stage');
  await canvas.dispatchEvent('dragenter', event);
  await canvas.dispatchEvent('dragover', event);
  await canvas.dispatchEvent('drop', event);
  await material.dispatchEvent('dragend', { dataTransfer: transfer });
  await transfer.dispose();
}

async function placeCurrentMaterial(page: Page) {
  const material = page.locator('.assembly-material-card:not(.future):not(:disabled)').first();
  await expect(material).toBeVisible();
  await dragMaterialToCanvas(page, material);
}

test('end-of-step review returns parts placed away from their targets', async ({ page }) => {
  await page.goto('/');
  await page.evaluate(() => localStorage.removeItem('brick-atlas-assembly-game-v1'));
  await page.goto('/assemble/31028-sailboat');
  await expect.poll(
    () => page.evaluate(() => window.__assemblyGame?.().ready),
    { timeout: 30000 },
  ).toBe(true);
  const required = await page.evaluate(() => window.__assemblyGame?.().required ?? 0);
  for (let index = 0; index < required; index++) {
    const material = page.locator('.assembly-material-card:not(:disabled)').first();
    await dragMaterialToCanvas(page, material, false);
  }
  await expect.poll(() => page.evaluate(() => window.__assemblyGame?.().review)).toBe('failed');
  expect(await page.evaluate(() => window.__assemblyGame?.().completedStep)).toBe(0);
  expect(await page.evaluate(() => window.__assemblyGame?.().placed)).toBe(0);
  await expect(page.locator('.assembly-material-card:not(:disabled)')).not.toHaveCount(0);
});

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
  const guideFrame = page.locator('.assembly-loop-frame img');
  const firstGuideFrame = await guideFrame.getAttribute('src');
  await page.waitForTimeout(150);
  expect(await guideFrame.getAttribute('src')).not.toBe(firstGuideFrame);
  await expect(page.locator('.assembly-static-guide figure')).toHaveCount(2);
  await expect(page.locator('.assembly-part-thumbnail').first()).toBeVisible();
  await expect.poll(() => page.evaluate(() => {
    const canvas = document.querySelector<HTMLCanvasElement>('.assembly-part-thumbnail');
    return canvas
      ? canvas.getContext('2d')!.getImageData(0, 0, canvas.width, canvas.height).data.some((value, index) => index % 4 === 3 && value > 0)
      : false;
  })).toBe(true);
  expect(await page.evaluate(() => window.__assemblyGame?.().completedStep)).toBe(0);
  const firstStepSize = await page.evaluate(() => window.__assemblyGame?.().required ?? 0);
  expect(await page.evaluate(() => window.__assemblyGame?.().scene?.visibleInstances)).toBe(firstStepSize);
  expect(await page.evaluate(() => window.__assemblyGame?.().scene?.ghosted)).toBe(firstStepSize);
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
  const futurePart = page.locator('.assembly-material-card.future').first();
  await expect(futurePart).toBeVisible();
  await expect(futurePart).toBeDisabled();
  expect(await page.evaluate(() => window.__assemblyGame?.().placed)).toBe(0);

  await steps.nth(0).click();
  await placeCurrentMaterial(page);
  await expect.poll(() => page.evaluate(() => window.__assemblyGame?.().completedStep)).toBe(1);
  await expect.poll(() => page.evaluate(() => window.__assemblyGame?.().advancing)).toBe(false);
  const firstMaterial = page.locator('.assembly-material-card:not(.future):not(:disabled)').first();
  await expect(firstMaterial.locator('b')).toHaveText('2×');
  await firstMaterial.click();
  await expect(page.getByRole('img', { name: '当前零件可旋转三维预览' })).toBeVisible();
  const target = await page.evaluate(() => {
    const game = window.__assemblyGame?.();
    return game?.scene?.projected.find(part => part.id === game.heldId) ?? null;
  });
  if (!target) throw new Error('Selected material has no projected target');
  const stage = (await page.locator('.assembly-game-stage').boundingBox())!;
  await page.mouse.move(stage.x + target.x, stage.y + target.y);
  await expect.poll(() => page.evaluate(() => window.__assemblyGame?.().scene?.manualPreview)).toBe(1);
  await page.mouse.click(stage.x + target.x, stage.y + target.y);
  await expect(firstMaterial.locator('b')).toHaveText('1×');
  expect(await page.evaluate(() => window.__assemblyGame?.().positions)).toBe(1);
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await page.reload();
  await expect.poll(
    () => page.evaluate(() => window.__assemblyGame?.().ready),
    { timeout: 30000 },
  ).toBe(true);
  expect(await page.evaluate(() => window.__assemblyGame?.().completedStep)).toBe(1);
  expect(await page.evaluate(() => window.__assemblyGame?.().positions)).toBe(1);
  expect(await page.evaluate(() => window.__assemblyGame?.().scene?.manualPlaced)).toBe(1);
  while ((await page.evaluate(() => window.__assemblyGame?.().completedStep ?? 0)) < 2) {
    await expect.poll(() => page.evaluate(() => window.__assemblyGame?.().advancing)).toBe(false);
    await placeCurrentMaterial(page);
    await expect.poll(() => page.evaluate(() => {
      const game = window.__assemblyGame?.();
      return Boolean(game?.placed || game?.advancing || game?.completedStep);
    })).toBe(true);
    if (await page.evaluate(() => window.__assemblyGame?.().advancing)) {
      expect(await page.evaluate(() => window.__assemblyGame?.().review)).toBe('passed');
    }
  }
  await page.getByRole('button', { name: '保存', exact: true }).click();
  await page.reload();
  await expect.poll(
    () => page.evaluate(() => window.__assemblyGame?.().ready),
    { timeout: 30000 },
  ).toBe(true);
  expect(await page.evaluate(() => window.__assemblyGame?.().completedStep)).toBe(2);

  for (let guard = 0; guard < 60; guard++) {
    if (await page.evaluate(() => window.__assemblyGame?.().completed)) break;
    await expect.poll(() => page.evaluate(() =>
      window.__assemblyGame?.().completed || !window.__assemblyGame?.().advancing,
    )).toBe(true);
    if (await page.evaluate(() => window.__assemblyGame?.().completed)) break;
    await placeCurrentMaterial(page);
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

test('identical tyres can be installed into a non-source wheel target', async ({ page, request }) => {
  const response = await request.get('/models/31027/manifest.json');
  const manifest = await response.json() as {
    instances: Array<{ instanceId: string; partNumber: string; originalMatrix: number[] }>;
    instructions: { steps: Array<{ instanceIds: string[] }> };
  };
  const byId = new Map(manifest.instances.map(part => [part.instanceId, part]));
  const tyreStepIndex = manifest.instructions.steps.findIndex(step =>
    step.instanceIds.filter(id => byId.get(id)?.partNumber === '50951').length === 4);
  expect(tyreStepIndex).toBeGreaterThan(0);

  await page.goto('/');
  await page.evaluate(({ completedStep }) => {
    localStorage.setItem('brick-atlas-assembly-game-v1', JSON.stringify({
      '31027': {
        completedStep,
        placedIds: [],
        placedTurns: {},
        placedPositions: {},
        completed: false,
        updatedAt: Date.now(),
      },
    }));
  }, { completedStep: tyreStepIndex });
  await page.goto('/assemble/31027');
  await expect.poll(
    () => page.evaluate(() => window.__assemblyGame?.().ready),
    { timeout: 30000 },
  ).toBe(true);

  const material = page.locator('.assembly-material-card:not(:disabled)').filter({ hasText: '50951' });
  await expect(material.locator('b')).toHaveText('4×');
  await material.click();
  const heldId = await page.evaluate(() => window.__assemblyGame?.().heldId);
  expect(heldId).not.toBeNull();
  const tyreIds = manifest.instructions.steps[tyreStepIndex].instanceIds
    .filter(id => byId.get(id)?.partNumber === '50951');
  const quarterTurn = (matrix: number[]) => {
    const angle = Math.hypot(matrix[0], matrix[2]) >= Math.hypot(matrix[8], matrix[10])
      ? Math.atan2(matrix[2], matrix[0])
      : Math.atan2(matrix[8], matrix[10]);
    return (Math.round(angle / (Math.PI / 2)) % 4 + 4) % 4;
  };
  const heldTurn = quarterTurn(byId.get(heldId!)!.originalMatrix);
  const targetId = tyreIds.find(id =>
    id !== heldId && quarterTurn(byId.get(id)!.originalMatrix) !== heldTurn)!;
  const target = await page.evaluate(id =>
    window.__assemblyGame?.().scene?.projected.find(part => part.id === id) ?? null,
  targetId);
  if (!target) throw new Error('Equivalent tyre target was not projected');
  const stage = (await page.locator('.assembly-game-stage').boundingBox())!;
  await page.mouse.move(stage.x + target.x, stage.y + target.y);
  await page.mouse.click(stage.x + target.x, stage.y + target.y);

  await expect(material.locator('b')).toHaveText('3×');
  const savedIds = await page.evaluate(() => {
    const saved = JSON.parse(localStorage.getItem('brick-atlas-assembly-game-v1') ?? '{}');
    return saved['31027']?.placedIds ?? [];
  });
  expect(savedIds).toContain(targetId);
  expect(savedIds).not.toContain(heldId);
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

test('placement steps accept one completed subassembly', async ({ page, request }) => {
  const response = await request.get('/models/10159/manifest.json');
  const manifest = await response.json() as {
    instructions: { steps: Array<{ kind?: string }> };
  };
  const placementIndex = manifest.instructions.steps.findIndex(step => step.kind === 'placement');
  expect(placementIndex).toBeGreaterThan(0);
  await page.goto('/');
  await page.evaluate(({ completedStep }) => localStorage.setItem('brick-atlas-assembly-game-v1', JSON.stringify({
    '10159': {
      completedStep,
      placedIds: [],
      completed: false,
      updatedAt: Date.now(),
    },
  })), { completedStep: placementIndex });
  await page.goto('/assemble/10159');
  await expect.poll(
    () => page.evaluate(() => window.__assemblyGame?.().ready),
    { timeout: 30000 },
  ).toBe(true);
  expect(await page.evaluate(() => window.__assemblyGame?.().activeStep)).toBe(placementIndex + 1);
  expect(await page.evaluate(() => window.__assemblyGame?.().required)).toBe(1);
  await dragMaterialToCanvas(page, page.locator('.assembly-material-card').first());
  await expect.poll(
    () => page.evaluate(() => window.__assemblyGame?.().completedStep),
    { timeout: 10000 },
  ).toBe(placementIndex + 1);
});
