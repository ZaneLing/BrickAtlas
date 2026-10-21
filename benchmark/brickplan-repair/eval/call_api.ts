import { existsSync, readFileSync, openSync, closeSync, unlinkSync } from 'node:fs';
import { resolve } from 'node:path';
import { Budget, atomicJson } from '../../core/budget';
import { randomUUID } from 'node:crypto';
import { completion, modelPricing } from '../../core/openrouter';
const root=resolve(import.meta.dirname,'../../..');
if(process.argv.includes('--pricing')) {
  console.log(JSON.stringify(await modelPricing()));
} else {
  const request=JSON.parse(readFileSync(0,'utf8'));
  const user=request.messages?.find((m:any)=>m.role==='user');
  const observation=Array.isArray(user?.content) && user.content.find((c:any)=>c.type==='text');
  if(!observation || JSON.parse(observation.text).protocol!=='visual-rgb-v3' ||
     !user.content.some((c:any)=>c.type==='image_url') ||
     !user.content.filter((c:any)=>c.type==='image_url').every((c:any)=>c.image_url?.detail==='high'))
    throw new Error('Only visual-rgb-v3 requests with high-detail images are enabled');
  const catalogueResponse=await fetch('https://openrouter.ai/api/v1/models',{signal:AbortSignal.timeout(20000)});
  if(!catalogueResponse.ok)throw new Error('Cannot verify visual model capability');
  const catalogue=await catalogueResponse.json() as {data:{id:string;architecture:{input_modalities:string[]}}[]};
  if(!catalogue.data.find(m=>m.id===request.model)?.architecture.input_modalities.includes('image'))
    throw new Error('Selected model does not accept image input');
  if(!process.env.OPENROUTER_API_KEY) process.loadEnvFile(resolve(root,'.env'));


  if(process.env.BRICKPLAN_AUDIT==='static-audit-2026-10-14' && existsSync(resolve(root,'benchmark/.runtime/static-audit-pause')))throw Error('Audit scheduler pause before reservation');
  const path=resolve(root,'benchmark/.runtime/pilot.lock');
  const fd=openSync(path,'wx',0o600);closeSync(fd);
  try {
    const ledgerPath=resolve(root,'benchmark/.runtime/campaign-ledger.json');
    const audit=process.env.BRICKPLAN_AUDIT==='static-audit-2026-10-14';
    const auth=JSON.parse(readFileSync(resolve(root,audit?'deliverables/brickplan-static-audit-2026-10-14/budget-authorization.json':'deliverables/brickplan-api-pilot/budget-authorization.json'),'utf8'));
    const ledger=JSON.parse(readFileSync(ledgerPath,'utf8'));
    const cap=audit?5:2;
    if(auth.additionalCapUSD!==cap || auth.cumulativeCeilingUSD!==auth.baselineSpentUSD+cap || (audit&&auth.scope!=='static-audit-2026-10-14')) throw new Error('Invalid explicit pilot authorization');
    const persist=()=>atomicJson(ledgerPath,ledger);
    // Keep the historical $4.50 policy intact; this explicit user authorization
    // allows only this runner to append charges up to baseline + $2.
    const budget={
      reserve(model:string,ceiling:number) {
        if(ledger.charges.some((c:any)=>c.status!=='settled'))throw new Error('Unsettled charge');
        const committed=ledger.charges.reduce((s:number,c:any)=>s+(c.actual??c.reserved),0);
        if(!Number.isFinite(ceiling)||ceiling<=0||committed+ceiling>auth.cumulativeCeilingUSD)throw new Error('Budget limit reached before request');
        const id=randomUUID();ledger.charges.push({id,model,reserved:ceiling,actual:null,status:'pending',authorization:audit?auth.scope:'static-and-dynamic-brickplan-pilot-2026-10-14',createdAt:new Date().toISOString()});persist();return id;
      },
      settle(id:string,actual:number,generationId:string) {
        const c=ledger.charges.find((c:any)=>c.id===id);
        if(!c||!Number.isFinite(actual)||actual<0)throw new Error('Invalid settlement');
        c.actual=actual;c.generationId=generationId;c.status=actual<=c.reserved?'settled':'uncertain';persist();
        if(c.status!=='settled')throw new Error('Provider exceeded reservation');
      },
      uncertain(id:string) {const c=ledger.charges.find((c:any)=>c.id===id);if(c?.status==='pending')c.status='uncertain';persist();}
    } as unknown as Budget;
    const result=await completion(process.env.OPENROUTER_API_KEY!,request.model,request.messages,budget);
    console.log(JSON.stringify(result));
  } finally {unlinkSync(path);}
}
