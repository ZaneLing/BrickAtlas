import {
  ACESFilmicToneMapping, AmbientLight, Box3, Color, CylinderGeometry, DirectionalLight, DataTexture,
  FloatType, RGBAFormat, NearestFilter, LineSegments, Matrix3, BoxGeometry,
  DynamicDrawUsage, Group, HemisphereLight, InstancedMesh, Matrix4, Mesh, MeshPhysicalMaterial,
  MOUSE, PerspectiveCamera, PlaneGeometry, Quaternion, Scene, ShadowMaterial, SRGBColorSpace, Vector3, WebGLRenderer,
  type BufferGeometry, type Material,
} from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import type { ImageBrick, ImageBrickBuild } from '../creator/imageBrickModel';
import { atlasMaterial } from './materials';
import type { SourceGeometry } from './sourceGeometry';

type VisualBrick = {
  brick: ImageBrick;
  base: Vector3;
  direction: Vector3;
  rotation: Quaternion;
  enter: number;
  visible: boolean;
};

type BodyBatch = {
  mesh: InstancedMesh;
  visuals: VisualBrick[];
};

type StudBatch = {
  mesh: InstancedMesh;
  studs: { visual: VisualBrick; offsetX: number; offsetZ: number }[];
};

const unit = 12;
const smooth = (value: number) => value * value * (3 - 2 * value);
export type ImageBrickView = 'perspective' | 'front' | 'side' | 'top';

export class ImageBrickScene {
  private readonly scene = new Scene();
  private readonly model = new Group();
  private readonly camera = new PerspectiveCamera(34, 1, 0.1, 5000);
  private readonly renderer = new WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
  private readonly controls: OrbitControls;
  private readonly observer: ResizeObserver;
  private readonly bodyBatches: BodyBatch[] = [];
  private readonly studBatches: StudBatch[] = [];
  private visuals: VisualBrick[] = [];
  private readonly sourceBatches: { visuals: VisualBrick[]; texture: DataTexture; data: Float32Array }[] = [];
  private sources: ReadonlyMap<string, SourceGeometry> = new Map();
  private buildRevision = 0;
  private renderedFrames = 0;
  private instanceDirty = false;
  private readonly disposableGeometries = new Set<BufferGeometry>();
  private readonly disposableMaterials = new Set<Material>();
  private readonly matrix = new Matrix4();
  private readonly position = new Vector3();
  private readonly scale = new Vector3(1, 1, 1);
  private readonly studOffset = new Vector3();
  private frame = 0;
  private lastTick = 0;
  private lastFrameMs = 0;
  private disposed = false;
  private dirty = true;
  private cameraMoving = false;
  private panMode = false;
  private view: ImageBrickView = 'perspective';
  private readonly desiredPosition = new Vector3();
  private readonly desiredTarget = new Vector3();
  private currentStep = 0;
  private explosion = 0;
  private actualExplosion = 0;
  private build: ImageBrickBuild | null = null;

  constructor(private host: HTMLElement, label: string) {
    this.renderer.outputColorSpace = SRGBColorSpace;
    this.renderer.toneMapping = ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.08;
    this.renderer.shadowMap.enabled = true;
    this.renderer.setClearColor('#f2f4f8');
    this.renderer.setPixelRatio(3);
    this.renderer.domElement.setAttribute('role', 'img');
    this.renderer.domElement.setAttribute('aria-label', label);
    host.appendChild(this.renderer.domElement);

    this.scene.add(this.model, new HemisphereLight(0xffffff, 0x78859d, 2.1), new AmbientLight(0xffffff, 0.35));
    const key = new DirectionalLight(0xffffff, 3.6);
    key.position.set(-120, 180, 110);
    key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    const rim = new DirectionalLight(0xffd9c7, 1.2);
    rim.position.set(120, 80, -100);
    this.scene.add(key, rim);

    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.08;
    this.controls.autoRotate = true;
    this.controls.autoRotateSpeed = 0.55;
    this.controls.enablePan = false;
    this.controls.addEventListener('change', this.invalidate);
    this.controls.addEventListener('start', this.controlStart);
    this.controls.addEventListener('end', this.controlEnd);
    this.observer = new ResizeObserver(this.resize);
    this.observer.observe(host);
    this.resize();
    this.frame = requestAnimationFrame(this.tick);
  }

