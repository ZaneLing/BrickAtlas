"""Current task selection. Historical sources and participant records are retained."""
RETIRED_MODELS={
    'rockefeller-crown':'用户移除：密集颜色与顶部结构难以可靠辨认。',
    'museum-roof-long':'用户移除：屋顶层数与阶段在图中难以可靠辨认。',
}
RETIRED_SOURCES={'set:21007','set:21004'}
RETIRED_MODEL_ALIASES=set(RETIRED_MODELS)|{'museum-roof','v23-21004','v23-21007'}


from functools import lru_cache
from pathlib import Path


def _source_withdrawals():
    root=Path(__file__).resolve().parents[3]
    path=root/'deliverables/brickplan-dynamic-arena/source-curation.json'
    modules=root/'deliverables/brickplan-quality-round/source-expansion/index.json'
    return _read_withdrawals(path.stat().st_mtime_ns if path.exists() else 0,modules.stat().st_mtime_ns if modules.exists() else 0)


@lru_cache(maxsize=4)
def _read_withdrawals(curation_version,module_version):
    # A whole source is withdrawn, including its previously selected modules.
    # Historical logs/files remain readable; current task entry points reject it.
    import json
    from pathlib import Path
    root=Path(__file__).resolve().parents[3]
    path=root/'deliverables/brickplan-dynamic-arena/source-curation.json'
    if not path.exists():return set(),set()
    rows=json.loads(path.read_text())['withdrawn']
    numbers={r['setNumber'].split('-')[0] for r in rows}
    aliases={r['id'] for r in rows}
    for n in numbers:aliases.update({n,'v23-'+n,'omr-'+n,'new-'+n+'-1','r-omr-'+n+'-1','arena-'+n+'-1'})
    modules=root/'deliverables/brickplan-quality-round/source-expansion/index.json'
    if modules.exists():
        for m in json.loads(modules.read_text())['models']:
            if m['sourceSetId'].split('-')[0] in numbers:aliases.add(m['id'])
    return {'set:'+n for n in numbers},aliases


def retired(case_id='',model=None,source=None):
    sources,aliases=_source_withdrawals()
    if model in aliases or source in sources or any(case_id.startswith(prefix+a+'::') for a in aliases for prefix in ('A4:','QN:','v7::')):return True
    return model in RETIRED_MODEL_ALIASES or source in RETIRED_SOURCES or any(
        mid in case_id for mid in RETIRED_MODEL_ALIASES)


def require_active(case_id,model=None,source=None):
    if retired(case_id,model,source):raise ValueError('This model was withdrawn from the active benchmark after human review.')
