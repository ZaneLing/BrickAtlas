import { chromium } from '@playwright/test';
import { spawn } from 'node:child_process';
import { writeFile } from 'node:fs/promises';
import net from 'node:net';

const port = await new Promise<number>((resolve, reject) => {
  const server = net.createServer();
  server.once('error', reject);
  server.listen(0, '127.0.0.1', () => {
    const address = server.address() as net.AddressInfo;
    server.close(() => resolve(address.port));
  });
});
const preview = spawn(process.execPath, ['node_modules/vite/bin/vite.js', 'preview', '--host', '127.0.0.1', '--port', String(port), '--strictPort'], { stdio: 'ignore' });
const url = `http://127.0.0.1:${port}`;
const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));
const browser = await chromium.launch({ channel: process.env.CI ? undefined : 'chrome', headless: true });
try {
  let available = false;
  for (let i = 0; i < 20; i++) {
    try { if ((await fetch(url)).ok) { available = true; break; } } catch { /* server starting */ }
    await sleep(100);
  }
  if (!available) throw new Error(`Production preview unavailable on ${port}`);
  const plans = [
    { modelId: '5867', runs: 3 },
    { modelId: '10220', runs: 2 },
    { modelId: '10214', runs: 2 },
    { modelId: '10213', runs: 2 },
  ];
  const samples: {
    modelId: string; firstVisibleMs: number; readyMs: number; drawCalls: number; triangles: number;
    frameMs: number; animationFps: number; heapBytes: number | null; explosionMs: number;
    inventoryDrawCalls: number; inventoryFrameMs: number; inventoryInside: number; instances: number;
  }[] = [];
  for (const plan of plans) for (let i = 0; i < plan.runs; i++) {
    const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await context.newPage();
    await page.goto(`${url}/explore/${plan.modelId}`);
    await page.getByText('模型已就绪', { exact: true }).waitFor();
    await page.waitForTimeout(300);
    const metrics = await page.evaluate(() => {
      const m = window.__atlas!();
      return { firstVisibleMs: m.firstVisibleMs!, readyMs: m.readyMs!, drawCalls: m.drawCalls, triangles: m.triangles, frameMs: m.frameMs };
    });
    await page.getByRole('button', { name: '自动旋转', exact: true }).click();
    const start = await page.evaluate(() => ({ frames: window.__atlas!().renderedFrames, at: performance.now() }));
    await page.waitForTimeout(1500);
    const end = await page.evaluate(() => ({ frames: window.__atlas!().renderedFrames, at: performance.now(), memory: (performance as Performance & { memory?: { usedJSHeapSize: number } }).memory?.usedJSHeapSize }));
    await page.getByRole('button', { name: /^零件陈列/ }).click();
    const explosionStarted = performance.now();
    await page.waitForFunction(() => window.__atlas?.().actualExplosion === 1);
    await page.waitForFunction(() => window.__atlas?.().cameraMoving === false);
    const inventory = await page.evaluate(() => {
      const state = window.__atlas!();
      return {
        drawCalls: state.drawCalls,
        frameMs: state.frameMs,
        inside: state.framing.insideInstances,
        instances: state.visibleInstances,
      };
    });
    samples.push({
      modelId: plan.modelId,
      ...metrics,
      animationFps: (end.frames - start.frames) / (end.at - start.at) * 1000,
      heapBytes: end.memory ?? null,
      explosionMs: performance.now() - explosionStarted,
      inventoryDrawCalls: inventory.drawCalls,
      inventoryFrameMs: inventory.frameMs,
      inventoryInside: inventory.inside,
      instances: inventory.instances,
    });
    await context.close();
  }
  const percentile = (values: number[], p: number) => [...values].sort((a, b) => a - b)[Math.min(values.length - 1, Math.ceil(values.length * p) - 1)];
  const summaries = Object.fromEntries(plans.map(plan => {
    const modelSamples = samples.filter(sample => sample.modelId === plan.modelId);
    return [plan.modelId, Object.fromEntries(
      ['readyMs', 'animationFps', 'frameMs', 'explosionMs', 'inventoryFrameMs'].map(key => {
        const values = modelSamples.map(sample => sample[key as keyof typeof sample] as number);
        return [key, { p50: percentile(values, 0.5), p95: percentile(values, 0.95) }];
      }),
    )];
  }));
  const report = {
    measuredAt: new Date().toISOString(), build: 'production', browser: browser.version(),
    environment: 'Headless Chrome, local macOS arm64, 1440x900, fresh browser contexts, production build on localhost.',
    timingDefinition: 'Scene initialization to geometry ready, assembled auto-rotation FPS, and 0-to-100 inventory animation with camera settling.',
    samples, summaries,
  };
  await writeFile('assets-built/performance-report.json', JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(summaries, null, 2));
} finally {
  await browser.close();
  preview.kill();
}
