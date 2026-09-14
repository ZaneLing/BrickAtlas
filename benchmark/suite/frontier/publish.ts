import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from '@playwright/test';
import { PNG } from 'pngjs';
import { frontierModels } from './models';
import { frontierTasks, publicTask } from './tasks';
import { evaluateFrontier, renderNegative } from './evaluate';
import { publicSolver, shortcut } from './baselines';
import { FRONTIER_VERSION } from './geometry';
import type { PaperFrame } from '../web/paper-render';

const here = dirname(fileURLToPath(import.meta.url)), root = resolve(here, '../../frontier-cases');
const sha = (s: string | Buffer) => createHash('sha256').update(s).digest('hex');
const json = (path: string, value: unknown) => writeFileSync(resolve(root, path), JSON.stringify(value, null, 2) + '\n');
const escape = (s: string) => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
const css = `*{box-sizing:border-box}body{margin:0;color:#202827;background:#fff;font:15px/1.55 system-ui,sans-serif}main{max-width:1280px;margin:auto;padding:24px}a{color:#166b79}h1{font-size:28px}h2{font-size:23px;margin-top:36px}h3{font-size:18px}header{border-bottom:2px solid #16816c;padding-bottom:18px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}img{width:100%;height:auto;aspect-ratio:4/3;object-fit:contain}article{border-bottom:1px solid #ccd4d2;padding:16px 0}pre{overflow:auto;background:#f2f5f4;padding:12px;max-height:260px}table{border-collapse:collapse;width:100%}th,td{text-align:left;border-bottom:1px solid #ccd4d2;padding:8px;overflow-wrap:anywhere}p,li{overflow-wrap:anywhere}figure{margin:0}figcaption{font-size:13px}details{margin:10px 0}@media(max-width:700px){main{padding:16px}.grid{grid-template-columns:1fr}h1{font-size:24px}}`;
const html = (title: string, body: string) => `<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><style>${css}</style><main>${body}</main></html>`;
const labels: Record<string, string> = {
  'service-plan': '最小拆装修复', 'access-certificate': '最小访问集合与可执行证书',
  'parallel-schedule': '多工位依赖调度', 'minimal-intervention': '最小支撑干预',
  'inventory-cover': '库存受限等体积替代', 'ambiguity-set': '隐藏接缝的可行解集合',
  'inspection-policy': '预算内条件查询策略', 'distributed-repair': '跨区域混合故障修复',
};

