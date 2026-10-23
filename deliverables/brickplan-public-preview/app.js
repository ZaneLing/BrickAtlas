'use strict';
const $ = s => document.querySelector(s);
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pretty = v => esc(JSON.stringify(v, null, 2));
const number = v => Number(v).toLocaleString('en-US');
const modeName = m => m === 'static' ? '静态修复' : '动态拼装';
const viewName = {isometric:'斜视', top:'俯视', rear:'背面'};
function partDescription(value) {
  return String(value).replace(/颜色#1e5aa8/gi,'蓝色').replace(/颜色#f4f4f4/gi,'白色')
    .replace(/颜色#635f52/gi,'深灰色').replace(/11477零件/g,'2×1弧面砖（11477）')
    .replace(/54200零件/g,'1×1小斜坡砖（54200）').replace(/2420零件/g,'2×2转角薄板（2420）');
}
const featured = ['Q084','Q038','Q057','Q039'];
const state = {rows:[], filtered:[], page:0, selected:null, sample:null, input:null, reference:null,
  tab:'input', stage:0, view:'isometric', request:0, packetRequest:0, pageSize:10, manual:false, pageName:'browse'};
const cache = new Map();
async function load(path) {
  if (!cache.has(path)) cache.set(path, fetch(path).then(r => {if (!r.ok) throw Error(`无法读取 ${path}`); return r.json();}));
  return cache.get(path);
}
function page(name) {
  state.pageName = name;
  for (const p of document.querySelectorAll('.page')) p.hidden = p.id !== name;
  for (const b of document.querySelectorAll('[data-page]')) b.classList.toggle('active', b.dataset.page === name);
  history.replaceState(null, '', '#' + name + (name === 'browse' && state.sample ? '/' + state.sample.id : ''));
}
function figure(record, caption='', labels=null, extra='') {
  if (!record) return '';
  return `<figure class="figure-box ${extra}">${labels ? `<div class="scene-labels"><span>${esc(labels[0])}</span><span>${esc(labels[1])}</span></div>` : ''}<img src="${esc(record.file)}" alt="${esc(caption)}" width="${record.width}" height="${record.height}" loading="lazy" data-zoom><figcaption>${esc(caption)}</figcaption></figure>`;
}
function refreshRows(reset=true) {
  if (reset) state.page = 0;
  const query = $('#search').value.trim().toLowerCase();
  state.filtered = state.rows.filter(r => ($('#coverage').value === 'all' || r.sample)
    && (!$('#mode').value || r.mode === $('#mode').value)
    && (!$('#bank').value || r.bank === $('#bank').value)
    && (!$('#level').value || r.level === $('#level').value)
    && (!query || [r.id,r.sample,r.title,r.familyName,r.model,r.source].join(' ').toLowerCase().includes(query)));
  const pages = Math.max(1, Math.ceil(state.filtered.length / state.pageSize));
  state.page = Math.max(0, Math.min(pages - 1, state.page));
  $('#result-count').textContent = `${number(state.filtered.length)} 条结果 · 类别是审题标签，不是给模型的错误提示`;
  $('#rows').innerHTML = state.filtered.slice(state.page * state.pageSize, (state.page+1) * state.pageSize).map(r =>
    `<button class="dataset-row ${state.selected === r.id ? 'selected' : ''}" data-case="${esc(r.id)}"><span class="row-title">${esc(r.title)}</span><span class="row-meta"><span>${r.mode === 'static' ? '静态' : '动态'} · ${esc(r.level)}</span><span>${esc(r.familyName)}</span><span class="row-code">${esc(r.sample || '仅目录')}</span></span></button>`).join('') || '<div class="empty-state">没有匹配的题目。可清空搜索或更换筛选。</div>';
  $('#pagination-label').textContent = `${state.page+1} / ${pages}`;
  $('#previous').disabled = state.page === 0;
  $('#next').disabled = state.page >= pages-1;
}
async function selectRow(row) {
  if (!row) return;
  const request = ++state.request;
  state.selected = row.id; state.sample = null; state.reference = null; state.tab = 'input'; state.stage = 0; state.manual = false;
  refreshRows(false);
  if (!row.sample) {
    const similar = state.rows.find(r => r.sample && r.bank === row.bank && r.mode === row.mode && r.family === row.family && r.level === row.level)
      || state.rows.find(r => r.sample && r.mode === row.mode && r.family === row.family);
    $('#sample-panel').innerHTML = `<div class="metadata-only"><div class="pills"><span class="pill">${modeName(row.mode)}</span><span class="pill neutral">${esc(row.level)} · 暂定</span></div><h2>${esc(row.title)}</h2><div class="callout amber">这道题在当前正式目录中，但本次没有为它导出完整公开图包。下面只显示目录信息，不用其他题的图片代替本题。</div><dl class="record-grid">${Object.entries({'题号':row.id,'类别':row.familyName,'目标件数':row.targetParts,'原始来源组':row.source,'数据分组':row.split,'物件配置':row.model}).map(([k,v])=>`<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>${similar ? `<button data-example="${similar.sample}">查看同类的完整例子 ${similar.sample} →</button>` : ''}</div>`;
    return;
  }
  $('#sample-panel').innerHTML = '<p class="loading">正在读取这道题的原始图包…</p>';
  try {
    const sample = await load(`samples/${row.sample}/sample.json`);
    const input = await load(sample.stages[0].inputFile);
    if (request !== state.request) return;
    state.sample = sample; state.input = input;
    if(state.pageName==='browse') history.replaceState(null, '', '#browse/' + sample.id);
    renderSample();
  } catch(e) { if (request === state.request) $('#sample-panel').innerHTML = `<p class="empty-state">${esc(e.message)}</p>`; }
}
function renderSample() {
  const s = state.sample;
  if (!s) return;
  $('#sample-panel').innerHTML = `<header class="sample-header"><div class="pills"><span class="pill">${modeName(s.mode)}</span><span class="pill neutral">${esc(s.level)} · 难度暂定</span><span class="pill neutral">${esc(s.bank)} · ${s.id}</span></div><h2>${esc(s.title)}</h2><div class="id">${esc(s.caseId)}</div></header><nav class="sample-tabs" aria-label="本题内容">${[['input','模型看到什么'],['output','怎么提交动作'],['answer','正确结果与修复'],['files','数据怎么存']].map(([k,v])=>`<button data-tab="${k}" class="${state.tab===k?'active':''}">${v}</button>`).join('')}</nav><div class="sample-content" id="sample-content"></div>`;
  renderContent();
}
function renderContent() {
  const s=state.sample, content=$('#sample-content'); if (!s || !content) return;
  if (state.tab === 'input') renderInput(content);
  if (state.tab === 'output') renderOutput(content);
  if (state.tab === 'answer') renderAnswer(content);
  if (state.tab === 'files') renderFiles(content);
}
function renderInput(content) {
  const s=state.sample, input=state.input;
  const current=input.images.find(i=>i.role==='current-target' && i.view===state.view) || input.images.find(i=>i.role==='current-target');
  const temporal=input.images.find(i=>i.role==='temporal-pair' && i.view===state.view);
  const inventory=input.images.filter(i=>i.role==='inventory');
  const instruction=s.mode==='static' ? '把左边的当前结构，修成右边本题的目标，然后结束。' : '从当前结构继续，一步步拼到右边的目标；过程中可能发生额外变化。';
  content.innerHTML = `<div class="task-instruction"><span class="step-number">1</span><div><strong>${instruction}</strong><p>每次只装或拆一块。随时查看新画面；允许采用不同的合法顺序。${s.contextLocked?'本题主体已装好且固定，只操作指定局部。':''}</p></div></div><div class="toolbar"><div class="stage-buttons">${s.stages.map((v,i)=>`<button data-stage="${i}" class="${i===state.stage?'active':''}">${esc(v.name)}</button>`).join('')}</div><div class="view-buttons">${Object.entries(viewName).map(([k,v])=>`<button data-view="${k}" class="${state.view===k?'active':''}">${v}</button>`).join('')}</div></div>${figure(current, '实际发给模型的原图。当前与目标同相机、同尺度；点击可看原始分辨率。',['现在是什么样','本题必须达到的 TARGET'])}${temporal ? `<div class="subheading"><h3>操作前后，发生了什么变化？</h3><span>这是另一组时间对照，不是第二个物件</span></div>${figure(temporal, '比较自己上一步之前和现在的画面，核对自己的动作及额外变化。',['上一步之前','现在'])}` : '<p class="micro">开始时还没有上一动作，因此不发送时间对照图。</p>'}<div class="subheading"><h3>全部可操作零件 · ${s.inventoryParts}块</h3><span>包括已装件与备用件；不是实时剩件托盘</span></div><div class="inventory-grid">${inventory.map((r,i)=>figure(r,`零件目录 ${i+1} / ${inventory.length} · 全部页均展示`)).join('')}</div><div class="callout">一轮输入共 <strong>${input.images.length} 张图</strong>：${input.images.filter(i=>i.role==='current-target').length}张当前／目标对照${temporal?'、3张操作前后对照':''}，以及${inventory.length}张零件目录。视角切换只是方便你阅读；模型实际收到图包中全部视角。</div>${s.manual?`<button id="manual-button">${state.manual?'收起这次查看的说明图':'查看一步说明书的真实返回图'}</button><p class="micro">说明书按需查看。这是参考顺序，不能替换本题TARGET。</p>${state.manual?figure(s.manual,`参考说明第${s.manual.step}步 · 只有主动查看才增加这张图`):''}`:'<p class="micro">此题沿用原S／D接口，没有说明书。社区模块与新长流程另有按需说明。</p>'}<div class="download-links"><a href="${esc(s.stages[state.stage].inputFile)}" target="_blank">查看这一轮完整输入 JSON ↗</a><a href="${esc(s.stages[state.stage].inputFile)}" download>下载模型输入 ↓</a></div>`;
}
function handles() {const o=state.input.observation; return o.handles || o.actionHandles || [];}
function renderOutput(content) {
  const s=state.sample;
  content.innerHTML = `<div class="task-instruction"><span class="step-number">2</span><div><strong>模型每轮提交一个可执行动作。</strong><p>整道题可以有多种合法修复路线。位置编号对应一个确定的位置和朝向，编号本身不标正确答案。</p></div></div><div class="output-form"><label>动作<select id="action-kind"><option value="attach">安装一块</option><option value="detach">拆下一块</option><option value="inspect">查看一个零件</option><option value="finish">结束本题</option></select></label><label id="actor-label">零件编号<select id="action-actor">${handles().map(h=>`<option>${esc(h.partId || h.id)}</option>`).join('')}</select></label><label id="candidate-label">安装位置编号<select id="action-candidate"></select></label></div><pre id="action-json" class="code-block compact"></pre><p class="micro">这里的编号来自本题真实输入。选择菜单只演示如何提交，不执行安装、不提交真人答案。某个编号能否安装、是否符合目标，仍需模型观察和执行器检查。</p><div class="comparison-table"><table><thead><tr><th>模型动作</th><th>系统会做什么</th></tr></thead><tbody><tr><td>安装 / 拆除</td><td>检查接点、碰撞与装入／拆出路径；成功才改变结构。</td></tr><tr><td>查看</td><td>返回当前视角、零件或候选预览；有说明书的题可按步骤查看。</td></tr><tr><td>结束</td><td>检查实际结构是否达到本题目标；只说“我拼好了”不会自动成功。</td></tr></tbody></table></div><div class="callout amber"><strong>现在没有要求模型自己回传任意三维坐标。</strong> 公开视觉接口主要使用候选位置。坐标定位需要单独定义单位、朝向和误差，作为另外一组实验。</div><p class="action-explain">S／D的模型回复用外层action字段；社区M／E7直接提交动作对象。两个真实格式都在对应图包中保留，没有在展示页伪装成完全相同的接口。</p>`;
  updateCandidates();
}
function updateCandidates() {
  const id=$('#action-actor')?.value, select=$('#action-candidate'); if(!select) return;
  const h=handles().find(h=>(h.partId||h.id)===id);
  select.innerHTML=(h?.candidates||[]).map(c=>`<option>${esc(c)}</option>`).join('');
  updateAction();
}
function updateAction() {
  const kind=$('#action-kind')?.value; if (!kind) return;
  const a={type:kind};
  $('#actor-label').hidden=kind==='finish'; $('#candidate-label').hidden=kind!=='attach';
  if(kind!=='finish') a.partId=$('#action-actor').value;
  if(kind==='attach') a.candidate=$('#action-candidate').value;
  if(kind==='inspect') a.view='isometric';
  const out=state.sample.bank==='D'?{action:a,unexpectedChange:false}:state.sample.bank==='S'?{action:a}:a;
  $('#action-json').textContent=JSON.stringify(out,null,2);
}
async function renderAnswer(content) {
  const sample=state.sample, request=state.request;
  if (!state.reference) {
    content.innerHTML='<p class="loading">读取独立保存的参考答案…</p>';
    try { const r=await load(sample.referenceFile); if(request!==state.request || state.tab!=='answer') return;state.reference=r; }
    catch(e){if(request===state.request)content.innerHTML=`<p>${esc(e.message)}</p>`;return;}
  }
  const r=state.reference;
  content.innerHTML=`<div class="task-instruction"><span class="step-number">3</span><div><strong>最终结构正确，且每一步操作合法，就算完成。</strong><p>下面是程序已验证的一条参考路线；不是模型实测，不要求逐步照抄，也未证明是最短路线。</p></div></div><div class="callout"><strong>审题答案：</strong>${esc(sample.familyName)}。${esc(sample.familyNote)}</div>${figure(r.final,'参考执行结束后，当前结构与本题TARGET相符。',['参考执行后的当前状态','本题目标'])}${r.strip?`<h3 class="mini-heading">参考过程关键帧</h3><div class="reference-strip"><img src="${esc(r.strip.file)}" alt="程序参考路线关键帧" data-zoom></div><p class="micro">展示抽取的关键帧，不是每一步的完整视频。</p>`:''}${r.events.map(e=>`<h3 class="mini-heading">第${e.number}次后台干扰 · 参考动作第${e.afterStep}步之后</h3>${figure(e.image,`${e.family} · 这是讲解图，不会发送给被测模型。`)}`).join('')}<h3 class="mini-heading">这一条参考路线用了哪些动作？</h3><table class="reference-actions"><thead><tr><th>步</th><th>操作</th><th>模型实际返回格式</th></tr></thead><tbody>${r.actions.map(a=>`<tr><td>${a.step}</td><td>${a.publicAction.type==='attach'?'装上':'拆下'} ${esc(a.publicAction.partId)}<br>${esc(partDescription(a.description))}${a.eventAfterThisAction?'<span class="event-tag">随后发生后台干扰</span>':''}</td><td><code>${esc(JSON.stringify(a.output))}</code></td></tr>`).join('')}<tr><td>结束</td><td>声明完成</td><td><code>${esc(JSON.stringify(r.finish))}</code></td></tr></tbody></table>${r.candidateExample?`<h3 class="mini-heading">安装位置编号具体表示什么？</h3><p class="micro">用参考动作中的一个位置举例，下面是请求查看后返回的真实预览。它不是完整候选列表，也不代表执行过安装。</p><pre class="code-block compact">${pretty(r.candidateExample.request)}</pre>${r.candidateExample.images.map(i=>figure(i,'参考动作所选位置的预览举例')).join('')}`:''}<div class="download-links"><a href="${esc(sample.referenceFile)}" download>下载参考答案文件 ↓</a></div>`;
}
function renderFiles(content) {
  const s=state.sample, o=state.input.observation;
  const visible={task:o.task,mode:s.mode,targetDisplay:o.targetDisplay,actionSchema:o.actionSchema||o.responseSchema,
    firstHandle:handles()[0],imagePages:state.input.images.map(i=>({role:i.role,view:i.view,page:i.page,file:i.file}))};
  content.innerHTML=`<div class="task-instruction"><span class="step-number">4</span><div><strong>模型输入和审题答案，分开保存。</strong><p>本页类别、来源、难度属于浏览目录。给模型的输入不包含错误类别、后台事件、参考动作或目标坐标答案。</p></div></div><dl class="record-grid">${Object.entries({'浏览题号':s.id,'实际题号':s.caseId,'来源组':s.source,'数据分组':s.split,'输入方式':'真实图片 + 任务说明 + 动作接口','回答方式':'每轮一个结构化动作','输入文件':s.stages[state.stage].inputFile,'参考文件':s.referenceFile}).map(([k,v])=>`<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl><h3 class="mini-heading">这一轮输入字段节选</h3><pre class="code-block">${pretty(visible)}</pre><p class="micro">上面省略了其他零件的编号列表与较长系统说明。完整内容可下载；图片用相对路径与SHA256对应，正式请求仍需把图片内容传给视觉模型。</p><div class="download-links"><a href="${esc(s.stages[state.stage].inputFile)}" download>下载完整模型输入 ↓</a><a href="samples/${s.id}/sample.json" download>下载浏览记录 ↓</a><a href="${esc(s.referenceFile)}" download>下载独立参考答案 ↓</a></div>`;
}
async function setStage(index) {
  const request=state.request, packetRequest=++state.packetRequest, s=state.sample; if(!s) return;
  const input=await load(s.stages[index].inputFile);if(request!==state.request || packetRequest!==state.packetRequest)return;
  state.stage=index;state.input=input;state.manual=false;renderContent();
}
async function renderPeers() {
  const peers=await load('references.json');
  $('#peer-list').innerHTML=peers.map(p=>`<article class="peer-card"><div><div class="peer-type">${esc(p.kind)}</div><h3>${esc(p.name)}</h3><p>${esc(p.summary)}</p><dl><dt>怎么存：</dt><dd>${esc(p.storage)}</dd><dt>怎么展示：</dt><dd>${esc(p.display)}</dd><dt>模型怎么答：</dt><dd>${esc(p.output)}</dd></dl>${p.image?`<img src="${esc(p.image)}" alt="${esc(p.imageCaption)}" data-zoom><p class="micro">${esc(p.imageCaption)}</p>`:''}<div class="links">${p.links.map(l=>`<a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.title)} ↗</a>`).join('')}</div></div><pre>${esc(p.fileExample)}</pre></article>`).join('');
}
document.addEventListener('click', async event=>{
  if(event.target.closest('.brand')){event.preventDefault();page('browse');return;}
  const b=event.target.closest('button');
  if(b?.dataset.page){page(b.dataset.page);return;}
  if(b?.dataset.case){selectRow(state.rows.find(r=>r.id===b.dataset.case));return;}
  if(b?.dataset.example){
    page('browse');$('#coverage').value='examples';for(const id of ['search','mode','bank','level'])$('#'+id).value='';
    const r=state.rows.find(r=>r.sample===b.dataset.example);refreshRows();
    state.page=Math.floor(state.filtered.indexOf(r)/state.pageSize);await selectRow(r);return;
  }
  if(b?.dataset.tab){state.tab=b.dataset.tab;renderSample();return;}
  if(b?.dataset.stage!==undefined){await setStage(Number(b.dataset.stage));return;}
  if(b?.dataset.view){state.view=b.dataset.view;renderContent();return;}
  if(b?.id==='manual-button'){state.manual=!state.manual;renderContent();return;}
  if(b?.id==='previous'){state.page--;refreshRows(false);return;}
  if(b?.id==='next'){state.page++;refreshRows(false);return;}
  if(b?.id==='close-zoom'){$('#zoom').close();return;}
  const im=event.target.closest('img[data-zoom]');if(im){$('#zoom img').src=im.src;$('#zoom').showModal();}
});
document.addEventListener('change',e=>{
  if(['coverage','mode','bank','level'].includes(e.target.id))refreshRows();
  if(e.target.id==='action-actor')updateCandidates();
  if(e.target.id==='action-kind'||e.target.id==='action-candidate')updateAction();
});
$('#search').addEventListener('input',()=>refreshRows());
async function init(){
  const parts=location.hash.slice(1).split('/');
  page(['peers','design'].includes(parts[0])?parts[0]:'browse');
  try{
    const [rows,summary]=await Promise.all([load('catalogue.json'),load('summary.json')]);
    state.rows=rows.sort((a,b)=>{
      const ai=featured.indexOf(a.sample),bi=featured.indexOf(b.sample);
      return(ai<0?100:ai)-(bi<0?100:bi)||(a.sample||'zzzz').localeCompare(b.sample||'zzzz');
    });
    $('#total').textContent=number(summary.totalTasks);$('#static-count').textContent=number(summary.taskModes.static);$('#dynamic-count').textContent=number(summary.taskModes.dynamic);
    refreshRows();
    const code=parts[1]||'Q084';
    await selectRow(state.rows.find(r=>r.sample===code)||state.rows.find(r=>r.sample));
    await renderPeers();page(state.pageName);
  }catch(e){$('#sample-panel').innerHTML=`<div class="empty-state">${esc(e.message)}。请从本机预览服务打开此页。</div>`;}
}
init();
