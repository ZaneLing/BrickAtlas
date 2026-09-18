import { useEffect, useMemo, useRef, useState } from 'react';
import { AtlasScene } from '../scene/AtlasScene';
import { BrickModel } from '../model/BrickModel';
import { initialState, visibleInstances, type AtlasManifest, type ExplorerState } from '../model/types';
import { NumberedOverlay } from './NumberedOverlay';
import { publicTask, type LDrawBundle, type LDrawEntry } from './ldrawTypes';
import { replay, score } from './engine';
import { downloadJson, importLDrawReviews, ldrawReviewBatch, loadLDrawReviews, makeLDrawReview, persistLDrawReviews } from './ldrawReviewStore';
import { loadReviews as loadHistoricalReviews, createReviewBatch as historicalBatch } from './reviewStore';
import './benchmark.css';
import './ldraw.css';

const root = import.meta.env.BASE_URL, base = `${root}benchmark/ldraw/`;
const layerNames = { atomic: '原子操作与识别', metacognitive: '连接证据与判断边界', procedural: '源步骤与编辑操作', integrative: '连接图综合推理' };
async function getJson<T>(url: string, signal?: AbortSignal): Promise<T> {
  const r = await fetch(url, { signal });
  if (!r.ok || !r.headers.get('content-type')?.includes('json')) throw new Error('当前版本没有这个模型。旧合成模型已撤下，请返回真实模型库。');
  return r.json();
}
function useCatalog() {
  const [entries, setEntries] = useState<LDrawEntry[]>([]), [error, setError] = useState('');
  useEffect(() => {
    const c = new AbortController();
    getJson<LDrawEntry[]>(`${base}catalog.json`, c.signal).then(setEntries).catch(e => { if (!c.signal.aborted) setError(String(e)); });
    return () => c.abort();
  }, []);
  return { entries, error };
}
export function BenchmarkLibrary({ compact = false }: { compact?: boolean }) {
  const { entries, error } = useCatalog();
  const [difficulty, setDifficulty] = useState('all'), [query, setQuery] = useState('');
  const shown = entries.filter(m => (difficulty === 'all' || m.difficulty === difficulty) && `${m.id} ${m.name} ${m.nameZh}`.toLowerCase().includes(query.toLowerCase()));
  return <section className="bench-library ldraw-library" id="benchmark">
    <div className="bench-heading"><div><small>BRICKATLAS · LDRAW-1</small><h2>真实积木源模型库</h2>
      <p>原始套装几何 · 逐件编号 · 按证据出题 · 人工逐题审核</p></div>
      <strong>{entries.length} 个原模型 / {entries.reduce((n, m) => n + m.tasks, 0)} 题</strong></div>
    <p className="ldraw-notice">旧合成数据集已撤下。当前保留原始 LDraw / OMR 零件、颜色与位置。连接覆盖和交叠候选均公开；尚未宣称全部模型通过物理稳定验证。</p>
    <div className="bench-controls"><select aria-label="模型规模筛选" value={difficulty} onChange={e => setDifficulty(e.target.value)}>
      <option value="all">全部规模</option>{['D1', 'D2', 'D3', 'D4'].map(v => <option key={v}>{v}</option>)}</select>
      <input aria-label="搜索基准模型" placeholder="套装编号 / 模型名称" value={query} onChange={e => setQuery(e.target.value)} />
      <a href={`${root}benchmark/review`}>人工审核台</a><a href={`${root}benchmark/docs/main.pdf`}>英文论文</a>
      <a href={`${root}benchmark/docs/supplement.pdf`}>英文附录</a><a href={`${base}release.json`}>来源与检查记录</a>
      {!compact && <a href={`${root}benchmark/docs/brickatlas-cvpr-source.zip`}>论文源码与图表</a>}
      {!compact && <a href={root}>项目首页</a>}</div>
    <small>D1 ≤150 件 · D2 151–400 件 · D3 401–1000 件 · D4 &gt;1000 件；这是规模分层，尚未标定题目难度。</small>
    {error && <p role="alert">{error}</p>}
    <div className="bench-grid">{shown.map(m => <a className="bench-card" key={m.id} href={`${root}benchmark/${m.id}`} data-bench-model={m.id}>
      <img src={`${base}thumbnails/${m.id}.png`} loading="lazy" alt={`${m.name} 原模型三维渲染`} />
      <div><span>{m.difficulty} · {m.setNumber}</span><h3>{m.nameZh}</h3><small>{m.name}</small><p>{m.parts} 零件 · {m.tasks} 题</p>
        <small>连接定义覆盖 {(m.connectorCoverage * 100).toFixed(1)}% · {m.intersectionCandidates} 对交叠待复核</small></div>
    </a>)}</div>
  </section>;
}
declare global {
  interface Window {
    __ldrawBench?: () => ReturnType<AtlasScene['snapshot']> & { modelId: string; taskId: string; labels: string[] };
    __ldrawCapture?: () => string;
    __ldrawSetView?: (view: ExplorerState['view']) => void;
  }
}
export function BenchmarkPage({ modelId }: { modelId?: string }) {
  const { entries } = useCatalog();
  const [bundle, setBundle] = useState<LDrawBundle | null>(null), [manifest, setManifest] = useState<AtlasManifest | null>(null);
  const [error, setError] = useState(''), [ready, setReady] = useState(false);
  const [view, setView] = useState<ExplorerState>({ ...initialState, grid: false, highlightStep: false });
  const [selected, setSelected] = useState(''), [isolated, setIsolated] = useState(false), [query, setQuery] = useState('');
  const [taskId, setTaskId] = useState(''), [layer, setLayer] = useState('all'), [filter, setFilter] = useState('all');
  const [program, setProgram] = useState(''), [result, setResult] = useState(''), [showAnswer, setShowAnswer] = useState(false);
  const [step, setStep] = useState(0), [playing, setPlaying] = useState(false), [sourcePlaying, setSourcePlaying] = useState(false);
  const [records, setRecords] = useState(loadLDrawReviews), [reason, setReason] = useState(''), [notice, setNotice] = useState('');
  const [advance, setAdvance] = useState(true);
  const host = useRef<HTMLDivElement>(null), scene = useRef<AtlasScene | null>(null), overlay = useRef<NumberedOverlay | null>(null);
  const current = bundle?.tasks.find(t => t.id === taskId);
  const currentIndex = bundle?.tasks.findIndex(t => t.id === taskId) ?? -1;
  const execution = useMemo(() => {
    if (!current || current.format !== 'actions') return null;
    try { return replay(current, program.trim() ? JSON.parse(program).actionIds : []); } catch { return null; }
  }, [current, program]);
  const references = useMemo(() => [...new Set([...(current?.references.map(r => r.id) ?? []), ...(selected ? [selected] : [])])], [current, selected]);
  useEffect(() => {
    if (!modelId) return;
    const abort = new AbortController(); setBundle(null); setManifest(null); setError(''); setReady(false);
    getJson<LDrawBundle>(`${base}models/${encodeURIComponent(modelId)}.json`, abort.signal).then(async b => {
      const m = await getJson<AtlasManifest>(`${root}models/${b.entry.sourceModelId}/manifest.json`, abort.signal);
      setBundle(b); setManifest({ ...m, instructions: b.instructions });
      const requested = new URLSearchParams(location.search).get('task');
      const review = new URLSearchParams(location.search).get('review') === '1';
      const task = b.tasks.find(t => t.id === requested) ?? (review ? b.tasks.find(t => !records[t.id]) : undefined);
      setTaskId(task?.id ?? '');
      setReason(task ? records[task.id]?.reason ?? '' : '');
      if (task) { const url = new URL(location.href); url.searchParams.set('task', task.id); history.replaceState(null, '', url); }
    }).catch(e => { if (!abort.signal.aborted) setError(String(e)); });
    return () => abort.abort();
  }, [modelId]);
  useEffect(() => {
    if (!manifest || !host.current) return;
    const s = new AtlasScene(host.current, new BrickModel(manifest), {
      progress: () => {}, ready: () => setReady(true), error: setError,
      select: id => { setSelected(id ?? ''); setIsolated(false); }, hover: () => {},
    });
    scene.current = s; overlay.current = new NumberedOverlay(host.current, s);
    window.__ldrawCapture = () => overlay.current!.capture();
    window.__ldrawSetView = v => setView(state => ({ ...state, view: v, revision: state.revision + 1 }));
    return () => { overlay.current?.dispose(); s.dispose(); scene.current = null; overlay.current = null;
      delete window.__ldrawCapture; delete window.__ldrawBench; delete window.__ldrawSetView; };
  }, [manifest]);
  useEffect(() => {
    const s = scene.current;
    if (!s || !bundle) return;
    let hiddenBrickIds: string[] = [];
    const frame = execution?.frames[Math.min(step, execution.frames.length - 1)];
    if (current?.input.editMode === 'visibility' && frame) hiddenBrickIds = bundle.parts.filter(p => !frame.activeModules.includes(p.id)).map(p => p.id);
    if (current?.input.editMode === 'source-window' && frame) {
      const shown = new Set((current.input.sourceWindow as Array<{ actionId: string; instanceIds: string[] }>)
        .filter((_, i) => frame.facts.includes(`done-${i + 1}`)).flatMap(s => s.instanceIds));
      hiddenBrickIds = bundle.parts.filter(p => !shown.has(p.id)).map(p => p.id);
    }
    const state = { ...view, selection: [], highlightedBrickIds: [],
      isolation: isolated ? (selected ? [selected] : references) : null, hiddenBrickIds };
    s.setState(state, { animateAssembly: false });
    const visible = new Set(visibleInstances(s.manifest, state).map(p => p.instanceId));
    const ids = (selected ? [selected, ...references.filter(id => id !== selected)] : references).filter(id => visible.has(id)).slice(0, 12);
    overlay.current?.setIds(ids);
    window.__ldrawBench = () => ({ ...s.snapshot(), modelId: bundle.entry.id, taskId,
      labels: ids.map(id => bundle.parts.find(p => p.id === id)!.label) });
  }, [bundle, view, references, isolated, selected, execution, step, ready, current, taskId]);
  useEffect(() => {
    if (!playing || !execution) return;
    if (step >= execution.frames.length - 1) { setPlaying(false); return; }
    const timer = setTimeout(() => setStep(n => n + 1), 800); return () => clearTimeout(timer);
  }, [playing, execution, step]);
  useEffect(() => {
    if (!sourcePlaying || !bundle?.instructions) return;
    if ((view.buildStep ?? 0) >= bundle.instructions.steps.length) { setSourcePlaying(false); return; }
    const timer = setTimeout(() => setView(s => ({ ...s, buildStep: (s.buildStep ?? 0) + 1 })), 650);
    return () => clearTimeout(timer);
  }, [sourcePlaying, bundle, view.buildStep]);
  function choose(id: string) {
    setTaskId(id); setSelected(''); setIsolated(false); setShowAnswer(false); setProgram(''); setResult('');
    setReason(records[id]?.reason ?? ''); setNotice(''); setStep(0); setPlaying(false); setSourcePlaying(false);
    setView(v => ({ ...v, buildStep: null, explosion: 0 }));
    const url = new URL(location.href); id ? url.searchParams.set('task', id) : url.searchParams.delete('task'); history.replaceState(null, '', url);
  }
  function save(decision: 'pass' | 'fail') {
    if (!current || !bundle) return;
    try {
      const record = makeLDrawReview(current, bundle.entry.sourceHash, decision, reason);
      const next = persistLDrawReviews({ ...loadLDrawReviews(), [current.id]: record }); setRecords(next);
      if (advance) {
        const nextTask = [...bundle.tasks.slice(currentIndex + 1), ...bundle.tasks.slice(0, currentIndex)].find(t => !next[t.id]);
        if (nextTask) choose(nextTask.id);
      }
      setNotice(`已保存：${decision === 'pass' ? '通过' : '不通过'}`);
    } catch (e) { setNotice(String(e)); }
  }
  if (!modelId) return <div className="bench-page"><BenchmarkLibrary /></div>;
  const partList = bundle?.parts.filter(p => `${p.label} ${p.id}`.toLowerCase().includes(query.toLowerCase())) ?? [];
  return <div className="bench-page bench-workspace">
    <header className="bench-topbar"><a href={`${root}benchmark`}>← 真实模型库</a><strong>LDRAW-1</strong>
      <select aria-label="切换基准模型" value={modelId} onChange={e => { location.href = `${root}benchmark/${e.target.value}`; }}>
        {entries.map(m => <option key={m.id} value={m.id}>{m.setNumber} · {m.nameZh}</option>)}</select><a href={`${root}benchmark/review`}>审核台</a>
      <a href={`${base}inputs/${modelId}.json`}>公开题目 JSON</a></header>
    {error && <p role="alert">{error}</p>}
    {!bundle && !error && <p role="status">正在读取原模型…</p>}
    {bundle && <div className="bench-workgrid">
      <aside className="bench-sidebar"><small>{bundle.entry.difficulty} · {bundle.entry.setNumber}</small><h1>{bundle.entry.nameZh}</h1>
        <p>{bundle.entry.name}</p><p>{bundle.parts.length} 个原始零件实例</p>
        <button onClick={() => { choose(''); setView(s => ({ ...initialState, grid: false, highlightStep: false, revision: s.revision + 1 })); }}>恢复完整源模型</button>
        <details><summary>来源与质量记录</summary><p>{bundle.entry.author} · {bundle.entry.license}</p>
          <a href={bundle.entry.sourceUrl} target="_blank" rel="noreferrer">原始来源</a> · <a href={`${base}sources/${modelId}.mpd`}>下载原 MPD</a>
          <p>连接定义覆盖 {(bundle.audit.connectorCoverage * 100).toFixed(1)}%；{bundle.audit.unsupported.length} 件未覆盖。</p>
          <p>识别图含 {bundle.audit.components.length} 个分量；场景独立物体和未识别接口均可能产生分量。</p>
          <p>{bundle.audit.nonMatingCollisionPairs.length} 对无已识别接口的网格交叠待复核。未测量承载力与动态稳定。</p>
          <small className="ldraw-hash">SHA256 {bundle.entry.sourceHash}</small>
          <a href={`${base}models/${modelId}.json`}>下载完整审核证据（含答案）</a></details>
        <h3>逐件编号</h3><input aria-label="搜索零件编号" placeholder="B0001 / brick_000001" value={query} onChange={e => setQuery(e.target.value)} />
        <p><small>编号指向几何中心；遮挡时可隔离查看。每件零件有唯一编号。</small></p>
        <div className="ldraw-inventory">{partList.map(p => <div className="bench-module" key={p.id}>
          <button className={selected === p.id ? 'selected' : ''} onClick={() => { setSelected(p.id); setIsolated(false); }}>{p.label}</button>
          <button aria-label={`隔离 ${p.label}`} onClick={() => { setSelected(p.id); setIsolated(true); }}>隔离</button></div>)}</div>
        {selected && <details><summary>所选编号的来源属性（审核用）</summary><pre>{JSON.stringify(bundle.parts.find(p => p.id === selected), null, 2)}</pre></details>}
      </aside>
      <main className="bench-view"><div className="bench-canvas ldraw-canvas" ref={host} />
        <div className="bench-viewtools">{(['perspective', 'front', 'side', 'top'] as const).map((v, i) =>
          <button key={v} onClick={() => setView(s => ({ ...s, view: v, revision: s.revision + 1 }))}>{['自由视角', '正视', '侧视', '俯视'][i]}</button>)}
          <button onClick={() => { setSelected(''); setIsolated(true); }}>隔离题目编号</button>
          <button onClick={() => scene.current?.focusNumberedInstances(references)} disabled={!references.length}>聚焦题目编号</button>
          <button onClick={() => setIsolated(false)}>取消隔离</button>
          <button onClick={() => scene.current?.focusNumberedInstances([selected])} disabled={!selected}>聚焦所选</button>
          <button disabled={!ready} onClick={() => { const a = document.createElement('a'); a.href = overlay.current!.capture(); a.download = `${modelId}-numbered.png`; a.click(); }}>下载带编号截图</button></div>
        {!ready && !error && <span className="ldraw-loading" role="status">正在载入真实 LDraw 几何…</span>}
        <div className="bench-explode"><label>展开查看 <input aria-label="基准展开程度" type="range" min="0" max=".9" step=".01" value={view.explosion}
          onChange={e => setView(s => ({ ...s, explosion: +e.target.value }))} /></label><output>{Math.round(view.explosion * 100)}%</output>
          <small>拖动旋转 · 滚轮缩放 · 右键平移；展开仅供观察，不表示物理拆装路径。</small></div>
        {bundle.instructions ? <div className="bench-replay"><button onClick={() => {
          choose(''); setView(s => ({ ...s, buildStep: 0 })); setSourcePlaying(true);
        }}>播放作者步骤</button><button onClick={() => setSourcePlaying(false)}>暂停</button>
          <input aria-label="作者步骤" type="range" min="0" max={bundle.instructions.steps.length} value={view.buildStep ?? bundle.instructions.steps.length}
            onChange={e => { setSourcePlaying(false); setTaskId(''); setView(s => ({ ...s, buildStep: +e.target.value })); }} />
          <output>{view.buildStep ?? bundle.instructions.steps.length}/{bundle.instructions.steps.length}</output>
          <small>作者 STEP 逐步显现，保持源坐标。</small></div> : <div className="bench-replay">源文件没有可用作者 STEP；未编造装配顺序。</div>}
      </main>
      <aside className="bench-tasks"><h2>逐题审核</h2>
        <p>{Object.values(records).filter(r => r.modelId === modelId && r.sourceHash === bundle.entry.sourceHash).length}/{bundle.tasks.length} 已审核</p>
        <button onClick={() => downloadJson(ldrawReviewBatch(records, entries.reduce((s, m) => s + m.tasks, 0)), 'ldraw1-reviews.json')}>导出本批次 JSON</button>
        <div className="bench-controls"><select aria-label="基准题型筛选" value={layer} onChange={e => setLayer(e.target.value)}><option value="all">全部能力层</option>
          {Object.entries(layerNames).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>
          <select aria-label="审核状态筛选" value={filter} onChange={e => setFilter(e.target.value)}><option value="all">全部状态</option><option value="pending">待审核</option><option value="pass">通过</option><option value="fail">不通过</option></select></div>
        <div className="bench-review-queue">{bundle.tasks.filter(t => (layer === 'all' || t.layer === layer) && (filter === 'all' || (records[t.id]?.decision ?? 'pending') === filter))
          .map(t => <button className={t.id === taskId ? 'current' : ''} key={t.id} onClick={() => choose(t.id)}>{t.title} · {records[t.id]?.decision ?? '待审核'}</button>)}</div>
        <div className="bench-review-nav"><button disabled={currentIndex <= 0} onClick={() => choose(bundle.tasks[currentIndex - 1].id)}>←</button>
          <span>{currentIndex + 1}/{bundle.tasks.length}</span><button disabled={currentIndex >= bundle.tasks.length - 1} onClick={() => choose(bundle.tasks[currentIndex + 1].id)}>→</button></div>
        {current ? <><h3>{current.title}</h3><p>{current.question}</p>
          <div className="ldraw-ref-list">{current.references.map(p => <button key={p.id} onClick={() => { setSelected(p.id); setIsolated(true); }}>{p.label}</button>)}</div>
          <small>{layerNames[current.layer]} · {current.modality}{current.references.length > 12 ? ' · 画面最多同时显示 12 个编号；点击编号可单独查看。' : ''}</small>
          {current.options?.map(o => <p className="bench-option" key={o.id}><b>{o.id}</b>{o.label}</p>)}
          <details><summary>公开输入与规则</summary><pre>{JSON.stringify(publicTask(current).input, null, 2)}</pre></details>
          <label>答案 JSON<textarea aria-label="基准答案 JSON" value={program} onChange={e => { setProgram(e.target.value); setStep(0); setPlaying(false); }} /></label>
          <div className="bench-controls"><button onClick={() => { try { const s = score(current, JSON.parse(program)); setResult(s.success ? '答案通过' : '答案未通过'); } catch { setResult('JSON 格式错误'); } }}>检查答案</button>
            <button onClick={() => { setProgram(JSON.stringify(current.answer, null, 2)); setShowAnswer(true); setStep(0); }}>载入参考答案</button></div>
          {result && <p role="status">{result}</p>}
          {showAnswer && <p>{current.evidenceDetail}</p>}
          {execution && <div className="bench-replay"><button onClick={() => { if (step >= execution.frames.length - 1) setStep(0); setPlaying(v => !v); }}>{playing ? '暂停' : '播放操作'}</button>
            <input aria-label="操作回放步骤" type="range" min="0" max={execution.frames.length - 1} value={step} onChange={e => { setStep(+e.target.value); setPlaying(false); }} />
            <span>{step}/{execution.frames.length - 1} · {execution.frames[step]?.actionId ?? '初始副本'} · {execution.frames[step]?.issue ?? ''}</span></div>}
          <section className={`bench-review-box ${records[current.id]?.decision ?? 'pending'}`}><strong>审核结论：{records[current.id]?.decision ?? '待审核'}</strong>
            <label>不通过理由 / 审核备注<textarea aria-label="审核意见" value={reason} onChange={e => setReason(e.target.value)} /></label>
            <label className="bench-auto-advance"><input type="checkbox" checked={advance} onChange={e => setAdvance(e.target.checked)} />保存后进入下一道待审核题</label>
            <div className="bench-review-decisions"><button onClick={() => save('pass')}>通过</button><button onClick={() => save('fail')}>不通过</button></div>
            {records[current.id] && <button onClick={() => { try { const next = { ...records }; delete next[current.id]; setRecords(persistLDrawReviews(next)); setNotice('已撤销'); } catch (e) { setNotice(String(e)); } }}>撤销本题审核</button>}
            {notice && <p role={notice.includes('必须') ? 'alert' : 'status'}>{notice}</p>}</section>
        </> : <p>选择一道题，画面会标出相关零件编号。编号按钮可单独隔离对应零件。</p>}
      </aside>
    </div>}
  </div>;
}
export function BenchmarkReviewDashboard() {
  const { entries, error } = useCatalog(), [records, setRecords] = useState(loadLDrawReviews), [notice, setNotice] = useState('');
  const total = entries.reduce((sum, m) => sum + m.tasks, 0);
  const rows = Object.values(records).filter(r => entries.some(m => m.id === r.modelId && m.sourceHash === r.sourceHash));
  return <div className="bench-page bench-review-page"><header className="bench-topbar"><a href={`${root}benchmark`}>← 真实模型库</a><strong>LDraw-1 人工审核台</strong></header>
    <main className="bench-review-main"><h1>{entries.length} 个原模型 · {rows.length}/{total} 题已审核</h1>
      <p>通过 {rows.filter(r => r.decision === 'pass').length} · 不通过 {rows.filter(r => r.decision === 'fail').length} · 待审核 {total - rows.length}</p>
      <div className="bench-controls"><button onClick={() => downloadJson(ldrawReviewBatch(Object.fromEntries(rows.map(r => [r.taskId, r])), total), 'ldraw1-reviews.json')}>导出本批次 JSON</button>
        <label>导入审核 JSON<input aria-label="导入审核 JSON" type="file" accept=".json" onChange={async e => {
          const f = e.target.files?.[0]; if (!f) return;
          try { setRecords(importLDrawReviews(await f.text())); setNotice('已导入合并'); } catch (e) { setNotice(String(e)); }
        }} /></label>
        <button onClick={() => downloadJson(historicalBatch(loadHistoricalReviews(), 6912), 'historical-hierarchy3-reviews.json')}>导出旧版审核记录</button></div>
      <p>新版审核独立保存。旧版人工意见保留，并可单独导出。</p>{(error || notice) && <p role="status">{error || notice}</p>}
      <div className="bench-review-table-wrap"><table className="bench-review-table"><thead><tr><th>规模</th><th>原模型</th><th>审核进度</th><th>检查记录</th><th>操作</th></tr></thead>
        <tbody>{entries.map(m => <tr key={m.id}><td>{m.difficulty}</td><td><strong>{m.setNumber} · {m.nameZh}</strong><small>{m.name}</small></td>
          <td>{rows.filter(r => r.modelId === m.id).length}/{m.tasks}</td><td>{m.intersectionCandidates} 对交叠待复核</td><td><a href={`${root}benchmark/${m.id}?review=1`}>逐题审核</a></td></tr>)}</tbody></table></div>
      <h2>不通过清单</h2><div className="bench-failure-list">{rows.filter(r => r.decision === 'fail').map(r => <a key={r.taskId} href={`${root}benchmark/${r.modelId}?task=${r.taskId}`}><span>{r.title}</span><strong>{r.reason}</strong></a>)}</div>
    </main></div>;
}
