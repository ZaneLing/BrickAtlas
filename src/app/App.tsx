import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowDownToLine, ArrowLeft, ArrowRight, Box, Boxes, Check, ChevronDown, ChevronRight,
  BookOpen, CircleDot, Crosshair, Expand, ExternalLink, Eye, EyeOff, FileDown, Focus, Grid2X2, Hand, Info, Layers3,
  Languages, Library, LoaderCircle, Minus, Pause, Play, Plus, Rotate3D, RotateCcw, Search, Settings2, ShieldCheck,
  SkipBack, SkipForward, Upload, X,
} from 'lucide-react';
import { AtlasScene } from '../scene/AtlasScene';
import { PartPreviewScene } from '../scene/PartPreview';
import { colorLabels, searchInstances, visibleInstances, type AtlasManifest, type ExplorerState, type GroupId, type PartInstance } from '../model/types';
import { BrickModel } from '../model/BrickModel';
import { useViewerStore } from '../store/viewerStore';
import { BrickAtlasMark } from '../ui/BrickAtlasMark';
import { IconButton, Modal } from '../ui/Controls';
import { diagnosticsReport, installDiagnostics, recordDiagnostic } from './diagnostics';
import { modelCatalog, type ModelConfig } from '../../atlas.config';
import { exportBuildGuide, groupStepParts } from '../instructions/exportGuide';
import { localCategory, localGroupName, useLocale, type Locale, type Translator } from './locale';
import { LandingShowcase } from './LandingShowcase';
import { ImageBrickStudio } from '../creator/ImageBrickStudio';

declare global { interface Window { __atlas?: () => ReturnType<AtlasScene['snapshot']> } }
const viewNames = (tr: Translator) => ({
  perspective: tr('三分之四', 'Perspective'), front: tr('正面', 'Front'), side: tr('侧面', 'Side'),
  rear: tr('背面', 'Rear'), top: tr('顶部', 'Top'),
});

function download(data: string, file: string, type: string) {
  const url = URL.createObjectURL(new Blob([data], { type }));
  const link = document.createElement('a');
  link.href = url; link.download = file; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function downloadBlob(blob: Blob, file: string) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url; link.download = file; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function LanguageButton({ locale, onToggle, tr }: { locale: Locale; onToggle: () => void; tr: Translator }) {
  return <button className="language-button" onClick={onToggle} aria-label={tr('切换为英文', 'Switch to Chinese')} title={tr('切换为英文', 'Switch to Chinese')}><Languages size={14} /><span>{locale === 'zh' ? 'EN' : '中'}</span></button>;
}

function SelectedPartPreview({ scene, part, onClose, tr }: { scene: AtlasScene; part: PartInstance; onClose: () => void; tr: Translator }) {
  const hostRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const data = scene.getPartPreview(part.instanceId);
    if (!data || !hostRef.current) return;
    const preview = new PartPreviewScene(hostRef.current, data, tr('选中积木可旋转三维预览', 'Selected brick interactive 3D preview'));
    return () => preview.dispose();
  }, [scene, part.instanceId, tr]);
  return <section className="part-preview-window" aria-label={tr('选中积木三维预览', 'Selected brick 3D preview')}>
    <header><span><Rotate3D size={14} />{part.partNumber}</span><IconButton label={tr('关闭积木预览', 'Close brick preview')} onClick={onClose}><X size={14} /></IconButton></header>
    <div className="part-preview-canvas" ref={hostRef} />
    <footer><strong>{part.displayName}</strong><span><i style={{ background: part.colorHex }} />{tr(colorLabels[part.colorCode] ?? part.colorName, part.colorName)}</span></footer>
  </section>;
}

