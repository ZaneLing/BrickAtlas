"""Direct DeepSeek / Aliyun routes and OpenRouter, with one auditable ledger.

No retry, no provider fallback. Native usage-based estimates are explicitly
separate from OpenRouter's returned monetary charge. CNY is budgeted at the
conservative 1 CNY = 0.20 USD; it is also reported in its native currency.
"""
import base64,gzip,hashlib,io,json,math,os,subprocess,time,uuid
from pathlib import Path
from PIL import Image
from dynamic_arena import ROOT
from dynamic_arena.transport import write_json
from unified_agent import OUT

LEDGER=OUT/'ledger.private.json'
MODELS=('deepseek/deepseek-flash','qwen/qwen3.8-flash',
        'google/gemini-2.5-flash','openai/gpt-6.1-sol')


class CostLimit(RuntimeError):pass


def env(name, fallback=None):
    value=os.environ.get(name)
    if value is None and (ROOT/'.env').exists():
        for line in (ROOT/'.env').read_text().splitlines():
            if line.startswith(name+'='):value=line.split('=',1)[1].strip().strip('\"\'');break
    return value or fallback


def route(model):
    bare=model.split('/',1)[-1]
    if model.startswith('deepseek/') or bare.startswith('deepseek-'):
        return dict(provider='deepseek',model=bare,baseURL='https://api.deepseek.com',keyEnv='DEEPSEEK_API_KEY')
    if model.startswith('qwen/') or bare.startswith(('qwen','qvq')):
        return dict(provider='aliyun',model=bare,baseURL='https://dashscope.aliyuncs.com/compatible-mode/v1',keyEnv='ALIYUN_API_KEY')
    return dict(provider='openrouter',model=model,baseURL='https://openrouter.ai/api/v1',keyEnv='OPENROUTER_API_KEY')


def http(url,secret=None,body=None,timeout=110):
    # Credential travels via stdin, never argv or files.
    config='url = '+json.dumps(url)+'\n'
    if secret:config+='header = "Authorization: Bearer '+secret+'"\n'
    args=['curl','-sS','--max-time',str(timeout),'--write-out','\n%{http_code}','--config','-']
    if body is not None:
        config+='header = "Content-Type: application/json"\n'
        args+=['--data-binary','@'+str(body)]
    res=subprocess.run(args,input=config,text=True,capture_output=True)
    if res.returncode:raise RuntimeError('HTTP transport failed (curl '+str(res.returncode)+')')
    text,status=res.stdout.rsplit('\n',1)
    if status!='200':raise RuntimeError('Provider HTTP '+status+': '+text[:300])
    return json.loads(text)


def total(ledger):
    return sum(c['accountedUSD'] if c.get('accountedUSD') is not None else
        c['actualUSD'] if c.get('actualUSD') is not None else c['reservedUSD'] for c in ledger['charges'])


