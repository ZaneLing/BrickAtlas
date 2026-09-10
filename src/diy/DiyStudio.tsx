import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowDown, ArrowLeft, ArrowRight, ArrowUp, Box, Check, ChevronDown, Download, Eraser,
  Focus, Grid2X2, Hand, Home, Languages, Layers3, Minus, MousePointer2, Paintbrush,
  Plus, Redo2, RotateCw, Save, Search, Trash2, Undo2, Upload,
} from 'lucide-react';
import type { Locale, Translator } from '../app/locale';
import { readLocal, writeLocal } from '../app/storage';
import { brickPalette } from '../creator/imageBrickModel';
import { BrickAtlasMark } from '../ui/BrickAtlasMark';
import { IconButton, Modal } from '../ui/Controls';
import { DiyScene, type DiyHover } from './DiyScene';
import { renderDiyThumbnails } from './diyGeometry';
import {
  canRemove, commitDiy, diyBom, DiyIndex, diyParts, diyRecipes, diyToLdraw, emptyDiyProject,
  diyCategories, parseDiyProject, partById, recipeById, redoDiy, stampSize, undoDiy,
  type DiyBrick, type DiyBrush, type DiyCategory, type DiyHistory, type DiyProject, type DiyTool, type Turn,
} from './diyModel';
import './diy.css';

const storageKey = 'brick-atlas-diy-v1';
declare global { interface Window { __diy?: () => ReturnType<DiyScene['snapshot']> } }

