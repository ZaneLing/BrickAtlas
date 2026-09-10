import { useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowDownToLine, ArrowLeft, ArrowRight, BookOpen, Box, ChevronDown, Crosshair,
  Cloud, Cpu, Expand, FileDown, Hand, ImagePlus, Layers3, Minus, Pause, Play,
  Plus, Rotate3D, RotateCcw, SkipBack, SkipForward, Triangle, X,
} from 'lucide-react';
import type { Locale, Translator } from '../app/locale';
import { ImageBrickScene, type ImageBrickView } from '../scene/ImageBrickScene';
import { MeshPreviewScene } from '../scene/MeshPreviewScene';
import { IconButton } from '../ui/Controls';
import { centeredSquare, ImageCropEditor, type CropRect, type ImageSource, type ImageViewRole } from './ImageCropEditor';
import { estimatePhotoDepth, type DepthPhase } from './depthEstimation';
import {
  createBrickModelFromMeshVolume, createEmptyBrickBuild, imageBrickBuildToLdraw,
  type ImageBrickBuild, type ImageBrickOptions, type ImageBrickViews, type SampledDepth,
  type SampledMeshVolume,
} from './imageBrickModel';
import {
  extractMeshTriangles, reconstructPhotoMesh, type CloudMeshPhase,
  type CloudMeshProvider, type CloudMeshResult, type ExtractedMesh,
} from './meshReconstruction';

declare global {
  interface Window {
    __imageBricks?: () => ReturnType<ImageBrickScene['snapshot']>;
    __imageMesh?: () => ReturnType<MeshPreviewScene['snapshot']>;
  }
}

const initialOptions: ImageBrickOptions = {
  width: 28,
  maxDepth: 16,
  maxColors: 12,
  removeBackground: true,
  backgroundThreshold: 18,
  method: 'hollow',
  bond: 'running',
  brickBudget: 2400,
};

const roles: ImageViewRole[] = ['front', 'left', 'back', 'right'];
type ReconstructionMode = 'mesh' | 'local';
type MeshStatus = 'idle' | CloudMeshPhase | 'parsing' | 'voxelizing' | 'ready' | 'error';

function download(data: string, filename: string, type: string) {
  const url = URL.createObjectURL(new Blob([data], { type }));
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
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
  if (source.fit) {
    const scale = Math.min(size / bitmap.width, size / bitmap.height);
    const width = bitmap.width * scale;
    const height = bitmap.height * scale;
    context.drawImage(bitmap, (size - width) / 2, (size - height) / 2, width, height);
  } else {
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
  }
  bitmap.close();
  return { data: context.getImageData(0, 0, size, size).data, width: size, height: size };
}

async function sourceFile(source: ImageSource, size = 768) {
  const bitmap = await createImageBitmap(source.file);
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const context = canvas.getContext('2d');
  if (!context) throw new Error('Canvas 2D is unavailable');
  context.fillStyle = '#ffffff';
  context.fillRect(0, 0, size, size);
  if (source.fit) {
    const scale = Math.min(size / bitmap.width, size / bitmap.height);
    const width = bitmap.width * scale;
    const height = bitmap.height * scale;
    context.drawImage(bitmap, (size - width) / 2, (size - height) / 2, width, height);
  } else {
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
  }
  bitmap.close();
  const blob = await new Promise<Blob>((resolve, reject) =>
    canvas.toBlob(value => value ? resolve(value) : reject(new Error('Could not encode image')), 'image/png'),
  );
  return new File([blob], source.file.name.replace(/\.[^.]+$/, '.png'), { type: 'image/png' });
}

async function voxelizeMesh(
  mesh: ExtractedMesh,
  source: ImageSource,
  options: ImageBrickOptions,
  providerName: string,
  signal: AbortSignal,
) {
  const front = await sampleSource(source, 512);
  let resolution = options.width;
  let build: ImageBrickBuild | null = null;
  while (resolution >= 12) {
    signal.throwIfAborted();
    const positions = mesh.positions.slice();
    const volume = await new Promise<SampledMeshVolume>((resolve, reject) => {
      const worker = new Worker(new URL('../workers/mesh.worker.ts', import.meta.url), { type: 'module' });
      const cleanup = () => {
        worker.terminate();
        signal.removeEventListener('abort', abort);
      };
      const abort = () => {
        cleanup();
        reject(new DOMException('Cancelled', 'AbortError'));
      };
      signal.addEventListener('abort', abort, { once: true });
      worker.onerror = event => {
        cleanup();
        reject(new Error(event.message));
      };
      worker.onmessage = ({ data }) => {
        cleanup();
        if (data.error) reject(new Error(data.error));
        else resolve(data.volume as SampledMeshVolume);
      };
      worker.postMessage({
        positions,
        resolution,
        hollow: options.method === 'hollow',
      }, [positions.buffer]);
    });
    build = createBrickModelFromMeshVolume(
      volume,
      front,
      { ...options, width: resolution },
      source.file.name.replace(/\.[^.]+$/, ''),
      `${providerName} public image-to-3D service`,
    );
    if (build.bricks.length <= options.brickBudget) break;
    if (resolution <= 12) {
      throw new Error(`Minimum resolution needs ${build.bricks.length} bricks; budget is ${options.brickBudget}.`);
    }
    const ratio = Math.cbrt(options.brickBudget / build.bricks.length);
    resolution = Math.max(12, Math.floor(resolution * Math.min(0.88, ratio * 0.94)));
  }
  return build!;
}