class PaidTransport:
    def __init__(self,directory,cap=1.5,model=MODELS[0],ledger_path=None,max_output=2048):
        if not 0<cap<=10:raise ValueError('Invalid dollar cap')
        self.directory=Path(directory);self.directory.mkdir(parents=True,exist_ok=True)
        self.model=model;self.route=route(model);self.latest=None;self.max_output=max_output
        self.ledger_path=Path(ledger_path or LEDGER)
        self.secret=env(self.route['keyEnv'])
        if not self.secret and self.route['provider']=='aliyun':self.secret=env('DASHSCOPE_API_KEY')
        if not self.secret:raise RuntimeError(self.route['keyEnv']+' is not configured')
        self.ledger=json.loads(self.ledger_path.read_text()) if self.ledger_path.exists() else dict(
            schema='brick-atlas-provider-ledger/1',capUSD=cap,
            authorization='User requested autonomous multi-backbone Arena pilot, 2026-10-30',charges=[])
        self.ledger['capUSD']=min(cap,self.ledger['capUSD'])
        provider=self.route['provider'];self.parameters=[];self.budget_factor=.2 if provider=='aliyun' else 1.
        if provider=='openrouter':
            catalog=http(self.route['baseURL']+'/models',timeout=25)
            self.catalogue=next(x for x in catalog['data'] if x['id']==model)
            if 'image' not in self.catalogue['architecture']['input_modalities']:raise ValueError('Backbone does not support images')
            self.parameters=self.catalogue.get('supported_parameters',[])
            self.input_price=float(self.catalogue['pricing']['prompt']);self.output_price=float(self.catalogue['pricing']['completion'])
            if self.input_price>2e-6 or self.output_price>10e-6:raise ValueError('Outside pilot price range')
            self.reasoning={'effort':'low'} if 'reasoning' in self.parameters else None
            self.price=dict(inputPerMillion=self.input_price*1e6,outputPerMillion=self.output_price*1e6,currency='USD',basis='provider usage.cost')
        elif provider=='deepseek':
            catalog=http(self.route['baseURL']+'/models',self.secret,timeout=25)
            self.catalogue=next(x for x in catalog['data'] if x['id']==self.route['model'])
            if 'image' not in self.catalogue.get('input_modalities',[]):raise ValueError('DeepSeek model does not accept images')
            if self.route['model']!='deepseek-flash':raise ValueError('Verify direct model pricing before adding it')
            self.input_price=.3e-6;self.output_price=1.2e-6;self.reasoning={'effort':'low'}
            self.price=dict(inputPerMillion=.3,outputPerMillion=1.2,cachedInputPerMillion=.006,currency='USD',basis='usage at peak list price; upper estimate, not invoice',source='https://api-docs.deepseek.com/quick_start/pricing/')
        else:
            from urllib.parse import quote
            catalog=http('https://dashscope.aliyuncs.com/api/v1/models?model='+quote(self.route['model']),self.secret,timeout=25)
            self.catalogue=next((x for x in catalog.get('output',{}).get('models',[]) if x['model']==self.route['model']),None)
            if not self.catalogue:raise ValueError('Model unavailable in Aliyun catalogue: '+self.route['model'])
            if 'Image' not in self.catalogue.get('inference_metadata',{}).get('request_modality',[]):raise ValueError('Aliyun model does not accept images')
            prices=[p for tier in self.catalogue['prices'] for p in tier['prices']]
            self.input_price=max(float(p['price']) for p in prices if p['type']=='input_token')/1e6
            self.output_price=max(float(p['price']) for p in prices if p['type']=='output_token')/1e6
            if self.input_price>2e-6 or self.output_price>8e-6:raise ValueError('Outside native Aliyun pilot price range')
            self.reasoning={'effort':'low'} if self.route['model'].startswith('qwen3.8') else None
            self.price=dict(inputPerMillion=self.input_price*1e6,outputPerMillion=self.output_price*1e6,currency='CNY',basis='usage at Beijing catalogue list price; upper estimate, not invoice',
                usdBudgetAccounting='1 CNY counted as 0.20 USD; conservative budget rate, not invoice FX',
                fxReference='ECB 2026-10-27 EUR/USD 1.1150 and EUR/CNY 7.4343 imply about 0.15 USD/CNY; budget uses 0.20',
                fxSource='https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html',
                source='https://dashscope.aliyuncs.com/api/v1/models?model='+quote(self.route['model']))
        write_json(self.directory/'provider.json',dict(**self.route,price=self.price,catalogue=self.catalogue,checkedAt=time.time(),maxOutputTokens=max_output,reasoning=self.reasoning))

    def __call__(self,payload):
        # Reload because multiple backbones share this ledger (runner holds flock).
        if self.ledger_path.exists():self.ledger=json.loads(self.ledger_path.read_text())
        if any(c['status'] in ('uncertain','pending') and c.get('provider','openrouter')==self.route['provider'] for c in self.ledger['charges']):
            raise RuntimeError('Unsettled provider request; reconcile before another call to this provider')
        chars,images=2048,0
        for message in payload['messages']:
            content=message['content']
            if isinstance(content,str):chars+=len(content.encode());continue
            for block in content:
                if block['type']=='text':chars+=len(block['text'].encode())
                else:
                    raw=base64.b64decode(block['image_url']['url'].split(',',1)[1])
                    with Image.open(io.BytesIO(raw)) as im:
                        if max(im.size)>1800:raise ValueError('Oversize input image')
                    images+=1
        if images>20 or chars>250000:raise ValueError('Oversize API input')
        reserve=((chars+images*16384)*self.input_price+(self.max_output+10)*self.output_price)*self.budget_factor
        if self.route['provider']=='openrouter':reserve+=images*.005
        if total(self.ledger)+reserve>self.ledger['capUSD']:raise CostLimit('Global pilot money ceiling reached before request')
        body=dict(model=self.route['model'],messages=payload['messages'],max_tokens=self.max_output,
                  response_format={'type':'json_object'},stream=False)
        if self.route['provider']=='openrouter':
            body['provider']=dict(sort='price',allow_fallbacks=False,require_parameters=True,data_collection='deny',
                max_price=dict(prompt=self.input_price*1e6,completion=self.output_price*1e6,image=.005))
            if self.reasoning:body['reasoning']=self.reasoning
            if 'temperature' in self.parameters:body['temperature']=0
        elif self.route['provider']=='deepseek':body.update(thinking={'type':'enabled'},reasoning_effort='low')
        else:
            body['temperature']=0
            if self.reasoning:
                # Aliyun max_tokens excludes reasoning. max_completion_tokens
                # bounds reasoning + answer (documented tolerance up to 10).
                body.pop('max_tokens')
                body.update(max_completion_tokens=self.max_output,enable_thinking=True,reasoning_effort='low',preserve_thinking=False)
        raw=json.dumps(body,ensure_ascii=False).encode();uid=uuid.uuid4().hex
        folder=self.directory/'api';folder.mkdir(exist_ok=True)
        with gzip.open(folder/(uid+'.request.json.gz'),'wb') as f:f.write(raw)
        pending=folder/(uid+'.pending');pending.write_bytes(raw)
        entry=dict(id=uid,run=self.directory.name,model=self.model,provider=self.route['provider'],status='pending',reservedUSD=reserve,createdAt=time.time())
        self.ledger['charges'].append(entry);write_json(self.ledger_path,self.ledger)
        started=time.time()
        try:
            result=http(self.route['baseURL']+'/chat/completions',self.secret,pending)
            with gzip.open(folder/(uid+'.response.private.json.gz'),'wt') as f:json.dump(result,f,ensure_ascii=False)
            usage=result.get('usage',{});prompt=usage.get('prompt_tokens');completion=usage.get('completion_tokens')
            if not result.get('id') or type(prompt) is not int or type(completion) is not int:raise RuntimeError('Missing provider usage receipt')
            native=prompt*self.input_price+completion*self.output_price
            if self.route['provider']=='deepseek':
                hits=usage.get('prompt_cache_hit_tokens',usage.get('prompt_tokens_details',{}).get('cached_tokens',0))
                native=(prompt-hits)*self.input_price+hits*.006e-6+completion*self.output_price
            cost=usage.get('cost') if self.route['provider']=='openrouter' else native*self.budget_factor
            if not isinstance(cost,(int,float)) or not math.isfinite(cost) or cost<0:raise RuntimeError('Missing verifiable charge')
            entry.update(accountedUSD=cost,costBasis=self.price['basis'],nativeCurrency=self.price['currency'],nativeCost=cost if self.route['provider']=='openrouter' else native,
                promptTokens=prompt,completionTokens=completion,reasoningTokens=usage.get('completion_tokens_details',{}).get('reasoning_tokens'),
                generationId=result['id'],status='settled' if self.route['provider']=='openrouter' else 'usage_estimated')
            if cost>reserve:entry['status']='uncertain'
            write_json(self.ledger_path,self.ledger)
            self.latest=dict(result=result,requestBodySha256=hashlib.sha256(raw).hexdigest(),
                requestShape=dict(model=body['model'],provider=self.route['provider'],images=images,maxTokens=self.max_output,reasoning=self.reasoning),
                costUSD=cost,costBasis=self.price['basis'],nativeCurrency=self.price['currency'],latencySeconds=round(time.time()-started,3),archiveId=uid)
            write_json(folder/(uid+'.private.json'),self.latest)
            if cost>reserve:raise RuntimeError('Provider exceeded reserved ceiling')
            choice=result['choices'][0]
            if choice.get('finish_reason') in ('content_filter','insufficient_system_resource','aborted'):raise RuntimeError('Provider stopped: '+choice['finish_reason'])
            return choice['message'].get('content') or ''
        except Exception as exc:
            if entry['status']=='pending':entry['status']='uncertain'
            entry['error']=str(exc)[:300];write_json(self.ledger_path,self.ledger);raise
        finally:pending.unlink(missing_ok=True)

    def usage(self):
        charges=[c for c in self.ledger['charges'] if c['run']==self.directory.name]
        return dict(calls=len(charges),costUSD=sum(c.get('accountedUSD',0) for c in charges),
            costLabel='USD charge / conservative native-provider estimate; see nativeCosts',
            confirmedUSD=sum(c.get('accountedUSD',0) for c in charges if c['status']=='settled'),
            nativeCosts={currency:sum(c.get('nativeCost',0) for c in charges if c.get('nativeCurrency')==currency) for currency in ['USD','CNY']},
            unsettledReservationsUSD=sum(c['reservedUSD'] for c in charges if c['status'] in ('pending','uncertain')),
            settled=all(c['status'] in ('settled','usage_estimated') for c in charges),capUSD=self.ledger['capUSD'],
            promptTokens=sum(c.get('promptTokens',0) for c in charges),completionTokens=sum(c.get('completionTokens',0) for c in charges),
            reasoningTokens=sum(c.get('reasoningTokens') or 0 for c in charges),provider=self.route['provider'])
