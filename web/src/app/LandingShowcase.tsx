import { useEffect, useRef, useState } from 'react';
import { Box, Boxes, Gamepad2, Layers3, MousePointer2, Play } from 'lucide-react';
import type { Locale, Translator } from './locale';
import type { AtlasManifest, ExplorerState } from '../model/types';
import { initialState } from '../model/types';
import { BrickModel } from '../model/BrickModel';
import { AtlasScene } from '../scene/AtlasScene';
import type { DiyScene } from '../diy/DiyScene';
import type { DiyBrick } from '../diy/diyModel';

declare global {
  interface Window {
    __landingAtlas?: () => ReturnType<AtlasScene['snapshot']>;
    __landingAtlases?: () => {
      build: ReturnType<AtlasScene['snapshot']> | null;
      explode: ReturnType<AtlasScene['snapshot']> | null;
      assemble: ReturnType<AtlasScene['snapshot']> | null;
      diy: ReturnType<DiyScene['snapshot']> | null;
    };
  }
}

const BUILD_DURATION = 26_000;
const BUILD_HOLD = 1_400;
const EXPLODE_DURATION = 4_600;
const EXPLODE_HOLD = 1_100;
const EXPLODE_CYCLE = EXPLODE_DURATION * 2 + EXPLODE_HOLD * 2;
const ASSEMBLE_STEP_DURATION = 2_200;
const ASSEMBLE_PREVIEW_DURATION = 720;
const DIY_STEP_DURATION = 430;
const DIY_HOLD_DURATION = 1_800;

const diyBrick = (
  id: string,
  partId: string,
  color: string,
  x: number,
  y: number,
  z: number,
  turn: DiyBrick['turn'] = 0,
): DiyBrick => ({ id, partId, color, x, y, z, turn, stampId: id });

const DIY_SHOWCASE_BRICKS: DiyBrick[] = [
  diyBrick('demo_base_1', '3031', 'dark-gray', -4, 0, -4),
  diyBrick('demo_base_2', '3031', 'dark-gray', 0, 0, -4),
  diyBrick('demo_base_3', '3031', 'dark-gray', -4, 0, 0),
  diyBrick('demo_base_4', '3031', 'dark-gray', 0, 0, 0),
  diyBrick('demo_wall_1', '3001', 'red', -4, 1, -4),
  diyBrick('demo_wall_2', '3001', 'yellow', 0, 1, -4),
  diyBrick('demo_wall_3', '3001', 'blue', -4, 1, 2),
  diyBrick('demo_wall_4', '3001', 'red', 0, 1, 2),
  diyBrick('demo_wall_5', '3001', 'yellow', -4, 1, -2, 1),
  diyBrick('demo_wall_6', '3001', 'blue', 2, 1, -2, 1),
  diyBrick('demo_upper_1', '3001', 'white', -4, 4, -4),
  diyBrick('demo_upper_2', '3001', 'blue', 0, 4, -4),
  diyBrick('demo_upper_3', '3001', 'white', -4, 4, 2),
  diyBrick('demo_upper_4', '3001', 'yellow', 0, 4, 2),
  diyBrick('demo_upper_5', '3004', 'red', -4, 4, -2, 1),
  diyBrick('demo_upper_6', '3004', 'red', 3, 4, -2, 1),
  diyBrick('demo_roof_1', '3039', 'red', -4, 7, -3),
  diyBrick('demo_roof_2', '3039', 'red', -2, 7, -3),
  diyBrick('demo_roof_3', '3039', 'red', 0, 7, -3),
  diyBrick('demo_roof_4', '3039', 'red', 2, 7, -3),
  diyBrick('demo_roof_5', '3039', 'yellow', -4, 7, 0, 2),
  diyBrick('demo_roof_6', '3039', 'yellow', -2, 7, 0, 2),
  diyBrick('demo_roof_7', '3039', 'yellow', 0, 7, 0, 2),
  diyBrick('demo_roof_8', '3039', 'yellow', 2, 7, 0, 2),
];

const showcaseState = (buildStep: number | null, explosion = 0): ExplorerState => ({
  ...initialState,
  buildStep,
  explosion,
  edges: false,
  grid: false,
  quality: 'high',
  autoRotate: false,
  highlightStep: false,
});

