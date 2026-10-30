"""Public tool contract: explicit defaults, bounded syntax normalization, no GT."""
import json,re
from copy import deepcopy

VERSION='brick-atlas-tool-contract/3'
SPECS={
 'observe':dict(required=[],defaults=dict(view='angled',rotateDegrees=0,show=['current']),
   optional=['view','rotateDegrees','show','inventoryPage','focus'],
   example=dict(tool='observe',args=dict(rotateDegrees=90,show=['current','inventory']))),
 'inspect':dict(required='partId OR manualStep OR point, never combined',defaults=dict(page=1),optional=['partId','page','manualStep','candidate','point','view'],
   example=dict(tool='inspect',args=dict(partId='PART_ID_FROM_INVENTORY',page=1))),
 'attach':dict(required=['partId','candidate'],optional=[],example=dict(tool='attach',args=dict(partId='PART_ID_FROM_INVENTORY',candidate='POSITION_ID_FROM_REQUESTED_PAGE'))),
 'detach':dict(required=['partId'],optional=[],example=dict(tool='detach',args=dict(partId='PART_ID_FROM_INVENTORY'))),
 'recall':dict(required=['decision'],optional=['scope'],defaults=dict(scope='current'),example=dict(tool='recall',args=dict(decision=0))),
 'finish':dict(required=[],optional=[],example=dict(tool='finish',args={})),
}
TOOLS=dict(version=VERSION,tools=SPECS,
 values=dict(view=['angled','top'],show=['current','target','inventory'],focus=['module','whole'],scope=['current','prefix']),
 normalization=['Omitted observe fields use angled, 0 degrees and current scene.',
  'isometric is an alias of angled. Rotations are multiples of 90 degrees, normalized modulo 360.',
  'Integer strings are accepted for page, manualStep, inventoryPage, decision and rotateDegrees.',
  'Part IDs and candidate IDs are exact strings; no guessed IDs or actions.',
  'One complete JSON object in a code fence or after prose is accepted. Multiple objects, broken JSON and truncated generation are never guessed or executed.',
  'Omitted plan/notes keep previous memory. Memory limits do not invalidate a physical action.'],
 note='Examples demonstrate syntax only. Their IDs and placements are not recommendations for this task.')


def strict_json(value):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('Duplicate JSON key: '+k)
            out[k]=v
        return out
    def constant(value):raise ValueError('Non-finite JSON number: '+value)
    return json.loads(value,object_pairs_hook=pairs,parse_constant=constant) if isinstance(value,str) else deepcopy(value)


