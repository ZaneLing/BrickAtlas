import {
  ACESFilmicToneMapping, Box3, Box3Helper, BufferGeometry, Color, CylinderGeometry, DirectionalLight,
  DynamicDrawUsage, Group, HemisphereLight, InstancedMesh, Matrix4, Mesh, MeshPhysicalMaterial,
  MeshStandardMaterial, LineBasicMaterial, MOUSE, PerspectiveCamera, Plane, PlaneGeometry, Raycaster, Scene,
  ShaderMaterial, SRGBColorSpace, Vector2, Vector3, WebGLRenderer,
} from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { brickPalette } from '../creator/imageBrickModel';
import {
  canRemove, DiyIndex, footprint, partById, PLATE_HEIGHT, stamp, stampSize,
  type DiyBrick, type DiyBrush, type DiyTool, type PlacementIssue,
} from './diyModel';
import { createDiyGeometry } from './diyGeometry';

export interface DiyHover {
  x: number;
  y: number;
  z: number;
  issue: PlacementIssue;
  hitId: string | null;
}
interface Callbacks {
  hover: (hover: DiyHover | null) => void;
  place: (parts: DiyBrick[]) => void;
  edit: (id: string, tool: 'erase' | 'paint') => void;
  select: (id: string | null) => void;
  error: (message: string) => void;
}
interface Batch { mesh: InstancedMesh; bricks: DiyBrick[]; capacity: number }
interface Pick { brick: DiyBrick; box: Box3; matrix: Matrix4 }

export class DiyScene {
  private readonly scene = new Scene();
  private readonly camera = new PerspectiveCamera(38, 1, 0.1, 10000);
  private readonly renderer = new WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
  private readonly controls: OrbitControls;
  private readonly observer: ResizeObserver;
  private readonly model = new Group();
  private readonly ghost = new Group();
  private readonly ghostMaterial = new MeshPhysicalMaterial({ color: '#3478d4', transparent: true, opacity: 0.48, depthWrite: false, roughness: 0.32 });
  private readonly material = new MeshPhysicalMaterial({ color: '#ffffff', roughness: 0.3, clearcoat: 0.25, clearcoatRoughness: 0.3 });
  private readonly geometries = new Map<string, BufferGeometry>();
  private readonly batches = new Map<string, Batch>();
  private readonly raycaster = new Raycaster();
  private readonly picker = new Mesh();
  private picks: Pick[] = [];
  private readonly pointer = new Vector2();
  private readonly groundPlane = new Plane(new Vector3(0, 1, 0), 0);
  private readonly point = new Vector3();
  private readonly matrix = new Matrix4();
  private readonly transform = new Group();
  private readonly floor: Mesh<PlaneGeometry, ShaderMaterial>;
  private readonly studs: InstancedMesh;
  private readonly focusLight: DirectionalLight;
  private readonly outline = new Box3Helper(new Box3(), new Color('#276bdb'));
  private readonly ghostOutline = new Box3Helper(new Box3(), new Color('#276bdb'));
  private index = new DiyIndex([]);
  private bricks: DiyBrick[] = [];
  private brush: DiyBrush = { recipeId: '3001', color: 'red', turn: 0 };
  private tool: DiyTool = 'place';
  private manualLayer: number | null = null;
  private selectedId: string | null = null;
  private hover: DiyHover | null = null;
  private inside = false;
  private pointerDirty = false;
  private down: { x: number; y: number; button: number } | null = null;
  private dragged = false;
  private dirty = true;
  private disposed = false;
  private frame = 0;
  private renderedFrames = 0;
  private frameMs = 0;
  private groundKey = '';

