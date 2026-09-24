import { useEffect, useRef, type PointerEvent as ReactPointerEvent } from 'react';
import { Crop, ImagePlus, Maximize2, X } from 'lucide-react';
import type { Translator } from '../app/locale';

export type ImageViewRole = 'front' | 'left' | 'back' | 'right';
export interface CropRect {
  x: number;
  y: number;
  size: number;
}
export interface ImageSource {
  file: File;
  url: string;
  width: number;
  height: number;
  crop: CropRect;
  fit: boolean;
}

export function centeredSquare(width: number, height: number): CropRect {
  const size = Math.min(width, height);
  return { x: (width - size) / 2, y: (height - size) / 2, size };
}

export function ImageCropEditor({
  role,
  source,
  onFile,
  onCrop,
  onFit,
  onRemove,
  tr,
}: {
  role: ImageViewRole;
  source?: ImageSource;
  onFile: (file?: File) => void;
  onCrop: (crop: CropRect) => void;
  onFit: (fit: boolean) => void;
  onRemove: () => void;
  tr: Translator;
}) {
  const frameRef = useRef<HTMLDivElement>(null);
  const cancelDrag = useRef<(() => void) | null>(null);
  useEffect(() => () => cancelDrag.current?.(), []);
  const labels = {
    front: tr('正视图', 'Front'),
    left: tr('左侧', 'Left'),
    back: tr('背面', 'Back'),
    right: tr('右侧', 'Right'),
  };

  function startDrag(event: ReactPointerEvent, mode: 'move' | 'resize') {
    if (!source || !frameRef.current) return;
    event.preventDefault();
    event.stopPropagation();
    cancelDrag.current?.();
    const bounds = frameRef.current.getBoundingClientRect();
    const startX = event.clientX;
    const startY = event.clientY;
    const origin = source.fit ? centeredSquare(source.width, source.height) : source.crop;
    if (source.fit) onFit(false);
    const move = (pointer: PointerEvent) => {
      const dx = (pointer.clientX - startX) / bounds.width * source.width;
      const dy = (pointer.clientY - startY) / bounds.height * source.height;
      if (mode === 'move') {
        onCrop({
          ...origin,
          x: Math.max(0, Math.min(source.width - origin.size, origin.x + dx)),
          y: Math.max(0, Math.min(source.height - origin.size, origin.y + dy)),
        });
        return;
      }
      const maximum = Math.min(source.width - origin.x, source.height - origin.y);
      const minimum = Math.min(maximum, Math.max(1, Math.min(source.width, source.height) * 0.18));
      const size = Math.max(
        minimum,
        Math.min(
          Math.min(source.width - origin.x, source.height - origin.y),
          origin.size + Math.max(dx, dy),
        ),
      );
      onCrop({ ...origin, size });
    };
    const finish = () => {
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerup', finish);
      window.removeEventListener('pointercancel', finish);
    };
    cancelDrag.current = finish;
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', finish);
    window.addEventListener('pointercancel', finish);
  }

  const cropStyle = source?.fit ? {
    left: '0',
    top: '0',
    width: '100%',
    height: '100%',
  } : source ? {
    left: `${source.crop.x / source.width * 100}%`,
    top: `${source.crop.y / source.height * 100}%`,
    width: `${source.crop.size / source.width * 100}%`,
    height: `${source.crop.size / source.height * 100}%`,
  } : undefined;

  const inputId = `image-view-${role}`;
  return <section className={`crop-source ${source ? 'has-source' : ''}`} aria-label={tr(`${labels[role]}裁剪`, `${labels[role]} crop`)}>
    <header>
      <span>{labels[role]}</span>
      <label htmlFor={inputId}>{source ? tr('更换', 'Replace') : role === 'front' ? tr('必需', 'Required') : tr('可选', 'Optional')}</label>
    </header>
    <div
      className="crop-source-frame"
      ref={frameRef}
      style={source ? { aspectRatio: `${source.width} / ${source.height}`, width: `min(100%, ${170 * source.width / source.height}px)` } : undefined}
    >
      {source ? <>
        <img src={source.url} alt={tr(`${labels[role]}原图`, `${labels[role]} source`)} />
        <span className="crop-shade" aria-hidden="true" />
        <span
          className="crop-selection"
          style={cropStyle}
          onPointerDown={event => startDrag(event, 'move')}
          onClick={event => { event.preventDefault(); event.stopPropagation(); }}
        >
          <Crop size={13} />
          <i
            aria-hidden="true"
            onPointerDown={event => startDrag(event, 'resize')}
            onClick={event => { event.preventDefault(); event.stopPropagation(); }}
          ><Maximize2 size={11} /></i>
        </span>
      </> : <label htmlFor={inputId} className="crop-empty"><ImagePlus size={20} />{tr('添加图片', 'Add image')}</label>}
      <input
        id={inputId}
        aria-label={tr(`上传${labels[role]}`, `Upload ${labels[role].toLowerCase()} view`)}
        type="file"
        accept="image/png,image/jpeg,image/webp"
        onChange={event => { onFile(event.target.files?.[0]); event.target.value = ''; }}
      />
    </div>
    {source && <footer>
      <span>{source.file.name}</span>
      <span className="crop-source-actions">
        <button type="button" onClick={() => onFit(true)}>{tr('完整图片', 'Full image')}</button>
        <button type="button" aria-label={tr(`移除${labels[role]}`, `Remove ${labels[role].toLowerCase()} view`)} onClick={onRemove}><X size={11} /></button>
      </span>
    </footer>}
  </section>;
}
