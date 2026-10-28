"""Physical, reversible incidents selected from the actual assembly.

No target-prefix comparison is used for triggering. Evidence and incident counts
remain private; every accepted transaction and inverse passes the same engine.
"""
from copy import deepcopy
from itertools import combinations
import random
import numpy as np

from expansion_v7 import PROTOCOL
from expansion_v7.scope import require_allowed
from community_modules.core import ModuleAssembly, Episode as BaseEpisode
from baseplate import PlateAssembly


def move(actor, key=None):
    return dict(type='attach', actor=actor, candidate=key) if key else dict(type='detach', actor=actor)


def execute(rt, state, actions):
    state, checks = dict(state), []
    for action in actions:
        state, check = rt.check(state, action['actor'], action['type'], candidate=action.get('candidate'))
        checks.append(check)
        if check['code'] != 'OK' or not rt.anchored(state):
            return None, checks
    return state, checks


def prune_roundtrips(rt, initial, actions, protected=()):
    """Remove whole detach/restore pairs only after replaying the shorter plan.

    Search subsets of these pairs, keeping the existing order of all remaining
    actions. This proves those pairs unnecessary, not global path optimality.
    """
    actions=deepcopy(actions);final,_=execute(rt,initial,actions)
    if final is None:raise ValueError('Cannot shorten an illegal reference')
    candidates=[]
    for actor,key in initial.items():
        if not key or actor in protected or final.get(actor)!=key:continue
        moves=[a for a in actions if a['actor']==actor]
        if len(moves)==2 and moves[0]['type']=='detach' and moves[1].get('candidate')==key:
            candidates.append(actor)
    if len(candidates)>12:raise ValueError('Reference cleanup search requires a larger explicit budget')
    for count in range(len(candidates),0,-1):
        for omitted in combinations(candidates,count):
            trial=[a for a in actions if a['actor'] not in omitted]
            end,checks=execute(rt,initial,trial)
            if end==final:
                return trial,dict(removedRoundtripActors=list(omitted),beforeMoves=len(actions),
                    afterMoves=len(trial),checks=checks,globalShortestClaim=False)
    return actions,dict(removedRoundtripActors=[],beforeMoves=len(actions),afterMoves=len(actions),globalShortestClaim=False)


