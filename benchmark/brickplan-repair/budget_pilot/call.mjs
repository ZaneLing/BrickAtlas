// One paid request, with a campaign-wide reservation made BEFORE network I/O.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const root = path.resolve(import.meta.dirname, '../../..');
if (fs.existsSync(path.join(root, '.env'))) process.loadEnvFile(path.join(root, '.env'));
const req = JSON.parse(fs.readFileSync(0, 'utf8'));
if(req.run?.startsWith('D--') && req.parserPolicy!=='one-explicit-json-object-with-optional-prose'){
 console.log(JSON.stringify({status:'budget_stop',reason:'Start a fresh process to use the audited response parser before dynamic calls'}));process.exit(0);
}
const dir = path.resolve(req.campaign);
const ledgerFile = path.join(dir, 'ledger.json');
const save = x => { fs.writeFileSync(ledgerFile+'.tmp', JSON.stringify(x,null,2)+'\n'); fs.renameSync(ledgerFile+'.tmp',ledgerFile); };
const ledger = JSON.parse(fs.readFileSync(ledgerFile,'utf8'));
// Timed-out requests retain their FULL reservation in committed spend. They are
// never retried and never treated as free; only a request still in flight blocks.
if (ledger.capUSD !== 10 || ledger.charges.some(c=>c.status==='pending')) throw Error('Campaign blocked by request in flight');
const cat = JSON.parse(fs.readFileSync(path.join(dir,'catalogue.json'),'utf8')).data;
const model = cat.find(m=>m.id===req.model);
if (!ledger.allowedModels.includes(req.model) || !model?.architecture?.input_modalities?.includes('image')) throw Error('Unregistered vision model');
if (!process.env.OPENROUTER_API_KEY) throw Error('Missing configured API key');
const rates = [model.pricing,...(model.pricing.overrides||[])];
const pin = Math.max(...rates.map(p=>Number(p.prompt||0))), pout = Math.max(...rates.map(p=>Number(p.completion||0)));
const inputBound=Math.max(pin,...rates.map(p=>Number(p.input_cache_write||0)),Number(model.pricing.input_cache_write_1h||0));
const iprice = Number(model.pricing.image||0), requestPrice=Number(model.pricing.request||0);
if (![pin,pout,iprice,requestPrice].every(x=>Number.isFinite(x)&&x>=0) || pin>0.0000041 || pout>0.000016) throw Error('Unexpected price');
let bytes=1024, images=0;
for (const m of req.messages) {
 if (typeof m.content==='string') bytes+=Buffer.byteLength(m.content);
 else for (const c of m.content) {if(c.type==='text')bytes+=Buffer.byteLength(c.text);else if(c.type==='image_url'){
  const raw=Buffer.from(c.image_url.url.split(',')[1]||'','base64');
  if(raw.length<24 || raw.toString('ascii',1,4)!=='PNG' || raw.readUInt32BE(16)>1600 || raw.readUInt32BE(20)>1200)throw Error('Image exceeds validated native raster envelope');
  images++;
 }else throw Error('Unsupported content');}
}
if (images<1 || images>64 || bytes>180000) throw Error('Input outside pilot limits');
// UTF-8 bytes bound text tokens; 16K/image exceeds our <=1600x1200 raster budgets.
// Also reserve a separate image charge, even for token-priced providers.
// Cache writes and separate reasoning/output allocation are reserved as well.
const ceiling=((bytes+images*16384)*inputBound+2*req.max_tokens*pout+images*Math.max(iprice,0.005)+requestPrice)*1.02;
const committed=ledger.charges.reduce((s,c)=>s+(c.actualUSD??c.reservedUSD),0);
if (committed+ceiling>ledger.capUSD || (req.remainingJobUSD!==undefined && ceiling>req.remainingJobUSD)) {
 console.log(JSON.stringify({status:'budget_stop',ceilingUSD:ceiling,committedUSD:committed}));process.exit(0);
}
const entry={id:crypto.randomUUID(),model:req.model,run:req.run,branch:req.branch,decision:req.decision,status:'pending',reservedUSD:ceiling,actualUSD:null,createdAt:new Date().toISOString()};
ledger.charges.push(entry);save(ledger);
const key=process.env.OPENROUTER_API_KEY;
const auth={Authorization:`Bearer ${key}`};
async function account(){try {const r=await fetch('https://openrouter.ai/api/v1/key',{headers:auth,signal:AbortSignal.timeout(15000)});if(!r.ok)return null;const d=(await r.json()).data;return {usage:d.usage,usage_daily:d.usage_daily,limit_remaining:d.limit_remaining};}catch{return null;}}
const before=await account();
entry.accountUsageBefore=before?.usage;save(ledger);
const body={model:req.model,messages:req.messages,max_tokens:req.max_tokens,stream:false,
 response_format:{type:'json_object'},
 provider:{sort:'price',allow_fallbacks:false,require_parameters:true,data_collection:'deny',max_price:{prompt:pin*1e6,completion:pout*1e6,image:Math.max(iprice,0.005)}},
 usage:{include:true}};
