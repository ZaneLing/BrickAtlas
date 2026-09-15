import * as THREE from 'three';

interface Frame {
  model: any;
  highlightModules?: string[];
  view?: 'iso' | 'front' | 'side' | 'top';
  accessPaths?: Array<{ start: [number, number, number]; end: [number, number, number]; accessible?: boolean }>;
  force?: { moduleId: string; vector: [number, number, number] };
}

const canvas = document.querySelector<HTMLCanvasElement>('#mechanism-scene')!;
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(1200, 900, false);
renderer.setClearColor('#f4f6f7', 1);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const scene = new THREE.Scene(), root = new THREE.Group();
scene.add(root);
scene.add(new THREE.HemisphereLight('#ffffff', '#60707a', 2.4));
const key = new THREE.DirectionalLight('#ffffff', 3.4);
key.position.set(-12, 22, 18); key.castShadow = true; scene.add(key);
const fill = new THREE.DirectionalLight('#b9d7ee', 1.6);
fill.position.set(16, 10, -10); scene.add(fill);
const ground = new THREE.Mesh(new THREE.PlaneGeometry(80, 80),
  new THREE.MeshStandardMaterial({ color: '#e8ecee', roughness: .95 }));
ground.rotation.x = -Math.PI / 2; ground.position.y = -.02; ground.receiveShadow = true; scene.add(ground);
const camera = new THREE.OrthographicCamera(-12, 12, 9, -9, .01, 300);
const disposable: Array<THREE.BufferGeometry | THREE.Material> = [];

function wedgeGeometry() {
  const vertices = new Float32Array([
    -.5, -.5, -.5, .5, -.5, -.5, .5, -.5, .5, -.5, -.5, .5,
    -.5, .5, .5, -.5, .5, -.5,
  ]);
  const indices = [0, 1, 2, 0, 2, 3, 0, 4, 5, 0, 3, 4, 3, 2, 4, 2, 1, 4, 1, 5, 4, 0, 5, 1];
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
  geometry.setIndex(indices); geometry.computeVertexNormals();
  return geometry;
}

function geometryFor(part: any) {
  const [x, y, z] = part.size;
  if (part.shape === 'sphere') return new THREE.SphereGeometry(Math.max(x, y, z) / 2, 32, 20);
  if (part.shape === 'slope') return wedgeGeometry();
  if (part.shape === 'arch') return new THREE.TorusGeometry(Math.max(x, z) * .33, Math.min(x, y, z) * .18, 12, 32, Math.PI);
  if (['cylinder', 'wheel', 'axle', 'gear'].includes(part.shape)) {
    return new THREE.CylinderGeometry(Math.max(x, z) / 2, Math.max(x, z) / 2, y, part.shape === 'gear' ? 20 : 32);
  }
  return new THREE.BoxGeometry(x, y, z);
}

function addStuds(group: THREE.Group, part: any, material: THREE.Material) {
  if (!['brick', 'plate'].includes(part.shape)) return;
  const [x, y, z] = part.size, nx = Math.max(1, Math.round(x)), nz = Math.max(1, Math.round(z));
  const stud = new THREE.CylinderGeometry(.22, .22, .12, 20);
  disposable.push(stud);
  for (let ix = 0; ix < nx; ix++) for (let iz = 0; iz < nz; iz++) {
    const mesh = new THREE.Mesh(stud, material);
    mesh.position.set((ix + .5) * x / nx - x / 2, y / 2 + .06, (iz + .5) * z / nz - z / 2);
    mesh.castShadow = true; group.add(mesh);
  }
}

