let data,filter='all';
const $=s=>document.querySelector(s);
const labels={'control':'无错误对照','missing':'少件','wrong-color':'错色','extra-layer':'多装一层','offset':'偏移','rotated':'装反／旋转','wrong-part':'错零件'};
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function cards(){
  const rows=data.models.filter(m=>filter==='all'||m.kind===filter);
  $('#count').textContent=`${rows.length} 个物件／任务范围`;
  $('#grid').innerHTML=rows.map(m=>`<button class="card" data-model="${esc(m.id)}" aria-label="查看${esc(m.title)}"><img src="${esc(m.images.full)}" alt="${esc(m.title)}完整成品" loading="lazy"><div class="text"><span class="tag ${m.kind}">${m.kind==='complete'?'从零拼完整物件':'主体已装好 · 补最后一部分'}</span><h3>${esc(m.title)}</h3><p>${m.kind==='complete'?`全部 ${m.parts} 块，都需要装`:`只补 ${m.parts} 块 · 原场景 ${m.sourceParts} 块`}</p><small>${m.kind==='complete'?'新增完整模型 · 原始零件无删减':'已有收尾模块 · 本次重新展示范围'} &nbsp; ↗</small></div></button>`).join('');
  document.querySelectorAll('[data-model]').forEach(b=>b.onclick=()=>{location.hash=b.dataset.model;show(b.dataset.model,true)});
}
function show(id,scroll=false){
  const m=data.models.find(m=>m.id===id);if(!m)return;
  const whole=m.kind==='complete';const el=$('#detail');el.hidden=false;
  el.innerHTML=`<div class="detail-head"><div><p class="eyebrow">${whole?'完整小物件 / COMPLETE OBJECT':'有明确用途的部分 / NAMED COMPLETION'}</p><h2>${esc(m.title)}</h2></div><button id="close-detail">收起详情</button></div><p class="detail-lead">${esc(m.explanation)}</p><div class="panels">
  <figure class="panel"><img src="${m.images.start}" alt="开局实际状态"><figcaption>① 开始时，桌上是什么<small>${whole?'只有白色底板，模型本身还没有装任何一块。':'完整主体保留在这里；本次需要补的零件尚未装上。'}</small></figcaption></figure>
  <figure class="panel"><img src="${m.images.full}" alt="唯一完整目标"><figcaption>② 最后要完成什么<small>${whole?`拼成这整个物件，原文件 ${m.parts} 块全部装好。`:'把缺的这部分补齐，让现有主体成为图中的完整成品。'}</small></figcaption></figure>
  <figure class="panel"><img src="${m.images.highlight}" alt="本次操作范围"><figcaption>③ 这道题只操作哪些<small>${whole?`整个物件，共 ${m.parts} 块；没有隐藏的预装主体。`:`橙色边缘标出本次补装的 ${m.parts} 块。其余主体不需要重建。`}</small></figcaption></figure></div>
  <div class="details-grid"><div><h3>参考拼装过程</h3><div class="stage-controls"><label for="step">看到第几步</label><select id="step">${m.stages.map(s=>`<option value="${s.step}">${s.step===0?'开始，尚未补装':`已装 ${s.step} / ${m.parts} 块`}</option>`).join('')}</select></div><img class="stage-image" id="stage-image" src="${m.images.start}" alt="开始状态"><p class="note">每步只安装一块。这是一条可行路线；其他顺序只要实际能装上、最终一致，也算正确。</p><a href="${m.reference}" download>下载参考步骤（讲解材料，不是模型输入）</a></div>
  <div><h3>题目怎么做</h3><ul><li>输入：当前状态、题目唯一目标、零件目录；说明步骤随时可查看。</li><li>输出：每次装一块、拆一块、查看，或者结束。</li><li>${whole?'动态：从空白底板完成整个小物件，过程中可能发生干扰。':'动态：从已装主体开始补完指定部分，干扰只作用于可操作范围。'}</li><li>静态：给某个阶段的错误状态，修到<strong>该阶段目标</strong>；后续成品仅供参考。</li><li>没有到达干扰位置的运行列“未触发”。正常拼装和修复成绩分开。</li></ul><h3>已有题目类别</h3><div class="families">${Object.entries(m.families).map(([f,n])=>`<span>${esc(labels[f]||f)} ${n}</span>`).join('')}</div><p class="note">正常路线和纳入的错误修复有程序运行证据。还没有本轮真人审查结果，也没有模型测试成绩。</p><div class="source">原文件 ${m.sourceParts} 块；本次操作 ${m.parts} 块；原始零件移除 0 块。<br><a href="${esc(m.source.url)}" target="_blank" rel="noreferrer">查看 LDraw OMR 原始来源 ↗</a><br>作者：${esc(m.source.author)}<br>原始几何未修改；碰撞代理的单三角面修补另有记录。许可与署名保留在原文件。</div></div></div>`;
  if(m.nativeInput){const link=document.createElement('a');link.href=m.nativeInput;link.download='';link.textContent='下载开局真实输入（另含当前／目标三视图和零件图）';link.style.cssText='display:block;margin-top:12px';$('#step').parentElement.parentElement.appendChild(link)}
  $('#step').onchange=e=>{const stage=m.stages.find(s=>s.step===Number(e.target.value));$('#stage-image').src=stage.image;$('#stage-image').alt=`已装 ${stage.step} 块后的实际状态`};
  $('#close-detail').onclick=()=>{el.hidden=true;history.replaceState(null,'',location.pathname);$('#grid').scrollIntoView({block:'start'})};
  if(scroll){el.scrollIntoView({behavior:'smooth',block:'start'});el.focus({preventScroll:true})}
}
fetch('models.json').then(r=>{if(!r.ok)throw Error('读取模型失败');return r.json()}).then(d=>{
  data=d;$('#metrics').innerHTML=`<div><b>${d.wholeCount}</b><span>新增完整小物件</span></div><div><b>${d.moduleCount}</b><span>已有收尾模块</span></div><div><b>0</b><span>删减原始零件</span></div>`;
  cards();if(location.hash)show(decodeURIComponent(location.hash.slice(1)),true);
  document.querySelectorAll('[data-filter]').forEach(b=>b.onclick=()=>{filter=b.dataset.filter;document.querySelectorAll('[data-filter]').forEach(x=>x.classList.toggle('active',x===b));cards()});
}).catch(e=>{$('#grid').textContent='页面读取失败：'+e.message});
window.addEventListener('hashchange',()=>{if(data&&location.hash)show(decodeURIComponent(location.hash.slice(1)),true)});
