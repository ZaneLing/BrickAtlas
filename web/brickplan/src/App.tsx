import { useEffect, useState } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { Blocks, LibraryBig, MousePointer2, Bot, FileDown, Menu, X, ArrowUpRight, Download } from 'lucide-react';
import { api, asset, read, staticMode } from './api';
import type { Catalogue, TaskInfo } from './types';
import { Library } from './Library';
import { Workcell } from './Workcell';
import { ModelPanel } from './ModelPanel';
import s from './Workbench.module.css';

function Release({ catalogue }: { catalogue: Catalogue }) {
  const file = (name: string) => asset(staticMode ? name : `download/${name}`);
  return <div className={s.release}>
    <div className={s.eyebrow}>PAPER / DATA / REPRODUCIBILITY</div><h1>从题目到实验，完整可复现。</h1>
    <p className={s.lead}>BrickPlan · Visual assembly planning under geometric, resource and history-dependent constraints.</p>
    <div className={s.releaseGrid}>
      <article><span>01 / MANUSCRIPT</span><h2>CVPR 论文与 Overleaf</h2><p>官方 CVPR 模板。独立源码包含正文、补充材料、参考文献、图和样式文件，可直接上传 Overleaf。</p>
        <a className={s.primary} href={file('brickplan-cvpr-overleaf.zip')} download><Download size={16} /> Overleaf ZIP</a><div className={s.inline}><a href={asset('paper.pdf')} target="_blank" rel="noreferrer">正文 PDF <ArrowUpRight size={13} /></a><a href={asset('supplement.pdf')} target="_blank" rel="noreferrer">补充材料 PDF <ArrowUpRight size={13} /></a></div></article>
      <article><span>02 / BENCHMARK</span><h2>完整运行包</h2><p>{catalogue.counts.episodes} 个交互任务、{catalogue.counts.probes} 道诊断题、评测器、精确几何与同一套 React 工作台。包含本地运行说明与模型接入协议。</p>
        <a className={s.primary} href={file(`brickplan-v${catalogue.release}-release.zip`)} download><Download size={16} /> Portable runtime ZIP</a><a href={file('questions.jsonl')} download>公开题库 JSONL · {catalogue.questions.length} records</a></article>
      <article><span>03 / EXPERIMENT PROTOCOL</span><h2>可检查的证据</h2><p>成功率、额外代价和最优率是主要指标。D1–D4 为操作长度分箱。模型案例为 2.1 历史记录，不是 2.2 新测量；大规模视觉模型与人类实验尚待完成。</p>
        <a href={file('manifest.json')}>发布校验清单 <ArrowUpRight size={13} /></a><a href={asset('VALIDITY.md')}>适用范围与限制</a><a href={asset('ASSET-LICENSES.json')}>几何资源与许可证</a></article>
    </div>
    <div className={s.releaseNote}><b>同一协议，两种使用方式</b><p>练习工作台开放自由 3D 检查。正式研究通过 study 配置运行：仅受控高清图、固定视角预算、冻结答案与服务端权威日志。模型通过公开 JSON 动作接口接入。</p><p>静态发布包已准备，可部署至静态站点或 Hugging Face；外部托管地址尚未发布。</p></div>
  </div>;
}
export default function App() {
  const query = new URLSearchParams(location.search);
  const initial = location.hash.slice(1);
  const [page, setPage] = useState(initial === 'case' ? 'models' : initial === 'release' ? 'release' : query.size || initial === 'work' ? 'work' : 'library');
  const [id, setId] = useState(query.get('probe') || query.get('task') || (initial.startsWith('q=') ? initial.slice(2) : ''));
  const [info, setInfo] = useState<TaskInfo>(), [catalogue, setCatalogue] = useState<Catalogue>(), [error, setError] = useState('');
  const [runId, setRunId] = useState('case-local'), [drawer, setDrawer] = useState(false);
  const [sessions, setSessions] = useState<Record<string, string>>({});
  useEffect(() => {
    async function boot() {
      const taskInfo = await api.info(); setInfo(taskInfo);
      if (taskInfo.study) {
        setPage('work');
        const probes = await read<{ probes: { id: string; kind: string }[] }>('api/probes');
        const assignments = [...taskInfo.tasks.map(t => ({ ...t, form: 'episode' })), ...probes.probes.map(p => ({ ...p, sessions: [], form: 'probe' }))];
        setCatalogue({ release: '2.2', questions: assignments.map(a => ({ id: a.id, stableId: '', category: '', form: a.form, kind: '', source: '', profile: '', split: '', tier: '', lengthBin: '' })), taxonomy: [], counts: { episodes: taskInfo.tasks.length, probes: probes.probes.length, pairs: 0, sources: 0 }, lengthNotice: { zh: '', en: '' } });
        setId(current => current || taskInfo.tasks.find(t => t.sessions.includes(query.get('session') || ''))?.id || assignments[0]?.id || '');
      } else {
        const cat = await api.catalogue(); setCatalogue(cat);
        const samples = await api.sampleIds();
        setId(current => current || taskInfo.tasks.find(t => t.sessions.includes(query.get('session') || ''))?.id || samples[0] || cat.questions.find(q => q.category === 'assembly')!.id);
      }
    }
    boot().catch(e => setError(e.message));
  }, []);
  const navigate = (next: string) => {
    setPage(next); setDrawer(false);
    if (next !== 'work') history.replaceState(null, '', `#${next === 'models' ? 'case' : next === 'library' ? `q=${id}` : next}`);
  };
  const choose = (next: string) => { setId(next); history.replaceState(null, '', page === 'work' ? `?${next.startsWith('Q') ? 'probe' : 'task'}=${next}#work` : `#q=${next}`); };
  const nav = <><div className={s.brand}><Blocks size={28} /><div>BrickPlan<small>ASSEMBLY INTELLIGENCE</small></div></div>
    <div className={s.navLabel}>WORKBENCH / {catalogue?.release || '2.2'}</div><nav>{[
      ['library', LibraryBig, '题目库', 'Question library'], ['work', MousePointer2, '人类作答', 'Human workspace'],
      ['models', Bot, '模型运行', 'Model runs'], ['release', FileDown, '论文与下载', 'Paper & release'],
    ].filter(([key]) => !info?.study || key === 'work').map(([key, Icon, label, english]) => {
      const C = Icon as typeof Blocks;
      return <button key={String(key)} aria-current={page === key ? 'page' : undefined} onClick={() => navigate(String(key))}><C size={18} /><span>{String(label)}<small>{String(english)}</small></span></button>;
    })}</nav><div className={s.sidebarFoot}><span className={s.liveDot} />{staticMode ? 'STATIC / READ ONLY' : info?.study ? 'CONTROLLED STUDY' : 'LOCAL PRACTICE'}<p>Geometry. Resources.<br />Decisions over time.</p></div></>;
  return <div className={s.app}>
    <aside className={s.sidebar}>{nav}</aside>
    <div className={s.shell}>
      <header className={s.topbar}>
        <Dialog.Root open={drawer} onOpenChange={setDrawer}><Dialog.Trigger className={s.mobileMenu} aria-label="打开导航 Open navigation"><Menu size={20} /></Dialog.Trigger><Dialog.Portal><Dialog.Overlay className={s.overlay} /><Dialog.Content className={s.navDrawer}><Dialog.Title className={s.srOnly}>Navigation</Dialog.Title><Dialog.Description className={s.srOnly}>Workbench sections</Dialog.Description><Dialog.Close className={s.drawerClose} aria-label="Close navigation"><X size={18} /></Dialog.Close>{nav}</Dialog.Content></Dialog.Portal></Dialog.Root>
        <span>VISUAL ASSEMBLY BENCHMARK</span><div><span className={s.badge}>{staticMode ? '静态预览' : info?.study ? '正式评测' : '练习模式 Practice'} · {info?.track}</span><span>1920 × 1440 · {info?.study ? 'Controlled images' : 'WebGL 2'}</span></div>
      </header>
      {!catalogue || !info ? <div className={s.empty} role="status">{error || '正在载入题库… / Loading…'}</div> :
        page === 'library' && !info.study ? <Library catalogue={catalogue} id={id} onSelect={choose} onPlay={() => { history.replaceState(null, '', `?${id.startsWith('Q') ? 'probe' : 'task'}=${id}#work`); navigate('work'); }} /> :
        page === 'models' && !info.study ? <ModelPanel catalogue={catalogue} runId={runId} onRun={setRunId} /> :
        page === 'release' && !info.study ? <Release catalogue={catalogue} /> :
        <><div className={s.assignment}><label>题目 / Assignment <select aria-label="Workspace question" value={id} onChange={e => choose(e.target.value)}>{catalogue.questions.map(q => <option key={q.id} value={q.id}>{q.id} {q.tier && `· ${q.tier} · ${q.kind}`}</option>)}</select></label></div>{id && <Workcell key={id} id={id} info={info} catalogue={catalogue} resumeId={sessions[id]} onSession={sid => setSessions(previous => ({ ...previous, [id]: sid }))} />}</>}
    </div>
  </div>;
}