  setLabel(label: string) {
    this.renderer.domElement.setAttribute('aria-label', label);
  }

  setSources(sources: ReadonlyMap<string, SourceGeometry>) { this.sources = sources; }

  setBuild(build: ImageBrickBuild, fit = true) {
    this.clearModel();
    this.build = build;
    this.currentStep = build.steps.length;
    this.buildRevision++;
    const visuals = build.bricks.map(brick => {
      const base = new Vector3(brick.x * unit, brick.y * unit, brick.z * unit);
      const direction = new Vector3(brick.x, 0.45 + brick.y * 0.22, brick.z);
      if (direction.lengthSq() < 0.01) direction.set(0, 1, 0);
      const rotation = new Quaternion().setFromAxisAngle(
        new Vector3(0, 1, 0),
        (brick.rotation ?? 0) * Math.PI / 2,
      );
      return { brick, base, direction: direction.normalize(), rotation, enter: 1, visible: true };
    });
    this.visuals = visuals;
    const sourceIds = new Set(build.sourceGroups?.flatMap(group => group.brickIds) ?? []);
    const materials = new Map<string, MeshPhysicalMaterial>();
    const materialFor = (color: string) => {
      let material = materials.get(color);
      if (!material) {
        material = new MeshPhysicalMaterial({
          color: new Color(color),
          roughness: 0.27,
          metalness: 0.015,
          clearcoat: 0.3,
          clearcoatRoughness: 0.28,
        });
        materials.set(color, material);
        this.disposableMaterials.add(material);
      }
      return material;
    };
    const bodies = new Map<string, VisualBrick[]>();
    for (const visual of visuals) {
      if (sourceIds.has(visual.brick.id)) continue;
      const key = [
        visual.brick.width,
        visual.brick.depth ?? 1,
        visual.brick.height ?? 1.2,
        visual.brick.shape ?? 'box',
        visual.brick.colorHex,
      ].join(':');
      if (!bodies.has(key)) bodies.set(key, []);
      bodies.get(key)!.push(visual);
    }
    for (const [key, batchVisuals] of bodies) {
      const [width, depth, height] = key.split(':').map(Number);
      const shape = batchVisuals[0].brick.shape;
      const geometry = shape === 'round' ? new CylinderGeometry(width * unit / 2 - 0.35, width * unit / 2 - 0.35, height * unit - 0.55, 24)
        : shape === 'slope' ? new BoxGeometry(width * unit - 0.7, height * unit - 0.55, depth * unit - 0.7)
        : new RoundedBoxGeometry(
        width * unit - 0.7,
        height * unit - 0.55,
        depth * unit - 0.7,
        2,
        0.65,
      );
      if (shape === 'slope') {
        const position = geometry.getAttribute('position');
        for (let index = 0; index < position.count; index++) {
          if (position.getY(index) > 0 && position.getZ(index) > 0) position.setY(index, -height * unit / 2 + unit * 0.4);
        }
        geometry.computeVertexNormals();
      }
      this.disposableGeometries.add(geometry);
      const mesh = new InstancedMesh(geometry, materialFor(batchVisuals[0].brick.colorHex), batchVisuals.length);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      mesh.instanceMatrix.setUsage(DynamicDrawUsage);
      mesh.frustumCulled = false;
      this.model.add(mesh);
      this.bodyBatches.push({ mesh, visuals: batchVisuals });
    }
    const studGeometry = new CylinderGeometry(unit * 0.3, unit * 0.3, unit * 0.16, 24);
    this.disposableGeometries.add(studGeometry);
    const studs = new Map<string, { visual: VisualBrick; offsetX: number; offsetZ: number }[]>();
    for (const visual of visuals) {
      if (sourceIds.has(visual.brick.id) || visual.brick.shape === 'tile' || visual.brick.shape === 'slope') continue;
      if (!studs.has(visual.brick.colorHex)) studs.set(visual.brick.colorHex, []);
      for (let x = 0; x < visual.brick.width; x++) {
        for (let z = 0; z < (visual.brick.depth ?? 1); z++) {
          studs.get(visual.brick.colorHex)!.push({
            visual,
            offsetX: (x - (visual.brick.width - 1) / 2) * unit,
            offsetZ: (z - ((visual.brick.depth ?? 1) - 1) / 2) * unit,
          });
        }
      }
    }
    for (const [color, batchStuds] of studs) {
      const mesh = new InstancedMesh(studGeometry, materialFor(color), batchStuds.length);
      mesh.castShadow = true;
      mesh.instanceMatrix.setUsage(DynamicDrawUsage);
      mesh.frustumCulled = false;
      this.model.add(mesh);
      this.studBatches.push({ mesh, studs: batchStuds });
    }
    const byId = new Map(visuals.map(visual => [visual.brick.id, visual]));
    for (const group of build.sourceGroups ?? []) {
      const source = this.sources.get(group.modelId);
      if (!source) throw new Error(`Source geometry not loaded: ${group.modelId}`);
      const count = group.brickIds.length;
      const data = new Float32Array(count * 12);
      const texture = new DataTexture(data, count, 3, RGBAFormat, FloatType);
      texture.minFilter = texture.magFilter = NearestFilter;
      const sourceVisuals = group.brickIds.map(id => byId.get(id)!);
      sourceVisuals.forEach((visual, index) => {
        const color = new Color(visual.brick.colorHex);
        data.set([color.r, color.g, color.b, 1], count * 8 + index * 4);
      });
      this.sourceBatches.push({ visuals: sourceVisuals, data, texture });
      const transform = new Matrix4().fromArray(group.matrix);
      const directionTransform = new Matrix3().setFromMatrix4(transform);
      for (const bucket of source.buckets) {
        const geometry = bucket.geometry.clone();
        geometry.applyMatrix4(transform);
        for (const name of ['control0', 'control1', 'direction']) {
          const attribute = geometry.getAttribute(name);
          if (!attribute) continue;
          const vector = new Vector3();
          for (let index = 0; index < attribute.count; index++) {
            vector.fromBufferAttribute(attribute, index);
            if (name === 'direction') vector.applyMatrix3(directionTransform);
            else vector.applyMatrix4(transform);
            attribute.setXYZ(index, vector.x, vector.y, vector.z);
          }
        }
        const material = atlasMaterial(bucket.definition, texture, count);
        const mesh = bucket.definition.kind === 'mesh' ? new Mesh(geometry, material) : new LineSegments(geometry, material);
        mesh.frustumCulled = false;
        this.model.add(mesh);
        this.disposableGeometries.add(geometry);
        this.disposableMaterials.add(material);
      }
    }
    const groundSize = Math.max(build.width, build.height, build.maxDepth) * unit * 2.3;
    const ground = new Mesh(new PlaneGeometry(groundSize, groundSize), new ShadowMaterial({ color: 0x283247, opacity: 0.13 }));
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -0.2;
    ground.receiveShadow = true;
    ground.name = 'image-brick-ground';
    this.scene.add(ground);
    this.disposableGeometries.add(ground.geometry);
    this.disposableMaterials.add(ground.material as Material);
    if (fit) this.fitVisible(true);
    this.updateInstances();
    this.dirty = true;
  }

