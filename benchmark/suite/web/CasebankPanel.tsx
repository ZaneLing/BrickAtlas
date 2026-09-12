import { useEffect, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight, Download, Eye, Send } from 'lucide-react';
import { TASKS, LABELS, type Part, type PublicTask } from '../shared';
import type { CaseSpec } from '../v2/cases';
import type { Evaluation } from '../v2/evaluate';
import type { groundTruth } from '../v2/ground-truth';
import { viewer } from './viewer';
import { TraceInspector } from './TraceInspector';
import './casebank.css';

type Truth = ReturnType<typeof groundTruth>;
interface Manifest { structures: number; cases: number; catalogQuestions: number; policyNames: string[] }
interface Page { total: number; page: number; items: CaseSpec[] }
interface Summary { id: string; model: string; baseline: boolean; cases: number;
  rows: { stratum: string; n: number; sourceGroups: number; missing: number;
    metrics: Record<string, { value: number; denominator: number }> }[] }
async function get<T>(path: string): Promise<T> {
  const response = await fetch(path), data = await response.json();
  if (!response.ok) throw new Error(data.error); return data;
}
function Geometry({ parts, label }: { parts: Part[]; label: string }) {
  const ref = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const v = viewer(ref.current!, true); v.setParts(parts);
    return () => v.dispose();
  }, [parts]);
  return <figure><figcaption>{label}</figcaption><canvas ref={ref} aria-label={label} width={640} height={480} /></figure>;
}
export function CasebankPanel({ token }: { token: string }) {
  const [manifest, setManifest] = useState<Manifest | null>(null), [page, setPage] = useState<Page | null>(null);
  const [filters, setFilters] = useState({ kind: 'reconstruct', split: 'test_id', condition: 'ordinary', policy: 'all', difficulty: 'all' });
  const [pageNumber, setPageNumber] = useState(0), [id, setId] = useState('');
  const [input, setInput] = useState<PublicTask | null>(null), [truth, setTruth] = useState<Truth | null>(null);
  const [showTruth, setShowTruth] = useState(false), [answer, setAnswer] = useState('{}');
  const [verdict, setVerdict] = useState<Evaluation | null>(null), [error, setError] = useState('');
  const [summaries, setSummaries] = useState<Summary[]>([]), [run, setRun] = useState('');
  const [runPage, setRunPage] = useState(0), [runRows, setRunRows] = useState<{ hasNext: boolean; items: { spec: CaseSpec; answer: unknown; verdict: Evaluation; missing: boolean }[] } | null>(null);
  const [traceCase, setTraceCase] = useState('');
  useEffect(() => {
    void get<Manifest>('/api/v2/manifest').then(setManifest).catch(e => setError(e.message));
    void get<Summary[]>('/api/v2/evaluations').then(setSummaries).catch(e => setError(e.message));
  }, []);
  useEffect(() => {
    let active = true;
    const query = new URLSearchParams({ ...filters, page: String(pageNumber) });
    void get<Page>('/api/v2/cases?' + query).then(data => { if (active) setPage(data); }).catch(e => { if (active) setError(e.message); });
    return () => { active = false; };
  }, [filters, pageNumber]);
  useEffect(() => {
    let active = true; setInput(null); setTruth(null); setShowTruth(false); setVerdict(null); setError('');
    if (id) void get<PublicTask>(`/api/v2/cases/${id}/input`).then(data => {
      if (active) { setInput(data); setAnswer(JSON.stringify(data.responseSchema, null, 2)); }
    }).catch(e => { if (active) setError(e.message); });
    return () => { active = false; };
  }, [id]);
  useEffect(() => {
    let active = true; setRunRows(null);
    if (run) void get<NonNullable<typeof runRows>>(`/api/v2/evaluations/${run}/cases?page=${runPage}`)
      .then(data => { if (active) setRunRows(data); }).catch(e => { if (active) setError(e.message); });
    return () => { active = false; };
  }, [run, runPage]);
  const toggleTruth = async () => {
    if (showTruth) { setShowTruth(false); return; }
    try { const data = await get<Truth>(`/api/v2/cases/${id}/truth`); setTruth(data); setShowTruth(true); }
    catch (e) { setError((e as Error).message); }
  };
  const submit = async () => {
    try {
      const res = await fetch('/api/v2/evaluate', { method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Benchmark-Client': token },
        body: JSON.stringify({ caseId: id, answer: JSON.parse(answer) }) });
      const data = await res.json(); if (!res.ok) throw new Error(data.error); setVerdict(data); setError('');
    } catch (e) { setError((e as Error).message); }
  };
  return <main className="casebank">
    <div className="heading"><h2>Casebank v2</h2><span>{manifest?.structures.toLocaleString()} 结构 · {manifest?.cases.toLocaleString()} 题 · {manifest?.catalogQuestions} 目录题</span></div>
    {error && <p role="alert">{error}</p>}
    <div className="casebank-filters">{Object.entries({
      kind: ['all', ...TASKS], split: ['all', 'train', 'validation', 'test_id', 'test_ood'],
      condition: ['all', 'default', 'ordinary', 'layers', 'symbolic'],
      policy: ['all', 'known-catalog', ...(manifest?.policyNames ?? [])], difficulty: ['all', 'isolated', 'small', 'medium', 'large'],
    }).map(([k, options]) => <label key={k}>{k}<select aria-label={`v2 ${k}`} value={filters[k as keyof typeof filters]}
      onChange={e => { setFilters({ ...filters, [k]: e.target.value }); setPageNumber(0); }}>
      {options.map(value => <option key={value}>{value}</option>)}</select></label>)}</div>
    <div className="casebank-pager"><span>{page?.total.toLocaleString() ?? 0} 题 · 第 {pageNumber + 1} 页</span>
      <button className="icon" title="上一页 case" disabled={!pageNumber} onClick={() => setPageNumber(n => n - 1)}><ChevronLeft size={18} /></button>
      <button className="icon" title="下一页 case" disabled={!page || (pageNumber + 1) * 30 >= page.total} onClick={() => setPageNumber(n => n + 1)}><ChevronRight size={18} /></button></div>
    <div className="table-wrap"><table><thead><tr><th>Case ID</th><th>任务</th><th>变体</th><th>条件</th><th>策略</th><th>划分</th><th /></tr></thead><tbody>
      {page?.items.map(s => <tr key={s.id}><td><code>{s.id}</code></td><td>{LABELS[s.kind]}</td><td>{s.variant}</td><td>{s.condition}</td><td>{s.policy}</td><td>{s.split}</td>
        <td><button className="icon" title={`查看 ${s.id}`} onClick={() => setId(s.id)}><Eye size={16} /></button></td></tr>)}
    </tbody></table></div>
    {id && <section className="casebank-detail"><div className="heading"><h3>Case {id}</h3><button className="command" disabled={!input} onClick={() => void toggleTruth()}><Eye size={15} />{showTruth ? '隐藏裁判真值' : '查看裁判真值'}</button></div>
      {!input && <p role="status">加载输入...</p>}
      {input && <><p className="task-prompt">{input.prompt}</p><div className="observation-grid">{input.images?.map((src, i) => <figure key={i}><img src={src} alt={input.imageTitles[i]} /><figcaption>{input.imageTitles[i]}</figcaption></figure>)}</div>
        <details><summary>模型输入 JSON</summary><pre>{JSON.stringify(input.input, null, 2)}</pre></details>
        {showTruth && truth && <div className="casebank-truth"><h3>GROUND TRUTH · 裁判专用 · 程序标注</h3>
          <div className="casebank-geometries">{truth.source && <Geometry parts={truth.source.parts} label="当前结构" />}<Geometry parts={truth.target.parts} label="真值参考结构" /></div>
          <p>{truth.answerSemantics} · 独立检查 {truth.independentCheck.issues.length === 0 ? 'PASS' : 'FAIL'}</p>
          <details><summary>答案、BOM、连接点、顺序见证与指标</summary><pre>{JSON.stringify(truth, null, 2)}</pre></details></div>}
        <div className="submission"><label>答案 JSON<textarea aria-label="v2 answer" rows={9} value={answer} onChange={e => setAnswer(e.target.value)} spellCheck={false} /></label>
          <button className="command primary" onClick={() => void submit()}><Send size={15} />评估此 case</button>
          {verdict && <><p role="status">{verdict.metrics.success === 1 ? 'PASS' : 'FAIL'} · {verdict.issues.join(', ')}</p>
            <div className="casebank-metrics">{Object.entries(verdict.metrics).map(([k, v]) => <div key={k}><span>{k}</span><b>{v === null ? 'N/A' : v.toFixed(4)}</b></div>)}</div>
            <details><summary>匹配与失败定位</summary><pre>{JSON.stringify(verdict.diagnostics, null, 2)}</pre></details></>}
        </div></>}
    </section>}
    <section className="casebank-evaluations"><h2>批量 Evaluation</h2><label>运行<select aria-label="v2 evaluation" value={run} onChange={e => { setRun(e.target.value); setRunPage(0); }}>
      <option value="">选择评测</option>{summaries.map(s => <option key={s.id} value={s.id}>{s.model} · {s.cases} cases · {s.id}</option>)}</select></label>
      {run && <><p>{summaries.find(s => s.id === run)?.baseline ? '公开输入算法基线 · 非神经模型' : '外部提交 · 来源由提交者声明'}</p>
        <div className="table-wrap"><table><thead><tr><th>分层</th><th>cases</th><th>对象组</th><th>漏答</th><th>Success</th></tr></thead><tbody>
          {summaries.find(s => s.id === run)?.rows.map(r => <tr key={r.stratum}><td>{r.stratum}</td><td>{r.n}</td><td>{r.sourceGroups}</td><td>{r.missing}</td><td>{r.metrics.success.value.toFixed(4)} / n={r.metrics.success.denominator}</td></tr>)}
        </tbody></table></div>
        <div className="casebank-pager"><span>输出第 {runPage + 1} 页</span><button className="icon" title="上一页输出" disabled={!runPage} onClick={() => setRunPage(n => n - 1)}><ChevronLeft size={18} /></button>
          <button className="icon" title="下一页输出" disabled={!runRows?.hasNext} onClick={() => setRunPage(n => n + 1)}><ChevronRight size={18} /></button></div>
        {runRows?.items.map(r => <details key={r.spec.id}><summary>{r.spec.id} · {r.spec.kind} · {r.verdict.metrics.success ? 'PASS' : 'FAIL'}{r.missing ? ' · missing' : ''}</summary>
          <button className="command" onClick={() => setId(r.spec.id)}><Eye size={15} />查看 case</button>
          <button className="command" onClick={() => setTraceCase(r.spec.id)}><Eye size={15} />回放提交</button>
          <pre>{JSON.stringify({ answer: r.answer, evaluation: r.verdict }, null, 2)}</pre></details>)}
        {traceCase && <TraceInspector key={run + traceCase} runId={run} caseIndex={0}
          endpointOverride={`/api/v2/evaluations/${run}/trace?caseId=${traceCase}`} />}</>}
    </section>
    <div className="casebank-downloads">{['case-index.jsonl.gz', 'structures.jsonl.gz', 'ground-truth-test_id.jsonl.gz'].map(file =>
      <a className="command" key={file} href={`/api/v2/download/${file}`}><Download size={14} />{file}</a>)}</div>
  </main>;
}
