/** Publication-only original-geometry renderer; does not edit the dataset. */
import { Box3, Mesh, Vector3 } from 'three';
import { AtlasScene } from '../src/scene/AtlasScene';
import { BrickModel } from '../src/model/BrickModel';
import { initialState, type AtlasManifest } from '../src/model/types';
import cases from '../benchmark/complex-examples-v1/render-cases.json';

const modelId = new URLSearchParams(location.search).get('model') ?? 'omr-42004';
const select = document.querySelector<HTMLSelectElement>('#case')!;
const status = document.querySelector<HTMLElement>('#status')!;
const button = document.querySelector<HTMLButtonElement>('#prepare')!;
let scene: AtlasScene, manifest: AtlasManifest, revision = 0;
let result: { image: string; metadata: Record<string, unknown> } | null = null;
declare global { interface Window { __complexCapture?: () => typeof result } }
for (const [id, c] of Object.entries(cases)) if (c.model === modelId) select.add(new Option(id, id));
const toId = (label: string) => `brick_${Number(label.slice(1)).toString().padStart(6, '0')}`;

async function settle() {
  const start = performance.now();
  await new Promise<void>((resolve, reject) => {
    let frames = 0;
    const step = () => {
      if (performance.now() - start > 20000) return reject(new Error('Camera did not settle'));
      frames = scene.snapshot().cameraMoving ? 0 : frames + 1;
      if (frames >= 3) resolve(); else requestAnimationFrame(step);
    };
    step();
  });
}

async function render() {
  button.disabled = true; status.textContent = 'Rendering';
  const key = select.value as keyof typeof cases, spec = cases[key];
  const ids = spec.ids?.map(toId) ?? null;
  scene.setState({ ...initialState, isolation: ids, quality: 'high', background: 'white',
    grid: false, highlightStep: false, revision: ++revision },
  { animateAssembly: false, preserveCamera: true });
  await settle();
  scene.renderer.shadowMap.enabled = false;
  scene.scene.traverse(o => {
    if (o instanceof Mesh && !Array.isArray(o.material) && o.material.type === 'ShadowMaterial') o.visible = false;
  });
  const visible = manifest.instances.filter(p => !ids || ids.includes(p.instanceId));
  const box = new Box3();
  for (const p of visible) { box.expandByPoint(new Vector3(...p.bounds.min)); box.expandByPoint(new Vector3(...p.bounds.max)); }
  const center = box.getCenter(new Vector3()), radius = box.getSize(new Vector3()).length() / 2;
  scene.camera.fov = 30;
  scene.camera.position.copy(center).addScaledVector(new Vector3(...spec.direction).normalize(),
    radius / Math.sin(15 * Math.PI / 180) * 1.06);
  scene.controls.target.copy(center); scene.controls.update();
  scene.camera.updateProjectionMatrix(); scene.camera.updateMatrixWorld();
  scene.renderer.render(scene.scene, scene.camera);
  const canvas = document.createElement('canvas');
  canvas.width = 2400; canvas.height = 1500;
  const ctx = canvas.getContext('2d')!;
  ctx.drawImage(scene.renderer.domElement, 0, 0, canvas.width, canvas.height);
  const bounds = scene.renderer.domElement.getBoundingClientRect();
  const sx = canvas.width / bounds.width, sy = canvas.height / bounds.height;
  ctx.font = 'bold 25px monospace'; ctx.textBaseline = 'middle';
  const occupied: { x: number; y: number }[] = [], projections = [];
  for (const label of spec.labels) {
    const p = manifest.instances.find(p => p.instanceId === toId(label))!;
    const v = scene.projectPart(p);
    const anchor = { x: v.x * sx, y: v.y * sy };
    let x = Math.min(canvas.width - 140, anchor.x + 40), y = Math.max(25, anchor.y - 35);
    while (occupied.some(p => Math.abs(p.x - x) < 155 && Math.abs(p.y - y) < 45)) y += 48;
    if (y > canvas.height - 30) throw new Error(`Label outside canvas: ${label}`);
    occupied.push({ x, y });
    ctx.lineWidth = 2; ctx.strokeStyle = '#254f70'; ctx.fillStyle = 'white';
    ctx.beginPath(); ctx.moveTo(anchor.x, anchor.y); ctx.lineTo(x, y); ctx.stroke();
    ctx.fillRect(x - 6, y - 18, 98, 36); ctx.strokeRect(x - 6, y - 18, 98, 36);
    ctx.fillStyle = '#193e5a'; ctx.fillText(label, x, y);
    projections.push({ label, anchor, text: { x, y } });
  }
  result = { image: canvas.toDataURL('image/png'), metadata: {
    id: key, model: modelId, sourceHash: manifest.sourceHash, sourcePosesPreserved: true,
    visibleIds: visible.map(p => p.instanceId), visibleCount: visible.length, projections,
    camera: { position: scene.camera.position.toArray(), target: scene.controls.target.toArray(), fov: 30 },
    width: canvas.width, height: canvas.height, scope: 'Source view, not a simulated fault or physically removed state',
  } };
  status.textContent = 'Ready'; button.disabled = false;
}

button.addEventListener('click', () => render().catch(error => { status.textContent = `Error: ${error}`; button.disabled = false; }));
async function start() {
  button.disabled = true;
  manifest = await (await fetch(`/models/${modelId}/manifest.json`)).json();
  await new Promise<void>((ready, reject) => {
    scene = new AtlasScene(document.querySelector<HTMLElement>('#scene')!, new BrickModel(manifest),
      { ready, error: reject, progress: () => {}, select: () => {}, hover: () => {} }, 'en');
  });
  scene.controls.enableDamping = false;
  window.__complexCapture = () => result;
  status.textContent = 'Loaded'; button.disabled = false;
}
start().catch(error => { status.textContent = `Error: ${error}`; });
