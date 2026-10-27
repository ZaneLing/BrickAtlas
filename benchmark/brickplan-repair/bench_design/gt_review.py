"""Answer-visible GT inspection, distinct from blind human operation.

Replays the actual reference through Session. Images keep a single camera for
all states and retain complete object context. No human construction is needed.
"""
from copy import deepcopy
from pathlib import Path
from collections import Counter,OrderedDict
import hashlib,io,time
import numpy as np
from PIL import Image,ImageFilter
from bench_design.session import Session,internal_action,digest
from bench_design.run_episode import source_rows
from bench_design.policy import FAULTS
from bench_design.challenges import QUALITY
from expansion_v7.build import read,write

REVIEW_VERSION='answer-visible-gt-inspection/1'
CHOICES={'correct':'GT正确','problem':'GT有问题','unclear':'看不清／无法判断'}
COLORS={'0':'黑色','1':'蓝色','2':'绿色','4':'红色','14':'黄色','15':'白色',
        '19':'米色','25':'橙色','28':'深绿色','70':'棕色','71':'浅灰色','72':'深灰色'}


class GTReview:
    def __init__(self,server):
        self.server=server;self.cache=server.data/'gt-previews';self.bundles={};self.renderers=OrderedDict()
        self.items={c['id']:c for c in read(QUALITY/'challenges.private.json.gz')['cases']}
        self.version=digest([REVIEW_VERSION,server.tasks['taskVersion'],
            hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            hashlib.sha256(Path(__file__).with_name('session.py').read_bytes()).hexdigest()])

    def title(self,code):
        cid=self.server.maps['gt'][code]['caseId']
        if cid in self.items:
            from bench_design.quality_report import NAMES
            return NAMES.get(self.items[cid]['model'],self.items[cid]['model'])
        return source_rows()[cid]['title']

    def folder(self,code):return self.cache/self.version[:16]/code

    def bundle(self,code):
        if code in self.bundles:return self.bundles[code]
        folder=self.folder(code);path=folder/'preview.private.json.gz'
        if path.exists():
            value=read(path);self.bundles[code]=value;return value
        cid=self.server.maps['gt'][code]['caseId']
        s=Session.open(cid,folder,actor='scripted:gt-preview');s.autosave=False
        ep=s.ep
        if s.row['bank'] in ('M','O','E7'):
            from bench_design.catalogue import module_runtime
            ep.runtime.q=module_runtime(s.row['bank'],s.row['model']).q
        initial=deepcopy(ep.state)
        frames=[dict(state=initial,label='起点',kind='initial')]
        case=s.row['case'];dynamic=s.row['mode']=='dynamic'
        if s.row['bank']=='D':
            actions=[dict(type='attach',partId=a,candidate=s.goal[a]) for a in ep.runtime.manual()['parts']]
        else:
            actions=deepcopy(case.get('referenceActions',case.get('oraclePlan',[])))
        start=0;incidents=[];moves=0;failure=None
        while actions:
            a=actions.pop(0);before=deepcopy(ep.state)
            if a['type']=='finish':continue
            actor=a.get('actor',a.get('partId'))
            part=ep.runtime.row(before[actor] if a['type']=='detach' else a['candidate'])['part']
            key=before[actor] if a['type']=='detach' else a['candidate']
            feedback=s.submit(internal_action(ep,a))
            if feedback['code']!='OK':
                failure='参考动作被拒绝：'+feedback['code'];break
            moves+=1;record=s.records[-1]
            color=COLORS.get(str(part.get('colorCode')),'')
            text=('拆下' if a['type']=='detach' else '装上')+color+'积木'
            frames.append(dict(state=deepcopy(record['afterOwnActionBeforeExternalChange']),
                label=text,kind=a['type'],actor=actor,key=key,before=before))
            for index in record['newEventIndices']:
                event=s.events[index-1]
                if not incidents:
                    start=len(frames)
                family=event['family'];name=FAULTS.get(family,('',family))[1]
                frames.append(dict(state=deepcopy(event['after']),label='变化'+str(index)+'：'+name,
                    kind='incident',eventIndex=index))
                incidents.append(index)
                if s.row['bank']=='D':actions=deepcopy(event['native']['recoveryWitness'])
        if not s.done:s.submit(dict(type='finish'))
        result=s.result()
        # Review the real intervention slice, not a fabricated checkpoint task.
        visible=frames[start:] if incidents else frames
        if len(visible)>1:visible[0]['label']='出现问题后的状态' if incidents else '修复前' if not dynamic else '拼装起点'
        final=deepcopy(ep.state)
        stage=not dynamic and sum(bool(k) for k in s.goal.values())<sum(bool(k) for k in ep.runtime.goal.values())
        value=dict(code=code,caseId=cid,title=self.title(code),mode='dynamic' if dynamic else 'static',
            reviewVersion=REVIEW_VERSION,previewVersion=self.version,
            current=deepcopy(visible[0]['state']),goal=deepcopy(s.goal),result=final,
            frames=visible,hasIncident=bool(incidents),incidentCount=len(incidents),
            referenceMoves=moves,replaySuccess=result['success'],failure=failure,
            apiCalls=0,answerVisible=True,isHumanCompletionEvidence=False,
            goalIsStage=stage,
            description=('从第一次出问题后开始看；GT包含后续修复和继续拼装。' if incidents else
                         '只需修到本题所示阶段，不必拼完整成品；下方是GT的修法。' if stage and len(visible)>1 else
                         '当前阶段已经正确，GT不需要拆装。' if stage else
                         '从当前状态修到目标；下方是GT的一种修法。' if not dynamic and len(visible)>1 else
                         '当前已经符合目标，GT不需要拆装。' if not dynamic else
                         '这是正常拼装题，下方展示GT怎样完成目标。'))
        folder.mkdir(parents=True,exist_ok=True);temporary=folder/'preview.pending.json.gz';write(temporary,value);temporary.replace(path)
        self.bundles[code]=value;self.renderers[code]=s
        while len(self.renderers)>3:self.renderers.popitem(last=False)
        return value

    def renderer(self,code):
        b=self.bundle(code)
        if code not in self.renderers:
            s=Session.open(b['caseId'],self.folder(code),actor='scripted:gt-preview');s.autosave=False
            self.renderers[code]=s
        self.renderers.move_to_end(code)
        while len(self.renderers)>3:self.renderers.popitem(last=False)
        s=self.renderers[code];r=s.packet.renderer if s.packet else s.renderer
        if '_gt_review_frame' not in r.bounds:
            keys={k for state in [b['current'],b['result'],b['goal']]+[f['state'] for f in b['frames']] for k in state.values() if k}
            keys.update(r.cert['fixed'])
            points=[r.bounds[k] for k in keys if k in r.bounds]
            r.bounds['_gt_review_frame']=np.concatenate(points)
        return r

    def image(self,code,which,view,step=None):
        if code not in self.server.maps['gt'] or view not in ('isometric','rear','top'):raise ValueError('图片无效')
        b=self.bundle(code)
        if which not in ('current','result','goal','step'):raise ValueError('图片无效')
        if which=='step' and (type(step) is not int or not 0<=step<len(b['frames'])):raise ValueError('步骤无效')
        path=self.folder(code)/f'{which}-{step if which=="step" else "main"}-{view}.png'
        if path.exists():return path
        r=self.renderer(code);f=b['frames'][step] if which=='step' else None
        state=f['state'] if f else b[which]
        image,mask=r.rgb(state,view,size=(1000,750),frame_keys=['_gt_review_frame'],supersample=1)
        if f and f.get('actor'):
            # Highlight the selected part, including its pre-removal outline.
            if f['kind']=='detach':_,mask=r.rgb(f['before'],view,size=(1000,750),frame_keys=['_gt_review_frame'],supersample=1)
            selected=Image.fromarray(np.uint8(mask==r.ids[f['actor']])*255)
            grown=np.asarray(selected.filter(ImageFilter.MaxFilter(9))).astype(int)
            border=Image.fromarray(np.uint8(np.maximum(0,grown-np.asarray(selected).astype(int))))
            image.paste((0,151,164),(0,0),border)
        temporary=path.with_suffix('.pending.png');image.save(temporary);temporary.replace(path)
        return path

    def public(self,person,code):
        b=self.bundle(code);saved=self.server.state(person,'gt',code)
        return {k:b[k] for k in ['code','title','mode','description','hasIncident','incidentCount','replaySuccess','failure','goalIsStage']}|dict(
            reviewVersion=REVIEW_VERSION,previewVersion=self.version,
            steps=[dict(index=i,label=f['label'],kind=f['kind']) for i,f in enumerate(b['frames'])],
            choice=saved.get('choice'),submitted=saved['submitted'],answerRevision=saved['answerRevision'])

    def summary(self):
        rows=[]
        for code in self.server.maps['gt']:
            entries=[self.server.state(p,'gt',code) for p in ('A','B','C')]
            votes=[v for v in entries if v['submitted']]
            counts=Counter(v['choice'] for v in votes)
            status=('GT存在异议，需复查' if counts['problem'] else '画面或题意需改进' if counts['unclear'] else
                    '三人一致认为GT正确' if counts['correct']==3 else '还需其他人检查' if votes else '待检查')
            rows.append(dict(code=code,title=self.title(code),submissions=len(votes),counts=dict(counts),status=status))
        return dict(reviewVersion=REVIEW_VERSION,answerVisible=True,isBlindHumanPerformance=False,
            submitted=sum(x['submissions'] for x in rows),total=len(rows),rows=rows,
            note='这是看过参考答案的GT检查，不能作为真人盲做成功率；有异议和看不清的题均保留待查。')
