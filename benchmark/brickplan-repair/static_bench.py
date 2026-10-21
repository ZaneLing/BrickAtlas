"""Static repair curation: observable state defects and exact repair difficulty.

No event prefix, external intervention, or counterfactual assembly history is
part of a task. Geometry certificates remain an authoring/execution constraint.
"""
from __future__ import annotations
import argparse
from collections import Counter
from copy import deepcopy
from functools import lru_cache
import hashlib
import heapq
from itertools import combinations, count
import json
import os
from pathlib import Path
import re
import shutil
import time

from engine import Domain

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(os.environ.get('BRICKPLAN_REPAIR_DATA', ROOT / 'deliverables/brickplan-repair-library'))
TYPES = {'missing': '漏件', 'wrong_color': '错颜色', 'wrong_type': '错形状/功能',
         'wrong_size': '同类错尺寸', 'offset': '水平错位', 'rotation': '朝向错误',
         'height_layer': '高度错层', 'extra': '多余零件', 'swapped_positions': '部件位置互换',
         'compound': '复合错误', 'control': '无故障对照'}
TAXONOMY = [(k, v, [k]) for k, v in TYPES.items() if k != 'control']
CHALLENGES = {'requires_disassembly': '需拆开正确件', 'deep_access': '深层嵌入',
              'shared_access': '多错误共享拆修通道', 'support_coupling': '连接依赖耦合',
              'mixed_faults': '异类错误组合', 'multi_fault': '三处及以上错误',
              'view_dependent': '需要换视角', 'visual_unverified': '视觉可辨性待验证'}
CHALLENGES.update(four_fault_coupling='四处错误耦合', visual_ambiguous='视觉不可辨，限符号赛道')
CHALLENGES.update(independent_access='独立拆修通道', joint_repair_savings='合并修复收益',
                  alternative_release='多条等价拆修通道', suspended_coupling='悬挂嵌合',
                  order_interference='修复顺序干涉', equivalence_control='物理等价对照', no_op='无需修复')
DYNAMIC = {'external_removal', 'stale_plan', 'wrong_order', 'costly_branch', 'premature_closure', 'path_blocked'}
VIEWS = ['isometric', 'front', 'rear', 'left', 'right', 'top', 'bottom']
PROTOCOL = {'schema': 'brickplan-static-repair/3', 'task': '给定错误状态和目标图像，观察、拆修并完成。', 'environmentChanges': False, 'buildFromEmpty': False, 'actions': ['inspect', 'attach', 'detach', 'finish'], 'inspect': {'views': ['isometric', 'front', 'rear', 'left', 'right', 'top', 'bottom'], 'arbitraryRotation': True, 'nativeResolutionCrop': True, 'pointSelection': True, 'uniformPieceInspection': True, 'changesAssembly': False, 'repairCost': 0, 'countSeparately': True}, 'tracks': {'visual': {'protocol': 'visual-rgb-v3', 'input': '独立高清当前/目标 RGB 与零件参考图。只提供匿名动作句柄，不提供型号、颜色描述、坐标矩阵、支撑/阻挡关系、状态映射或错误标签。', 'resolution': [1600, 1200], 'initialViews': ['isometric', 'rear', 'top'], 'mainSceneLabels': False, 'status': 'offline_verified_not_yet_model_retested', 'admission': '每例调用前重新检查 v3 实际状态的可见差异；旧协议成绩不能并入。', 'hiddenInterior': '可按需对任意件做统一隔离观察；不等于仅靠外部相机，也不是实物 VLA 评测。'}}, 'retiredTracks': ['symbolic', 'text', 'visual-v1', 'visual-v2'], 'reviewTools': '网页审核与回放独立于模型输入。'}
PROTOCOL['manipulation'] = {'protocol': 'connector-workbench/4', 'support': '连接无方向；手持/夹具保持子装配；不检查底部承重', 'paths': '连接轴和零件轴的多个直线路径，保留碰撞检查', 'success': '最终几何与颜色一致，允许同款同色互换和已登记对称性', 'sequence': '不限参考修复顺序；操作、失败、观察分别计数', 'optimalCost': '旧库最优步数仅作历史参考，不是新操作域最优值', 'placementDomain': '人工支持连接点吸附的自由姿态；现有 VLM 动作目录仍为已登记姿态'}



