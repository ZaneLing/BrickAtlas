import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, renameSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from '@playwright/test';
import { PNG } from 'pngjs';
import { digest } from '../data';
import { insertIssue, removeIssue } from '../geometry';
import type { PaperFrame } from '../web/paper-render';
import { CHALLENGE_VERSION, challengeModels } from './models';
import { challengeTasks } from './tasks';
import { publicChallenge, challengeProtocol } from './protocol';

export const CHALLENGE_OUTPUT = resolve(dirname(fileURLToPath(import.meta.url)), '../../challenge-cases-v2');
const sourceRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const sha = (bytes: Buffer) => createHash('sha256').update(bytes).digest('hex');

function highlights(task: ReturnType<typeof challengeTasks>[number]) {
  if (task.kind === 'support-counterfactual') return task.input.forcedRemoveIds as string[];
  if (task.kind === 'graph-reasoning') return [task.input.startId, task.input.goalId] as string[];
  if (task.kind === 'pose-estimation') return [(task.input.selected as { id: string }).id];
  if (task.kind === 'step-selection') return (task.input.candidates as Array<{ id: string }>).map(c => c.id);
  return task.changedIds;
}

export async function renderChallengeCases(url: string) {
  const temporary = `${CHALLENGE_OUTPUT}.building`;
  assert.ok(!existsSync(temporary), 'Inspect or remove incomplete challenge-cases.building');
  mkdirSync(temporary, { recursive: true });
  const browser = await chromium.launch({ headless: true, channel: process.env.CI ? undefined : 'chrome' });
  const page = await browser.newPage({ viewport: { width: 1000, height: 750 } });
  const files: Array<{ path: string; sha256: string; bytes: number; foreground?: number }> = [];
  const write = (relative: string, bytes: Buffer) => {
    const path = resolve(temporary, relative);
    mkdirSync(dirname(path), { recursive: true });
    writeFileSync(path, bytes);
    files.push({ path: relative, sha256: sha(bytes), bytes: bytes.length });
  };
  const json = (relative: string, value: unknown) =>
    write(relative, Buffer.from(JSON.stringify(value, null, 2) + '\n'));
  try {
    await page.goto(url + '/paper-render.html');
    await page.waitForFunction(() => typeof window.atlasPaperRender === 'function');
    const render = async (relative: string, frame: PaperFrame) => {
      const result = await page.evaluate(value => window.atlasPaperRender(value), frame);
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
      write(relative, bytes);
      files.at(-1)!.foreground = foreground;
    };

    for (const model of challengeModels()) {
      const root = `models/${model.tier}/${model.id}`;
      json(`${root}/metadata.json`, {
        version: CHALLENGE_VERSION, id: model.id, name: model.name, tier: model.tier,
        domain: model.domain, description: model.description, capabilityPressure: model.capabilityPressure,
        palette: model.palette, parts: model.structure.parts.length, assemblyOrder: model.assemblyOrder,
        source: 'original explicit BrickAtlas challenge design', license: 'CC0-1.0',
      });
      json(`${root}/structure.json`, model.structure);
      for (const view of ['iso', 'top', 'front', 'side'] as const) {
        await render(`${root}/views/${view}.png`, { parts: model.structure.parts, view });
      }
      const checkpoints = [...new Set([.25, .5, .75, 1].map(f => Math.ceil(model.assemblyOrder.length * f)))];
      let previous = 0;
      for (const count of checkpoints) {
        const ids = model.assemblyOrder.slice(0, count);
        await render(`${root}/steps/${String(count).padStart(2, '0')}-of-${model.assemblyOrder.length}.png`, {
          parts: ids.map(id => model.structure.parts.find(p => p.id === id)!),
          frameParts: model.structure.parts, highlightIds: ids.slice(previous),
        });
        previous = count;
      }
      await render(`${root}/exploded.png`, { parts: model.structure.parts, explode: .65 });
    }

    for (const task of challengeTasks()) {
      const root = `tasks/${task.kind}`, marked = highlights(task);
      json(`${root}/task.json`, {
        version: CHALLENGE_VERSION, id: task.id, kind: task.kind, sourceId: task.model.id,
        tier: task.model.tier, prompt: task.prompt, input: task.input,
        responseSchema: task.responseSchema, groundTruth: task.oracle,
        scoring: 'benchmark/suite/challenge/evaluate.ts',
      });
      await render(`${root}/input/context.png`, {
        parts: task.source?.parts ?? task.target.parts, frameParts: task.target.parts, highlightIds: marked,
      });
      const modelImages: string[] = [];
      for (const [index, frame] of task.frames.entries()) {
        modelImages.push(`input/reference-${String(index + 1).padStart(2, '0')}-${frame.view}.png`);
        await render(`${root}/input/reference-${String(index + 1).padStart(2, '0')}-${frame.view}.png`, {
          parts: frame.parts, view: frame.view,
        });
      }
      json(`${root}/public.json`, { ...publicChallenge(task), images: modelImages,
        note: 'Only this file and its referenced PNGs are model input. Context and ground-truth images are reviewer-only.' });
      await render(`${root}/ground-truth/iso.png`, { parts: task.target.parts, highlightIds: task.changedIds });
      await render(`${root}/ground-truth/exploded.png`, {
        parts: task.target.parts, explode: .65, highlightIds: task.changedIds,
      });
      if (task.kind === 'active-inspection') {
        await render(`${root}/ground-truth/minimal-inspection.png`, {
          parts: task.target.parts.filter(p => p.y === 13), frameParts: task.target.parts, view: 'top',
        });
      }
      if (task.kind === 'support-counterfactual') {
        const removed = new Set([
          ...(task.input.forcedRemoveIds as string[]),
          ...(task.oracle as { unsupportedIds: string[] }).unsupportedIds,
        ]);
        await render(`${root}/ground-truth/after-collapse.png`, {
          parts: task.target.parts.filter(p => !removed.has(p.id)), frameParts: task.target.parts,
        });
      }
      if (task.kind === 'recovery-plan') {
        let current = structuredClone(task.source!.parts);
        const actions = (task.oracle as { actions: Array<{ type: 'remove' | 'place'; id: string }> }).actions;
        const checkpoints = new Set([0, Math.ceil(actions.length / 3), Math.ceil(2 * actions.length / 3), actions.length]);
        await render(`${root}/ground-truth/recovery-00.png`, { parts: current, frameParts: task.target.parts });
        for (const [index, action] of actions.entries()) {
          if (action.type === 'remove') {
            assert.equal(removeIssue(current, action.id), null);
            current = current.filter(p => p.id !== action.id);
          } else {
            const part = task.target.parts.find(p => p.id === action.id)!;
            assert.equal(insertIssue(current, part), null);
            current = [...current, part];
          }
          if (checkpoints.has(index + 1)) await render(
            `${root}/ground-truth/recovery-${String(index + 1).padStart(2, '0')}.png`,
            { parts: current, frameParts: task.target.parts, highlightIds: [action.id] },
          );
        }
      }
    }

    json('protocol.json', challengeProtocol());
    const manifest = {
      version: CHALLENGE_VERSION, generatedAt: 'deterministic-from-source',
      sourceHashes: Object.fromEntries(
        ['challenge/models.ts', 'challenge/tasks.ts', 'challenge/evaluate.ts', 'challenge/inspection.ts', 'challenge/protocol.ts', 'challenge/render.ts', 'web/paper-render.ts']
          .map(path => [path, digest(readFileSync(resolve(sourceRoot, path), 'utf8'))]),
      ),
      models: challengeModels().map(model => ({
        id: model.id, name: model.name, tier: model.tier, domain: model.domain,
        parts: model.structure.parts.length, capabilityPressure: model.capabilityPressure,
      })),
      tasks: challengeTasks().map(task => ({
        id: task.id, kind: task.kind, sourceId: task.model.id, tier: task.model.tier,
      })),
      totals: {
        models: challengeModels().length,
        tasks: challengeTasks().length,
        placedPartInstances: challengeModels().reduce((sum, model) => sum + model.structure.parts.length, 0),
        minParts: Math.min(...challengeModels().map(model => model.structure.parts.length)),
        maxParts: Math.max(...challengeModels().map(model => model.structure.parts.length)),
      },
      files,
      guarantees: [
        'All models are connected, collision-free, supported, and executable under vertical insertion.',
        'Every task oracle passes the dedicated challenge evaluator.',
        'No model inference result is reported for this new challenge layer.',
      ],
      limitations: [
        'Still restricted to 25 rectangular grid parts and stud connections.',
        'No force, clutch, hinge, axle, ball-joint, or robot-motion validation.',
        'Difficulty tiers are design strata pending independent human calibration.',
      ],
    };
    json('manifest.json', manifest);
    write('README.md', Buffer.from(`# BrickAtlas Challenge Cases\n\n` +
      `Six original 49-63 part structures and twelve advanced task contracts. ` +
      `This layer stresses long-horizon recovery, counterfactual support, compound editing, multi-fault repair, ` +
      `active inspection, graph reasoning, distributed completion, module transforms, next-step selection, pose estimation, ` +
      `large-scene reconstruction, and inventory-constrained redesign.\n\n` +
      `No model scores have been run on this layer. See \`../CHALLENGE_REPORT.zh-CN.md\`, \`CONTACT_SHEET.png\`, and \`TASK_MATRIX.png\`.\n`));
  } finally {
    await browser.close();
  }
  if (existsSync(CHALLENGE_OUTPUT)) rmSync(CHALLENGE_OUTPUT, { recursive: true });
  renameSync(temporary, CHALLENGE_OUTPUT);
  return JSON.parse(readFileSync(resolve(CHALLENGE_OUTPUT, 'manifest.json'), 'utf8'));
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const config = JSON.parse(readFileSync(resolve(dirname(fileURLToPath(import.meta.url)), '../../.runtime/suite-server.json'), 'utf8'));
  const result = await renderChallengeCases(process.env.BRICKATLAS_URL ?? config.url);
  console.log(JSON.stringify(result.totals));
}
