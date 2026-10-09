import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import type { SceneData } from './types';

const palette: Record<string, string> = { '0': '#202326', '1': '#0055bf', '4': '#c91a09', '7': '#9ba19d', '14': '#f2cd37', '15': '#ffffff', '71': '#a0a5a9', '72': '#6c6e68' };
type Piece = { group: THREE.Group; center: THREE.Vector3; site: number; id: string; label: HTMLSpanElement; materials: THREE.MeshStandardMaterial[] };

/** Owns every camera update and GPU frame; React only sends semantic changes. */
export class BrickSceneController {
  private renderer: THREE.WebGLRenderer;
  private scene = new THREE.Scene();
  private camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100000);
  private controls: OrbitControls;
  private pieces: Piece[] = [];
  private geometries: THREE.BufferGeometry[] = [];
  private labels = document.createElement('div');
  private center = new THREE.Vector3();
  private radius = 1;
  private resize: ResizeObserver;
  private queued = 0;
  private disposed = false;
  private labelVisible = true;
  private selected = '';
  private start = { x: 0, y: 0 };
  constructor(private host: HTMLDivElement, data: SceneData, private onSelect: (id: string) => void) {
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    this.renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    this.renderer.setClearColor('#f0f3f6');
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.domElement.setAttribute('aria-label', 'Interactive LDraw assembly. Drag to orbit, scroll to zoom.');
    this.renderer.domElement.setAttribute('role', 'img');
    this.labels.className = 'scene-labels';
    host.append(this.renderer.domElement, this.labels);
    this.scene.add(new THREE.HemisphereLight(0xffffff, 0x8694a5, 2.7));
    const key = new THREE.DirectionalLight(0xffffff, 2.5); key.position.set(120, 300, 200); this.scene.add(key);
    const bounds = new THREE.Box3();
    for (const [local, part] of data.parts.entries()) {
      const group = new THREE.Group(), materials: THREE.MeshStandardMaterial[] = [];
      const matrix = new THREE.Matrix4().makeScale(1, -1, -1).multiply(new THREE.Matrix4().set(...part.rawMatrix.flat() as Parameters<THREE.Matrix4['set']>));
      for (const [color, vertices] of Object.entries(data.meshes[part.partNumber])) {
        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        geometry.applyMatrix4(matrix); geometry.computeVertexNormals(); this.geometries.push(geometry);
        const shade = new THREE.Color(color === '16' ? part.colorHex : palette[color] || part.colorHex);
        if (data.grayscale) { const v = shade.r * .2126 + shade.g * .7152 + shade.b * .0722; shade.setRGB(v, v, v); }
        const material = new THREE.MeshStandardMaterial({ color: shade, roughness: .34, metalness: .025, side: THREE.DoubleSide });
        materials.push(material); group.add(new THREE.Mesh(geometry, material));
      }
      const box = new THREE.Box3().setFromObject(group); bounds.union(box);
      const site = data.mutable.indexOf(local), id = site >= 0 ? data.partIds[site] : data.fixedIds[local];
      const label = document.createElement('span'); label.textContent = site >= 0 ? `${id} / ${data.siteIds[site]}` : id;
      this.labels.append(label); group.userData.pieceId = id;
      this.pieces.push({ group, center: box.getCenter(new THREE.Vector3()), site, id, label, materials });
      this.scene.add(group);
    }
    bounds.getCenter(this.center); this.radius = Math.max(1, bounds.getSize(new THREE.Vector3()).length() * .58);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.target.copy(this.center); this.controls.enableDamping = false;
    this.controls.minDistance = this.radius * .35; this.controls.maxDistance = this.radius * 12;
    this.controls.addEventListener('change', this.invalidate);
    this.renderer.domElement.addEventListener('pointerdown', this.pointerDown);
    this.renderer.domElement.addEventListener('pointerup', this.pointerUp);
    this.resize = new ResizeObserver(this.onResize); this.resize.observe(host);
    this.preset('isometric'); this.onResize();
  }
  private pointerDown = (e: PointerEvent) => { this.start = { x: e.clientX, y: e.clientY }; };
  private pointerUp = (e: PointerEvent) => {
    if (Math.hypot(e.clientX - this.start.x, e.clientY - this.start.y) > 5) return;
    const rect = this.renderer.domElement.getBoundingClientRect();
    const ray = new THREE.Raycaster();
    ray.setFromCamera(new THREE.Vector2((e.clientX - rect.left) / rect.width * 2 - 1, -(e.clientY - rect.top) / rect.height * 2 + 1), this.camera);
    const hit = ray.intersectObjects(this.pieces.filter(p => p.group.visible).map(p => p.group), true)[0];
    if (hit) { let object: THREE.Object3D | null = hit.object; while (object && !object.userData.pieceId) object = object.parent; if (object) this.onSelect(object.userData.pieceId); }
  };
  private onResize = () => {
    const width = this.host.clientWidth, height = this.host.clientHeight;
    if (!width || !height) return;
    this.renderer.setSize(width, height, false); this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix(); this.invalidate();
  };
  private invalidate = () => {
    if (this.queued || this.disposed) return;
    this.queued = requestAnimationFrame(() => {
      this.queued = 0; this.renderer.render(this.scene, this.camera);
      for (const p of this.pieces) {
        const at = p.center.clone().add(p.group.position).project(this.camera);
        p.label.hidden = !this.labelVisible || !p.group.visible || (p.site < 0 && p.id !== this.selected)
          || Math.abs(at.x) > .95 || Math.abs(at.y) > .94 || Math.abs(at.z) > 1;
        p.label.style.left = `${(at.x + 1) * 50}%`; p.label.style.top = `${(1 - at.y) * 50}%`;
        p.label.dataset.selected = String(p.id === this.selected);
      }
    });
  };
  preset(view: string) {
    const directions: Record<string, number[]> = { isometric: [1, .85, 1.5], front: [0, .01, 1], rear: [0, .01, -1], left: [-1, .01, 0], right: [1, .01, 0], top: [0, 1, .001], bottom: [0, -1, .001] };
    this.camera.position.copy(this.center).add(new THREE.Vector3(...(directions[view] || directions.isometric)).normalize().multiplyScalar(this.radius * 2.8));
    this.controls.target.copy(this.center); this.controls.update(); this.invalidate();
  }
  show(mask: number, explode: number, labels: boolean, selected: string) {
    this.labelVisible = labels; this.selected = selected;
    for (const p of this.pieces) {
      p.group.visible = p.site < 0 || Boolean(mask & (1 << p.site));
      p.group.position.copy(p.center).sub(this.center).multiplyScalar(explode * 1.3);
      p.materials.forEach(m => { m.emissive.set(p.id === selected ? '#3669ba' : '#000000'); m.emissiveIntensity = .3; });
    }
    this.invalidate();
  }
  dispose() {
    this.disposed = true; cancelAnimationFrame(this.queued); this.resize.disconnect(); this.controls.dispose();
    this.renderer.domElement.removeEventListener('pointerdown', this.pointerDown);
    this.renderer.domElement.removeEventListener('pointerup', this.pointerUp);
    this.geometries.forEach(g => g.dispose()); this.pieces.forEach(p => p.materials.forEach(m => m.dispose()));
    this.renderer.dispose(); this.renderer.forceContextLoss(); this.host.replaceChildren();
  }
}
