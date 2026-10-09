const $ = id => document.getElementById(id);
const state = {session:null, observation:null, probe:null, probeId:null, tasks:[],
  busy:false, study:false, historical:false, reviewing:false, frames:[], viewer:null};
const option = (value,label=value) => {const e=document.createElement('option');e.value=value;e.textContent=label;return e;};
const message = text => {$('message').textContent=text;};
const describe = a => a.type==='attach' ? `Attach ${a.partId} → ${a.siteId}` :
  a.type==='audit' ? `Inspect ${a.partId} off assembly` : a.type==='detach' ? `Detach ${a.partId}` :
  a.type==='inspect' ? `Camera: ${a.view}` : a.type==='diagnose' ? `Diagnosis: ${a.avoidableError?'error':'no error'}` : 'Finish';
async function api(path,payload) {
  const response=await fetch(path,payload===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  const data=await response.json();if(!response.ok)throw Error(data.error||response.status);return data;
}
function enable() {
  const unavailable=state.busy||state.historical||state.reviewing||!state.session||state.observation?.terminated;
  for(const id of ['attach','detach','audit','error-yes','error-no','finish'])$(id).disabled=unavailable;
  for(const id of ['start','mode','task-select','show-view','open-3d','replay'])$(id).disabled=state.busy;
  $('inspect').disabled=state.busy||state.historical||state.reviewing||!state.observation||state.observation.remainingViews===0||
    (state.probe?state.probe.answered:state.observation.terminated);
  $('submit-answer').disabled=state.busy||!state.probe||state.probe.answered;
  $('probe-answer').disabled=$('submit-answer').disabled;
}
function guarded(fn){return async(...args)=>{
  if(state.busy)return;state.busy=true;enable();
  try{await fn(...args);}catch(e){message(e.message);}finally{state.busy=false;enable();}
};}
async function draw(images) {
  for(const [key,raster] of Object.entries(images||{})) {
    const bytes=Uint8Array.from(atob(raster.base64),c=>c.charCodeAt(0));
    const bitmap=await createImageBitmap(new Blob([bytes],{type:raster.mime}));
    const canvas=$(key);canvas.width=raster.width;canvas.height=raster.height;
    canvas.getContext('2d').drawImage(bitmap,0,0);bitmap.close();
  }
}
function publicSummary(value) {
  return JSON.parse(JSON.stringify(value,(key,item)=>key==='images'?Object.keys(item):item));
}
async function populate(obs) {
  state.observation=obs;state.historical=false;
  await draw(obs.images);
  const selected=$('part').value;
  $('part').replaceChildren(...obs.partIds.map(p=>option(p)));
  $('site').replaceChildren(...obs.siteIds.map(s=>option(s)));
  if(obs.partIds.includes(selected))$('part').value=selected;
  selectRegistered();
  $('counts').textContent=state.probe?'Checkpoint':`${obs.attempts} / ${obs.actionBudget}`;
  $('rack-count').textContent=`${obs.rack.occupiedHolders} / ${obs.rack.capacity} holders occupied`;
  $('work-orders').replaceChildren(...(obs.workOrders.length?obs.workOrders.map(w=>{
    const e=document.createElement('div');e.textContent=`${w.completed?'✓':'○'} ${w.partId} · ${w.completed?'inspection done':'inspection pending'}`;return e;
  }):[document.createTextNode('No inspection work orders')]));
  $('inspection-count').textContent=`${obs.remainingViews} views · ${obs.remainingDiagnoses} diagnoses left`;
  $('view').value=obs.view;
  $('saved-view').replaceChildren(option('','Current live view'),...obs.inspectionHistory.map((v,i)=>
    option(String(i),`${i+1}. ${v.view} · revision ${v.atRevision}`)));
  $('saved-label').textContent=`Current live view · ${obs.view} · revision ${obs.revision}`;
  $('observation').textContent=JSON.stringify(publicSummary(obs),null,2);
  enable();
}
function selectRegistered(){
  const registration=state.observation?.registration.find(x=>x.partId===$('part').value);
  if(registration)$('site').value=registration.siteId;
}
async function history(){
  const events=(await api(`/api/sessions/${state.session}/history`)).events;
  $('history').textContent=events.map(e=>`${e.revision}. ${describe(e.action)} · ${e.code}`).join('\n');
}
async function review(){
  if(state.study){message('Episode ended. Your response is recorded.');return;}
  const score=await api(`/api/sessions/${state.session}/score`);
  state.frames=(await api(`/api/sessions/${state.session}/replay`)).frames;
  $('score').textContent=JSON.stringify({success:score.success,operations:score.operations,optimal:score.optimal,
    regret:score.regret,avoidableErrors:score.errorEvents.length,conditionalExtraCost:score.conditionalExcessTotal},null,2);
  $('review').hidden=false;$('replay').max=state.frames.length-1;$('replay').value=state.frames.length-1;
  $('frame-label').textContent=`${state.frames.length-1} / ${state.frames.length-1}`;
}
async function act(action){
  const request={requestId:crypto.randomUUID(),revision:state.observation.revision,action};
  try{
    const response=await api(`/api/sessions/${state.session}/actions`,request);
    await populate(response.observation);await history();message(`${describe(action)} · ${response.result.code}`);
    if(response.observation.terminated)await review();
  }catch(e){
    await populate((await api(`/api/sessions/${state.session}`)).observation);await history();throw e;
  }
}
async function loadProbe(probe){
  state.probe=probe;state.session=null;
  $('probe-panel').hidden=false;$('review').hidden=true;
  $('probe-question').textContent=probe.question;
  $('proposed-plan').replaceChildren(...(probe.proposedPlan||[]).map(a=>{
    const li=document.createElement('li');li.textContent=describe(a);return li;
  }));
  $('probe-answer').replaceChildren(...(probe.kind==='next-action'
    ?probe.candidates.map((a,i)=>option(String(i),describe(a)))
    :[option('null','No conflict'),...probe.proposedPlan.map((_,i)=>option(String(i+1),`First conflict: ${i+1}`))]));
  await populate(probe.observation);
  if(probe.answered)message('Answer recorded and frozen.');
}
async function openTask(existing=null){
  state.reviewing=false;
  if(state.viewer){state.viewer.dispose();state.viewer=null;}
  $('free-review').hidden=true;$('review').hidden=true;$('probe-panel').hidden=true;$('history').textContent='';
  if($('mode').value==='probes'){
    state.probeId=$('task-select').value;
    await loadProbe(await api(`/api/probes/${state.probeId}`));
    $('session-label').textContent=state.probeId;
    window.history.replaceState(null,'',`/?probe=${state.probeId}`);
  }else{
    const task=state.tasks.find(t=>t.id===$('task-select').value);
    const resume=existing||(state.study&&task?.sessions.at(-1));
    const response=resume?await api(`/api/sessions/${resume}`):
      await api('/api/sessions',{taskId:$('task-select').value,requestId:crypto.randomUUID()});
    state.session=response.sessionId;state.probe=null;
    if(task&&!task.sessions.includes(state.session))task.sessions.push(state.session);
    $('task-select').value=response.observation.taskId;$('session-label').textContent=response.observation.taskId;
    window.history.replaceState(null,'',`/?session=${state.session}`);
    await populate(response.observation);await history();
    if(response.observation.terminated)await review();
  }
  if(!state.probe?.answered&&!state.observation.terminated)message('Workcell ready. Inspect the assembly, rack and work orders.');
}
async function catalog(){
  const probes=$('mode').value==='probes';
  const response=await api(probes?'/api/probes':'/api/tasks');
  if(!probes)state.tasks=response.tasks;
  $('task-select').replaceChildren(...(response.probes||response.tasks).map(t=>
    option(t.id,`${t.id}${t.profile?` · ${t.profile} · ${t.tier}`:t.kind?` · ${t.kind}`:''}${t.answered?' · recorded':''}`)));
}
function download(name,value){
  const url=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)],{type:'application/json'}));
  const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
