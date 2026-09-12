import { useEffect, useMemo, useRef, useState } from 'react';
import { Play, Pause, SkipBack, SkipForward, ChevronLeft, ChevronRight, Download, AlertTriangle, Eye } from 'lucide-react';
import type { CaseTrace, TraceActor } from '../trace-types';
import type { Part, View } from '../shared';
import { traceViewer, type CameraPose } from './trace-viewer';
import './trace.css';

const ACTORS: Record<TraceActor, string> = { model: '模型', harness: 'Harness', environment: '执行器', evaluator: '裁判' };
const DIFF = { missing: '缺失', extra: '多余', color: '颜色', pose: '位姿' };
function TraceScenes({ trace, index, showEdges, showDiff }: { trace: CaseTrace; index: number; showEdges: boolean; showDiff: boolean }) {
  const first = useRef<HTMLCanvasElement>(null), second = useRef<HTMLCanvasElement>(null), third = useRef<HTMLCanvasElement>(null);
  const renderers = useRef<ReturnType<typeof traceViewer>[]>([]);
  const [view, setView] = useState<View>('iso');
  const frame = useMemo(() => [...trace.reference, ...trace.source, ...trace.output], [trace]);
  useEffect(() => {
    const canvases = [first, second, third];
    renderers.current = canvases.map((ref, index) => traceViewer(ref.current!, (pose: CameraPose) => {
      renderers.current.forEach((r, i) => { if (i !== index) r.setPose(pose); });
    }));
    return () => { renderers.current.forEach(r => r.dispose()); renderers.current = []; };
  }, []);
  useEffect(() => {
    const event = trace.events[index], current = trace.states[event.after] ?? [];
    const final = index === trace.events.length - 1;
    const warn = final && showDiff ? trace.differences.flatMap(d => d.actualId ? [d.actualId] : []) : [];
    const missing: Part[] = final && showDiff ? trace.reference.filter(p => trace.differences.some(d => d.kind === 'missing' && d.expectedId === p.id)) : [];
    const scenes = [trace.source, current, trace.reference];
    renderers.current.forEach((r, i) => r.update(scenes[i], frame,
      { warningIds: i === 1 ? warn : [], missing: i === 1 ? missing : [], edges: showEdges }));
  }, [trace, index, showEdges, showDiff, frame]);
  return <>
    <div className="trace-views">{(['iso', 'top', 'front', 'side'] as View[]).map((v, i) =>
      <button key={v} aria-pressed={view === v} title={`同步${['斜视', '俯视', '前视', '侧视'][i]}`}
        onClick={() => { setView(v); renderers.current.forEach(r => r.setView(v)); }}>
        <Eye size={14} />{['斜视', '俯视', '前视', '侧视'][i]}</button>)}
      <span>三视窗相机联动 · 事后回放</span></div>
    <div className="trace-scenes">
      {[['输入结构', first], [trace.evidence.outputMeaning === 'context-only' ? '题目上下文（非模型生成）' : '本事件后的结构', second], [trace.evidence.referenceIsExample ? '参考样例 · 非唯一答案' : '目标终态 · 裁判视图', third]].map(([label, ref], i) =>
        <figure key={i}><figcaption>{String(label)}</figcaption><canvas ref={ref as typeof first} width={640} height={480} aria-label={String(label)} /></figure>)}
    </div>
  </>;
}