class ExpandedAssembly(ModuleAssembly):
    def incident(self, family, state, latest=None, placement_order=None, variant=0):
        order = placement_order or {}
        installed = sorted((a for a, k in state.items() if k and a != latest),
                           key=lambda a: (order.get(a, 0), a))
        if installed:
            shift = variant % len(installed)
            installed = installed[shift:] + installed[:shift]

        def qualify(changes, inverse, affected, **extra):
            after, checks = execute(self, state, changes)
            if after is None or self.signature(after) == self.signature(state):
                return None
            recovered, inverse_checks = execute(self, after, inverse)
            if recovered is None or recovered != state:
                return None
            return dict(family=family, affected=affected, before=dict(state), after=after,
                        changes=changes, recovery=inverse, checks=checks,
                        recoveryChecks=inverse_checks, **extra)

        if family in ('missing', 'wrong-color', 'wrong-part', 'offset', 'rotated'):
            for actor in installed:
                old = state[actor]
                options = [(None, None)] if family == 'missing' else [
                    (row['actor'], key) for key, row in self.candidates.items()
                    if row.get('faultFamily') == family and row.get('originalActor') == actor]
                for other, key in options:
                    if other and other != actor and state.get(other):
                        continue
                    if other:
                        current=self.row(old)['part'];replacement=self.row(key)['part']
                        old_pose=np.asarray(current['rawMatrix']);new_pose=np.asarray(replacement['rawMatrix'])
                        if family=='wrong-color' and not np.allclose(old_pose,new_pose,atol=.001):continue
                        if family=='wrong-part':
                            from assembly import info
                            old_info,new_info=info(current['canonical']),info(replacement['canonical'])
                            old_frames=np.asarray(current['matrix'])@old_info.frames
                            new_frames=np.asarray(replacement['matrix'])@new_info.frames
                            common=any(a[:2]==b[:2] and np.allclose(f[:3,3],g[:3,3],atol=.025)
                                for a,f in zip(old_info.conns,old_frames)
                                for b,g in zip(new_info.conns,new_frames))
                            if not common:continue
                        if family=='wrong-color' and current['canonical']!=replacement['canonical']:continue
                        if family=='offset':
                            delta=old_pose[:3,:3].T@(new_pose[:3,3]-old_pose[:3,3])
                            if not np.allclose(old_pose[:3,:3],new_pose[:3,:3],atol=.001) or not np.isclose(np.linalg.norm(delta),20,atol=.001):continue
                        if family=='rotated' and np.allclose(old_pose[:3,:3],new_pose[:3,:3],atol=.001):continue
                    changes = [move(actor)] + ([move(other, key)] if other else [])
                    inverse = ([move(other)] if other else []) + [move(actor, old)]
                    found = qualify(changes, inverse, [actor])
                    if found:
                        return found
        elif family in ('extra-layer', 'repeated-step'):
            for key, row in self.candidates.items():
                actor = row['actor']
                if row.get('faultFamily') != 'extra-layer' or state.get(actor):
                    continue
                if not any(self.q.connection(row['part'], self.row(state[a])['part']) for a in installed):
                    continue
                found = qualify([move(actor, key)], [move(actor)], [actor])
                if found:
                    return found
        elif family in ('repeat-omission', 'cascade-removal'):
            for actors in combinations(installed[:12], 2):
                pa, pb = [self.row(state[a])['part'] for a in actors]
                if family == 'repeat-omission' and (pa['canonical'], pa['colorHex']) != (pb['canonical'], pb['colorHex']):
                    continue
                if family == 'cascade-removal' and not self.q.connection(pa, pb):
                    continue
                for pair in (actors, tuple(reversed(actors))):
                    found = qualify([move(a) for a in pair],
                        [move(a, state[a]) for a in reversed(pair)], list(pair))
                    if found:
                        return found
        elif family == 'left-right-swap':
            for a, b in combinations(installed[:14], 2):
                ka, kb = f'{a}:swap:{b}', f'{b}:swap:{a}'
                if ka not in self.candidates or kb not in self.candidates:
                    continue
                if not np.allclose(self.row(ka)['part']['rawMatrix'],self.row(state[b])['part']['rawMatrix'],atol=.001):continue
                if not np.allclose(self.row(kb)['part']['rawMatrix'],self.row(state[a])['part']['rawMatrix'],atol=.001):continue
                found = qualify([move(a), move(b), move(a, ka), move(b, kb)],
                    [move(b), move(a), move(b, state[b]), move(a, state[a])], [a, b])
                if found:
                    return found
        elif family == 'early-cover':
            # A later, otherwise-correct cover can be placed legally while
            # blocking another absent piece. Its removal is the legal recovery.
            absent = [(a, k) for a, k in self.goal.items() if k and not state.get(a)]
            available = []
            for a, key in absent:
                trial, _ = execute(self, state, [move(a, key)])
                if trial is not None:
                    available.append((a, key, trial))
            for cover, key, after in available:
                blocked = []
                for actor, target, _ in available:
                    if actor == cover:
                        continue
                    _, check = self.check(after, actor, 'attach', candidate=target)
                    if check['code'] == 'PATH_BLOCKED':
                        blocked.append(actor)
                if blocked:
                    found = qualify([move(cover, key)], [move(cover)], [cover], blockedNextParts=blocked)
                    if found:
                        return found
        elif family == 'buried-repair':
            for actor in installed:
                _, blocked = self.check(state, actor, 'detach')
                if blocked['code'] != 'PATH_BLOCKED':
                    continue
                replacements = [(r['actor'], k) for k, r in self.candidates.items()
                                if r.get('faultFamily') == 'wrong-color'
                                and r.get('originalActor') == actor and not state.get(r['actor'])
                                and np.allclose(r['part']['rawMatrix'],self.row(state[actor])['part']['rawMatrix'],atol=.001)]
                if not replacements:
                    continue
                shadow, removed = dict(state), []
                covers = sorted((a for a in installed + ([latest] if latest else []) if a != actor),
                                key=lambda a: (-order.get(a, 0), a))
                for cover in covers:
                    trial, _ = execute(self, shadow, [move(cover)])
                    if trial is None:
                        continue
                    shadow = trial
                    removed.append(cover)
                    base, _ = execute(self, shadow, [move(actor)])
                    if base is not None:
                        wa, wk = replacements[0]
                        down = [move(a) for a in removed]
                        up = [move(a, state[a]) for a in reversed(removed)]
                        found = qualify(down + [move(actor), move(wa, wk)] + up,
                            down + [move(wa), move(actor, state[actor])] + up,
                            [actor], temporarilyRemovedCorrectParts=removed)
                        if found:
                            # The greedy access search may remove an unrelated
                            # pillar before finding the real blocker. Do not
                            # preserve that unnecessary round trip in the GT.
                            changes,change_audit=prune_roundtrips(self,state,found['changes'],[actor,wa])
                            recovery,repair_audit=prune_roundtrips(self,found['after'],found['recovery'],[actor,wa])
                            necessary=[a for a in removed if a not in repair_audit['removedRoundtripActors']]
                            cleaned=qualify(changes,recovery,[actor],temporarilyRemovedCorrectParts=necessary,
                                referenceCleanup=dict(intervention=change_audit,recovery=repair_audit))
                            if cleaned:return cleaned
                    if len(removed) >= 4:
                        break
        return None


