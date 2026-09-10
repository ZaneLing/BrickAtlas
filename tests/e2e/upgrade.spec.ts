import { expect, test } from '@playwright/test';
import { PNG } from 'pngjs';

function tetrahedronGlb() {
  const positions = new Float32Array([
    0, 0, 0, 0, 1, 0, 1, 0, 0,
    0, 0, 0, 1, 0, 0, 0, 0, 1,
    0, 0, 0, 0, 0, 1, 0, 1, 0,
    1, 0, 0, 0, 1, 0, 0, 0, 1,
  ]);
  const json = Buffer.from(JSON.stringify({
    asset: { version: '2.0' }, scene: 0, scenes: [{ nodes: [0] }], nodes: [{ mesh: 0 }],
    meshes: [{ primitives: [{ attributes: { POSITION: 0 } }] }],
    buffers: [{ byteLength: positions.byteLength }],
    bufferViews: [{ buffer: 0, byteOffset: 0, byteLength: positions.byteLength }],
    accessors: [{ bufferView: 0, componentType: 5126, count: 12, type: 'VEC3', min: [0, 0, 0], max: [1, 1, 1] }],
  }));
  const padded = Math.ceil(json.length / 4) * 4;
  const buffer = Buffer.alloc(28 + padded + positions.byteLength);
  buffer.writeUInt32LE(0x46546c67, 0); buffer.writeUInt32LE(2, 4); buffer.writeUInt32LE(buffer.length, 8);
  buffer.writeUInt32LE(padded, 12); buffer.writeUInt32LE(0x4e4f534a, 16);
  buffer.fill(32, 20, 20 + padded); json.copy(buffer, 20);
  buffer.writeUInt32LE(positions.byteLength, 20 + padded); buffer.writeUInt32LE(0x004e4942, 24 + padded);
  Buffer.from(positions.buffer).copy(buffer, 28 + padded);
  return buffer;
}

test('lobby filters, favorites and continuation persist across navigation', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('searchbox', { name: '搜索模型' }).fill('blue racer');
  await expect(page.locator('.model-card')).toHaveCount(1);
  await page.getByRole('button', { name: '收藏 Blue Racer', exact: true }).click();
  await page.reload();
  await page.getByLabel('游玩状态').selectOption('favorites');
  await expect(page.locator('.model-card')).toHaveCount(1);
  await expect(page.getByRole('heading', { name: 'Blue Racer', exact: true })).toBeVisible();
  await page.getByLabel('模型难度').selectOption('5');
  await expect(page.getByText('没有符合条件的模型')).toBeVisible();
  await page.getByRole('button', { name: '重置筛选' }).click();
  await expect(page.locator('.model-card')).toHaveCount(15);
});

test('Compose preserves corrupt input and supports undo, redo, import and snapshots', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('brick-atlas-composition-v1', '{"invalid":true}'));
  await page.goto('/compose');
  await expect(page.getByRole('alert')).toContainText('原始存档尚未覆盖');
  await page.waitForTimeout(700);
  expect(await page.evaluate(() => localStorage.getItem('brick-atlas-composition-v1'))).toBe('{"invalid":true}');
  await page.getByRole('tab', { name: '零件', exact: true }).click();
  await page.getByRole('button', { name: '添加基础砖 2×4', exact: true }).click();
  await expect.poll(() => page.evaluate(() => window.__composer?.().items)).toBe(1);
  const original = await page.evaluate(() => window.__composer!().bricks);
  await page.getByRole('button', { name: '撤销', exact: true }).click();
  await expect.poll(() => page.evaluate(() => window.__composer?.().items)).toBe(0);
  await page.getByRole('button', { name: '重做', exact: true }).click();
  await expect.poll(() => page.evaluate(() => window.__composer?.().bricks)).toBe(original);
  await page.getByRole('button', { name: '作品快照', exact: true }).click();
  await page.getByRole('button', { name: /保存当前作品快照/ }).click();
  await expect(page.locator('.project-shelf-row')).toHaveCount(1);
  await page.getByRole('button', { name: '关闭弹窗' }).click();
  await page.getByRole('button', { name: '保存', exact: true }).click();
  const json = await page.evaluate(() => localStorage.getItem('brick-atlas-composition-v1')!);
  await page.getByLabel('导入组建 JSON').setInputFiles({ name: 'scene.json', mimeType: 'application/json', buffer: Buffer.from(json) });
  await page.getByRole('button', { name: '打开项目', exact: true }).click();
  await expect.poll(() => page.evaluate(() => window.__composer?.().items)).toBe(1);
});

