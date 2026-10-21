"""Bounded visual API pilot. One model action per call, with fresh state images."""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parent))
sys.path.insert(0,str(HERE.parent/'eval'))
from dynamic_v5.episode import BANK, DynamicEpisode, load_case
from vision import VisionRenderer, images as render_images
from dynamic_v5.vision import DynamicVisionRenderer

MODEL=os.environ.get('BRICKPLAN_DYNAMIC_MODEL','google/gemini-2.5-flash')
NODE=ROOT/'.tools/node-v22.23.2-darwin-arm64/bin/node'
PILOT=BANK/'pilot'
SYSTEM='''You are physically assembling a LEGO model from an empty white plate. The target and current assemblies are shown as RGB images after EVERY action. Pieces may change between actions without a notification. Compare the latest current image to the target before deciding. You may inspect a part, candidate placement, angle, or crop at any time. Candidate IDs are anonymous registered placements and do not signal which is correct. Use the inventory image to map part handles to shapes. An attach requires partId and candidate; a detach requires partId. Inspect accepts candidate, partId, view, or view and crop. Finish only when the current assembly matches the target. Return a JSON object with exactly one action, for example {"action":{"type":"attach","partId":"A01","candidate":"C001"},"note":"brief reasoning"}. No batch of actions.'''
SYSTEM_DIAGNOSTIC=SYSTEM+' This separate diagnostic track also supplies exact current/target placement handles and every currently legal physical manipulation. Compare those maps, then choose a legal action. No event label is supplied.'
SYSTEM_MANUAL=SYSTEM+' This manual-assisted track supplies the correct original build sequence as anonymous action handles. Follow it one action at a time. Before each action, use the new CURRENT images to check whether a previously installed piece moved, vanished, or an extra piece appeared. If the structure differs from the manual and target, repair it first. The manual is not an oracle for changes that happen during your work.'
SYSTEM_MANUAL_V2=SYSTEM_MANUAL+''' The buildGuide is EXHAUSTIVE: exactly its listed actors belong in the target. All other action handles are spare or distractor parts. Never attach an actor absent from buildGuide. Once every guide actor has been installed at its guide candidate, issue finish unless a guide piece is missing or an extra piece is visible. If a move is rejected, do not repeat it in the same state: use the blocker ID and latest image to correct the state first. A failed attach leaves that piece in the rack; never detach it as though it were installed.'''
SYSTEM_MANUAL_V3=SYSTEM_MANUAL_V2+''' The manualProgress field counts buildGuide actions you successfully executed at least once. It is only a history counter: a hidden change can undo a completed step. When manualProgress reaches the total, compare the current image with target and finish if they match. Do not search the actionHandles for further target pieces: the buildGuide is the complete target list.'''
SYSTEM_VISUAL_V5=SYSTEM+''' The white stud grid is a fixed visual coordinate reference. To discover placement handles, inspect a partId: the next observation includes an exhaustive visual catalog of that actor's registered candidate placements. Catalog entries do not indicate correctness or physical legality. Compare the catalog with the target and the latest current image. An inspection uses one decision but does not change the assembly.'''
SYSTEM_VISUAL_V6=SYSTEM_VISUAL_V5+''' For each actor you consider attaching, first issue inspect with that partId and study its candidate-catalog image before choosing a candidate. Do not guess candidate IDs from their numbering or the order in actionHandles. After a rejected attach, the piece is still in the rack; choose a different action using the latest images instead of detaching a rack piece. Inventory contains distractors, so attaching every actor is not a valid plan.'''
SYSTEM_TEMPORAL=SYSTEM_VISUAL_V6+''' From the second decision onward, every view has a BEFORE-LAST-ACTION image immediately followed by CURRENT and TARGET images. BEFORE is the scene just before your last action; CURRENT is the scene after it and any unannounced environmental change. Compare the pair after every move, accounting for the move you attempted. An inspect does not move pieces. Candidate catalog cards show every registered placement in the current scene, with the inspected part outlined in cyan; the outline does not mark correctness or legality. No target-only part isolation is available. To attach, either use a candidate ID or click its catalog card with catalogPage (1-based) and catalogPoint [x,y] normalized over the whole catalog image. A click anywhere on a card selects that candidate.'''
SYSTEM_MONITOR=SYSTEM_MANUAL_V3+''' From the second decision onward, every view has a BEFORE-LAST-ACTION image immediately followed by CURRENT and TARGET images. BEFORE is the scene just before your last action; CURRENT is after that action and any unannounced environmental change. Compare the pair and the original buildGuide after every move. A successful action does not guarantee that other pieces stayed in place. Candidate catalog cards show every registered placement in the current scene with the candidate part outlined in cyan; no target-only part isolation is available. To attach, either use the guide's candidate ID or click its catalog card with catalogPage (1-based) and catalogPoint [x,y] normalized over the whole catalog image.'''
SYSTEM_MONITOR_V2='''You are assembling the pictured LEGO object one action at a time. The buildGuide is the complete, correct NORMAL assembly plan, and nextUnexecutedGuideAction identifies the next guide step that your own action history has not yet executed successfully. That field is only a history aid: an unannounced environmental change may have undone an earlier step. Each view shows BEFORE-LAST-ACTION, CURRENT, and TARGET images. BEFORE is immediately before your last move; CURRENT is after that move and any unseen environmental change. Check whether CURRENT contains every guide piece you already installed, plus any unexpected extra or misplaced piece. Future guide pieces missing from an unfinished model are normal. If the scene is consistent with your own actions, execute nextUnexecutedGuideAction exactly. If a previously installed piece vanished or changed, fix it before continuing. Never attach a part absent from buildGuide; it can only be an extra to remove. Do not detach a correctly placed guide part simply because the final target includes later pieces. An OK feedback means your requested move was legal, not that all earlier pieces stayed in place. Finish only after all guide steps have been done and CURRENT matches TARGET. Return exactly one JSON object: {"action":{"type":"attach","partId":"A01","candidate":"C001"},"note":"short reason"}. You may instead use detach, inspect, or finish. No batch. Candidate catalog cards show all registered placements without correctness/legality marks; the candidate part is outlined in cyan. No target-only part isolation is available.'''
SYSTEM_VISUAL_V9=SYSTEM_VISUAL_V6+''' For each view, the BEFORE LAST ACTION scene is on the LEFT and CURRENT NOW is on the RIGHT of ONE labeled comparison image. A separate labeled FINAL TARGET image shows the unchanged goal. At the first decision the left panel says NO PRIOR ACTION. Compare left to right, accounting for your last move; do not swap their meanings. All candidate cards show the inspected part in the current scene with a cyan outline, not correctness. You can attach using a candidate ID or by clicking its catalog card with catalogPage and normalized catalogPoint [x,y]. No target-only part isolation is available.'''
SYSTEM_VISUAL_V10=SYSTEM_VISUAL_V9+''' At EVERY decision also return JSON boolean unexpectedChange: true only if you observe a new environmental change beyond the effect of your own previous action; false otherwise. The left and right panels are two states of the same one assembly, not duplicate pieces. First decision must be false. This flag is a separate detection answer and does not replace the one action. Example: {"action":{"type":"inspect","partId":"A01"},"unexpectedChange":false,"note":"short reason"}.'''
SYSTEM_MONITOR_V3=SYSTEM_MONITOR_V2.replace('Each view shows BEFORE-LAST-ACTION, CURRENT, and TARGET images. BEFORE is immediately before your last move; CURRENT is after that move and any unseen environmental change.', 'For each view, ONE labeled comparison image has BEFORE LAST ACTION on the LEFT and CURRENT NOW on the RIGHT; a separate labeled FINAL TARGET image shows the unchanged goal. The first comparison has NO PRIOR ACTION on the left. Do not swap left and right. CURRENT is after your last move and any unseen environmental change.')
SYSTEM_MONITOR_V4=SYSTEM_MONITOR_V3+''' At EVERY decision, also return a JSON boolean unexpectedChange: true only when the scene contains an unexpected change beyond the effect of your own last action; false otherwise. Base it on the paired scene and your executed guide history. Example: {"action":{"type":"attach","partId":"A01","candidate":"C001"},"unexpectedChange":false,"note":"short reason"}. The boolean is a separate detection judgment; you must still take one action.'''
SYSTEM_MONITOR_V5='''You are assembling the pictured LEGO object one action at a time. The buildGuide is the complete normal build plan. At every decision after the first, each comparison image shows TWO ALTERNATIVE STATES OF THE SAME SINGLE ASSEMBLY at the same moment: LEFT = EXPECTED AFTER YOUR ACTION if nothing else happened; RIGHT = ACTUAL NOW after your action and any unseen environmental change. Two panels do not mean two sets of pieces. Compare left and right within the same view. If they match, unexpectedChange must be false; do not count pieces across panels or across the isometric and top views. The FINAL TARGET images are a separate goal, not part of the current scene. The first decision has no prior action, so unexpectedChange is false. The buildGuide and nextUnexecutedGuideAction summarize only your successful guide actions; an unseen change may undo an earlier one. If left and right differ, identify the difference and repair the actual assembly before following the next normal guide action. An OK feedback confirms only your requested move, not that the environment stayed still. Finish only when the actual assembly matches the final target. Return one JSON object with exactly one action, a boolean unexpectedChange, and a short note: {"action":{"type":"attach","partId":"A01","candidate":"C001"},"unexpectedChange":false,"note":"short reason"}. Other actions are detach, inspect, or finish. Candidate IDs are anonymous registered placements; inspecting a part shows all its candidate cards in current-scene context with the candidate part outlined in cyan. No target-only part isolation is available.'''