def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


@lru_cache(maxsize=2048)
def part_name(stem):
    path = ROOT / f'assets-source/ldraw-library/locked/parts/{stem}.dat'
    if not path.exists():
        return stem
    return path.read_text().splitlines()[0].removeprefix('0 ').lstrip('~_=')


def shape_signature(name):
    clean = re.sub(r'\s+', ' ', name).lower().strip()
    # A size variant must have exactly the same descriptive shape/feature family.
    signature = re.sub(r'\b\d+(?:\.\d+)?\b', '#', clean)
    dimensions = tuple(re.findall(r'\b\d+(?:\.\d+)?\b', clean))
    return signature, dimensions


def replacement_kind(target, actual):
    a, b = shape_signature(part_name(target['partNumber'])), shape_signature(part_name(actual['partNumber']))
    if target['canonical'] == actual['canonical']:
        return 'wrong_color' if target['colorHex'].lower() != actual['colorHex'].lower() else None
    return 'wrong_size' if a[0] == b[0] and a[1] != b[1] else 'wrong_type'


def difficulty(cost):
    return 'D0' if cost == 0 else 'D1' if cost <= 2 else 'D2' if cost <= 5 else 'D3' if cost <= 9 else 'D4' if cost <= 15 else 'D5'


def exact_plan(domain, case, max_expansions=200000):
    """A* with a consistent per-piece edit lower bound; never label a timeout solved."""
    initial, goal = domain.pack(case, case['initial']), domain.pack(case, case['goal'])
    def h(state):
        return sum(0 if a == b else 2 if a and b else 1 for a, b in zip(state, goal))
    serial = count()
    queue = [(h(initial), 0, next(serial), initial)]
    distance, previous = {initial: 0}, {initial: None}
    expanded = 0
    while queue:
        _, neg_g, _, node = heapq.heappop(queue)
        g = -neg_g
        if distance[node] != g:
            continue
        if node == goal:
            plan = []
            while previous[node]:
                node, action = previous[node]
                plan.append(action)
            return list(reversed(plan)), expanded
        expanded += 1
        if expanded > max_expansions:
            raise ValueError('Exact search limit reached; no optimum claimed')
        for action in domain.actions(case, node):
            after, check = domain.transition(case, node, action)
            if check['code'] == 'OK' and g + 1 < distance.get(after, 10**9):
                distance[after] = g + 1
                previous[after] = node, action
                heapq.heappush(queue, (g + 1 + h(after), -(g + 1), next(serial), after))
    raise ValueError('No repair path')


def make_case(cert, model, edits, groups, kind=None):
    goals = {r['actor']: k for k, r in cert['candidates'].items() if r['kind'] == 'goal'}
    actors = sorted(set(goals) | set(edits))
    goal = {a: goals.get(a, '') for a in actors}
    initial = {**goal, **edits}
    kind = kind or ('control' if not groups else groups[0]['type'] if len(groups) == 1 else 'compound')
    return dict(id=f'{model}:{kind}:{digest(edits)[:10]}', modelId=model, kind=kind,
                title=TYPES[kind], description='', actors=actors, initial=initial, goal=goal,
                choices={a: list(dict.fromkeys(k for k in [initial[a], goal[a]] if k)) for a in actors},
                roots=[dict(eventId=f'defect-{i+1}', stage='StaticDefect', **g) for i, g in enumerate(groups)],
                rackCapacity=len(actors), sourceExample=cert.get('source', {}).get('modelId', model),
                sourcePieces=len(goals)+len(cert['fixed']), contract='Static state repair in the registered geometric domain.')


