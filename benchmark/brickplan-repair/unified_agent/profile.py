"""Public, model-independent budgets and memory rules."""
from copy import deepcopy

PROFILE = dict(
    name='visual-memory-pull-v5', initialViews=['isometric', 'rear', 'top'],
    initialInventoryPage=1, targetRetention='all three target views every decision',
    observationRule='initial views, then only agent-requested images; no automatic scene after a move',
    sceneMemory='latest observation plus one preceding observation; timestamps retained',
    catalogueMemory='latest inventory page and latest candidate/manual page',
    textHistoryTurns=8, planItems=6, planItemCharacters=160, notesCharacters=1200,
    maxActions=16, maxObservations=24, maxDecisions=40,
    maxOutputTokensPerDecision=2048, maxGeneratedTokens=81920,
    reasoningPolicy='off-when-supported; required-thinking models use low; all reported generation tokens count',
    reasoningMode='off-when-supported', requestTimeoutSeconds=180,
    outputContract='brick-atlas-tool-contract/4', truncationPolicy='stop without executing; exclude from assembly score',
    preflightRequired=True,
    retries=0, scriptedPrefix=0, automaticRepair=False,
    nativeComputeEqualityClaim=False,
)


def profile(**changes):
    value=deepcopy(PROFILE);value.update(changes)
    for k in ('maxActions','maxObservations','maxDecisions','maxOutputTokensPerDecision','maxGeneratedTokens'):
        if type(value[k]) is not int or value[k] <= 0:raise ValueError(k+' must be positive')
    return value


def for_session(session):
    """Public inventory size sets the same budgets for every backbone on a case."""
    aliases=getattr(session.ep,'actor_alias',getattr(session.ep,'alias',{}))
    n=len(aliases)
    decisions=min(session.cap,getattr(session.ep,'decision_budget',session.cap))
    actions=min(getattr(session.ep,'manipulation_budget',decisions),max(16,6*n))
    return profile(maxActions=actions,maxObservations=min(decisions,max(24,4*n)),maxDecisions=decisions,
        maxGeneratedTokens=2048*decisions,budgetRule='public inventory count; capped at native task limits; identical for all backbones',publicInventoryParts=n)
