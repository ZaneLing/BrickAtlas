import { useEffect, useRef, useState } from 'react';
import { Box, Layers3, Play } from 'lucide-react';
import type { Locale, Translator } from './locale';
import type { AtlasManifest, ExplorerState } from '../model/types';
import { initialState } from '../model/types';
import { BrickModel } from '../model/BrickModel';
import { AtlasScene } from '../scene/AtlasScene';

declare global {
  interface Window {
    __landingAtlas?: () => ReturnType<AtlasScene['snapshot']>;
    __landingAtlases?: () => {
      build: ReturnType<AtlasScene['snapshot']> | null;
      explode: ReturnType<AtlasScene['snapshot']> | null;
    };
  }
}

const BUILD_DURATION = 26_000;
const BUILD_HOLD = 1_400;
const EXPLODE_DURATION = 4_600;
const EXPLODE_HOLD = 1_100;
const EXPLODE_CYCLE = EXPLODE_DURATION * 2 + EXPLODE_HOLD * 2;

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
  const buildHostRef = useRef<HTMLDivElement>(null);
  const explodeHostRef = useRef<HTMLDivElement>(null);
  const buildSceneRef = useRef<AtlasScene | null>(null);
  const explodeSceneRef = useRef<AtlasScene | null>(null);
  const buildStateRef = useRef(showcaseState(0));
  const explodeStateRef = useRef(showcaseState(null));
  const buildStepRef = useRef(-1);
  const [ready, setReady] = useState({ build: false, explode: false });
  const [error, setError] = useState(false);

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
    buildSceneRef.current?.setLocale(locale);
    explodeSceneRef.current?.setLocale(locale);
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
    if (sectionRef.current) observer.observe(sectionRef.current);
    frame = requestAnimationFrame(update);
    return () => {
      observer.disconnect();
      cancelAnimationFrame(frame);
    };
  }, []);

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

  return <section className="landing-showcase" ref={sectionRef} aria-label={tr('双动画积木演示', 'Dual animated brick showcase')}>
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
  </section>;
}
