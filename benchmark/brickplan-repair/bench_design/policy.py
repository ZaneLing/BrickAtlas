"""Keep physical faults, human explanations and temporal conditions separate."""
INPUT_VERSION='brick-atlas-direct-actions-full-context/1'
FAULTS={
 'missing':('E01','少件'), 'removed_piece':('E01','少件'), 'repeat-omission':('E01','少件'),
 'extra':('E02','多件'), 'extra_layer':('E02','多件'), 'extra-layer':('E02','多件'), 'repeated-step':('E02','多件'),
 'wrong_color':('E03','错色'), 'wrong-color':('E03','错色'), 'buried_wrong_color':('E03','错色'), 'buried-repair':('E03','错色'),
 'wrong_type':('E04','错零件'), 'wrong_part':('E04','错零件'), 'wrong-part':('E04','错零件'), 'wrong_size':('E04','错零件'),
 'offset':('E05','位置偏移'), 'shifted_piece':('E05','位置偏移'), 'height_layer':('HEIGHT','高度／层数异常（组合标签）'),
 'rotation':('E06','方向错误'), 'rotated':('E06','方向错误'), 'rotated_piece':('E06','方向错误'),
 'swapped_positions':('E07','位置关系互换'), 'left-right-swap':('E07','位置关系互换'),
 'early_cover':('P01','提前挡住安装通路'), 'early-cover':('P01','提前挡住安装通路'),
 'compound':('MIX','同时多错'), 'compound_fault':('MIX','同时多错'),
 'repair_state':('DERIVED','可验证修复中的状态，基本类别待细分'),
 'none':('OK','无错误对照'), 'control':('OK','无错误对照'),
}


def tags(family):
    if family.startswith('multiple-'):
        return sorted({FAULTS[f][0] for f in family.removeprefix('multiple-').split('then-')}), '连续多次干扰'
    if family not in FAULTS:raise ValueError('Unclassified family: '+family)
    code,name=FAULTS[family];return [code],name


def descriptors(parts,moves,covers,events,family,mode='dynamic',target_parts=None):
    # These are measured structural descriptors, not human/model success labels.
    basis=target_parts if mode=='static' and target_parts is not None else parts
    length='B1' if basis<=12 else 'B2' if basis<=24 else 'B3'
    rework=('R0' if family in ('none','control') else 'R3' if covers or (moves is not None and moves>=7)
            else 'R2' if moves is None or moves>=3 or family in ('compound','compound_fault','repeat-omission')
            else 'R1')
    level='G3' if length=='B3' or events>=3 or (events>=2 and rework=='R3') else 'G2' if length=='B2' or rework in ('R2','R3') or events>=2 else 'G1'
    return dict(buildLength=length,rework=rework,eventLevel='T'+str(events),planningLevel=level,
        gradingParts=basis,lengthBasis='current-stage-target' if mode=='static' else 'complete-operable-build',
        activeParts=parts,referenceRepairMoves=moves,referenceCorrectCoverRemovals=covers,
        empiricalDifficulty=None,difficultyStatus='STRUCTURAL_DESCRIPTORS_ONLY')
