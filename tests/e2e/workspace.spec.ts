import { readFile } from 'node:fs/promises';
import { expect, test } from '@playwright/test';

test('catalog exposes fifteen projects, real previews and model parameters', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Brick Atlas' })).toBeVisible();
  await expect(page.getByRole('region', { name: '双动画积木演示' }).locator('canvas')).toHaveCount(2);
  await expect(page.getByRole('navigation', { name: '选择积木空间' }).getByRole('link')).toHaveCount(4);
  await expect(page.locator('.landing-brick-backdrop .backdrop-brick')).toHaveCount(30);
  expect(await page.locator('.landing-brick-backdrop .backdrop-brick').evaluateAll(bricks =>
    new Set(bricks.map(brick => [...brick.classList].find(name => name.startsWith('backdrop-brick-')))).size,
  )).toBe(6);
  expect(await page.locator('.landing-brick-backdrop').evaluate(element => ({
    pointerEvents: getComputedStyle(element).pointerEvents,
    animation: getComputedStyle(element.firstElementChild!).animationName,
    opacity: getComputedStyle(element.firstElementChild!).opacity,
  }))).toEqual({ pointerEvents: 'none', animation: 'backdrop-brick-float', opacity: '0.32' });
  await expect(page.locator('.model-card')).toHaveCount(15);
  await expect(page.getByRole('searchbox', { name: '搜索模型' })).toBeVisible();
  await expect(page.locator('.model-card-explore')).toHaveCount(15);
  await expect(page.getByText('探索模型', { exact: true })).toHaveCount(0);
  await expect(page.getByRole('link', { name: '观看拼装' })).toHaveCount(15);
  await expect(page.getByRole('link', { name: '手动拼装' })).toHaveCount(15);
  await expect(page.locator('.model-difficulty')).toHaveCount(15);
  await expect(page.locator('.model-card-specs')).toHaveCount(15);
  await expect(page.getByText('积木树').first()).toBeVisible();
  await expect(page.locator('.model-art img')).toHaveCount(15);
  expect(await page.locator('.model-art img').evaluateAll(images => images.every(image => (image as HTMLImageElement).naturalWidth >= 1000))).toBe(true);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await page.getByRole('button', { name: '切换为英文' }).click();
  await expect(page.locator('.brick-burst-piece')).toHaveCount(10);
  await expect(page.locator('.brick-burst-piece')).toHaveCount(0, { timeout: 1500 });
});

test('landing opens with equal build and explode animations running together', async ({ page }) => {
  test.setTimeout(60000);
  await page.goto('/');
  const showcase = page.getByRole('region', { name: '双动画积木演示' });
  await expect(showcase.getByRole('article')).toHaveCount(2);
  await expect(showcase.locator('canvas')).toHaveCount(2);
  await expect(showcase.locator('canvas').first()).toBeVisible();
  const layout = await showcase.getByRole('article').evaluateAll(panels => panels.map(panel => {
    const rect = panel.getBoundingClientRect();
    return { left: rect.left, top: rect.top, width: rect.width, height: rect.height };
  }));
  expect(layout[0].top).toBe(layout[1].top);
  expect(Math.abs(layout[0].width - layout[1].width)).toBeLessThan(2);
  expect(layout[0].top).toBeLessThan(100);
  expect(await page.evaluate(() => {
    const showcase = document.querySelector('.landing-showcase')!;
    const lobby = document.querySelector('.play-lobby')!;
    return Boolean(showcase.compareDocumentPosition(lobby) & Node.DOCUMENT_POSITION_FOLLOWING);
  })).toBe(true);

  const initial = await page.evaluate(() => window.__landingAtlases?.().build?.visibleInstances ?? 0);
  await expect.poll(() => page.evaluate(() => window.__landingAtlases?.().build?.visibleInstances ?? 0)).toBeGreaterThan(initial);
  const landingDuration = await page.evaluate(() => window.__landingAtlases?.().build?.assemblyDurationMs ?? 0);
  expect(landingDuration).toBeGreaterThan(250);
  expect(landingDuration).toBeLessThan(18_000 / 52);
  expect(await page.evaluate(() => window.__landingAtlases?.().build?.controlsEnabled)).toBe(false);
  expect(await page.evaluate(() => window.__landingAtlases?.().explode?.controlsEnabled)).toBe(false);
  await expect.poll(
    () => page.evaluate(() => window.__landingAtlases?.().explode?.actualExplosion ?? 0),
    { timeout: 6500 },
  ).toBeGreaterThan(0.95);
  await expect.poll(
    () => page.evaluate(() => window.__landingAtlases?.().explode?.actualExplosion ?? 1),
    { timeout: 7500 },
  ).toBeLessThan(0.05);
});