  setBuildStep(step: number, animate = true) {
    if (!this.build) return;
    const next = Math.max(0, Math.min(this.build.steps.length, Math.round(step)));
    for (const visual of this.visuals) {
        const wasVisible = visual.visible;
        visual.visible = visual.brick.step <= next;
        if (animate && visual.visible && !wasVisible) visual.enter = 0;
        if (!visual.visible) visual.enter = 1;
    }
    this.currentStep = next;
    this.instanceDirty = true;
    this.dirty = true;
  }

  setExplosion(value: number) {
    this.explosion = Math.max(0, Math.min(1, value));
    this.dirty = true;
  }

  setAutoRotate(enabled: boolean) {
    this.controls.autoRotate = enabled;
    if (!enabled) {
      const damping = this.controls.enableDamping;
      this.controls.enableDamping = false;
      this.controls.update();
      this.controls.enableDamping = damping;
    }
    this.dirty = true;
  }

  setPanMode(enabled: boolean) {
    this.panMode = enabled;
    this.controls.enablePan = enabled;
    this.controls.enableRotate = !enabled;
    this.controls.mouseButtons.LEFT = enabled ? MOUSE.PAN : MOUSE.ROTATE;
    this.renderer.domElement.style.cursor = enabled ? 'grab' : '';
  }

