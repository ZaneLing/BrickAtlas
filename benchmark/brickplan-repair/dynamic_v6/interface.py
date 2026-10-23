"""One image/input contract shared by humans and API models."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent),str(HERE.parent/'eval')]
from dynamic_v5.vision import DynamicVisionRenderer
from vision import images
VIEWS=('isometric','top','rear')
SYSTEM='''Build the fixed TARGET from an empty white baseplate, one movable part per attach or detach. This is one continuing episode. Three current-target pages show CURRENT NOW on the left and the sole required TARGET on the right, in isometric/top/rear views. After an action, three additional temporal-pair pages show BEFORE LAST ACTION on the left and CURRENT NOW on the right. These are different views/times of one assembly; never add their pieces together. Each page uses the same 1600x636 canvas with two 800x600 scene rectangles and a 36-pixel caption. At the first decision no temporal page is needed. Inventory contact sheets include all movable pieces and spares. There is no instruction manual for this from-empty track. Compare the actual current scene with your own previous action and the target. The environment may change without a message; feedback describes only whether your action was accepted. Inspect any time to see candidate pages for a selected part, another view, or a crop. All candidates are shown uniformly in the current scene; no card indicates correctness. Use a candidate ID or a normalized click within a catalog page. One response must be a JSON object with action and unexpectedChange. unexpectedChange is true only for a new external change beyond your previous action; use false at the first decision. An optional note is allowed but never required. Attach requires partId and either candidate or catalogPage+catalogPoint. Detach requires partId. Inspect may specify partId or view or point or crop. Finish ends the episode even when incomplete. Rejected actions leave the actual state unchanged. No more than one action per response.'''
POINT_GUIDE=''' Inspect point [x,y] and crop [left,top,right,bottom] are normalized over the CURRENT scene rectangle alone, excluding the caption. In a current-target page CURRENT is [0,36,800,636], so pixel (u,v) becomes [u/800,(v-36)/600]. In a temporal-pair page CURRENT is [800,36,1600,636], so it becomes [(u-800)/800,(v-36)/600]. Both give the same scene coordinates. Do not normalize over the entire comparison page. catalogPoint remains normalized over the entire candidate-catalog page.'''
SYSTEM+=POINT_GUIDE

def renderer_for(ep):
    r=DynamicVisionRenderer(ep.cert,ep.runtime);r.catalog_in_context=True;ep.vision_renderer=r;return r

def packet(ep,renderer,directory,extra=None,diagnostic=False):
    records=images(ep,renderer,Path(directory),extra=extra,views=VIEWS,previous_state=ep.previous_state,
                   matched_layout=True,expected_state=ep.expected_after_last_action if diagnostic else None)
    obs=ep.observe()
    obs['track']='expected-actual-diagnostic' if diagnostic else 'visual-temporal-v6'
    obs['providedViews']=list(VIEWS)
    obs['visualProtocol']='matched-canvas/1'
    obs['targetDisplay']={'role':'target','pageRole':'current-target','panel':'right',
                          'policy':'sole required final state; no competing completion reference'}
    obs['imagePages']=[{k:v for k,v in x.items() if k not in ('file','sha256','detail')} for x in records]
    obs['inspectionCoordinates']={'pointAndCrop':'CURRENT scene rectangle only; exclude header',
        'sceneRectangleInCurrentTargetPixels':[0,36,800,636],
        'sceneRectangleInTemporalPairPixels':[800,36,1600,636],
        'pointFromCurrentTargetPixel':'[u/800, (v-36)/600]',
        'pointFromTemporalPixel':'[(u-800)/800, (v-36)/600]',
        'catalogPoint':'entire candidate-catalog page'}
    if diagnostic:obs['visualTiming']['temporalPair']['left']='Simulator prediction after your own previous action only; privileged diagnostic information.'
    return obs,records
