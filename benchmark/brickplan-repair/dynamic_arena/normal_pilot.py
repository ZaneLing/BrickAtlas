"""Paid normal-build prerequisite pilot: three VLMs by three complete objects.

Uses the same pull-observation arena as the public demo. Every run starts on
an empty physical white stud plate, has no external event, and is scored by
the existing evaluator. The global pilot ledger caps total spend at $3;
uncertain provider requests reserve their full ceiling rather than disappearing.
"""
import argparse
import json
import re
import time
from pathlib import Path
from dynamic_arena import OUT
from dynamic_arena.demo import create
from dynamic_arena.tool_arena import ToolArena
from dynamic_arena.transport import Transport, write_json
from bench_design.metrics import aggregate

MODELS = ('google/gemini-2.5-flash', 'qwen/qwen3-vl-235b-a22b-instruct',
          'openai/gpt-6.1-sol', 'anthropic/claude-sonnet-5.5')
OBJECTS = ('obj-chair', 'obj-city-car', 'obj-crane')
LEDGER = OUT / 'normal-pilot-ledger.private.json'
REPORT = OUT / 'normal-pilot-results.json'


def launch(model, obj, decisions, cap):
    runid = 'normal-' + re.sub('[^a-z0-9]+', '-', model.lower()).strip('-') + '-' + obj + '-' + time.strftime('%Y%m%d-%H%M%S')
    directory = OUT / 'runs' / runid
    session = create(directory, model, events=False, model_id=obj)
    transport = Transport(directory, cap=cap, model=model, ledger_path=LEDGER)
    result = ToolArena(session, transport, max_decisions=decisions).run()
    return dict(runId=runid, objectId=obj, model=model, result=result)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--max-decisions',type=int,default=30)
    p.add_argument('--max-cost',type=float,default=3.0)
    p.add_argument('--models',nargs='*',choices=MODELS,default=MODELS)
    p.add_argument('--objects',nargs='*',choices=OBJECTS,default=OBJECTS)
    p.add_argument('--rerun-service-errors',action='store_true')
    args=p.parse_args()
    if not 0 < args.max_cost <= 3: raise ValueError('Pilot cost cap must be at most $3')
    old=json.loads(REPORT.read_text())['runs'] if REPORT.exists() else []
    latest={(r['model'],r['objectId']):r for r in old}
    for model in args.models:
        for obj in args.objects:
            prior=latest.get((model,obj))
            if prior and not (args.rerun_service_errors and prior['result']['terminalStatus']=='service_error'):
                continue
            item=launch(model,obj,args.max_decisions,args.max_cost)
            old.append(item);latest[(model,obj)]=item
            ledger=json.loads(LEDGER.read_text())
            total=sum(c['actualUSD'] if c['actualUSD'] is not None else c['reservedUSD'] for c in ledger['charges'])
            summary=dict(schema='brick-atlas-normal-pilot/1',protocol='brick-atlas-tool-arena/2',
                noInterventions=True,objects=list(args.objects),models=list(args.models),
                runs=old,latestRuns=list(latest.values()),
                aggregate=aggregate([r['result'] for r in latest.values()]),
                confirmedCostUSD=sum(c['actualUSD'] or 0 for c in ledger['charges']),
                chargedOrReservedUpperBoundUSD=total,capUSD=ledger['capUSD'],
                unsettledRequests=sum(c['status']!='settled' for c in ledger['charges']),
                repairMetrics='Not applicable to normal controls; incident runs require normal success and a matched-prefix branch.')
            write_json(REPORT,summary)
            print(json.dumps(dict(runId=item['runId'],model=model,object=obj,
                terminal=item['result']['terminalStatus'],success=item['result']['success'],
                fullPlacementF1=item['result']['stateMetrics']['fullPlacement']['f1'],
                legalActionRate=item['result']['executionMetrics']['legalActionRate'],
                costUSD=item['result']['providerUsage']['costUSD'],
                totalUpperBoundUSD=total),ensure_ascii=False),flush=True)


if __name__=='__main__':main()
