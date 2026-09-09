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
  const samples: { firstVisibleMs: number; readyMs: number; drawCalls: number; triangles: number; frameMs: number; animationFps: number; heapBytes: number | null }[] = [];
  for (let i = 0; i < 7; i++) {
    const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await context.newPage();
    await page.goto(url);
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
    samples.push({ ...metrics, animationFps: (end.frames - start.frames) / (end.at - start.at) * 1000, heapBytes: end.memory ?? null });
    await context.close();
  }
  const percentile = (values: number[], p: number) => [...values].sort((a, b) => a - b)[Math.min(values.length - 1, Math.ceil(values.length * p) - 1)];
  const summaries = Object.fromEntries(['firstVisibleMs', 'readyMs', 'animationFps', 'frameMs'].map(key => {
    const values = samples.map(s => s[key as keyof typeof s] as number);
    return [key, { p50: percentile(values, 0.5), p95: percentile(values, 0.95) }];
  }));
  const report = {
    measuredAt: new Date().toISOString(), build: 'production', browser: await browser.version(),
    environment: 'Headless Chrome, local macOS arm64, 1440x900, fresh browser contexts, localhost; not a physical-phone/network benchmark.',
    timingDefinition: 'Scene initialization to first attached geometry / all geometry decoded. Includes no DNS or production CDN delay.',
    samples, summaries,
  };
  await writeFile('assets-built/performance-report.json', JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(summaries, null, 2));
} finally {
  await browser.close();
  preview.kill();
}