  setView(view: ImageBrickView) {
    if (this.view === view) return;
    this.view = view;
    this.fitVisible();
  }

  zoom(factor: number) {
    const delta = this.camera.position.clone().sub(this.controls.target).multiplyScalar(factor);
    if (delta.length() < this.controls.minDistance || delta.length() > this.controls.maxDistance) return;
    this.camera.position.copy(this.controls.target).add(delta);
    this.desiredPosition.copy(this.camera.position);
    this.cameraMoving = false;
    this.controls.update();
    this.dirty = true;
  }

  focusStep(step: number) {
    if (!this.build) return;
    this.setAutoRotate(false);
    const ids = new Set(this.build.steps.find(item => item.id === step)?.brickIds ?? []);
    this.frameVisuals(
      this.visuals.filter(visual => ids.has(visual.brick.id)),
      1.65,
      false,
    );
  }

  private updateInstances() {
    const spread = smooth(this.actualExplosion) * unit * 5.5;
    for (const batch of this.bodyBatches) {
      batch.visuals.forEach((visual, index) => {
        if (!visual.visible) {
          this.scale.setScalar(0);
          this.position.copy(visual.base);
        } else {
          this.scale.setScalar(1);
          const arrival = (1 - smooth(visual.enter)) * unit * 7;
          this.position.copy(visual.base)
            .addScaledVector(visual.direction, spread);
          this.position.y += arrival;
        }
        this.matrix.compose(this.position, visual.rotation, this.scale);
        batch.mesh.setMatrixAt(index, this.matrix);
      });
      batch.mesh.instanceMatrix.needsUpdate = true;
    }
    for (const batch of this.studBatches) {
      batch.studs.forEach(({ visual, offsetX, offsetZ }, index) => {
        if (!visual.visible) {
          this.scale.setScalar(0);
          this.position.copy(visual.base);
        } else {
          this.scale.setScalar(1);
          const arrival = (1 - smooth(visual.enter)) * unit * 7;
          this.studOffset.set(offsetX, 0, offsetZ).applyQuaternion(visual.rotation);
          this.position.copy(visual.base)
            .addScaledVector(visual.direction, spread)
            .add(this.studOffset);
          this.position.y += (visual.brick.height ?? 1.2) * unit / 2 + unit * 0.08 + arrival;
        }
        this.matrix.compose(this.position, visual.rotation, this.scale);
        batch.mesh.setMatrixAt(index, this.matrix);
      });
      batch.mesh.instanceMatrix.needsUpdate = true;
    }
    for (const batch of this.sourceBatches) {
      batch.visuals.forEach((visual, index) => {
        this.position.copy(visual.direction).multiplyScalar(spread);
        this.position.y += (1 - smooth(visual.enter)) * unit * 7;
        batch.data.set([this.position.x, this.position.y, this.position.z, Number(visual.visible)], index * 4);
      });
      batch.texture.needsUpdate = true;
    }
    this.instanceDirty = false;
  }

  fitVisible(immediate = false) {
    if (!this.build) return;
    this.frameVisuals(
      this.visuals.filter(visual => visual.visible),
      1.62,
      immediate,
    );
  }

