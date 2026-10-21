"""Blind human packet using the exact three-image API timing and original guide."""
from hashlib import sha256
from pathlib import Path
import html
import json
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
sys.path.insert(0,str(HERE.parent/'eval'))
from dynamic_v5.episode import BANK,DynamicEpisode,load_case
from dynamic_v5.vision import DynamicVisionRenderer
from vision import images

OUT=BANK/'human-temporal-review'
PRIMARY={'obj-chair':'shifted_piece','obj-city-car':'extra_layer',
         'obj-crane':'wrong_color','obj-table':'early_cover'}


def order(value):
    return sha256(('temporal-human-2026-10-19/'+value).encode()).hexdigest()


def page(reviewer,rows):
    cards=[]
    for number,row in enumerate(sorted(rows,key=lambda r:order(reviewer+r['code'])),1):
        figures=''.join(
            f'<figure><figcaption>{label} · {"斜着看" if rec.get("view")=="isometric" else "从上往下看"}</figcaption>'
            f'<a href="{rec["file"]}" target="_blank"><img src="{rec["file"]}" alt="{label}"></a></figure>'
            for view in ('isometric','top')
            for role,label in (('temporal-pair','左：刚才动作前　→　右：现在'),('target','最终拼完的样子，仅供参照'))
            for rec in row['images'] if rec['role']==role and rec.get('view')==view)
        inventory=next(rec for rec in row['images'] if rec['role']=='inventory')
        first,second,third=row['firstParts']
        cards.append(f'''<section class="case" data-code="{row['code']}"><h2>第 {number} / {len(rows)} 题 · {html.escape(row['objectNameZh'])} <small>（编号 {row['code']}）</small></h2>
<div class="timeline"><div><b>要拼什么</b><br>{html.escape(row['objectNameZh'])}。右侧“最终目标”是全部拼完的样子。</div>
<div><b>刚才动作前</b><br>已经按计划装了零件 {first}、{second}。看对比图的左半边。</div>
<div><b>刚才执行</b><br>要求把零件 <b>{third}</b> 装上去；机器回复“成功”。零件编号可以在下方零件卡片中查。</div>
<div><b>当前状态</b><br>对比图的<b>右半边</b>就是这一步结束后真实看到的积木。请检查 {third} 是否出现，以及其他积木有没有变化。</div></div>
<div class="images">{figures}</div>
<div class="parts"><b>本题零件卡片（直接对照 A 编号，点击图片可放大）</b><a href="{inventory['file']}" target="_blank"><img class="inventory" src="{inventory['file']}" alt="本题零件卡片"></a></div>
<fieldset><legend>现在的积木和刚才要求的安装相比，有异常吗？</legend>
<label><input type="radio" name="changed-{row['code']}" data-field="changed" value="yes"> 有：该装的没出现，或其他积木多了、少了、移位了、变色了</label>
<label><input type="radio" name="changed-{row['code']}" data-field="changed" value="no"> 没有：该装的装上了，其他积木也没变化</label>
<label><input type="radio" name="changed-{row['code']}" data-field="changed" value="unsure"> 无法判断：图片或说明看不清</label></fieldset>
</section>''')
    script='''<script>
const reviewer = '__REVIEWER__';
const storageKey = 'brickplan-temporal-draft-' + reviewer;
const cards = [...document.querySelectorAll('.case')];
function answersNow() {
  return cards.map(card => {
    return {code:card.dataset.code, changed:card.querySelector('[data-field="changed"]:checked')?.value || ''};
  });
}
function setStatus(message, kind='') {
  const box = document.getElementById('status');
  box.textContent = message;
  box.dataset.kind = kind;
}
function updateProgress() {
  const count = answersNow().filter(answer => answer.changed).length;
  document.getElementById('progress').textContent = '已判断 ' + count + ' / ' + cards.length + ' 题';
  const next = cards.find(card => !card.querySelector('[data-field="changed"]:checked'));
  document.getElementById('remaining').textContent = next
    ? '还需完成 ' + (cards.length - count) + ' 题；下一题是第 ' + (cards.indexOf(next) + 1) + ' 题。全部选完才能提交。'
    : '全部 12 题已完成，请点页面底部“提交回答”。';
}
function saveDraft() {
  try { localStorage.setItem(storageKey, JSON.stringify(answersNow())); }
  catch (_) { setStatus('浏览器无法保存草稿，请保持页面打开直到提交。', 'error'); }
  updateProgress();
}
function restoreDraft() {
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || '[]');
    for (const answer of saved) {
      const card = cards.find(item => item.dataset.code === answer.code);
      if (!card) continue;
      const selected = card.querySelector('[data-field="changed"][value="' + answer.changed + '"]');
      if (selected) selected.checked = true;
    }
  } catch (_) { /* Corrupt local draft does not block a new response. */ }
  updateProgress();
}
async function submitReview() {
  const answers = answersNow();
  const missing = answers.find(answer => !answer.changed);
  if (missing) {
    document.querySelector('.case[data-code="' + missing.code + '"]').scrollIntoView({behavior:'smooth'});
    const completed = answers.filter(answer => answer.changed).length;
    setStatus('已答 ' + completed + ' / ' + cards.length + ' 题；已跳到下一道未答题。完成全部题目后再提交。', 'error');
    return;
  }
  if (location.protocol === 'file:') {
    setStatus('请使用分配给你的网页链接打开，而不是直接打开本地 HTML 文件。', 'error');
    return;
  }
  const token = location.pathname.split('/').filter(Boolean).pop();
  const buttons = [...document.querySelectorAll('.submit-button')];
  buttons.forEach(button => button.disabled = true);
  setStatus('正在提交，请稍候…');
  try {
    const response = await fetch('/api/submit/' + encodeURIComponent(token), {
      method:'POST', headers:{'Content-Type':'application/json'},
      body:JSON.stringify({reviewer, answers})
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.message || '提交失败');
    saveDraft();
    setStatus('提交成功。你的回答已保存在研究者的电脑上。若要修改，编辑后再点提交即可。', 'success');
  } catch (error) {
    setStatus('提交未成功：' + error.message + '。草稿仍保存在本浏览器。', 'error');
  } finally { buttons.forEach(button => button.disabled = false); }
}
for (const card of cards) {
  card.addEventListener('input', saveDraft);
  card.addEventListener('change', saveDraft);
}
restoreDraft();
</script>'''.replace('__REVIEWER__',reviewer)
    html_text=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><base href="/"><meta name="viewport" content="width=device-width,initial-scale=1"><title>动态积木接口盲审 {reviewer}</title>
