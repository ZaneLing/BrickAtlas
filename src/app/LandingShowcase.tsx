import { useEffect, useRef, useState } from 'react';
import { Box, Layers3, Play, ScanSearch } from 'lucide-react';
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

const clamp = (value: number) => Math.max(0, Math.min(1, value));

export function LandingShowcase({ locale, tr }: { locale: Locale; tr: Translator }) {
  const sectionRef = useRef<HTMLElement>(null);
  const hostRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<AtlasScene | null>(null);
  const sceneStateRef = useRef<ExplorerState>({ ...initialState, buildStep: 0, edges: false, grid: false, quality: 'high' });
  const stepRef = useRef(-1);
  const [phase, setPhase] = useState<'build' | 'inspect' | 'explode'>('build');
  const [ready, setReady] = useState(false);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!hostRef.current) return;
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
  }, []);

  useEffect(() => {
    sceneRef.current?.setLocale(locale);
  }, [locale]);

  useEffect(() => {
    let frame = 0;
    const update = () => {
      frame = 0;
      const section = sectionRef.current;
      const scene = sceneRef.current;
      if (!section || !scene) return;
      const rect = section.getBoundingClientRect();
      const travel = Math.max(1, rect.height - innerHeight);
      const progress = matchMedia('(prefers-reduced-motion: reduce)').matches ? 0.58 : clamp(-rect.top / travel);
      section.style.setProperty('--story-progress', String(progress));
      const steps = scene.manifest.instructions?.steps.length ?? 1;
      const nextStep = progress < 0.5 ? Math.round(clamp(progress / 0.46) * steps) : steps;
      const nextPhase = progress < 0.46 ? 'build' : progress < 0.67 ? 'inspect' : 'explode';
      const explosion = progress < 0.67 ? 0 : clamp((progress - 0.67) / 0.3) * 0.72;
      if (nextPhase !== phase) setPhase(nextPhase);
      const stepChanged = nextStep !== stepRef.current;
      if (stepChanged || Math.abs(sceneStateRef.current.explosion - explosion) > 0.005) {
        stepRef.current = nextStep;
        sceneStateRef.current = {
          ...sceneStateRef.current,
          buildStep: nextStep,
          explosion,
          autoRotate: nextPhase !== 'build',
          assemblyRevision: sceneStateRef.current.assemblyRevision + Number(stepChanged),
        };
        scene.setState(sceneStateRef.current);
      }
    };
    const schedule = () => {
      if (!frame) frame = requestAnimationFrame(update);
    };
    update();
    addEventListener('scroll', schedule, { passive: true });
    addEventListener('resize', schedule);
    return () => {
      removeEventListener('scroll', schedule);
      removeEventListener('resize', schedule);
      cancelAnimationFrame(frame);
    };
  }, [phase]);

  const phases = [
    { id: 'build', icon: Play, title: tr('逐步拼装', 'Build step by step'), text: tr('零件按结构顺序入位', 'Bricks arrive in structural order') },
    { id: 'inspect', icon: ScanSearch, title: tr('观察结构', 'Inspect the structure'), text: tr('自由旋转真实 LDraw 几何', 'Orbit true LDraw geometry') },
    { id: 'explode', icon: Layers3, title: tr('三维拆分', 'Explode in 3D'), text: tr('分组展开内部连接关系', 'Reveal internal assemblies') },
  ] as const;

  return <section className="landing-story" ref={sectionRef} aria-label={tr('滚动式功能演示', 'Scroll-driven feature demo')}>
    <div className="landing-story-sticky">
      <div className="story-copy">
        <span className="eyebrow">SCROLL TO BUILD</span>
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
