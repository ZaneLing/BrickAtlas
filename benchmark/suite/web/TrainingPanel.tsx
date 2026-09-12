import { useEffect, useState } from 'react';
import './research.css';

interface Job {
  name: string; condition: string; seed: number; status: string; device: string;
  steps: number; targetSteps: number; trainedParameters: number; tokens: number;
  before: Record<string, number> | null; after: Record<string, number> | null;
  history: { step: number; loss: number; task: string }[];
}
export function TrainingPanel() {
  const [jobs, setJobs] = useState<Job[]>([]), [error, setError] = useState('');
  useEffect(() => {
    let live = true;
    const poll = () => fetch('/api/research/training').then(r => r.json()).then(d => { if (live) setJobs(d.jobs); }).catch(e => { if (live) setError(e.message); });
    void poll(); const timer = setInterval(() => void poll(), 5000);
    return () => { live = false; clearInterval(timer); };
  }, []);
  return <main className="training-page"><div className="heading"><div><span className="eyebrow">LOCAL TRAINING EVIDENCE</span><h2>本地训练与验证</h2></div><span className="dataset-tag">Qwen3-0.6B · LoRA · 文本/结构</span></div>
    {error && <p role="alert">{error}</p>}
    <div className="table-wrap"><table><thead><tr><th>实验</th><th>状态</th><th>设备</th><th>优化步</th><th>可训练参数</th><th>已处理 tokens</th></tr></thead>
      <tbody>{jobs.map(j => <tr key={j.name}><td>{j.name}</td><td>{j.status}</td><td>{j.device}</td><td>{j.steps}/{j.targetSteps}</td><td>{j.trainedParameters.toLocaleString()}</td><td>{j.tokens.toLocaleString()}</td></tr>)}</tbody></table></div>
    <div className="training-charts">{jobs.filter(j => j.history.length).map(j => {
      const max = Math.max(0.1, ...j.history.map(p => p.loss)), last = Math.max(1, j.targetSteps);
      const points = j.history.map(p => `${40 + 530 * p.step / last},${200 - 160 * p.loss / max}`).join(' ');
      return <section key={j.name}><h3>{j.name}</h3><svg viewBox="0 0 600 240" role="img" aria-label={`${j.name}训练损失`}>
        <path d="M40 25V200H575" stroke="#b8cbbc" fill="none" />
        <polyline points={points} stroke="#347f62" strokeWidth="2" fill="none" />
        <text x="8" y="42" fill="#738d7e" fontSize="11">{max.toFixed(2)}</text><text x="15" y="200" fill="#738d7e" fontSize="11">0</text>
        <text x="40" y="223" fill="#738d7e" fontSize="11">0</text><text x="535" y="223" fill="#738d7e" fontSize="11">{last} step</text>
      </svg><div className="table-wrap"><table><thead><tr><th>验证任务</th><th>训练前 NLL</th><th>训练后 NLL</th></tr></thead><tbody>
        {Object.keys(j.before ?? {}).map(k => <tr key={k}><td>{k}</td><td>{j.before?.[k]?.toFixed(4)}</td><td>{j.after?.[k]?.toFixed(4) ?? '待验证'}</td></tr>)}
      </tbody></table></div></section>;
    })}</div>
    <p className="trace-warning">训练损失下降不等于任务成功。这里是短程文本/结构 LoRA 基线，不是视觉模型训练；single 与 multi 匹配优化步数，但未严格匹配监督 token 和数据覆盖。</p>
  </main>;
}
