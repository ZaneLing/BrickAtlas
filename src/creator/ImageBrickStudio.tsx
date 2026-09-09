import { useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowDownToLine, ArrowLeft, ArrowRight, BookOpen, Box, ChevronDown, Crosshair,
  Expand, Hand, Layers3, Minus, Pause, Play, Plus, Rotate3D, RotateCcw,
  SkipBack, SkipForward,
} from 'lucide-react';
import type { Locale, Translator } from '../app/locale';
import { ImageBrickScene, type ImageBrickView } from '../scene/ImageBrickScene';
import { IconButton } from '../ui/Controls';
import { centeredSquare, ImageCropEditor, type CropRect, type ImageSource, type ImageViewRole } from './ImageCropEditor';
import {
  createBrickModelFromViews, createDemoBrickBuild, imageBrickBuildToLdraw,
  type ImageBrickBuild, type ImageBrickOptions, type ImageBrickViews,
} from './imageBrickModel';

declare global {
  interface Window {
    __imageBricks?: () => ReturnType<ImageBrickScene['snapshot']>;
  }
}

const initialOptions: ImageBrickOptions = {
  width: 28,
  maxDepth: 4,
  maxColors: 12,
  removeBackground: true,
  backgroundThreshold: 18,
  method: 'relief',
  bond: 'running',
  brickBudget: 1800,
};

const roles: ImageViewRole[] = ['front', 'top', 'side'];

