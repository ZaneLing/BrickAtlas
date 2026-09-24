/** Scientific stimulus renderer. UI actions prepare images; capture API only reads them. */
import { AtlasScene } from '../scene/AtlasScene';
import { BrickModel } from '../model/BrickModel';
import { initialState, type AtlasManifest } from '../model/types';
import { Box3, Color, Mesh, MeshPhysicalMaterial, Vector3 } from 'three';

type Job = { observation_id: string; model_id: string; kind: string; target_id: string;
  labels: Record<string, string>; render_operands: string[]; candidate_ids?: string[];
  panel_boxes?: number[][]; body_color?: { hex: string } };
const status = document.querySelector<HTMLElement>('#status')!;
const select = document.querySelector<HTMLSelectElement>('#job')!;
const button = document.querySelector<HTMLButtonElement>('#prepare')!;
const modelId = new URLSearchParams(location.search).get('model') ?? '31028';
const appearance = { value: new Color() }, maskMode = { value: false };
let scene: AtlasScene, manifest: AtlasManifest, jobs: Job[], revision = 0;
let result: { image: string; mask: string | null; metadata: Record<string, unknown> } | null = null;
const originals = new Map<Mesh, MeshPhysicalMaterial>(), overrides = new Map<Mesh, MeshPhysicalMaterial>();
declare global { interface Window { __evidenceV2Capture?: () => typeof result } }
async function json(url: string) {
  const r = await fetch(url); if (!r.ok) throw new Error(`${r.status}: ${url}`); return r.json();
}
async function settle() {
  const start = performance.now(); let frames = 0;
  await new Promise<void>((resolve, reject) => {
    function tick() {
      if (performance.now() - start > 20000) { reject(new Error('Scene did not settle')); return; }
      frames = scene.snapshot().cameraMoving ? 0 : frames + 1;
      if (frames >= 3) resolve(); else requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
}
async function isolate(ids: string[]) {
  scene.setState({ ...initialState, quality: 'auto', grid: false, background: 'white',
    highlightStep: false, isolation: ids, revision: ++revision },
  { animateAssembly: false, preserveCamera: true });
  scene.renderer.shadowMap.enabled = false;
  await settle();
  scene.scene.traverse(o => {
    if (o instanceof Mesh && !Array.isArray(o.material) && o.material.type === 'ShadowMaterial') o.visible = false;
  });
  const box = new Box3();
  for (const p of manifest.instances.filter(p => ids.includes(p.instanceId))) {
    box.expandByPoint(new Vector3(...p.bounds.min)); box.expandByPoint(new Vector3(...p.bounds.max));
  }
  const center = box.getCenter(new Vector3()), radius = box.getSize(new Vector3()).length() / 2;
  scene.camera.fov = 34;
  scene.camera.position.copy(center).addScaledVector(new Vector3(-1, .65, 1).normalize(),
    Math.max(15, radius / Math.sin(17 * Math.PI / 180) * 1.08));
  scene.controls.target.copy(center); scene.controls.update();
  scene.camera.updateProjectionMatrix(); scene.camera.updateMatrixWorld();
}
function camera() {
  return { position: scene.camera.position.toArray(), target: scene.controls.target.toArray(),
    fov: scene.camera.fov, aspect: scene.camera.aspect };
}
function bodyMaterials(enabled: boolean) {
  for (const [mesh, original] of originals) {
    mesh.material = enabled ? overrides.get(mesh)! : original;
    if (enabled) {
      // Atlas setState can reset transparency from source metadata. Reset both arms identically.
      const m = mesh.material as MeshPhysicalMaterial;
      m.transparent = false; m.opacity = 1; m.depthWrite = true;
      m.roughness = .35; m.metalness = 0; m.clearcoat = .24;
      m.clearcoatRoughness = .32; m.transmission = 0; m.ior = 1.46;
      m.needsUpdate = true;
    }
  }
}
function canvas() { const c = document.createElement('canvas'); c.width = 1280; c.height = 800; return c; }
async function render(job: Job) {
  status.textContent = 'Rendering'; button.disabled = true; result = null;
  const c = canvas(), ctx = c.getContext('2d')!;
  ctx.fillStyle = 'white'; ctx.fillRect(0, 0, c.width, c.height);
  let mask: string | null = null;
  const projections: unknown[] = [], cameras: unknown[] = [];
  if (job.kind === 'appearance-color') {
    bodyMaterials(false); await isolate([job.target_id]);
    appearance.value.set(job.body_color!.hex); bodyMaterials(true);
    scene.renderer.render(scene.scene, scene.camera);
    ctx.drawImage(scene.renderer.domElement, 0, 0, 1280, 800);
    const p = scene.projectPart(manifest.instances.find(p => p.instanceId === job.target_id)!);
    if (p.z < -1 || p.z > 1 || p.x < 0 || p.x > 1280 || p.y < 0 || p.y > 800)
      throw new Error('Target outside viewport');
    const x = Math.max(6, Math.min(1194, p.x + 16)), y = Math.max(18, Math.min(780, p.y - 22));
    const label = job.labels[job.target_id];
    ctx.font = 'bold 16px ui-monospace, monospace'; ctx.textBaseline = 'middle';
    ctx.strokeStyle = '#174263'; ctx.lineWidth = 1.4;
    ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(x, y); ctx.stroke();
    ctx.fillStyle = '#ffffffef'; ctx.fillRect(x - 4, y - 12, ctx.measureText(label).width + 8, 24);
    ctx.strokeRect(x - 4, y - 12, ctx.measureText(label).width + 8, 24);
    ctx.fillStyle = '#174263'; ctx.fillText(label, x, y);
    projections.push({ id: job.target_id, label, anchor: [p.x, p.y], text: [x, y] });
    cameras.push(camera());
    // A separate body silhouette constrains pixel differences independently of appearance.
    const hidden: { object: import('three').Object3D; visible: boolean }[] = [];
    scene.scene.traverse(o => {
      if ('material' in o && !originals.has(o as Mesh)) { hidden.push({ object: o, visible: o.visible }); o.visible = false; }
    });
    maskMode.value = true; scene.renderer.render(scene.scene, scene.camera);
    const mc = canvas(); mc.getContext('2d')!.drawImage(scene.renderer.domElement, 0, 0, 1280, 800);
    mask = mc.toDataURL('image/png'); maskMode.value = false;
    for (const h of hidden) h.object.visible = h.visible;
  } else if (job.kind === 'position-panels') {
    bodyMaterials(false);
    for (const [i, id] of [job.target_id, ...job.candidate_ids!].entries()) {
      await isolate([id]); scene.renderer.render(scene.scene, scene.camera);
      const [x, y, w, h] = job.panel_boxes![i];
      const scale = Math.min((w - 16) / 1280, (h - 16) / 800), dw = 1280 * scale, dh = 800 * scale;
      ctx.drawImage(scene.renderer.domElement, x + (w - dw) / 2, y + (h - dh) / 2, dw, dh);
      ctx.strokeStyle = '#d4d9df'; ctx.lineWidth = 2; ctx.strokeRect(x + 3, y + 3, w - 6, h - 6);
      cameras.push({ id, panel: job.panel_boxes![i], camera: camera() });
    }
  } else throw new Error('Unexpected render kind');
  result = { image: c.toDataURL('image/png'), mask, metadata: {
    observation_id: job.observation_id, model_id: modelId, kind: job.kind,
    width: 1280, height: 800, cameras, projections, render_operands: job.render_operands,
    source_poses_preserved: true, shadows: false, background: 'white',
    color_settings: job.kind === 'appearance-color' ? {
      body: job.body_color, opacity: 1, roughness: .35, metalness: 0,
      clearcoat: .24, clearcoat_roughness: .32, transmission: 0, ior: 1.46,
      edges: 'fixed source edge material', tone_mapping: 'ACESFilmic', exposure: 1.12,
    } : null,
  } };
  scene.renderer.render(scene.scene, scene.camera);
  status.textContent = 'Ready'; button.disabled = false;
}
button.addEventListener('click', () => {
  render(jobs.find(j => j.observation_id === select.value)!).catch(error => {
    status.textContent = `Error: ${error}`; button.disabled = false;
  });
});
async function start() {
  button.disabled = true;
  jobs = (await json('/benchmark/evidence-v2/render-plan.json')).jobs.filter((j: Job) => j.model_id === modelId);
  manifest = await json(`/models/${modelId}/manifest.json`);
  for (const j of jobs) select.add(new Option(j.observation_id, j.observation_id));
  await new Promise<void>((ready, error) => {
    scene = new AtlasScene(document.querySelector<HTMLElement>('#scene')!, new BrickModel(manifest),
      { ready, error, progress: () => {}, select: () => {}, hover: () => {} }, 'en');
  });
  scene.controls.enableDamping = false;
  scene.scene.traverse(o => {
    if (!(o instanceof Mesh) || !(o.material instanceof MeshPhysicalMaterial) || !o.material.userData.atlas) return;
    const original = o.material, replacement = original.clone();
    const compile = original.onBeforeCompile.bind(original);
    replacement.onBeforeCompile = (shader, renderer) => {
      compile(shader, renderer);
      shader.uniforms.displayAppearance = appearance; shader.uniforms.displayMask = maskMode;
      shader.fragmentShader = 'uniform vec3 displayAppearance;\nuniform bool displayMask;\n' + shader.fragmentShader;
      shader.fragmentShader = shader.fragmentShader.replace('#include <color_fragment>',
        '#include <color_fragment>\ndiffuseColor.rgb = displayAppearance;');
      shader.fragmentShader += ''; // Keep the source Atlas visibility shader intact.
      shader.fragmentShader = shader.fragmentShader.replace('#include <dithering_fragment>',
        '#include <dithering_fragment>\nif(displayMask) gl_FragColor = vec4(0.,0.,0.,1.);');
    };
    replacement.customProgramCacheKey = () => 'display-appearance-v2-body';
    originals.set(o, original); overrides.set(o, replacement);
  });
  if (!originals.size) throw new Error('No source body meshes');
  window.__evidenceV2Capture = () => result;
  status.textContent = 'Loaded'; button.disabled = false;
}
start().catch(error => { status.textContent = `Error: ${error}`; });
