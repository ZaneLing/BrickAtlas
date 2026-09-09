import {
  AmbientLight, BufferAttribute, BufferGeometry, Color, DirectionalLight, EdgesGeometry,
  LineBasicMaterial, LineSegments, Mesh, MeshStandardMaterial, PerspectiveCamera, Scene,
  Sphere, SRGBColorSpace, Vector3, WebGLRenderer,
} from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

export interface PartPreviewData {
  positions: Float32Array;
  color: string;
}

export class PartPreviewScene {
  private readonly scene = new Scene();
  private readonly camera = new PerspectiveCamera(32, 1, 0.1, 5000);
  private readonly renderer = new WebGLRenderer({ antialias: true, alpha: false });
  private readonly controls: OrbitControls;
  private readonly observer: ResizeObserver;
  private frame = 0;
  private disposed = false;

  constructor(private host: HTMLElement, data: PartPreviewData) {
    this.renderer.setClearColor('#f4f7f5');
    this.renderer.outputColorSpace = SRGBColorSpace;
    this.renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    this.renderer.domElement.setAttribute('aria-label', '选中积木可旋转三维预览');
    this.renderer.domElement.setAttribute('role', 'img');
    host.appendChild(this.renderer.domElement);

    const geometry = new BufferGeometry();
    geometry.setAttribute('position', new BufferAttribute(data.positions, 3));
    geometry.computeVertexNormals();
    geometry.computeBoundingBox();
    geometry.computeBoundingSphere();
    const center = geometry.boundingBox?.getCenter(new Vector3()) ?? new Vector3();
    geometry.translate(-center.x, -center.y, -center.z);
    geometry.computeBoundingBox();
    geometry.computeBoundingSphere();

    const mesh = new Mesh(geometry, new MeshStandardMaterial({
      color: new Color(data.color), roughness: 0.34, metalness: 0.02,
    }));
    const edges = new LineSegments(new EdgesGeometry(geometry, 22), new LineBasicMaterial({
      color: 0x526159, transparent: true, opacity: 0.65,
    }));
    this.scene.add(mesh, edges);
    const key = new DirectionalLight(0xffffff, 3.2);
    key.position.set(-2, 4, 3);
    const fill = new DirectionalLight(0xdde9ff, 1.4);
    fill.position.set(3, 1, -2);
    this.scene.add(key, fill, new AmbientLight(0xffffff, 1.3));

    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.09;
    this.controls.enablePan = false;
    this.controls.addEventListener('change', this.render);
    this.fit(geometry.boundingSphere ?? new Sphere(new Vector3(), 20));

    this.observer = new ResizeObserver(this.resize);
    this.observer.observe(host);
    this.resize();
    this.frame = requestAnimationFrame(this.tick);
  }

  private fit(sphere: Sphere) {
    const radius = Math.max(sphere.radius, 4);
    const distance = radius / Math.sin(this.camera.fov * Math.PI / 360) * 1.22;
    this.camera.near = Math.max(0.01, distance / 100);
    this.camera.far = distance * 20;
    this.camera.position.set(distance * 0.72, distance * 0.58, distance);
    this.camera.lookAt(0, 0, 0);
    this.camera.updateProjectionMatrix();
    this.controls.minDistance = radius * 1.25;
    this.controls.maxDistance = distance * 4;
    this.controls.update();
  }

  private resize = () => {
    const { width, height } = this.host.getBoundingClientRect();
    if (!width || !height || this.disposed) return;
    this.renderer.setSize(width, height, false);
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.render();
  };

  private render = () => {
    if (!this.disposed) this.renderer.render(this.scene, this.camera);
  };

  private tick = () => {
    if (this.disposed) return;
    if (this.controls.update()) this.render();
    this.frame = requestAnimationFrame(this.tick);
  };

  dispose() {
    this.disposed = true;
    cancelAnimationFrame(this.frame);
    this.observer.disconnect();
    this.controls.dispose();
    this.scene.traverse(object => {
      const mesh = object as Mesh;
      mesh.geometry?.dispose();
      if (mesh.material) (Array.isArray(mesh.material) ? mesh.material : [mesh.material]).forEach(material => material.dispose());
    });
    this.renderer.dispose();
    this.renderer.domElement.remove();
  }
}
