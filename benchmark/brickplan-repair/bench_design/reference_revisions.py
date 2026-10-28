"""Versioned reference corrections shared by the runner and the GT viewer.

The task's initial state, target, incident schedule and stored participant answers
are untouched. Historical source witnesses remain available for comparison.
"""
from copy import deepcopy
from functools import lru_cache
from bench_design.challenges import QUALITY
from expansion_v7.build import read,digest

PATH=QUALITY/'gt-reference-revisions.private.json.gz'
FIELDS=('referenceActions','referenceChecks','referenceIncident','referenceEvents','referenceScore',
        'referenceRevision','referenceActorLabels','referenceRepairNote')


def fingerprint(case):
    return digest({k:case.get(k) for k in ('initial','goal','events','referenceActions')})


@lru_cache(maxsize=1)
def revisions():
    return {r['caseId']:r for r in read(PATH)['revisions']} if PATH.exists() else {}


def apply(row,ep):
    revision=revisions().get(row['key'])
    if not revision:return
    case=row['case']
    if fingerprint(case)!=revision['sourceFingerprint']:
        raise ValueError('Reference correction does not match this task version: '+row['key'])
    for key in FIELDS:
        if key in revision['updates']:
            case[key]=deepcopy(revision['updates'][key]);ep.case[key]=deepcopy(case[key])