$('part').onchange=selectRegistered;
$('start').onclick=guarded(()=>openTask());
$('mode').onchange=guarded(async()=>{
  if(state.viewer){state.viewer.dispose();state.viewer=null;}
  $('review').hidden=true;$('free-review').hidden=true;$('probe-panel').hidden=true;
  state.reviewing=false;state.historical=false;
  state.probe=null;state.session=null;state.observation=null;
  await catalog();message('Select a task and open it.');
});
$('attach').onclick=guarded(()=>act({type:'attach',partId:$('part').value,siteId:$('site').value}));
$('detach').onclick=guarded(()=>act({type:'detach',partId:$('part').value}));
$('audit').onclick=guarded(()=>act({type:'audit',partId:$('part').value}));
$('error-yes').onclick=guarded(()=>act({type:'diagnose',avoidableError:true}));
$('error-no').onclick=guarded(()=>act({type:'diagnose',avoidableError:false}));
$('finish').onclick=guarded(()=>act({type:'finish'}));
$('inspect').onclick=guarded(async()=>{
  if(state.session)await act({type:'inspect',view:$('view').value});
  else{
    const selected=$('probe-answer').value;
    await api(`/api/probes/${state.probeId}/actions`,{requestId:crypto.randomUUID(),revision:state.probe.revision,
      action:{type:'inspect',view:$('view').value}});
    await loadProbe(await api(`/api/probes/${state.probeId}`));$('probe-answer').value=selected;
    message('New view recorded. Previous views remain available.');
  }
});
$('probe-form').onsubmit=e=>{e.preventDefault();guarded(async()=>{
  const key=state.probe.kind==='next-action'?'choice':'firstConflict';
  await api(`/api/probes/${state.probeId}/actions`,{requestId:crypto.randomUUID(),revision:state.probe.revision,
    action:{type:'answer',answer:{[key]:JSON.parse($('probe-answer').value)}}});
  await loadProbe(await api(`/api/probes/${state.probeId}`));message(`Answer frozen for ${state.probeId}.`);
})();};
$('show-view').onclick=guarded(async()=>{
  const key=$('saved-view').value;
  if(key===''){await draw(state.observation.images);state.historical=false;$('saved-label').textContent='Current live view';}
  else{
    const saved=state.observation.inspectionHistory[+key];await draw(saved.images);state.historical=true;
    $('saved-label').textContent=`Saved ${saved.view} · revision ${saved.atRevision} · return to live view to act`;
  }
});
$('replay').onchange=guarded(async()=>{
  const n=+$('replay').value;await populate((await api(`/api/sessions/${state.session}/frame/${n}`)).observation);
  state.historical=true;state.reviewing=true;$('frame-label').textContent=`${n} / ${state.frames.length-1} · ${state.frames[n].code}`;
  state.viewer?.frame(n);
});
$('open-3d').onclick=guarded(async()=>{
  if(state.viewer)return;
  const {makeViewer}=await import('/review.js');
  const data=await api(`/api/sessions/${state.session}/review3d`);
  $('free-review').hidden=false;
  state.viewer=makeViewer($('three-stage'),data);state.viewer.frame(+$('replay').value);
});
$('explode').oninput=()=>{
  state.viewer?.explode(+$('explode').value/100);
  $('explode-note').textContent=+$('explode').value?'EXPLODED REFERENCE ONLY · not an executable assembly':'Original source poses';
};
$('export').onclick=guarded(async()=>download(`brickplan-${state.session}.json`,await api(`/api/sessions/${state.session}/export`)));
$('export-feedback').onclick=()=>download(`brickplan-review-${state.session}.json`,{
  schema:'brickplan-review/2.0',sessionId:state.session,frame:+$('replay').value,
  track:state.observation.track,view:state.observation.view,note:$('feedback').value});
guarded(async()=>{
  const info=await api('/api/tasks');state.study=info.study;
  $('track').textContent=`${info.track} · ${info.study?'study':'practice'}`;
  const query=new URLSearchParams(location.search);
  if(query.has('probe'))$('mode').value='probes';
  await catalog();
  if(query.has('probe')){$('task-select').value=query.get('probe');await openTask();}
  else if(query.has('session'))await openTask(query.get('session'));
  else if(!state.study){const challenge=state.tasks.find(t=>t.tier==='D4');if(challenge)$('task-select').value=challenge.id;await openTask();}
  else message('Study ready. Select an assignment and open it to begin.');
})();
