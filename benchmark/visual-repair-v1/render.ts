import { Box3, Mesh, Vector3 } from 'three';
import { AtlasScene } from '../../src/scene/AtlasScene';
import { BrickModel } from '../../src/model/BrickModel';
import { initialState, type AtlasManifest } from '../../src/model/types';
import specs from './render-specs.json';

const modelId = new URLSearchParams(location.search).get('model')!;
const select = document.querySelector<HTMLSelectElement>('#construction')!;
const status = document.querySelector<HTMLElement>('#status')!;
const button = document.querySelector<HTMLButtonElement>('#render')!;
type Spec = typeof specs[keyof typeof specs];
type Frame = { id: string; image: string; metadata: Record<string, unknown> };
let scene: AtlasScene, manifest: AtlasManifest, revision = 0;
let result: Frame[] | null = null;
declare global { interface Window {
  __visualRepairCapture?: () => Frame[] | null;
  __visualRepairFont?: () => string;
} }

for (const cid of new Set(Object.values(specs).filter(s => s.model === modelId).map(s => s.construction_id))) {
  select.add(new Option(cid, cid));
}

async function settle() {
  await new Promise<void>((resolve, reject) => {
    const start = performance.now();
    let stable = 0;
    const tick = () => {
      if (performance.now() - start > 15000) return reject(new Error('Camera did not settle'));
      stable = scene.snapshot().cameraMoving ? 0 : stable + 1;
      if (stable >= 3) resolve(); else requestAnimationFrame(tick);
    };
    tick();
  });
}

function bounds(ids: string[]) {
  const box = new Box3();
  for (const p of manifest.instances.filter(p => ids.includes(p.instanceId))) {
    box.expandByPoint(new Vector3(...p.bounds.min));
    box.expandByPoint(new Vector3(...p.bounds.max));
  }
  return box;
}

async function sourceView(ids: string[], radius: number, direction: number[]) {
  scene.setState({ ...initialState, isolation: ids, quality: 'high', background: 'white',
    grid: false, highlightStep: false, revision: ++revision },
    { animateAssembly: false, preserveCamera: true });
  await settle();
  scene.renderer.shadowMap.enabled = false;
  scene.scene.traverse(o => {
    if (o instanceof Mesh && !Array.isArray(o.material) && o.material.type === 'ShadowMaterial') o.visible = false;
  });
  const center = bounds(ids).getCenter(new Vector3());
  scene.camera.fov = 30;
  scene.camera.position.copy(center).addScaledVector(new Vector3(...direction).normalize(),
    radius / Math.sin(Math.PI / 12) * 1.10);
  scene.controls.target.copy(center);
  scene.controls.update();
  scene.camera.updateProjectionMatrix();
  scene.camera.updateMatrixWorld();
  scene.renderer.render(scene.scene, scene.camera);
  const canvas = document.createElement('canvas');
  canvas.width = 480; canvas.height = 300;
  canvas.getContext('2d')!.drawImage(scene.renderer.domElement, 0, 0, 480, 300);
  return { canvas, camera: { position: scene.camera.position.toArray(),
    target: center.toArray(), fov: 30, direction } };
}

