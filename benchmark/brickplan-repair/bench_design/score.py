"""Aggregate normalized result JSONL; never starts a provider request."""
import argparse,json
from pathlib import Path
from bench_design.metrics import aggregate,aggregate_pairs


def main():
    p=argparse.ArgumentParser();p.add_argument('results',type=Path);p.add_argument('--output',type=Path)
    args=p.parse_args();rows=[json.loads(l) for l in args.results.read_text().splitlines() if l.strip()]
    pairs=[r for r in rows if r.get('schema')=='brick-atlas-paired-evaluation/2']
    runs=[r.get('normalizedResult',r) for r in rows if r not in pairs]
    result=dict(groups=aggregate(runs),pairedGroups=aggregate_pairs(pairs),inputRecords=len(rows),note='Explicit terminal statuses required; missing outcomes are never fabricated.')
    text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')


if __name__=='__main__':main()
