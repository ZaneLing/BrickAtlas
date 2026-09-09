import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowDownToLine, ArrowLeft, ArrowRight, Box, Boxes, Check, ChevronDown, ChevronRight,
  BookOpen, CircleDot, Crosshair, Expand, ExternalLink, Eye, EyeOff, FileDown, Focus, Grid2X2, Info, Layers3,
  Library, LoaderCircle, Minus, Pause, Play, Plus, Rotate3D, RotateCcw, Search, Settings2, ShieldCheck,
  SkipBack, SkipForward, Upload, X,
} from 'lucide-react';
import { AtlasScene } from '../scene/AtlasScene';
import { PartPreviewScene } from '../scene/PartPreview';
import { colorLabels, searchInstances, visibleInstances, type AtlasManifest, type ExplorerState, type GroupId, type PartInstance } from '../model/types';
import { BrickModel } from '../model/BrickModel';
import { useViewerStore } from '../store/viewerStore';
import { IconButton, Modal } from '../ui/Controls';
import { diagnosticsReport, installDiagnostics, recordDiagnostic } from './diagnostics';
import { modelCatalog, type ModelConfig } from '../../atlas.config';
import { exportBuildGuide, groupStepParts } from '../instructions/exportGuide';

declare global { interface Window { __atlas?: () => ReturnType<AtlasScene['snapshot']> } }
const viewNames = { perspective: '三分之四', front: '正面', side: '侧面', rear: '背面', top: '顶部' };

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

function SelectedPartPreview({ scene, part, onClose }: { scene: AtlasScene; part: PartInstance; onClose: () => void }) {
  const hostRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const data = scene.getPartPreview(part.instanceId);
    if (!data || !hostRef.current) return;
    const preview = new PartPreviewScene(hostRef.current, data);
    return () => preview.dispose();
  }, [scene, part.instanceId]);
  return <section className="part-preview-window" aria-label="选中积木三维预览">
    <header><span><Rotate3D size={14} />{part.partNumber}</span><IconButton label="关闭积木预览" onClick={onClose}><X size={14} /></IconButton></header>
    <div className="part-preview-canvas" ref={hostRef} />
    <footer><strong>{part.displayName}</strong><span><i style={{ background: part.colorHex }} />{colorLabels[part.colorCode] ?? part.colorName}</span></footer>
  </section>;
}

