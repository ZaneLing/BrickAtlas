"""Run one continuous API episode and publish a separate spectator recording."""
import argparse
import base64
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import time
from PIL import Image
from bench_design.run_autonomous import AutonomousRun
from dynamic_arena import OUT, MODEL
from dynamic_arena.demo import create, TITLE, CASE_ID
from dynamic_arena.transport import Transport, write_json


class ArenaRun(AutonomousRun):
    def __init__(self, session, policy, usage, max_decisions=32):
        super().__init__(session, policy, max_decisions=max_decisions)
        self.usage = usage
        self.frames = []
        self.started = time.time()
        self.phase = 'ready'
        self.assets = OUT / 'assets'
        self.assets.mkdir(parents=True, exist_ok=True)

    def result(self):
        value = super().result()
        usage = self.usage()
        value['normalizedResult'].update(apiCalls=usage['calls'], providerUsage=usage)
        return value

    def asset(self, path):
        data = Path(path).read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        dest = self.assets / (sha + '.png')
        if not dest.exists():
            dest.write_bytes(data)
        return '/assets/' + dest.name

    def crop(self, path, rectangle):
        with Image.open(path) as im:
            crop = im.crop(rectangle)
        import io
        stream = io.BytesIO()
        crop.save(stream, format='PNG')
        data = stream.getvalue()
        sha = hashlib.sha256(data).hexdigest()
        dest = self.assets / (sha + '.png')
        if not dest.exists():
            dest.write_bytes(data)
        return '/assets/' + dest.name

    def capture(self, observation):
        scenes, inputs = {}, []
        for asset in observation['images']:
            inputs.append({**{k: v for k, v in asset.items() if k != 'file'}, 'url': self.asset(asset['file'])})
            if asset['role'] == 'current-target':
                scenes[asset['view']] = dict(
                    current=self.crop(asset['file'], (0, 36, 800, 636)),
                    target=self.crop(asset['file'], (800, 36, 1600, 636)))
        frame = dict(index=len(self.steps), environmentStep=len(self.session.records), scenes=scenes,
            inputs=inputs, action=self.steps[-1].get('action') if self.steps else None,
            feedback=self.steps[-1].get('feedback') if self.steps else None,
            events=[dict(index=e['index'], atDecision=e['atDecision'],
                affected=[self.session.ep.actor_alias[a] for a in e['native'].get('affected', [])],
                description='系统移走一块已安装的积木', verified=e['effectiveIncidentVerified'])
                for e in self.session.events],
            usage=deepcopy(self.usage()), recordedAt=time.time())
        if self.frames and self.frames[-1]['index'] == frame['index']:
            self.frames[-1] = frame
        else:
            self.frames.append(frame)
        return frame

    def publish(self):
        result = self.result() if self.session.done else None
        data = dict(schema='brick-atlas-spectator-arena/1', runId=self.session.directory.name,
            title=TITLE, caseId=CASE_ID, model=self.session.actor, phase=self.phase,
            startedAt=self.started, updatedAt=time.time(), frames=self.frames, usage=self.usage(),
            targetParts=5, maxDecisions=self.cap, result=result,
            fullModelControl=True, scriptedPrefix=0, autoRepair=0, resets=0,
            formalBenchmarkResult=False, inputMode='visual observations + anonymous action handles',
            description='模型从空白底板接管。每次只装或拆一块，也可以自主查看。中途变化不发通知。',
            spectatorNotice='此页面是观看者视角；干扰标记与最终评分不发送给模型。')
        write_json(self.session.directory / 'spectator.json', data)
        write_json(OUT / 'latest.json', dict(runId=self.session.directory.name))

    def request(self):
        payload, public = super().request()
        frame = self.capture(public)
        # Copy precisely the images handed to the API, including optional
        # history lookups. Spectator metadata is never added to payload.
        model_inputs = []
        label = '观察图'
        for block in payload['messages'][-1]['content']:
            if block['type'] == 'text':
                try:
                    metadata = json.loads(block['text'])
                    label = metadata.get('role', '观察图')
                    if metadata.get('view'):
                        label += ' · ' + metadata['view']
                except (ValueError, TypeError):
                    if block['text'].startswith('HISTORICAL'):
                        label = '历史状态'
            elif block['type'] == 'image_url':
                raw = base64.b64decode(block['image_url']['url'].split(',', 1)[1])
                sha = hashlib.sha256(raw).hexdigest()
                (self.assets / (sha + '.png')).write_bytes(raw)
                model_inputs.append(dict(url='/assets/' + sha + '.png', role=label, sha256=sha))
        frame['modelInputs'] = model_inputs
        self.phase = 'thinking'
        self.publish()
        return payload, public

    def save(self):
        super().save()
        self.capture(self.session.observe())
        self.phase = 'finished' if self.session.done else 'running'
        self.publish()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true', help='Render the empty arena without contacting an API')
    parser.add_argument('--max-decisions', type=int, default=32)
    args = parser.parse_args()
    # Only one process may consume this demo budget. Viewer requests never call an API.
    import fcntl
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / 'run.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        runid = ('preview-' if args.prepare else 'gemini-') + time.strftime('%Y%m%d-%H%M%S')
        directory = OUT / 'runs' / runid
        session = create(directory, 'preview:no-model' if args.prepare else MODEL)
        if args.prepare:
            driver = ArenaRun(session, lambda _: None, lambda: dict(calls=0, costUSD=0, capUSD=1, settled=True), args.max_decisions)
            driver.capture(session.observe())
            driver.publish()
            print(json.dumps(dict(run=runid, preview=True, apiCalls=0)))
            return
        transport = Transport(directory)
        driver = ArenaRun(session, transport, transport.usage, args.max_decisions)
        result = driver.run()
        usage = transport.usage()
        result['normalizedResult'].update(apiCalls=usage['calls'], providerUsage=usage)
        write_json(directory / 'result.json', result)
        print(json.dumps(dict(run=runid, result=result['normalizedResult'], usage=usage), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