  constructor(private host: HTMLElement, private callbacks: Callbacks, label: string) {
    this.renderer.setClearColor('#f2f5f8');
    this.renderer.outputColorSpace = SRGBColorSpace;
    this.renderer.toneMapping = ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.12;
    this.renderer.domElement.setAttribute('role', 'img');
    this.renderer.domElement.setAttribute('aria-label', label);
    this.renderer.domElement.tabIndex = 0;
    host.appendChild(this.renderer.domElement);
    this.camera.position.set(22, 26, 31);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.target.set(0, 0, 0);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.12;
    this.controls.screenSpacePanning = false;
    this.controls.minDistance = 4;
    this.controls.maxDistance = 200;
    this.controls.maxPolarAngle = Math.PI * 0.47;
    this.controls.mouseButtons = { LEFT: MOUSE.ROTATE, MIDDLE: MOUSE.DOLLY, RIGHT: MOUSE.PAN };
    this.controls.addEventListener('change', this.invalidate);
    const hemi = new HemisphereLight(0xffffff, 0x8192a1, 2.6);
    this.focusLight = new DirectionalLight(0xffffff, 3);
    this.focusLight.position.set(-15, 35, 20);
    const fill = new DirectionalLight(0xffefd7, 0.65);
    fill.position.set(20, 5, -20);
    this.scene.add(hemi, this.focusLight, fill, this.model, this.ghost, this.outline, this.ghostOutline);
    this.ghost.visible = this.outline.visible = this.ghostOutline.visible = false;

    this.floor = new Mesh(new PlaneGeometry(20000, 20000), new ShaderMaterial({
      uniforms: { base: { value: new Color('#dfe6ed') }, line: { value: new Color('#b9c7d3') } },
      vertexShader: `
        varying vec2 world;
        void main() {
          vec4 p = modelMatrix * vec4(position, 1.);
          world = p.xz;
          gl_Position = projectionMatrix * viewMatrix * p;
        }`,
      fragmentShader: `
        varying vec2 world;
        uniform vec3 base;
        uniform vec3 line;
        void main() {
          vec2 grid = abs(fract(world / 8. - .5) - .5) / max(fwidth(world / 8.), vec2(.001));
          float major = 1. - min(min(grid.x, grid.y), 1.);
          float dotDistance = length(fract(world) - .5);
          float edge = max(fwidth(dotDistance), .008);
          float dot = 1. - smoothstep(.22 - edge, .22 + edge, dotDistance);
          gl_FragColor = vec4(mix(base, line, major * .38 + dot * .10), 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }`,
    }));
    this.floor.rotation.x = -Math.PI / 2;
    this.floor.position.y = -0.03;
    const studMaterial = new MeshStandardMaterial({ color: '#d4dee7', roughness: 0.5 });
    this.studs = new InstancedMesh(new CylinderGeometry(0.3, 0.3, 0.12, 12), studMaterial, 80 * 80);
    this.studs.instanceMatrix.setUsage(DynamicDrawUsage);
    this.studs.frustumCulled = false;
    this.scene.add(this.floor, this.studs);

    const canvas = this.renderer.domElement;
    canvas.addEventListener('pointermove', this.pointerMove);
    canvas.addEventListener('pointerdown', this.pointerDown);
    canvas.addEventListener('pointerleave', this.pointerLeave);
    window.addEventListener('pointerup', this.pointerUp);
    window.addEventListener('pointercancel', this.pointerCancel);
    canvas.addEventListener('webglcontextlost', this.contextLost);
    this.observer = new ResizeObserver(this.resize);
    this.observer.observe(host);
    this.rebuildGhost();
    this.resize();
    this.controls.update();
    this.frame = requestAnimationFrame(this.tick);
  }

