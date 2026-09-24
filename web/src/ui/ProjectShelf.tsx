import { useState } from 'react';
import { FolderOpen, Save, Trash2 } from 'lucide-react';
import type { Translator } from '../app/locale';
import { readSnapshots, removeSnapshot, saveSnapshot, snapshotKey, type ProjectSnapshot } from '../app/projectSnapshots';
import { IconButton, Modal } from './Controls';

export function ProjectShelf({ space, name, serialize, restore, tr }: {
  space: 'diy' | 'compose'; name: string; serialize: () => string;
  restore: (text: string) => void; tr: Translator;
}) {
  const [open, setOpen] = useState(false);
  const [snapshots, setSnapshots] = useState<ProjectSnapshot[]>([]);
  const [pending, setPending] = useState<{ item: ProjectSnapshot; action: 'open' | 'delete' } | null>(null);
  const [error, setError] = useState('');
  const key = snapshotKey(space);
  const refresh = () => setSnapshots(readSnapshots(key));
  return <>
    <IconButton label={tr('作品快照', 'Project snapshots')} onClick={() => { refresh(); setOpen(true); setError(''); }}><FolderOpen size={18} /></IconButton>
    {open && <Modal title={tr('作品快照', 'Project snapshots')} onClose={() => { setOpen(false); setPending(null); }}>
      <div className="project-shelf">
        <button className="primary-button" disabled={snapshots.length >= 8} onClick={() => {
          if (saveSnapshot(key, name, serialize())) { refresh(); setError(''); }
          else setError(tr('快照保存失败，容量不足。请导出 JSON 备份。', 'Snapshot could not be saved. Export JSON as a backup.'));
        }}><Save size={16} />{tr('保存当前作品快照', 'Save current snapshot')}<span>{snapshots.length} / 8</span></button>
        {!snapshots.length && <p>{tr('暂无快照', 'No snapshots yet')}</p>}
        {snapshots.map(item => <div className="project-shelf-row" key={item.id}>
          <div><strong>{item.name}</strong><small>{new Date(item.savedAt).toLocaleString()}</small></div>
          <IconButton label={tr(`打开快照 ${item.name}`, `Open snapshot ${item.name}`)} onClick={() => setPending({ item, action: 'open' })}><FolderOpen size={17} /></IconButton>
          <IconButton label={tr(`删除快照 ${item.name}`, `Delete snapshot ${item.name}`)} onClick={() => setPending({ item, action: 'delete' })}><Trash2 size={17} /></IconButton>
        </div>)}
        {pending && <div className="snapshot-confirm" role="alert">
          <p>{pending.action === 'open'
            ? tr(`打开「${pending.item.name}」？替换当前作品，可撤销。`, `Open "${pending.item.name}"? This replaces the current project and can be undone.`)
            : tr(`删除「${pending.item.name}」？此快照无法恢复。`, `Delete "${pending.item.name}"? This snapshot cannot be recovered.`)}</p>
          <button className="primary-button" onClick={() => {
            try {
              if (pending.action === 'open') { restore(pending.item.data); setOpen(false); }
              else if (!removeSnapshot(key, pending.item.id)) throw new Error('storage');
              refresh(); setPending(null); setError('');
            } catch { setError(tr('操作失败，原作品已保留。', 'Operation failed. The current project is preserved.')); }
          }}>{tr('确认', 'Confirm')}</button>
          <button className="text-button" onClick={() => setPending(null)}>{tr('取消', 'Cancel')}</button>
        </div>}
        {error && <p role="alert">{error}</p>}
      </div>
    </Modal>}
  </>;
}
