import { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, CheckCircle2, Download, FileUp, RotateCcw, XCircle } from 'lucide-react';
import {
  clearReviews,
  createReviewBatch,
  importReviewBatch,
  loadReviews,
  type ReviewRecord,
} from './reviewStore';
import './benchmark.css';

const base = `${import.meta.env.BASE_URL}benchmark/`;
interface Entry {
  id: string;
  name: string;
  nameZh: string;
  difficulty: string;
  parts: number;
  modules: number;
  tasks: number;
}

function downloadJson(value: unknown, filename: string) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(value, null, 2) + '\n'], { type: 'application/json' }));
  const link = document.createElement('a');
  link.href = url; link.download = filename; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 0);
}

export function BenchmarkReviewDashboard() {
  const [entries, setEntries] = useState<Entry[]>([]);
  const [records, setRecords] = useState<Record<string, ReviewRecord>>(() => loadReviews());
  const [error, setError] = useState(''), [notice, setNotice] = useState('');
  const input = useRef<HTMLInputElement>(null);
  useEffect(() => {
    const controller = new AbortController();
    fetch(`${base}catalog.json`, { signal: controller.signal }).then(response => {
      if (!response.ok) throw new Error(`模型库 HTTP ${response.status}`);
      return response.json();
    }).then(setEntries).catch(reason => { if (!controller.signal.aborted) setError(String(reason)); });
    return () => controller.abort();
  }, []);
  const total = entries.reduce((sum, entry) => sum + entry.tasks, 0);
  const rows = Object.values(records);
  const passed = rows.filter(row => row.decision === 'pass').length;
  const failed = rows.length - passed;
  const firstPending = entries.find(entry => rows.filter(row => row.modelId === entry.id).length < entry.tasks);
  const byDifficulty = useMemo(() => ['D1', 'D2', 'D3', 'D4'].map(difficulty => {
    const models = entries.filter(entry => entry.difficulty === difficulty);
    const taskCount = models.reduce((sum, entry) => sum + entry.tasks, 0);
    const reviewed = rows.filter(row => row.difficulty === difficulty).length;
    const failures = rows.filter(row => row.difficulty === difficulty && row.decision === 'fail').length;
    return { difficulty, taskCount, reviewed, failures };
  }), [entries, rows]);
  const exportBatch = () => {
    const batch = createReviewBatch(records, total);
    downloadJson(batch, `${batch.batchId}.json`);
    setNotice(`已导出 ${batch.summary.reviewed} 条审核记录`);
  };
  const importFile = async (file?: File) => {
    if (!file) return;
    try {
      const merged = importReviewBatch(await file.text());
      setRecords(merged); setError(''); setNotice(`已导入并合并 ${Object.keys(merged).length} 条记录`);
    } catch (reason) { setError(reason instanceof Error ? reason.message : String(reason)); }
    if (input.current) input.current.value = '';
  };
  return <div className="bench-page bench-review-page">
    <header className="bench-topbar">
      <a href={`${import.meta.env.BASE_URL}benchmark`}><ArrowLeft size={18} />基准模型库</a>
      <strong>Hierarchy-3 人工审核台</strong>
      {firstPending
        ? <a className="bench-primary-link" href={`${import.meta.env.BASE_URL}benchmark/${firstPending.id}?review=1`}>继续逐题审核</a>
        : entries.length > 0 && <span>本批次已全部审核</span>}
    </header>
    <main className="bench-review-main">
      <section className="bench-review-summary">
        <div><small>批次进度</small><strong>{rows.length} / {total || 2304}</strong>
          <progress max={total || 2304} value={rows.length} /></div>
        <div><CheckCircle2 size={18} /><span>通过</span><strong>{passed}</strong></div>
        <div><XCircle size={18} /><span>不通过</span><strong>{failed}</strong></div>
        <div><span>待审核</span><strong>{Math.max(0, (total || 2304) - rows.length)}</strong></div>
      </section>
      <div className="bench-review-actions">
        <button onClick={exportBatch}><Download size={17} />导出本批次 JSON</button>
        <button onClick={() => input.current?.click()}><FileUp size={17} />导入审核 JSON</button>
        <input ref={input} hidden type="file" accept="application/json,.json"
          onChange={event => void importFile(event.target.files?.[0])} />
        <button onClick={() => {
          if (!confirm('确定清空浏览器中的全部 Hierarchy-3 审核记录？请先导出备份。')) return;
          setRecords(clearReviews()); setNotice('本地审核记录已清空');
        }}><RotateCcw size={17} />清空本地批次</button>
      </div>
      {error && <p role="alert" className="bench-review-error">{error}</p>}
      {notice && <p role="status" className="bench-review-notice">{notice}</p>}
      <section>
        <h1>按难度汇总</h1>
        <div className="bench-review-levels">{byDifficulty.map(level =>
          <div key={level.difficulty}><strong>{level.difficulty}</strong>
            <span>{level.reviewed}/{level.taskCount || 576} 已审核</span>
            <small>{level.failures} 条不通过</small>
            <progress max={level.taskCount || 576} value={level.reviewed} /></div>)}</div>
      </section>
      <section>
        <h2>全部模型</h2>
        <div className="bench-review-table-wrap"><table className="bench-review-table">
          <thead><tr><th>难度</th><th>模型</th><th>审核进度</th><th>通过</th><th>不通过</th><th>操作</th></tr></thead>
          <tbody>{entries.map(entry => {
            const modelRows = rows.filter(row => row.modelId === entry.id);
            const modelPass = modelRows.filter(row => row.decision === 'pass').length;
            const modelFail = modelRows.length - modelPass;
            return <tr key={entry.id}><td>{entry.difficulty}</td><td><strong>{entry.nameZh}</strong><small>{entry.name}</small></td>
              <td><progress max={entry.tasks} value={modelRows.length} /><span>{modelRows.length}/{entry.tasks}</span></td>
              <td>{modelPass}</td><td>{modelFail}</td>
              <td><a href={`${import.meta.env.BASE_URL}benchmark/${entry.id}?review=1`}>{modelRows.length ? '继续审核' : '开始审核'}</a></td></tr>;
          })}</tbody>
        </table></div>
      </section>
      <section>
        <h2>不通过清单</h2>
        {failed === 0 ? <p>当前批次没有不通过记录。</p>
          : <div className="bench-failure-list">{rows.filter(row => row.decision === 'fail')
            .sort((a, b) => b.reviewedAt.localeCompare(a.reviewedAt)).map(row =>
              <a key={row.taskId} href={`${import.meta.env.BASE_URL}benchmark/${row.modelId}?review=1&task=${encodeURIComponent(row.taskId)}`}>
                <span>{row.difficulty} · {row.modelId} · {row.title}</span><strong>{row.reason}</strong>
              </a>)}</div>}
      </section>
    </main>
  </div>;
}
