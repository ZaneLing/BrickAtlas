import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowLeft, ArrowRight, Box, Check, CheckCircle2, ChevronRight, CircleAlert,
  Crosshair, Hand, Languages, Library, LoaderCircle, LockKeyhole, Play, Pause,
  Rotate3D, RotateCcw, RotateCw, Save, Sparkles, Trophy, Undo2,
} from 'lucide-react';
import { modelCatalog, type ModelConfig } from '../../atlas.config';
import { groupStepParts } from '../instructions/exportGuide';
import { BrickModel } from '../model/BrickModel';
import {
  initialState, type AssemblyStep, type AtlasManifest, type ExplorerState,
} from '../model/types';
import { AtlasScene, type ManualAssemblyPlacement } from '../scene/AtlasScene';
import { PartPreviewScene, type PartPreviewData } from '../scene/PartPreview';
import { BrickAtlasMark } from '../ui/BrickAtlasMark';
import { IconButton, Modal } from '../ui/Controls';
import { CatalogFilters } from '../ui/CatalogFilters';
import { defaultCatalogFilter, filterCatalog, readFavorites } from '../app/catalog';
import type { Locale, Translator } from '../app/locale';
import {
  assemblyDifficulty, difficultyLabel, type AssemblyDifficulty,
} from './difficulty';
import {
  auditAssemblyStep, type QuarterTurn,
} from './orientation';
import {
  clearModelAssemblyProgress, completedAssemblyModels, readModelAssemblyProgress,
  saveModelAssemblyProgress, readAssemblyProgress,
} from './progress';

declare global {
  interface Window {
    __assemblyGame?: () => {
      modelId: string;
      ready: boolean;
      completedStep: number;
      activeStep: number;
      placed: number;
      required: number;
      completed: boolean;
      advancing: boolean;
      feedback: 'idle' | 'correct' | 'wrong';
      review: 'idle' | 'passed' | 'failed';
      selectedTurn: QuarterTurn | null;
      heldId: string | null;
      positions: number;
      scene: ReturnType<AtlasScene['snapshot']> | null;
    };
  }
}

type MaterialPayload = {
  step: number;
  kind: 'part' | 'assembly';
  key: string;
  turn: QuarterTurn;
  instanceId?: string;
};

type GuideMedia = {
  step: number;
  frames: string[];
};

const payloadType = 'application/x-brick-atlas-material';
const GUIDE_FPS = 24;
const GUIDE_FRAME_COUNT = 24;
const GUIDE_FRAME_INTERVAL = 1000 / GUIDE_FPS;

function DifficultyStuds({
  difficulty,
  locale,
}: {
  difficulty: AssemblyDifficulty;
  locale: Locale;
}) {
  return <span
    className="assembly-difficulty"
    role="img"
    aria-label={`${difficulty} / 5 · ${difficultyLabel(difficulty, locale)}`}
    title={`${difficulty} / 5 · ${difficultyLabel(difficulty, locale)}`}
  >
    {Array.from({ length: 5 }, (_, index) =>
      <i className={index < difficulty ? 'filled' : ''} key={index} />,
    )}
  </span>;
}

function modelProgressPercent(completedStep: number, total: number) {
  return total ? Math.round(completedStep / total * 100) : 0;
}

function stepIds(step?: AssemblyStep) {
  if (!step) return [];
  return step.kind === 'placement'
    ? step.motionInstanceIds ?? []
    : step.instanceIds;
}

function stepTitle(
  step: AssemblyStep,
  number: number,
  locale: Locale,
) {
  if (locale === 'zh') return step.title;
  return step.kind === 'placement'
    ? `Place subassembly · Step ${number}`
    : `Add bricks · Step ${number}`;
}

function payload(event: React.DragEvent): MaterialPayload | null {
  try {
    return JSON.parse(event.dataTransfer.getData(payloadType)) as MaterialPayload;
  } catch {
    return null;
  }
}

function languageButton(
  locale: Locale,
  toggleLocale: () => void,
  tr: Translator,
) {
  return <button
    className="language-button"
    onClick={toggleLocale}
    aria-label={tr('切换为英文', 'Switch to Chinese')}
    title={tr('切换为英文', 'Switch to Chinese')}
  >
    <Languages size={14} />
    <span>{locale === 'zh' ? 'EN' : '中'}</span>
  </button>;
}

function AssemblyPartThumbnail({
  data,
  label,
  turn,
}: {
  data: PartPreviewData | null;
  label: string;
  turn: QuarterTurn;
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !data?.positions.length) return;
    const width = 112;
    const height = 80;
    const ratio = Math.min(2, devicePixelRatio);
    canvas.width = width * ratio;
    canvas.height = height * ratio;
    const context = canvas.getContext('2d');
    if (!context) return;
    context.scale(ratio, ratio);
    context.clearRect(0, 0, width, height);
    const source = data.positions;
    const min = [Infinity, Infinity, Infinity];
    const max = [-Infinity, -Infinity, -Infinity];
    for (let index = 0; index < source.length; index += 3) {
      for (let axis = 0; axis < 3; axis++) {
        min[axis] = Math.min(min[axis], source[index + axis]);
        max[axis] = Math.max(max[axis], source[index + axis]);
      }
    }
    const center = min.map((value, axis) => (value + max[axis]) / 2);
    const angle = -Math.PI / 4 + turn * Math.PI / 2;
    const cosine = Math.cos(angle);
    const sine = Math.sin(angle);
    const project = (offset: number) => {
      const x = source[offset] - center[0];
      const y = source[offset + 1] - center[1];
      const z = source[offset + 2] - center[2];
      const rx = x * cosine - z * sine;
      const rz = x * sine + z * cosine;
      return { x: rx, y: -y * 0.88 + rz * 0.34, depth: rz + y * 0.08 };
    };
    const triangles = Array.from({ length: source.length / 9 }, (_, triangle) => {
      const points = [0, 3, 6].map(corner => project(triangle * 9 + corner));
      const ax = points[1].x - points[0].x;
      const ay = points[1].y - points[0].y;
      const bx = points[2].x - points[0].x;
      const by = points[2].y - points[0].y;
      return {
        points,
        depth: points.reduce((sum, point) => sum + point.depth, 0) / 3,
        light: 0.62 + Math.min(0.35, Math.abs(ax * by - ay * bx) * 0.002),
      };
    }).sort((a, b) => a.depth - b.depth);
    const projected = triangles.flatMap(triangle => triangle.points);
    const bounds = {
      minX: Math.min(...projected.map(point => point.x)),
      maxX: Math.max(...projected.map(point => point.x)),
      minY: Math.min(...projected.map(point => point.y)),
      maxY: Math.max(...projected.map(point => point.y)),
    };
    const scale = Math.min(
      (width - 12) / Math.max(1e-6, bounds.maxX - bounds.minX),
      (height - 12) / Math.max(1e-6, bounds.maxY - bounds.minY),
    );
    const offsetX = width / 2 - (bounds.minX + bounds.maxX) / 2 * scale;
    const offsetY = height / 2 - (bounds.minY + bounds.maxY) / 2 * scale;
    const rgb = [1, 3, 5].map(index => Number.parseInt(data.color.slice(index, index + 2), 16));
    for (const triangle of triangles) {
      context.beginPath();
      triangle.points.forEach((point, index) => {
        const x = point.x * scale + offsetX;
        const y = point.y * scale + offsetY;
        if (index) context.lineTo(x, y);
        else context.moveTo(x, y);
      });
      context.closePath();
      context.fillStyle = `rgb(${rgb.map(channel => Math.round(channel * triangle.light)).join(' ')})`;
      context.fill();
      context.strokeStyle = '#24314942';
      context.lineWidth = 0.55;
      context.stroke();
    }
  }, [data, turn]);
  return <canvas
    className="assembly-part-thumbnail"
    ref={canvasRef}
    role="img"
    aria-label={label}
  />;
}

