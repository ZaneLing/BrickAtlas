const $ = id => document.getElementById(id);
const state = {session:null, observation:null, probe:null, probeId:null, frames:[], busy:false, study:false, reviewing:false};
async function api(path, data) {
  const res = await fetch(path, data === undefined ? {} :
    {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)});
  const out = await res.json(); if (!res.ok) throw Error(out.error || res.status); return out;
}
const opt = (value, label=value) => {const o=document.createElement('option');o.value=value;o.textContent=label;return o;};
const message = text => {$('message').textContent=text;};
const describe = a => a?.type === 'attach' ? `Attach ${a.partId} → ${a.siteId}` :
  a?.type === 'detach' ? `Detach ${a.partId}` : JSON.stringify(a);
function download(name, value) {
  const url=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)],{type:'application/json'}));
  const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
function disabled() {
  const off = state.busy || state.reviewing || !state.session || state.observation?.terminated;
  for(const id of ['attach','detach','rework-yes','rework-no','finish']) $(id).disabled=off;
  for(const id of ['start','mode','task-select','inspect','probe-answer']) $(id).disabled=state.busy;
  $('inspect').disabled ||= state.reviewing || state.observation?.terminated || state.observation?.remainingInspections === 0;
}
function guarded(fn) {return async (...args)=>{
  if(state.busy)return;state.busy=true;disabled();
  try{await fn(...args);}catch(e){message(e.message);}finally{state.busy=false;disabled();}
};}
async function populate(obs) {
  state.observation=obs;
  for(const [key,raster] of Object.entries(obs.images || {})) {
    const bytes=Uint8Array.from(atob(raster.base64),ch=>ch.charCodeAt(0));
    const bitmap=await createImageBitmap(new Blob([bytes],{type:raster.mime}));
    const canvas=$(key);canvas.width=raster.width;canvas.height=raster.height;
    canvas.getContext('2d').drawImage(bitmap,0,0);bitmap.close();
  }
  const selectedSite=$('site').value,selectedPart=$('part').value;
  const sites=obs.siteIds || obs.sites.map(s=>s.id);
  const parts=obs.partIds || [...obs.inventory.map(p=>p.id),...obs.sites.map(s=>s.installedPartId).filter(Boolean)].sort();
  $('site').replaceChildren(...sites.map(s=>opt(s)));
  $('part').replaceChildren(...parts.map(p=>opt(p)));
  if(sites.includes(selectedSite))$('site').value=selectedSite;
  if(parts.includes(selectedPart))$('part').value=selectedPart;
  $('counts').textContent=`${obs.attempts} / ${obs.actionBudget} actions · revision ${obs.revision}${obs.terminated?' · ended':''}`;
  $('inspection-count').textContent=`${obs.remainingInspections} inspections · ${obs.remainingDiagnoses} diagnoses left`;
  $('view').value=obs.view;
  const {images,...publicFields}=obs;
  $('observation').textContent=JSON.stringify({...publicFields,images:Object.keys(images || {})},null,2);
  disabled();
}
async function history() {
  const events=(await api(`/api/sessions/${state.session}/history`)).events;
  $('history').textContent=events.map(e=>`${e.revision}. ${describe(e.action)} · ${e.code}`).join('\n');
}
async function review() {
  if(state.study){message('Episode ended. Scores remain private during the study.');return;}
  const report=await api(`/api/sessions/${state.session}/score`);
  state.frames=(await api(`/api/sessions/${state.session}/replay`)).frames;
  $('score').textContent=JSON.stringify({status:report.status,actions:report.attempts,
    actionRegret:report.actionRegret,detachRegret:report.detachRegret,
    selfInducedEvents:report.online.selfInducedEvents},null,2);
  $('review').hidden=false;$('replay').max=state.frames.length-1;$('replay').value=state.frames.length-1;
  $('frame-label').textContent=`${state.frames.length-1} / ${state.frames.length-1}`;
}
async function act(action) {
  const request={requestId:crypto.randomUUID(),revision:state.observation.revision,action};
  try {
    const result=await api(`/api/sessions/${state.session}/actions`,request);
    await populate(result.observation);await history();message(`${describe(action)} · ${result.result.code}`);
    if(result.observation.terminated)await review();
  } catch(e) {
    // Re-read authoritative state after network uncertainty; never auto-repeat a move.
    const current=await api(`/api/sessions/${state.session}`);
    await populate(current.observation);await history();throw e;
  }
}
async function loadProbe(response) {
  state.probe=response;state.session=null;
  $('probe-panel').hidden=false;$('review').hidden=true;
  $('probe-question').textContent=response.question;
  $('proposed-plan').replaceChildren(...(response.proposedPlan||[]).map(a=>{
    const li=document.createElement('li');li.textContent=describe(a);return li;}));
  $('probe-answer').replaceChildren(...(response.kind==='lookahead' ?
    [opt('null','No conflict'),...response.proposedPlan.map((_,i)=>opt(String(i+1),`First conflict: ${i+1}`))] :
    response.candidates.map((a,i)=>opt(String(i),describe(a)))));
  await populate(response.observation);
}
async function openTask(existing=null) {
  state.reviewing=false;
  $('review').hidden=true;$('probe-panel').hidden=true;$('history').textContent='';
  if($('mode').value==='probes') {
    state.probeId=$('task-select').value;
    await loadProbe(await api(`/api/probes/${state.probeId}`));
    $('session-label').textContent=state.probeId;
    window.history.replaceState(null,'','/');
  } else {
    const response=existing ? await api(`/api/sessions/${existing}`) :
      await api('/api/sessions',{taskId:$('task-select').value,seed:crypto.getRandomValues(new Uint32Array(1))[0]});
    state.session=response.sessionId;state.probe=null;
    $('task-select').value=response.taskId;$('session-label').textContent=response.taskId;
    window.history.replaceState(null,'',`/?session=${state.session}`);
    await populate(response.observation);await history();
    if(response.observation.terminated)await review();
  }
  message('Workcell ready. Inspect the images, then choose an action.');
}
async function catalog() {
  const mode=$('mode').value;
  const response=await api(mode==='episodes'?'/api/tasks':'/api/probes');
  $('task-select').replaceChildren(...(response.tasks||response.probes).map(t=>opt(t.id,`${t.id} · ${t.case||t.kind}`)));
}
$('start').onclick=guarded(()=>openTask());
$('mode').onchange=guarded(async()=>{await catalog();await openTask();});
$('attach').onclick=guarded(()=>act({type:'attach',partId:$('part').value,siteId:$('site').value}));
$('detach').onclick=guarded(()=>act({type:'detach',partId:$('part').value}));
$('rework-yes').onclick=guarded(()=>act({type:'diagnose',needsRework:true}));
$('rework-no').onclick=guarded(()=>act({type:'diagnose',needsRework:false}));
$('finish').onclick=guarded(()=>act({type:'finish'}));
$('inspect').onclick=guarded(async()=>{
  if(state.session)await act({type:'inspect',view:$('view').value});
  else {const answer=$('probe-answer').value;
    const result=await api(`/api/probes/${state.probeId}/inspect`,{view:$('view').value});
    await loadProbe(result);$('probe-answer').value=answer;message(result.result.code);}
});
$('probe-form').onsubmit=guarded(async e=>{
  e.preventDefault();
  const key=state.probe.kind==='lookahead'?'firstConflict':'choice';
  await api(`/api/probes/${state.probeId}/answer`,{[key]:JSON.parse($('probe-answer').value)});
  message(`Answer frozen for ${state.probeId}.`);
});
$('replay').onchange=guarded(async()=>{
  state.reviewing=true;
  const n=+$('replay').value;
  await populate((await api(`/api/sessions/${state.session}/frame/${n}`)).observation);
  $('frame-label').textContent=`${n} / ${state.frames.length-1} · ${state.frames[n].code}`;
  // Reviewing a past frame must never enable structural actions on the ended session.
  for(const id of ['attach','detach','rework-yes','rework-no','finish','inspect'])$(id).disabled=true;
});
$('export').onclick=guarded(async()=>download(`brickplan-${state.session}.json`,await api(`/api/sessions/${state.session}/export`)));
$('export-feedback').onclick=()=>download(`brickplan-feedback-${state.session}.json`,{
  schema:'brickplan-review/1.2',sessionId:state.session,frame:+$('replay').value,
  track:state.observation.track,note:$('feedback').value});
async function init() {
  const info=await api('/api/tasks');state.study=info.study;
  $('track').textContent=`${info.track} · ${info.study?'study':'practice'}`;
  await catalog();
  const existing=new URLSearchParams(location.search).get('session');
  await openTask(existing);
}
guarded(init)();
