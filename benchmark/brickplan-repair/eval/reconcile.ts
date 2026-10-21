/** Manual, evidence-preserving aggregate reconciliation. Never retries inference. */
import {readFileSync,writeFileSync,openSync,closeSync,unlinkSync} from 'node:fs';
import {resolve} from 'node:path';
import {atomicJson} from '../../core/budget';
const root=resolve(import.meta.dirname,'../../..');
process.loadEnvFile(resolve(root,'.env'));
const lock=resolve(root,'benchmark/.runtime/pilot.lock');closeSync(openSync(lock,'wx',0o600));
try {
  const path=resolve(root,'benchmark/.runtime/campaign-ledger.json');
  const ledger=JSON.parse(readFileSync(path,'utf8')),pending=ledger.charges.filter((c:any)=>c.status!=='settled');
  if(pending.length!==1)throw Error('Manual reconciliation expects exactly one interrupted request');
  const evidencePath=resolve(root,'deliverables/brickplan-api-pilot/accounting/reconciliations.json');
  const evidence=JSON.parse(readFileSync(evidencePath,'utf8'));
  async function snapshot(){
    const response=await fetch('https://openrouter.ai/api/v1/key',{headers:{Authorization:`Bearer ${process.env.OPENROUTER_API_KEY}`},signal:AbortSignal.timeout(20000)});
    if(!response.ok)throw Error('Usage evidence unavailable');
    const {data}=await response.json() as any;
    return {queriedAt:new Date().toISOString(),usageDailyUSD:data.usage_daily};
  }
  const before=await snapshot();await new Promise(r=>setTimeout(r,20000));const after=await snapshot();
  const day=after.queriedAt.slice(0,10);
  if(before.queriedAt.slice(0,10)!==day||before.usageDailyUSD!==after.usageDailyUSD)throw Error('Usage not stable; no settlement');
  const known=ledger.charges.filter((c:any)=>c.generationId&&new Date(Number(c.generationId.split('-')[1])*1000).toISOString().slice(0,10)===day).reduce((s:number,c:any)=>s+c.actual,0);
  const previous=evidence.events.filter((e:any)=>e.utcDate===day).reduce((s:number,e:any)=>s+e.interruptedCostUpperBoundUSD,0);
  const additional=Number((after.usageDailyUSD-known-previous).toFixed(10));
  if(additional<0||additional>pending[0].reserved)throw Error('Usage remainder cannot be safely allocated');
  const event={utcDate:day,endpoint:'https://openrouter.ai/api/v1/key',snapshots:[before,after],knownResponseCostUSD:known,previousUnknownProvisionUSD:previous,
    interruptedChargeId:pending[0].id,interruptedCostUpperBoundUSD:additional,
    method:'Stable provider daily account usage minus all known same-day generation costs and prior unknown provisions. The aggregate unknown provision is an upper bound including possible unrelated usage; individual allocation is not exact generation billing. Interrupted episode is retained, never retried.'};
  evidence.events.push(event);atomicJson(evidencePath,evidence);
  Object.assign(pending[0],{actual:additional,status:'settled',accountingBasis:'provider_daily_usage_remainder_upper_bound',generationCostKnown:false,reconciliation:'deliverables/brickplan-api-pilot/accounting/reconciliations.json'});atomicJson(path,ledger);
  console.log(JSON.stringify(event));
} finally {unlinkSync(lock)}
