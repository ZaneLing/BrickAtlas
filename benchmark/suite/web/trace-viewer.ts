import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { CATALOG, COLORS, type Part, type View } from '../shared';

export interface CameraPose { position: number[]; target: number[]; zoom: number }
export interface Overlay { warningIds: string[]; missing: Part[]; edges: boolean }
const dimensions = (p: Part) => {
  const s = CATALOG[p.partId];
  return { w: p.turn % 2 ? s.d : s.w, d: p.turn % 2 ? s.w : s.d, h: s.h };
};
export function traceViewer(canvas: HTMLCanvasElement, onCamera: (pose: CameraPose) => void) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setSize(640, 480, false); renderer.setClearColor('#edf1f2');
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  const scene = new THREE.Scene(), objects = new THREE.Group();
  scene.add(objects, new THREE.HemisphereLight('#ffffff', '#7f9594', 2));
  const sun = new THREE.DirectionalLight('#ffffff', 2.4); sun.position.set(-6, 14, 12); scene.add(sun);
  const camera = new THREE.OrthographicCamera(-8, 8, 6, -6, 0.01, 300);
  const controls = new OrbitControls(camera, canvas);
  controls.enablePan = false;
  let muting = false, fitted = '', center = new THREE.Vector3();
  const materials: THREE.Material[] = [], geometries: THREE.BufferGeometry[] = [];
  const draw = () => renderer.render(scene, camera);
  const pose = (): CameraPose => ({ position: camera.position.toArray(), target: controls.target.toArray(), zoom: camera.zoom });
  controls.addEventListener('change', () => { draw(); if (!muting) onCamera(pose()); });
  function setPose(p: CameraPose) {
    muting = true; camera.position.fromArray(p.position); camera.zoom = p.zoom;
    controls.target.fromArray(p.target); camera.updateProjectionMatrix(); controls.update();
    muting = false; draw();
  }
  function setView(view: View) {
    const offset: Record<View, number[]> = { iso: [14, 16, 18], top: [0, 30, 0.001], front: [0, 0.001, 30], side: [30, 0.001, 0] };
    setPose({ position: center.clone().add(new THREE.Vector3().fromArray(offset[view])).toArray(),
      target: center.toArray(), zoom: 1 });
  }
  function update(parts: Part[], frame: Part[], overlay: Overlay) {
    objects.clear(); materials.splice(0).forEach(m => m.dispose()); geometries.splice(0).forEach(g => g.dispose());
    const box = new THREE.Box3();
    for (const p of frame) {
      const d = dimensions(p);
      box.expandByPoint(new THREE.Vector3(p.x, p.y * 0.4, p.z));
      box.expandByPoint(new THREE.Vector3(p.x + d.w, (p.y + d.h) * 0.4 + 0.2, p.z + d.d));
    }
    if (box.isEmpty()) box.set(new THREE.Vector3(0, 0, 0), new THREE.Vector3(6, 3, 6));
    const signature = JSON.stringify([box.min.toArray(), box.max.toArray()]);
    if (signature !== fitted) {
      fitted = signature; center = box.getCenter(new THREE.Vector3());
      const extent = Math.max(3, box.getSize(new THREE.Vector3()).length() * 0.58);
      camera.left = -extent * 4 / 3; camera.right = extent * 4 / 3; camera.top = extent; camera.bottom = -extent;
      setView('iso');
    }
    const body = new THREE.BoxGeometry(1, 1, 1), stud = new THREE.CylinderGeometry(0.3, 0.3, 0.16, 18);
    geometries.push(body, stud);
    function add(p: Part, ghost: boolean) {
      const d = dimensions(p), warning = overlay.warningIds.includes(p.id);
      const material = new THREE.MeshStandardMaterial({ color: ghost ? '#c34e46' : COLORS[p.color],
        roughness: 0.45, transparent: ghost, opacity: ghost ? 0.2 : 1,
        emissive: warning ? '#581c16' : '#000000', emissiveIntensity: warning ? 0.35 : 0 });
      materials.push(material);
      const mesh = new THREE.Mesh(body, material);
      mesh.scale.set(d.w - 0.02, d.h * 0.4 - 0.012, d.d - 0.02);
      mesh.position.set(p.x + d.w / 2, p.y * 0.4 + d.h * 0.2, p.z + d.d / 2); objects.add(mesh);
      if (ghost || warning) {
        const edge = new THREE.EdgesGeometry(body), lineMat = new THREE.LineBasicMaterial({ color: '#c44238' });
        geometries.push(edge); materials.push(lineMat);
        const line = new THREE.LineSegments(edge, lineMat); line.position.copy(mesh.position); line.scale.copy(mesh.scale);
        objects.add(line);
      }
      if (!ghost) for (let x = 0; x < d.w; x++) for (let z = 0; z < d.d; z++) {
        const cap = new THREE.Mesh(stud, material);
        cap.position.set(p.x + x + 0.5, (p.y + d.h) * 0.4 + 0.08, p.z + z + 0.5); objects.add(cap);
      }
    }
    parts.forEach(p => add(p, false)); overlay.missing.forEach(p => add(p, true));
    if (overlay.edges) {
      const endpoints: THREE.Vector3[] = [];
      for (let i = 0; i < parts.length; i++) for (const b of parts.slice(i + 1)) {
        const a = parts[i], ad = dimensions(a), bd = dimensions(b);
        if ((a.y + ad.h === b.y || b.y + bd.h === a.y) && a.x < b.x + bd.w && a.x + ad.w > b.x
          && a.z < b.z + bd.d && a.z + ad.d > b.z) {
          for (const p of [a, b]) { const d = dimensions(p); endpoints.push(new THREE.Vector3(p.x + d.w / 2, p.y * 0.4 + d.h * 0.2, p.z + d.d / 2)); }
        }
      }
      const geometry = new THREE.BufferGeometry().setFromPoints(endpoints), material = new THREE.LineBasicMaterial({ color: '#232eaa', depthTest: false });
      geometries.push(geometry); materials.push(material);
      const lines = new THREE.LineSegments(geometry, material); lines.renderOrder = 10; objects.add(lines);
    }
    const grid = new THREE.GridHelper(32, 32, '#bbc9c6', '#d4dfdc'); grid.position.set(12, -0.04, 12);
    geometries.push(grid.geometry); materials.push(grid.material as THREE.Material); objects.add(grid);
    draw();
  }
  return { update, setPose, setView, dispose() {
    controls.dispose(); materials.forEach(m => m.dispose()); geometries.forEach(g => g.dispose()); renderer.dispose();
  } };
}