class ExpandedPlateAssembly(PlateAssembly):
    incident = ExpandedAssembly.incident
    anchored = ExpandedAssembly.anchored


def runtime(cert):
    return ExpandedPlateAssembly(cert) if cert.get('environmentMode') == 'white-baseplate' else ExpandedAssembly(cert)


class Episode(BaseEpisode):
    def __init__(self, cert, case, seed=41):
        require_allowed(case)
        self.cert, self.case = cert, deepcopy(case)
        self.schedule = deepcopy(case.get('events', []))
        self.case['event'] = None  # Parent handles only physical actions.
        self.runtime = runtime(cert)
        self.runtime.goal = dict(case['goal'])
        self.state = dict(case['initial'])
        rng = random.Random(seed)
        actors, keys = list(self.runtime.actors), list(cert['candidates'])
        rng.shuffle(actors); rng.shuffle(keys)
        self.actor_alias = {a: f'A{i+1:03}' for i, a in enumerate(actors)}
        self.pose_alias = {k: f'C{i+1:05}' for i, k in enumerate(keys)}
        self.actors = {v: k for k, v in self.actor_alias.items()}
        self.poses = {v: k for k, v in self.pose_alias.items()}
        self.actions = self.inspections = self.successful_installs = 0
        self.event_applied = self.done = False
        self.history, self.decisions, self.events, self.trigger_attempts = [], [], [], []
        self.feedback = self.previous = self.last_event = None
        self.placement_order = {}
        self.manipulation_budget = 6 * len(cert['source']['moduleSourceIndices']) + 24
        self.decision_budget = 10 * len(cert['source']['moduleSourceIndices']) + 40
        self.seed = seed

    def observe(self):
        obs = super().observe()
        obs.update(protocol=PROTOCOL, decisionsUsed=len(self.decisions), decisionBudget=self.decision_budget)
        if self.cert.get('environmentMode') == 'white-baseplate':
            obs['contextIsLocked'] = False
            if self.case['mode']=='static':
                step=self.case['completedInstructionStep']
                obs['task'] = f'修复当前场景，使其符合 TARGET（说明第 {step} 步的阶段目标）。从当前状态开始，不是从空白底板重搭。后续成品仅供参考，允许其他合法修复顺序；一次只装或拆一块，完成后 finish。'
            else:
                obs['task'] = '从空白色底板开始，逐件完成 TARGET。参考说明是一种可行顺序，允许其他合法顺序。每轮可查看实际状态，一次只装或拆一块；完成后 finish。过程中可能有未提示的变化。'
        return obs

    def step(self, action):
        if len(self.decisions) >= self.decision_budget:
            raise ValueError('Decision budget exhausted')
        before_history = len(self.history)
        try:
            super().step(action)
        except (ValueError, KeyError, TypeError) as exc:
            if self.done:
                raise
            self.previous = dict(self.state)
            self.feedback = dict(code='INVALID_REQUEST', message=str(exc))
            self.decisions.append(deepcopy(action))
            return self.observe()
        self.decisions.append(deepcopy(action))
        if len(self.history) == before_history or self.feedback.get('code') != 'OK':
            return self.observe()
        index = len(self.events)
        if index >= len(self.schedule):
            return self.observe()
        event = self.schedule[index]
        last_at = self.events[-1]['atManipulation'] if self.events else 0
        if (sum(bool(k) for k in self.state.values()) < event['minimumInstalled']
                or self.actions - last_at < event.get('minimumActionsSincePrevious', 1)):
            return self.observe()
        actor = self.actors.get(action.get('partId'))
        incident = self.runtime.incident(event['family'], self.state,
            latest=actor if action['type'] == 'attach' else None,
            placement_order=self.placement_order, variant=event.get('variant', 0))
        if incident is None:
            self.trigger_attempts.append(dict(event=index+1, at=self.actions, reason='no-legal-reversible-change'))
            return self.observe()
        incident.update(index=index+1, atManipulation=self.actions, atDecision=len(self.decisions),
                        humanErrorIds=event.get('humanErrorIds', []))
        self.events.append(incident)
        self.last_event = incident
        self.event_applied = True
        self.state = dict(incident['after'])
        self.history[-1].update(after=dict(self.state), eventApplied=True, intervention=deepcopy(incident))
        return self.observe()

    def score(self):
        correct = self.runtime.complete(self.state)
        return dict(success=self.done and correct, completionSuccess=self.done and correct,
                    finalGeometryCorrect=correct, finished=self.done,
                    scheduledEvents=len(self.schedule), appliedEvents=len(self.events),
                    allScheduledEventsTriggered=len(self.events) == len(self.schedule),
                    eventApplied=bool(self.events),
                    observedCompletionAfterEvent=(self.done and correct) if self.events else None,
                    repairSuccess=None, recoveryPairEligible=False,
                    repairEligibilityReason='Requires successful matched normal control and all scheduled events.',
                    manipulations=self.actions, inspections=self.inspections, decisions=len(self.decisions),
                    intermediateStateComparedToGT=False, humanValidated=False)


def public_action(ep, action):
    result = dict(type=action['type'], partId=ep.actor_alias[action['actor']])
    if action['type'] == 'attach':
        result['candidate'] = ep.pose_alias[action['candidate']]
    return result


def fork(prefix, fault_case, seed=None):
    """Replay the exact common prefix, then enable the hidden schedule in one copy."""
    require_allowed(fault_case)
    if prefix.events or prefix.done:
        raise ValueError('Branch requires an unfinished normal prefix')
    clones = []
    seed = prefix.seed if seed is None else seed
    for _ in range(2):
        clone = Episode(prefix.cert, {**prefix.case, 'events': []}, seed)
        for action in prefix.decisions:
            clone.step(deepcopy(action))
        assert clone.state == prefix.state and clone.previous == prefix.previous
        assert clone.actor_alias == prefix.actor_alias and clone.pose_alias == prefix.pose_alias
        assert clone.history == prefix.history
        clones.append(clone)
    clones[1].schedule = deepcopy(fault_case.get('events', []))
    return tuple(clones)
