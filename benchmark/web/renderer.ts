import * as THREE from 'three';
import { CATALOG, COLORS } from '../shared/catalog';
import type { Brick, View } from '../shared/types';

const canvas = document.querySelector<HTMLCanvasElement>('#scene')!;
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(640, 480);
renderer.setPixelRatio(1);
renderer.setClearColor('#edf1f2');
renderer.outputColorSpace = THREE.SRGBColorSpace;
const camera = new THREE.OrthographicCamera(-5.5 * 4 / 3, 5.5 * 4 / 3, 5.5, -5.5, 0.1, 100);
const bodyGeometry = new THREE.BoxGeometry(1, 1, 1);
const studGeometry = new THREE.CylinderGeometry(0.3, 0.3, 0.16, 24);
const composite = document.createElement('canvas');
composite.width = 640;
composite.height = 480;
const ctx = composite.getContext('2d')!;
const raycaster = new THREE.Raycaster();

export function renderScene(parts: Brick[], view: View, labels: string[] = []) {
  const scene = new THREE.Scene();
  scene.add(new THREE.HemisphereLight('#ffffff', '#7d8990', 2.8));
  const light = new THREE.DirectionalLight('#ffffff', 3);
  light.position.set(-4, 12, 8);
  scene.add(light);
  const grid = new THREE.GridHelper(16, 16, '#7e9495', '#ced8d9');
  grid.position.set(3, -0.025, 3);
  scene.add(grid);
  const materials: THREE.Material[] = [];
  const meshes: THREE.Mesh[] = [];
  const centers = new Map<string, THREE.Vector3>();
  parts.forEach(part => {
    const item = CATALOG[part.partId as keyof typeof CATALOG];
    if (!item) return;
    const w = part.turn % 2 ? item.depth : item.width;
    const d = part.turn % 2 ? item.width : item.depth;
    const h = item.height * 0.4;
    const material = new THREE.MeshStandardMaterial({
      color: COLORS[part.color], roughness: 0.32, metalness: 0.02,
    });
    materials.push(material);
    const body = new THREE.Mesh(bodyGeometry, material);
    body.scale.set(w - 0.025, h - 0.012, d - 0.025);
    body.position.set(part.x + w / 2, part.y * 0.4 + h / 2, part.z + d / 2);
    body.userData.id = part.id;
    centers.set(part.id, body.position.clone());
    scene.add(body);
    meshes.push(body);
    for (let x = 0; x < w; x++) for (let z = 0; z < d; z++) {
      const stud = new THREE.Mesh(studGeometry, material);
      stud.position.set(part.x + x + 0.5, (part.y + item.height) * 0.4 + 0.08, part.z + z + 0.5);
      stud.userData.id = part.id;
      scene.add(stud);
      meshes.push(stud);
    }
  });
  const target = new THREE.Vector3(3, 0.8, 3);
  const directions: Record<View, THREE.Vector3> = {
    iso: new THREE.Vector3(9, 10, 12), top: new THREE.Vector3(0, 16, 0.001),
    front: new THREE.Vector3(0, 7, 14), back: new THREE.Vector3(0, 7, -14),
  };
  camera.position.copy(target).add(directions[view]);
  camera.up.set(0, 1, 0);
  camera.lookAt(target);
  camera.updateMatrixWorld();
  scene.updateMatrixWorld(true);
  renderer.render(scene, camera);
  ctx.drawImage(canvas, 0, 0);
  ctx.font = '12px monospace';
  ctx.textAlign = 'center';
  const project = (p: THREE.Vector3) => {
    const ndc = p.clone().project(camera);
    return { x: (ndc.x + 1) * 320, y: (1 - ndc.y) * 240, ndc };
  };
  for (let i = 0; i <= 6; i++) {
    const px = project(new THREE.Vector3(i + 0.5, 0, 7.3));
    const pz = project(new THREE.Vector3(-1.1, 0, i + 0.5));
    ctx.fillStyle = '#33494e';
    ctx.fillText(String(i), px.x, px.y);
    ctx.fillText(String(i), pz.x, pz.y);
  }
  const xAxis = project(new THREE.Vector3(3.5, 0, 8.1));
  const zAxis = project(new THREE.Vector3(-1.8, 0, 3.5));
  ctx.fillText('X', xAxis.x, xAxis.y);
  ctx.fillText('Z', zAxis.x, zAxis.y);
  for (const [id, center] of centers) {
    if (!labels.includes(id)) continue;
    const p = project(center);
    raycaster.setFromCamera(new THREE.Vector2(p.ndc.x, p.ndc.y), camera);
    const first = raycaster.intersectObjects(meshes, false)[0];
    if (first?.object.userData.id !== id) continue;
    const width = ctx.measureText(id).width + 12;
    ctx.fillStyle = '#ffffffed';
    ctx.fillRect(p.x - width / 2, p.y - 11, width, 19);
    ctx.fillStyle = '#1d363c';
    ctx.fillText(id, p.x, p.y + 3);
  }
  ctx.textAlign = 'left';
  ctx.fillStyle = '#28434a';
  ctx.fillText(`${view.toUpperCase()}   X/Z: studs   Y: plates`, 16, 24);
  ctx.textAlign = 'right';
  ctx.fillText('0,0 = base minimum corner', 624, 462);
  const url = composite.toDataURL('image/png');
  materials.forEach(m => m.dispose());
  grid.geometry.dispose();
  (grid.material as THREE.Material).dispose();
  return url;
}

declare global {
  interface Window { careRender: typeof renderScene }
}
window.careRender = renderScene;
