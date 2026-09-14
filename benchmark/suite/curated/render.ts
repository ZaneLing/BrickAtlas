import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, renameSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from '@playwright/test';
import { PNG } from 'pngjs';
import { digest } from '../data';
import type { PaperFrame } from '../web/paper-render';
import { curatedCases, CURATED_VERSION } from './cases';
import { curatedTasks } from './tasks';
import { insertIssue } from '../geometry';

export const CURATED_OUTPUT = resolve(dirname(fileURLToPath(import.meta.url)), '../../curated-cases');
const sourceRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const sha = (bytes: Buffer) => createHash('sha256').update(bytes).digest('hex');

export async function renderCuratedCases(url: string) {
  const temporary = `${CURATED_OUTPUT}.building`;
  assert.ok(!existsSync(temporary), 'Inspect or remove incomplete curated-cases.building');
  mkdirSync(temporary, { recursive: true });
  const browser = await chromium.launch({ headless: true, channel: process.env.CI ? undefined : 'chrome' });
  const page = await browser.newPage({ viewport: { width: 1000, height: 750 } });
  const files: Array<{ path: string; sha256: string; bytes: number; foreground?: number }> = [];
  const write = (relative: string, bytes: Buffer) => {
    const path = resolve(temporary, relative); mkdirSync(dirname(path), { recursive: true }); writeFileSync(path, bytes);
    files.push({ path: relative, sha256: sha(bytes), bytes: bytes.length });
  };
  const json = (relative: string, value: unknown) => write(relative, Buffer.from(JSON.stringify(value, null, 2) + '\n'));
  try {
    await page.goto(url + '/paper-render.html');
    await page.waitForFunction(() => typeof window.atlasPaperRender === 'function');
    const render = async (relative: string, frame: PaperFrame) => {
      const result = await page.evaluate(frame => window.atlasPaperRender(frame), frame);
      const bytes = Buffer.from(result.png.split(',')[1], 'base64'), png = PNG.sync.read(bytes);
      let foreground = 0, edge = 0;
      for (let i = 0; i < png.data.length; i += 4) {
        if (png.data[i] < 245 || png.data[i + 1] < 245 || png.data[i + 2] < 245) {
          foreground++;
          const x = (i / 4) % png.width, y = Math.floor(i / 4 / png.width);
          if (x < 3 || y < 3 || x >= png.width - 3 || y >= png.height - 3) edge++;
        }
      }
      assert.ok(foreground > 1000 && edge === 0, relative);
      write(relative, bytes); files.at(-1)!.foreground = foreground;
    };
    const models = curatedCases();
    for (const model of models) {
      const root = `models/${model.difficulty}/${model.id}`;
      json(`${root}/metadata.json`, { version: CURATED_VERSION, id: model.id, name: model.name,
        difficulty: model.difficulty, style: model.style, description: model.description,
        designIntent: model.designIntent, palette: model.palette, difficultyProfile: model.difficultyProfile,
        assemblyOrder: model.assemblyOrder, source: 'original explicit BrickAtlas design', license: 'CC0-1.0' });
      json(`${root}/structure.json`, model.structure);
      for (const view of ['iso', 'top', 'front', 'side'] as const) {
        await render(`${root}/views/${view}.png`, { parts: model.structure.parts, view });
      }
      for (const y of [...new Set(model.structure.parts.map(p => p.y))].sort((a, b) => a - b)) {
        await render(`${root}/layers/y-${String(y).padStart(2, '0')}.png`,
          { parts: model.structure.parts.filter(p => p.y === y), frameParts: model.structure.parts, view: 'iso' });
      }
      const checkpoints = [...new Set([1, .25, .5, .75, 1].map(f => Math.max(1, Math.ceil(model.assemblyOrder.length * f))))].sort((a, b) => a - b);
      let previous = 0;
      for (const count of checkpoints) {
        const ids = model.assemblyOrder.slice(0, count);
        await render(`${root}/steps/${String(count).padStart(2, '0')}-of-${model.assemblyOrder.length}.png`,
          { parts: ids.map(id => model.structure.parts.find(p => p.id === id)!),
            frameParts: model.structure.parts, highlightIds: ids.slice(previous) });
        previous = count;
      }
      await render(`${root}/exploded.png`, { parts: model.structure.parts, explode: 1.2 });
    }

    for (const item of curatedTasks()) {
      const { task, model, display } = item, root = `tasks/${task.spec.kind}`;
      const oracle = task.spec.kind === 'repair' ? { structure: task.target, faultIds: task.changedIds } : task.oracle;
      json(`${root}/task.json`, { version: CURATED_VERSION, caseId: task.spec.id, sourceId: model.id,
        difficulty: model.difficulty, style: model.style, kind: task.spec.kind, variant: task.spec.variant,
        condition: task.spec.condition, title: display.title, public: task.public,
        display: { inputLabel: display.inputLabel, groundTruthLabel: display.groundTruthLabel },
        groundTruth: oracle, scoring: 'benchmark/suite/v2/evaluate.ts via strict evaluator' });
      if (task.source) await render(`${root}/input/current.png`,
        { parts: task.source.parts, frameParts: task.target.parts, highlightIds: task.changedIds });
      if (task.spec.kind === 'parts') {
        await render(`${root}/input/isolated-iso.png`, { parts: task.target.parts });
        await render(`${root}/input/isolated-top.png`, { parts: task.target.parts, view: 'top' });
      } else if (task.spec.kind === 'relations') {
        await render(`${root}/input/symbolic-structure-illustration.png`,
          { parts: task.target.parts, highlightIds: display.highlightIds });
      } else if (task.frames.length) {
        for (const frame of task.frames) await render(`${root}/input/reference-${frame.view}.png`,
          { parts: frame.parts, view: frame.view });
      }
      await render(`${root}/ground-truth/iso.png`,
        { parts: task.target.parts, highlightIds: display.highlightIds });
      await render(`${root}/ground-truth/exploded.png`,
        { parts: task.target.parts, explode: 1.2, highlightIds: display.highlightIds });
      if (task.spec.kind === 'plan') {
        const order = (task.oracle as { order: string[] }).order;
        for (const count of [...new Set([1, .25, .5, .75, 1].map(f => Math.ceil(order.length * f)))].sort((a, b) => a - b)) {
          const ids = order.slice(0, count);
          await render(`${root}/ground-truth/steps/${String(count).padStart(2, '0')}-of-${order.length}.png`,
            { parts: ids.map(id => task.target.parts.find(p => p.id === id)!),
              frameParts: task.target.parts, highlightIds: ids.slice(Math.max(0, count - Math.ceil(order.length / 4))) });
        }
        const byRole = (prefix: string) => task.target.parts.filter(p => p.id.startsWith(prefix));
        const invalidIds = [...byRole('water-'), ...byRole('pier-').filter(p => ['pier-1', 'pier-2', 'pier-3',
          'pier-10', 'pier-11', 'pier-12'].includes(p.id)), ...byRole('deck-')].map(p => p.id);
        const invalidState = invalidIds.map(id => task.target.parts.find(p => p.id === id)!);
        const blocked = task.target.parts.find(p => p.id === 'pier-4')!;
        let prefix: typeof invalidState = [];
        for (const part of invalidState) {
          assert.equal(insertIssue(prefix, part), null, `Curated dead-end prefix/${part.id}`);
          prefix = [...prefix, part];
        }
        assert.equal(insertIssue(invalidState, blocked), 'blocked');
        await render(`${root}/ground-truth/dead-end.png`, { parts: invalidState, frameParts: task.target.parts,
          explode: .7, highlightIds: byRole('deck-').map(p => p.id) });
        await render(`${root}/ground-truth/dead-end-target.png`, { parts: task.target.parts,
          explode: .7, highlightIds: [blocked.id] });
        json(`${root}/ground-truth/dead-end.json`, { legalPrefix: invalidIds,
          attemptedId: blocked.id, rejection: 'blocked',
          explanation: 'The two decks are inserted while inner pier positions remain empty; a missing pier can no longer descend vertically.' });
      }
    }
    const manifest = { version: CURATED_VERSION, generatedAt: 'deterministic-from-source',
      sourceHashes: Object.fromEntries(['curated/cases.ts', 'curated/tasks.ts', 'curated/render.ts', 'web/paper-render.ts']
        .map(path => [path, digest(readFileSync(resolve(sourceRoot, path), 'utf8'))])),
      models: curatedCases().map(c => ({ id: c.id, name: c.name, difficulty: c.difficulty, style: c.style,
        parts: c.structure.parts.length, colors: Object.keys(c.palette).length,
        occupiedLevels: c.difficultyProfile.occupiedLevels, occlusion: c.difficultyProfile.occlusion,
        supportReasoning: c.difficultyProfile.supportReasoning })),
      tasks: curatedTasks().map(t => ({ id: t.task.spec.id, kind: t.task.spec.kind, sourceId: t.model.id,
        difficulty: t.model.difficulty })), files,
      guarantees: ['No random geometry or color sampling.', 'At most four semantic color roles per model.',
        'All structures pass nominal and independent geometry checks.', 'Every stored assembly order is executable.',
        'Every task ground truth passes the strict evaluator.', 'Images use fixed cameras within each source/task pair.'],
      limitations: ['Original rectangular-grid designs, not imported official LEGO sets.',
        'Semantic recognizability is a design assertion pending independent human review.',
        'Curated set is a qualitative and calibration layer, not a replacement for the 5,120-source v2 population.'] };
    json('manifest.json', manifest);
    write('README.md', Buffer.from(`# BrickAtlas Curated Cases\n\n` +
      `This folder contains 12 original, explicitly designed structures: four easy, four medium, and four hard. ` +
      `Every model has coherent role-based colors, four views, occupied-layer renders, an exploded view, legal assembly snapshots, metadata, and exact structure JSON.\n\n` +
      `The eight task folders contain the model-facing input contract, ground truth, and paired illustrations for recognition, relation, reconstruction, generation, completion, editing, planning, and repair.\n\n` +
      `Open \`index.html\`, \`CONTACT_SHEET.png\`, and \`TASK_GROUND_TRUTH.png\` for review. These examples are original CC0 BrickAtlas designs and are not copied from official sets. Semantic quality still needs independent human review.\n`));
    write('index.html', Buffer.from(`<!doctype html><meta charset="utf-8"><title>BrickAtlas Curated Cases</title>
<style>body{font:15px system-ui;margin:32px;color:#182428}h1,h2{letter-spacing:0}.grid{display:grid;grid-template-columns:repeat(4,minmax(220px,1fr));gap:18px}.card{border:1px solid #ccd5d7;padding:12px}.card img{width:100%;aspect-ratio:4/3;object-fit:contain}.meta{color:#526166}</style>
<h1>BrickAtlas Curated Cases</h1><p>12 original structures; coherent palettes; verified geometry and assembly orders.</p>
${(['easy', 'medium', 'hard'] as const).map(d => `<h2>${d.toUpperCase()}</h2><div class="grid">${models.filter(m => m.difficulty === d)
  .map(m => `<div class="card"><img src="models/${d}/${m.id}/views/iso.png"><b>${m.name}</b><div class="meta">${m.style} · ${m.structure.parts.length} parts · ${Object.keys(m.palette).length} colors</div><p>${m.description}</p></div>`).join('')}</div>`).join('')}
<h2>Task Ground Truth</h2><div class="grid">${curatedTasks().map(t => `<div class="card"><img src="tasks/${t.task.spec.kind}/ground-truth/iso.png"><b>${t.display.title}</b><div class="meta">${t.model.name} · ${t.model.difficulty}</div><p>${t.display.inputLabel} → ${t.display.groundTruthLabel}</p></div>`).join('')}</div>`));
  } finally {
    await browser.close();
  }
  if (existsSync(CURATED_OUTPUT)) rmSync(CURATED_OUTPUT, { recursive: true });
  renameSync(temporary, CURATED_OUTPUT);
  return JSON.parse(readFileSync(resolve(CURATED_OUTPUT, 'manifest.json'), 'utf8'));
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const config = JSON.parse(readFileSync(resolve(dirname(fileURLToPath(import.meta.url)), '../../.runtime/suite-server.json'), 'utf8'));
  const result = await renderCuratedCases(process.env.BRICKATLAS_URL ?? config.url);
  console.log(JSON.stringify({ models: result.models.length, tasks: result.tasks.length, files: result.files.length }));
}
