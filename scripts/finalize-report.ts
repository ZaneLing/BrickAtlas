import { readFile, writeFile, mkdir, copyFile, readdir } from 'node:fs/promises';

const report = JSON.parse(await readFile('assets-built/e2e-report.json', 'utf8'));
if (report.stats.unexpected || report.stats.flaky) throw new Error('Browser validation has failures or flaky tests');
const directories = await readdir('test-results', { withFileTypes: true });
const artifacts: string[] = [];
await mkdir('docs/screenshots', { recursive: true });
for (const directory of directories) {
  if (!directory.isDirectory()) continue;
  const files = await readdir(`test-results/${directory.name}`);
  for (const file of files) {
    if (!/^(assembled|inventory-100|structure-45)\.png$/.test(file)) continue;
    if (!directory.name.endsWith('desktop-chrome')) continue;
    const target = `docs/screenshots/desktop-${file}`;
    await copyFile(`test-results/${directory.name}/${file}`, target);
    artifacts.push(target);
  }
}
const summary = {
  measuredAt: report.stats.startTime,
  passed: report.stats.expected, skipped: report.stats.skipped,
  failed: report.stats.unexpected, flaky: report.stats.flaky,
  projects: report.config.projects.map((p: { name: string }) => p.name),
  screenshots: artifacts.sort(),
  skippedReason: 'Platform-specific audits: axe and throttled-network checks on Chromium; context-loss checks where the extension is available.',
};
await writeFile('assets-built/verification-summary.json', JSON.stringify(summary, null, 2) + '\n');
console.log(summary);