  setLabel(label: string) { this.renderer.domElement.setAttribute('aria-label', label); }
  private geometry(id: string) {
    let geometry = this.geometries.get(id);
    if (!geometry) { geometry = createDiyGeometry(partById.get(id)!); this.geometries.set(id, geometry); }
    return geometry;
  }
  setBricks(bricks: DiyBrick[]) {
    this.bricks = bricks;
    this.index = new DiyIndex(bricks);
    const groups = new Map<string, DiyBrick[]>();
    bricks.forEach(brick => { const group = groups.get(brick.partId) ?? []; group.push(brick); groups.set(brick.partId, group); });
    for (const [id, batch] of this.batches) {
      if (!groups.has(id)) { this.model.remove(batch.mesh); batch.mesh.dispose(); this.batches.delete(id); }
    }
    for (const [id, parts] of groups) {
      let batch = this.batches.get(id);
      if (!batch || batch.capacity < parts.length) {
        if (batch) { this.model.remove(batch.mesh); batch.mesh.dispose(); }
        const capacity = Math.max(16, 2 ** Math.ceil(Math.log2(parts.length)));
        const mesh = new InstancedMesh(this.geometry(id), this.material, capacity);
        mesh.instanceMatrix.setUsage(DynamicDrawUsage);
        mesh.frustumCulled = false;
        batch = { mesh, bricks: parts, capacity };
        this.batches.set(id, batch);
        this.model.add(mesh);
      }
      batch.bricks = parts;
      batch.mesh.count = parts.length;
      parts.forEach((brick, i) => {
        this.brickTransform(brick);
        batch!.mesh.setMatrixAt(i, this.transform.matrix);
        batch!.mesh.setColorAt(i, new Color(brickPalette.find(color => color.id === brick.color)!.hex));
      });
      batch.mesh.instanceMatrix.needsUpdate = true;
      if (batch.mesh.instanceColor) batch.mesh.instanceColor.needsUpdate = true;
      batch.mesh.computeBoundingSphere();
    }
    this.model.updateMatrixWorld(true);
    this.picks = bricks.map(brick => {
      this.brickTransform(brick);
      return { brick, box: this.brickBox(brick), matrix: this.transform.matrix.clone() };
    });
    this.updateSelection();
    this.dirty = this.pointerDirty = true;
  }
  private brickTransform(brick: DiyBrick) {
    const size = footprint(brick);
    this.transform.position.set(brick.x + size.width / 2, brick.y * PLATE_HEIGHT, brick.z + size.depth / 2);
    this.transform.rotation.set(0, brick.turn * Math.PI / 2, 0);
    this.transform.updateMatrix();
  }
  setBrush(brush: DiyBrush) {
    this.brush = brush;
    this.rebuildGhost();
    this.dirty = this.pointerDirty = true;
  }
  setTool(tool: DiyTool) {
    this.tool = tool;
    this.controls.mouseButtons.LEFT = tool === 'pan' ? MOUSE.PAN : MOUSE.ROTATE;
    this.renderer.domElement.style.cursor = tool === 'pan' ? 'grab' : tool === 'orbit' ? 'grab' : 'crosshair';
    this.dirty = this.pointerDirty = true;
  }
  setLayer(layer: number | null) { this.manualLayer = layer; this.pointerDirty = true; }
  select(id: string | null) { this.selectedId = id; this.updateSelection(); this.dirty = true; }