def groups_for(cert, edits):
    candidates = cert['candidates']
    goals = {r['actor']: k for k, r in candidates.items() if r['kind'] == 'goal'}
    source_actor = {candidates[k]['part']['sourceIndex']: a for a, k in goals.items()}
    groups, owned = [], set()
    for actor, key in sorted(edits.items()):
        if key and actor not in goals:
            row = candidates[key]
            target = source_actor.get(row['part'].get('derivedFromSourceIndex'))
            affected = [actor] + ([target] if target in edits else [])
            kind = row['kind']
            if kind == 'extra' and target in edits and edits[target] and candidates[edits[target]]['kind'] == 'height_layer':
                kind = 'height_layer'
            groups.append(dict(partId=actor, type=kind, affectedActors=affected))
            owned.update(affected)
    for actor, key in sorted(edits.items()):
        if actor not in owned:
            if key and candidates[key]['kind'] == 'swapped_positions':
                partner = candidates[key]['part'].get('swapPartner')
                if partner not in edits or not edits[partner] or candidates[edits[partner]]['part'].get('swapPartner') != actor:
                    raise ValueError('位置互换必须同时移动两个对应零件')
                affected = sorted([actor, partner])
                groups.append(dict(partId=actor, type='swapped_positions', affectedActors=affected))
                owned.update(affected)
                continue
            groups.append(dict(partId=actor, type=candidates[key]['kind'] if key else 'missing', affectedActors=[actor]))
    return groups


