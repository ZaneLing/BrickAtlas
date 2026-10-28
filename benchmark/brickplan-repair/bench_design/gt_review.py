"""Answer-visible GT inspection, distinct from blind human operation.

Replays the actual reference through Session. Images keep a single camera for
all states and retain complete object context. No human construction is needed.
"""
from copy import deepcopy
from pathlib import Path
from collections import Counter,OrderedDict
import hashlib,io,time
import numpy as np
from PIL import Image,ImageFilter,ImageDraw
from bench_design.session import Session,internal_action,digest
from bench_design.run_episode import source_rows
from bench_design.policy import FAULTS
from bench_design.challenges import QUALITY
from expansion_v7.build import read,write

REVIEW_VERSION='answer-visible-gt-inspection/2'
ANGLES={'isometric':(35,30),'rear':(145,30),'left':(-55,15),'top':(0,90)}
CHOICES={'correct':'GT正确','problem':'GT有问题','unclear':'看不清／无法判断'}
COLORS={'0':'黑色','1':'蓝色','2':'绿色','4':'红色','14':'黄色','15':'白色',
        '6':'棕色','69':'淡紫色','84':'中棕色','85':'深紫色','86':'棕色','288':'深绿色','308':'深棕色','19':'米色','25':'橙色','28':'深绿色','70':'棕色','71':'浅灰色','72':'深灰色'}