test('language toggle translates the complete workspace and persists', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: '切换为英文' }).click();
  await expect(page.getByRole('heading', { name: 'Choose your next build' })).toBeVisible();
  await expect(page.getByRole('link', { name: 'Models', exact: true })).toBeVisible();
  await expect(page.getByText('Tree nodes').first()).toBeVisible();
  await page.locator('.model-card-explore').first().click();
  await expect(page.getByText('Model ready', { exact: true })).toBeVisible();
  await expect(page.getByLabel('Search bricks', { exact: true })).toBeVisible();
  await page.reload();
  await expect(page.getByText('Model ready', { exact: true })).toBeVisible();
  expect(await page.locator('html').getAttribute('lang')).toBe('en');
});

test('clicking a specific project card opens its explore workspace', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('link', { name: '探索 Super Speedster', exact: true }).click();
  await expect(page).toHaveURL(/\/explore\/5867$/);
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
});

test('additional project loads real geometry and supports search highlight and x-ray', async ({ page }) => {
  await page.goto('/explore/31027');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  await expect.poll(async () => page.evaluate(() => window.__atlas?.().loadedInstances)).toBe(67);
  await page.getByLabel('顶部搜索零件').fill('wheel');
  await expect.poll(async () => page.evaluate(() => window.__atlas?.().selected.length)).toBe(0);
  await page.getByRole('button', { name: 'X-Ray 透视模式' }).first().click();
  await expect(page.getByRole('button', { name: 'X-Ray 透视模式' }).first()).toHaveAttribute('aria-pressed', 'true');
});

test('desktop renderer uses high-density pixels and supports 4x ultra mode', async ({ page }) => {
  await page.goto('/explore/31027');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  const ratio = () => page.locator('.canvas-host canvas').evaluate(canvas => (canvas as HTMLCanvasElement).width / canvas.getBoundingClientRect().width);
  expect(await ratio()).toBeGreaterThanOrEqual(1.9);
  await page.getByRole('button', { name: '显示设置' }).click();
  await page.getByLabel('渲染质量').selectOption('ultra');
  await expect.poll(ratio).toBeGreaterThanOrEqual(3.9);
});

test('build mode advances, animates and persists progress per project', async ({ page }, testInfo) => {
  await page.goto('/build/5867');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  await page.getByLabel('下一步', { exact: true }).click();
  await expect(page.getByLabel('当前拼装步骤')).toHaveValue('1');
  await expect.poll(async () => page.evaluate(() => window.__atlas?.().visibleInstances)).toBe(6);
  await expect(page.getByRole('complementary', { name: '步骤说明书' })).toBeVisible();
  const accordion = page.getByRole('region', { name: '可折叠拼装步骤' });
  const stepBricks = accordion.locator('.instruction-brick-step');
  await expect(stepBricks).toHaveCount(51);
  await expect(accordion.locator('.instruction-brick-step[open]')).toHaveCount(0);
  await stepBricks.first().locator('summary').click();
  await expect(page.getByRole('region', { name: '本步所需零件' })).toContainText('本步所需零件');
  const stepPreview = page.getByAltText('第 1 步从起始位置到安装位置的高清图示');
  await expect(stepPreview).toBeVisible({ timeout: 20000 });
  expect(await stepPreview.evaluate((image: HTMLImageElement) => [image.naturalWidth, image.naturalHeight])).toEqual([2560, 1120]);
  await page.screenshot({ path: testInfo.outputPath('build-static-step.png') });
  await expect(page.getByText('自动循环 · 聚焦本步')).toHaveCount(0);
  await expect(page.getByAltText(/动态拼装图/)).toHaveCount(0);
  await page.getByRole('button', { name: '放大第 1 步高清入位图' }).click();
  await expect(page.getByRole('dialog', { name: '第 1 步高清入位图' })).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath('build-static-step-enlarged.png') });
  await page.getByRole('button', { name: '关闭弹窗' }).click();
  await page.locator('.instruction-parts > button').first().click();
  await expect(page.getByRole('region', { name: '选中积木三维预览' })).toBeVisible();
  await page.waitForTimeout(850);
  expect((await page.evaluate(() => window.__atlas?.().offsets))?.filter(offset => offset.some(value => Math.abs(value) > 0.01)).length).toBe(0);
  await page.reload();
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  await expect(page.getByLabel('当前拼装步骤')).toHaveValue('1');
  await expect(stepBricks.first()).not.toHaveAttribute('open', '');
  await stepBricks.first().locator('summary').click();
  await expect(stepBricks.first()).toHaveAttribute('open', '');
  await page.getByLabel('下一步', { exact: true }).click();
  await expect(page.getByLabel('当前拼装步骤')).toHaveValue('2');
  await expect(stepBricks.first()).toHaveAttribute('open', '');
  await expect(stepBricks.nth(1)).not.toHaveAttribute('open', '');
  await stepBricks.nth(1).locator('summary').click();
  await expect(page.getByLabel('当前拼装步骤')).toHaveValue('2');
  await expect(stepBricks.nth(1)).toHaveAttribute('open', '');
  await expect(stepBricks.first()).not.toHaveAttribute('open', '');
  await stepBricks.nth(1).locator('summary').click();
  await page.getByLabel('上一步', { exact: true }).click();
  await expect(page.getByLabel('当前拼装步骤')).toHaveValue('1');
  await expect(accordion.locator('.instruction-brick-step[open]')).toHaveCount(0);
  await page.getByLabel('自动播放拼装').click();
  await expect(page.getByLabel('当前拼装步骤')).toHaveValue('2', { timeout: 3000 });
  await page.getByLabel('暂停自动拼装').click();
  await expect(accordion.locator('.instruction-brick-step[open]')).toHaveCount(0);
});

