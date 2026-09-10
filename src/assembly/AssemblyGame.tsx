import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowLeft, ArrowRight, Box, Check, CheckCircle2, ChevronRight, CircleAlert,
  Crosshair, Hand, Languages, Library, LoaderCircle, LockKeyhole, Play,
  Rotate3D, RotateCcw, RotateCw, Save, Sparkles, Trophy,
} from 'lucide-react';
import { modelCatalog, type ModelConfig } from '../../atlas.config';
import { BrickModel } from '../model/BrickModel';
import {
  initialState, type AssemblyStep, type AtlasManifest, type ExplorerState,
} from '../model/types';
import { AtlasScene } from '../scene/AtlasScene';
import { BrickAtlasMark } from '../ui/BrickAtlasMark';
import { IconButton } from '../ui/Controls';
import type { Locale, Translator } from '../app/locale';
import {
  assemblyDifficulty, difficultyLabel, type AssemblyDifficulty,
} from './difficulty';
import {
  assemblyMaterialKey, groupAssemblyMaterials, partOrientationMatches,
  type QuarterTurn,
} from './orientation';
import {
  clearModelAssemblyProgress, completedAssemblyModels, readModelAssemblyProgress,
  saveModelAssemblyProgress,
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
      selectedTurn: QuarterTurn | null;
      scene: ReturnType<AtlasScene['snapshot']> | null;
    };
  }
}

type MaterialPayload = {
  step: number;
  kind: 'part' | 'assembly';
  key: string;
  turn: QuarterTurn;
};

type GuideMedia = {
  step: number;
  frames: string[];
};

const payloadType = 'application/x-brick-atlas-material';

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

