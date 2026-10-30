"""Meaningful no-API checks: payload bounds, current-state pairing, references."""
from pathlib import Path
import argparse,json,hashlib
from copy import deepcopy
from bench_design.session import Session,digest
from dynamic_arena.tool_arena import ToolArena,parse,PROTOCOL
from dynamic_arena.validate_replays import Witness
from reliability.run import Offline
from reliability.paired import fork,score,state_contract
from reliability import OUT
from expansion_v7.build import write

STATIC='E7:v7::v7-long-bookshelf::static::wrong-color::t14'
DYNAMIC='SC:158-1:dynamic:missing'

def runner(cid,path,control=False):
 s=Session.open(cid,path,'scripted:reliability-check',control=control);s.autosave=False
 a=ToolArena(s,Offline(),min(80,s.cap))
 a.spectator_frame=lambda *args,**kw:None
 return a

def perform(a,action):return a.step(json.dumps(action))

def complete(a):
 witness=Witness(a.session)
 while not a.session.done and len(a.calls)<a.cap:perform(a,json.loads(witness({})))
 old=getattr(a.session,'autosave',True);a.session.autosave=True;a.session.save();a.session.autosave=old
 write(a.session.directory/'log.json',dict(protocol=PROTOCOL,calls=a.calls,result=a.result()))
 write(a.session.directory/'result.json',a.result())
 assert a.result()['success'],(a.session.row['key'],a.result())
 return a.result()

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=OUT/'checks');p.add_argument('--community-only',action='store_true')
 opts=p.parse_args();out=opts.output
 a=runner('SC:158-1:static:missing' if opts.community_only else STATIC,out/'preview-static')
 assert not a.request()[3]
 obs=perform(a,dict(tool='observe',args=dict(view='angled',rotateDegrees=0,show=['current','target','inventory'])))
 assert len(obs['images'])==2 and obs['images'][0]['role']=='current-target'
 assert obs['images'][0]['width']==1600 and obs['images'][0]['height']==636
 assert len(obs['inventoryAvailability'])<=12
 actor=a.public_request()['actionHandles'][0]['id']
 perform(a,dict(tool='inspect',args=dict(partId=actor,page=1)))
 assert len(a.request()[3])==1
 before=deepcopy(a.session.ep.state)
 rejected=perform(a,dict(tool='inspect',args=dict(partId=actor,page=999999)))
 assert rejected['code']=='INVALID_SENSOR_REQUEST' and a.session.ep.state==before and not a.request()[3]
 complete(a)
 assert max(a.result()['inputMetrics']['imageCounts'])<=2
 normal=runner(DYNAMIC,out/'preview-normal',True);normal_result=complete(normal)
 retained=runner('D:obj-city-car--t5--removed_piece--v01',out/'preview-retained-normal',True)
 retained_normal=complete(retained)
 retained_incident=runner('D:obj-city-car--t5--removed_piece--v01',out/'preview-retained-incident')
 retained_recovery=complete(retained_incident)
 assert retained_recovery['appliedEvents']==1
 origin=runner(DYNAMIC,out/'preview-prefix');witness=Witness(origin.session)
 while not origin.session.events:perform(origin,json.loads(witness({})))
 origin.session.normal_gate=dict(eligible=True,normalRunId=normal.session.directory.name,sameCase=True,sameModel=True,sharedPrefixVerified=False)
 branches,proof=fork(origin,out/'pair')
 for b in branches.values():b.spectator_frame=lambda *args,**kw:None
 assert digest(state_contract(branches['continuing']))==digest(state_contract(branches['fresh']))
 assert branches['continuing'].history and not branches['fresh'].history
 look=dict(tool='observe',args=dict(view='angled',rotateDegrees=0,show=['current','target','inventory']))
 for b in branches.values():perform(b,look)
 assert [i['sha256'] for i in branches['continuing'].pending_images]==[i['sha256'] for i in branches['fresh'].pending_images]
 for b in branches.values():complete(b)
 paired=score(branches,proof,out/'pair');assert paired['valid'] and paired['completionDifference']==0
 # A technical interruption must not be interpreted as an ability failure.
 branches['fresh'].session.terminal='service_error'
 invalid=score(branches,proof,out/'invalid-pair');assert not invalid['valid'] and invalid['completionDifference'] is None
 branches['fresh'].session.terminal='completed'
 write(out/'report.json',dict(passed=True,protocol=PROTOCOL,apiCalls=0,modelPerformance=False,
     defaultImages=0,maxRequestedImages=2,oneCandidatePage=True,invalidPageNoStateChange=True,
     staticComplete=True,normalComplete=normal_result['success'],effectiveEvent=True,
     retainedNormalComplete=retained_normal['success'],retainedRecoveryComplete=retained_recovery['success'],
     sameStateGoalInventoryToolsBudget=True,sameRequestedImageHashes=True,
     matchedBranchesCompleted=True,technicalFailureExcluded=True,
     staticInputImageCounts=a.result()['inputMetrics']['imageCounts']))
 print(json.dumps(__import__('json').loads((out/'report.json').read_text()),indent=2))

if __name__=='__main__':main()
