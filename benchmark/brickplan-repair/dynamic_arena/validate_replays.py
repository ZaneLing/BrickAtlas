"""Visible scripted end-to-end checks. These never pretend to be model runs."""
from copy import deepcopy
import json,time
from dynamic_arena import OUT
from dynamic_arena.run import open_session
from dynamic_arena.tool_arena import ToolArena
from bench_design.session import internal_action
from dynamic_v6.episode import continuation
from expansion_v7.build import write

CASES=[
 ('chair','D:obj-chair--t3--compound_fault--v01'),
 ('bookshelf','E7:v7::v7-long-bookshelf::dynamic::missing::t14'),
 ('truck','QN:truck-cab-30024::dynamic::missing'),
 ('overlap','QX:quality::v7-long-bookshelf::repair-overlap'),
 ('inventory','QI:horizontal::dynamic-shortage'),
 ('railroad','A4:arena-158-1::missing'),
]

class Witness:
    model='程序动作检查 · 非 API 模型'
    def __init__(self,s):
        self.s=s;self.calls=0;self.latest=None;self.seen=0;self.pending_observation=False
        case=s.ep.case
        if s.row['bank']=='QI':self.queue=deepcopy(case['normalReferenceActions'] if s.control else case['referenceActions']);self.scripted_events=True
        elif s.row.get('evaluationMetadata',{}).get('taskType')=='S0':
            # A correct intermediate stage is already complete. An empty
            # reference must not fall through to the full-object manual.
            self.queue=[];self.scripted_events=True
        elif not s.control and case.get('referenceActions'):
            self.queue=deepcopy(case['referenceActions']);self.scripted_events=True
        else:
            self.queue=deepcopy(s.packet.manual['actions']) if s.packet and hasattr(s.packet,'manual') else continuation(s.ep.runtime,s.ep.state)
            assert self.queue is not None
            self.scripted_events=False
    def __call__(self,payload):
        self.calls+=1
        if self.calls==1 or self.pending_observation:
            self.pending_observation=False
            action=dict(tool='observe',args=dict(view='angled',rotateDegrees=0 if self.calls==1 else 90,show=['current','target','inventory']))
        else:
            if len(self.s.events)>self.seen:
                event=self.s.events[-1]['native'];self.seen=len(self.s.events)
                if not self.scripted_events:
                    if 'recoveryWitness' in event:self.queue=deepcopy(event['recoveryWitness'])
                    else:self.queue=deepcopy(event['recovery'])+self.queue
            while self.queue:
                a=self.queue.pop(0);actor=a.get('actor',a.get('partId'));current=self.s.ep.state.get(actor)
                if a['type']=='detach' and not current:continue
                if a['type']=='attach' and current==a['candidate']:continue
                public=internal_action(self.s.ep,a);action=dict(tool=public.pop('type'),args=public);break
            else:action=dict(tool='finish',args={})
            if action['tool']!='finish':self.pending_observation=True
        self.latest=dict(result=dict(id='scripted-'+str(self.calls),usage=dict(cost=0,prompt_tokens=0,completion_tokens=0)),requestBodySha256='0'*64)
        return json.dumps(action)
    def usage(self):return dict(calls=0,costUSD=0.,capUSD=0.)


def main():
    results=[]
    for name,cid in CASES:
        for normal in [True,False]:
            tag='normal' if normal else 'incident';runid=f'check-{name}-{tag}-v3'
            print('REPLAY',runid,flush=True)
            s=open_session(cid,OUT/'runs'/runid,'scripted:reference-validation',normal);s.autosave=False
            arena=ToolArena(s,Witness(s),s.cap)
            r=arena.run();assert r['success'],(runid,r['terminalStatus'],r['stateMetrics'])
            assert not normal or r['appliedEvents']==0
            assert normal or r['appliedEvents']>0
            results.append(dict(runId=runid,caseId=cid,normal=normal,success=r['success'],appliedEvents=r['appliedEvents'],decisions=len(arena.calls),metrics=r))
            print('PASS',runid,len(arena.calls),r['appliedEvents'],flush=True)
    write(OUT/'migration-replay-check.json',dict(apiCalls=0,passed=True,runs=results,notModelPerformance=True))


if __name__=='__main__':main()
