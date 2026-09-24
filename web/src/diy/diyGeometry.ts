import {
  AmbientLight, Box3, BoxGeometry, BufferGeometry, Color, ConeGeometry, CylinderGeometry, DirectionalLight,
  ExtrudeGeometry, Group, MathUtils, Mesh, MeshStandardMaterial, Path, PerspectiveCamera, Scene, Shape,
  SphereGeometry, TorusGeometry, Vector3, WebGLRenderer, ACESFilmicToneMapping,
} from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { footprint, partById, PLATE_HEIGHT, stamp, type DiyPart, type DiyRecipe } from './diyModel';
import { brickPalette } from '../creator/imageBrickModel';

export function createDiyGeometry(part: DiyPart): BufferGeometry {
  const { width, depth, shape } = part;
  const h = part.height * PLATE_HEIGHT;
  const geometries: BufferGeometry[] = [];
  const add = (geometry: BufferGeometry) => {
    const value = geometry.index ? geometry.toNonIndexed() : geometry;
    if (value !== geometry) geometry.dispose();
    geometries.push(value);
    return value;
  };
  const box = (w: number, height: number, d: number, x = 0, y = height / 2, z = 0) => {
    const geometry = new RoundedBoxGeometry(Math.max(.04, w), Math.max(.04, height), Math.max(.04, d), 2, Math.min(.045, w / 5, height / 5, d / 5));
    geometry.translate(x, y, z);
    return add(geometry);
  };
  let body: BufferGeometry;
  if (shape === 'round') {
    body = add(new CylinderGeometry(Math.max(.3, width / 2 - .035), Math.max(.3, width / 2 - .035), h - .025, 28));
    body.translate(0, h / 2, 0);
  } else if (shape === 'cone') {
    body = add(new ConeGeometry(Math.max(.42, width / 2 - .04), h, 32));
    body.translate(0, h / 2, 0);
  } else if (shape === 'dish') {
    body = add(new SphereGeometry(Math.max(.45, width / 2), 24, 8, 0, Math.PI * 2, 0, Math.PI * .32));
    body.scale(1, .38, 1);
    body.translate(0, .08, 0);
  } else if (shape === 'turntable') {
    body = add(new CylinderGeometry(width / 2 - .04, width / 2 - .04, h - .025, 32));
    body.translate(0, h / 2, 0);
    const ring = add(new TorusGeometry(width * .32, .055, 8, 28));
    ring.rotateX(Math.PI / 2); ring.translate(0, h + .025, 0);
  } else if (shape === 'wheel') {
    body = add(new TorusGeometry(Math.max(.38, width * .27), .19, 12, 28));
    body.translate(0, Math.max(.45, width * .27), 0);
    const hub = add(new CylinderGeometry(.17, .17, depth * .9, 16));
    hub.rotateX(Math.PI / 2); hub.translate(0, Math.max(.45, width * .27), 0);
  } else if (shape === 'pin') {
    body = add(new CylinderGeometry(.22, .22, width - .08, 16));
    body.rotateZ(Math.PI / 2); body.translate(0, .3, 0);
    const collar = add(new CylinderGeometry(.3, .3, .18, 16));
    collar.rotateZ(Math.PI / 2); collar.translate(width * .18, .3, 0);
  } else if (shape === 'axle') {
    body = add(new BoxGeometry(width - .08, .2, .2)); body.translate(0, .28, 0);
    const cross = add(new BoxGeometry(width - .08, .12, .32)); cross.translate(0, .28, 0);
  } else if (shape === 'bar') {
    body = add(new CylinderGeometry(.13, .13, width - .08, 14));
    body.rotateZ(Math.PI / 2); body.translate(0, .26, 0);
  } else if (shape === 'technic' || shape === 'beam') {
    const bh = shape === 'beam' ? Math.max(.48, h) : h;
    const profile = new Shape();
    profile.moveTo(-width / 2 + .04, .04);
    profile.lineTo(width / 2 - .04, .04);
    profile.lineTo(width / 2 - .04, bh - .04);
    profile.lineTo(-width / 2 + .04, bh - .04);
    profile.closePath();
    for (let x = 0; x < width; x++) {
      const hole = new Path();
      hole.absellipse(x + .5 - width / 2, bh / 2, .255, .255, 0, Math.PI * 2, true);
      profile.holes.push(hole);
    }
    body = add(new ExtrudeGeometry(profile, { depth: Math.max(.3, depth - .08), bevelEnabled: false, curveSegments: 16 }));
    body.translate(0, 0, -Math.max(.3, depth - .08) / 2);
  } else if (shape === 'arch') {
    body = box(width - .04, Math.min(1.2, h), depth - .04, 0, h - Math.min(.6, h / 2));
    box(.92, Math.max(.3, h - .6), depth - .04, -(width - 1) / 2, (h - .6) / 2);
    box(.92, Math.max(.3, h - .6), depth - .04, (width - 1) / 2, (h - .6) / 2);
  } else if (shape === 'fence') {
    body = box(width - .04, .25, depth - .04, 0, .125);
    box(width - .04, .18, .18, 0, h * .52);
    box(width - .04, .18, .18, 0, h - .12);
    for (let x = 0; x < width; x++) box(.13, h - .18, .18, x + .5 - width / 2, h / 2);
  } else if (shape === 'panel') {
    body = box(width - .04, .36, depth - .04, 0, .18);
    box(width - .08, Math.max(.3, h - .34), .16, 0, .34 + (h - .34) / 2, -(depth - .16) / 2);
  } else if (shape === 'propeller') {
    body = add(new CylinderGeometry(.34, .34, .25, 20)); body.translate(0, .2, 0);
    for (let blade = 0; blade < 3; blade++) {
      const geometry = add(new BoxGeometry(width * .42, .14, .38));
      geometry.translate(width * .2, .2, 0);
      geometry.rotateY(blade * Math.PI * 2 / 3);
    }
  } else if (shape === 'slope' || shape === 'inverted-slope' || shape === 'curved') {
    body = new BoxGeometry(width - 0.035, h - 0.025, depth - 0.035);
    const position = body.getAttribute('position');
    for (let i = 0; i < position.count; i++) {
      const high = position.getZ(i) < 0;
      if (shape === 'slope' && position.getY(i) > 0 && !high) position.setY(i, -h / 2 + PLATE_HEIGHT);
      if (shape === 'inverted-slope' && position.getY(i) < 0 && !high) position.setY(i, h / 2 - PLATE_HEIGHT);
      if (shape === 'curved' && position.getY(i) > 0) {
        const t = MathUtils.clamp((position.getZ(i) / depth + .5), 0, 1);
        position.setY(i, -h / 2 + PLATE_HEIGHT + (h - PLATE_HEIGHT) * Math.cos(t * Math.PI / 2));
      }
    }
    body.computeVertexNormals();
    body.translate(0, h / 2, 0);
    add(body);
  } else {
    body = box(width - .035, h - .025, depth - .035);
    if (shape === 'grille') {
      for (let x = 0; x < width * 3; x++) box(.045, .055, depth * .72, x / 3 + 1 / 6 - width / 2, h + .025);
    }
    if (shape === 'side-stud') {
      const side = add(new CylinderGeometry(.3, .3, .16, 18));
      side.rotateX(Math.PI / 2); side.translate(0, Math.min(h * .62, .72), depth / 2 + .08);
    }
    if (shape === 'clip') {
      const clip = add(new TorusGeometry(.28, .09, 8, 16, Math.PI * 1.5));
      clip.rotateX(Math.PI / 2); clip.rotateZ(Math.PI / 2); clip.translate(width / 2 + .18, Math.max(.3, h), 0);
    }
  }
  if (!['tile', 'grille', 'beam', 'pin', 'axle', 'bar', 'fence', 'wheel', 'propeller'].includes(shape)) {
    const studPositions: [number, number][] = [];
    if (part.top === 'center') studPositions.push([0, 0]);
    else {
      const rows = part.top === 'rear' ? 1 : depth;
      for (let x = 0; x < width; x++) for (let z = 0; z < rows; z++) studPositions.push([x + .5 - width / 2, z + .5 - depth / 2]);
    }
    for (const [x, z] of studPositions) {
      const cylinder = new CylinderGeometry(0.3, 0.3, 0.16, 20);
      cylinder.translate(x, h + 0.08, z);
      add(cylinder);
    }
  }
  const result = mergeGeometries(geometries);
  geometries.forEach(geometry => geometry.dispose());
  if (!result) throw new Error(`Unable to generate DIY geometry for ${part.id}`);
  result.computeBoundingBox();
  result.computeBoundingSphere();
  return result;
}

