import { modelCatalog, type ModelConfig } from '../../atlas.config';
import { assemblyDifficulty } from '../assembly/difficulty';
import { readLocal, writeLocal } from './storage';

export interface CatalogFilter {
  query: string;
  category: string;
  difficulty: string;
  status: 'all' | 'favorites' | 'started' | 'completed';
  sort: 'recommended' | 'name' | 'newest';
}
export const defaultCatalogFilter: CatalogFilter = {
  query: '', category: '', difficulty: '', status: 'all', sort: 'recommended',
};
export const FAVORITES_KEY = 'brick-atlas-favorites-v1';

export function readFavorites(): string[] {
  try {
    const value: unknown = JSON.parse(readLocal(FAVORITES_KEY) ?? '[]');
    return Array.isArray(value)
      ? modelCatalog.filter(model => value.includes(model.id)).map(model => model.id)
      : [];
  } catch { return []; }
}

export function saveFavorites(ids: string[]) {
  return writeLocal(FAVORITES_KEY, JSON.stringify([...new Set(ids)]));
}

export function filterCatalog(
  models: readonly ModelConfig[],
  filter: CatalogFilter,
  favorites: readonly string[],
  progress: Record<string, { completedStep: number; placedIds: string[]; completed: boolean }>,
) {
  const terms = filter.query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  return models.filter(model => {
    const text = `${model.id} ${model.title} ${model.subtitle} ${model.theme} ${model.category}`.toLocaleLowerCase();
    const saved = progress[model.id];
    return terms.every(term => text.includes(term))
      && (!filter.category || model.category === filter.category)
      && (!filter.difficulty || assemblyDifficulty(model.id) === Number(filter.difficulty))
      && (filter.status === 'all'
        || filter.status === 'favorites' && favorites.includes(model.id)
        || filter.status === 'completed' && saved?.completed
        || filter.status === 'started' && saved && !saved.completed && (saved.completedStep > 0 || saved.placedIds.length > 0));
  }).sort((a, b) => filter.sort === 'newest' ? b.year - a.year || a.id.localeCompare(b.id)
    : filter.sort === 'name' ? a.title.localeCompare(b.title)
      : assemblyDifficulty(a.id) - assemblyDifficulty(b.id) || a.title.localeCompare(b.title));
}
