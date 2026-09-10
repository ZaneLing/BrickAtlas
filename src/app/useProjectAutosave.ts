import { useEffect, useRef, useState } from 'react';
import { writeLocal } from './storage';

export type SaveState = 'saved' | 'saving' | 'error' | 'invalid';

export function useProjectAutosave<T>(key: string, project: T, invalid = false) {
  const [state, setState] = useState<SaveState>(invalid ? 'invalid' : 'saved');
  const latest = useRef({ project, dirty: false, invalid });
  if (latest.current.project !== project) {
    latest.current = { project, dirty: true, invalid: false };
  }
  const save = () => {
    const saved = writeLocal(key, JSON.stringify(latest.current.project));
    if (saved) latest.current.dirty = false;
    latest.current.invalid = false;
    setState(saved ? 'saved' : 'error');
    return saved;
  };
  useEffect(() => {
    if (latest.current.invalid || !latest.current.dirty) return;
    setState('saving');
    const timer = window.setTimeout(save, 450);
    return () => clearTimeout(timer);
  }, [project, key]);
  useEffect(() => {
    const flush = () => {
      const current = latest.current;
      if (current.dirty && !current.invalid) {
        const saved = writeLocal(key, JSON.stringify(current.project));
        current.dirty = !saved;
        setState(saved ? 'saved' : 'error');
      }
    };
    const visibility = () => { if (document.visibilityState === 'hidden') flush(); };
    window.addEventListener('pagehide', flush);
    document.addEventListener('visibilitychange', visibility);
    return () => {
      window.removeEventListener('pagehide', flush);
      document.removeEventListener('visibilitychange', visibility);
      flush();
    };
  }, [key]);
  return { state, save };
}
