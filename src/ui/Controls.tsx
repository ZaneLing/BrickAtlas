import { useEffect, useRef, type ReactNode, type ButtonHTMLAttributes } from 'react';
import { X } from 'lucide-react';

export function IconButton({ label, children, active, ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { label: string; children: ReactNode; active?: boolean }) {
  return <button {...props} className={`icon-button ${active ? 'active' : ''} ${props.className ?? ''}`} title={label} aria-label={label} aria-pressed={active}>{children}</button>;
}

export function Modal({ title, onClose, children }: { title: string; onClose: () => void; children: ReactNode }) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    const dialog = ref.current!;
    dialog.showModal();
    return () => dialog.close();
  }, []);
  return <dialog ref={ref} aria-label={title} onCancel={onClose} onClick={e => { if (e.target === ref.current) onClose(); }} className="modal">
    <div className="modal-inner">
      <header><h2>{title}</h2><IconButton label={localStorage.getItem('brick-atlas-locale') === 'en' ? 'Close dialog' : '关闭弹窗'} onClick={onClose}><X size={18} /></IconButton></header>
      {children}
    </div>
  </dialog>;
}