test('DIY precise edits flush immediately on leaving and snapshots restore with undo', async ({ page }) => {
  const project = { version: 1, name: 'Move test', bricks: [{ id: 'one', partId: '3001', color: 'red', x: 0, y: 0, z: 0, turn: 0, stampId: 'one' }] };
  await page.goto('/diy');
  await page.getByLabel('导入 DIY JSON').setInputFiles({ name: 'diy.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(project)) });
  await expect.poll(() => page.evaluate(() => window.__diy?.().bricks.length)).toBe(1);
  await page.getByRole('button', { name: '选择与旋转视图', exact: true }).click();
  const screen = await page.evaluate(() => window.__diy!().bricks[0].screen);
  const canvasBox = (await page.locator('.diy-canvas').boundingBox())!;
  await page.mouse.click(canvasBox.x + screen.x, canvasBox.y + screen.y);
  await page.getByLabel('选中积木 X', { exact: true }).fill('4');
  await expect.poll(() => page.evaluate(() => window.__diy!().bricks[0].x)).toBe(4);
  await page.getByRole('button', { name: '复制选中积木' }).click();
  await expect.poll(() => page.evaluate(() => window.__diy?.().bricks.length)).toBe(2);
  await page.getByRole('button', { name: '撤销', exact: true }).click();
  await expect.poll(() => page.evaluate(() => window.__diy?.().bricks.length)).toBe(1);
  await page.getByRole('button', { name: '作品快照', exact: true }).click();
  await page.getByRole('button', { name: /保存当前作品快照/ }).click();
  await page.getByRole('button', { name: '关闭弹窗' }).click();
  await page.getByLabel('DIY 项目名称').fill('Last edit');
  await page.getByRole('link', { name: '组件组建', exact: true }).click();
  const saved = await page.evaluate(() => JSON.parse(localStorage.getItem('brick-atlas-diy-v1')!));
  expect(saved.name).toBe('Last edit');
  expect(saved.bricks).toHaveLength(1);
  await page.goto('/diy');
  await page.getByRole('button', { name: '作品快照', exact: true }).click();
  await page.getByRole('button', { name: '打开快照 Move test', exact: true }).click();
  await page.getByRole('button', { name: '确认', exact: true }).click();
  await expect(page.getByLabel('DIY 项目名称')).toHaveValue('Move test');
  await page.getByRole('button', { name: '撤销', exact: true }).click();
  await expect(page.getByLabel('DIY 项目名称')).toHaveValue('Last edit');
});

test('local GLB converts without cloud calls and rejects malformed files', async ({ page }) => {
  await page.goto('/create');
  await page.getByLabel('导入 GLB 网格').setInputFiles({ name: 'tetrahedron.glb', mimeType: 'model/gltf-binary', buffer: tetrahedronGlb() });
  await expect.poll(() => page.evaluate(() => window.__imageBricks?.().bricks ?? 0)).toBeGreaterThan(0);
  await expect.poll(() => page.evaluate(() => window.__imageMesh?.().triangleCount ?? 0)).toBe(4);
  await page.getByRole('tab', { name: '原始网格', exact: true }).click();
  await expect(page.locator('.image-mesh-canvas canvas')).toBeVisible();
  await page.getByRole('button', { name: '放大网格', exact: true }).click();
  const image = PNG.sync.read(await page.locator('.image-mesh-canvas canvas').screenshot());
  expect(new Set(Array.from({ length: Math.floor(image.data.length / 400) }, (_, i) => image.data.readUInt32BE(i * 400))).size).toBeGreaterThan(12);
  await page.getByRole('tab', { name: '积木模型', exact: true }).click();
  const brickCount = await page.evaluate(() => window.__imageBricks!().bricks);
  await page.getByLabel('导入 GLB 网格').setInputFiles({ name: 'bad.glb', mimeType: 'model/gltf-binary', buffer: Buffer.from('not glb') });
  await expect(page.getByRole('alert')).toContainText('GLB 导入失败');
  expect(await page.evaluate(() => window.__imageBricks!().bricks)).toBe(brickCount);
});

test('lobby loads a compact catalog and defers the offscreen 3D demo', async ({ page }) => {
  const manifests: string[] = [];
  page.on('request', request => { if (request.url().endsWith('/manifest.json')) manifests.push(request.url()); });
  await page.goto('/');
  await expect(page.locator('.model-card')).toHaveCount(15);
  await expect(page.locator('.model-card-specs dd').first()).not.toHaveText('—');
  expect(manifests).toEqual([]);
});

test('large model rotation remains responsive with bounded draw calls', async ({ page }, testInfo) => {
  await page.goto('/explore/10214');
  await page.getByText('模型已就绪', { exact: true }).waitFor();
  await page.getByRole('button', { name: '自动旋转', exact: true }).click();
  const before = await page.evaluate(() => ({ frames: window.__atlas!().renderedFrames, time: performance.now() }));
  await page.waitForTimeout(1800);
  const metrics = await page.evaluate(before => ({
    fps: (window.__atlas!().renderedFrames - before.frames) / (performance.now() - before.time) * 1000,
    drawCalls: window.__atlas!().drawCalls, instances: window.__atlas!().loadedInstances,
  }), before);
  expect(metrics.instances).toBe(4281);
  expect(metrics.drawCalls).toBeLessThan(650);
  expect(metrics.fps).toBeGreaterThan(30);
  await testInfo.attach('tower-bridge-performance', { body: JSON.stringify(metrics, null, 2), contentType: 'application/json' });
});

test('assembly reset requires confirmation and inconsistent completion cannot skip the game', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('brick-atlas-assembly-game-v1', JSON.stringify({
    '31028-sailboat': { completedStep: 0, placedIds: [], completed: true, updatedAt: Date.now() },
  })));
  await page.goto('/assemble/31028-sailboat');
  await expect.poll(() => page.evaluate(() => window.__assemblyGame?.().ready)).toBe(true);
  expect(await page.evaluate(() => window.__assemblyGame?.().completed)).toBe(false);
  await page.getByRole('button', { name: '重新开始', exact: true }).click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await page.getByRole('button', { name: '关闭弹窗' }).click();
  expect(await page.evaluate(() => window.__assemblyGame?.().activeStep)).toBe(1);
  await page.getByRole('button', { name: '暂停指导动画' }).click();
  await expect(page.getByRole('button', { name: '播放指导动画' })).toBeVisible();
});

