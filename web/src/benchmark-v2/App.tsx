import { useEffect, useMemo, useRef, useState } from 'react';
import { AtlasScene } from '../scene/AtlasScene';
import { BrickModel } from '../model/BrickModel';
import { initialState, visibleInstances, type AtlasManifest, type ExplorerState } from '../model/types';
import { NumberedOverlay } from '../benchmark/NumberedOverlay';
import { replay } from '../benchmark/engine';
import type { Task } from '../benchmark/types';
import type { LDrawEntry } from '../benchmark/ldrawTypes';
import type { InternalBundle, PublicBundle } from '../../benchmark/suite/ldraw-v2/types';
import { score } from './scoring';
import { VERSION, STORAGE, decisions, download, emptyBatch, keyOf, makeRecord, mergeBatch, validateBatch,
  type ReviewBatch, type ReviewIndex } from './reviews';
import './style.css';

const base = '/benchmark/ldraw-v2/';
const query = new URLSearchParams(location.search), modelId = query.get('model');
const layers: Record<string, string> = { atomic: '原子识别', metacognitive: '证据判断', procedural: '步骤与编辑', 'graph-internal': '图内运算' };
async function json<T>(path: string, signal?: AbortSignal): Promise<T> {
  const r = await fetch(path, { signal });
  if (!r.ok || !r.headers.get('content-type')?.includes('json')) throw new Error(`无法读取 ${path}`);
  return r.json();
}
declare global {
  interface Window {
    __ldraw2?: () => { modelId: string; unitId: string; ready: boolean; labels: string[]; scene: ReturnType<AtlasScene['snapshot']> };
  }
}

