import { expect, test } from '@playwright/test';
import { PNG } from 'pngjs';
import { modelCatalog } from '../../atlas.config';

test('Create and Compose restart updates the actual GPU state', async ({ page }) => {
  for (const route of ['/create', '/compose']) {
    await page.goto(route);
    if (route === '/compose') {
      await page.getByRole('tab', { name: '拼装', exact: true }).click();
    }
    await page.getByRole('button', { name: '回到开始', exact: true }).click();
    await expect.poll(() => page.evaluate(route =>
      route === '/create' ? window.__imageBricks?.().drawnInstances : window.__composer?.().drawnInstances, route)).toBe(0);
    await page.getByRole('button', { name: '下一步', exact: true }).click();
    await expect.poll(() => page.evaluate(route =>
      route === '/create' ? window.__imageBricks?.().drawnInstances : window.__composer?.().drawnInstances, route)).toBeGreaterThan(0);
    await page.waitForTimeout(800);
    await page.getByRole('button', { name: '回到开始', exact: true }).click();
    await expect.poll(() => page.evaluate(route =>
      route === '/create' ? window.__imageBricks?.().drawnInstances : window.__composer?.().drawnInstances, route)).toBe(0);
  }
});

test('Compose retains real source geometry and does not rebuild on selection, rename or mode', async ({ page }) => {
  await page.goto('/compose');
  await page.getByRole('button', { name: '添加水上飞机' }).click();
  await expect.poll(() => page.evaluate(() => window.__composer?.().sourceModels)).toBe(1);
  await expect.poll(() => page.evaluate(() => window.__composer?.().triangles ?? 0)).toBeGreaterThan(21000);
  const revision = await page.evaluate(() => window.__composer!().buildRevision);
  await page.locator('.compose-tree-base').click();
  await page.getByLabel('项目名称').fill('Scene audit');
  await page.getByRole('tab', { name: '拼装', exact: true }).click();
  expect(await page.evaluate(() => window.__composer!().buildRevision)).toBe(revision);
  await page.getByRole('tab', { name: '场景', exact: true }).click();
  await expect(page.getByRole('button', { name: '添加积木小猫' })).toBeVisible();
  await expect(page.getByRole('button', { name: '添加城市小人' })).toBeVisible();
});

test('corrupt image and saved composition fail safely', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('brick-atlas-composition-v1', '{"version":1,"items":[{}]}'));
  await page.goto('/compose');
  await expect.poll(() => page.evaluate(() => window.__composer?.().items)).toBe(0);
  await page.goto('/create');
  await page.getByLabel('上传正视图').setInputFiles({ name: 'invalid.png', mimeType: 'image/png', buffer: Buffer.from('not an image') });
  await expect(page.getByRole('alert')).toContainText('图片解码失败');
  await expect(page.locator('.image-brick-canvas canvas')).toBeVisible();
});

test('portrait cropping stays square on screen and supports re-upload after removal', async ({ page }) => {
  const image = new PNG({ width: 80, height: 240 });
  for (let i = 0; i < image.data.length; i += 4) image.data.set([190, 30, 20, 255], i);
  const file = { name: 'portrait.png', mimeType: 'image/png', buffer: PNG.sync.write(image) };
  await page.goto('/create');
  await page.getByLabel('上传正视图').setInputFiles(file);
  const crop = page.locator('.crop-selection').first();
  await expect(crop).toBeVisible();
  const box = (await crop.boundingBox())!;
  expect(Math.abs(box.width - box.height)).toBeLessThan(1);
  await page.getByRole('button', { name: '移除正视图' }).click();
  await page.getByLabel('上传正视图').setInputFiles(file);
  await expect(crop).toBeVisible();
});

test('every catalog model loads its full instance set', async ({ page, request }) => {
  test.setTimeout(120000);
  for (const config of modelCatalog) {
    const manifest = await (await request.get(`/models/${config.id}/manifest.json`)).json();
    await page.goto(`/explore/${config.id}`);
    await page.getByText('模型已就绪', { exact: true }).waitFor();
    expect(await page.evaluate(() => window.__atlas!().loadedInstances)).toBe(manifest.instances.length);
  }
});

test('corrupt geometry is rejected by checksum and a retry recovers', async ({ page }) => {
  await page.route('**/models/31028/*.bin', route => route.fulfill({ body: Buffer.from('corrupt'), contentType: 'application/octet-stream' }));
  await page.goto('/explore/31028');
  await expect(page.getByText(/Asset checksum mismatch/)).toBeVisible();
  await page.unroute('**/models/31028/*.bin');
  await page.reload();
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
});

test('all workspace surfaces have visible pixels and accessible controls at desktop sizes', async ({ page }, testInfo) => {
  test.setTimeout(120000);
  const errors: string[] = [];
  page.on('pageerror', error => errors.push(error.message));
  for (const width of [1180, 1440, 3840]) {
    await page.setViewportSize({ width, height: width === 3840 ? 2160 : 900 });
    for (const route of ['/', '/explore/31028', '/build/31027', '/create', '/compose']) {
      await page.goto(route);
      if (route.startsWith('/explore') || route.startsWith('/build')) await page.getByText('模型已就绪', { exact: true }).waitFor();
      if (route.startsWith('/build')) {
        await page.getByRole('slider', { name: '当前拼装步骤' }).fill('1');
        await page.getByAltText('第 1 步动态拼装图').waitFor();
      }
      if (route === '/compose') {
        await page.getByRole('button', { name: '添加水上飞机' }).click();
        await expect.poll(() => page.evaluate(() => window.__composer?.().sourceModels ?? 0)).toBeGreaterThan(0);
        expect(await page.locator('.compose-mode-tabs').evaluate(element => {
          const rect = element.getBoundingClientRect();
          const parent = element.closest('.compose-stage')!.getBoundingClientRect();
          return rect.right <= parent.right && rect.left >= parent.left;
        })).toBe(true);
      }
      await page.waitForTimeout(600);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
      const path = testInfo.outputPath(`${width}-${route.replaceAll('/', '_') || 'home'}.png`);
      await page.screenshot({ path });
      await testInfo.attach(`${width} ${route}`, { path, contentType: 'image/png' });
      const canvas = page.locator('.canvas-host canvas, .image-brick-canvas canvas, .compose-canvas canvas').first();
      if (await canvas.count()) {
        const image = PNG.sync.read(await canvas.screenshot());
        const colors = new Set<number>();
        for (let i = 0; i < image.data.length; i += 400) colors.add(image.data.readUInt32BE(i));
        expect(colors.size).toBeGreaterThan(12);
      }
    }
  }
  expect(errors).toEqual([]);
});
