import { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, Play, Pause, RotateCcw, Expand, Download, Box } from 'lucide-react';
import { BenchmarkScene } from './Scene';
import { replay, score } from './engine';
import type { BenchModel, Task } from './types';
import './benchmark.css';

const base = `${import.meta.env.BASE_URL}benchmark/`;
interface Entry { id: string; name: string; nameZh: string; difficulty: string; parts: number; modules: number; tasks: number }
const layerNames = { atomic: '原子能力', metacognitive: '元认知与物理', procedural: '操作执行', integrative: '综合任务' };
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
  const shown = entries.filter(m => (difficulty === 'all' || m.difficulty === difficulty)
    && `${m.id} ${m.name} ${m.nameZh}`.toLowerCase().includes(query.toLowerCase()));
  return <section className="bench-library" id="benchmark">
    <div className="bench-heading"><div><small>BRICKATLAS · HIERARCHY-2</small><h2>分层基准积木库</h2>
      <p>四级结构难度 × 四层任务 · 每个模型都可旋转、展开、隔离和逐步回放。</p></div>
      <strong>{entries.length} 个对象 / {entries.reduce((s, m) => s + m.tasks, 0)} 题</strong></div>
    <div className="bench-controls"><select aria-label="基准难度筛选" value={difficulty} onChange={e => setDifficulty(e.target.value)}>
      <option value="all">全部难度</option>{['D1 部件级', 'D2 装配体级', 'D3 机构级', 'D4 系统级'].map(v => <option key={v} value={v.slice(0, 2)}>{v}</option>)}
    </select><input aria-label="搜索基准模型" placeholder="搜索模型名称" value={query} onChange={e => setQuery(e.target.value)} />
    {!compact && <a href={import.meta.env.BASE_URL}>返回原项目库</a>}
    <a href={`${base}docs/main.pdf`}>论文 PDF</a><a href={`${base}docs/supplement.pdf`}>附录 PDF</a>
    <a href={`${base}docs/REPORT.zh-CN.md`}>中文报告</a></div>
    {!compact && <details><summary>展开难度矩阵与试跑热力图（每格 n=1）</summary>
      <div className="bench-figures"><a href={`${base}figures/hierarchy2-matrix.png`}><img src={`${base}figures/hierarchy2-matrix.png`} alt="四级结构与四层任务矩阵" /></a>
      <a href={`${base}figures/hierarchy2-pilot.png`}><img src={`${base}figures/hierarchy2-pilot.png`} alt="16题流程试跑计数，非总体准确率" /></a></div>
      <a href={`${base}docs/QUESTION_BANK.zh-CN.md`}>下载全部题目、输入与答案</a>
    </details>}
    {error && <p role="alert">{error}</p>}
    <div className="bench-grid">{shown.map(m => <a className="bench-card" key={m.id}
      href={`${import.meta.env.BASE_URL}benchmark/${m.id}`} data-bench-model={m.id}>
      <img src={`${base}images/${m.id}-iso.png`} loading="lazy" alt={`${m.nameZh} 实际三维渲染`} />
      <div><span>{m.difficulty} · {m.modules} 模块</span><h3>{m.nameZh}</h3><small>{m.name}</small>
      <p>{m.parts} 零件 · {m.tasks} 题 · 打开 3D ↗</p></div>
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
  const [layer, setLayer] = useState('all'), [taskId, setTaskId] = useState('');
  const [program, setProgram] = useState(''), [step, setStep] = useState(0), [playing, setPlaying] = useState(false);
  const [showAnswer, setShowAnswer] = useState(false), [feedback, setFeedback] = useState('');
  const host = useRef<HTMLDivElement>(null), scene = useRef<BenchmarkScene | null>(null);
  const { entries } = useCatalog();
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
    const s = new BenchmarkScene(host.current, data.model, setSelected); scene.current = s;
    window.__benchmark = () => s.snapshot();
    window.__benchmarkCapture = view => { s.view(view); return s.png(); };
    return () => { s.dispose(); scene.current = null; delete window.__benchmark; delete window.__benchmarkCapture; };
  }, [data]);
  useEffect(() => { scene.current?.explosion(explosion); }, [explosion]);
  useEffect(() => { scene.current?.highlight(selected || null); }, [selected]);
  const current = data?.tasks.find(t => t.id === taskId);
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
    setTaskId(id); setSelected(task?.targetModule ?? ''); setShowAnswer(false); setFeedback('');
    setProgram(''); setStep(0); setPlaying(false);
  };
  if (!modelId) return <div className="bench-page"><BenchmarkLibrary /></div>;
  return <div className="bench-page bench-workspace">
    <header className="bench-topbar"><a href={import.meta.env.BASE_URL}><ArrowLeft size={18} />原项目库</a>
      <a href={`${import.meta.env.BASE_URL}benchmark`}>BRICK ATLAS · 基准库</a>
      <select aria-label="切换基准模型" value={modelId} onChange={e => { location.href = `${import.meta.env.BASE_URL}benchmark/${e.target.value}`; }}>
        {entries.map(m => <option key={m.id} value={m.id}>{m.difficulty} · {m.nameZh}</option>)}
      </select><a href={`${base}docs/main.pdf`}>论文</a><a href={`${base}docs/supplement.pdf`}>附录</a></header>
    {error && <div role="alert">{error}</div>}
    {!data && !error && <p role="status">正在加载三维积木…</p>}
    {data && <div className="bench-workgrid">
      <aside className="bench-sidebar"><small>{data.model.difficulty} · {data.model.family}</small><h1>{data.model.nameZh}</h1><p>{data.model.name}</p>
        <p>{data.model.parts.length} 零件 · {data.model.modules.length} 模块 · {data.model.joints.length} 关节</p>
        <h3>结构与模块</h3><button onClick={() => { setSelected(''); scene.current?.highlight(null); scene.current?.state(null); }}>显示完整模型</button>
        {data.model.modules.map(m => <div className="bench-module" key={m.id}>
          <button className={selected === m.id ? 'selected' : ''} onClick={() => setSelected(m.id)}>{m.name}</button>
          <button aria-label={`隔离 ${m.id}`} onClick={() => { setSelected(m.id); requestAnimationFrame(() => scene.current?.highlight(m.id, true)); }}>隔离</button>
        </div>)}
        <details><summary>结构核验范围</summary><p>原创可视部件与声明关节。展开仅用于查看，不是物理拆装路径。模拟采用固定基座与包围盒碰撞体。</p>
        <p>原位稳定漂移：{data.physics.nominalDrift.toFixed(4)}；{data.physics.nominalWithinTolerance ? '在声明容差内' : '超出容差，物理题仅作轨迹诊断'}。</p></details>
      </aside>
      <main className="bench-view"><div className="bench-canvas" ref={host} />
        <div className="bench-viewtools">{['iso', 'front', 'side', 'top'].map((v, i) => <button key={v} onClick={() => scene.current?.view(v)}>{['自由视角', '正视', '侧视', '俯视'][i]}</button>)}
          <button onClick={() => scene.current?.fit()} aria-label="适配基准模型"><Expand size={16} /></button>
          <button onClick={() => { setExplosion(0); setSelected(''); scene.current?.state(null); scene.current?.view('iso'); }} aria-label="复原基准模型"><RotateCcw size={16} /></button>
          <button onClick={() => { const a = document.createElement('a'); a.href = scene.current!.png(); a.download = `${modelId}.png`; a.click(); }} aria-label="下载基准截图"><Download size={16} /></button>
        </div>
        <div className="bench-explode"><Box size={18} /><label>3D 展开 <input aria-label="基准展开程度" type="range" min="0" max="1" step="0.01" value={explosion} onChange={e => setExplosion(Number(e.target.value))} /></label><output>{Math.round(explosion * 100)}%</output><small>拖动旋转 · 滚轮缩放 · 右键平移</small></div>
        {execution && <div className="bench-replay"><button aria-label="播放动作回放" onClick={() => { if (step >= execution.frames.length - 1) setStep(0); setPlaying(!playing); }}>{playing ? <Pause size={17} /> : <Play size={17} />}</button>
          <input aria-label="动作回放步骤" type="range" min="0" max={execution.frames.length - 1} value={step} onChange={e => { setPlaying(false); setStep(Number(e.target.value)); }} />
          <output>{step}/{execution.frames.length - 1}</output><span>{execution.frames[step]?.actionId ?? '初始状态'}</span></div>}
      </main>
      <aside className="bench-tasks"><h2>任务与能力</h2><select aria-label="基准题型筛选" value={layer} onChange={e => setLayer(e.target.value)}>
        <option value="all">全部题型（35）</option>{Object.entries(layerNames).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>
        <select aria-label="选择基准题目" value={taskId} onChange={e => chooseTask(e.target.value)}><option value="">选择题目</option>
          {data.tasks.filter(t => layer === 'all' || t.layer === layer).map(t => <option key={t.id} value={t.id}>{layerNames[t.layer]} · {t.title}</option>)}</select>
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
        </> : <p>选择任一题查看输入、能力与评分规则。操作题可逐步执行参考或模型动作。</p>}
      </aside></div>}
  </div>;
}
