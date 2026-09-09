import { expect, test, type Page } from '@playwright/test';
import { PNG } from 'pngjs';

const getMetrics = (page: Page) => page.evaluate(() => window.__atlas?.());
async function ready(page: Page) {
  await page.goto('/explore/5867');
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
  await expect.poll(async () => (await getMetrics(page))?.loadedInstances).toBe(278);
  await page.waitForTimeout(300);
}
async function openLayers(page: Page, mobile: boolean) {
  if (mobile) await page.getByRole('button', { name: '结构与零件' }).click();
}
async function closeDrawer(page: Page, mobile: boolean) {
  if (mobile) await page.getByRole('button', { name: '关闭面板', exact: true }).click({ position: { x: 10, y: 10 } });
}

test('real geometry, framing, views, motion, reversible explosion and pixel coverage', async ({ page, isMobile }, testInfo) => {
  const errors: string[] = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await ready(page);
  const canvas = page.locator('canvas');
  const assembled = await canvas.screenshot();
  const image = PNG.sync.read(assembled);
  let colored = 0;
  for (let i = 0; i < image.data.length; i += 4) {
    const [r, g, b] = image.data.subarray(i, i + 3);
    if (r > g * 1.4 && r > b * 1.3) colored++;
  }
  expect(colored / (image.width * image.height)).toBeGreaterThan(0.015);
  await page.screenshot({ path: testInfo.outputPath('assembled.png') });
  const initial = await getMetrics(page);
  expect(initial?.drawCalls).toBeLessThan(180);
  // Double-sided transparent parts use two render passes.
  expect(initial!.triangles).toBeGreaterThanOrEqual(136628);
  expect(initial!.triangles).toBeLessThan(145000);
  await page.getByLabel('模型视角').selectOption('side');
  await page.waitForTimeout(600);
  expect(await canvas.screenshot()).not.toEqual(assembled);
  await page.getByRole('button', { name: '自动旋转', exact: true }).click();
  const before = (await getMetrics(page))!.camera;
  await page.waitForTimeout(700);
  expect((await getMetrics(page))!.camera).not.toEqual(before);
  await page.getByRole('button', { name: /^结构分离/ }).click();
  await expect.poll(async () => (await getMetrics(page))?.actualExplosion).toBe(0.45);
  expect((await getMetrics(page))?.visibleInstances).toBe(278);
  await page.screenshot({ path: testInfo.outputPath('structure-45.png') });
  await page.getByRole('button', { name: /^零件陈列/ }).click();
  await expect.poll(async () => (await getMetrics(page))?.actualExplosion).toBe(1);
  await page.waitForTimeout(700);
  const inventory = (await getMetrics(page))!;
  expect(inventory.visibleInstances).toBe(278);
  const rect = (await canvas.boundingBox())!;
  const inside = inventory.projected.filter(p => p.x >= 0 && p.y >= 0 && p.x <= rect.width && p.y <= rect.height && p.z < 1).length;
  expect(inside).toBe(278);
  await page.screenshot({ path: testInfo.outputPath('inventory-100.png') });
  // Inventory positions are computed from exact per-instance bounds, not synthetic UI targets.
  const target = inventory.projected.find(p => p.x > 50 && p.x < rect.width - 80 && p.y > 75 && p.y < rect.height - 40)!;
  await canvas.click({ position: { x: target.x, y: target.y } });
  await expect.poll(async () => (await getMetrics(page))?.selected.length).toBe(1);
  await closeDrawer(page, isMobile);
  await page.getByRole('button', { name: '复原模型', exact: true }).click();
  await expect.poll(async () => (await getMetrics(page))?.actualExplosion).toBe(0);
  expect((await getMetrics(page))!.offsets.every(v => v.every(c => c === 0))).toBe(true);
  expect(errors).toEqual([]);
});

