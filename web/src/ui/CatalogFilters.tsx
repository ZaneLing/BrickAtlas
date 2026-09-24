import { Search, X } from 'lucide-react';
import { modelCatalog } from '../../atlas.config';
import { localCategory, type Locale, type Translator } from '../app/locale';
import { defaultCatalogFilter, type CatalogFilter } from '../app/catalog';
import { IconButton } from './Controls';

export function CatalogFilters({ filter, onChange, count, locale, tr }: {
  filter: CatalogFilter;
  onChange: (filter: CatalogFilter) => void;
  count: number;
  locale: Locale;
  tr: Translator;
}) {
  const patch = (value: Partial<CatalogFilter>) => onChange({ ...filter, ...value });
  return <section className="catalog-filters" aria-label={tr('模型筛选', 'Model filters')}>
    <label className="catalog-search"><Search size={17} /><input type="search"
      aria-label={tr('搜索模型', 'Search models')} placeholder={tr('模型名称、编号或主题', 'Model name, number or theme')}
      value={filter.query} onChange={event => patch({ query: event.target.value })} /></label>
    <select aria-label={tr('模型分类', 'Model category')} value={filter.category} onChange={event => patch({ category: event.target.value })}>
      <option value="">{tr('全部分类', 'All categories')}</option>
      {[...new Set(modelCatalog.map(model => model.category))].map(category => <option key={category} value={category}>{localCategory(locale, category)}</option>)}
    </select>
    <select aria-label={tr('模型难度', 'Model difficulty')} value={filter.difficulty} onChange={event => patch({ difficulty: event.target.value })}>
      <option value="">{tr('全部难度', 'All levels')}</option>
      {[1, 2, 3, 4, 5].map(level => <option key={level} value={level}>{tr(`难度 ${level}`, `Level ${level}`)}</option>)}
    </select>
    <select aria-label={tr('游玩状态', 'Play status')} value={filter.status} onChange={event => patch({ status: event.target.value as CatalogFilter['status'] })}>
      <option value="all">{tr('全部模型', 'All models')}</option><option value="favorites">{tr('我的收藏', 'Favorites')}</option>
      <option value="started">{tr('进行中', 'In progress')}</option><option value="completed">{tr('已完成', 'Completed')}</option>
    </select>
    <select aria-label={tr('模型排序', 'Model order')} value={filter.sort} onChange={event => patch({ sort: event.target.value as CatalogFilter['sort'] })}>
      <option value="recommended">{tr('从易到难', 'Easy to advanced')}</option><option value="name">{tr('名称排序', 'Name')}</option><option value="newest">{tr('年份倒序', 'Newest')}</option>
    </select>
    <IconButton label={tr('重置筛选', 'Reset filters')} onClick={() => onChange(defaultCatalogFilter)}><X size={16} /></IconButton>
    <output aria-live="polite">{count} {tr('个模型', 'models')}</output>
  </section>;
}