export function ExplorerWorkspace({ config, mode }: { config: ModelConfig; mode: 'explore' | 'build' }) {
  const base = `${import.meta.env.BASE_URL}models/${config.id}/`;
  const [manifest, setManifest] = useState<AtlasManifest | null>(null);
  const state = useViewerStore(store => store.viewer);
  const setState = useViewerStore(store => store.update);
  const patch = useViewerStore(store => store.patch);
  const loadModel = useViewerStore(store => store.loadModel);
  const resetViewer = useViewerStore(store => store.reset);
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState('读取实例清单');
  const [error, setError] = useState<string | null>(null);
  const [retry, setRetry] = useState(0);
  const [query, setQuery] = useState('');
  const [tab, setTab] = useState<'structure' | 'parts'>('structure');
  const [drawer, setDrawer] = useState<'layers' | 'details' | null>(null);
  const [detailsOpen, setDetailsOpen] = useState(true);
  const [modal, setModal] = useState<'credits' | 'settings' | null>(null);
  const [hover, setHover] = useState<{ part: PartInstance; x: number; y: number } | null>(null);
  const [readyTime, setReadyTime] = useState<number | null>(null);
  const [notice, setNotice] = useState('');
  const [playing, setPlaying] = useState(false);
  const [exportSize, setExportSize] = useState(3840);
  const [instructionPreview, setInstructionPreview] = useState('');
  const [guideExport, setGuideExport] = useState<{ current: number; total: number } | null>(null);
  const stageRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<AtlasScene | null>(null);
  const manifestRef = useRef<AtlasManifest | null>(null);
  const focusAfter = useRef(false);
  useEffect(installDiagnostics, []);
  useEffect(() => { if (error) recordDiagnostic('model-error', { message: error }); }, [error]);
  useEffect(() => {
    const desktop = matchMedia('(min-width: 1050px)');
    const change = () => { if (desktop.matches) setDrawer(null); };
    desktop.addEventListener('change', change);
    return () => desktop.removeEventListener('change', change);
  }, []);

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
    if (mode !== 'build') {
      setDetailsOpen(true);
      if (innerWidth < 1050) setDrawer('details');
    }
  }, [mode]);

  useEffect(() => {
    const abort = new AbortController();
    setLoading(true); setError(null); setProgress(0);
    fetch(`${base}manifest.json`, { signal: abort.signal })
      .then(async response => {
        if (!response.ok) throw new Error(`manifest.json: HTTP ${response.status}`);
        const m = await response.json() as AtlasManifest;
        if (m.version !== 1 || !Array.isArray(m.instances) || !Array.isArray(m.chunks) || !m.instances.length) throw new Error('实例清单格式无效');
        if (!abort.signal.aborted) {
          loadModel(config.id, mode, m.instructions?.steps.length ?? 0);
          setManifest(m); manifestRef.current = m;
        }
      })
      .catch(e => { if (!abort.signal.aborted) { setError(`模型载入失败：${e.message}`); setLoading(false); } });
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
      });
      sceneRef.current = scene;
      window.__atlas = () => scene!.snapshot();
    } catch (e) {
      setError(`无法初始化 3D 视图：${e instanceof Error ? e.message : String(e)}。请确认浏览器已启用 WebGL 2。`);
      setLoading(false);
    }
    return () => { scene?.dispose(); sceneRef.current = null; delete window.__atlas; };
  }, [brickModel, selectPart]);

  useEffect(() => {
    sceneRef.current?.setState(state);
    if (focusAfter.current) { sceneRef.current?.focusSelection(); focusAfter.current = false; }
  }, [state, manifest]);
  useEffect(() => {
    if (!notice) return;
    const timeout = setTimeout(() => setNotice(''), 2500);
    return () => clearTimeout(timeout);
  }, [notice]);
  useEffect(() => {
    const escape = (e: KeyboardEvent) => { if (e.key === 'Escape' && !modal) setDrawer(null); };
    window.addEventListener('keydown', escape);
    return () => window.removeEventListener('keydown', escape);
  }, [modal]);
  useEffect(() => {
    if (!drawer || modal) return;
    const previous = document.activeElement as HTMLElement | null;
    const panel = document.querySelector<HTMLElement>('.sidebar.mobile-open');
    const focusable = () => [...(panel?.querySelectorAll<HTMLElement>('button:not([disabled]), input, select, a[href]') ?? [])].filter(element => element.getClientRects().length);
    focusable()[0]?.focus();
    const trap = (event: KeyboardEvent) => {
      if (event.key !== 'Tab') return;
      const items = focusable();
      const first = items[0], last = items.at(-1);
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
    };
    document.addEventListener('keydown', trap);
    return () => { document.removeEventListener('keydown', trap); if (previous?.isConnected) previous.focus(); };
  }, [drawer, modal]);

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
    if (!playing || mode !== 'build') return;
    if (currentBuildStep >= steps.length) { setPlaying(false); return; }
    const timer = setTimeout(() => patch({ buildStep: currentBuildStep + 1, assemblyRevision: state.assemblyRevision + 1 }), 1150);
    return () => clearTimeout(timer);
  }, [playing, mode, currentBuildStep, steps.length, patch, state.assemblyRevision]);
  useEffect(() => {
    if (mode !== 'build' || !readyTime || currentBuildStep < 1 || !sceneRef.current) {
      setInstructionPreview('');
      return;
    }
    let cancelled = false;
    let url = '';
    const timer = setTimeout(() => {
      sceneRef.current?.captureBuildStep(currentBuildStep, 720, 540).then(blob => {
        if (cancelled) return;
        url = URL.createObjectURL(blob);
        setInstructionPreview(url);
      }).catch(() => {});
    }, 180);
    return () => {
      cancelled = true;
      clearTimeout(timer);
      if (url) URL.revokeObjectURL(url);
    };
  }, [mode, readyTime, currentBuildStep]);

  function reset() {
    resetViewer(mode);
    setQuery(''); setDrawer(null); setDetailsOpen(true); setHover(null);
  }
  function toggleGroup(id: GroupId) {
    setState(s => ({ ...s, hiddenGroups: s.hiddenGroups.includes(id) ? s.hiddenGroups.filter(g => g !== id) : [...s.hiddenGroups, id] }));
  }
  function isolate(ids: string[]) {
    setState(s => ({ ...s, isolation: ids, hiddenGroups: [], hiddenBrickIds: [], autoRotate: false }));
    if (innerWidth < 1050) setDrawer(null);
  }
  function selectAllType() {
    setState(s => ({ ...s, selection: sameType.map(p => p.instanceId), hiddenGroups: s.hiddenGroups.filter(g => !sameType.some(p => p.groupId === g)), isolation: null }));
  }
  function exportInventory() {
    const rows = [['instanceId', 'partNumber', 'name', 'color', 'group', 'sourceFile', 'sourceLine', 'step']];
    for (const p of visible) rows.push([p.instanceId, p.partNumber, p.displayName, p.colorName, p.groupId, p.sourceFile, String(p.sourceLine), p.buildStep === null ? '' : String(p.buildStep)]);
    download('\uFEFF' + rows.map(row => row.map(v => `"${v.replaceAll('"', '""')}"`).join(',')).join('\n'), `${config.id}-inventory.csv`, 'text/csv;charset=utf-8');
    setNotice('零件清单已导出');
  }
  async function screenshot() {
    if (!sceneRef.current) return;
    try {
      const blob = await sceneRef.current.exportPng(exportSize, Math.round(exportSize * 9 / 16));
      downloadBlob(blob, `brick-atlas-${config.id}-${exportSize}p.png`);
      setNotice(`${exportSize}px 高清模型图已导出`);
    } catch (cause) {
      setNotice(cause instanceof Error ? cause.message : '高清导出失败');
    }
  }
  function setBuildStep(step: number) {
    const next = Math.max(0, Math.min(steps.length, step));
    patch({ buildStep: next, explosion: 0, autoRotate: false, isolation: null, assemblyRevision: state.assemblyRevision + 1 });
  }
  async function exportInstructions() {
    if (!sceneRef.current || !manifest?.instructions) return;
    setPlaying(false);
    setGuideExport({ current: 0, total: manifest.instructions.steps.length });
    try {
      const blob = await exportBuildGuide(sceneRef.current, config, manifest, (current, total) => setGuideExport({ current, total }));
      downloadBlob(blob, `brick-atlas-${config.id}-build-guide.pdf`);
      setNotice('完整拼装说明书 PDF 已导出');
    } catch (cause) {
      setNotice(cause instanceof Error ? cause.message : '说明书导出失败');
    } finally {
      setGuideExport(null);
    }
  }

  return <div className={`app ${mode}-mode`}>
    <header className="topbar" inert={!!drawer}>
      <a href={import.meta.env.BASE_URL} className="icon-button workspace-back" aria-label="返回项目库" title="返回项目库"><ArrowLeft size={18} /></a>
      <a href={import.meta.env.BASE_URL} className="brand" aria-label="Brick Atlas 首页">
        <span className="brand-mark"><Boxes size={23} strokeWidth={1.6} /></span>
        <strong>BRICK<span>ATLAS</span></strong>
      </a>
      <div className="top-divider" />
      <span className="workspace-label">{mode === 'build' ? '分步拼装工作台' : '模型探索空间'}</span>
      <div className="top-search"><Search size={16} /><input aria-label="顶部搜索零件" placeholder="搜索 Part ID、名称、子装配" value={query} onChange={event => setQuery(event.target.value)} /></div>
      <div className="top-actions">
        <a className="text-button source-button" href={import.meta.env.BASE_URL}><Library size={16} />项目库</a>
        <a className="text-button source-button" href={`${import.meta.env.BASE_URL}${mode === 'build' ? 'explore' : 'build'}/${config.id}`}>{mode === 'build' ? <Layers3 size={16} /> : <BookOpen size={16} />}{mode === 'build' ? '探索' : '拼装'}</a>
        {mode === 'build' && <button className="text-button source-button" disabled={!!guideExport || loading} onClick={exportInstructions}><FileDown size={16} />导出说明书</button>}
        <IconButton label="X-Ray 透视模式" active={state.xray} onClick={() => patch({ xray: !state.xray })}><Eye size={18} /></IconButton>
        <button className="text-button source-button" onClick={() => setModal('credits')}><Info size={16} />来源与署名</button>
        <IconButton label="显示设置" onClick={() => setModal('settings')}><Settings2 size={18} /></IconButton>
        <IconButton label="导出模型截图" disabled={loading || !!error} onClick={screenshot}><ArrowDownToLine size={18} /></IconButton>
      </div>
    </header>

    <div className={`workspace ${detailsOpen ? '' : 'details-collapsed'}`}>
      {drawer && <button className="drawer-backdrop" aria-label="关闭面板" onClick={() => setDrawer(null)} />}
      <aside className={`sidebar left-sidebar ${drawer === 'layers' ? 'mobile-open' : ''}`} aria-label="模型结构与搜索" role={drawer === 'layers' ? 'dialog' : undefined} aria-modal={drawer === 'layers' ? true : undefined}>
        <div className="set-heading">
          <div className="eyebrow"><span className="set-number">{config.id}</span><span>{config.theme.split(' ')[0].toUpperCase()} / {config.year}</span><IconButton className="mobile-close" label="关闭结构面板" onClick={() => setDrawer(null)}><X size={18} /></IconButton></div>
          <h1>{config.title}</h1>
          <div className="set-subtitle">{config.subtitle} <span className="tiny-divider" /> {config.theme.replace('Creator ', '')}</div>
          <label className="model-switcher"><Library size={15} /><span>切换模型</span><select aria-label="切换模型" value={config.id} onChange={event => { location.href = `${import.meta.env.BASE_URL}${mode}/${event.target.value}`; }}>{modelCatalog.map(model => <option key={model.id} value={model.id}>{model.setNumber} · {model.title}</option>)}</select><ChevronDown size={12} /></label>
          <div className="set-stats"><div><strong>{manifest?.stats.instances ?? '—'}</strong><span>零件实例</span></div><div><strong>{manifest?.stats.uniqueParts ?? '—'}</strong><span>零件型号</span></div><div><strong>{manifest?.stats.colors ?? '—'}</strong><span>颜色</span></div></div>
        </div>
        <div className="search-wrap"><Search size={17} /><input aria-label="搜索零件" placeholder="搜索零件、颜色、编号" value={query} onChange={e => { setQuery(e.target.value); if (e.target.value) setTab('parts'); }} />{query && <IconButton label="清空搜索" onClick={() => setQuery('')}><X size={14} /></IconButton>}</div>
        <div className="panel-tabs" role="tablist" aria-label="浏览方式">
          <button role="tab" aria-selected={tab === 'structure'} onClick={() => setTab('structure')}><Layers3 size={16} />结构分组</button>
          <button role="tab" aria-selected={tab === 'parts'} onClick={() => setTab('parts')}><Boxes size={16} />零件清单</button>
        </div>
        <div className="panel-scroll">
          {tab === 'structure' ? <>
            <div className="list-heading"><span>结构层级</span><button onClick={() => patch({ hiddenGroups: [], hiddenBrickIds: [], isolation: null })}>全部显示</button></div>
            <button className="root-row" onClick={() => patch({ hiddenGroups: [], hiddenBrickIds: [], isolation: null })}><ChevronDown size={15} /><Box size={17} /><strong>完整模型</strong><span>{manifest?.stats.instances ?? 0}</span></button>
            <div className="group-list">{manifest?.groups.map(group => {
              const count = visible.filter(p => p.groupId === group.id).length;
              const hidden = state.hiddenGroups.includes(group.id);
              return <div className={`group-row ${hidden ? 'hidden-group' : ''}`} key={group.id}>
                <span className="tree-line" /><span className="group-dot" style={{ background: group.color }} />
                <button className="group-name" onClick={() => isolate(group.instanceIds)} title={`只看${group.name}`}>{group.name}</button>
                <span className="group-count">{count}</span>
                <IconButton label={`${hidden ? '显示' : '隐藏'}${group.name}`} active={undefined} onClick={() => toggleGroup(group.id)}>{hidden ? <EyeOff size={15} /> : <Eye size={15} />}</IconButton>
              </div>;
            })}</div>
            <div className="section-rule" />
            <div className="list-heading"><span>原始子模型</span><span>{manifest?.submodels.length ?? 0}</span></div>
            <div className="submodel-list">{manifest?.submodels.filter(s => s.parentId).map(submodel => <button key={submodel.id} onClick={() => isolate(manifest.instances.filter(p => p.parentSubmodelId === submodel.id).map(p => p.instanceId))}><Box size={14} /><span>{submodel.name}</span><ChevronRight size={13} /></button>)}</div>
          </> : <>
            <div className="list-heading"><span>{query ? '搜索结果' : '所有零件'}</span><span>{results.length} 个实例</span></div>
            {resultGroups.length === 0 ? <div className="empty-results"><Search size={24} /><strong>没有匹配的零件</strong><button className="text-button" onClick={() => setQuery('')}>清空筛选</button></div> : resultGroups.map(parts => {
              const part = parts[0];
              return <button key={`${part.partNumber}:${part.colorCode}`} className={`part-row ${state.selection.some(id => parts.some(p => p.instanceId === id)) ? 'selected' : ''}`} onClick={() => selectPart(part.instanceId, true)}>
                <span className="part-swatch" style={{ backgroundColor: part.colorHex }}><Box size={19} color={['15', '19', '47', '71'].includes(part.colorCode) ? '#53615b' : '#ffffff'} strokeWidth={1.3} /></span>
                <span className="part-row-text"><strong>{part.displayName}</strong><small>{part.partNumber}<span>·</span>{colorLabels[part.colorCode] ?? part.colorName}</small></span><span className="quantity">{parts.length}</span>
              </button>;
            })}
          </>}
        </div>
        <div className="sidebar-footer"><span className="status-dot" /><span>{visible.length} / {manifest?.stats.instances ?? 0} 个实例可见</span><IconButton label="导出可见零件 CSV" disabled={!manifest} onClick={exportInventory}><ArrowDownToLine size={15} /></IconButton></div>
      </aside>

      <main className="main-stage" aria-label="模型探索器" inert={!!drawer}>
        <div className="stage-heading">
          <div><span className="eyebrow">{mode === 'build' ? 'BUILD INSTRUCTIONS' : 'MODEL EXPLORER'}</span><div className="stage-title">{config.title}<span>{config.id}</span></div></div>
          <div className="stage-status"><span className={`status-dot ${loading ? 'loading-dot' : ''}`} />{error ? '载入失败' : loading ? `${Math.floor(progress)}%` : `${visible.length} 个零件`}</div>
        </div>
        <div className="mobile-top-tools"><button onClick={() => setDrawer('layers')}><Layers3 size={17} />结构与零件</button><IconButton label={mode === 'build' ? '打开步骤说明书' : '打开详情'} onClick={() => { setDetailsOpen(true); setDrawer('details'); }}>{mode === 'build' ? <BookOpen size={18} /> : <Info size={18} />}</IconButton></div>
        <div className="canvas-host" ref={stageRef} />
        {mode === 'build' && selected && sceneRef.current && <SelectedPartPreview scene={sceneRef.current} part={selected} onClose={() => patch({ selection: [] })} />}
        <div className="viewport-toolbar" aria-label="视角工具">
          <div className="view-select"><Box size={16} /><select aria-label="模型视角" value={state.view} onChange={e => patch({ view: e.target.value as ExplorerState['view'], revision: state.revision + 1 })}>{Object.entries(viewNames).map(([id, name]) => <option key={id} value={id}>{name}</option>)}</select><ChevronDown size={12} /></div>
          <div className="toolbar-divider" />
          <IconButton label="自动旋转" active={state.autoRotate} disabled={state.explosion >= 0.98} onClick={() => patch({ autoRotate: !state.autoRotate })}><Rotate3D size={18} /></IconButton>
          <IconButton label="适配全部可见零件" onClick={() => patch({ revision: state.revision + 1 })}><Expand size={18} /></IconButton>
          <IconButton label="零件边线" active={state.edges} onClick={() => patch({ edges: !state.edges })}><Box size={17} /></IconButton>
          <IconButton label="X-Ray 透视模式" active={state.xray} onClick={() => patch({ xray: !state.xray })}><Eye size={17} /></IconButton>
        </div>
        <div className="zoom-tools">
          <IconButton label="放大模型" onClick={() => sceneRef.current?.zoom(0.8)}><Plus size={18} /></IconButton>
          <IconButton label="缩小模型" onClick={() => sceneRef.current?.zoom(1.25)}><Minus size={18} /></IconButton>
          <div />
          <IconButton label="复原模型" onClick={reset}><RotateCcw size={17} /></IconButton>
        </div>
        {!detailsOpen && <IconButton className="reopen-details" label={mode === 'build' ? '打开步骤说明书' : '打开详情面板'} onClick={() => setDetailsOpen(true)}>{mode === 'build' ? <BookOpen size={18} /> : <Info size={18} />}</IconButton>}
        {state.isolation && <div className="isolation-indicator"><Focus size={14} />隔离中 · {visible.length} 个零件<button aria-label="退出隔离" title="退出隔离" onClick={() => patch({ isolation: null })}><X size={15} /></button></div>}
        {state.selection.length > 0 && <div className="selection-indicator"><span className="status-dot" /><button onClick={() => { setDetailsOpen(true); if (innerWidth < 1050) setDrawer('details'); }}>已选 {state.selection.length} 个零件</button><IconButton label="清除选择" onClick={() => patch({ selection: [] })}><X size={14} /></IconButton></div>}
        {!loading && !error && visible.length === 0 && mode !== 'build' && <div className="empty-stage"><EyeOff size={32} /><strong>所有零件已隐藏</strong><button className="primary-button" onClick={() => patch({ hiddenGroups: [], hiddenBrickIds: [], isolation: null })}><Eye size={16} />显示全部</button></div>}
        {(loading || error) && <div className={`loading-state ${error ? 'error-state' : ''}`} role={error ? 'alert' : 'status'}>
          {error ? <><Info size={30} /><strong>模型暂时无法显示</strong><p>{error}</p><button className="primary-button" onClick={() => { sceneRef.current?.dispose(); sceneRef.current = null; setManifest(null); setRetry(r => r + 1); }}><RotateCcw size={16} />重新加载</button><a href={`${base}model.packed.mpd`} download>下载源模型</a></> : <><LoaderCircle className="spinner" size={26} /><strong>{stage}</strong><progress max={100} value={progress} /><span>{Math.floor(progress)}%</span></>}
        </div>}
        <div className="scene-corner"><span>LDRAW</span><span>毫米 · 1:1</span></div>
        {mode === 'build' ? <section className="explosion-dock build-dock" aria-label="拼装步骤控制">
          <div className="dock-heading"><div><BookOpen size={18} /><strong>{currentBuildStep === 0 ? '准备拼装' : activeStep?.title}</strong><span className="phase-name">{manifest?.instructions?.provenance === 'source' ? 'OMR 源步骤' : '结构演示'}</span></div><output aria-live="polite">{currentBuildStep}<span> / {steps.length}</span></output></div>
          <div className="step-controls">
            <IconButton label="回到开始" disabled={currentBuildStep === 0} onClick={() => setBuildStep(0)}><SkipBack size={17} /></IconButton>
            <IconButton label="上一步" disabled={currentBuildStep === 0} onClick={() => setBuildStep(currentBuildStep - 1)}><ArrowLeft size={18} /></IconButton>
            <IconButton label={playing ? '暂停自动拼装' : '自动播放拼装'} active={playing} disabled={!steps.length || currentBuildStep === steps.length} onClick={() => setPlaying(value => !value)}>{playing ? <Pause size={18} /> : <Play size={18} />}</IconButton>
            <input type="range" min={0} max={steps.length} value={currentBuildStep} aria-label="当前拼装步骤" aria-valuetext={`第 ${currentBuildStep} 步，共 ${steps.length} 步`} onChange={event => setBuildStep(Number(event.target.value))} style={{ '--range-fill': `${steps.length ? currentBuildStep / steps.length * 100 : 0}%` } as React.CSSProperties} />
            <IconButton label="下一步" disabled={currentBuildStep === steps.length} onClick={() => setBuildStep(currentBuildStep + 1)}><ArrowRight size={18} /></IconButton>
            <IconButton label="完成模型" disabled={currentBuildStep === steps.length} onClick={() => setBuildStep(steps.length)}><SkipForward size={17} /></IconButton>
          </div>
          <div className="step-parts">{currentBuildStep === 0
            ? <span>整理零件并选择“下一步”开始</span>
            : <><strong>本步 {activeStepParts?.length ?? 0} 件</strong>{activeStepParts?.slice(0, 4).map(part => <button key={part.instanceId} onClick={() => selectPart(part.instanceId, true)}><span style={{ background: part.colorHex }} />{part.partNumber}</button>)}{(activeStepParts?.length ?? 0) > 4 && <span>+{activeStepParts!.length - 4}</span>}</>}
          </div>
          <p className="instruction-note">{manifest?.instructions?.disclaimer}</p>
        </section> : <section className="explosion-dock" aria-label="拆解控制">
          <div className="dock-heading"><div><Layers3 size={18} /><strong>拆解程度</strong><span className="phase-name">{state.explosion === 0 ? '完整装配' : state.explosion <= 0.45 ? '结构分离' : state.explosion === 1 ? '零件陈列' : '实例展开'}</span></div><output aria-live="off">{Math.round(state.explosion * 100)}<span>%</span></output></div>
          <div className="slider-row"><Box size={18} /><input type="range" min={0} max={100} step={1} value={Math.round(state.explosion * 100)} aria-label="拆解程度" aria-valuetext={`${Math.round(state.explosion * 100)}%`} onChange={e => patch({ explosion: Number(e.target.value) / 100, autoRotate: false })} style={{ '--range-fill': `${state.explosion * 100}%` } as React.CSSProperties} /><Grid2X2 size={18} /></div>
          <div className="dock-presets"><button className={state.explosion === 0 ? 'current' : ''} onClick={() => patch({ explosion: 0 })}>完整装配<span>0%</span></button><button className={state.explosion === 0.45 ? 'current' : ''} onClick={() => patch({ explosion: 0.45, autoRotate: false })}>结构分离<span>45%</span></button><button className={state.explosion === 1 ? 'current' : ''} onClick={() => patch({ explosion: 1, autoRotate: false })}>零件陈列<span>100%</span></button></div>
        </section>}
      </main>

      <aside className={`sidebar right-sidebar ${drawer === 'details' ? 'mobile-open' : ''}`} aria-label={mode === 'build' ? '步骤说明书' : '零件详情'} role={drawer === 'details' ? 'dialog' : undefined} aria-modal={drawer === 'details' ? true : undefined}>
        <header className="detail-header"><span>{mode === 'build' ? <BookOpen size={16} /> : <CircleDot size={16} />}{mode === 'build' ? '步骤说明书' : selected ? '零件详情' : '套装档案'}</span><IconButton label="关闭详情面板" onClick={() => { setDetailsOpen(false); setDrawer(null); }}><X size={17} /></IconButton></header>
        <div className="detail-scroll">
          {mode === 'build' ? <div className="instruction-sidebar">
            <div className="instruction-page-heading"><span>STEP</span><strong>{currentBuildStep || '—'}</strong><small>/ {steps.length}</small></div>
            {currentBuildStep === 0 ? <div className="instruction-start"><BookOpen size={32} /><h2>准备开始拼装</h2><p>左侧整理零件，点击“下一步”查看第一张说明页和入位动画。</p><button className="primary-button" onClick={() => setBuildStep(1)}>进入第 1 步<ArrowRight size={16} /></button></div> : <>
              <div className="instruction-static-frame">
                {instructionPreview ? <img src={instructionPreview} alt={`第 ${currentBuildStep} 步静态拼装图`} /> : <LoaderCircle className="spinner" size={24} />}
                <span>本步新增积木以绿色高亮</span>
              </div>
              <div className="instruction-step-title"><span>{manifest?.instructions?.provenance === 'source' ? 'OMR AUTHOR STEP' : 'EDITORIAL STRUCTURE STEP'}</span><h2>{activeStep?.title}</h2></div>
              <section className="instruction-parts" aria-label="本步所需零件">
                <h3>本步所需零件 <span>{activeStepParts?.length ?? 0}</span></h3>
                {activePartGroups.map(group => <button key={group.key} onClick={() => selectPart(group.instanceIds[0], true)}>
                  <span className="instruction-part-swatch" style={{ background: group.colorHex }}><Box size={18} color={['15', '19', '47', '71'].includes(manifest?.instances.find(part => part.instanceId === group.instanceIds[0])?.colorCode ?? '') ? '#53615b' : '#fff'} /></span>
                  <span><strong>{group.quantity}× {group.partNumber}</strong><small>{group.name}<br />{group.colorName}</small></span>
                </button>)}
              </section>
              <div className="instruction-side-nav"><button disabled={currentBuildStep === 1} onClick={() => setBuildStep(currentBuildStep - 1)}><ArrowLeft size={16} />上一步</button><button disabled={currentBuildStep === steps.length} onClick={() => setBuildStep(currentBuildStep + 1)}>下一步<ArrowRight size={16} /></button></div>
            </>}
            <section className="instruction-index"><h3>步骤目录</h3><div>{steps.map((step, index) => <button key={step.id} className={currentBuildStep === index + 1 ? 'current' : ''} onClick={() => setBuildStep(index + 1)}><span>{index + 1}</span><strong>{step.title}</strong><small>{step.instanceIds.length} 件</small></button>)}</div></section>
            <button className="primary-button guide-export" disabled={!!guideExport || loading} onClick={exportInstructions}>{guideExport ? <LoaderCircle className="spinner" size={16} /> : <FileDown size={16} />}{guideExport ? `正在生成 ${guideExport.current} / ${guideExport.total}` : '导出完整说明书 PDF'}</button>
            <p className="guide-disclaimer">{manifest?.instructions?.disclaimer}</p>
          </div> : selected ? <>
            <div className="part-identity"><div className="eyebrow">{selected.instanceId}</div><div className="part-number">{selected.partNumber}<span className="identity-swatch" style={{ background: selected.colorHex }} /></div><h2>{selected.displayName}</h2><div className="color-label"><span style={{ background: selected.colorHex }} />{colorLabels[selected.colorCode] ?? selected.colorName}<small>{selected.colorCode}</small></div></div>
            <div className="part-actions"><button className="primary-button" onClick={() => isolate(state.selection)}><Focus size={16} />隔离选择</button><IconButton label="隐藏选中积木" onClick={() => patch({ hiddenBrickIds: [...new Set([...state.hiddenBrickIds, ...state.selection])], selection: [] })}><EyeOff size={18} /></IconButton><IconButton label="聚焦选中零件" onClick={() => { sceneRef.current?.focusSelection(); if (innerWidth < 1050) setDrawer(null); }}><Crosshair size={18} /></IconButton></div>
            <dl className="metadata"><div><dt>Part ID</dt><dd>{selected.partNumber}</dd></div><div><dt>颜色</dt><dd>{selected.colorName}</dd></div><div><dt>尺寸</dt><dd>{selectedBrick?.dimensions.map(value => `${value.toFixed(1)}`).join(' × ')} mm</dd></div><div><dt>模型内数量</dt><dd>{sameType.length} 个</dd></div><div><dt>Subassembly</dt><dd>{selectedAssembly?.name ?? selectedGroup?.name}</dd></div><div><dt>所属结构</dt><dd><span className="group-dot" style={{ background: selectedGroup?.color }} />{selectedGroup?.name}</dd></div><div><dt>装配步骤</dt><dd>{selected.buildStep === null ? '结构演示' : `源步骤 ${selected.buildStep}`}</dd></div></dl>
            <div className="detail-section"><h3>同型号实例 <span>{sameType.length}</span></h3><div className="instance-navigation"><IconButton label="上一个同型号实例" onClick={() => selectPart(sameType[(sameType.findIndex(p => p.instanceId === selected.instanceId) + sameType.length - 1) % sameType.length].instanceId, true)}><ArrowLeft size={16} /></IconButton><span>{sameType.findIndex(p => p.instanceId === selected.instanceId) + 1} / {sameType.length}</span><IconButton label="下一个同型号实例" onClick={() => selectPart(sameType[(sameType.findIndex(p => p.instanceId === selected.instanceId) + 1) % sameType.length].instanceId, true)}><ArrowRight size={16} /></IconButton></div><button className="secondary-button" onClick={selectAllType}><Boxes size={16} />高亮全部同型号</button><button className="secondary-button" onClick={() => isolate(sameType.map(p => p.instanceId))}><Focus size={16} />隔离全部同型号</button></div>
            <div className="detail-section"><h3>来源路径</h3><div className="source-path">{selected.path.map((p, i) => <div key={`${p}-${i}`}><ChevronRight size={12} /><span>{p}</span></div>)}<div><ChevronRight size={12} /><strong>{selected.partNumber}.dat</strong></div></div><div className="source-line">原始 MPD · 第 {selected.sourceLine} 行</div><button className="secondary-button" onClick={() => isolate(manifest!.instances.filter(p => p.parentSubmodelId === selected.parentSubmodelId).map(p => p.instanceId))}><Layers3 size={16} />隔离所属子模型</button><a className="source-link" href={`${base}model.packed.mpd`} download><ExternalLink size={13} />查看打包源文件</a></div>
          </> : <>
            <div className="model-identity"><span className="archive-icon"><Box size={32} strokeWidth={1.2} /></span><div className="eyebrow">MODEL NO. {config.id}</div><h2>{config.title}</h2><p>{config.subtitle}</p><span className="model-tag">{config.theme}</span></div>
            <dl className="metadata"><div><dt>发行年份</dt><dd>{config.year}</dd></div><div><dt>模型实例</dt><dd>{manifest?.stats.instances ?? '—'}</dd></div><div><dt>独立零件型号</dt><dd>{manifest?.stats.uniqueParts ?? '—'}</dd></div><div><dt>拼装步骤</dt><dd>{steps.length || '—'}</dd></div><div><dt>步骤来源</dt><dd>{manifest?.instructions?.provenance === 'source' ? 'OMR 作者' : '结构演示'}</dd></div><div><dt>几何来源</dt><dd>LDraw OMR</dd></div><div><dt>模型许可</dt><dd>{config.license}</dd></div></dl>
            <div className="detail-section"><h3>模型配色 <span>{colors.length}</span></h3><div className="color-palette">{colors.map(([code, color]) => <button key={code} style={{ backgroundColor: color.hex }} aria-label={`筛选颜色 ${color.name}`} title={`${colorLabels[code] ?? color.name} · ${color.count}`} onClick={() => { setQuery(color.name); setTab('parts'); if (innerWidth < 1050) setDrawer('layers'); }} />)}</div><div className="color-distribution">{colors.map(([code, color]) => <span key={code} style={{ backgroundColor: color.hex, flex: color.count }} />)}</div></div>
            <div className="detail-section provenance-summary"><ShieldCheck size={20} /><div><strong>开放模型，来源可追溯</strong><span>{config.author.split(' [')[0]}</span><a href={config.sourceUrl} target="_blank" rel="noreferrer">Official Model Repository<ExternalLink size={12} /></a></div></div>
            <button className="secondary-button inventory-download" onClick={exportInventory} disabled={!manifest}><ArrowDownToLine size={16} />导出零件清单</button>
          </>}
        </div>
        <div className="detail-footer"><ShieldCheck size={14} /><span>非 LEGO 官方产品</span><button onClick={() => setModal('credits')}>许可信息</button></div>
      </aside>
    </div>
    <footer className="app-footer"><span><span className="status-dot" />{loading ? '模型载入中' : error ? '资源异常' : '模型已就绪'}</span><span>LDraw 几何 · {manifest ? `${(manifest.stats.triangles / 1000).toFixed(1)}k 三角面` : '—'}</span><span>BRICK ATLAS <span className="footer-version">v1.0</span></span></footer>
    {hover && !drawer && !loading && <div className="part-tooltip" style={{ left: Math.min(hover.x + 16, innerWidth - 260), top: Math.min(hover.y + 16, innerHeight - 80) }}><strong>{hover.part.partNumber}</strong><span>{hover.part.displayName}</span></div>}
    {notice && <div className="toast" role="status"><Check size={16} />{notice}</div>}
    {modal === 'settings' && <Modal title="显示设置" onClose={() => setModal(null)}><div className="settings-content">
      <label>渲染质量<select value={state.quality} onChange={e => patch({ quality: e.target.value as ExplorerState['quality'] })}><option value="auto">自动 · 根据屏幕调整</option><option value="high">高 · 2x 像素密度</option><option value="ultra">超清 · 3x 像素密度</option><option value="low">性能 · 1x，无边线</option></select></label>
      <label>工作台背景<select value={state.background} onChange={e => patch({ background: e.target.value as ExplorerState['background'] })}><option value="studio">工作室灰</option><option value="white">纯白</option><option value="dark">深色</option></select></label>
      <label>导出分辨率<select value={exportSize} onChange={e => setExportSize(Number(e.target.value))}><option value={1920}>Full HD · 1920 × 1080</option><option value={3840}>4K · 3840 × 2160</option><option value={7680}>8K · 7680 × 4320</option></select></label>
      <label className="checkbox-row"><span>显示零件边线</span><input type="checkbox" checked={state.edges} onChange={e => patch({ edges: e.target.checked })} /></label>
      <label className="checkbox-row"><span>显示参考网格</span><input type="checkbox" checked={state.grid} onChange={e => patch({ grid: e.target.checked })} /></label>
      <label className="checkbox-row"><span>X-Ray 透视</span><input type="checkbox" checked={state.xray} onChange={e => patch({ xray: e.target.checked })} /></label>
      <label className="checkbox-row"><span>自动旋转</span><input type="checkbox" disabled={state.explosion >= 0.98} checked={state.autoRotate} onChange={e => patch({ autoRotate: e.target.checked })} /></label>
      <button className="primary-button settings-export" onClick={screenshot}><ArrowDownToLine size={16} />导出高清 PNG</button>
      <dl className="metadata"><div><dt>几何压缩体积</dt><dd>{manifest ? (manifest.stats.compressedBytes / 1024 / 1024).toFixed(2) : '—'} MiB</dd></div><div><dt>本次完整加载</dt><dd>{readyTime ? `${(readyTime / 1000).toFixed(2)} s` : '—'}</dd></div><div><dt>绘制调用</dt><dd>{sceneRef.current?.metrics.drawCalls ?? '—'}</dd></div><div><dt>减弱动态效果</dt><dd>{matchMedia('(prefers-reduced-motion: reduce)').matches ? '已启用' : '未启用'}</dd></div></dl>
      <button className="secondary-button" onClick={() => download(JSON.stringify(diagnosticsReport(), null, 2), 'brick-atlas-diagnostics.json', 'application/json')}><ArrowDownToLine size={16} />导出本次运行诊断</button>
    </div></Modal>}
    {modal === 'credits' && <Modal title="来源与署名" onClose={() => setModal(null)}><div className="credits-content"><div className="credit-brand"><Boxes size={24} /><strong>Brick Atlas</strong><span>非官方积木模型探索器</span></div><p>本项目为非官方社区项目，与 LEGO Group 无隶属、赞助或认可关系。LEGO 是 LEGO Group 的商标。</p><h3>套装模型</h3><p>{config.setNumber} {config.title} · {config.author}<br /><a href={config.licenseUrl} target="_blank" rel="noreferrer">Creative Commons Attribution 2.0</a><br /><a href={config.sourceUrl} target="_blank" rel="noreferrer">OMR 模型来源页 <ExternalLink size={12} /></a></p><h3>零件库</h3><p>LDraw.org 官方零件库 · 2026-08-31 快照。每个文件的作者、许可及历史保留在打包源文件中；CC BY 2.0、CC BY 4.0 等许可按文件头分别适用。</p><div className="credit-links"><a href={`${base}credits.json`} target="_blank" rel="noreferrer">逐文件署名</a><a href={`${base}CAlicense.txt`} target="_blank" rel="noreferrer">CC BY 2.0 全文</a><a href={`${base}CAlicense4.txt`} target="_blank" rel="noreferrer">CC BY 4.0 全文</a><a href={`${base}provenance.json`} target="_blank" rel="noreferrer">来源与哈希</a></div><h3>步骤声明</h3><p>{manifest?.instructions?.disclaimer}</p><h3>加工与完整性声明</h3><p>模型已做依赖打包、毫米坐标转换、语义分组、实例索引、几何合批和无损压缩。原始模型未修改，几何未减面。</p><ul>{manifest?.model.notes.map(note => <li key={note}>{note}</li>)}</ul><h3>应用代码</h3><p>MIT License · React · Three.js · Lucide<br />源码及构建、测试方法随项目提供。</p><a className="secondary-button" href={`${base}build-report.json`} target="_blank" rel="noreferrer"><ShieldCheck size={16} />查看资产构建报告</a></div></Modal>}
  </div>;
}

