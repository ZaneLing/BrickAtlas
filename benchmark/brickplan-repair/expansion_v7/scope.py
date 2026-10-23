"""User-approved human-error scope, shared by current runners and manifests."""
APPROVED=tuple(f'H{i:02}' for i in range(1,12))+('H13',)
EXCLUDED=('H12','H14','H15','H16','H17')
DEFERRED=('H18',)
POLICY='human-error-scope/2026-10-23-user-v1'


def exclusion_reason(case):
    if 'H12' in case.get('humanErrorIds',[]):return 'H12'
    names=[case.get('family',''),case.get('kind','')]
    names.extend(e.get('family','') for e in case.get('events',[]))
    if any('cascade-removal' in n or 'cascade_removal' in n for n in names):return 'H12'
    if set(case.get('humanErrorIds',[]))&set(EXCLUDED):return 'user-excluded-human-error'
    return None


def allowed(case):return exclusion_reason(case) is None


def require_allowed(case):
    reason=exclusion_reason(case)
    if reason:raise ValueError(f'This case is outside the user-approved benchmark scope: {reason}')