test('all spaces fit mobile and tablet screens with nonblank canvases', async ({ page }, testInfo) => {
  test.setTimeout(120000);
  const errors: string[] = [];
  page.on('pageerror', error => errors.push(error.message));
  for (const width of [390, 820]) {
    await page.setViewportSize({ width, height: 900 });
    for (const route of ['/', '/assemble', '/explore/31028', '/build/31027', '/diy', '/compose', '/create', '/assemble/31028-sailboat']) {
      await page.goto(route);
      if (route.startsWith('/explore') || route.startsWith('/build')) await page.getByText('模型已就绪', { exact: true }).waitFor();
      if (route.startsWith('/build')) await page.getByRole('button', { name: '下一步', exact: true }).click();
      if (route.startsWith('/assemble/')) await expect.poll(() => page.evaluate(() => window.__assemblyGame?.().ready)).toBe(true);
      await page.waitForTimeout(500);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `${width} ${route}`).toBe(true);
      const path = testInfo.outputPath(`${width}-${route.replaceAll('/', '_')}.png`);
      await page.screenshot({ path });
      await testInfo.attach(`${width} ${route}`, { path, contentType: 'image/png' });
      const canvas = page.locator('.canvas-host canvas, .diy-canvas canvas, .compose-canvas canvas, .assembly-game-canvas canvas').first();
      if (await canvas.count()) {
        const box = await canvas.boundingBox();
        expect(box?.width).toBeGreaterThan(200);
        const image = PNG.sync.read(await canvas.screenshot());
        const colors = new Set<number>();
        for (let i = 0; i < image.data.length; i += 400) colors.add(image.data.readUInt32BE(i));
        expect(colors.size, `${width} ${route} canvas`).toBeGreaterThan(12);
      }
    }
  }
  expect(errors).toEqual([]);
});
