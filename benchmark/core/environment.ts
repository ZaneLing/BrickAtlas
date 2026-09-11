import type { Action, Blueprint, Brick, EpisodeScore, Observation, Phase, Protocol, View } from '../shared/types';
import type { Task } from './tasks';
import { compileBlueprint, components, parseBlueprint, removalIssue, scoreWorld, validBrick, validateWorld } from './world';

export class Environment {
  phase: Phase = 'inspect';
  view: View = 'iso';
  inspection: Brick[];
  built: Brick[] = [];
  inventory: Task['inventory'];
  blueprint: Blueprint | null = null;
  feedback = 'ready';
  actions = 0;
  primitiveActions = 0;
  invalidActions = 0;
  inspectionRemovals = 0;
  faultTriggered = false;
  faultEligible = false;
  faultAt = 0;
  private serial = 0;
  private placements = 0;
  private causal: boolean[] = [];
  readonly maxActions = 14;
  readonly maxPrimitives = 48;

  constructor(readonly task: Task, readonly protocol: Protocol = 'active') {
    this.inspection = structuredClone(task.target);
    this.inventory = structuredClone(task.inventory);
  }

  visibleParts() {
    if (this.phase !== 'inspect') return this.built;
    // The closed opaque shell hides these interiors for every allowed exterior view.
    const closed = this.inspection.some(p => p.id === this.task.coverId);
    return this.inspection.filter(p => !closed || !this.task.hiddenIds.includes(p.id));
  }

  sceneParts() { return this.phase === 'inspect' ? this.inspection : this.built; }

  observe(): Observation {
    return {
      phase: this.phase, protocol: this.protocol, view: this.view,
      visible: this.visibleParts().map(p => ({ id: p.id, partId: p.partId, color: p.color })),
      inventory: structuredClone(this.inventory),
      blueprint: this.phase === 'inspect' ? null : structuredClone(this.blueprint),
      feedback: this.feedback, remainingActions: Math.max(0, this.maxActions - this.actions),
    };
  }

  step(raw: unknown) {
    if (this.phase === 'done') return this.observe();
    this.actions++;
    this.feedback = 'accepted';
    if (!raw || typeof raw !== 'object' || this.actions > this.maxActions) {
      this.reject('invalid_action');
      this.phase = this.actions >= this.maxActions ? 'done' : this.phase;
      return this.observe();
    }
    const action = raw as Action;
    if (action.type === 'look') {
      if (!['iso', 'top', 'front', 'back'].includes(action.view)) this.reject('invalid_view');
      else this.view = action.view;
    } else if (action.type === 'detach') {
      this.primitiveActions++;
      if (this.phase === 'inspect' && this.protocol === 'passive') this.reject('inspection_disabled');
      else if (!this.visibleParts().some(p => p.id === action.id)) this.reject('not_observed');
      else {
        const parts = this.sceneParts();
        const issue = removalIssue(parts, action.id);
        if (issue) this.reject(issue);
        else {
          const before = new Set(this.visibleParts().map(p => p.id));
          const removed = parts.find(p => p.id === action.id)!;
          const remaining = parts.filter(p => p.id !== action.id);
          if (this.phase === 'inspect') {
            this.inspection = remaining;
            this.inspectionRemovals++;
            const newlyVisible = this.visibleParts().filter(p => !before.has(p.id)).length;
            this.causal.push(action.predict?.newlyVisible === newlyVisible
              && action.predict?.components === components(remaining));
          } else {
            this.built = remaining;
            this.returnToInventory(removed);
          }
        }
      }
    } else if (action.type === 'blueprint') {
      if (this.phase !== 'inspect') this.reject('wrong_phase');
      else {
        const blueprint = parseBlueprint(action.blueprint);
        if (!blueprint) this.reject('invalid_blueprint');
        else {
          this.blueprint = blueprint;
          this.phase = 'build';
          this.view = 'iso';
          this.feedback = 'handoff';
        }
      }
    } else if (action.type === 'place' || action.type === 'build') {
      if (this.phase !== 'build') this.reject('wrong_phase');
      else {
        const parts = action.type === 'place' ? [action.part] : action.parts;
        if (!Array.isArray(parts) || !parts.length || parts.length > 12) this.reject('invalid_batch');
        else {
          for (const p of parts) {
            this.primitiveActions++;
            if (this.primitiveActions > this.maxPrimitives) { this.reject('primitive_budget'); break; }
            const part = { ...p, id: `b${++this.serial}` };
            if (!validBrick(part)) { this.reject('invalid_part'); break; }
            const item = this.inventory.find(i => i.partId === part.partId && i.color === part.color);
            const issue = validateWorld([...this.built, part]);
            if (!item?.count || issue) { this.reject(issue ?? 'no_inventory'); break; }
            item.count--;
            this.built.push(part);
            this.placements++;
            this.injectFault();
          }
        }
      }
    } else if (action.type === 'finish') {
      this.phase = 'done';
      this.feedback = 'submitted';
    } else this.reject('invalid_action');
    if (this.actions >= this.maxActions || this.primitiveActions >= this.maxPrimitives) {
      this.phase = 'done';
      this.feedback = 'budget_exhausted';
    }
    return this.observe();
  }

  private reject(reason: string) {
    this.invalidActions++;
    this.feedback = reason;
  }

  private returnToInventory(part: Brick) {
    const item = this.inventory.find(i => i.partId === part.partId && i.color === part.color);
    if (item) item.count++;
    else this.inventory.push({ partId: part.partId, color: part.color, count: 1 });
  }

  private injectFault() {
    if (this.faultTriggered || this.task.fault === 'none' || this.placements < this.task.target.length) return;
    const roof = this.built.find(p => p.partId === '3958' && p.y === 4);
    if (!roof || removalIssue(this.built, roof.id)) return;
    const candidate = this.task.fault === 'missing'
      ? this.built.filter(p => p !== roof)
      : this.built.map(p => p === roof ? { ...p, x: p.x + 1 } : p);
    if (validateWorld(candidate)) return;
    this.faultEligible = scoreWorld(this.task.target, this.built).exact;
    this.faultTriggered = true;
    this.faultAt = this.primitiveActions;
    this.built = candidate;
    if (this.task.fault === 'missing') this.returnToInventory(roof);
  }

  score(): EpisodeScore {
    const anatomy = scoreWorld(this.task.target, this.blueprint?.parts ?? []);
    const construction = scoreWorld(this.task.target, this.built);
    const blueprintExecutable = this.blueprint
      ? compileBlueprint(this.blueprint, this.task.inventory).ok : false;
    return {
      anatomy, construction, blueprintExecutable,
      lifecycleSuccess: this.phase === 'done' && anatomy.exact && blueprintExecutable
        && construction.exact && (this.task.fault === 'none' || this.faultTriggered),
      causalAccuracy: this.causal.length ? this.causal.filter(Boolean).length / this.causal.length : null,
      causalAttempts: this.causal.length,
      actions: this.actions, primitiveActions: this.primitiveActions,
      invalidActions: this.invalidActions, inspectionRemovals: this.inspectionRemovals,
      recoverySuccess: this.faultTriggered && this.faultEligible ? construction.exact : null,
      faultTriggered: this.faultTriggered, faultEligible: this.faultEligible,
      postFaultActions: this.faultTriggered ? this.primitiveActions - this.faultAt : 0,
    };
  }
}
