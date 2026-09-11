import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { CATALOG, COLORS, type FrameSpec, type Part, type View } from '../shared';

export function viewer(canvas: HTMLCanvasElement, interactive = false) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setSize(640, 480, false);
  renderer.setClearColor('#edf1f2');
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1;
  const camera = new THREE.OrthographicCamera(-6, 6, 4.5, -4.5, 0.01, 200);
  const scene = new THREE.Scene(), group = new THREE.Group();
  scene.add(group);
  scene.add(new THREE.HemisphereLight('#ffffff', '#889598', 2));
  const light = new THREE.DirectionalLight('#ffffff', 2.4);
  light.position.set(-6, 15, 10); scene.add(light);
  const controls = interactive ? new OrbitControls(camera, canvas) : null;
  if (controls) { controls.enableDamping = false; controls.enablePan = false; }
  const render = () => { scene.updateMatrixWorld(true); renderer.render(scene, camera); };
  controls?.addEventListener('change', render);
  let center = new THREE.Vector3(), span = 8;
  const materials: THREE.Material[] = [], geometries: THREE.BufferGeometry[] = [];
  function clear() {
    group.clear(); materials.splice(0).forEach(m => m.dispose()); geometries.splice(0).forEach(g => g.dispose());
  }
  function setView(view: View) {
    camera.left = -span * 4 / 3; camera.right = span * 4 / 3; camera.top = span; camera.bottom = -span;
    const offsets: Record<View, [number, number, number]> = {
      iso: [12, 14, 16], top: [0, 25, 0.001], front: [0, 0.001, 25], side: [25, 0.001, 0],
    };
    camera.position.copy(center).add(new THREE.Vector3(...offsets[view]));
    camera.up.set(0, 1, 0); camera.lookAt(center); camera.updateProjectionMatrix(); camera.updateMatrixWorld();
    if (controls) { controls.target.copy(center); controls.update(); }
    render();
  }
  function setParts(parts: Part[], view: View = 'iso') {
    clear();
    const box = new THREE.Box3();
    const body = new THREE.BoxGeometry(1, 1, 1), stud = new THREE.CylinderGeometry(0.3, 0.3, 0.16, 20);
    geometries.push(body, stud);
    for (const p of parts) {
      const c = CATALOG[p.partId]; if (!c) continue;
      const w = p.turn % 2 ? c.d : c.w, d = p.turn % 2 ? c.w : c.d, h = c.h * 0.4;
      const material = new THREE.MeshStandardMaterial({ color: COLORS[p.color], roughness: 0.45 });
      materials.push(material);
      const mesh = new THREE.Mesh(body, material);
      mesh.scale.set(w - 0.018, h - 0.008, d - 0.018);
      mesh.position.set(p.x + w / 2, p.y * 0.4 + h / 2, p.z + d / 2);
      group.add(mesh);
      box.expandByPoint(new THREE.Vector3(p.x, p.y * 0.4, p.z));
      box.expandByPoint(new THREE.Vector3(p.x + w, p.y * 0.4 + h + 0.16, p.z + d));
      for (let x = 0; x < w; x++) for (let z = 0; z < d; z++) {
        const cap = new THREE.Mesh(stud, material);
        cap.position.set(p.x + x + 0.5, p.y * 0.4 + h + 0.08, p.z + z + 0.5);
        group.add(cap);
      }
    }
    if (box.isEmpty()) box.set(new THREE.Vector3(0, 0, 0), new THREE.Vector3(6, 2, 4));
    center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    span = Math.max(3, size.length() * 0.56 + 1);
    const gridSize = Math.ceil(Math.max(size.x, size.z, 8) + 4);
    const grid = new THREE.GridHelper(gridSize, gridSize, '#a0b2b2', '#d0dadb');
    grid.position.set(gridSize / 2 - 2, Math.max(0, box.min.y) - 0.03, gridSize / 2 - 2);
    group.add(grid); geometries.push(grid.geometry); materials.push(grid.material as THREE.Material);
    setView(view);
  }
  function png(frame: FrameSpec) {
    setParts(frame.parts, frame.view);
    const output = document.createElement('canvas'); output.width = 640; output.height = 480;
    const ctx = output.getContext('2d')!; ctx.drawImage(canvas, 0, 0);
    ctx.fillStyle = '#24464e'; ctx.font = '12px monospace'; ctx.fillText(frame.title.slice(0, 78), 12, 22);
    if (frame.view === 'top') {
      const project = (x: number, z: number) => {
        const v = new THREE.Vector3(x, center.y, z).project(camera);
        return { x: (v.x + 1) * 320, y: (1 - v.y) * 240 };
      };
      const maxX = Math.max(...frame.parts.map(p => p.x + (p.turn % 2 ? CATALOG[p.partId].d : CATALOG[p.partId].w)));
      const maxZ = Math.max(...frame.parts.map(p => p.z + (p.turn % 2 ? CATALOG[p.partId].w : CATALOG[p.partId].d)));
      ctx.textAlign = 'center';
      for (let x = 0; x < maxX; x++) { const p = project(x + 0.5, maxZ + 0.6); ctx.fillText(`${x}`, p.x, p.y); }
      for (let z = 0; z < maxZ; z++) { const p = project(-0.6, z + 0.5); ctx.fillText(`${z}`, p.x, p.y); }
      const x = project(maxX / 2, maxZ + 1.3), z = project(-1.4, maxZ / 2);
      ctx.fillText('X', x.x, x.y); ctx.fillText('Z', z.x, z.y);
    }
    ctx.textAlign = 'left'; ctx.fillText('X/Z: studs | Y: plates | origin: minimum ground corner', 12, 462);
    return output.toDataURL('image/png');
  }
  return { setParts, setView, png, dispose() { controls?.dispose(); clear(); renderer.dispose(); } };
}