export function ExplorerWorkspace({ config, mode, locale, tr, toggleLocale }: { config: ModelConfig; mode: 'explore' | 'build'; locale: Locale; tr: Translator; toggleLocale: () => void }) {
  const base = `${import.meta.env.BASE_URL}models/${config.id}/`;
  const [manifest, setManifest] = useState<AtlasManifest | null>(null);
  const state = useViewerStore(store => store.viewer);
  const setState = useViewerStore(store => store.update);
  const patch = useViewerStore(store => store.patch);
  const loadModel = useViewerStore(store => store.loadModel);
  const resetViewer = useViewerStore(store => store.reset);
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState(tr('读取实例清单', 'Reading brick manifest'));
  const [error, setError] = useState<string | null>(null);
  const [retry, setRetry] = useState(0);
  const [query, setQuery] = useState('');
  const [tab, setTab] = useState<'structure' | 'parts'>('structure');
  const [detailsOpen, setDetailsOpen] = useState(true);
  const [modal, setModal] = useState<'credits' | 'settings' | null>(null);
  const [hover, setHover] = useState<{ part: PartInstance; x: number; y: number } | null>(null);
  const [readyTime, setReadyTime] = useState<number | null>(null);
  const [notice, setNotice] = useState('');
  const [playing, setPlaying] = useState(false);
  const [panMode, setPanMode] = useState(mode === 'build');
  const [exportSize, setExportSize] = useState(3840);
  const [instructionFrames, setInstructionFrames] = useState<string[]>([]);
  const [instructionFrame, setInstructionFrame] = useState(0);
  const [openInstructionStep, setOpenInstructionStep] = useState<number | null>(null);
  const [guideExport, setGuideExport] = useState<{ current: number; total: number } | null>(null);
  const stageRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<AtlasScene | null>(null);
  const manifestRef = useRef<AtlasManifest | null>(null);
  const focusAfter = useRef(false);
  const focusStepAfter = useRef<number | null>(null);
  useEffect(installDiagnostics, []);
  useEffect(() => { if (error) recordDiagnostic('model-error', { message: error }); }, [error]);

  const selectPart = useCallback((id: string | null, focus = false) => {
    const m = manifestRef.current;
    if (!m) return;
    const part = m.instances.find(p => p.instanceId === id);
    if (!part) { setState(s => ({ ...s, selection: [] })); return; }
    focusAfter.current = focus;
    setState(s => ({
      ...s, selection: [part.instanceId],
      hiddenGroups: s.hiddenGroups.filter(g => g !== part.groupId),
      isolation: s.isolation && !s.isolation.includes(part.instanceId) ? null : s.isolation,
    }));
    if (mode !== 'build') setDetailsOpen(true);
  }, [mode]);

  useEffect(() => {
    const abort = new AbortController();
    setLoading(true); setError(null); setProgress(0);
    fetch(`${base}manifest.json`, { signal: abort.signal })
      .then(async response => {
        if (!response.ok) throw new Error(`manifest.json: HTTP ${response.status}`);
        const m = await response.json() as AtlasManifest;
        if (m.version !== 1 || !Array.isArray(m.instances) || !Array.isArray(m.chunks) || !m.instances.length) throw new Error(tr('实例清单格式无效', 'Invalid model manifest'));
        if (!abort.signal.aborted) {
          loadModel(config.id, mode, m.instructions?.steps.length ?? 0);
          setManifest(m); manifestRef.current = m;
        }
      })
      .catch(e => { if (!abort.signal.aborted) { setError(`${tr('模型载入失败', 'Model failed to load')}: ${e.message}`); setLoading(false); } });
    return () => abort.abort();
  }, [retry, config.id, mode, base, loadModel]);

  const brickModel = useMemo(() => manifest ? new BrickModel(manifest) : null, [manifest]);
  useEffect(() => {
    if (!brickModel || !stageRef.current) return;
    let scene: AtlasScene | null = null;
    try {
      scene = new AtlasScene(stageRef.current, brickModel, {
        progress: (value, label) => { setProgress(value); setStage(label); },
        ready: () => {
          setLoading(false); setReadyTime(scene?.metrics.readyMs ?? null);
          recordDiagnostic('model-ready', { ...scene?.metrics });
        },
        error: message => { setError(message); setLoading(false); },
        select: id => selectPart(id),
        hover: (part, x, y) => setHover(part ? { part, x, y } : null),
      }, locale);
      sceneRef.current = scene;
      window.__atlas = () => scene!.snapshot();
    } catch (e) {
      setError(`${tr('无法初始化 3D 视图', 'Unable to initialize the 3D view')}: ${e instanceof Error ? e.message : String(e)}. ${tr('请确认浏览器已启用 WebGL 2。', 'Make sure WebGL 2 is enabled.')}`);
      setLoading(false);
    }
    return () => { scene?.dispose(); sceneRef.current = null; delete window.__atlas; };
  }, [brickModel, selectPart]);

  useEffect(() => {
    sceneRef.current?.setState(state);
    if (focusAfter.current) { sceneRef.current?.focusSelection(); focusAfter.current = false; }
    if (focusStepAfter.current !== null) {
      sceneRef.current?.focusBuildStep(focusStepAfter.current);
      focusStepAfter.current = null;
    }
  }, [state, manifest]);
  useEffect(() => { sceneRef.current?.setLocale(locale); }, [locale]);
  useEffect(() => { sceneRef.current?.setPanMode(panMode); }, [panMode, readyTime]);
  useEffect(() => {
    if (!notice) return;
    const timeout = setTimeout(() => setNotice(''), 2500);
    return () => clearTimeout(timeout);
  }, [notice]);
  const selected = manifest?.instances.find(p => state.selection.includes(p.instanceId));
  const selectedBrick = selected ? brickModel?.getBrick(selected.instanceId) : undefined;
  const selectedGroup = manifest?.groups.find(g => g.id === selected?.groupId);
  const selectedAssembly = manifest?.submodels.find(group => group.id === selected?.parentSubmodelId);
  const sameType = useMemo(() => manifest?.instances.filter(p => p.partNumber === selected?.partNumber) ?? [], [manifest, selected]);
  const visible = useMemo(() => manifest ? visibleInstances(manifest, state) : [], [manifest, state]);
  const results = useMemo(() => manifest ? searchInstances(manifest, query) : [], [manifest, query]);
  const steps = manifest?.instructions?.steps ?? [];
  const currentBuildStep = state.buildStep ?? 0;
  const activeStep = currentBuildStep > 0 ? steps[currentBuildStep - 1] : null;
  const activeStepParts = activeStep?.instanceIds.map(id => manifest?.instances.find(part => part.instanceId === id)).filter(Boolean) as PartInstance[] | undefined;
  const activePartGroups = useMemo(() => groupStepParts(activeStepParts ?? []), [activeStepParts]);
  const instructionDisclaimer = locale === 'zh' ? manifest?.instructions?.disclaimer
    : manifest?.instructions?.provenance === 'source'
      ? 'Steps follow the OMR author metadata; page numbers do not match official printed instructions.'
      : 'The source has no STEP metadata. This is an editorial structural guide, not an official instruction sequence.';
  const stepTitle = useCallback((step: (typeof steps)[number]) => {
    if (locale === 'zh') return step.title;
    const ids = step.motionInstanceIds ?? step.instanceIds;
    const part = manifest?.instances.find(item => ids.includes(item.instanceId));
    const group = part ? manifest?.groups.find(item => item.id === part.groupId) : null;
    const section = group && part ? localGroupName(locale, part.groupId, group.name) : 'Assembly';
    return `${section} · ${step.kind === 'placement' ? 'Place subassembly' : manifest?.instructions?.provenance === 'source' ? `Source step ${step.sourceStep ?? ''}`.trim() : 'Build subassembly'}`;
  }, [locale, manifest, steps]);
  const resultGroups = useMemo(() => {
    const map = new Map<string, PartInstance[]>();
    for (const part of results) {
      const key = `${part.partNumber}:${part.colorCode}`;
      if (!map.has(key)) map.set(key, []);
      map.get(key)!.push(part);
    }
    return [...map.values()];
  }, [results]);
  const colors = useMemo(() => {
    const map = new Map<string, { hex: string; name: string; count: number }>();
    manifest?.instances.forEach(p => {
      const item = map.get(p.colorCode) ?? { hex: p.colorHex, name: p.colorName, count: 0 };
      item.count++; map.set(p.colorCode, item);
    });
    return [...map.entries()].sort((a, b) => b[1].count - a[1].count);
  }, [manifest]);
  useEffect(() => {
    patch({ highlightedBrickIds: query ? results.map(part => part.instanceId) : [] });
  }, [query, results, patch]);
  useEffect(() => {
    if (mode !== 'build') return;
    setOpenInstructionStep(currentBuildStep || null);
    if (currentBuildStep < 1) return;
    requestAnimationFrame(() => {
      document.querySelector(`[data-instruction-step="${currentBuildStep}"]`)
        ?.scrollIntoView({ block: 'nearest' });
    });
  }, [mode, currentBuildStep, config.id]);
  useEffect(() => {
    if (!playing || mode !== 'build') return;
    if (currentBuildStep >= steps.length) { setPlaying(false); return; }
    const timer = setTimeout(() => {
      focusStepAfter.current = currentBuildStep + 1;
      patch({ buildStep: currentBuildStep + 1, assemblyRevision: state.assemblyRevision + 1 });
    }, 1150);
    return () => clearTimeout(timer);
  }, [playing, mode, currentBuildStep, steps.length, patch, state.assemblyRevision]);
  useEffect(() => {
    if (mode !== 'build' || !readyTime || currentBuildStep < 1 || !sceneRef.current) {
      setInstructionFrames([]);
      return;
    }
    let cancelled = false;
    const urls: string[] = [];
    const timer = setTimeout(() => {
      Promise.all([0, 0.12, 0.28, 0.46, 0.64, 0.8, 0.92, 1, 1, 1].map(progress =>
        sceneRef.current!.captureBuildStep(currentBuildStep, 560, 420, {
          progress,
          focusStep: true,
          shadows: false,
          motionInstanceId: activeStep?.kind === 'placement' ? undefined : activeStep?.instanceIds[0],
        }),
      )).then(async blobs => {
        const nextUrls = blobs.map(blob => URL.createObjectURL(blob));
        await Promise.all(nextUrls.map(url => new Promise<void>(resolve => {
          const image = new Image();
          image.onload = () => resolve();
          image.onerror = () => resolve();
          image.src = url;
        })));
        if (cancelled) {
          nextUrls.forEach(url => URL.revokeObjectURL(url));
          return;
        }
        urls.push(...nextUrls);
        setInstructionFrame(0);
        setInstructionFrames(urls);
      }).catch(() => {});
    }, 180);
    return () => {
      cancelled = true;
      clearTimeout(timer);
      urls.forEach(url => URL.revokeObjectURL(url));
    };
  }, [mode, readyTime, currentBuildStep, activeStep]);
  useEffect(() => {
    if (instructionFrames.length < 2) return;
    const timer = setInterval(() => setInstructionFrame(index => (index + 1) % instructionFrames.length), 300);
    return () => clearInterval(timer);
  }, [instructionFrames]);

  function reset() {
    resetViewer(mode);
    setQuery(''); setDetailsOpen(true); setHover(null); setPanMode(mode === 'build');
  }
  function toggleGroup(id: GroupId) {
    setState(s => ({ ...s, hiddenGroups: s.hiddenGroups.includes(id) ? s.hiddenGroups.filter(g => g !== id) : [...s.hiddenGroups, id] }));
  }
  function isolate(ids: string[]) {
    setState(s => ({ ...s, isolation: ids, hiddenGroups: [], hiddenBrickIds: [], autoRotate: false }));
  }
  function selectAllType() {
    setState(s => ({ ...s, selection: sameType.map(p => p.instanceId), hiddenGroups: s.hiddenGroups.filter(g => !sameType.some(p => p.groupId === g)), isolation: null }));
  }
  function exportInventory() {
    const rows = [['instanceId', 'partNumber', 'name', 'color', 'group', 'sourceFile', 'sourceLine', 'step']];
    for (const p of visible) rows.push([p.instanceId, p.partNumber, p.displayName, p.colorName, p.groupId, p.sourceFile, String(p.sourceLine), p.buildStep === null ? '' : String(p.buildStep)]);
    download('\uFEFF' + rows.map(row => row.map(v => `"${v.replaceAll('"', '""')}"`).join(',')).join('\n'), `${config.id}-inventory.csv`, 'text/csv;charset=utf-8');
    setNotice(tr('零件清单已导出', 'Inventory exported'));
  }
  async function screenshot() {
    if (!sceneRef.current) return;
    try {
      const blob = await sceneRef.current.exportPng(exportSize, Math.round(exportSize * 9 / 16));
      downloadBlob(blob, `brick-atlas-${config.id}-${exportSize}p.png`);
      setNotice(tr(`${exportSize}px 高清模型图已导出`, `${exportSize}px model image exported`));
    } catch (cause) {
      setNotice(cause instanceof Error ? cause.message : tr('高清导出失败', 'High-resolution export failed'));
    }
  }
  function setBuildStep(step: number) {
    const next = Math.max(0, Math.min(steps.length, step));
    focusStepAfter.current = next || null;
    patch({ buildStep: next, explosion: 0, autoRotate: false, isolation: null, assemblyRevision: state.assemblyRevision + 1 });
  }
  function toggleInstructionStep(step: number) {
    if (openInstructionStep === step) {
      setOpenInstructionStep(null);
      return;
    }
    setOpenInstructionStep(step);
    setBuildStep(step);
  }
  async function exportInstructions() {
    if (!sceneRef.current || !manifest?.instructions) return;
    setPlaying(false);
    setGuideExport({ current: 0, total: manifest.instructions.steps.length });
    try {
      const blob = await exportBuildGuide(sceneRef.current, config, manifest, (current, total) => setGuideExport({ current, total }));
      downloadBlob(blob, `brick-atlas-${config.id}-build-guide.pdf`);
      setNotice(tr('完整拼装说明书 PDF 已导出', 'Complete build guide PDF exported'));
    } catch (cause) {
      setNotice(cause instanceof Error ? cause.message : tr('说明书导出失败', 'Build guide export failed'));
    } finally {
      setGuideExport(null);
    }
  }

  return <div className={`app ${mode}-mode`}>
    <header className="topbar">
      <a href={import.meta.env.BASE_URL} className="icon-button workspace-back" aria-label={tr('返回项目库', 'Back to library')} title={tr('返回项目库', 'Back to library')}><ArrowLeft size={18} /></a>
      <a href={import.meta.env.BASE_URL} className="brand" aria-label={tr('Brick Atlas 首页', 'Brick Atlas home')}>
        <span className="brand-mark"><BrickAtlasMark /></span>
        <strong>BRICK<span>ATLAS</span></strong>
      </a>
      <div className="top-divider" />
      <span className="workspace-label">{mode === 'build' ? tr('分步拼装工作台', 'Build workspace') : tr('模型探索空间', 'Model explorer')}</span>
      <div className="top-search"><Search size={16} /><input aria-label={tr('顶部搜索零件', 'Global brick search')} placeholder={tr('搜索 Part ID、名称、子装配', 'Search part ID, name, assembly')} value={query} onChange={event => setQuery(event.target.value)} /></div>
      <div className="top-actions">
        <a className="text-button source-button" href={import.meta.env.BASE_URL}><Library size={16} />{tr('项目库', 'Library')}</a>
        <a className="text-button source-button" href={`${import.meta.env.BASE_URL}${mode === 'build' ? 'explore' : 'build'}/${config.id}`}>{mode === 'build' ? <Layers3 size={16} /> : <BookOpen size={16} />}{mode === 'build' ? tr('探索', 'Explore') : tr('拼装', 'Build')}</a>
        {mode === 'build' && <button className="text-button source-button" disabled={!!guideExport || loading} onClick={exportInstructions}><FileDown size={16} />{tr('导出说明书', 'Export guide')}</button>}
        <IconButton label={tr('X-Ray 透视模式', 'X-Ray mode')} active={state.xray} onClick={() => patch({ xray: !state.xray })}><Eye size={18} /></IconButton>
        <button className="text-button source-button" onClick={() => setModal('credits')}><Info size={16} />{tr('来源与署名', 'Credits')}</button>
        <IconButton label={tr('显示设置', 'Display settings')} onClick={() => setModal('settings')}><Settings2 size={18} /></IconButton>
        <IconButton label={tr('导出模型截图', 'Export model image')} disabled={loading || !!error} onClick={screenshot}><ArrowDownToLine size={18} /></IconButton>
        <LanguageButton locale={locale} onToggle={toggleLocale} tr={tr} />
      </div>
    </header>

    <div className={`workspace ${detailsOpen ? '' : 'details-collapsed'}`}>
      <aside className="sidebar left-sidebar" aria-label={tr('模型结构与搜索', 'Model structure and search')}>
        <div className="set-heading">
          <div className="eyebrow"><span className="set-number">{config.id}</span><span>{config.theme.split(' ')[0].toUpperCase()} / {config.year}</span></div>
          <h1>{config.title}</h1>
          <div className="set-subtitle">{locale === 'zh' ? config.subtitle : config.title} <span className="tiny-divider" /> {config.theme.replace('Creator ', '')}</div>
          <label className="model-switcher"><Library size={15} /><span>{tr('切换模型', 'Model')}</span><select aria-label={tr('切换模型', 'Switch model')} value={config.id} onChange={event => { location.href = `${import.meta.env.BASE_URL}${mode}/${event.target.value}`; }}>{modelCatalog.map(model => <option key={model.id} value={model.id}>{model.setNumber} · {model.title}</option>)}</select><ChevronDown size={12} /></label>
          <div className="set-stats"><div><strong>{manifest?.stats.instances ?? '—'}</strong><span>{tr('零件实例', 'Bricks')}</span></div><div><strong>{manifest?.stats.uniqueParts ?? '—'}</strong><span>{tr('零件型号', 'Part types')}</span></div><div><strong>{manifest?.stats.colors ?? '—'}</strong><span>{tr('颜色', 'Colors')}</span></div></div>
        </div>
        <div className="search-wrap"><Search size={17} /><input aria-label={tr('搜索零件', 'Search bricks')} placeholder={tr('搜索零件、颜色、编号', 'Search part, color, ID')} value={query} onChange={e => { setQuery(e.target.value); if (e.target.value) setTab('parts'); }} />{query && <IconButton label={tr('清空搜索', 'Clear search')} onClick={() => setQuery('')}><X size={14} /></IconButton>}</div>
        <div className="panel-tabs" role="tablist" aria-label={tr('浏览方式', 'Browse mode')}>
          <button role="tab" aria-selected={tab === 'structure'} onClick={() => setTab('structure')}><Layers3 size={16} />{tr('结构分组', 'Structure')}</button>
          <button role="tab" aria-selected={tab === 'parts'} onClick={() => setTab('parts')}><Boxes size={16} />{tr('零件清单', 'Parts')}</button>
        </div>
        <div className="panel-scroll">
          {tab === 'structure' ? <>
            <div className="list-heading"><span>{tr('结构层级', 'Structure tree')}</span><button onClick={() => patch({ hiddenGroups: [], hiddenBrickIds: [], isolation: null })}>{tr('全部显示', 'Show all')}</button></div>
            <button className="root-row" onClick={() => patch({ hiddenGroups: [], hiddenBrickIds: [], isolation: null })}><ChevronDown size={15} /><Box size={17} /><strong>{tr('完整模型', 'Complete model')}</strong><span>{manifest?.stats.instances ?? 0}</span></button>
            <div className="group-list">{manifest?.groups.map(group => {
              const count = visible.filter(p => p.groupId === group.id).length;
              const hidden = state.hiddenGroups.includes(group.id);
              return <div className={`group-row ${hidden ? 'hidden-group' : ''}`} key={group.id}>
                <span className="tree-line" /><span className="group-dot" style={{ background: group.color }} />
                <button className="group-name" onClick={() => isolate(group.instanceIds)} title={tr(`只看${group.name}`, `Isolate ${localGroupName(locale, group.id, group.name)}`)}>{localGroupName(locale, group.id, group.name)}</button>
                <span className="group-count">{count}</span>
                <IconButton label={hidden
                  ? tr(`显示${localGroupName(locale, group.id, group.name)}`, `Show ${localGroupName(locale, group.id, group.name)}`)
                  : tr(`隐藏${localGroupName(locale, group.id, group.name)}`, `Hide ${localGroupName(locale, group.id, group.name)}`)
                } active={undefined} onClick={() => toggleGroup(group.id)}>{hidden ? <EyeOff size={15} /> : <Eye size={15} />}</IconButton>
              </div>;
            })}</div>
            <div className="section-rule" />
            <div className="list-heading"><span>{tr('原始子模型', 'Source submodels')}</span><span>{manifest?.submodels.length ?? 0}</span></div>
            <div className="submodel-list">{manifest?.submodels.filter(s => s.parentId).map(submodel => <button key={submodel.id} onClick={() => isolate(manifest.instances.filter(p => p.parentSubmodelId === submodel.id).map(p => p.instanceId))}><Box size={14} /><span>{submodel.name}</span><ChevronRight size={13} /></button>)}</div>
          </> : <>
            <div className="list-heading"><span>{query ? tr('搜索结果', 'Search results') : tr('所有零件', 'All parts')}</span><span>{results.length} {tr('个实例', 'instances')}</span></div>
            {resultGroups.length === 0 ? <div className="empty-results"><Search size={24} /><strong>{tr('没有匹配的零件', 'No matching parts')}</strong><button className="text-button" onClick={() => setQuery('')}>{tr('清空筛选', 'Clear filters')}</button></div> : resultGroups.map(parts => {
              const part = parts[0];
              return <button key={`${part.partNumber}:${part.colorCode}`} className={`part-row ${state.selection.some(id => parts.some(p => p.instanceId === id)) ? 'selected' : ''}`} onClick={() => selectPart(part.instanceId, true)}>
                <span className="part-swatch" style={{ backgroundColor: part.colorHex }}><Box size={19} color={['15', '19', '47', '71'].includes(part.colorCode) ? '#53615b' : '#ffffff'} strokeWidth={1.3} /></span>
                <span className="part-row-text"><strong>{part.displayName}</strong><small>{part.partNumber}<span>·</span>{tr(colorLabels[part.colorCode] ?? part.colorName, part.colorName)}</small></span><span className="quantity">{parts.length}</span>
              </button>;
            })}
          </>}
        </div>
        <div className="sidebar-footer"><span className="status-dot" /><span>{visible.length} / {manifest?.stats.instances ?? 0} {tr('个实例可见', 'visible')}</span><IconButton label={tr('导出可见零件 CSV', 'Export visible parts CSV')} disabled={!manifest} onClick={exportInventory}><ArrowDownToLine size={15} /></IconButton></div>
      </aside>

      <main className="main-stage" aria-label={tr('模型探索器', 'Model explorer')}>
        <div className="stage-heading">
          <div><span className="eyebrow">{mode === 'build' ? 'BUILD INSTRUCTIONS' : 'MODEL EXPLORER'}</span><div className="stage-title">{config.title}<span>{config.id}</span></div></div>
          <div className="stage-status"><span className={`status-dot ${loading ? 'loading-dot' : ''}`} />{error ? tr('载入失败', 'Load failed') : loading ? `${Math.floor(progress)}%` : `${visible.length} ${tr('个零件', 'bricks')}`}</div>
        </div>
        <div className="canvas-host" ref={stageRef} />
        {mode === 'build' && selected && sceneRef.current && <SelectedPartPreview scene={sceneRef.current} part={selected} onClose={() => patch({ selection: [] })} tr={tr} />}
        <div className="viewport-toolbar" aria-label={tr('视角工具', 'View tools')}>
          <div className="view-select"><Box size={16} /><select aria-label={tr('模型视角', 'Model view')} value={state.view} onChange={e => patch({ view: e.target.value as ExplorerState['view'], revision: state.revision + 1 })}>{Object.entries(viewNames(tr)).map(([id, name]) => <option key={id} value={id}>{name}</option>)}</select><ChevronDown size={12} /></div>
          <div className="toolbar-divider" />
          <IconButton label={tr('自动旋转', 'Auto rotate')} active={state.autoRotate} disabled={state.explosion >= 0.98} onClick={() => patch({ autoRotate: !state.autoRotate })}><Rotate3D size={18} /></IconButton>
          <IconButton label={tr('平移视图（上下左右拖动）', 'Pan view in any direction')} active={panMode} onClick={() => { setPanMode(value => !value); patch({ autoRotate: false }); }}><Hand size={17} /></IconButton>
          <IconButton label={tr('适配全部可见零件', 'Fit visible bricks')} onClick={() => patch({ revision: state.revision + 1 })}><Expand size={18} /></IconButton>
          <IconButton label={tr('零件边线', 'Part edges')} active={state.edges} onClick={() => patch({ edges: !state.edges })}><Box size={17} /></IconButton>
          <IconButton label={tr('X-Ray 透视模式', 'X-Ray mode')} active={state.xray} onClick={() => patch({ xray: !state.xray })}><Eye size={17} /></IconButton>
        </div>
        <div className="zoom-tools">
          <IconButton label={tr('放大模型', 'Zoom in')} onClick={() => sceneRef.current?.zoom(0.8)}><Plus size={18} /></IconButton>
          <IconButton label={tr('缩小模型', 'Zoom out')} onClick={() => sceneRef.current?.zoom(1.25)}><Minus size={18} /></IconButton>
          <div />
          <IconButton label={tr('复原模型', 'Reset model')} onClick={reset}><RotateCcw size={17} /></IconButton>
        </div>
        {!detailsOpen && <IconButton className="reopen-details" label={mode === 'build' ? tr('打开步骤说明书', 'Open build guide') : tr('打开详情面板', 'Open details')} onClick={() => setDetailsOpen(true)}>{mode === 'build' ? <BookOpen size={18} /> : <Info size={18} />}</IconButton>}
        {state.isolation && <div className="isolation-indicator"><Focus size={14} />{tr('隔离中', 'Isolated')} · {visible.length} {tr('个零件', 'bricks')}<button aria-label={tr('退出隔离', 'Exit isolation')} title={tr('退出隔离', 'Exit isolation')} onClick={() => patch({ isolation: null })}><X size={15} /></button></div>}
        {state.selection.length > 0 && <div className="selection-indicator"><span className="status-dot" /><button onClick={() => setDetailsOpen(true)}>{tr('已选', 'Selected')} {state.selection.length} {tr('个零件', 'bricks')}</button><IconButton label={tr('清除选择', 'Clear selection')} onClick={() => patch({ selection: [] })}><X size={14} /></IconButton></div>}
        {!loading && !error && visible.length === 0 && mode !== 'build' && <div className="empty-stage"><EyeOff size={32} /><strong>{tr('所有零件已隐藏', 'All bricks are hidden')}</strong><button className="primary-button" onClick={() => patch({ hiddenGroups: [], hiddenBrickIds: [], isolation: null })}><Eye size={16} />{tr('显示全部', 'Show all')}</button></div>}
        {(loading || error) && <div className={`loading-state ${error ? 'error-state' : ''}`} role={error ? 'alert' : 'status'}>
          {error ? <><Info size={30} /><strong>{tr('模型暂时无法显示', 'Model unavailable')}</strong><p>{error}</p><button className="primary-button" onClick={() => { sceneRef.current?.dispose(); sceneRef.current = null; setManifest(null); setRetry(r => r + 1); }}><RotateCcw size={16} />{tr('重新加载', 'Reload')}</button><a href={`${base}model.packed.mpd`} download>{tr('下载源模型', 'Download source model')}</a></> : <><LoaderCircle className="spinner" size={26} /><strong>{stage}</strong><progress max={100} value={progress} /><span>{Math.floor(progress)}%</span></>}
        </div>}
        <div className="scene-corner"><span>LDRAW</span><span>{tr('毫米', 'Millimetres')} · 1:1</span></div>
        {mode === 'build' ? <section className="explosion-dock build-dock" aria-label={tr('拼装步骤控制', 'Build step controls')}>
          <div className="dock-heading"><div><BookOpen size={18} /><strong>{currentBuildStep === 0 ? tr('准备拼装', 'Ready to build') : activeStep ? stepTitle(activeStep) : ''}</strong><span className="phase-name">{manifest?.instructions?.provenance === 'source' ? tr('OMR 源步骤', 'OMR source steps') : tr('结构演示', 'Structural guide')}</span></div><output aria-live="polite">{currentBuildStep}<span> / {steps.length}</span></output></div>
          <div className="step-controls">
            <IconButton label={tr('回到开始', 'Restart')} disabled={currentBuildStep === 0} onClick={() => setBuildStep(0)}><SkipBack size={17} /></IconButton>
            <IconButton label={tr('上一步', 'Previous step')} disabled={currentBuildStep === 0} onClick={() => setBuildStep(currentBuildStep - 1)}><ArrowLeft size={18} /></IconButton>
            <IconButton label={playing ? tr('暂停自动拼装', 'Pause build') : tr('自动播放拼装', 'Play build')} active={playing} disabled={!steps.length || currentBuildStep === steps.length} onClick={() => setPlaying(value => !value)}>{playing ? <Pause size={18} /> : <Play size={18} />}</IconButton>
            <input type="range" min={0} max={steps.length} value={currentBuildStep} aria-label={tr('当前拼装步骤', 'Current build step')} aria-valuetext={tr(`第 ${currentBuildStep} 步，共 ${steps.length} 步`, `Step ${currentBuildStep} of ${steps.length}`)} onChange={event => setBuildStep(Number(event.target.value))} style={{ '--range-fill': `${steps.length ? currentBuildStep / steps.length * 100 : 0}%` } as React.CSSProperties} />
            <IconButton label={tr('下一步', 'Next step')} disabled={currentBuildStep === steps.length} onClick={() => setBuildStep(currentBuildStep + 1)}><ArrowRight size={18} /></IconButton>
            <IconButton label={tr('完成模型', 'Complete model')} disabled={currentBuildStep === steps.length} onClick={() => setBuildStep(steps.length)}><SkipForward size={17} /></IconButton>
          </div>
          <div className="step-parts">{currentBuildStep === 0
            ? <span>{tr('整理零件并选择“下一步”开始', 'Sort the bricks and choose Next')}</span>
            : activeStep?.kind === 'placement'
              ? <strong>{tr('放置已完成的子装配', 'Place the completed subassembly')}</strong>
              : <><strong>{tr('本步', 'This step')} {activeStepParts?.length ?? 0} {tr('件', 'bricks')}</strong>{activeStepParts?.slice(0, 4).map(part => <button key={part.instanceId} onClick={() => selectPart(part.instanceId, true)}><span style={{ background: part.colorHex }} />{part.partNumber}</button>)}{(activeStepParts?.length ?? 0) > 4 && <span>+{activeStepParts!.length - 4}</span>}</>}
          </div>
          <p className="instruction-note">{instructionDisclaimer}</p>
        </section> : <section className="explosion-dock" aria-label={tr('拆解控制', 'Explode controls')}>
          <div className="dock-heading"><div><Layers3 size={18} /><strong>{tr('拆解程度', 'Explode')}</strong><span className="phase-name">{state.explosion === 0 ? tr('完整装配', 'Assembled') : state.explosion <= 0.45 ? tr('结构分离', 'Structure') : state.explosion === 1 ? tr('零件陈列', 'Inventory') : tr('实例展开', 'Expanded')}</span></div><output aria-live="off">{Math.round(state.explosion * 100)}<span>%</span></output></div>
          <div className="slider-row"><Box size={18} /><input type="range" min={0} max={100} step={1} value={Math.round(state.explosion * 100)} aria-label={tr('拆解程度', 'Explode amount')} aria-valuetext={`${Math.round(state.explosion * 100)}%`} onChange={e => patch({ explosion: Number(e.target.value) / 100, autoRotate: false })} style={{ '--range-fill': `${state.explosion * 100}%` } as React.CSSProperties} /><Grid2X2 size={18} /></div>
          <div className="dock-presets"><button className={state.explosion === 0 ? 'current' : ''} onClick={() => patch({ explosion: 0 })}>{tr('完整装配', 'Assembled')}<span>0%</span></button><button className={state.explosion === 0.45 ? 'current' : ''} onClick={() => patch({ explosion: 0.45, autoRotate: false })}>{tr('结构分离', 'Structure')}<span>45%</span></button><button className={state.explosion === 1 ? 'current' : ''} onClick={() => patch({ explosion: 1, autoRotate: false })}>{tr('零件陈列', 'Inventory')}<span>100%</span></button></div>
        </section>}
      </main>

      <aside className="sidebar right-sidebar" aria-label={mode === 'build' ? tr('步骤说明书', 'Build guide') : tr('零件详情', 'Part details')}>
        <header className="detail-header"><span>{mode === 'build' ? <BookOpen size={16} /> : <CircleDot size={16} />}{mode === 'build' ? tr('步骤说明书', 'Build guide') : selected ? tr('零件详情', 'Part details') : tr('套装档案', 'Model profile')}</span><IconButton label={tr('关闭详情面板', 'Close details')} onClick={() => setDetailsOpen(false)}><X size={17} /></IconButton></header>
        <div className="detail-scroll">
          {mode === 'build' ? <div className="instruction-sidebar">
            <div className="instruction-guide-cover">
              <img src={`${base}preview.png`} alt="" />
              <div><span>{tr('积木拼装册', 'BRICK BUILD BOOK')}</span><div className="instruction-page-heading"><strong>{currentBuildStep || '—'}</strong><small>/ {steps.length}</small></div></div>
            </div>
            {currentBuildStep === 0 && <div className="instruction-start"><BookOpen size={28} /><h2>{tr('准备开始拼装', 'Ready to build')}</h2><p>{tr('打开任意步骤积木，查看零件与入位动画。', 'Open any step brick to see its parts and placement animation.')}</p><button className="primary-button" onClick={() => setBuildStep(1)}>{tr('进入第 1 步', 'Start step 1')}<ArrowRight size={16} /></button></div>}
            <section className="instruction-accordion" aria-label={tr('可折叠拼装步骤', 'Collapsible build steps')}>
              {steps.map((step, index) => {
                const stepNumber = index + 1;
                const isOpen = openInstructionStep === stepNumber;
                const ids = step.motionInstanceIds ?? step.instanceIds;
                const firstPart = manifest?.instances.find(part => ids.includes(part.instanceId));
                const group = firstPart ? manifest?.groups.find(item => item.id === firstPart.groupId) : null;
                return <details
                  key={step.id}
                  data-instruction-step={stepNumber}
                  className={`instruction-brick-step ${currentBuildStep === stepNumber ? 'current' : ''}`}
                  open={isOpen}
                  style={{ '--step-color': group?.color ?? '#376dd1' } as React.CSSProperties}
                >
                  <summary
                    aria-controls={`instruction-step-panel-${stepNumber}`}
                    aria-expanded={isOpen}
                    onClick={event => {
                      event.preventDefault();
                      toggleInstructionStep(stepNumber);
                    }}
                  >
                    <span className="instruction-brick-studs" aria-hidden="true"><i /><i /><i /><i /></span>
                    <span className="instruction-brick-number">{String(stepNumber).padStart(2, '0')}</span>
                    <span className="instruction-brick-label"><strong>{stepTitle(step)}</strong><small>{step.kind === 'placement' ? tr('放置总成', 'Place assembly') : `${step.instanceIds.length} ${tr('件积木', 'bricks')}`}</small></span>
                    <ChevronDown className="instruction-brick-chevron" size={16} />
                  </summary>
                  {isOpen && <div className="instruction-brick-panel" id={`instruction-step-panel-${stepNumber}`}>
                    <div>
                      <div className="instruction-static-frame instruction-motion-frame">
                        {instructionFrames.length ? <img src={instructionFrames[instructionFrame]} decoding="sync" alt={tr(`第 ${currentBuildStep} 步动态拼装图`, `Animated build view for step ${currentBuildStep}`)} /> : <LoaderCircle className="spinner" size={24} />}
                        <span><Play size={10} />{tr('自动循环 · 聚焦本步', 'Auto loop · focused step')}</span>
                      </div>
                      {instructionFrames.length > 1 && <div className="instruction-placement-diagram" role="img" aria-label={tr(`第 ${currentBuildStep} 步积木从起点到安装位置`, `Step ${currentBuildStep} brick path from start to final position`)}>
                        <figure><img src={instructionFrames[0]} alt="" /><figcaption>{tr('起始位置', 'START')}</figcaption></figure>
                        <span className="instruction-path-arrow" aria-hidden="true"><i /><ArrowRight size={16} /></span>
                        <figure className="target"><img src={instructionFrames[instructionFrames.length - 1]} alt="" /><figcaption>{tr('最终位置', 'TARGET')}</figcaption></figure>
                      </div>}
                      <div className="instruction-step-title"><span>{step.kind === 'placement' ? 'SUBASSEMBLY PLACEMENT' : manifest?.instructions?.provenance === 'source' ? 'OMR AUTHOR STEP' : 'EDITORIAL ASSEMBLY STEP'}</span><h2>{stepTitle(step)}</h2></div>
                      {step.kind === 'placement'
                        ? <section className="instruction-placement" aria-label={tr('总成放置', 'Subassembly placement')}><Layers3 size={24} /><strong>{tr('放置已完成的子装配', 'Place the completed subassembly')}</strong><span>{step.motionInstanceIds?.length ?? 0} {tr('块积木整体入位', 'bricks move into final position')}</span></section>
                        : <section className="instruction-parts" aria-label={tr('本步所需零件', 'Parts for this step')}>
                          <h3>{tr('本步所需零件', 'Parts for this step')} <span>{activeStepParts?.length ?? 0}</span></h3>
                          {activePartGroups.map(partGroup => <button key={partGroup.key} onClick={() => selectPart(partGroup.instanceIds[0], true)}>
                            <span className="instruction-part-swatch" style={{ background: partGroup.colorHex }}><Box size={18} color={['15', '19', '47', '71'].includes(manifest?.instances.find(part => part.instanceId === partGroup.instanceIds[0])?.colorCode ?? '') ? '#53615b' : '#fff'} /></span>
                            <span><strong>{partGroup.quantity}× {partGroup.partNumber}</strong><small>{partGroup.name}<br />{partGroup.colorName}</small></span>
                          </button>)}
                        </section>}
                      <div className="instruction-side-nav"><button disabled={stepNumber === 1} onClick={() => setBuildStep(stepNumber - 1)}><ArrowLeft size={16} />{tr('上一步', 'Previous')}</button><button disabled={stepNumber === steps.length} onClick={() => setBuildStep(stepNumber + 1)}>{tr('下一步', 'Next')}<ArrowRight size={16} /></button></div>
                    </div>
                  </div>}
                </details>;
              })}
            </section>
            <button className="primary-button guide-export" disabled={!!guideExport || loading} onClick={exportInstructions}>{guideExport ? <LoaderCircle className="spinner" size={16} /> : <FileDown size={16} />}{guideExport ? tr(`正在生成 ${guideExport.current} / ${guideExport.total}`, `Generating ${guideExport.current} / ${guideExport.total}`) : tr('导出完整说明书 PDF', 'Export complete PDF guide')}</button>
            <p className="guide-disclaimer">{instructionDisclaimer}</p>
          </div> : selected ? <>
            <div className="part-identity"><div className="eyebrow">{selected.instanceId}</div><div className="part-number">{selected.partNumber}<span className="identity-swatch" style={{ background: selected.colorHex }} /></div><h2>{selected.displayName}</h2><div className="color-label"><span style={{ background: selected.colorHex }} />{tr(colorLabels[selected.colorCode] ?? selected.colorName, selected.colorName)}<small>{selected.colorCode}</small></div></div>
            <div className="part-actions"><button className="primary-button" onClick={() => isolate(state.selection)}><Focus size={16} />{tr('隔离选择', 'Isolate')}</button><IconButton label={tr('隐藏选中积木', 'Hide selected brick')} onClick={() => patch({ hiddenBrickIds: [...new Set([...state.hiddenBrickIds, ...state.selection])], selection: [] })}><EyeOff size={18} /></IconButton><IconButton label={tr('聚焦选中零件', 'Focus selected brick')} onClick={() => sceneRef.current?.focusSelection()}><Crosshair size={18} /></IconButton></div>
            <dl className="metadata"><div><dt>Part ID</dt><dd>{selected.partNumber}</dd></div><div><dt>{tr('颜色', 'Color')}</dt><dd>{selected.colorName}</dd></div><div><dt>{tr('尺寸', 'Dimensions')}</dt><dd>{selectedBrick?.dimensions.map(value => `${value.toFixed(1)}`).join(' × ')} mm</dd></div><div><dt>{tr('模型内数量', 'Quantity')}</dt><dd>{sameType.length}</dd></div><div><dt>Subassembly</dt><dd>{selectedAssembly?.name ?? (selectedGroup ? localGroupName(locale, selectedGroup.id, selectedGroup.name) : '')}</dd></div><div><dt>{tr('所属结构', 'Assembly')}</dt><dd><span className="group-dot" style={{ background: selectedGroup?.color }} />{selectedGroup ? localGroupName(locale, selectedGroup.id, selectedGroup.name) : ''}</dd></div><div><dt>{tr('装配步骤', 'Build step')}</dt><dd>{selected.buildStep === null ? tr('结构演示', 'Structural guide') : tr(`源步骤 ${selected.buildStep}`, `Source step ${selected.buildStep}`)}</dd></div></dl>
            <div className="detail-section"><h3>{tr('同型号实例', 'Where used')} <span>{sameType.length}</span></h3><div className="instance-navigation"><IconButton label={tr('上一个同型号实例', 'Previous instance')} onClick={() => selectPart(sameType[(sameType.findIndex(p => p.instanceId === selected.instanceId) + sameType.length - 1) % sameType.length].instanceId, true)}><ArrowLeft size={16} /></IconButton><span>{sameType.findIndex(p => p.instanceId === selected.instanceId) + 1} / {sameType.length}</span><IconButton label={tr('下一个同型号实例', 'Next instance')} onClick={() => selectPart(sameType[(sameType.findIndex(p => p.instanceId === selected.instanceId) + 1) % sameType.length].instanceId, true)}><ArrowRight size={16} /></IconButton></div><button className="secondary-button" onClick={selectAllType}><Boxes size={16} />{tr('高亮全部同型号', 'Highlight all of this part')}</button><button className="secondary-button" onClick={() => isolate(sameType.map(p => p.instanceId))}><Focus size={16} />{tr('隔离全部同型号', 'Isolate all of this part')}</button></div>
            <div className="detail-section"><h3>{tr('来源路径', 'Source path')}</h3><div className="source-path">{selected.path.map((p, i) => <div key={`${p}-${i}`}><ChevronRight size={12} /><span>{p}</span></div>)}<div><ChevronRight size={12} /><strong>{selected.partNumber}.dat</strong></div></div><div className="source-line">{tr(`原始 MPD · 第 ${selected.sourceLine} 行`, `Source MPD · line ${selected.sourceLine}`)}</div><button className="secondary-button" onClick={() => isolate(manifest!.instances.filter(p => p.parentSubmodelId === selected.parentSubmodelId).map(p => p.instanceId))}><Layers3 size={16} />{tr('隔离所属子模型', 'Isolate submodel')}</button><a className="source-link" href={`${base}model.packed.mpd`} download><ExternalLink size={13} />{tr('查看打包源文件', 'Download packed source')}</a></div>
          </> : <>
            <div className="model-identity"><span className="archive-icon"><Box size={32} strokeWidth={1.2} /></span><div className="eyebrow">MODEL NO. {config.id}</div><h2>{config.title}</h2><p>{locale === 'zh' ? config.subtitle : config.title}</p><span className="model-tag">{config.theme}</span></div>
            <dl className="metadata"><div><dt>{tr('发行年份', 'Released')}</dt><dd>{config.year}</dd></div><div><dt>{tr('模型实例', 'Brick instances')}</dt><dd>{manifest?.stats.instances ?? '—'}</dd></div><div><dt>{tr('独立零件型号', 'Part types')}</dt><dd>{manifest?.stats.uniqueParts ?? '—'}</dd></div><div><dt>{tr('拼装步骤', 'Build steps')}</dt><dd>{steps.length || '—'}</dd></div><div><dt>{tr('步骤来源', 'Step source')}</dt><dd>{manifest?.instructions?.provenance === 'source' ? tr('OMR 作者', 'OMR author') : tr('结构演示', 'Structural guide')}</dd></div><div><dt>{tr('几何来源', 'Geometry')}</dt><dd>LDraw OMR</dd></div><div><dt>{tr('模型许可', 'License')}</dt><dd>{config.license}</dd></div></dl>
            <div className="detail-section"><h3>{tr('模型配色', 'Color palette')} <span>{colors.length}</span></h3><div className="color-palette">{colors.map(([code, color]) => <button key={code} style={{ backgroundColor: color.hex }} aria-label={tr(`筛选颜色 ${color.name}`, `Filter color ${color.name}`)} title={`${tr(colorLabels[code] ?? color.name, color.name)} · ${color.count}`} onClick={() => { setQuery(color.name); setTab('parts'); }} />)}</div><div className="color-distribution">{colors.map(([code, color]) => <span key={code} style={{ backgroundColor: color.hex, flex: color.count }} />)}</div></div>
            <div className="detail-section provenance-summary"><ShieldCheck size={20} /><div><strong>{tr('开放模型，来源可追溯', 'Open model with traceable provenance')}</strong><span>{config.author.split(' [')[0]}</span><a href={config.sourceUrl} target="_blank" rel="noreferrer">Official Model Repository<ExternalLink size={12} /></a></div></div>
            <button className="secondary-button inventory-download" onClick={exportInventory} disabled={!manifest}><ArrowDownToLine size={16} />{tr('导出零件清单', 'Export inventory')}</button>
          </>}
        </div>
        <div className="detail-footer"><ShieldCheck size={14} /><span>{tr('非 LEGO 官方产品', 'Unofficial LEGO project')}</span><button onClick={() => setModal('credits')}>{tr('许可信息', 'Licenses')}</button></div>
      </aside>
    </div>
    <footer className="app-footer"><span><span className="status-dot" />{loading ? tr('模型载入中', 'Loading model') : error ? tr('资源异常', 'Asset error') : tr('模型已就绪', 'Model ready')}</span><span>LDraw · {manifest ? `${(manifest.stats.triangles / 1000).toFixed(1)}k ${tr('三角面', 'triangles')}` : '—'}</span><span>BRICK ATLAS <span className="footer-version">v1.1</span></span></footer>
    {hover && !loading && <div className="part-tooltip" style={{ left: Math.min(hover.x + 16, innerWidth - 260), top: Math.min(hover.y + 16, innerHeight - 80) }}><strong>{hover.part.partNumber}</strong><span>{hover.part.displayName}</span></div>}
    {notice && <div className="toast" role="status"><Check size={16} />{notice}</div>}
    {modal === 'settings' && <Modal title={tr('显示设置', 'Display settings')} onClose={() => setModal(null)}><div className="settings-content">
      <label>{tr('渲染质量', 'Render quality')}<select value={state.quality} onChange={e => patch({ quality: e.target.value as ExplorerState['quality'] })}><option value="auto">{tr('自动 · 根据屏幕调整', 'Auto · Match display')}</option><option value="high">{tr('高 · 3x 像素密度', 'High · 3x pixel density')}</option><option value="ultra">{tr('超清 · 4x 像素密度', 'Ultra · 4x pixel density')}</option><option value="low">{tr('性能 · 1x，无边线', 'Performance · 1x, no edges')}</option></select></label>
      <label>{tr('工作台背景', 'Workspace background')}<select value={state.background} onChange={e => patch({ background: e.target.value as ExplorerState['background'] })}><option value="studio">{tr('工作室灰', 'Studio gray')}</option><option value="white">{tr('纯白', 'White')}</option><option value="dark">{tr('深色', 'Dark')}</option></select></label>
      <label>{tr('导出分辨率', 'Export resolution')}<select value={exportSize} onChange={e => setExportSize(Number(e.target.value))}><option value={1920}>Full HD · 1920 × 1080</option><option value={3840}>4K · 3840 × 2160</option><option value={7680}>8K · 7680 × 4320</option><option value={11520}>12K · 11520 × 6480</option></select></label>
      <label className="checkbox-row"><span>{tr('显示零件边线', 'Show part edges')}</span><input type="checkbox" checked={state.edges} onChange={e => patch({ edges: e.target.checked })} /></label>
      <label className="checkbox-row"><span>{tr('显示参考网格', 'Show reference grid')}</span><input type="checkbox" checked={state.grid} onChange={e => patch({ grid: e.target.checked })} /></label>
      <label className="checkbox-row"><span>{tr('X-Ray 透视', 'X-Ray')}</span><input type="checkbox" checked={state.xray} onChange={e => patch({ xray: e.target.checked })} /></label>
      <label className="checkbox-row"><span>{tr('自动旋转', 'Auto rotate')}</span><input type="checkbox" disabled={state.explosion >= 0.98} checked={state.autoRotate} onChange={e => patch({ autoRotate: e.target.checked })} /></label>
      <button className="primary-button settings-export" onClick={screenshot}><ArrowDownToLine size={16} />{tr('导出高清 PNG', 'Export high-resolution PNG')}</button>
      <dl className="metadata"><div><dt>{tr('几何压缩体积', 'Compressed geometry')}</dt><dd>{manifest ? (manifest.stats.compressedBytes / 1024 / 1024).toFixed(2) : '—'} MiB</dd></div><div><dt>{tr('本次完整加载', 'Full load time')}</dt><dd>{readyTime ? `${(readyTime / 1000).toFixed(2)} s` : '—'}</dd></div><div><dt>{tr('绘制调用', 'Draw calls')}</dt><dd>{sceneRef.current?.metrics.drawCalls ?? '—'}</dd></div><div><dt>{tr('减弱动态效果', 'Reduced motion')}</dt><dd>{matchMedia('(prefers-reduced-motion: reduce)').matches ? tr('已启用', 'Enabled') : tr('未启用', 'Disabled')}</dd></div></dl>
      <button className="secondary-button" onClick={() => download(JSON.stringify(diagnosticsReport(), null, 2), 'brick-atlas-diagnostics.json', 'application/json')}><ArrowDownToLine size={16} />{tr('导出本次运行诊断', 'Export diagnostics')}</button>
    </div></Modal>}
    {modal === 'credits' && <Modal title={tr('来源与署名', 'Credits and provenance')} onClose={() => setModal(null)}><div className="credits-content"><div className="credit-brand"><Boxes size={24} /><strong>Brick Atlas</strong><span>{tr('非官方积木模型探索器', 'Unofficial brick model explorer')}</span></div><p>{tr('本项目为非官方社区项目，与 LEGO Group 无隶属、赞助或认可关系。LEGO 是 LEGO Group 的商标。', 'This is an unofficial community project and is not affiliated with, sponsored, or endorsed by the LEGO Group. LEGO is a trademark of the LEGO Group.')}</p><h3>{tr('套装模型', 'Set model')}</h3><p>{config.setNumber} {config.title} · {config.author}<br /><a href={config.licenseUrl} target="_blank" rel="noreferrer">Creative Commons Attribution 2.0</a><br /><a href={config.sourceUrl} target="_blank" rel="noreferrer">OMR {tr('模型来源页', 'model page')} <ExternalLink size={12} /></a></p><h3>{tr('零件库', 'Parts library')}</h3><p>{tr('LDraw.org 官方零件库快照。每个文件的作者、许可及历史保留在打包源文件中。', 'LDraw.org official parts library snapshot. Per-file authorship, licensing, and history are retained in the packed source.')}</p><div className="credit-links"><a href={`${base}credits.json`} target="_blank" rel="noreferrer">{tr('逐文件署名', 'Per-file credits')}</a><a href={`${base}CAlicense.txt`} target="_blank" rel="noreferrer">CC BY 2.0</a><a href={`${base}CAlicense4.txt`} target="_blank" rel="noreferrer">CC BY 4.0</a><a href={`${base}provenance.json`} target="_blank" rel="noreferrer">{tr('来源与哈希', 'Provenance and hashes')}</a></div><h3>{tr('步骤声明', 'Step disclosure')}</h3><p>{locale === 'zh' ? manifest?.instructions?.disclaimer : manifest?.instructions?.provenance === 'source' ? 'Steps follow OMR author metadata and do not reproduce official printed page numbering.' : 'The source contains no STEP metadata. The sequence is an editorial structural walkthrough.'}</p><h3>{tr('加工与完整性声明', 'Processing and integrity')}</h3><p>{tr('模型经过依赖打包、毫米坐标转换、语义分组、实例索引、几何合批和无损压缩；未进行减面。', 'Models are dependency-packed, converted to millimetres, semantically grouped, instance-indexed, batched, and losslessly compressed without mesh decimation.')}</p><h3>{tr('应用代码', 'Application')}</h3><p>MIT License · React · Three.js · Lucide</p><a className="secondary-button" href={`${base}build-report.json`} target="_blank" rel="noreferrer"><ShieldCheck size={16} />{tr('查看资产构建报告', 'View asset build report')}</a></div></Modal>}
  </div>;
}