async function renderConstruction() {
  button.disabled = true; status.textContent = 'Rendering'; result = null;
  const entries = Object.entries(specs).filter(([, s]) => s.construction_id === select.value);
  const first = entries[0][1];
  const ids = first.cards.map(c => c.source_id);
  const radius = Math.max(...ids.map(id => bounds([id]).getSize(new Vector3()).length() / 2));
  const reference = await sourceView([first.reference_id], radius, [-1, .8, 1.2]);
  const cardViews = new Map<string, Awaited<ReturnType<typeof sourceView>>>();
  for (const id of ids) cardViews.set(id, await sourceView([id], radius, [1, 1, 1.2]));
  const frames: Frame[] = [];
  for (const [id, spec] of entries as [string, Spec][]) {
    const canvas = document.createElement('canvas');
    canvas.width = 1600; canvas.height = 900;
    const ctx = canvas.getContext('2d')!;
    ctx.fillStyle = 'white'; ctx.fillRect(0, 0, 1600, 900);
    ctx.fillStyle = '#183042'; ctx.font = '26px sans-serif';
    ctx.fillText('Match reference geometry; read its current candidate ID.', 28, 40);
    ctx.font = 'bold 25px sans-serif';
    ctx.fillText('REFERENCE', 160, 230);
    ctx.drawImage(reference.canvas, 20, 260);
    ctx.font = '18px sans-serif';
    ctx.fillText('Different camera, same scale.', 82, 595);
    ctx.fillText('Source geometry; neutral materials.', 51, 625);
    const cards = [];
    for (const [i, card] of spec.cards.entries()) {
      const x = 560 + (i % 2) * 510, y = 80 + Math.floor(i / 2) * 400;
      ctx.strokeStyle = '#d4dde5'; ctx.lineWidth = 1;
      ctx.strokeRect(x - 10, y - 10, 500, 370);
      ctx.drawImage(cardViews.get(card.source_id)!.canvas, x, y);
      ctx.fillStyle = '#183042'; ctx.font = 'bold 28px "Courier New"';
      ctx.textAlign = 'center'; ctx.textBaseline = 'top';
      ctx.fillText(card.label, x + 240, y + 317);
      ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
      cards.push({ label: card.label, source_id: card.source_id,
        shape_box: [x, y, 480, 300], label_box: [x + 130, y + 307, 220, 50],
        camera: cardViews.get(card.source_id)!.camera });
    }
    frames.push({ id, image: canvas.toDataURL('image/png'), metadata: {
      construction_id: spec.construction_id, replicate: spec.replicate, arm: spec.arm,
      source_id: modelId, source_hash: manifest.sourceHash, source_poses_preserved: true,
      geometry_modified: false, display_material: 'uniform opaque neutral gray, no source color cue',
      reference_id: first.reference_id, reference_box: [20, 260, 480, 300],
      reference_camera: reference.camera, cards, width: 1600, height: 900,
      common_camera_radius: radius,
    } });
  }
  const context = await sourceView(first.source_ids,
    bounds(first.source_ids).getSize(new Vector3()).length() / 2, [-1, .8, 1.2]);
  frames.push({ id: select.value, image: context.canvas.toDataURL('image/png'), metadata: {
    construction_id: select.value, source_id: modelId, source_poses_preserved: true,
    ids: first.source_ids, camera: context.camera,
    scope: 'Provenance-only source subassembly, not a physically removed state or native evidence',
  } });
  result = frames; status.textContent = 'Ready'; button.disabled = false;
}

button.addEventListener('click', () => renderConstruction().catch(e => {
  status.textContent = `Error: ${e}`; button.disabled = false;
}));
async function start() {
  manifest = await (await fetch(`/models/${modelId}/manifest.json`)).json();
  // Clone metadata, never change source records or vertex/instance transforms.
  const display = structuredClone(manifest);
  for (const p of display.instances) p.colorHex = '#acb8c4';
  for (const chunk of display.chunks) for (const bucket of chunk.buckets) {
    bucket.material.color = '#75808c';
    bucket.material.opacity = 1; bucket.material.roughness = .65; bucket.material.metalness = 0;
  }
  await new Promise<void>((ready, reject) => {
    scene = new AtlasScene(document.querySelector<HTMLElement>('#scene')!, new BrickModel(display),
      { ready, error: reject, progress: () => {}, select: () => {}, hover: () => {} }, 'en');
  });
  scene.controls.enableDamping = false;
  window.__visualRepairCapture = () => result;
  window.__visualRepairFont = () => {
    const canvas = document.createElement('canvas');
    canvas.width = 352; canvas.height = 50;
    const ctx = canvas.getContext('2d')!;
    ctx.fillStyle = 'white'; ctx.fillRect(0, 0, 352, 50);
    ctx.fillStyle = '#183042'; ctx.font = 'bold 28px "Courier New"';
    ctx.textAlign = 'center'; ctx.textBaseline = 'top';
    [...'V0123456789'].forEach((c, i) => ctx.fillText(c, 16 + i * 32, 10));
    return canvas.toDataURL('image/png');
  };
  status.textContent = 'Loaded'; button.disabled = false;
}
start().catch(e => { status.textContent = `Error: ${e}`; });
