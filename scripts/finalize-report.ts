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
    if (!/^(assembled|inventory-100|structure-45|landscape|narrow-mobile)\.png$/.test(file)) continue;
    const device = directory.name.endsWith('mobile-chrome') ? 'mobile' : directory.name.endsWith('desktop-chrome') ? 'desktop' : null;
    if (!device) continue;
    const target = `docs/screenshots/${device}-${file}`;
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
  skippedReason: 'Platform-specific audits: CDP/axe on Chromium, exhaustive inventory picking on desktop, 320px layout on mobile, one throttled-network run.',
};
await writeFile('assets-built/verification-summary.json', JSON.stringify(summary, null, 2) + '\n');
console.log(summary);
