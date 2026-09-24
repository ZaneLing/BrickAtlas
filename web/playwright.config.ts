import { defineConfig, devices } from '@playwright/test';
import { resolve } from 'node:path';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 45000,
  expect: { timeout: 12000 },
  fullyParallel: false,
  workers: 1,
  outputDir: resolve(import.meta.dirname, '../tem/verification/playwright-results'),
  reporter: [
    ['list'],
    ['html', { open: 'never', outputFolder: resolve(import.meta.dirname, '../tem/verification/playwright-report') }],
    ['json', { outputFile: resolve(import.meta.dirname, '../tem/verification/e2e-report.json') }],
  ],
  use: { baseURL: 'http://127.0.0.1:5173', screenshot: 'only-on-failure', trace: 'retain-on-failure' },
  projects: [
    { name: 'desktop-chrome', use: { ...devices['Desktop Chrome'], channel: process.env.CI ? undefined : 'chrome', viewport: { width: 1440, height: 1000 } } },
    { name: 'desktop-firefox', use: { ...devices['Desktop Firefox'], viewport: { width: 1440, height: 900 } } },
    { name: 'desktop-webkit', use: { ...devices['Desktop Safari'], viewport: { width: 1440, height: 900 } } },
  ],
  webServer: { command: 'npm run dev -- --port 5173 --strictPort', cwd: resolve(import.meta.dirname, '..'),
    url: 'http://127.0.0.1:5173', reuseExistingServer: !process.env.CI },
});