function FloatingBricks() {
  const colors = ['#ef4438', '#f3c744', '#3478d4', '#21a8b8', '#d95b9f', '#784fc4', '#ff7b32'];
  return <div className="floating-bricks" aria-hidden="true">{Array.from({ length: 22 }, (_, index) => <span key={index} style={{
    '--brick-x': `${(index * 47) % 101}%`,
    '--brick-y': `${(index * 31) % 92}%`,
    '--brick-r': `${(index * 29) % 70 - 35}deg`,
    '--brick-delay': `${-(index % 9) * 1.3}s`,
    '--brick-duration': `${11 + index % 7}s`,
    '--brick-color': colors[index % colors.length],
    '--brick-scale': `${0.55 + index % 5 * 0.17}`,
  } as React.CSSProperties}>{[0, 1, 2, 3].map(stud => <i key={stud} />)}</span>)}</div>;
}

function CatalogPage({ locale, tr, toggleLocale }: { locale: Locale; tr: Translator; toggleLocale: () => void }) {
  type CatalogSummary = {
    stats: AtlasManifest['stats'];
    treeNodes: number;
    steps: number;
    provenance: 'source' | 'editorial';
  };
  const [summaries, setSummaries] = useState<Record<string, CatalogSummary>>({});
  useEffect(() => {
    const abort = new AbortController();
    Promise.all(modelCatalog.map(async model => {
      const response = await fetch(`${import.meta.env.BASE_URL}models/${model.id}/manifest.json`, { signal: abort.signal });
      if (!response.ok) return [model.id, null] as const;
      const manifest = await response.json() as AtlasManifest;
      return [model.id, {
        stats: manifest.stats,
        treeNodes: manifest.submodels.length + manifest.groups.length,
        steps: manifest.instructions?.steps.length ?? 0,
        provenance: manifest.instructions?.provenance ?? 'editorial',
      }] as const;
    })).then(items => setSummaries(Object.fromEntries(items.filter((item): item is [string, CatalogSummary] => !!item[1])))).catch(() => {});
    return () => abort.abort();
  }, []);
  return <div className="catalog-page landing-page">
    <header className="topbar landing-nav">
      <a href={import.meta.env.BASE_URL} className="brand"><span className="brand-mark"><BrickAtlasMark /></span><strong>BRICK<span>ATLAS</span></strong></a>
      <nav className="landing-links"><a href="#features">{tr('功能', 'Features')}</a><a href="#models">{tr('模型商店', 'Model shop')}</a><a href={`${import.meta.env.BASE_URL}create`}>{tr('图片创作', 'Create')}</a></nav>
      <LanguageButton locale={locale} onToggle={toggleLocale} tr={tr} />
    </header>
    <main>
      <section className="landing-hero">
        <FloatingBricks />
        <div className="rainbow-rail" aria-hidden="true">{['#ef4438', '#f3c744', '#3478d4', '#21a8b8', '#d95b9f', '#784fc4'].map(color => <span key={color} style={{ background: color }} />)}</div>
        <img className="hero-model" src={`${import.meta.env.BASE_URL}models/5867/preview.png`} alt="LEGO 5867 Super Speedster" />
        <div className="hero-copy">
          <span className="eyebrow">EXPLORE · BUILD · CREATE</span>
          <h1>Brick Atlas</h1>
          <h2>{tr('把每一块积木看清楚', 'See every brick. Build every idea.')}</h2>
          <p>{tr('旋转真实 LDraw 模型，拆解每个结构，逐步完成拼装，并导出属于你的说明书。', 'Rotate real LDraw models, inspect every assembly, build step by step, and export your own guide.')}</p>
          <div className="hero-actions"><a className="hero-primary" href="#models"><Library size={17} />{tr('浏览模型', 'Browse models')}</a><a href={`${import.meta.env.BASE_URL}explore/5867`}><Rotate3D size={17} />{tr('打开旗舰模型', 'Open flagship model')}</a></div>
          <dl><div><dt>{tr('积木实例', 'Brick instances')}</dt><dd>{Object.values(summaries).reduce((sum, item) => sum + item.stats.instances, 0) || '—'}</dd></div><div><dt>{tr('可探索项目', 'Models')}</dt><dd>{modelCatalog.length}</dd></div><div><dt>{tr('拼装步骤', 'Build steps')}</dt><dd>{Object.values(summaries).reduce((sum, item) => sum + item.steps, 0) || '—'}</dd></div></dl>
        </div>
        <div className="hero-model-label"><strong>5867</strong><span>Super Speedster</span></div>
      </section>
      <section className="feature-band" id="features">
        <div><Rotate3D size={22} /><strong>{tr('真实 3D 探索', 'True 3D exploration')}</strong><span>{tr('自由旋转、缩放和拆解', 'Orbit, zoom, isolate, and explode')}</span></div>
        <div><BookOpen size={22} /><strong>{tr('动态拼装', 'Animated building')}</strong><span>{tr('步骤、零件和入位动画同步', 'Steps, parts, and motion stay in sync')}</span></div>
        <div><Search size={22} /><strong>{tr('逐块理解', 'Inspect every brick')}</strong><span>{tr('型号、颜色、尺寸和来源', 'Part ID, color, dimensions, provenance')}</span></div>
        <div><FileDown size={22} /><strong>{tr('高清输出', 'High-resolution output')}</strong><span>{tr('最高 12K 图像与完整 PDF 说明书', 'Up to 12K imagery and complete PDF guides')}</span></div>
      </section>
      <LandingShowcase locale={locale} tr={tr} />
      <section className="catalog-shell" id="models">
        <section className="catalog-heading"><div><span className="eyebrow">MODEL SHOP</span><h2>{tr('选择你的下一盒积木', 'Choose your next build')}</h2><p>{tr('点击任意模型进入探索，或直接开始逐步拼装。', 'Open any model to explore it, or jump straight into guided building.')}</p></div><dl><div><dt>{tr('项目', 'Models')}</dt><dd>{modelCatalog.length}</dd></div><div><dt>{tr('套装', 'Sets')}</dt><dd>{new Set(modelCatalog.map(model => model.setNumber)).size}</dd></div><div><dt>{tr('积木', 'Bricks')}</dt><dd>{Object.values(summaries).reduce((sum, item) => sum + item.stats.instances, 0) || '—'}</dd></div></dl></section>
      <section className="model-grid" aria-label={tr('积木模型项目', 'Brick model projects')}>
        {modelCatalog.map((model, index) => <article className="model-card" key={model.id}>
          <a className="model-card-explore" href={`${import.meta.env.BASE_URL}explore/${model.id}`} aria-label={tr(`探索 ${model.title}`, `Explore ${model.title}`)}>
            <div className={`model-art art-${index % 5}`}><img src={`${import.meta.env.BASE_URL}models/${model.id}/preview.png`} alt={tr(`${model.title} 三维模型预览`, `${model.title} 3D model preview`)} /><Boxes size={42} aria-hidden="true" /></div>
            <div className="model-card-body"><div className="eyebrow"><span className="set-number">{model.id}</span>{localCategory(locale, model.category)} / {model.year}</div><h3>{model.title}</h3><p>{locale === 'zh' ? model.subtitle : model.theme}</p>
              <dl className="model-card-specs">
                <div><dt>{tr('积木', 'Bricks')}</dt><dd>{summaries[model.id]?.stats.instances ?? '—'}</dd></div>
                <div><dt>{tr('零件型号', 'Part types')}</dt><dd>{summaries[model.id]?.stats.uniqueParts ?? '—'}</dd></div>
                <div><dt>{tr('积木树', 'Tree nodes')}</dt><dd>{summaries[model.id]?.treeNodes ?? '—'}</dd></div>
                <div><dt>{tr('拼装步骤', 'Build steps')}</dt><dd>{summaries[model.id]?.steps ?? '—'}</dd></div>
                <div><dt>{tr('几何面', 'Triangles')}</dt><dd>{summaries[model.id] ? `${(summaries[model.id].stats.triangles / 1000).toFixed(0)}k` : '—'}</dd></div>
                <div><dt>{tr('步骤来源', 'Step source')}</dt><dd>{summaries[model.id]?.provenance === 'source' ? 'OMR' : tr('结构', 'Editorial')}</dd></div>
              </dl>
            </div>
          </a>
          <div className="model-card-actions"><a className="primary-link" href={`${import.meta.env.BASE_URL}build/${model.id}`}><BookOpen size={16} />{tr('开始拼装', 'Start building')}</a></div>
        </article>)}
      </section>
      <p className="catalog-legal">{tr('非官方社区项目。模型来自 LDraw OMR；LEGO 是 LEGO Group 的商标。', 'Unofficial community project. Models are sourced from LDraw OMR. LEGO is a trademark of the LEGO Group.')}</p>
      </section>
    </main>
  </div>;
}

