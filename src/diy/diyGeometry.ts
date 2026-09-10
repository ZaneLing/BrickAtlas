import {
  AmbientLight, Box3, BoxGeometry, BufferGeometry, Color, CylinderGeometry, DirectionalLight,
  Group, Mesh, MeshStandardMaterial, PerspectiveCamera, Scene, Vector3, WebGLRenderer, ACESFilmicToneMapping,
} from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { footprint, partById, PLATE_HEIGHT, stamp, type DiyPart, type DiyRecipe } from './diyModel';

export function createDiyGeometry(part: DiyPart): BufferGeometry {
  const { width, depth, shape } = part;
  const h = part.height * PLATE_HEIGHT;
  let body: BufferGeometry;
  if (shape === 'round') body = new CylinderGeometry(0.48, 0.48, h - 0.025, 24);
  else if (shape === 'slope') {
    body = new BoxGeometry(width - 0.035, h - 0.025, depth - 0.035);
    const position = body.getAttribute('position');
    for (let i = 0; i < position.count; i++) {
      if (position.getY(i) > 0 && position.getZ(i) > 0) position.setY(i, -h / 2 + PLATE_HEIGHT);
    }
    body.computeVertexNormals();
  } else body = new RoundedBoxGeometry(width - 0.035, h - 0.025, depth - 0.035, 2, 0.045);
  body.translate(0, h / 2, 0);
  const geometries = [body.index ? body.toNonIndexed() : body];
  if (geometries[0] !== body) body.dispose();
  if (shape !== 'tile') {
    const rows = shape === 'slope' ? 1 : depth;
    for (let x = 0; x < width; x++) for (let z = 0; z < rows; z++) {
      const cylinder = new CylinderGeometry(0.3, 0.3, 0.16, 20);
      cylinder.translate(x + 0.5 - width / 2, h + 0.08, z + 0.5 - depth / 2);
      geometries.push(cylinder.toNonIndexed());
      cylinder.dispose();
    }
  }
  const result = mergeGeometries(geometries);
  geometries.forEach(geometry => geometry.dispose());
  result.computeBoundingBox();
  result.computeBoundingSphere();
  return result;
}

// All library thumbnails use the same real geometry as the placement preview.
// A single short-lived WebGL context renders the whole library into 2D canvases.
export function renderDiyThumbnails(targets: { recipe: DiyRecipe; canvas: HTMLCanvasElement }[], color: string) {
  const renderer = new WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(200, 130);
  renderer.toneMapping = ACESFilmicToneMapping;
  const scene = new Scene();
  scene.add(new AmbientLight(0xffffff, 2.1));
  const light = new DirectionalLight(0xffffff, 3);
  light.position.set(8, 12, 10);
  scene.add(light);
  const material = new MeshStandardMaterial({ color: new Color(color), roughness: 0.3 });
  const cache = new Map<string, BufferGeometry>();
  const camera = new PerspectiveCamera(32, 200 / 130, 0.1, 200);
  try {
    for (const { recipe, canvas } of targets) {
      const group = new Group();
      for (const brick of stamp({ recipeId: recipe.id, turn: 0, color: 'red' }, 0, 0, 0)) {
        let geometry = cache.get(brick.partId);
        if (!geometry) {
          geometry = createDiyGeometry(partById.get(brick.partId)!);
          cache.set(brick.partId, geometry);
        }
        const mesh = new Mesh(geometry, material);
        const size = footprint(brick);
        mesh.position.set(brick.x + size.width / 2, brick.y * PLATE_HEIGHT, brick.z + size.depth / 2);
        mesh.rotation.y = brick.turn * Math.PI / 2;
        group.add(mesh);
      }
      const box = new Box3().setFromObject(group), size = box.getSize(new Vector3()), center = box.getCenter(new Vector3());
      const distance = Math.max(size.length() * 1.7, 5);
      camera.position.copy(center).addScaledVector(new Vector3(0.8, 0.8, 1).normalize(), distance);
      camera.lookAt(center);
      scene.add(group);
      renderer.render(scene, camera);
      canvas.width = 200; canvas.height = 130;
      canvas.getContext('2d')?.drawImage(renderer.domElement, 0, 0);
      scene.remove(group);
    }
  } finally {
    cache.forEach(geometry => geometry.dispose());
    material.dispose();
    renderer.dispose();
    renderer.forceContextLoss();
  }
}
