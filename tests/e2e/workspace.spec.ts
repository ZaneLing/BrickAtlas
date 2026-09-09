import { readFile } from 'node:fs/promises';
import { expect, test } from '@playwright/test';

test('catalog exposes twelve projects, real previews and model parameters', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Brick Atlas' })).toBeVisible();
  await expect(page.locator('.floating-bricks > span')).toHaveCount(22);
  await expect(page.locator('.model-card')).toHaveCount(12);
  await expect(page.getByText('积木实例')).toBeVisible();
  await expect(page.locator('.model-card-explore')).toHaveCount(12);
  await expect(page.getByText('探索模型', { exact: true })).toHaveCount(0);
  await expect(page.getByRole('link', { name: '开始拼装' })).toHaveCount(12);
  await expect(page.locator('.model-card-specs')).toHaveCount(12);
  await expect(page.getByText('积木树').first()).toBeVisible();
  await expect(page.locator('.model-art img')).toHaveCount(12);
  expect(await page.locator('.model-art img').evaluateAll(images => images.every(image => (image as HTMLImageElement).naturalWidth >= 1000))).toBe(true);
  const position = await page.locator('.floating-bricks > span').first().evaluate(element => getComputedStyle(element).translate);
  await page.waitForTimeout(350);
  expect(await page.locator('.floating-bricks > span').first().evaluate(element => getComputedStyle(element).translate)).not.toBe(position);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
});

test('landing scroll story builds and explodes a live 3D model', async ({ page }) => {
  await page.goto('/');
  const story = page.getByRole('region', { name: '滚动式功能演示' });
  await story.scrollIntoViewIfNeeded();
  await expect(story.locator('canvas')).toBeVisible();
  await expect(story.getByText('实时渲染')).toBeVisible();
  const scrollStory = (progress: number) => page.evaluate(value => {
    const section = document.querySelector('.landing-story')!;
    const top = section.getBoundingClientRect().top + scrollY;
    scrollTo(0, top + (section.clientHeight - innerHeight) * value);
  }, progress);
  await scrollStory(0.25);
  await expect.poll(async () => page.evaluate(() => {
    const count = window.__landingAtlas?.().visibleInstances ?? 0;
    return count > 0 && count < 278;
  })).toBe(true);
  await scrollStory(0.9);
  await expect(story.getByText('三维拆分', { exact: true }).locator('..').locator('..')).toHaveClass(/active/);
  await expect.poll(async () => page.evaluate(() => window.__landingAtlas?.().actualExplosion ?? 0)).toBeGreaterThan(0.35);
});

test('language toggle translates the complete workspace and persists', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: '切换为英文' }).click();
  await expect(page.getByRole('heading', { name: 'See every brick. Build every idea.' })).toBeVisible();
  await expect(page.getByRole('link', { name: 'Browse models' })).toBeVisible();
  await expect(page.getByText('Tree nodes').first()).toBeVisible();
  await page.locator('.model-card-explore').first().click();
  await expect(page.getByText('Model ready', { exact: true })).toBeVisible();
  await expect(page.getByLabel('Search bricks', { exact: true })).toBeVisible();
  await page.reload();
  await expect(page.getByText('Model ready', { exact: true })).toBeVisible();
  expect(await page.locator('html').getAttribute('lang')).toBe('en');
});

test('clicking a project card opens explore while the only command is build', async ({ page }) => {
  await page.goto('/');
  await page.locator('.model-card-explore').first().click();
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

test('build mode advances, animates and persists progress per project', async ({ page }) => {
  await page.goto('/build/5867');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: '下一步' }).click();
  await expect(page.getByLabel('当前拼装步骤')).toHaveValue('1');
  await expect.poll(async () => page.evaluate(() => window.__atlas?.().visibleInstances)).toBe(6);
  await expect(page.getByRole('complementary', { name: '步骤说明书' })).toBeVisible();
  await expect(page.getByRole('region', { name: '本步所需零件' })).toContainText('本步所需零件');
  await expect(page.getByAltText('第 1 步静态拼装图')).toBeVisible();
  await page.waitForTimeout(850);
  expect((await page.evaluate(() => window.__atlas?.().offsets))?.filter(offset => offset.some(value => Math.abs(value) > 0.01)).length).toBe(0);
  await page.reload();
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  await expect(page.getByLabel('当前拼装步骤')).toHaveValue('1');
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
  await expect(page.getByAltText('第 1 步静态拼装图')).toBeVisible();
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

test('complex train and truck models load all addressable bricks', async ({ page }) => {
  for (const [id, count] of [['10014', 170], ['10156', 111], ['10001', 848], ['10128', 336], ['10036', 166], ['10159', 592]] as const) {
    await page.goto(`/explore/${id}`);
    await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
    await expect.poll(async () => page.evaluate(() => window.__atlas?.().loadedInstances)).toBe(count);
  }
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

test('image studio converts an image into bricks, steps, and exports', async ({ page }) => {
  await page.goto('/create');
  await expect(page.getByRole('region', { name: '图片转积木工作台' })).toBeVisible();
  await page.locator('input[accept^="image/"]').setInputFiles('public/models/5867/preview.png');
  await expect(page.locator('.image-stage-heading strong')).toHaveText('preview');
  await expect.poll(async () => page.evaluate(() => window.__imageBricks?.().bricks ?? 0)).toBeGreaterThan(20);
  const canvas = page.getByRole('img', { name: '图片生成的积木三维模型' });
  await expect(canvas).toBeVisible();
  const ratio = await canvas.evaluate(element => (element as HTMLCanvasElement).width / element.getBoundingClientRect().width);
  expect(ratio).toBeGreaterThanOrEqual(1.9);
  await page.getByLabel('拆分程度').fill('70');
  await expect.poll(async () => page.evaluate(() => window.__imageBricks?.().explosion ?? 0)).toBeGreaterThan(0.6);
  const bomDownload = page.waitForEvent('download');
  await page.getByRole('button', { name: 'BOM CSV' }).click();
  expect((await bomDownload).suggestedFilename()).toContain('-bom.csv');
  const ldrawDownload = page.waitForEvent('download');
  await page.getByRole('button', { name: 'LDraw', exact: true }).click();
  expect((await ldrawDownload).suggestedFilename()).toContain('.ldr');
});
