import React, { useEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import {
  ArrowDownToLine, ArrowLeft, ArrowUpRight, Box, Check, ChevronRight, CircleAlert,
  ClipboardList, Code2, Eye, FlaskConical, Play, RotateCcw, Send, ShieldCheck, Unplug, X,
} from 'lucide-react';
import { CATALOG, COLORS } from '../shared/catalog';
import type { Action, EpisodeScore, Observation, TaskSummary, View } from '../shared/types';
import type { RunResult, TraceStep } from '../core/results';
import './styles.css';

interface Status {
  keyPresent: boolean;
  clientToken: string;
  running: boolean;
  models: { id: string; label: string }[];
  budget: { cap: number; spent: number; committed: number; calls: number; blocked: boolean };
  progress: { status: string; completed: number; total: number; error?: string };
}
interface ResultItem {
  id: string;
  status: string;
  episodes: number;
  plannedEpisodes: number;
  summaries: { model: string; protocol: string; n: number; successes: number; cost: number;
    anatomyF1: number | null; finalF1: number | null; errors: number }[];
}
type LiveObservation = Observation & { score: EpisodeScore | null };
const phaseLabels = { inspect: '观察与拆解', build: '蓝图交接 / 重建', done: '已提交' };
const feedbackLabels: Record<string, string> = {
  ready: '准备就绪', accepted: '动作已执行', handoff: '蓝图已交接',
  submitted: '已提交评分', blocked_above: '上方有遮挡，无法拆卸',
  unsupported: '剩余结构缺少支撑', overlap: '砖体重叠', no_inventory: '库存不足',
  not_observed: '目标不在已观察集合内', inspection_disabled: '被动协议禁止拆解',
  invalid_blueprint: '蓝图格式无效', invalid_action: '动作格式无效',
  budget_exhausted: '动作预算已用尽', invalid_part: '零件或坐标无效',
};
const views: { id: View; label: string }[] = [
  { id: 'iso', label: '斜视' }, { id: 'top', label: '俯视' },
  { id: 'front', label: '前视' }, { id: 'back', label: '后视' },
];
async function api<T>(path: string, token?: string, body?: unknown): Promise<T> {
  const response = await fetch(path, body === undefined ? undefined : {
    method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Benchmark-Client': token ?? '' },
    body: JSON.stringify(body),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error ?? 'Request failed');
  return data as T;
}
function FrameCanvas({ url, onView }: { url?: string; onView?: (view: View) => void }) {
  const canvas = useRef<HTMLCanvasElement>(null);
  const down = useRef<number | null>(null);
  useEffect(() => {
    if (!url) return;
    const abort = new AbortController();
    void fetch(url, { signal: abort.signal }).then(r => r.blob()).then(createImageBitmap).then(bitmap => {
      if (!abort.signal.aborted) canvas.current?.getContext('2d')?.drawImage(bitmap, 0, 0, 640, 480);
      bitmap.close();
    }).catch(() => {});
    return () => abort.abort();
  }, [url]);
  return <canvas ref={canvas} width={640} height={480} className="scene-canvas"
    aria-label="积木模型三维视图" role="img"
    onPointerDown={e => { down.current = e.clientX; }}
    onPointerUp={e => {
      if (down.current !== null && Math.abs(e.clientX - down.current) > 45) {
        onView?.(e.clientX > down.current ? 'back' : 'front');
      }
      down.current = null;
    }}
    onPointerCancel={() => { down.current = null; }} />;
}

function App() {
  const [status, setStatus] = useState<Status | null>(null);
  const [tasks, setTasks] = useState<TaskSummary[]>([]);
  const [taskId, setTaskId] = useState('');
  const [protocol, setProtocol] = useState<'active' | 'passive'>('active');
  const [session, setSession] = useState('');
  const [obs, setObs] = useState<LiveObservation | null>(null);
  const [tab, setTab] = useState<'lab' | 'results' | 'protocol'>('lab');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [selected, setSelected] = useState('');
  const [predict, setPredict] = useState({ newlyVisible: 0, components: 1 });
  const [draft, setDraft] = useState('{\n  "version": 1,\n  "parts": []\n}');
  const [part, setPart] = useState({ partId: '3958', color: 'gray', x: 0, y: 0, z: 0, turn: 0 });
  const [models, setModels] = useState(['openai/gpt-4.1-mini', 'google/gemini-2.5-flash']);
  const [results, setResults] = useState<ResultItem[]>([]);
  const [run, setRun] = useState<RunResult | null>(null);
  const [episodeIndex, setEpisodeIndex] = useState(0);
  const [stepIndex, setStepIndex] = useState(0);
  const confirm = useRef<HTMLDialogElement>(null);
  const [events, setEvents] = useState<{ action: string; feedback: string }[]>([]);

  useEffect(() => {
    let live = true;
    const refresh = async () => {
      try {
        const data = await api<Status>('/api/status');
        if (live) setStatus(data);
        const list = await api<ResultItem[]>('/api/results');
        if (live) setResults(list);
      } catch (e) { if (live) setError((e as Error).message); }
    };
    void refresh();
    void api<TaskSummary[]>('/api/tasks').then(items => {
      if (live) { setTasks(items); setTaskId(items[0]?.id ?? ''); }
    }).catch(e => setError(e.message));
    const interval = setInterval(() => void refresh(), 3000);
    return () => { live = false; clearInterval(interval); };
  }, []);

  const start = async () => {
    if (!status) return;
    setBusy(true); setError('');
    try {
      const data = await api<{ id: string; observation: LiveObservation }>('/api/sessions', status.clientToken, { taskId, protocol });
      setSession(data.id); setObs(data.observation); setSelected(''); setEvents([]);
      setDraft('{\n  "version": 1,\n  "parts": []\n}');
    } catch (e) { setError((e as Error).message); }
    finally { setBusy(false); }
  };
  const initialized = useRef(false);
  useEffect(() => {
    if (status && taskId && !initialized.current) {
      initialized.current = true;
      void start();
    }
  }, [status?.clientToken, taskId]);
  const act = async (action: Action) => {
    if (!status || !session || busy) return;
    setBusy(true); setError('');
    try {
      const data = await api<LiveObservation>(`/api/sessions/${session}/actions`, status.clientToken, action);
      setObs(data);
      setEvents(value => [...value, { action: action.type, feedback: data.feedback }]);
      if (action.type === 'detach') setSelected('');
    } catch (e) { setError((e as Error).message); }
    finally { setBusy(false); }
  };
  const sendBlueprint = () => {
    try { void act({ type: 'blueprint', blueprint: JSON.parse(draft) }); }
    catch { setError('蓝图不是有效 JSON'); }
  };
  const loadRun = async (id: string) => {
    try {
      setRun(await api<RunResult>(`/api/results/${id}`)); setEpisodeIndex(0); setStepIndex(0);
    } catch (e) { setError((e as Error).message); }
  };
  const paid = async () => {
    if (!status) return;
    confirm.current?.close();
    try {
      await api('/api/pilot', status.clientToken, { confirmPaid: true, models });
      setStatus({ ...status, running: true, progress: { status: 'running', completed: 0, total: models.length * 6 } });
      setTab('results');
    } catch (e) { setError((e as Error).message); }
  };
  const episode = run?.episodes[episodeIndex];
  const trace: TraceStep | undefined = episode?.trace[stepIndex];
  const canAct = !!obs && obs.phase !== 'done' && !busy;

  return <div className="app">
    <header className="masthead">
      <a href="http://127.0.0.1:5173" className="brand" title="返回 Brick Atlas"><Box size={22} /><span>Brick Atlas</span><ArrowUpRight size={14} /></a>
      <span className="separator" />
      <div className="page-title"><h1>模型测试场</h1><span>CARE-mini v1</span></div>
      <div className="connection"><i className={status?.keyPresent ? 'online' : ''} />{status?.keyPresent ? 'OpenRouter 已连接' : 'OpenRouter 未配置'}</div>
    </header>
    <div className="topbar">
      <nav aria-label="测试场导航">
        <button className={tab === 'lab' ? 'active' : ''} onClick={() => setTab('lab')}><FlaskConical size={16} />测试场</button>
        <button className={tab === 'results' ? 'active' : ''} onClick={() => setTab('results')}><ClipboardList size={16} />试验结果</button>
        <button className={tab === 'protocol' ? 'active' : ''} onClick={() => setTab('protocol')}><ShieldCheck size={16} />协议与边界</button>
      </nav>
      <div className="spend"><span>累计 API 费用</span><strong>${(status?.budget.spent ?? 0).toFixed(4)}</strong><small>/ $4.50</small></div>
    </div>
    {error && <div className="error" role="alert"><CircleAlert size={16} />{error}<button className="icon" title="关闭错误" onClick={() => setError('')}><X size={16} /></button></div>}
    {status?.budget.blocked && <div className="error" role="alert">存在未核账请求，付费运行已锁定。</div>}

    {tab === 'lab' && <main className="workspace">
      <aside className="task-rail">
        <div className="section-head"><h2>任务集</h2><span>PUBLIC PILOT</span></div>
        <div className="task-list">{tasks.map((task, index) => <button key={task.id}
          className={`task ${taskId === task.id ? 'chosen' : ''}`} onClick={() => { setTaskId(task.id); }}
          aria-pressed={taskId === task.id}>
          <span className="task-number">{String(index + 1).padStart(2, '0')}</span>
          <span><b>{task.title}</b><small>{task.parts} 块 · sealed-box</small></span><ChevronRight size={14} />
        </button>)}</div>
        <fieldset className="protocol-picker"><legend>观察协议</legend>
          <label><input type="radio" checked={protocol === 'active'} onChange={() => setProtocol('active')} />Active</label>
          <label><input type="radio" checked={protocol === 'passive'} onChange={() => setProtocol('passive')} />Passive</label>
        </fieldset>
        <button className="command primary full" disabled={busy || !taskId} onClick={() => void start()}><Play size={15} />{session ? '重置任务' : '进入任务'}</button>
        <div className="rail-divider" />
        <div className="section-head"><h2>模型试验</h2><span>SMALL BATCH</span></div>
        <div className="model-options">{status?.models.map(model => <label key={model.id}>
          <input type="checkbox" checked={models.includes(model.id)} disabled={status.running}
            onChange={e => setModels(prev => e.target.checked ? [...prev, model.id] : prev.filter(id => id !== model.id))} />
          <span>{model.label}</span>
        </label>)}</div>
        <div className="run-spec"><span>每模型</span><b>4 active + 2 passive</b><span>付费上限</span><b>$4.50 / campaign</b></div>
        <button className="command full dark" disabled={!models.length || !status?.keyPresent || status.running || status.budget.blocked}
          onClick={() => confirm.current?.showModal()}><Play size={15} />{status?.running ? '试验运行中' : '运行付费 Pilot'}</button>
        <div className="rail-foot"><ShieldCheck size={15} /><span>独立模块 · 原工作区未改动</span></div>
      </aside>

      <section className="stage">
        <div className="stage-heading"><div><span className="eyebrow">WORKBENCH</span><h2>{obs ? phaseLabels[obs.phase] : '密封结构实验'}</h2></div>
          <div className="mode-badge">{obs?.protocol ?? protocol}</div></div>
        <div className="phase-strip">{['观察 / 拆解', '蓝图交接', '重建 / 恢复', '评分'].map((label, index) =>
          <span key={label} className={obs && (obs.phase === 'inspect' ? index === 0 : obs.phase === 'build' ? index === 2 : index === 3) ? 'current' : ''}>
            <i>{index + 1}</i>{label}
          </span>)}</div>
        <div className={`scene ${!obs ? 'empty' : ''}`}>
          {obs ? <FrameCanvas url={obs.imageUrl} onView={view => { if (canAct) void act({ type: 'look', view }); }} />
            : <div className="empty-state"><Box size={60} strokeWidth={1} /><h3>待启动</h3><span>8 块积木 / 有限观察 / 隐藏结构</span></div>}
          {busy && <div className="rendering" role="status">渲染中</div>}
        </div>
        <div className="scene-toolbar">
          <div className="segmented" aria-label="镜头视角">{views.map(v => <button key={v.id} title={v.label} disabled={!canAct}
            className={obs?.view === v.id ? 'selected' : ''} onClick={() => void act({ type: 'look', view: v.id })}><Eye size={14} />{v.label}</button>)}</div>
          <span className="remaining">剩余决策 <b>{obs?.remainingActions ?? 14}</b></span>
          <button className="icon" title="重置任务" disabled={busy || !session} onClick={() => void start()}><RotateCcw size={17} /></button>
        </div>
        <div className="feedback" aria-live="polite"><Check size={14} />{feedbackLabels[obs?.feedback ?? 'ready'] ?? obs?.feedback}</div>
        {obs?.score && <div className="score-band">
          <div><span>全流程</span><strong>{obs.score.lifecycleSuccess ? 'PASS' : 'FAIL'}</strong></div>
          <div><span>解剖 F1</span><strong>{(obs.score.anatomy.partF1 * 100).toFixed(1)}%</strong></div>
          <div><span>最终 F1</span><strong>{(obs.score.construction.partF1 * 100).toFixed(1)}%</strong></div>
          <div><span>非法动作</span><strong>{obs.score.invalidActions}</strong></div>
        </div>}
        <div className="event-log"><div className="section-head"><h2>动作记录</h2><span>{events.length} EVENTS</span></div>
          {events.length ? events.slice(-5).map((event, i) => <div className="event" key={events.length - 5 + i}><code>{event.action}</code><span>{feedbackLabels[event.feedback] ?? event.feedback}</span></div>)
            : <span className="muted">暂无动作</span>}
        </div>
      </section>

      <aside className="action-rail">
        <div className="section-head"><h2>可见零件</h2><span>{obs?.visible.length ?? 0}</span></div>
        <div className="visible-list">{obs?.visible.map(p => <button key={p.id} disabled={!canAct}
          className={selected === p.id ? 'selected' : ''} onClick={() => setSelected(p.id)}>
          <i style={{ background: COLORS[p.color] }} /><code>{p.id}</code><span>{p.partId}</span><small>{p.color}</small>
        </button>)}</div>
        <div className="prediction"><label>新增可见<input aria-label="预计新增可见零件数" type="number" min={0} max={32} value={predict.newlyVisible}
          onChange={e => setPredict({ ...predict, newlyVisible: Number(e.target.value) })} /></label>
          <label>连通分量<input aria-label="预计连通分量" type="number" min={0} max={32} value={predict.components}
            onChange={e => setPredict({ ...predict, components: Number(e.target.value) })} /></label></div>
        <button className="command full" disabled={!canAct || !selected} onClick={() => void act({ type: 'detach', id: selected, predict })}><Unplug size={15} />预测并拆卸</button>
        <div className="rail-divider" />
        {(!obs || obs.phase === 'inspect') ? <>
          <div className="section-head"><h2>Blueprint IR</h2><Code2 size={15} /></div>
          <textarea aria-label="蓝图 JSON" spellCheck={false} value={draft} onChange={e => setDraft(e.target.value)} rows={11} />
          <button className="command full" disabled={!canAct} onClick={sendBlueprint}><Send size={15} />提交蓝图</button>
        </> : <>
          <div className="section-head"><h2>重建操作</h2><Box size={15} /></div>
          <label className="field">零件<select value={part.partId} onChange={e => setPart({ ...part, partId: e.target.value })}>{Object.entries(CATALOG).map(([id, p]) => <option key={id} value={id}>{id} · {p.name}</option>)}</select></label>
          <label className="field">颜色<select value={part.color} onChange={e => setPart({ ...part, color: e.target.value })}>{Object.keys(COLORS).map(c => <option key={c}>{c}</option>)}</select></label>
          <div className="coordinates">{(['x', 'y', 'z'] as const).map(axis => <label key={axis}>{axis.toUpperCase()}<input aria-label={`放置 ${axis}`} type="number" value={part[axis]} min={axis === 'y' ? 0 : -8} max={16}
            onChange={e => setPart({ ...part, [axis]: Number(e.target.value) })} /></label>)}</div>
          <label className="field">朝向<select value={part.turn} onChange={e => setPart({ ...part, turn: Number(e.target.value) })}>
            {[0, 1, 2, 3].map(t => <option key={t} value={t}>{t * 90}°</option>)}</select></label>
          <button className="command full" disabled={!canAct} onClick={() => void act({ type: 'place', part: { ...part, turn: part.turn as 0 | 1 | 2 | 3 } })}><Box size={15} />放置</button>
          <button className="command full" disabled={!canAct || !obs.blueprint} onClick={() => void act({ type: 'build', parts: obs.blueprint!.parts })}><Play size={15} />执行蓝图</button>
          <details><summary>交接蓝图</summary><pre>{JSON.stringify(obs.blueprint, null, 2)}</pre></details>
        </>}
        <button className="command primary full" disabled={!canAct} onClick={() => void act({ type: 'finish' })}><ShieldCheck size={15} />结束并评分</button>
        <div className="rail-divider" /><div className="section-head"><h2>库存</h2><span>含干扰件</span></div>
        <div className="inventory">{obs?.inventory.filter(i => i.count > 0).map(p => <div key={`${p.partId}:${p.color}`}><i style={{ background: COLORS[p.color] }} /><code>{p.partId}</code><span>{p.color}</span><b>×{p.count}</b></div>)}</div>
      </aside>
    </main>}

    {tab === 'results' && <main className="results-page">
      <div className="results-heading"><div><span className="eyebrow">EVALUATION RUNS</span><h2>小规模试验结果</h2></div><span className="mode-badge">public pilot · 非正式排名</span></div>
      {status?.running && <div className="run-progress" role="status"><Play size={16} />运行中 <progress max={status.progress.total || 12} value={status.progress.completed} /><span>{status.progress.completed} / {status.progress.total || 'CLI'}</span></div>}
      {status?.progress.error && <div className="error">{status.progress.error}</div>}
      {!results.length && <div className="results-empty"><ClipboardList size={42} /><h3>暂无已保存的试验</h3></div>}
      {results.map(item => <section className="result-section" key={item.id}>
        <div className="run-heading"><code>{item.id}</code><span>{item.status} · {item.episodes}/{item.plannedEpisodes}</span>
          <button className="command" onClick={() => void loadRun(item.id)}><Eye size={15} />逐步回放</button>
          <a className="command" href={`/api/results/${item.id}/report`}><ArrowDownToLine size={15} />报告</a></div>
        <div className="table-scroll"><table><thead><tr><th>模型</th><th>协议</th><th>完成 n</th><th>全流程成功</th><th>解剖 F1</th><th>最终 F1</th><th>API 费用</th></tr></thead>
          <tbody>{item.summaries.map(row => <tr key={row.model + row.protocol}><td>{row.model}</td><td><span className={`protocol-tag ${row.protocol}`}>{row.protocol}</span></td><td>{row.n}{row.errors ? ` + ${row.errors} error` : ''}</td><td>{row.successes}/{row.n}</td><td>{row.anatomyF1 === null ? 'N/A' : `${(row.anatomyF1 * 100).toFixed(1)}%`}</td><td>{row.finalF1 === null ? 'N/A' : `${(row.finalF1 * 100).toFixed(1)}%`}</td><td>${row.cost.toFixed(5)}</td></tr>)}</tbody>
        </table></div>
      </section>)}
      {run && <section className="replay">
        <div className="section-head"><h2>Episode 回放</h2><button className="icon" title="关闭回放" onClick={() => setRun(null)}><X size={17} /></button></div>
        <label className="field">Episode<select value={episodeIndex} onChange={e => { setEpisodeIndex(Number(e.target.value)); setStepIndex(0); }}>{run.episodes.map((e, i) =>
          <option key={e.id} value={i}>{e.model} · {e.protocol} · {e.taskId} · {e.score.lifecycleSuccess ? 'PASS' : 'FAIL'}</option>)}</select></label>
        <div className="replay-grid"><div>
          <FrameCanvas url={trace ? `/api/results/${run.id}/${trace.image}` : episode ? `/api/results/${run.id}/${episode.finalImage}` : undefined} />
          <div className="playback"><button className="icon" title="前一动作" disabled={stepIndex === 0} onClick={() => setStepIndex(v => v - 1)}><ArrowLeft size={16} /></button>
            <input aria-label="回放步骤" type="range" min={0} max={Math.max(0, (episode?.trace.length ?? 1) - 1)} value={stepIndex} onChange={e => setStepIndex(Number(e.target.value))} />
            <span>{stepIndex + 1}/{episode?.trace.length ?? 0}</span><button className="icon" title="后一动作" disabled={stepIndex >= (episode?.trace.length ?? 1) - 1} onClick={() => setStepIndex(v => v + 1)}><ChevronRight size={16} /></button></div>
        </div><div className="trace-detail"><span className="eyebrow">{trace?.context ?? 'FINAL'}</span><h3>{trace?.action?.type ?? '无动作'}</h3><pre>{JSON.stringify(trace?.action, null, 2)}</pre>
          <dl><dt>环境反馈</dt><dd>{trace?.feedback}</dd><dt>费用</dt><dd>${trace?.response.cost.toFixed(6)}</dd><dt>Provider</dt><dd>{trace?.response.provider}</dd><dt>Generation</dt><dd>{trace?.response.id}</dd></dl></div></div>
      </section>}
    </main>}

    {tab === 'protocol' && <main className="protocol-page">
      <span className="eyebrow">CARE-MINI V1 / FROZEN PILOT</span><h2>协议与测量边界</h2>
      <dl className="protocol-facts">
        <dt>观察</dt><dd>640 × 480 RGB + 可见身份/颜色；不提供目标位姿。</dd>
        <dt>动作</dt><dd>look / detach / blueprint / place / build / finish</dd>
        <dt>网格</dt><dd>X/Z: 8 mm stud；Y: 3.2 mm plate；位置为砖体最小角。</dd>
        <dt>配额</dt><dd>14 次决策 · 48 次原子编辑 · 每批至多 12 块</dd>
        <dt>交接</dt><dd>同型号模型的新上下文；仅交接 Blueprint IR。</dd>
        <dt>连接</dt><dd>整数凸点对接、无重叠、下方支撑；只允许 +Y 拆卸。</dd>
        <dt>评分</dt><dd>多重集 Part F1 / Edge F1 / exact；ID 互换与 yaw 对称不扣分。</dd>
        <dt>费用</dt><dd>逐请求预留，usage.cost 核账；累计硬预算 $4.50；账单不明停止。</dd>
        <dt>不测</dt><dd>承重、扣合力、连续姿态、机器人控制、通用连接器。</dd>
        <dt>数据</dt><dd>一个结构族、4 个 Active 配置、2 个 Passive 配置；公开可复现 pilot。</dd>
        <dt>统计</dt><dd>样本少且共享结构族；不宣称模型排名、显著提升或超越既有基准。</dd>
      </dl>
    </main>}
    <footer><span>Brick Atlas · CARE-mini v1</span><span>Discrete connectivity · No force simulation</span></footer>
    <dialog ref={confirm} className="paid-dialog">
      <div className="section-head"><h2>确认付费试验</h2><button className="icon" title="取消" onClick={() => confirm.current?.close()}><X size={17} /></button></div>
      <p>{models.length} 个模型 · {models.length * 6} 个 episode</p>
      <dl><dt>已核账</dt><dd>${(status?.budget.spent ?? 0).toFixed(4)}</dd><dt>剩余可预留</dt><dd>${Math.max(0, 4.5 - (status?.budget.committed ?? 0)).toFixed(4)}</dd></dl>
      <p className="muted">本次会调用 OpenRouter。累计上限 $4.50；超时或账单不明将停止。</p>
      <div className="dialog-actions"><button className="command" onClick={() => confirm.current?.close()}>取消</button><button className="command primary" onClick={() => void paid()}><Play size={15} />确认并运行</button></div>
    </dialog>
  </div>;
}

createRoot(document.getElementById('root')!).render(<App />);