function render(frame: Frame) {
  root.clear(); disposable.splice(0).forEach(item => item.dispose());
  const highlight = new Set(frame.highlightModules ?? []);
  const moduleGroups = new Map<string, THREE.Group>();
  for (const module of frame.model.modules) {
    const group = new THREE.Group();
    group.position.fromArray(module.position);
    group.quaternion.fromArray(module.rotation);
    root.add(group); moduleGroups.set(module.id, group);
  }
  for (const part of frame.model.parts) {
    const group = new THREE.Group();
    group.position.fromArray(part.position); group.quaternion.fromArray(part.rotation);
    const material = new THREE.MeshStandardMaterial({
      color: part.color,
      roughness: part.shape === 'window' ? .12 : .38,
      metalness: ['axle', 'gear'].includes(part.shape) ? .35 : 0,
      transparent: part.shape === 'window',
      opacity: part.shape === 'window' ? .58 : 1,
      emissive: highlight.has(part.moduleId) ? '#4b190d' : '#000000',
      emissiveIntensity: highlight.has(part.moduleId) ? .35 : 0,
    });
    const geometry = geometryFor(part);
    disposable.push(material, geometry);
    const mesh = new THREE.Mesh(geometry, material);
    if (part.shape === 'slope') mesh.scale.set(part.size[0], part.size[1], part.size[2]);
    mesh.castShadow = true; mesh.receiveShadow = true; group.add(mesh);
    addStuds(group, part, material);
    if (part.shape === 'wheel') {
      const hubMaterial = new THREE.MeshStandardMaterial({ color: '#b9c1c7', metalness: .5, roughness: .25 });
      const hub = new THREE.Mesh(new THREE.CylinderGeometry(part.size[0] * .2, part.size[0] * .2, part.size[1] * 1.06, 24), hubMaterial);
      disposable.push(hub.geometry, hubMaterial); group.add(hub);
    }
    moduleGroups.get(part.moduleId)!.add(group);
  }
  const box = new THREE.Box3().setFromObject(root);
  const center = box.getCenter(new THREE.Vector3()), size = box.getSize(new THREE.Vector3());
  for (const path of frame.accessPaths ?? []) {
    const start = new THREE.Vector3(...path.start), end = new THREE.Vector3(...path.end);
    const delta = end.clone().sub(start), length = delta.length();
    const arrow = new THREE.ArrowHelper(delta.normalize(), start, length,
      path.accessible ? '#27865e' : '#c83c32', .55, .28);
    root.add(arrow); box.expandByPoint(start); box.expandByPoint(end);
  }
  if (frame.force) {
    const module = frame.model.modules.find((m: any) => m.id === frame.force!.moduleId);
    if (module) {
      const start = new THREE.Vector3(...module.position), delta = new THREE.Vector3(...frame.force.vector);
      root.add(new THREE.ArrowHelper(delta.clone().normalize(), start, delta.length(), '#d43a32', .8, .4));
    }
  }
  const offsets: Record<NonNullable<Frame['view']>, [number, number, number]> = {
    iso: [18, 15, 22], front: [0, 5, 30], side: [30, 5, 0], top: [0, 35, .001],
  };
  camera.position.copy(center).add(new THREE.Vector3(...offsets[frame.view ?? 'iso']));
  camera.up.set(0, 1, 0); camera.lookAt(center); camera.updateMatrixWorld();
  const inverse = camera.matrixWorldInverse;
  let halfX = 1, halfY = 1;
  for (const x of [box.min.x, box.max.x]) for (const y of [box.min.y, box.max.y]) for (const z of [box.min.z, box.max.z]) {
    const projected = new THREE.Vector3(x, y, z).applyMatrix4(inverse);
    halfX = Math.max(halfX, Math.abs(projected.x)); halfY = Math.max(halfY, Math.abs(projected.y));
  }
  const span = Math.max(halfY, halfX / (4 / 3)) * 1.14;
  camera.left = -span * 4 / 3; camera.right = span * 4 / 3;
  camera.top = span; camera.bottom = -span; camera.updateProjectionMatrix();
  scene.updateMatrixWorld(true); renderer.render(scene, camera);
  return { png: canvas.toDataURL('image/png'), parts: frame.model.parts.length, size: size.toArray() };
}

declare global { interface Window { atlasMechanismRender: typeof render } }
window.atlasMechanismRender = render;
