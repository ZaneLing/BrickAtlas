import {
  ACESFilmicToneMapping, AmbientLight, Box3, BufferAttribute, BufferGeometry, DataTexture, DirectionalLight, DoubleSide,
  FloatType, GridHelper, Group, HemisphereLight, LineSegments, Matrix4, Mesh, MeshBasicMaterial,
  MOUSE, NearestFilter, PerspectiveCamera, PMREMGenerator, Raycaster, RGBAFormat,
  Scene, SRGBColorSpace, Vector2, Vector3, WebGLRenderer, type Intersection, type Material,
} from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { atlasMaterial, setAtlasXray } from './materials';
import type { PartPreviewData } from './PartPreview';
import { explosionOffset, inventoryLayout, inventoryRotation, smoothstep, type InventoryLayout } from '../explosion/layout';
import { initialState, visibleInstances, type ExplorerState, type GroupId, type PartInstance } from '../model/types';
import { BrickModel } from '../model/BrickModel';

export interface SceneMetrics {
  loadedInstances: number; visibleInstances: number; drawCalls: number; triangles: number;
  renderedFrames: number; frameMs: number; firstVisibleMs: number | null; readyMs: number | null;
  actualExplosion: number; contextLost: boolean;
}
interface Callbacks {
  progress: (value: number, stage: string) => void;
  ready: () => void;
  error: (message: string) => void;
  select: (id: string | null) => void;
  hover: (part: PartInstance | null, x: number, y: number) => void;
}
type PickPart = { part: PartInstance; mesh: Mesh; box: Box3; transparent: boolean };

export class AtlasScene {
  readonly scene = new Scene();
  readonly camera = new PerspectiveCamera(34, 1, 0.1, 20000);
  readonly renderer: WebGLRenderer;
  readonly controls: OrbitControls;
  readonly metrics: SceneMetrics = {
    loadedInstances: 0, visibleInstances: 0, drawCalls: 0, triangles: 0,
    renderedFrames: 0, frameMs: 0, firstVisibleMs: null, readyMs: null, actualExplosion: 0, contextLost: false,
  };
  private state: ExplorerState = initialState;
  private model = new Group();
  private grid = new GridHelper(600, 30, 0xced6d2, 0xe3e8e5);
  private texture: DataTexture;
  private stateData: Float32Array;
  private visible: PartInstance[] = [];
  private offsets: Vector3[] = [];
  private inventory: InventoryLayout;
  private picks = new Map<number, PickPart>();
  private loaded = new Set<GroupId>();
  private worker: Worker;
  private observer: ResizeObserver;
  private frame = 0;
  private disposed = false;
  private dirty = true;
  private fitRequested = true;
  private cameraMoving = false;
  private interaction = false;
  private actualExplosion = 0;
  private assemblyProgress = 1;
  private assemblyIds = new Set<string>();
  private desiredTarget = new Vector3();
  private desiredPosition = new Vector3();
  private userDirection = new Vector3(-1, 0.7, 1);
  private raycaster = new Raycaster();
  private pointerStart = new Vector2();
  private maxPointerDistance = 0;
  private pointers = new Set<number>();
  private multiTouch = false;
  private lastTick = 0;
  private started = performance.now();
  private motionPreference = matchMedia('(prefers-reduced-motion: reduce)');
  private reducedMotion = this.motionPreference.matches;
  private lineObjects: LineSegments[] = [];
  private environment: import('three').WebGLRenderTarget;
  private captureRenderer: WebGLRenderer | null = null;
  private onSelect: Callbacks['select'];
  private onHover: Callbacks['hover'];

