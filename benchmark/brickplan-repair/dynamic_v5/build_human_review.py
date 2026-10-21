"""Make a blinded, stratified visual-review pilot packet.

The packet asks whether a person can see and explain the change. It is not a
completed human study, and the private answer key is never embedded in HTML.
"""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent/'eval'))
from dynamic_v5.episode import BANK, DynamicEpisode, load_case
from dynamic_v5.vision import DynamicVisionRenderer

OUT = BANK/'human-review'
VIEWS = ('isometric','top')


def token(value):
    return sha256(('human-review-pilot-2026-10-19/'+value).encode()).hexdigest()


def pick(cases):
    by_kind = {}
    for case in cases:
        if case['kind'] != 'none':
            by_kind.setdefault(case['kind'], []).append(case)
    chosen = []
    for kind, rows in sorted(by_kind.items()):
        ordered = sorted(rows, key=lambda row: token(row['id']))
        families = set()
        subset = []
        # Prefer distinct source families, then fill up to three examples.
        for row in ordered:
            if row['sourceFamily'] not in families:
                subset.append(row);families.add(row['sourceFamily'])
            if len(subset) == 3:
                break
        for row in ordered:
            if len(subset) == 3:
                break
            if row not in subset:
                subset.append(row)
        chosen += subset
    # Every new complete object must appear at least once, so reviewers can
    # say whether the pictured target is recognizable without seeing its name.
    for model_id in sorted({c['modelId'] for c in cases if c['modelId'].startswith('obj-')}):
        if any(c['modelId']==model_id for c in chosen):
            continue
        options=[c for c in cases if c['modelId']==model_id and c['kind']!='none']
        chosen.append(min(options,key=lambda row:token(row['id'])))
    return sorted(chosen, key=lambda row: token(row['id']+'-order'))


def make_page(reviewer, rows):
    ordered = sorted(rows, key=lambda row: token(reviewer+row['code']))
    cards = []
    for row in ordered:
        images = ''.join(
            f'<figure><img src="assets/{row["code"]}-{role}-{view}.png" alt="{role} {view}">'
            f'<figcaption>{label} / {"斜视" if view=="isometric" else "俯视"}</figcaption></figure>'
            for role,label in (('before','变化前'),('after','变化后'),('target','最终目标'))
            for view in VIEWS)
        code = row['code']
        cards.append(f'''<section class="case" data-code="{code}"><h2>{code}</h2>
<div class="images">{images}</div>
<label>最终目标看起来像什么物件？<textarea name="object_guess"></textarea></label>
<label>能看出变化吗？ <select name="visible"><option value="">请选择</option><option>能</option><option>不能</option><option>不确定</option></select></label>
<label>哪里变了？请用自己的话描述。<textarea name="description"></textarea></label>
<label>你会怎么修？<textarea name="repair"></textarea></label>
<label>图片是否太小或被挡住？ <select name="occluded"><option value="">请选择</option><option>否</option><option>是</option><option>不确定</option></select></label>
<label>判断把握 <select name="confidence"><option value="">请选择</option><option>高</option><option>中</option><option>低</option></select></label>
</section>''')
    html = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>积木变化盲审 {reviewer}</title>
<style>body{{font-family:-apple-system,BlinkMacSystemFont,sans-serif;color:#1d2834;max-width:1500px;margin:auto;padding:24px;background:#f5f7f8}}.case{{background:white;margin:25px 0;padding:20px;border:1px solid #ccd4db;border-radius:10px}}.images{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}figure{{margin:0}}img{{width:100%;border:1px solid #dce1e5}}figcaption{{font-size:13px;color:#536473}}label{{display:block;margin:12px 0;font-weight:600}}textarea{{display:block;width:98%;height:60px;margin-top:5px}}select{{margin-left:8px}}button{{font-size:17px;padding:10px 16px;cursor:pointer}}</style>
<h1>积木变化盲审 · {reviewer}</h1><p>请看每题的变化前、变化后和最终目标。先判断能否看出变化，再写怎样修。题目类别和答案没有显示。请独立完成，不与其他审查者讨论。</p>
<p>这是第一轮抽样检查，共 {len(ordered)} 题。若某题看不清楚，直接选“不能”或“不确定”。</p>
<button onclick="save()">下载我的回答 JSON</button>{''.join(cards)}<button onclick="save()">下载我的回答 JSON</button>
<script>function save(){{const rows=[...document.querySelectorAll('.case')].map(c=>{{let x={{code:c.dataset.code}};for(let e of c.querySelectorAll('select,textarea'))x[e.name]=e.value;return x}});let data={{reviewer:'{reviewer}',answers:rows}};let a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{{type:'application/json'}}));a.download='brick-review-{reviewer}.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)}}</script></html>'''
    (OUT/f'{reviewer}.html').write_text(html)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'assets').mkdir(exist_ok=True)
    cases = json.loads((BANK/'index.json').read_text())['cases']
    chosen = pick(cases)
    rows = []
    renderers = {}
    for i, public in enumerate(chosen,1):
        cert, case = load_case(public['id'])
        ep = DynamicEpisode(cert,case)
        if case['modelId'] not in renderers:
            renderers[case['modelId']] = DynamicVisionRenderer(ep.cert,ep.runtime)
        renderer = renderers[case['modelId']]
        before = ep.runtime.manual()['states'][case['trigger']]
        after = dict(before)
        for action in case['privateEvent']['transaction']:
            after, feedback = ep.runtime.check(after,action['partId'],action['type'],candidate=action.get('candidate'))
            assert feedback['code']=='OK'
        code = f'H{i:03}'
        for role,state in (('before',before),('after',after),('target',ep.runtime.goal)):
            for view in VIEWS:
                renderer.rgb(state,view,size=(800,600),supersample=1)[0].save(
                    OUT/'assets'/f'{code}-{role}-{view}.png')
        rows.append(dict(code=code,caseId=case['id'],kind=case['kind'],
                         modelId=case['modelId'],sourceFamily=case['sourceFamily']))
        print(code,case['kind'],flush=True)
    for reviewer in ('reviewer-A','reviewer-B','reviewer-C'):
        make_page(reviewer,rows)
    answer = dict(schema='brickplan-dynamic-human-review-pilot/1',
                  instruction='Keep private from reviewers until all answers are collected.',
                  seed='human-review-pilot-2026-10-19',cases=len(rows),
                  kinds=dict(Counter(r['kind'] for r in rows)),rows=rows)
    (BANK/'human-review-answer-key.private.json').write_text(json.dumps(answer,ensure_ascii=False,indent=2)+'\n')
    print('review packet',len(rows),dict(Counter(r['kind'] for r in rows)),flush=True)


if __name__ == '__main__':
    main()
