import assert from 'node:assert/strict';
import { edges, dims } from '../geometry';
import { evaluateChallenge } from './evaluate';
import type { ChallengeTask } from './tasks';

// A query costs budget even when the policy chooses an uninformative exterior view.
export class InspectionEpisode {
  readonly events: Array<Record<string, unknown>> = [];
  private queryId: string | null = null;
  private finished = false;
  constructor(private readonly task: ChallengeTask) {
    assert.equal(task.kind, 'active-inspection');
  }
  query(id: string) {
    assert.ok(!this.queryId && !this.finished, 'Only one query is allowed');
    const option = (this.task.input.queryOptions as Array<{ id: string; cost: number }>).find(q => q.id === id);
    assert.ok(option, 'Unknown query');
    const parts = this.task.target.parts;
    const rearParts = parts.map(p => {
      const { w, d } = dims(p);
      return { ...p, x: 24 - p.x - w, z: 4 - p.z - d, turn: (p.turn + 2) % 4 };
    });
    const observation = id === 'layer-y-13'
      ? { frame: { parts: parts.filter(p => p.y === 13), view: 'top', layer: 13 } }
      : id === 'symbolic-graph' ? { structure: this.task.target, contacts: edges(parts) }
        : { frame: { parts: id === 'rear-rgb' ? rearParts : parts,
          view: id === 'top-rgb' ? 'top' : 'front', layer: null } };
    this.queryId = id;
    this.events.push({ actor: 'model', type: 'query', id }, { actor: 'environment', type: 'observation', cost: option.cost });
    // frame is a trusted renderer recipe; only its PNG is passed to a visual model.
    return observation;
  }
  submit(answer: unknown) {
    assert.ok(this.queryId && !this.finished, 'Query before submitting; episode already finished or query absent');
    this.finished = true;
    const verdict = evaluateChallenge(this.task, { queryId: this.queryId, answer });
    this.events.push({ actor: 'model', type: 'answer', answer }, { actor: 'evaluator', type: 'score', verdict });
    return verdict;
  }
}
