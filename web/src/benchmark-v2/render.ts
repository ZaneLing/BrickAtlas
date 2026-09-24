import { AtlasScene } from '../scene/AtlasScene';
import { BrickModel } from '../model/BrickModel';
import { initialState, type AtlasManifest } from '../model/types';
import { labelPermutation, operandLabels } from '../../benchmark/suite/ldraw-v2/conditions';
import type { InternalBundle, V2Task } from '../../benchmark/suite/ldraw-v2/types';
import { Box3, Vector3, Mesh } from 'three';

const status = document.querySelector<HTMLElement>('#status')!;
const taskSelect = document.querySelector<HTMLSelectElement>('#task')!;
const conditionSelect = document.querySelector<HTMLSelectElement>('#condition')!;
const prepare = document.querySelector<HTMLButtonElement>('#prepare')!;
const host = document.querySelector<HTMLElement>('#scene')!;
const modelId = new URLSearchParams(location.search).get('model') ?? '31028';
const modes = ['full', 'mask', 'crop', 'id', 'camera', 'neutral', 'wrong'];
for (const mode of modes) conditionSelect.add(new Option(mode, mode));
let scene: AtlasScene, manifest: AtlasManifest, bundle: InternalBundle;
let revision = 0;
let image = '', metadata: Record<string, unknown> = {};
declare global {
  interface Window {
    __v2RenderCapture?: () => { image: string; metadata: Record<string, unknown> };
  }
}
const json = async (url: string) => {
  const response = await fetch(url); if (!response.ok) throw new Error(`${response.status}: ${url}`);
  return response.json();
};
async function settled() {
  const started = performance.now();
  let frames = 0;
  await new Promise<void>((resolve, reject) => {
    function check() {
      if (performance.now() - started > 20000) { reject(new Error('Camera did not settle')); return; }
      if (!scene.snapshot().cameraMoving) frames++; else frames = 0;
      if (frames >= 3) resolve(); else requestAnimationFrame(check);
    }
    requestAnimationFrame(check);
  });
}
function setState(ids: string[] | null, view: 'perspective' | 'rear') {
  scene.setState({ ...initialState, quality: 'auto', grid: false, background: 'white',
    highlightStep: false, isolation: ids, view, revision: ++revision }, { animateAssembly: false, preserveCamera: true });
  // Shadows must not change between full and masked conditions.
  scene.renderer.shadowMap.enabled = false;
}
function canonicalCamera(ids: string[] | null, rear = false) {
  const box = new Box3();
  for (const p of manifest.instances.filter(p => !ids || ids.includes(p.instanceId))) {
    box.expandByPoint(new Vector3(...p.bounds.min)); box.expandByPoint(new Vector3(...p.bounds.max));
  }
  const center = box.getCenter(new Vector3()), radius = box.getSize(new Vector3()).length() / 2;
  const direction = new Vector3(rear ? 1 : -1, .65, 1).normalize();
  scene.camera.fov = 34;
  scene.camera.position.copy(center).addScaledVector(direction, Math.max(15, radius / Math.sin(17 * Math.PI / 180) * 1.08));
  scene.controls.target.copy(center); scene.controls.update();
  scene.camera.updateProjectionMatrix(); scene.camera.updateMatrixWorld();
}
function capture(ids: string[], labels: Record<string, string>, neutral = false) {
  // ShadowMaterial can retain an earlier shadow-map texture even when shadow
  // updates are disabled. Remove the receiver explicitly for deterministic
  // background ablation; original part meshes remain untouched.
  scene.scene.traverse(object => {
    if (object instanceof Mesh && !Array.isArray(object.material) && object.material.type === 'ShadowMaterial')
      object.visible = false;
  });
  scene.renderer.render(scene.scene, scene.camera);
  const canvas = document.createElement('canvas');
  canvas.width = 1280; canvas.height = 800;
  const ctx = canvas.getContext('2d')!;
  ctx.filter = neutral ? 'grayscale(1)' : 'none';
  ctx.drawImage(scene.renderer.domElement, 0, 0, 1280, 800); ctx.filter = 'none';
  ctx.font = 'bold 16px ui-monospace, monospace'; ctx.textBaseline = 'middle';
  const occupied: { x: number; y: number }[] = [], projections = [];
  for (const id of [...ids].sort((a, b) => labels[a].localeCompare(labels[b]))) {
    const p = scene.projectPart(manifest.instances.find(part => part.instanceId === id)!);
    if (p.z < -1 || p.z > 1 || p.x < 0 || p.x > 1280 || p.y < 0 || p.y > 800)
      throw new Error(`Operand outside viewport: ${id}`);
    let x = Math.max(6, Math.min(1194, p.x + 16)), y = Math.max(18, Math.min(780, p.y - 22));
    for (let i = 0; i <= occupied.length; i++) {
      if (!occupied.some(o => Math.abs(o.x - x) < 87 && Math.abs(o.y - y) < 29)) break;
      y += 30;
      if (y > 780) { y = 18; x = Math.max(6, x - 90); }
    }
    occupied.push({ x, y });
    ctx.strokeStyle = '#174263'; ctx.lineWidth = 1.4;
    ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(x, y); ctx.stroke();
    const width = ctx.measureText(labels[id]).width + 8;
    ctx.fillStyle = '#ffffffef'; ctx.fillRect(x - 4, y - 12, width, 24);
    ctx.strokeRect(x - 4, y - 12, width, 24);
    ctx.fillStyle = '#174263'; ctx.fillText(labels[id], x, y);
    projections.push({ id, label: labels[id], anchor: [p.x, p.y], text: [x, y] });
  }
  return { image: canvas.toDataURL('image/png'), projections };
}
async function render(task: V2Task, mode: string) {
  status.textContent = 'Rendering'; prepare.disabled = true;
  const labelsNeeded = operandLabels(task);
  const refs = task.references.filter(r => labelsNeeded.includes(r.label)).sort((a, b) => a.label.localeCompare(b.label));
  if (refs.length > 12 || !refs.length) throw new Error('Invalid visual operand count');
  let ids = refs.map(r => r.id), labels = Object.fromEntries(refs.map(r => [r.id, r.label]));
  let mismatch: Record<string, unknown> | null = null;
  if (mode === 'wrong') {
    if (task.family === 'color') {
      const target = manifest.instances.find(p => p.instanceId === ids[0])!;
      const candidateColors = task.options!.filter(o => o.id !== task.answer.choiceId).map(o => o.label);
      const donor = manifest.instances.find(p => p.colorName !== target.colorName && candidateColors.includes(p.colorName))!;
      if (!donor) throw new Error('No semantic color mismatch');
      ids = [donor.instanceId]; labels = { [donor.instanceId]: labelsNeeded[0] };
      mismatch = { original: target.instanceId, donor: donor.instanceId,
        alternateChoiceId: task.options!.find(o => o.label === donor.colorName)!.id };
    } else {
      const correct = task.options!.find(o => o.id === task.answer.choiceId)!;
      const other = task.options!.find(o => o.id !== task.answer.choiceId)!;
      const a = refs.find(r => r.label === correct.label)!, b = refs.find(r => r.label === other.label)!;
      [labels[a.id], labels[b.id]] = [labels[b.id], labels[a.id]];
      mismatch = { swappedLabels: [a.label, b.label], alternateChoiceId: other.id };
    }
  }
  // Every item resets the full camera, making the mask pair independent of
  // browser interaction history and of previous tasks/conditions.
  setState(null, 'perspective'); await settled(); canonicalCamera(null);
  const fullCamera = { position: scene.camera.position.toArray(), target: scene.controls.target.toArray() };
  if (mode !== 'full') {
    setState(ids, mode === 'camera' ? 'rear' : 'perspective');
    await settled();
    canonicalCamera(mode === 'mask' ? null : ids, mode === 'camera');
  }
  if (mode === 'id') {
    const mapping = labelPermutation({ question: task.promptEn, options: task.options!.map(o => ({ id: o.id, label: o.label })) });
    labels = Object.fromEntries(Object.entries(labels).map(([id, name]) => [id, mapping[name]]));
  }
  const result = capture(ids, labels, mode === 'neutral');
  image = result.image;
  metadata = { version: 2, taskId: task.id, modelId, mode, sourceHash: bundle.entry.sourceHash,
    width: 1280, height: 800, labels, projections: result.projections, fullCamera,
    camera: { position: scene.camera.position.toArray(), target: scene.controls.target.toArray(), fov: scene.camera.fov },
    visibleInstances: scene.snapshot().visibleInstances, renderOperands: ids, mismatch,
    background: 'white', shadows: false, sourcePosesPreserved: true };
  status.textContent = 'Ready'; prepare.disabled = false;
}
prepare.addEventListener('click', () => {
  const task = bundle.tasks.find(t => t.id === taskSelect.value)!;
  render(task, conditionSelect.value).catch(error => { status.textContent = `Error: ${error}`; prepare.disabled = false; });
});
async function start() {
  prepare.disabled = true;
  bundle = await json(`/benchmark/ldraw-v2/models/${modelId}.json`);
  manifest = await json(`/models/${modelId}/manifest.json`);
  for (const task of bundle.tasks.filter(t => t.visualInput)) taskSelect.add(new Option(task.id, task.id));
  await new Promise<void>((ready, reject) => {
    scene = new AtlasScene(host, new BrickModel(manifest), {
      ready, error: reject, progress: () => {}, select: () => {}, hover: () => {},
    }, 'en');
  });
  scene.controls.enableDamping = false;
  setState(null, 'perspective'); await settled();
  window.__v2RenderCapture = () => ({ image, metadata });
  status.textContent = 'Loaded'; prepare.disabled = false;
}
start().catch(error => { status.textContent = `Error: ${error}`; });