test('build steps preserve the user camera unless follow mode is enabled', async ({ page }) => {
  await page.goto('/build/5867');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  await page.getByLabel('下一步', { exact: true }).click();
  await page.waitForTimeout(1000);
  await page.getByRole('button', { name: '放大模型' }).click();
  await page.getByRole('button', { name: '放大模型' }).click();
  const camera = (await page.evaluate(() => window.__atlas!().camera))!;
  const target = (await page.evaluate(() => window.__atlas!().target))!;

  await page.getByLabel('下一步', { exact: true }).click();
  await page.waitForTimeout(1100);
  expect(await page.evaluate(({ camera, target }) => {
    const state = window.__atlas!();
    return Math.max(
      Math.hypot(...state.camera.map((value, index) => value - camera[index])),
      Math.hypot(...state.target.map((value, index) => value - target[index])),
    );
  }, { camera, target })).toBeLessThan(0.05);

  await page.getByRole('button', { name: '步骤镜头跟随' }).click();
  await page.getByLabel('下一步', { exact: true }).click();
  await expect.poll(async () => page.evaluate(before => {
    const camera = window.__atlas!().camera;
    return Math.hypot(...camera.map((value, index) => value - before[index]));
  }, camera)).toBeGreaterThan(1);
});

test('build canvas pans horizontally and vertically without moving the model base', async ({ page }) => {
  await page.goto('/build/5867');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  const panButton = page.getByRole('button', { name: '平移视图（上下左右拖动）' });
  await expect(panButton).toHaveAttribute('aria-pressed', 'true');
  await expect.poll(async () => page.evaluate(() => window.__atlas?.().panMode)).toBe(true);

  const canvas = page.locator('.canvas-host canvas');
  const box = (await canvas.boundingBox())!;
  const start = { x: box.x + box.width * 0.62, y: box.y + box.height * 0.55 };
  const initialTarget = (await page.evaluate(() => window.__atlas!().target))!;

  await page.mouse.move(start.x, start.y);
  await page.mouse.down();
  await page.mouse.move(start.x + 90, start.y, { steps: 8 });
  await page.mouse.up();
  await expect.poll(async () => page.evaluate(target => {
    const next = window.__atlas!().target;
    return Math.hypot(...next.map((value, index) => value - target[index]));
  }, initialTarget)).toBeGreaterThan(0.1);

  const horizontalTarget = (await page.evaluate(() => window.__atlas!().target))!;
  await page.mouse.move(start.x, start.y);
  await page.mouse.down();
  await page.mouse.move(start.x, start.y - 80, { steps: 8 });
  await page.mouse.up();
  await expect.poll(async () => page.evaluate(target => {
    const next = window.__atlas!().target;
    return Math.hypot(...next.map((value, index) => value - target[index]));
  }, horizontalTarget)).toBeGreaterThan(0.1);
});