def dump(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    tmp.replace(path)

def request(model,observation,records,directory,system=SYSTEM,dialogue=None):
    content=[{'type':'text','text':json.dumps(observation,ensure_ascii=False,separators=(',',':'))}]
    for item in records:
        path=directory/item['file'];data=path.read_bytes()
        assert hashlib.sha256(data).hexdigest()==item['sha256']
        content.append({'type':'text','text':json.dumps({k:v for k,v in item.items() if k not in ('file','sha256','detail')},separators=(',',':'))})
        content.append({'type':'image_url','image_url':{'url':'data:image/png;base64,'+base64.b64encode(data).decode(),'detail':'high'}})
    return dict(model=model,messages=[dict(role='system',content=system),*(dialogue or []),dict(role='user',content=content)])

def call(payload):
    proc=subprocess.run([str(NODE),'--import','tsx',str(HERE/'call_api.ts')],cwd=ROOT,
                        input=json.dumps(payload),text=True,capture_output=True,timeout=115)
    if proc.returncode:
        reason=re.search(r'(Budget limit reached|Unsettled charge|OpenRouter HTTP \d{3}|Missing API key|Model price exceeds preset ceiling|Model no longer accepts images)',proc.stderr)
        raise RuntimeError(reason.group(0) if reason else 'API adapter failed; inspect private stderr locally')
    return json.loads(proc.stdout)

def parse(content):
    try:
        obj=json.loads(content)
        action=obj['action']
        if not isinstance(action,dict) or action.get('type') not in ('attach','detach','inspect','finish'):
            raise ValueError('Invalid action')
        return action,obj.get('note',''),obj.get('unexpectedChange') if type(obj.get('unexpectedChange')) is bool else None
    except (ValueError,KeyError,TypeError):
        return {'type':'invalid'},'format_error',None

def diagnostic(ep,observation):
    observation['track']='symbolic-diagnostic-with-rgb'
    observation['current']={ep.alias[a]:ep.pose(k) if k else None for a,k in ep.state.items()}
    observation['target']={ep.alias[a]:ep.pose(k) if k else None for a,k in ep.runtime.goal.items()}
    legal=[]
    for actor,key in ep.state.items():
        options=[dict(type='detach',partId=actor)] if key else [dict(type='attach',partId=actor,candidate=k) for k in ep.case['choices'][actor]]
        for action in options:
            _,feedback=ep.runtime.check(ep.state,actor,action['type'],candidate=action.get('candidate'))
            if feedback['code']=='OK':
                public={'type':action['type'],'partId':ep.alias[actor]}
                if 'candidate' in action:public['candidate']=ep.pose(action['candidate'])
                legal.append(public)
    observation['legalActions']=legal
    observation['assistance']='Privileged diagnostic: exact handles and legal-action mask, computed from current state only. Scores must not mix with visual track.'
    return observation

def run(case_id,max_calls=40,track='visual',seed=41):
    cert,case=load_case(case_id)
    ep=DynamicEpisode(cert,case,seed=seed)
    temporal=track in ('visual-v8','monitor-v1','monitor-v2','visual-v9','visual-v10','monitor-v3','monitor-v4','monitor-v5')
    paired_layout=track in ('visual-v9','visual-v10','monitor-v3','monitor-v4','monitor-v5')
    renderer=DynamicVisionRenderer(ep.cert,ep.runtime) if track in ('visual-v5','visual-v6','visual-v7','manual-v5','visual-v8','monitor-v1','monitor-v2','visual-v9','visual-v10','monitor-v3','monitor-v4','monitor-v5') else VisionRenderer(ep.cert)
    if isinstance(renderer,DynamicVisionRenderer) and track not in ('visual-v7','visual-v8','monitor-v1','monitor-v2','visual-v9','visual-v10','monitor-v3','monitor-v4','monitor-v5'):
        renderer.no_target_isolation=False  # Archived pilot interface.
    if temporal:renderer.catalog_in_context=True
    ep.vision_renderer=renderer
    run_id=case_id if track=='visual' else case_id+'--'+track
    if seed!=41:
        run_id+=f'--seed-{seed}'
    out=(PILOT/'latest-runs'/MODEL.replace('/','--')/run_id
         if MODEL!='google/gemini-2.5-flash' else PILOT/'runs'/run_id)
    out.mkdir(parents=True,exist_ok=True)
    file=out/'trace.json'
    if file.exists():
        existing=json.loads(file.read_text())
        if existing.get('status') in ('complete','call_budget','api_error'):
            return existing
        raise RuntimeError('Incomplete existing trace requires manual review')
    system={'visual':SYSTEM,'visual-v4':SYSTEM,'visual-v5':SYSTEM_VISUAL_V5,'visual-v6':SYSTEM_VISUAL_V6,'visual-v7':SYSTEM_VISUAL_V6,'visual-v8':SYSTEM_TEMPORAL,'visual-v9':SYSTEM_VISUAL_V9,'visual-v10':SYSTEM_VISUAL_V10,'monitor-v1':SYSTEM_MONITOR,'monitor-v2':SYSTEM_MONITOR_V2,'monitor-v3':SYSTEM_MONITOR_V3,'monitor-v4':SYSTEM_MONITOR_V4,'monitor-v5':SYSTEM_MONITOR_V5,
            'diagnostic':SYSTEM_DIAGNOSTIC,'manual':SYSTEM_MANUAL,
            'manual-v2':SYSTEM_MANUAL_V2,'manual-v3':SYSTEM_MANUAL_V3,
            'manual-v4':SYSTEM_MANUAL_V3,'manual-v5':SYSTEM_MANUAL_V3}[track]
    build_guide=json.loads((BANK/'models'/case['modelId']/'evidence.json').read_text())['buildWitness']
    result=dict(caseId=case_id,model=MODEL,protocol='brickplan-dynamic/5',track=track,seed=seed,
                imageInterface=('single-labeled-expected-actual-panel-plus-target' if track=='monitor-v5' else
                                'single-labeled-before-current-panel-plus-target' if paired_layout else
                                'paired-before-current-target-grid-context-catalog') if temporal else ('grid-catalog-no-target-isolation' if track=='visual-v7' else None),
                conversationMode='persistent-text-history' if track in ('visual-v4','manual-v4','visual-v5','visual-v6','visual-v7','manual-v5','visual-v8','monitor-v1','monitor-v2','visual-v9','visual-v10','monitor-v3','monitor-v4','monitor-v5') else 'current-observation-and-recent-feedback',
                startedAt=datetime.now(timezone.utc).isoformat(),
                status='running',systemPrompt=system,maxCalls=max_calls,steps=[],costUSD=0)
    dump(file,result);extra=None;dialogue=[];previous_state=None
    for index in range(max_calls):
        observation=ep.observe()
        if track=='diagnostic':diagnostic(ep,observation)
        if track in ('manual','manual-v2','manual-v3','manual-v4','manual-v5','monitor-v1','monitor-v2','monitor-v3','monitor-v4','monitor-v5'):
            observation['track']='manual-assisted-rgb'
            observation['buildGuide']=[dict(type='attach',partId=ep.alias[a['partId']],candidate=ep.pose(a['candidate'])) for a in build_guide]
            observation['assistance']='The original build manual; it does not describe disturbances or repairs.'
            if track in ('manual-v3','manual-v4','manual-v5','monitor-v1','monitor-v2','monitor-v3','monitor-v4','monitor-v5'):
                guide={json.dumps(a,sort_keys=True) for a in observation['buildGuide']}
                def normalized_guide_action(action):
                    if action.get('type')=='attach' and 'catalogPoint' in action:
                        key=ep.catalog_click_candidate(action)
                        return dict(type='attach',partId=action.get('partId'),candidate=ep.pose(key) if key else None)
                    return action
                done={json.dumps(normalized_guide_action(r['action']),sort_keys=True) for r in ep.records
                      if r['feedback']['code']=='OK' and json.dumps(normalized_guide_action(r['action']),sort_keys=True) in guide}
                observation['manualProgress']={'executedAtLeastOnce':len(done),'total':len(guide),
                                               'warning':'History only; parts may have changed after execution.'}
                if track in ('monitor-v2','monitor-v3','monitor-v4','monitor-v5'):
                    observation['nextUnexecutedGuideAction']=next((a for a in observation['buildGuide']
                        if json.dumps(a,sort_keys=True) not in done),None)
        if temporal:
            observation['track']='temporal-monitor-with-original-guide' if track.startswith('monitor-') else 'temporal-visual'
            observation['visualTiming']=({'expectedAfterAction':'Scene after your last action only; absent at first decision.',
                                          'actualNow':'Scene after your last action and any unannounced change.',
                                          'target':'Unchanging final goal.',
                                          'views':['isometric','top'],
                                          'pairAvailable':previous_state is not None,
                                          'layout':'one labeled left-expected/right-actual panel plus separate labeled target'}
                                         if track=='monitor-v5' else
                                         {'beforeLastAction':'Scene immediately before the last action; absent at first decision.',
                                          'current':'Scene after the last action and any unannounced change.',
                                          'target':'Unchanging final goal.',
                                          'views':['isometric','top'],
                                          'pairAvailable':previous_state is not None,
                                          'layout':'one labeled left-before/right-current panel plus separate labeled target' if paired_layout else 'three separate images'})
            if track in ('visual-v10','monitor-v4','monitor-v5'):
                observation['responseSchema']['unexpectedChange']='boolean: environmental change beyond own last action'
        records=render_images(ep,renderer,out,extra,views=('isometric','top'),
                              previous_state=previous_state if temporal else None,paired_layout=paired_layout,
                              expected_state=ep.expected_after_last_action if track=='monitor-v5' else None)
        step=dict(index=index,observation=observation,images=records,beforeSha256=hashlib.sha256(json.dumps(ep.state,sort_keys=True).encode()).hexdigest(),status='requesting')
        result['steps'].append(step);dump(file,result)
        payload=request(MODEL,observation,records,out,system,dialogue)
        step['priorDialogue']=dialogue.copy()
        try:response=call(payload)
        except Exception as exc:
            result.update(status='api_error',error=str(exc),score=ep.score(),event=ep.event)
            dump(file,result);return result
        step['response']=response;result['costUSD']+=response['cost']
        action,note,reported_change=parse(response['content'])
        previous_state=ep.assignments() if temporal else None
        feedback=ep.step(action)
        if track in ('visual-v4','manual-v4','visual-v5','visual-v6','visual-v7','manual-v5','visual-v8','monitor-v1','monitor-v2','visual-v9','visual-v10','monitor-v3','monitor-v4','monitor-v5'):
            dialogue.append(dict(role='assistant',content=response['content']))
            dialogue.append(dict(role='user',content=json.dumps(dict(toolFeedback=feedback,
                instruction='Continue the same build episode. Review the next current images before acting.'),separators=(',',':'))))
        step.update(action=action,note=note,reportedUnexpectedChange=reported_change,
                    feedback=feedback,afterSha256=hashlib.sha256(json.dumps(ep.state,sort_keys=True).encode()).hexdigest(),status='executed')
        extra=({'partId':feedback['partId']} if 'partId' in feedback else action) if action.get('type')=='inspect' and feedback['code']=='OBSERVED' else None
        result.update(score=ep.score(),event=ep.event)
        dump(file,result)
        print(json.dumps(dict(case=case_id,step=index+1,action=action,feedback=feedback,costUSD=result['costUSD'],eventTriggered=bool(ep.event)),ensure_ascii=False),flush=True)
        if ep.finished:break
    result.update(status='complete' if ep.finished else 'call_budget',finishedAt=datetime.now(timezone.utc).isoformat(),
                  score=ep.score(),event=ep.event,episode=ep.export())
    if track in ('visual-v10','monitor-v4','monitor-v5'):
        event_decision=ep.event['atRecord']+1 if ep.event else None
        result['detectionReport']=dict(eventDecisionIndex=event_decision,
             declaredAtEvent=next((s.get('reportedUnexpectedChange') for s in result['steps']
                                   if s['index']==event_decision and s.get('status')=='executed'),None),
             preEventFalseAlarms=sum(s.get('reportedUnexpectedChange') is True for s in result['steps']
                                     if s.get('status')=='executed' and (event_decision is None or s['index']<event_decision)))
    dump(file,result)
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',action='append',required=True)
    parser.add_argument('--calls',type=int,default=40)
    parser.add_argument('--seed',type=int,default=41)
    parser.add_argument('--track',choices=['visual','visual-v4','visual-v5','visual-v6','visual-v7','visual-v8','visual-v9','visual-v10','diagnostic','manual','manual-v2','manual-v3','manual-v4','manual-v5','monitor-v1','monitor-v2','monitor-v3','monitor-v4','monitor-v5'],default='visual')
    args=parser.parse_args()
    for case in args.case:
        r=run(case,args.calls,args.track,args.seed)
        print(json.dumps({k:r.get(k) for k in ('caseId','status','costUSD','score','error')},ensure_ascii=False),flush=True)
        if r['status']=='api_error':break
