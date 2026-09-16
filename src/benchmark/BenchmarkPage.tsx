import { useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowLeft, Play, Pause, RotateCcw, Expand, Download, Box, CheckCircle2, XCircle,
  ChevronLeft, ChevronRight, ClipboardCheck, Undo2,
} from 'lucide-react';
import { BenchmarkScene } from './Scene';
import { replay, score } from './engine';
import type { BenchModel, Task } from './types';
import {
  createReviewBatch,
  loadReviews,
  removeReview,
  reviewTask,
  saveReview,
  type ReviewRecord,
} from './reviewStore';
import './benchmark.css';

const base = `${import.meta.env.BASE_URL}benchmark/`;
interface Entry { id: string; name: string; nameZh: string; difficulty: string; parts: number; modules: number; tasks: number }
const layerNames = { atomic: '原子能力', metacognitive: '元认知与物理', procedural: '操作执行', integrative: '综合任务' };
type ReviewFilter = 'all' | 'pending' | 'pass' | 'fail';
function downloadReviewBatch(records: Record<string, ReviewRecord>, total: number) {
  const batch = createReviewBatch(records, total);
  const url = URL.createObjectURL(new Blob([JSON.stringify(batch, null, 2) + '\n'], { type: 'application/json' }));
  const link = document.createElement('a');
  link.href = url; link.download = `${batch.batchId}.json`; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 0);
}
function useCatalog() {
  const [entries, setEntries] = useState<Entry[]>([]);
  const [error, setError] = useState('');
  useEffect(() => {
    const controller = new AbortController();
    fetch(`${base}catalog.json`, { signal: controller.signal }).then(r => {
      if (!r.ok) throw new Error(`模型库 HTTP ${r.status}`);
      return r.json();
    }).then(setEntries).catch(e => { if (!controller.signal.aborted) setError(String(e)); });
    return () => controller.abort();
  }, []);
  return { entries, error };
}
export function BenchmarkLibrary({ compact = false }: { compact?: boolean }) {
  const { entries, error } = useCatalog();
  const [difficulty, setDifficulty] = useState('all'), [query, setQuery] = useState('');
  const [reviews] = useState<Record<string, ReviewRecord>>(() => loadReviews());
  const shown = entries.filter(m => (difficulty === 'all' || m.difficulty === difficulty)
    && `${m.id} ${m.name} ${m.nameZh}`.toLowerCase().includes(query.toLowerCase()));
  return <section className="bench-library" id="benchmark">
    <div className="bench-heading"><div><small>BRICKATLAS · HIERARCHY-3</small><h2>分层基准积木库</h2>
      <p>四级结构难度 × 四层任务 · 每个模型都可旋转、展开、隔离和逐步回放。</p></div>
      <strong>{entries.length} 个对象 / {entries.reduce((s, m) => s + m.tasks, 0)} 题</strong></div>
    <div className="bench-controls"><select aria-label="基准难度筛选" value={difficulty} onChange={e => setDifficulty(e.target.value)}>
      <option value="all">全部难度</option>{['D1 部件级', 'D2 装配体级', 'D3 机构级', 'D4 系统级'].map(v => <option key={v} value={v.slice(0, 2)}>{v}</option>)}
    </select><input aria-label="搜索基准模型" placeholder="搜索模型名称" value={query} onChange={e => setQuery(e.target.value)} />
    {!compact && <a href={import.meta.env.BASE_URL}>返回原项目库</a>}
    <a href={`${import.meta.env.BASE_URL}benchmark/review`}><ClipboardCheck size={16} />人工审核台</a>
    <a href={`${base}docs/main.pdf`}>论文 PDF</a><a href={`${base}docs/supplement.pdf`}>附录 PDF</a>
    <a href={`${base}docs/REPORT.zh-CN.md`}>中文报告</a></div>
    {!compact && <details><summary>展开模型库与任务覆盖矩阵</summary>
      <div className="bench-figures"><a href={`${base}figures/expanded-matrix.png`}><img src={`${base}figures/expanded-matrix.png`} alt="四级结构与四层任务矩阵" /></a>
      <a href={`${base}figures/expanded-library.png`}><img src={`${base}figures/expanded-library.png`} alt="全部模型实际三维视图" /></a></div>
      <a href={`${base}docs/QUESTION_BANK.zh-CN.md`}>下载全部题目、输入与答案</a>
      <p>旧版 48 模型上的 16 题试跑单独保留，新增模型尚未进行模型准确率测量。</p>
    </details>}
    {error && <p role="alert">{error}</p>}
    <div className="bench-grid">{shown.map(m => <a className="bench-card" key={m.id}
      href={`${import.meta.env.BASE_URL}benchmark/${m.id}`} data-bench-model={m.id}>
      <img src={`${base}images/${m.id}-iso.png`} loading="lazy" alt={`${m.nameZh} 实际三维渲染`} />
      <div><span>{m.difficulty} · {m.modules} 模块</span><h3>{m.nameZh}</h3><small>{m.name}</small>
      <p>{m.parts} 零件 · {m.tasks} 题 · 已审核 {Object.values(reviews).filter(row => row.modelId === m.id).length}/{m.tasks}</p></div>
    </a>)}</div>{!shown.length && !error && <p>{entries.length ? '无匹配模型' : '正在加载模型库…'}</p>}
  </section>;
}
declare global {
  interface Window {
    __benchmark?: () => ReturnType<BenchmarkScene['snapshot']>;
    __benchmarkCapture?: (view: string) => string;
  }
}
export function BenchmarkPage({ modelId }: { modelId?: string }) {
  const [data, setData] = useState<{ model: BenchModel; tasks: Task[]; physics: any } | null>(null);
  const [error, setError] = useState('');
  const [explosion, setExplosion] = useState(0), [selected, setSelected] = useState('');
  const [isolated, setIsolated] = useState(false);
  const [layer, setLayer] = useState('all'), [taskId, setTaskId] = useState('');
  const [program, setProgram] = useState(''), [step, setStep] = useState(0), [playing, setPlaying] = useState(false);
  const [showAnswer, setShowAnswer] = useState(false), [feedback, setFeedback] = useState('');
  const [reviews, setReviews] = useState<Record<string, ReviewRecord>>(() => loadReviews());
  const [reviewFilter, setReviewFilter] = useState<ReviewFilter>(
    () => new URLSearchParams(location.search).get('review') === '1' ? 'pending' : 'all',
  );
  const [reviewReason, setReviewReason] = useState(''), [reviewMessage, setReviewMessage] = useState('');
  const [autoAdvance, setAutoAdvance] = useState(true);
  const host = useRef<HTMLDivElement>(null), scene = useRef<BenchmarkScene | null>(null);
  const { entries } = useCatalog();
  const reviewMode = new URLSearchParams(location.search).get('review') === '1';
  useEffect(() => {
    if (!modelId) return;
    const abort = new AbortController();
    setData(null); setError(''); setPlaying(false); setTaskId('');
    fetch(`${base}models/${encodeURIComponent(modelId)}.json`, { signal: abort.signal })
      .then(r => { if (!r.ok) throw new Error(`模型 ${modelId} 不可用 (${r.status})`); return r.json(); })
      .then(setData).catch(e => { if (!abort.signal.aborted) setError(String(e)); });
    return () => abort.abort();
  }, [modelId]);
  useEffect(() => {
    if (!data || !host.current) return;
    const s = new BenchmarkScene(host.current, data.model, id => { setSelected(id); setIsolated(false); }); scene.current = s;
    window.__benchmark = () => s.snapshot();
    window.__benchmarkCapture = view => { s.view(view); return s.png(); };
    return () => { s.dispose(); scene.current = null; delete window.__benchmark; delete window.__benchmarkCapture; };
  }, [data]);
  useEffect(() => { scene.current?.explosion(explosion); }, [explosion]);
  useEffect(() => { scene.current?.highlight(selected || null, isolated); }, [selected, isolated]);
  const current = data?.tasks.find(t => t.id === taskId);
  const currentIndex = current && data ? data.tasks.findIndex(task => task.id === current.id) : -1;
  const modelReviews = Object.values(reviews).filter(row => row.modelId === modelId);
  const filteredTasks = useMemo(() => (data?.tasks ?? []).filter(task => {
    if (layer !== 'all' && task.layer !== layer) return false;
    const decision = reviews[task.id]?.decision;
    return reviewFilter === 'all' || (reviewFilter === 'pending' ? !decision : decision === reviewFilter);
  }), [data, layer, reviewFilter, reviews]);
  const execution = useMemo(() => {
    if (!current || current.format !== 'actions') return null;
    try { const raw = JSON.parse(program); return replay(current, Array.isArray(raw) ? raw : raw.actionIds); }
    catch { return null; }
  }, [current, program]);
  useEffect(() => { scene.current?.state(execution?.frames[Math.min(step, execution.frames.length - 1)] ?? null); }, [execution, step]);
  useEffect(() => {
    if (!playing || !execution) return;
    if (step >= execution.frames.length - 1) { setPlaying(false); return; }
    const timer = setTimeout(() => setStep(s => s + 1), 650); return () => clearTimeout(timer);
  }, [playing, step, execution]);
  const chooseTask = (id: string) => {
    const task = data?.tasks.find(t => t.id === id);
    setTaskId(id); setSelected(task?.targetModule ?? ''); setIsolated(false); setShowAnswer(false); setFeedback('');
    setProgram(''); setStep(0); setPlaying(false); setReviewMessage('');
    const url = new URL(location.href);
    if (id) url.searchParams.set('task', id); else url.searchParams.delete('task');
    history.replaceState(null, '', url);
  };
  useEffect(() => {
    if (!data || taskId) return;
    const requested = new URLSearchParams(location.search).get('task');
    const selectedTask = data.tasks.find(task => task.id === requested)
      ?? (reviewMode ? data.tasks.find(task => !reviews[task.id]) : undefined);
    if (!selectedTask) return;
    setTaskId(selectedTask.id); setSelected(selectedTask.targetModule); setIsolated(false);
  }, [data, reviewMode, reviews, taskId]);
  useEffect(() => {
    setReviewReason(current ? reviews[current.id]?.reason ?? '' : '');
  }, [current?.id, reviews]);
  const advanceReview = (nextReviews: Record<string, ReviewRecord>) => {
    if (!data || !current) return;
    const after = data.tasks.slice(currentIndex + 1).find(task => !nextReviews[task.id])
      ?? data.tasks.slice(0, currentIndex).find(task => !nextReviews[task.id]);
    if (after) { chooseTask(after.id); return; }
    const modelIndex = entries.findIndex(entry => entry.id === modelId);
    for (let offset = 1; offset <= entries.length; offset++) {
      const entry = entries[(modelIndex + offset + entries.length) % entries.length];
      const reviewed = Object.values(nextReviews).filter(row => row.modelId === entry.id).length;
      if (reviewed < entry.tasks) {
        location.href = `${import.meta.env.BASE_URL}benchmark/${entry.id}?review=1`;
        return;
      }
    }
    setReviewMessage('本批次题目已全部审核');
  };
  const submitReview = (decision: 'pass' | 'fail') => {
    if (!current) return;
    try {
      const next = saveReview(reviewTask(current, decision, reviewReason));
      setReviews(next);
      if (autoAdvance) advanceReview(next);
      setReviewMessage(decision === 'pass' ? '已记录：通过' : '已记录：不通过');
    } catch (reason) {
      setReviewMessage(reason instanceof Error ? reason.message : String(reason));
    }
  };
  if (!modelId) return <div className="bench-page"><BenchmarkLibrary /></div>;
  return <div className="bench-page bench-workspace">
    <header className="bench-topbar"><a href={import.meta.env.BASE_URL}><ArrowLeft size={18} />原项目库</a>
      <a href={`${import.meta.env.BASE_URL}benchmark`}>BRICK ATLAS · 基准库</a>
      <select aria-label="切换基准模型" value={modelId} onChange={e => {
        location.href = `${import.meta.env.BASE_URL}benchmark/${e.target.value}${reviewMode ? '?review=1' : ''}`;
      }}>
        {entries.map(m => <option key={m.id} value={m.id}>{m.difficulty} · {m.nameZh}</option>)}
      </select><a href={`${import.meta.env.BASE_URL}benchmark/review`}><ClipboardCheck size={17} />审核台</a>
      <a href={`${base}docs/main.pdf`}>论文</a><a href={`${base}docs/supplement.pdf`}>附录</a></header>
    {error && <div role="alert">{error}</div>}
    {!data && !error && <p role="status">正在加载三维积木…</p>}
    {data && <div className="bench-workgrid">
      <aside className="bench-sidebar"><small>{data.model.difficulty} · {data.model.family}</small><h1>{data.model.nameZh}</h1><p>{data.model.name}</p>
        <p>{data.model.parts.length} 零件 · {data.model.modules.length} 模块 · {data.model.joints.length} 关节</p>
        <h3>结构与模块</h3><button onClick={() => { chooseTask(''); scene.current?.highlight(null); scene.current?.state(null); }}>显示完整模型</button>
        {data.model.modules.map(m => <div className="bench-module" key={m.id}>
          <button className={selected === m.id ? 'selected' : ''} onClick={() => { setSelected(m.id); setIsolated(false); }}>{m.name}</button>
          <button aria-label={`隔离 ${m.id}`} onClick={() => { setSelected(m.id); setIsolated(true); }}>隔离</button>
        </div>)}
        <details><summary>结构核验范围</summary><p>原创可视部件与声明关节。展开仅用于查看，不是物理拆装路径。模拟采用固定基座与包围盒碰撞体。</p>
        <p>含凸点包围体；基座固定，活动关节采用有限力位置伺服。</p>
        <p>模块代表点位移：{data.physics.nominalPointDrift.toFixed(4)}；最大转角：{data.physics.nominalAngularDrift.toFixed(4)} rad；{data.physics.nominalWithinTolerance ? '通过名义状态核验' : '未通过名义状态核验'}。</p></details>
      </aside>
      <main className="bench-view"><div className="bench-canvas" ref={host} />
        <div className="bench-viewtools">{['iso', 'front', 'side', 'top'].map((v, i) => <button key={v} onClick={() => scene.current?.view(v)}>{['自由视角', '正视', '侧视', '俯视'][i]}</button>)}
          <button onClick={() => scene.current?.fit()} aria-label="适配基准模型"><Expand size={16} /></button>
          <button onClick={() => { setExplosion(0); chooseTask(''); scene.current?.highlight(null); scene.current?.state(null); scene.current?.view('iso'); }} aria-label="复原基准模型"><RotateCcw size={16} /></button>
          <button onClick={() => { const a = document.createElement('a'); a.href = scene.current!.png(); a.download = `${modelId}.png`; a.click(); }} aria-label="下载基准截图"><Download size={16} /></button>
        </div>
        <div className="bench-explode"><Box size={18} /><label>3D 展开 <input aria-label="基准展开程度" type="range" min="0" max="1" step="0.01" value={explosion} onChange={e => setExplosion(Number(e.target.value))} /></label><output>{Math.round(explosion * 100)}%</output><small>拖动旋转 · 滚轮缩放 · 右键平移</small></div>
        {execution && <div className="bench-replay"><button aria-label="播放动作回放" onClick={() => { if (step >= execution.frames.length - 1) setStep(0); setPlaying(!playing); }}>{playing ? <Pause size={17} /> : <Play size={17} />}</button>
          <input aria-label="动作回放步骤" type="range" min="0" max={execution.frames.length - 1} value={step} onChange={e => { setPlaying(false); setStep(Number(e.target.value)); }} />
          <output>{step}/{execution.frames.length - 1}</output><span>{execution.frames[step]?.actionId ?? '初始状态'}</span></div>}
      </main>
      <aside className="bench-tasks"><div className="bench-task-heading"><div><small>逐题人工审核</small><h2>任务与能力</h2></div>
        <button title="导出当前审核批次" aria-label="导出当前审核批次" disabled={!entries.length}
          onClick={() => downloadReviewBatch(reviews, entries.reduce((sum, entry) => sum + entry.tasks, 0))}>
          <Download size={17} /></button></div>
        <div className="bench-model-review-progress">
          <span>本模型 {modelReviews.length}/{data.tasks.length}</span>
          <progress max={data.tasks.length} value={modelReviews.length} />
          <small>{modelReviews.filter(row => row.decision === 'fail').length} 条不通过</small>
        </div>
        <select aria-label="基准题型筛选" value={layer} onChange={e => setLayer(e.target.value)}>
          <option value="all">全部能力层（{data.tasks.length}）</option>{Object.entries(layerNames).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>
        <div className="bench-review-filter" role="group" aria-label="审核状态筛选">
          {([['pending', '待审核'], ['all', '全部'], ['pass', '通过'], ['fail', '不通过']] as const).map(([value, label]) =>
            <button key={value} className={reviewFilter === value ? 'active' : ''}
              onClick={() => setReviewFilter(value)}>{label}</button>)}
        </div>
        <div className="bench-review-nav">
          <button title="上一题" aria-label="上一题" disabled={currentIndex <= 0}
            onClick={() => chooseTask(data.tasks[currentIndex - 1].id)}><ChevronLeft size={17} /></button>
          <span>{currentIndex >= 0 ? `${currentIndex + 1} / ${data.tasks.length}` : '选择一道题'}</span>
          <button title="下一题" aria-label="下一题" disabled={currentIndex < 0 || currentIndex >= data.tasks.length - 1}
            onClick={() => chooseTask(data.tasks[currentIndex + 1].id)}><ChevronRight size={17} /></button>
        </div>
        <div className="bench-review-queue" aria-label="审核题目队列">
          {filteredTasks.map(task => {
            const decision = reviews[task.id]?.decision;
            return <button key={task.id} className={`${task.id === taskId ? 'current' : ''} ${decision ?? 'pending'}`}
              onClick={() => chooseTask(task.id)}>
              <span>{layerNames[task.layer]} · {task.title}</span>
              {decision === 'pass' ? <CheckCircle2 size={16} /> : decision === 'fail' ? <XCircle size={16} /> : <i />}
            </button>;
          })}
          {!filteredTasks.length && <p>当前筛选下没有题目。</p>}
        </div>
        <select aria-label="选择基准题目" value={taskId} onChange={e => chooseTask(e.target.value)}><option value="">按名称选择题目</option>
          {data.tasks.map(t => <option key={t.id} value={t.id}>{layerNames[t.layer]} · {t.title}</option>)}</select>
        {current ? <><h3>{current.title}</h3><p>{current.question}</p><small>{current.capabilities.join(' · ')} / {current.evidence}</small>
          {current.options?.map(o => <p key={o.id} className="bench-option"><b>{o.id}</b> {o.label}</p>)}
          <details><summary>公开输入与规则</summary><pre>{JSON.stringify(current.input, null, 2)}</pre></details>
          <label>提交答案 JSON<textarea aria-label="基准答案 JSON" value={program} onChange={e => { setProgram(e.target.value); setStep(0); setPlaying(false); }} placeholder={current.format === 'actions' ? '{"actionIds":[]}' : '{"choiceId":"A"}'} /></label>
          <div className="bench-controls"><button onClick={() => {
            try { const verdict = score(current, JSON.parse(program)); setFeedback(verdict.success ? '通过' : '未通过：检查输出格式、前置条件及目标'); }
            catch { setFeedback('JSON 格式错误'); }
          }}>检查答案</button><button onClick={() => { setProgram(JSON.stringify(current.answer, null, 2)); setShowAnswer(true); setStep(0); }}>载入参考答案</button></div>
          {feedback && <p role="status">{feedback}</p>}
          {execution && <><p>{execution.success ? '序列达到目标' : execution.issue} · 总成本 {execution.frames.at(-1)?.cost}</p>
            <ol className="bench-actionlist">{execution.frames.slice(1).map(f => <li key={f.step}><button onClick={() => { setStep(f.step); setPlaying(false); }}>{f.step}. {f.actionId} {f.accepted ? '✓' : '×'}</button></li>)}</ol>
            <details><summary>当前状态证据</summary><pre>{JSON.stringify(execution.frames[step], null, 2)}</pre></details></>}
          {showAnswer && <small>当前载入的是参考答案；可粘贴模型输出后使用同一解释器回放。</small>}
          <section className={`bench-review-box ${reviews[current.id]?.decision ?? 'pending'}`}>
            <div className="bench-review-box-title"><div><small>审核结论</small>
              <strong>{reviews[current.id]?.decision === 'pass' ? '已通过'
                : reviews[current.id]?.decision === 'fail' ? '不通过' : '待审核'}</strong></div>
              {reviews[current.id] && <button title="撤销当前审核" aria-label="撤销当前审核" onClick={() => {
                const next = removeReview(current.id);
                setReviews(next); setReviewReason(''); setReviewMessage('已撤销当前题目的审核结论');
              }}><Undo2 size={16} /></button>}</div>
            <label>审核备注 / 不通过理由
              <textarea aria-label="审核意见" value={reviewReason} onChange={event => setReviewReason(event.target.value)}
                placeholder="判为不通过时必须填写具体问题、预期修正和证据。" />
            </label>
            <label className="bench-auto-advance"><input type="checkbox" checked={autoAdvance}
              onChange={event => setAutoAdvance(event.target.checked)} />提交后自动进入下一道待审核题</label>
            <div className="bench-review-decisions">
              <button className="pass" onClick={() => submitReview('pass')}><CheckCircle2 size={18} />通过</button>
              <button className="fail" onClick={() => submitReview('fail')}><XCircle size={18} />不通过</button>
            </div>
            {reviewMessage && <p role={reviewMessage.includes('必须') ? 'alert' : 'status'}>{reviewMessage}</p>}
          </section>
        </> : <p>选择任一题查看输入、能力与评分规则。操作题可逐步执行参考或模型动作。</p>}
      </aside></div>}
  </div>;
}
