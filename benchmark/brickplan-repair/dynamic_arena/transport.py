"""One real API transport with a persistent $1 demo ceiling and no retries."""
import base64
import hashlib
import io
import json
import math
import os
import time
import urllib.request
import uuid
from pathlib import Path
from PIL import Image
from dynamic_arena import ROOT, OUT, MODEL


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.pending')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def key():
    value = os.environ.get('OPENROUTER_API_KEY')
    if not value:
        for line in (ROOT / '.env').read_text().splitlines():
            if line.startswith('OPENROUTER_API_KEY='):
                value = line.split('=', 1)[1].strip().strip('"\'')
    if not value:
        raise RuntimeError('OPENROUTER_API_KEY is not configured')
    return value


def catalogue():
    with urllib.request.urlopen('https://openrouter.ai/api/v1/models', timeout=25) as response:
        data = json.load(response)
    model = next(x for x in data['data'] if x['id'] == MODEL)
    assert 'image' in model['architecture']['input_modalities']
    assert float(model['pricing']['prompt']) <= .4 / 1e6
    assert float(model['pricing']['completion']) <= 3 / 1e6
    write_json(OUT / 'model-pricing.json', dict(id=MODEL, pricing=model['pricing'],
        architecture=model['architecture'], checkedAt=time.time(), source='https://openrouter.ai/api/v1/models'))
    return model


class Transport:
    def __init__(self, directory, cap=1.0):
        assert 0 < cap <= 1.0
        self.directory = Path(directory)
        self.ledger_path = OUT / 'api-ledger.private.json'
        self.ledger = json.loads(self.ledger_path.read_text()) if self.ledger_path.exists() else dict(
            capUSD=cap, authorization='User requested one API-model arena example, 2026-10-28', charges=[])
        self.ledger['capUSD'] = min(self.ledger['capUSD'], cap)
        self.latest = None
        self.secret = key()
        catalogue()

    def __call__(self, payload):
        if any(c['status'] != 'settled' for c in self.ledger['charges']):
            raise RuntimeError('Unsettled API charge; reconcile before any further call')
        # Bound text by UTF-8 bytes and images by 16K tokens each. The provider
        # price cap matches this bound; oversize images/requests are rejected.
        text_bytes, image_count = 2048, 0
        for message in payload['messages']:
            content = message['content']
            if isinstance(content, str):
                text_bytes += len(content.encode())
            else:
                for item in content:
                    if item['type'] == 'text':
                        text_bytes += len(item['text'].encode())
                    else:
                        raw = base64.b64decode(item['image_url']['url'].split(',', 1)[1])
                        with Image.open(io.BytesIO(raw)) as im:
                            assert max(im.size) <= 1800
                        image_count += 1
        assert image_count <= 20 and text_bytes <= 250_000
        reserved = (text_bytes + image_count * 16384) * .4 / 1e6 + 2048 * 3 / 1e6 + image_count * .005
        spent = sum(c['actualUSD'] for c in self.ledger['charges'])
        if spent + reserved > self.ledger['capUSD']:
            raise RuntimeError('Arena demo budget limit reached before request')
        entry = dict(id=uuid.uuid4().hex, model=MODEL, reservedUSD=reserved,
            actualUSD=None, status='pending', createdAt=time.time(), run=self.directory.name)
        self.ledger['charges'].append(entry)
        write_json(self.ledger_path, self.ledger)
        body = dict(model=MODEL, messages=payload['messages'], temperature=0, max_tokens=2048,
            reasoning=dict(enabled=False), response_format=dict(type='json_object'),
            provider=dict(sort='price', allow_fallbacks=False, require_parameters=True,
                data_collection='deny', max_price=dict(prompt=.4, completion=3, image=.005)))
        raw_body = json.dumps(body, ensure_ascii=False).encode()
        request = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=raw_body,
            headers={'Authorization': 'Bearer ' + self.secret, 'Content-Type': 'application/json',
                'X-OpenRouter-Title': 'Brick Atlas continuous assembly arena'})
        start = time.time()
        try:
            with urllib.request.urlopen(request, timeout=110) as response:
                result = json.load(response)
            cost = result.get('usage', {}).get('cost')
            if not isinstance(cost, (float, int)) or not math.isfinite(cost) or cost < 0 or not result.get('id'):
                raise RuntimeError('API response missing a verifiable charge')
            entry.update(actualUSD=cost, generationId=result['id'],
                status='settled' if cost <= reserved else 'uncertain',
                promptTokens=result['usage'].get('prompt_tokens'), completionTokens=result['usage'].get('completion_tokens'))
            write_json(self.ledger_path, self.ledger)
            self.latest = dict(result=result, requestBodySha256=hashlib.sha256(raw_body).hexdigest(),
                requestShape=dict(model=MODEL, messages=len(body['messages']), images=image_count,
                    maxTokens=2048, reasoningEnabled=False), latencySeconds=round(time.time() - start, 3))
            write_json(self.directory / 'api' / (entry['id'] + '.private.json'), self.latest)
            if entry['status'] != 'settled':
                raise RuntimeError('Provider exceeded reserved ceiling')
            return result['choices'][0]['message']['content']
        except Exception:
            if entry['status'] == 'pending':
                entry['status'] = 'uncertain'
                write_json(self.ledger_path, self.ledger)
            raise

    def usage(self):
        charges = [c for c in self.ledger['charges'] if c['run'] == self.directory.name]
        return dict(calls=len(charges), costUSD=sum(c['actualUSD'] or 0 for c in charges),
            settled=all(c['status'] == 'settled' for c in charges), capUSD=self.ledger['capUSD'],
            promptTokens=sum(c.get('promptTokens') or 0 for c in charges),
            completionTokens=sum(c.get('completionTokens') or 0 for c in charges))