// All library thumbnails use the same real geometry as the placement preview.
// A single short-lived WebGL context renders the whole library into 2D canvases.
export function renderDiyThumbnails(targets: { recipe: DiyRecipe; canvas: HTMLCanvasElement }[], colorId: string) {
  const renderer = new WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(200, 130);
  renderer.toneMapping = ACESFilmicToneMapping;
  const scene = new Scene();
  scene.add(new AmbientLight(0xffffff, 2.1));
  const light = new DirectionalLight(0xffffff, 3);
  light.position.set(8, 12, 10);
  scene.add(light);
  const materials = new Map<string, MeshStandardMaterial>();
  const cache = new Map<string, BufferGeometry>();
  const camera = new PerspectiveCamera(32, 200 / 130, 0.1, 200);
  try {
    for (const { recipe, canvas } of targets) {
      const group = new Group();
      for (const brick of stamp({ recipeId: recipe.id, turn: 0, color: colorId }, 0, 0, 0)) {
        let geometry = cache.get(brick.partId);
        if (!geometry) {
          geometry = createDiyGeometry(partById.get(brick.partId)!);
          cache.set(brick.partId, geometry);
        }
        const hex = brickPalette.find(color => color.id === brick.color)!.hex;
        let material = materials.get(hex);
        if (!material) {
          material = new MeshStandardMaterial({ color: new Color(hex), roughness: 0.3 });
          materials.set(hex, material);
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
    materials.forEach(material => material.dispose());
    renderer.dispose();
    renderer.forceContextLoss();
  }
}
