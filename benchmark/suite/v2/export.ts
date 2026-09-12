import { createWriteStream, existsSync, mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { once } from 'node:events';
import { finished } from 'node:stream/promises';
import { atomicJson } from '../../core/budget';
import { BENCHMARK, SYSTEM } from '../storage';
import { digest } from '../data';
import { SuiteRenderer } from '../render';
import { taskForV2 } from './cases';
import { verifySelection, type Selection } from './batch';
import { DIRECTORY, sourceHashes } from './build';

export async function exportInputs(selection: Selection, renderer: SuiteRenderer) {
  const specs = verifySelection(selection);
  const manifest = JSON.parse(readFileSync(resolve(DIRECTORY, 'manifest.json'), 'utf8'));
  if (digest(manifest.sourceHashes) !== digest(sourceHashes())) throw new Error('Casebank sources differ');
  const dir = resolve(BENCHMARK, '.runtime/casebank-exports', selection.id);
  if (existsSync(resolve(dir, 'export.json'))) throw new Error('Completed export exists; preserve it or explicitly archive it before re-export');
  mkdirSync(resolve(dir, 'images'), { recursive: true });
  atomicJson(resolve(dir, 'selection.json'), selection);
  const output = createWriteStream(resolve(dir, 'inputs.jsonl')), done = finished(output);
  const cache = new Map<string, string>();
  let imageUses = 0;
  try {
    for (const [i, spec] of specs.entries()) {
      const task = taskForV2(spec), images = [];
      for (const f of task.frames) {
        const frameKey = digest(f);
        let path = cache.get(frameKey);
        if (!path) {
          const rendered = await renderer.render(f);
          path = `images/${rendered.hash}.png`; cache.set(frameKey, path);
          writeFileSync(resolve(dir, path), rendered.buffer);
        }
        images.push(path); imageUses++;
      }
      const line = JSON.stringify({ caseId: spec.id, system: SYSTEM, input: task.public, images }) + '\n';
      if (!output.write(line)) await once(output, 'drain');
      if ((i + 1) % 100 === 0) console.log(JSON.stringify({ exported: i + 1, total: specs.length }));
    }
    output.end(); await done;
  } catch (e) { output.destroy(); void done.catch(() => {}); throw e; }
  const report = { selection: selection.id, cases: specs.length, imageUses, uniqueFrames: cache.size, apiRequests: 0,
    status: 'complete', sourceHashes: sourceHashes(), taskInputBytesContainNoPrivateRenderRecipes: true };
  atomicJson(resolve(dir, 'export.json'), report); return report;
}