  constructor(private host: HTMLElement, readonly brickModel: BrickModel, private callbacks: Callbacks) {
    const manifest = brickModel.manifest;
    this.onSelect = callbacks.select;
    this.onHover = callbacks.hover;
    this.renderer = new WebGLRenderer({ antialias: true, alpha: false, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
    this.renderer.setClearColor('#f2f5f3');
    this.renderer.outputColorSpace = SRGBColorSpace;
    this.renderer.toneMapping = ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.05;
    this.renderer.setPixelRatio(Math.min(devicePixelRatio, innerWidth < 768 ? 1.5 : 2));
    this.renderer.domElement.setAttribute('aria-label', `${manifest.model.title} 交互式三维模型`);
    this.renderer.domElement.setAttribute('role', 'img');
    this.renderer.domElement.tabIndex = 0;
    host.appendChild(this.renderer.domElement);
    this.scene.add(this.model, this.grid, new HemisphereLight(0xffffff, 0xc6d0c9, 2.3), new AmbientLight(0xffffff, 0.3));
    const key = new DirectionalLight(0xffffff, 3.3);
    key.position.set(-100, 180, 130);
    this.scene.add(key);
    const fill = new DirectionalLight(0xe7edff, 1.5);
    fill.position.set(100, 60, -130);
    this.scene.add(fill);
    const pmrem = new PMREMGenerator(this.renderer);
    const room = new RoomEnvironment();
    this.environment = pmrem.fromScene(room, 0.04);
    this.scene.environment = this.environment.texture;
    room.dispose();
    pmrem.dispose();
    (this.grid.material as Material).transparent = true;
    (this.grid.material as Material).opacity = 0.6;
    this.grid.position.y = manifest.bounds.min[1] - 0.5;
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.09;
    this.controls.minDistance = 8;
    this.controls.maxDistance = 6000;
    this.controls.autoRotateSpeed = 0.65;
    this.controls.addEventListener('change', this.invalidate);
    this.controls.addEventListener('start', this.controlStart);
    this.controls.addEventListener('end', this.controlEnd);
    this.stateData = new Float32Array(manifest.instances.length * 8);
    this.texture = new DataTexture(this.stateData, manifest.instances.length, 2, RGBAFormat, FloatType);
    this.texture.minFilter = NearestFilter;
    this.texture.magFilter = NearestFilter;
    this.texture.needsUpdate = true;
    this.offsets = manifest.instances.map(() => new Vector3());
    this.visible = manifest.instances;
    this.inventory = inventoryLayout(this.visible, 1);
    this.observer = new ResizeObserver(this.resize);
    this.observer.observe(host);
    this.resize();
    this.updateLayout();
    this.fit(true);
    this.attachEvents();
    this.motionPreference.addEventListener('change', this.motionChanged);
    this.worker = new Worker(new URL('../workers/geometry.worker.ts', import.meta.url), { type: 'module' });
    this.worker.onmessage = event => {
      if (this.disposed) return;
      const data = event.data;
      if (data.type === 'progress') callbacks.progress(Math.min(98, data.downloaded / manifest.stats.compressedBytes * 100), '读取模型几何');
      if (data.type === 'chunk') {
        try {
          this.addChunk(data.groupId, data.buffer);
          this.metrics.loadedInstances = manifest.instances.filter(p => this.loaded.has(p.groupId)).length;
          if (this.metrics.firstVisibleMs === null) this.metrics.firstVisibleMs = performance.now() - this.started;
          this.updateLayout();
        } catch (error) { callbacks.error(String(error)); this.worker.terminate(); }
      }
      if (data.type === 'complete') {
        this.metrics.readyMs = performance.now() - this.started;
        callbacks.progress(100, '模型就绪');
        callbacks.ready();
        this.worker.terminate();
      }
      if (data.type === 'error') { callbacks.error(data.message); this.worker.terminate(); }
    };
    this.worker.onerror = error => callbacks.error(error.message || '模型解码工作线程失败');
    this.worker.postMessage({ base: new URL(`${import.meta.env.BASE_URL}models/${manifest.model.id}/`, location.href).href, chunks: manifest.chunks });
    this.frame = requestAnimationFrame(this.tick);
  }

  get manifest() { return this.brickModel.manifest; }
  private invalidate = () => { this.dirty = true; };
  private motionChanged = () => {
    this.reducedMotion = this.motionPreference.matches;
    this.setState(this.state);
  };
  private controlStart = () => { this.interaction = true; this.cameraMoving = false; this.callbacks.hover(null, 0, 0); };
  private controlEnd = () => { this.interaction = false; this.userDirection.copy(this.camera.position).sub(this.controls.target).normalize(); };

  private resize = () => {
    const { width, height } = this.host.getBoundingClientRect();
    if (!width || !height || this.disposed) return;
    const current = this.renderer.getSize(new Vector2());
    if (Math.abs(current.x - width) > 0.5 || Math.abs(current.y - height) > 0.5) {
      this.renderer.setSize(width, height);
    }
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.inventory = inventoryLayout(this.visible, this.camera.aspect);
    this.fitRequested = true;
    this.updateLayout();
  };

  private addChunk(groupId: GroupId, buffer: ArrayBuffer) {
    const chunk = this.manifest.chunks.find(c => c.groupId === groupId)!;
    const pickPositions = new Map<number, number[]>();
    for (const bucket of chunk.buckets) {
      const geometry = new BufferGeometry();
      for (const [name, attr] of Object.entries(bucket.attributes)) {
        if (attr.offset + attr.count * 4 > buffer.byteLength) throw new Error('Invalid geometry attribute range');
        geometry.setAttribute(name, new BufferAttribute(new Float32Array(buffer, attr.offset, attr.count), attr.itemSize));
      }
      const material = atlasMaterial(bucket, this.texture, this.manifest.instances.length);
      setAtlasXray(material, this.state.xray);
      const object = bucket.kind === 'mesh'
        ? new Mesh(geometry, material)
        : new LineSegments(geometry, material);
      geometry.computeBoundingSphere();
      // Vertices move in the shader; static geometry bounds must never cull them.
      object.frustumCulled = false;
      if (bucket.kind !== 'mesh') { this.lineObjects.push(object as LineSegments); object.visible = this.state.edges; }
      else {
        const positions = geometry.getAttribute('position');
        const ids = geometry.getAttribute('instanceIndex');
        for (let i = 0; i < ids.count; i++) {
          const id = ids.getX(i);
          if (!pickPositions.has(id)) pickPositions.set(id, []);
          pickPositions.get(id)!.push(positions.getX(i), positions.getY(i), positions.getZ(i));
        }
      }
      this.model.add(object);
    }
    for (const [index, positions] of pickPositions) {
      const part = this.manifest.instances[index];
      const geometry = new BufferGeometry();
      geometry.setAttribute('position', new BufferAttribute(new Float32Array(positions), 3));
      geometry.computeBoundingBox();
      geometry.computeBoundingSphere();
      const mesh = new Mesh(geometry, new MeshBasicMaterial({ side: DoubleSide }));
      this.picks.set(index, { part, mesh, box: geometry.boundingBox!.clone(), transparent: /Trans/i.test(part.colorName) });
    }
    this.loaded.add(groupId);
    this.dirty = true;
  }

  setState(state: ExplorerState) {
    const previous = this.state;
    this.state = state;
    const visibilityChanged = previous.hiddenGroups.join() !== state.hiddenGroups.join()
      || previous.hiddenBrickIds.join() !== state.hiddenBrickIds.join()
      || previous.isolation?.join() !== state.isolation?.join()
      || previous.buildStep !== state.buildStep;
    const viewChanged = previous.view !== state.view || previous.revision !== state.revision;
    const assemblyChanged = previous.buildStep !== state.buildStep || previous.assemblyRevision !== state.assemblyRevision;
    if (assemblyChanged && state.buildStep !== null && state.buildStep > 0
      && (previous.buildStep === null || state.buildStep >= (previous.buildStep ?? 0))) {
      this.assemblyIds = new Set(this.manifest.instructions?.steps[state.buildStep - 1]?.instanceIds ?? []);
      this.assemblyProgress = this.reducedMotion ? 1 : 0;
    } else if (assemblyChanged) {
      this.assemblyIds.clear();
      this.assemblyProgress = 1;
    }
    this.visible = visibleInstances(this.manifest, state);
    if (visibilityChanged) this.inventory = inventoryLayout(this.visible, this.camera.aspect);
    this.controls.autoRotate = state.autoRotate && !this.reducedMotion && state.explosion < 0.98;
    if (viewChanged) {
      this.userDirection.copy({
        perspective: new Vector3(-1, 0.65, 1), front: new Vector3(-1, 0.15, 0),
        side: new Vector3(0, 0.12, 1), rear: new Vector3(1, 0.15, 0), top: new Vector3(0, 1, 0.001),
      }[state.view]).normalize();
    }
    for (const line of this.lineObjects) line.visible = state.edges && state.quality !== 'low';
    const pixelRatio = state.quality === 'low' ? 1 : state.quality === 'ultra' ? 3
      : state.quality === 'high' ? 2 : Math.min(devicePixelRatio, innerWidth < 768 ? 1.5 : 2);
    if (this.renderer.getPixelRatio() !== pixelRatio) this.renderer.setPixelRatio(pixelRatio);
    if (previous.xray !== state.xray) this.model.traverse(object => {
      const material = (object as Mesh).material;
      if (material) (Array.isArray(material) ? material : [material]).forEach(item => setAtlasXray(item, state.xray));
    });
    if (previous.background !== state.background) {
      this.renderer.setClearColor({ studio: '#f2f5f3', white: '#ffffff', dark: '#18201c' }[state.background]);
    }
    if (previous.explosion !== state.explosion || viewChanged || visibilityChanged) this.fitRequested = true;
    if (this.reducedMotion) this.actualExplosion = state.explosion;
    this.updateLayout();
    if (this.fitRequested) this.fit();
  }

  private updateLayout() {
    const visible = new Set(this.visible.map(p => p.instanceId));
    const currentStep = this.state.buildStep && this.manifest.instructions
      ? this.manifest.instructions.steps[this.state.buildStep - 1]?.instanceIds ?? [] : [];
    const selected = new Set([...this.state.selection, ...this.state.highlightedBrickIds, ...(this.state.highlightStep ? currentStep : [])]);
    const n = this.manifest.instances.length;
    for (const part of this.manifest.instances) {
      const offset = new Vector3(...explosionOffset(part, this.actualExplosion, this.manifest, this.inventory));
      if (this.assemblyProgress < 1 && this.assemblyIds.has(part.instanceId)) {
        const direction = new Vector3(...(this.manifest.groups.find(group => group.id === part.groupId)?.direction ?? [0, 1, 0]));
        direction.y += 55;
        if (!direction.lengthSq()) direction.set(0, 1, 0);
        const size = new Vector3(...part.bounds.max).sub(new Vector3(...part.bounds.min)).length();
        offset.add(direction.normalize().multiplyScalar(Math.max(70, size * 2.5) * (1 - smoothstep(this.assemblyProgress))));
      }
      this.offsets[part.index].copy(offset);
      this.stateData.set([offset.x, offset.y, offset.z, Number(visible.has(part.instanceId))], part.index * 4);
      this.stateData[n * 4 + part.index * 4] = Number(selected.has(part.instanceId));
    }
    this.texture.needsUpdate = true;
    this.metrics.visibleInstances = this.visible.filter(p => this.loaded.has(p.groupId)).length;
    this.metrics.actualExplosion = this.actualExplosion;
    this.grid.visible = this.state.grid && this.actualExplosion < 0.02;
    this.controls.mouseButtons.LEFT = this.actualExplosion > 0.98 ? MOUSE.PAN : MOUSE.ROTATE;
    this.controls.enableRotate = this.actualExplosion < 0.98;
    this.dirty = true;
  }

  private fit(immediate = false) {
    if (!this.visible.length) { this.fitRequested = false; return; }
    const box = new Box3();
    for (const part of this.visible) {
      const offset = this.offsets[part.index];
      box.union(new Box3(new Vector3(...part.bounds.min).add(offset), new Vector3(...part.bounds.max).add(offset)));
    }
    box.getCenter(this.desiredTarget);
    const inventoryMix = Math.max(0, Math.min(1, (this.actualExplosion - 0.45) / 0.55));
    const inventoryDirection = new Vector3(0, 0, 1).applyMatrix4(inventoryRotation.clone().invert());
    const direction = this.userDirection.clone().normalize().lerp(inventoryDirection, inventoryMix).normalize();
    this.camera.fov = 34 - inventoryMix * 18;
    this.camera.updateProjectionMatrix();
    const temporary = new PerspectiveCamera(this.camera.fov, this.camera.aspect);
    temporary.position.copy(this.desiredTarget).add(direction);
    temporary.lookAt(this.desiredTarget);
    temporary.updateMatrixWorld();
    const rotation = new Matrix4().makeRotationFromQuaternion(temporary.quaternion).invert();
    const viewBox = new Box3();
    for (const part of this.visible) {
      const offset = this.offsets[part.index].clone().sub(this.desiredTarget);
      viewBox.union(new Box3(new Vector3(...part.bounds.min).add(offset), new Vector3(...part.bounds.max).add(offset)).applyMatrix4(rotation));
    }
    const tan = Math.tan(this.camera.fov * Math.PI / 360);
    const distance = Math.max(viewBox.max.y, -viewBox.min.y) / tan;
    const horizontal = Math.max(viewBox.max.x, -viewBox.min.x) / tan / this.camera.aspect;
    const fitDistance = Math.max(distance, horizontal, 20) * 1.15 + viewBox.max.z;
    this.desiredPosition.copy(this.desiredTarget).addScaledVector(direction, fitDistance);
    this.cameraMoving = true;
    if (immediate || this.reducedMotion) {
      this.camera.position.copy(this.desiredPosition);
      this.controls.target.copy(this.desiredTarget);
      this.controls.update();
      this.cameraMoving = false;
    }
    this.fitRequested = false;
    this.dirty = true;
  }

  focusSelection() {
    const chosen = this.visible.filter(p => this.state.selection.includes(p.instanceId));
    if (!chosen.length) return;
    const visible = this.visible;
    this.visible = chosen;
    this.fit();
    this.visible = visible;
  }

  zoom(factor: number) {
    const delta = this.camera.position.clone().sub(this.controls.target).multiplyScalar(factor);
    if (delta.length() < this.controls.minDistance || delta.length() > this.controls.maxDistance) return;
    this.camera.position.copy(this.controls.target).add(delta);
    this.cameraMoving = false;
    this.controls.update();
    this.dirty = true;
  }

  private tick = (time: number) => {
    if (this.disposed) return;
    const dt = Math.min((time - (this.lastTick || time - 16)) / 1000, 0.05);
    this.lastTick = time;
    const delta = this.state.explosion - this.actualExplosion;
    if (Math.abs(delta) > 0.0001) {
      this.actualExplosion += delta * (1 - Math.exp(-10 * dt));
      if (Math.abs(this.state.explosion - this.actualExplosion) < 0.0001) this.actualExplosion = this.state.explosion;
      this.updateLayout();
      if (!this.interaction) this.fit();
    }
    if (this.assemblyProgress < 1) {
      this.assemblyProgress = Math.min(1, this.assemblyProgress + dt / 0.75);
      this.updateLayout();
    }
    if (this.cameraMoving && !this.interaction) {
      const t = 1 - Math.exp(-8 * dt);
      this.camera.position.lerp(this.desiredPosition, t);
      this.controls.target.lerp(this.desiredTarget, t);
      if (this.camera.position.distanceTo(this.desiredPosition) < 0.02) this.cameraMoving = false;
      this.dirty = true;
    }
    this.controls.update(dt);
    if (this.dirty && !this.metrics.contextLost && document.visibilityState !== 'hidden') {
      const before = performance.now();
      this.renderer.render(this.scene, this.camera);
      this.metrics.frameMs = performance.now() - before;
      this.metrics.drawCalls = this.renderer.info.render.calls;
      this.metrics.triangles = this.renderer.info.render.triangles;
      this.metrics.renderedFrames++;
      this.dirty = false;
    }
    this.frame = requestAnimationFrame(this.tick);
  };

  private pick(clientX: number, clientY: number, allowGlass = false) {
    const rect = this.renderer.domElement.getBoundingClientRect();
    const mouse = new Vector2((clientX - rect.left) / rect.width * 2 - 1, -(clientY - rect.top) / rect.height * 2 + 1);
    this.raycaster.setFromCamera(mouse, this.camera);
    const originalRay = this.raycaster.ray.clone();
    const hits: { part: PartInstance; distance: number; transparent: boolean }[] = [];
    for (const part of this.visible) {
      const pick = this.picks.get(part.index);
      if (!pick) continue;
      this.raycaster.ray.copy(originalRay);
      this.raycaster.ray.origin.sub(this.offsets[part.index]);
      if (!this.raycaster.ray.intersectsBox(pick.box)) continue;
      const intersections: Intersection[] = [];
      pick.mesh.raycast(this.raycaster, intersections);
      if (intersections.length) hits.push({ part, distance: Math.min(...intersections.map(i => i.distance)), transparent: pick.transparent });
    }
    this.raycaster.ray.copy(originalRay);
    hits.sort((a, b) => a.distance - b.distance);
    const candidate = allowGlass ? hits[0] : hits.find(h => !h.transparent) ?? hits[0];
    if (candidate) return candidate.part;
    if (this.actualExplosion > 0.98) {
      let closest: PartInstance | null = null, distance = innerWidth < 768 ? 24 : 12;
      for (const part of this.visible) {
        if (!this.loaded.has(part.groupId)) continue;
        const projected = this.projectPart(part);
        const d = Math.hypot(projected.x - (clientX - rect.left), projected.y - (clientY - rect.top));
        if (d < distance) { distance = d; closest = part; }
      }
      return closest;
    }
    return null;
  }

  projectPart(part: PartInstance) {
    const center = new Vector3(...part.bounds.min).add(new Vector3(...part.bounds.max)).multiplyScalar(0.5).add(this.offsets[part.index]);
    center.project(this.camera);
    const { width, height } = this.renderer.domElement.getBoundingClientRect();
    return { id: part.instanceId, x: (center.x + 1) / 2 * width, y: (1 - center.y) / 2 * height, z: center.z };
  }

  getPartPreview(instanceId: string): PartPreviewData | null {
    const part = this.manifest.instances.find(item => item.instanceId === instanceId);
    const pick = part ? this.picks.get(part.index) : null;
    if (!part || !pick) return null;
    const positions = pick.mesh.geometry.getAttribute('position').array;
    return { positions: new Float32Array(positions as ArrayLike<number>), color: part.colorHex };
  }

  async exportPng(width: number, height: number) {
    return this.renderBlob(width, height, 'image/png');
  }

  async captureBuildStep(step: number, width = 960, height = 720) {
    const savedState = this.state;
    const savedExplosion = this.actualExplosion;
    const savedProgress = this.assemblyProgress;
    const savedIds = this.assemblyIds;
    const savedCamera = this.camera.position.clone();
    const savedTarget = this.controls.target.clone();
    const savedDirection = this.userDirection.clone();
    const savedFov = this.camera.fov;
    const savedAspect = this.camera.aspect;
    const savedDesiredTarget = this.desiredTarget.clone();
    const savedDesiredPosition = this.desiredPosition.clone();
    const savedCameraMoving = this.cameraMoving;
    const savedFitRequested = this.fitRequested;
    const savedInventory = this.inventory;
    const savedEnvironment = this.scene.environment;
    const capture = this.captureRenderer ??= new WebGLRenderer({ antialias: true, alpha: false, preserveDrawingBuffer: true });
    capture.outputColorSpace = SRGBColorSpace;
    capture.toneMapping = ACESFilmicToneMapping;
    capture.toneMappingExposure = this.renderer.toneMappingExposure;
    capture.setPixelRatio(1);
    capture.setSize(width, height, false);
    capture.setClearColor('#ffffff');
    this.state = {
      ...savedState, buildStep: step, explosion: 0, autoRotate: false, grid: false,
      background: 'white', selection: [], highlightedBrickIds: [], highlightStep: true,
    };
    this.actualExplosion = 0;
    this.assemblyProgress = 1;
    this.assemblyIds = new Set(this.manifest.instructions?.steps[step - 1]?.instanceIds ?? []);
    this.visible = visibleInstances(this.manifest, this.state);
    this.inventory = inventoryLayout(this.visible, width / height);
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.updateLayout();
    this.fit(true);
    this.scene.environment = null;
    capture.render(this.scene, this.camera);
    const dataUrl = capture.domElement.toDataURL('image/jpeg', 0.84);
    this.state = savedState;
    this.actualExplosion = savedExplosion;
    this.assemblyProgress = savedProgress;
    this.assemblyIds = savedIds;
    this.visible = visibleInstances(this.manifest, savedState);
    this.camera.position.copy(savedCamera);
    this.controls.target.copy(savedTarget);
    this.userDirection.copy(savedDirection);
    this.camera.fov = savedFov;
    this.camera.aspect = savedAspect;
    this.desiredTarget.copy(savedDesiredTarget);
    this.desiredPosition.copy(savedDesiredPosition);
    this.cameraMoving = savedCameraMoving;
    this.fitRequested = savedFitRequested;
    this.inventory = savedInventory;
    this.scene.environment = savedEnvironment;
    this.camera.updateProjectionMatrix();
    this.controls.update();
    this.renderer.setClearColor({ studio: '#f2f5f3', white: '#ffffff', dark: '#18201c' }[savedState.background]);
    this.updateLayout();
    const encoded = atob(dataUrl.slice(dataUrl.indexOf(',') + 1));
    const bytes = new Uint8Array(encoded.length);
    for (let index = 0; index < encoded.length; index++) bytes[index] = encoded.charCodeAt(index);
    return new Blob([bytes], { type: 'image/jpeg' });
  }

  private async renderBlob(width: number, height: number, type: 'image/png' | 'image/jpeg', quality?: number) {
    const max = this.renderer.capabilities.maxTextureSize;
    if (width > max || height > max) throw new Error(`设备最大导出边长为 ${max}px`);
    const oldSize = this.renderer.getSize(new Vector2());
    const oldRatio = this.renderer.getPixelRatio();
    const oldAspect = this.camera.aspect;
    this.renderer.setPixelRatio(1);
    this.renderer.setSize(width, height, false);
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.render(this.scene, this.camera);
    const blob = await new Promise<Blob>((resolve, reject) => this.renderer.domElement.toBlob(
      value => value ? resolve(value) : reject(new Error('图像编码失败')), type, quality,
    ));
    this.renderer.setPixelRatio(oldRatio);
    this.renderer.setSize(oldSize.x, oldSize.y, false);
    this.camera.aspect = oldAspect;
    this.camera.updateProjectionMatrix();
    this.dirty = true;
    return blob;
  }

  private pointerDown = (event: PointerEvent) => {
    this.pointers.add(event.pointerId);
    if (this.pointers.size > 1) this.multiTouch = true;
    this.pointerStart.set(event.clientX, event.clientY);
    this.maxPointerDistance = 0;
  };
  private pointerMove = (event: PointerEvent) => {
    if (this.pointers.size) this.maxPointerDistance = Math.max(this.maxPointerDistance, this.pointerStart.distanceTo(new Vector2(event.clientX, event.clientY)));
    if (this.pointers.size || event.pointerType === 'touch') return;
    const part = this.pick(event.clientX, event.clientY, event.altKey);
    this.renderer.domElement.style.cursor = part ? 'pointer' : 'grab';
    this.onHover(part, event.clientX, event.clientY);
  };
  private pointerUp = (event: PointerEvent) => {
    const distance = this.pointerStart.distanceTo(new Vector2(event.clientX, event.clientY));
    if (!this.multiTouch && this.maxPointerDistance < 6 && distance < 6 && event.button === 0) {
      const part = this.pick(event.clientX, event.clientY, event.altKey);
      this.onSelect(part?.instanceId ?? null);
    }
    this.pointers.delete(event.pointerId);
    if (!this.pointers.size) this.multiTouch = false;
  };
  private pointerCancel = (event: PointerEvent) => { this.pointers.delete(event.pointerId); if (!this.pointers.size) this.multiTouch = false; };
  private pointerLeave = () => this.onHover(null, 0, 0);
  private contextLost = (event: Event) => { event.preventDefault(); this.metrics.contextLost = true; this.callbacks.error('WebGL 上下文丢失，请重新加载模型。'); };
  private contextRestored = () => { this.metrics.contextLost = false; this.dirty = true; };
  private keydown = (event: KeyboardEvent) => {
    if (event.key === '+' || event.key === '=') { event.preventDefault(); this.zoom(0.85); }
    if (event.key === '-') { event.preventDefault(); this.zoom(1.15); }
    if (event.key === 'Escape') this.onSelect(null);
  };
  private attachEvents() {
    const canvas = this.renderer.domElement;
    canvas.addEventListener('pointerdown', this.pointerDown);
    canvas.addEventListener('pointermove', this.pointerMove);
    canvas.addEventListener('pointerup', this.pointerUp);
    canvas.addEventListener('pointercancel', this.pointerCancel);
    canvas.addEventListener('pointerleave', this.pointerLeave);
    canvas.addEventListener('webglcontextlost', this.contextLost);
    canvas.addEventListener('webglcontextrestored', this.contextRestored);
    canvas.addEventListener('keydown', this.keydown);
  }

  snapshot() {
    return {
      ...this.metrics,
      selected: [...this.state.selection],
      projected: this.visible.filter(p => this.loaded.has(p.groupId)).map(p => this.projectPart(p)),
      inventoryCells: this.inventory.cells,
      offsets: this.offsets.map(v => v.toArray()),
      camera: this.camera.position.toArray(),
    };
  }

  dispose() {
    this.disposed = true;
    cancelAnimationFrame(this.frame);
    this.worker?.terminate();
    this.motionPreference.removeEventListener('change', this.motionChanged);
    this.observer.disconnect();
    this.controls.dispose();
    const geometries = new Set<BufferGeometry>(), materials = new Set<Material>();
    this.scene.traverse(object => {
      const mesh = object as Mesh;
      if (mesh.geometry) geometries.add(mesh.geometry);
      if (mesh.material) (Array.isArray(mesh.material) ? mesh.material : [mesh.material]).forEach(m => materials.add(m));
    });
    for (const pick of this.picks.values()) { pick.mesh.geometry.dispose(); (pick.mesh.material as Material).dispose(); }
    geometries.forEach(g => g.dispose());
    materials.forEach(m => m.dispose());
    this.texture.dispose();
    this.environment.dispose();
    this.captureRenderer?.dispose();
    this.renderer.dispose();
    this.renderer.domElement.remove();
  }
}