  private brickBox(brick: DiyBrick) {
    const size = footprint(brick);
    return new Box3(
      new Vector3(brick.x - 0.03, brick.y * PLATE_HEIGHT, brick.z - 0.03),
      new Vector3(brick.x + size.width + 0.03, (brick.y + partById.get(brick.partId)!.height) * PLATE_HEIGHT + 0.19, brick.z + size.depth + 0.03),
    );
  }
  private updateSelection() {
    const brick = this.bricks.find(item => item.id === this.selectedId);
    this.outline.visible = !!brick;
    if (brick) this.outline.box.copy(this.brickBox(brick));
  }
  private rebuildGhost() {
    this.ghost.clear();
    for (const brick of stamp(this.brush, 0, 0, 0)) {
      const mesh = new Mesh(this.geometry(brick.partId), this.ghostMaterial);
      this.brickTransform(brick);
      mesh.position.copy(this.transform.position);
      mesh.quaternion.copy(this.transform.quaternion);
      mesh.renderOrder = 2;
      this.ghost.add(mesh);
    }
  }
  private pointerMove = (event: PointerEvent) => {
    const bounds = this.renderer.domElement.getBoundingClientRect();
    this.pointer.set((event.clientX - bounds.left) / bounds.width * 2 - 1, -(event.clientY - bounds.top) / bounds.height * 2 + 1);
    this.inside = true;
    if (this.down && Math.hypot(event.clientX - this.down.x, event.clientY - this.down.y) > 5) this.dragged = true;
    this.pointerDirty = true;
  };
  private pointerLeave = () => {
    this.inside = false;
    this.ghost.visible = this.ghostOutline.visible = false;
    this.publishHover(null);
    this.dirty = true;
  };
  private pointerDown = (event: PointerEvent) => {
    this.down = { x: event.clientX, y: event.clientY, button: event.button };
    this.dragged = false;
    this.pointerMove(event);
  };
  private pointerCancel = () => { this.down = null; this.dragged = false; this.pointerDirty = true; };
  private pointerUp = (event: PointerEvent) => {
    if (!this.down) return;
    const clicked = this.down.button === 0 && !this.dragged && this.inside
      && Math.hypot(event.clientX - this.down.x, event.clientY - this.down.y) <= 5;
    this.down = null;
    this.dragged = false;
    this.pointerDirty = true;
    if (!clicked) return;
    this.updateHover();
    if (!this.hover) return;
    if (this.tool === 'place') {
      if (this.hover.issue) return;
      const id = crypto.randomUUID();
      this.callbacks.place(stamp(this.brush, this.hover.x, this.hover.y, this.hover.z, id));
    } else if ((this.tool === 'erase' || this.tool === 'paint') && this.hover.hitId) {
      this.callbacks.edit(this.hover.hitId, this.tool);
    } else this.callbacks.select(this.hover.hitId);
  };
  private publishHover(hover: DiyHover | null) {
    if (JSON.stringify(hover) !== JSON.stringify(this.hover)) { this.hover = hover; this.callbacks.hover(hover); }
  }
  private updateHover() {
    this.pointerDirty = false;
    if (!this.inside || this.dragged) {
      this.ghost.visible = this.ghostOutline.visible = false;
      this.dirty = true;
      return;
    }
    this.camera.updateMatrixWorld();
    this.raycaster.setFromCamera(this.pointer, this.camera);
    // Broad-phase boxes keep triangle raycasts limited to nearby candidates.
    const broadPoint = new Vector3();
    const candidates = this.picks.flatMap(pick => this.raycaster.ray.intersectBox(pick.box, broadPoint)
      ? [{ pick, distance: this.raycaster.ray.origin.distanceToSquared(broadPoint) }] : [])
      .sort((a, b) => a.distance - b.distance);
    let hit: ReturnType<Raycaster['intersectObject']>[number] | undefined;
    let hitBrick: DiyBrick | undefined;
    for (const candidate of candidates) {
      if (hit && candidate.distance > hit.distance * hit.distance) break;
      this.picker.geometry = this.geometry(candidate.pick.brick.partId);
      this.picker.matrixWorld.copy(candidate.pick.matrix);
      const result = this.raycaster.intersectObject(this.picker, false)[0];
      if (result && (!hit || result.distance < hit.distance)) { hit = result; hitBrick = candidate.pick.brick; }
    }
    let y = this.manualLayer ?? 0;
    if (this.manualLayer === null && hitBrick && hit?.face && hit.face.normal.y > 0.2) {
      this.point.copy(hit.point);
      y = hitBrick.y + partById.get(hitBrick.partId)!.height;
    } else {
      this.groundPlane.constant = -y * PLATE_HEIGHT;
      if (!this.raycaster.ray.intersectPlane(this.groundPlane, this.point)) {
        this.ghost.visible = this.ghostOutline.visible = false;
        this.publishHover(null);
        this.dirty = true;
        return;
      }
    }
    const size = stampSize(this.brush);
    const x = Math.floor(this.point.x - (size.width - 1) / 2);
    const z = Math.floor(this.point.z - (size.depth - 1) / 2);
    const parts = stamp(this.brush, x, y, z);
    const issue = this.index.validate(parts, this.bricks.length);
    this.ghost.visible = this.ghostOutline.visible = this.tool === 'place';
    this.ghost.position.set(x, y * PLATE_HEIGHT, z);
    this.ghostMaterial.color.set(issue ? '#d83b34' : brickPalette.find(color => color.id === this.brush.color)!.hex);
    (this.ghostOutline.material as LineBasicMaterial).color.set(issue ? '#d83b34' : '#276bdb');
    this.ghostOutline.box.set(new Vector3(x, y * PLATE_HEIGHT + 0.01, z), new Vector3(x + size.width, y * PLATE_HEIGHT + 0.04, z + size.depth));
    if ((this.tool === 'erase' || this.tool === 'paint') && hitBrick) {
      this.outline.visible = true;
      this.outline.box.copy(this.brickBox(hitBrick));
      (this.outline.material as LineBasicMaterial).color.set(this.tool === 'erase' ? '#d83b34' : '#276bdb');
    } else { (this.outline.material as LineBasicMaterial).color.set('#276bdb'); this.updateSelection(); }
    this.publishHover({ x, y, z, issue, hitId: hitBrick?.id ?? null });
    this.dirty = true;
  }

