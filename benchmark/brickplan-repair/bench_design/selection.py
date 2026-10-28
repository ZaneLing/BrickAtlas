"""Current task selection. Historical sources and participant records are retained."""
RETIRED_MODELS={
    'rockefeller-crown':'用户移除：密集颜色与顶部结构难以可靠辨认。',
    'museum-roof-long':'用户移除：屋顶层数与阶段在图中难以可靠辨认。',
}
RETIRED_SOURCES={'set:21007','set:21004'}
RETIRED_MODEL_ALIASES=set(RETIRED_MODELS)|{'museum-roof','v23-21004','v23-21007'}


def retired(case_id='',model=None,source=None):
    return model in RETIRED_MODEL_ALIASES or source in RETIRED_SOURCES or any(
        mid in case_id for mid in RETIRED_MODEL_ALIASES)


def require_active(case_id,model=None,source=None):
    if retired(case_id,model,source):raise ValueError('This model was withdrawn from the active benchmark after human review.')
