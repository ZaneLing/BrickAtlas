import * as THREE from 'three';
import { CATALOG, COLORS, type Part } from '../shared';

export interface PaperFrame {
  parts: Part[];
  frameParts?: Part[];
  explode?: number;
  highlightIds?: string[];
  view?: 'iso' | 'top' | 'front' | 'side';
}
const canvas = document.querySelector<HTMLCanvasElement>('#paper-scene')!;
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(1000, 750, false);
renderer.setClearColor('#ffffff', 1);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
const scene = new THREE.Scene(), group = new THREE.Group();
scene.add(group);
scene.add(new THREE.HemisphereLight('#ffffff', '#858585', 2.5));
const light = new THREE.DirectionalLight('#ffffff', 3);
light.position.set(-8, 16, 12); scene.add(light);
const camera = new THREE.OrthographicCamera(-8, 8, 6, -6, .01, 200);
const geometry: THREE.BufferGeometry[] = [], materials: THREE.Material[] = [];

function render(frame: PaperFrame) {
  group.clear();
  geometry.splice(0).forEach(g => g.dispose()); materials.splice(0).forEach(m => m.dispose());
  const box = new THREE.Box3(), levels = [...new Set((frame.frameParts ?? frame.parts).map(p => p.y))].sort((a, b) => a - b);
  const yOffset = (p: Part) => levels.indexOf(p.y) * (frame.explode ?? 0);
  const body = new THREE.BoxGeometry(1, 1, 1), stud = new THREE.CylinderGeometry(.30, .30, .16, 32);
  geometry.push(body, stud);
  const dimensions = (p: Part) => {
    const c = CATALOG[p.partId];
    return { w: p.turn % 2 ? c.d : c.w, d: p.turn % 2 ? c.w : c.d, h: c.h * .4 };
  };
  for (const p of frame.frameParts ?? frame.parts) {
    const { w, d, h } = dimensions(p), y = p.y * .4 + yOffset(p);
    box.expandByPoint(new THREE.Vector3(p.x, y, p.z));
    box.expandByPoint(new THREE.Vector3(p.x + w, y + h + .16, p.z + d));
  }
  for (const p of frame.parts) {
    const { w, d, h } = dimensions(p), y = p.y * .4 + yOffset(p);
    const material = new THREE.MeshStandardMaterial({ color: COLORS[p.color], roughness: .32, metalness: 0 });
    materials.push(material);
    const mesh = new THREE.Mesh(body, material);
    mesh.scale.set(w - .018, h - .008, d - .018);
    mesh.position.set(p.x + w / 2, y + h / 2, p.z + d / 2);
    group.add(mesh);
    for (let x = 0; x < w; x++) for (let z = 0; z < d; z++) {
      const cap = new THREE.Mesh(stud, material);
      cap.position.set(p.x + x + .5, y + h + .08, p.z + z + .5);
      group.add(cap);
    }
    if (frame.highlightIds?.includes(p.id)) {
      const g = new THREE.EdgesGeometry(body), m = new THREE.LineBasicMaterial({ color: '#141414' });
      geometry.push(g); materials.push(m);
      const outline = new THREE.LineSegments(g, m);
      outline.position.copy(mesh.position); outline.scale.copy(mesh.scale);
      group.add(outline);
    }
  }
  if (box.isEmpty()) box.set(new THREE.Vector3(0, 0, 0), new THREE.Vector3(8, 3, 4));
  const center = box.getCenter(new THREE.Vector3()), size = box.getSize(new THREE.Vector3());
  const offsets: Record<NonNullable<PaperFrame['view']>, [number, number, number]> = {
    iso: [12, 13, 16], top: [0, 25, .001], front: [0, .001, 25], side: [25, .001, 0],
  };
  camera.position.copy(center).add(new THREE.Vector3(...offsets[frame.view ?? 'iso']));
  camera.up.set(0, 1, 0); camera.lookAt(center); camera.updateMatrixWorld();
  // Fit the actual projected bounding corners with fixed frameParts across steps.
  const inverse = camera.matrixWorldInverse;
  let halfX = 0, halfY = 0;
  for (const x of [box.min.x, box.max.x]) for (const y of [box.min.y, box.max.y]) for (const z of [box.min.z, box.max.z]) {
    const v = new THREE.Vector3(x, y, z).applyMatrix4(inverse);
    halfX = Math.max(halfX, Math.abs(v.x)); halfY = Math.max(halfY, Math.abs(v.y));
  }
  const span = Math.max(.5, halfY, halfX / (4 / 3)) * 1.10;
  camera.left = -span * 4 / 3; camera.right = span * 4 / 3; camera.top = span; camera.bottom = -span;
  camera.updateProjectionMatrix();
  scene.updateMatrixWorld(true); renderer.render(scene, camera);
  return { png: canvas.toDataURL('image/png'), parts: frame.parts.length, size: size.toArray() };
}
declare global { interface Window { atlasPaperRender: typeof render } }
window.atlasPaperRender = render;
