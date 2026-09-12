import { useEffect, useRef, useState } from 'react';
import { Send, ShieldCheck } from 'lucide-react';
import { viewer } from './viewer';
import type { Part } from '../shared';
import './research.css';

interface Item { id: string; family: string; structure: { parts: Part[] } }
interface Summary { queued: number; submissions: number; reviewedSamples: number; doubleReviewed: number; disagreements: number }
export function ReviewPanel({ token }: { token: string }) {
  const [items, setItems] = useState<Item[]>([]), [summary, setSummary] = useState<Summary | null>(null), [index, setIndex] = useState(0);
  const [reviewer, setReviewer] = useState(''), [judgment, setJudgment] = useState(''), [notes, setNotes] = useState('');
  const [independent, setIndependent] = useState(false), [ack, setAck] = useState(false), [message, setMessage] = useState('');
  const canvas = useRef<HTMLCanvasElement>(null), renderer = useRef<ReturnType<typeof viewer> | null>(null);
  const refresh = () => fetch('/api/research/reviews').then(r => r.json()).then(d => { setItems(d.items); setSummary(d.summary); });
  useEffect(() => {
    void refresh().catch(e => setMessage(e.message));
    renderer.current = viewer(canvas.current!, true);
    return () => renderer.current?.dispose();
  }, []);
  useEffect(() => { if (items[index]) renderer.current?.setParts(items[index].structure.parts); }, [items, index]);
  const submit = async () => {
    try {
      const response = await fetch('/api/research/reviews', { method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Benchmark-Client': token },
        body: JSON.stringify({ sampleId: items[index]?.id, reviewer, judgment, notes, independent, acknowledged: ack }) });
      const data = await response.json(); if (!response.ok) throw new Error(data.error);
      setMessage('审核已记录'); setJudgment(''); setNotes(''); setAck(false); await refresh();
    } catch (e) { setMessage((e as Error).message); }
  };
  return <main className="review-page"><div className="heading"><div><span className="eyebrow">INDEPENDENT HUMAN REVIEW</span><h2>独立审核队列</h2></div><ShieldCheck size={21} /></div>
    <div className="review-counts"><span>待审核样本 <b>{summary?.queued ?? 0}</b></span><span>真实提交 <b>{summary?.submissions ?? 0}</b></span>
      <span>双人独立审核 <b>{summary?.doubleReviewed ?? 0}</b></span><span>分歧 <b>{summary?.disagreements ?? 0}</b></span></div>
    <label>样本<select value={index} onChange={e => { setIndex(Number(e.target.value)); setJudgment(''); setNotes(''); setAck(false); }}>
      {items.map((m, i) => <option key={m.id} value={i}>{i + 1} · {m.family} · {m.id}</option>)}</select></label>
    <div className="review-grid"><div><canvas ref={canvas} width={640} height={480} aria-label="人工审核结构" />
      <details><summary>部件与位姿</summary><pre>{JSON.stringify(items[index]?.structure, null, 2)}</pre></details></div>
      <section className="review-form"><label>审核者代号<input aria-label="审核者代号" value={reviewer} onChange={e => setReviewer(e.target.value)} placeholder="reviewer_01" /></label>
        <label>判断<select aria-label="审核判断" value={judgment} onChange={e => setJudgment(e.target.value)}><option value="">未判断</option>
          <option value="acceptable">在声明的数字规则内可接受</option><option value="problem">发现问题</option><option value="uncertain">无法确定</option></select></label>
        <label>检查证据<textarea aria-label="审核证据" rows={7} value={notes} onChange={e => setNotes(e.target.value)} /></label>
        <label className="check"><input type="checkbox" checked={independent} onChange={e => setIndependent(e.target.checked)} />我独立于该样本生成与标注过程</label>
        <label className="check"><input type="checkbox" checked={ack} onChange={e => setAck(e.target.checked)} />我已实际检查，并同意保存此审核记录</label>
        <button className="command primary" disabled={!reviewer || !judgment || notes.trim().length < 8 || !ack} onClick={() => void submit()}><Send size={15} />提交人工审核</button>
        <p className="description" role="status">{message}</p>
      </section></div>
    <p className="trace-warning">只判断本系统声明的几何、连接和装配规则，不把模型渲染当作真实受力实验。独立性是审核者自述；自动测试与模型回答不计为人工审核。</p>
  </main>;
}