export function App() {
  const [catalog, setCatalog] = useState<LDrawEntry[]>([]), [index, setIndex] = useState<ReviewIndex>();
  const [bundle, setBundle] = useState<InternalBundle>(), [publicBundle, setPublicBundle] = useState<PublicBundle>();
  const [manifest, setManifest] = useState<AtlasManifest>(), [ready, setReady] = useState(false);
  const [error, setError] = useState(''), [notice, setNotice] = useState('');
  const [view, setView] = useState<ExplorerState>({ ...initialState, grid: false, highlightStep: false });
  const [unitId, setUnitId] = useState(query.get('unit') ?? ''), [scope, setScope] = useState(query.get('unit')?.includes('-pair-') ? 'pair' : 'all');
  const [pendingOnly, setPendingOnly] = useState(false), [selected, setSelected] = useState('');
  const [isolation, setIsolation] = useState<'none' | 'operands' | 'selected'>('none');
  const [search, setSearch] = useState(''), [answer, setAnswer] = useState(''), [verdict, setVerdict] = useState('');
  const [frame, setFrame] = useState(0), [playing, setPlaying] = useState(false), [sourcePlaying, setSourcePlaying] = useState(false);
  const [batch, setBatch] = useState<ReviewBatch>(), [reviewer, setReviewer] = useState(''), [reason, setReason] = useState('');
  const [showOracle, setShowOracle] = useState(false), [frozenView, setFrozenView] = useState('views');
  const [storageBlocked, setStorageBlocked] = useState(false);
  const host = useRef<HTMLDivElement>(null), scene = useRef<AtlasScene | undefined>(undefined), overlay = useRef<NumberedOverlay | undefined>(undefined);
  const unit = index?.units.find(u => u.id === unitId && u.sourceId === modelId);
  const task = bundle?.tasks.find(t => t.id === unitId);
  const publicTask = publicBundle?.tasks.find(t => t.id === unitId);
  const operands = useMemo(() => unit?.operands.map(o => o.id) ?? [], [unit]);
  const records = batch?.records.filter(r => r.id === unitId) ?? [];
  const execution = useMemo(() => {
    if (task?.format !== 'actions') return null;
    try { return replay(task as Task, answer.trim() ? JSON.parse(answer).actionIds : []); }
    catch { return replay(task as Task, []); }
  }, [task, answer]);

  useEffect(() => {
    const c = new AbortController();
    json<LDrawEntry[]>(base + 'catalog.json', c.signal).then(setCatalog).catch(e => { if (!c.signal.aborted) setError(String(e)); });
    json<ReviewIndex>(base + 'review-index.json', c.signal).then(i => {
      if (i.version !== VERSION) throw new Error('题集版本不匹配');
      setIndex(i);
      try {
        const raw = localStorage.getItem(STORAGE);
        setBatch(raw ? validateBatch(JSON.parse(raw), i) : emptyBatch(i));
      } catch (e) {
        setBatch(emptyBatch(i)); setStorageBlocked(true);
        setNotice(`本地旧记录未覆盖：${String(e)}。请先导出备份，再使用新的浏览器存储空间审核。`);
      }
    }).catch(e => { if (!c.signal.aborted) setError(String(e)); });
    return () => c.abort();
  }, []);
  useEffect(() => {
    if (!modelId) return;
    const c = new AbortController();
    json<InternalBundle>(`${base}models/${encodeURIComponent(modelId)}.json`, c.signal).then(async b => {
      if (b.version !== VERSION || b.role !== 'internal-scoring-review') throw new Error('审核数据角色不匹配');
      const m = await json<AtlasManifest>(`/models/${b.entry.sourceModelId}/manifest.json`, c.signal);
      if (c.signal.aborted) return;
      setBundle(b); setManifest({ ...m, instructions: b.instructions });
    }).catch(e => { if (!c.signal.aborted) setError(String(e)); });
    json<PublicBundle>(`${base}inputs/${encodeURIComponent(modelId)}.json`, c.signal).then(setPublicBundle)
      .catch(e => { if (!c.signal.aborted) setError(String(e)); });
    return () => c.abort();
  }, []);
  useEffect(() => {
    if (!manifest || !host.current) return;
    const s = new AtlasScene(host.current, new BrickModel(manifest), {
      progress: () => {}, ready: () => setReady(true), error: setError,
      select: id => { setSelected(id ?? ''); setIsolation('none'); }, hover: () => {},
    });
    scene.current = s; overlay.current = new NumberedOverlay(host.current, s);
    return () => { overlay.current?.dispose(); s.dispose(); scene.current = undefined; delete window.__ldraw2; };
  }, [manifest]);
  useEffect(() => {
    const s = scene.current;
    if (!s || !bundle) return;
    let hiddenBrickIds: string[] = [];
    const stateFrame = execution?.frames[Math.min(frame, execution.frames.length - 1)];
    if (task?.input.editMode === 'visibility' && stateFrame)
      hiddenBrickIds = bundle.parts.filter(p => !stateFrame.activeModules.includes(p.id)).map(p => p.id);
    if (task?.input.editMode === 'source-window' && stateFrame) {
      const shown = new Set((task.input.sourceWindow as { instanceIds: string[] }[])
        .filter((_, i) => stateFrame.facts.includes(`done-${i + 1}`)).flatMap(r => r.instanceIds));
      hiddenBrickIds = bundle.parts.filter(p => !shown.has(p.id)).map(p => p.id);
    }
    const state = { ...view, selection: [], highlightedBrickIds: [], hiddenBrickIds,
      isolation: isolation === 'selected' && selected ? [selected] : isolation === 'operands' ? operands : null };
    s.setState(state, { animateAssembly: false });
    const visible = new Set(visibleInstances(s.manifest, state).map(p => p.instanceId));
    const ids = [...new Set([...(selected ? [selected] : []), ...operands])].filter(id => visible.has(id)).slice(0, 12);
    overlay.current?.setIds(ids);
    window.__ldraw2 = () => ({ modelId: bundle.entry.id, unitId, ready,
      labels: ids.map(id => bundle.parts.find(p => p.id === id)!.label), scene: s.snapshot() });
  }, [bundle, view, selected, isolation, operands, execution, frame, task, ready, unitId]);
  useEffect(() => {
    if (!playing || !execution) return;
    if (frame >= execution.frames.length - 1) { setPlaying(false); return; }
    const timer = setTimeout(() => setFrame(s => s + 1), 700);
    return () => clearTimeout(timer);
  }, [playing, execution, frame]);
  useEffect(() => {
    if (!sourcePlaying || !bundle?.instructions) return;
    if ((view.buildStep ?? 0) >= bundle.instructions.steps.length) { setSourcePlaying(false); return; }
    const timer = setTimeout(() => setView(v => ({ ...v, buildStep: (v.buildStep ?? 0) + 1 })), 600);
    return () => clearTimeout(timer);
  }, [sourcePlaying, bundle, view.buildStep]);

  function choose(id: string) {
    setUnitId(id); setSelected(''); setIsolation('none'); setAnswer(''); setVerdict(''); setShowOracle(false);
    setReason(''); setFrame(0); setPlaying(false); setSourcePlaying(false);
    setView(v => ({ ...v, explosion: 0, buildStep: null }));
    const url = new URL(location.href); id ? url.searchParams.set('unit', id) : url.searchParams.delete('unit');
    history.replaceState(null, '', url);
  }
  function persist(next: ReviewBatch) {
    if (!index || storageBlocked) throw new Error('本地记录需先备份，当前禁止覆盖');
    const valid = validateBatch(next, index);
    localStorage.setItem(STORAGE, JSON.stringify(valid)); setBatch(valid);
  }
  function save(decision: string) {
    if (!unit || !index || !batch) return;
    try {
      const r = makeRecord(unit, reviewer, decision, reason);
      persist({ ...batch, records: [...batch.records.filter(old => keyOf(old) !== keyOf(r)), r] });
      setNotice('已保存审核记录');
    } catch (e) { setNotice(String(e)); }
  }
  const units = index?.units.filter(u => u.sourceId === modelId && (scope === 'all' ? u.kind === 'task' :
    scope === 'required' ? u.kind === 'task' && u.required : u.kind === 'pair') &&
    (!pendingOnly || !batch?.records.some(r => r.id === u.id))) ?? [];
  const reviewed = new Set(batch?.records.map(r => r.id));
  const requiredReviewed = index?.units.filter(u => u.required && reviewed.has(u.id)).length ?? 0;
  const partList = bundle?.parts.filter(p => `${p.label} ${p.id}`.toLowerCase().includes(search.toLowerCase())) ?? [];
  const pos = units.findIndex(u => u.id === unitId);

  return <div className="v2-app">
    <header><a className="brand" href="/ldraw-v2.html">BRICKATLAS <b>LDRAW–2</b></a>
      <nav><a href={`${base}docs/main-v2.pdf`}>英文论文</a><a href={`${base}docs/supplement-v2.pdf`}>完整附录</a>
        <a href={`${base}docs/brickatlas-ldraw-v2-source.zip`}>论文源码</a><a href={`${base}release.json`}>数据记录</a></nav></header>
    <section className="intro"><div><span className="eyebrow">原始模型 · 实例对齐 · 分模块评测</span>
      <h1>{bundle ? `${bundle.entry.setNumber} · ${bundle.entry.nameZh}` : '积木基准与审核工作台'}</h1>
      <p>617 道题的自动 Oracle 检查已通过。视觉有效性与物理可靠性仍待人工核查；模型实验尚未运行。</p></div>
      <div className="metrics"><strong>{index?.summary.sources ?? '…'}<small>原始套装</small></strong>
        <strong>{index?.summary.tasks ?? '…'}<small>版本化题目</small></strong>
        <strong>{requiredReviewed}/{(index?.summary.humanQueue ?? 251) + (index?.summary.physicalQueue ?? 573)}<small>必要审核项目已记录</small></strong></div></section>
    <section className="review-tools">
      <button disabled={!batch} onClick={() => download(batch, 'brickatlas-ldraw2-feedback.json')}>导出反馈 JSON</button>
      <label className="file-button">导入反馈<input aria-label="导入反馈 JSON" type="file" accept=".json" onChange={async e => {
        const f = e.target.files?.[0]; if (!f || !index || !batch) return;
        try { persist(mergeBatch(batch, JSON.parse(await f.text()), index)); setNotice('已验证版本并合并反馈'); }
        catch (err) { setNotice(String(err)); }
        e.target.value = '';
      }} /></label>
      {storageBlocked && <button onClick={() => download({ raw: localStorage.getItem(STORAGE) }, 'ldraw2-local-backup.json')}>备份本地旧记录</button>}
      <span>需要核查：140 道视觉题 + 111 道其他标记题 + 573 对交叠候选</span>
    </section>
    {(error || notice) && <p className="message" role={error ? 'alert' : 'status'}>{error || notice}</p>}
    {!modelId ? <main className="library"><p>D1–D4 表示源模型零件规模，尚未标定题目难度。每件积木均可通过唯一编号单独查看。</p>
      <div className="cards">{catalog.map(m => <a className="card" key={m.id} href={`?model=${m.id}`}>
        <img src={`/benchmark/ldraw/thumbnails/${m.id}.png`} alt={`${m.name} 原始几何`} loading="lazy" />
        <div><span>{m.difficulty} · {m.setNumber}</span><h2>{m.nameZh}</h2><p>{m.name}</p>
          <small>{m.parts} 零件 · {m.tasks} 题 · {m.intersectionCandidates} 对待复核</small></div></a>)}</div></main> :
      <><div className="model-nav"><a href="/ldraw-v2.html">← 模型库</a><select aria-label="切换模型" value={modelId}
        onChange={e => { location.href = `?model=${e.target.value}`; }}>{catalog.map(m => <option value={m.id} key={m.id}>{m.setNumber} · {m.nameZh}</option>)}</select>
        <a href={`${base}inputs/${modelId}.json`}>公开模型输入</a><span>{bundle?.parts.length ?? '…'} 个原始零件</span></div>
      <main className="workspace">
        <aside className="inventory"><h2>实例编号</h2>
          <input aria-label="搜索零件编号" value={search} placeholder="B0001 / brick_000001" onChange={e => setSearch(e.target.value)} />
          <p className="muted">点编号定位，点隔离单独查看。</p>
          <div className="part-list">{partList.map(p => <div key={p.id}><button className={selected === p.id ? 'active' : ''}
            onClick={() => { setSelected(p.id); setIsolation('none'); }}>{p.label}</button>
            <button aria-label={`隔离 ${p.label}`} onClick={() => { setSelected(p.id); setIsolation('selected'); }}>隔离</button></div>)}</div>
          {bundle && <details><summary>来源与审核证据</summary><p>{bundle.entry.author} · {bundle.entry.license}</p>
            <a href={bundle.entry.sourceUrl} target="_blank" rel="noreferrer">原始来源</a>
            <p>连接定义覆盖 {(bundle.entry.connectorCoverage * 100).toFixed(1)}%。交叠候选不等于已确认缺陷。</p>
            <code>{bundle.entry.sourceHash}</code></details>}
          {selected && <details><summary>所选实例源属性</summary><pre>{JSON.stringify(bundle?.parts.find(p => p.id === selected), null, 2)}</pre></details>}
        </aside>
        <section className="viewer"><div className="canvas" ref={host} />
          <p className="viewer-status" role="status">{ready ? '真实几何已载入' : '正在载入真实几何…'}</p>
          <div className="view-tools">{(['perspective', 'front', 'side', 'top'] as const).map((v, i) =>
            <button key={v} onClick={() => setView(s => ({ ...s, view: v, revision: s.revision + 1 }))}>{['自由视角', '正视', '侧视', '俯视'][i]}</button>)}
            <button disabled={!operands.length} onClick={() => { setSelected(''); setIsolation('operands'); }}>隔离当前编号</button>
            <button disabled={!operands.length} onClick={() => scene.current?.focusNumberedInstances(operands)}>聚焦当前编号</button>
            <button onClick={() => { setIsolation('none'); setSelected(''); }}>显示全部</button>
            <button onClick={() => { choose(''); setView(v => ({ ...initialState, grid: false, highlightStep: false, revision: v.revision + 1 })); }}>重置模型</button></div>
          <label className="slider">展开 <input aria-label="展开程度" type="range" min="0" max=".9" step=".01" value={view.explosion}
            onChange={e => setView(s => ({ ...s, explosion: +e.target.value }))} /><output>{Math.round(view.explosion * 100)}%</output></label>
          <p className="muted">拖动旋转 · 滚轮缩放 · 右键平移。展开是观察工具，不能证明真实拆装路径。</p>
          {bundle?.instructions && <div className="replay"><button onClick={() => { choose(''); setView(v => ({ ...v, buildStep: 0 })); setSourcePlaying(true); }}>播放作者步骤</button>
            <button onClick={() => setSourcePlaying(false)}>暂停作者步骤</button><input type="range" aria-label="作者步骤" min="0" max={bundle.instructions.steps.length}
              value={view.buildStep ?? bundle.instructions.steps.length} onChange={e => { choose(''); setView(v => ({ ...v, buildStep: +e.target.value })); }} />
            <output>{view.buildStep ?? bundle.instructions.steps.length}/{bundle.instructions.steps.length}</output></div>}
          {publicTask?.visualInput && <details open className="frozen"><summary>该题实际图像与配对条件</summary>
            <select aria-label="图像条件" value={frozenView} onChange={e => setFrozenView(e.target.value)}>
              {Object.entries({ views: '标准隔离图', 'views-full': '完整场景', 'views-mask': '同相机隐藏背景', 'views-crop': '操作数裁剪', 'views-camera': '替代视角' })
                .map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>
            <a href={`${base}inputs/${frozenView}/${unitId}.png`} target="_blank" rel="noreferrer">
              <img src={`${base}inputs/${frozenView}/${unitId}.png`} alt={`${unitId} ${frozenView} 编号图`} /></a>
            <p className="muted">完整场景与隐藏背景使用同一相机；裁剪条件会改变放大比例。点图查看原始像素。</p></details>}
        </section>
        <aside className="task-panel"><h2>题目与交叠审核</h2>
          <select aria-label="审核队列" value={scope} onChange={e => { setScope(e.target.value); choose(''); }}>
            <option value="all">全部题目</option><option value="required">必须人工复核的题目</option><option value="pair">物理交叠候选</option></select>
          <label className="check"><input type="checkbox" checked={pendingOnly} onChange={e => setPendingOnly(e.target.checked)} />只显示尚无审核记录</label>
          <select size={6} className="queue" aria-label="选择审核项目" value={unitId} onChange={e => choose(e.target.value)}>
            {units.map(u => <option key={u.id} value={u.id}>{reviewed.has(u.id) ? '●' : '○'} {u.title} · {u.id}</option>)}</select>
          <div className="pagination"><button disabled={pos <= 0} onClick={() => choose(units[pos - 1].id)}>上一项</button>
            <small>{pos + 1}/{units.length}</small><button disabled={pos >= units.length - 1} onClick={() => choose(units[pos + 1].id)}>下一项</button></div>
          {unit ? <><code className="unit-id">{unit.id}</code><h3>{unit.title}</h3>
            {task && <><p className="question">{task.promptEn}</p><small>{layers[task.layer]} · {task.modality} · {task.format}</small></>}
            {unit.kind === 'pair' && <p>无已识别配对接口的网格交叠候选。请结合原始位置、零件形状与隔离视图判断。</p>}
            <div className="operands">{unit.operands.map(p => <button key={p.id} onClick={() => { setSelected(p.id); setIsolation('selected'); }}>{p.label}</button>)}</div>
            <p className="muted">{unit.reasons.join(' · ') || '该项无额外人工复核标记'}</p>
            {task && <><ul className="options">{task.options?.map(o => <li key={o.id}><b>{o.id}</b> {o.label}</li>)}</ul>
              <details><summary>模型收到的公开证据</summary><pre>{JSON.stringify(publicTask?.input, null, 2)}</pre></details>
              <label>答案 JSON<textarea aria-label="答案 JSON" value={answer} onChange={e => { setAnswer(e.target.value); setFrame(0); setPlaying(false); }} /></label>
              <div className="view-tools"><button onClick={() => { try { const r = score(task, JSON.parse(answer)); setVerdict(r.success ? '答案通过' : `答案未通过${r.validFormat ? '' : '：格式无效'}`); } catch { setVerdict('JSON 格式错误'); } }}>检查答案</button>
                <button onClick={() => { setAnswer(JSON.stringify(task.answer, null, 2)); setShowOracle(true); setFrame(0); }}>载入参考答案</button></div>
              {verdict && <p role="status">{verdict}</p>}
              {showOracle && <p className="muted">{task.evidenceDetail}</p>}
              {execution && <div className="replay"><button onClick={() => { if (frame >= execution.frames.length - 1) setFrame(0); setPlaying(v => !v); }}>{playing ? '暂停操作' : '播放操作'}</button>
                <input type="range" aria-label="操作回放" min="0" max={execution.frames.length - 1} value={frame} onChange={e => { setFrame(+e.target.value); setPlaying(false); }} />
                <output>{frame}/{execution.frames.length - 1} {execution.frames[frame]?.actionId ?? '初始状态'}</output>
                {execution.frames[frame]?.issue && <p>{execution.frames[frame].issue}</p>}</div>}</>}
            <section className="review-form"><h3>人工审核记录</h3>
              <label>审核人<input aria-label="审核人" value={reviewer} onChange={e => setReviewer(e.target.value)} /></label>
              <label>判定理由<textarea aria-label="判定理由" value={reason} onChange={e => setReason(e.target.value)} /></label>
              <div className="view-tools">{Object.entries(decisions[unit.kind]).map(([k, v]) =>
                <button key={k} disabled={storageBlocked} onClick={() => save(k)}>{v}</button>)}</div>
              {records.map(r => <div className="record" key={keyOf(r)}><b>{r.reviewer} · {r.decision}</b><p>{r.rationale}</p>
                <small>{r.updatedAt}</small><button onClick={() => { try { persist({ ...batch!, records: batch!.records.filter(old => keyOf(old) !== keyOf(r)) }); setNotice('已撤销该条本地记录'); } catch (e) { setNotice(String(e)); } }}>撤销此记录</button></div>)}
            </section></> : <p className="muted">选择题目或交叠候选后，场景会标出相关唯一编号。该工作台包含答案，仅供审核。</p>}
        </aside>
      </main></>}
    <footer>LDRAW–2 · 保留原始几何与坐标 · 当前不提供物理稳定性认证</footer>
  </div>;
}
