import assert from 'node:assert/strict';
import { solveActions } from '../../../src/benchmark/engine';
import type { AtlasManifest } from '../../../src/model/types';
import type { Task } from '../../../src/benchmark/types';
import type { PublicTask } from './types';

/** No generator imports, reference answers, evidenceDetail or reference order. */
export function deriveAnswer(t: PublicTask, manifest: AtlasManifest) {
  const input = t.input;
  const target = t.promptEn.match(/\bB\d{4,}\b/)?.[0];
  const parts = new Map(manifest.instances.map(p => [`B${String(p.index + 1).padStart(4, '0')}`, p]));
  const choice = (label: string) => {
    const options = t.options!.filter(o => o.label === label);
    assert.equal(options.length, 1, `Ambiguous oracle option ${t.id}: ${label}`);
    return { choiceId: options[0].id };
  };
  switch (t.family) {
    case 'color': return choice(parts.get(target!)!.colorName);
    case 'shape-match': {
      const candidates = t.options!.filter(o => parts.get(o.label)!.partNumber === parts.get(target!)!.partNumber);
      assert.equal(candidates.length, 1, `Ambiguous source type: ${t.id}`);
      return { choiceId: candidates[0].id };
    }
    case 'distance': {
      const coords: Record<string, number[]> = input.centers;
      const distance = (label: string) => Math.hypot(...coords[label].map((n, i) => n - coords[target!][i]));
      const options = [...t.options!].sort((a, b) => distance(a.label) - distance(b.label));
      assert.ok(distance(options[1].label) - distance(options[0].label) > .009);
      return { choiceId: options[0].id };
    }
    case 'interface': return choice(input.connectorRecord.family);
    case 'neighbors': {
      const adjacent = new Set<string>();
      for (const [a, b] of input.edges) {
        if (a === target) adjacent.add(b);
        if (b === target) adjacent.add(a);
      }
      return { choiceIds: t.options!.filter(o => adjacent.has(o.label)).map(o => o.id) };
    }
    case 'graph-removal': {
      // Union-find is independent from the generator's breadth-first traversal.
      const nodes: string[] = input.nodes.filter((n: string) => n !== target);
      const parents = new Map(nodes.map(n => [n, n]));
      const find = (n: string): string => parents.get(n) === n ? n : find(parents.get(n)!);
      for (const [a, b] of input.edges)
        if (parents.has(a) && parents.has(b)) parents.set(find(a), find(b));
      return { value: new Set(nodes.map(find)).size };
    }
    case 'coverage': {
      const unknown = input.coverage.filter((r: any) => !r.supported);
      assert.equal(unknown.length, 1);
      return choice(unknown[0].label);
    }
    case 'evidence-limit': return choice('Not established by this evidence');
    case 'source-step': {
      const steps = input.steps.filter((s: any) => s.numbers.includes(target));
      return choice(String(Math.min(...steps.map((s: any) => s.index))));
    }
    case 'source-sequence':
    case 'restore-instance':
      return solveActions({ input } as Task);
    default: throw new Error(`No independent oracle: ${t.family}`);
  }
}
