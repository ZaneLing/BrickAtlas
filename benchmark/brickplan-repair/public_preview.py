"""Export a portable, read-only dataset browser from existing verified examples.

No model is called and no benchmark state, answer or interface is changed.
Model inputs and explanatory reference answers are separate files.
"""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
import shutil

import question_showcase as show

ROOT = show.ROOT
SOURCE = ROOT / 'deliverables/brickplan-question-showcase'
OUT = ROOT / 'deliverables/brickplan-public-preview'


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, _, _ = show.dataset()
    examples = [json.loads(p.read_text()) for p in sorted((SOURCE / 'examples').glob('Q*.json'))]
    by_key = {e['key']: e for e in examples}
    catalogue = []
    for row in rows:
        e = by_key.get(row['key'])
        catalogue.append(dict(id=row['key'], sample=e['example'] if e else None,
            title=row['title'], bank=row['bank'], mode=row['mode'], model=row['model'],
            family=row['family'], familyName=show.label(row['family']), level=row['level'],
            split=row['profile']['split'], source=row['profile']['source'],
            targetParts=row['profile']['targetParts'],
            scheduledEvents=row['profile'].get('scheduledEvents', 0)))
    catalogue.sort(key=lambda r: (r['sample'] is None, r['sample'] or '', r['id']))
    write(OUT / 'catalogue.json', catalogue)
    (OUT / 'catalogue.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in catalogue))
    assets = {}

    def image_record(record):
        if record is None:
            return None
        source = SOURCE / record['file']
        data = source.read_bytes()
        assert sha256(data).hexdigest() == record['sha256'], source
        destination = OUT / 'assets' / source.name
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        assets[source.name] = record['sha256']
        return {**record, 'file': 'assets/' + source.name}

    def packet(record, output):
        raw = json.loads((SOURCE / record['input']).read_text())
        clean = {k: v for k, v in raw.items() if k != 'assetPathBase'}
        clean['images'] = [image_record(i) for i in raw['images']]
        clean['assetPathBase'] = '.'
        forbidden = {'goal', 'initial', 'oraclePlan', 'referenceActions', 'privateEvent',
                     'humanErrorIds', 'family', 'events', 'intervention', 'eventApplied'}

        def inspect(value):
            if isinstance(value, dict):
                assert not forbidden.intersection(value), forbidden.intersection(value)
                for v in value.values(): inspect(v)
            elif isinstance(value, list):
                for v in value: inspect(v)
        inspect(clean['observation'])
        write(OUT / output, clean)
        return dict(inputFile=output, images=clean['images'])

    metadata = []
    for e in examples:
        code = e['example']
        stages = [dict(name='开始时的输入', **packet(e['initial'], f'samples/{code}/initial.model-input.json'))]
        for event in e['events']:
            stages.append(dict(name=f'中途观察 {event["number"]}',
                **packet(event['packet'], f'samples/{code}/observation-{event["number"]}.model-input.json')))
        reference = dict(sampleId=code, caseId=e['key'], type='program-verified-reference-not-model-performance',
            actions=[{k: a[k] for k in ('step', 'output', 'publicAction', 'description', 'feedback', 'eventAfterThisAction')}
                     for a in e['gt']], finish=e['finish'],
            referenceWitnessPassed=e['referenceWitnessPassed'], requiredReferenceOrder=False,
            referenceIsShortest=False, intermediateStateMatching=False,
            acceptance='Final geometry and color must match the episode target; all executed moves must be legal.',
            strip=image_record(e['gtStrip']), final=image_record(e['finalImage']),
            events=[dict(number=v['number'], afterStep=v['afterStep'], family=show.label(v['family']),
                         image=image_record(v['truthImage'])) for v in e['events']],
            candidateExample=(dict(request=e['candidateExample']['request'],
                images=[image_record(i) for i in e['candidateExample']['images']],
                policy='One preview selected from the reference action, for explanation only; not a complete option set.')
                if e.get('candidateExample') else None))
        reference_file = f'samples/{code}/reference.answer.json'
        write(OUT / reference_file, reference)
        summary = dict(id=code, caseId=e['key'], title=e['title'], bank=e['bank'], mode=e['mode'],
            family=e['family'], familyName=show.label(e['family']), familyNote=show.family_note(e['family']),
            model=e['model'], level=e['level'], split=e['profile']['split'], source=e['profile']['source'],
            targetParts=e['targetParts'], inventoryParts=e['inventoryParts'],
            contextLocked=e['contextLocked'], referenceActions=e['referenceActions'],
            stages=stages, referenceFile=reference_file,
            manual=image_record(e['manual']) if e.get('manual') else None,
            visibility=e['visibility'])
        write(OUT / f'samples/{code}/sample.json', summary)
        metadata.append(dict(file_name=stages[0]['images'][0]['file'], sample_id=code,
            task='把当前结构修复到本题唯一目标。' if e['mode']=='static' else '逐步完成目标结构，并处理过程中可能发生的变化。',
            mode=e['mode'], source_group=e['profile']['source'], split=e['profile']['split'],
            difficulty=e['level'], difficulty_is_provisional=True,
            model_input_file=stages[0]['inputFile'], reference_answer_file=reference_file,
            answer_policy='Any legal sequence reaching the required final geometry and color; reference is not unique.'))
    (OUT / 'metadata.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in metadata))
    summary = dict(schema='brick-atlas-dataset-browser/1', date='2026-10-23',
        totalTasks=len(catalogue), taskModes=dict(Counter(r['mode'] for r in catalogue)),
        detailedExamples=len(examples), assetCount=len(assets), apiModelCalls=0,
        deployment='Local preview only; not uploaded to Hugging Face.',
        scope='All active task metadata, plus 95 previously exported native image/input/reference examples. Other tasks do not claim full image export.',
        answers='Explanatory reference files are separate from model-input files; this is not a hidden-test release package.')
    write(OUT / 'summary.json', summary)
    write(OUT / 'asset-manifest.json', assets)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
