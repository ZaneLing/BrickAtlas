import type { AtlasScene } from '../scene/AtlasScene';

/** The on-screen labels and exported labels share the same drawing path. */
export class NumberedOverlay {
  readonly canvas = document.createElement('canvas');
  private frame = 0;
  private ids: string[] = [];
  constructor(private host: HTMLElement, private scene: AtlasScene) {
    this.canvas.className = 'ldraw-number-overlay';
    this.canvas.setAttribute('aria-hidden', 'true');
    host.appendChild(this.canvas);
    this.frame = requestAnimationFrame(this.tick);
  }
  setIds(ids: string[]) { this.ids = [...new Set(ids)]; }
  private tick = () => {
    const w = this.host.clientWidth, h = this.host.clientHeight;
    const ratio = Math.min(devicePixelRatio || 1, 2);
    if (this.canvas.width !== Math.round(w * ratio) || this.canvas.height !== Math.round(h * ratio)) {
      this.canvas.width = Math.round(w * ratio); this.canvas.height = Math.round(h * ratio);
    }
    const ctx = this.canvas.getContext('2d')!;
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0); ctx.clearRect(0, 0, w, h);
    ctx.font = 'bold 12px ui-monospace, monospace'; ctx.textBaseline = 'middle';
    const occupied: Array<{ x: number; y: number }> = [];
    for (const id of this.ids) {
      const part = this.scene.manifest.instances.find(p => p.instanceId === id);
      if (!part) continue;
      const p = this.scene.projectPart(part);
      if (p.z < -1 || p.z > 1 || p.x < 0 || p.x > w || p.y < 0 || p.y > h) continue;
      let x = Math.max(5, Math.min(w - 66, p.x + 12));
      let y = Math.max(55, Math.min(h - 17, p.y - 18));
      for (let i = 0; i < occupied.length + 1; i++) {
        if (!occupied.some(o => Math.abs(o.x - x) < 66 && Math.abs(o.y - y) < 24)) break;
        y += 25;
        if (y > h - 17) { y = 55; x = Math.max(5, x - 70); }
      }
      occupied.push({ x, y });
      ctx.strokeStyle = '#1c4165'; ctx.lineWidth = 1.4; ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(x, y); ctx.stroke();
      ctx.fillStyle = '#17639a'; ctx.beginPath(); ctx.arc(p.x, p.y, 3, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#ffffffee'; ctx.fillRect(x - 3, y - 10, 59, 21);
      ctx.strokeRect(x - 3, y - 10, 59, 21);
      ctx.fillStyle = '#163a5b'; ctx.fillText(`B${String(part.index + 1).padStart(4, '0')}`, x + 1, y + .5);
    }
    this.frame = requestAnimationFrame(this.tick);
  };
  capture() {
    const source = this.scene.renderer.domElement;
    const canvas = document.createElement('canvas');
    canvas.width = source.width; canvas.height = source.height;
    const ctx = canvas.getContext('2d')!;
    ctx.drawImage(source, 0, 0);
    ctx.drawImage(this.canvas, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/png');
  }
  dispose() { cancelAnimationFrame(this.frame); this.canvas.remove(); }
}