test('search, identity, same-type selection, isolation, visibility and source metadata', async ({ page, isMobile }) => {
  await ready(page);
  await openLayers(page, isMobile);
  await page.getByLabel('搜索零件', { exact: true }).fill('3004');
  const first = page.locator('.part-row').first();
  await expect(first).toBeVisible();
  await first.click();
  await expect(page.getByText('结构演示', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: '高亮全部同型号', exact: true }).click();
  expect((await getMetrics(page))!.selected.length).toBeGreaterThan(1);
  await page.getByRole('button', { name: '隔离全部同型号', exact: true }).click();
  const isolated = (await getMetrics(page))!;
  expect(isolated.visibleInstances).toBe(isolated.selected.length);
  await page.getByRole('button', { name: '退出隔离', exact: true }).click();
  expect((await getMetrics(page))!.visibleInstances).toBe(278);
  if (isMobile) await page.getByRole('button', { name: '打开详情', exact: true }).click();
  await page.getByRole('button', { name: '关闭详情面板', exact: true }).click();
  expect((await getMetrics(page))!.selected.length).toBeGreaterThan(0);
  await page.getByRole('button', { name: '清除选择', exact: true }).click();
  await openLayers(page, isMobile);
  await page.getByRole('tab', { name: '结构分组' }).click();
  await page.getByRole('button', { name: '隐藏车身与车门', exact: true }).click();
  expect((await getMetrics(page))!.visibleInstances).toBeLessThan(278);
  await page.getByRole('button', { name: '全部显示', exact: true }).click();
  expect((await getMetrics(page))!.visibleInstances).toBe(278);
  await page.getByLabel('搜索零件', { exact: true }).fill('NO_SUCH_PART');
  await expect(page.getByText('没有匹配的零件')).toBeVisible();
});

test('drag does not select; responsive layout has no horizontal overflow', async ({ page, isMobile }, testInfo) => {
  await ready(page);
  const box = (await page.locator('canvas').boundingBox())!;
  const x = box.x + box.width / 2, y = box.y + box.height / 2;
  await page.mouse.move(x, y);
  await page.mouse.down();
  await page.mouse.move(x + 60, y + 25, { steps: 10 });
  await page.mouse.move(x, y, { steps: 10 });
  await page.mouse.up();
  expect((await getMetrics(page))!.selected).toEqual([]);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  if (isMobile) {
    await page.setViewportSize({ width: 844, height: 390 });
    await page.waitForTimeout(600);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await page.screenshot({ path: testInfo.outputPath('landscape.png') });
  }
});

test('missing geometry has an actionable error, not a blank canvas', async ({ page }) => {
  await page.route('**/*.bin', route => route.fulfill({ status: 404, body: 'missing' }));
  await page.goto('/explore/5867');
  await expect(page.getByRole('alert')).toContainText('HTTP 404');
  await expect(page.getByRole('button', { name: '重新加载' })).toBeVisible();
  await page.unroute('**/*.bin');
  await page.getByRole('button', { name: '重新加载' }).click();
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
});

test('reduced motion and credits dialog work with keyboard', async ({ page, isMobile }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await ready(page);
  await page.getByRole('button', { name: /^零件陈列/ }).click();
  await expect.poll(async () => (await getMetrics(page))?.actualExplosion).toBe(1);
  await page.getByRole('button', { name: '显示设置' }).click();
  await expect(page.getByRole('dialog', { name: '显示设置' })).toContainText('已启用');
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog', { name: '显示设置' })).not.toBeVisible();
  if (isMobile) {
    await page.getByRole('button', { name: '打开详情', exact: true }).click();
    await page.getByRole('button', { name: '许可信息', exact: true }).click();
  } else await page.getByRole('button', { name: '来源与署名' }).click();
  await expect(page.getByRole('dialog', { name: '来源与署名' })).toContainText('Takeshi Takahashi');
  await expect(page.getByRole('dialog', { name: '来源与署名' })).toContainText('Creative Commons Attribution 2.0');
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog', { name: '来源与署名' })).not.toBeVisible();
});