test('both build sidebars collapse independently and release space to the model', async ({ page }, testInfo) => {
  await page.goto('/build/5867');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  const stage = page.locator('.main-stage');
  const initial = (await stage.boundingBox())!.width;
  await page.getByRole('button', { name: '折叠模型信息' }).click();
  await expect(page.getByRole('complementary', { name: '模型结构与搜索' })).toBeHidden();
  const withoutLeft = (await stage.boundingBox())!.width;
  expect(withoutLeft).toBeGreaterThan(initial + 200);
  await page.getByRole('button', { name: '折叠步骤说明书' }).click();
  await expect(page.getByRole('complementary', { name: '步骤说明书' })).toBeHidden();
  expect((await stage.boundingBox())!.width).toBeGreaterThan(withoutLeft + 300);
  await page.screenshot({ path: testInfo.outputPath('build-sidebars-collapsed.png') });
  await page.getByRole('button', { name: '打开模型信息' }).click();
  await page.getByRole('button', { name: '打开步骤说明书' }).click();
  await expect(page.getByRole('complementary', { name: '模型结构与搜索' })).toBeVisible();
  await expect(page.getByRole('complementary', { name: '步骤说明书' })).toBeVisible();
});

test('step snapshots never resize or flash the live canvas and controls stay top-left', async ({ page }) => {
  await page.goto('/build/5867');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  await page.evaluate(() => {
    const canvas = document.querySelector('.canvas-host canvas')!;
    (window as unknown as { __canvasMutations: string[] }).__canvasMutations = [];
    new MutationObserver(records => {
      (window as unknown as { __canvasMutations: string[] }).__canvasMutations.push(...records.map(record => record.attributeName ?? ''));
    }).observe(canvas, { attributes: true, attributeFilter: ['width', 'height'] });
  });
  await page.getByLabel('下一步', { exact: true }).click();
  await page.waitForTimeout(900);
  await page.getByLabel('下一步', { exact: true }).click();
  await page.waitForTimeout(900);
  expect(await page.evaluate(() => (window as unknown as { __canvasMutations: string[] }).__canvasMutations)).toEqual([]);
  const layout = await page.evaluate(() => {
    const main = document.querySelector('.main-stage')!.getBoundingClientRect();
    const dock = document.querySelector('.build-dock')!.getBoundingClientRect();
    const canvas = document.querySelector('.canvas-host')!.getBoundingClientRect();
    return { mainHeight: main.height, dockTop: dock.top - main.top, dockWidth: dock.width, canvasBottom: main.bottom - canvas.bottom };
  });
  expect(layout.dockTop).toBeLessThan(layout.mainHeight / 3);
  expect(layout.dockWidth).toBeLessThanOrEqual(430);
  expect(layout.canvasBottom).toBeLessThanOrEqual(1);
});

test('selected build brick opens an interactive geometry preview', async ({ page }) => {
  await page.goto('/build/5867');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: '下一步' }).click();
  await expect.poll(async () => page.evaluate(() => window.__atlas?.().visibleInstances)).toBe(6);
  await page.waitForTimeout(900);
  const canvas = page.locator('.canvas-host canvas');
  const point = await page.evaluate(() => {
    const canvas = document.querySelector('.canvas-host canvas')!.getBoundingClientRect();
    const dock = document.querySelector('.build-dock')!.getBoundingClientRect();
    return window.__atlas!().projected.find(point => {
      const x = canvas.left + point.x, y = canvas.top + point.y;
      return x > canvas.left && x < canvas.right && y > canvas.top && y < canvas.bottom
        && !(x >= dock.left && x <= dock.right && y >= dock.top && y <= dock.bottom);
    })!;
  });
  await canvas.click({ position: { x: point.x, y: point.y } });
  await expect.poll(async () => page.evaluate(() => window.__atlas?.().selected.length)).toBe(1);
  const preview = page.getByRole('region', { name: '选中积木三维预览' });
  await expect(preview).toBeVisible();
  const previewCanvas = preview.getByRole('img', { name: '选中积木可旋转三维预览' });
  await expect(previewCanvas).toBeVisible();
  const before = await previewCanvas.screenshot();
  const box = (await previewCanvas.boundingBox())!;
  await page.mouse.move(box.x + box.width * 0.35, box.y + box.height * 0.5);
  await page.mouse.down();
  await page.mouse.move(box.x + box.width * 0.7, box.y + box.height * 0.55, { steps: 8 });
  await page.mouse.up();
  await page.waitForTimeout(250);
  expect(await previewCanvas.screenshot()).not.toEqual(before);
});