def annotate_static(case, domain, known_plan=None, singleton_costs=None):
    c = deepcopy(case)
    for k in ('preIntervention', 'intervention', 'interventions', 'oldPlan', 'rejectedPrefix', 'branchCostEvidence',
              'causalReplay', 'counterfactuals', 'propagation', 'sourceLabels', 'visibilityEvidence'):
        c.pop(k, None)
    initial, goal = domain.pack(c, c['initial']), domain.pack(c, c['goal'])
    for state in (initial, goal):
        code = domain.valid(c, state)
        if code != 'OK':
            raise ValueError(code)
    if known_plan is None:
        plan, expanded = exact_plan(domain, c)
    else:
        plan, expanded = deepcopy(known_plan), None
    state = initial
    for action in plan:
        state, check = domain.transition(c, state, action)
        if check['code'] != 'OK':
            raise ValueError('Invalid oracle: '+check['code'])
    if state != goal:
        raise ValueError('Oracle misses goal')
    changed = {a for a in c['actors'] if c['initial'][a] != c['goal'][a]}
    groups = c['roots']
    covered = [a for r in groups for a in r['affectedActors']]
    if len(covered) != len(set(covered)) or set(covered) != changed:
        raise ValueError('Defect groups must partition state differences')
    collateral = sorted({a['partId'] for a in plan if a['type'] == 'detach' and a['partId'] not in changed})
    lower = sum(0 if a == b else 2 if a and b else 1 for a, b in zip(initial, goal))
    direct_checks, replacements = [], []
    support_coupled = False
    for root in groups:
        for actor in root['affectedActors']:
            if c['initial'][actor]:
                action = dict(type='detach', partId=actor)
            else:
                action = dict(type='attach', partId=actor, candidate=c['goal'][actor])
            _, check = domain.transition(c, initial, action)
            direct_checks.append(dict(partId=actor, action=action, **check))
            # Isolates support dependency even if path occlusion rejects first.
            if c['initial'][actor]:
                removed = list(initial); removed[c['actors'].index(actor)] = ''
                support_coupled |= domain.valid(c, tuple(removed)) == 'DISCONNECTED_ASSEMBLY'
        if root['type'] in ('wrong_type', 'wrong_size', 'wrong_color'):
            actual = domain.candidates[c['initial'][root['partId']]]['part']
            target_actor = next(a for a in root['affectedActors'] if c['goal'][a])
            target = domain.candidates[c['goal'][target_actor]]['part']
            replacements.append(dict(type=root['type'], targetActor=target_actor,
                                     expected=dict(part=target['partNumber'], name=part_name(target['partNumber']), color=target['colorHex']),
                                     actual=dict(part=actual['partNumber'], name=part_name(actual['partNumber']), color=actual['colorHex'])))
    tags = []
    if len(plan) > lower: tags.append('requires_disassembly')
    if len(collateral) >= 3: tags.append('deep_access')
    if support_coupled: tags.append('support_coupling')
    if len({r['type'] for r in groups}) > 1: tags.append('mixed_faults')
    if len(groups) >= 3: tags.append('multi_fault')
    savings = sum(singleton_costs)-len(plan) if singleton_costs else 0
    if savings > 0: tags.append('shared_access')
    structural_types = sorted({r['type'] for r in groups} | ({'extra'} if any(r['type']=='height_layer' for r in groups) else set()))
    c.update(schema='brickplan-static-repair-case/2', benchmarkMode='static', environmentChanges=False,
             structuralTypes=structural_types,
             oraclePlan=plan, expectedOptimum=len(plan), difficulty=difficulty(len(plan)), tags=tags,
             repairEvidence=dict(unconstrainedEditLowerBound=lower, requiredExtraActions=len(plan)-lower,
                                 oracleCollateralParts=collateral, directRepairChecks=direct_checks,
                                 independentRepairCosts=singleton_costs, sharedRepairSavings=max(0,savings),
                                 replacements=replacements, searchExpanded=expanded,
                                 optimumScope='Exact minimum attach/detach count in the registered finite domain.'),
             observation=dict(symbolicEligible=True, visualEligibility='unverified',
                              reason='尚未验证此错误初态与目标的多视角像素差异。', reviewOrbitAvailable=True,
                              evaluationAdapterConnected=True, proposedViews=VIEWS))
    labels = ' + '.join(dict.fromkeys(TYPES[r['type']] for r in groups))
    prefix = '多层拆修 · ' if len(collateral) >= 3 else '受限拆修 · ' if len(plan) > lower else ''
    if c['kind'] == 'control':
        c['title'], c['description'] = '无故障对照', '当前状态已与目标一致，直接提交。'
    else:
        c['title'] = prefix + labels + ' · ' + '/'.join(r['partId'] for r in groups)
        c['description'] = f'静态初态；{len(groups)} 处错误，最少 {len(plan)} 次拆装。'
        if collateral:
            c['description'] += f' 最优回放需暂拆 {len(collateral)} 个原本正确的零件。'
    return c


def visual_reference(case, visibility):
    """Existing target-only segmentation is evidence of occlusion, not VLM admission."""
    rows = []
    for root in case['roots']:
        for a in root['affectedActors']:
            if not case['goal'].get(a): continue
            views = visibility.get('measurements', {}).get(a, [])
            if not views: continue
            visible = [v for v in views if v['fullScenePixels'] >= 24 and v['visibleFraction'] >= .03]
            rows.append(dict(actor=a, visibleViews=[v['view'] for v in visible],
                             hiddenInReferenceIsometric=not any(v['view']=='isometric' for v in visible)))
    if rows:
        case['observation']['referenceVisibility'] = rows
        case['observation']['referenceScope'] = '旧目标状态的分件可见像素；不能替代实际错误初态的差异验证。'
        if any(r['hiddenInReferenceIsometric'] for r in rows):
            case['tags'].append('view_dependent')
        if any(not r['visibleViews'] for r in rows):
            case['observation']['reason'] = '参考视角中存在完全不可见的目标零件；纯视觉评测需内部参考/主动拆检协议。'
    case['tags'].append('visual_unverified')


def normalized_state(case, cert):
    """Deduplicate physical layouts even when old T/Z actor aliases differ."""
    return digest(sorted((r['part']['canonical'], r['part']['colorHex'].lower(), r['part']['rawMatrix'])
                         for key in case['initial'].values() if key for r in [cert['candidates'][key]]))


