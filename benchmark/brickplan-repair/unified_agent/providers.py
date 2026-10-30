"""Direct DeepSeek / Aliyun routes and OpenRouter, with one auditable ledger.

No retry, no provider fallback. Native usage-based estimates are explicitly
separate from OpenRouter's returned monetary charge. CNY is budgeted at the
conservative 1 CNY = 0.20 USD; it is also reported in its native currency.
"""
import base64,gzip,hashlib,io,json,math,os,subprocess,time,uuid,fcntl
from pathlib import Path
from PIL import Image
from dynamic_arena import ROOT
from dynamic_arena.transport import write_json
from unified_agent import RUN_OUT as OUT
from unified_agent.failures import ProviderError,GenerationError,InputContractError

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
    if model.startswith('ark/'):
        return dict(provider='ark',model=bare,baseURL='https://ark.cn-beijing.volces.com/api/v3',keyEnv='ARK_API_KEY')
    if model.startswith('deepseek/') or bare.startswith('deepseek-'):
        return dict(provider='deepseek',model=bare,baseURL='https://api.deepseek.com',keyEnv='DEEPSEEK_API_KEY')
    if model.startswith('qwen/') or bare.startswith(('qwen','qvq')):
        return dict(provider='aliyun',model=bare,baseURL='https://dashscope.aliyuncs.com/compatible-mode/v1',keyEnv='ALIYUN_API_KEY')
    return dict(provider='openrouter',model=model,baseURL='https://openrouter.ai/api/v1',keyEnv='OPENROUTER_API_KEY')


def inference_model(model):
    """Account-specific endpoint mapping, explicitly supplied by the user."""
    names={'ark/gpt-6-1-sol-260929':'ARK_SOL_ENDPOINT',
        'ark/doubao-seed-2-1-pro-260915':'ARK_SEED_PRO_ENDPOINT',
        'ark/deepseek-v4-1-flash-261017':'ARK_DEEPSEEK_ENDPOINT'}
    value=env(names[model]) if model in names else None
    if value:
        if not value.startswith('ep-') or not all(c.isalnum() or c=='-' for c in value):raise ValueError('Invalid Ark endpoint ID')
        return value
    return route(model)['model']


def http(url,secret=None,body=None,timeout=180):
    # Credential travels via stdin, never argv or files.
    config='url = '+json.dumps(url)+'\n'
    if secret:config+='header = '+json.dumps('Authorization: Bearer '+secret)+'\n'
    args=['curl','-sS','--connect-timeout','20','--max-time',str(timeout),'--write-out','\n%{http_code}','--config','-']
    if body is not None:
        config+='header = "Content-Type: application/json"\n'
        args+=['--data-binary','@'+str(body)]
    res=subprocess.run(args,input=config,text=True,capture_output=True)
    if res.returncode:raise ProviderError('API_TIMEOUT' if res.returncode==28 else 'API_TRANSPORT_ERROR','HTTP transport failed (curl '+str(res.returncode)+')')
    text,status=res.stdout.rsplit('\n',1)
    try:value=json.loads(text)
    except ValueError:raise ProviderError('API_NON_JSON','Provider returned a non-JSON body',status=int(status),response={'body':text[:20000]})
    if status!='200':
        code={400:'API_BAD_REQUEST',401:'API_AUTH',403:'API_FORBIDDEN',404:'API_MODEL_NOT_FOUND',429:'API_RATE_LIMIT'}.get(int(status),'API_SERVER_ERROR')
        raise ProviderError(code,'Provider HTTP '+status+': '+text[:300],status=int(status),response=value)
    return value


def total(ledger):
    return sum(c['accountedUSD'] if c.get('accountedUSD') is not None else
        c['actualUSD'] if c.get('actualUSD') is not None else c['reservedUSD'] for c in ledger['charges'])