test('build guide exports cover and one page per step', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'desktop-chrome', 'One browser verifies the generated PDF payload.');
  await page.goto('/build/31027');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: '下一步' }).click();
  const download = page.waitForEvent('download');
  await page.getByRole('button', { name: '导出完整说明书 PDF' }).click();
  const file = await download;
  const path = testInfo.outputPath(file.suggestedFilename());
  await file.saveAs(path);
  const payload = await readFile(path);
  expect(file.suggestedFilename()).toBe('brick-atlas-31027-build-guide.pdf');
  expect(payload.subarray(0, 4).toString()).toBe('%PDF');
  expect((payload.toString('latin1').match(/\/Type \/Page\b/g) ?? [])).toHaveLength(13);
});

test('source-authored instruction model exposes OMR steps', async ({ page }) => {
  await page.goto('/build/31009');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  await expect(page.getByLabel('当前拼装步骤')).toHaveAttribute('max', '79');
  await expect(page.getByText('OMR 源步骤', { exact: true })).toBeVisible();
});

test('editorial scene builds movable assemblies before final placement', async ({ page }) => {
  await page.goto('/build/10159');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  await expect(page.getByLabel('当前拼装步骤')).toHaveAttribute('max', '115');
  const labels = await page.locator('.instruction-brick-label strong').allTextContents();
  expect(labels.slice(0, 3).every(label => label.includes('airplane'))).toBe(true);
  expect(labels.slice(-11).every(label => label.includes('放置总成'))).toBe(true);
  const placement = await page.evaluate(async () => {
    const manifest = await fetch('/models/10159/manifest.json').then(response => response.json());
    const index = manifest.instructions.steps.findIndex((step: { kind?: string }) => step.kind === 'placement');
    const instanceId = manifest.instructions.steps[index].motionInstanceIds[0];
    return { step: index + 1, partIndex: manifest.instances.findIndex((part: { instanceId: string }) => part.instanceId === instanceId) };
  });
  await page.getByLabel('当前拼装步骤').fill(String(placement.step - 1));
  await expect.poll(async () => page.evaluate(index =>
    Math.max(...window.__atlas!().offsets[index].map(value => Math.abs(value))), placement.partIndex,
  )).toBeGreaterThan(1);
  await page.getByLabel('当前拼装步骤').fill(String(placement.step));
  const accordion = page.getByRole('region', { name: '可折叠拼装步骤' });
  await accordion.locator('.instruction-brick-step').nth(placement.step - 1).locator('summary').click();
  await expect(page.getByAltText(`第 ${placement.step} 步从起始位置到安装位置的高清图示`)).toBeVisible({ timeout: 20000 });
  await expect.poll(async () => page.evaluate(index =>
    Math.max(...window.__atlas!().offsets[index].map(value => Math.abs(value))), placement.partIndex,
  )).toBeLessThan(0.1);
});

test('complex train and truck models load all addressable bricks', async ({ page }) => {
  for (const [id, count] of [['10014', 170], ['10156', 111], ['10001', 848], ['10128', 336], ['10036', 166], ['10159', 592]] as const) {
    await page.goto(`/explore/${id}`);
    await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
    await expect.poll(async () => page.evaluate(() => window.__atlas?.().loadedInstances)).toBe(count);
  }
});

test('large batched model expands completely without multiplying draw calls', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'desktop-chrome', 'One Chromium GPU stress run is sufficient.');
  test.setTimeout(90000);
  await page.goto('/explore/10214');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible({ timeout: 60000 });
  await expect.poll(async () => page.evaluate(() => window.__atlas?.().loadedInstances), { timeout: 60000 }).toBe(4281);
  const assembled = (await page.evaluate(() => window.__atlas!()))!;
  expect(assembled.drawCalls).toBeLessThan(650);
  await page.getByRole('button', { name: /^零件陈列/ }).click();
  await expect.poll(async () => page.evaluate(() => window.__atlas?.().actualExplosion), { timeout: 10000 }).toBe(1);
  await expect.poll(
    async () => page.evaluate(() => window.__atlas?.().framing.insideInstances),
    { timeout: 10000 },
  ).toBe(4281);
  const inventory = (await page.evaluate(() => window.__atlas!()))!;
  expect(inventory.visibleInstances).toBe(4281);
  expect(inventory.framing.insideInstances).toBe(4281);
  expect(inventory.drawCalls).toBeLessThan(650);
  expect(inventory.frameMs).toBeLessThan(80);

  await page.goto('/build/10214');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible({ timeout: 60000 });
  const buildStarted = Date.now();
  for (let step = 1; step <= 3; step++) {
    await page.getByLabel('下一步', { exact: true }).click();
    await expect(page.getByRole('slider', { name: '当前拼装步骤' })).toHaveValue(String(step));
    await page.waitForTimeout(1050);
  }
  expect(Date.now() - buildStarted).toBeLessThan(8000);
  const buildMetrics = (await page.evaluate(() => window.__atlas!()))!;
  expect(buildMetrics.drawCalls).toBeLessThan(650);
  expect(buildMetrics.frameMs).toBeLessThan(80);
});