export function AssemblyGameHub({
  locale,
  tr,
  toggleLocale,
}: {
  locale: Locale;
  tr: Translator;
  toggleLocale: () => void;
}) {
  const completed = completedAssemblyModels();
  const models = [...modelCatalog].sort((a, b) =>
    assemblyDifficulty(a.id) - assemblyDifficulty(b.id)
    || a.title.localeCompare(b.title),
  );
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
          <p>{tr(
            '从材料托盘拖入正确零件，按顺序完成真实模型。',
            'Drag the correct bricks from the tray and complete a real model in order.',
          )}</p>
        </div>
        <div className="assembly-hub-completion">
          <Trophy size={24} />
          <strong>{completed.size}</strong>
          <span>{tr('已完成', 'completed')}</span>
        </div>
      </section>
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
              <p>{model.theme}</p>
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
  const [manifest, setManifest] = useState<AtlasManifest | null>(null);
  const [loading, setLoading] = useState(true);
  const [ready, setReady] = useState(false);
  const [error, setError] = useState('');
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState(tr('读取模型', 'Loading model'));
  const [completedStep, setCompletedStep] = useState(0);
  const [placedIds, setPlacedIds] = useState<string[]>([]);
  const [placedTurns, setPlacedTurns] = useState<Record<string, QuarterTurn>>({});
  const [completed, setCompleted] = useState(false);
  const [previewStep, setPreviewStep] = useState(1);
  const [selectedMaterial, setSelectedMaterial] = useState<MaterialPayload | null>(null);
  const [feedback, setFeedback] = useState<'idle' | 'correct' | 'wrong'>('idle');
  const [notice, setNotice] = useState('');
  const [advancing, setAdvancing] = useState(false);
  const [placementAnimating, setPlacementAnimating] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const [view, setView] = useState<ExplorerState['view']>('perspective');
  const [panMode, setPanMode] = useState(false);
  const [guideMedia, setGuideMedia] = useState<GuideMedia | null>(null);
  const [guideLoading, setGuideLoading] = useState(false);
  const [frameIndex, setFrameIndex] = useState(0);

  const steps = manifest?.instructions?.steps ?? [];
  const activeStepNumber = completed ? steps.length : Math.min(completedStep + 1, steps.length);
  const activeStep = steps[activeStepNumber - 1];
  const activeIds = stepIds(activeStep);
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
  const previewGroups = useMemo(() => groupAssemblyMaterials(previewParts), [previewParts]);
  const placed = useMemo(() => new Set(placedIds), [placedIds]);
  const difficulty = assemblyDifficulty(config.id);
  const percent = modelProgressPercent(completedStep, steps.length);

  useEffect(() => {
    const abort = new AbortController();
    setLoading(true);
    setReady(false);
    setError('');
    fetch(`${base}manifest.json`, { signal: abort.signal })
      .then(async response => {
        if (!response.ok) throw new Error(`manifest.json: HTTP ${response.status}`);
        const next = await response.json() as AtlasManifest;
        if (!next.instructions?.steps.length) throw new Error(tr('模型没有拼装步骤', 'Model has no assembly steps'));
        const saved = readModelAssemblyProgress(config.id);
        const clamped = Math.min(saved.completedStep, next.instructions.steps.length);
        const currentIds = new Set(stepIds(next.instructions.steps[clamped]));
        setCompletedStep(clamped);
        setPlacedIds(saved.placedIds.filter(id => currentIds.has(id)));
        setPlacedTurns(Object.fromEntries(
          Object.entries(saved.placedTurns ?? {})
            .filter(([id]) => currentIds.has(id)),
        ));
        setCompleted(saved.completed || clamped >= next.instructions.steps.length);
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
    if (!manifest || !steps.length) return;
    const hiddenBrickIds = !completed && activeStep?.kind !== 'placement'
      ? activeIds.filter(id => !placed.has(id))
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
      hiddenBrickIds,
      view,
      grid: false,
      edges: true,
      highlightStep: false,
      assemblyRevision: completedStep * 1000 + Number(placementAnimating),
    }, { preserveCamera });
    appliedView.current = view;
    if (!preserveCamera && activeStepNumber > 0) {
      requestAnimationFrame(() => sceneRef.current?.focusBuildStep(activeStepNumber));
    }
  }, [
    manifest, steps.length, completed, activeStep, activeIds, activeStepNumber,
    completedStep, placed, placedIds.length, placementAnimating, view,
  ]);

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
      selectedTurn: selectedMaterial?.turn ?? null,
      scene: sceneRef.current?.snapshot() ?? null,
    });
    return () => {
      delete window.__assemblyGame;
    };
  }, [
    config.id, ready, completedStep, activeStepNumber, placedIds.length,
    activeStep, activeIds.length, completed, advancing, feedback, selectedMaterial,
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
    if (!guideMedia?.frames.length) return;
    setFrameIndex(0);
    const timer = window.setInterval(() => {
      setFrameIndex(index => (index + 1) % guideMedia.frames.length);
    }, 420);
    return () => clearInterval(timer);
  }, [guideMedia]);

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
      Promise.all(Array.from({ length: 7 }, (_, index) =>
        sceneRef.current!.captureBuildStep(previewStep, 960, 620, {
          progress: index / 6,
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
  ) => saveModelAssemblyProgress(config.id, {
    completedStep: nextCompletedStep,
    placedIds: nextPlacedIds,
    placedTurns: nextPlacedTurns,
    completed: nextCompleted,
    updatedAt: Date.now(),
  }), [config.id, completedStep, placedIds, placedTurns, completed]);

  const finishStep = useCallback((
    nextPlaced: string[],
    nextTurns: Record<string, QuarterTurn> = placedTurns,
  ) => {
    if (!activeStep || advancing) return;
    setPlacedIds(nextPlaced);
    setPlacedTurns(nextTurns);
    setAdvancing(true);
    setFeedback('correct');
    if (activeStep.kind === 'placement') setPlacementAnimating(true);
    save(completedStep, nextPlaced, false, nextTurns);
    advanceTimer.current = window.setTimeout(() => {
      const nextStep = activeStepNumber;
      const done = nextStep >= steps.length;
      setCompletedStep(nextStep);
      setPlacedIds([]);
      setPlacedTurns({});
      setCompleted(done);
      setAdvancing(false);
      setPlacementAnimating(false);
      setSelectedMaterial(null);
      setFeedback('idle');
      setPreviewStep(done ? steps.length : nextStep + 1);
      save(nextStep, [], done, {});
      setNotice(done
        ? tr('模型拼装完成', 'Model completed')
        : tr(`第 ${nextStep} 步完成`, `Step ${nextStep} completed`));
    }, activeStep.kind === 'placement' ? 1100 : 760);
  }, [
    activeStep, advancing, save, completedStep, activeStepNumber, steps.length,
    placedTurns, tr,
  ]);

  const placeMaterial = useCallback((item: MaterialPayload | null) => {
    if (!item || !activeStep || completed || advancing) return;
    if (item.step !== activeStepNumber) {
      setFeedback('wrong');
      setNotice(tr('这不是当前步骤的材料', 'This material belongs to another step'));
      window.setTimeout(() => setFeedback('idle'), 700);
      return;
    }
    if (activeStep.kind === 'placement') {
      if (item.kind !== 'assembly') {
        setFeedback('wrong');
        return;
      }
      finishStep([], {});
      return;
    }
    const candidates = activeParts.filter(part =>
      assemblyMaterialKey(part) === item.key && !placed.has(part.instanceId));
    const candidate = candidates.find(part => partOrientationMatches(part, item.turn));
    if (!candidate) {
      setFeedback('wrong');
      setNotice(candidates.length
        ? tr('积木方向不正确，请旋转 90° 后重试', 'Wrong orientation. Rotate the brick 90° and try again')
        : tr('材料数量或型号不正确', 'Wrong part or quantity'));
      window.setTimeout(() => setFeedback('idle'), 700);
      return;
    }
    const next = [...placedIds, candidate.instanceId];
    const nextTurns = { ...placedTurns, [candidate.instanceId]: item.turn };
    setPlacedIds(next);
    setPlacedTurns(nextTurns);
    window.setTimeout(() => sceneRef.current?.animateInstances([candidate.instanceId]), 30);
    setSelectedMaterial(null);
    setFeedback('correct');
    save(completedStep, next, false, nextTurns);
    window.setTimeout(() => setFeedback('idle'), 520);
    if (next.length === activeIds.length) finishStep(next, nextTurns);
  }, [
    activeStep, completed, advancing, activeStepNumber, activeParts, placed,
    placedIds, placedTurns, save, completedStep, activeIds.length, finishStep, tr,
  ]);

  const rotateMaterial = useCallback(() => {
    setSelectedMaterial(current => current?.kind === 'part'
      ? { ...current, turn: ((current.turn + 1) % 4) as QuarterTurn }
      : current);
  }, []);

  useEffect(() => {
    const keydown = (event: KeyboardEvent) => {
      if (
        event.key.toLowerCase() !== 'r'
        || (event.target as HTMLElement)?.closest('input, textarea, select')
      ) return;
      event.preventDefault();
      rotateMaterial();
    };
    window.addEventListener('keydown', keydown);
    return () => window.removeEventListener('keydown', keydown);
  }, [rotateMaterial]);

  function dragMaterial(event: React.DragEvent, item: MaterialPayload) {
    event.dataTransfer.effectAllowed = 'copy';
    event.dataTransfer.setData(payloadType, JSON.stringify(item));
    setSelectedMaterial(item);
  }

  function resetGame() {
    if (advanceTimer.current !== null) clearTimeout(advanceTimer.current);
    clearModelAssemblyProgress(config.id);
    setCompletedStep(0);
    setPlacedIds([]);
    setPlacedTurns({});
    setCompleted(false);
    setPreviewStep(1);
    setSelectedMaterial(null);
    setAdvancing(false);
    setPlacementAnimating(false);
    setFeedback('idle');
    setNotice(tr('进度已重置', 'Progress reset'));
  }

  function remaining(groupKey: string) {
    return activeParts.filter(part =>
      assemblyMaterialKey(part) === groupKey
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
          save();
          setNotice(tr('当前进度已保存', 'Progress saved'));
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
        <button className="assembly-reset" onClick={resetGame}>
          <RotateCcw size={15} />{tr('重新开始', 'Start over')}
        </button>
      </aside>

      <main className="assembly-game-stage" aria-label={tr('手动拼装画布', 'Manual assembly canvas')}>
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

        {!completed && !loading && <section
          className={`assembly-drop-zone ${dragOver ? 'drag-over' : ''} ${feedback}`}
          onDragEnter={event => {
            event.preventDefault();
            setDragOver(true);
          }}
          onDragOver={event => {
            event.preventDefault();
            event.dataTransfer.dropEffect = 'copy';
          }}
          onDragLeave={event => {
            if (!event.currentTarget.contains(event.relatedTarget as Node | null)) setDragOver(false);
          }}
          onDrop={event => {
            event.preventDefault();
            setDragOver(false);
            placeMaterial(payload(event));
          }}
          onClick={() => placeMaterial(selectedMaterial)}
          role="button"
          tabIndex={0}
          aria-label={tr('积木安装区域', 'Brick installation area')}
          onKeyDown={event => {
            if (event.key === 'Enter' || event.key === ' ') placeMaterial(selectedMaterial);
          }}
        >
          {feedback === 'wrong'
            ? <><CircleAlert size={24} /><strong>{tr('材料不匹配', 'Material rejected')}</strong></>
            : feedback === 'correct'
              ? <><Check size={24} /><strong>{tr('安装正确', 'Correct placement')}</strong></>
              : advancing
                ? <><Sparkles size={24} /><strong>{tr('步骤完成', 'Step complete')}</strong></>
                : <><Box size={25} /><strong>{tr('拖动材料到这里安装', 'Drop a material here to install')}</strong><span>{selectedMaterial
                  ? selectedMaterial.kind === 'part'
                    ? tr(`已选方向 ${selectedMaterial.turn * 90}°，也可点击安装`, `Selected orientation ${selectedMaterial.turn * 90}°. Click to install`)
                    : tr('也可点击放置已选材料', 'Click to place the selected material')
                  : tr('必须使用当前步骤材料', 'Current-step materials only')}</span></>}
        </section>}
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
            <div className="assembly-guide-label"><Play size={14} />{tr('循环动画', 'Loop animation')}</div>
            <div className="assembly-loop-frame">
              {guideMedia?.step === previewStep && guideMedia.frames.length
                ? <img src={guideMedia.frames[frameIndex]} alt={tr(`第 ${previewStep} 步动画`, `Step ${previewStep} animation`)} />
                : <><LoaderCircle className="spinner" size={24} /><span>{guideLoading ? tr('生成清晰动画', 'Rendering clear animation') : tr('等待模型', 'Waiting for model')}</span></>}
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
            {selectedMaterial?.kind === 'part' && selectedMaterial.step === activeStepNumber && <div className="assembly-orientation-control">
              <span><Box style={{ transform: `rotate(${selectedMaterial.turn * 90}deg)` }} size={19} /><strong>{selectedMaterial.turn * 90}°</strong></span>
              <button onClick={rotateMaterial} aria-label={tr('旋转当前积木 90°', 'Rotate current brick 90°')}>
                <RotateCw size={15} />{tr('旋转 90°', 'Rotate 90°')}
              </button>
            </div>}
            {preview?.kind === 'placement'
              ? <button
                  className={`assembly-material-card ${previewStep !== activeStepNumber ? 'future' : ''}`}
                  draggable
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
                  <span className="assembly-material-swatch assembly-swatch-group"><Sparkles size={20} /></span>
                  <span><strong>{tr('完整子装配', 'Completed subassembly')}</strong><small>{stepIds(preview).length} {tr('块积木', 'bricks')}</small></span>
                  <b>1×</b>
                </button>
              : previewGroups.map(group => {
                  const left = previewStep === activeStepNumber ? remaining(group.key) : group.quantity;
                  const selected = selectedMaterial?.step === previewStep
                    && selectedMaterial.kind === 'part'
                    && selectedMaterial.key === group.key;
                  const turn = selected ? selectedMaterial.turn : 0;
                  return <button
                    className={`assembly-material-card ${selected ? 'selected' : ''} ${!left ? 'placed' : ''} ${previewStep !== activeStepNumber ? 'future' : ''}`}
                    disabled={!left}
                    draggable={Boolean(left)}
                    key={group.key}
                    data-required-turn={group.requiredTurn}
                    data-current-turn={turn}
                    data-rotation-relevant={group.rotationRelevant}
                    onDragStart={event => dragMaterial(event, {
                      step: previewStep,
                      kind: 'part',
                      key: group.key,
                      turn,
                    })}
                    onClick={() => setSelectedMaterial({
                      step: previewStep,
                      kind: 'part',
                      key: group.key,
                      turn,
                    })}
                  >
                    <span className="assembly-material-swatch" style={{ background: group.colorHex }}><Box size={18} style={{ transform: `rotate(${turn * 90}deg)` }} /></span>
                    <span><strong>{group.partNumber}</strong><small>{group.name}<br />{group.colorName}<br />{group.rotationRelevant
                      ? tr(`目标方向 ${group.requiredTurn * 90}°`, `Target orientation ${group.requiredTurn * 90}°`)
                      : tr('方向任意', 'Any orientation')}</small></span>
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
  </div>;
}
