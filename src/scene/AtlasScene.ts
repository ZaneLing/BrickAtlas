import {
  ACESFilmicToneMapping, AmbientLight, Box3, BufferAttribute, BufferGeometry, Color, DataTexture, DirectionalLight, DoubleSide,
  FloatType, GridHelper, Group, HemisphereLight, LineSegments, Matrix4, Mesh, MeshBasicMaterial,
  MOUSE, NearestFilter, PCFSoftShadowMap, PerspectiveCamera, PlaneGeometry, PMREMGenerator, Raycaster, RGBAFormat,
  ShadowMaterial,
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
  private grid = new GridHelper(600, 30, 0xc8ceda, 0xe3e6ec);
  private ground: Mesh;
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
  private panMode = false;
  private requestedPixelRatio = Math.min(Math.max(devicePixelRatio, 2), 3);
  private drawingPixelLimit = Infinity;
  private actualExplosion = 0;
  private assemblyProgress = 1;
  private assemblyIds = new Set<string>();
  private assemblyOrder = new Map<string, number>();
  private settleFocusStep: number | null = null;
  private desiredTarget = new Vector3();
  private desiredPosition = new Vector3();
  private userDirection = new Vector3(-1, 0.7, 1);
  private raycaster = new Raycaster();
  private pointerStart = new Vector2();
  private maxPointerDistance = 0;
  private pointerActive = false;
  private lastTick = 0;
  private started = performance.now();
  private motionPreference = matchMedia('(prefers-reduced-motion: reduce)');
  private reducedMotion = this.motionPreference.matches;
  private lineObjects: LineSegments[] = [];
  private environment: import('three').WebGLRenderTarget;
  private captureRenderer: WebGLRenderer | null = null;
  private placementByInstance = new Map<string, { step: number; offset: Vector3 }>();
  private onSelect: Callbacks['select'];
  private onHover: Callbacks['hover'];

  constructor(private host: HTMLElement, readonly brickModel: BrickModel, private callbacks: Callbacks, private locale: 'zh' | 'en' = 'zh') {
    const manifest = brickModel.manifest;
    this.onSelect = callbacks.select;
    this.onHover = callbacks.hover;
    this.renderer = new WebGLRenderer({ antialias: true, alpha: false, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
    this.renderer.setClearColor('#f4f5f8');
    this.renderer.outputColorSpace = SRGBColorSpace;
    this.renderer.toneMapping = ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.12;
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = PCFSoftShadowMap;
    this.renderer.setPixelRatio(this.requestedPixelRatio);
    this.renderer.domElement.setAttribute('aria-label', `${manifest.model.title} ${this.text('交互式三维模型', 'interactive 3D model')}`);
    this.renderer.domElement.setAttribute('role', 'img');
    this.renderer.domElement.tabIndex = 0;
    host.appendChild(this.renderer.domElement);
    const extent = new Vector3(...manifest.bounds.max).sub(new Vector3(...manifest.bounds.min));
    const groundSize = Math.max(600, extent.length() * 3);
    this.ground = new Mesh(new PlaneGeometry(groundSize, groundSize), new ShadowMaterial({ color: 0x273342, opacity: 0.13 }));
    this.ground.rotation.x = -Math.PI / 2;
    this.ground.position.y = manifest.bounds.min[1] - 0.7;
    this.ground.receiveShadow = true;
    this.scene.add(this.model, this.grid, this.ground, new HemisphereLight(0xffffff, 0x8292ae, 2), new AmbientLight(0xffffff, 0.2));
    const key = new DirectionalLight(0xffffff, 3.3);
    key.position.set(-100, 180, 130);
    key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    const shadowExtent = Math.max(180, extent.length());
    key.shadow.camera.left = -shadowExtent;
    key.shadow.camera.right = shadowExtent;
    key.shadow.camera.top = shadowExtent;
    key.shadow.camera.bottom = -shadowExtent;
    key.shadow.camera.near = 1;
    key.shadow.camera.far = shadowExtent * 6;
    key.shadow.bias = -0.00015;
    this.scene.add(key);
    const fill = new DirectionalLight(0xdde7ff, 1.65);
    fill.position.set(100, 60, -130);
    const rim = new DirectionalLight(0xffdfca, 1.15);
    rim.position.set(20, 80, 170);
    this.scene.add(fill, rim);
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
    this.controls.enablePan = true;
    this.controls.screenSpacePanning = true;
    this.controls.panSpeed = 1;
    this.controls.minDistance = 8;
    this.controls.maxDistance = 6000;
    this.controls.autoRotateSpeed = 0.65;
    this.controls.addEventListener('change', this.invalidate);
    this.controls.addEventListener('start', this.controlStart);
    this.controls.addEventListener('end', this.controlEnd);
    this.stateData = new Float32Array(manifest.instances.length * 12);
    for (const part of manifest.instances) {
      const color = new Color(part.colorHex);
      this.stateData.set([color.r, color.g, color.b, 1], manifest.instances.length * 8 + part.index * 4);
    }
    this.texture = new DataTexture(this.stateData, manifest.instances.length, 3, RGBAFormat, FloatType);
    this.texture.minFilter = NearestFilter;
    this.texture.magFilter = NearestFilter;
    this.texture.needsUpdate = true;
    this.offsets = manifest.instances.map(() => new Vector3());
    manifest.instructions?.steps.forEach((step, index) => {
      if (step.kind !== 'placement' || !step.stagingOffset) return;
      for (const id of step.motionInstanceIds ?? []) {
        this.placementByInstance.set(id, { step: index + 1, offset: new Vector3(...step.stagingOffset) });
      }
    });
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
      if (data.type === 'progress') callbacks.progress(Math.min(98, data.downloaded / manifest.stats.compressedBytes * 100), this.text('读取模型几何', 'Loading model geometry'));
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
        callbacks.progress(100, this.text('模型就绪', 'Model ready'));
        callbacks.ready();
        this.worker.terminate();
      }
      if (data.type === 'error') { callbacks.error(data.message); this.worker.terminate(); }
    };
    this.worker.onerror = error => callbacks.error(error.message || this.text('模型解码工作线程失败', 'Geometry worker failed'));
    this.worker.postMessage({ base: new URL(`${import.meta.env.BASE_URL}models/${manifest.model.id}/`, location.href).href, chunks: manifest.chunks });
    this.frame = requestAnimationFrame(this.tick);
  }

  get manifest() { return this.brickModel.manifest; }
  private text(zh: string, en: string) { return this.locale === 'zh' ? zh : en; }
  setLocale(locale: 'zh' | 'en') {
    this.locale = locale;
    this.renderer.domElement.setAttribute('aria-label', `${this.manifest.model.title} ${this.text('交互式三维模型', 'interactive 3D model')}`);
  }
  setPanMode(enabled: boolean) {
    this.panMode = enabled;
    this.controls.mouseButtons.LEFT = enabled || this.actualExplosion > 0.98 ? MOUSE.PAN : MOUSE.ROTATE;
    this.controls.enableRotate = !enabled && this.actualExplosion < 0.98;
    this.renderer.domElement.style.cursor = enabled ? 'grab' : '';
    this.dirty = true;
  }
  private invalidate = () => { this.dirty = true; };
  private motionChanged = () => {
    this.reducedMotion = this.motionPreference.matches;
    this.setState(this.state);
  };
  private controlStart = () => {
    this.interaction = true;
    this.cameraMoving = false;
    this.settleFocusStep = null;
    if (this.panMode) this.renderer.domElement.style.cursor = 'grabbing';
    this.callbacks.hover(null, 0, 0);
  };
  private controlEnd = () => {
    this.interaction = false;
    this.renderer.domElement.style.cursor = this.panMode ? 'grab' : '';
    this.userDirection.copy(this.camera.position).sub(this.controls.target).normalize();
  };

  private resize = () => {
    const { width, height } = this.host.getBoundingClientRect();
    if (!width || !height || this.disposed) return;
    const current = this.renderer.getSize(new Vector2());
    if (Math.abs(current.x - width) > 0.5 || Math.abs(current.y - height) > 0.5) {
      this.renderer.setSize(width, height);
    }
    this.applyPixelRatio(width, height);
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.inventory = inventoryLayout(this.visible, this.camera.aspect);
    this.fitRequested = true;
    this.updateLayout();
    this.fit();
  };

  private applyPixelRatio(width: number, height: number) {
    const gl = this.renderer.getContext();
    const viewport = gl.getParameter(gl.MAX_VIEWPORT_DIMS) as Int32Array;
    const maximumRatio = Math.min(
      this.renderer.capabilities.maxTextureSize / width,
      this.renderer.capabilities.maxTextureSize / height,
      viewport[0] / width,
      viewport[1] / height,
      Math.sqrt(this.drawingPixelLimit / (width * height)),
    );
    let pixelRatio = Math.max(1, Math.min(this.requestedPixelRatio, maximumRatio));
    if (Math.abs(this.renderer.getPixelRatio() - pixelRatio) > 0.001) {
      this.renderer.setPixelRatio(pixelRatio);
    }
    const expectedWidth = Math.floor(width * pixelRatio);
    const expectedHeight = Math.floor(height * pixelRatio);
    const drawingWidth = gl.drawingBufferWidth;
    const drawingHeight = gl.drawingBufferHeight;
    if (drawingWidth + 1 < expectedWidth || drawingHeight + 1 < expectedHeight) {
      this.drawingPixelLimit = Math.min(this.drawingPixelLimit, drawingWidth * drawingHeight);
      pixelRatio = Math.min(this.requestedPixelRatio, maximumRatio) * Math.min(
        drawingWidth / expectedWidth,
        drawingHeight / expectedHeight,
      ) * 0.98;
      this.renderer.setPixelRatio(Math.max(1, pixelRatio));
    }
  }

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
      if (bucket.kind === 'mesh' && bucket.material.opacity >= 1) object.castShadow = true;
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
    const activeStep = state.buildStep ? this.manifest.instructions?.steps[state.buildStep - 1] : undefined;
    const visibilityChanged = previous.hiddenGroups.join() !== state.hiddenGroups.join()
      || previous.hiddenBrickIds.join() !== state.hiddenBrickIds.join()
      || previous.isolation?.join() !== state.isolation?.join()
      || previous.buildStep !== state.buildStep;
    const viewChanged = previous.view !== state.view || previous.revision !== state.revision;
    const assemblyChanged = previous.buildStep !== state.buildStep || previous.assemblyRevision !== state.assemblyRevision;
    if (assemblyChanged && state.buildStep !== null && state.buildStep > 0
      && (previous.buildStep === null || state.buildStep >= (previous.buildStep ?? 0))) {
      const ids = activeStep?.motionInstanceIds ?? activeStep?.instanceIds ?? [];
      this.assemblyIds = new Set(ids);
      this.assemblyOrder = new Map(ids.map((id, index) => [id, index]));
      this.assemblyProgress = this.reducedMotion ? 1 : 0;
    } else if (assemblyChanged) {
      this.assemblyIds.clear();
      this.assemblyOrder.clear();
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
    this.renderer.shadowMap.enabled = state.buildStep === null;
    this.requestedPixelRatio = state.quality === 'low' ? 1 : state.quality === 'ultra' ? 4
      : state.quality === 'high' ? 3 : Math.min(Math.max(devicePixelRatio, 2), 3);
    const { width, height } = this.host.getBoundingClientRect();
    if (width && height) this.applyPixelRatio(width, height);
    if (previous.xray !== state.xray) this.model.traverse(object => {
      const material = (object as Mesh).material;
      if (material) (Array.isArray(material) ? material : [material]).forEach(item => setAtlasXray(item, state.xray));
    });
    if (previous.background !== state.background) {
    this.renderer.setClearColor({ studio: '#f4f5f8', white: '#ffffff', dark: '#171c2c' }[state.background]);
    }
    if (previous.explosion !== state.explosion || viewChanged || visibilityChanged) this.fitRequested = true;
    if (this.reducedMotion) this.actualExplosion = state.explosion;
    this.updateLayout();
    if (this.fitRequested) this.fit();
  }

  private updateLayout() {
    const visible = new Set(this.visible.map(p => p.instanceId));
    const activeStep = this.state.buildStep && this.manifest.instructions
      ? this.manifest.instructions.steps[this.state.buildStep - 1] : undefined;
    const currentStep = activeStep?.motionInstanceIds ?? activeStep?.instanceIds ?? [];
    const selected = new Set([...this.state.selection, ...this.state.highlightedBrickIds, ...(this.state.highlightStep ? currentStep : [])]);
    const n = this.manifest.instances.length;
    for (const part of this.manifest.instances) {
      const offset = new Vector3(...explosionOffset(part, this.actualExplosion, this.manifest, this.inventory));
      const placement = this.state.buildStep === null ? undefined : this.placementByInstance.get(part.instanceId);
      if (placement && this.state.buildStep! <= placement.step) {
        const amount = this.state.buildStep === placement.step ? 1 - smoothstep(this.assemblyProgress) : 1;
        offset.addScaledVector(placement.offset, amount);
      }
      if (this.assemblyProgress < 1 && this.assemblyIds.has(part.instanceId) && activeStep?.kind !== 'placement') {
        const direction = new Vector3(...(this.manifest.groups.find(group => group.id === part.groupId)?.direction ?? [0, 1, 0]));
        direction.y += 55;
        if (!direction.lengthSq()) direction.set(0, 1, 0);
        const size = new Vector3(...part.bounds.max).sub(new Vector3(...part.bounds.min)).length();
        const order = this.assemblyOrder.get(part.instanceId) ?? 0;
        const span = 1 + Math.max(0, this.assemblyIds.size - 1) * 0.12;
        const localProgress = Math.max(0, Math.min(1, this.assemblyProgress * span - order * 0.12));
        offset.add(direction.normalize().multiplyScalar(Math.max(70, size * 2.5) * (1 - smoothstep(localProgress))));
      }
      this.offsets[part.index].copy(offset);
      this.stateData.set([offset.x, offset.y, offset.z, Number(visible.has(part.instanceId))], part.index * 4);
      this.stateData[n * 4 + part.index * 4] = Number(selected.has(part.instanceId));
    }
    this.texture.needsUpdate = true;
    this.metrics.visibleInstances = this.visible.filter(p => this.loaded.has(p.groupId)).length;
    this.metrics.actualExplosion = this.actualExplosion;
    this.grid.visible = this.state.grid && this.actualExplosion < 0.02;
    this.ground.visible = this.state.buildStep === null && this.actualExplosion < 0.98;
    this.controls.mouseButtons.LEFT = this.panMode || this.actualExplosion > 0.98 ? MOUSE.PAN : MOUSE.ROTATE;
    this.controls.enableRotate = !this.panMode && this.actualExplosion < 0.98;
    this.dirty = true;
  }

  private fit(immediate = false) {
    if (!this.visible.length) { this.fitRequested = false; return; }
    const inventoryMix = Math.max(0, Math.min(1, (this.actualExplosion - 0.45) / 0.55));
    const inventoryDirection = new Vector3(0, 0, 1).applyMatrix4(inventoryRotation.clone().invert());
    const direction = this.userDirection.clone().normalize().lerp(inventoryDirection, inventoryMix).normalize();
    this.camera.fov = 34 - inventoryMix * 18;
    this.camera.updateProjectionMatrix();
    const temporary = new PerspectiveCamera(this.camera.fov, this.camera.aspect);
    temporary.position.copy(direction);
    temporary.lookAt(new Vector3());
    temporary.updateMatrixWorld();
    const worldToView = new Matrix4().makeRotationFromQuaternion(temporary.quaternion).invert();
    const viewBox = new Box3();
    for (const part of this.visible) {
      const offset = this.offsets[part.index];
      viewBox.union(this.partBox(part).translate(offset).applyMatrix4(worldToView));
    }
    const viewCenter = viewBox.getCenter(new Vector3());
    this.desiredTarget.copy(viewCenter).applyMatrix4(worldToView.clone().invert());
    const tan = Math.tan(this.camera.fov * Math.PI / 360);
    const halfWidth = Math.max(viewBox.max.x - viewCenter.x, viewCenter.x - viewBox.min.x);
    const halfHeight = Math.max(viewBox.max.y - viewCenter.y, viewCenter.y - viewBox.min.y);
    const nearDepth = Math.max(0, viewBox.max.z - viewCenter.z);
    const padding = 1.15 + inventoryMix * 0.13;
    const fitDistance = Math.max(
      halfHeight / tan,
      halfWidth / tan / this.camera.aspect,
      20,
    ) * padding + nearDepth;
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
    this.focusInstances(this.state.selection, 1.5, true);
  }

  focusBuildStep(step: number) {
    const instruction = this.manifest.instructions?.steps[step - 1];
    this.settleFocusStep = instruction ? step : null;
    this.focusInstances(
      instruction?.motionInstanceIds ?? instruction?.instanceIds ?? [],
      instruction?.kind === 'placement' ? 1.45 : 1.7,
      true,
      true,
    );
  }

  private focusInstances(ids: string[], padding: number, useOffsets = false, includeFinal = false) {
    const selected = new Set(ids);
    const chosen = this.manifest.instances.filter(part => selected.has(part.instanceId));
    if (!chosen.length) return;
    const box = new Box3();
    for (const part of chosen) {
      const bounds = new Box3(new Vector3(...part.bounds.min), new Vector3(...part.bounds.max));
      if (!useOffsets || includeFinal) box.union(bounds);
      if (useOffsets) box.union(bounds.clone().translate(this.offsets[part.index]));
    }
    box.getCenter(this.desiredTarget);
    const direction = this.userDirection.clone().normalize();
    const camera = new PerspectiveCamera(34, this.camera.aspect);
    camera.position.copy(this.desiredTarget).add(direction);
    camera.lookAt(this.desiredTarget);
    camera.updateMatrixWorld();
    const local = box.clone().translate(this.desiredTarget.clone().negate()).applyMatrix4(new Matrix4().makeRotationFromQuaternion(camera.quaternion).invert());
    const tan = Math.tan(34 * Math.PI / 360);
    const distance = Math.max(
      Math.max(local.max.y, -local.min.y) / tan,
      Math.max(local.max.x, -local.min.x) / tan / this.camera.aspect,
      14,
    ) * padding + local.max.z;
    this.camera.fov = 34;
    this.camera.updateProjectionMatrix();
    this.desiredPosition.copy(this.desiredTarget).addScaledVector(direction, distance);
    this.cameraMoving = true;
    this.fitRequested = false;
    this.dirty = true;
  }

  zoom(factor: number) {
    const delta = this.camera.position.clone().sub(this.controls.target).multiplyScalar(factor);
    if (delta.length() < this.controls.minDistance || delta.length() > this.controls.maxDistance) return;
    this.camera.position.copy(this.controls.target).add(delta);
    this.cameraMoving = false;
    this.controls.update();
    this.dirty = true;
  }

  pan(deltaX: number, deltaY: number) {
    const height = Math.max(1, this.renderer.domElement.clientHeight);
    const distance = this.camera.position.distanceTo(this.controls.target);
    const scale = 2 * distance * Math.tan(this.camera.fov * Math.PI / 360) / height;
    const right = new Vector3(1, 0, 0).applyQuaternion(this.camera.quaternion);
    const up = new Vector3(0, 1, 0).applyQuaternion(this.camera.quaternion);
    const shift = right.multiplyScalar(-deltaX * scale).add(up.multiplyScalar(deltaY * scale));
    this.camera.position.add(shift);
    this.controls.target.add(shift);
    this.desiredPosition.add(shift);
    this.desiredTarget.add(shift);
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
      const wasAnimating = this.assemblyProgress < 1;
      const settleStep = this.settleFocusStep;
      this.assemblyProgress = Math.min(1, this.assemblyProgress + dt / 0.95);
      this.updateLayout();
      if (
        wasAnimating &&
        this.assemblyProgress === 1 &&
        settleStep !== null &&
        settleStep === this.state.buildStep &&
        !this.interaction
      ) {
        const step = this.manifest.instructions?.steps[settleStep - 1];
        this.focusInstances(
          step?.motionInstanceIds ?? step?.instanceIds ?? [],
          step?.kind === 'placement' ? 1.45 : 1.7,
        );
        this.settleFocusStep = null;
      }
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
      let closest: PartInstance | null = null, distance = 12;
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
    const center = this.partBox(part).getCenter(new Vector3()).add(this.offsets[part.index]);
    center.project(this.camera);
    const { width, height } = this.renderer.domElement.getBoundingClientRect();
    return { id: part.instanceId, x: (center.x + 1) / 2 * width, y: (1 - center.y) / 2 * height, z: center.z };
  }

  private partBox(part: PartInstance) {
    return this.picks.get(part.index)?.box.clone()
      ?? new Box3(new Vector3(...part.bounds.min), new Vector3(...part.bounds.max));
  }

  private projectedFraming() {
    const { width, height } = this.renderer.domElement.getBoundingClientRect();
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    let insideInstances = 0;
    let totalInstances = 0;
    for (const part of this.visible) {
      if (!this.loaded.has(part.groupId)) continue;
      totalInstances++;
      const bounds = this.partBox(part).translate(this.offsets[part.index]);
      const { min, max } = bounds;
      let inside = true;
      for (const x of [min.x, max.x]) {
        for (const y of [min.y, max.y]) {
          for (const z of [min.z, max.z]) {
            const point = new Vector3(x, y, z).project(this.camera);
            const screenX = (point.x + 1) / 2 * width;
            const screenY = (1 - point.y) / 2 * height;
            minX = Math.min(minX, screenX);
            maxX = Math.max(maxX, screenX);
            minY = Math.min(minY, screenY);
            maxY = Math.max(maxY, screenY);
            inside &&= point.z >= -1 && point.z <= 1
              && screenX >= 0 && screenX <= width
              && screenY >= 0 && screenY <= height;
          }
        }
      }
      if (inside) insideInstances++;
    }
    return {
      width,
      height,
      minX,
      maxX,
      minY,
      maxY,
      insideInstances,
      totalInstances,
    };
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

  async captureBuildStep(
    step: number,
    width = 960,
    height = 720,
    options: { progress?: number; focusStep?: boolean; shadows?: boolean; motionInstanceId?: string } = {},
  ) {
    const savedState = this.state;
    const savedExplosion = this.actualExplosion;
    const savedProgress = this.assemblyProgress;
    const savedIds = this.assemblyIds;
    const savedOrder = this.assemblyOrder;
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
    const savedGroundVisible = this.ground.visible;
    const activeStep = this.manifest.instructions?.steps[step - 1];
    const capture = this.captureRenderer ??= new WebGLRenderer({ antialias: true, alpha: false, preserveDrawingBuffer: true });
    capture.outputColorSpace = SRGBColorSpace;
    capture.toneMapping = ACESFilmicToneMapping;
    capture.toneMappingExposure = this.renderer.toneMappingExposure;
    capture.shadowMap.enabled = options.shadows ?? true;
    capture.shadowMap.type = PCFSoftShadowMap;
    capture.setPixelRatio(1);
    capture.setSize(width, height, false);
    capture.setClearColor('#ffffff');
    this.state = {
      ...savedState, buildStep: step, explosion: 0, autoRotate: false, grid: false,
      background: 'white', selection: [], highlightedBrickIds: [], highlightStep: false,
    };
    this.actualExplosion = 0;
    this.assemblyProgress = options.focusStep ? 0 : options.progress ?? 1;
    const motionIds = options.motionInstanceId
      ? [options.motionInstanceId]
      : activeStep?.motionInstanceIds ?? activeStep?.instanceIds ?? [];
    this.assemblyIds = new Set(motionIds);
    this.assemblyOrder = new Map(motionIds.map((id, index) => [id, index]));
    this.visible = visibleInstances(this.manifest, this.state);
    this.inventory = inventoryLayout(this.visible, width / height);
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.updateLayout();
    if (options.focusStep) this.focusInstances(
      [...this.assemblyIds],
      activeStep?.kind === 'placement' ? 1.55 : 1.9,
      true,
      true,
    );
    else this.fit(true);
    if (options.focusStep) {
      this.camera.position.copy(this.desiredPosition);
      this.controls.target.copy(this.desiredTarget);
      this.controls.update();
      this.cameraMoving = false;
      this.assemblyProgress = options.progress ?? 1;
      this.updateLayout();
    }
    this.scene.environment = null;
    this.ground.visible = options.shadows ?? true;
    capture.render(this.scene, this.camera);
    const dataUrl = capture.domElement.toDataURL('image/jpeg', 0.84);
    this.state = savedState;
    this.actualExplosion = savedExplosion;
    this.assemblyProgress = savedProgress;
    this.assemblyIds = savedIds;
    this.assemblyOrder = savedOrder;
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
    this.ground.visible = savedGroundVisible;
    this.camera.updateProjectionMatrix();
    this.controls.update();
    this.renderer.setClearColor({ studio: '#f4f5f8', white: '#ffffff', dark: '#171c2c' }[savedState.background]);
    this.updateLayout();
    const encoded = atob(dataUrl.slice(dataUrl.indexOf(',') + 1));
    const bytes = new Uint8Array(encoded.length);
    for (let index = 0; index < encoded.length; index++) bytes[index] = encoded.charCodeAt(index);
    return new Blob([bytes], { type: 'image/jpeg' });
  }

  private async renderBlob(width: number, height: number, type: 'image/png' | 'image/jpeg', quality?: number) {
    const max = this.renderer.capabilities.maxTextureSize;
    if (width > max || height > max) throw new Error(this.text(`设备最大导出边长为 ${max}px`, `Maximum export dimension on this device is ${max}px`));
    const oldSize = this.renderer.getSize(new Vector2());
    const oldRatio = this.renderer.getPixelRatio();
    const oldAspect = this.camera.aspect;
    this.renderer.setPixelRatio(1);
    this.renderer.setSize(width, height, false);
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.render(this.scene, this.camera);
    const blob = await new Promise<Blob>((resolve, reject) => this.renderer.domElement.toBlob(
      value => value ? resolve(value) : reject(new Error(this.text('图像编码失败', 'Image encoding failed'))), type, quality,
    ));
    this.renderer.setPixelRatio(oldRatio);
    this.renderer.setSize(oldSize.x, oldSize.y, false);
    this.camera.aspect = oldAspect;
    this.camera.updateProjectionMatrix();
    this.dirty = true;
    return blob;
  }

  private pointerDown = (event: PointerEvent) => {
    this.pointerActive = true;
    this.pointerStart.set(event.clientX, event.clientY);
    this.maxPointerDistance = 0;
  };
  private pointerMove = (event: PointerEvent) => {
    if (this.pointerActive) this.maxPointerDistance = Math.max(this.maxPointerDistance, this.pointerStart.distanceTo(new Vector2(event.clientX, event.clientY)));
    if (this.pointerActive) return;
    if (this.panMode) {
      this.renderer.domElement.style.cursor = 'grab';
      this.onHover(null, 0, 0);
      return;
    }
    const part = this.pick(event.clientX, event.clientY, event.altKey);
    this.renderer.domElement.style.cursor = part ? 'pointer' : '';
    this.onHover(part, event.clientX, event.clientY);
  };
  private pointerUp = (event: PointerEvent) => {
    const distance = this.pointerStart.distanceTo(new Vector2(event.clientX, event.clientY));
    if (this.maxPointerDistance < 6 && distance < 6 && event.button === 0) {
      const part = this.pick(event.clientX, event.clientY, event.altKey);
      this.onSelect(part?.instanceId ?? null);
    }
    this.pointerActive = false;
  };
  private pointerCancel = () => { this.pointerActive = false; };
  private pointerLeave = () => this.onHover(null, 0, 0);
  private contextLost = (event: Event) => { event.preventDefault(); this.metrics.contextLost = true; this.callbacks.error(this.text('WebGL 上下文丢失，请重新加载模型。', 'WebGL context lost. Reload the model.')); };
  private contextRestored = () => { this.metrics.contextLost = false; this.dirty = true; };
  private keydown = (event: KeyboardEvent) => {
    if (event.key === '+' || event.key === '=') { event.preventDefault(); this.zoom(0.85); }
    if (event.key === '-') { event.preventDefault(); this.zoom(1.15); }
    if (event.key === 'ArrowUp') { event.preventDefault(); this.pan(0, 32); }
    if (event.key === 'ArrowDown') { event.preventDefault(); this.pan(0, -32); }
    if (event.key === 'ArrowLeft') { event.preventDefault(); this.pan(32, 0); }
    if (event.key === 'ArrowRight') { event.preventDefault(); this.pan(-32, 0); }
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

  private detachEvents() {
    const canvas = this.renderer.domElement;
    canvas.removeEventListener('pointerdown', this.pointerDown);
    canvas.removeEventListener('pointermove', this.pointerMove);
    canvas.removeEventListener('pointerup', this.pointerUp);
    canvas.removeEventListener('pointercancel', this.pointerCancel);
    canvas.removeEventListener('pointerleave', this.pointerLeave);
    canvas.removeEventListener('webglcontextlost', this.contextLost);
    canvas.removeEventListener('webglcontextrestored', this.contextRestored);
    canvas.removeEventListener('keydown', this.keydown);
  }

  snapshot() {
    const gl = this.renderer.getContext();
    const viewport = gl.getParameter(gl.MAX_VIEWPORT_DIMS) as Int32Array;
    return {
      ...this.metrics,
      selected: [...this.state.selection],
      projected: this.visible.filter(p => this.loaded.has(p.groupId)).map(p => this.projectPart(p)),
      inventoryCells: this.inventory.cells,
      offsets: this.offsets.map(v => v.toArray()),
      camera: this.camera.position.toArray(),
      target: this.controls.target.toArray(),
      panMode: this.panMode,
      buildStep: this.state.buildStep,
      requestedExplosion: this.state.explosion,
      autoRotate: this.controls.autoRotate,
      controlsEnabled: this.controls.enabled,
      pixelRatio: this.renderer.getPixelRatio(),
      renderBuffer: {
        width: this.renderer.domElement.width,
        height: this.renderer.domElement.height,
        drawingWidth: gl.drawingBufferWidth,
        drawingHeight: gl.drawingBufferHeight,
        maxWidth: Math.min(this.renderer.capabilities.maxTextureSize, viewport[0]),
        maxHeight: Math.min(this.renderer.capabilities.maxTextureSize, viewport[1]),
      },
      framing: this.projectedFraming(),
    };
  }

  dispose() {
    this.disposed = true;
    cancelAnimationFrame(this.frame);
    this.worker?.terminate();
    this.motionPreference.removeEventListener('change', this.motionChanged);
    this.observer.disconnect();
    this.detachEvents();
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
    this.captureRenderer?.forceContextLoss();
    this.renderer.dispose();
    this.renderer.forceContextLoss();
    this.renderer.domElement.remove();
  }
}
