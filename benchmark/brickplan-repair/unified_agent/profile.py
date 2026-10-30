"""Public, model-independent budgets and memory rules."""
from copy import deepcopy

PROFILE = dict(
    name='visual-memory-pull-v1', initialViews=['isometric', 'rear', 'top'],
    initialInventoryPage=1, targetRetention='all three target views every decision',
    observationRule='initial views, then only agent-requested images; no automatic scene after a move',
    sceneMemory='latest observation plus one preceding observation; timestamps retained',
    catalogueMemory='latest inventory page and latest candidate/manual page',
    textHistoryTurns=8, planItems=6, planItemCharacters=160, notesCharacters=1200,
    maxActions=16, maxObservations=24, maxDecisions=40,
    maxOutputTokensPerDecision=2048, maxGeneratedTokens=81920,
    reasoningPolicy='low when supported; non-thinking-only backbones remain non-thinking; generated-token ceiling includes reported reasoning tokens',
    retries=0, scriptedPrefix=0, automaticRepair=False,
    nativeComputeEqualityClaim=False,
)


def profile(**changes):
    value=deepcopy(PROFILE);value.update(changes)
    for k in ('maxActions','maxObservations','maxDecisions','maxOutputTokensPerDecision','maxGeneratedTokens'):
        if type(value[k]) is not int or value[k] <= 0:raise ValueError(k+' must be positive')
    return value
