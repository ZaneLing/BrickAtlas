import { useCallback, useEffect, useState } from 'react';
import type { GroupId } from '../model/types';

export type Locale = 'zh' | 'en';
export type Translator = (zh: string, en: string) => string;

export function useLocale() {
  const [locale, setLocale] = useState<Locale>(() => localStorage.getItem('brick-atlas-locale') === 'en' ? 'en' : 'zh');
  useEffect(() => {
    localStorage.setItem('brick-atlas-locale', locale);
    document.documentElement.lang = locale === 'zh' ? 'zh-CN' : 'en';
  }, [locale]);
  const tr = useCallback<Translator>((zh, en) => locale === 'zh' ? zh : en, [locale]);
  return { locale, tr, toggleLocale: () => setLocale(value => value === 'zh' ? 'en' : 'zh') };
}

const groupNames: Record<GroupId, string> = {
  body: 'Body',
  chassis: 'Foundation',
  wheels: 'Wheels & moving parts',
  cockpit: 'Cabin & characters',
  front: 'Front & accessories',
  rear: 'Rear & exterior',
};

export function localGroupName(locale: Locale, id: GroupId, fallback: string) {
  return locale === 'zh' ? fallback : groupNames[id];
}

export function localCategory(locale: Locale, category: string) {
  if (locale === 'zh') return category;
  return ({ '车辆': 'Vehicles', '飞行': 'Aircraft', '船舶': 'Marine', '建筑': 'Buildings', '铁路': 'Rail' } as Record<string, string>)[category] ?? category;
}
