import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { dirname } from 'node:path';
import { randomUUID } from 'node:crypto';

export const HARD_CAP_USD = 4.5;
export interface Charge {
  id: string;
  model: string;
  reserved: number;
  actual: number | null;
  status: 'pending' | 'settled' | 'uncertain';
  generationId?: string;
}
export interface Ledger {
  version: 1;
  cap: number;
  charges: Charge[];
}
export function atomicJson(path: string, value: unknown) {
  mkdirSync(dirname(path), { recursive: true });
  const temporary = `${path}.${process.pid}.tmp`;
  writeFileSync(temporary, JSON.stringify(value, null, 2) + '\n', { mode: 0o600 });
  renameSync(temporary, path);
}
export class Budget {
  ledger: Ledger;
  constructor(readonly path: string, cap = HARD_CAP_USD) {
    if (!Number.isFinite(cap) || cap <= 0 || cap > HARD_CAP_USD) throw new Error('Budget must be within (0, 4.50] USD');
    this.ledger = existsSync(path)
      ? JSON.parse(readFileSync(path, 'utf8'))
      : { version: 1, cap, charges: [] };
    if (this.ledger.version !== 1 || !Array.isArray(this.ledger.charges)
      || !Number.isFinite(this.ledger.cap) || this.ledger.cap <= 0 || this.ledger.cap > HARD_CAP_USD
      || this.ledger.charges.some(c => !Number.isFinite(c.reserved) || c.reserved < 0
        || c.actual !== null && (!Number.isFinite(c.actual) || c.actual < 0)
        || !['pending', 'settled', 'uncertain'].includes(c.status))) throw new Error('Invalid budget ledger');
    this.ledger.cap = Math.min(this.ledger.cap, cap);
    this.persist();
  }
  get spent() { return this.ledger.charges.reduce((s, c) => s + (c.actual ?? 0), 0); }
  get committed() { return this.ledger.charges.reduce((s, c) => s + (c.actual ?? c.reserved), 0); }
  get blocked() { return this.ledger.charges.some(c => c.status !== 'settled'); }
  reserve(model: string, ceiling: number) {
    if (this.blocked) throw new Error('Unsettled charge: reconcile before another request');
    if (!Number.isFinite(ceiling) || ceiling <= 0 || this.committed + ceiling > this.ledger.cap) {
      throw new Error('Budget limit reached before request');
    }
    const charge: Charge = { id: randomUUID(), model, reserved: ceiling, actual: null, status: 'pending' };
    this.ledger.charges.push(charge);
    this.persist();
    return charge.id;
  }
  settle(id: string, actual: number, generationId: string) {
    const charge = this.ledger.charges.find(c => c.id === id);
    if (!charge || charge.status !== 'pending' || !Number.isFinite(actual) || actual < 0) {
      throw new Error('Invalid charge settlement');
    }
    charge.actual = actual;
    charge.generationId = generationId;
    charge.status = actual <= charge.reserved ? 'settled' : 'uncertain';
    this.persist();
    if (charge.status === 'uncertain') throw new Error('Provider exceeded reserved ceiling; stopped');
  }
  uncertain(id: string) {
    const charge = this.ledger.charges.find(c => c.id === id);
    if (charge?.status === 'pending') charge.status = 'uncertain';
    this.persist();
  }
  summary() {
    return { cap: this.ledger.cap, spent: this.spent, committed: this.committed,
      calls: this.ledger.charges.length, blocked: this.blocked };
  }
  private persist() { atomicJson(this.path, this.ledger); }
}
