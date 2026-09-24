import { useCallback, useRef, useState, type SetStateAction } from 'react';

export interface ProjectHistory<T> { past: T[]; present: T; future: T[] }
export function changeHistory<T>(history: ProjectHistory<T>, action: 'undo' | 'redo'): ProjectHistory<T> {
  if (action === 'undo') {
    const previous = history.past.at(-1);
    return previous === undefined ? history : {
      past: history.past.slice(0, -1), present: previous, future: [history.present, ...history.future],
    };
  }
  const next = history.future[0];
  return next === undefined ? history : {
    past: [...history.past, history.present], present: next, future: history.future.slice(1),
  };
}

export function useProjectHistory<T>(initial: T) {
  const [history, setHistory] = useState<ProjectHistory<T>>({ past: [], present: initial, future: [] });
  const ref = useRef(history);
  const apply = useCallback((next: ProjectHistory<T>) => { ref.current = next; setHistory(next); }, []);
  const setProject = useCallback((action: SetStateAction<T>) => {
    const previous = ref.current;
    const next = typeof action === 'function' ? (action as (value: T) => T)(previous.present) : action;
    if (next === previous.present) return;
    apply({ past: [...previous.past.slice(-49), previous.present], present: next, future: [] });
  }, [apply]);
  const hydrate = useCallback((action: (value: T) => T) => {
    apply({ ...ref.current, present: action(ref.current.present) });
  }, [apply]);
  const undo = useCallback(() => apply(changeHistory(ref.current, 'undo')), [apply]);
  const redo = useCallback(() => apply(changeHistory(ref.current, 'redo')), [apply]);
  return { project: history.present, setProject, hydrate, undo, redo, canUndo: !!history.past.length, canRedo: !!history.future.length };
}
