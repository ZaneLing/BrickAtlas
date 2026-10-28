"""No-API proof of pull observation, 90-degree camera and physical replay."""
import json
from pathlib import Path
import tempfile
import dynamic_arena.tool_arena as module
from dynamic_arena.demo import create


class ScriptedHarness:
    def __init__(self, session):
        self.session = session
        self.calls = 0
        self.latest = None
        self.observed_at_start = False
        self.observed_after_event = False

    def __call__(self, payload):
        self.calls += 1
        last = payload['messages'][-1]['content']
        if self.calls == 1:
            assert not any(b['type'] == 'image_url' for b in last)
            action = dict(tool='observe', args=dict(view='angled', rotateDegrees=0,
                                                    show=['current', 'target', 'inventory']))
            self.observed_at_start = True
        elif self.session.events and not self.observed_after_event:
            # This scripted controller may inspect private state. A real model
            # gets only the images it requested. This is an engine check only.
            self.observed_after_event = True
            action = dict(tool='observe', args=dict(view='angled', rotateDegrees=90,
                                                    show=['current', 'target']))
        else:
            if self.calls == 2 or self.observed_after_event and self.calls == 6:
                assert any(b['type'] == 'image_url' for b in last)
            else:
                assert not any(b['type'] == 'image_url' for b in last)
            missing = [a for a in ('F001', 'P001', 'P002', 'P003', 'P004')
                       if not self.session.ep.state[a]]
            if missing:
                actor = missing[0]
                action = dict(tool='attach', args=dict(partId=self.session.ep.actor_alias[actor],
                    candidate=self.session.ep.pose_alias[actor+':goal']))
            else:
                action = dict(tool='finish', args={})
        self.latest = dict(result=dict(id='scripted-' + str(self.calls),
            usage=dict(cost=0., prompt_tokens=0, completion_tokens=0)),
            requestBodySha256='0' * 64)
        return json.dumps(action)

    def usage(self):
        return dict(calls=self.calls, costUSD=0., capUSD=1., settled=True,
                    promptTokens=0, completionTokens=0)


def main():
    with tempfile.TemporaryDirectory(prefix='brick-tool-arena-check-') as tmp:
        module.OUT = Path(tmp)
        session = create(Path(tmp) / 'runs/scripted-proof', 'scripted:tool-proof')
        transport = ScriptedHarness(session)
        runner = module.ToolArena(session, transport, max_decisions=16)
        first, readable, _, assets = runner.request()
        assert not assets and not any(x['type'] == 'image_url' for x in first['messages'][-1]['content'])
        result = runner.run()
        assert result['success'] and result['appliedEvents'] == 1 and runner.azimuth == 125
        assert runner.calls[0]['modelOutput']['tool'] == 'observe'
        assert runner.calls[0]['environmentOutput']['images'][0]['role'] == 'current'
        assert runner.calls[4]['modelOutput']['tool'] == 'observe'
        assert runner.calls[4]['environmentOutput']['camera']['azimuthDegrees'] == 125
        assert all('events' not in json.dumps(c['modelInput']) for c in runner.calls)
        assert all(c['modelOutput']['tool'] != 'attach' or 'stateChanged' in c['environmentOutput']
                   for c in runner.calls)
        for call in runner.calls:
            content = call['modelInput']['messages'][-1]['content']
            images = [x for x in content if x['type'] == 'image_url']
            assert len(images) == (3 if call['index'] == 2 else 2 if call['index'] == 6 else 0)
        assert len(runner.frames) == len(runner.calls) + 1
        assert all('scenes' in f for f in runner.frames)
        print('PASS pull observation, 90-degree camera, whole-episode recovery and JSON trace; scripted, no API')


if __name__ == '__main__': main()
