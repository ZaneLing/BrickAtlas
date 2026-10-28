"""A small whole object, with an event certified against the actual live state.

This demonstration is separate from the formal released question counts.
Normal instructions describe a feasible order, never the next required action.
"""
from copy import deepcopy
from bench_design.session import Session
from expansion_v7.designs import certificate
from expansion_v7.runtime import Episode, runtime, move
from expansion_v7.run_episode import Packet

CASE_ID = 'arena:blue-table:continuous-v1'
TITLE = '蓝色小桌 · 从空底板到完成'


def create(directory, actor, events=True):
    spec = dict(name='蓝色小桌', family='arena-table', category='furniture',
        wrongColorActor='P002', wrongColor='#9b59b6', parts=[
            ('F001', '3005', -30, -24, -10, '#a66b35', 0),
            ('P001', '3005', 30, -24, -10, '#a66b35', 0),
            ('P002', '3005', -30, -24, 10, '#a66b35', 0),
            ('P003', '3005', 30, -24, 10, '#a66b35', 0),
            ('P004', '3020', 0, -32, 0, '#0055bf', 0)])
    cert = certificate('arena-blue-table', spec)
    cert['source'].update(longProcess=False, generator='dynamic_arena/demo.py')
    rt = runtime(cert)
    normal = [move(a, a + ':goal') for a in ['F001', 'P001', 'P002', 'P003', 'P004']]
    initial = {a: '' for a in rt.actors}
    states = [deepcopy(initial)]
    for action in normal:
        after, feedback = rt.check(states[-1], action['actor'], action['type'], candidate=action['candidate'])
        assert feedback['code'] == 'OK', feedback
        states.append(after)
    assert rt.complete(states[-1])
    case = dict(id=CASE_ID, mode='dynamic', family='missing', initial=initial, goal=rt.goal,
        events=[dict(family='missing', minimumInstalled=3)] if events else [],
        completedInstructionStep=0, normalReferenceActions=normal)
    ep = Episode(cert, case, 41)
    packet = Packet(ep, dict(actions=normal, states=states), directory)
    row = dict(key=CASE_ID, bank='E7', model='arena-blue-table', title=TITLE,
        mode='dynamic', case=deepcopy(case), evaluationMetadata=dict(
            canonicalId=CASE_ID, taskType='D1' if events else 'D0',
            track='whole-object-dynamic', source='original:arena-blue-table', model='arena-blue-table'))
    return Session(row, ep, packet, None, directory, actor=actor)