async function generateBuild(
  sources: Partial<Record<ImageViewRole, ImageSource>>,
  options: ImageBrickOptions,
  signal: AbortSignal,
  frontDepth?: SampledDepth,
) {
  if (!sources.front) throw new Error('A front view is required');
  let resolution = options.width;
  let result: ImageBrickBuild | null = null;
  while (resolution >= 12) {
    signal.throwIfAborted();
    const sampled = {} as Partial<ImageBrickViews>;
    for (const role of roles) {
      if (sources[role]) sampled[role] = await sampleSource(sources[role]!, resolution);
    }
    if (frontDepth) sampled.frontDepth = frontDepth;
    signal.throwIfAborted();
    result = await new Promise<ImageBrickBuild>((resolve, reject) => {
      const worker = new Worker(new URL('../workers/image.worker.ts', import.meta.url), { type: 'module' });
      const cleanup = () => { worker.terminate(); signal.removeEventListener('abort', abort); };
      const abort = () => { cleanup(); reject(new DOMException('Cancelled', 'AbortError')); };
      signal.addEventListener('abort', abort, { once: true });
      worker.onerror = event => { cleanup(); reject(new Error(event.message)); };
      worker.onmessage = ({ data }) => {
        cleanup();
        if (data.error) reject(new Error(data.error)); else resolve(data.build);
      };
      worker.postMessage({
        views: sampled as ImageBrickViews,
        options: { ...options, width: resolution },
        name: sources.front!.file.name.replace(/\.[^.]+$/, ''),
      });
    });
    if (result.bricks.length <= options.brickBudget) break;
    if (resolution <= 12) throw new Error(`Minimum resolution needs ${result.bricks.length} bricks; budget is ${options.brickBudget}.`);
    const dimensions = options.method === 'relief' ? 2 : 3;
    const ratio = Math.pow(options.brickBudget / result.bricks.length, 1 / dimensions);
    resolution = Math.max(12, Math.floor(resolution * Math.min(0.88, ratio * 0.94)));
  }
  return result!;
}

