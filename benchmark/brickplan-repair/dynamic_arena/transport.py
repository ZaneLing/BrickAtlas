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
    """All current controllers share the audited provider adapter.

    Old API logs remain immutable; this prevents direct/static runners from
    accidentally bypassing native routing, truncation or receipt checks.
    """
    def __init__(self,directory,cap=1.0,model=MODEL,ledger_path=None):
        from unified_agent.providers import PaidTransport
        self._native=PaidTransport(directory,cap,model,
            ledger_path=ledger_path or OUT/'api-ledger.private.json')
        self.directory,self.model,self.latest=Path(directory),model,None

    def __call__(self,payload):
        try:return self._native(payload)
        finally:self.latest=self._native.latest

    def usage(self):return self._native.usage()
