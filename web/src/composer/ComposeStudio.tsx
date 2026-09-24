import { useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowDown, ArrowLeft, ArrowRight, ArrowUp, BookOpen, Boxes, Box,
  Check, Copy, Crosshair, Download, Expand, Grid2X2, Hand, Layers3,
  Minus, Pause, Play, Plus, Rotate3D, RotateCw, Save, SkipBack,
  SkipForward, Trash2, Undo2, Redo2, Upload, Search,
} from 'lucide-react';
import type { Locale, Translator } from '../app/locale';
import { readLocal } from '../app/storage';
import { useProjectHistory } from '../app/useProjectHistory';
import { useProjectAutosave } from '../app/useProjectAutosave';
import { ProjectShelf } from '../ui/ProjectShelf';
import { loadSourceGeometry, type SourceGeometry } from '../scene/sourceGeometry';
import { ImageBrickScene, type ImageBrickView } from '../scene/ImageBrickScene';
import { IconButton, Modal } from '../ui/Controls';
import { brickPalette, imageBrickBuildToLdraw } from '../creator/imageBrickModel';
import {
  baseplateCatalog,
  canPlaceItem,
  changeBaseplate,
  composerAssets,
  createComposerItem,
  createCompositionBuild,
  createCompositionProject, readCompositionProject,
  sourceBricksFromManifest,
  type ComposerAsset,
  type ComposerItem,
  type CompositionProject,
  type QuarterTurn,
} from './compositionModel';

declare global {
  interface Window {
    __composer?: () => ReturnType<ImageBrickScene['snapshot']> & {
      items: number;
      selectedItem: string | null;
      mode: ComposerMode;
    };
  }
}

type LibraryTab = 'models' | 'scenes' | 'parts';
type ComposerMode = 'edit' | 'build' | 'explode';
const storageKey = 'brick-atlas-composition-v1';