<style>body{{font-family:-apple-system,BlinkMacSystemFont,sans-serif;max-width:1600px;margin:auto;padding:24px;background:#f4f6f8;color:#182734;line-height:1.5}}.case{{background:white;border:1px solid #cad3db;border-radius:10px;padding:20px;margin:24px 0}}.timeline{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:12px 0 20px}}.timeline>div{{padding:12px;background:#eef5f8;border-radius:7px}}.images{{display:grid;grid-template-columns:2fr 1fr;gap:10px}}figure{{margin:0}}img{{width:100%;border:1px solid #d1d9df}}figcaption{{font-weight:700;padding:6px 0}}.parts{{margin-top:16px}}.parts img{{display:block;margin-top:8px}}fieldset{{border:2px solid #9eb8c7;border-radius:8px;margin-top:18px}}legend{{font-weight:700;font-size:18px}}fieldset label{{display:block;padding:8px;cursor:pointer;font-size:17px}}input[type=radio]{{width:18px;height:18px;vertical-align:middle;margin-right:7px}}button{{font-size:16px;padding:6px}}.inventory{{width:100%;max-width:320px}}.toolbar{{position:sticky;top:0;z-index:2;background:#e7f0f4;padding:12px;border:1px solid #b3cbd5;display:flex;align-items:center;gap:18px;flex-wrap:wrap}}.submit-button{{background:#176384;color:white;border:0;border-radius:5px;padding:9px 18px;cursor:pointer}}.submit-button:disabled{{opacity:.55}}#status[data-kind="error"]{{color:#a52716}}#status[data-kind="success"]{{color:#146136}}@media(max-width:850px){{.images{{grid-template-columns:1fr}}.timeline{{grid-template-columns:1fr 1fr}}}}</style>
<h1>积木拼装变化判断 · {reviewer[-1]}</h1><p><b>你要做的事：</b>共 {len(rows)} 题，每题选一个答案，<b>全部选完后才能提交</b>。题目编号打乱，所以 T005 后面可能是 T010；看“第几题／共几题”往下做即可。每题比较“动作前”和“现在”，判断刚才要求安装的零件是否真的装上、其他积木是否意外变化。每一步只要求安装一块积木；如果左右一样，而刚才本应装上一块，也选“有异常”。不用写字。</p>
<p><b>怎么看：</b>并排图的左边＝刚才装零件前；右边＝装完后真实的当前状态。旁边的“最终目标”＝全部零件装完后应该长什么样，只作参照；现在还没拼完是正常的。斜视和俯视是同一状态的两个角度，点击可放大。</p>
<div class="toolbar"><strong id="progress">已判断 0 / {len(rows)} 题</strong><span id="remaining">全部选完才能提交。</span><span id="status" role="status" aria-live="polite"></span></div>
{''.join(cards)}<button type="button" class="submit-button" onclick="submitReview()">提交回答</button>
{script}</html>'''
    (OUT/f'{reviewer}.html').write_text(html_text)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    cases={c['id']:c for c in json.loads((BANK/'cases.private.json').read_text())['cases']}
    selection=[]
    for model,kind in PRIMARY.items():
        selection.extend([f'{model}--t3--control',f'{model}--t3--removed_piece',f'{model}--t3--{kind}'])
    temporal={r['caseId']:r for r in json.loads((BANK/'temporal-interface-audit.json').read_text())['rows']}
    assert all(temporal[c]['category']=='candidate-for-human-validation' for c in selection if c.endswith(tuple(PRIMARY.values())))
    rows=[]
    for i,case_id in enumerate(sorted(selection,key=order),1):
        case=cases[case_id]
        cert,_=load_case(case_id)
        ep=DynamicEpisode(cert,case)
        renderer=DynamicVisionRenderer(ep.cert,ep.runtime)
        renderer.catalog_in_context=True
        witness=json.loads((BANK/'models'/case['modelId']/'evidence.json').read_text())['buildWitness']
        previous=None;last=None
        for action in witness[:3]:
            previous=ep.assignments()
            last=dict(type='attach',partId=ep.alias[action['partId']],candidate=ep.pose(action['candidate']))
            assert ep.step(last)['code']=='OK'
        records=images(ep,renderer,OUT,views=('isometric','top'),previous_state=previous,paired_layout=True)
        code=f'T{i:03}'
        evidence=json.loads((BANK/'models'/case['modelId']/'evidence.json').read_text())
        rows.append(dict(code=code,caseId=case_id,kind=case['kind'],
                         category=temporal[case_id]['category'],modelId=case['modelId'],
                         objectNameZh=evidence['objectNameZh'],
                         firstParts=[ep.alias[a['partId']] for a in witness[:3]],images=records))
        print(code,case_id,flush=True)
    for reviewer in ('reviewer-A','reviewer-B','reviewer-C'):
        page(reviewer,rows)
    answer=dict(schema='brickplan-dynamic-temporal-human-review/1',cases=len(rows),
                instruction='Keep private until all answers are collected.',
                rows=[{k:r[k] for k in ('code','caseId','kind','category','modelId')} for r in rows])
    (BANK/'human-temporal-answer-key.private.json').write_text(json.dumps(answer,ensure_ascii=False,indent=2)+'\n')
    (OUT/'README.zh-CN.md').write_text('''# 动态接口盲审\n\n从项目根目录启动提交服务：\n\n```bash\nbenchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/dynamic_v5/review_server.py --host 127.0.0.1 --port 8765\n```\n\n服务会打印 A、B、C 三个不同链接和研究者专用的提交状态链接。三位审查者各用自己的网页独立完成 12 题，每题只选“有意外变化／没有／无法判断”，不用输入文字，最后直接点“提交回答”。页面会在该浏览器自动保存草稿。不要直接用文件管理器打开 HTML：那样无法提交到服务端。默认地址供同一台电脑使用。\n\n每题明确展示要拼的物件、刚才动作前已装的两块积木、刚才要求安装的第三块、当前真实状态，以及最终目标。并排图左边是动作前，右边是现在；目标图只作参照，现在尚未完成是正常的。三种题目类别和答案只在上一级私有答案文件中。服务端把提交保存到 `submissions/`。统计每类的“有／没有／无法判断”，再决定哪些题有资格进入模型恢复成绩。\n''')
    print('human temporal packet',len(rows))


if __name__=='__main__':main()
