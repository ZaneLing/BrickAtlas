import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { Budget } from '../../core/budget';
import { completion, LATEST_MODELS } from '../../core/openrouter';

const root=resolve(import.meta.dirname,'../../..');
const request=JSON.parse(readFileSync(0,'utf8'));
const latest=LATEST_MODELS.find(m=>m.id===request.model);
if(!latest && request.model!=='google/gemini-2.5-flash')throw Error('Model is not registered for this visual pilot');
if(!request.messages?.some((m:any)=>Array.isArray(m.content)&&m.content.some((c:any)=>c.type==='image_url')))
  throw Error('Dynamic pilot requires image observations');
if(!process.env.OPENROUTER_API_KEY)process.loadEnvFile(resolve(root,'.env'));
if(!process.env.OPENROUTER_API_KEY)throw Error('Missing API key');
const catalogue=await fetch('https://openrouter.ai/api/v1/models',{signal:AbortSignal.timeout(20000)});
if(!catalogue.ok)throw Error('Cannot verify model availability');
const entry=(await catalogue.json()).data.find((m:any)=>m.id===request.model);
if(!entry?.architecture?.input_modalities?.includes('image'))throw Error('Model no longer accepts images');
if(Number(entry.pricing.prompt)*1e6>(latest?.promptCap??.4)||Number(entry.pricing.completion)*1e6>(latest?.completionCap??3))
  throw Error('Model price exceeds preset ceiling');
const ledger=latest?`dynamic-v5-${request.model.replace('/','--')}-ledger.json`:'dynamic-v5-ledger.json';
const budget=new Budget(resolve(root,'benchmark/.runtime',ledger),latest?4.5:2);
console.log(JSON.stringify(await completion(process.env.OPENROUTER_API_KEY,request.model,request.messages,budget)));