def validate(reply,*,memory=False,limits=None):
    errors=[];normalizations=[];limits=limits or {}
    try:
        try:obj=strict_json(reply)
        except ValueError:
            if not isinstance(reply,str):raise
            text=reply.strip()
            fenced=re.fullmatch(r'```(?:json)?\s*([\s\S]*?)\s*```',text,re.I)
            if fenced:
                obj=strict_json(fenced[1]);normalizations.append('single JSON code fence removed')
            else:
                start=text.find('{')
                # Only one complete final object is accepted. Never choose
                # between actions, repair broken JSON, or process truncation.
                if start<=0 or any(c in text[:start] for c in '{}[]'):raise
                obj=strict_json(text[start:]);normalizations.append('prose before one complete final JSON object removed')
    except (ValueError,TypeError) as exc:
        return dict(action=dict(tool='invalid',args={}),valid=False,jsonError=True,errors=[str(exc)],normalizations=[])
    def bad(message):errors.append(message)
    if not isinstance(obj,dict):obj={};bad('Return one JSON object.')
    allowed={'tool','args'}|({'plan','notes'} if memory else set())
    if set(obj)-allowed:bad('Unknown top-level fields: '+', '.join(sorted(set(obj)-allowed)))
    name=obj.get('tool');args=deepcopy(obj.get('args',{}))
    if not isinstance(name,str) or name not in SPECS:bad('tool must be observe, inspect, attach, detach, recall or finish.')
    if not isinstance(args,dict):args={};bad('args must be an object.')
    if isinstance(name,str) and name in SPECS:
        spec=SPECS[name];allowed_args=set(spec['optional'])|set(spec['required'] if isinstance(spec['required'],list) else [])
        if set(args)-allowed_args:bad('Unknown args fields: '+', '.join(sorted(set(args)-allowed_args)))
        for field in ('page','manualStep','inventoryPage','decision','rotateDegrees'):
            if field in args and isinstance(args[field],str) and re.fullmatch(r'-?\d+',args[field]):
                args[field]=int(args[field]);normalizations.append(field+': integer string converted')
        if name=='observe':
            for k,v in spec['defaults'].items():
                if k not in args:args[k]=deepcopy(v);normalizations.append(k+': documented default')
            if args.get('view')=='isometric':args['view']='angled';normalizations.append('isometric -> angled')
            rotation=args.get('rotateDegrees')
            if type(rotation) is not int or rotation%90:bad('rotateDegrees must be an integer multiple of 90.')
            else:
                normalized={0:0,90:90,180:180,270:-90}[rotation%360]
                if rotation!=normalized:normalizations.append('rotation modulo 360')
                args['rotateDegrees']=normalized
            if args['view'] not in ('angled','top'):bad('view must be angled (or isometric) or top.')
            show=args['show']
            if not isinstance(show,list) or not show or any(not isinstance(s,str) or s not in TOOLS['values']['show'] for s in show):bad('show must be a nonempty list of current, target and/or inventory.')
            elif len(set(show))!=len(show):bad('show must not contain duplicate roles.')
            if 'inventoryPage' in args and (type(args['inventoryPage']) is not int or args['inventoryPage']<1):bad('inventoryPage must be >= 1.')
            if args.get('focus','module') not in ('module','whole'):bad('focus must be module or whole.')
        elif name=='inspect':
            if sum(k in args for k in ('partId','manualStep','point'))!=1:bad('inspect needs exactly one of partId, manualStep or point.')
            if 'manualStep' in args:
                if set(args)!={'manualStep'}:bad('manualStep cannot be combined with partId/page.')
                if type(args['manualStep']) is not int or args['manualStep']<1:bad('manualStep must be >= 1.')
            elif 'point' in args:
                if set(args)-{'point','view'}:bad('point may only be combined with view.')
                point=args['point']
                if not isinstance(point,list) or len(point)!=2 or any(type(x) not in (int,float) or not 0<=x<=1 for x in point):bad('point must be [x,y] normalized to the full current image, between 0 and 1.')
                if args.get('view','isometric') not in ('isometric','rear','top'):bad('point view must be isometric, rear or top.')
            else:
                if type(args.get('page',1)) is not int or args.get('page',1)<1:bad('page must be >= 1.')
                if 'candidate' in args and 'page' in args:bad('Use candidate for one enlarged preview or page for a catalogue, not both.')
                if 'view' in args and args['view'] not in ('isometric','rear','top'):bad('inspect view must be isometric, rear or top.')
        elif name=='recall':
            if type(args.get('decision')) is not int or args['decision']<0:bad('decision must be >= 0; 0 is the initial packet.')
            if args.get('scope','current') not in ('current','prefix'):bad('scope must be current or prefix.')
        if isinstance(spec['required'],list):
            for field in spec['required']:
                if field not in args:bad('Missing args.'+field)
        for field in ('partId','candidate'):
            if field in args and (not isinstance(args[field],str) or not args[field]):bad(field+' must be a nonempty exact ID string.')
    action=dict(tool=name,args=args)
    if memory:
        for k in ('plan','notes'):
            if k not in obj:continue
            val=obj[k]
            if k=='plan':
                if not isinstance(val,list) or any(not isinstance(i,str) for i in val):bad('plan must be a list of strings.');continue
                limited=[i[:limits.get('planItemCharacters',160)] for i in val[:limits.get('planItems',6)]]
            else:
                if not isinstance(val,str):bad('notes must be a string.');continue
                limited=val[:limits.get('notesCharacters',1200)]
            action[k]=limited
            if limited!=val:normalizations.append(k+': trimmed to published memory limit')
    return dict(action=action if not errors else dict(tool='invalid',args={}),valid=not errors,jsonError=False,
        errors=errors,normalizations=normalizations,example=SPECS.get(name,{}).get('example',SPECS['observe']['example']) if isinstance(name,str) else SPECS['observe']['example'])
