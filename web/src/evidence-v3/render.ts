/** Scientific label-only rendering at frozen source poses and reference positions. */
import { AtlasScene } from '../scene/AtlasScene';
import { BrickModel } from '../model/BrickModel';
import { initialState, type AtlasManifest } from '../model/types';
import { Mesh } from 'three';

type Job = { observation_id: string; model_id: string; target_id: string;
  render_operands: string[]; labels: Record<string,string>;
  camera: { position: [number,number,number]; target: [number,number,number]; fov: number };
  reference_positions: { id: string; anchor: [number,number]; text: [number,number] }[] };
type Capture = { image: string; base: string; mask: string; metadata: Record<string,unknown> };
const status = document.querySelector<HTMLElement>('#status')!;
const select = document.querySelector<HTMLSelectElement>('#job')!;
const button = document.querySelector<HTMLButtonElement>('#prepare')!;
const modelId = new URLSearchParams(location.search).get('model') ?? 'omr-42004';
let scene: AtlasScene, manifest: AtlasManifest, jobs: Job[], revision = 0;
let result: Capture | null = null;
declare global { interface Window { __evidenceV3Capture?: () => Capture | null } }
async function json(url: string) {
  const r = await fetch(url); if (!r.ok) throw new Error(`${r.status}: ${url}`); return r.json();
}
async function settled() {
  const start = performance.now(); let frames = 0;
  await new Promise<void>((resolve,reject) => {
    function tick() {
      if (performance.now()-start > 20000) { reject(new Error('Camera did not settle')); return; }
      frames = scene.snapshot().cameraMoving ? 0 : frames+1;
      if (frames >= 3) resolve(); else requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
}
function state(ids: string[] | null) {
  scene.setState({ ...initialState, quality:'auto', grid:false, background:'white',
    highlightStep:false, isolation:ids, view:'perspective', revision:++revision },
  { animateAssembly:false, preserveCamera:true });
  scene.renderer.shadowMap.enabled = false;
}
function canvas() { const c = document.createElement('canvas'); c.width=1280; c.height=800; return c; }
async function render(job: Job) {
  result = null; button.disabled=true; status.textContent='Rendering';
  state(null); await settled(); state(job.render_operands); await settled();
  scene.camera.fov=job.camera.fov;
  scene.camera.position.set(...job.camera.position); scene.controls.target.set(...job.camera.target);
  scene.controls.update(); scene.camera.updateProjectionMatrix(); scene.camera.updateMatrixWorld();
  scene.scene.traverse(o => {
    if (o instanceof Mesh && !Array.isArray(o.material) && o.material.type==='ShadowMaterial') o.visible=false;
  });
  scene.renderer.render(scene.scene,scene.camera);
  const base=canvas(), b=base.getContext('2d')!;
  b.drawImage(scene.renderer.domElement,0,0,1280,800);
  const image=canvas(), ctx=image.getContext('2d')!;
  ctx.drawImage(base,0,0);
  const mask=canvas(), m=mask.getContext('2d')!;
  m.fillStyle='white'; m.fillRect(0,0,1280,800); m.fillStyle='black'; m.strokeStyle='black';
  ctx.font='bold 16px ui-monospace, monospace'; ctx.textBaseline='middle';
  for (const ref of job.reference_positions) {
    const p=scene.projectPart(manifest.instances.find(i=>i.instanceId===ref.id)!);
    if (Math.abs(p.x-ref.anchor[0])>1e-4 || Math.abs(p.y-ref.anchor[1])>1e-4)
      throw new Error(`Frozen projection mismatch: ${ref.id}`);
    const [x,y]=ref.text, [ax,ay]=ref.anchor, label=job.labels[ref.id];
    const width=ctx.measureText(label).width+8;
    ctx.strokeStyle='#174263'; ctx.lineWidth=1.4;
    ctx.beginPath(); ctx.moveTo(ax,ay); ctx.lineTo(x,y); ctx.stroke();
    ctx.fillStyle='#ffffffef'; ctx.fillRect(x-4,y-12,width,24);
    ctx.strokeRect(x-4,y-12,width,24); ctx.fillStyle='#174263'; ctx.fillText(label,x,y);
    // Includes a conservative antialiasing border around both text boxes and leaders.
    m.lineWidth=5; m.beginPath(); m.moveTo(ax,ay); m.lineTo(x,y); m.stroke();
    m.fillRect(x-7,y-15,width+6,30);
  }
  result={image:image.toDataURL('image/png'),base:base.toDataURL('image/png'),mask:mask.toDataURL('image/png'),
    metadata:{observation_id:job.observation_id,model_id:modelId,width:1280,height:800,
      camera:job.camera,labels:job.labels,reference_positions:job.reference_positions,
      render_operands:job.render_operands,source_poses_preserved:true,shadows:false,
      label_policy:'fixed per-instance positions and order; underlying render unchanged'}};
  status.textContent='Ready'; button.disabled=false;
}
button.addEventListener('click',()=>render(jobs.find(j=>j.observation_id===select.value)!).catch(e=>{
  status.textContent=`Error: ${e}`;button.disabled=false;
}));
async function start() {
  button.disabled=true;
  jobs=(await json('/benchmark/evidence-v3/render-plan.json')).jobs.filter((j:Job)=>j.model_id===modelId);
  manifest=await json(`/models/${modelId}/manifest.json`);
  for(const j of jobs)select.add(new Option(j.observation_id,j.observation_id));
  await new Promise<void>((ready,error)=>{
    scene=new AtlasScene(document.querySelector<HTMLElement>('#scene')!,new BrickModel(manifest),
      {ready,error,progress:()=>{},select:()=>{},hover:()=>{}},'en');
  });
  scene.controls.enableDamping=false;
  window.__evidenceV3Capture=()=>result;
  status.textContent='Loaded';button.disabled=false;
}
start().catch(e=>{status.textContent=`Error: ${e}`});
