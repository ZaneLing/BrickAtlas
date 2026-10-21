"""Package the certified static cases with an explicit white-board input contract."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from baseplate import PlateAssembly,PROTOCOL

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'deliverables/brickplan-static-held4/combined'
DEST=ROOT/'deliverables/brickplan-static-plate5'
def rows(path):return [json.loads(x) for x in path.read_text().splitlines()]

def main():
    cases=rows(DEST/'cases.jsonl');models={};questions=[];new=[]
    for case in cases:
        mid=case['modelId']
        if mid not in models:
            models[mid]=PlateAssembly(json.loads((SOURCE/case['qualificationFile']).read_text()))
        runtime=models[mid]
        catalog={a:sorted(k for k,r in runtime.candidates.items() if r['actor']==a)
                 for a in runtime.actors}
        case.update(schema='brickplan-static-repair-case/plate5',
                    actors=list(runtime.actors),choices=catalog,
                    rackCapacity=max(case.get('rackCapacity',0),len(runtime.actors)),
                    contract='One brick per attach or detach. White baseplate is permanent environment geometry.',
                    description='观察白色底板上的当前状态和目标，每次只安装或拆卸一块积木，完成修复。',
                    whiteBaseplate=runtime.baseplate,
                    observation={'protocol':'visual-rgb-v5','visualEligibility':'pending-plate5-render-review'})
        question=dict(schema='brickplan-static-plate5-question/1',publicId=case['publicId'],
            modelId=mid,title=case['title'],manipulationProtocol=PROTOCOL,
            task='观察当前状态与目标；每步只安装或拆卸一块积木。白色底板始终存在，不算零件。',
            baseplate=runtime.baseplate,inventory=list(runtime.actors),
            currentState=case['initial'],targetState=case['goal'],candidateCatalog=catalog,
            observationProtocol='visual-rgb-v5',visualStatus='pending-render-review',
            allowedActions=['inspect','attach','detach','finish'],
            finishRule='终态与目标的几何、零件类型和颜色等价')
        questions.append(question);new.append(case)
    assert len(new)==3292 and len({x['publicId'] for x in new})==3292
    (DEST/'cases.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in new))
    (DEST/'questions.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in questions))
    summary=json.loads((DEST/'summary.json').read_text())
    summary.update(schema='brickplan-static-plate5-migration/2',
        certifiedBankSha256=hashlib.sha256((DEST/'cases.jsonl').read_bytes()).hexdigest(),
        questionBankSha256=hashlib.sha256((DEST/'questions.jsonl').read_bytes()).hexdigest(),
        questionCount=len(questions),visualStatus='pending-render-review',
        modelConfigurations=len(models),methods=dict(Counter(x['migrationMethod'] for x in new)))
    (DEST/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(cases=len(new),questions=len(questions),models=len(models)),ensure_ascii=False))
if __name__=='__main__':main()