test('workspace navigation returns home and switches models', async ({ page }) => {
  await page.goto('/explore/5867');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  await page.getByLabel('切换模型').selectOption('31028');
  await expect(page).toHaveURL(/\/explore\/31028$/);
  await page.getByRole('link', { name: '返回项目库' }).click();
  await expect(page).toHaveURL(/\/$/);
});

test('creator preflights a local MPD without uploading it', async ({ page }) => {
  await page.goto('/create');
  await page.locator('input[accept*=".ldr"]').setInputFiles('assets-source/set-original/31027-1.mpd');
  await expect(page.getByRole('heading', { name: '31027-1.mpd' })).toBeVisible();
  await expect(page.getByText('Type-1 引用')).toBeVisible();
  await expect(page.getByText('结构演示', { exact: false })).toBeVisible();
});

test('composer snaps reusable models and parts into a buildable saved scene', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'desktop-chrome', 'The compose workflow is verified once in Chromium.');
  await page.goto('/compose');
  await expect(page.getByRole('region', { name: '组建工作台' })).toBeVisible();
  await expect(page.getByRole('img', { name: '组建模型三维工作区' })).toBeVisible();
  await page.getByRole('button', { name: '添加水上飞机' }).click();
  await expect.poll(async () => page.evaluate(() => window.__composer?.().items)).toBe(1);
  await expect.poll(async () => page.evaluate(() => window.__composer?.().bricks ?? 0)).toBeGreaterThan(100);

  await page.getByRole('tab', { name: '场景' }).click();
  await page.getByRole('button', { name: /大型场景底板/ }).click();
  await expect(page.locator('.compose-tree-base')).toContainText('64 × 48 studs');
  await page.getByRole('tab', { name: '零件' }).click();
  await page.getByRole('button', { name: '添加基础砖 2×4' }).click();
  await expect.poll(async () => page.evaluate(() => window.__composer?.().items)).toBe(2);
  await page.getByRole('button', { name: '向右移动' }).click();
  await page.getByRole('button', { name: '旋转 90 度' }).click();

  await page.getByRole('tab', { name: '拼装', exact: true }).click();
  await page.getByLabel('当前组建步骤').fill('1');
  await expect.poll(async () => page.evaluate(() => window.__composer?.().step)).toBe(1);
  await page.getByRole('button', { name: '下一步' }).click();
  await expect.poll(async () => page.evaluate(() => window.__composer?.().step)).toBe(2);

  await page.getByRole('tab', { name: '展开' }).click();
  await page.getByLabel('组建展开程度').fill('100');
  await expect.poll(async () => page.evaluate(() => window.__composer?.().explosion ?? 0)).toBeGreaterThan(0.95);
  expect((await page.evaluate(() => window.__composer!())).drawCalls).toBeLessThan(100);

  await page.getByRole('button', { name: '保存' }).click();
  await page.reload();
  await expect.poll(async () => page.evaluate(() => window.__composer?.().items)).toBe(2);
  const download = page.waitForEvent('download');
  await page.getByRole('button', { name: 'LDraw', exact: true }).click();
  expect((await download).suggestedFilename()).toContain('.ldr');
});