class PaidTransport:
    def __init__(self,directory,cap=1.5,model=MODELS[0],ledger_path=None,max_output=8192,reasoning_mode='off-when-supported',timeout=180):
        if not 0<cap<=10:raise ValueError('Invalid dollar cap')
        self.directory=Path(directory);self.directory.mkdir(parents=True,exist_ok=True)
        self.model=model;self.route=route(model);self.inference_model=inference_model(model);self.latest=None;self.max_output=max_output;self.cap=cap
        if reasoning_mode not in ('off-when-supported','low'):raise ValueError('Unknown reasoning policy')
        self.reasoning_mode=reasoning_mode;self.timeout=timeout
        self.ledger_path=Path(ledger_path or LEDGER)
        self.secret=env(self.route['keyEnv'])
        if not self.secret and self.route['provider']=='aliyun':self.secret=env('DASHSCOPE_API_KEY')
        if not self.secret:raise RuntimeError(self.route['keyEnv']+' is not configured')
        self.ledger=json.loads(self.ledger_path.read_text()) if self.ledger_path.exists() else dict(
            schema='brick-atlas-provider-ledger/1',capUSD=cap,
            authorization='User requested autonomous multi-backbone Arena pilot, 2026-10-30',charges=[])
        self.ledger['capUSD']=min(cap,self.ledger['capUSD'])
        provider=self.route['provider'];self.parameters=[];self.budget_factor=.2 if provider in ('aliyun','ark') else 1.
        if provider=='openrouter':
            catalog=http(self.route['baseURL']+'/models',timeout=25)
            self.catalogue=next((x for x in catalog['data'] if x['id']==model),None)
            if not self.catalogue:raise ProviderError('API_MODEL_NOT_FOUND','Model absent from OpenRouter catalogue: '+model)
            if 'image' not in self.catalogue['architecture']['input_modalities']:raise ValueError('Backbone does not support images')
            self.parameters=self.catalogue.get('supported_parameters',[])
            self.input_price=float(self.catalogue['pricing']['prompt']);self.output_price=float(self.catalogue['pricing']['completion'])
            if self.input_price>2e-6 or self.output_price>10e-6:raise ValueError('Outside pilot price range')
            self.reasoning=({'effort':'low'} if model=='openai/gpt-6.1-sol' or reasoning_mode=='low' else {'enabled':False}) if 'reasoning' in self.parameters else None
            self.price=dict(inputPerMillion=self.input_price*1e6,outputPerMillion=self.output_price*1e6,currency='USD',basis='provider usage.cost')
        elif provider=='ark':
            catalog=http(self.route['baseURL']+'/models',self.secret,timeout=25)
            self.catalogue=next((x for x in catalog['data'] if x['id']==self.route['model']),None)
            if not self.catalogue:raise ProviderError('API_MODEL_NOT_FOUND','Model absent from Ark catalogue: '+self.route['model'])
            prices={'doubao-seed-2-1-pro-260915':(6.,30.),'deepseek-v4-1-flash-261017':(2.,8.),'gpt-6-1-sol-260929':(15.,75.)}
            if self.route['model'] not in prices:raise ValueError('Ark account price not verified for '+self.route['model'])
            pin,pout=prices[self.route['model']]
            self.input_price=pin/1e6;self.output_price=pout/1e6
            self.reasoning={'effort':'low'} if reasoning_mode=='low' else {'enabled':False}
            self.price=dict(inputPerMillion=pin,outputPerMillion=pout,currency='CNY',
                basis='Ark regular-online peak list price, no cache discount; upper usage estimate, not invoice',
                source='https://docs.volcengine.com/docs/ark/model-pricing?lang=zh&redirect=1',
                budgetAccounting='CNY x 0.20 accounting units; global 8 units = CNY 40, not FX')
            if self.route['model'].startswith('gpt-6-1-sol'):
                self.reasoning={'effort':'low'}
                self.price.update(basis='PROVISIONAL only: OpenAI native USD 2/10 per million x assumed 7.5 CNY/USD; Ark price unknown, user authorized running anyway',
                    source='https://developers.openai.com/api/docs/models/gpt-6.1-sol',arkPriceVerified=False,
                    authorization='2026-10-30: ark别管价格，用就行了')
        elif provider=='deepseek':
            catalog=http(self.route['baseURL']+'/models',self.secret,timeout=25)
            self.catalogue=next((x for x in catalog['data'] if x['id']==self.route['model']),None)
            if not self.catalogue:raise ProviderError('API_MODEL_NOT_FOUND','Model absent from DeepSeek catalogue: '+self.route['model'])
            if 'image' not in self.catalogue.get('input_modalities',[]):raise ValueError('DeepSeek model does not accept images')
            if self.route['model']!='deepseek-flash':raise ValueError('Verify direct model pricing before adding it')
            self.input_price=.3e-6;self.output_price=1.2e-6;self.reasoning={'effort':'low'} if reasoning_mode=='low' else {'enabled':False}
            self.price=dict(inputPerMillion=.3,outputPerMillion=1.2,cachedInputPerMillion=.006,currency='USD',basis='usage at peak list price; upper estimate, not invoice',source='https://api-docs.deepseek.com/quick_start/pricing/')
        else:
            from urllib.parse import quote
            catalog=http('https://dashscope.aliyuncs.com/api/v1/models?model='+quote(self.route['model']),self.secret,timeout=25)
            self.catalogue=next((x for x in catalog.get('output',{}).get('models',[]) if x['model']==self.route['model']),None)
            if not self.catalogue:raise ProviderError('API_MODEL_NOT_FOUND','Model unavailable in Aliyun catalogue: '+self.route['model'])
            if 'Image' not in self.catalogue.get('inference_metadata',{}).get('request_modality',[]):raise ValueError('Aliyun model does not accept images')
            prices=[p for tier in self.catalogue['prices'] for p in tier['prices']]
            self.input_price=max(float(p['price']) for p in prices if p['type']=='input_token')/1e6
            self.output_price=max(float(p['price']) for p in prices if p['type']=='output_token')/1e6
            if self.input_price>2e-6 or self.output_price>8e-6:raise ValueError('Outside native Aliyun pilot price range')
            self.reasoning=({'effort':'low'} if reasoning_mode=='low' else {'enabled':False}) if self.route['model'].startswith('qwen3.8') else None
            self.price=dict(inputPerMillion=self.input_price*1e6,outputPerMillion=self.output_price*1e6,currency='CNY',basis='usage at Beijing catalogue list price; upper estimate, not invoice',
                usdBudgetAccounting='1 CNY counted as 0.20 USD; conservative budget rate, not invoice FX',
                fxReference='ECB 2026-10-27 EUR/USD 1.1150 and EUR/CNY 7.4343 imply about 0.15 USD/CNY; budget uses 0.20',
                fxSource='https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html',
                source='https://dashscope.aliyuncs.com/api/v1/models?model='+quote(self.route['model']))
        write_json(self.directory/'provider.json',dict(**self.route,inferenceModel=self.inference_model,price=self.price,catalogue=self.catalogue,checkedAt=time.time(),maxOutputTokens=max_output,reasoning=self.reasoning,reasoningMode=reasoning_mode,requestTimeoutSeconds=timeout))

    def __call__(self,payload):
        self.ledger_path.parent.mkdir(parents=True,exist_ok=True)
        with self.ledger_path.with_suffix('.lock').open('w') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            return self._call(payload)

    def _call(self,payload):
        self.latest=None;self.latest_attempt=None
        # Reload because multiple backbones share this ledger (runner holds flock).
        if self.ledger_path.exists():self.ledger=json.loads(self.ledger_path.read_text())
        self.ledger['capUSD']=min(self.cap,self.ledger['capUSD'])
        if any(c['status'] in ('uncertain','pending') and c.get('provider','openrouter')==self.route['provider'] for c in self.ledger['charges']):
            raise RuntimeError('Unsettled provider request; reconcile before another call to this provider')
        chars,images=2048,0
        if not isinstance(payload,dict) or not isinstance(payload.get('messages'),list):raise InputContractError('messages must be a list')
        for message in payload['messages']:
            if not isinstance(message,dict) or message.get('role') not in ('system','user','assistant'):raise InputContractError('Invalid message role')
            content=message['content']
            if isinstance(content,str):chars+=len(content.encode());continue
            if not isinstance(content,list):raise InputContractError('Message content must be text or content blocks')
            for block in content:
                if block['type']=='text':chars+=len(block['text'].encode())
                else:
                    try:
                        url=block['image_url']['url']
                        if block['type']!='image_url' or not url.startswith('data:image/png;base64,'):raise ValueError('Expected embedded PNG')
                        raw=base64.b64decode(url.split(',',1)[1],validate=True)
                        with Image.open(io.BytesIO(raw)) as im:
                            if max(im.size)>1800:raise ValueError('Oversize input image')
                            im.verify()
                    except (ValueError,KeyError,TypeError,OSError) as exc:raise InputContractError('Invalid image payload: '+str(exc)) from exc
                    images+=1
        if images>20 or chars>250000:raise InputContractError('Oversize API input')
        reserve=((chars+images*16384)*self.input_price+(self.max_output+10)*self.output_price)*self.budget_factor
        if self.route['provider']=='openrouter':reserve+=images*.005
        if total(self.ledger)+reserve>self.ledger['capUSD']:raise CostLimit('Global pilot money ceiling reached before request')
        body=dict(model=self.inference_model,messages=payload['messages'],max_tokens=self.max_output,
                  response_format={'type':'json_object'},stream=False)
        if self.route['provider']=='openrouter':
            body['provider']=dict(sort='price',allow_fallbacks=False,require_parameters=True,data_collection='deny',
                max_price=dict(prompt=self.input_price*1e6,completion=self.output_price*1e6,image=.005))
            if self.reasoning:body['reasoning']=self.reasoning
            if 'temperature' in self.parameters and self.model!='openai/gpt-6.1-sol':body['temperature']=0
        elif self.route['provider']=='ark':
            # DeepSeek's Ark catalogue does not advertise JSON mode. The same
            # strict public JSON action contract is still enforced locally.
            if self.route['model'].startswith('deepseek-'):body.pop('response_format')
            if self.route['model'].startswith('gpt-6-1-sol'):
                body.pop('max_tokens');body['max_completion_tokens']=self.max_output
                body['reasoning_effort']='low'
            else:
                body['thinking']={'type':'enabled' if self.reasoning_mode=='low' else 'disabled'}
                if self.reasoning_mode=='low':body['reasoning_effort']='low'
                body['temperature']=0
        elif self.route['provider']=='deepseek':
            if self.reasoning_mode=='low':body.update(thinking={'type':'enabled'},reasoning_effort='low')
            else:body.update(thinking={'type':'disabled'},reasoning_effort='none')
        else:
            body['temperature']=0
            if self.reasoning:
                # Aliyun max_tokens excludes reasoning. max_completion_tokens
                # bounds reasoning + answer (documented tolerance up to 10).
                body.pop('max_tokens')
                body.update(max_completion_tokens=self.max_output,enable_thinking=self.reasoning_mode=='low',preserve_thinking=False)
                if self.reasoning_mode=='low':body['reasoning_effort']='low'
        raw=json.dumps(body,ensure_ascii=False).encode();uid=uuid.uuid4().hex
        self.latest_attempt=dict(archiveId=uid,requestBodySha256=hashlib.sha256(raw).hexdigest(),responseAvailable=False)
        folder=self.directory/'api';folder.mkdir(exist_ok=True)
        with gzip.open(folder/(uid+'.request.json.gz'),'wb') as f:f.write(raw)
        pending=folder/(uid+'.pending');pending.write_bytes(raw)
        entry=dict(id=uid,run=self.directory.name,model=self.model,provider=self.route['provider'],status='pending',reservedUSD=reserve,createdAt=time.time())
        self.ledger['charges'].append(entry);write_json(self.ledger_path,self.ledger)
        started=time.time()
        try:
            result=http(self.route['baseURL']+'/chat/completions',self.secret,pending,timeout=self.timeout)
            with gzip.open(folder/(uid+'.response.private.json.gz'),'wt') as f:json.dump(result,f,ensure_ascii=False)
            self.latest_attempt['responseAvailable']=True
            entry['generationId']=result.get('id')
            entry['responseArchive']='api/'+uid+'.response.private.json.gz'
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
            choices=result.get('choices',[])
            if len(choices)!=1:raise GenerationError('API_CHOICES','Expected exactly one provider choice')
            choice=choices[0];finish=choice.get('finish_reason')
            if finish=='length':raise GenerationError('OUTPUT_TRUNCATED','Output ended at token/context limit; no action executed')
            if finish!='stop':raise GenerationError('API_FINISH_REASON','Provider did not finish normally: '+str(finish))
            content=choice.get('message',{}).get('content')
            if not isinstance(content,str) or not content.strip():raise GenerationError('API_EMPTY_OUTPUT','Provider returned no action text')
            return content
        except Exception as exc:
            if isinstance(exc,ProviderError) and exc.response is not None:
                with gzip.open(folder/(uid+'.error.json.gz'),'wt') as f:json.dump(dict(code=exc.code,status=exc.status,response=exc.response),f,ensure_ascii=False)
            if entry['status']=='pending':
                no_generation=isinstance(exc,ProviderError) and exc.status in (400,401,403,404,422,429) and isinstance(exc.response,dict) and not exc.response.get('choices') and not exc.response.get('usage')
                entry['status']='rejected_before_generation' if no_generation else 'uncertain'
                if no_generation:entry.update(accountedUSD=0,costBasis='HTTP rejection before generation; not a monetary receipt')
            entry['errorCode']=getattr(exc,'code',type(exc).__name__)
            entry['error']=str(exc)[:300];write_json(self.ledger_path,self.ledger);raise
        finally:
            pending.unlink(missing_ok=True)
            entry['latencySeconds']=round(time.time()-started,3);write_json(self.ledger_path,self.ledger)

    def usage(self):
        charges=[c for c in self.ledger['charges'] if c['run']==self.directory.name]
        return dict(calls=len(charges),costUSD=sum(c.get('accountedUSD',0) for c in charges),
            costLabel='USD charge / conservative native-provider estimate; see nativeCosts',
            confirmedUSD=sum(c.get('accountedUSD',0) for c in charges if c['status']=='settled'),
            nativeCosts={currency:sum(c.get('nativeCost',0) for c in charges if c.get('nativeCurrency')==currency) for currency in ['USD','CNY']},
            unsettledReservationsUSD=sum(c['reservedUSD'] for c in charges if c['status'] in ('pending','uncertain')),
            settled=all(c['status'] in ('settled','usage_estimated','rejected_before_generation') for c in charges),capUSD=self.ledger['capUSD'],
            promptTokens=sum(c.get('promptTokens',0) for c in charges),completionTokens=sum(c.get('completionTokens',0) for c in charges),
            reasoningTokens=sum(c.get('reasoningTokens') or 0 for c in charges),provider=self.route['provider'])