export function TraceInspector({ runId, caseIndex, endpointOverride }: { runId: string; caseIndex: number; endpointOverride?: string }) {
  const [trace, setTrace] = useState<CaseTrace | null>(null);
  const [error, setError] = useState(''), [index, setIndex] = useState(0), [playing, setPlaying] = useState(false);
  const [showEdges, setShowEdges] = useState(false), [showDiff, setShowDiff] = useState(true), [inputOnly, setInputOnly] = useState(false);
  const endpoint = endpointOverride ?? `/api/runs/${runId}/cases/${caseIndex}/trace`;
  useEffect(() => {
    const abort = new AbortController();
    setTrace(null); setIndex(0); setPlaying(false); setError('');
    void fetch(endpoint, { signal: abort.signal }).then(async response => {
      const data = await response.json(); if (!response.ok) throw new Error(data.error); return data;
    }).then(data => { if (!abort.signal.aborted) setTrace(data); }).catch(e => { if (!abort.signal.aborted) setError(e.message); });
    return () => abort.abort();
  }, [endpoint]);
  useEffect(() => {
    if (!playing || !trace) return;
    const timer = setInterval(() => setIndex(i => {
      if (i + 1 >= trace.events.length) { setPlaying(false); return i; } return i + 1;
    }), 700);
    const visibility = () => { if (document.hidden) setPlaying(false); };
    document.addEventListener('visibilitychange', visibility);
    return () => { clearInterval(timer); document.removeEventListener('visibilitychange', visibility); };
  }, [playing, trace]);
  if (error) return <div className="alert" role="alert">{error}</div>;
  if (!trace) return <div className="trace-loading" role="status">加载完整事件轨迹…</div>;
  const event = trace.events[index];
  const go = (n: number) => { setPlaying(false); setIndex(Math.max(0, Math.min(trace.events.length - 1, n))); };
  const failed = trace.events.findIndex(e => e.kind === 'reject' || e.kind === 'error'
    || e.kind === 'score' && typeof e.payload === 'object' && e.payload !== null
      && 'metrics' in e.payload && (e.payload as { metrics: { success: number } }).metrics.success === 0);
  return <section className="trace-inspector">
    <div className="trace-heading"><div><span className="eyebrow">AUDITABLE EVENT REPLAY</span><h2>全步骤可视化</h2></div>
      <a className="command" href={`${endpoint}${endpoint.includes('?') ? '&' : '?'}format=jsonl`}><Download size={15} />事件 JSONL</a></div>
    <div className="trace-facts"><span>{trace.events.length} 个事件</span><span>{trace.evidence.responseCount} 次真实模型响应</span>
      <span>{endpointOverride ? '未提供调用收据 · 离线回放' : `新增费用 $${trace.evidence.cost.toFixed(6)}`}</span>{trace.evidence.reusedFirstResponse && <span>首答复用 · 不重复计费</span>}
      <strong>{trace.evidence.scoreMatches ? '分数复算一致' : '版本不一致'}</strong></div>
    <div className="trace-mode"><label><input type="checkbox" checked={inputOnly} onChange={e => { setInputOnly(e.target.checked); setPlaying(false); }} />仅看模型原始输入</label>
      {!inputOnly && <><label><input type="checkbox" checked={showEdges} onChange={e => setShowEdges(e.target.checked)} />连接图</label>
        <label><input type="checkbox" checked={showDiff} onChange={e => setShowDiff(e.target.checked)} />最终差分</label></>}</div>
    {inputOnly ? <div className="trace-inputs"><p>{trace.input.prompt}</p><div className="observation-grid">{trace.frames.map((path, i) =>
      <figure key={path + i}><img src={path.startsWith('/api/') ? path : `/api/runs/${runId}/${path}`} alt={trace.input.imageTitles[i]} /><figcaption>{trace.input.imageTitles[i]}</figcaption></figure>)}</div>
      <pre>{JSON.stringify(trace.modelInput, null, 2)}</pre></div>
      : <TraceScenes key={`${runId}:${caseIndex}`} trace={trace} index={index} showEdges={showEdges} showDiff={showDiff} />}
    {!inputOnly && <><div className="trace-transport">
      <button className="icon" title="第一个事件" disabled={index === 0} onClick={() => go(0)}><SkipBack size={17} /></button>
      <button className="icon" title="上一个事件" disabled={index === 0} onClick={() => go(index - 1)}><ChevronLeft size={17} /></button>
      <button className="icon" title={playing ? '暂停回放' : '播放回放'} onClick={() => { if (index === trace.events.length - 1) setIndex(0); setPlaying(p => !p); }}>{playing ? <Pause size={17} /> : <Play size={17} />}</button>
      <input aria-label="事件时间轴" type="range" min={0} max={trace.events.length - 1} value={index} onChange={e => go(Number(e.target.value))} />
      <span>{index + 1} / {trace.events.length}</span>
      <button className="icon" title="下一个事件" disabled={index === trace.events.length - 1} onClick={() => go(index + 1)}><ChevronRight size={17} /></button>
      <button className="icon" title="最终事件" disabled={index === trace.events.length - 1} onClick={() => go(trace.events.length - 1)}><SkipForward size={17} /></button>
      <button className="icon" title="跳到失败事件" disabled={failed < 0} onClick={() => go(failed)}><AlertTriangle size={17} /></button>
    </div>
    <div className="trace-body"><div className="trace-event-list" aria-label="事件列表">{trace.events.map(e =>
      <button key={e.id} aria-pressed={index === e.id} className={`trace-event ${e.actor}`} onClick={() => go(e.id)}>
        <code>{String(e.id + 1).padStart(2, '0')}</code><span>{e.title}</span><small>{ACTORS[e.actor]}</small></button>)}</div>
      <div className="trace-event-detail"><div className={`actor-label ${event.actor}`}>{ACTORS[event.actor]} · {event.provenance === 'recorded' ? '原始记录' : '事后确定性派生'}</div>
        <h3>{event.title}</h3><pre>{JSON.stringify(event.payload, null, 2)}</pre><dl><dt>状态前</dt><dd>{event.before}</dd><dt>状态后</dt><dd>{event.after}</dd><dt>本事件费用</dt><dd>${event.cost.toFixed(6)}</dd><dt>历史时间戳</dt><dd>未记录</dd></dl></div></div>
    <div className="trace-warning">结构展开不是模型装配计划。模型响应与系统派生过程已分开标记；未记录内部思考，不补写思维链。</div>
    <details><summary>最终几何差分与评分</summary><div className="trace-differences">{trace.differences.length ? trace.differences.map((d, i) =>
      <span key={i}>{DIFF[d.kind]} · {d.expectedId ?? '∅'} → {d.actualId ?? '∅'}</span>) : <span>没有需要标注的几何差分</span>}</div>
      <p className="meta">近邻位姿/颜色归因是诊断提示，不替代原始严格评分。生成任务可接受不同拆砖方案。</p><pre>{JSON.stringify(trace.verdict, null, 2)}</pre></details></>}
  </section>;
}