function CreatorPage({ locale, tr, toggleLocale }: { locale: Locale; tr: Translator; toggleLocale: () => void }) {
  const [report, setReport] = useState<{ name: string; references: number; steps: number; files: number } | null>(null);
  function inspectFile(file?: File) {
    if (!file) return;
    file.text().then(text => setReport({
      name: file.name,
      references: text.split(/\r?\n/).filter(line => line.trim().startsWith('1 ')).length,
      steps: text.split(/\r?\n/).filter(line => /^0 (STEP|ROTSTEP)( |$)/.test(line.trim())).length,
      files: text.split(/\r?\n/).filter(line => /^0 FILE /i.test(line.trim())).length || 1,
    }));
  }
  return <div className="catalog-page creator-page">
    <header className="topbar"><a href={import.meta.env.BASE_URL} className="brand"><span className="brand-mark"><BrickAtlasMark /></span><strong>BRICK<span>ATLAS</span></strong></a><div className="top-divider" /><span className="workspace-label">{tr('图片创作工坊', 'Creator studio')}</span><nav className="top-actions"><a className="text-button" href={import.meta.env.BASE_URL}><Library size={16} />{tr('项目库', 'Library')}</a><LanguageButton locale={locale} onToggle={toggleLocale} tr={tr} /></nav></header>
    <main className="creator-shell creator-studio-shell">
      <ImageBrickStudio locale={locale} tr={tr} />
      <section className="ldraw-import-section">
        <div><span className="eyebrow">LDRAW PROJECT IMPORT</span><h2>{tr('已有数字模型', 'Existing digital model')}</h2><p>{tr('本地预检 `.ldr` 或 `.mpd` 文件；文件不会上传。', 'Preflight an `.ldr` or `.mpd` file locally. The file never leaves your browser.')}</p></div>
        <label className="upload-zone compact-upload"><Upload size={22} /><strong>{tr('选择 LDraw 文件', 'Choose an LDraw file')}</strong><span>.ldr / .mpd</span><input type="file" accept=".ldr,.mpd,text/plain" onChange={event => inspectFile(event.target.files?.[0])} /></label>
        {report && <div className="import-report"><h2>{report.name}</h2><dl><div><dt>Type-1 {tr('引用', 'references')}</dt><dd>{report.references}</dd></div><div><dt>STEP {tr('标记', 'markers')}</dt><dd>{report.steps}</dd></div><div><dt>{tr('内嵌文件', 'Embedded files')}</dt><dd>{report.files}</dd></div></dl><p>{report.steps ? tr('检测到作者步骤，可进入资产审核与构建流程。', 'Author steps detected. The model can proceed to asset review and build.') : tr('未检测到 STEP；发布前需要明确标注为结构演示。', 'No STEP metadata found. Publish only as an explicitly labeled structural guide.')}</p></div>}
      </section>
    </main>
  </div>;
}

export default function App() {
  const { locale, tr, toggleLocale } = useLocale();
  useEffect(() => { document.title = tr('Brick Atlas｜积木世界', 'Brick Atlas | Build the world'); }, [tr]);
  const relative = location.pathname.slice(import.meta.env.BASE_URL.replace(/\/$/, '').length) || '/';
  if (relative === '/' || relative === '') return <CatalogPage locale={locale} tr={tr} toggleLocale={toggleLocale} />;
  if (relative === '/create' || relative === '/create/') return <CreatorPage locale={locale} tr={tr} toggleLocale={toggleLocale} />;
  const match = /^\/(explore|build)\/([^/]+)\/?$/.exec(relative);
  const config = match ? modelCatalog.find(model => model.id === decodeURIComponent(match[2])) : null;
  if (match && config) return <ExplorerWorkspace config={config} mode={match[1] as 'explore' | 'build'} locale={locale} tr={tr} toggleLocale={toggleLocale} />;
  return <div className="route-error"><Boxes size={38} /><h1>{tr('项目不存在', 'Project not found')}</h1><a className="primary-button" href={import.meta.env.BASE_URL}>{tr('返回项目库', 'Back to library')}</a></div>;
}