function download(data: Blob, name: string) {
  const url = URL.createObjectURL(data);
  const link = document.createElement('a');
  link.href = url; link.download = name; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function loadProject() {
  try {
    const text = readLocal(storageKey);
    return { project: text ? parseDiyProject(text) : emptyDiyProject(), invalid: false };
  } catch { return { project: emptyDiyProject(), invalid: true }; }
}

export function DiyStudio({ locale, tr, toggleLocale }: { locale: Locale; tr: Translator; toggleLocale: () => void }) {
  const [loaded] = useState(loadProject);
  const [history, setHistory] = useState<DiyHistory>({ past: [], present: loaded.project, future: [] });
  const historyRef = useRef(history);
  const [brush, setBrush] = useState<DiyBrush>({ recipeId: '3001', color: 'red', turn: 0 });
  const [tool, setTool] = useState<DiyTool>('place');
  const [hover, setHover] = useState<DiyHover | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [autoHeight, setAutoHeight] = useState(true);
  const [layer, setLayer] = useState(0);
  const [tab, setTab] = useState<'parts' | 'components'>('parts');
  const [category, setCategory] = useState<'all' | DiyCategory>('basic');
  const [query, setQuery] = useState('');
  const [topView, setTopView] = useState(false);
  const [notice, setNotice] = useState('');
  const [storageState, setStorageState] = useState<'saved' | 'saving' | 'error' | 'invalid'>(loaded.invalid ? 'invalid' : 'saved');
  const [sceneError, setSceneError] = useState('');
  const [pendingImport, setPendingImport] = useState<DiyProject | null>(null);
  const [clearOpen, setClearOpen] = useState(false);
  const [sceneRevision, setSceneRevision] = useState(0);
  const host = useRef<HTMLDivElement>(null);
  const library = useRef<HTMLDivElement>(null);
  const scene = useRef<DiyScene | null>(null);
  const fileInput = useRef<HTMLInputElement>(null);
  const current = useRef({ brush, tr });
  current.current = { brush, tr };
  const project = history.present;
  const selected = project.bricks.find(brick => brick.id === selectedId);
  const color = brickPalette.find(color => color.id === brush.color)!;
  const recipe = recipeById.get(brush.recipeId)!;
  const size = stampSize(brush);
  const entries = useMemo(() => diyRecipes.filter(recipe => {
    const single = recipe.parts.length === 1;
    const part = single ? partById.get(recipe.parts[0].partId) : null;
    const categoryMatch = tab === 'components' || category === 'all' || part?.category === category;
    const text = `${recipe.nameZh} ${recipe.nameEn} ${recipe.id} ${part?.tags?.join(' ') ?? ''}`.toLowerCase();
    return (tab === 'parts' ? single : !single) && categoryMatch && text.includes(query.trim().toLowerCase());
  }), [tab, category, query]);

  const applyHistory = useCallback((next: DiyHistory) => {
    historyRef.current = next;
    setHistory(next);
    setStorageState('saving');
  }, []);
  const commit = useCallback((next: DiyProject) => applyHistory(commitDiy(historyRef.current, next)), [applyHistory]);
  const place = useCallback((bricks: DiyBrick[]) => {
    const project = historyRef.current.present;
    if (new DiyIndex(project.bricks).validate(bricks, project.bricks.length)) return;
    commit({ ...project, bricks: [...project.bricks, ...bricks] });
    setSelectedId(bricks.at(-1)!.id);
  }, [commit]);
  const edit = useCallback((id: string, action: 'erase' | 'paint') => {
    const project = historyRef.current.present;
    if (!project.bricks.some(brick => brick.id === id)) return;
    if (action === 'erase') {
      if (!canRemove(project.bricks, id)) {
        setNotice(current.current.tr('该积木正在支撑上方结构', 'This brick supports the structure above'));
        return;
      }
      commit({ ...project, bricks: project.bricks.filter(brick => brick.id !== id) });
      setSelectedId(null);
    } else {
      const color = current.current.brush.color;
      if (project.bricks.find(brick => brick.id === id)?.color === color) return;
      commit({ ...project, bricks: project.bricks.map(brick => brick.id === id ? { ...brick, color } : brick) });
      setSelectedId(id);
    }
  }, [commit]);

  useEffect(() => {
    if (!host.current) return;
    let instance: DiyScene | null = null;
    try {
      instance = new DiyScene(host.current, { place, edit, select: setSelectedId, hover: setHover, error: setSceneError }, current.current.tr('自由 DIY 三维画布', 'Free DIY 3D canvas'));
      scene.current = instance;
      window.__diy = () => instance!.snapshot();
    } catch {
      setSceneError('WebGL unavailable');
    }
    return () => { instance?.dispose(); scene.current = null; delete window.__diy; };
  }, [place, edit, sceneRevision]);
  useEffect(() => { scene.current?.setBricks(project.bricks); }, [project.bricks, sceneRevision]);
  useEffect(() => { scene.current?.setBrush(brush); }, [brush, sceneRevision]);
  useEffect(() => { scene.current?.setTool(tool); }, [tool, sceneRevision]);
  useEffect(() => { scene.current?.setLayer(autoHeight ? null : layer); }, [autoHeight, layer, sceneRevision]);
  useEffect(() => { scene.current?.select(selectedId); }, [selectedId, project.bricks, sceneRevision]);
  useEffect(() => { scene.current?.setLabel(tr('自由 DIY 三维画布', 'Free DIY 3D canvas')); }, [tr]);
  useEffect(() => {
    // Preserve malformed stored input until an explicit edit/save replaces it.
    if (storageState === 'invalid') return;
    const timer = setTimeout(() => setStorageState(writeLocal(storageKey, JSON.stringify(project)) ? 'saved' : 'error'), 450);
    return () => clearTimeout(timer);
  }, [project, storageState === 'invalid']);
  useEffect(() => {
    const timer = setTimeout(() => {
      try {
        renderDiyThumbnails(entries.flatMap(recipe => {
          const canvas = library.current?.querySelector<HTMLCanvasElement>(`canvas[data-recipe="${recipe.id}"]`);
          return canvas ? [{ recipe, canvas }] : [];
        }), color.id);
      } catch { /* The main canvas displays the actionable WebGL error. */ }
    }, 70);
    return () => clearTimeout(timer);
  }, [entries, color.hex, sceneRevision]);
  useEffect(() => {
    if (!notice) return;
    const timer = setTimeout(() => setNotice(''), 2800);
    return () => clearTimeout(timer);
  }, [notice]);
  const undo = useCallback(() => { applyHistory(undoDiy(historyRef.current)); setSelectedId(null); }, [applyHistory]);
  const redo = useCallback(() => { applyHistory(redoDiy(historyRef.current)); setSelectedId(null); }, [applyHistory]);
  const rotate = useCallback(() => setBrush(brush => ({ ...brush, turn: ((brush.turn + 1) % 4) as Turn })), []);
  useEffect(() => {
    const keydown = (event: KeyboardEvent) => {
      if ((event.target as HTMLElement)?.closest('input, textarea, select, dialog')) return;
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'z') {
        event.preventDefault(); event.shiftKey ? redo() : undo();
      } else if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'y') { event.preventDefault(); redo(); }
      else if (event.key.toLowerCase() === 'r') { event.preventDefault(); rotate(); }
      else if (event.key === 'Escape') { setTool('orbit'); setSelectedId(null); }
      else if (event.key === 'Delete' || event.key === 'Backspace') { if (selectedId) { event.preventDefault(); edit(selectedId, 'erase'); } }
      else if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) {
        event.preventDefault();
        scene.current?.pan(event.key === 'ArrowLeft' ? -8 : event.key === 'ArrowRight' ? 8 : 0, event.key === 'ArrowUp' ? -8 : event.key === 'ArrowDown' ? 8 : 0);
      }
    };
    window.addEventListener('keydown', keydown);
    return () => window.removeEventListener('keydown', keydown);
  }, [undo, redo, rotate, edit, selectedId]);

  function save() { setStorageState(writeLocal(storageKey, JSON.stringify(project)) ? 'saved' : 'error'); }
  async function importProject(file?: File) {
    if (!file) return;
    try {
      if (file.size > 4_000_000) throw new Error('oversize');
      const next = parseDiyProject(await file.text());
      if (project.bricks.length) setPendingImport(next);
      else { commit(next); setSelectedId(null); requestAnimationFrame(() => scene.current?.fit()); }
    } catch { setNotice(tr('无法读取：请选择有效的 DIY 项目 JSON', 'Cannot read this file. Choose a valid DIY project JSON')); }
  }
  function exportFile(format: 'json' | 'csv' | 'ldr' | 'png') {
    if (format === 'png') {
      scene.current?.capture().then(blob => download(blob, `${project.name}.png`)).catch(() => setNotice(tr('截图失败', 'Capture failed')));
      return;
    }
    const csv = ['partId,colorCode,color,quantity', ...diyBom(project).map(item =>
      `${item.partId},${brickPalette.find(color => color.id === item.color)!.code},${item.color},${item.count}`,
    )].join('\n');
    download(new Blob([format === 'json' ? JSON.stringify(project, null, 2) : format === 'ldr' ? diyToLdraw(project) : csv], { type: format === 'json' ? 'application/json' : 'text/plain;charset=utf-8' }), `${project.name}.${format}`);
  }
  const tools = [
    { id: 'place', icon: Plus, label: tr('放置积木', 'Place bricks') },
    { id: 'paint', icon: Paintbrush, label: tr('涂色', 'Paint') },
    { id: 'erase', icon: Eraser, label: tr('移除积木', 'Erase bricks') },
    { id: 'orbit', icon: MousePointer2, label: tr('选择与旋转视图', 'Select and orbit') },
    { id: 'pan', icon: Hand, label: tr('平移视图', 'Pan view') },
  ] as const;
  const issueLabel = hover?.issue === 'overlap' ? tr('位置已占用', 'Space occupied')
    : hover?.issue === 'unsupported' ? tr('下方没有连接点', 'No connection below')
      : hover?.issue === 'limit' ? tr('达到编辑容量上限', 'Editing capacity reached')
        : tr('可放置', 'Ready to place');

  return <div className="diy-page">
    <header className="topbar diy-topbar">
      <a className="brand" href={import.meta.env.BASE_URL} aria-label={tr('返回首页', 'Home')}><span className="brand-mark"><BrickAtlasMark /></span><strong>BRICK<span>ATLAS</span></strong></a>
      <div className="top-divider" />
      <h1>{tr('自由 DIY', 'Free DIY')}</h1>
      <input className="diy-project-name" aria-label={tr('DIY 项目名称', 'DIY project name')} maxLength={100} value={project.name}
        onChange={event => { const next = { ...historyRef.current, present: { ...historyRef.current.present, name: event.target.value } }; applyHistory(next); }} />
      <div className="diy-file-tools">
        <IconButton label={tr('撤销', 'Undo')} disabled={!history.past.length} onClick={undo}><Undo2 size={18} /></IconButton>
        <IconButton label={tr('重做', 'Redo')} disabled={!history.future.length} onClick={redo}><Redo2 size={18} /></IconButton>
        <span className="diy-tool-divider" />
        <IconButton label={tr('保存 DIY', 'Save DIY')} onClick={save}><Save size={18} /></IconButton>
        <IconButton label={tr('打开 DIY 项目', 'Open DIY project')} onClick={() => fileInput.current?.click()}><Upload size={18} /></IconButton>
        <input hidden ref={fileInput} type="file" accept=".json,application/json" aria-label={tr('导入 DIY JSON', 'Import DIY JSON')} onChange={event => { void importProject(event.target.files?.[0]); event.target.value = ''; }} />
        <details className="diy-download">
          <summary aria-label={tr('导出 DIY', 'Export DIY')} title={tr('导出 DIY', 'Export DIY')}><Download size={18} /><ChevronDown size={12} /></summary>
          <div>{(['json', 'ldr', 'csv', 'png'] as const).map(format => <button key={format} onClick={event => {
            exportFile(format);
            event.currentTarget.closest('details')?.removeAttribute('open');
          }}>{format === 'ldr' ? 'LDraw' : format === 'csv' ? 'BOM CSV' : format.toUpperCase()}</button>)}</div>
        </details>
        <button className="language-button" title={tr('切换为英文', 'Switch to Chinese')} onClick={toggleLocale}><Languages size={14} />{locale === 'zh' ? 'EN' : '中'}</button>
        <a className="icon-button" title={tr('组件组建', 'Compose')} aria-label={tr('组件组建', 'Compose')} href={`${import.meta.env.BASE_URL}compose`}><Layers3 size={18} /></a>
      </div>
    </header>
    <div className="diy-workspace">
      <main className="diy-stage">
        <div className="diy-canvas" ref={host} />
        <div className="diy-floating-tools" role="toolbar" aria-label={tr('DIY 编辑工具', 'DIY editing tools')}>
          {tools.map(({ id, label, icon: Icon }) => <IconButton key={id} label={label} active={tool === id} onClick={() => setTool(id)}><Icon size={19} /></IconButton>)}
          <span className="diy-tool-divider" />
          <IconButton label={tr('旋转待放积木 90°', 'Rotate preview 90°')} disabled={tool !== 'place'} onClick={rotate}><RotateCw size={19} /></IconButton>
        </div>
        <div className="diy-view-tools">
          <IconButton label={tr('透视视图', 'Perspective view')} active={!topView} onClick={() => { setTopView(false); scene.current?.setView(false); }}><Box size={17} /></IconButton>
          <IconButton label={tr('俯视视图', 'Top view')} active={topView} onClick={() => { setTopView(true); scene.current?.setView(true); }}><Grid2X2 size={17} /></IconButton>
          <IconButton label={tr('适配全部积木', 'Fit all bricks')} onClick={() => { setTopView(false); scene.current?.fit(); }}><Focus size={17} /></IconButton>
        </div>
        <div className="diy-view-navigation">
          <IconButton label={tr('向北平移', 'Pan north')} onClick={() => scene.current?.pan(0, -16)}><ArrowUp size={16} /></IconButton>
          <div>
            <IconButton label={tr('向西平移', 'Pan west')} onClick={() => scene.current?.pan(-16, 0)}><ArrowLeft size={16} /></IconButton>
            <IconButton label={tr('返回原点', 'Return to origin')} onClick={() => {
              const target = scene.current?.snapshot().target;
              if (target) scene.current?.pan(-target[0], -target[2]);
            }}><Home size={16} /></IconButton>
            <IconButton label={tr('向东平移', 'Pan east')} onClick={() => scene.current?.pan(16, 0)}><ArrowRight size={16} /></IconButton>
          </div>
          <IconButton label={tr('向南平移', 'Pan south')} onClick={() => scene.current?.pan(0, 16)}><ArrowDown size={16} /></IconButton>
          <div className="diy-zoom">
            <IconButton label={tr('放大 DIY', 'Zoom in DIY')} onClick={() => scene.current?.zoom(0.8)}><Plus size={17} /></IconButton>
            <IconButton label={tr('缩小 DIY', 'Zoom out DIY')} onClick={() => scene.current?.zoom(1.25)}><Minus size={17} /></IconButton>
          </div>
        </div>
        <div className="diy-selection-strip">
          <span className="diy-live-dot" />
          <strong>{tools.find(item => item.id === tool)!.label}</strong>
          {tool === 'place' && <><i style={{ background: color.hex }} /><span>{locale === 'zh' ? recipe.nameZh : recipe.nameEn}</span><small>{brush.turn * 90}°</small></>}
        </div>
        {notice && <div className="diy-toast" role="status">{notice}</div>}
        {sceneError && <div className="diy-error" role="alert"><strong>{tr('3D 视图暂不可用', '3D view unavailable')}</strong><span>{sceneError}</span><button onClick={() => { setSceneError(''); setSceneRevision(value => value + 1); }}>{tr('重试', 'Retry')}</button></div>}
        <footer className="diy-statusbar">
          <span>{project.bricks.length} {tr('块积木', 'bricks')} · {new Set(project.bricks.map(brick => brick.color)).size} {tr('种颜色', 'colors')}</span>
          <span className={hover?.issue ? 'invalid' : ''}>{hover && tool === 'place' ? `${issueLabel} · X ${hover.x}  Z ${hover.z}  Y ${hover.y}` : tr('无限底板', 'Infinite baseplate')}</span>
          <span>{storageState === 'saved' ? tr('已保存', 'Saved') : storageState === 'saving' ? tr('保存中…', 'Saving...') : tr('未保存', 'Not saved')}</span>
        </footer>
      </main>
      <aside className="diy-library" aria-label={tr('DIY 零件与组件库', 'DIY parts and components')}>
        <header><span className="eyebrow">BRICK LIBRARY</span><h2>{tr('下一块，随你拼', 'Your next brick')}</h2></header>
        <section className="diy-color-section">
          <div className="diy-section-label"><strong>{tr('颜色', 'Color')}</strong><span>{locale === 'zh' ? color.nameZh : color.nameEn}</span></div>
          <div className="diy-swatches" role="group" aria-label={tr('DIY 颜色', 'DIY colors')}>
            {brickPalette.map(item => <button key={item.id} aria-label={tr(`选择${item.nameZh}`, `Choose ${item.nameEn}`)} title={locale === 'zh' ? item.nameZh : item.nameEn} aria-pressed={brush.color === item.id}
              style={{ background: item.hex, color: ['white', 'yellow', 'tan', 'lime', 'pink', 'lavender'].includes(item.id) ? '#202a44' : '#ffffff' }}
              onClick={() => setBrush(brush => ({ ...brush, color: item.id }))}>{brush.color === item.id && <Check size={15} />}</button>)}
          </div>
        </section>
        <div className="diy-library-tabs" role="tablist" aria-label={tr('DIY 素材类型', 'DIY library type')}>
          <button role="tab" aria-selected={tab === 'parts'} onClick={() => setTab('parts')}><Box size={15} />{tr('零件', 'Parts')}<small>{diyParts.length}</small></button>
          <button role="tab" aria-selected={tab === 'components'} onClick={() => setTab('components')}><Layers3 size={15} />{tr('小组件', 'Assemblies')}<small>{diyRecipes.length - diyParts.length}</small></button>
        </div>
        <label className="diy-search"><Search size={16} /><input value={query} onChange={event => setQuery(event.target.value)} aria-label={tr('搜索 DIY 素材', 'Search DIY library')} placeholder={tr('名称 / Part ID', 'Name / Part ID')} /></label>
        {tab === 'parts' && <div className="diy-categories" role="group" aria-label={tr('DIY 零件分类', 'DIY part categories')}>
          <button aria-pressed={category === 'all'} onClick={() => setCategory('all')}>{tr('全部', 'All')}<small>{diyParts.length}</small></button>
          {diyCategories.map(item => <button key={item.id} aria-pressed={category === item.id} onClick={() => setCategory(item.id)}>
            {locale === 'zh' ? item.nameZh : item.nameEn}<small>{diyParts.filter(part => part.category === item.id).length}</small>
          </button>)}
        </div>}
        <div className="diy-parts-grid" ref={library}>
          {entries.map(item => <button key={item.id} className={`diy-part ${brush.recipeId === item.id ? 'active' : ''}`} aria-pressed={brush.recipeId === item.id}
            data-brick-effect="shatter"
            aria-label={tr(`选取${item.nameZh}`, `Pick ${item.nameEn}`)} onClick={() => { setBrush(brush => ({ ...brush, recipeId: item.id })); setTool('place'); }}>
            <canvas data-recipe={item.id} aria-hidden="true" />
            <strong>{locale === 'zh' ? item.nameZh : item.nameEn}</strong>
            <span>{item.parts.length === 1 ? item.id : `${item.parts.length} ${tr('块积木', 'bricks')}`}</span>
          </button>)}
          {!entries.length && <p className="diy-no-results">{tr('没有匹配的素材', 'No matching parts')}</p>}
        </div>
        <section className="diy-placement-settings">
          <div className="diy-section-label"><strong>{tr('待放积木', 'Placement')}</strong><span>{size.width} × {size.depth} studs · {brush.turn * 90}°</span></div>
          <div className="diy-height-row"><label><input type="checkbox" checked={autoHeight} onChange={event => setAutoHeight(event.target.checked)} />{tr('自动叠放', 'Auto stack')}</label>
            <label>{tr('层高', 'Layer')}<input aria-label={tr('DIY 放置层高', 'DIY placement layer')} type="number" min={0} max={3000} step={1} disabled={autoHeight} value={layer} onChange={event => {
              const n = Number(event.target.value);
              if (Number.isFinite(n)) setLayer(Math.max(0, Math.min(3000, Math.round(n))));
            }} /></label></div>
          {selected && <div className="diy-selected">
            <span>{tr('选中', 'Selected')} · {selected.partId} · X {selected.x} · Z {selected.z}</span>
            <div><IconButton label={tr('聚焦选中积木', 'Focus selected brick')} onClick={() => scene.current?.fit(true)}><Focus size={16} /></IconButton>
              <IconButton label={tr('拾取选中样式', 'Pick selected style')} onClick={() => { setBrush({ recipeId: selected.partId, color: selected.color, turn: selected.turn }); setTool('place'); }}><Paintbrush size={16} /></IconButton>
              <IconButton label={tr('删除选中积木', 'Delete selected brick')} onClick={() => edit(selected.id, 'erase')}><Trash2 size={16} /></IconButton></div>
          </div>}
          {(storageState === 'error' || storageState === 'invalid') && <p className="diy-save-error" role="alert">{storageState === 'error'
            ? tr('浏览器保存失败，请导出 JSON 备份。', 'Browser save failed. Export JSON as a backup.')
            : tr('本地项目损坏，原始存档尚未覆盖。', 'Local project is invalid. Its original data has not been overwritten.')}</p>}
          <button className="diy-clear" disabled={!project.bricks.length} onClick={() => setClearOpen(true)}><Trash2 size={14} />{tr('清空底板', 'Clear baseplate')}</button>
        </section>
      </aside>
    </div>
    {clearOpen && <Modal title={tr('清空当前 DIY？', 'Clear this DIY?')} onClose={() => setClearOpen(false)}>
      <div className="diy-confirm"><p>{tr(`移除 ${project.bricks.length} 块积木，此操作可以撤销。`, `Remove ${project.bricks.length} bricks. This action can be undone.`)}</p>
        <button className="primary-button" data-brick-effect="shatter" onClick={() => { commit({ ...project, bricks: [] }); setSelectedId(null); setClearOpen(false); }}>{tr('确认清空', 'Confirm clear')}</button></div>
    </Modal>}
    {pendingImport && <Modal title={tr('打开另一个 DIY 项目？', 'Open another DIY project?')} onClose={() => setPendingImport(null)}>
      <div className="diy-confirm"><p>{pendingImport.name} · {pendingImport.bricks.length} {tr('块积木，替换后可撤销。', 'bricks. Replacement can be undone.')}</p>
        <button className="primary-button" data-brick-effect="shatter" onClick={() => { commit(pendingImport); setPendingImport(null); setSelectedId(null); requestAnimationFrame(() => scene.current?.fit()); }}>{tr('打开项目', 'Open project')}</button></div>
    </Modal>}
  </div>;
}