function AssemblyMaterialInspector({
  data,
  label,
}: {
  data: PartPreviewData | null;
  label: string;
}) {
  const hostRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!hostRef.current || !data) return;
    const preview = new PartPreviewScene(hostRef.current, data, label);
    return () => preview.dispose();
  }, [data, label]);
  return <div className="assembly-material-inspector" ref={hostRef}>
    {!data && <LoaderCircle className="spinner" size={18} />}
  </div>;
}

function AssemblyGuideLoop({
  media,
  playing,
  loading,
  step,
  tr,
}: {
  media: GuideMedia | null;
  playing: boolean;
  loading: boolean;
  step: number;
  tr: Translator;
}) {
  const imageRef = useRef<HTMLImageElement>(null);
  const frameRef = useRef(0);
  useEffect(() => {
    frameRef.current = 0;
    if (imageRef.current && media?.frames.length) imageRef.current.src = media.frames[0];
  }, [media]);
  useEffect(() => {
    if (!media?.frames.length || !playing) return;
    const timer = window.setInterval(() => {
      if (document.hidden || !imageRef.current) return;
      frameRef.current = (frameRef.current + 1) % media.frames.length;
      imageRef.current.src = media.frames[frameRef.current];
    }, GUIDE_FRAME_INTERVAL);
    return () => clearInterval(timer);
  }, [media, playing]);
  return media?.step === step && media.frames.length
    ? <img ref={imageRef} src={media.frames[0]} alt={tr(`第 ${step} 步动画`, `Step ${step} animation`)} />
    : <><LoaderCircle className="spinner" size={24} /><span>{loading ? tr('生成清晰动画', 'Rendering clear animation') : tr('等待模型', 'Waiting for model')}</span></>;
}

export function AssemblyGameHub({
  locale,
  tr,
  toggleLocale,
}: {
  locale: Locale;
  tr: Translator;
  toggleLocale: () => void;
}) {
  const [progressMap] = useState(readAssemblyProgress);
  const [filter, setFilter] = useState(defaultCatalogFilter);
  const [favorites] = useState(readFavorites);
  const completed = completedAssemblyModels();
  const models = filterCatalog(modelCatalog, filter, favorites, progressMap);
  return <div className="assembly-hub catalog-page">
    <header className="topbar">
      <a href={import.meta.env.BASE_URL} className="brand">
        <span className="brand-mark"><BrickAtlasMark /></span>
        <strong>BRICK<span>ATLAS</span></strong>
      </a>
      <div className="top-divider" />
      <span className="workspace-label">{tr('线上拼装空间', 'Assembly game')}</span>
      <nav className="top-actions">
        <a className="text-button" href={import.meta.env.BASE_URL}>
          <Library size={16} />{tr('项目库', 'Library')}
        </a>
        {languageButton(locale, toggleLocale, tr)}
      </nav>
    </header>
    <main className="assembly-hub-main">
      <section className="assembly-hub-heading">
        <div>
          <span className="eyebrow">BUILD IT YOURSELF</span>
          <h1>{tr('选择一个模型开始挑战', 'Choose a model to assemble')}</h1>
        </div>
        <div className="assembly-hub-completion">
          <Trophy size={24} />
          <strong>{completed.size}</strong>
          <span>{tr('已完成', 'completed')}</span>
        </div>
      </section>
      <CatalogFilters filter={filter} onChange={setFilter} count={models.length} locale={locale} tr={tr} />
      {!models.length && <p className="catalog-empty">{tr('没有符合条件的模型', 'No matching models')}</p>}
      <section className="assembly-model-grid" aria-label={tr('拼装模型列表', 'Assembly model list')}>
        {models.map(model => {
          const difficulty = assemblyDifficulty(model.id);
          const done = completed.has(model.id);
          return <a
            className={`assembly-model-card ${done ? 'completed' : ''}`}
            href={`${import.meta.env.BASE_URL}assemble/${model.id}`}
            key={model.id}
          >
            <div className="assembly-model-art">
              <img src={`${import.meta.env.BASE_URL}models/${model.id}/preview.png`} alt="" />
              {done && <span className="assembly-complete-mark">
                <CheckCircle2 size={31} />
                {tr('已完成', 'Completed')}
              </span>}
            </div>
            <div>
              <span className="eyebrow">{model.setNumber} · {model.year}</span>
              <h2>{locale === 'zh' ? model.subtitle : model.title}</h2>
              <p>{model.theme}{!done && progressMap[model.id] && ` · ${tr(`已完成 ${progressMap[model.id].completedStep} 步`, `${progressMap[model.id].completedStep} steps complete`)}`}</p>
              <footer>
                <DifficultyStuds difficulty={difficulty} locale={locale} />
                <span>{difficultyLabel(difficulty, locale)}</span>
                <ChevronRight size={17} />
              </footer>
            </div>
          </a>;
        })}
      </section>
    </main>
  </div>;
}

