import { chromium, type Browser, type Page } from '@playwright/test';
import type { FrameSpec } from './shared';
import { digest } from './data';

export class SuiteRenderer {
  browser?: Browser;
  page?: Page;
  queue: Promise<unknown> = Promise.resolve();
  constructor(readonly url: string) {}
  render(frame: FrameSpec): Promise<{ hash: string; buffer: Buffer }> {
    const result = this.queue.then(async () => {
      if (!this.page) {
        this.browser = await chromium.launch({ headless: true, channel: process.env.CI ? undefined : 'chrome' });
        this.page = await this.browser.newPage({ viewport: { width: 640, height: 480 } });
        await this.page.goto(this.url + '/render.html');
        await this.page.waitForFunction(() => typeof window.atlasRender === 'function');
      }
      const data = await this.page.evaluate(frame => window.atlasRender(frame), frame);
      const buffer = Buffer.from(data.split(',')[1], 'base64');
      return { hash: digest(buffer.toString('base64')), buffer };
    });
    this.queue = result.catch(() => {});
    return result;
  }
  async close() { await this.queue; await this.browser?.close(); }
}
