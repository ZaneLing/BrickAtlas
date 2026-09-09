import {
  ACESFilmicToneMapping, AmbientLight, Color, CylinderGeometry, DirectionalLight,
  DynamicDrawUsage, Group, HemisphereLight, InstancedMesh, Matrix4, Mesh, MeshPhysicalMaterial,
  PerspectiveCamera, PlaneGeometry, Scene, ShadowMaterial, SRGBColorSpace, Vector3, WebGLRenderer,
  type BufferGeometry, type Material,
} from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import type { ImageBrick, ImageBrickBuild } from '../creator/imageBrickModel';

type VisualBrick = {
  brick: ImageBrick;
  base: Vector3;
  direction: Vector3;
  enter: number;
  visible: boolean;
};

type BodyBatch = {
  mesh: InstancedMesh;
  visuals: VisualBrick[];
};

type StudBatch = {
  mesh: InstancedMesh;
  studs: { visual: VisualBrick; offset: number }[];
};

const unit = 12;
const brickHeight = unit * 1.16;
const smooth = (value: number) => value * value * (3 - 2 * value);

export class ImageBrickScene {
  private readonly scene = new Scene();
  private readonly model = new Group();
  private readonly camera = new PerspectiveCamera(34, 1, 0.1, 5000);
  private readonly renderer = new WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
  private readonly controls: OrbitControls;
  private readonly observer: ResizeObserver;
  private readonly bodyBatches: BodyBatch[] = [];
  private readonly studBatches: StudBatch[] = [];
  private readonly disposableGeometries = new Set<BufferGeometry>();
  private readonly disposableMaterials = new Set<Material>();
  private readonly matrix = new Matrix4();
  private readonly position = new Vector3();
  private readonly scale = new Vector3(1, 1, 1);
  private readonly rotation = new Group().quaternion;
  private frame = 0;
  private lastTick = 0;
  private disposed = false;
  private dirty = true;
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
    this.observer = new ResizeObserver(this.resize);
    this.observer.observe(host);
    this.resize();
    this.frame = requestAnimationFrame(this.tick);
  }

  setLabel(label: string) {
    this.renderer.domElement.setAttribute('aria-label', label);
  }

  setBuild(build: ImageBrickBuild) {
    this.clearModel();
    this.build = build;
    this.currentStep = build.steps.length;
    const visuals = build.bricks.map(brick => {
      const base = new Vector3(brick.x * unit, brick.y * unit, brick.z * unit);
      const direction = new Vector3(brick.x, 0.45 + brick.y * 0.22, brick.z);
      if (direction.lengthSq() < 0.01) direction.set(0, 1, 0);
      return { brick, base, direction: direction.normalize(), enter: 1, visible: true };
    });
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
      const key = `${visual.brick.width}:${visual.brick.colorHex}`;
      if (!bodies.has(key)) bodies.set(key, []);
      bodies.get(key)!.push(visual);
    }
    for (const [key, batchVisuals] of bodies) {
      const width = Number(key.split(':')[0]);
      const geometry = new RoundedBoxGeometry(width * unit - 0.7, brickHeight - 0.55, unit - 0.7, 2, 0.65);
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
    const studs = new Map<string, { visual: VisualBrick; offset: number }[]>();
    for (const visual of visuals) {
      if (!studs.has(visual.brick.colorHex)) studs.set(visual.brick.colorHex, []);
      for (let index = 0; index < visual.brick.width; index++) {
        studs.get(visual.brick.colorHex)!.push({
          visual,
          offset: (index - (visual.brick.width - 1) / 2) * unit,
        });
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
    const groundSize = Math.max(build.width, build.height) * unit * 2.3;
    const ground = new Mesh(new PlaneGeometry(groundSize, groundSize), new ShadowMaterial({ color: 0x283247, opacity: 0.13 }));
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -0.2;
    ground.receiveShadow = true;
    ground.name = 'image-brick-ground';
    this.scene.add(ground);
    this.disposableGeometries.add(ground.geometry);
    this.disposableMaterials.add(ground.material as Material);
    this.fit();
    this.updateInstances();
  }

  setBuildStep(step: number, animate = true) {
    if (!this.build) return;
    const next = Math.max(0, Math.min(this.build.steps.length, Math.round(step)));
    for (const batch of this.bodyBatches) {
      for (const visual of batch.visuals) {
        const wasVisible = visual.visible;
        visual.visible = visual.brick.step <= next;
        if (animate && visual.visible && !wasVisible) visual.enter = 0;
        if (!visual.visible) visual.enter = 1;
      }
    }
    this.currentStep = next;
    this.dirty = true;
  }

  setExplosion(value: number) {
    this.explosion = Math.max(0, Math.min(1, value));
    this.dirty = true;
  }

  setAutoRotate(enabled: boolean) {
    this.controls.autoRotate = enabled;
    this.dirty = true;
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
            .addScaledVector(visual.direction, spread)
            .add(new Vector3(0, arrival, 0));
        }
        this.matrix.compose(this.position, this.rotation, this.scale);
        batch.mesh.setMatrixAt(index, this.matrix);
      });
      batch.mesh.instanceMatrix.needsUpdate = true;
    }
    for (const batch of this.studBatches) {
      batch.studs.forEach(({ visual, offset }, index) => {
        if (!visual.visible) {
          this.scale.setScalar(0);
          this.position.copy(visual.base);
        } else {
          this.scale.setScalar(1);
          const arrival = (1 - smooth(visual.enter)) * unit * 7;
          this.position.copy(visual.base)
            .addScaledVector(visual.direction, spread)
            .add(new Vector3(offset, brickHeight / 2 + unit * 0.08 + arrival, 0));
        }
        this.matrix.compose(this.position, this.rotation, this.scale);
        batch.mesh.setMatrixAt(index, this.matrix);
      });
      batch.mesh.instanceMatrix.needsUpdate = true;
    }
  }

  private fit() {
    if (!this.build) return;
    const span = Math.max(this.build.width, this.build.height) * unit;
    this.camera.position.set(span * 0.72, span * 0.82, span * 0.9);
    this.camera.near = Math.max(0.1, span / 200);
    this.camera.far = span * 12;
    this.controls.target.set(0, this.build.maxDepth * brickHeight * 0.35, 0);
    this.camera.lookAt(this.controls.target);
    this.camera.updateProjectionMatrix();
    this.controls.minDistance = span * 0.45;
    this.controls.maxDistance = span * 3.2;
    this.controls.update();
    this.dirty = true;
  }

  private resize = () => {
    if (this.disposed) return;
    const { width, height } = this.host.getBoundingClientRect();
    if (!width || !height) return;
    this.renderer.setSize(width, height, false);
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.dirty = true;
  };

  private invalidate = () => {
    this.dirty = true;
  };

  private tick = (time: number) => {
    if (this.disposed) return;
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
    for (const batch of this.bodyBatches) {
      for (const visual of batch.visuals) {
        if (visual.visible && visual.enter < 1) {
          visual.enter = Math.min(1, visual.enter + dt / 0.55);
          moving = true;
        }
      }
    }
    if (moving) {
      this.updateInstances();
      this.dirty = true;
    }
    if (this.controls.update(dt)) this.dirty = true;
    if (this.dirty) {
      this.renderer.render(this.scene, this.camera);
      this.dirty = false;
    }
    this.frame = requestAnimationFrame(this.tick);
  };

  snapshot() {
    return {
      bricks: this.build?.bricks.length ?? 0,
      visible: this.bodyBatches.flatMap(batch => batch.visuals).filter(visual => visual.visible).length,
      step: this.currentStep,
      explosion: this.actualExplosion,
      pixelRatio: this.renderer.getPixelRatio(),
    };
  }

  private clearModel() {
    for (const child of [...this.model.children]) this.model.remove(child);
    const ground = this.scene.getObjectByName('image-brick-ground');
    if (ground) this.scene.remove(ground);
    this.bodyBatches.length = 0;
    this.studBatches.length = 0;
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
    this.controls.dispose();
    this.clearModel();
    this.renderer.dispose();
    this.renderer.forceContextLoss();
    this.renderer.domElement.remove();
  }
}
