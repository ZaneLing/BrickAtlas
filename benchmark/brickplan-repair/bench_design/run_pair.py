"""Execute explicit shared-prefix action files, then score both continuations.

No API calls. Full provider request-context hashes are required for a non-scripted
actor's formal pairing; environment/image equality alone is insufficient.
"""
from pathlib import Path
import argparse,json,uuid
from bench_design import OUT
from bench_design.session import Session,assess_pair
from bench_design.metrics import aggregate,aggregate_pairs
from expansion_v7.build import write


def actions(path):
    for line in Path(path).read_text().splitlines():
        if not line.strip():continue
        value=json.loads(line)
        yield value if isinstance(value,dict) and 'action' in value else dict(action=value)


def perform(session,entry):
    session.observe()
    session.submit(entry['action'],request_evidence=entry.get('requestEvidence'))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--id',required=True);p.add_argument('--prefix',type=Path,required=True)
    p.add_argument('--control-actions',type=Path,required=True);p.add_argument('--fault-actions',type=Path,required=True)
    p.add_argument('--actor',default='scripted-pair-cli');p.add_argument('--output',type=Path)
    a=p.parse_args();root=(a.output or OUT/'paired-runs'/uuid.uuid4().hex).resolve()
    left=Session.open(a.id,root/'control',a.actor,control=True)
    right=Session.open(a.id,root/'intervention',a.actor)
    if right.row['evaluationMetadata']['taskType'] not in ('D1','D2'):raise ValueError('Select a dynamic incident condition')
    prefix=list(actions(a.prefix))
    for entry in prefix:
        for session in [left,right]:perform(session,entry)
        if right.events or left.done or right.done:raise ValueError('The shared prefix must end before an event or finish')
    for session,path in [(left,a.control_actions),(right,a.fault_actions)]:
        for entry in actions(path):
            if session.done:break
            perform(session,entry)
        session.save()
    pair=assess_pair(left,right,len(prefix));write(root/'pair.private.json',pair)
    runs=[left.result(),right.result()]
    (root/'normalized-runs.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in runs))
    (root/'normalized-pairs.jsonl').write_text(json.dumps(pair,ensure_ascii=False)+'\n')
    summary=dict(groups=aggregate(runs),pairedGroups=aggregate_pairs([pair]),
        sharedPrefixProof=pair['sharedPrefixProof'],apiCalls=0)
    write(root/'summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
