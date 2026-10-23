"""Complete objects and named modules, retaining full object context in images."""
import argparse
import json
import sys
import uuid
import numpy as np
from recognizable_models import ROOT, OUT
from recognizable_models.specs import MODULE_IDS
from community_modules.core import Episode as NativeModuleEpisode
from community_modules.run_episode import ModulePacket
from community_modules.specs import SPECS
from expansion_v7.build import read,write
from expansion_v7.runtime import Episode as NativeEpisode
from expansion_v7.run_episode import Packet


class Episode(NativeEpisode):
    def observe(self):
        obs=super().observe()
        if self.case['mode']=='static':
            step=self.case['completedInstructionStep']
            obs['task']=f'修复当前场景，使其符合 TARGET（说明第 {step} 步的阶段目标）。不是从空白底板重搭。后续成品仅供参考；允许其他合法修复顺序，一次只装或拆一块。'
        return obs


class CompletionEpisode(NativeModuleEpisode):
    def observe(self):
        obs=super().observe()
        spec=next(s for s in SPECS if s['id']==self.case['module'])
        obs['startingStateDescription']=spec['explanation']
        obs['fullObjectContextShown']=True
        return obs


class CompletionPacket(ModulePacket):
    def __init__(self,ep,module,directory):
        super().__init__(ep,module,directory)
        keys=list(self.renderer.cert['fixed'])+[k for k,r in ep.cert['candidates'].items() if r['kind']=='goal']
        self.renderer.bounds['_module_frame']=np.concatenate([self.renderer.bounds[k] for k in keys])


def load_episode(case_id,seed=41,directory=None):
    directory=directory or OUT/'runs'/uuid.uuid4().hex
    row=next((r for r in read(OUT/'case-index.json')['cases'] if r['id']==case_id),None)
    if row:
        folder=OUT/'models'/row['module'];cert=read(folder/'certificate.private.json.gz')
        case=next(c for c in read(folder/'cases.private.json.gz') if c['id']==case_id)
        ep=Episode(cert,case,seed)
        return ep,Packet(ep,read(folder/'manual.private.json.gz'),directory)
    for mid in MODULE_IDS:
        folder=ROOT/'deliverables/brickplan-community-modules'/mid
        case=next((c for c in read(folder/'cases.private.json') if c['id']==case_id),None)
        if case is None:continue
        cert=read(folder/'certificate.private.json');ep=CompletionEpisode(cert,case,seed)
        module=next(m for m in read(folder.parent/'gallery-data.js.json') if m['id']==mid)
        return ep,CompletionPacket(ep,module,directory)
    raise ValueError('Unknown complete-object or named-completion case')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--case',required=True)
    parser.add_argument('--seed',type=int,default=41);args=parser.parse_args()
    directory=OUT/'runs'/uuid.uuid4().hex;ep,packet=load_episode(args.case,args.seed,directory)
    print(json.dumps(packet.observation(),ensure_ascii=False),flush=True)
    for line in sys.stdin:
        try:action=json.loads(line)
        except json.JSONDecodeError:action={'type':'invalid'}
        try:ep.step(action)
        except (ValueError,KeyError,TypeError) as exc:
            ep.previous=dict(ep.state);ep.feedback=dict(code='INVALID_REQUEST',message=str(exc))
        print(json.dumps(packet.observation(),ensure_ascii=False),flush=True)
        if ep.done:break
    write(directory/'record.private.json.gz',dict(caseId=args.case,score=ep.score(),history=ep.history,
        events=getattr(ep,'events',None),finalState=ep.state))


if __name__=='__main__':main()