function CatalogPage() {
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
  return <div className="catalog-page">
    <header className="topbar">
      <a href={import.meta.env.BASE_URL} className="brand"><span className="brand-mark"><Boxes size={23} /></span><strong>BRICK<span>ATLAS</span></strong></a>
      <div className="top-divider" /><span className="workspace-label">项目工作空间</span>
      <nav className="top-actions"><a className="text-button" href={`${import.meta.env.BASE_URL}create`}><Upload size={16} />导入项目</a></nav>
    </header>
    <main className="catalog-shell">
      <section className="catalog-heading"><div><span className="eyebrow">MODEL LIBRARY</span><h1>积木项目</h1><p>选择模型进入结构探索，或从第一个零件开始分步拼装。</p></div><dl><div><dt>项目</dt><dd>{modelCatalog.length}</dd></div><div><dt>套装</dt><dd>{new Set(modelCatalog.map(model => model.setNumber)).size}</dd></div><div><dt>可拼装实例</dt><dd>{Object.values(summaries).reduce((sum, item) => sum + item.stats.instances, 0) || '—'}</dd></div></dl></section>
      <section className="model-grid" aria-label="积木模型项目">
        {modelCatalog.map((model, index) => <article className="model-card" key={model.id}>
          <a className="model-card-explore" href={`${import.meta.env.BASE_URL}explore/${model.id}`} aria-label={`探索 ${model.title}`}>
            <div className={`model-art art-${index % 5}`}><img src={`${import.meta.env.BASE_URL}models/${model.id}/preview.png`} alt={`${model.title} 三维模型预览`} /><Boxes size={42} aria-hidden="true" /></div>
            <div className="model-card-body"><div className="eyebrow"><span className="set-number">{model.id}</span>{model.category} / {model.year}</div><h2>{model.title}</h2><p>{model.subtitle}</p>
              <dl className="model-card-specs">
                <div><dt>积木</dt><dd>{summaries[model.id]?.stats.instances ?? '—'}</dd></div>
                <div><dt>零件型号</dt><dd>{summaries[model.id]?.stats.uniqueParts ?? '—'}</dd></div>
                <div><dt>积木树</dt><dd>{summaries[model.id]?.treeNodes ?? '—'}</dd></div>
                <div><dt>拼装步骤</dt><dd>{summaries[model.id]?.steps ?? '—'}</dd></div>
                <div><dt>几何面</dt><dd>{summaries[model.id] ? `${(summaries[model.id].stats.triangles / 1000).toFixed(0)}k` : '—'}</dd></div>
                <div><dt>步骤来源</dt><dd>{summaries[model.id]?.provenance === 'source' ? 'OMR' : '结构'}</dd></div>
              </dl>
            </div>
          </a>
          <div className="model-card-actions"><a className="primary-link" href={`${import.meta.env.BASE_URL}build/${model.id}`}><BookOpen size={16} />开始拼装</a></div>
        </article>)}
      </section>
      <p className="catalog-legal">非官方社区项目。模型来自 LDraw OMR；LEGO 是 LEGO Group 的商标。</p>
    </main>
  </div>;
}