  private frameVisuals(visuals: VisualBrick[], padding: number, immediate = false) {
    if (!visuals.length) return;
    const spread = smooth(this.actualExplosion) * unit * 5.5;
    const box = new Box3();
    for (const visual of visuals) {
      const center = visual.base.clone().addScaledVector(visual.direction, spread);
      const rotated = (visual.brick.rotation ?? 0) % 2 === 1;
      const half = new Vector3(
        (rotated ? visual.brick.depth ?? 1 : visual.brick.width) * unit / 2,
        (visual.brick.height ?? 1.2) * unit / 2,
        (rotated ? visual.brick.width : visual.brick.depth ?? 1) * unit / 2,
      );
      box.expandByPoint(center.clone().sub(half));
      box.expandByPoint(center.clone().add(half));
    }
    const center = box.getCenter(new Vector3());
    const size = box.getSize(new Vector3());
    const direction = {
      perspective: new Vector3(0.72, 0.82, 0.9),
      front: new Vector3(0, 0.08, 1),
      side: new Vector3(1, 0.08, 0),
      top: new Vector3(0, 1, 0.001),
    }[this.view].normalize();
    const camera = new PerspectiveCamera(this.camera.fov, this.camera.aspect);
    camera.position.copy(center).add(direction);
    camera.lookAt(center);
    camera.updateMatrixWorld();
    const local = box.clone().translate(center.clone().negate())
      .applyMatrix4(new Matrix4().makeRotationFromQuaternion(camera.quaternion).invert());
    const tan = Math.tan(this.camera.fov * Math.PI / 360);
    const distance = Math.max(
      Math.max(local.max.y, -local.min.y) / tan,
      Math.max(local.max.x, -local.min.x) / tan / this.camera.aspect,
      unit * 3,
    ) * padding + Math.max(0, local.max.z);
    this.camera.near = Math.max(0.1, distance / 200);
    this.camera.far = Math.max(distance * 12, size.length() * 8);
    this.camera.updateProjectionMatrix();
    this.desiredTarget.copy(center);
    this.desiredPosition.copy(center).addScaledVector(direction, distance);
    this.controls.minDistance = Math.max(unit * 2, distance * 0.08);
    this.controls.maxDistance = Math.max(unit * 20, distance * 4);
    this.cameraMoving = !immediate;
    if (immediate) {
      this.camera.position.copy(this.desiredPosition);
      this.controls.target.copy(this.desiredTarget);
      this.controls.update();
    }
    this.dirty = true;
  }

  private resize = () => {
    if (this.disposed) return;
    const { width, height } = this.host.getBoundingClientRect();
    if (!width || !height) return;
    const gl = this.renderer.getContext();
    const viewport = gl.getParameter(gl.MAX_VIEWPORT_DIMS) as Int32Array;
    const limit = this.renderer.capabilities.maxTextureSize;
    this.renderer.setPixelRatio(Math.min(3, limit / width, limit / height, viewport[0] / width, viewport[1] / height, Math.sqrt(16_000_000 / (width * height))));
    this.renderer.setSize(width, height, false);
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.dirty = true;
  };

  private invalidate = () => {
    this.dirty = true;
  };
  private controlStart = () => {
    this.cameraMoving = false;
    if (this.panMode) this.renderer.domElement.style.cursor = 'grabbing';
  };
  private controlEnd = () => {
    this.renderer.domElement.style.cursor = this.panMode ? 'grab' : '';
  };

