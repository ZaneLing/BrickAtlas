import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import type { BenchModel, ReplayFrame } from './types';
import { bodyGeometry, studs } from './geometry';

export class BenchmarkScene {
  readonly renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  readonly scene = new THREE.Scene();
  readonly camera = new THREE.PerspectiveCamera(38, 1, 0.05, 2000);
  readonly controls: OrbitControls;
  readonly root = new THREE.Group();
  private modules = new Map<string, THREE.Group>();
  private parts: Array<{ mesh: THREE.Group; position: THREE.Vector3; moduleId: string }> = [];
  private originals = new Map<string, THREE.Vector3>();
  private observer: ResizeObserver;
  private frame = 0;
  private disposed = false;
  private explode = 0;
  private center = new THREE.Vector3();
  private materials: THREE.Material[] = [];
  private geometries: THREE.BufferGeometry[] = [];
  private sourceColors = new Map<THREE.MeshStandardMaterial, THREE.Color>();
  private click: (event: PointerEvent) => void;
  private down: (event: PointerEvent) => void;
  private pointer = new THREE.Vector2();
  private selected: string | null = null;
  private activeModules: Set<string> | null = null;
  private isolated = false;

  constructor(private host: HTMLElement, readonly model: BenchModel, onSelect: (id: string) => void) {
    this.renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    this.renderer.setClearColor('#edf1f4');
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    host.appendChild(this.renderer.domElement);
    this.renderer.domElement.setAttribute('aria-label', `${model.nameZh} 交互式三维模型`);
    this.renderer.domElement.tabIndex = 0;
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true; this.controls.maxDistance = 600;
    this.scene.add(this.root, new THREE.HemisphereLight('#ffffff', '#6c7e97', 2.5));
    const key = new THREE.DirectionalLight('#ffffff', 3); key.position.set(-12, 22, 18); this.scene.add(key);
    const fill = new THREE.DirectionalLight('#cfe0ff', 1.5); fill.position.set(18, 8, -12); this.scene.add(fill);
    for (const m of model.modules) {
      const group = new THREE.Group();
      group.position.fromArray(m.position); group.quaternion.fromArray(m.rotation);
      this.originals.set(m.id, group.position.clone()); this.modules.set(m.id, group); this.root.add(group);
    }
    for (const p of model.parts) {
      const group = new THREE.Group();
      group.position.fromArray(p.position); group.quaternion.fromArray(p.rotation); group.userData.moduleId = p.moduleId;
      const material = new THREE.MeshStandardMaterial({ color: p.color, roughness: 0.4,
        transparent: p.shape === 'window', opacity: p.shape === 'window' ? 0.52 : 1 });
      this.materials.push(material); this.sourceColors.set(material, material.color.clone());
      const geometry = bodyGeometry(p);
      this.geometries.push(geometry); group.add(new THREE.Mesh(geometry, material));
      for (const s of studs(p)) {
        const stud = new THREE.CylinderGeometry(s.radius, s.radius, s.height, 12);
        this.geometries.push(stud);
        const mesh = new THREE.Mesh(stud, material);
        mesh.position.fromArray(s.position); group.add(mesh);
      }
      this.modules.get(p.moduleId)!.add(group);
      this.parts.push({ mesh: group, position: group.position.clone(), moduleId: p.moduleId });
    }
    new THREE.Box3().setFromObject(this.root).getCenter(this.center);
    this.observer = new ResizeObserver(() => this.resize()); this.observer.observe(host);
    this.resize(); this.view('iso');
    this.down = e => this.pointer.set(e.clientX, e.clientY);
    this.click = e => {
      if (this.pointer.distanceTo(new THREE.Vector2(e.clientX, e.clientY)) > 5) return;
      const rect = this.renderer.domElement.getBoundingClientRect();
      const ray = new THREE.Raycaster();
      ray.setFromCamera(new THREE.Vector2((e.clientX - rect.left) / rect.width * 2 - 1,
        -(e.clientY - rect.top) / rect.height * 2 + 1), this.camera);
      const hit = ray.intersectObject(this.root, true).find(hit => {
        let node: THREE.Object3D | null = hit.object;
        while (node) { if (!node.visible) return false; node = node.parent; }
        return true;
      });
      let node = hit?.object;
      while (node && !node.userData.moduleId) node = node.parent!;
      if (node?.userData.moduleId) onSelect(node.userData.moduleId);
    };
    this.renderer.domElement.addEventListener('pointerdown', this.down);
    this.renderer.domElement.addEventListener('pointerup', this.click);
    const tick = () => {
      if (this.disposed) return;
      this.controls.update(); this.renderer.render(this.scene, this.camera);
      this.frame = requestAnimationFrame(tick);
    };
    tick();
  }
  private resize() {
    const { width, height } = this.host.getBoundingClientRect();
    if (!width || !height) return;
    this.renderer.setSize(width, height); this.camera.aspect = width / height; this.camera.updateProjectionMatrix();
  }
  fit() {
    const box = new THREE.Box3().setFromObject(this.root), size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());
    const direction = this.camera.position.clone().sub(this.controls.target).normalize();
    const radius = size.length() / 2;
    const distance = radius / Math.sin(Math.atan(Math.tan(THREE.MathUtils.degToRad(19)) * Math.min(1, this.camera.aspect))) * 1.1;
    this.camera.position.copy(center).addScaledVector(direction.lengthSq() ? direction : new THREE.Vector3(1, 0.7, 1), distance);
    this.controls.target.copy(center); this.controls.update();
  }
  view(mode: string) {
    const directions: Record<string, number[]> = { iso: [1, 0.7, 1], front: [0, 0, 1], side: [1, 0, 0], top: [0, 1, 0.001] };
    this.camera.position.copy(this.controls.target).add(new THREE.Vector3(...(directions[mode] ?? directions.iso)));
    this.fit();
  }
  explosion(amount: number) {
    this.explode = amount;
    for (const [i, m] of this.model.modules.entries()) {
      const group = this.modules.get(m.id)!;
      const box = new THREE.Box3();
      for (const p of this.parts.filter(p => p.moduleId === m.id)) {
        p.mesh.position.copy(p.position);
      }
      group.position.copy(this.originals.get(m.id)!); group.updateMatrixWorld(true);
      box.setFromObject(group);
      const direction = box.getCenter(new THREE.Vector3()).sub(this.center);
      if (direction.lengthSq() < 0.01) direction.set(Math.cos(i * 2.4), 0.7, Math.sin(i * 2.4));
      group.position.add(direction.normalize().multiplyScalar(amount * 5));
      for (const p of this.parts.filter(p => p.moduleId === m.id)) {
        p.mesh.position.addScaledVector(p.position.clone().sub(box.getCenter(new THREE.Vector3())
          .sub(this.originals.get(m.id)!)), Math.max(0, amount - 0.5) * 0.5);
      }
    }
    this.fit();
  }
  highlight(id: string | null, isolate = false) {
    this.selected = id;
    this.isolated = isolate;
    for (const [moduleId, group] of this.modules) {
      group.visible = (!this.activeModules || this.activeModules.has(moduleId))
        && (!isolate || !id || moduleId === id);
      group.traverse(obj => {
        const material = (obj as THREE.Mesh).material as THREE.MeshStandardMaterial | undefined;
        if (material?.emissive) material.emissive.set(moduleId === id ? '#483011' : '#000000');
      });
    }
  }
  state(frame: ReplayFrame | null) {
    this.activeModules = frame ? new Set(frame.activeModules) : null;
    for (const [id, group] of this.modules) {
      group.visible = (!this.activeModules || this.activeModules.has(id))
        && (!this.isolated || !this.selected || this.selected === id);
      group.traverse(obj => {
        const material = (obj as THREE.Mesh).material as THREE.MeshStandardMaterial | undefined;
        if (material?.color) material.color.copy(frame?.colors[id]
          ? new THREE.Color(frame.colors[id]) : this.sourceColors.get(material)!);
      });
    }
  }
  snapshot() {
    return { modelId: this.model.id, parts: this.parts.length, modules: this.modules.size,
      visibleModules: [...this.modules].filter(([, g]) => g.visible).map(([id]) => id), explosion: this.explode,
      selected: this.selected, camera: this.camera.position.toArray(), drawCalls: this.renderer.info.render.calls,
      triangles: this.renderer.info.render.triangles, contextLost: this.renderer.getContext().isContextLost() };
  }
  png() { this.renderer.render(this.scene, this.camera); return this.renderer.domElement.toDataURL('image/png'); }
  dispose() {
    this.disposed = true; cancelAnimationFrame(this.frame); this.observer.disconnect(); this.controls.dispose();
    this.renderer.domElement.removeEventListener('pointerdown', this.down);
    this.renderer.domElement.removeEventListener('pointerup', this.click);
    this.geometries.forEach(g => g.dispose()); this.materials.forEach(m => m.dispose());
    this.renderer.dispose(); this.renderer.forceContextLoss(); this.renderer.domElement.remove();
  }
}
