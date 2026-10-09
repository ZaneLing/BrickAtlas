import { useEffect, useRef, useState } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { Maximize2, X, RotateCcw, Box, Image as ImageIcon } from 'lucide-react';
import type { Images, Raster, SceneData } from './types';
import type { BrickSceneController } from './BrickSceneController';
import { asset, publicJSON } from './api';
import s from './Workbench.module.css';

export function JSONView({ value, title = '原始 JSON / Raw JSON' }: { value: unknown; title?: string }) {
  return <details className={s.details}><summary>{title}</summary><pre>{publicJSON(value)}</pre></details>;
}
export function RasterView({ raster, title }: { raster?: Raster; title: string }) {
  const [native, setNative] = useState(false);
  if (!raster) return <div className={s.empty}>图像尚未载入 / Image unavailable</div>;
  const url = raster.url ? asset(raster.url) : `data:${raster.mime};base64,${raster.base64}`;
  return <Dialog.Root>
    <Dialog.Trigger asChild><button className={s.rasterButton} aria-label={`放大 ${title}`}><img src={url} alt={title} /><span><Maximize2 size={13} /> {raster.width} × {raster.height}</span></button></Dialog.Trigger>
    <Dialog.Portal><Dialog.Overlay className={s.overlay} /><Dialog.Content className={s.imageDialog}>
      <div className={s.dialogTop}><Dialog.Title>{title} · {raster.width} × {raster.height}</Dialog.Title>
        <button onClick={() => setNative(!native)}>{native ? '适应窗口 Fit' : '原生像素 1:1'}</button><Dialog.Close aria-label="关闭 Close"><X size={18} /></Dialog.Close></div>
      <Dialog.Description className={s.srOnly}>Original benchmark image. Scroll at native resolution.</Dialog.Description>
      <div className={s.zoomScroll}><img className={native ? s.native : s.fit} src={url} alt={title} /></div>
    </Dialog.Content></Dialog.Portal>
  </Dialog.Root>;
}
function Scene({ data, mask, selected, onSelect, explode, labels, preset, reset }: {
  data: SceneData; mask: number; selected: string; onSelect: (id: string) => void; explode: number; labels: boolean; preset: string; reset: number;
}) {
  const host = useRef<HTMLDivElement>(null), controller = useRef<BrickSceneController | null>(null);
  const selection = useRef(onSelect); selection.current = onSelect;
  const [error, setError] = useState('');
  useEffect(() => {
    let active = true; setError('');
    import('./BrickSceneController').then(({ BrickSceneController }) => {
      if (!active || !host.current) return;
      try {
        controller.current = new BrickSceneController(host.current, data, id => selection.current(id));
        controller.current.show(mask, explode, labels, selected);
      } catch { setError('此环境无法使用 WebGL2，请切换到高清图。 WebGL2 unavailable; use HD images.'); }
    });
    return () => { active = false; controller.current?.dispose(); controller.current = null; };
  }, [data]);
  useEffect(() => { controller.current?.show(mask, explode, labels, selected); }, [mask, explode, labels, selected]);
  useEffect(() => { controller.current?.preset(preset); }, [preset, reset]);
  return <div className={s.scene} ref={host} data-mask={mask}>{error && <p className={s.sceneError}>{error}</p>}</div>;
}
export function Visuals({ data, images, frame, selected = '', onSelect = () => {}, study = false, title = '当前结构 Current', targetTitle = '目标结构 Target' }: {
  data?: SceneData; images?: Images; frame?: number; selected?: string; onSelect?: (id: string) => void; study?: boolean; title?: string; targetTitle?: string;
}) {
  const [mode, setMode] = useState('3d'), [labels, setLabels] = useState(true), [explode, setExplode] = useState(0);
  const [preset, setPreset] = useState('isometric'), [reset, setReset] = useState(0);
  const show3d = mode === '3d' && !study && !!data;
  const mask = data?.frames[frame ?? data.revision]?.assembly ?? data?.current.assembly ?? 0;
  return <section className={s.visuals} aria-label="Assembly comparison">
    <div className={s.visualToolbar}>
      <div className={s.segment}>
        {!study && <button aria-pressed={mode === '3d'} onClick={() => setMode('3d')}><Box size={14} /> 自由 3D</button>}
        <button aria-pressed={mode === 'raster' || study} onClick={() => setMode('raster')}><ImageIcon size={14} /> 高清图 HD</button>
      </div>
      {show3d && <div className={s.inline}>
        <select aria-label="3D camera preset" value={preset} onChange={e => setPreset(e.target.value)}>{['isometric', 'front', 'rear', 'left', 'right', 'top', 'bottom'].map(v => <option key={v}>{v}</option>)}</select>
        <button aria-label="重置相机 Reset camera" onClick={() => setReset(n => n + 1)}><RotateCcw size={14} /></button>
        <label><input type="checkbox" checked={labels} onChange={e => setLabels(e.target.checked)} /> IDs</label>
        <label>展开<input aria-label="Explode diagram" type="range" min="0" max="100" value={explode} onChange={e => setExplode(+e.target.value)} /></label>
      </div>}
    </div>
    <div className={s.comparison} data-render-mode={show3d ? 'webgl2' : 'raster'}>
      {['current', 'target'].map((name, i) => <div className={s.viewport} key={name}>
        <div className={s.viewportTitle}><span className={i ? s.targetDot : s.currentDot} />{i ? targetTitle : title}<span>{show3d ? 'WEBGL 2' : '1920 × 1440'}</span></div>
        {show3d ? <Scene data={data!} mask={i ? data!.goal : mask} selected={selected} onSelect={onSelect} explode={explode / 100} labels={labels} preset={preset} reset={reset} /> : <RasterView raster={images?.[name]} title={i ? targetTitle : title} />}
      </div>)}
    </div>
    <div className={s.visualNote}>{show3d ? explode > 0 ? '展开示意图 · 非可执行装配状态 / Exploded diagram only' : '拖动旋转 · 滚轮缩放 · 右键平移 · 点击零件选择 ID / Original source poses' : '评测原始图像 · 点击放大，支持 1:1 像素查看 / Native benchmark evidence'}</div>
    {images && <details className={s.details}><summary>暂存架、位置对照与零件目录 / Rack · site reference · catalog</summary>
      <div className={s.supportImages}>{['rack', 'siteReference', 'catalog'].map(name => <div key={name}><h4>{name}</h4><RasterView raster={images[name]} title={name} /></div>)}</div>
    </details>}
  </section>;
}