  private tick = (time: number) => {
    if (this.disposed) return;
    if (document.hidden || !this.host.clientWidth || !this.host.clientHeight) {
      this.lastTick = time;
      this.frame = requestAnimationFrame(this.tick);
      return;
    }
    const dt = Math.min((time - (this.lastTick || time - 16)) / 1000, 0.05);
    this.lastTick = time;
    let moving = false;
    const explosionDelta = this.explosion - this.actualExplosion;
    if (Math.abs(explosionDelta) > 0.001) {
      this.actualExplosion += explosionDelta * (1 - Math.exp(-9 * dt));
      moving = true;
    } else {
      this.actualExplosion = this.explosion;
    }
    for (const visual of this.visuals) {
        if (visual.visible && visual.enter < 1) {
          visual.enter = Math.min(1, visual.enter + dt / 0.55);
          moving = true;
        }
    }
    if (moving || this.instanceDirty) {
      this.updateInstances();
      this.dirty = true;
    }
    if (this.cameraMoving) {
      const amount = 1 - Math.exp(-8 * dt);
      this.camera.position.lerp(this.desiredPosition, amount);
      this.controls.target.lerp(this.desiredTarget, amount);
      if (this.camera.position.distanceTo(this.desiredPosition) < 0.02) this.cameraMoving = false;
      this.dirty = true;
    }
    if (this.controls.update(dt)) this.dirty = true;
    if (this.dirty) {
      const before = performance.now();
      this.renderer.render(this.scene, this.camera);
      const frameMs = performance.now() - before;
      this.lastFrameMs = frameMs;
      this.renderedFrames++;
      this.dirty = false;
    }
    this.frame = requestAnimationFrame(this.tick);
  };

  snapshot() {
    return {
      bricks: this.build?.bricks.length ?? 0,
      steps: this.build?.steps.length ?? 0,
      visible: this.visuals.filter(visual => visual.visible).length,
      drawnInstances: this.bodyBatches.reduce((sum, batch) => sum + batch.visuals.filter((_, i) => batch.mesh.instanceMatrix.array[i * 16] !== 0 || batch.mesh.instanceMatrix.array[i * 16 + 1] !== 0 || batch.mesh.instanceMatrix.array[i * 16 + 2] !== 0).length, 0) + this.sourceBatches.reduce((sum, batch) => sum + batch.visuals.filter((_, i) => batch.data[i * 4 + 3] === 1).length, 0),
      buildRevision: this.buildRevision,
      renderedFrames: this.renderedFrames,
      sourceModels: this.sourceBatches.length,
      step: this.currentStep,
      explosion: this.actualExplosion,
      method: this.build?.method ?? 'relief',
      reconstruction: this.build?.reconstruction ?? 'empty',
      viewCount: this.build?.viewCount ?? 0,
      brickBudget: this.build?.brickBudget ?? 0,
      dimensions: this.build
        ? [this.build.width, this.build.height, this.build.maxDepth]
        : [0, 0, 0],
      pixelRatio: this.renderer.getPixelRatio(),
      bodyBatches: this.bodyBatches.length,
      studBatches: this.studBatches.length,
      drawCalls: this.renderer.info.render.calls,
      triangles: this.renderer.info.render.triangles,
      frameMs: this.lastFrameMs,
      camera: this.camera.position.toArray(),
      target: this.controls.target.toArray(),
      cameraMoving: this.cameraMoving,
      panMode: this.panMode,
      view: this.view,
    };
  }

  private clearModel() {
    for (const child of [...this.model.children]) {
      if (child instanceof InstancedMesh) child.dispose();
      this.model.remove(child);
    }
    const ground = this.scene.getObjectByName('image-brick-ground');
    if (ground) this.scene.remove(ground);
    this.bodyBatches.length = 0;
    this.studBatches.length = 0;
    this.visuals = [];
    this.sourceBatches.forEach(batch => batch.texture.dispose());
    this.sourceBatches.length = 0;
    this.disposableGeometries.forEach(geometry => geometry.dispose());
    this.disposableMaterials.forEach(material => material.dispose());
    this.disposableGeometries.clear();
    this.disposableMaterials.clear();
  }

  dispose() {
    this.disposed = true;
    cancelAnimationFrame(this.frame);
    this.observer.disconnect();
    this.controls.removeEventListener('change', this.invalidate);
    this.controls.removeEventListener('start', this.controlStart);
    this.controls.removeEventListener('end', this.controlEnd);
    this.controls.dispose();
    this.clearModel();
    this.renderer.dispose();
    this.renderer.forceContextLoss();
    this.renderer.domElement.remove();
  }
}