function CreatorPage() {
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
    <header className="topbar"><a href={import.meta.env.BASE_URL} className="brand"><span className="brand-mark"><Boxes size={23} /></span><strong>BRICK<span>ATLAS</span></strong></a><div className="top-divider" /><span className="workspace-label">Creator</span><nav className="top-actions"><a className="text-button" href={import.meta.env.BASE_URL}><Library size={16} />项目库</a></nav></header>
    <main className="creator-shell"><section className="creator-workbench"><div><span className="eyebrow">LOCAL PROJECT IMPORT</span><h1>导入 LDraw 模型</h1><p>选择 `.ldr` 或 `.mpd` 文件进行本地预检。文件不会上传；正式发布仍需完成零件依赖、许可与哈希构建。</p></div><label className="upload-zone"><Upload size={28} /><strong>选择 LDraw 文件</strong><span>.ldr / .mpd</span><input type="file" accept=".ldr,.mpd,text/plain" onChange={event => inspectFile(event.target.files?.[0])} /></label>{report && <div className="import-report"><h2>{report.name}</h2><dl><div><dt>Type-1 引用</dt><dd>{report.references}</dd></div><div><dt>STEP 标记</dt><dd>{report.steps}</dd></div><div><dt>内嵌文件</dt><dd>{report.files}</dd></div></dl><p>{report.steps ? '检测到作者步骤，可进入资产审核与构建流程。' : '未检测到 STEP；发布前需要明确标注为结构演示。'}</p></div>}</section></main>
  </div>;
}

export default function App() {
  const relative = location.pathname.slice(import.meta.env.BASE_URL.replace(/\/$/, '').length) || '/';
  if (relative === '/' || relative === '') return <CatalogPage />;
  if (relative === '/create' || relative === '/create/') return <CreatorPage />;
  const match = /^\/(explore|build)\/([^/]+)\/?$/.exec(relative);
  const config = match ? modelCatalog.find(model => model.id === decodeURIComponent(match[2])) : null;
  if (match && config) return <ExplorerWorkspace config={config} mode={match[1] as 'explore' | 'build'} />;
  return <div className="route-error"><Boxes size={38} /><h1>项目不存在</h1><a className="primary-button" href={import.meta.env.BASE_URL}>返回项目库</a></div>;
}
