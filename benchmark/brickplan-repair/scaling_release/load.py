"""Shared static and dynamic adapter; private schedules never enter public inputs."""
from scaling_release import OUT
from expansion_v7.build import read
from expansion_v7.runtime import Episode
from expansion_v7.run_episode import Packet


def load(cid,directory):
    number=cid.split(':')[1];folder=OUT/'private'/number
    from scaling_release.check import verified
    if not verified(folder):raise ValueError('This source/task revision has not passed the final dataset audit: '+number)
    meta=read(folder/'metadata.json')
    from scaling_release.export import display_title
    case=next(c for c in read(folder/'cases.private.json.gz') if c['id']==cid)
    from bench_design.selection import require_active
    require_active(cid,meta['id'],'set:'+number.split('-')[0])
    cert=read(folder/'certificate.private.json.gz');ep=Episode(cert,case,41)
    from bench_design.source_expansion import guard_incidents
    guard_incidents(ep.runtime)
    packet=Packet(ep,read(folder/'manual.private.json.gz'),directory)
    task='S0' if case['mode']=='static' and case['family']=='control' else 'S1' if case['mode']=='static' else 'D0' if not case['events'] else 'D2' if len(case['events'])>1 else 'D1'
    track=('whole-object' if cert.get('environmentMode')=='white-baseplate' else 'finishing-stage')+'-'+case['mode']
    row=dict(key=cid,bank='SC',model=meta['id'],title=display_title(meta['source']),mode=case['mode'],case=case,family=case['family'],evaluationMetadata=dict(canonicalId=cid,taskType=task,track=track,source='set:'+number.split('-')[0],model=meta['id']))
    return row,ep,packet,None
