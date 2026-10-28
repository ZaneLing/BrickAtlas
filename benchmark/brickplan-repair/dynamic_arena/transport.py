"""One real API transport with a persistent $1 demo ceiling and no retries."""
import base64
import gzip
import hashlib
import io
import json
import math
import os
import subprocess
import time
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


def catalogue(model_id=MODEL, output=None):
    response = subprocess.run(['curl', '-fsS', '--max-time', '25',
        'https://openrouter.ai/api/v1/models'], capture_output=True, check=True)
    data = json.loads(response.stdout)
    model = next(x for x in data['data'] if x['id'] == model_id)
    assert 'image' in model['architecture']['input_modalities']
    assert float(model['pricing']['prompt']) <= 2 / 1e6
    assert float(model['pricing']['completion']) <= 10 / 1e6
    write_json(output or OUT / 'model-pricing.json', dict(id=model_id, pricing=model['pricing'],
        architecture=model['architecture'], checkedAt=time.time(), source='https://openrouter.ai/api/v1/models'))
    return model


class Transport:
    def __init__(self, directory, cap=1.0, model=MODEL, ledger_path=None):
        assert 0 < cap <= 10.0
        self.directory = Path(directory)
        self.model = model
        self.ledger_path = Path(ledger_path) if ledger_path else OUT / 'api-ledger.private.json'
        self.ledger = json.loads(self.ledger_path.read_text()) if self.ledger_path.exists() else dict(
            capUSD=cap, authorization='User requested multiple model/object normal-gate API tests, 2026-10-28', charges=[])
        self.ledger['capUSD'] = min(self.ledger['capUSD'], cap)
        self.latest = None
        self.secret = key()
        self.catalogue = catalogue(model, self.directory / 'model-pricing.json' if ledger_path else None)
        self.input_price = float(self.catalogue['pricing']['prompt'])
        self.output_price = float(self.catalogue['pricing']['completion'])

    def __call__(self, payload):
        if self.ledger_path == OUT / 'api-ledger.private.json' and any(c['status'] != 'settled' for c in self.ledger['charges']):
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
        reserved = (text_bytes + image_count * 16384) * self.input_price + 2048 * self.output_price + image_count * .005
        spent = sum(c['actualUSD'] if c['actualUSD'] is not None else c['reservedUSD']
                    for c in self.ledger['charges'])
        if spent + reserved > self.ledger['capUSD']:
            raise RuntimeError('Arena demo budget limit reached before request')
        entry = dict(id=uuid.uuid4().hex, model=self.model, reservedUSD=reserved,
            actualUSD=None, status='pending', createdAt=time.time(), run=self.directory.name)
        self.ledger['charges'].append(entry)
        write_json(self.ledger_path, self.ledger)
        reasoning = dict(effort='low') if self.model.startswith(('openai/', 'anthropic/')) else dict(enabled=False)
        body = dict(model=self.model, messages=payload['messages'], temperature=0, max_tokens=2048,
            reasoning=reasoning, response_format=dict(type='json_object'),
            provider=dict(sort='price', allow_fallbacks=False, require_parameters=False,
                data_collection='deny', max_price=dict(prompt=self.input_price * 1e6,
                    completion=self.output_price * 1e6, image=.005)))
        raw_body = json.dumps(body, ensure_ascii=False).encode()
        # Keep the exact request body (including image bytes) for an audit.
        # No Authorization header or API key is written to this file.
        request_archive = self.directory / 'api' / (entry['id'] + '.request.json.gz')
        request_archive.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(request_archive, 'wb') as archive:
            archive.write(raw_body)
        pending = self.directory / 'api' / (entry['id'] + '.request.pending')
        pending.write_bytes(raw_body)
        start = time.time()
        try:
            # curl handles repeated TLS connections more reliably here. The
            # credential is sent on stdin, never in process arguments or logs.
            config = ('url = "https://openrouter.ai/api/v1/chat/completions"\n'
                'request = "POST"\n'
                'header = "Authorization: Bearer ' + self.secret + '"\n'
                'header = "Content-Type: application/json"\n'
                'header = "X-OpenRouter-Title: Brick Atlas continuous assembly arena"\n')
            response = subprocess.run(['curl', '-sS', '--max-time', '110',
                '--data-binary', '@' + str(pending), '--write-out', '\n%{http_code}',
                '--config', '-'], input=config, text=True, capture_output=True)
            if response.returncode:
                raise RuntimeError('HTTP transport error: ' + response.stderr[:160])
            body_text, status = response.stdout.rsplit('\n', 1)
            if status != '200':
                raise RuntimeError('Provider HTTP ' + status + ': ' + body_text[:240])
            result = json.loads(body_text)
            cost = result.get('usage', {}).get('cost')
            if not isinstance(cost, (float, int)) or not math.isfinite(cost) or cost < 0 or not result.get('id'):
                raise RuntimeError('API response missing a verifiable charge')
            entry.update(actualUSD=cost, generationId=result['id'],
                status='settled' if cost <= reserved else 'uncertain',
                promptTokens=result['usage'].get('prompt_tokens'), completionTokens=result['usage'].get('completion_tokens'))
            write_json(self.ledger_path, self.ledger)
            self.latest = dict(result=result, requestBodySha256=hashlib.sha256(raw_body).hexdigest(),
                requestShape=dict(model=self.model, messages=len(body['messages']), images=image_count,
                    maxTokens=2048, reasoning=reasoning), latencySeconds=round(time.time() - start, 3))
            write_json(self.directory / 'api' / (entry['id'] + '.private.json'), self.latest)
            if entry['status'] != 'settled':
                raise RuntimeError('Provider exceeded reserved ceiling')
            return result['choices'][0]['message']['content']
        except Exception:
            if entry['status'] == 'pending':
                entry['status'] = 'uncertain'
                write_json(self.ledger_path, self.ledger)
            raise
        finally:
            pending.unlink(missing_ok=True)

    def usage(self):
        charges = [c for c in self.ledger['charges'] if c['run'] == self.directory.name]
        return dict(calls=len(charges), costUSD=sum(c['actualUSD'] or 0 for c in charges),
            unsettledReservationsUSD=sum(c['reservedUSD'] for c in charges if c['status'] != 'settled'),
            settled=all(c['status'] == 'settled' for c in charges), capUSD=self.ledger['capUSD'],
            promptTokens=sum(c.get('promptTokens') or 0 for c in charges),
            completionTokens=sum(c.get('completionTokens') or 0 for c in charges))