  zoom(factor: number) {
    const delta = this.camera.position.clone().sub(this.controls.target);
    delta.setLength(Math.max(4, Math.min(200, delta.length() * factor)));
    this.camera.position.copy(this.controls.target).add(delta);
    this.controls.update();
    this.invalidate();
  }
  pan(dx: number, dz: number) {
    const shift = new Vector3(dx, 0, dz);
    this.camera.position.add(shift); this.controls.target.add(shift); this.controls.update(); this.invalidate();
  }
  setView(top: boolean) {
    const distance = this.camera.position.distanceTo(this.controls.target);
    this.camera.position.copy(this.controls.target).addScaledVector(new Vector3(top ? 0 : 0.65, 1, top ? 0.001 : 0.9).normalize(), distance);
    this.controls.update();
    this.invalidate();
  }
  fit(selection = false) {
    const items = selection ? this.bricks.filter(brick => brick.id === this.selectedId) : this.bricks;
    const box = new Box3();
    items.forEach(brick => box.union(this.brickBox(brick)));
    const target = items.length ? box.getCenter(new Vector3()) : new Vector3();
    const size = items.length ? box.getSize(new Vector3()) : new Vector3(16, 0, 16);
    const distance = Math.max(8, Math.min(200, size.length() * 1.5 / Math.min(1, this.camera.aspect)));
    this.controls.target.copy(target);
    this.camera.position.copy(target).addScaledVector(new Vector3(0.65, 1, 0.9).normalize(), distance);
    this.controls.update();
    this.invalidate();
  }
  async capture() {
    const ghost = this.ghost.visible, outline = this.ghostOutline.visible;
    this.ghost.visible = this.ghostOutline.visible = false;
    this.renderer.render(this.scene, this.camera);
    const blob = await new Promise<Blob>((resolve, reject) => this.renderer.domElement.toBlob(blob => blob ? resolve(blob) : reject(new Error('PNG capture failed')), 'image/png'));
    this.ghost.visible = ghost; this.ghostOutline.visible = outline; this.dirty = true;
    return blob;
  }
  private updateGround() {
    const x = Math.floor(this.controls.target.x / 8) * 8, z = Math.floor(this.controls.target.z / 8) * 8;
    const key = `${x}:${z}`;
    if (key === this.groundKey) return;
    this.groundKey = key;
    this.floor.position.set(x, -0.03, z);
    let i = 0;
    for (let dx = -40; dx < 40; dx++) for (let dz = -40; dz < 40; dz++) {
      const edge = Math.max(Math.abs(dx + 0.5), Math.abs(dz + 0.5));
      const fade = Math.max(0, Math.min(1, (40 - edge) / 9));
      const smooth = fade * fade * (3 - 2 * fade);
      this.matrix.makeScale(0.73 + 0.27 * smooth, smooth, 0.73 + 0.27 * smooth);
      this.matrix.setPosition(x + dx + 0.5, -0.02 + 0.06 * smooth, z + dz + 0.5);
      this.studs.setMatrixAt(i++, this.matrix);
    }
    this.studs.instanceMatrix.needsUpdate = true;
    this.focusLight.position.set(x - 15, 35, z + 20);
    this.focusLight.target.position.set(x, 0, z);
    this.focusLight.target.updateMatrixWorld();
    this.dirty = true;
  }
  private invalidate = () => { this.dirty = this.pointerDirty = true; };
  private resize = () => {
    const { width, height } = this.host.getBoundingClientRect();
    if (!width || !height || this.disposed) return;
    const gl = this.renderer.getContext();
    const limit = this.renderer.capabilities.maxTextureSize;
    const viewport = gl.getParameter(gl.MAX_VIEWPORT_DIMS) as Int32Array;
    this.renderer.setPixelRatio(Math.min(2.5, limit / width, limit / height, viewport[0] / width, viewport[1] / height, Math.sqrt(12_000_000 / (width * height))));
    this.renderer.setSize(width, height, false);
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.invalidate();
  };
  private tick = () => {
    if (this.disposed) return;
    this.controls.update();
    this.updateGround();
    if (this.pointerDirty) this.updateHover();
    if (this.dirty) {
      const start = performance.now();
      this.renderer.render(this.scene, this.camera);
      this.frameMs = performance.now() - start;
      this.renderedFrames++;
      this.dirty = false;
    }
    this.frame = requestAnimationFrame(this.tick);
  };
  private contextLost = (event: Event) => {
    event.preventDefault();
    this.callbacks.error('WebGL context lost');
  };
  snapshot() {
    const { width, height } = this.host.getBoundingClientRect();
    const project = (point: Vector3) => {
      const p = point.project(this.camera);
      return { x: (p.x + 1) * width / 2, y: (1 - p.y) * height / 2 };
    };
    return {
      count: this.bricks.length, tool: this.tool, brush: this.brush, hover: this.hover,
      frameMs: this.frameMs, renderedFrames: this.renderedFrames, batches: this.batches.size,
      drawCalls: this.renderer.info.render.calls, groundInstances: this.studs.count,
      target: this.controls.target.toArray(), groundCenter: this.floor.position.toArray(),
      preview: this.ghost.visible, pixelRatio: this.renderer.getPixelRatio(),
      canDeleteSelected: this.selectedId ? canRemove(this.bricks, this.selectedId) : false,
      bricks: this.bricks.map(brick => ({ ...brick, screen: project(new Vector3(brick.x + footprint(brick).width / 2, (brick.y + partById.get(brick.partId)!.height) * PLATE_HEIGHT + 0.17, brick.z + footprint(brick).depth / 2)) })),
      grid: [-8, 0, 8].flatMap(x => [-8, 0, 8].map(z => ({ worldX: x, worldZ: z, ...project(new Vector3(x + 0.5, 0, z + 0.5)) }))),
    };
  }
  dispose() {
    this.disposed = true;
    cancelAnimationFrame(this.frame);
    this.observer.disconnect();
    this.controls.removeEventListener('change', this.invalidate);
    this.controls.dispose();
    const canvas = this.renderer.domElement;
    canvas.removeEventListener('pointermove', this.pointerMove);
    canvas.removeEventListener('pointerdown', this.pointerDown);
    canvas.removeEventListener('pointerleave', this.pointerLeave);
    canvas.removeEventListener('webglcontextlost', this.contextLost);
    window.removeEventListener('pointerup', this.pointerUp);
    window.removeEventListener('pointercancel', this.pointerCancel);
    this.batches.forEach(batch => batch.mesh.dispose());
    this.geometries.forEach(geometry => geometry.dispose());
    this.material.dispose(); this.ghostMaterial.dispose();
    this.floor.geometry.dispose(); this.floor.material.dispose();
    this.studs.dispose(); this.studs.geometry.dispose(); (this.studs.material as MeshStandardMaterial).dispose();
    this.outline.geometry.dispose(); (this.outline.material as LineBasicMaterial).dispose();
    this.ghostOutline.geometry.dispose(); (this.ghostOutline.material as LineBasicMaterial).dispose();
    (this.picker.material as MeshStandardMaterial).dispose();
    this.renderer.dispose(); this.renderer.forceContextLoss(); canvas.remove();
  }
}
