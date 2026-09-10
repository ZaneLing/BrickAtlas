import { test, expect, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { PNG } from 'pngjs';
import { readFile } from 'node:fs/promises';

async function ground(page: Page, x = 0, z = 0) {
  const canvas = page.locator('.diy-canvas canvas');
  const box = (await canvas.boundingBox())!;
  const point = await page.evaluate(({ x, z }) => window.__diy!().grid.find(point => point.worldX === x && point.worldZ === z)!, { x, z });
  return { x: box.x + point.x, y: box.y + point.y };
}
async function placeAt(page: Page, x = 0, z = 0) {
  const point = await ground(page, x, z);
  await page.mouse.move(point.x, point.y);
  await expect.poll(() => page.evaluate(() => window.__diy!().preview)).toBe(true);
  await page.mouse.click(point.x, point.y);
}

test('mouse preview follows, stamps continuously, rotates, stacks, paints and undoes', async ({ page }) => {
  await page.goto('/diy');
  await page.getByRole('button', { name: '选取基础砖 2×4', exact: true }).click();
  const first = await ground(page, 0, 0), second = await ground(page, 8, 0);
  await page.mouse.move(first.x, first.y);
  await expect.poll(() => page.evaluate(() => window.__diy!().preview)).toBe(true);
  const hover = await page.evaluate(() => window.__diy!().hover);
  await page.mouse.move(second.x, second.y, { steps: 5 });
  await expect.poll(() => page.evaluate(() => window.__diy!().hover?.x)).not.toBe(hover!.x);
  await page.getByRole('button', { name: '旋转待放积木 90°' }).click();
  await placeAt(page);
  await expect.poll(() => page.evaluate(() => window.__diy!().count)).toBe(1);
  expect(await page.evaluate(() => window.__diy!().bricks[0].turn)).toBe(1);
  await page.mouse.move(100, 50);
  await expect.poll(() => page.evaluate(() => window.__diy!().preview)).toBe(false);
  const box = (await page.locator('.diy-canvas canvas').boundingBox())!;
  const top = await page.evaluate(() => window.__diy!().bricks[0].screen);
  await page.mouse.move(box.x + top.x, box.y + top.y);
  await expect.poll(() => page.evaluate(() => window.__diy!().hover?.y)).toBe(3);
  await page.mouse.click(box.x + top.x, box.y + top.y);
  await expect.poll(() => page.evaluate(() => window.__diy!().count)).toBe(2);
  await page.getByRole('button', { name: '选择亮蓝色', exact: true }).click();
  await page.getByRole('button', { name: '涂色', exact: true }).click();
  const target = await page.evaluate(() => window.__diy!().bricks[1].screen);
  await page.mouse.click(box.x + target.x, box.y + target.y);
  await expect.poll(() => page.evaluate(() => window.__diy!().bricks[1].color)).toBe('blue');
  await page.getByRole('button', { name: '撤销', exact: true }).click();
  await expect.poll(() => page.evaluate(() => window.__diy!().bricks[1].color)).toBe('red');
  await page.getByRole('button', { name: '撤销', exact: true }).click();
  await expect.poll(() => page.evaluate(() => window.__diy!().count)).toBe(1);
  await page.getByRole('button', { name: '重做', exact: true }).click();
  await expect.poll(() => page.evaluate(() => window.__diy!().count)).toBe(2);
});

test('expanded categories expose real shapes and tactile brick effects', async ({ page }) => {
  await page.goto('/diy');
  await expect(page.getByRole('tab', { name: /零件/ })).toContainText('78');
  await page.getByRole('button', { name: /Technic 9/ }).click();
  await expect(page.getByRole('button', { name: '选取Technic 孔砖 1×16' })).toBeVisible();
  await expect(page.getByRole('button', { name: '选取基础砖 2×4' })).toHaveCount(0);
  await expect.poll(() => page.locator('.diy-part canvas').first().evaluate((canvas: HTMLCanvasElement) =>
    canvas.getContext('2d')!.getImageData(0, 0, canvas.width, canvas.height).data.some((value, i) => i % 4 === 3 && value > 0),
  )).toBe(true);
  const technic = page.getByRole('button', { name: '选取Technic 孔砖 1×4' });
  await technic.click();
  await expect(page.locator('.brick-shatter-piece')).toHaveCount(14);
  await expect(page.locator('.brick-shatter-piece')).toHaveCount(0, { timeout: 1500 });
  await page.getByRole('button', { name: /建筑件 6/ }).click();
  await expect(page.getByRole('button', { name: '选取拱门 1×5×4' })).toBeVisible();
  await page.getByRole('button', { name: /连接件 11/ }).click();
  await expect(page.getByRole('button', { name: '选取Technic 摩擦销' })).toBeVisible();
  await page.getByRole('button', { name: /全部 78/ }).click();
  await page.getByLabel('搜索 DIY 素材').fill('clip');
  await expect(page.locator('.diy-part')).toHaveCount(5);
  await page.getByLabel('搜索 DIY 素材').fill('');
  await page.getByRole('button', { name: '选取圆锥 2×2×2' }).click();
  await placeAt(page);
  await expect(page.locator('.brick-placement-ring')).toHaveCount(1);
  await expect(page.locator('.brick-placement-ring')).toHaveCount(0, { timeout: 1500 });
  expect(await page.evaluate(() => window.__diy!().bricks[0].partId)).toBe('3942c');
  await page.getByRole('tab', { name: /小组件/ }).click();
  await expect(page.getByRole('tab', { name: /小组件/ })).toContainText('12');
  await page.getByRole('button', { name: '选取小树' }).click();
  await placeAt(page, 8, 0);
  await expect.poll(() => page.evaluate(() => window.__diy!().count)).toBe(4);
  expect(await page.evaluate(() => [...new Set(window.__diy!().bricks.slice(1).map(brick => brick.color))].sort())).toEqual(['brown', 'green']);
});

test('dragging never places and collisions are rejected on a locked layer', async ({ page }) => {
  await page.goto('/diy');
  const point = await ground(page);
  await page.mouse.move(point.x, point.y);
  await page.mouse.down();
  await page.mouse.move(point.x + 80, point.y + 25, { steps: 8 });
  await page.mouse.up();
  expect(await page.evaluate(() => window.__diy!().count)).toBe(0);
  await page.getByRole('button', { name: '适配全部积木' }).click();
  await page.getByLabel('自动叠放', { exact: true }).uncheck();
  await placeAt(page);
  await expect.poll(() => page.evaluate(() => window.__diy!().count)).toBe(1);
  const hover = await page.evaluate(() => window.__diy!().hover);
  await placeAt(page);
  expect(await page.evaluate(() => window.__diy!().count)).toBe(1);
  expect(await page.evaluate(() => window.__diy!().hover?.issue)).toBe('overlap');
  expect(hover?.y).toBe(0);
});

test('assemblies are atomic, ground extends, persistence and file exports work', async ({ page }, testInfo) => {
  await page.goto('/diy');
  await page.getByRole('tab', { name: /小组件/ }).click();
  await page.getByRole('button', { name: '选取小桌子' }).click();
  await placeAt(page);
  await expect.poll(() => page.evaluate(() => window.__diy!().count)).toBe(5);
  await page.getByRole('button', { name: '撤销', exact: true }).click();
  await expect.poll(() => page.evaluate(() => window.__diy!().count)).toBe(0);
  await page.getByRole('button', { name: '重做', exact: true }).click();
  await expect.poll(() => page.evaluate(() => window.__diy!().count)).toBe(5);
  for (let i = 0; i < 12; i++) await page.getByRole('button', { name: '向东平移' }).click();
  await expect.poll(() => page.evaluate(() => window.__diy!().target[0])).toBeGreaterThan(180);
  const canvas = (await page.locator('.diy-canvas canvas').boundingBox())!;
  await page.mouse.click(canvas.x + canvas.width * 0.5, canvas.y + canvas.height * 0.55);
  await expect.poll(() => page.evaluate(() => window.__diy!().count)).toBe(10);
  const metrics = await page.evaluate(() => window.__diy!());
  expect(metrics.bricks.some(brick => brick.x > 150)).toBe(true);
  expect(metrics.groundInstances).toBe(6400);
  expect(metrics.drawCalls).toBeLessThan(20);
  await page.getByRole('button', { name: '保存 DIY' }).click();
  await page.reload();
  await expect.poll(() => page.evaluate(() => window.__diy?.().count)).toBe(10);
  await page.locator('.diy-download summary').click();
  const event = page.waitForEvent('download');
  await page.getByRole('button', { name: 'JSON', exact: true }).click();
  const file = await event;
  await file.saveAs(testInfo.outputPath('diy.json'));
  await page.getByRole('button', { name: '清空底板' }).click();
  await page.getByRole('button', { name: '确认清空' }).click();
  await expect.poll(() => page.evaluate(() => window.__diy!().count)).toBe(0);
  await page.getByLabel('导入 DIY JSON').setInputFiles(testInfo.outputPath('diy.json'));
  await expect.poll(() => page.evaluate(() => window.__diy!().count)).toBe(10);
  for (const format of ['PNG', 'LDraw', 'BOM CSV']) {
    await page.locator('.diy-download summary').click();
    const event = page.waitForEvent('download');
    await page.getByRole('button', { name: format, exact: true }).click();
    const file = await event;
    const path = testInfo.outputPath(file.suggestedFilename());
    await file.saveAs(path);
    const bytes = await readFile(path);
    if (format === 'PNG') expect(PNG.sync.read(bytes).width).toBeGreaterThan(1000);
    if (format === 'LDraw') expect(bytes.toString().split('\n').filter(line => line.startsWith('1 '))).toHaveLength(10);
    if (format === 'BOM CSV') expect(bytes.toString()).toContain('partId,colorCode,color,quantity');
  }
});

test('large projects remain batched and storage failures keep editing available', async ({ page }, testInfo) => {
  await page.addInitScript(() => {
    localStorage.setItem('brick-atlas-diy-v1', JSON.stringify({
      version: 1, name: 'Batch test', bricks: Array.from({ length: 2500 }, (_, i) => ({
        id: `b${i}`, stampId: `s${i}`, partId: '3005', color: i % 2 ? 'red' : 'blue',
        x: i % 50 * 2 - 50, y: 0, z: Math.floor(i / 50) * 2 - 50, turn: 0,
      })),
    }));
    const original = Storage.prototype.setItem;
    Storage.prototype.setItem = function(key, value) {
      if (key === 'brick-atlas-diy-v1') throw new DOMException('Quota exceeded', 'QuotaExceededError');
      original.call(this, key, value);
    };
  });
  await page.goto('/diy');
  await expect.poll(() => page.evaluate(() => window.__diy?.().count)).toBe(2500);
  await page.getByRole('button', { name: '适配全部积木' }).click();
  const box = (await page.locator('.diy-canvas canvas').boundingBox())!;
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  await expect.poll(() => page.evaluate(() => window.__diy!().preview)).toBe(true);
  const metrics = await page.evaluate(() => window.__diy!());
  expect(metrics.batches).toBe(1);
  expect(metrics.drawCalls).toBeLessThan(12);
  expect(metrics.frameMs).toBeLessThan(80);
  await testInfo.attach('batch-metrics', { body: JSON.stringify({ count: metrics.count, batches: metrics.batches, calls: metrics.drawCalls, frameMs: metrics.frameMs }), contentType: 'application/json' });
  await page.getByRole('button', { name: '保存 DIY' }).click();
  await expect(page.getByRole('alert')).toContainText('浏览器保存失败');
  await expect(page.locator('.diy-canvas canvas')).toBeVisible();
});

test('desktop screenshots contain geometry, thumbnails and accessible controls', async ({ page }, testInfo) => {
  test.setTimeout(90000);
  const errors: string[] = [];
  page.on('pageerror', error => errors.push(error.message));
  for (const width of [1180, 1440, 3840]) {
    await page.setViewportSize({ width, height: width === 3840 ? 2160 : 900 });
    await page.goto('/diy');
    await page.getByRole('tab', { name: /小组件/ }).click();
    await page.getByRole('button', { name: '选取小门廊' }).click();
    await placeAt(page, -8, 0);
    await page.getByRole('button', { name: '选择亮蓝色' }).click();
    await page.getByRole('button', { name: '选取小台阶' }).click();
    await placeAt(page, 8, 0);
    await page.mouse.move(100, 50);
    await page.waitForTimeout(250);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    const image = PNG.sync.read(await page.locator('.diy-canvas canvas').screenshot());
    const colors = new Set<number>();
    for (let i = 0; i < image.data.length; i += 400) colors.add(image.data.readUInt32BE(i));
    expect(colors.size).toBeGreaterThan(50);
    const path = testInfo.outputPath(`diy-${width}.png`);
    await page.screenshot({ path });
    await testInfo.attach(`diy-${width}`, { path, contentType: 'image/png' });
    expect(await page.locator('.diy-part canvas').first().evaluate((canvas: HTMLCanvasElement) => canvas.getContext('2d')!.getImageData(0, 0, canvas.width, canvas.height).data.some((value, i) => i % 4 === 3 && value > 0))).toBe(true);
    if (width === 1440) {
      await page.getByRole('tab', { name: /零件/ }).click();
      await page.getByRole('button', { name: /Technic 9/ }).click();
      await expect.poll(() => page.locator('.diy-part canvas').first().evaluate((canvas: HTMLCanvasElement) =>
        canvas.getContext('2d')!.getImageData(0, 0, canvas.width, canvas.height).data.some((value, i) => i % 4 === 3 && value > 0),
      )).toBe(true);
      const libraryPath = testInfo.outputPath('diy-1440-technic-library.png');
      await page.screenshot({ path: libraryPath });
      await testInfo.attach('diy-1440-technic-library', { path: libraryPath, contentType: 'image/png' });
    }
  }
  expect(errors).toEqual([]);
  const axe = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze();
  expect(axe.violations.map(v => ({ id: v.id, nodes: v.nodes.map(n => n.target) }))).toEqual([]);
});
