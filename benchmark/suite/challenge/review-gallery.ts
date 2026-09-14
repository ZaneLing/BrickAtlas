import assert from 'node:assert/strict';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { gunzipSync } from 'node:zlib';
import { chromium } from '@playwright/test';
import { curatedCases } from '../curated/cases';
import { challengeTasks } from './tasks';
import { evaluateChallenge } from './evaluate';
import { evaluateStrict } from '../study/strict-evaluate';
import { dims } from '../geometry';
import { digest } from '../data';
import type { Part } from '../shared';
import type { CaseTask } from '../v2/cases';

const root = resolve(import.meta.dirname, '../..'), out = resolve(root, 'review-gallery');
mkdirSync(out, { recursive: true });
const json = (path: string, value: unknown) => writeFileSync(resolve(out, path), JSON.stringify(value, null, 2) + '\n');
const config = JSON.parse(readFileSync(resolve(root, '.runtime/suite-server.json'), 'utf8'));
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const page = await browser.newPage();
await page.goto(config.url + '/paper-render.html');
await page.waitForFunction(() => typeof window.atlasPaperRender === 'function');
const render = async (path: string, parts: Part[], frameParts = parts) => {
  const encoded = await page.evaluate(({ parts, frameParts }) => {
    window.atlasPaperRender({ parts, frameParts });
    const canvas = document.createElement('canvas');
    canvas.width = 400; canvas.height = 300;
    canvas.getContext('2d')!.drawImage(document.querySelector<HTMLCanvasElement>('#paper-scene')!, 0, 0, 400, 300);
    return canvas.toDataURL('image/jpeg', .85).split(',')[1];
  }, { parts, frameParts });
  writeFileSync(resolve(out, path), Buffer.from(encoded, 'base64'));
};
const html = (title: string, body: string) => `<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><style>
body{font:15px/1.6 system-ui;margin:24px;color:#192126}a{color:#076452}h1{font-size:26px}h2{font-size:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:16px}
article{border-bottom:1px solid #cdd4d5;padding:12px 0;min-width:0}img{width:100%;height:auto;aspect-ratio:4/3;object-fit:contain}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}code{overflow-wrap:anywhere}nav{display:flex;gap:16px;flex-wrap:wrap}
</style><h1>${title}</h1>${body}</html>`;
const esc = (v: unknown) => String(v).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
const rows: any[] = [];
const fixtures: any[] = [];
try {
  for (const model of curatedCases()) for (const kind of ['plan', 'repair'] as const) {
    const top = [...model.structure.parts].sort((a, b) => b.y + dims(b).h - a.y - dims(a).h)[0];
    const source = structuredClone(model.structure);
    source.parts.find(p => p.id === top.id)!.color = top.color === 'blue' ? 'red' : 'blue';
    const spec = { id: digest({ gallery: 1, source: model.id, kind }).slice(0, 24), modelId: model.id,
      group: model.id, kind, variant: kind === 'plan' ? 'assemble' : 'color', condition: 'symbolic' as const,
      split: 'validation' as const, policy: model.style, difficulty: model.difficulty };
    const good = kind === 'plan' ? { order: model.assemblyOrder } : { structure: model.structure, faultIds: [top.id] };
    const bad = kind === 'plan' ? { order: [...model.assemblyOrder].reverse() } : { structure: source, faultIds: [] };
    const task: CaseTask = { spec, target: model.structure, source: kind === 'plan' ? null : source,
      changedIds: kind === 'plan' ? [] : [top.id], oracle: good, frames: [],
      public: { id: spec.id, kind, split: 'validation', family: model.style,
        prompt: kind === 'plan' ? '按给定目标提交合法装配顺序；不重排。' : '对照完整符号参考修复颜色，报告错误当前 ID。',
        input: kind === 'plan' ? { target: model.structure, direction: 'assemble' } : { current: source, reference: model.structure },
        responseSchema: {}, imageTitles: [] } };
    const positive = evaluateStrict(task, good), negative = evaluateStrict(task, bad);
    assert.equal(positive.metrics.success, 1); assert.equal(negative.metrics.success, 0);
    fixtures.push({ modelId: model.id, name: model.name, kind, id: spec.id,
      prompt: task.public.prompt, public: task.public, good, bad, positive, negative,
      target: task.target, source: task.source, badParts: kind === 'plan' ? [] : source.parts });
  }
  for (const task of challengeTasks()) {
    const bad: any = structuredClone(task.oracle);
    let badParts: Part[] = task.target.parts;
    let goodParts: Part[] = task.target.parts;
    if (task.kind === 'recovery-plan') {
      bad.actions = bad.actions.slice(3); badParts = task.source!.parts;
    } else if (task.kind === 'support-counterfactual') {
      bad.unsupportedIds = [];
      const forced = task.input.forcedRemoveIds as string[];
      badParts = task.target.parts.filter(p => !forced.includes(p.id));
      goodParts = badParts.filter(p => !(task.oracle as { unsupportedIds: string[] }).unsupportedIds.includes(p.id));
    } else if (task.kind === 'active-inspection') {
      bad.queryId = 'unknown'; goodParts = task.target.parts.filter(p => p.y === 13);
    }
    else if (task.kind === 'graph-reasoning') bad.shortestPath++;
    else if (task.kind === 'step-selection') bad.legalIds = [];
    else if (task.kind === 'pose-estimation') {
      bad.x++;
      const id = (task.input.selected as { id: string }).id;
      badParts = task.target.parts.map(p => p.id === id ? { ...p, x: p.x + 1 } : p);
    } else if (task.kind === 'multi-fault-repair') {
      bad.structure = task.source; bad.faultIds = []; badParts = task.source!.parts;
    } else {
      const s = bad.structure ?? bad;
      const top = [...s.parts].sort((a: Part, b: Part) => b.y - a.y)[0];
      s.parts = s.parts.filter((p: Part) => p.id !== top.id); badParts = s.parts;
    }
    const positive = evaluateChallenge(task, task.oracle), negative = evaluateChallenge(task, bad);
    assert.equal(positive.success, 1); assert.equal(negative.success, 0, task.kind);
    fixtures.push({ modelId: task.model.id, name: task.model.name, kind: task.kind, id: task.id,
      prompt: task.prompt, public: { prompt: task.prompt, input: task.input, images: task.frames.map(f => f.title) },
      good: task.oracle, bad, positive, negative, target: task.target, source: task.source, badParts, goodParts });
  }
  for (const [i, item] of fixtures.entries()) {
    const stem = `case-${String(i + 1).padStart(2, '0')}`;
    await render(`${stem}-input.jpg`, item.source?.parts ?? item.target.parts, item.target.parts);
    await render(`${stem}-model.jpg`, item.target.parts);
    await render(`${stem}-good.jpg`, item.goodParts ?? item.target.parts, item.target.parts);
    await render(`${stem}-bad.jpg`, item.badParts, item.target.parts);
    const { target, source, badParts, ...publicRecord } = item;
    json(`${stem}.json`, { ...publicRecord, evidenceType: 'constructed evaluator control; NOT a model response' });
    rows.push({ ...item, stem });
  }
  const groups = [...new Set(rows.map(r => r.modelId))];
  for (const [index, modelId] of groups.entries()) {
    const selected = rows.filter(r => r.modelId === modelId);
    const body = `<nav><a href="index.html">全部模型</a><a href="procedural-001.html">5,120 个程序结构</a></nav>` +
      selected.map(item => `<section><h2>${esc(item.kind)} / ${item.id}</h2><p>${esc(item.prompt)}</p>
      <div class="grid"><article><h3>输入 / 上下文</h3><img src="${item.stem}-input.jpg"></article>
      <article><h3>正确参考</h3><img src="${item.stem}-good.jpg"></article>
      <article><h3>构造错误 / FAIL</h3><img src="${item.stem}-bad.jpg"></article></div>
      <p>字段题图像仅作上下文，请核对 JSON 字段。正反例为程序构造对照，不是模型实测。</p>
      <a href="${item.stem}.json">完整题面、正误答案与评分 JSON</a>
      <details><summary>正反评分</summary><pre>${esc(JSON.stringify({ positive: item.positive, negative: item.negative }, null, 2))}</pre></details></section>`).join('');
    writeFileSync(resolve(out, `model-${index + 1}.html`), html(selected[0].name, body));
  }
  writeFileSync(resolve(out, 'index.html'), html('BrickAtlas 全模型审核图集', `<p>18 个设计模型，36 个正反案例。旧版 5,120 个结构完整单列。</p>
    <nav><a href="procedural-001.html">打开 5,120 个程序结构全目录</a><a href="../REVIEW_REPORT.zh-CN.md">九维度审稿报告</a></nav><div class="grid">` +
    groups.map((id, i) => { const row = rows.find(r => r.modelId === id)!;
      return `<article><a href="model-${i + 1}.html"><img src="${row.stem}-model.jpg"><h2>${row.name}</h2></a><p>${row.target.parts.length} 件 · 2 个案例</p></article>`; }).join('') + '</div>'));
  json('cases.json', rows.map(({ target, source, badParts, ...row }) => row));
  console.log(JSON.stringify({ authoredModels: groups.length, controls: rows.length }));

  // The complete frozen population, not a best-looking subset. Two real case IDs per source.
  const records = gunzipSync(readFileSync(resolve(root, 'suite/artifacts/casebank-v2/structures.jsonl.gz')))
    .toString().trim().split('\n').map(line => JSON.parse(line));
  const index = gunzipSync(readFileSync(resolve(root, 'suite/artifacts/casebank-v2/case-index.jsonl.gz')))
    .toString().trim().split('\n').map(line => JSON.parse(line));
  const byModel = new Map<string, any[]>();
  for (const spec of index.filter(s => ['plan', 'reconstruct'].includes(s.kind)
    && (s.variant === 'assemble' || s.condition === 'ordinary'))) {
    byModel.set(spec.modelId, [...(byModel.get(spec.modelId) ?? []), spec]);
  }
  for (const [i, model] of records.entries()) {
    const path = `source-${String(i + 1).padStart(4, '0')}.jpg`;
    if (!readable(path)) await render(path, model.structure.parts);
    if ((i + 1) % 128 === 0) console.log(JSON.stringify({ rendered: i + 1, total: records.length }));
  }
  for (let p = 0; p < records.length / 64; p++) {
    const prev = `procedural-${String(Math.max(1, p)).padStart(3, '0')}.html`;
    const next = `procedural-${String(Math.min(80, p + 2)).padStart(3, '0')}.html`;
    const items = records.slice(p * 64, (p + 1) * 64).map((m, i) => {
      const n = p * 64 + i + 1, cases = byModel.get(m.id)!;
      assert.equal(cases.length, 2);
      return `<article><img loading="lazy" src="source-${String(n).padStart(4, '0')}.jpg"><h2>#${n} ${m.policy}</h2>
      <p>${m.structure.parts.length} 件 · ${m.split}</p><code>${m.id}</code><details><summary>两个实际 case 与结构</summary>
      <p>重建：从四视图与 BOM 恢复；规划：从空场装配全部件。完整题面在冻结 inputs 分片，答案在 ground-truth 分片。</p>
      <pre>${esc(JSON.stringify({ cases: cases.map(s => ({ id: s.id, kind: s.kind, condition: s.condition })), structure: m.structure }, null, 2))}</pre></details></article>`;
    }).join('');
    writeFileSync(resolve(out, `procedural-${String(p + 1).padStart(3, '0')}.html`),
      html(`全部程序结构 · ${p + 1}/80`, `<nav><a href="index.html">18 个设计模型</a><a href="${prev}">上一页</a><a href="${next}">下一页</a></nav><div class="grid">${items}</div>`));
  }
  json('catalog.json', { sourceManifest: digest(readFileSync(resolve(root, 'suite/artifacts/casebank-v2/manifest.json'), 'utf8')),
    sources: records.length, pages: 80, casesPerSource: 2, selectedByOutcome: false,
    models: records.map((m, i) => ({ id: m.id, image: `source-${String(i + 1).padStart(4, '0')}.jpg`, caseIds: byModel.get(m.id)!.map(s => s.id) })) });
  console.log(JSON.stringify({ complete: true, sources: records.length, casesLinked: 10240 }));
} finally { await browser.close(); }

function readable(path: string) {
  try { return readFileSync(resolve(out, path)).length > 100; } catch { return false; }
}
