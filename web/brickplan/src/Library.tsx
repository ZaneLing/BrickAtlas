import { useEffect, useMemo, useState } from 'react';
import { ArrowUpRight, Search, ArrowLeft, ArrowRight } from 'lucide-react';
import type { Catalogue, Preview, SceneData } from './types';
import { api, staticMode } from './api';
import { Brief } from './Workcell';
import { JSONView, SavedViews, Visuals } from './Visuals';
import s from './Workbench.module.css';

export function Library({ catalogue, id, onSelect, onPlay }: { catalogue: Catalogue; id: string; onSelect: (id: string) => void; onPlay: () => void }) {
  const [family, setFamily] = useState(catalogue.questions.find(q => q.id === id)?.category || 'assembly');
  const [search, setSearch] = useState(''), [tier, setTier] = useState(''), [page, setPage] = useState(0);
  const [split, setSplit] = useState(''), [cohort, setCohort] = useState(''), [saved, setSaved] = useState('');
  const [preview, setPreview] = useState<Preview>(), [scene, setScene] = useState<SceneData>(), [error, setError] = useState('');
  const [sampleIds, setSampleIds] = useState<string[]>([]);
  useEffect(() => { api.sampleIds().then(setSampleIds).catch(e => setError(e.message)); }, []);
  useEffect(() => {
    let alive = true; setError(''); setPreview(undefined); setScene(undefined); setSaved('');
    api.preview(id).then(p => { if (alive) setPreview(p); }).catch(e => { if (alive) setError(e.message); });
    api.scene(id).then(p => { if (alive) setScene(p); }).catch(e => { if (alive) setError(e.message); });
    return () => { alive = false; };
  }, [id]);
  const rows = useMemo(() => catalogue.questions.filter(q => q.category === family && (!tier || q.tier === tier) && (!split || q.split === split) &&
    (!cohort || q.evaluationCohort === cohort) &&
    `${q.id} ${q.stableId} ${q.source} ${q.profile} ${q.kind}`.toLowerCase().includes(search.toLowerCase())), [catalogue, family, tier, split, cohort, search]);
  const selectFamily = (key: string) => {
    setFamily(key); setSearch(''); setTier(''); setSplit(''); setCohort(''); setPage(0);
    const candidates = catalogue.questions.filter(q => q.category === key);
    onSelect((candidates.find(q => sampleIds.includes(q.id)) || candidates[0]).id);
  };
  return <div className={s.library}>
    <div className={s.pageHeader}><div><div className={s.eyebrow}>BRICKPLAN {catalogue.release} / QUESTION LIBRARY</div><h1>先看懂题目，再开始规划。</h1><p>Inspect the task. Plan the assembly. Trace every decision.</p></div>
      <div className={s.census}><div><b>{catalogue.counts.episodes}</b><span>交互任务</span></div><div><b>{catalogue.counts.probes}</b><span>诊断题</span></div><div><b>{catalogue.counts.sources}</b><span>独立来源 Sources</span></div><div><b>{catalogue.taxonomy.length}</b><span>任务类别</span></div></div>
    </div>
    <div className={s.families}>{catalogue.taxonomy.map(f => <button key={f.id} aria-pressed={family === f.id} onClick={() => selectFamily(f.id)}>
      <span className={s.familyNumber}>{f.number}</span><b>{f.name.zh}</b><span>{f.count} questions</span>
    </button>)}</div>
    <div className={s.libraryBody}>
      <section className={s.questionList} aria-label="Question catalogue">
        <div className={s.listFilters}><label className={s.search}><Search size={15} /><input aria-label="Search questions" placeholder="搜索 ID / source…" value={search} onChange={e => { setSearch(e.target.value); setPage(0); }} /></label>
          <select aria-label="Length bin" value={tier} onChange={e => { setTier(e.target.value); setPage(0); }}><option value="">全部长度</option>{['D1', 'D2', 'D3', 'D4'].map(d => <option key={d}>{d}</option>)}</select>
          <select aria-label="Dataset split" value={split} onChange={e => { setSplit(e.target.value); setPage(0); }}><option value="">全部分组</option><option value="development">Development</option><option value="heldout-source">Held-out source</option></select>
          {family === 'geometry' && <select aria-label="Geometry cohort" value={cohort} onChange={e => { setCohort(e.target.value); setPage(0); }}><option value="">All geometry / appearance</option>{catalogue.cohorts?.map(c => <option key={c.id} value={c.id}>{c.label.en}</option>)}</select>}</div>
        <div className={s.listCaption}>{rows.length} questions <span>ID / LENGTH / SOURCE</span></div>
        <div>{rows.slice(page * 18, (page + 1) * 18).map(q => <button className={s.questionRow} aria-pressed={q.id === id} key={q.id} onClick={() => onSelect(q.id)}>
          <div><b>{q.id}</b><span>{q.tier} · {q.lengthBin} ops</span>{sampleIds.includes(q.id) && <i>3D sample</i>}</div><small>{q.profile}</small><span>{q.form === 'episode' ? '交互任务' : '诊断题'} · {q.split}</span>
        </button>)}</div>
        <div className={s.pagination}><button aria-label="Previous question page" disabled={page === 0} onClick={() => setPage(p => p - 1)}><ArrowLeft size={14} /></button><span>{page + 1} / {Math.max(1, Math.ceil(rows.length / 18))}</span><button aria-label="Next question page" disabled={(page + 1) * 18 >= rows.length} onClick={() => setPage(p => p + 1)}><ArrowRight size={14} /></button></div>
        {family === 'geometry' && <div className={s.listNote} aria-label="Geometry cohort census">{catalogue.cohorts?.map(c => <p key={c.id}><b>{c.label.en}</b><br />{c.probes} questions · {c.pairs} pairs · {c.sources} sources · {c.heldoutSources} held-out sources</p>)}<p>Practice metadata only. Cohorts are reported separately, never pooled.</p></div>}
        <p className={s.listNote}>{catalogue.lengthNotice.zh}</p>
      </section>
      <section className={s.preview}>
        <Brief catalogue={catalogue} id={id} />
        {!!preview?.observation.inspectionHistory.length && <div className={s.visualToolbar}><SavedViews observation={preview.observation} value={saved} onChange={setSaved} /></div>}
        <Visuals data={saved === '' ? scene : undefined} study={saved !== ''}
          images={saved === '' ? preview?.observation.images : preview?.observation.inspectionHistory[+saved]?.images} />
        <div className={s.previewFooter}><span>{error || (preview ? `${preview.observation.partIds.length} registered pieces · ${preview.observation.workOrders.length} work orders` : '正在加载原始网格与高清图…')}</span>
          <button className={s.primary} onClick={onPlay}>{staticMode ? '查看题目详情' : '进入作答工作区'}<ArrowUpRight size={16} /></button></div>
        {preview?.proposedPlan && <details className={s.details}><summary>完整候选序列 / Full proposed sequence ({preview.proposedPlan.length} steps)</summary><JSONView value={preview.proposedPlan} /></details>}
        <JSONView value={preview} title="题目公开输入 / Public question record" />
      </section>
    </div>
  </div>;
}
