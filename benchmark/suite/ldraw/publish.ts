/** Synchronize current entry points; preserve historical source data and reviews. */
import { readFileSync, writeFileSync, mkdirSync, copyFileSync, readdirSync, renameSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
const root = resolve(import.meta.dirname, '../../..'), data = resolve(root, 'benchmark/ldraw-v1');
const site = resolve(root, 'public/benchmark'), paper = resolve(root, 'benchmark/paper');
const read = (p: string) => JSON.parse(readFileSync(p, 'utf8'));
const release = read(resolve(data, 'release.json'));
const catalog = read(resolve(data, 'catalog.json'));
const lockPath = resolve(root, 'assets-source/library-lock.json');
const lock = { ...read(lockPath), ...read(resolve(data, 'dependency-lock.json')) };
writeFileSync(lockPath, JSON.stringify(Object.fromEntries(Object.entries(lock).sort()), null, 2) + '\n');
mkdirSync(resolve(site, 'docs'), { recursive: true });
for (const file of ['main.pdf', 'supplement.pdf', 'main.zh-CN.md']) copyFileSync(resolve(paper, file), resolve(site, 'docs', file));
for (const file of ['ERRATA.zh-CN.md', 'ATTRIBUTION.md']) copyFileSync(resolve(data, file), resolve(site, 'docs', file));
copyFileSync(resolve(data, 'ERRATA.zh-CN.md'), resolve(site, 'docs/REPORT.zh-CN.md'));
copyFileSync(resolve(data, 'catalog.json'), resolve(site, 'catalog.json'));
writeFileSync(resolve(site, 'audit.json'), JSON.stringify({
  version: release.version, status: release.status, models: release.models, tasks: release.tasks,
  sourceGeometryModified: false, report: 'ldraw/release.json',
}, null, 2) + '\n');
const questionBank = ['# LDraw-1 当前题目审核库', '', '原始模型不变。答案只用于审核，不能作为模型输入。', ''];
for (const m of catalog) {
  const bundle = read(resolve(site, 'ldraw/models', `${m.id}.json`));
  questionBank.push(`## ${m.setNumber} ${m.nameZh}`, '');
  for (const t of bundle.tasks) {
    questionBank.push(`### ${t.id}`, '', t.question, '', `编号：${t.references.map((p: any) => p.label).join(', ') || '无特定零件'}`,
      '', '```json', JSON.stringify({ input: t.input, options: t.options, answer: t.answer }, null, 2), '```', '');
  }
}
writeFileSync(resolve(site, 'docs/QUESTION_BANK.zh-CN.md'), questionBank.join('\n'));
writeFileSync(resolve(data, 'QUESTION_BANK.zh-CN.md'), questionBank.join('\n'));
// Retired copies leave the active static-site tree. The authoritative
// historical datasets remain versioned under benchmark/hierarchy-*.
const retired = resolve(root, 'benchmark/.runtime/retired-site');
mkdirSync(retired, { recursive: true });
for (const name of ['models', 'images', 'figures']) {
  const old = resolve(site, name), destination = resolve(retired, `benchmark-${name}`);
  if (existsSync(old) && !existsSync(destination)) renameSync(old, destination);
}
const retained = new Set(catalog.map((m: any) => m.id));
for (const name of readdirSync(resolve(root, 'public/models'))) {
  if (!name.startsWith('omr-') || retained.has(name)) continue;
  const destination = resolve(retired, name);
  if (!existsSync(destination)) renameSync(resolve(root, 'public/models', name), destination);
}
console.log(`Published ${release.models} original sources and ${release.tasks} tasks; retired synthetic static assets.`);
