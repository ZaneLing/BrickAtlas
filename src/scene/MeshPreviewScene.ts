import {
  ACESFilmicToneMapping,
  Box3,
  Color,
  DirectionalLight,
  Group,
  HemisphereLight,
  Mesh,
  MeshStandardMaterial,
  PerspectiveCamera,
  Scene,
  SRGBColorSpace,
  Vector3,
  WebGLRenderer,
} from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

export class MeshPreviewScene {
  private readonly scene = new Scene();
  private readonly camera = new PerspectiveCamera(38, 1, 0.1, 1000);
  private readonly renderer = new WebGLRenderer({
    antialias: true,
    alpha: true,
    powerPreference: 'high-performance',
  });
  private readonly controls: OrbitControls;
  private readonly model = new Group();
  private readonly observer: ResizeObserver;
  private frame = 0;
  private disposed = false;
  private triangleCount = 0;

  constructor(private readonly host: HTMLElement, label: string) {
    this.renderer.setClearColor(new Color('#eef2f6'), 1);
    this.renderer.outputColorSpace = SRGBColorSpace;
    this.renderer.toneMapping = ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.05;
    this.renderer.domElement.setAttribute('role', 'img');
    this.renderer.domElement.setAttribute('aria-label', label);
    this.renderer.domElement.tabIndex = 0;
    this.host.appendChild(this.renderer.domElement);
    this.camera.position.set(7, 5, 9);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.1;
    this.controls.autoRotate = true;
    this.controls.autoRotateSpeed = 1.2;
    this.controls.minDistance = 3;
    this.controls.maxDistance = 40;
    const hemisphere = new HemisphereLight(0xffffff, 0x718095, 2.8);
    const key = new DirectionalLight(0xffffff, 3.1);
    key.position.set(-8, 12, 10);
    const fill = new DirectionalLight(0xffe6ca, 1.2);
    fill.position.set(9, 4, -8);
    this.scene.add(hemisphere, key, fill, this.model);
    this.observer = new ResizeObserver(this.resize);
    this.observer.observe(host);
    this.resize();
    this.frame = requestAnimationFrame(this.tick);
  }

  setLabel(label: string) {
    this.renderer.domElement.setAttribute('aria-label', label);
  }

  async setGlb(blob: Blob) {
    const gltf = await new GLTFLoader().parseAsync(await blob.arrayBuffer(), '');
    if (this.disposed) return;
    this.clearModel();
    this.model.add(gltf.scene);
    gltf.scene.updateMatrixWorld(true);
    const bounds = new Box3().setFromObject(gltf.scene);
    const size = bounds.getSize(new Vector3());
    const center = bounds.getCenter(new Vector3());
    const scale = 10 / Math.max(size.x, size.y, size.z, 1e-6);
    gltf.scene.scale.setScalar(scale);
    gltf.scene.position.copy(center).multiplyScalar(-scale);
    gltf.scene.updateMatrixWorld(true);
    this.triangleCount = 0;
    gltf.scene.traverse(object => {
      if (!(object instanceof Mesh)) return;
      const position = object.geometry.getAttribute('position');
      this.triangleCount += object.geometry.index
        ? Math.floor(object.geometry.index.count / 3)
        : Math.floor((position?.count ?? 0) / 3);
      if (!object.material) {
        object.material = new MeshStandardMaterial({
          color: '#b9c5d3',
          roughness: 0.58,
        });
      }
    });
    this.controls.target.set(0, 0, 0);
    const normalized = size.multiplyScalar(scale);
    const tangent = Math.tan(this.camera.fov * Math.PI / 360);
    const distance = Math.max(
      normalized.y / (2 * tangent),
      normalized.x / (2 * tangent * Math.max(0.25, this.camera.aspect)),
      normalized.z,
    ) * 1.45;
    this.camera.position
      .copy(new Vector3(0.78, 0.5, 1).normalize())
      .multiplyScalar(distance);
    this.controls.update();
  }

  private clearModel() {
    this.model.traverse(object => {
      if (!(object instanceof Mesh)) return;
      object.geometry.dispose();
      const materials = Array.isArray(object.material)
        ? object.material
        : [object.material];
      materials.forEach(material => {
        for (const value of Object.values(material)) {
          if (value && typeof value === 'object' && 'isTexture' in value) {
            (value as unknown as { dispose: () => void }).dispose();
          }
        }
        material.dispose();
      });
    });
    this.model.clear();
  }

  private resize = () => {
    const { width, height } = this.host.getBoundingClientRect();
    if (!width || !height || this.disposed) return;
    const limit = Math.sqrt(10_000_000 / (width * height));
    this.renderer.setPixelRatio(Math.min(2.25, devicePixelRatio, limit));
    this.renderer.setSize(width, height, false);
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
  };

  private tick = () => {
    if (this.disposed) return;
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
    this.frame = requestAnimationFrame(this.tick);
  };

  snapshot() {
    return {
      triangleCount: this.triangleCount,
      children: this.model.children.length,
      pixelRatio: this.renderer.getPixelRatio(),
    };
  }

  dispose() {
    this.disposed = true;
    cancelAnimationFrame(this.frame);
    this.observer.disconnect();
    this.controls.dispose();
    this.clearModel();
    this.renderer.dispose();
    this.renderer.forceContextLoss();
    this.renderer.domElement.remove();
  }
}