def curate_model(folder, pair_budget=44):
    cert = json.loads((folder/'qualification.json').read_text())
    record = json.loads((folder/'record.json').read_text())
    if 'targetProvenance' not in record:
        source=cert.get('source',record.get('source',{}));selected=set(source.get('includedSourceIndices',[]))
        displacement=max((r['maxVertexDisplacementLDU'] for r in source.get('poseCorrections',[]) if r['sourceIndex'] in selected),default=0.)
        modified=source.get('sourceGeometryModified',False)
        record['targetProvenance']=dict(kind='connector_reconstructed' if modified else 'source_exact',
            sourceGeometryModified=modified,scope=source.get('scope','Original rigid-part source subset.'),
            maxSelectedVertexCorrectionMm=displacement*.4,
            maximumAllowedVertexCorrectionMm=source.get('maximumAllowedVertexCorrectionLDU',.25)*.4 if modified else 0.)
    proposal_path = folder/'static-proposals.json'
    if not proposal_path.exists():
        archived = OUT/'archive/before-static-v2/models'/folder.name/'cases.json'
        if archived.exists():
            proposal_path = archived
        else:
            dump(proposal_path, json.loads((folder/'cases.json').read_text()))
    old = json.loads(proposal_path.read_text())
    visibility = json.loads((folder/'visibility.json').read_text()) if (folder/'visibility.json').exists() else {}
    candidates = cert['candidates']
    goals = {r['actor']: k for k,r in candidates.items() if r['kind']=='goal'}
    originals = {r['part']['sourceIndex']: r['part'] for r in candidates.values() if r['kind']=='goal'}
    for key,row in candidates.items():
        row['part']['name'] = part_name(row['part']['partNumber'])
        if row['kind'] in ('wrong_type','wrong_size'):
            row['kind'] = replacement_kind(originals[row['part']['derivedFromSourceIndex']],row['part']) or row['kind']
            row['label'] = TYPES[row['kind']]
    domain = Domain(cert,{})
    pool, seen, removed = [], set(), Counter()
    for source in old.values():
        if source['kind'] in DYNAMIC or source['kind']=='compound':
            removed[source['kind']] += 1; continue
        edits = {a:k for a,k in source['initial'].items() if k != source['goal'].get(a,'')}
        groups = groups_for(cert, edits)
        if any(g['type'] not in TYPES for g in groups):
            removed['unsupported'] += 1; continue
        c = make_case(cert, record['modelId'], edits, groups)
        c['id'] = source['id'] if source['kind']==c['kind'] else c['id']
        physical = normalized_state(c, cert)
        if physical in seen:
            removed['duplicate_layout'] += 1; continue
        seen.add(physical)
        try:
            c = annotate_static(c, domain, known_plan=source.get('oraclePlan'))
            pool.append(c)
        except ValueError as exc:
            removed[str(exc)] += 1
    # Pool retains every qualified color placement for use in mixed faults.
    selected = []
    for kind in TYPES:
        rows = sorted([c for c in pool if c['kind']==kind],key=lambda c:(c['expectedOptimum'],c['id']))
        limit = 3 if kind=='wrong_color' else 4 if kind=='missing' else 2 if kind in ('offset','rotation','wrong_type','wrong_size') else len(rows)
        if len(rows)>limit:
            indexes = sorted(set(round(i*(len(rows)-1)/(limit-1)) for i in range(limit)))
            kept = [rows[i] for i in indexes]
            removed[kind+':repetition'] += len(rows)-len(kept)
        else: kept=rows
        selected.extend(kept)
    singles = [c for c in pool if len(c['roots'])==1]
    pairs = []
    for a,b in combinations(singles,2):
        ra,rb=a['roots'][0],b['roots'][0]
        if set(ra['affectedActors']) & set(rb['affectedActors']):continue
        if ra['type']==rb['type']=='wrong_color':continue
        shared=set(a['repairEvidence']['oracleCollateralParts']) & set(b['repairEvidence']['oracleCollateralParts'])
        score=(bool(shared), len(shared), a['expectedOptimum']+b['expectedOptimum'],ra['type']!=rb['type'])
        pairs.append((score,a,b))
    pairs.sort(key=lambda row:row[0],reverse=True)
    # Interleave type signatures so a deep color/missing pair cannot monopolize proposals.
    buckets={}
    for _,a,b in pairs:buckets.setdefault(tuple(sorted([a['kind'],b['kind']])),[]).append((a,b))
    proposals=[]
    while any(buckets.values()) and len(proposals)<pair_budget:
        for bucket in buckets.values():
            if bucket and len(proposals)<pair_budget:proposals.append(bucket.pop(0))
    compounds=[]
    for parts in proposals:
        edits={a:k for p in parts for a,k in p['initial'].items() if k!=p['goal'].get(a,'')}
        groups=[{k:v for k,v in r.items() if k in ('partId','type','affectedActors')} for p in parts for r in p['roots']]
        c=make_case(cert,record['modelId'],edits,groups)
        if normalized_state(c,cert) in seen:continue
        try:
            c=annotate_static(c,domain,singleton_costs=[p['expectedOptimum'] for p in parts])
            compounds.append((c,parts));seen.add(normalized_state(c,cert))
        except ValueError as exc: removed['compound:'+str(exc)] += 1
    # Three independent defects on the same structure, prioritizing coupled access.
    for pair,parts in sorted(compounds,key=lambda row:(row[0]['repairEvidence']['sharedRepairSavings'],row[0]['expectedOptimum']),reverse=True)[:4]:
        occupied={a for r in pair['roots'] for a in r['affectedActors']}
        for third in sorted(singles,key=lambda c:c['expectedOptimum'],reverse=True):
            if occupied.intersection(third['roots'][0]['affectedActors']):continue
            group_parts=(*parts,third)
            edits={a:k for p in group_parts for a,k in p['initial'].items() if k!=p['goal'].get(a,'')}
            groups=[{k:v for k,v in r.items() if k in ('partId','type','affectedActors')} for p in group_parts for r in p['roots']]
            c=make_case(cert,record['modelId'],edits,groups)
            if normalized_state(c,cert) in seen:continue
            try:
                c=annotate_static(c,domain,singleton_costs=[p['expectedOptimum'] for p in group_parts])
                compounds.append((c,group_parts));seen.add(normalized_state(c,cert));break
            except ValueError:continue
    ranked=sorted([c for c,_ in compounds],key=lambda c:(c['repairEvidence']['sharedRepairSavings']>0,
        c['repairEvidence']['requiredExtraActions']>0,len(c['roots'])>=3,c['expectedOptimum']),reverse=True)
    kept,counts=[],Counter()
    for c in ranked:
        signature=tuple(sorted(r['type'] for r in c['roots']))
        if counts[signature]>=2:continue
        if len(kept)>=8:break
        if c['repairEvidence']['requiredExtraActions']==0 and len(kept)>=3:continue
        counts[signature]+=1;kept.append(c)
    selected.extend(kept)
    # Existing review IDs survive where the structural meaning is unchanged.
    cert.pop('contentSha256',None);cert['contentSha256']=digest(cert)
    for c in selected:
        visual_reference(c,visibility)
        c['qualificationSha256']=cert['contentSha256']
        c['targetProvenance']=record.get('targetProvenance',{})
    selected.sort(key=lambda c:(c['kind']=='control',-c['expectedOptimum'],c['kind'],c['id']))
    record.update(schema='brickplan-static-repair-model/2',benchmarkMode='static',caseCount=len(selected),
                  kinds=dict(Counter(c['kind'] for c in selected)),difficulty=dict(Counter(c['difficulty'] for c in selected)),
                  qualificationSha256=cert['contentSha256'],
                  staticCuration=dict(removed=dict(removed),testedPairs=len(proposals),compoundCases=len(kept),maxSingleColor=3),
                  cases=[{k:c[k] for k in ('id','title','kind','difficulty','expectedOptimum')} for c in selected])
    record['coverage']=[dict(id=k,label=label,status='covered' if (ids:=[c['id'] for c in selected if c['kind'] in kinds or set(c['structuralTypes']).intersection(kinds)]) else 'not_admitted',caseIds=ids,
                              reason=None if ids else '当前子结构没有通过验证的此类静态案例。') for k,label,kinds in TAXONOMY]
    dump(folder/'qualification.json',cert);dump(folder/'cases.json',{c['id']:c for c in selected});dump(folder/'record.json',record)
    print(record['modelId'],len(selected),dict(Counter(c['difficulty'] for c in selected)),'compound',len(kept),flush=True)
    return record


