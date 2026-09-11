import { viewer } from './viewer';
import type { FrameSpec } from '../shared';
const scene = viewer(document.querySelector<HTMLCanvasElement>('#scene')!);
declare global { interface Window { atlasRender: (frame: FrameSpec) => string } }
window.atlasRender = frame => scene.png(frame);