mkdirSync(root, { recursive: true });
const browser = await chromium.launch({ headless: true, channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 1000, height: 750 } });
const config = JSON.parse(readFileSync(resolve(here, '../../.runtime/suite-server.json'), 'utf8'));
const files: Record<string, string> = {}, rows: any[] = [], baselineRows: any[] = [], modelLinks: string[] = [];
const render = async (path: string, frame: PaperFrame) => {
  const result = await page.evaluate(frame => window.atlasPaperRender(frame), frame);
  const bytes = Buffer.from(result.png.split(',')[1], 'base64'), image = PNG.sync.read(bytes);
  let foreground = 0, edge = 0;
  for (let i = 0; i < image.data.length; i += 4) if (image.data[i] < 235 || image.data[i + 1] < 235 || image.data[i + 2] < 235) {
    foreground++;
    const x = i / 4 % image.width, y = Math.floor(i / 4 / image.width);
    if (x < 2 || y < 2 || x >= image.width - 2 || y >= image.height - 2) edge++;
  }
  assert.ok(foreground > 1000 && edge === 0, path);
  writeFileSync(resolve(root, path), bytes); files[path] = sha(bytes);
};
try {
  await page.goto(config.url + '/paper-render.html');
  await page.waitForFunction(() => typeof window.atlasPaperRender === 'function');
  for (const m of frontierModels()) {
    json(`${m.id}.json`, m);
    for (const view of ['iso', 'top', 'front', 'side'] as const) await render(`${m.id}-${view}.png`, { parts: m.structure.parts, view });
    await render(`${m.id}-exploded.png`, { parts: m.structure.parts, explode: .8 });
    for (const y of [...new Set(m.structure.parts.map(p => p.y))].sort((a, b) => a - b))
      await render(`${m.id}-layer-${y}.png`, { parts: m.structure.parts.filter(p => p.y === y), frameParts: m.structure.parts, view: 'top' });
    let body = `<header><a href="index.html">全部模型</a><h1>${m.name}</h1><p>${m.description}</p><p>${m.stats.parts} 件 · ${m.stats.layers} 层 · 依赖深度 ${m.stats.depth} · X/Y/Z ${Object.values(m.stats.extent).join('/')}</p><a href="${m.id}.json">结构与模块 JSON</a></header><div class="grid">` +
      ['iso', 'top', 'front', 'side', 'exploded'].map(view => `<figure><img src="${m.id}-${view}.png" alt="${view}"><figcaption>${view}</figcaption></figure>`).join('') + '</div>';
    for (const t of frontierTasks().filter(t => t.modelId === m.id)) {
      const good = evaluateFrontier(t, t.oracle), bad = evaluateFrontier(t, t.negative);
      assert.equal(good.success, 1, t.id); assert.equal(bad.success, 0, t.id);
      const pub = publicTask(t);
      const start = performance.now(), solved = publicSolver(pub), elapsed = performance.now() - start;
      const solverResult = evaluateFrontier(t, solved), simpleResult = evaluateFrontier(t, shortcut(pub));
      assert.equal(solverResult.success, 1, t.id);
      baselineRows.push({ id: t.id, kind: t.kind, source: m.id, solver: solverResult,
        shortcut: simpleResult, solverLatencyMs: elapsed, publicInputHash: sha(JSON.stringify(pub)), modelInference: false });
      const stem = `${m.id}-${t.kind}`;
      const targetParts = good.finalParts ?? m.structure.parts;
      const negativeParts = bad.finalParts ?? renderNegative(t);
      const frameParts = [...m.structure.parts, ...targetParts, ...negativeParts];
      await render(`${stem}-good.png`, { parts: targetParts, frameParts, highlightIds: t.highlight });
      await render(`${stem}-bad.png`, { parts: negativeParts.length ? negativeParts : m.structure.parts,
        frameParts, highlightIds: t.highlight });
      json(`${stem}-public.json`, pub);
      json(`${stem}-review.json`, { ...t, positiveResult: good, negativeResult: bad });
      const row = { modelId: m.id, kind: t.kind, label: labels[t.kind], stem,
        good: { ...good, finalParts: undefined }, bad: { ...bad, finalParts: undefined }, positive: t.oracle, negative: t.negative };
      rows.push(row);
      body += `<article><h2>${labels[t.kind]}</h2><p>${escape(t.prompt.split('\n').at(-1)!)}</p><div class="grid">` +
        `<figure><img loading="lazy" src="${m.id}-iso.png"><figcaption>完整结构上下文，非额外允许输入</figcaption></figure>` +
        `<figure><img loading="lazy" src="${stem}-good.png"><figcaption>正确参考 · success=1</figcaption></figure>` +
        `<figure><img loading="lazy" src="${stem}-bad.png"><figcaption>构造错误 · success=0 · ${escape(bad.issues.join(', '))}</figcaption></figure></div>` +
        `<p><a href="${stem}-public.json">公开题面</a> · <a href="${stem}-review.json">裁判与正反答案</a></p>` +
        `<details><summary>指标、正例和反例 JSON</summary><pre>${escape(JSON.stringify({ metrics: good.metrics, positive: t.oracle, negative: t.negative }, null, 2))}</pre></details></article>`;
    }
    writeFileSync(resolve(root, `${m.id}.html`), html(m.name, body));
    modelLinks.push(`<article><a href="${m.id}.html"><img src="${m.id}-iso.png" alt="${m.name}"><h2>${m.name}</h2></a><p>${m.stats.parts} 件 · 8 类任务 · ${m.domain}</p></article>`);
    console.log(JSON.stringify({ rendered: m.id, parts: m.stats.parts }));
  }
} finally { await browser.close(); }
json('cases.json', rows); json('baselines.json', baselineRows);
const consistent = frontierModels().map(m => {
  const ts = frontierTasks().filter(t => t.modelId === m.id);
  const service = publicSolver(publicTask(ts.find(t => t.kind === 'service-plan')!)) as any;
  const certificate = publicSolver(publicTask(ts.find(t => t.kind === 'access-certificate')!)) as any;
  const removed = service.actions.filter((a: any) => a.op === 'remove').map((a: any) => a.id).sort();
  assert.deepEqual(removed, [...certificate.removeIds].sort());
  return { modelId: m.id, serviceAccessConsistent: true };
});
json('consistency.json', consistent);
json('protocol.json', { version: FRONTIER_VERSION, status: 'public-development', objects: 6, cases: 48,
  modelResults: null, humanCalibration: null, robotControl: false,
  tracks: { symbolic: ['service-plan', 'access-certificate', 'parallel-schedule', 'minimal-intervention', 'inventory-cover', 'distributed-repair'],
    finiteObservation: ['ambiguity-set', 'inspection-policy'] },
  rules: ['Only *-public.json is model input. Review JSON, context and exploded images are not extra model evidence.',
    'All eight tasks share six source groups; do not bootstrap the 48 cases as independent sources.',
    'Raw model answers and tool-assisted answers require separate tracks and matched budgets.',
    'No image-only measurements are claimed. Rich views and layers are audit artifacts.',
    'Record truncation, tokens, API cost, inference and tool latency separately; remote memory unknown stays null.',
    'Oracle success is not model performance; public solver is a transparent algorithmic ceiling, not a learned model.'] });
writeFileSync(resolve(root, 'index.html'), html('BrickAtlas Frontier', `<header><h1>BrickAtlas Frontier</h1><p>6 个大结构 · 48 道任务 · 158–408 件</p><p><a href="../FRONTIER_REPORT.zh-CN.md">调研与升级报告</a> · <a href="REPORT.zh-CN.md">逐模型案例报告</a> · <a href="protocol.json">版本协议</a></p></header><div class="grid">${modelLinks.join('')}</div>`));
for (const name of readdirSync(root).filter(n => !n.startsWith('manifest') && /\.(json|html|png)$/.test(n))) files[name] = sha(readFileSync(resolve(root, name)));
json('manifest.json', { version: FRONTIER_VERSION, models: frontierModels().map(({ structure, modules, ...m }) => m),
  cases: rows.length, modelInferences: 0, positivesPassed: 48, negativesRejected: 48, publicSolverPassed: 48,
  placedParts: frontierModels().reduce((n, m) => n + m.stats.parts, 0), files,
  sourceHashes: Object.fromEntries(readdirSync(here).filter(n => n.endsWith('.ts')).map(n => [n, sha(readFileSync(resolve(here, n)))])) });
console.log(JSON.stringify({ models: 6, cases: rows.length, renderedImages: Object.keys(files).filter(n => n.endsWith('.png')).length }));