export function AssemblyGame({
  config,
  locale,
  tr,
  toggleLocale,
}: {
  config: ModelConfig;
  locale: Locale;
  tr: Translator;
  toggleLocale: () => void;
}) {
  const base = `${import.meta.env.BASE_URL}models/${config.id}/`;
  const stageRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<AtlasScene | null>(null);
  const advanceTimer = useRef<number | null>(null);
  const appliedView = useRef<ExplorerState['view']>('perspective');
  const initialFocusDone = useRef(false);
  const [manifest, setManifest] = useState<AtlasManifest | null>(null);
  const [loading, setLoading] = useState(true);
  const [ready, setReady] = useState(false);
  const [error, setError] = useState('');
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState(tr('读取模型', 'Loading model'));
  const [completedStep, setCompletedStep] = useState(0);
  const [placedIds, setPlacedIds] = useState<string[]>([]);
  const [placedTurns, setPlacedTurns] = useState<Record<string, QuarterTurn>>({});
  const [placedPositions, setPlacedPositions] = useState<Record<string, [number, number, number]>>({});
  const [completed, setCompleted] = useState(false);
  const [previewStep, setPreviewStep] = useState(1);
  const [selectedMaterial, setSelectedMaterial] = useState<MaterialPayload | null>(null);
  const [feedback, setFeedback] = useState<'idle' | 'correct' | 'wrong'>('idle');
  const [review, setReview] = useState<'idle' | 'passed' | 'failed'>('idle');
  const [notice, setNotice] = useState('');
  const [advancing, setAdvancing] = useState(false);
  const [placementAnimating, setPlacementAnimating] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const [view, setView] = useState<ExplorerState['view']>('perspective');
  const [panMode, setPanMode] = useState(false);
  const [guideMedia, setGuideMedia] = useState<GuideMedia | null>(null);
  const [guideLoading, setGuideLoading] = useState(false);
  const [guidePlaying, setGuidePlaying] = useState(() => !matchMedia('(prefers-reduced-motion: reduce)').matches);
  const [resetOpen, setResetOpen] = useState(false);
  const [storageError, setStorageError] = useState(false);
  const pointerPlacement = useRef<[number, number, number] | null>(null);
  const pointerClient = useRef<[number, number] | null>(null);

  const steps = manifest?.instructions?.steps ?? [];
  const activeStepNumber = completed ? steps.length : Math.min(completedStep + 1, steps.length);
  const activeStep = steps[activeStepNumber - 1];
  const activeIds = useMemo(() => stepIds(activeStep), [activeStep]);
  const activeParts = useMemo(() => {
    if (!manifest || !activeStep || activeStep.kind === 'placement') return [];
    const ids = new Set(activeStep.instanceIds);
    return manifest.instances.filter(part => ids.has(part.instanceId));
  }, [manifest, activeStep]);
  const preview = steps[Math.max(0, previewStep - 1)];
  const previewParts = useMemo(() => {
    if (!manifest || !preview || preview.kind === 'placement') return [];
    const ids = new Set(preview.instanceIds);
    return manifest.instances.filter(part => ids.has(part.instanceId));
  }, [manifest, preview]);
  const previewGroups = useMemo(() => groupStepParts(previewParts), [previewParts]);
  const previewGeometry = useMemo(() => new Map(
    previewGroups.map(group => [
      group.key,
      sceneRef.current?.getPartPreview(group.instanceIds[0]) ?? null,
    ]),
  ), [previewGroups, ready]);
  const placed = useMemo(() => new Set(placedIds), [placedIds]);
  const difficulty = assemblyDifficulty(config.id);
  const percent = modelProgressPercent(completedStep, steps.length);

  useEffect(() => {
    const abort = new AbortController();
    setLoading(true);
    setReady(false);
    initialFocusDone.current = false;
    setError('');
    fetch(`${base}manifest.json`, { signal: abort.signal })
      .then(async response => {
        if (!response.ok) throw new Error(`manifest.json: HTTP ${response.status}`);
        const next = await response.json() as AtlasManifest;
        if (!next.instructions?.steps.length) throw new Error(tr('模型没有拼装步骤', 'Model has no assembly steps'));
        const saved = readModelAssemblyProgress(config.id);
        if (abort.signal.aborted) return;
        const clamped = saved.completedStep <= next.instructions.steps.length ? saved.completedStep : 0;
        const currentIds = new Set(stepIds(next.instructions.steps[clamped]));
        const restoredIds = saved.placedIds.filter(id => currentIds.has(id));
        const byId = new Map(next.instances.map(part => [part.instanceId, part]));
        setCompletedStep(clamped);
        setPlacedIds(restoredIds);
        setPlacedTurns(Object.fromEntries(restoredIds.map(id => [
          id,
          saved.placedPositions?.[id] ? saved.placedTurns?.[id] ?? 0 : 0,
        ])));
        setPlacedPositions(Object.fromEntries(restoredIds.flatMap(id => {
          const part = byId.get(id);
          if (!part) return [];
          return [[id, saved.placedPositions?.[id] ?? [0, 1, 2].map(axis =>
            (part.bounds.min[axis] + part.bounds.max[axis]) / 2) as [number, number, number]]];
        })));
        setCompleted(clamped === next.instructions.steps.length);
        setPreviewStep(Math.min(clamped + 1, next.instructions.steps.length));
        setManifest(next);
      })
      .catch(cause => {
        if (!abort.signal.aborted) {
          setError(cause instanceof Error ? cause.message : String(cause));
          setLoading(false);
        }
      });
    return () => abort.abort();
  }, [base, config.id, tr]);

  const brickModel = useMemo(() => manifest ? new BrickModel(manifest) : null, [manifest]);
  useEffect(() => {
    if (!brickModel || !stageRef.current) return;
    let scene: AtlasScene | null = null;
    try {
      scene = new AtlasScene(stageRef.current, brickModel, {
        progress: (value, label) => {
          setProgress(value);
          setStage(label);
        },
        ready: () => {
          setReady(true);
          setLoading(false);
        },
        error: message => {
          setError(message);
          setLoading(false);
        },
        select: () => {},
        hover: () => {},
      }, locale);
      sceneRef.current = scene;
      appliedView.current = 'perspective';
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause));
      setLoading(false);
    }
    return () => {
      scene?.dispose();
      sceneRef.current = null;
    };
  }, [brickModel]);

  useEffect(() => {
    sceneRef.current?.setLocale(locale);
  }, [locale]);

  useEffect(() => {
    sceneRef.current?.setPanMode(panMode);
  }, [panMode, ready]);

  useEffect(() => {
    const placements = Object.fromEntries(placedIds.flatMap(id => {
      const position = placedPositions[id];
      if (!position) return [];
      return [[id, {
        position,
        turn: placedTurns[id] ?? 0,
      } satisfies ManualAssemblyPlacement]];
    }));
    sceneRef.current?.setManualAssemblyPlacements(placements);
  }, [placedIds, placedPositions, placedTurns, ready]);

  useEffect(() => {
    const selected = selectedMaterial?.kind === 'part'
      && selectedMaterial.step === activeStepNumber
      && selectedMaterial.instanceId
      ? selectedMaterial
      : null;
    sceneRef.current?.setAssemblyPlacementMode(Boolean(selected));
    if (!selected) {
      pointerPlacement.current = null;
      pointerClient.current = null;
      sceneRef.current?.clearManualAssemblyPreview();
      return;
    }
    const pointer = pointerClient.current;
    if (pointer) {
      pointerPlacement.current = sceneRef.current?.previewManualAssembly(
        selected.instanceId!,
        pointer[0],
        pointer[1],
        selected.turn,
      ) ?? null;
    }
  }, [selectedMaterial, activeStepNumber, ready]);

  useEffect(() => {
    if (!manifest || !steps.length) return;
    const ghostBrickIds = !completed && activeStep?.kind !== 'placement'
      ? activeIds
      : [];
    const buildStep = completed
      ? steps.length
      : activeStep?.kind === 'placement' && !placementAnimating
        ? completedStep
        : activeStepNumber;
    const preserveCamera = appliedView.current === view;
    sceneRef.current?.setState({
      ...initialState,
      buildStep,
      ghostBrickIds,
      view,
      grid: false,
      edges: true,
      highlightStep: false,
      assemblyRevision: completedStep * 1000 + Number(placementAnimating),
    }, {
      preserveCamera,
      animateAssembly: activeStep?.kind === 'placement' && placementAnimating,
    });
    appliedView.current = view;
    if (!preserveCamera && activeStepNumber > 0) {
      requestAnimationFrame(() => sceneRef.current?.focusBuildStep(activeStepNumber));
    }
  }, [
    manifest, steps.length, completed, activeStep, activeIds, activeStepNumber,
    completedStep, placed, placedIds.length, placementAnimating, view,
  ]);

  useEffect(() => {
    if (!ready || initialFocusDone.current || !activeStepNumber) return;
    initialFocusDone.current = true;
    requestAnimationFrame(() => sceneRef.current?.focusBuildStep(activeStepNumber));
  }, [ready, activeStepNumber]);

  useEffect(() => {
    window.__assemblyGame = () => ({
      modelId: config.id,
      ready,
      completedStep,
      activeStep: activeStepNumber,
      placed: placedIds.length,
      required: activeStep?.kind === 'placement' ? 1 : activeIds.length,
      completed,
      advancing,
      feedback,
      review,
      selectedTurn: selectedMaterial?.turn ?? null,
      heldId: selectedMaterial?.instanceId ?? null,
      positions: Object.keys(placedPositions).length,
      scene: sceneRef.current?.snapshot() ?? null,
    });
    return () => {
      delete window.__assemblyGame;
    };
  }, [
    config.id, ready, completedStep, activeStepNumber, placedIds.length,
    activeStep, activeIds.length, completed, advancing, feedback, review,
    selectedMaterial, placedPositions,
  ]);

  useEffect(() => () => {
    if (advanceTimer.current !== null) clearTimeout(advanceTimer.current);
  }, []);

  useEffect(() => {
    if (!notice) return;
    const timer = window.setTimeout(() => setNotice(''), 2200);
    return () => clearTimeout(timer);
  }, [notice]);

  useEffect(() => {
    if (!ready || !previewStep || !preview || !sceneRef.current) {
      setGuideMedia(current => {
        current?.frames.forEach(URL.revokeObjectURL);
        return null;
      });
      return;
    }
    let cancelled = false;
    let urls: string[] = [];
    setGuideLoading(true);
    const timer = window.setTimeout(() => {
      Promise.all(Array.from({ length: GUIDE_FRAME_COUNT }, (_, index) =>
        sceneRef.current!.captureBuildStep(previewStep, 960, 620, {
          progress: index / (GUIDE_FRAME_COUNT - 1),
          focusStep: true,
          focusPadding: 0.86,
          shadows: false,
          format: 'jpeg',
        }),
      )).then(blobs => {
        if (cancelled) return;
        urls = blobs.map(URL.createObjectURL);
        setGuideMedia(current => {
          current?.frames.forEach(URL.revokeObjectURL);
          return { step: previewStep, frames: urls };
        });
      }).catch(() => {}).finally(() => {
        if (!cancelled) setGuideLoading(false);
      });
    }, 160);
    return () => {
      cancelled = true;
      clearTimeout(timer);
      urls.forEach(URL.revokeObjectURL);
    };
  }, [ready, previewStep, preview]);

  const save = useCallback((
    nextCompletedStep = completedStep,
    nextPlacedIds = placedIds,
    nextCompleted = completed,
    nextPlacedTurns = placedTurns,
    nextPlacedPositions = placedPositions,
  ) => {
    const saved = saveModelAssemblyProgress(config.id, {
    completedStep: nextCompletedStep,
    placedIds: nextPlacedIds,
    placedTurns: nextPlacedTurns,
    placedPositions: nextPlacedPositions,
    completed: nextCompleted,
    updatedAt: Date.now(),
    });
    setStorageError(!saved);
    return saved;
  }, [
    config.id, completedStep, placedIds, placedTurns, placedPositions, completed,
  ]);

  const finishStep = useCallback((
    nextPlaced: string[],
    nextTurns: Record<string, QuarterTurn> = placedTurns,
    nextPositions: Record<string, [number, number, number]> = placedPositions,
    assemblyPlaced = false,
  ) => {
    if (!activeStep || advancing) return;
    const audit = auditAssemblyStep(
      activeStep,
      activeParts,
      nextPlaced,
      nextTurns,
      nextPositions,
      assemblyPlaced,
    );
    if (!audit.ok) {
      const rejected = new Set([
        ...audit.unexpectedIds,
        ...audit.wrongOrientationIds,
        ...audit.wrongPositionIds,
      ]);
      const accepted = nextPlaced.filter(id => !rejected.has(id));
      const acceptedTurns = Object.fromEntries(
        Object.entries(nextTurns).filter(([id]) => accepted.includes(id)),
      );
      const acceptedPositions = Object.fromEntries(
        Object.entries(nextPositions).filter(([id]) => accepted.includes(id)),
      );
      setPlacedIds(accepted);
      setPlacedTurns(acceptedTurns);
      setPlacedPositions(acceptedPositions);
      setSelectedMaterial(null);
      setReview('failed');
      setFeedback('wrong');
      save(completedStep, accepted, false, acceptedTurns, acceptedPositions);
      setNotice(tr(
        `本步审核未通过，${rejected.size || audit.missingIds.length} 块已退回材料区`,
        `Step review failed. ${rejected.size || audit.missingIds.length} part(s) returned to the tray`,
      ));
      window.setTimeout(() => setFeedback('idle'), 900);
      return;
    }
    setPlacedIds(nextPlaced);
    setPlacedTurns(nextTurns);
    setPlacedPositions(nextPositions);
    setReview('passed');
    setAdvancing(true);
    setFeedback('correct');
    if (activeStep.kind === 'placement') setPlacementAnimating(true);
    save(completedStep, nextPlaced, false, nextTurns, nextPositions);
    advanceTimer.current = window.setTimeout(() => {
      const nextStep = activeStepNumber;
      const done = nextStep >= steps.length;
      setCompletedStep(nextStep);
      setPlacedIds([]);
      setPlacedTurns({});
      setPlacedPositions({});
      setCompleted(done);
      setAdvancing(false);
      setPlacementAnimating(false);
      setSelectedMaterial(null);
      setFeedback('idle');
      setReview('idle');
      setPreviewStep(done ? steps.length : nextStep + 1);
      save(nextStep, [], done, {}, {});
      setNotice(done
        ? tr('模型拼装完成', 'Model completed')
        : tr(`第 ${nextStep} 步完成`, `Step ${nextStep} completed`));
    }, activeStep.kind === 'placement' ? 1100 : 760);
  }, [
    activeStep, activeParts, activeIds, advancing, save, completedStep,
    activeStepNumber, steps.length, placedTurns, placedPositions, tr,
  ]);

  const placeMaterial = useCallback((
    item: MaterialPayload | null,
    position?: [number, number, number] | null,
  ) => {
    if (!item || !activeStep || completed || advancing || ![0, 1, 2, 3].includes(item.turn)) return;
    if (item.step !== activeStepNumber) {
      setFeedback('wrong');
      setNotice(tr('这不是当前步骤的材料', 'This material belongs to another step'));
      window.setTimeout(() => setFeedback('idle'), 700);
      return;
    }
    if (activeStep.kind === 'placement') {
      if (item.kind !== 'assembly' || item.key !== activeStep.id) {
        setFeedback('wrong');
        return;
      }
      finishStep([], {}, {}, true);
      return;
    }
    const candidates = activeParts.filter(part =>
      `${part.partNumber}:${part.colorCode}` === item.key && !placed.has(part.instanceId));
    const candidate = candidates.find(part => part.instanceId === item.instanceId) ?? candidates[0];
    if (!candidate) {
      setFeedback('wrong');
      setNotice(tr('材料数量或型号不正确', 'Wrong part or quantity'));
      window.setTimeout(() => setFeedback('idle'), 700);
      return;
    }
    if (item.kind !== 'part' || !position || position.length !== 3 || !position.every(n => Number.isFinite(n) && Math.abs(n) <= 1_000_000)) {
      setFeedback('wrong');
      setNotice(tr('请先在画布中选择安装位置', 'Choose an installation position on the canvas'));
      window.setTimeout(() => setFeedback('idle'), 700);
      return;
    }
    const next = [...placedIds, candidate.instanceId];
    const nextTurns = { ...placedTurns, [candidate.instanceId]: item.turn };
    const nextPositions = { ...placedPositions, [candidate.instanceId]: position };
    setPlacedIds(next);
    setPlacedTurns(nextTurns);
    setPlacedPositions(nextPositions);
    setReview('idle');
    setSelectedMaterial(null);
    setFeedback('correct');
    save(completedStep, next, false, nextTurns, nextPositions);
    window.setTimeout(() => setFeedback('idle'), 520);
    if (next.length === activeIds.length) finishStep(next, nextTurns, nextPositions);
  }, [
    activeStep, completed, advancing, activeStepNumber, activeParts, placed,
    placedIds, placedTurns, placedPositions, save, completedStep,
    activeIds.length, finishStep, tr,
  ]);

  const rotateMaterial = useCallback(() => {
    setSelectedMaterial(current => current?.kind === 'part'
      ? { ...current, turn: ((current.turn + 1) % 4) as QuarterTurn }
      : current);
  }, []);

  useEffect(() => {
    const keydown = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && selectedMaterial) {
        event.preventDefault();
        setSelectedMaterial(null);
        return;
      }
      if (
        event.key.toLowerCase() !== 'r'
        || (event.target as HTMLElement)?.closest('input, textarea, select')
      ) return;
      event.preventDefault();
      rotateMaterial();
    };
    window.addEventListener('keydown', keydown);
    return () => window.removeEventListener('keydown', keydown);
  }, [rotateMaterial, selectedMaterial]);

  function resolveMaterial(item: MaterialPayload) {
    if (item.kind === 'assembly') return item;
    const candidate = activeParts.find(part =>
      `${part.partNumber}:${part.colorCode}` === item.key
      && !placed.has(part.instanceId));
    return candidate ? { ...item, instanceId: candidate.instanceId } : null;
  }

  function dragMaterial(event: React.DragEvent, item: MaterialPayload) {
    const resolved = resolveMaterial(item);
    if (!resolved) {
      event.preventDefault();
      return;
    }
    event.dataTransfer.effectAllowed = 'copy';
    event.dataTransfer.setData(payloadType, JSON.stringify(resolved));
    setSelectedMaterial(resolved);
  }

  function selectMaterial(item: MaterialPayload) {
    const resolved = resolveMaterial(item);
    if (resolved) setSelectedMaterial(resolved);
  }

  function resetGame() {
    if (advanceTimer.current !== null) clearTimeout(advanceTimer.current);
    setStorageError(!clearModelAssemblyProgress(config.id));
    setResetOpen(false);
    setCompletedStep(0);
    setPlacedIds([]);
    setPlacedTurns({});
    setPlacedPositions({});
    setCompleted(false);
    setPreviewStep(1);
    setSelectedMaterial(null);
    setAdvancing(false);
    setPlacementAnimating(false);
    setFeedback('idle');
    setReview('idle');
    setNotice(tr('进度已重置', 'Progress reset'));
  }

  function undoPlacement() {
    if (!placedIds.length || advancing || completed) return;
    const id = placedIds.at(-1)!;
    const next = placedIds.slice(0, -1);
    const turns = { ...placedTurns }, positions = { ...placedPositions };
    delete turns[id]; delete positions[id];
    setPlacedIds(next); setPlacedTurns(turns); setPlacedPositions(positions);
    setSelectedMaterial(null); setReview('idle'); setFeedback('idle');
    save(completedStep, next, false, turns, positions);
  }

  function remaining(groupKey: string) {
    return activeParts.filter(part =>
      `${part.partNumber}:${part.colorCode}` === groupKey
      && !placed.has(part.instanceId),
    ).length;
  }

  return <div className="assembly-game-page">
    <header className="topbar assembly-game-topbar">
      <a href={`${import.meta.env.BASE_URL}assemble`} className="icon-button" aria-label={tr('返回模型选择', 'Back to model selection')}>
        <ArrowLeft size={18} />
      </a>
      <a href={import.meta.env.BASE_URL} className="brand">
        <span className="brand-mark"><BrickAtlasMark /></span>
        <strong>BRICK<span>ATLAS</span></strong>
      </a>
      <div className="top-divider" />
      <span className="workspace-label">{tr('线上拼装空间', 'Assembly game')}</span>
      <nav className="top-actions">
        <button className="text-button" onClick={() => {
          if (save()) setNotice(tr('当前进度已保存', 'Progress saved'));
        }}><Save size={16} />{tr('保存', 'Save')}</button>
        <a className="text-button" href={import.meta.env.BASE_URL}>
          <Library size={16} />{tr('项目库', 'Library')}
        </a>
        {languageButton(locale, toggleLocale, tr)}
      </nav>
    </header>

    <div className="assembly-game-workspace">
      <aside className="assembly-game-info" aria-label={tr('模型与进度', 'Model and progress')}>
        <div className="assembly-game-model">
          <span className="eyebrow">MODEL {config.setNumber}</span>
          <h1>{locale === 'zh' ? config.subtitle : config.title}</h1>
          <p>{config.theme} · {config.year}</p>
          <DifficultyStuds difficulty={difficulty} locale={locale} />
          <span>{difficultyLabel(difficulty, locale)}</span>
        </div>
        <label className="assembly-model-select">
          <span>{tr('选择模型', 'Choose model')}</span>
          <select
            aria-label={tr('选择拼装模型', 'Choose assembly model')}
            value={config.id}
            onChange={event => {
              location.href = `${import.meta.env.BASE_URL}assemble/${event.target.value}`;
            }}
          >
            {[...modelCatalog]
              .sort((a, b) => assemblyDifficulty(a.id) - assemblyDifficulty(b.id))
              .map(model =>
                <option key={model.id} value={model.id}>
                  {'★'.repeat(assemblyDifficulty(model.id))} · {model.setNumber} · {model.title}
                </option>,
              )}
          </select>
        </label>
        <dl className="assembly-game-stats">
          <div><dt>{tr('零件', 'Bricks')}</dt><dd>{manifest?.stats.instances ?? '—'}</dd></div>
          <div><dt>{tr('步骤', 'Steps')}</dt><dd>{steps.length || '—'}</dd></div>
          <div><dt>{tr('已完成', 'Completed')}</dt><dd>{completedStep}</dd></div>
          <div><dt>{tr('当前材料', 'Current parts')}</dt><dd>{activeStep?.kind === 'placement' ? 1 : activeIds.length}</dd></div>
        </dl>
        <section className="assembly-progress-panel">
          <header>
            <strong>{tr('拼装进度', 'Build progress')}</strong>
            <span>{percent}%</span>
          </header>
          <progress max={steps.length || 1} value={completedStep} />
          <p>{completed
            ? tr('全部步骤完成', 'All steps completed')
            : tr(`第 ${activeStepNumber} / ${steps.length} 步`, `Step ${activeStepNumber} / ${steps.length}`)}</p>
        </section>
        <section className="assembly-current-info">
          <span className="eyebrow">{tr('当前任务', 'CURRENT TASK')}</span>
          <h2>{activeStep
            ? stepTitle(activeStep, activeStepNumber, locale)
            : tr('模型已完成', 'Model complete')}</h2>
          {!completed && <p>{activeStep?.kind === 'placement'
            ? tr('拖入完整子装配', 'Drag the completed subassembly')
            : tr(
              `已放置 ${placedIds.length} / ${activeIds.length} 块`,
              `${placedIds.length} / ${activeIds.length} bricks placed`,
            )}</p>}
        </section>
        {storageError && <p role="alert">{tr('进度未保存：浏览器存储不可用', 'Progress not saved: browser storage is unavailable')}</p>}
        <IconButton label={tr('撤回最后一块', 'Undo last placement')} disabled={!placedIds.length || advancing || completed} onClick={undoPlacement}><Undo2 size={17} /></IconButton>
        <a className="text-button" href={`${import.meta.env.BASE_URL}build/${config.id}`}>{tr('查看完整拼装说明', 'Open guided build')}</a>
        <button className="assembly-reset" onClick={() => setResetOpen(true)}>
          <RotateCcw size={15} />{tr('重新开始', 'Start over')}
        </button>
      </aside>

      <main
        className={`assembly-game-stage ${dragOver ? 'drag-over' : ''}`}
        aria-label={tr('手动拼装画布', 'Manual assembly canvas')}
        onDragEnterCapture={event => {
          event.preventDefault();
          setDragOver(true);
        }}
        onDragOverCapture={event => {
          event.preventDefault();
          event.dataTransfer.dropEffect = 'copy';
          if (selectedMaterial?.kind === 'part' && selectedMaterial.instanceId) {
            pointerClient.current = [event.clientX, event.clientY];
            pointerPlacement.current = sceneRef.current?.previewManualAssembly(
              selectedMaterial.instanceId,
              event.clientX,
              event.clientY,
              selectedMaterial.turn,
            ) ?? null;
          }
        }}
        onDragLeaveCapture={event => {
          if (!event.currentTarget.contains(event.relatedTarget as Node | null)) setDragOver(false);
        }}
        onDropCapture={event => {
          event.preventDefault();
          setDragOver(false);
          const item = payload(event);
          const position = item?.kind === 'part' && item.instanceId
            ? sceneRef.current?.assemblyPlacementPoint(item.instanceId, event.clientX, event.clientY)
            : null;
          placeMaterial(item, position);
        }}
        onPointerMove={event => {
          if (selectedMaterial?.kind !== 'part' || !selectedMaterial.instanceId) return;
          pointerClient.current = [event.clientX, event.clientY];
          pointerPlacement.current = sceneRef.current?.previewManualAssembly(
            selectedMaterial.instanceId,
            event.clientX,
            event.clientY,
            selectedMaterial.turn,
          ) ?? null;
        }}
        onPointerLeave={() => {
          pointerPlacement.current = null;
          pointerClient.current = null;
          sceneRef.current?.clearManualAssemblyPreview();
        }}
        onClick={event => {
          if ((event.target as HTMLElement).closest('.assembly-game-view-tools, button, a, select')) return;
          if (selectedMaterial?.kind === 'assembly') { placeMaterial(selectedMaterial); return; }
          if (
            selectedMaterial?.kind !== 'part'
            || !selectedMaterial.instanceId
            || (event.target as HTMLElement).closest('.assembly-game-view-tools')
          ) return;
          const position = pointerPlacement.current
            ?? sceneRef.current?.assemblyPlacementPoint(
              selectedMaterial.instanceId,
              event.clientX,
              event.clientY,
            );
          placeMaterial(selectedMaterial, position);
        }}
      >
        <div className="assembly-game-canvas" ref={stageRef} />
        <div className="assembly-game-view-tools">
          <label>
            <Box size={16} />
            <select
              aria-label={tr('模型视角', 'Model view')}
              value={view}
              onChange={event => setView(event.target.value as ExplorerState['view'])}
            >
              <option value="perspective">{tr('三分之四', 'Perspective')}</option>
              <option value="front">{tr('正面', 'Front')}</option>
              <option value="side">{tr('侧面', 'Side')}</option>
              <option value="rear">{tr('背面', 'Rear')}</option>
              <option value="top">{tr('顶部', 'Top')}</option>
            </select>
          </label>
          <IconButton label={tr('旋转视图', 'Orbit view')} active={!panMode} onClick={() => setPanMode(false)}>
            <Rotate3D size={17} />
          </IconButton>
          <IconButton label={tr('平移视图', 'Pan view')} active={panMode} onClick={() => setPanMode(true)}>
            <Hand size={17} />
          </IconButton>
          <IconButton label={tr('聚焦模型', 'Fit model')} onClick={() => sceneRef.current?.focusBuildStep(Math.max(1, activeStepNumber))}>
            <Crosshair size={17} />
          </IconButton>
        </div>

        {(loading || error) && <div className={`assembly-game-loading ${error ? 'error' : ''}`} role={error ? 'alert' : 'status'}>
          {error
            ? <><CircleAlert size={30} /><strong>{tr('模型载入失败', 'Model failed to load')}</strong><span>{error}</span></>
            : <><LoaderCircle className="spinner" size={27} /><strong>{stage}</strong><progress max={100} value={progress} /><span>{Math.floor(progress)}%</span></>}
        </div>}

        {completed && !loading && <section className="assembly-win">
          <CheckCircle2 size={48} />
          <h2>{tr('拼装完成', 'Build complete')}</h2>
          <p>{locale === 'zh' ? config.subtitle : config.title}</p>
          <a href={import.meta.env.BASE_URL}>{tr('返回主页查看勾选', 'View completion on home')}</a>
        </section>}

        {!completed && !loading && <div className={`assembly-canvas-status ${feedback} ${review}`} role="status">
          {review === 'passed'
            ? <><CheckCircle2 size={16} /><span>{tr('本步审核通过，正在进入下一步', 'Step verified. Advancing')}</span></>
            : review === 'failed' || feedback === 'wrong'
              ? <><CircleAlert size={16} /><span>{tr('本步零件不匹配', 'Part does not match this step')}</span></>
              : feedback === 'correct'
                ? <><Check size={16} /><span>{tr('已安装，材料数量已更新', 'Installed. Material count updated')}</span></>
                : dragOver
                  ? <><Sparkles size={16} /><span>{tr('松开积木，保留当前安装位置', 'Release the part at this position')}</span></>
                  : selectedMaterial?.kind === 'part'
                    ? <><Box size={16} /><span>{tr('移动鼠标定位，点击画布安装', 'Move to position the part, then click the canvas')}</span></>
                    : <><Box size={16} /><span>{tr('点击或拖动右侧零件，开始手动安装', 'Select or drag a part from the right to begin')}</span></>}
        </div>}
        {notice && <div className="assembly-game-toast" role="status">{notice}</div>}
      </main>

      <aside className="assembly-game-guide" aria-label={tr('拼装步骤与材料', 'Assembly steps and materials')}>
        <header>
          <div>
            <span className="eyebrow">STEP GUIDE</span>
            <h2>{preview ? stepTitle(preview, previewStep, locale) : tr('已完成', 'Complete')}</h2>
          </div>
          <output>{previewStep}<span> / {steps.length || '—'}</span></output>
        </header>
        <div className="assembly-guide-scroll">
          <section className="assembly-loop">
            <div className="assembly-guide-label"><Play size={14} />{tr('循环动画', 'Loop animation')}<IconButton label={guidePlaying ? tr('暂停指导动画', 'Pause guide animation') : tr('播放指导动画', 'Play guide animation')} onClick={() => setGuidePlaying(value => !value)}>{guidePlaying ? <Pause size={14} /> : <Play size={14} />}</IconButton></div>
            <div className="assembly-loop-frame">
              <AssemblyGuideLoop media={guideMedia} playing={guidePlaying} loading={guideLoading} step={previewStep} tr={tr} />
            </div>
          </section>
          <section className="assembly-static-guide">
            <div className="assembly-guide-label"><Box size={14} />{tr('静态前后对照', 'Static before and after')}</div>
            <div>
              {guideMedia?.step === previewStep && guideMedia.frames.length
                ? <>
                    <figure><img src={guideMedia.frames[0]} alt={tr('安装前', 'Before placement')} /><figcaption>{tr('安装前', 'Before')}</figcaption></figure>
                    <ArrowRight size={21} />
                    <figure><img src={guideMedia.frames.at(-1)} alt={tr('安装后', 'After placement')} /><figcaption>{tr('安装后', 'After')}</figcaption></figure>
                  </>
                : <span>{tr('正在准备静态图', 'Preparing static guide')}</span>}
            </div>
          </section>
          <section className="assembly-materials">
            <div className="assembly-guide-label"><Box size={14} />{tr('本步材料', 'Materials')}</div>
            {selectedMaterial?.kind === 'part' && selectedMaterial.step === activeStepNumber && <div className="assembly-selected-material">
              <AssemblyMaterialInspector
                data={previewGeometry.get(selectedMaterial.key) ?? null}
                label={tr('当前零件可旋转三维预览', 'Interactive 3D preview of current part')}
              />
              <div className="assembly-orientation-control">
                <span><Rotate3D size={19} /><strong>{tr(`安装方向 ${selectedMaterial.turn * 90}°`, `Placement ${selectedMaterial.turn * 90}°`)}</strong></span>
                <button onClick={rotateMaterial} aria-label={tr('旋转当前积木 90°', 'Rotate current brick 90°')}>
                  <RotateCw size={15} />{tr('旋转 90°', 'Rotate 90°')}
                </button>
              </div>
            </div>}
            {preview?.kind === 'placement'
              ? <button
                  className={`assembly-material-card ${previewStep !== activeStepNumber ? 'future' : ''}`}
                  disabled={previewStep !== activeStepNumber}
                  draggable={previewStep === activeStepNumber}
                  onDragStart={event => dragMaterial(event, {
                    step: previewStep,
                    kind: 'assembly',
                    key: preview.id,
                    turn: 0,
                  })}
                  onClick={() => setSelectedMaterial({
                    step: previewStep,
                    kind: 'assembly',
                    key: preview.id,
                    turn: 0,
                  })}
                >
                  <span className="assembly-material-swatch assembly-swatch-group">
                    {guideMedia?.frames.at(-1)
                      ? <img src={guideMedia.frames.at(-1)} alt="" />
                      : <Sparkles size={20} />}
                  </span>
                  <span><strong>{tr('完整子装配', 'Completed subassembly')}</strong><small>{stepIds(preview).length} {tr('块积木', 'bricks')}</small></span>
                  <b>1×</b>
                </button>
              : previewGroups.map(group => {
                  const left = previewStep === activeStepNumber ? remaining(group.key) : group.quantity;
                  if (previewStep === activeStepNumber && !left) return null;
                  const selected = selectedMaterial?.step === previewStep
                    && selectedMaterial.kind === 'part'
                    && selectedMaterial.key === group.key;
                  const turn = selected ? selectedMaterial.turn : 0;
                  return <button
                    className={`assembly-material-card ${selected ? 'selected' : ''} ${previewStep !== activeStepNumber ? 'future' : ''}`}
                    disabled={previewStep !== activeStepNumber || !left}
                    draggable={previewStep === activeStepNumber && Boolean(left)}
                    key={group.key}
                    data-current-turn={turn}
                    onDragStart={event => dragMaterial(event, {
                      step: previewStep,
                      kind: 'part',
                      key: group.key,
                      turn,
                    })}
                    onClick={() => selectMaterial({
                      step: previewStep,
                      kind: 'part',
                      key: group.key,
                      turn,
                    })}
                  >
                    <AssemblyPartThumbnail
                      data={previewGeometry.get(group.key) ?? null}
                      label={tr(`${group.name} 三维零件预览`, `${group.name} 3D part preview`)}
                      turn={turn}
                    />
                    <span><strong>{group.partNumber}</strong><small>{group.name}<br />{group.colorName}<br />{previewStep === activeStepNumber
                      ? tr('拖入左侧画布安装', 'Drag into the canvas')
                      : tr('预览步骤材料', 'Preview material')}</small></span>
                    <b>{left}×</b>
                  </button>;
                })}
          </section>
          <section className="assembly-step-list">
            <div className="assembly-guide-label"><Library size={14} />{tr('全部步骤', 'All steps')}</div>
            {steps.map((item, index) => {
              const number = index + 1;
              const done = number <= completedStep;
              const active = number === activeStepNumber && !completed;
              return <button
                className={`${done ? 'done' : ''} ${active ? 'active' : ''}`}
                key={item.id}
                onClick={() => setPreviewStep(number)}
                aria-current={active ? 'step' : undefined}
              >
                <span>{done ? <Check size={13} /> : active ? <Box size={13} /> : <LockKeyhole size={12} />}</span>
                <strong>{String(number).padStart(2, '0')}</strong>
                <small>{stepTitle(item, number, locale)}</small>
                <ChevronRight size={13} />
              </button>;
            })}
          </section>
        </div>
      </aside>
    </div>
    {resetOpen && <Modal title={tr('重新开始拼装？', 'Restart assembly?')} onClose={() => setResetOpen(false)}>
      <div className="diy-confirm"><p>{tr('当前模型的拼装进度将被清除。', 'The assembly progress for this model will be cleared.')}</p>
        <button className="primary-button" onClick={resetGame}>{tr('确认重新开始', 'Confirm restart')}</button></div>
    </Modal>}
  </div>;
}