export function LandingShowcase({ locale, tr }: { locale: Locale; tr: Translator }) {
  const sectionRef = useRef<HTMLElement>(null);
  const primaryRowRef = useRef<HTMLDivElement>(null);
  const secondaryRowRef = useRef<HTMLDivElement>(null);
  const buildHostRef = useRef<HTMLDivElement>(null);
  const explodeHostRef = useRef<HTMLDivElement>(null);
  const assembleHostRef = useRef<HTMLDivElement>(null);
  const diyHostRef = useRef<HTMLDivElement>(null);
  const buildSceneRef = useRef<AtlasScene | null>(null);
  const explodeSceneRef = useRef<AtlasScene | null>(null);
  const assembleSceneRef = useRef<AtlasScene | null>(null);
  const diySceneRef = useRef<DiyScene | null>(null);
  const buildStateRef = useRef(showcaseState(0));
  const explodeStateRef = useRef(showcaseState(null));
  const assembleStateRef = useRef(showcaseState(1));
  const buildStepRef = useRef(-1);
  const assemblePhaseRef = useRef('');
  const diySignatureRef = useRef('');
  const [ready, setReady] = useState({ build: false, explode: false, assemble: false, diy: false });
  const [error, setError] = useState(false);
  const [secondaryStarted, setSecondaryStarted] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setSecondaryStarted(true);
        observer.disconnect();
      }
    }, { threshold: 0.3 });
    if (secondaryRowRef.current) observer.observe(secondaryRowRef.current);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!buildHostRef.current || !explodeHostRef.current) return;
    const abort = new AbortController();
    let buildScene: AtlasScene | null = null;
    let explodeScene: AtlasScene | null = null;
    fetch(`${import.meta.env.BASE_URL}models/5867/manifest.json`, { signal: abort.signal })
      .then(async response => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json() as Promise<AtlasManifest>;
      })
      .then(manifest => {
        if (abort.signal.aborted || !buildHostRef.current || !explodeHostRef.current) return;
        const model = new BrickModel(manifest);
        const callbacks = (kind: 'build' | 'explode') => ({
          progress: () => {},
          ready: () => setReady(value => ({ ...value, [kind]: true })),
          error: () => setError(true),
          select: () => {},
          hover: () => {},
        });
        buildScene = new AtlasScene(buildHostRef.current, model, callbacks('build'), locale);
        explodeScene = new AtlasScene(explodeHostRef.current, model, callbacks('explode'), locale);
        for (const scene of [buildScene, explodeScene]) {
          scene.controls.enablePan = false;
          scene.controls.enableZoom = false;
          scene.controls.enabled = false;
        }
        const stepInterval = BUILD_DURATION / ((manifest.instructions?.steps.length ?? 1) + 1);
        buildScene.setAssemblyDuration(stepInterval * 0.88);
        buildScene.setState(buildStateRef.current);
        explodeScene.setState(explodeStateRef.current);
        buildSceneRef.current = buildScene;
        explodeSceneRef.current = explodeScene;
        window.__landingAtlas = () => buildScene!.snapshot();
        window.__landingAtlases = () => ({
          build: buildSceneRef.current?.snapshot() ?? null,
          explode: explodeSceneRef.current?.snapshot() ?? null,
          assemble: assembleSceneRef.current?.snapshot() ?? null,
          diy: diySceneRef.current?.snapshot() ?? null,
        });
      })
      .catch(() => {
        if (!abort.signal.aborted) setError(true);
      });
    return () => {
      abort.abort();
      buildScene?.dispose();
      explodeScene?.dispose();
      buildSceneRef.current = null;
      explodeSceneRef.current = null;
      delete window.__landingAtlas;
      delete window.__landingAtlases;
    };
  }, []);

  useEffect(() => {
    if (!secondaryStarted || !assembleHostRef.current || !diyHostRef.current) return;
    const abort = new AbortController();
    let assembleScene: AtlasScene | null = null;
    let diyScene: DiyScene | null = null;
    Promise.all([
      fetch(`${import.meta.env.BASE_URL}models/31028-sailboat/manifest.json`, { signal: abort.signal })
        .then(async response => {
          if (!response.ok) throw new Error(`HTTP ${response.status}`);
          return response.json() as Promise<AtlasManifest>;
        }),
      import('../diy/DiyScene'),
    ])
      .then(([manifest, { DiyScene: DiySceneClass }]) => {
        if (abort.signal.aborted || !assembleHostRef.current || !diyHostRef.current) return;
        assembleScene = new AtlasScene(assembleHostRef.current, new BrickModel(manifest), {
          progress: () => {},
          ready: () => setReady(value => ({ ...value, assemble: true })),
          error: () => setError(true),
          select: () => {},
          hover: () => {},
        }, locale);
        assembleScene.controls.enablePan = false;
        assembleScene.controls.enableZoom = false;
        assembleScene.controls.enabled = false;
        assembleScene.setAssemblyDuration(820);
        const firstStep = manifest.instructions?.steps[0];
        assembleStateRef.current = {
          ...showcaseState(1),
          ghostBrickIds: firstStep?.motionInstanceIds ?? firstStep?.instanceIds ?? [],
        };
        assembleScene.setState(assembleStateRef.current, { animateAssembly: false });
        assembleSceneRef.current = assembleScene;

        diyScene = new DiySceneClass(diyHostRef.current, {
          hover: () => {},
          place: () => {},
          edit: () => {},
          select: () => {},
          error: () => setError(true),
        }, tr('DIY 自由组建动画', 'DIY free-build animation'));
        diyScene.setTool('orbit');
        diyScene.setBricks(DIY_SHOWCASE_BRICKS);
        diyScene.fit();
        diyScene.setBricks([]);
        diySceneRef.current = diyScene;
        setReady(value => ({ ...value, diy: true }));
      })
      .catch(() => {
        if (!abort.signal.aborted) setError(true);
      });
    return () => {
      abort.abort();
      assembleScene?.dispose();
      diyScene?.dispose();
      assembleSceneRef.current = null;
      diySceneRef.current = null;
    };
  }, [secondaryStarted]);

  useEffect(() => {
    buildSceneRef.current?.setLocale(locale);
    explodeSceneRef.current?.setLocale(locale);
    assembleSceneRef.current?.setLocale(locale);
    diySceneRef.current?.setLabel(tr('DIY 自由组建动画', 'DIY free-build animation'));
  }, [locale]);

  useEffect(() => {
    let frame = 0;
    let active = true;
    let cycleStarted = performance.now();
    const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const update = (time: number) => {
      const buildScene = buildSceneRef.current;
      const explodeScene = explodeSceneRef.current;
      if (!active || !buildScene || !explodeScene || document.hidden) {
        frame = requestAnimationFrame(update);
        return;
      }
      const steps = buildScene.manifest.instructions?.steps.length ?? 1;
      const buildElapsed = reducedMotion ? BUILD_DURATION : (time - cycleStarted) % (BUILD_DURATION + BUILD_HOLD);
      const nextStep = buildElapsed >= BUILD_DURATION
        ? steps
        : Math.min(steps, Math.floor(buildElapsed / BUILD_DURATION * (steps + 1)));
      if (nextStep !== buildStepRef.current) {
        buildStepRef.current = nextStep;
        buildStateRef.current = {
          ...buildStateRef.current,
          buildStep: nextStep,
          assemblyRevision: buildStateRef.current.assemblyRevision + 1,
        };
        buildScene.setState(buildStateRef.current, { preserveCamera: nextStep > 1 });
      }

      const explodeElapsed = reducedMotion ? EXPLODE_DURATION * 0.42 : (time - cycleStarted) % EXPLODE_CYCLE;
      const explosion = explodeElapsed < EXPLODE_DURATION
        ? explodeElapsed / EXPLODE_DURATION
        : explodeElapsed < EXPLODE_DURATION + EXPLODE_HOLD
          ? 1
          : explodeElapsed < EXPLODE_DURATION * 2 + EXPLODE_HOLD
            ? 1 - (explodeElapsed - EXPLODE_DURATION - EXPLODE_HOLD) / EXPLODE_DURATION
            : 0;
      if (Math.abs(explodeStateRef.current.explosion - explosion) > 0.005) {
        explodeStateRef.current = { ...explodeStateRef.current, explosion };
        explodeScene.setState(explodeStateRef.current);
      }
      sectionRef.current?.style.setProperty('--build-progress', `${Math.min(100, buildElapsed / BUILD_DURATION * 100)}%`);
      sectionRef.current?.style.setProperty('--explode-progress', `${explosion * 100}%`);
      frame = requestAnimationFrame(update);
    };
    const observer = new IntersectionObserver(([entry]) => {
      active = entry.isIntersecting;
      if (active) cycleStarted = performance.now();
    }, { threshold: 0.08 });
    if (primaryRowRef.current) observer.observe(primaryRowRef.current);
    frame = requestAnimationFrame(update);
    return () => {
      observer.disconnect();
      cancelAnimationFrame(frame);
    };
  }, []);

  useEffect(() => {
    if (!secondaryStarted) return;
    let frame = 0;
    let active = false;
    let initialized = false;
    let cycleStarted = performance.now();
    const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const update = (time: number) => {
      const assembleScene = assembleSceneRef.current;
      const diyScene = diySceneRef.current;
      if (!active || !assembleScene || !diyScene || document.hidden) {
        frame = requestAnimationFrame(update);
        return;
      }
      if (!initialized) {
        initialized = true;
        cycleStarted = time;
      }
      const steps = assembleScene.manifest.instructions?.steps ?? [];
      if (reducedMotion) {
        if (assemblePhaseRef.current !== 'static') {
          assemblePhaseRef.current = 'static';
          assembleStateRef.current = { ...assembleStateRef.current, buildStep: steps.length, ghostBrickIds: [] };
          assembleScene.setState(assembleStateRef.current, { animateAssembly: false });
          diyScene.setBricks(DIY_SHOWCASE_BRICKS);
        }
        frame = requestAnimationFrame(update);
        return;
      }

      if (steps.length) {
        const elapsed = time - cycleStarted;
        const cycleIndex = Math.floor(elapsed / ASSEMBLE_STEP_DURATION);
        const stepNumber = cycleIndex % steps.length + 1;
        const phaseElapsed = elapsed % ASSEMBLE_STEP_DURATION;
        const phase = phaseElapsed < ASSEMBLE_PREVIEW_DURATION ? 'preview' : 'place';
        const phaseKey = `${stepNumber}:${phase}`;
        if (phaseKey !== assemblePhaseRef.current) {
          assemblePhaseRef.current = phaseKey;
          const step = steps[stepNumber - 1];
          const ids = step.motionInstanceIds ?? step.instanceIds;
          if (phase === 'preview') {
            assembleStateRef.current = { ...assembleStateRef.current, buildStep: stepNumber, ghostBrickIds: ids };
            assembleScene.setState(assembleStateRef.current, {
              animateAssembly: false,
              preserveCamera: stepNumber > 1,
            });
          } else {
            assembleStateRef.current = {
              ...assembleStateRef.current,
              ghostBrickIds: [],
              assemblyRevision: assembleStateRef.current.assemblyRevision + 1,
            };
            assembleScene.setState(assembleStateRef.current, { preserveCamera: true });
          }
          secondaryRowRef.current?.setAttribute('data-assemble-phase', phase);
        }
        sectionRef.current?.style.setProperty(
          '--assemble-progress',
          `${phaseElapsed / ASSEMBLE_STEP_DURATION * 100}%`,
        );
      }

      const diyCycleDuration = DIY_SHOWCASE_BRICKS.length * DIY_STEP_DURATION + DIY_HOLD_DURATION;
      const diyElapsed = (time - cycleStarted) % diyCycleDuration;
      const placedCount = Math.min(DIY_SHOWCASE_BRICKS.length, Math.floor(diyElapsed / DIY_STEP_DURATION));
      const placementProgress = Math.min(1, (diyElapsed % DIY_STEP_DURATION) / DIY_STEP_DURATION);
      const progressBucket = Math.round(placementProgress * 30);
      const signature = `${placedCount}:${progressBucket}`;
      if (signature !== diySignatureRef.current) {
        diySignatureRef.current = signature;
        const bricks = DIY_SHOWCASE_BRICKS.slice(0, placedCount);
        if (placedCount < DIY_SHOWCASE_BRICKS.length) {
          const target = DIY_SHOWCASE_BRICKS[placedCount];
          const eased = 1 - (1 - placementProgress) ** 3;
          bricks.push({ ...target, y: target.y + (1 - eased) * 7 });
        }
        diyScene.setBricks(bricks);
      }
      sectionRef.current?.style.setProperty(
        '--diy-progress',
        `${Math.min(100, diyElapsed / (DIY_SHOWCASE_BRICKS.length * DIY_STEP_DURATION) * 100)}%`,
      );
      frame = requestAnimationFrame(update);
    };
    const observer = new IntersectionObserver(([entry]) => {
      active = entry.isIntersecting;
      if (active) {
        initialized = false;
        assemblePhaseRef.current = '';
        diySignatureRef.current = '';
      }
    }, { threshold: 0.08 });
    if (secondaryRowRef.current) observer.observe(secondaryRowRef.current);
    frame = requestAnimationFrame(update);
    return () => {
      observer.disconnect();
      cancelAnimationFrame(frame);
    };
  }, [secondaryStarted]);

  const panels = [
    {
      id: 'build',
      icon: Play,
      title: tr('逐步拼装', 'Build step by step'),
      text: tr('从第一块到完整结构', 'From the first brick to the full build'),
      host: buildHostRef,
      ready: ready.build,
    },
    {
      id: 'explode',
      icon: Layers3,
      title: tr('三维拆分', 'Explode in 3D'),
      text: tr('展开结构，观察每一块积木', 'Expand the structure and inspect every brick'),
      host: explodeHostRef,
      ready: ready.explode,
    },
  ] as const;

  return <section className="landing-showcase" ref={sectionRef} aria-label={tr('四动画积木演示', 'Four animated brick showcases')}>
    <div className="landing-showcase-row landing-showcase-primary" ref={primaryRowRef}>
      {panels.map(panel => {
        const Icon = panel.icon;
        return <article className={`landing-demo landing-demo-${panel.id}`} key={panel.id} aria-label={panel.title}>
          <header className="landing-demo-heading">
            <span><Icon size={17} />{panel.title}</span>
            <strong>{panel.text}</strong>
          </header>
          <div className={`landing-demo-scene ${panel.ready ? 'ready' : ''}`} ref={panel.host}>
            {!panel.ready && !error && <span className="story-loading">{tr('正在装载真实模型', 'Loading the real model')}</span>}
            {error && <span className="story-loading">{tr('三维演示暂不可用', '3D demo unavailable')}</span>}
          </div>
          <footer>
            <span>{panel.id === 'build' ? tr('实时拼装', 'LIVE BUILD') : tr('实时拆分', 'LIVE EXPLODE')}</span>
            <a href={`${import.meta.env.BASE_URL}${panel.id === 'build' ? 'build' : 'explore'}/5867`}><Box size={14} />{tr('打开工作台', 'Open workspace')}</a>
          </footer>
        </article>;
      })}
    </div>
    <div className="landing-showcase-row landing-showcase-secondary" ref={secondaryRowRef}>
      <article className="landing-demo landing-demo-assemble" aria-label={tr('自主 Assemble', 'Self-guided Assemble')}>
        <header className="landing-demo-heading">
          <span><Gamepad2 size={17} />{tr('自主 Assemble', 'Self-guided Assemble')}</span>
          <strong>{tr('自动选件，旋转并吸附到目标', 'Pick, rotate, and snap each part into place')}</strong>
        </header>
        <div className={`landing-demo-scene ${ready.assemble ? 'ready' : ''}`} ref={assembleHostRef}>
          {!ready.assemble && !error && <span className="story-loading">{tr('正在准备自主拼装', 'Preparing guided assembly')}</span>}
          {error && <span className="story-loading">{tr('三维演示暂不可用', '3D demo unavailable')}</span>}
        </div>
        <span className="landing-assemble-pointer" aria-hidden="true"><MousePointer2 size={19} /><i /></span>
        <footer>
          <span>{tr('自动选件 · 吸附校验', 'AUTO PICK · SNAP CHECK')}</span>
          <a href={`${import.meta.env.BASE_URL}assemble/31028-sailboat`}><Gamepad2 size={14} />{tr('进入自主拼装', 'Open Assemble')}</a>
        </footer>
      </article>
      <article className="landing-demo landing-demo-diy" aria-label={tr('DIY 自由组建', 'DIY free build')}>
        <header className="landing-demo-heading">
          <span><Boxes size={17} />{tr('DIY 自由组建', 'DIY free build')}</span>
          <strong>{tr('从空底板逐块搭出彩色作品', 'Build a colorful original creation brick by brick')}</strong>
        </header>
        <div className={`landing-demo-scene ${ready.diy ? 'ready' : ''}`} ref={diyHostRef}>
          {!ready.diy && !error && <span className="story-loading">{tr('正在准备 DIY 底板', 'Preparing the DIY baseplate')}</span>}
          {error && <span className="story-loading">{tr('三维演示暂不可用', '3D demo unavailable')}</span>}
        </div>
        <span className="landing-diy-pulse" aria-hidden="true" />
        <footer>
          <span>{tr('彩色作品 · 实时搭建', 'COLOR BUILD · LIVE PLACEMENT')}</span>
          <a href={`${import.meta.env.BASE_URL}diy`}><Boxes size={14} />{tr('进入自由 DIY', 'Open Free DIY')}</a>
        </footer>
      </article>
    </div>
  </section>;
}
