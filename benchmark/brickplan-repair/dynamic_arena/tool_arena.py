"""Pull-observation arena: the model calls every camera and assembly tool."""
import argparse
import base64
import fcntl
import hashlib
import io
import json
from pathlib import Path
import time
from PIL import Image
from bench_design.session import digest
from dynamic_arena import OUT, MODEL
from dynamic_arena.demo import create, CASE_ID, TITLE
from dynamic_arena.sensors import Sensors
from dynamic_arena.transport import Transport, write_json

PROTOCOL = 'brick-atlas-tool-arena/3'
SYSTEM = '''You control one continuous LEGO assembly episode. The starting scene may be an empty white studded baseplate or a preassembled object with a named section to finish. Match the sole target; all physically legal assembly orders are accepted. Call exactly ONE tool per JSON response, with only tool and args. Use observe for current/target/inventory images, inspect for a part's neutral candidate positions or an optional instruction page, attach or detach to move one physical part, recall to retrieve a previously requested image, and finish to submit. No image is supplied automatically after a move. Observation is your responsibility. Environment changes may happen without announcement; feedback only describes your requested action. Choose observations, plan, build, recheck and repair autonomously. Anonymous handles do not encode answers. A candidate preview is hypothetical, not a legality or correctness label. Inventory is finite; one handle represents one physical part. For tasks explicitly allowing equivalent assemblies, match the stated colored volume and connections, not the illustrated seams. The manual provides a possible construction order, never a required order. Return a direct JSON object, for example {"tool":"observe","args":{"view":"angled","rotateDegrees":0,"show":["current","target","inventory"]}}.'''

TOOLS = {
    'observe': {'args': {'view': ['angled', 'top'], 'rotateDegrees': [-90, 0, 90, 180],
                         'show': ['current', 'target', 'inventory'],
                         'inventoryPage': 'optional 1-based page, default 1', 'focus': 'optional module (default) or whole'},
                'example': {'tool': 'observe', 'args': {'view': 'angled', 'rotateDegrees': 90,
                                                       'show': ['current', 'target']}}},
    'inspect': {'args': {'partId': 'part handle (candidate catalogue)', 'page': '1-based page; default 1', 'manualStep': 'instruction number; use instead of partId'}},
    'attach': {'args': {'partId': 'anonymous inventory handle', 'candidate': 'registered placement handle'}},
    'detach': {'args': {'partId': 'anonymous installed handle'}},
    'recall': {'args': {'decision': 'a previously requested observe decision number'}},
    'finish': {'args': {}}
}


def parse(reply):
    try:
        obj = json.loads(reply) if isinstance(reply, str) else reply
        if not isinstance(obj, dict) or set(obj) != {'tool', 'args'} or not isinstance(obj['args'], dict):
            raise ValueError('Expected tool and args')
        name, args = obj['tool'], obj['args']
        if name == 'attach' and set(args) == {'partId', 'candidate'} and all(isinstance(v, str) for v in args.values()):
            return obj
        if name == 'detach' and set(args) == {'partId'} and isinstance(args['partId'], str):
            return obj
        if name == 'finish' and not args:
            return obj
        if name == 'recall' and set(args) == {'decision'} and type(args['decision']) is int and args['decision'] > 0:
            return obj
        if name == 'inspect' and ((set(args) <= {'partId','page'} and isinstance(args.get('partId'),str) and type(args.get('page',1)) is int and args.get('page',1)>0) or (set(args)=={'manualStep'} and type(args['manualStep']) is int and args['manualStep']>0)):
            return obj
        if name == 'observe' and {'view','rotateDegrees','show'} <= set(args) <= {'view','rotateDegrees','show','inventoryPage','focus'}:
            show = args['show']
            if (args['view'] in ('angled', 'top') and type(args['rotateDegrees']) is int
                    and args['rotateDegrees'] in (-90, 0, 90, 180)
                    and isinstance(show, list) and show and len(show) == len(set(show))
                    and set(show) <= {'current', 'target', 'inventory'}
                    and type(args.get('inventoryPage',1)) is int and args.get('inventoryPage',1)>0
                    and args.get('focus','module') in ('module','whole')):
                return obj
    except (ValueError, TypeError, KeyError):
        pass
    return {'tool': 'invalid', 'args': {}}