test('image studio converts an image into bricks, steps, and exports', async ({ page }) => {
  test.setTimeout(120000);
  await page.goto('/create');
  await expect(page.getByRole('region', { name: '图片转积木工作台' })).toBeVisible();
  await expect.poll(async () => page.evaluate(() => window.__imageBricks?.().bricks ?? -1)).toBe(0);
  await page.getByRole('tab', { name: '本地备用' }).click();
  await page.getByLabel('上传正视图').setInputFiles('public/models/5867/preview.png');
  await expect.poll(
    async () => page.evaluate(() => window.__imageBricks?.().bricks ?? 0),
    { timeout: 90000 },
  ).toBeGreaterThan(20);
  await expect(page.locator('.image-stage-heading strong')).toHaveText('preview');
  const crop = page.locator('.crop-source').first().locator('.crop-selection');
  const cropBefore = await crop.getAttribute('style');
  const cropBox = (await crop.boundingBox())!;
  await page.mouse.move(cropBox.x + cropBox.width / 2, cropBox.y + cropBox.height / 2);
  await page.mouse.down();
  await page.mouse.move(cropBox.x + cropBox.width / 2 - 35, cropBox.y + cropBox.height / 2, { steps: 8 });
  await page.mouse.up();
  await expect.poll(async () => crop.getAttribute('style')).not.toBe(cropBefore);

  await page.getByLabel('上传左侧').setInputFiles('public/models/5867/preview.png');
  await page.getByLabel('上传背面').setInputFiles('public/models/5867/preview.png');
  await page.getByLabel('生成方法').selectOption('hollow');
  await page.getByLabel('积木预算').fill('800');
  await expect.poll(
    async () => page.evaluate(() => window.__imageBricks?.().viewCount),
    { timeout: 90000 },
  ).toBe(3);
  await expect.poll(async () => page.evaluate(() => window.__imageBricks?.().method)).toBe('hollow');
  await expect.poll(async () => page.evaluate(() => window.__imageBricks?.().bricks ?? 9999)).toBeLessThanOrEqual(800);
  await page.getByRole('tab', { name: '拼装步骤' }).click();
  const createSteps = page.locator('.image-instruction-step');
  await expect(createSteps).toHaveCount((await page.evaluate(() => window.__imageBricks!().steps))!);
  await createSteps.first().locator('summary').click();
  await expect(createSteps.first().getByRole('button', { name: '聚焦本步' })).toBeVisible();
  const canvas = page.getByRole('img', { name: '图片生成的积木三维模型' });
  await expect(canvas).toBeVisible();
  const ratio = await canvas.evaluate(element => (element as HTMLCanvasElement).width / element.getBoundingClientRect().width);
  expect(ratio).toBeGreaterThanOrEqual(1.9);
  const createAutoRotate = page.getByRole('button', { name: '自动旋转' });
  if (await createAutoRotate.getAttribute('aria-pressed') === 'true') await createAutoRotate.click();
  await page.getByLabel('拆分程度').fill('70');
  await expect.poll(async () => page.evaluate(() => window.__imageBricks?.().explosion ?? 0)).toBeGreaterThan(0.6);
  await expect.poll(async () => page.evaluate(() => window.__imageBricks?.().cameraMoving)).toBe(false);
  const metrics = (await page.evaluate(() => window.__imageBricks!()))!;
  expect(metrics.drawCalls).toBeLessThan(80);
  expect(metrics.bodyBatches + metrics.studBatches).toBeLessThan(80);
  const camera = metrics.camera;
  await page.getByRole('slider', { name: '当前拼装步骤' }).fill(String(Math.max(1, metrics.steps - 1)));
  await page.getByRole('button', { name: '下一步' }).click();
  await page.waitForTimeout(700);
  expect(await page.evaluate(before => {
    const camera = window.__imageBricks!().camera;
    return Math.hypot(...camera.map((value, index) => value - before[index]));
  }, camera)).toBeLessThan(0.05);
  await page.getByRole('button', { name: '步骤镜头跟随' }).click();
  await page.getByRole('button', { name: '回到开始' }).click();
  await page.getByRole('button', { name: '下一步' }).click();
  await expect.poll(async () => page.evaluate(before => {
    const camera = window.__imageBricks!().camera;
    return Math.hypot(...camera.map((value, index) => value - before[index]));
  }, camera)).toBeGreaterThan(1);
  const bomDownload = page.waitForEvent('download');
  await page.getByRole('button', { name: 'BOM CSV' }).click();
  expect((await bomDownload).suggestedFilename()).toContain('-bom.csv');
  const ldrawDownload = page.waitForEvent('download');
  await page.getByRole('button', { name: 'LDraw', exact: true }).click();
  expect((await ldrawDownload).suggestedFilename()).toContain('.ldr');
});
