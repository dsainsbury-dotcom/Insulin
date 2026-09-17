from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="async function fetchCgmHistory(hours=24){const cfg=nightscoutConfig();if(!cfg.url||!cfg.token)return false;const count=Math.max(48,Math.ceil(hours*12)+24);const r=await fetch(`${cfg.url}/api/v1/entries.json?count=${count}&token=${encodeURIComponent(cfg.token)}`,{cache:'no-store'});if(!r.ok)throw new Error(`Nightscout HTTP ${r.status}`);const data=await r.json(),cutoff=Date.now()-hours*3600000;cgmHistory=(Array.isArray(data)?data:[]).filter(e=>Number.isFinite(Number(e.sgv))&&(Number(e.date)||Date.parse(e.dateString||''))>=cutoff).sort((a,b)=>(Number(a.date)||0)-(Number(b.date)||0));return cgmHistory.length>0}"
new="async function fetchCgmHistory(hours=24){const cfg=nightscoutConfig();if(!cfg.url||!cfg.token)return false;const cutoff=Date.now()-hours*3600000,pageSize=500,maxPages=Math.max(1,Math.ceil((hours*12+24)/pageSize)),all=[];for(let page=0;page<maxPages;page++){const skip=page*pageSize,endpoint=`${cfg.url}/api/v1/entries.json?count=${pageSize}&skip=${skip}&token=${encodeURIComponent(cfg.token)}`,r=await fetch(endpoint,{cache:'no-store'});if(!r.ok)throw new Error(`Nightscout history HTTP ${r.status} on page ${page+1}`);const data=await r.json();if(!Array.isArray(data)||!data.length)break;all.push(...data);const oldest=data.reduce((a,e)=>Math.min(a,Number(e.date)||Date.parse(e.dateString||'')||Infinity),Infinity);if(oldest<=cutoff||data.length<pageSize)break}const seen=new Map();for(const e of all){const t=Number(e.date)||Date.parse(e.dateString||'');if(Number.isFinite(Number(e.sgv))&&Number.isFinite(t)&&t>=cutoff)seen.set(`${t}:${e.sgv}`,e)}cgmHistory=[...seen.values()].sort((a,b)=>(Number(a.date)||Date.parse(a.dateString||''))-(Number(b.date)||Date.parse(b.dateString||'')));return cgmHistory.length>0}"
if old not in s: raise SystemExit('fetchCgmHistory target not found')
s=s.replace(old,new,1)
s=s.replace('<title>ICR Meal Dashboard v2.9.1</title>','<title>ICR Meal Dashboard v2.9.2</title>',1)
s=s.replace('v2.9.1 LIVE','v2.9.2 LIVE')
needle='<div class="versionGrid">'
entry='<div class="versionItem"><strong>v2.9.2 - Nightscout history pagination fix</strong><ul><li>Loads the 7-day Nightscout history in smaller paged requests instead of one oversized request.</li><li>This prevents Live Intelligence from failing when the Nightscout server limits large entry counts.</li><li>Duplicate readings are removed before meal matching and CGM analysis.</li><li>No insulin calculation or dosing recommendation logic changed.</li></ul></div>'
if needle not in s: raise SystemExit('version history target not found')
s=s.replace(needle,needle+entry,1)
p.write_text(s,encoding='utf-8')
print('v2.9.2 patch applied')