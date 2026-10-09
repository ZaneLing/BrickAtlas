import * as THREE from 'three';
import { OrbitControls } from '/vendor/OrbitControls.js';

const $ = id => document.getElementById(id);
const state = { observation: null, session: null, mode: 'episodes', busy: false,
  meshes: {}, geometry: new Map(), events: [], frames: [], probe: null, probeId: null };
const colors = { '0': '#202326', '1': '#0055bf', '4': '#c91a09', '7': '#9ba19d',
  '14': '#f2cd37', '15': '#ffffff', '71': '#a0a5a9', '72': '#6c6e68' };
const worldAxis = new THREE.Matrix4().makeRotationX(Math.PI);
const views = { isometric: [1.35, 1.05, 1.55], front: [0, .05, 2], rear: [0, .05, -2],
  left: [-2, .05, 0], right: [2, .05, 0], top: [0, 2, .001], bottom: [0, -2, .001] };
const message = (text, error = false) => { $('message').textContent = text; $('message').classList.toggle('error', error); };
async function api(path, data) {
  const response = await fetch(path, data === undefined ? {} : {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || `HTTP ${response.status}`);
  return result;
}
function option(value, text) { const node = document.createElement('option'); node.value = value; node.textContent = text; return node; }
function download(name, value) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(value, null, 2)], { type: 'application/json' }));
  const link = document.createElement('a'); link.href = url; link.download = name; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function describe(a) {
  return a?.type === 'attach' ? `Attach ${a.partId} → ${a.siteId}` :
    a?.type === 'detach' ? `Detach ${a.partId}` :
    a?.type === 'diagnose' ? `Diagnose: ${a.needsRework ? 'needs rework' : 'no rework'}` :
    a?.type === 'inspect' ? `Inspect ${a.view}` : a?.type || 'Initial state';
}
function partObject(part, siteId = null, ghost = false) {
  const root = new THREE.Group();
  const groups = state.meshes[part.partNumber];
  if (!groups) throw new Error(`Missing original part geometry: ${part.partNumber}`);
  for (const [color, positions] of Object.entries(groups)) {
    const key = `${part.partNumber}:${color}`;
    if (!state.geometry.has(key)) {
      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
      geometry.computeVertexNormals(); state.geometry.set(key, geometry);
    }
    const material = new THREE.MeshStandardMaterial({
      color: ghost ? '#d1f589' : color === '16' ? part.color : colors[color] || part.color,
      roughness: .33, metalness: .03, side: THREE.DoubleSide,
      wireframe: ghost, transparent: ghost, opacity: ghost ? .18 : 1,
      depthWrite: !ghost,
    });
    const mesh = new THREE.Mesh(state.geometry.get(key), material);
    mesh.userData.siteId = siteId;
    root.add(mesh);
  }
  root.applyMatrix4(worldAxis.clone().multiply(new THREE.Matrix4().set(...part.matrix.flat())));
  root.userData.siteId = siteId;
  return root;
}
function disposeGroup(group) {
  group.traverse(child => {
    if (child.material) child.material.dispose();
    // Original part buffers are shared and cached.
    if (child.geometry && ![...state.geometry.values()].includes(child.geometry)) child.geometry.dispose();
  });
  group.clear();
}
class SceneView {
  constructor(hostId, target = false) {
    this.host = $(hostId); this.target = target;
    this.scene = new THREE.Scene(); this.scene.background = new THREE.Color(target ? '#242d2c' : '#202827');
    this.renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    this.renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.setClearColor(this.scene.background);
    this.host.append(this.renderer.domElement);
    this.camera = new THREE.PerspectiveCamera(36, 1, 1, 4000);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true; this.controls.dampingFactor = .12;
    this.scene.add(new THREE.HemisphereLight('#f3ffec', '#596466', 2.6));
    const sun = new THREE.DirectionalLight('#ffffff', 3.2); sun.position.set(140, 250, 180); this.scene.add(sun);
    const fill = new THREE.DirectionalLight('#c9dced', 1.6); fill.position.set(-180, 90, -120); this.scene.add(fill);
    this.parts = new THREE.Group(); this.stage = new THREE.Group(); this.scene.add(this.parts, this.stage);
    this.labels = []; this.selected = null; this.radius = 170; this.center = new THREE.Vector3();
    new ResizeObserver(() => this.resize()).observe(this.host);
    this.renderer.domElement.addEventListener('pointerdown', e => { this.pointer = [e.clientX, e.clientY]; });
    this.renderer.domElement.addEventListener('pointerup', e => {
      if (!this.pointer || Math.hypot(e.clientX - this.pointer[0], e.clientY - this.pointer[1]) > 5) return;
      const rect = this.host.getBoundingClientRect();
      const ray = new THREE.Raycaster();
      ray.setFromCamera(new THREE.Vector2(2 * (e.clientX - rect.left) / rect.width - 1,
        1 - 2 * (e.clientY - rect.top) / rect.height), this.camera);
      const hit = ray.intersectObjects(this.parts.children, true).find(h => h.object.userData.siteId);
      if (hit) { $('site').value = hit.object.userData.siteId; selectionChanged(); }
    });
  }
  resize() {
    const { width, height } = this.host.getBoundingClientRect();
    if (!width || !height) return;
    this.camera.aspect = width / height; this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height, false);
  }
  orient(view = 'isometric') {
    const direction = new THREE.Vector3(...views[view]).normalize();
    const aspectFactor = Math.max(1, 1 / this.camera.aspect);
    this.camera.position.copy(this.center).addScaledVector(direction, this.radius * 3.2 * aspectFactor);
    this.camera.up.set(0, 1, 0); this.camera.lookAt(this.center);
    this.controls.target.copy(this.center); this.controls.update();
  }
  renderObservation(obs, fit = false) {
    disposeGroup(this.parts); disposeGroup(this.stage);
    this.labels.forEach(l => l.node.remove()); this.labels = [];
    const boundsGroup = new THREE.Group();
    for (const p of [...obs.fixed, ...obs.sites]) boundsGroup.add(partObject(p));
    const box = new THREE.Box3().setFromObject(boundsGroup);
    box.getCenter(this.center); this.radius = box.getSize(new THREE.Vector3()).length() * .52;
    disposeGroup(boundsGroup);
    for (const part of obs.fixed) this.parts.add(partObject(part));
    const explode = this.target ? +$('explode').value / 100 : 0;
    for (const part of obs.sites) {
      const visible = this.target ? part.required : Boolean(part.installedPartId);
      if (!visible && part.id !== $('site').value) continue;
      const root = partObject(part, part.id, !visible);
      if (this.target && visible && explode) {
        const direction = new THREE.Vector3().copy(root.position).sub(this.center);
        if (direction.length() < 5) direction.set(0, 25, 0);
        root.position.addScaledVector(direction.normalize(), explode * 75);
      }
      this.parts.add(root);
      const partBox = new THREE.Box3().setFromObject(root);
      const anchor = partBox.getCenter(new THREE.Vector3()); anchor.y = partBox.max.y + 3;
      const node = document.createElement('button'); node.className = 'part-label';
      node.textContent = this.target || !part.installedPartId ? part.id : `${part.installedPartId} · ${part.id}`;
      node.title = `Select ${part.id}`; node.onclick = () => { $('site').value = part.id; selectionChanged(); };
      this.host.append(node); this.labels.push({ node, anchor, siteId: part.id });
    }
    const bed = new THREE.Mesh(new THREE.BoxGeometry(box.max.x - box.min.x + 35, 5, box.max.z - box.min.z + 35),
      new THREE.MeshStandardMaterial({ color: '#37433e', roughness: .9 }));
    bed.position.set(this.center.x, box.min.y - 3, this.center.z); this.stage.add(bed);
    const grid = new THREE.GridHelper(500, 25, '#49554d', '#303b36');
    grid.position.set(this.center.x, box.min.y - 6, this.center.z); this.stage.add(grid);
    if (fit) { this.resize(); this.orient(obs.view); }
  }
  draw() {
    this.controls.update();
    for (const { node, anchor, siteId } of this.labels) {
      const selected = siteId === $('site').value;
      const v = anchor.clone().project(this.camera);
      node.hidden = !($('labels').checked || selected) || v.z > 1 || v.z < -1;
      node.classList.toggle('selected', selected);
      node.style.left = `${(v.x + 1) * this.host.clientWidth / 2}px`;
      node.style.top = `${(1 - v.y) * this.host.clientHeight / 2}px`;
    }
    this.renderer.render(this.scene, this.camera);
  }
}
let currentView, goalView;
function selectionChanged() {
  const obs = displayedObservation();
  if (!obs) return;
  const part = obs.sites.find(s => s.id === $('site').value) || obs.sites[0];
  $('site-detail').replaceChildren();
  const title = document.createElement('b'); title.textContent = `${part.name} · ${part.partNumber}`;
  const swatch = document.createElement('i'); swatch.className = 'swatch'; swatch.style.background = part.color;
  const detail = document.createElement('div');
  detail.textContent = `${part.required ? 'Required in target' : 'Not required in target'} · ${part.installedPartId || 'Empty site'}`;
  $('site-detail').append(swatch, title, detail);
  currentView.renderObservation(obs); goalView.renderObservation(obs);
}
function displayedObservation() {
  return state.frames.length && ! $('review').hidden ? state.frames[+$('replay').value].observation : state.observation;
}
function populate(obs, fit = false) {
  const site = $('site').value, inventory = $('part').value;
  $('site').replaceChildren(...obs.sites.map(s => option(s.id, `${s.id} · ${s.partNumber} · ${s.installedPartId || 'empty'}`)));
  if (obs.sites.some(s => s.id === site)) $('site').value = site;
  $('part').replaceChildren(...obs.inventory.map(p => option(p.id, `${p.id} · type ${p.partType}`)));
  if (obs.inventory.some(p => p.id === inventory)) $('part').value = inventory;
  $('revision').textContent = `REV ${String(obs.revision).padStart(3, '0')}`;
  $('goal-count').textContent = `${obs.sites.filter(s => s.required).length} sites`;
  $('attempt-count').textContent = obs.attempts; $('budget-total').textContent = `/ ${obs.actionBudget} actions`;
  $('installed-count').textContent = `${obs.sites.filter(s => s.installedPartId).length} movable parts installed · ${obs.fixed.length} fixed`;
  $('budget-fill').style.width = `${100 * obs.attempts / obs.actionBudget}%`;
  $('inspection-count').textContent = `${obs.remainingInspections} inspections left`;
  $('observation').textContent = JSON.stringify(obs, null, 2);
  $('run-state').textContent = state.mode === 'probes' ? 'PROBE' : state.frames.length ? 'REVIEW' : obs.terminated ? 'ENDED' : 'ACTIVE';
  selectionChanged(); if (fit) { currentView.orient(obs.view); goalView.orient(obs.view); }
  setDisabled();
}
function setDisabled() {
  const disabled = state.busy || state.mode === 'probes' || !state.observation || state.observation.terminated;
  for (const id of ['attach', 'detach', 'finish', 'rework-yes', 'rework-no', 'part']) $(id).disabled = disabled;
  $('inspect').disabled = state.busy;
  for (const id of ['start', 'task-select', 'episodes-tab', 'probes-tab']) $(id).disabled = state.busy;
}
function renderHistory() {
  $('history-count').textContent = `${state.events.length} events`;
  $('history').replaceChildren();
  for (const event of state.events) {
    const row = document.createElement('div'); row.className = 'event';
    const n = document.createElement('span'); n.className = 'number'; n.textContent = String(event.revision).padStart(2, '0');
    const desc = document.createElement('span'); desc.textContent = describe(event.action);
    const result = document.createElement('span'); result.className = 'result';
    result.textContent = event.code;
    if (!['OK', 'FINISHED', 'INSPECTED', 'DIAGNOSIS_RECORDED'].includes(event.code)) result.classList.add('bad');
    row.append(n, desc, result); $('history').append(row);
  }
  $('history').scrollTop = $('history').scrollHeight;
}
async function review() {
  const report = await api(`/api/sessions/${state.session}/score`);
  state.frames = (await api(`/api/sessions/${state.session}/replay`)).frames;
  $('replay').max = state.frames.length - 1; $('replay').value = state.frames.length - 1;
  $('score').replaceChildren();
  for (const [label, value] of [['Outcome', report.status], ['Actions', `${report.attempts} / ${report.budget}`],
    ['Action regret', report.actionRegret ?? '—'], ['Detach regret', report.detachRegret ?? '—']]) {
    const cell = document.createElement('div'); cell.className = 'score-cell';
    const title = document.createElement('span'); title.textContent = label;
    const num = document.createElement('strong'); num.textContent = value; cell.append(title, num); $('score').append(cell);
  }
  $('review').hidden = false; showFrame();
}
function showFrame() {
  const index = +$('replay').value, frame = state.frames[index];
  $('frame-label').textContent = `${index} / ${state.frames.length - 1} · ${frame.code}`;
  populate(frame.observation);
}
async function action(a) {
  if (state.busy) return;
  state.busy = true; setDisabled();
  try {
    const before = state.observation;
    const result = await api(`/api/sessions/${state.session}/actions`,
      { requestId: crypto.randomUUID(), revision: before.revision, action: a });
    state.observation = result.observation;
    state.events.push({ revision: state.observation.revision, action: a, code: result.result.code });
    renderHistory(); populate(state.observation);
    if (a.type === 'inspect') { currentView.orient(a.view); goalView.orient(a.view); }
    message(`${describe(a)} · ${result.result.code}`, !['OK', 'INSPECTED', 'FINISHED', 'DIAGNOSIS_RECORDED'].includes(result.result.code));
    if (state.observation.terminated) await review();
  } catch (error) {
    message(error.message, true);
    // Network uncertainty never triggers an automatic duplicate structural action.
    const recovered = await api(`/api/sessions/${state.session}`);
    state.observation = recovered.observation;
    state.events = (await api(`/api/sessions/${state.session}/history`)).events;
    populate(state.observation); renderHistory();
    if (state.observation.terminated) await review();
  } finally { state.busy = false; setDisabled(); }
}
async function loadSession(key = null) {
  state.frames = []; $('review').hidden = true; $('probe-panel').hidden = true;
  const response = key ? await api(`/api/sessions/${key}`) :
    await api('/api/sessions', { taskId: $('task-select').value, seed: crypto.getRandomValues(new Uint32Array(1))[0] });
  state.session = response.sessionId; state.observation = response.observation;
  $('task-select').value = response.taskId;
  localStorage.setItem('brickplan-session', state.session);
  history.replaceState(null, '', `/?session=${state.session}`);
  $('session-label').textContent = `${response.taskId} · SESSION ${state.session.slice(0, 8)}`;
  state.events = (await api(`/api/sessions/${state.session}/history`)).events;
  renderHistory(); populate(state.observation, true);
  message('Workcell ready. Select a site and an inventory part, then attach. Current legality is checked on execution.');
  if (state.observation.terminated) await review();
}
async function loadProbe() {
  state.frames = []; state.events = []; state.session = null; $('review').hidden = true;
  state.probeId = $('task-select').value;
  state.probe = await api(`/api/probes/${state.probeId}`);
  state.observation = state.probe.observation; $('probe-panel').hidden = false;
  history.replaceState(null, '', '/');
  $('session-label').textContent = `PROBE ${state.probeId}`;
  $('probe-kind').textContent = state.probe.kind.toUpperCase();
  $('probe-question').textContent = state.probe.question;
  $('proposed-plan').replaceChildren();
  for (const a of state.probe.proposedPlan || []) { const li = document.createElement('li'); li.textContent = describe(a); $('proposed-plan').append(li); }
  const answers = state.probe.kind === 'lookahead'
    ? [option('null', 'No conflict: all actions execute'), ...state.probe.proposedPlan.map((_, i) => option(String(i + 1), `First conflict at action ${i + 1}`))]
    : state.probe.candidates.map((a, i) => option(String(i), `${i + 1}. ${describe(a)}`));
  $('probe-answer').replaceChildren(...answers);
  renderHistory(); populate(state.observation, true);
  message('Read the current scene and target. Predict before execution; the proposed plan is not played for you.');
}
async function switchMode(mode) {
  state.mode = mode; state.frames = []; $('review').hidden = true;
  $('episodes-tab').classList.toggle('active', mode === 'episodes'); $('probes-tab').classList.toggle('active', mode === 'probes');
  const catalog = await api(mode === 'episodes' ? '/api/tasks' : '/api/probes');
  const items = catalog.tasks || catalog.probes;
  $('task-select').replaceChildren(...items.map(t => option(t.id, `${t.id} · ${t.case || t.kind}${t.startType ? ` · ${t.startType}` : ''}`)));
  $('start').textContent = mode === 'episodes' ? 'Start new episode' : 'Open probe';
  if (mode === 'episodes') {
    $('task-select').value = items.find(t => t.startType === 'full build').id;
    await loadSession();
  } else await loadProbe();
}
function safely(fn) { return (...args) => Promise.resolve(fn(...args)).catch(e => message(e.message, true)); }
function loadSafely(fn) {
  return safely(async () => {
    if (state.busy) return;
    state.busy = true; setDisabled();
    try { await fn(); } finally { state.busy = false; setDisabled(); }
  });
}
$('site').onchange = selectionChanged;
$('explode').oninput = () => { if (state.observation) goalView.renderObservation(displayedObservation()); };
$('attach').onclick = () => action({ type: 'attach', partId: $('part').value, siteId: $('site').value });
$('detach').onclick = () => action({ type: 'detach', partId: state.observation.sites.find(s => s.id === $('site').value)?.installedPartId || '' });
$('rework-yes').onclick = () => action({ type: 'diagnose', needsRework: true });
$('rework-no').onclick = () => action({ type: 'diagnose', needsRework: false });
$('finish').onclick = () => action({ type: 'finish' });
$('inspect').onclick = () => {
  if (state.mode === 'probes' || state.observation?.terminated) {
    currentView.orient($('view').value); goalView.orient($('view').value);
  } else action({ type: 'inspect', view: $('view').value });
};
$('start').onclick = loadSafely(() => state.mode === 'episodes' ? loadSession() : loadProbe());
$('episodes-tab').onclick = loadSafely(() => switchMode('episodes'));
$('probes-tab').onclick = loadSafely(() => switchMode('probes'));
$('probe-form').onsubmit = safely(async event => {
  event.preventDefault();
  const key = state.probe.kind === 'lookahead' ? 'firstConflict' : 'choice';
  await api(`/api/probes/${state.probeId}/answer`, { [key]: JSON.parse($('probe-answer').value) });
  message(`Answer frozen for ${state.probeId}.`);
});
$('replay').oninput = showFrame;
$('previous').onclick = () => { $('replay').value = Math.max(0, +$('replay').value - 1); showFrame(); };
$('next').onclick = () => { $('replay').value = Math.min(state.frames.length - 1, +$('replay').value + 1); showFrame(); };
$('export').onclick = safely(async () => download(`brickplan-${state.session}.json`, await api(`/api/sessions/${state.session}/export`)));
$('export-feedback').onclick = () => download(`brickplan-feedback-${state.session}.json`, {
  schema: 'brickplan-review/1.0', sessionId: state.session, frame: +$('replay').value,
  revision: displayedObservation().revision, category: $('feedback-category').value,
  note: $('feedback').value, status: 'open', track: 'known-pose-structured',
});
async function init() {
  state.meshes = (await api('/meshes.json')).meshes;
  currentView = new SceneView('current-view'); goalView = new SceneView('goal-view', true);
  const animate = () => { requestAnimationFrame(animate); currentView.draw(); goalView.draw(); }; animate();
  const catalog = (await api('/api/tasks')).tasks;
  $('task-select').replaceChildren(...catalog.map(t => option(t.id, `${t.id} · ${t.case} · ${t.startType}`)));
  $('task-select').value = catalog.find(t => t.startType === 'full build').id;
  const key = new URLSearchParams(location.search).get('session') || localStorage.getItem('brickplan-session');
  if (key) {
    try { await loadSession(key); } catch { await loadSession(); }
  } else await loadSession();
}
init().catch(error => message(`Arena could not start: ${error.message}`, true));