export function ImageBrickStudio({ locale, tr }: { locale: Locale; tr: Translator }) {
  const hostRef = useRef<HTMLDivElement>(null);
  const meshHostRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<ImageBrickScene | null>(null);
  const meshSceneRef = useRef<MeshPreviewScene | null>(null);
  const meshAbortRef = useRef<AbortController | null>(null);
  const sourcesRef = useRef<Partial<Record<ImageViewRole, ImageSource>>>({});
  const uploadVersions = useRef<Record<ImageViewRole, number>>({ front: 0, left: 0, back: 0, right: 0 });
  const [sources, setSources] = useState<Partial<Record<ImageViewRole, ImageSource>>>({});
  const [options, setOptions] = useState(initialOptions);
  const [reconstructionMode, setReconstructionMode] = useState<ReconstructionMode>('mesh');
  const [meshProvider, setMeshProvider] = useState<CloudMeshProvider>('triposr-cpu');
  const [hfToken, setHfToken] = useState('');
  const [meshStatus, setMeshStatus] = useState<MeshStatus>('idle');
  const [meshDetail, setMeshDetail] = useState('');
  const [meshResult, setMeshResult] = useState<CloudMeshResult | null>(null);
  const [meshData, setMeshData] = useState<ExtractedMesh | null>(null);
  const [meshSignature, setMeshSignature] = useState('');
  const [stageMode, setStageMode] = useState<'mesh' | 'bricks'>('bricks');
  const [build, setBuild] = useState<ImageBrickBuild>(() => createEmptyBrickBuild());
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
  const [depthState, setDepthState] = useState<{
    signature: string;
    status: 'idle' | 'loading' | 'ready' | 'fallback';
    phase?: DepthPhase;
    depth?: SampledDepth;
  }>({ signature: '', status: 'idle' });
  const [error, setError] = useState('');
  const frontSignature = sources.front
    ? [
        sources.front.file.name,
        sources.front.file.size,
        sources.front.crop.x.toFixed(2),
        sources.front.crop.y.toFixed(2),
        sources.front.crop.size.toFixed(2),
        sources.front.fit ? 'fit' : 'crop',
      ].join(':')
    : '';

  useEffect(() => {
    sourcesRef.current = sources;
  }, [sources]);
  useEffect(() => () => {
    meshAbortRef.current?.abort();
    roles.forEach(role => uploadVersions.current[role]++);
    Object.values(sourcesRef.current).forEach(source => URL.revokeObjectURL(source.url));
  }, []);

  useEffect(() => {
    if (!hostRef.current) return;
    const scene = new ImageBrickScene(hostRef.current, tr('图片生成的积木三维模型', 'Image-generated brick model'));
    sceneRef.current = scene;
    window.__imageBricks = () => scene.snapshot();
    return () => {
      scene.dispose();
      sceneRef.current = null;
      delete window.__imageBricks;
    };
  }, []);
  useEffect(() => {
    if (!meshHostRef.current) return;
    const scene = new MeshPreviewScene(
      meshHostRef.current,
      tr('AI 生成的中间三维网格', 'AI-generated intermediate 3D mesh'),
    );
    meshSceneRef.current = scene;
    window.__imageMesh = () => scene.snapshot();
    return () => {
      scene.dispose();
      meshSceneRef.current = null;
      delete window.__imageMesh;
    };
  }, []);

  useEffect(() => {
    sceneRef.current?.setLabel(tr('图片生成的积木三维模型', 'Image-generated brick model'));
    meshSceneRef.current?.setLabel(tr('AI 生成的中间三维网格', 'AI-generated intermediate 3D mesh'));
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
    if (!meshResult) return;
    void meshSceneRef.current?.setGlb(meshResult.blob).catch(cause => {
      setError(cause instanceof Error ? cause.message : String(cause));
    });
  }, [meshResult]);

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
    if (reconstructionMode !== 'local' || !sources.front) {
      setDepthState({ signature: '', status: 'idle' });
      return;
    }
    const source = sources.front;
    const signature = frontSignature;
    let active = true;
    const abort = new AbortController();
    setDepthState({ signature, status: 'loading', phase: 'model' });
    const timer = window.setTimeout(() => {
      sampleSource(source, 518)
        .then(image => estimatePhotoDepth(image, abort.signal, phase => {
          if (active) setDepthState({ signature, status: 'loading', phase });
        }))
        .then(depth => {
          if (active) setDepthState({ signature, status: 'ready', depth });
        })
        .catch(cause => {
          if (!active || cause instanceof DOMException && cause.name === 'AbortError') return;
          setDepthState({ signature, status: 'fallback' });
        });
    }, 360);
    return () => {
      active = false;
      abort.abort();
      window.clearTimeout(timer);
    };
  }, [frontSignature, reconstructionMode]);

  useEffect(() => {
    if (reconstructionMode !== 'local' || !sources.front) {
      setProcessing(false);
      return;
    }
    if (depthState.signature !== frontSignature || depthState.status === 'loading') return;
    let active = true;
    const abort = new AbortController();
    setProcessing(true);
    setError('');
    const timer = window.setTimeout(() => {
      generateBuild(sources, options, abort.signal, depthState.depth)
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
      abort.abort();
      window.clearTimeout(timer);
    };
  }, [sources, options, tr, frontSignature, depthState, reconstructionMode]);

  useEffect(() => {
    if (
      reconstructionMode !== 'mesh'
      || !sources.front
      || !meshData
      || !meshResult
      || meshSignature !== frontSignature
    ) return;
    let active = true;
    const abort = new AbortController();
    setProcessing(true);
    setMeshStatus('voxelizing');
    setError('');
    const timer = window.setTimeout(() => {
      voxelizeMesh(
        meshData,
        sources.front!,
        options,
        meshResult.providerName,
        abort.signal,
      ).then(next => {
        if (!active) return;
        if (!next.bricks.length) throw new Error(tr(
          '三维网格未产生可用积木，请提高分辨率。',
          'The 3D mesh produced no usable bricks. Increase the resolution.',
        ));
        setBuild(next);
        setStep(next.steps.length);
        setOpenStep(next.steps.length);
        setExplosion(0);
        setPlaying(false);
        setMeshStatus('ready');
        setStageMode('bricks');
      }).catch(cause => {
        if (!active || cause instanceof DOMException && cause.name === 'AbortError') return;
        setMeshStatus('error');
        setError(cause instanceof Error ? cause.message : String(cause));
      }).finally(() => {
        if (active) setProcessing(false);
      });
    }, 120);
    return () => {
      active = false;
      abort.abort();
      clearTimeout(timer);
    };
  }, [
    reconstructionMode, sources.front, options, meshData, meshResult,
    meshSignature, frontSignature, tr,
  ]);

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
  const reconstructionLabel = {
    empty: tr('等待照片', 'Waiting for photo'),
    relief: tr('浅浮雕', 'Relief'),
    'shape-inflation': tr('轮廓体积', 'Shape volume'),
    'depth-ai': tr('AI 深度实体', 'AI depth volume'),
    'multi-view': tr('多视图实体', 'Multi-view volume'),
    'mesh-ai': tr('AI 网格体素', 'AI mesh voxels'),
  }[build.reconstruction];

  function resetMesh() {
    meshAbortRef.current?.abort();
    meshAbortRef.current = null;
    setMeshStatus('idle');
    setMeshDetail('');
    setMeshResult(null);
    setMeshData(null);
    setMeshSignature('');
    setStageMode('bricks');
  }

  async function generateCloudMesh() {
    if (!sources.front || meshStatus === 'queued' || meshStatus === 'generating') return;
    meshAbortRef.current?.abort();
    const abort = new AbortController();
    meshAbortRef.current = abort;
    setError('');
    setBuild(createEmptyBrickBuild());
    setStep(0);
    setOpenStep(null);
    setProcessing(true);
    try {
      const upload = await sourceFile(sources.front);
      const result = await reconstructPhotoMesh(
        upload,
        meshProvider,
        abort.signal,
        (status, detail) => {
          setMeshStatus(status);
          setMeshDetail(detail ?? '');
        },
        hfToken,
      );
      abort.signal.throwIfAborted();
      setMeshStatus('parsing');
      const extracted = await extractMeshTriangles(result.blob);
      abort.signal.throwIfAborted();
      setMeshResult(result);
      setMeshData(extracted);
      setMeshSignature(frontSignature);
      setMeshStatus('voxelizing');
      setStageMode('mesh');
    } catch (cause) {
      if (cause instanceof DOMException && cause.name === 'AbortError') return;
      const message = cause instanceof Error ? cause.message : String(cause);
      setMeshStatus('error');
      setError(/ZeroGPU quota/i.test(message)
        ? tr(
          '公开 GPU 的匿名额度暂不可用。可稍后重试，或临时输入 Hugging Face Token；Token 不会保存。',
          'Anonymous public GPU quota is unavailable. Retry later or enter a temporary Hugging Face token; it is not saved.',
        )
        : message);
    } finally {
      if (meshAbortRef.current === abort) meshAbortRef.current = null;
      setProcessing(false);
    }
  }

  async function acceptFile(role: ImageViewRole, next?: File) {
    if (!next) return;
    const version = ++uploadVersions.current[role];
    if (!next.type.startsWith('image/')) {
      setError(tr('请选择 PNG、JPEG 或 WebP 图片。', 'Choose a PNG, JPEG, or WebP image.'));
      return;
    }
    if (next.size > 25 * 1024 * 1024) {
      setError(tr('图片不能超过 25 MB。', 'Image must not exceed 25 MB.'));
      return;
    }
    try {
    const bitmap = await createImageBitmap(next);
    if (version !== uploadVersions.current[role]) { bitmap.close(); return; }
    if (bitmap.width * bitmap.height > 40_000_000) {
      bitmap.close();
      throw new Error(tr('图片不能超过 4000 万像素。', 'Image must not exceed 40 megapixels.'));
    }
    const source: ImageSource = {
      file: next,
      url: URL.createObjectURL(next),
      width: bitmap.width,
      height: bitmap.height,
      crop: centeredSquare(bitmap.width, bitmap.height),
      fit: true,
    };
    bitmap.close();
    setSources(current => {
      if (current[role]) URL.revokeObjectURL(current[role]!.url);
      return { ...current, [role]: source };
    });
    if (role === 'front') {
      resetMesh();
      setBuild(createEmptyBrickBuild());
      setStep(0);
    }
    if (role !== 'front') setOptions(current => ({ ...current, method: current.method === 'relief' ? 'hollow' : current.method }));
    } catch {
      if (version === uploadVersions.current[role]) setError(tr('图片解码失败，请选择有效的 PNG、JPEG 或 WebP。', 'Could not decode the image. Choose a valid PNG, JPEG, or WebP.'));
    }
  }

  function updateCrop(role: ImageViewRole, crop: CropRect) {
    if (role === 'front') {
      resetMesh();
      setBuild(createEmptyBrickBuild());
    }
    setSources(current => current[role]
      ? { ...current, [role]: { ...current[role]!, crop, fit: false } }
      : current);
  }

  function updateFit(role: ImageViewRole, fit: boolean) {
    if (role === 'front') {
      resetMesh();
      setBuild(createEmptyBrickBuild());
    }
    setSources(current => current[role]
      ? { ...current, [role]: { ...current[role]!, fit } }
      : current);
  }

  function removeSource(role: ImageViewRole) {
    uploadVersions.current[role]++;
    setSources(current => {
      if (!current[role]) return current;
      URL.revokeObjectURL(current[role]!.url);
      const next = { ...current };
      delete next[role];
      return next;
    });
    if (role === 'front') {
      resetMesh();
      setBuild(createEmptyBrickBuild());
      setStep(0);
      setOpenStep(null);
      setError('');
      setProcessing(false);
      setPlaying(false);
      setExplosion(0);
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
      ...build.bom.map(item => [
        item.partId,
        `${item.width}x${item.depth ?? 1}`,
        locale === 'zh' ? item.colorNameZh : item.colorNameEn,
        String(item.colorCode),
        String(item.quantity),
      ]),
    ];
    download(rows.map(row => row.map(value => `"${value.replaceAll('"', '""')}"`).join(',')).join('\n'), `${build.name}-bom.csv`, 'text/csv;charset=utf-8');
  }

  const cloudBusy = ['connecting', 'uploading', 'queued', 'generating', 'downloading', 'parsing']
    .includes(meshStatus);
  const meshStatusLabel: Record<MeshStatus, string> = {
    idle: tr('等待生成真实网格', 'Ready to generate a real mesh'),
    connecting: tr('连接公开三维服务', 'Connecting to public 3D service'),
    uploading: tr('上传处理后的正面照片', 'Uploading the processed front photo'),
    queued: tr('等待公共 GPU', 'Waiting for public GPU'),
    generating: tr('生成三维网格', 'Generating the 3D mesh'),
    downloading: tr('下载 GLB 网格', 'Downloading the GLB mesh'),
    parsing: tr('解析三角网格', 'Parsing triangle mesh'),
    voxelizing: tr('将网格体素化并打包积木', 'Voxelizing and packing the mesh'),
    ready: tr('真实三维网格已转换', 'Real 3D mesh converted'),
    error: tr('三维网格生成失败', '3D mesh generation failed'),
  };

  return <section className="image-studio" aria-label={tr('图片转积木工作台', 'Image to brick studio')}>
    <aside className="image-studio-controls">
      <div className="creator-title">
        <span className="eyebrow">PHOTO TO 3D BRICKS</span>
        <h1>{tr('真实物体重建', 'Real-object reconstruction')}</h1>
        <p>{reconstructionMode === 'mesh'
          ? tr('先生成真实 GLB 三维网格，再将网格体素化为积木。', 'Generate a real GLB mesh first, then voxelize it into bricks.')
          : tr('本地深度或多视图轮廓重建，不会生成真实网格。', 'Local depth or multi-view silhouette reconstruction; no real mesh is generated.')}</p>
      </div>
      <div className="creator-reconstruction-tabs" role="tablist" aria-label={tr('重建引擎', 'Reconstruction engine')}>
        <button
          role="tab"
          aria-selected={reconstructionMode === 'mesh'}
          onClick={() => {
            setReconstructionMode('mesh');
            setStageMode(meshResult ? 'mesh' : 'bricks');
            setError('');
            if (options.method === 'relief') setOptions(value => ({ ...value, method: 'hollow' }));
            if (!meshData) setBuild(createEmptyBrickBuild());
          }}
        ><Cloud size={15} />{tr('公开 AI 网格', 'Public AI mesh')}</button>
        <button
          role="tab"
          aria-selected={reconstructionMode === 'local'}
          onClick={() => {
            setReconstructionMode('local');
            setStageMode('bricks');
            setBuild(createEmptyBrickBuild());
            setError('');
          }}
        ><Cpu size={15} />{tr('本地备用', 'Local fallback')}</button>
      </div>
      <div className="crop-source-list">
        {(reconstructionMode === 'mesh' ? roles.slice(0, 1) : roles).map(role => <ImageCropEditor
          key={role}
          role={role}
          source={sources[role]}
          onFile={file => acceptFile(role, file)}
          onCrop={crop => updateCrop(role, crop)}
          onFit={fit => updateFit(role, fit)}
          onRemove={() => removeSource(role)}
          tr={tr}
        />)}
      </div>
      {reconstructionMode === 'mesh' && <section className="creator-cloud-panel">
        <label>{tr('公开服务', 'Public provider')}<select
          aria-label={tr('公开三维服务', 'Public 3D provider')}
          value={meshProvider}
          disabled={cloudBusy}
          onChange={event => {
            resetMesh();
            setBuild(createEmptyBrickBuild());
            setMeshProvider(event.target.value as CloudMeshProvider);
          }}
        >
          <option value="triposr-cpu">Hugging Face · TripoSR Public CPU</option>
          <option value="triposr">Hugging Face · TripoSR Official ZeroGPU</option>
          <option value="stable-fast-3d">Hugging Face · Stable Fast 3D</option>
        </select></label>
        <label>{tr('HF Token（可选）', 'HF token (optional)')}<input
          aria-label={tr('临时 Hugging Face Token', 'Temporary Hugging Face token')}
          type="password"
          autoComplete="off"
          placeholder="hf_..."
          value={hfToken}
          onChange={event => setHfToken(event.target.value)}
        /></label>
        <button
          className="creator-cloud-generate"
          data-brick-effect="shatter"
          disabled={!sources.front || meshStatus === 'voxelizing'}
          onClick={() => {
            if (cloudBusy) {
              meshAbortRef.current?.abort();
              setMeshStatus('idle');
              setMeshDetail('');
              setProcessing(false);
            } else void generateCloudMesh();
          }}
        >{cloudBusy ? <X size={16} /> : <Triangle size={16} />}{cloudBusy
          ? tr('取消生成', 'Cancel generation')
          : meshResult
            ? tr('重新生成三维网格', 'Regenerate 3D mesh')
            : tr('生成真实三维网格', 'Generate real 3D mesh')}</button>
        <small>{tr(
          '照片将发送到所选公开 Hugging Face Space。Token 仅保存在当前页面内存中。',
          'The photo is sent to the selected public Hugging Face Space. A token stays only in this page memory.',
        )}</small>
      </section>}
      <div className="image-option-selects">
        <label>{tr('生成方法', 'Generation method')}<select aria-label={tr('生成方法', 'Generation method')} value={options.method} onChange={event => setOptions(value => ({ ...value, method: event.target.value as ImageBrickOptions['method'] }))}>
          <option value="hollow">{tr('空心外壳', 'Hollow sculpture')}</option>
          <option value="solid">{tr('立体实体', 'Solid sculpture')}</option>
          {reconstructionMode === 'local' && <option value="relief">{tr('浅浮雕', 'Low-profile relief')}</option>}
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
        {reconstructionMode === 'local' && <label><span>{tr('模型厚度', 'Model depth')}<b>{options.maxDepth}</b></span><input aria-label={tr('模型厚度', 'Model depth')} type="range" min={4} max={32} step={2} value={options.maxDepth} onChange={event => setOptions(value => ({ ...value, maxDepth: Number(event.target.value) }))} /></label>}
        <label><span>{tr('颜色数量', 'Color count')}<b>{options.maxColors}</b></span><input aria-label={tr('颜色数量', 'Color count')} type="range" min={4} max={18} value={options.maxColors} onChange={event => setOptions(value => ({ ...value, maxColors: Number(event.target.value) }))} /></label>
        {reconstructionMode === 'local' && <label><span>{tr('背景阈值', 'Background threshold')}<b>{options.backgroundThreshold}</b></span><input aria-label={tr('背景阈值', 'Background threshold')} type="range" min={4} max={42} value={options.backgroundThreshold} disabled={!options.removeBackground} onChange={event => setOptions(value => ({ ...value, backgroundThreshold: Number(event.target.value) }))} /></label>}
      </div>
      {reconstructionMode === 'local' && <label className="creator-check"><input type="checkbox" checked={options.removeBackground} onChange={event => setOptions(value => ({ ...value, removeBackground: event.target.checked }))} /><span>{tr('移除近似背景', 'Remove similar background')}</span></label>}
      <div className="image-build-stats">
        <div><strong>{brickCount}</strong><span>{tr('积木', 'Bricks')}</span></div>
        <div><strong>{build.steps.length}</strong><span>{tr('步骤', 'Steps')}</span></div>
        <div><strong>{colorCount}</strong><span>{tr('颜色', 'Colors')}</span></div>
        <div><strong>{reconstructionMode === 'mesh'
          ? meshData?.sampledTriangleCount.toLocaleString(locale === 'zh' ? 'zh-CN' : 'en-US') ?? 0
          : build.viewCount}</strong><span>{reconstructionMode === 'mesh' ? tr('三角面', 'Triangles') : tr('视图', 'Views')}</span></div>
      </div>
      {sources.front && reconstructionMode === 'local' && <div className={`creator-depth-state ${depthState.status}`}>
        <Cpu size={15} />
        <span>
          <strong>{depthState.status === 'ready'
            ? tr('AI 深度已应用', 'AI depth applied')
            : depthState.status === 'fallback'
              ? tr('几何回退已应用', 'Geometry fallback applied')
              : depthState.phase === 'depth'
                ? tr('正在估计真实深度', 'Estimating object depth')
                : tr('正在载入深度模型', 'Loading depth model')}</strong>
          <small>{tr(`${viewCount} / 4 个视角`, `${viewCount} / 4 views`)}</small>
        </span>
      </div>}
      {sources.front && reconstructionMode === 'mesh' && <div className={`creator-depth-state mesh-${meshStatus}`}>
        <Cloud size={15} />
        <span><strong>{meshStatusLabel[meshStatus]}</strong><small>{meshDetail || meshResult?.providerName || tr('尚未调用公开服务', 'Public service not called yet')}</small></span>
      </div>}
      {sources.front && !error && build.sourceWidth > 0 && build.sourceWidth < options.width && <div className="creator-status">{tr(`为满足 ${options.brickBudget} 块预算，分辨率自动调整为 ${build.sourceWidth}`, `Resolution adjusted to ${build.sourceWidth} to fit the ${options.brickBudget}-brick budget`)}</div>}
      {processing && reconstructionMode === 'local' && <div className="creator-status" role="status">{tr('正在融合视图并生成积木模型…', 'Fusing views and generating the brick model...')}</div>}
      {error && <div className="creator-error" role="alert">{error}</div>}
      <div className="creator-export-row">
        {meshResult && <button data-brick-effect="shatter" onClick={() => downloadBlob(meshResult.blob, `${build.name || 'image-mesh'}.glb`)}><FileDown size={15} />GLB</button>}
        <button data-brick-effect="shatter" disabled={!brickCount} onClick={exportBom}><ArrowDownToLine size={15} />BOM CSV</button>
        <button data-brick-effect="shatter" disabled={!brickCount} onClick={() => download(imageBrickBuildToLdraw(build), `${build.name}.ldr`, 'text/plain;charset=utf-8')}><ArrowDownToLine size={15} />LDraw</button>
      </div>
    </aside>

    <main className="image-studio-stage">
      <div className="image-stage-heading">
        <div><span className="eyebrow">{sources.front ? tr('照片重建', 'Photo reconstruction') : tr('等待输入', 'Awaiting input')}</span><strong>{build.name || sources.front?.file.name || tr('上传真实物体照片', 'Upload a real-object photo')}</strong></div>
        {meshResult && <div className="image-stage-tabs" role="tablist" aria-label={tr('三维阶段', '3D stage')}>
          <button role="tab" aria-selected={stageMode === 'mesh'} onClick={() => setStageMode('mesh')}>
            <Triangle size={14} />{tr('原始网格', 'Source mesh')}
          </button>
          <button role="tab" aria-selected={stageMode === 'bricks'} onClick={() => setStageMode('bricks')}>
            <Box size={14} />{tr('积木模型', 'Brick model')}
          </button>
        </div>}
      </div>
      <div className={`image-brick-canvas ${stageMode === 'bricks' ? '' : 'stage-hidden'}`} ref={hostRef} />
      <div className={`image-mesh-canvas ${stageMode === 'mesh' ? '' : 'stage-hidden'}`} ref={meshHostRef} />
      {!sources.front && <div className="image-empty-state">
        <ImagePlus size={34} />
        <strong>{tr('从真实照片开始', 'Start with a real photo')}</strong>
        <span>{tr('正面照片必需', 'Front view required')}</span>
      </div>}
      {sources.front && reconstructionMode === 'mesh' && !meshResult && !cloudBusy && <div className="image-empty-state">
        <Triangle size={34} />
        <strong>{tr('照片已就绪', 'Photo ready')}</strong>
        <span>{tr('点击“生成真实三维网格”开始两阶段转换', 'Generate the real 3D mesh to start the two-stage conversion')}</span>
      </div>}
      {sources.front && reconstructionMode === 'mesh' && !meshResult && cloudBusy && <div className="image-empty-state image-cloud-progress" role="status">
        <Cloud size={34} />
        <strong>{meshStatusLabel[meshStatus]}</strong>
        <span>{meshDetail || tr('公共 GPU 可能需要排队', 'The public GPU may have a queue')}</span>
      </div>}
      {stageMode === 'mesh' && meshResult && <div className="image-mesh-badge">
        <Triangle size={14} />
        <strong>{meshResult.providerName}</strong>
        <span>{meshData?.triangleCount.toLocaleString(locale === 'zh' ? 'zh-CN' : 'en-US')} {tr('原始三角面', 'source triangles')}</span>
      </div>}
      {stageMode === 'bricks' && <div className="image-viewport-toolbar" aria-label={tr('视角工具', 'View tools')}>
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
        <IconButton label={tr('适配全部可见积木', 'Fit visible bricks')} disabled={!brickCount} onClick={() => sceneRef.current?.fitVisible()}><Expand size={17} /></IconButton>
      </div>}
      {stageMode === 'bricks' && <div className="image-zoom-tools">
        <IconButton label={tr('放大模型', 'Zoom in')} onClick={() => sceneRef.current?.zoom(0.8)}><Plus size={17} /></IconButton>
        <IconButton label={tr('缩小模型', 'Zoom out')} onClick={() => sceneRef.current?.zoom(1.25)}><Minus size={17} /></IconButton>
        <IconButton label={tr('复原模型', 'Reset model')} onClick={() => {
          setExplosion(0);
          setAutoRotate(false);
          setPanMode(false);
          setView('perspective');
          sceneRef.current?.fitVisible();
        }}><RotateCcw size={17} /></IconButton>
      </div>}
      {stageMode === 'bricks' && <section className="image-build-dock" aria-label={tr('拼装步骤控制', 'Build step controls')}>
        <div className="dock-heading"><div><BookOpen size={17} /><strong>{currentStep ? tr(`第 ${step} 步`, `Step ${step}`) : tr('准备拼装', 'Ready to build')}</strong><span className="phase-name">{reconstructionLabel}</span></div><output>{step}<span> / {build.steps.length}</span></output></div>
        <div className="step-controls">
          <IconButton label={tr('回到开始', 'Restart')} disabled={step === 0} onClick={() => setBuildStep(0)}><SkipBack size={16} /></IconButton>
          <IconButton label={tr('上一步', 'Previous step')} disabled={step === 0} onClick={() => setBuildStep(step - 1)}><ArrowLeft size={17} /></IconButton>
          <IconButton label={playing ? tr('暂停拼装', 'Pause build') : tr('播放拼装', 'Play build')} active={playing} disabled={step === build.steps.length} onClick={() => setPlaying(value => !value)}>{playing ? <Pause size={17} /> : <Play size={17} />}</IconButton>
          <input aria-label={tr('当前拼装步骤', 'Current build step')} type="range" min={0} max={build.steps.length} value={step} onChange={event => setBuildStep(Number(event.target.value))} style={{ '--range-fill': `${build.steps.length ? step / build.steps.length * 100 : 0}%` } as React.CSSProperties} />
          <IconButton label={tr('下一步', 'Next step')} disabled={step === build.steps.length} onClick={() => setBuildStep(step + 1)}><ArrowRight size={17} /></IconButton>
          <IconButton label={tr('完成模型', 'Complete model')} disabled={step === build.steps.length} onClick={() => setBuildStep(build.steps.length)}><SkipForward size={16} /></IconButton>
        </div>
        <div className="image-explode-row"><Layers3 size={15} /><span>{tr('拆分', 'Explode')}</span><input aria-label={tr('拆分程度', 'Explosion')} type="range" min={0} max={100} value={Math.round(explosion * 100)} onChange={event => setExplosion(Number(event.target.value) / 100)} /><output>{Math.round(explosion * 100)}%</output></div>
      </section>}
    </main>

    <aside className="image-studio-results">
      <div className="image-result-tabs" role="tablist" aria-label={tr('生成结果', 'Generated result')}>
        <button role="tab" aria-selected={activePanel === 'parts'} onClick={() => setActivePanel('parts')}>{tr('材料清单', 'Materials')}</button>
        <button role="tab" aria-selected={activePanel === 'steps'} onClick={() => setActivePanel('steps')}>{tr('拼装步骤', 'Build steps')}</button>
      </div>
      <div className="image-result-scroll">
        {activePanel === 'parts'
          ? build.bom.map(item => <div className="image-bom-row" key={item.key}><i style={{ background: item.colorHex }} /><span><strong>Brick {item.width} × {item.depth ?? 1}</strong><small>{locale === 'zh' ? item.colorNameZh : item.colorNameEn} · {item.partId}</small></span><b>× {item.quantity}</b></div>)
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
        {!build.bricks.length && <div className="image-results-empty">
          <Box size={28} />
          <span>{tr('材料与步骤将在重建后出现', 'Materials and steps appear after reconstruction')}</span>
        </div>}
      </div>
      <div className="image-current-step">
        <span>{tr('本步零件', 'Current step')}</span>
        <strong>{currentStep?.brickIds.length ?? 0}</strong>
        <div>{currentParts.slice(0, 7).map(item => <i key={item.key} title={`${locale === 'zh' ? item.colorNameZh : item.colorNameEn} × ${item.quantity}`} style={{ background: item.colorHex }} />)}</div>
      </div>
    </aside>
  </section>;
}
