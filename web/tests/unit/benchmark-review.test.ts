import { describe, expect, it } from 'vitest';
import {
  BENCHMARK_VERSION,
  REVIEW_STORAGE_KEY,
  clearReviews,
  createReviewBatch,
  importReviewBatch,
  loadReviews,
  removeReview,
  reviewTask,
  saveReview,
} from '../../src/benchmark/reviewStore';
import type { Task } from '../../src/benchmark/types';

class MemoryStorage {
  values = new Map<string, string>();
  getItem(key: string) { return this.values.get(key) ?? null; }
  setItem(key: string, value: string) { this.values.set(key, value); }
  removeItem(key: string) { this.values.delete(key); }
}
const task = (id: string): Task => ({
  id,
  modelId: 'camera-gimbal',
  difficulty: 'D1',
  layer: 'atomic',
  family: 'identify',
  title: '模块识别',
  question: '审核题目',
  capabilities: ['模块识别'],
  format: 'single-choice',
  input: {},
  answer: { choiceId: 'A' },
  targetModule: 'mount',
  evidence: 'model-state',
});

describe('benchmark human review batch', () => {
  it('requires a reason for failures but permits a pass without notes', () => {
    expect(() => reviewTask(task('h3-camera-gimbal-a'), 'fail', '  ')).toThrow('必须填写理由');
    expect(reviewTask(task('h3-camera-gimbal-a'), 'pass', '').decision).toBe('pass');
    expect(reviewTask(task('h3-camera-gimbal-a'), 'fail', '选项语义重复').reason).toBe('选项语义重复');
  });

  it('persists, replaces, and removes one decision per task', () => {
    const storage = new MemoryStorage();
    const first = reviewTask(task('h3-camera-gimbal-a'), 'fail', '错误', '2026-09-16T01:00:00.000Z');
    expect(saveReview(first, storage)[first.taskId].decision).toBe('fail');
    const second = reviewTask(task(first.taskId), 'pass', '已复核', '2026-09-16T02:00:00.000Z');
    expect(saveReview(second, storage)[first.taskId].decision).toBe('pass');
    expect(loadReviews(storage)[first.taskId].reason).toBe('已复核');
    expect(removeReview(first.taskId, storage)).toEqual({});
    expect(storage.values.get(REVIEW_STORAGE_KEY)).toBe('[]');
  });

  it('exports complete batch counts and imports only the matching schema', () => {
    const storage = new MemoryStorage();
    const records = Object.fromEntries([
      reviewTask(task('h3-camera-gimbal-a'), 'pass', '', '2026-09-16T01:00:00.000Z'),
      reviewTask(task('h3-camera-gimbal-b'), 'fail', '物理证据不足', '2026-09-16T02:00:00.000Z'),
    ].map(row => [row.taskId, row]));
    const batch = createReviewBatch(records, 2304, new Date('2026-09-16T03:00:00.000Z'));
    expect(batch.benchmarkVersion).toBe(BENCHMARK_VERSION);
    expect(batch.summary).toEqual({ totalTasks: 2304, reviewed: 2, passed: 1, failed: 1, pending: 2302 });
    expect(Object.keys(importReviewBatch(JSON.stringify(batch), storage))).toHaveLength(2);
    expect(() => importReviewBatch(JSON.stringify({ ...batch, benchmarkVersion: 'old' }), storage))
      .toThrow('版本不匹配');
  });

  it('keeps the newer local or imported record during a merge and clears explicitly', () => {
    const storage = new MemoryStorage();
    const id = 'h3-camera-gimbal-a';
    saveReview(reviewTask(task(id), 'pass', 'newer', '2026-09-16T04:00:00.000Z'), storage);
    const older = createReviewBatch(
      { [id]: reviewTask(task(id), 'fail', 'older', '2026-09-16T01:00:00.000Z') },
      2304,
      new Date('2026-09-16T05:00:00.000Z'),
    );
    expect(importReviewBatch(JSON.stringify(older), storage)[id].decision).toBe('pass');
    expect(clearReviews(storage)).toEqual({});
    expect(storage.getItem(REVIEW_STORAGE_KEY)).toBeNull();
  });

  it('ignores corrupt local drafts instead of inventing review decisions', () => {
    const storage = new MemoryStorage();
    storage.setItem(REVIEW_STORAGE_KEY, '{not-json');
    expect(loadReviews(storage)).toEqual({});
  });
});
