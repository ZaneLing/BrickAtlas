import { useEffect, useState } from 'react';
import { ChevronLeft, ChevronRight, Eye } from 'lucide-react';
import { TraceInspector } from './TraceInspector';
import type { Evaluation } from '../v2/evaluate';

interface Run { id: string; status: string; error: string | null; completed: number; expected: number; cost: number;
  rows: { stratum: string; n: number; metrics: Record<string, { value: number | null; n: number }> }[] }
interface Case { index: number; caseId: string; model: string; arm: string; verdict: Evaluation }
interface Training { name: string; status: string; steps: number; targetSteps: number; supervisedTokens: number; predictions: number; inferenceSeconds: number }
async function readJSON<T>(url: string): Promise<T> {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}
export function StudyPanel() {
  const [runs, setRuns] = useState<Run[]>([]), [id, setId] = useState(''), [page, setPage] = useState(0);
  const [rows, setRows] = useState<{ total: number; items: Case[] } | null>(null), [index, setIndex] = useState<number | null>(null);
  const [error, setError] = useState('');
  const [training, setTraining] = useState<Training[]>([]);
  useEffect(() => {
    let active = true;
    const load = () => readJSON<Run[]>('/api/study/runs').then(r => { if (active) setRuns(r); }).catch(e => { if (active) setError(e.message); });
    void load(); const timer = setInterval(load, 5000);
    const loadTraining = () => readJSON<Training[]>('/api/study/training').then(r => { if (active) setTraining(r); }).catch(e => { if (active) setError(e.message); });
    void loadTraining(); const trainingTimer = setInterval(loadTraining, 10000);
    return () => { active = false; clearInterval(timer); clearInterval(trainingTimer); };
  }, []);
  useEffect(() => {
    let active = true; setRows(null); setIndex(null);
    if (id) void readJSON<{ total: number; items: Case[] }>(`/api/study/runs/${id}/cases?page=${page}`)
      .then(r => { if (active) { setRows(r); setError(''); } }).catch(e => { if (active) setError(e.message); });
    return () => { active = false; };
  }, [id, page]);
  const run = runs.find(r => r.id === id);
  return <main className="casebank"><div className="heading"><h2>v2 模型实测</h2></div>
    {error && <p role="alert">{error}</p>}
    <label>实验<select aria-label="study run" value={id} onChange={e => { setId(e.target.value); setPage(0); }}>
      <option value="">选择实验</option>{runs.map(r => <option key={r.id} value={r.id}>{r.id} · {r.status} · {r.completed}/{r.expected}</option>)}</select></label>
    {run && <><p>{run.status} · {run.completed}/{run.expected} · ${run.cost.toFixed(6)} {run.error}</p>
      <div className="table-wrap"><table><thead><tr><th>模型/任务/条件/划分</th><th>n</th><th>成功</th><th>格式</th><th>合法</th></tr></thead><tbody>
        {run.rows.map(r => <tr key={r.stratum}><td>{r.stratum}</td><td>{r.n}</td><td>{r.metrics.success.value?.toFixed(3)}</td>
          <td>{r.metrics.format.value?.toFixed(3)}</td><td>{r.metrics.valid.value?.toFixed(3)}</td></tr>)}</tbody></table></div></>}
    <div className="casebank-pager"><span>第 {page+1} 页</span>
      <button className="icon" title="上一页实测" disabled={!page} onClick={() => setPage(p => p-1)}><ChevronLeft size={18} /></button>
      <button className="icon" title="下一页实测" disabled={!rows || (page+1)*30 >= rows.total} onClick={() => setPage(p => p+1)}><ChevronRight size={18} /></button></div>
    <div className="table-wrap"><table><thead><tr><th>Case</th><th>模型</th><th>条件</th><th>结果</th><th /></tr></thead><tbody>
      {rows?.items.map(r => <tr key={r.index}><td>{r.caseId}</td><td>{r.model}</td><td>{r.arm}</td><td>{r.verdict.metrics.success ? 'PASS' : 'FAIL'}</td>
        <td><button className="icon" title={`回放实测 ${r.index}`} onClick={() => setIndex(r.index)}><Eye size={16} /></button></td></tr>)}</tbody></table></div>
    {index !== null && <TraceInspector key={id+index} runId={id} caseIndex={index} endpointOverride={`/api/study/runs/${id}/cases/${index}/trace`} />}
    <section className="casebank-evaluations"><h2>SmolVLM 多模态训练</h2><div className="table-wrap"><table>
      <thead><tr><th>条件</th><th>状态</th><th>优化步</th><th>监督tokens</th><th>测试输出</th><th>推理秒数</th></tr></thead>
      <tbody>{training.map(t => <tr key={t.name}><td>{t.name}</td><td>{t.status}</td><td>{t.steps}/{t.targetSteps}</td>
        <td>{t.supervisedTokens}</td><td>{t.predictions}/337</td><td>{t.inferenceSeconds.toFixed(1)}</td></tr>)}</tbody>
    </table></div></section>
  </main>;
}
