"""One common policy loop. Every observation and action is chosen by the backbone.

Persistent memory contains only public observations and model-authored short
plans/notes. Ground truth, scores, disturbances, and spectator views are excluded.
"""
import base64,hashlib,json,time
from copy import deepcopy
from dynamic_arena import OUT as ARENA_OUT
from dynamic_arena.tool_arena import ToolArena,TOOLS
from dynamic_arena.contract import validate
from dynamic_arena.transport import write_json
from bench_design.session import digest
from unified_agent import PROTOCOL
from unified_agent.profile import profile
from unified_agent.providers import CostLimit
from unified_agent.failures import terminal_for,describe,GenerationError

SYSTEM='''You operate a continuous LEGO assembly Arena. Match the sole TARGET with any physically legal assembly order. You control every action and every extra observation. The initial packet contains three current views, the same three target views, and inventory page 1. After an action NO new scene image is sent automatically: call observe to inspect what is really there. An unannounced environment change may occur after a physical move. Action success only says your requested move was legal; it does not certify that the scene still matches your expectations.
Use observe to change camera or inspect stock, inspect to view neutral placement candidates or an optional instruction step, attach/detach to move ONE physical part, recall to retrieve an old observation, and finish to submit the final state. inspect with partId and candidate gives an enlarged current/proposed comparison; inspect with point [x,y] and a preset view identifies only the visible part at that image point. Optional manual pages identify the pictured part handle so you can find its candidate catalogue. Each partId is one physical part; parts and stock are finite. Candidate previews are hypothetical; they do not say a placement is legal or correct. Position IDs do not encode the answer. A manual is a possible order, never a mandatory one. For a task permitting equivalent assemblies, use its explicit target contract.
Your memory is maintained in the same way every turn: all target views, the latest two requested scene observations, the latest inventory page, the latest candidate/manual page, recent tool dialogue, and YOUR short plan and notes. Images have capture timestamps and can be stale. A recalled or remembered image is not a new observation. Additional pages, angles and instructions are available through tools. No hidden state, evaluator score, or suggested action is supplied.
Reply with exactly one JSON object containing tool and args; plan and notes are optional updates. plan is at most 6 short next-step items (160 characters each). notes is at most 1200 characters of concise operational facts/uncertainties you want to retain. Do not write an essay or private reasoning trace. Provided plan/notes replace the previous values; omitted fields preserve memory. Long memory is trimmed at the published limits. observe with empty args means current scene, angled view, 0 degree rotation; isometric is accepted as an alias of angled. Example: {"tool":"inspect","args":{"partId":"PART_ID_FROM_INVENTORY","page":1},"plan":["Locate a legal base placement","Build and visually verify"],"notes":"I have not installed any pieces yet."}. Tool errors are feedback; decide your next step yourself.'''


def parse_agent(reply,p):
    result=validate(reply,memory=True,limits=p)
    return result['action'],result['valid']


