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
  }
}

const BUILD_DURATION = 18000;
const COMPLETE_HOLD_DURATION = 1500;
const EXPLODE_OUT_DURATION = 3500;
const EXPLODE_HOLD_DURATION = 1000;
const EXPLODE_IN_DURATION = 3500;
const ASSEMBLED_HOLD_DURATION = 2500;
const EXPLODE_START = BUILD_DURATION + COMPLETE_HOLD_DURATION;
const EXPLODE_OUT_END = EXPLODE_START + EXPLODE_OUT_DURATION;
const EXPLODE_HOLD_END = EXPLODE_OUT_END + EXPLODE_HOLD_DURATION;
const EXPLODE_IN_END = EXPLODE_HOLD_END + EXPLODE_IN_DURATION;
const CYCLE_DURATION = EXPLODE_IN_END + ASSEMBLED_HOLD_DURATION;

export function LandingShowcase({ locale, tr }: { locale: Locale; tr: Translator }) {
  const sectionRef = useRef<HTMLElement>(null);
  const hostRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<AtlasScene | null>(null);
  const sceneStateRef = useRef<ExplorerState>({ ...initialState, buildStep: 0, edges: false, grid: false, quality: 'high' });
  const stepRef = useRef(-1);
  const phaseRef = useRef<'build' | 'explode'>('build');
  const [phase, setPhase] = useState<'build' | 'explode'>('build');
  const [ready, setReady] = useState(false);
  const [error, setError] = useState(false);
  const [started, setStarted] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) { setStarted(true); observer.disconnect(); }
    }, { rootMargin: '200px' });
    if (sectionRef.current) observer.observe(sectionRef.current);
    return () => observer.disconnect();
  }, []);
  useEffect(() => {
    if (!hostRef.current || !started) return;
    const abort = new AbortController();
    let scene: AtlasScene | null = null;
    fetch(`${import.meta.env.BASE_URL}models/5867/manifest.json`, { signal: abort.signal })
      .then(async response => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json() as Promise<AtlasManifest>;
      })
      .then(manifest => {
        if (abort.signal.aborted || !hostRef.current) return;
        scene = new AtlasScene(hostRef.current, new BrickModel(manifest), {
          progress: () => {},
          ready: () => setReady(true),
          error: () => setError(true),
          select: () => {},
          hover: () => {},
        }, locale);
        scene.controls.enablePan = false;
        scene.controls.enableZoom = false;
        scene.controls.enabled = false;
        scene.setState(sceneStateRef.current);
        sceneRef.current = scene;
        window.__landingAtlas = () => scene!.snapshot();
      })
      .catch(() => {
        if (!abort.signal.aborted) setError(true);
      });
    return () => {
      abort.abort();
      scene?.dispose();
      sceneRef.current = null;
      delete window.__landingAtlas;
    };
  }, [started]);

  useEffect(() => {
    sceneRef.current?.setLocale(locale);
  }, [locale]);

  useEffect(() => {
    let frame = 0, active = false, cycleStarted = performance.now();
    const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const update = (time: number) => {
      const section = sectionRef.current;
      const scene = sceneRef.current;
      if (!section || !scene || (!active && !reducedMotion)) {
        frame = requestAnimationFrame(update);
        return;
      }
      const elapsed = reducedMotion
        ? BUILD_DURATION + COMPLETE_HOLD_DURATION / 2
        : (time - cycleStarted) % CYCLE_DURATION;
      const progress = elapsed / CYCLE_DURATION;
      section.style.setProperty('--story-progress', String(progress));
      const steps = scene.manifest.instructions?.steps.length ?? 1;
      const nextStep = elapsed < BUILD_DURATION
        ? Math.round(elapsed / BUILD_DURATION * steps)
        : steps;
      const nextPhase = elapsed < BUILD_DURATION ? 'build' : 'explode';
      const explosion = elapsed < EXPLODE_START
        ? 0
        : elapsed < EXPLODE_OUT_END
          ? (elapsed - EXPLODE_START) / EXPLODE_OUT_DURATION
          : elapsed < EXPLODE_HOLD_END
            ? 1
            : elapsed < EXPLODE_IN_END
              ? 1 - (elapsed - EXPLODE_HOLD_END) / EXPLODE_IN_DURATION
              : 0;
      const phaseChanged = nextPhase !== phaseRef.current;
      if (phaseChanged) {
        phaseRef.current = nextPhase;
        setPhase(nextPhase);
      }
      const stepChanged = nextStep !== stepRef.current;
      if (
        phaseChanged ||
        stepChanged ||
        Math.abs(sceneStateRef.current.explosion - explosion) > 0.005
      ) {
        stepRef.current = nextStep;
        sceneStateRef.current = {
          ...sceneStateRef.current,
          buildStep: nextStep,
          explosion,
          autoRotate: false,
          assemblyRevision: sceneStateRef.current.assemblyRevision + Number(stepChanged),
        };
        scene.setState(sceneStateRef.current);
      }
      frame = requestAnimationFrame(update);
    };
    const observer = new IntersectionObserver(([entry]) => {
      active = entry.isIntersecting;
      if (active) cycleStarted = performance.now();
    }, { threshold: 0.12 });
    if (sectionRef.current) observer.observe(sectionRef.current);
    frame = requestAnimationFrame(update);
    return () => {
      observer.disconnect();
      cancelAnimationFrame(frame);
    };
  }, []);

  const phases = [
    { id: 'build', icon: Play, title: tr('逐步拼装', 'Build step by step'), text: tr('按清晰节奏逐组完成结构', 'Build each structural group at a clear pace') },
    { id: 'explode', icon: Layers3, title: tr('三维拆分', 'Explode in 3D'), text: tr('从完整装配展开至 100%，再收回', 'Expand from 0 to 100%, then return') },
  ] as const;

  return <section className="landing-story" ref={sectionRef} aria-label={tr('自动循环功能演示', 'Auto-playing feature demo')}>
    <div className="landing-story-sticky">
      <div className="story-copy">
        <span className="eyebrow">AUTOMATED BUILD CYCLE</span>
        <h2>{tr('从第一块，到完整结构', 'From the first brick to the full structure')}</h2>
        <div className="story-phases">
          {phases.map((item, index) => {
            const Icon = item.icon;
            return <div className={phase === item.id ? 'active' : ''} key={item.id}><span>{String(index + 1).padStart(2, '0')}</span><Icon size={19} /><div><strong>{item.title}</strong><small>{item.text}</small></div></div>;
          })}
        </div>
        <a href={`${import.meta.env.BASE_URL}build/5867`}><Box size={16} />{tr('进入完整拼装', 'Open the complete build')}</a>
      </div>
      <div className={`story-scene ${ready ? 'ready' : ''}`} ref={hostRef}>
        {!ready && !error && <span className="story-loading">{tr('正在装载真实模型', 'Loading the real model')}</span>}
        {error && <span className="story-loading">{tr('三维演示暂不可用', '3D demo unavailable')}</span>}
        <div className="story-scene-label"><span>{tr('实时渲染', 'Live render')}</span><strong>3× DPR · WebGL 2</strong></div>
      </div>
    </div>
  </section>;
}