function download(data: string, filename: string, type: string) {
  const url = URL.createObjectURL(new Blob([data], { type }));
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

async function sampleSource(source: ImageSource, size: number) {
  const bitmap = await createImageBitmap(source.file);
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const context = canvas.getContext('2d', { willReadFrequently: true });
  if (!context) throw new Error('Canvas 2D is unavailable');
  context.clearRect(0, 0, size, size);
  context.drawImage(
    bitmap,
    source.crop.x,
    source.crop.y,
    source.crop.size,
    source.crop.size,
    0,
    0,
    size,
    size,
  );
  bitmap.close();
  return { data: context.getImageData(0, 0, size, size).data, width: size, height: size };
}

async function generateBuild(
  sources: Partial<Record<ImageViewRole, ImageSource>>,
  options: ImageBrickOptions,
) {
  if (!sources.front) throw new Error('A front view is required');
  let resolution = options.width;
  let result: ImageBrickBuild | null = null;
  for (let attempt = 0; attempt < 4; attempt++) {
    const sampled = {} as Partial<ImageBrickViews>;
    for (const role of roles) {
      if (sources[role]) sampled[role] = await sampleSource(sources[role]!, resolution);
    }
    result = createBrickModelFromViews(sampled as ImageBrickViews, { ...options, width: resolution }, sources.front.file.name.replace(/\.[^.]+$/, ''));
    if (result.bricks.length <= options.brickBudget || resolution <= 12) break;
    const dimensions = options.method === 'relief' ? 2 : 3;
    const ratio = Math.pow(options.brickBudget / result.bricks.length, 1 / dimensions);
    resolution = Math.max(12, Math.floor(resolution * Math.min(0.88, ratio * 0.94)));
  }
  return result!;
}

export function ImageBrickStudio({ locale, tr }: { locale: Locale; tr: Translator }) {
  const hostRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<ImageBrickScene | null>(null);
  const sourcesRef = useRef<Partial<Record<ImageViewRole, ImageSource>>>({});
  const [sources, setSources] = useState<Partial<Record<ImageViewRole, ImageSource>>>({});
  const [options, setOptions] = useState(initialOptions);
  const [build, setBuild] = useState<ImageBrickBuild>(() => createDemoBrickBuild());
  const [step, setStep] = useState(build.steps.length);
  const [explosion, setExplosion] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [autoRotate, setAutoRotate] = useState(true);
  const [panMode, setPanMode] = useState(false);
  const [followStep, setFollowStep] = useState(false);
  const [view, setView] = useState<ImageBrickView>('perspective');
  const [activePanel, setActivePanel] = useState<'parts' | 'steps'>('parts');
  const [openStep, setOpenStep] = useState<number | null>(null);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    sourcesRef.current = sources;
  }, [sources]);
  useEffect(() => () => {
    Object.values(sourcesRef.current).forEach(source => URL.revokeObjectURL(source.url));
  }, []);

  useEffect(() => {
    if (!hostRef.current) return;
    const scene = new ImageBrickScene(hostRef.current, tr('图片生成的积木三维模型', 'Image-generated brick model'));
    sceneRef.current = scene;
    window.__imageBricks = () => scene.snapshot();
    scene.setBuild(build);
    scene.setBuildStep(step, false);
    return () => {
      scene.dispose();
      sceneRef.current = null;
      delete window.__imageBricks;
    };
  }, []);

  useEffect(() => {
    sceneRef.current?.setLabel(tr('图片生成的积木三维模型', 'Image-generated brick model'));
  }, [tr]);
  useEffect(() => {
    sceneRef.current?.setBuild(build);
    sceneRef.current?.setBuildStep(step, false);
  }, [build]);
  useEffect(() => {
    sceneRef.current?.setBuildStep(step);
    if (followStep && step > 0) requestAnimationFrame(() => sceneRef.current?.focusStep(step));
  }, [step, followStep]);
  useEffect(() => { sceneRef.current?.setExplosion(explosion); }, [explosion]);
  useEffect(() => { sceneRef.current?.setAutoRotate(autoRotate); }, [autoRotate]);
  useEffect(() => { sceneRef.current?.setPanMode(panMode); }, [panMode]);
  useEffect(() => { sceneRef.current?.setView(view); }, [view]);

  useEffect(() => {
    if (!playing || !build.steps.length) return;
    if (step >= build.steps.length) {
      setPlaying(false);
      return;
    }
    const timer = window.setTimeout(() => setStep(current => Math.min(build.steps.length, current + 1)), 850);
    return () => window.clearTimeout(timer);
  }, [playing, build.steps.length, step]);

  useEffect(() => {
    if (!sources.front) return;
    let active = true;
    setProcessing(true);
    setError('');
    const timer = window.setTimeout(() => {
      generateBuild(sources, options)
        .then(next => {
          if (!active) return;
          if (!next.bricks.length) throw new Error(tr('没有识别到主体，请调整框选区域或背景阈值。', 'No subject found. Adjust the crop or background threshold.'));
          setBuild(next);
          setStep(next.steps.length);
          setOpenStep(next.steps.length);
          setExplosion(0);
          setPlaying(false);
        })
        .catch(cause => {
          if (active) setError(cause instanceof Error ? cause.message : String(cause));
        })
        .finally(() => {
          if (active) setProcessing(false);
        });
    }, 180);
    return () => {
      active = false;
      window.clearTimeout(timer);
    };
  }, [sources, options, tr]);

  const brickCount = build.bricks.length;
  const colorCount = new Set(build.bricks.map(brick => brick.colorId)).size;
  const currentStep = build.steps.find(item => item.id === step);
  const currentParts = useMemo(() => {
    if (!currentStep) return [];
    const ids = new Set(currentStep.brickIds);
    return build.bom.map(item => ({
      ...item,
      quantity: build.bricks.filter(brick => ids.has(brick.id) && `${brick.partId}:${brick.colorId}` === item.key).length,
    })).filter(item => item.quantity);
  }, [build, currentStep]);
  const viewCount = Object.values(sources).filter(Boolean).length;

  async function acceptFile(role: ImageViewRole, next?: File) {
    if (!next) return;
    if (!next.type.startsWith('image/')) {
      setError(tr('请选择 PNG、JPEG 或 WebP 图片。', 'Choose a PNG, JPEG, or WebP image.'));
      return;
    }
    const bitmap = await createImageBitmap(next);
    const source: ImageSource = {
      file: next,
      url: URL.createObjectURL(next),
      width: bitmap.width,
      height: bitmap.height,
      crop: centeredSquare(bitmap.width, bitmap.height),
    };
    bitmap.close();
    setSources(current => {
      if (current[role]) URL.revokeObjectURL(current[role]!.url);
      return { ...current, [role]: source };
    });
    if (role !== 'front') setOptions(current => ({ ...current, method: current.method === 'relief' ? 'hollow' : current.method }));
  }

  function updateCrop(role: ImageViewRole, crop: CropRect) {
    setSources(current => current[role] ? { ...current, [role]: { ...current[role]!, crop } } : current);
  }

  function removeSource(role: ImageViewRole) {
    setSources(current => {
      if (!current[role]) return current;
      URL.revokeObjectURL(current[role]!.url);
      const next = { ...current };
      delete next[role];
      if (role !== 'front' && Object.values(next).filter(Boolean).length < 2) {
        setOptions(value => ({ ...value, method: 'relief' }));
      }
      return next;
    });
    if (role === 'front') {
      const demo = createDemoBrickBuild();
      setBuild(demo);
      setStep(demo.steps.length);
      setOpenStep(null);
      setError('');
    }
  }

  function setBuildStep(next: number) {
    const clamped = Math.max(0, Math.min(build.steps.length, next));
    const focusFirstStep = step === 0 && clamped === 1 && !followStep;
    setStep(clamped);
    if (focusFirstStep) {
      setAutoRotate(false);
      requestAnimationFrame(() => sceneRef.current?.focusStep(clamped));
    }
  }

  function exportBom() {
    const rows = [
      ['partId', 'size', 'color', 'ldrawColor', 'quantity'],
      ...build.bom.map(item => [item.partId, `1x${item.width}`, locale === 'zh' ? item.colorNameZh : item.colorNameEn, String(item.colorCode), String(item.quantity)]),
    ];
    download(rows.map(row => row.map(value => `"${value.replaceAll('"', '""')}"`).join(',')).join('\n'), `${build.name}-bom.csv`, 'text/csv;charset=utf-8');
  }

  return <section className="image-studio" aria-label={tr('图片转积木工作台', 'Image to brick studio')}>
    <aside className="image-studio-controls">
      <div className="creator-title">
        <span className="eyebrow">IMAGE TO BRICKS</span>
        <h1>{tr('多视图积木工坊', 'Multi-view Brick Studio')}</h1>
        <p>{tr('框选主体并融合正视、俯视与侧视轮廓', 'Crop the subject and fuse front, top, and side silhouettes')}</p>
      </div>
      <div className="crop-source-list">
        {roles.map(role => <ImageCropEditor
          key={role}
          role={role}
          source={sources[role]}
          onFile={file => acceptFile(role, file)}
          onCrop={crop => updateCrop(role, crop)}
          onRemove={() => removeSource(role)}
          tr={tr}
        />)}
      </div>
      <div className="image-option-selects">
        <label>{tr('生成方法', 'Generation method')}<select aria-label={tr('生成方法', 'Generation method')} value={options.method} onChange={event => setOptions(value => ({ ...value, method: event.target.value as ImageBrickOptions['method'] }))}>
          <option value="relief">{tr('彩色浮雕', 'Color relief')}</option>
          <option value="hollow" disabled={viewCount < 2}>{tr('空心立体外壳', 'Hollow sculpture')}</option>
          <option value="solid" disabled={viewCount < 2}>{tr('实心视觉体', 'Solid visual hull')}</option>
        </select></label>
        <label>{tr('砌砖方式', 'Brick bond')}<select aria-label={tr('砌砖方式', 'Brick bond')} value={options.bond} onChange={event => setOptions(value => ({ ...value, bond: event.target.value as ImageBrickOptions['bond'] }))}>
          <option value="running">{tr('错缝拼接', 'Running bond')}</option>
          <option value="stacked">{tr('齐缝拼接', 'Stacked bond')}</option>
          <option value="reinforced">{tr('加强拼接', 'Reinforced bond')}</option>
        </select></label>
      </div>
      <div className="image-controls-grid">
        <label><span>{tr('目标分辨率', 'Target resolution')}<b>{options.width}</b></span><input aria-label={tr('目标分辨率', 'Target resolution')} type="range" min={16} max={40} step={2} value={options.width} onChange={event => setOptions(value => ({ ...value, width: Number(event.target.value) }))} /></label>
        <label><span>{tr('积木预算', 'Brick budget')}<b>{options.brickBudget}</b></span><input aria-label={tr('积木预算', 'Brick budget')} type="range" min={300} max={5000} step={100} value={options.brickBudget} onChange={event => setOptions(value => ({ ...value, brickBudget: Number(event.target.value) }))} /></label>
        <label><span>{tr('浮雕深度', 'Relief depth')}<b>{options.maxDepth}</b></span><input aria-label={tr('浮雕深度', 'Relief depth')} type="range" min={1} max={6} value={options.maxDepth} disabled={options.method !== 'relief'} onChange={event => setOptions(value => ({ ...value, maxDepth: Number(event.target.value) }))} /></label>
        <label><span>{tr('颜色数量', 'Color count')}<b>{options.maxColors}</b></span><input aria-label={tr('颜色数量', 'Color count')} type="range" min={4} max={18} value={options.maxColors} onChange={event => setOptions(value => ({ ...value, maxColors: Number(event.target.value) }))} /></label>
        <label><span>{tr('背景阈值', 'Background threshold')}<b>{options.backgroundThreshold}</b></span><input aria-label={tr('背景阈值', 'Background threshold')} type="range" min={4} max={42} value={options.backgroundThreshold} disabled={!options.removeBackground} onChange={event => setOptions(value => ({ ...value, backgroundThreshold: Number(event.target.value) }))} /></label>
      </div>
      <label className="creator-check"><input type="checkbox" checked={options.removeBackground} onChange={event => setOptions(value => ({ ...value, removeBackground: event.target.checked }))} /><span>{tr('移除近似背景', 'Remove similar background')}</span></label>
      <div className="image-build-stats">
        <div><strong>{brickCount}</strong><span>{tr('积木', 'Bricks')}</span></div>
        <div><strong>{build.steps.length}</strong><span>{tr('步骤', 'Steps')}</span></div>
        <div><strong>{colorCount}</strong><span>{tr('颜色', 'Colors')}</span></div>
        <div><strong>{build.viewCount}</strong><span>{tr('视图', 'Views')}</span></div>
      </div>
      {build.sourceWidth < options.width && <div className="creator-status">{tr(`为满足 ${options.brickBudget} 块预算，分辨率自动调整为 ${build.sourceWidth}`, `Resolution adjusted to ${build.sourceWidth} to fit the ${options.brickBudget}-brick budget`)}</div>}
      {processing && <div className="creator-status" role="status">{tr('正在融合视图并生成积木模型…', 'Fusing views and generating the brick model...')}</div>}
      {error && <div className="creator-error" role="alert">{error}</div>}
      <div className="creator-export-row">
        <button onClick={exportBom}><ArrowDownToLine size={15} />BOM CSV</button>
        <button onClick={() => download(imageBrickBuildToLdraw(build), `${build.name}.ldr`, 'text/plain;charset=utf-8')}><ArrowDownToLine size={15} />LDraw</button>
      </div>
    </aside>

    <main className="image-studio-stage">
      <div className="image-stage-heading">
        <div><span className="eyebrow">{sources.front ? tr('已生成模型', 'Generated model') : tr('交互演示', 'Interactive demo')}</span><strong>{build.name}</strong></div>
      </div>
      <div className="image-brick-canvas" ref={hostRef} />
      <div className="image-viewport-toolbar" aria-label={tr('视角工具', 'View tools')}>
        <div className="view-select"><Box size={16} /><select aria-label={tr('模型视角', 'Model view')} value={view} onChange={event => setView(event.target.value as ImageBrickView)}>
          <option value="perspective">{tr('三分之四', 'Perspective')}</option>
          <option value="front">{tr('正面', 'Front')}</option>
          <option value="side">{tr('侧面', 'Side')}</option>
          <option value="top">{tr('顶部', 'Top')}</option>
        </select><ChevronDown size={12} /></div>
        <IconButton label={tr('自动旋转', 'Auto rotate')} active={autoRotate} onClick={() => setAutoRotate(value => !value)}><Rotate3D size={17} /></IconButton>
        <IconButton label={tr('平移视图（上下左右拖动）', 'Pan view in any direction')} active={panMode} onClick={() => setPanMode(value => !value)}><Hand size={17} /></IconButton>
        <IconButton label={tr('步骤镜头跟随', 'Step camera follow')} active={followStep} onClick={() => {
          setFollowStep(value => !value);
          if (!followStep && step > 0) {
            setAutoRotate(false);
            sceneRef.current?.focusStep(step);
          }
        }}><Crosshair size={17} /></IconButton>
        <IconButton label={tr('适配全部可见积木', 'Fit visible bricks')} onClick={() => sceneRef.current?.fitVisible()}><Expand size={17} /></IconButton>
      </div>
      <div className="image-zoom-tools">
        <IconButton label={tr('放大模型', 'Zoom in')} onClick={() => sceneRef.current?.zoom(0.8)}><Plus size={17} /></IconButton>
        <IconButton label={tr('缩小模型', 'Zoom out')} onClick={() => sceneRef.current?.zoom(1.25)}><Minus size={17} /></IconButton>
        <IconButton label={tr('复原模型', 'Reset model')} onClick={() => {
          setExplosion(0);
          setAutoRotate(false);
          setPanMode(false);
          setView('perspective');
          sceneRef.current?.fitVisible();
        }}><RotateCcw size={17} /></IconButton>
      </div>
      <section className="image-build-dock" aria-label={tr('拼装步骤控制', 'Build step controls')}>
        <div className="dock-heading"><div><BookOpen size={17} /><strong>{currentStep ? tr(`第 ${step} 步`, `Step ${step}`) : tr('准备拼装', 'Ready to build')}</strong><span className="phase-name">{build.method === 'relief' ? tr('浮雕', 'Relief') : tr('多视图立体', 'Multi-view')}</span></div><output>{step}<span> / {build.steps.length}</span></output></div>
        <div className="step-controls">
          <IconButton label={tr('回到开始', 'Restart')} disabled={step === 0} onClick={() => setBuildStep(0)}><SkipBack size={16} /></IconButton>
          <IconButton label={tr('上一步', 'Previous step')} disabled={step === 0} onClick={() => setBuildStep(step - 1)}><ArrowLeft size={17} /></IconButton>
          <IconButton label={playing ? tr('暂停拼装', 'Pause build') : tr('播放拼装', 'Play build')} active={playing} disabled={step === build.steps.length} onClick={() => setPlaying(value => !value)}>{playing ? <Pause size={17} /> : <Play size={17} />}</IconButton>
          <input aria-label={tr('当前拼装步骤', 'Current build step')} type="range" min={0} max={build.steps.length} value={step} onChange={event => setBuildStep(Number(event.target.value))} style={{ '--range-fill': `${build.steps.length ? step / build.steps.length * 100 : 0}%` } as React.CSSProperties} />
          <IconButton label={tr('下一步', 'Next step')} disabled={step === build.steps.length} onClick={() => setBuildStep(step + 1)}><ArrowRight size={17} /></IconButton>
          <IconButton label={tr('完成模型', 'Complete model')} disabled={step === build.steps.length} onClick={() => setBuildStep(build.steps.length)}><SkipForward size={16} /></IconButton>
        </div>
        <div className="image-explode-row"><Layers3 size={15} /><span>{tr('拆分', 'Explode')}</span><input aria-label={tr('拆分程度', 'Explosion')} type="range" min={0} max={100} value={Math.round(explosion * 100)} onChange={event => setExplosion(Number(event.target.value) / 100)} /><output>{Math.round(explosion * 100)}%</output></div>
      </section>
    </main>

    <aside className="image-studio-results">
      <div className="image-result-tabs" role="tablist" aria-label={tr('生成结果', 'Generated result')}>
        <button role="tab" aria-selected={activePanel === 'parts'} onClick={() => setActivePanel('parts')}>{tr('材料清单', 'Materials')}</button>
        <button role="tab" aria-selected={activePanel === 'steps'} onClick={() => setActivePanel('steps')}>{tr('拼装步骤', 'Build steps')}</button>
      </div>
      <div className="image-result-scroll">
        {activePanel === 'parts'
          ? build.bom.map(item => <div className="image-bom-row" key={item.key}><i style={{ background: item.colorHex }} /><span><strong>Brick 1 × {item.width}</strong><small>{locale === 'zh' ? item.colorNameZh : item.colorNameEn} · {item.partId}</small></span><b>× {item.quantity}</b></div>)
          : build.steps.map(item => {
            const isOpen = openStep === item.id;
            const parts = build.bricks.filter(brick => item.brickIds.includes(brick.id));
            return <details className={`instruction-brick-step image-instruction-step ${item.id === step ? 'current' : ''}`} open={isOpen} key={item.id}>
              <summary onClick={event => {
                event.preventDefault();
                setOpenStep(isOpen ? null : item.id);
                setAutoRotate(false);
                setBuildStep(item.id);
                requestAnimationFrame(() => sceneRef.current?.focusStep(item.id));
              }}>
                <span className="instruction-brick-studs" aria-hidden="true"><i /><i /><i /><i /></span>
                <span className="instruction-brick-number">{String(item.id).padStart(2, '0')}</span>
                <span className="instruction-brick-label"><strong>{tr(`第 ${item.layer + 1} 层`, `Layer ${item.layer + 1}`)}</strong><small>{item.brickIds.length} {tr('块积木', 'bricks')}</small></span>
                <ChevronDown className="instruction-brick-chevron" size={16} />
              </summary>
              {isOpen && <div className="image-step-detail">
                <div className="image-step-swatches">{parts.slice(0, 16).map(brick => <i key={brick.id} style={{ background: brick.colorHex }} />)}</div>
                <button onClick={() => {
                  setAutoRotate(false);
                  sceneRef.current?.focusStep(item.id);
                }}><Crosshair size={14} />{tr('聚焦本步', 'Focus step')}</button>
              </div>}
            </details>;
          })}
      </div>
      <div className="image-current-step">
        <span>{tr('本步零件', 'Current step')}</span>
        <strong>{currentStep?.brickIds.length ?? 0}</strong>
        <div>{currentParts.slice(0, 7).map(item => <i key={item.key} title={`${locale === 'zh' ? item.colorNameZh : item.colorNameEn} × ${item.quantity}`} style={{ background: item.colorHex }} />)}</div>
      </div>
    </aside>
  </section>;
}