class GTReview:
    def __init__(self,server):
        self.server=server;self.cache=server.data/'gt-previews';self.bundles={};self.renderers=OrderedDict()
        self.items={c['id']:c for c in read(QUALITY/'challenges.private.json.gz')['cases']}
        extension=QUALITY/'source-expansion/review-tasks.json'
        from bench_design.reference_revisions import PATH as reference_path
        source_hashes=[hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((QUALITY/'source-expansion/models').glob('*/*.json*'))]
        self.version=digest([REVIEW_VERSION,server.tasks['taskVersion'],read(extension) if extension.exists() else None,source_hashes,
            hashlib.sha256(reference_path.read_bytes()).hexdigest() if reference_path.exists() else None,
            hashlib.sha256(Path(__file__).parents[1].joinpath('expansion_v7/runtime.py').read_bytes()).hexdigest(),
            hashlib.sha256(Path(__file__).with_name('reference_revisions.py').read_bytes()).hexdigest(),
            hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            hashlib.sha256(Path(__file__).with_name('session.py').read_bytes()).hexdigest()])

    def title(self,code):
        cid=self.server.maps['gt'][code]['caseId']
        if cid in self.items:
            from bench_design.quality_report import NAMES
            return NAMES.get(self.items[cid]['model'],self.items[cid]['model'])
        if cid.startswith('QN:'):
            from bench_design.source_expansion import source_row
            return source_row(cid)['title']
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
            piece=case.get('referenceActorLabels',{}).get(actor,color+'积木（'+part['partNumber']+'）')
            text=('拆下' if a['type']=='detach' else '装上')+piece
            frames.append(dict(state=deepcopy(record['afterOwnActionBeforeExternalChange']),
                label=text,kind=a['type'],actor=actor,key=key,before=before))
            for index in record['newEventIndices']:
                event=s.events[index-1]
                if not incidents:
                    start=len(frames)
                family=event['family'];name=FAULTS.get(family,('',family))[1]
                frames.append(dict(state=deepcopy(event['after']),label='变化'+str(index)+'：'+name,
                    kind='incident',eventIndex=index,before=deepcopy(event['before'])))
                incidents.append(index)
                if s.row['bank']=='D':actions=deepcopy(event['native']['recoveryWitness'])
        if not s.done:s.submit(dict(type='finish'))
        result=s.result()
        # Review the real intervention slice, not a fabricated checkpoint task.
        visible=frames[start:] if incidents else frames
        if len(visible)>1:visible[0]['label']='出现问题后的状态' if incidents else '修复前' if not dynamic else '拼装起点'
        final=deepcopy(ep.state)
        full_goal={r['actor']:k for k,r in ep.cert['candidates'].items() if r['kind']=='goal'}
        stage=not dynamic and sum(bool(k) for k in s.goal.values())<len(full_goal)
        cp=case.get('completedInstructionStep',sum(bool(k) for k in s.goal.values()))
        value=dict(code=code,caseId=cid,title=self.title(code),mode='dynamic' if dynamic else 'static',
            reviewVersion=REVIEW_VERSION,previewVersion=self.version,
            current=deepcopy(visible[0]['state']),goal=deepcopy(s.goal),result=final,
            frames=visible,hasIncident=bool(incidents),incidentCount=len(incidents),
            referenceMoves=moves,replaySuccess=result['success'],failure=failure,
            apiCalls=0,answerVisible=True,isHumanCompletionEvidence=False,
            goalIsStage=stage,stageNumber=cp,fullGoal=full_goal,
            acceptanceParts=sum(bool(k) for k in s.goal.values()),fullParts=len(full_goal),
            description=('从第一次出问题后开始看；GT包含后续修复和继续拼装。' if incidents else
                         f'本题只验收第 {cp} 步的状态（{sum(bool(k) for k in s.goal.values())} 块）。修到右图即可，不用继续拼完整物件。' if stage and len(visible)>1 else
                         '当前阶段已经正确，GT不需要拆装。' if stage else
                         '从当前状态修到目标；下方是GT的一种修法。' if not dynamic and len(visible)>1 else
                         '当前已经符合目标，GT不需要拆装。' if not dynamic else
                         '这是正常拼装题，下方展示GT怎样完成目标。'))
        if case.get('referenceRepairNote'):value['description']+=' '+case['referenceRepairNote']
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
            # This is an explicitly answer-visible GT audit. Frame the actual
            # first incident (or static discrepancy), not the entire building.
            # This private crop is NEVER added to model observation packets.
            event=next((f for f in b['frames'] if f['kind']=='incident'),None)
            before,after=(event['before'],event['state']) if event else (b['current'],b['goal'])
            changed={a for a in set(before)|set(after) if before.get(a,'')!=after.get(a,'')}
            focus={k for state in (before,after) for a,k in state.items() if a in changed and k}
            if b['mode']=='dynamic' and not event:focus=keys
            active=[r.bounds[k] for k in focus if k in r.bounds]
            pts=np.concatenate(active or [r.bounds[k] for k in keys if k in r.bounds])
            lo,hi=pts.min(0),pts.max(0);pad=np.maximum((hi-lo)*.22,28)
            lo-=pad;hi+=pad
            r.bounds['_gt_review_focus']=np.array([[x,y,z] for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])])
            keys.update(r.cert['fixed'])
            r.bounds['_gt_review_frame']=np.concatenate([r.bounds[k] for k in keys if k in r.bounds])
        return r

    def image(self,code,which,view,step=None,scope='focus'):
        if code not in self.server.maps['gt'] or view not in ANGLES:raise ValueError('图片无效')
        b=self.bundle(code)
        if which not in ('current','result','goal','step','before','context'):raise ValueError('图片无效')
        if scope not in ('focus','whole'):raise ValueError('取景无效')
        if which in ('step','before') and (type(step) is not int or not 0<=step<len(b['frames'])):raise ValueError('步骤无效')
        path=self.folder(code)/f'{which}-{step if step is not None else "main"}-{view}-{scope}.png'
        if path.exists():return path
        r=self.renderer(code);f=b['frames'][step] if which in ('step','before') else None
        state=(f.get('before',f['state']) if which=='before' else f['state']) if f else b['current' if which=='context' else which]
        frame='_gt_review_frame' if scope=='whole' or which=='context' else '_gt_review_focus'
        # Step closeups frame the moved brick and its immediate surroundings.
        # All scene geometry remains rendered; the camera never removes occluders.
        if f and f.get('key') and scope=='focus':
            pts=r.bounds[f['key']];lo,hi=pts.min(0),pts.max(0);pad=np.maximum((hi-lo)*.55,32)
            lo-=pad;hi+=pad
            frame='_gt_step_'+str(step)
            r.bounds[frame]=np.array([[x,y,z] for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])])
        size=(1200,900) if which!='context' else (480,360)
        image,mask=r.rgb(state,'isometric',angles=ANGLES[view],size=size,frame_keys=[frame],supersample=1)
        if f and f.get('actor') and (f['kind']=='attach' and which=='step' or f['kind']=='detach' and which=='before'):
            selected=Image.fromarray(np.uint8(mask==r.ids[f['actor']])*255)
            grown=np.asarray(selected.filter(ImageFilter.MaxFilter(7))).astype(int)
            border=Image.fromarray(np.uint8(np.maximum(0,grown-np.asarray(selected).astype(int))))
            image.paste((0,151,164),(0,0),border)
        if which=='context':
            from vision import _camera
            camera=_camera('isometric',ANGLES[view]);full=r.bounds['_gt_review_frame']@camera
            lo,hi=full.min(0),full.max(0);center=(lo+hi)/2
            scale=min(size[0]*.88/max(hi[0]-lo[0],1),size[1]*.88/max(hi[1]-lo[1],1))
            pts=r.bounds['_gt_review_focus']@camera
            xy=np.c_[(pts[:,0]-center[0])*scale+size[0]/2,-(pts[:,1]-center[1])*scale+size[1]/2]
            a=xy.min(0);z=xy.max(0);ImageDraw.Draw(image).rectangle([*a,*z],outline='#0097a4',width=3)
        temporary=path.with_suffix('.pending.png');image.save(temporary);temporary.replace(path)
        return path

    def previous(self,person,code):
        candidates=[]
        for p in (self.server.data/person/'gt').glob('*/'+code+'/review.json'):
            value=read(p)
            if value.get('previewVersion')!=self.version and value.get('submitted'):candidates.append(value)
        return max(candidates,key=lambda x:x.get('submittedAt',0),default=None)

    def default_view(self,code):
        # Private answer-visible audit only. Choose a useful initial oblique
        # view of the actual discrepancy; do not change model observations.
        path=self.folder(code)/'preferred-view.json'
        if path.exists():return read(path)['view']
        b=self.bundle(code);event=next((f for f in b['frames'] if f['kind']=='incident'),None)
        reference=event['before'] if event else b['goal'];r=self.renderer(code);scores={}
        for view in ('isometric','rear','left'):
            current=Image.open(self.image(code,'current',view)).convert('RGB')
            target,_=r.rgb(reference,'isometric',angles=ANGLES[view],size=(1200,900),frame_keys=['_gt_review_focus'],supersample=1)
            scores[view]=int(np.count_nonzero(np.max(abs(np.asarray(current).astype(int)-np.asarray(target).astype(int)),axis=2)>24))
        view=max(scores,key=scores.get);write(path,dict(view=view,changedPixels=scores,answerVisible=True))
        return view

    def needs_attention(self,code):
        return any(((self.server.state(p,'gt',code) if self.server.state(p,'gt',code).get('submitted') else self.previous(p,code)) or {}).get('choice') in ('problem','unclear') for p in ('A','B','C'))

    def public(self,person,code):
        b=self.bundle(code);saved=self.server.state(person,'gt',code)
        return {k:b[k] for k in ['code','title','mode','description','hasIncident','incidentCount','replaySuccess','failure','goalIsStage']}|dict(
            reviewVersion=REVIEW_VERSION,previewVersion=self.version,
            steps=[dict(index=i,label=f['label'],kind=f['kind']) for i,f in enumerate(b['frames'])],
            previousReview=self.previous(person,code),
            defaultView=self.default_view(code),
            stageNumber=b['stageNumber'],acceptanceParts=b['acceptanceParts'],fullParts=b['fullParts'],
            choice=saved.get('choice'),submitted=saved['submitted'],answerRevision=saved['answerRevision'])

    def summary(self):
        rows=[]
        for code in self.server.maps['gt']:
            entries=[self.server.state(p,'gt',code) for p in ('A','B','C')]
            votes=[v for v in entries if v['submitted']]
            historical=[self.previous(p,code) for p,v in zip(('A','B','C'),entries) if not v['submitted']]
            historical=[v for v in historical if v]
            counts=Counter(v['choice'] for v in votes+historical)
            status=('GT存在异议，需复查' if counts['problem'] else '画面或题意需改进' if counts['unclear'] else
                    '三人一致认为GT正确' if counts['correct']==3 else '还需其他人检查' if votes else '历史判断已保留' if historical else '待检查')
            rows.append(dict(code=code,title=self.title(code),submissions=len(votes),historicalSubmissions=len(historical),counts=dict(counts),currentCounts=dict(Counter(v['choice'] for v in votes)),status=status))
        return dict(reviewVersion=REVIEW_VERSION,answerVisible=True,isBlindHumanPerformance=False,
            submitted=sum(x['submissions'] for x in rows),historicalSubmissions=sum(x['historicalSubmissions'] for x in rows),total=len(rows),rows=rows,
            note='这是看过参考答案的GT检查，不能作为真人盲做成功率；有异议和看不清的题均保留待查。')
