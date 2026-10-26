"""Shared execution, private incident ledger, and normalized evaluation records.

The CLI, scripted checks, and human interface use this same path. No score,
incident label, pose truth, or recovery witness is included in public packets.
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import uuid
import math
from bench_design.metrics import state_metrics, execution_metrics, event_recovery, pair_metrics
from bench_design.policy import INPUT_VERSION as CATALOGUE_INPUT_VERSION
from expansion_v7.build import write
INPUT_VERSION='brick-atlas-direct-actions-full-context/2'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def events_of(ep):
    if hasattr(ep, 'events'):
        return ep.events
    event = getattr(ep, 'event', None) or getattr(ep, 'last_event', None)
    return [event] if event else []


def scheduled_of(ep):
    c = ep.case
    if hasattr(ep, 'schedule'):
        return len(ep.schedule)
    if 'events' in c:
        return len(c['events'])
    return int(bool(c.get('privateEvent') or c.get('event')))


def alias_maps(ep):
    return dict(parts=getattr(ep, 'actor_alias', getattr(ep, 'alias', {})),
                poses=getattr(ep, 'pose_alias', {}))


def disable_events(ep):
    if hasattr(ep, 'schedule'):
        ep.schedule = []
    for key in ['events', 'event', 'privateEvent']:
        if key in ep.case:
            ep.case[key] = [] if key == 'events' else None


def internal_action(ep, action):
    actor = action.get('actor', action.get('partId'))
    aliases = getattr(ep, 'actor_alias', getattr(ep, 'alias', {}))
    poses = getattr(ep, 'pose_alias', {})
    if action['type'] == 'finish':
        return dict(type='finish')
    out = dict(type=action['type'], partId=aliases[actor])
    if action['type'] == 'attach':
        out['candidate'] = poses[action['candidate']]
    return out


class Session:
    def __init__(self, row, ep, packet, renderer, directory, actor='scripted', condition=None):
        self.row, self.ep, self.packet, self.renderer = row, ep, packet, renderer
        self.directory = Path(directory).resolve()
        self.directory.mkdir(parents=True, exist_ok=True)
        self.actor, self.condition = actor, condition or row['key']
        self.initial = deepcopy(ep.state)
        self.goal = deepcopy(row['case'].get('goal', ep.runtime.goal))
        self.records, self.events, self.observations = [], [], []
        self.extra, self.terminal = None, None
        self.run_id = uuid.uuid4().hex
        self.cap = max(40, 6 * sum(bool(k) for k in self.goal.values()) + 20)
        self._pending_observation = None

    @classmethod
    def open(cls, case_id, directory, actor='scripted', diagnostic=False, control=False):
        from bench_design.run_episode import load
        row, ep, packet, renderer = load(case_id, Path(directory).resolve(), diagnostic)
        if control:
            disable_events(ep)
        result = cls(row, ep, packet, renderer, directory, actor,
                     case_id + ('/normal-branch' if control else ''))
        result.control = control
        return result

    def observe(self):
        from bench_design.run_episode import observation
        value = observation(self.row, self.ep, self.packet, self.renderer,
                            self.directory, self.extra)
        value['inputVersion']=INPUT_VERSION
        value['catalogueSnapshotInputVersion']=CATALOGUE_INPUT_VERSION
        value['responseSchema']['inspect']='type plus view/point, partId, candidate, manualStep or inventoryPage as supported'
        value['pointInspection']=dict(request=dict(type='inspect',view='isometric',point=[.5,.5]),
            pointCoordinates='Normalized CURRENT scene rectangle only; [0,36,800,636] on current-target pages.',
            output='Foremost visible movable part handle and its neutral position catalogue; no target or legality label.')
        if self.packet and self.extra and self.extra.get('partId'):
            from bench_design.catalogue_images import position_pages
            value['images'].extend(position_pages(self,self.extra['partId'],self.extra.get('view','isometric')))
            value['positionCataloguePolicy']='All registered positions, neutral ordering; cyan outlines identify only the hypothetical moving piece.'
        elif self.extra and self.extra.get('partId'):
            ep=self.ep;public_part=self.extra['partId'];actor=ep.reverse.get(public_part)
            keys=sorted(ep.case['choices'].get(actor,[]),key=ep.pose_alias.get)
            for image in value.get('images',[]):
                if image.get('role')=='candidate-catalog':
                    group=keys[(image['page']-1)*12:image['page']*12]
                    image['items']=[dict(candidate=ep.pose_alias[k],rectangle=[(i%4)*400,(i//4)*316,(i%4+1)*400,(i//4+1)*316]) for i,k in enumerate(group)]
                    image['hypothetical']=True;image['legalityOrCorrectnessShown']=False
        # These are neutral public rules, also displayed verbatim by the human UI.
        value['physicalRules'] = [
            '每次只安装或拆下一块；结束状态正确即可，不要求照参考顺序。',
            '夹具允许托住分离的子结构；本任务不模拟重力、摩擦和卡扣力度。',
            '零件不能穿过其他零件；安装和拆卸需要存在直线通路。',
            '位置预览是假设效果，按安装后才改变实际状态。']
        value['done'] = self.done
        value['decisionsUsed'] = len(self.records)
        value['outerDecisionBudget'] = self.cap
        canonical = deepcopy(value)
        for image in canonical.get('images', []):
            image.pop('file', None)
        self._pending_observation = dict(decision=len(self.records)+1,
                                        packetSha256=digest(canonical),
                                        imageHashes=[i['sha256'] for i in value.get('images', [])])
        name=f'observations/{len(self.records)+1:04}-{self._pending_observation["packetSha256"]}.json'
        self._pending_observation['packetFile']=name
        for path,data in [(self.directory/name,canonical),
                          (self.directory/'pending-observation.private.json',self._pending_observation)]:
            temporary=path.with_name(path.name+'.pending')
            write(temporary,data)
            temporary.replace(path)
        return value

    @property
    def done(self):
        return self.terminal is not None

    def submit(self, supplied, parse_error=False, request_evidence=None, client_request_id=None):
        from bench_design.run_episode import valid
        if client_request_id is not None:
            previous=next((r for r in self.records if r.get('clientRequestId')==client_request_id),None)
            if previous:return deepcopy(previous['feedback'])
        if self.done:
            raise ValueError('本题已经结束')
        if request_evidence is not None:
            value=request_evidence.get('requestContextSha256')
            if not isinstance(value,str) or len(value)!=64 or any(c not in '0123456789abcdef' for c in value):
                raise ValueError('Request evidence requires a SHA-256 of the actual full request context')
        before = deepcopy(self.ep.state)
        count = len(events_of(self.ep))
        valid_shape = valid(supplied)
        action = deepcopy(supplied) if valid_shape else {'type': 'invalid'}
        resolved=action
        no_visible=False
        if self.packet and action.get('type')=='inspect' and 'point' in action:
            point=action['point'];view=action.get('view','isometric')
            valid_point=(set(action)<={'type','point','view'} and view in ('isometric','rear','top') and
                isinstance(point,list) and len(point)==2 and all(type(x) in (int,float) and math.isfinite(x) and 0<=x<=1 for x in point))
            if not valid_point:
                resolved={'type':'invalid'};valid_shape=False
            else:
                frame=['_module_frame'] if '_module_frame' in self.packet.renderer.bounds else None
                _,mask=self.packet.renderer.rgb(self.ep.state,view,size=(800,600),supersample=1,frame_keys=frame)
                picked=int(mask[min(599,int(point[1]*600)),min(799,int(point[0]*800))])
                actor=next((a for a,idx in self.packet.renderer.ids.items() if idx==picked),None)
                if actor in self.ep.actor_alias:
                    resolved=dict(type='inspect',view=view,partId=self.ep.actor_alias[actor])
                else:
                    no_visible=True;resolved=dict(type='inspect',view=view)
        try:
            response = self.ep.step(resolved)
            fb = deepcopy(self.ep.feedback if hasattr(self.ep, 'feedback') else response)
        except (ValueError, KeyError, TypeError) as exc:
            if 'budget exhausted' in str(exc).lower():
                self.terminal = 'model_budget_exhausted'
                fb = dict(code='BUDGET_EXHAUSTED')
            else:
                fb = dict(code='INVALID_REQUEST', message=str(exc))
            if hasattr(self.ep, 'feedback'):
                self.ep.feedback = fb
        if not valid_shape:
            fb = dict(code='INVALID_REQUEST')
            if hasattr(self.ep,'feedback'):self.ep.feedback=fb
        elif no_visible:
            fb=dict(code='NO_VISIBLE_MOVABLE_PIECE')
            self.ep.feedback=fb
        fb = fb or dict(code='INVALID_REQUEST')
        new = events_of(self.ep)[count:]
        own = deepcopy(new[0].get('before', getattr(self.ep, 'expected_after_last_action', self.ep.state))) if new else deepcopy(self.ep.state)
        if own is None:
            raise ValueError('Missing pre-incident state; refusing an unverifiable event ledger')
        record = dict(decision=len(self.records)+1,
                      action=deepcopy(supplied) if isinstance(supplied, dict) else {'type': 'invalid'},
                      parseError=bool(parse_error), feedback=fb, before=before,
                      afterOwnActionBeforeExternalChange=own, after=deepcopy(self.ep.state),
                      newEventIndices=[])
        if resolved!=action:record['resolvedAction']=deepcopy(resolved)
        if client_request_id is not None:record['clientRequestId']=client_request_id
        if self._pending_observation:
            record['observation'] = deepcopy(self._pending_observation)
            self.observations.append(deepcopy(self._pending_observation))
        if request_evidence is not None:
            record['requestEvidence']=deepcopy(request_evidence)
        for native in new:
            event = self._event(native, own, self.ep.state, record['decision'])
            self.events.append(event)
            record['newEventIndices'].append(event['index'])
        self.records.append(record)
        self._pending_observation = None
        explicit = valid_shape and action['type'] == 'finish' and fb['code'] in ('FINISHED','SUCCESS','INCOMPLETE')
        if explicit:
            self.terminal = 'completed'
        elif len(self.records) >= self.cap or getattr(self.ep, 'budget_exhausted', False):
            self.terminal = 'model_budget_exhausted'
        self.extra = resolved if resolved['type'] == 'inspect' and fb['code'] in ('INSPECT','OBSERVED') else None
        if self.extra and fb.get('partId'):
            self.extra=dict(type='inspect',view=action.get('view','isometric'),partId=fb['partId'])
        self.save()
        return fb

    def _event(self, native, own, after, decision):
        before = deepcopy(native.get('before', own))
        after = deepcopy(native.get('after', after))
        changes = deepcopy(native.get('changes', native.get('transaction', [])))
        replay, checks = dict(before), []
        try:
            for move in changes:
                actor = move.get('actor', move.get('partId'))
                replay, check = self.ep.runtime.check(replay, actor, move['type'], candidate=move.get('candidate'))
                checks.append(check['code'])
            verified = bool(changes and all(c == 'OK' for c in checks) and replay == after)
        except (ValueError, KeyError, TypeError):
            verified = False
        rt = self.ep.runtime
        b, a, g = (rt.signature(s) for s in (before, after, self.goal))
        lost, excess = (b & g)-a, (a-g)-(b-g)
        obstruction = False
        for actor in native.get('blockedNextParts', []):
            key = self.goal.get(actor)
            if key:
                _, first = rt.check(before, actor, 'attach', candidate=key)
                _, second = rt.check(after, actor, 'attach', candidate=key)
                obstruction |= first['code']=='OK' and second['code']=='PATH_BLOCKED'
        return dict(index=len(self.events)+1, atDecision=decision, before=before, after=after,
                    beforeSha256=digest(before), afterSha256=digest(after),
                    changes=changes, transactionVerified=verified,
                    newlyMissingCorrectPlacements=sum(lost.values()), newExcessPlacements=sum(excess.values()),
                    processObstructionVerified=bool(obstruction),
                    effectiveIncidentVerified=bool(verified and (lost or excess or obstruction)),
                    family=native.get('family', native.get('kind')), native=deepcopy(native))

    def result(self):
        finished = self.terminal == 'completed' and bool(self.records) and self.records[-1]['action'].get('type')=='finish'
        metrics = state_metrics(self.ep.runtime, self.initial, self.ep.state, self.goal, finished=finished)
        terminal = self.terminal or 'external_stop'
        meta = self.row['evaluationMetadata']
        control = getattr(self, 'control', False)
        windows = []
        for i, event in enumerate(self.events):
            start = event['atDecision']
            next_at = self.events[i+1]['atDecision'] if i+1<len(self.events) else None
            entries = [r for r in self.records if r['decision']>start and (next_at is None or r['decision']<=next_at)]
            states = [r['afterOwnActionBeforeExternalChange'] if r['decision']==next_at else r['after'] for r in entries]
            measured = event_recovery(self.ep.runtime, event['before'], event['after'], self.goal,
                                      states, process_incident=event['processObstructionVerified'])
            windows.append(dict(eventIndex=event['index'], startAfterDecision=start,
                                endBeforeEventIndex=i+2 if next_at is not None else None,
                                endDecision=entries[-1]['decision'] if entries else start,
                                postNextEventStateExcluded=True, **measured))
        scheduled = scheduled_of(self.ep)
        reference = self.row['case'].get('referenceActions', self.row['case'].get('oraclePlan'))
        reference_moves=len(reference) if reference is not None else None
        if control or meta['taskType']=='D0':reference_moves=sum(bool(k) for k in self.goal.values())
        elif reference_moves is None and self.row['case'].get('privateEvent'):
            reference_moves=self.row['case']['trigger']+len(self.row['case']['privateEvent']['recoveryWitness'])
        execution = execution_metrics(self.records, initial_was_correct=metrics['initialWasCorrect'],
                                      reference_moves=reference_moves)
        task_type = 'D0' if control else meta['taskType']
        return dict(schema='brick-atlas-evaluated-run/2', runId=self.run_id, model=self.actor,
                    caseId=self.row['key'], conditionId=self.condition, inputVersion=INPUT_VERSION,
                    canonicalTaskId=meta.get('normalCanonicalId', meta['canonicalId']) if control else meta['canonicalId'],
                    objectId=meta['model'], sourceGroup=meta['source'], track=meta['track'], taskType=task_type,
                    terminalStatus=terminal, success=metrics['success'] if terminal in ('completed','model_budget_exhausted') else None,
                    scheduledEvents=scheduled, appliedEvents=len(self.events),
                    effectiveIncidentVerified=bool(self.events and all(e['effectiveIncidentVerified'] for e in self.events)),
                    incidentExposure='normal_control' if not scheduled else 'untriggered' if not self.events else 'partial' if len(self.events)<scheduled else 'all_applied',
                    repairApplicable=bool(scheduled and len(self.events)==scheduled and all(e['effectiveIncidentVerified'] for e in self.events)),
                    standaloneConditionalRecovery=None, stateMetrics=metrics, executionMetrics=execution,
                    allIncidentCompletion=metrics['success'] if scheduled and len(self.events)==scheduled and all(e['effectiveIncidentVerified'] for e in self.events) else None,
                    allWindowsRecovered=(all(w['observedRecovery'] for w in windows) if windows and all(w.get('observedRecovery') is not None for w in windows) else None),
                    eventWindows=windows,apiCallsByEnvironment=0,
                    apiCalls=0 if self.actor.startswith(('scripted','human:')) else None,providerUsage=None)

    def export(self):
        normalized=self.result()
        return dict(schema='brick-atlas-private-execution/2', caseId=self.row['key'], runId=self.run_id,
                    inputVersion=INPUT_VERSION, evaluationMetadata=self.row['evaluationMetadata'],
                    initial=self.initial, final=deepcopy(self.ep.state), goal=self.goal,
                    aliasMaps=alias_maps(self.ep), decisionCap=self.cap, records=self.records,
                    nativeEvents=deepcopy(events_of(self.ep)), eventLedger=self.events,
                    normalizedResult=normalized, nativeScore=self.ep.score(),
                    apiCallsByEnvironment=0,apiCalls=normalized['apiCalls'])

    def save(self):
        if not getattr(self,'autosave',True):return
        temporary=self.directory/'record.private.pending.json.gz'
        write(temporary,self.export())
        temporary.replace(self.directory/'record.private.json.gz')


def assess_pair(control, intervention, prefix_decisions):
    """Verify actual state, actions, handles, images, rules and budget at the fork."""
    if prefix_decisions<0 or prefix_decisions>min(len(control.records), len(intervention.records)):
        raise ValueError('Invalid shared-prefix length')
    a, b = control.records[:prefix_decisions], intervention.records[:prefix_decisions]
    def has_observation(record):
        observation=record.get('observation') or {}
        hashes=[observation.get('packetSha256')]+observation.get('imageHashes',[])
        return bool(observation.get('imageHashes') and all(isinstance(h,str) and len(h)==64 and
            all(c in '0123456789abcdef' for c in h) for h in hashes))
    known_images = all(has_observation(r) for r in a+b)
    forks=[s.records[prefix_decisions] if len(s.records)>prefix_decisions else {} for s in [control,intervention]]
    fork_images=bool(all(has_observation(r) for r in forks) and
                     forks[0]['observation']==forks[1]['observation'])
    equal = (control.initial==intervention.initial and a==b and known_images
             and alias_maps(control.ep)==alias_maps(intervention.ep) and control.cap==intervention.cap
             and not any(r['newEventIndices'] for r in a+b) and fork_images)
    left, right = control.result(), intervention.result()
    context_pairs=list(zip(a,b))+[(forks[0],forks[1])]
    contexts=all(x.get('requestEvidence',{}).get('requestContextSha256') and
                 x.get('requestEvidence')==y.get('requestEvidence') for x,y in context_pairs)
    scripted=control.actor.startswith('scripted') and intervention.actor.startswith('scripted')
    verified=bool(equal and (scripted or contexts))
    proof = dict(verified=verified, decisions=prefix_decisions, imagesVerified=known_images and fork_images,
                 requestContextVerified=bool(contexts),executorOnlyScriptedDiagnostic=scripted,
                 formalModelRateEligible=bool(equal and contexts and not scripted),
                 prefixSha256=digest(a), scope='Executed state/actions, public packet/image hashes, aliases, budget; no provider dialogue in scripted/human runs.')
    return dict(schema='brick-atlas-paired-evaluation/2', sharedPrefixProof=proof,
                control=left, intervention=right,
                metrics=pair_metrics(left, right, shared_prefix_verified=verified))
