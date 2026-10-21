"""Validate and persist static user-designed repair states."""
import json
import re
import sys
import time
from static_bench import (OUT, Domain, TYPES, annotate_static, digest, dump,
                          groups_for, make_case, visual_reference)


def design(request):
    model = request['modelId']
    if not re.fullmatch(r'[A-Za-z0-9_-]+', model):
        raise ValueError('模型 ID 无效')
    folder = OUT/'models'/model
    certificate = json.loads((folder/'qualification.json').read_text())
    candidates = certificate['candidates']
    goals = {r['actor']:k for k,r in candidates.items() if r['kind']=='goal'}
    supplied = request.get('assignments', {})
    if not isinstance(supplied, dict) or any(not isinstance(v,str) for v in supplied.values()):
        raise ValueError('assignments 必须是积木 ID 到位置 ID 的映射')
    assignments = {**goals, **supplied}
    if not set(assignments) <= {r['actor'] for r in candidates.values()}:
        raise ValueError('包含未注册的积木 ID')
    for actor,key in assignments.items():
        if key and (key not in candidates or candidates[key]['actor']!=actor):
            raise ValueError(f'{actor} 使用了未认证的位置')
    edits={a:k for a,k in assignments.items() if k!=goals.get(a,'')}
    if len(edits)>8:raise ValueError('单个案例最多修改 8 个实体')
    groups=groups_for(certificate,edits)
    if len(groups)>4:raise ValueError('单个案例最多 4 处独立错误')
    case=make_case(certificate,model,edits,groups)
    eligible={case['kind']}
    if case['kind']=='height_layer':eligible.add('extra')
    category=request.get('category') or case['kind']
    if category not in eligible:
        raise ValueError('所选类别与静态结构差异不符；可选类别：'+', '.join(TYPES[k] for k in sorted(eligible)))
    case['kind']=category
    try:case=annotate_static(case,Domain(certificate,{}))
    except ValueError as exc:raise ValueError('该组合未通过结构与可修复性检查：'+str(exc))
    case['title']=str(request.get('title') or case['title'])[:120]
    visibility=json.loads((folder/'visibility.json').read_text()) if (folder/'visibility.json').exists() else {}
    visual_reference(case,visibility)
    case['id']='custom-'+digest(dict(model=model,edits=edits,created=time.time_ns()))[:16]
    case.update(createdAt=time.strftime('%Y-%m-%dT%H:%M:%S%z'),authoring='human',category=category,
                eligibleCategories=sorted(eligible),categoryEvidence='static-state-differences',
                qualificationSha256=certificate['contentSha256'],notes=str(request.get('notes',''))[:4000])
    record=json.loads((folder/'record.json').read_text())
    case['targetProvenance']=record.get('targetProvenance',{})
    if request.get('save',True):dump(OUT/'saved'/(case['id']+'.json'),case)
    return case


if __name__=='__main__':
    try:print(json.dumps(dict(case=design(json.load(sys.stdin))),ensure_ascii=False))
    except (KeyError,ValueError) as exc:
        print(json.dumps(dict(error=str(exc)),ensure_ascii=False));sys.exit(1)
