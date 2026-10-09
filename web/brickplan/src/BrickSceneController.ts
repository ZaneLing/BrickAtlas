import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import type { SceneData } from './types';

const palette: Record<string, string> = { '0': '#202326', '1': '#0055bf', '4': '#c91a09', '7': '#9ba19d', '14': '#f2cd37', '15': '#ffffff', '71': '#a0a5a9', '72': '#6c6e68' };
type Piece = { group: THREE.Group; center: THREE.Vector3; site: number; id: string; siteId?: string; partNumber: string; materials: THREE.MeshStandardMaterial[] };

/** Owns every camera update and GPU frame; React only sends semantic changes. */
export class BrickSceneController {
  private renderer: THREE.WebGLRenderer;
  private scene = new THREE.Scene();
  private camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100000);
  private controls: OrbitControls;
  private pieces: Piece[] = [];
  private geometries: THREE.BufferGeometry[] = [];
  private tooltip = document.createElement('div');
  private tooltipTitle = document.createElement('strong');
  private tooltipDetail = document.createElement('span');
  private ray = new THREE.Raycaster();
  private pointer?: { x: number; y: number };
  private hover?: Piece;
  private hoverPending = false;
  private center = new THREE.Vector3();
  private radius = 1;
  private resize: ResizeObserver;
  private queued = 0;
  private disposed = false;
  private selected = '';
  private start = { x: 0, y: 0 };
  constructor(private host: HTMLDivElement, data: SceneData, private onSelect: (id: string) => void) {
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    this.renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    this.renderer.setClearColor('#f0f3f6');
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.domElement.setAttribute('aria-label', 'Interactive LDraw assembly. Drag to orbit, scroll to zoom.');
    this.renderer.domElement.setAttribute('role', 'img');
    this.renderer.domElement.tabIndex = 0;
    this.tooltip.className = 'scene-tooltip';
    this.tooltip.setAttribute('role', 'tooltip');
    this.tooltip.hidden = true;
    this.tooltip.append(this.tooltipTitle, this.tooltipDetail);
    host.append(this.renderer.domElement, this.tooltip);
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
      group.userData.pieceId = id;
      this.pieces.push({ group, center: box.getCenter(new THREE.Vector3()), site, id,
        siteId: site >= 0 ? data.siteIds[site] : undefined, partNumber: part.partNumber, materials });
      this.scene.add(group);
    }
    bounds.getCenter(this.center); this.radius = Math.max(1, bounds.getSize(new THREE.Vector3()).length() * .58);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.target.copy(this.center); this.controls.enableDamping = false;
    this.controls.minDistance = this.radius * .35; this.controls.maxDistance = this.radius * 12;
    this.controls.addEventListener('change', this.invalidate);
    this.controls.addEventListener('start', this.clearHover);
    this.renderer.domElement.addEventListener('pointerdown', this.pointerDown);
    this.renderer.domElement.addEventListener('pointerup', this.pointerUp);
    this.renderer.domElement.addEventListener('pointermove', this.pointerMove);
    this.renderer.domElement.addEventListener('pointerleave', this.pointerLeave);
    this.renderer.domElement.addEventListener('pointercancel', this.clearHover);
    this.renderer.domElement.addEventListener('keydown', this.keyDown);
    document.addEventListener('pointerdown', this.outsidePointer);
    this.resize = new ResizeObserver(this.onResize); this.resize.observe(host);
    this.preset('isometric'); this.onResize(); host.dataset.sceneReady = 'true';
  }
  private pointerDown = (e: PointerEvent) => {
    this.start = { x: e.clientX, y: e.clientY }; this.clearHover();
  };
  private pointerMove = (e: PointerEvent) => {
    if (e.buttons || e.pointerType === 'touch') return;
    this.pointer = { x: e.clientX, y: e.clientY }; this.hoverPending = true; this.invalidate();
  };
  private pick(x: number, y: number) {
    this.scene.updateMatrixWorld(true);
    const rect = this.renderer.domElement.getBoundingClientRect();
    this.ray.setFromCamera(new THREE.Vector2((x - rect.left) / rect.width * 2 - 1, -(y - rect.top) / rect.height * 2 + 1), this.camera);
    const hit = this.ray.intersectObjects(this.pieces.filter(p => p.group.visible).map(p => p.group), true)[0];
    if (!hit) return;
    let object: THREE.Object3D | null = hit.object;
    while (object && !object.userData.pieceId) object = object.parent;
    return this.pieces.find(p => p.id === object?.userData.pieceId);
  }
  private pointerUp = (e: PointerEvent) => {
    if (e.button !== 0 || Math.hypot(e.clientX - this.start.x, e.clientY - this.start.y) > 5) return;
    const piece = this.pick(e.clientX, e.clientY);
    if (piece) this.onSelect(piece.id);
    this.pointer = { x: e.clientX, y: e.clientY }; this.setHover(piece); this.invalidate();
  };
  private clearHover = () => {
    this.pointer = undefined; this.hoverPending = false; this.setHover(undefined); this.invalidate();
  };
  private pointerLeave = (e: PointerEvent) => { if (e.pointerType !== 'touch') this.clearHover(); };
  private outsidePointer = (e: PointerEvent) => { if (!this.host.contains(e.target as Node)) this.clearHover(); };
  private keyDown = (e: KeyboardEvent) => {
    if (e.key === 'Escape') this.clearHover();
    if (!['ArrowLeft', 'ArrowRight', 'Enter'].includes(e.key)) return;
    e.preventDefault();
    if (e.key === 'Enter') { if (this.hover) this.onSelect(this.hover.id); return; }
    const visible = this.pieces.filter(p => p.group.visible), index = visible.indexOf(this.hover!);
    const piece = visible[(index + (e.key === 'ArrowRight' ? 1 : visible.length - 1)) % visible.length];
    if (!piece) return;
    const rect = this.host.getBoundingClientRect();
    this.pointer = { x: rect.left + 15, y: rect.top + 45 }; this.setHover(piece); this.invalidate();
  };
  private setHover(piece?: Piece) {
    if (piece !== this.hover) {
      this.hover = piece;
      this.pieces.forEach(p => p.materials.forEach(m => {
        m.emissive.set(p === piece ? '#397daa' : p.id === this.selected ? '#3669ba' : '#000000');
        m.emissiveIntensity = p === piece ? .45 : .3;
      }));
    }
    this.tooltip.hidden = !piece;
    if (piece) {
      this.tooltip.dataset.pieceId = piece.id;
      this.tooltipTitle.textContent = `零件 ${piece.id}`;
      this.tooltipDetail.textContent = `${piece.siteId ? `注册位置 ${piece.siteId}` : '固定基座 · 不可移动'} · LDraw ${piece.partNumber}`;
      const rect = this.host.getBoundingClientRect(), at = this.pointer || { x: rect.left, y: rect.top };
      this.tooltip.style.left = `${Math.max(10, Math.min(at.x - rect.left + 14, rect.width - this.tooltip.offsetWidth - 10))}px`;
      this.tooltip.style.top = `${Math.max(40, Math.min(at.y - rect.top + 14, rect.height - this.tooltip.offsetHeight - 10))}px`;
    }
  }
  private onResize = () => {
    const width = this.host.clientWidth, height = this.host.clientHeight;
    if (!width || !height) return;
    this.renderer.setSize(width, height, false); this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix(); this.invalidate();
  };
  private invalidate = () => {
    if (this.queued || this.disposed) return;
    this.queued = requestAnimationFrame(() => {
      this.queued = 0;
      if (this.hoverPending && this.pointer) {
        this.hoverPending = false; this.setHover(this.pick(this.pointer.x, this.pointer.y));
      }
      this.renderer.render(this.scene, this.camera);
    });
  };
  preset(view: string) {
    const directions: Record<string, number[]> = { isometric: [1, .85, 1.5], front: [0, .01, 1], rear: [0, .01, -1], left: [-1, .01, 0], right: [1, .01, 0], top: [0, 1, .001], bottom: [0, -1, .001] };
    this.camera.position.copy(this.center).add(new THREE.Vector3(...(directions[view] || directions.isometric)).normalize().multiplyScalar(this.radius * 2.8));
    this.controls.target.copy(this.center); this.controls.update(); this.invalidate();
  }
  show(mask: number, explode: number, selected: string) {
    this.selected = selected;
    for (const p of this.pieces) {
      p.group.visible = p.site < 0 || Boolean(mask & (1 << p.site));
      p.group.position.copy(p.center).sub(this.center).multiplyScalar(explode * 1.3);
      p.materials.forEach(m => { m.emissive.set(p === this.hover ? '#397daa' : p.id === selected ? '#3669ba' : '#000000'); m.emissiveIntensity = p === this.hover ? .45 : .3; });
    }
    if (this.hover && !this.hover.group.visible) this.setHover(undefined);
    this.invalidate();
  }
  dispose() {
    this.disposed = true; cancelAnimationFrame(this.queued); this.resize.disconnect(); this.controls.dispose();
    this.renderer.domElement.removeEventListener('pointerdown', this.pointerDown);
    this.renderer.domElement.removeEventListener('pointerup', this.pointerUp);
    this.renderer.domElement.removeEventListener('pointermove', this.pointerMove);
    this.renderer.domElement.removeEventListener('pointerleave', this.pointerLeave);
    this.renderer.domElement.removeEventListener('pointercancel', this.clearHover);
    this.renderer.domElement.removeEventListener('keydown', this.keyDown);
    document.removeEventListener('pointerdown', this.outsidePointer);
    this.geometries.forEach(g => g.dispose()); this.pieces.forEach(p => p.materials.forEach(m => m.dispose()));
    this.renderer.dispose(); this.renderer.forceContextLoss(); this.host.replaceChildren(); delete this.host.dataset.sceneReady;
  }
}