if(req.providerOnly){
 if(req.model!=='openai/gpt-6.1-sol' || JSON.stringify(req.providerOnly)!=='["OpenAI"]')throw Error('Unexpected provider selection');
 body.provider.only=req.providerOnly;
}
if(model.supported_parameters?.includes('seed'))body.seed=41;
if(model.supported_parameters?.includes('reasoning'))body.reasoning={effort:'low',exclude:true};
else if(model.supported_parameters?.includes('temperature'))body.temperature=0;
const start=performance.now();
try {
 const r=await fetch('https://openrouter.ai/api/v1/chat/completions',{method:'POST',headers:{...auth,'Content-Type':'application/json','X-OpenRouter-Title':'BrickAtlas $10 static dynamic usage pilot'},body:JSON.stringify(body),signal:AbortSignal.timeout(100000)});
 const d=await r.json();
 if(!r.ok || d.error){
  const after=await account();const verifiedNoCharge=before && after && before.usage===after.usage;
  Object.assign(entry,{status:verifiedNoCharge?'settled':'uncertain',actualUSD:verifiedNoCharge?0:null,httpStatus:r.status,errorCode:d.error?.code,providerUsageUnchanged:!!verifiedNoCharge,accountUsageBefore:before?.usage,accountUsageAfter:after?.usage});save(ledger);
  console.log(JSON.stringify({status:'api_error',httpStatus:r.status,errorCode:d.error?.code,message:String(d.error?.message||'Provider rejected request').replace(/Bearer\s+\S+|sk-[A-Za-z0-9_-]+/g,'[REDACTED]').slice(0,500),actualUSD:entry.actualUSD,blocked:entry.status!=='settled'}));process.exit(0);
 }
 let cost=d.usage?.cost;
 if(!Number.isFinite(cost) && d.id){const g=await fetch('https://openrouter.ai/api/v1/generation?id='+encodeURIComponent(d.id),{headers:auth,signal:AbortSignal.timeout(15000)});if(g.ok)cost=(await g.json()).data?.total_cost;}
 if(!Number.isFinite(cost)||cost<0)throw Error('Missing settled provider cost');
 Object.assign(entry,{status:cost<=ceiling?'settled':'uncertain',actualUSD:cost,generationId:d.id,servedModel:d.model,provider:d.provider});save(ledger);
 if(entry.status!=='settled')throw Error('Provider exceeded request reservation');
 const result={status:'returned',id:d.id,requestedModel:req.model,servedModel:d.model,provider:d.provider,
 content:d.choices?.[0]?.message?.content||'',usage:d.usage,costUSD:cost,finishReason:d.choices?.[0]?.finish_reason,
 latencyMs:Math.round(performance.now()-start),imageCount:images,textBytes:bytes,reservedUSD:ceiling,
 configuration:{maxTokens:req.max_tokens,reasoning:body.reasoning||null,temperature:body.temperature??null,seed:body.seed??null,provider:body.provider}};
 console.log(JSON.stringify(result));
}catch(e){if(entry.status==='pending')entry.status='uncertain';entry.error=String(e.message).slice(0,160);const after=await account();entry.accountUsageAfter=after?.usage;save(ledger);console.log(JSON.stringify({status:'api_error',message:entry.error,blocked:false,actualUSD:entry.actualUSD,reservedUnknownUSD:entry.status==='uncertain'?entry.reservedUSD:0}));}