function download(data: string, filename: string, type: string) {
  const url = URL.createObjectURL(new Blob([data], { type }));
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export function ComposeStudio({ locale, tr }: { locale: Locale; tr: Translator }) {
  const hostRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<ImageBrickScene | null>(null);
  const fitNextBuild = useRef(true);
  const [loaded] = useState(() => {
    const raw = readLocal(storageKey);
    try { return { project: raw ? readCompositionProject(raw) : createCompositionProject(), invalid: false }; }
    catch { return { project: createCompositionProject(), invalid: true }; }
  });
  const { project, setProject, hydrate, undo, redo, canUndo, canRedo } = useProjectHistory(loaded.project);
  const autosave = useProjectAutosave(storageKey, project, loaded.invalid);
  const projectRef = useRef(project);
  projectRef.current = project;
  const loadingRef = useRef(false);
  const [sources, setSources] = useState<ReadonlyMap<string, SourceGeometry>>(new Map());
  const [sourceError, setSourceError] = useState('');
  const [query, setQuery] = useState('');
  const [pendingImport, setPendingImport] = useState<CompositionProject | null>(null);
  const fileInput = useRef<HTMLInputElement>(null);
  const [selectedId, setSelectedId] = useState<string | null>(project.items[0]?.id ?? null);
  const [libraryTab, setLibraryTab] = useState<LibraryTab>('models');
  const [mode, setMode] = useState<ComposerMode>('edit');
  const [view, setView] = useState<ImageBrickView>('perspective');
  const [step, setStep] = useState(1);
  const [explosion, setExplosion] = useState(0);
  const [autoRotate, setAutoRotate] = useState(false);
  const [panMode, setPanMode] = useState(false);
  const [followStep, setFollowStep] = useState(false);
  const [playing, setPlaying] = useState(false);
  const [loadingAsset, setLoadingAsset] = useState<string | null>(null);
  const [notice, setNotice] = useState('');
  const build = useMemo(() => createCompositionBuild(project, new Map([...sources].map(([id, source]) => [id, source.manifest]))), [project.items, project.baseplateId, sources]);
  const sourcesReady = project.items.every(item => !item.sourceModelId || sources.has(item.sourceModelId));
  const selected = project.items.find(item => item.id === selectedId) ?? null;
  const base = baseplateCatalog.find(item => item.id === project.baseplateId) ?? baseplateCatalog[0];
  const visibleAssets = composerAssets.filter(asset => {
    if (!`${asset.nameZh} ${asset.nameEn} ${asset.id}`.toLowerCase().includes(query.trim().toLowerCase())) return false;
    if (libraryTab === 'models') return asset.kind === 'model';
    if (libraryTab === 'parts') return asset.kind === 'part';
    return asset.kind === 'character' || asset.kind === 'animal';
  });

  useEffect(() => {
    const missing = [...new Set(project.items.map(item => item.sourceModelId).filter((id): id is string => !!id && !sources.has(id)))];
    if (!missing.length) return;
    let cancelled = false;
    (async () => {
      const loaded = new Map(sources);
      for (const id of missing) loaded.set(id, await loadSourceGeometry(id));
      if (cancelled) return;
      // Upgrade saved box approximations from the canonical source without changing placement or IDs.
      const restored = { ...projectRef.current, items: projectRef.current.items.map(item => {
        const source = item.sourceModelId ? loaded.get(item.sourceModelId) : undefined;
        if (!source) return item;
        const bricks = sourceBricksFromManifest(source.manifest);
        return { ...item, bricks, footprint: [
          Math.ceil((source.manifest.bounds.max[0] - source.manifest.bounds.min[0]) / 8),
          Math.ceil((source.manifest.bounds.max[2] - source.manifest.bounds.min[2]) / 8),
        ] as [number, number] };
      }) };
      readCompositionProject(JSON.stringify(restored));
      setSources(loaded);
      setSourceError('');
      hydrate(() => restored);
    })().catch(error => { if (!cancelled) setSourceError(String(error)); });
    return () => { cancelled = true; };
  }, [project.items, sources]);

  useEffect(() => {
    if (!hostRef.current) return;
    const scene = new ImageBrickScene(hostRef.current, tr('组建模型三维工作区', 'Composition 3D workspace'));
    sceneRef.current = scene;
    scene.setAutoRotate(false);
    window.__composer = () => ({
      ...scene.snapshot(),
      items: project.items.length,
      selectedItem: selectedId,
      mode,
    });
    return () => {
      scene.dispose();
      sceneRef.current = null;
      delete window.__composer;
    };
  }, []);

  useEffect(() => {
    const scene = sceneRef.current;
    if (!scene || !sourcesReady) return;
    scene.setSources(sources);
    scene.setBuild(build, fitNextBuild.current);
    fitNextBuild.current = false;
    scene.setBuildStep(mode === 'build' ? step : build.steps.length, false);
    scene.setExplosion(mode === 'explode' ? explosion : 0);
  }, [build, sourcesReady]);
  useEffect(() => {
    const scene = sceneRef.current;
    if (!scene) return;
    scene.setLabel(tr('组建模型三维工作区', 'Composition 3D workspace'));
    window.__composer = () => ({
      ...scene.snapshot(),
      items: project.items.length,
      selectedItem: selectedId,
      mode,
    });
  }, [project.items.length, selectedId, mode, tr]);
  useEffect(() => {
    if (selectedId && !project.items.some(item => item.id === selectedId)) setSelectedId(null);
    setStep(value => Math.min(value, project.items.length + 1));
  }, [project.items, selectedId]);
  useEffect(() => {
    const keydown = (event: KeyboardEvent) => {
      if ((event.target as HTMLElement)?.closest('input, textarea, select, dialog')) return;
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'z') {
        event.preventDefault(); setPlaying(false); event.shiftKey ? redo() : undo();
      }
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'y') {
        event.preventDefault(); setPlaying(false); redo();
      }
    };
    window.addEventListener('keydown', keydown);
    return () => window.removeEventListener('keydown', keydown);
  }, [undo, redo]);
  useEffect(() => { sceneRef.current?.setView(view); }, [view]);
  useEffect(() => { sceneRef.current?.setAutoRotate(autoRotate); }, [autoRotate]);
  useEffect(() => { sceneRef.current?.setPanMode(panMode); }, [panMode]);
  useEffect(() => {
    if (mode === 'build') {
      sceneRef.current?.setExplosion(0);
      sceneRef.current?.setBuildStep(step);
      if (followStep && step > 0) requestAnimationFrame(() => sceneRef.current?.focusStep(step));
    } else {
      sceneRef.current?.setBuildStep(build.steps.length, false);
      sceneRef.current?.setExplosion(mode === 'explode' ? explosion : 0);
    }
  }, [mode, step, explosion, followStep, build.steps.length]);
  useEffect(() => {
    if (!playing || mode !== 'build') return;
    if (step >= build.steps.length) {
      setPlaying(false);
      return;
    }
    const timer = window.setTimeout(() => setStep(value => value + 1), 950);
    return () => window.clearTimeout(timer);
  }, [playing, mode, step, build.steps.length]);
  useEffect(() => {
    if (!notice) return;
    const timer = window.setTimeout(() => setNotice(''), 2400);
    return () => window.clearTimeout(timer);
  }, [notice]);

  async function addAsset(asset: ComposerAsset) {
    if (loadingRef.current || !sourcesReady) return;
    loadingRef.current = true;
    setLoadingAsset(asset.id);
    try {
      let bricks = asset.bricks ?? [];
      let sourceUrl: string | undefined;
      if (asset.modelId) {
        const source = await loadSourceGeometry(asset.modelId);
        const manifest = source.manifest;
        setSources(current => new Map(current).set(asset.modelId!, source));
        bricks = sourceBricksFromManifest(manifest);
        sourceUrl = manifest.model.sourceUrl;
      }
      const item = createComposerItem(projectRef.current, asset, bricks, sourceUrl);
      if (!item) {
        setNotice(tr('底板空间不足，或达到 5,000 块 / 200 组件上限', 'No baseplate space, or the 5,000-brick / 200-component limit was reached'));
        return;
      }
      setProject(current => ({ ...current, items: [...current.items, item], updatedAt: Date.now() }));
      fitNextBuild.current = true;
      setSelectedId(item.id);
      setMode('edit');
      setNotice(tr(`已加入 ${asset.nameZh}`, `${asset.nameEn} added`));
    } catch (error) {
      setNotice(`${tr('组件加载失败', 'Component failed to load')}: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      setLoadingAsset(null);
      loadingRef.current = false;
    }
  }

  function updateSelected(update: Partial<ComposerItem>) {
    if (!selected) return;
    const candidate = { ...selected, ...update };
    if (!canPlaceItem(project, candidate, selected.id)) {
      setNotice(tr('该位置越过底板或与已有组件冲突', 'That position is outside the base or collides with another component'));
      return;
    }
    setProject(current => ({
      ...current,
      items: current.items.map(item => item.id === selected.id ? candidate : item),
      updatedAt: Date.now(),
    }));
  }

  function duplicateSelected() {
    if (!selected) return;
    const asset: ComposerAsset = {
      id: selected.assetId,
      nameZh: selected.nameZh,
      nameEn: selected.nameEn,
      categoryZh: '',
      categoryEn: '',
      kind: selected.kind,
      modelId: selected.sourceModelId,
      footprint: selected.footprint,
      bricks: selected.bricks,
    };
    const item = createComposerItem(project, asset, selected.bricks, selected.sourceUrl);
    if (!item) {
      setNotice(tr('底板没有可用于副本的空间', 'No space is available for a copy'));
      return;
    }
    setProject(current => ({ ...current, items: [...current.items, item], updatedAt: Date.now() }));
    fitNextBuild.current = true;
    setSelectedId(item.id);
  }

  function removeSelected() {
    if (!selected) return;
    setProject(current => ({
      ...current,
      items: current.items.filter(item => item.id !== selected.id),
      updatedAt: Date.now(),
    }));
    fitNextBuild.current = true;
    setSelectedId(project.items.find(item => item.id !== selected.id)?.id ?? null);
  }

  function switchMode(next: ComposerMode) {
    setMode(next);
    setPlaying(false);
    if (next === 'build') setStep(Math.min(step, build.steps.length));
    if (next === 'explode') setExplosion(value => value || 0.72);
  }

  function saveProject() {
    const saved = autosave.save();
    if (saved) setNotice(tr('项目已保存在当前浏览器', 'Project saved in this browser'));
  }
  async function importProject(file?: File) {
    if (!file) return;
    try {
      if (file.size > 4_000_000) throw new Error('size');
      setPendingImport(readCompositionProject(await file.text()));
    } catch { setNotice(tr('项目无效：请检查格式、碰撞、边界和零件预算', 'Invalid project: check format, collisions, boundaries and brick budget')); }
  }
  function restoreProject(next: CompositionProject) {
    setPlaying(false); setMode('edit'); setSourceError(''); fitNextBuild.current = true;
    setProject(next); setSelectedId(next.items[0]?.id ?? null);
  }

  const currentLabel = step === 1
    ? tr('铺设底板', 'Place baseplate')
    : project.items[step - 2]
      ? locale === 'zh' ? project.items[step - 2].nameZh : project.items[step - 2].nameEn
      : '';

  return <section className="compose-studio" aria-label={tr('组建工作台', 'Compose workspace')}>
    <aside className="compose-library">
      <header>
        <span className="eyebrow">COMPONENT LIBRARY</span>
        <h1>{tr('组件库', 'Component library')}</h1>
      </header>
      <div className="compose-library-tabs" role="tablist">
        {([
          ['models', tr('模型', 'Models')],
          ['scenes', tr('场景', 'Scenes')],
          ['parts', tr('零件', 'Parts')],
        ] as [LibraryTab, string][]).map(([id, label]) =>
          <button key={id} role="tab" aria-selected={libraryTab === id} onClick={() => setLibraryTab(id)}>{label}</button>,
        )}
      </div>
      <label className="diy-search"><Search size={16} /><input aria-label={tr('搜索组件', 'Search components')} value={query} onChange={event => setQuery(event.target.value)} placeholder={tr('名称 / 编号', 'Name / ID')} /></label>
      {libraryTab === 'scenes' && <div className="baseplate-library">
        {baseplateCatalog.map(item => <button
          key={item.id}
          className={project.baseplateId === item.id ? 'active' : ''}
          onClick={() => {
            const next = changeBaseplate(project, item.id);
            if (!next) {
              setNotice(tr('底板无法容纳当前场景，已保留所有组件与原底板', 'This base cannot contain the scene. All components and the original base are preserved.'));
              return;
            }
            fitNextBuild.current = true;
            setProject(next);
          }}
        >
          <i style={{ background: item.colorHex }} />
          <span><strong>{locale === 'zh' ? item.nameZh : item.nameEn}</strong><small>{item.width} × {item.depth} studs</small></span>
          {project.baseplateId === item.id && <Check size={15} />}
        </button>)}
      </div>}
      <div className="component-grid">
        {visibleAssets.map(asset => <article key={asset.id} className="component-card">
          <div className="component-art">
            {asset.preview
              ? <img src={`${import.meta.env.BASE_URL}${asset.preview}`} alt={locale === 'zh' ? asset.nameZh : asset.nameEn} />
              : <Boxes size={34} />}
          </div>
          <div><small>{locale === 'zh' ? asset.categoryZh : asset.categoryEn}</small><strong>{locale === 'zh' ? asset.nameZh : asset.nameEn}</strong><span>{asset.footprint[0]} × {asset.footprint[1]} studs</span></div>
          <button data-brick-effect="shatter" disabled={!!loadingAsset || !sourcesReady} onClick={() => addAsset(asset)} aria-label={tr(`添加${asset.nameZh}`, `Add ${asset.nameEn}`)}>
            {loadingAsset === asset.id ? '...' : <Plus size={15} />}
          </button>
        </article>)}
      </div>
    </aside>

    <main className="compose-stage">
      <header className="compose-stage-heading">
        <div><span className="eyebrow">DIY MODEL COMPOSER</span><input maxLength={100} aria-label={tr('项目名称', 'Project name')} value={project.name} onChange={event => setProject(current => ({ ...current, name: event.target.value, updatedAt: Date.now() }))} /></div>
        <div className="compose-mode-tabs" role="tablist">
          <button role="tab" aria-selected={mode === 'edit'} onClick={() => switchMode('edit')}><Grid2X2 size={15} />{tr('编辑', 'Edit')}</button>
          <button role="tab" aria-selected={mode === 'build'} onClick={() => switchMode('build')}><BookOpen size={15} />{tr('拼装', 'Build')}</button>
          <button role="tab" aria-selected={mode === 'explode'} onClick={() => switchMode('explode')}><Expand size={15} />{tr('展开', 'Explode')}</button>
        </div>
      </header>
      <div className="compose-canvas" ref={hostRef} />
      {(!sourcesReady || sourceError) && <div className="compose-notice" role="status">{sourceError || tr('正在校验并载入真实模型几何…', 'Validating and loading model geometry...')}</div>}
      <div className="image-viewport-toolbar compose-toolbar">
        {(['perspective', 'front', 'side', 'top'] as ImageBrickView[]).map(item =>
          <IconButton key={item} label={{
            perspective: tr('透视图', 'Perspective'),
            front: tr('正视图', 'Front'),
            side: tr('侧视图', 'Side'),
            top: tr('俯视图', 'Top'),
          }[item]} active={view === item} onClick={() => setView(item)}>
            {item === 'perspective' ? <Box size={16} /> : item === 'top' ? <Grid2X2 size={16} /> : <Layers3 size={16} />}
          </IconButton>,
        )}
        <IconButton label={tr('自动旋转', 'Auto rotate')} active={autoRotate} onClick={() => setAutoRotate(value => !value)}><Rotate3D size={16} /></IconButton>
        <IconButton label={tr('平移视图', 'Pan view')} active={panMode} onClick={() => setPanMode(value => !value)}><Hand size={16} /></IconButton>
        <IconButton label={tr('适应画面', 'Fit view')} onClick={() => sceneRef.current?.fitVisible()}><Crosshair size={16} /></IconButton>
      </div>
      <div className="image-zoom-tools">
        <IconButton label={tr('放大', 'Zoom in')} onClick={() => sceneRef.current?.zoom(0.82)}><Plus size={16} /></IconButton>
        <IconButton label={tr('缩小', 'Zoom out')} onClick={() => sceneRef.current?.zoom(1.22)}><Minus size={16} /></IconButton>
      </div>
      {mode === 'build' && <section className="image-build-dock compose-build-dock" aria-label={tr('组建拼装控制', 'Composition build controls')}>
        <div className="dock-heading"><div><BookOpen size={17} /><strong>{currentLabel}</strong></div><output>{step}<span> / {build.steps.length}</span></output></div>
        <div className="step-controls">
          <IconButton label={tr('回到开始', 'Restart')} onClick={() => setStep(0)}><SkipBack size={17} /></IconButton>
          <IconButton label={tr('上一步', 'Previous')} disabled={step <= 0} onClick={() => setStep(value => Math.max(0, value - 1))}><ArrowLeft size={17} /></IconButton>
          <IconButton label={playing ? tr('暂停', 'Pause') : tr('播放', 'Play')} active={playing} onClick={() => setPlaying(value => !value)}>{playing ? <Pause size={17} /> : <Play size={17} />}</IconButton>
          <input type="range" min={0} max={build.steps.length} value={step} aria-label={tr('当前组建步骤', 'Current composition step')} onChange={event => setStep(Number(event.target.value))} />
          <IconButton label={tr('下一步', 'Next')} disabled={step >= build.steps.length} onClick={() => setStep(value => Math.min(build.steps.length, value + 1))}><ArrowRight size={17} /></IconButton>
          <IconButton label={tr('完成', 'Complete')} onClick={() => setStep(build.steps.length)}><SkipForward size={17} /></IconButton>
          <IconButton label={tr('步骤镜头跟随', 'Step camera follow')} active={followStep} onClick={() => setFollowStep(value => !value)}><Crosshair size={17} /></IconButton>
        </div>
      </section>}
      {mode === 'explode' && <section className="compose-explode-dock">
        <Expand size={17} /><span>{tr('展开程度', 'Explosion')}</span>
        <input type="range" min={0} max={100} value={Math.round(explosion * 100)} aria-label={tr('组建展开程度', 'Composition explosion')} onChange={event => setExplosion(Number(event.target.value) / 100)} />
        <output>{Math.round(explosion * 100)}%</output>
      </section>}
      {notice && <div className="compose-notice" role="status">{notice}</div>}
    </main>

    <aside className="compose-inspector">
      <header><div><span className="eyebrow">MODEL TREE</span><h2>{tr('场景结构', 'Scene structure')}</h2></div><strong>{project.items.length}</strong></header>
      <button className={`compose-tree-base ${!selected ? 'active' : ''}`} onClick={() => setSelectedId(null)}>
        <i style={{ background: base.colorHex }} /><span><strong>{locale === 'zh' ? base.nameZh : base.nameEn}</strong><small>{base.width} × {base.depth} studs</small></span>
      </button>
      <div className="compose-tree">
        {project.items.map((item, index) => <button key={item.id} className={selectedId === item.id ? 'active' : ''} onClick={() => setSelectedId(item.id)}>
          <span>{String(index + 1).padStart(2, '0')}</span>
          <div><strong>{locale === 'zh' ? item.nameZh : item.nameEn}</strong><small>{item.bricks.length} {tr('块积木', 'bricks')} · X {item.x} · Z {item.z}</small></div>
        </button>)}
        {!project.items.length && <div className="compose-empty"><Boxes size={28} /><span>{tr('从左侧加入第一个组件', 'Add your first component from the library')}</span></div>}
      </div>
      {selected && <section className="compose-properties">
        <h3>{tr('对齐与安装', 'Align and mount')}</h3>
        <div className="nudge-grid">
          <span />
          <IconButton label={tr('向后移动', 'Move backward')} onClick={() => updateSelected({ z: selected.z - 1 })}><ArrowUp size={16} /></IconButton>
          <span />
          <IconButton label={tr('向左移动', 'Move left')} onClick={() => updateSelected({ x: selected.x - 1 })}><ArrowLeft size={16} /></IconButton>
          <button className="rotation-button" onClick={() => updateSelected({ rotation: ((selected.rotation + 1) % 4) as QuarterTurn })} aria-label={tr('旋转 90 度', 'Rotate 90 degrees')}><RotateCw size={17} /><span>{selected.rotation * 90}°</span></button>
          <IconButton label={tr('向右移动', 'Move right')} onClick={() => updateSelected({ x: selected.x + 1 })}><ArrowRight size={16} /></IconButton>
          <span />
          <IconButton label={tr('向前移动', 'Move forward')} onClick={() => updateSelected({ z: selected.z + 1 })}><ArrowDown size={16} /></IconButton>
          <span />
        </div>
        <div className="coordinate-grid">
          <label>X <input type="number" step={1} value={selected.x} onChange={event => updateSelected({ x: Math.round(Number(event.target.value)) })} /></label>
          <label>Z <input type="number" step={1} value={selected.z} onChange={event => updateSelected({ z: Math.round(Number(event.target.value)) })} /></label>
          <label>{tr('高度（薄板层）', 'Height (plates)')} <input type="number" min={0} max={60} step={1} value={selected.level ?? 0} onChange={event => updateSelected({ level: Math.max(0, Math.min(60, Math.round(Number(event.target.value)))) })} /></label>
        </div>
        {selected.kind === 'part' && <div className="compose-color-picker" role="group" aria-label={tr('零件颜色', 'Part color')}>
          <span>{tr('颜色', 'Color')}</span>
          <div>{brickPalette.slice(0, 14).map(color => <button
            key={color.id}
            title={locale === 'zh' ? color.nameZh : color.nameEn}
            aria-label={locale === 'zh' ? color.nameZh : color.nameEn}
            style={{ background: color.hex }}
            className={selected.bricks[0]?.colorCode === color.code ? 'active' : ''}
            onClick={() => updateSelected({
              bricks: selected.bricks.map(item => ({
                ...item,
                colorCode: color.code,
                colorHex: color.hex,
              })),
            })}
          />)}</div>
        </div>}
        <div className="compose-property-actions">
          <button onClick={duplicateSelected}><Copy size={15} />{tr('复制', 'Duplicate')}</button>
          <button onClick={removeSelected}><Trash2 size={15} />{tr('删除', 'Delete')}</button>
        </div>
        {selected.sourceUrl && <a href={selected.sourceUrl} target="_blank" rel="noreferrer">{tr('查看组件模型来源', 'View component source')}</a>}
      </section>}
      <footer className="compose-export">
        <div className="compose-history-tools">
          <IconButton label={tr('撤销', 'Undo')} disabled={!canUndo} onClick={() => { setPlaying(false); undo(); }}><Undo2 size={17} /></IconButton>
          <IconButton label={tr('重做', 'Redo')} disabled={!canRedo} onClick={() => { setPlaying(false); redo(); }}><Redo2 size={17} /></IconButton>
          <IconButton label={tr('导入组建项目', 'Import composition')} onClick={() => fileInput.current?.click()}><Upload size={17} /></IconButton>
          <input type="file" hidden ref={fileInput} accept=".json" aria-label={tr('导入组建 JSON', 'Import composition JSON')} onChange={event => { void importProject(event.target.files?.[0]); event.target.value = ''; }} />
          <ProjectShelf space="compose" name={project.name} serialize={() => JSON.stringify(projectRef.current)} restore={text => restoreProject(readCompositionProject(text))} tr={tr} />
        </div>
        {autosave.state === 'invalid' && <p role="alert">{tr('本地项目损坏，原始存档尚未覆盖。', 'Local project is invalid. Its original data has not been overwritten.')}</p>}
        {autosave.state === 'error' && <p role="alert">{tr('浏览器存储不可用，请导出 JSON 保留项目。', 'Browser storage unavailable. Export JSON to keep your project.')}</p>}
        <dl>
          <div><dt>{tr('总积木', 'Bricks')}</dt><dd>{build.bricks.length}</dd></div>
          <div><dt>{tr('步骤', 'Steps')}</dt><dd>{build.steps.length}</dd></div>
          <div><dt>{tr('型号', 'Parts')}</dt><dd>{build.bom.length}</dd></div>
        </dl>
        <div>
          <button onClick={saveProject}><Save size={15} />{tr('保存', 'Save')}</button>
          <button onClick={() => download(JSON.stringify(project, null, 2), `${project.name}.brick-atlas.json`, 'application/json')}><Download size={15} />JSON</button>
          <button disabled={!sourcesReady} onClick={() => download(imageBrickBuildToLdraw({ ...build, name: project.name }), `${project.name}.ldr`, 'text/plain')}><Download size={15} />LDraw</button>
          <button disabled={!sourcesReady} onClick={() => download(['partId,colorCode,quantity', ...build.bom.map(item => `${item.partId},${item.colorCode},${item.quantity}`)].join('\n'), `${project.name}-bom.csv`, 'text/csv')}><Download size={15} />BOM</button>
        </div>
      </footer>
    </aside>
    {pendingImport && <Modal title={tr('打开组建项目？', 'Open composition?')} onClose={() => setPendingImport(null)}>
      <div className="diy-confirm"><p>{pendingImport.name} · {tr('替换当前场景，可撤销。', 'Replace the current scene. This can be undone.')}</p>
        <button className="primary-button" onClick={() => { restoreProject(pendingImport); setPendingImport(null); }}>{tr('打开项目', 'Open project')}</button></div>
    </Modal>}
  </section>;
}
