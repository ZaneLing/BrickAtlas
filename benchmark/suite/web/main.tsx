import { useEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Box, Database, FlaskConical, BarChart3, ShieldCheck, Eye, Play, Send, Download, X, ArrowUpRight, Code2, Cpu, ClipboardCheck } from 'lucide-react';
import { LABELS, TASKS, VERSION, type DatasetSummary, type Kind, type Mode, type Part, type PublicTask, type SampleSummary, type Verdict, type View } from '../shared';
import { viewer } from './viewer';
import { TraceInspector } from './TraceInspector';
import { TrainingPanel } from './TrainingPanel';
import { ReviewPanel } from './ReviewPanel';
import { CasebankPanel } from './CasebankPanel';
import { StudyPanel } from './StudyPanel';
import './style.css';

interface Status {
  token: string; keyPresent: boolean; locked: boolean;
  models: { id: string; label: string }[]; budget: { spent: number; cap: number; uncertain: boolean };
  progress: { running: boolean; completed: number; total: number; error?: string };
}
interface Model extends SampleSummary {
  structure: { parts: Part[] }; provenance: { source: string; license: string };
  ports?: unknown; portsSource?: string; certificate?: unknown;
}
interface RunSummary {
  id: string; status: string; mode: string; representation: string; cost: number; version?: string;
  rows: { model: string; kind: Kind; condition?: string; n: number; errors: number; metrics: Record<string, number | null>; cost: number }[];
}
interface RunDetail {
  id: string; results: { taskId: string; kind: Kind; model: string; split: string; input: PublicTask; frames: string[];
    answers: unknown[]; calls: { cost: number; id: string; content: string; provider: string }[]; verdict: Verdict }[];
}
async function api<T>(path: string, token?: string, data?: unknown): Promise<T> {
  const res = await fetch(path, data === undefined ? undefined : {
    method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Benchmark-Client': token ?? '' }, body: JSON.stringify(data),
  });
  const value = await res.json(); if (!res.ok) throw new Error(value.error ?? 'Request failed'); return value;
}
function Scene({ parts }: { parts: Part[] }) {
  const canvas = useRef<HTMLCanvasElement>(null);
  const handle = useRef<ReturnType<typeof viewer> | null>(null);
  const [view, setView] = useState<View>('iso');
  useEffect(() => {
    const scene = viewer(canvas.current!, true); handle.current = scene; scene.setParts(parts);
    return () => { handle.current = null; scene.dispose(); };
  }, []);
  useEffect(() => { handle.current?.setParts(parts, view); }, [parts]);
  return <div className="scene-wrap"><canvas aria-label="交互式积木结构" ref={canvas} width={640} height={480} />
    <div className="scene-tools">{(['iso', 'top', 'front', 'side'] as View[]).map((v, i) => <button key={v} title={['斜视', '俯视', '前视', '侧视'][i]} aria-pressed={view === v}
      onClick={() => { setView(v); handle.current?.setView(v); }}><Eye size={14} />{['斜视', '俯视', '前视', '侧视'][i]}</button>)}</div>
  </div>;
}
function App() {
  const [tab, setTab] = useState<'data' | 'task' | 'result' | 'protocol' | 'training' | 'review' | 'casebank' | 'study'>('data');
  const [status, setStatus] = useState<Status | null>(null);
  const [dataset, setDataset] = useState<{ summary: DatasetSummary; items: SampleSummary[] } | null>(null);
  const [release, setRelease] = useState<'pilot' | 'research'>('pilot');
  const [condition, setCondition] = useState('ordinary');
  const dataApi = release === 'research' ? '/api/research' : '/api';
  const [family, setFamily] = useState('all'), [split, setSplit] = useState('all');
  const [modelId, setModelId] = useState(''), [model, setModel] = useState<Model | null>(null);
  const [kind, setKind] = useState<Kind>('reconstruct'), [task, setTask] = useState<PublicTask | null>(null);
  const [answer, setAnswer] = useState('{\n  "version": 1,\n  "parts": []\n}'), [verdict, setVerdict] = useState<Verdict | null>(null);
  const [loading, setLoading] = useState(false), [error, setError] = useState('');
  const [runs, setRuns] = useState<RunSummary[]>([]), [detail, setDetail] = useState<RunDetail | null>(null), [caseIndex, setCaseIndex] = useState(0);
  const [mode, setMode] = useState<Mode>('one-shot'), [paidModels, setPaidModels] = useState(['openai/gpt-4.1-mini', 'google/gemini-2.5-flash']);
  const dialog = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    let live = true;
    const poll = async () => {
      try {
        const s = await api<Status>('/api/status'); if (live) setStatus(s);
        const r = await api<RunSummary[]>('/api/runs'); if (live) setRuns(r);
      } catch (e) { if (live) setError((e as Error).message); }
    };
    void poll();
    const timer = setInterval(() => void poll(), 3000);
    return () => { live = false; clearInterval(timer); };
  }, []);
  useEffect(() => {
    let live = true;
    setModelId(''); setModel(null); setTask(null); setDataset(null); setFamily('all'); setSplit('all');
    if (release === 'research') setMode('one-shot');
    void api<{ summary: DatasetSummary; items: SampleSummary[] }>(dataApi + '/dataset').then(d => {
      if (live) { setDataset(d); setModelId(d.items[0]?.id ?? ''); }
    }).catch(e => { if (live) setError(e.message); });
    return () => { live = false; };
  }, [release]);
  useEffect(() => {
    let live = true;
    if (modelId && modelId.startsWith('r') === (release === 'research')) {
      void api<Model>(`${dataApi}/models/${modelId}`).then(m => { if (live) setModel(m); }).catch(e => { if (live) setError(e.message); });
    }
    return () => { live = false; };
  }, [modelId, release]);
  useEffect(() => {
    let live = true;
    if (modelId && tab === 'task' && modelId.startsWith('r') === (release === 'research')) {
      setLoading(true); setTask(null); setVerdict(null);
      void api<PublicTask>(`${dataApi}/task?model=${modelId}&kind=${kind}&condition=${condition}`).then(t => {
        if (live) { setTask(t); setAnswer(JSON.stringify(t.responseSchema, null, 2)); }
      }).catch(e => { if (live) setError(e.message); }).finally(() => { if (live) setLoading(false); });
    }
    return () => { live = false; };
  }, [modelId, kind, tab, condition, release]);
  const filtered = dataset?.items.filter(m => (family === 'all' || m.family === family) && (split === 'all' || m.split === split)) ?? [];
  const submit = async () => {
    try { setVerdict(await api<Verdict>('/api/submit', status?.token, { modelId, kind, condition, answer: JSON.parse(answer) })); setError(''); }
    catch (e) { setError((e as Error).message); }
  };
  const paid = async () => {
    dialog.current?.close();
    try {
      await api(dataApi + '/run', status?.token, { confirmPaid: true, models: paidModels, mode });
      setTab('result');
      if (status) setStatus({ ...status, locked: true });
    } catch (e) { setError((e as Error).message); }
  };
  const selectedCase = detail?.results[caseIndex];
  const pct = (value: number | null | undefined) => typeof value === 'number' ? `${(value * 100).toFixed(1)}%` : 'N/A';
  return <div className="shell">
    <header><a className="brand" href="http://127.0.0.1:5173"><Box size={25} /><b>BrickAtlas</b><ArrowUpRight size={14} /></a>
      <span className="header-line" /><h1>多任务 Benchmark</h1><span className="version">RESEARCH SUITE 1.0</span>
      <span className="connection"><i />{status?.keyPresent ? 'OpenRouter 已配置' : '未配置模型 API'}</span></header>
    <div className="nav-row"><nav>{([
      ['data', '结构数据', Database], ['task', '任务评测', FlaskConical], ['result', '模型结果', BarChart3], ['protocol', '协议与指标', ShieldCheck],
      ['training', '训练与验证', Cpu], ['review', '人工审核', ClipboardCheck],
      ['casebank', 'Casebank v2', Database],
      ['study', 'v2 模型实测', FlaskConical],
    ] as const).map(([id, text, Icon]) => <button key={id} className={tab === id ? 'active' : ''} onClick={() => setTab(id)}><Icon size={16} />{text}</button>)}</nav>
      <div className="budget">累计 <strong>${status?.budget.spent.toFixed(4) ?? '0.0000'}</strong><span>/ $4.50</span></div></div>
    {error && <div role="alert" className="alert">{error}<button className="icon" title="关闭错误" onClick={() => setError('')}><X size={16} /></button></div>}
    {(status?.locked || status?.progress.running) && <div role="status" className="progress">模型运行中 <progress value={status.progress.completed} max={status.progress.total || 1} /><span>{status.progress.completed}/{status.progress.total}</span></div>}
    <div className="metrics-strip"><div><span>结构样本</span><b>{dataset?.summary.models ?? '—'}</b></div><div><span>独立几何组</span><b>{dataset?.summary.groups ?? '—'}</b></div><div><span>结构族</span><b>{Object.keys(dataset?.summary.families ?? {}).length}</b></div><div><span>任务实例</span><b>{dataset?.summary.tasks.toLocaleString() ?? '—'}</b></div><div><span>目录零件</span><b>{dataset?.summary.catalogParts ?? '—'}</b></div><span className="dataset-tag">{release === 'research' ? 'Composition grammar · 研究开发集' : 'Public development · Grid v1'}</span></div>

    {(tab === 'data' || tab === 'task') && <main className="workbench">
      <aside className="catalog">
        <div className="section-title"><h2>模型集合</h2><span>{filtered.length}</span></div>
        <label className="release-select">数据版本<select aria-label="数据版本" value={release} onChange={e => setRelease(e.target.value as typeof release)}>
          <option value="pilot">初始 Pilot · 552</option><option value="research">组合语法 · 576 几何组</option></select></label>
        <label>结构族<select value={family} onChange={e => setFamily(e.target.value)}><option value="all">全部结构族</option>{Object.keys(dataset?.summary.families ?? {}).map(f => <option key={f}>{f}</option>)}</select></label>
        <label>数据划分<select value={split} onChange={e => setSplit(e.target.value)}><option value="all">全部划分</option>{['train', 'validation', 'test_id', 'test_ood'].map(s => <option key={s}>{s}</option>)}</select></label>
        <div className="sample-list">{filtered.map(m => <button key={m.id} aria-pressed={modelId === m.id} onClick={() => setModelId(m.id)}>
          <Box size={17} /><span><b>{m.family}</b><small>{m.parts} 块 · {m.id.slice(0, 6)}</small></span><i className={m.split}>{m.split.replace('test_', '')}</i>
        </button>)}</div>
      </aside>
      <section className="main-area">
        <div className="heading"><div><span className="eyebrow">{tab === 'data' ? 'STRUCTURE EXPLORER' : 'TASK INSPECTOR'}</span><h2>{tab === 'data' ? model?.family ?? '加载结构' : LABELS[kind]}</h2></div>
          {tab === 'data' && <button className="command primary" onClick={() => setTab('task')}><FlaskConical size={15} />进入评测</button>}</div>
        {tab === 'data' && model && <>
          <Scene parts={model.structure.parts} />
          <div className="model-facts"><span>几何组 <code>{model.group}</code></span><span>{model.split}</span><span>{model.provenance.license}</span></div>
          <p className="description">{model.description}</p>
          {release === 'research' && <details><summary>连接端口与独立检查</summary><p className="description">{model.portsSource}</p>
            <pre>{JSON.stringify({ certificate: model.certificate, ports: model.ports ?? '未安装上游目录' }, null, 2)}</pre></details>}
          <div className="task-grid">{TASKS.map(k => <button key={k} onClick={() => { setKind(k); setTab('task'); }}><span>{LABELS[k]}</span><small>{k}</small><ArrowUpRight size={14} /></button>)}</div>
        </>}
        {tab === 'task' && <>
          {release === 'research' && <label>输入信息条件<select aria-label="输入信息条件" value={condition} onChange={e => setCondition(e.target.value)}>
            <option value="ordinary">普通多视图 / 任务默认输入</option><option value="layers">逐层检查图（额外信息）</option><option value="symbolic">符号参考（诊断上界）</option></select></label>}
          <div className="task-switch">{TASKS.map(k => <button key={k} aria-pressed={kind === k} onClick={() => setKind(k)}>{LABELS[k]}</button>)}</div>
          {loading && <div className="loading">生成任务视图…</div>}
          {task && <><div className="task-prompt"><span className="eyebrow">MODEL INPUT</span><p>{task.prompt}</p></div>
            {!!task.images?.length && <div className="observation-grid">{task.images.map((src, i) => <figure key={src + i}><img src={src} alt={task.imageTitles[i]} /><figcaption>{task.imageTitles[i]}</figcaption></figure>)}</div>}
            <details open><summary><Code2 size={14} />输入结构与约束</summary><pre>{JSON.stringify(task.input, null, 2)}</pre></details>
            <div className="submission"><div className="section-title"><h2>模型输出 / 人工练习</h2><span>JSON</span></div>
              <textarea aria-label="评测答案 JSON" rows={12} spellCheck={false} value={answer} onChange={e => setAnswer(e.target.value)} />
              <button className="command primary" onClick={() => void submit()}><Send size={15} />提交并评分</button>
              {verdict && <div className="verdict" role="status"><strong>{verdict.metrics.success ? 'PASS' : 'FAIL'}</strong><span>{verdict.issues.join(' · ')}</span><pre>{JSON.stringify(verdict.metrics, null, 2)}</pre></div>}
            </div>
          </>}
        </>}
      </section>
      <aside className="run-controls"><div className="section-title"><h2>模型运行</h2><span>SMOKE</span></div>
        <label>评测模式<select aria-label="评测模式" value={mode} disabled={release === 'research'} onChange={e => setMode(e.target.value as Mode)}><option value="one-shot">单次提交 · 主榜</option><option value="validator-once">一次合法性反馈 · 辅助榜</option></select></label>
        <fieldset><legend>模型</legend>{status?.models.map(m => <label className="check" key={m.id}><input type="checkbox" checked={paidModels.includes(m.id)}
          onChange={e => setPaidModels(previous => e.target.checked ? [...previous, m.id] : previous.filter(id => id !== m.id))} />{m.label}</label>)}</fieldset>
        <dl><dt>任务覆盖</dt><dd>8 个维度</dd><dt>每个模型</dt><dd>{release === 'research' ? '56 个配对条件' : '16 个样本'}</dd><dt>划分</dt><dd>ID + OOD</dd><dt>控制</dt><dd>无机器人</dd></dl>
        <button className="command dark" disabled={!status?.keyPresent || status.locked || status.budget.uncertain || !paidModels.length} onClick={() => dialog.current?.showModal()}><Play size={15} />运行付费评测</button>
        <div className="rail-note"><ShieldCheck size={17} /><span>one-shot / assisted 分榜</span></div>
        <a className="legacy" href="http://127.0.0.1:5174">CARE-mini 交互场 <ArrowUpRight size={13} /></a>
      </aside>
    </main>}
    {tab === 'result' && <main className="results"><div className="heading"><div><span className="eyebrow">MODEL EVALUATION</span><h2>多维度评测结果</h2></div><span className="dataset-tag">不合并主榜与辅助榜</span></div>
      {!runs.length && <p className="empty">暂无模型结果</p>}
      {runs.map(r => <section className="result-section" key={r.id}><div className="run-heading"><code>{r.id}</code><span>{r.status} · {r.mode} · {r.representation} · ${r.cost.toFixed(5)}</span>
        <button className="command" onClick={() => void api<RunDetail>(`/api/runs/${r.id}`).then(d => { setDetail(d); setCaseIndex(0); })}><Eye size={15} />逐例查看</button>
        <a className="command" href={`/api/runs/${r.id}/report`}><Download size={15} />报告</a></div>
        <div className="table-wrap"><table><thead><tr><th>模型</th><th>任务</th><th>n</th><th>错误</th><th>成功率</th><th>格式率</th><th>合法率</th><th>费用</th></tr></thead><tbody>
          {r.rows.map(x => <tr key={x.model + x.kind + (x.condition ?? '')}><td>{x.model}</td><td>{LABELS[x.kind]}{x.condition ? ` · ${x.condition}` : ''}</td><td>{x.n}</td><td>{x.errors}</td><td>{pct(x.metrics.success)}</td><td>{pct(x.metrics.format)}</td><td>{pct(x.metrics.valid)}</td><td>${x.cost.toFixed(5)}</td></tr>)}
        </tbody></table></div></section>)}
      {detail && <section className="case-detail"><div className="section-title"><h2>原始观测与响应</h2><button className="icon" title="关闭逐例详情" onClick={() => setDetail(null)}><X size={17} /></button></div>
        <select aria-label="结果样本" value={caseIndex} onChange={e => setCaseIndex(Number(e.target.value))}>{detail.results.map((r, i) => <option key={r.taskId + r.model} value={i}>{r.model} · {r.kind} · {r.split} · {r.verdict.metrics.success ? 'PASS' : 'FAIL'}</option>)}</select>
        {selectedCase && <TraceInspector key={`${detail.id}:${caseIndex}`} runId={detail.id} caseIndex={caseIndex} />}
      </section>}
    </main>}
    {tab === 'training' && <TrainingPanel />}
    {tab === 'review' && <ReviewPanel token={status?.token ?? ''} />}
    {tab === 'casebank' && <CasebankPanel token={status?.token ?? ''} />}
    {tab === 'study' && <StudyPanel />}
    {tab === 'protocol' && <main className="protocol"><span className="eyebrow">{VERSION} · 初始协议，研究版按结果条件单列</span><h2>协议与指标</h2><div className="table-wrap"><table><thead><tr><th>维度</th><th>输入</th><th>主评分</th></tr></thead><tbody>
      {TASKS.map((k, i) => <tr key={k}><td>{LABELS[k]}</td><td>{['孤立零件 RGB','完整结构程序','组装图 + 逐层图 + BOM','文字 + 占用体积约束','部分结构 + 参考图','结构 + 改色/增删指令','目标 + 装配/拆解方向','错误结构 + 参考图'][i]}</td><td>{['型号/颜色/studs','关系字段正确率','Part / BOM / Edge F1','合法性 + 体积 IoU','复原 + 原结构保持','目标正确 + 非目标保持','逐步合法性 + 完整性','定位 F1 + 复原'][i]}</td></tr>)}
    </tbody></table></div><dl className="rules"><dt>结构</dt><dd>25 类规则砖/板，整数 stud/plate 网格，四向 yaw；支持绝对与相对程序。</dd><dt>数据</dt><dd>初始版552个配色样本、138几何组；组合语法版576独立几何组。均为公开程序化开发集，不是人工设计资产。</dd><dt>主榜</dt><dd>固定输入、一次提交、无反馈；LLM/MLLM 按输入条件记录，不测试 VLA。</dd><dt>辅助榜</dt><dd>额外一次与目标无关的合法性检查；不是完整自主 agent。</dd><dt>划分</dt><dd>同几何组的所有派生任务不跨split；两版分别保持独立的整族留出协议。</dd><dt>物理边界</dt><dd>检查重叠、支撑与垂直通道，不模拟承重、扣合力或机器人。</dd><dt>研究边界</dt><dd>本地文本/结构LoRA实验见“训练与验证”；不是多模态微调。连接器导入也不等于所有类型已被验证。</dd></dl></main>}
    <footer><span>BrickAtlas Research Suite</span><span>Structured data · Multimodal evaluation · No robotics</span></footer>
    <dialog ref={dialog}><div className="section-title"><h2>确认付费运行</h2><button className="icon" title="关闭付费确认" onClick={() => dialog.current?.close()}><X size={17} /></button></div>
      <p>{paidModels.length} 个模型 × {release === 'research' ? 56 : 16} 个任务条件 · {mode}</p><p>累计费用上限 $4.50；当前已花 ${status?.budget.spent.toFixed(4)}。不明账单立即停止，不自动重试。</p>
      <div className="dialog-actions"><button className="command" onClick={() => dialog.current?.close()}>取消</button><button className="command primary" onClick={() => void paid()}><Play size={15} />确认并运行</button></div>
    </dialog>
  </div>;
}
createRoot(document.getElementById('root')!).render(<App />);
