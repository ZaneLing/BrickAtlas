import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import { PNG } from 'pngjs';
import { atomicJson } from '../../core/budget';
import { BENCHMARK } from '../storage';
import { SuiteRenderer } from '../render';
import { dataset, POLICIES } from './dataset';
import { caseSpecs, taskForV2 } from './cases';
import { DIRECTORY } from './build';

const { url } = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
const renderer = new SuiteRenderer(url), images = [];
const out = resolve(DIRECTORY, 'render-audit'); mkdirSync(out, { recursive: true });
try {
  for (const policy of POLICIES) {
    const model = dataset().filter(m => m.policy === policy).sort((a, b) => b.structure.parts.length - a.structure.parts.length)[0];
    for (const condition of ['ordinary', 'layers'] as const) {
      const s = caseSpecs().find(s => s.modelId === model.id && s.kind === 'reconstruct' && s.condition === condition)!;
      for (const [i, frame] of taskForV2(s).frames.entries()) {
        const r = await renderer.render(frame), png = PNG.sync.read(r.buffer), colors = new Set<string>();
        assert.equal(png.width, 640); assert.equal(png.height, 480);
        for (let p = 0; p < png.data.length; p += 32) colors.add(png.data.subarray(p, p + 3).toString('hex'));
        assert.ok(colors.size > 40);
        images.push({ policy, caseId: s.id, condition, frame: i, hash: r.hash, colors: colors.size });
        if (condition === 'ordinary' && i === 0) writeFileSync(resolve(out, policy + '.png'), r.buffer);
      }
    }
  }
  const result = { checkedAt: new Date().toISOString(), policies: POLICIES.length, frames: images.length, images,
    scope: 'Largest sample per policy, ordinary and layer views; not all dataset PNGs were pre-rendered.', apiRequests: 0 };
  atomicJson(resolve(out, 'verification.json'), result); console.log(JSON.stringify({ policies: result.policies, frames: result.frames }));
} finally { await renderer.close(); }