class VisualAgent(ToolArena):
    def __init__(self,session,transport,configuration=None):
        self.profile=deepcopy(configuration or profile())
        session.cap=max(session.cap,self.profile['maxDecisions'])
        for attr,needed in [('decision_budget',self.profile['maxDecisions']),('manipulation_budget',self.profile['maxActions'])]:
            if hasattr(session.ep,attr) and getattr(session.ep,attr)<needed:
                raise ValueError('Native '+attr+' is below the declared agent budget')
        super().__init__(session,transport,self.profile['maxDecisions'])
        session.agent_input_version=PROTOCOL
        self.plan,self.notes=[],''
        self.action_attempts=self.observation_attempts=0
        self.target_images=[];self.scene_memory=[];self.inventory_images=[];self.catalogue_images=[];self.extra_target_images=[]
        self.inventory_snapshot=[];self.initial_images=[]
        for view in self.profile['initialViews']:
            self.target_images.append(self.capture(self.session.goal,'target',view))
        initial=[self.capture(self.session.ep.state,'current',view) for view in self.profile['initialViews']]
        self.scene_memory=[initial]
        self.inventory_images=[self.image(self.sensors.inventory(1),'inventory',page=1,pages=self.sensors.inventory_count,observedAfterDecision=0)]
        self.inventory_snapshot=deepcopy(self.sensors.availability(page=1))
        self.initial_images=self.target_images+initial+self.inventory_images
        self.archive[0]=deepcopy(self.initial_images)
        from dynamic_arena.run import task_digest
        from pathlib import Path
        self.contract_sha=digest(dict(initial=session.initial,goal=session.goal,certificate=session.ep.runtime.cert,
            aliases=self.sensors.handles(),inventory=sorted(getattr(session.ep.runtime,'available',[])),
            profile=self.profile,system=SYSTEM,tools=TOOLS,environment=task_digest(session,self.cap),
            implementation={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ['agent.py','profile.py','providers.py']},
            assemblyImplementation=hashlib.sha256(Path(__file__).parents[1].joinpath('assembly.py').read_bytes()).hexdigest()))

    def capture(self,state,role,view='isometric',angles=None,focus='module'):
        return self.image(self.render(state,view,angles,focus),role,view=view,
            camera={'azimuthDegrees':angles[0],'elevationDegrees':angles[1]} if angles else {'preset':view},
            observedAfterDecision=len(self.session.records),focus=focus)

    def public_request(self):
        value=super().public_request()
        for key in ('payloadLimits','observationPolicy','decisionBudget'):value.pop(key,None)
        value.update(protocol=PROTOCOL,profile=self.profile,
            observationPolicy=self.profile['observationRule'],
            memory=dict(plan=self.plan,notes=self.notes,inventorySnapshot=self.inventory_snapshot,
                        inventoryCapturedAfterDecision=self.inventory_images[0]['observedAfterDecision'] if self.inventory_images else None),
            budget=dict(decisionsRemaining=self.cap-len(self.calls),actionsRemaining=self.profile['maxActions']-self.action_attempts,
                        observationRequestsRemaining=self.profile['maxObservations']-self.observation_attempts,
                        generatedTokensRemaining=self.profile['maxGeneratedTokens']-self.transport.usage().get('completionTokens',0)),
            responseSchema=dict(required=['tool'],tool='one available tool',args='object; omitted means empty object',plan='optional list, up to 6 short operational steps',notes='optional operational notes, max 1200 characters'),
            visualMemoryPolicy='Same image pixels are retained; capture time is explicit. Old images are NOT refreshed when the world changes.',
            pagination=dict(inventoryItemsPerPage=12,candidateItemsPerPage=12))
        return value

    def request(self):
        visible=self.public_request()
        refs=self.target_images+[im for batch in self.scene_memory for im in batch]+self.inventory_images+self.catalogue_images+self.extra_target_images
        # Same file may occur in different semantic roles; preserve those labels.
        unique=[];seen=set()
        for original in refs:
            asset=deepcopy(original);key=(asset['sha256'],asset['role'],asset.get('observedAfterDecision'))
            if key in seen:continue
            seen.add(key)
            start=asset.get('observedAfterDecision',0)
            asset['physicalActionsSinceCapture']=sum(r['action'].get('type') in ('attach','detach') for r in self.session.records[start:]) if asset['role']!='target' else 0
            asset['historicalNotLive']=asset['role']!='target' and asset['physicalActionsSinceCapture']>0
            unique.append(asset)
        content=[dict(type='text',text=json.dumps(visible,ensure_ascii=False))]
        readable_content=[dict(type='text',value=visible)]
        for asset in unique:
            raw=(ARENA_OUT/asset['url'].lstrip('/')).read_bytes()
            if hashlib.sha256(raw).hexdigest()!=asset['sha256']:raise ValueError('Image hash mismatch')
            meta={k:v for k,v in asset.items() if k!='url'}
            content.extend([dict(type='text',text=json.dumps(meta)),dict(type='image_url',image_url=dict(url='data:image/png;base64,'+base64.b64encode(raw).decode(),detail='high'))])
            readable_content.extend([dict(type='text',value=meta),dict(type='image_url',image_url=dict(**asset,detail='high'))])
        recent=self.history[-2*self.profile['textHistoryTurns']:]
        provider=dict(model=self.model,messages=[dict(role='system',content=SYSTEM),*recent,dict(role='user',content=content)])
        readable=dict(model=self.model,system=SYSTEM,messages=[*recent,dict(role='user',content=readable_content)],
            binaryImagePolicy='Exact PNG bytes are in raw API requests; these URLs and hashes identify the same pixels.')
        return provider,readable,visible,unique

    def observe(self,args,number):
        if 'inventory' in args['show'] and not 1<=args.get('inventoryPage',1)<=self.sensors.inventory_count:
            raise ValueError('inventoryPage must be between 1 and '+str(self.sensors.inventory_count))
        self.azimuth=(self.azimuth+args['rotateDegrees'])%360
        self.elevation=90 if args['view']=='top' else 30
        angles=(self.azimuth,self.elevation);view='top' if self.elevation==90 else 'isometric'
        images=[]
        # Render before the inspect record; observation has no physical effect.
        for role in args['show']:
            if role=='inventory':
                page=args.get('inventoryPage',1)
                images.append(self.image(self.sensors.inventory(page),role,page=page,pages=self.sensors.inventory_count,observedAfterDecision=len(self.session.records)))
            else:images.append(self.capture(self.session.ep.state if role=='current' else self.session.goal,role,view,angles,args.get('focus','module')))
        self.session.submit(dict(type='inspect',view='isometric'))
        if 'current' in args['show']:
            self.scene_memory=(self.scene_memory+[[im for im in images if im['role']=='current']])[-2:]
        if 'inventory' in args['show']:
            self.inventory_images=[im for im in images if im['role']=='inventory']
            self.inventory_snapshot=deepcopy(self.sensors.availability(page=args.get('inventoryPage',1)))
        if 'target' in args['show']:self.extra_target_images=[im for im in images if im['role']=='target']
        self.archive[number]=images
        return dict(code='OBSERVED',images=images,camera=dict(azimuthDegrees=self.azimuth,elevationDegrees=self.elevation),
            environmentDecision=len(self.session.records),**({'inventoryAvailability':self.inventory_snapshot} if 'inventory' in args['show'] else {}))

    def execute(self,action,number):
        name=action['tool'];group='action' if name in ('attach','detach') else 'observation' if name in ('observe','inspect','recall') else None
        if group:
            key='action_attempts' if group=='action' else 'observation_attempts'
            limit=self.profile['maxActions' if group=='action' else 'maxObservations']
            if getattr(self,key)>=limit:
                self.session.submit(dict(type='invalid'))
                return dict(code='RESOURCE_BUDGET_EXHAUSTED',resource=group,stateChanged=False),[]
            setattr(self,key,getattr(self,key)+1)
        output,images=super().execute(action,number)
        if name=='inspect' and images:
            for im in images:im['observedAfterDecision']=len(self.session.records)
            self.catalogue_images=images
        elif name=='recall' and images:
            # Recalled images keep their original capture timestamp.
            self.catalogue_images=deepcopy(images)
        return output,images

    def step(self,reply,request=None):
        provider,readable,visible,images=request or self.request()
        number=len(self.calls)+1
        validation=validate(reply,memory=True,limits=self.profile)
        action,valid=validation['action'],validation['valid']
        self._tool_parse_failed=validation['jsonError']
        if valid:self.plan,self.notes=deepcopy(action.get('plan',self.plan)),action.get('notes',self.notes)
        self.session._pending_observation=dict(decision=len(self.session.records)+1,packetSha256=digest(visible),imageHashes=[im['sha256'] for im in images])
        output,returned=self.execute(action,number)
        output['syntaxNormalization']=validation['normalizations']
        if not valid:output.update(validationErrors=validation['errors'],example=validation.get('example',TOOLS['tools']['observe']['example']))
        self.last_result=output
        receipt=getattr(self.transport,'latest',None)
        call=dict(index=number,modelInput=readable,modelOutputRaw=reply,modelOutput=action,environmentOutput=output,outputValidation=validation,
            memoryAfter=dict(plan=self.plan,notes=self.notes),inputImageHashes=[im['sha256'] for im in images],
            inputImagePixels=sum(im['width']*im['height'] for im in images),requestBytes=len(json.dumps(provider).encode()),
            requestContextSha256=digest(provider),providerReceipt=None)
        if receipt:
            call['providerReceipt']=dict(id=receipt['result']['id'],archiveId=receipt['archiveId'],requestBodySha256=receipt['requestBodySha256'],
                costUSD=receipt['costUSD'],costBasis=receipt['costBasis'],nativeCurrency=receipt['nativeCurrency'],
                inputTokens=receipt['result']['usage']['prompt_tokens'],outputTokens=receipt['result']['usage']['completion_tokens'],
                reasoningTokens=receipt['result']['usage'].get('completion_tokens_details',{}).get('reasoning_tokens'),
                finishReason=receipt['result']['choices'][0].get('finish_reason'),latencySeconds=receipt['latencySeconds'])
        self.calls.append(call)
        history_result={k:v for k,v in output.items() if k!='images'}
        self.history.extend([dict(role='assistant',content=reply if isinstance(reply,str) else json.dumps(reply)),
            dict(role='user',content=json.dumps(dict(toolResult=history_result),ensure_ascii=False))])
        self.spectator_frame(action,output);self.session.save()
        print(json.dumps(dict(run=self.session.directory.name,decision=number,tool=action['tool'],args=action['args'],feedback=output['code'],cost=self.transport.usage()['costUSD']),ensure_ascii=False),flush=True)
        return output

    def result(self):
        value=super().result();value.update(inputVersion=PROTOCOL,agentProfile=self.profile,agentContractSha256=self.contract_sha,
            experimentArm='dynamic-visual-agent',agentMemory=dict(plan=self.plan,notes=self.notes))
        value['controllerMetrics'].update(actionAttempts=self.action_attempts,observationRequests=self.observation_attempts,
            inspectCalls=sum(c.get('modelOutput',{}).get('tool')=='inspect' for c in self.calls),
            formatErrors=sum(c.get('modelOutput',{}).get('tool')=='invalid' for c in self.calls),
            actionBudget=self.profile['maxActions'],observationBudget=self.profile['maxObservations'])
        value['inputMetrics']['maxImagesPerRequest']=max(value['inputMetrics']['imageCounts'],default=0)
        value['inputMetrics']['configuredTwoImageLimit']=False
        value['inputMetrics']['initialImages']=len(self.initial_images)
        # Controller budget rejections are not malformed model JSON.
        value['executionMetrics']['formatErrorResponses']=sum(bool(c.get('outputValidation',{}).get('jsonError')) for c in self.calls)
        value['executionMetrics']['schemaErrorResponses']=sum(c.get('modelOutput',{}).get('tool')=='invalid' and not c.get('outputValidation',{}).get('jsonError') for c in self.calls)
        value['executionMetrics']['budgetRejectedResponses']=sum(c.get('environmentOutput',{}).get('code') in ('RESOURCE_BUDGET_EXHAUSTED','BUDGET_EXHAUSTED') for c in self.calls)

        value['interfaceMetrics']=dict(normalizedDecisions=sum(bool(c.get('outputValidation',{}).get('normalizations')) for c in self.calls),
            invalidDecisions=sum(c.get('modelOutput',{}).get('tool')=='invalid' for c in self.calls),
            attribution='mixed_interface_and_assembly' if any(c.get('modelOutput',{}).get('tool')=='invalid' for c in self.calls) else 'no_schema_errors')
        value['assemblyScoreEligible']=value['terminalStatus'] in ('completed','model_budget_exhausted') and not value['interfaceMetrics']['invalidDecisions']
        return value

    def publish(self):
        super().publish()
        path=self.session.directory/'spectator.json'
        state=json.loads(path.read_text());state.update(protocol=PROTOCOL,agentProfile=self.profile,
            experimentArm='dynamic-visual-agent',initialImages=self.initial_images,
            inputMode='initial three views + persistent visual memory + agent-requested observations',
            agentMemory=dict(plan=self.plan,notes=self.notes),budgetCounters=dict(actions=self.action_attempts,observations=self.observation_attempts))
        write_json(path,state)

    def run(self,stop_after_incident=False):
        self.spectator_frame()
        while not self.session.done and len(self.calls)<self.cap:
            provider=readable=None;images=[]
            if self.transport.usage().get('completionTokens',0)+self.profile['maxOutputTokensPerDecision']>self.profile['maxGeneratedTokens']:
                self.session.terminal='model_budget_exhausted';break
            try:
                provider,readable,visible,images=self.request();self.phase='thinking';self.publish()
                reply=self.transport(provider)
            except Exception as exc:
                self.session.terminal=('client_budget_exhausted' if isinstance(exc,CostLimit) else terminal_for(exc) if provider else 'harness_error')
                receipt=getattr(self.transport,'latest',None)
                archive=getattr(self.transport,'latest_attempt',None)
                if receipt:archive=dict(archiveId=receipt['archiveId'],requestBodySha256=receipt['requestBodySha256'],responseAvailable=True)
                self.calls.append(dict(index=len(self.calls)+1,modelInput=readable,inputImageHashes=[im['sha256'] for im in images],
                    inputImagePixels=sum(im['width']*im['height'] for im in images),providerReceipt=archive,
                    error=describe(exc),environmentOutput=dict(code=self.session.terminal,stateChanged=False,actionExecuted=False)))
                break
            self.step(reply,(provider,readable,visible,images))
        if not self.session.done and self.session.terminal is None:self.session.terminal='model_budget_exhausted'
        self.phase='finished';self.session.save();self.publish()
        result=self.result();write_json(self.session.directory/'result.json',result)
        write_json(self.session.directory/'log.json',dict(protocol=PROTOCOL,profile=self.profile,initialImages=self.initial_images,calls=self.calls,result=result))
        return result
