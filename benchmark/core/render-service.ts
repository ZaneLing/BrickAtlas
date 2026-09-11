import { chromium, type Browser, type Page } from '@playwright/test';
import { createHash } from 'node:crypto';
import type { Brick, View } from '../shared/types';

export interface Frame { hash: string; buffer: Buffer }
export class RenderService {
  private browser?: Browser;
  private page?: Page;
  private queue: Promise<unknown> = Promise.resolve();

  constructor(readonly url: string) {}

  render(parts: Brick[], view: View, visible: string[]): Promise<Frame> {
    const next = this.queue.then(async () => {
      if (!this.page) {
        this.browser = await chromium.launch({
          headless: true, channel: process.env.CI ? undefined : 'chrome',
        });
        this.page = await this.browser.newPage({ viewport: { width: 640, height: 480 } });
        await this.page.goto(`${this.url}/render.html`);
        await this.page.waitForFunction(() => typeof window.careRender === 'function');
      }
      const dataUrl = await this.page.evaluate(
        ({ parts, view, visible }) => window.careRender(parts, view, visible), { parts, view, visible },
      );
      const buffer = Buffer.from(dataUrl.split(',')[1], 'base64');
      return { hash: createHash('sha256').update(buffer).digest('hex'), buffer };
    });
    this.queue = next.catch(() => {});
    return next;
  }

  async close() {
    await this.queue;
    await this.browser?.close();
    this.page = undefined;
    this.browser = undefined;
  }
}
