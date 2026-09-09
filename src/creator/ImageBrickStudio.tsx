import { useEffect, useMemo, useRef, useState, type DragEvent } from 'react';
import {
  ArrowDownToLine, Boxes, ChevronLeft, ChevronRight, FileImage, Layers3, Pause, Play,
  Rotate3D, Upload,
} from 'lucide-react';
import type { Locale, Translator } from '../app/locale';
import { ImageBrickScene } from '../scene/ImageBrickScene';
import {
  createBrickRelief, createDemoBrickBuild, imageBrickBuildToLdraw,
  type ImageBrickBuild, type ImageBrickOptions,
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
};

function download(data: string, filename: string, type: string) {
  const url = URL.createObjectURL(new Blob([data], { type }));
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

async function sampleImage(file: File, options: ImageBrickOptions) {
  const bitmap = await createImageBitmap(file);
  const width = Math.max(12, Math.min(48, Math.round(options.width)));
  const height = Math.max(8, Math.min(48, Math.round(width / (bitmap.width / bitmap.height) / 1.2)));
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const context = canvas.getContext('2d', { willReadFrequently: true });
  if (!context) throw new Error('Canvas 2D is unavailable');
  context.clearRect(0, 0, width, height);
  context.drawImage(bitmap, 0, 0, width, height);
  bitmap.close();
  return createBrickRelief(
    context.getImageData(0, 0, width, height).data,
    width,
    height,
    options,
    file.name.replace(/\.[^.]+$/, ''),
  );
}

export function ImageBrickStudio({ locale, tr }: { locale: Locale; tr: Translator }) {
  const hostRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<ImageBrickScene | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [options, setOptions] = useState(initialOptions);
  const [build, setBuild] = useState<ImageBrickBuild>(() => createDemoBrickBuild());
  const [step, setStep] = useState(build.steps.length);
  const [explosion, setExplosion] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [autoRotate, setAutoRotate] = useState(true);
  const [activePanel, setActivePanel] = useState<'parts' | 'steps'>('parts');
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState('');

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
  }, [step]);

  useEffect(() => {
    sceneRef.current?.setExplosion(explosion);
  }, [explosion]);

  useEffect(() => {
    sceneRef.current?.setAutoRotate(autoRotate);
  }, [autoRotate]);

  useEffect(() => {
    if (!playing || !build.steps.length) return;
    const timer = window.setInterval(() => {
      setStep(current => current >= build.steps.length ? 0 : current + 1);
    }, 850);
    return () => window.clearInterval(timer);
  }, [playing, build.steps.length]);

  useEffect(() => {
    if (!file) return;
    let active = true;
    setProcessing(true);
    setError('');
    const timer = window.setTimeout(() => {
      sampleImage(file, options)
        .then(next => {
          if (!active) return;
          if (!next.bricks.length) throw new Error(tr('没有识别到主体，请关闭背景移除或降低阈值。', 'No subject found. Disable background removal or lower the threshold.'));
          setBuild(next);
          setStep(next.steps.length);
          setExplosion(0);
          setPlaying(false);
        })
        .catch(cause => {
          if (active) setError(cause instanceof Error ? cause.message : String(cause));
        })
        .finally(() => {
          if (active) setProcessing(false);
        });
    }, 120);
    return () => {
      active = false;
      window.clearTimeout(timer);
    };
  }, [file, options, tr]);

  useEffect(() => {
    if (!file) return;
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

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

  function acceptFile(next?: File) {
    if (!next) return;
    if (!next.type.startsWith('image/')) {
      setError(tr('请选择 PNG、JPEG 或 WebP 图片。', 'Choose a PNG, JPEG, or WebP image.'));
      return;
    }
    setFile(next);
  }

  function drop(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    acceptFile(event.dataTransfer.files[0]);
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
        <h1>{tr('图片积木工坊', 'Image Brick Studio')}</h1>
        <p>{tr('单图彩色体素浮雕', 'Single-image color relief')}</p>
      </div>
      <label className="image-upload" onDragOver={event => event.preventDefault()} onDrop={drop}>
        {previewUrl
          ? <img src={previewUrl} alt={tr('上传图片预览', 'Uploaded image preview')} />
          : <div className="image-upload-empty"><FileImage size={28} /><strong>{tr('选择物品图片', 'Choose an object image')}</strong><span>PNG · JPEG · WEBP</span></div>}
        <input type="file" accept="image/png,image/jpeg,image/webp" onChange={event => acceptFile(event.target.files?.[0])} />
        <span className="image-upload-action"><Upload size={14} />{file ? tr('更换图片', 'Replace image') : tr('上传图片', 'Upload image')}</span>
      </label>
      <div className="image-controls-grid">
        <label><span>{tr('模型宽度', 'Model width')}<b>{options.width}</b></span><input aria-label={tr('模型宽度', 'Model width')} type="range" min={16} max={40} step={2} value={options.width} onChange={event => setOptions(value => ({ ...value, width: Number(event.target.value) }))} /></label>
        <label><span>{tr('浮雕深度', 'Relief depth')}<b>{options.maxDepth}</b></span><input aria-label={tr('浮雕深度', 'Relief depth')} type="range" min={1} max={6} value={options.maxDepth} onChange={event => setOptions(value => ({ ...value, maxDepth: Number(event.target.value) }))} /></label>
        <label><span>{tr('颜色数量', 'Color count')}<b>{options.maxColors}</b></span><input aria-label={tr('颜色数量', 'Color count')} type="range" min={4} max={18} value={options.maxColors} onChange={event => setOptions(value => ({ ...value, maxColors: Number(event.target.value) }))} /></label>
        <label><span>{tr('背景阈值', 'Background threshold')}<b>{options.backgroundThreshold}</b></span><input aria-label={tr('背景阈值', 'Background threshold')} type="range" min={4} max={42} value={options.backgroundThreshold} disabled={!options.removeBackground} onChange={event => setOptions(value => ({ ...value, backgroundThreshold: Number(event.target.value) }))} /></label>
      </div>
      <label className="creator-check"><input type="checkbox" checked={options.removeBackground} onChange={event => setOptions(value => ({ ...value, removeBackground: event.target.checked }))} /><span>{tr('移除近似背景', 'Remove similar background')}</span></label>
      <div className="image-build-stats">
        <div><strong>{brickCount}</strong><span>{tr('积木', 'Bricks')}</span></div>
        <div><strong>{build.steps.length}</strong><span>{tr('步骤', 'Steps')}</span></div>
        <div><strong>{colorCount}</strong><span>{tr('颜色', 'Colors')}</span></div>
      </div>
      {processing && <div className="creator-status" role="status">{tr('正在生成积木模型…', 'Generating brick model...')}</div>}
      {error && <div className="creator-error" role="alert">{error}</div>}
      <div className="creator-export-row">
        <button onClick={exportBom}><ArrowDownToLine size={15} />BOM CSV</button>
        <button onClick={() => download(imageBrickBuildToLdraw(build), `${build.name}.ldr`, 'text/plain;charset=utf-8')}><ArrowDownToLine size={15} />LDraw</button>
      </div>
    </aside>

    <div className="image-studio-stage">
      <div className="image-stage-heading">
        <div><span className="eyebrow">{file ? tr('已生成模型', 'Generated model') : tr('交互演示', 'Interactive demo')}</span><strong>{build.name}</strong></div>
        <button className={autoRotate ? 'active' : ''} onClick={() => setAutoRotate(value => !value)} aria-pressed={autoRotate}><Rotate3D size={16} />{tr('旋转', 'Rotate')}</button>
      </div>
      <div className="image-brick-canvas" ref={hostRef} />
      <div className="image-stage-controls">
        <button aria-label={playing ? tr('暂停拼装', 'Pause build') : tr('播放拼装', 'Play build')} onClick={() => setPlaying(value => !value)}>{playing ? <Pause size={17} /> : <Play size={17} />}</button>
        <button aria-label={tr('上一步', 'Previous step')} disabled={step === 0} onClick={() => setStep(value => Math.max(0, value - 1))}><ChevronLeft size={17} /></button>
        <input aria-label={tr('拼装进度', 'Build progress')} type="range" min={0} max={build.steps.length} value={step} onChange={event => setStep(Number(event.target.value))} />
        <output>{step} / {build.steps.length}</output>
        <button aria-label={tr('下一步', 'Next step')} disabled={step === build.steps.length} onClick={() => setStep(value => Math.min(build.steps.length, value + 1))}><ChevronRight size={17} /></button>
        <label><Layers3 size={16} /><span>{tr('拆分', 'Explode')}</span><input aria-label={tr('拆分程度', 'Explosion')} type="range" min={0} max={100} value={Math.round(explosion * 100)} onChange={event => setExplosion(Number(event.target.value) / 100)} /></label>
      </div>
    </div>

    <aside className="image-studio-results">
      <div className="image-result-tabs" role="tablist" aria-label={tr('生成结果', 'Generated result')}>
        <button role="tab" aria-selected={activePanel === 'parts'} onClick={() => setActivePanel('parts')}>{tr('材料清单', 'Materials')}</button>
        <button role="tab" aria-selected={activePanel === 'steps'} onClick={() => setActivePanel('steps')}>{tr('拼装步骤', 'Build steps')}</button>
      </div>
      <div className="image-result-scroll">
        {activePanel === 'parts'
          ? build.bom.map(item => <div className="image-bom-row" key={item.key}><i style={{ background: item.colorHex }} /><span><strong>Brick 1 × {item.width}</strong><small>{locale === 'zh' ? item.colorNameZh : item.colorNameEn} · {item.partId}</small></span><b>× {item.quantity}</b></div>)
          : build.steps.map(item => <button className={item.id === step ? 'current' : ''} key={item.id} onClick={() => setStep(item.id)}><span>{String(item.id).padStart(2, '0')}</span><strong>{tr(`第 ${item.layer + 1} 层 · 第 ${item.rowStart + 1}-${item.rowEnd + 1} 行`, `Layer ${item.layer + 1} · rows ${item.rowStart + 1}-${item.rowEnd + 1}`)}</strong><small>{item.brickIds.length}</small></button>)}
      </div>
      <div className="image-current-step">
        <span>{tr('本步零件', 'Current step')}</span>
        <strong>{currentStep?.brickIds.length ?? 0}</strong>
        <div>{currentParts.slice(0, 7).map(item => <i key={item.key} title={`${locale === 'zh' ? item.colorNameZh : item.colorNameEn} × ${item.quantity}`} style={{ background: item.colorHex }} />)}</div>
      </div>
    </aside>
  </section>;
}
