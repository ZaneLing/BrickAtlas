import { useEffect, useRef, useState } from 'react';
import { Play, SkipForward, Square, Download, ArrowLeft, ArrowRight } from 'lucide-react';
import { api, describe, download, read, staticMode } from './api';
import type { Catalogue, ModelRun, Models, SceneData } from './types';
import { JSONView, Visuals } from './Visuals';
import s from './Workbench.module.css';

export function ModelPanel({ catalogue, runId, onRun }: { catalogue: Catalogue; runId: string; onRun: (id: string) => void }) {
  const [models, setModels] = useState<Models>(), [run, setRun] = useState<ModelRun>(), [scene, setScene] = useState<SceneData>();
  const [step, setStep] = useState(0), [phase, setPhase] = useState('before'), [provider, setProvider] = useState('local');
  const [task, setTask] = useState(catalogue.questions.find(q => q.form === 'episode')!.id), [calls, setCalls] = useState(4);
  const [busy, setBusy] = useState(false), [error, setError] = useState('');
  const gate = useRef(false);
  useEffect(() => { api.models().then(setModels).catch(e => setError(e.message)); }, [runId, run?.status]);
  useEffect(() => {
    let alive = true; setRun(undefined); setScene(undefined); setStep(0); setError('');
    api.run(runId).then(r => { if (alive) setRun(r); }).catch(e => { if (alive) setError(e.message); });
    api.runScene(runId).then(r => { if (alive) setScene(r); }).catch(e => { if (alive) setError(e.message); });
    return () => { alive = false; };
  }, [runId]);
  useEffect(() => {
    if (!run || !['running', 'stopping'].includes(run.status)) return;
    let alive = true, timer: ReturnType<typeof setTimeout>;
    async function poll() {
      try {
        const next = await api.run(runId);
        if (!alive) return;
        setRun(next);
        if (!['running', 'stopping'].includes(next.status)) { setScene(await api.runScene(runId)); return; }
        timer = setTimeout(poll, 1200);
      } catch (e) { if (alive) setError((e as Error).message); }
    }
    timer = setTimeout(poll, 1200);
    return () => { alive = false; clearTimeout(timer); };
  }, [runId, run?.status]);
  async function guard(fn: () => Promise<void>) {
    if (gate.current) return; gate.current = true; setBusy(true); setError('');
    try { await fn(); } catch (e) { setError((e as Error).message); }
    finally { gate.current = false; setBusy(false); }
  }
  const create = () => guard(async () => {
    const next = await read<ModelRun>('api/model-runs', { taskId: task, provider, maxCalls: calls });
    onRun(next.id); setModels(await api.models());
  });
  const control = (mode: string) => guard(async () => {
    const next = await read<ModelRun>(`api/model-runs/${runId}/${mode}`, {}); setRun(next);
    if (mode === 'step' || mode === 'run') setStep(next.steps.length);
    if (mode === 'stop') setScene(await api.runScene(runId));
  });
  const current = run?.steps[step], obs = (phase === 'after' ? current?.after : current?.input.observation) || run?.initialObservation;
  const recorded = runId === 'case-local', running = ['running', 'stopping'].includes(run?.status || '');
  return <div className={s.modelLayout}>
    <aside className={s.runSidebar}>
      <h3>模型运行 / Model runs</h3>
      <button className={s.runItem} aria-pressed={recorded} onClick={() => onRun('case-local')}><b>SmolVLM-256M</b><span>真实记录 · 4 calls · failure case</span></button>
      {models?.runs.map(r => <button className={s.runItem} key={r.id} aria-pressed={runId === r.id} onClick={() => onRun(r.id)}><b>{r.taskId} · {r.model.split('/').at(-1)}</b><span>{r.id === run?.id ? run.status : r.status} · {r.id.slice(0, 8)}</span></button>)}
      <hr /><h4>新建运行 / New run</h4>
      <label className={s.field}>任务<select aria-label="Model task" value={task} onChange={e => setTask(e.target.value)}>{catalogue.questions.filter(q => q.form === 'episode').map(q => <option key={q.id} value={q.id}>{q.id} · {q.tier} · {q.profile}</option>)}</select></label>
      <label className={s.field}>模型<select aria-label="Model provider" value={provider} onChange={e => setProvider(e.target.value)}>{models?.providers.map(p => <option key={p.id} value={p.id} disabled={!p.available}>{p.name} {p.available ? '' : '· 未配置'}</option>)}</select></label>
      <label className={s.field}>调用上限 / Max calls<input aria-label="Maximum calls" type="number" min="1" max="32" value={calls} onChange={e => setCalls(+e.target.value)} /></label>
      <button className={s.primary} disabled={staticMode || busy || running || !models?.providers.some(p => p.id === provider && p.available) || calls < 1 || calls > 32 || !Number.isInteger(calls)} onClick={create}>创建运行 Create</button>
      <p className={s.muted}>创建后点击单步或运行才会调用模型。远程 API 按供应商计费，密钥在服务端配置。</p>
      {staticMode && <p>静态站支持记录回放；实时调用需启动完整运行包。</p>}
    </aside>
    <main className={s.modelMain}>
      <div className={s.brief}><div className={s.eyebrow}>MODEL OBSERVATION → RESPONSE → EXECUTOR</div><h2>{recorded ? '逐步案例 / Recorded case study' : '实时模型工作台 / Live model run'}</h2>
        <p>{run?.model} · {run?.taskId} <span className={s.badge}>{run?.status || 'Loading'}</span></p>
        <p className={s.muted}>{recorded ? '真实本地推理的四次输出均不符合动作协议。保留失败原文，用于展示接口与错误模式；不代表整体模型评测结果。' : run?.scope}</p>
      </div>
      <div className={s.workStatus}>
        <button disabled={recorded || staticMode || busy || run?.status !== 'paused'} onClick={() => control('step')}><SkipForward size={14} /> 单步 Step</button>
        <button className={s.primary} disabled={recorded || staticMode || busy || run?.status !== 'paused'} onClick={() => control('run')}><Play size={14} /> 连续运行 Run</button>
        <button disabled={recorded || staticMode || busy || !['running', 'paused'].includes(run?.status || '')} onClick={() => control('stop')}><Square size={14} /> 停止 Stop</button>
        <span>{run?.steps.length || 0} / {run?.maxCalls || 0} calls</span>
        <button disabled={!run} onClick={() => download(`brickplan-model-${runId}.json`, run)}><Download size={14} /> 导出</button>
      </div>
      <div className={s.timeline} aria-label="Model call timeline">{run?.steps.map((v, i) => <button key={v.index} aria-pressed={step === i} onClick={() => setStep(i)}><b>{String(v.index).padStart(2, '0')}</b><span>{v.feedback?.code || v.status}</span></button>)}</div>
      <div className={s.visualToolbar}>
        <div className={s.inline}><button aria-label="Previous model step" disabled={step <= 0} onClick={() => setStep(n => n - 1)}><ArrowLeft size={14} /></button>
          <span>Call {current?.index || '—'}</span><button aria-label="Next model step" disabled={step >= (run?.steps.length || 0) - 1} onClick={() => setStep(n => n + 1)}><ArrowRight size={14} /></button></div>
        <div className={s.segment}><button aria-pressed={phase === 'before'} onClick={() => setPhase('before')}>调用前 Input</button><button disabled={!current?.after} aria-pressed={phase === 'after'} onClick={() => setPhase('after')}>执行后 After</button></div>
      </div>
      <Visuals data={scene} images={obs?.images} frame={obs?.revision || 0} title={phase === 'after' ? '执行后 After action' : '模型观察 Before call'} />
      <div className={s.callDetail}>
        <section><div className={s.eyebrow}>01 / MODEL OUTPUT</div><h3>原始回复 / Raw response</h3><pre className={s.raw}>{current?.rawOutput || (running ? '等待模型返回…' : '尚无输出')}</pre>
          {current?.explanation && <p>{current.explanation}</p>}{current?.parseError && <p className={s.error}>{current.parseError}</p>}</section>
        <section><div className={s.eyebrow}>02 / ENVIRONMENT FEEDBACK</div><h3>{current?.feedback?.code || 'Waiting'}</h3><p>{describe(current?.action)}</p>
          <dl className={s.metrics}><div><dt>Latency</dt><dd>{current?.latencySeconds ?? '—'} s</dd></div><div><dt>Input tokens</dt><dd>{current?.usage?.inputTokens ?? '—'}</dd></div><div><dt>Output tokens</dt><dd>{current?.usage?.outputTokens ?? '—'}</dd></div></dl>
          {run?.stopReason && <p>停止原因：{run.stopReason}</p>}</section>
      </div>
      {error && <p role="alert" className={s.error}>{error}</p>}
      <JSONView value={{ systemPrompt: run?.systemPrompt, input: current?.input }} title="完整模型输入 / Exact model input, prompts and image order" />
      <JSONView value={current} title="该步完整记录 / Full step record" />
      {run?.score && <JSONView value={run.score} title="执行器评分 / Executor score" />}
    </main>
  </div>;
}