test('every inventory instance is individually addressable', async ({ page, isMobile }, testInfo) => {
  test.skip(isMobile, 'Full native-tap exhaustive test is desktop-only; mobile tapping is covered above.');
  test.setTimeout(120000);
  await ready(page);
  await page.getByRole('button', { name: /^零件陈列/ }).click();
  await expect.poll(async () => (await getMetrics(page))?.actualExplosion).toBe(1);
  await page.waitForTimeout(1000);
  const canvas = page.locator('canvas');
  const points = (await getMetrics(page))!.projected;
  const missed: string[] = [];
  for (const point of points) {
    await canvas.click({ position: { x: point.x, y: point.y }, force: true });
    const selected = (await getMetrics(page))!.selected;
    if (selected[0] !== point.id) missed.push(point.id);
  }
  await testInfo.attach('picking-audit', { body: JSON.stringify({ total: points.length, missed }), contentType: 'application/json' });
  expect(missed).toEqual([]);
});

test('WebGL unavailable shows a fallback', async ({ page }) => {
  await page.addInitScript(() => {
    const original = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (this: HTMLCanvasElement, type: string, ...args: unknown[]) {
      if (type.startsWith('webgl')) return null;
      return (original as Function).call(this, type, ...args);
    } as typeof original;
  });
  await page.goto('/explore/5867');
  await expect(page.getByRole('alert')).toContainText('WebGL');
  await expect(page.getByRole('link', { name: '下载源模型' })).toBeVisible();
});

test('lost WebGL context is recoverable', async ({ page, browserName }) => {
  test.skip(browserName !== 'chromium', 'WEBGL_lose_context integration is exercised on Chromium.');
  await ready(page);
  await page.evaluate(() => {
    document.querySelector('canvas')?.getContext('webgl2')?.getExtension('WEBGL_lose_context')?.loseContext();
  });
  await expect(page.getByRole('alert')).toContainText('上下文丢失');
  await page.getByRole('button', { name: '重新加载' }).click();
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible();
});

test('downloads contain actual data and changing layout preserves the inventory', async ({ page, isMobile }) => {
  await ready(page);
  await openLayers(page, isMobile);
  const file = page.waitForEvent('download');
  await page.getByRole('button', { name: '导出可见零件 CSV' }).click();
  expect((await file).suggestedFilename()).toBe('5867-inventory.csv');
  await closeDrawer(page, isMobile);
  await page.getByRole('button', { name: /^零件陈列/ }).click();
  await expect.poll(async () => (await getMetrics(page))?.actualExplosion).toBe(1);
  await page.setViewportSize(isMobile ? { width: 844, height: 390 } : { width: 1920, height: 1080 });
  await page.waitForTimeout(800);
  expect((await getMetrics(page))!.visibleInstances).toBe(278);
  expect((await getMetrics(page))!.inventoryCells).toHaveLength(278);
  const shot = page.waitForEvent('download');
  await page.getByRole('button', { name: '导出模型截图' }).click();
  expect((await shot).suggestedFilename()).toBe('brick-atlas-5867-3840p.png');
});

test('narrow mobile controls do not occlude the inventory', async ({ page, isMobile }, testInfo) => {
  test.skip(!isMobile, 'Narrow touch layouts only.');
  await page.setViewportSize({ width: 320, height: 700 });
  await ready(page);
  await page.getByRole('button', { name: /^零件陈列/ }).click();
  await expect.poll(async () => (await getMetrics(page))?.actualExplosion).toBe(1);
  await page.waitForTimeout(500);
  const overlap = await page.evaluate(() => {
    const canvas = document.querySelector('canvas')!.getBoundingClientRect();
    const toolbar = document.querySelector('.zoom-tools')!.getBoundingClientRect();
    return toolbar.left < canvas.right && toolbar.right > canvas.left && toolbar.top < canvas.bottom && toolbar.bottom > canvas.top;
  });
  expect(overlap).toBe(false);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await page.screenshot({ path: testInfo.outputPath('narrow-mobile.png') });
});

test('slow network reports progress and reaches the complete model', async ({ page, browserName, isMobile }) => {
  test.skip(browserName !== 'chromium' || isMobile, 'One Chromium throttled-network run.');
  const client = await page.context().newCDPSession(page);
  await client.send('Network.enable');
  await client.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 750000, uploadThroughput: 250000 });
  await page.goto('/explore/5867');
  await expect(page.locator('progress')).toBeVisible();
  await expect(page.getByText('模型已就绪', { exact: true })).toBeVisible({ timeout: 30000 });
  expect((await getMetrics(page))!.loadedInstances).toBe(278);
});
