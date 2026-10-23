"""One image/input contract shared by humans and API models."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent),str(HERE.parent/'eval')]
from dynamic_v5.vision import DynamicVisionRenderer
from vision import images
VIEWS=('isometric','top','rear')
SYSTEM='''Build the fixed target from an empty white baseplate, one movable part per attach or detach. This is one continuing episode. Every decision receives BEFORE LAST ACTION / CURRENT NOW images in three labeled views, separate FINAL TARGET views, and all inventory pages. The left and right are two times of the same scene, not two objects. At the first decision there is no previous action. Compare the actual current scene with your own previous action and the target. The environment may change without a message; feedback describes only whether your action was accepted. Inspect any time to see all candidate pages for a selected part, another view, or a crop. All candidates are shown uniformly in the current scene; no card indicates correctness. Use a candidate ID or a normalized click within a catalog page. One response must be a JSON object with action and unexpectedChange. unexpectedChange is true only for a new external change beyond your previous action; use false at the first decision. An optional note is allowed but never required. Attach requires partId and either candidate or catalogPage+catalogPoint. Detach requires partId. Inspect may specify partId or view or point or crop. Finish ends the episode even when incomplete. Rejected actions leave the actual state unchanged. No more than one action per response.'''
POINT_GUIDE=''' For inspect point [x,y] and crop [left,top,right,bottom], coordinates are normalized over the CURRENT scene rectangle alone: the right 800x600 scene inside a temporal-pair image, excluding its 36-pixel header. The scene fills x=800..1599 and y=36..635 of the 1600x636 comparison image. Convert a pixel (u,v) in that right scene to point [(u-800)/800,(v-36)/600]. Coordinates do not refer to the entire comparison image or the left scene. catalogPoint instead remains normalized over the entire candidate-catalog page.'''
SYSTEM+=POINT_GUIDE

def renderer_for(ep):
    r=DynamicVisionRenderer(ep.cert,ep.runtime);r.catalog_in_context=True;ep.vision_renderer=r;return r

def packet(ep,renderer,directory,extra=None,diagnostic=False):
    records=images(ep,renderer,Path(directory),extra=extra,views=VIEWS,previous_state=ep.previous_state,
                   paired_layout=True,expected_state=ep.expected_after_last_action if diagnostic else None)
    obs=ep.observe()
    obs['track']='expected-actual-diagnostic' if diagnostic else 'visual-temporal-v6'
    obs['providedViews']=list(VIEWS)
    obs['imagePages']=[{k:v for k,v in x.items() if k not in ('file','sha256','detail')} for x in records]
    obs['inspectionCoordinates']={'pointAndCrop':'CURRENT scene rectangle only; right half excluding header',
        'sceneRectangleInTemporalPairPixels':[800,36,1600,636],
        'pointFromPixel':'[(u-800)/800, (v-36)/600]',
        'catalogPoint':'entire candidate-catalog page'}
    if diagnostic:obs['visualTiming']['left']='Simulator prediction after your own previous action only; this diagnostic supplies extra information.'
    return obs,records