def aggregate():
    records,cases=[],[]
    for folder in sorted((OUT/'models').iterdir()):
        if not (folder/'record.json').exists():continue
        r=json.loads((folder/'record.json').read_text())
        if r.get('benchmarkMode')!='static':continue
        model_cases=json.loads((folder/'cases.json').read_text())
        for c in model_cases.values():
            c['structuralTypes']=sorted({root['type'] for root in c['roots']} | ({'extra'} if any(root['type']=='height_layer' for root in c['roots']) else set()))
        r['coverage']=[dict(id=k,label=label,status='covered' if (ids:=[c['id'] for c in model_cases.values() if c['kind'] in kinds or set(c['structuralTypes']).intersection(kinds)]) else 'not_admitted',caseIds=ids,
                           reason=None if ids else '当前子结构没有通过验证的此类静态案例。') for k,label,kinds in TAXONOMY]
        dump(folder/'cases.json',model_cases);dump(folder/'record.json',r)
        records.append(r);cases.extend(model_cases.values())
    index=dict(schema='brickplan-static-repair-library/2',benchmarkMode='static',modelCount=len(records),readyModels=len(records),
               caseCount=len(cases),models=records,taxonomy=[dict(id=i,label=l,kinds=k) for i,l,k in TAXONOMY],
               kinds=dict(Counter(c['kind'] for c in cases)),difficulty=dict(Counter(c['difficulty'] for c in cases)),
               challenges=CHALLENGES,challengeCounts=dict(Counter(t for c in cases for t in c['tags'])),
               observationProtocol=PROTOCOL,sourceExactModels=sum(r.get('targetProvenance',{}).get('kind')=='source_exact' for r in records))
    dump(OUT/'index.json',index)
    (OUT/'cases.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in cases))
    dump(OUT/'observation-protocol.json',PROTOCOL)
    print(json.dumps({k:v for k,v in index.items() if k not in ('models','taxonomy','observationProtocol')},ensure_ascii=False),flush=True)
    return index


def archive():
    target=OUT/'archive'/'before-static-v2'
    if target.exists():return
    target.mkdir(parents=True)
    for name in ('index.json','cases.jsonl','DATASET.md','README.zh-CN.md','reviews.json'):
        if (OUT/name).exists():shutil.copy2(OUT/name,target/name)
    for folder in (OUT/'models').iterdir():
        if not folder.is_dir():continue
        for name in ('cases.json','record.json','qualification.json'):
            if (folder/name).exists():
                (target/'models'/folder.name).mkdir(parents=True,exist_ok=True)
                shutil.copy2(folder/name,target/'models'/folder.name/name)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--model',action='append');parser.add_argument('--aggregate',action='store_true');parser.add_argument('--resume',action='store_true')
    args=parser.parse_args();archive()
    if not args.aggregate:
        folders=[OUT/'models'/m for m in args.model] if args.model else sorted((OUT/'models').iterdir())
        for folder in folders:
            if not (folder/'cases.json').exists():continue
            if args.resume and json.loads((folder/'record.json').read_text()).get('benchmarkMode')=='static':continue
            curate_model(folder)
    aggregate()


if __name__=='__main__':main()
