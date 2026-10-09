import { useEffect, useRef, useState } from 'react';
import * as Tabs from '@radix-ui/react-tabs';
import { Play, Download, CheckCircle2, ArrowLeft, ArrowRight } from 'lucide-react';
import { api, describe, download, read, staticMode } from './api';
import type { Action, Catalogue, Event, Observation, Preview, SceneData, Score, TaskInfo } from './types';
import { JSONView, RasterView, Visuals } from './Visuals';
import s from './Workbench.module.css';

export function Brief({ catalogue, id }: { catalogue?: Catalogue; id: string }) {
  const row = catalogue?.questions.find(q => q.id === id), family = catalogue?.taxonomy.find(f => f.id === row?.category);
  return <div className={s.brief}>
    <div className={s.eyebrow}>{id} {row && ` / ${row.tier} · ${row.form} · ${row.source}`}</div>
    <h2>{family?.question.zh || '完成当前任务'}<small>{family?.question.en || 'Complete the assigned task'}</small></h2>
    {family && <div className={s.contract}><p><b>已知 Given</b>{family.given.zh}</p><p><b>作答 Answer</b>{family.answer.zh}</p><p><b>评分 Score</b>{family.score.zh}</p></div>}
  </div>;
}
const feedback: Record<string, string> = {
  OK: '操作已执行', ATTACHED: '零件已安装', DETACHED: '零件已拆下', AUDITED: '检修已完成',
  FINISHED: '本次作答已结束', INSPECTED: '已获取视角', DIAGNOSIS_RECORDED: '诊断已记录',
  INVALID_ACTION: '操作格式无效，已计入预算', BLOCKED: '路径被其他零件阻挡', RACK_FULL: '暂存架已满',
  UNSUPPORTED: '操作会破坏支撑', REGISTERED_SITE_MISMATCH: '零件与注册位置不匹配',
};
export function Workcell({ id, info, catalogue, resumeId, onSession }: { id: string; info: TaskInfo; catalogue?: Catalogue; resumeId?: string; onSession: (sid: string) => void }) {
  const [preview, setPreview] = useState<Preview>(), [obs, setObs] = useState<Observation>();
  const [scene, setScene] = useState<SceneData>(), [sid, setSid] = useState(''), [events, setEvents] = useState<Event[]>([]);
  const [selected, setSelected] = useState(''), [site, setSite] = useState(''), [busy, setBusy] = useState(false), [message, setMessage] = useState('');
  const [answer, setAnswer] = useState(''), [review, setReview] = useState<unknown>(), [score, setScore] = useState<Score>();
  const [frame, setFrame] = useState<number | undefined>(), [frameObs, setFrameObs] = useState<Observation>();
  const [saved, setSaved] = useState(''), [view, setView] = useState('isometric'), [note, setNote] = useState('');
  const gate = useRef(false), epoch = useRef(0);
  const probe = id.startsWith('Q'), historical = frame !== undefined || saved !== '';
  const active = Boolean(sid || (probe && preview)) && !staticMode;
  const frozen = probe ? preview?.answered : obs?.terminated;
  const canAct = active && !frozen && !historical && !busy;
  const effectiveObs = frameObs || obs;
  const displayImages = saved !== '' ? obs?.inspectionHistory[+saved]?.images : effectiveObs?.images;
  const select = (part: string) => { setSelected(part); setSite(obs?.registration.find(r => r.partId === part)?.siteId || ''); };
  async function sessionExtras(key: string, observation: Observation) {
    setEvents((await read<{ events: Event[] }>(`api/sessions/${key}/history`)).events);
    if (!info.study) {
      setScene(await read<SceneData>(`api/sessions/${key}/scene`));
      if (observation.terminated) setScore(await read<Score>(`api/sessions/${key}/score`));
    }
  }
  useEffect(() => {
    const generation = ++epoch.current; let alive = true;
    setBusy(true); setObs(undefined); setScene(undefined); setSid(''); setEvents([]); setScore(undefined);
    setPreview(undefined); setReview(undefined); setFrame(undefined); setFrameObs(undefined); setSaved(''); setAnswer('');
    async function load() {
      const query = new URLSearchParams(location.search), requested = query.get('session');
      const resume = requested || resumeId || (info.study ? info.tasks.find(t => t.id === id)?.sessions.at(-1) : undefined);
      if (resume && !probe && !staticMode) {
        const loaded = await read<{ sessionId: string; observation: Observation }>(`api/sessions/${resume}`);
        if (!alive) return;
        setSid(resume); onSession(resume); setObs(loaded.observation); await sessionExtras(resume, loaded.observation);
      } else if (probe && !staticMode) {
        const p = await read<Preview>(`api/probes/${id}`); if (!alive) return;
        setPreview(p); setObs(p.observation);
        if (!info.study) {
          setScene(await api.scene(id));
          if (p.answered) setReview(await read(`api/probes/${id}/review`));
        }
      } else if (!info.study) {
        const p = await api.preview(id); if (!alive) return;
        setPreview(p); setObs(p.observation); setScene(await api.scene(id));
      }
      if (alive) setMessage(staticMode ? '静态预览：下载完整运行包后可作答。' : probe ? '冻结状态诊断题：选择答案后提交。' : '检查目标与工单，然后开始或继续作答。');
    }
    load().catch(e => { if (alive) setMessage(e.message); }).finally(() => { if (alive && generation === epoch.current) setBusy(false); });
    return () => { alive = false; epoch.current++; };
  }, [id]);
  useEffect(() => {
    if (obs && !obs.partIds.includes(selected)) { setSelected(obs.partIds[0] || ''); setSite(obs.registration[0]?.siteId || ''); }
  }, [obs]);
  async function guard(fn: () => Promise<void>) {
    if (gate.current) return; gate.current = true; setBusy(true);
    try { await fn(); } catch (e) { setMessage((e as Error).message); }
    finally { setBusy(false); gate.current = false; }
  }
  const start = () => guard(async () => {
    const result = await read<{ sessionId: string; observation: Observation }>('api/sessions', { taskId: id, requestId: crypto.randomUUID() });
    setSid(result.sessionId); onSession(result.sessionId); setObs(result.observation); setScore(undefined); setFrame(undefined); setFrameObs(undefined); setSaved('');
    history.replaceState(null, '', `?session=${result.sessionId}#work`);
    await sessionExtras(result.sessionId, result.observation); setMessage('作答已开始。选择零件与操作，观察执行反馈。');
  });
  const act = (action: Action) => guard(async () => {
    try {
      if (probe) {
        await read(`api/probes/${id}/actions`, { requestId: crypto.randomUUID(), revision: preview!.revision, action });
        const p = await read<Preview>(`api/probes/${id}`); setPreview(p); setObs(p.observation);
        if (p.answered && !info.study) setReview(await read(`api/probes/${id}/review`));
        setMessage(p.answered ? '答案已记录并冻结。 Answer recorded.' : '视角已保存。 Camera recorded.');
      } else {
        const result = await read<{ observation: Observation; result: { code: string } }>(`api/sessions/${sid}/actions`, { requestId: crypto.randomUUID(), revision: obs!.revision, action });
        setObs(result.observation); await sessionExtras(sid, result.observation);
        setMessage(`${feedback[result.result.code] || '执行器反馈'} · ${result.result.code}`);
      }
    } catch (error) {
      if (sid) { const latest = await read<{ observation: Observation }>(`api/sessions/${sid}`); setObs(latest.observation); await sessionExtras(sid, latest.observation); }
      else if (probe) { const latest = await read<Preview>(`api/probes/${id}`); setPreview(latest); setObs(latest.observation); }
      throw error;
    }
  });
  const replay = (n: number) => guard(async () => {
    const result = await read<{ observation: Observation }>(`api/sessions/${sid}/frame/${n}`);
    setFrame(n); setFrameObs(result.observation); setSaved('');
  });
  return <div className={s.workcell}>
    <div className={s.workMain}>
      <Brief catalogue={catalogue} id={id} />
      <div className={s.workStatus}>
        <span className={s.badge}>{historical ? '历史记录 History' : frozen ? '已提交 Recorded' : active ? '进行中 Live' : '预览 Preview'}</span>
        <span>{obs && `revision ${effectiveObs?.revision} · ${probe ? 'frozen checkpoint' : `${obs.attempts} / ${obs.actionBudget} operations`}`}</span>
        {!probe && !sid && <button className={s.primary} disabled={busy || staticMode} onClick={start}><Play size={14} /> 开始作答 Start</button>}
        {!probe && sid && obs?.terminated && !info.study && <button disabled={busy} onClick={start}>重新练习 New attempt</button>}
        {historical && <button onClick={() => { setFrame(undefined); setFrameObs(undefined); setSaved(''); }}>返回当前 Return to live</button>}
      </div>
      <Visuals data={saved === '' ? scene : undefined} images={displayImages} frame={frame} selected={selected} onSelect={select} study={info.study || saved !== ''} />
      {preview?.repairContext && <details className={s.details} open><summary>错误前检查点与后续历史 / Repair checkpoint</summary>
        <div className={s.repair}><RasterView raster={preview.repairContext.checkpointObservation.images?.current} title="Pre-error checkpoint" />
          <div><p>{preview.repairContext.rule}</p><ol>{preview.repairContext.executedHistory.map((a, i) => <li key={i}>{describe(a)}</li>)}</ol></div></div>
      </details>}
      <div className={s.status} role="status">{busy ? '正在处理… / Working…' : message}</div>
      {score && <div className={s.score}><b>{score.success ? '✓ 任务完成 Success' : '未完成目标 Incomplete'}</b><span>操作 {score.operations}</span><span>最优 {score.optimal}</span><span>额外 {score.regret ?? '—'}</span></div>}
      <Tabs.Root defaultValue="history" className={s.bottomPanel}>
        <Tabs.List className={s.tabList}><Tabs.Trigger value="history">操作记录 History</Tabs.Trigger><Tabs.Trigger value="observation">公开输入 Observation</Tabs.Trigger><Tabs.Trigger value="feedback">审核反馈 Feedback</Tabs.Trigger></Tabs.List>
        <Tabs.Content value="history">
          {!events.length && <p className={s.muted}>尚无操作。每次操作及拒绝原因会按顺序保存在这里。</p>}
          {sid && obs?.terminated && !info.study && <div className={s.inline}><button disabled={busy} onClick={() => replay(Math.max(0, (frame ?? events.length) - 1))}><ArrowLeft size={14} /></button>
            <input aria-label="Replay revision" type="range" min="0" max={events.length} value={frame ?? events.length} disabled={busy} onChange={e => replay(+e.target.value)} />
            <span>Frame {frame ?? events.length} / {events.length}</span><button disabled={busy} onClick={() => replay(Math.min(events.length, (frame ?? events.length) + 1))}><ArrowRight size={14} /></button></div>}
          <ol className={s.history}>{events.map(e => <li key={e.revision}><span>{e.revision.toString().padStart(2, '0')}</span><b>{describe(e.action)}</b><code>{e.code}</code></li>)}</ol>
          {sid && <button onClick={() => guard(async () => download(`brickplan-${sid}.json`, await read(`api/sessions/${sid}/export`)))}><Download size={14} /> 导出轨迹</button>}
        </Tabs.Content>
        <Tabs.Content value="observation"><JSONView value={effectiveObs} title="完整公开观察 / Full public observation" />{score && <JSONView value={score} title="完整评分 / Score" />}</Tabs.Content>
        <Tabs.Content value="feedback"><label className={s.field}>质量反馈 / Review note<textarea value={note} onChange={e => setNote(e.target.value)} placeholder="指出具体 ID、步骤与问题…" /></label>
          <button onClick={() => download(`brickplan-review-${id}.json`, { schema: 'brickplan-review/2.1', questionId: id, sessionId: sid || null, revision: effectiveObs?.revision, frame, selected, note })}><Download size={14} /> 导出反馈 JSON</button></Tabs.Content>
      </Tabs.Root>
    </div>
    <aside className={s.inspector}>
      <h3>{probe ? '提交判断 Answer' : '操作台 Actions'}</h3>
      {probe ? <>
        <p className={s.prompt}>{preview?.question}</p>
        {preview?.proposedPlan && <ol className={s.plan}>{preview.proposedPlan.map((a, i) => <li key={i}>{describe(a)}</li>)}</ol>}
        <label className={s.field}>选择答案<select aria-label="Probe answer" value={answer} disabled={!canAct} onChange={e => setAnswer(e.target.value)}>
          <option value="">请选择 / Select…</option>
          {preview?.candidates ? preview.candidates.map((a, i) => <option key={i} value={i}>{i + 1}. {describe(a)}</option>) : <><option value="null">全部合法 / All legal</option>{preview?.proposedPlan?.map((_, i) => <option key={i} value={i + 1}>首个冲突在第 {i + 1} 步</option>)}</>}
        </select></label>
        <button className={s.primary} disabled={!canAct || answer === ''} onClick={() => act({ type: 'answer', answer: { [preview?.candidates ? 'choice' : 'firstConflict']: JSON.parse(answer) } })}><CheckCircle2 size={15} /> 提交答案 Submit</button>
        {preview?.answered && <p className={s.recorded}>答案已冻结 / Answer frozen</p>}
        {!!review && <JSONView value={review} title="已提交答案解析 / Answer review" />}
      </> : <>
        <label className={s.field}>零件 / Piece<select aria-label="Piece" value={selected} onChange={e => select(e.target.value)}>{obs?.partIds.map(p => <option key={p}>{p}</option>)}{selected.startsWith('F') && <option>{selected}</option>}</select></label>
        <label className={s.field}>注册位置 / Site<select aria-label="Site" value={site} onChange={e => setSite(e.target.value)}>{obs?.siteIds.map(p => <option key={p}>{p}</option>)}</select></label>
        {selected.startsWith('F') && <p>F 是固定基座，不能移动。</p>}
        <div className={s.actionGrid}>
          <button className={s.primary} disabled={!canAct || selected.startsWith('F')} onClick={() => act({ type: 'attach', partId: selected, siteId: site })}>安装 Attach</button>
          <button disabled={!canAct || selected.startsWith('F')} onClick={() => act({ type: 'detach', partId: selected })}>拆卸 Detach</button>
          <button disabled={!canAct || selected.startsWith('F')} onClick={() => act({ type: 'audit', partId: selected })}>离架检修 Audit</button>
          <button disabled={!canAct} onClick={() => act({ type: 'finish' })}>结束 Finish</button>
        </div>
      </>}
      <hr /><h4>资源与工单 / Resources</h4>
      <p>暂存架 <b>{obs?.rack.occupiedHolders ?? '—'} / {obs?.rack.capacity ?? '—'}</b></p>
      <div className={s.capacity}>{Array.from({ length: Math.min(obs?.rack.capacity || 0, 24) }, (_, i) => <span key={i} data-filled={i < (obs?.rack.occupiedHolders || 0)} />)}</div>
      {obs?.workOrders.length ? <ul className={s.orders}>{obs.workOrders.map(w => <li key={w.partId}>{w.completed ? '✓' : '○'} {w.partId} · {w.completed ? '检修完成' : '待离架检修'}</li>)}</ul> : <p className={s.muted}>无检修工单 / No work orders</p>}
      <hr /><h4>评测视角 / Camera acquisition</h4>
      <label className={s.field}>剩余 {obs?.remainingViews ?? '—'} 次<select aria-label="Acquisition view" value={view} onChange={e => setView(e.target.value)}>{['isometric', 'front', 'rear', 'left', 'right', 'top', 'bottom', 'exploded-reference'].map(v => <option key={v}>{v}</option>)}</select></label>
      <button disabled={!canAct || !obs?.remainingViews} onClick={() => act({ type: 'inspect', view })}>获取并记录 Acquire</button>
      <label className={s.field}>已保存视角<select aria-label="Saved view" value={saved} disabled={busy} onChange={e => { setSaved(e.target.value); setFrame(undefined); setFrameObs(undefined); }}>
        <option value="">当前视角 Live</option>{obs?.inspectionHistory.map((v, i) => <option key={v.frameId} value={i}>{v.view} · revision {v.atRevision}</option>)}</select></label>
      {!probe && <><hr /><h4>自我诊断 / Diagnosis</h4><p className={s.muted}>自上次诊断后，是否有合法操作增加了可避免的未来代价？</p>
        <div className={s.actionGrid}>{[true, false].map(v => <button key={String(v)} disabled={!canAct || !obs?.remainingDiagnoses} onClick={() => act({ type: 'diagnose', avoidableError: v })}>{v ? '有错误 Yes' : '无错误 No'}</button>)}</div></>}
      <hr /><details><summary>零件图层 / Registered pieces</summary><div className={s.layers}>{obs?.registration.map(r => <button aria-pressed={selected === r.partId} key={r.partId} onClick={() => select(r.partId)}>{r.partId}<span>{r.siteId}</span></button>)}</div></details>
    </aside>
  </div>;
}