class ToolArena:
    def __init__(self, session, transport, max_decisions=30):
        assert session.row['mode'] == 'dynamic' and not session.records
        session.row.setdefault('title', session.row['model'])
        assert type(max_decisions) is int and 1 <= max_decisions <= session.cap
        self.session, self.transport, self.cap = session, transport, max_decisions
        self.model = getattr(transport, 'model', MODEL)
        self.frames, self.calls, self.history, self.archive = [], [], [], {}
        self.azimuth, self.elevation = 35, 30
        self.pending_images, self.last_result = [], None
        self.phase, self.started = 'ready', time.time()
        self.asset_dir = OUT / 'assets'
        self.asset_dir.mkdir(parents=True, exist_ok=True)
        self.sensors = Sensors(session)

    def image(self, im, role, **extra):
        stream = io.BytesIO()
        im.save(stream, format='PNG')
        raw = stream.getvalue()
        sha = hashlib.sha256(raw).hexdigest()
        path = self.asset_dir / (sha + '.png')
        if not path.exists(): path.write_bytes(raw)
        return dict(role=role, url='/assets/' + sha + '.png', sha256=sha,
                    width=im.width, height=im.height, **extra)

    def render(self, state, view='isometric', angles=None, focus='module'):
        return self.sensors.render(state, view, angles, focus)

    def spectator_frame(self, action=None, feedback=None):
        scenes = {}
        for view in ('isometric', 'rear', 'top'):
            scenes[view] = dict(current=self.image(self.render(self.session.ep.state, view), 'spectator-current')['url'],
                                target=self.image(self.render(self.session.goal, view), 'spectator-target')['url'])
        frame = dict(index=len(self.calls), environmentStep=len(self.session.records), scenes=scenes,
                     action=action, feedback=feedback, events=[dict(index=e['index'], atDecision=e['atDecision'],
                     affected=[self.sensors.aliases.get(a,a) for a in e['native'].get('affected', [])],
                     description='环境干扰：'+str(e['native'].get('family',e['native'].get('kind','库存变化'))), verified=e['effectiveIncidentVerified'])
                     for e in self.session.events], recordedAt=time.time())
        self.frames.append(frame)
        self.publish()

    def public_request(self):
        number = len(self.calls) + 1
        handles = self.sensors.handles()
        return dict(protocol=PROTOCOL, episode='episode-'+self.session.run_id, decision=number, decisionBudget=self.cap,
                    task='Complete the sole target: ' + self.session.row['title'],
                    startingState='preassembled context; finish the indicated module' if self.session.ep.runtime.cert.get('fixed') or any(self.session.initial.values()) else 'empty white studded baseplate',
                    targetContract=self.session.ep.observe().get('targetContract','Match the target physical assembly.'),
                    physicalRules=['One physical part per attach/detach.', 'Any legal order is accepted.', 'Fixtures may support subassemblies; gravity, friction and snap force are not simulated.', 'No overlap; a straight insertion/removal path is required.'],
                    inventoryPages=self.sensors.inventory_count, manualSteps=self.sensors.manual_count,
                    inspectionOptions={'inventoryPage':'1-based; default 1','focus':['module','whole'],'candidatePages':'inspect partId and page'},
                    camera=dict(azimuthDegrees=self.azimuth, elevationDegrees=self.elevation),
                    actionHandles=handles, availableTools=TOOLS, lastToolResult=self.last_result,
                    observationPolicy='No images are sent unless you called observe, inspect or recall on the previous turn.',
                    disturbancePolicy='An environmental change may occur after a physical move without announcement.')

    def request(self):
        visible = self.public_request()
        content = [dict(type='text', text=json.dumps(visible, ensure_ascii=False, separators=(',', ':')))]
        image_refs = []
        for asset in self.pending_images:
            raw = (OUT / asset['url'].lstrip('/')).read_bytes()
            assert hashlib.sha256(raw).hexdigest() == asset['sha256']
            content.append(dict(type='text', text=json.dumps({k: v for k, v in asset.items() if k != 'url'}, ensure_ascii=False)))
            content.append(dict(type='image_url', image_url=dict(
                url='data:image/png;base64,' + base64.b64encode(raw).decode(), detail='high')))
            image_refs.append(asset)
        messages = [dict(role='system', content=SYSTEM), *self.history, dict(role='user', content=content)]
        provider = dict(model=self.model, messages=messages)
        # This is the exact message structure given to the transport. Binary
        # image contents are represented by verified URLs in the readable log.
        readable = dict(model=self.model, messages=[*self.history, dict(role='user', content=[
            dict(type='text', value=visible), *[dict(type='image_url', image_url=dict(
                url=a['url'], sha256=a['sha256'], detail='high', role=a['role'])) for a in image_refs]])],
            system=SYSTEM, binaryImagePolicy='URLs and hashes shown here; full base64 request is stored in api/*.request.json.gz')
        return provider, readable, visible, image_refs

    def observe(self, args, number):
        self.azimuth = (self.azimuth + args['rotateDegrees']) % 360
        self.elevation = 90 if args['view'] == 'top' else 30
        view = 'top' if self.elevation == 90 else 'isometric'
        angles = (self.azimuth, self.elevation)
        out = []
        for role in args['show']:
            if role == 'current': im = self.render(self.session.ep.state, view, angles, args.get('focus','module'))
            elif role == 'target': im = self.render(self.session.goal, view, angles, args.get('focus','module'))
            else: im = self.sensors.inventory(args.get('inventoryPage',1))
            if isinstance(im, dict):
                with Image.open(im['file']) as source: im = source.copy()
            out.append(self.image(im, role, camera=dict(azimuthDegrees=self.azimuth, elevationDegrees=self.elevation), **({'page':args.get('inventoryPage',1),'pages':self.sensors.inventory_count} if role=='inventory' else {})))
        self.session.submit(dict(type='inspect', view='isometric'))
        self.archive[number] = out
        return dict(code='OBSERVED', camera=dict(azimuthDegrees=self.azimuth, elevationDegrees=self.elevation),
                    images=out, environmentDecision=len(self.session.records),
                    **({'inventoryAvailability':self.sensors.availability()} if 'inventory' in args['show'] else {}))

    def execute(self, action, number):
        name, args = action['tool'], action['args']
        if name in ('observe','inspect'):
            try:
                if name=='observe': return self.observe(args,number),self.archive[number]
                if 'manualStep' in args:
                    im=self.sensors.instruction(args['manualStep']);meta=dict(step=args['manualStep'],isTarget=False,referenceOnly=True);role='instruction-reference'
                else:
                    im,meta=self.sensors.candidates(args['partId'],args.get('page',1),'top' if self.elevation==90 else 'isometric',(self.azimuth,self.elevation));role='candidate-catalog'
                self.session.submit(dict(type='inspect',view='isometric'))
                images=[self.image(im,role,**meta)];self.archive[number]=images
                return dict(code='OBSERVED',images=images,environmentDecision=len(self.session.records)),images
            except (KeyError,ValueError,IndexError):
                self.session.submit(dict(type='invalid'),parse_error=True)
                return dict(code='INVALID_SENSOR_REQUEST'),[]
        if name == 'recall':
            self.session.submit(dict(type='inspect',view='isometric'))
            images = self.archive.get(args['decision'])
            return (dict(code='HISTORY_AVAILABLE' if images else 'UNKNOWN_HISTORY_STEP',
                         historicalDecision=args['decision'], currentStateUnchanged=True,
                         images=images or []), images or [])
        if name in ('attach', 'detach', 'finish'):
            physical = dict(type=name, **args)
            feedback = self.session.submit(physical)
            return dict(code=feedback['code'], feedback=feedback,
                        environmentDecision=len(self.session.records),
                        stateChanged=feedback['code'] == 'OK',
                        visualUpdate='Call observe to see the current scene.'), []
        self.session.submit(dict(type='invalid'), parse_error=True)
        return dict(code='INVALID_TOOL_REQUEST', environmentDecision=len(self.session.records),
                    stateChanged=False), []

    def publish(self):
        result = self.result() if self.session.done else None
        state = dict(schema='brick-atlas-spectator-arena/2', protocol=PROTOCOL,
            runId=self.session.directory.name, title=self.session.row['title'],
            caseId=self.session.row['key'], model=self.model,
            phase=self.phase, startedAt=self.started, updatedAt=time.time(), frames=self.frames,
            calls=self.calls, usage=self.transport.usage(),
            targetParts=sum(bool(v) for v in self.session.goal.values()), maxDecisions=self.cap,
            result=result, fullModelControl=not self.session.actor.startswith('scripted'), scriptedPrefix=0, autoRepair=0, resets=0,
            formalBenchmarkResult=False,
            evaluationScope='per-task run; aggregate eligibility requires normal gate and source admission',
            evidenceType='scripted-validation' if self.session.actor.startswith('scripted') else 'api-model',
            condition='normal' if getattr(self.session,'control',False) else 'incident',
            track=self.session.row['evaluationMetadata']['track'], inputMode='model-requested observation images + tool JSON',
            spectatorNotice='Spectator camera images, event markers and score never enter model messages.')
        write_json(self.session.directory / 'spectator.json', state)
        if not self.session.directory.name.startswith('preview-'):
            write_json(OUT / 'latest.json', dict(runId=self.session.directory.name))

    def result(self):
        out = self.session.result()
        out['baseInputVersion'] = out['inputVersion']
        out['inputVersion'] += '|' + PROTOCOL
        out['apiCalls'] = self.transport.usage()['calls']
        out['providerUsage'] = self.transport.usage()
        out['repairPrerequisite']=getattr(self.session,'normal_gate',None)
        out['controllerMetrics'] = dict(decisions=len(self.calls), observeCalls=sum(
            c.get('modelOutput', {}).get('tool') == 'observe' for c in self.calls),
            recallCalls=sum(c.get('modelOutput', {}).get('tool') == 'recall' for c in self.calls),
            budget=self.cap)
        return out

    def run(self):
        self.spectator_frame()
        while not self.session.done and len(self.calls) < self.cap:
            number = len(self.calls) + 1
            provider, readable = None, None
            try:
                provider, readable, visible, image_refs = self.request()
                self.phase = 'thinking'; self.publish()
                reply = self.transport(provider)
            except Exception as exc:
                self.session.terminal = 'service_error' if provider is not None else 'harness_error'
                self.calls.append(dict(index=number, modelInput=readable,
                    error=dict(code=self.session.terminal, type=type(exc).__name__, message=str(exc)[:160])))
                break
            action = parse(reply)
            self.session._pending_observation=dict(decision=len(self.session.records)+1,packetSha256=digest(visible),imageHashes=[i['sha256'] for i in image_refs])
            output, images = self.execute(action, number)
            self.pending_images = images
            self.last_result = output
            call = dict(index=number, modelInput=readable, modelOutputRaw=reply,
                modelOutput=action, environmentOutput=output,
                providerReceipt=dict(id=self.transport.latest['result']['id'],
                    requestBodySha256=self.transport.latest['requestBodySha256'],
                    costUSD=self.transport.latest['result']['usage']['cost'],
                    inputTokens=self.transport.latest['result']['usage'].get('prompt_tokens'),
                    outputTokens=self.transport.latest['result']['usage'].get('completion_tokens')))
            if self.session.actor.startswith('scripted'):call['providerReceipt']=None
            self.calls.append(call)
            # Old camera images are intentionally not kept in the next API
            # messages. The model can request a fresh view at any time.
            history_result = {k: v for k, v in output.items() if k != 'images'}
            self.history.extend([dict(role='assistant', content=reply),
                                 dict(role='user', content=json.dumps(dict(toolResult=history_result), ensure_ascii=False))])
            self.spectator_frame(action, output)
            self.session.save()
        if not self.session.done and self.session.terminal is None:
            self.session.terminal = 'model_budget_exhausted'
        self.phase = 'finished'
        self.session.save()
        self.publish()
        write_json(self.session.directory / 'result.json', self.result())
        write_json(self.session.directory / 'log.json', dict(protocol=PROTOCOL, calls=self.calls,
            result=self.result(), note='Image JSON uses URLs and SHA256; exact API body is stored in api/*.request.json.gz.'))
        return self.result()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-decisions', type=int, default=30)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / 'run.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        runid = 'tool-gemini-' + time.strftime('%Y%m%d-%H%M%S')
        directory = OUT / 'runs' / runid
        session = create(directory, MODEL)
        transport = Transport(directory)
        result = ToolArena(session, transport, args.max_decisions).run()
        print(json.dumps(dict(runId=runid, terminal=result['terminalStatus'], success=result['success'],
            calls=result['apiCalls'], costUSD=result['providerUsage']['costUSD'],
            appliedEvents=result['appliedEvents']), ensure_ascii=False), flush=True)


if __name__ == '__main__': main()
