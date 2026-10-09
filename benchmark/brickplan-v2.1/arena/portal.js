const $=id=>document.getElementById(id);
let lang=localStorage.getItem('brickplan-lang')||'zh',bank,models,selected=null,preview=null,page=0,run=null,stepIndex=0,loading=0,timer=null;
const t=(zh,en)=>lang==='zh'?zh:en, tr=v=>v?.[lang]||v?.en||v||'';
const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const action=a=>a?.type==='attach'?`${t('安装','Attach')} ${a.partId} → ${a.siteId}`:a?.type==='detach'?`${t('拆卸','Detach')} ${a.partId}`:a?.type==='audit'?`${t('离架检修','Audit')} ${a.partId}`:JSON.stringify(a);
const category=id=>bank.taxonomy.find(c=>c.id===id);
function toast(text){$('status').textContent=text;}
async function api(path,payload){
  const r=await fetch(path,payload===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  const data=await r.json();if(!r.ok)throw Error(data.error||r.status);return data;
}
function safe(fn){return async(...args)=>{try{await fn(...args);}catch(e){toast(e.message);}};}
function localize(){
  document.documentElement.lang=lang;
  document.querySelectorAll('[data-zh]').forEach(e=>e.textContent=e.dataset[lang]);
  $('language').textContent=lang==='zh'?'English':'中文';
}
function options(id,values,all){
  const current=$(id).value;
  $(id).innerHTML=`<option value="">${esc(all)}</option>`+values.map(([v,l])=>`<option value="${esc(v)}">${esc(l)}</option>`).join('');
  if([...$(id).options].some(o=>o.value===current))$(id).value=current;
}
function setup(){
  localize();
  $('census').innerHTML=[[bank.counts.episodes,t('交互任务','episodes')],[bank.counts.probes,t('诊断问题','probes')],[bank.counts.sources,t('来源套装','source kits')],[bank.counts.pairs,t('配对对照','paired controls')]]
    .map(([n,l])=>`<div><strong>${n}</strong><span>${l}</span></div>`).join('');
  $('taxonomy').innerHTML=bank.taxonomy.map(c=>`<button class="type-card" data-category="${c.id}"><span class="number">${c.number} / ${c.id.toUpperCase()}</span><span class="count">${c.count} Q</span><h3>${esc(tr(c.name))}</h3><p>${esc(tr(c.question))}</p></button>`).join('');
  document.querySelectorAll('[data-category]').forEach(b=>b.onclick=()=>{$('filter-category').value=b.dataset.category;page=0;list();$('questions').scrollIntoView({behavior:'smooth'});});
  options('filter-category',bank.taxonomy.map(c=>[c.id,tr(c.name)]),t('全部题型','All families'));
  options('filter-source',[...new Set(bank.questions.map(q=>q.source))].sort().map(x=>[x,`LEGO ${x}`]),t('全部来源','All sources'));
  options('filter-split',[['development',t('开发来源','Development')],['heldout-source',t('新增来源','New source')]],t('全部划分','All splits'));
  options('filter-tier',[['D1','D1 · 1–8'],['D2','D2 · 9–16'],['D3','D3 · 17–24'],['D4','D4 · 25+']],t('操作长度','Operation length'));
  $('length-notice').textContent=tr(bank.lengthNotice);
  list();
}
function filtered(){
  const search=$('search').value.trim().toLowerCase();
  return bank.questions.filter(q=>
    (!$('filter-category').value||q.category===$('filter-category').value)&&
    (!$('filter-source').value||q.source===$('filter-source').value)&&
    (!$('filter-split').value||q.split===$('filter-split').value)&&
    (!$('filter-tier').value||q.tier===$('filter-tier').value)&&
    (!search||[q.id,q.stableId,q.source,q.kind].some(s=>s.toLowerCase().includes(search))));
}
function list(){
  const all=filtered(),pages=Math.max(1,Math.ceil(all.length/12));page=Math.min(page,pages-1);
  $('results-count').textContent=`${all.length} ${t('道题目','questions')}`;
  $('question-list').innerHTML=all.slice(page*12,(page+1)*12).map(q=>`<button class="question-row ${selected?.id===q.id?'active':''}" data-question="${q.id}"><span class="qid">${q.id} · ${q.form==='episode'?'INTERACTIVE':'DIAGNOSTIC'}</span><strong>${esc(tr(category(q.category).name))}</strong><small>LEGO ${q.source} · ${q.tier} / ${q.lengthBin} · ${q.split}</small></button>`).join('')||`<p class="empty">${t('没有匹配题目','No matching questions')}</p>`;
  document.querySelectorAll('[data-question]').forEach(b=>b.onclick=safe(async()=>{history.replaceState(null,'',`#q=${b.dataset.question}`);await choose(b.dataset.question);}));
  $('page-number').textContent=`${page+1} / ${pages}`;$('prev').disabled=page===0;$('next').disabled=page===pages-1;
  document.querySelectorAll('[data-category]').forEach(b=>b.classList.toggle('active',b.dataset.category===$('filter-category').value));
}
async function paint(canvas,raster){
  if(!raster)return;
  const response=await fetch(raster.url||`data:${raster.mime};base64,${raster.base64}`);
  const bitmap=await createImageBitmap(await response.blob());
  canvas.width=bitmap.width;canvas.height=bitmap.height;canvas.getContext('2d').drawImage(bitmap,0,0);bitmap.close();
  canvas.onclick=()=>zoom(canvas);
}
function zoom(source){
  const c=$('zoom-canvas');c.width=source.width;c.height=source.height;c.getContext('2d').drawImage(source,0,0);
  $('zoom-label').textContent=`${source.width} × ${source.height} px · ${t('原始渲染','Native render')}`;
  $('zoom-dialog').showModal();zoomFit();
}
function zoomFit(){const c=$('zoom-canvas'),area=document.querySelector('.zoom-scroll');const ratio=Math.min(area.clientWidth/c.width,area.clientHeight/c.height);c.style.width=`${c.width*ratio}px`;c.style.height=`${c.height*ratio}px`;}
$('zoom-fit').onclick=zoomFit;
$('zoom-native').onclick=()=>{const c=$('zoom-canvas');c.style.width=`${c.width}px`;c.style.height=`${c.height}px`;};
$('zoom-close').onclick=()=>$('zoom-dialog').close();
function rasters(images,prefix,keys=['current','target']){
  const names={current:t('当前结构','Current assembly'),target:t('目标结构','Target assembly'),rack:t('暂存架零件','Rack pieces'),siteReference:t('原始位置参考','Original site reference'),catalog:t('零件 / 位置目录','Piece / site catalogue')};
  return `<div class="raster-grid">${keys.filter(k=>images?.[k]).map(k=>`<figure class="raster ${k==='rack'?'wide':''}"><figcaption>${names[k]}<small>${images[k].width} px ↗</small></figcaption><canvas id="${prefix}-${k}" aria-label="${names[k]}"></canvas></figure>`).join('')}</div>`;
}
async function paintSet(images,prefix,keys=Object.keys(images||{})){for(const k of keys){const c=$(`${prefix}-${k}`);if(c)await paint(c,images[k]);}}
async function choose(id){
  const token=++loading;selected=bank.questions.find(q=>q.id===id);if(!selected)return;
  const index=filtered().findIndex(q=>q.id===id);if(index>=0)page=Math.floor(index/12);
  list();toast(t('正在读取高清题面…','Loading high-resolution question…'));
  const data=await api(`/api/preview/${id}`);if(token!==loading)return;
  preview=data;await detail();toast('');
}
async function detail(){
  const q=selected,c=category(q.category),o=preview.observation,episode=q.form==='episode';
  const prompt=lang==='zh'?episode
    ?'请在操作预算内，将当前结构变为目标结构，并完成全部离架检修工单。每次提交一个动作；完成后点击“结束任务”。'
    :preview.candidates?(q.category==='repair'?'参考错误前检查点及执行历史，选择一个动作，使回到原最优路径的非终点状态所需操作最少。只到达目标不算恢复。':'从下列合法候选动作中选择一个，使完成目标和全部工单所需的总操作最少。')
      :'从当前状态出发，逐步检查下列序列。请指出第一个非法操作的序号（从 1 开始）；如果全部可执行，选择“全部合法”。'
    :preview.question;
  $('question-detail').innerHTML=`
    <div class="detail-head"><div><p class="eyebrow">${q.id} / ${episode?'INTERACTIVE EPISODE':'DIAGNOSTIC QUESTION'}</p><h2>${esc(tr(c.name))}</h2></div><div class="tags"><span class="tag">${q.tier} · ${q.lengthBin}</span><span class="tag">LEGO ${q.source}</span><span class="tag">${q.split}</span></div></div>
    <p class="stable-id">${esc(q.stableId)} · ${esc(q.kind)}</p><p class="question-prompt">${esc(prompt)}</p>
    <dl class="contract"><div><dt>${t('给定信息','GIVEN')}</dt><dd>${esc(tr(c.given))}</dd></div><div><dt>${t('答案格式','ANSWER FORMAT')}</dt><dd>${esc(tr(c.answer))}</dd></div><div><dt>${t('如何评分','SCORING')}</dt><dd>${esc(tr(c.score))}</dd></div></dl>
    <div class="actions"><a class="primary button" href="/play?${episode?'task':'probe'}=${q.id}">${t('开始作答 →','Try this question →')}</a><button id="copy-link">${t('复制题目链接','Copy question link')}</button></div>
    ${rasters(o.images,'question')}
    <div class="work-orders">${t('暂存架','Rack')}: ${o.rack.occupiedHolders} / ${o.rack.capacity} · ${t('操作预算','Action budget')}: ${o.actionBudget} · ${t('视角预算','View budget')}: ${o.remainingViews}<br>${o.workOrders.length?o.workOrders.map(w=>`${w.completed?'✓':'○'} ${w.partId} · ${w.completed?t('检修完成','audit done'):t('待离架检修','off-assembly audit pending')}`).join('<br>'):t('无检修工单','No inspection work orders')}</div>
    ${preview.candidates?`<h3>${t('候选动作','Candidate actions')}</h3><ol class="plan">${preview.candidates.map(a=>`<li>${esc(action(a))}</li>`).join('')}</ol>`:''}
    ${preview.proposedPlan?`<h3>${t('待检查的操作序列','Proposed sequence')}</h3><ol class="plan">${preview.proposedPlan.map(a=>`<li>${esc(action(a))}</li>`).join('')}</ol>`:''}
    ${preview.repairContext?`<section class="checkpoint"><h3>${t('错误前检查点与已执行历史','Pre-error checkpoint & executed history')}</h3><p class="note">${t('错误后额外执行步数','Lag after error')}: ${preview.repairContext.lagAfterError}</p>${rasters(preview.repairContext.checkpointObservation.images,'checkpoint',['current'])}<ol class="plan">${preview.repairContext.executedHistory.map(a=>`<li>${esc(action(a))}</li>`).join('')}</ol></section>`:''}
    <details><summary>${t('查看暂存架、位置参考与完整零件目录','Rack, site reference and full piece catalogue')}</summary>${rasters(o.images,'reference',['rack','siteReference','catalog'])}</details>
    <details><summary>${t('作答规则与 ID 对应','Rules and registered IDs')}</summary><p>${t('每个 P 零件只能放回它对应的 S 位置。F 零件为固定底座，不能移动。拆下的每个零件占用一个暂存位；检修仅能在拆下后进行。非法操作消耗一次操作预算。','Each P piece fits its registered S site. F pieces form a fixed base. Every detached piece uses one holder. Audit requires detachment. Rejected operations consume one action.')}</p><pre>${esc(JSON.stringify(o.registration,null,2))}</pre></details>
    ${episode?`<div class="model-launch"><h3>${t('让模型来做这道题','Let a model attempt this episode')}</h3><div class="actions"><select id="model-provider" aria-label="Model provider">${models.providers.map(p=>`<option value="${p.id}" ${p.available?'':'disabled'}>${esc(p.name)}${p.available?'':t(' · 未配置',' · unavailable')}</option>`).join('')}</select><label>${t('最多调用','Call limit')} <input id="model-budget" type="number" value="4" min="1" max="32"></label><button id="create-run">${t('创建模型任务','Create model run')}</button></div><p class="note">${t('创建后可单步运行或连续运行；本地模型不产生 API 费用。','After creation, run one step or the remaining budget. Local inference has no API charge.')}</p></div>`:`<p class="note">${t('单题诊断在作答后显示答案解析；模型实时交互在交互任务中体验。','Diagnostic answer review unlocks after submission. Live model interaction is available on interactive episodes.')}</p>`}`;
  $('copy-link').onclick=safe(async()=>{await navigator.clipboard.writeText(`${location.origin}/#q=${q.id}`);toast(t('题目链接已复制','Question link copied'));});
  if(episode)$('create-run').onclick=safe(async()=>{
    $('create-run').disabled=true;toast(t('正在创建模型任务…','Creating model run…'));
    try{run=await api('/api/model-runs',{taskId:q.id,provider:$('model-provider').value,maxCalls:+$('model-budget').value});location.hash=`case=${run.id}`;}
    finally{if($('create-run'))$('create-run').disabled=false;}
  });
  await paintSet(o.images,'question');await paintSet(o.images,'reference');
  if(preview.repairContext)await paintSet(preview.repairContext.checkpointObservation.images,'checkpoint');
}
async function modelList(){
  models=await api('/api/models');
  $('case-select').innerHTML=[...models.cases,...models.runs.map(r=>({id:r.id,title:`${r.taskId} · ${r.model} · ${r.status}`}))].map(r=>`<option value="${r.id}">${esc(r.title)}</option>`).join('');
}
async function loadRun(id){
  if(!id)return;
  run=await api(`/api/model-runs/${id}`);run.displayId=id;
  stepIndex=Math.max(0,run.steps.length-1);await renderRun();
  $('case-select').value=id;
  clearTimeout(timer);
  if(['running','stopping'].includes(run.status))timer=setTimeout(()=>safe(poll)(),1500);
}
async function poll(){
  const before=run?.steps.length,last=run?.steps.at(-1)?.status,id=run?.displayId||run?.id;if(!id)return;
  const next=await api(`/api/model-runs/${id}`);next.displayId=id;run=next;
  if(next.steps.length!==before)stepIndex=next.steps.length-1;
  const changed=next.steps.length!==before||next.steps.at(-1)?.status!==last||!['running','stopping'].includes(next.status);
  if(changed)await renderRun();
  if(['running','stopping'].includes(run.status))timer=setTimeout(()=>safe(poll)(),1500);
}
async function renderRun(){
  const recorded=run.displayId==='case-local',done=run.steps.filter(s=>s.status==='executed').length;
  $('run-summary').innerHTML=`<strong>${esc(run.model)} · ${esc(run.status)}</strong>${esc(run.stableTaskId)} · ${run.track} · ${done} / ${run.maxCalls} ${t('次调用','calls')} · temperature ${run.temperature}<br>${run.score?`${t('完成','Completed')}: ${run.score.success?'✓':'✗'} · ${t('操作数','Operations')}: ${run.score.operations} · `:''}${esc(run.stopReason||t('可点击运行一步，观察模型反馈。','Run one step to observe the response.'))}<br><span class="mono">${esc(run.createdAt)}${run.modelWeightsSHA256?` · weights ${run.modelWeightsSHA256.slice(0,16)}`:''}</span>`;
  $('run-controls').hidden=false;
  for(const id of ['model-step','model-run'])$(id).disabled=recorded||run.status!=='paused';
  $('model-stop').disabled=recorded||!['running','paused'].includes(run.status);
  $('run-review').hidden=recorded||!run.score;
  $('run-review').href=`/play?session=${run.sessionId}`;
  $('timeline').innerHTML=run.steps.map((s,i)=>`<button class="step-button ${i===stepIndex?'active':''}" data-step="${i}">${String(i+1).padStart(2,'0')} · ${esc(s.feedback?.code||s.status)}<small>${s.latencySeconds?`${s.latencySeconds}s · `:''}${s.usage?.outputTokens??'—'} output tokens</small></button>`).join('')||`<p class="note">${t('还没有模型调用。点击“运行一步”开始。','No model call yet. Select “One step” to start.')}</p>`;
  document.querySelectorAll('[data-step]').forEach(b=>b.onclick=safe(async()=>{stepIndex=+b.dataset.step;await renderRun();}));
  const s=run.steps[stepIndex],obs=s?.input.observation||run.initialObservation;
  $('step-detail').innerHTML=`<div class="step-card"><p class="eyebrow">${s?`CALL ${s.index} / ${run.maxCalls}`:'INITIAL OBSERVATION'}</p><h3>${t('模型收到的当前状态与目标','Current state and target received by the model')}</h3>${rasters(obs.images,'model')}
    ${s?`<h3>${t('原始回答','Raw model response')}</h3><pre class="raw-output">${esc(s.rawOutput??t('推理中…','Inference in progress…'))}</pre>
    ${s.explanation?`<p>${esc(s.explanation)}</p>`:''}<h3>${t('解析动作与执行反馈','Parsed action & executor feedback')}</h3><div class="feedback">${esc(JSON.stringify({action:s.action||null,feedback:s.feedback||null,...(s.parseError?{parseError:s.parseError}:{})},null,2))}</div>
    ${s.after?`<h3 style="margin-top:24px">${t('执行后的状态','State after execution')}</h3>${rasters(s.after.images,'after',['current'])}`:''}
    <p class="note">${t('延迟','Latency')}: ${s.latencySeconds??'—'}s · input ${s.usage?.inputTokens??'—'} / output ${s.usage?.outputTokens??'—'} tokens · ${t('费用','Cost')}: ${s.usage?.costUSD===0?'$0 local':t('未报告','not reported')}</p>
    <details><summary>${t('完整公开输入与模型预处理','Full public input & model preprocessing')}</summary><pre>${esc(JSON.stringify({systemPrompt:run.systemPrompt,input:s.input,formattedPrompt:s.formattedPrompt,preprocessing:s.preprocessing},null,2))}</pre>${rasters(obs.images,'model-extra',['rack','siteReference','catalog'])}</details>`:`<p class="note">${t('模型只收到公开图像、ID、资源约束和历史反馈。','The model receives only public images, IDs, resource constraints and past feedback.')}</p>`}</div>`;
  await paintSet(obs.images,'model');if(s?.after)await paintSet(s.after.images,'after');
  if(s)await paintSet(obs.images,'model-extra');
  toast('');
}
function download(name,data){
  const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
async function route(){
  const hash=location.hash.slice(1),isCase=hash.startsWith('case'),release=hash==='release';
  $('explore-page').hidden=isCase||release;$('case-page').hidden=!isCase;$('release-page').hidden=!release;
  clearTimeout(timer);
  if(isCase){await modelList();const id=hash.split('=')[1]||models.cases[0]?.id||models.runs.at(-1)?.id;await loadRun(id);}
  else if(hash.startsWith('q=')){await choose(hash.slice(2));$('questions').scrollIntoView();}
  else if(hash==='questions')$('questions').scrollIntoView();
  else window.scrollTo(0,0);
}
$('load-case').onclick=safe(async()=>{location.hash=`case=${$('case-select').value}`;await loadRun($('case-select').value);});
for(const mode of ['step','run','stop'])$(`model-${mode}`).onclick=safe(async()=>{
  for(const id of ['model-step','model-run','model-stop'])$(id).disabled=true;
  const id=run.id;await api(`/api/model-runs/${id}/${mode}`,{});await loadRun(id);
});
$('export-run').onclick=()=>download(`brickplan-model-${run.id}.json`,run);
for(const id of ['filter-category','filter-source','filter-split','filter-tier'])$(id).onchange=()=>{page=0;list();};
$('search').oninput=()=>{page=0;list();};
$('reset-filters').onclick=()=>{for(const id of ['search','filter-category','filter-source','filter-split','filter-tier'])$(id).value='';page=0;list();};
$('prev').onclick=()=>{page--;list();};$('next').onclick=()=>{page++;list();};
$('language').onclick=safe(async()=>{lang=lang==='zh'?'en':'zh';localStorage.setItem('brickplan-lang',lang);setup();if(preview)await detail();if(run)await renderRun();});
window.onhashchange=safe(route);
safe(async()=>{
  localize();toast(t('载入题库…','Loading question bank…'));
  bank=await api('/api/catalogue');await modelList();setup();
  const hero=bank.questions.find(q=>q.stableId==='kart-deck-08')||bank.questions.find(q=>q.category==='resource');
  await choose(hero.id);
  await paint($('hero-canvas'),preview.observation.images.current);
  $('hero-title').textContent=`${hero.id} / LEGO ${hero.source} / ${hero.profile}`;
  await route();toast('');
})();
