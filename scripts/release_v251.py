from pathlib import Path

p=Path('index.html')
s=p.read_text()
assert 'v2.5.0' in s
s=s.replace('<title>ICR Meal Dashboard v2.5.0</title>','<title>ICR Meal Dashboard v2.5.1</title>')
s=s.replace('<h1>ICR Meal Dashboard <small style="font-size:.48em;color:#0b5cab">v2.5.0</small></h1>','<h1>ICR Meal Dashboard <small style="font-size:.48em;color:#0b5cab">v2.5.1</small></h1>')
s=s.replace('<div class="badge">v2.5.0 LIVE</div>','<div class="badge">v2.5.1 LIVE</div>')
s=s.replace('.reassure{margin-top:12px;border-left:4px solid var(--green);padding:10px 12px;background:var(--softgreen);border-radius:10px;font-size:.84rem;line-height:1.45}', '.reassure{margin-top:12px;border-left:4px solid var(--green);padding:10px 12px;background:var(--softgreen);border-radius:10px;font-size:.84rem;line-height:1.45}.liveCgmHero{border:1px solid #b7e1cf;background:linear-gradient(180deg,#f2fbf7,#fff);border-radius:16px;padding:15px}.liveCgmValue{font-size:2rem;font-weight:900;color:var(--green);margin-top:4px}.liveCgmMeta{font-size:.78rem;color:var(--muted);margin-top:4px}.liveCgmSettings{margin-top:12px;padding-top:12px;border-top:1px solid var(--line)}')
anchor='<section class="card"><h2>Add meal</h2><form id="mealForm"><div class="grid">'
live='''<section class="card"><div class="liveCgmHero"><div class="reviewHead"><div><h2 style="margin-bottom:4px">Live CGM - Nightscout</h2><div class="sectionNote">Reads your latest Nightscout glucose and trend. Live values can fill the meal glucose and trend fields, but you can always edit them manually.</div></div><span id="nightscoutBadge" class="pill">NOT SET UP</span></div><div id="liveCgmValue" class="liveCgmValue">-- mmol/L</div><div id="liveCgmMeta" class="liveCgmMeta">Add your Nightscout connection below.</div><div class="actions"><button id="useLiveCgm" class="primary" type="button" disabled>Use live reading</button><button id="refreshLiveCgm" class="secondary" type="button">Refresh now</button></div><div class="liveCgmSettings"><div class="grid"><div><label>Nightscout site URL</label><input id="nightscoutUrl" type="url" placeholder="https://your-site.example.com"></div><div><label>Read-only Nightscout token</label><input id="nightscoutToken" type="password" autocomplete="off" placeholder="subject-xxxxxxxxxxxxxxxx"></div></div><div class="actions"><button id="saveNightscout" class="secondary" type="button">Save connection on this device</button><button id="forgetNightscout" class="danger" type="button">Forget token</button></div><div class="hint">The token is stored only in this browser on this device. It is not saved to Supabase and is not included in GitHub. Use a Nightscout subject with the readable role, never your API_SECRET.</div></div></div></section>
'''
assert anchor in s
s=s.replace(anchor,live+anchor,1)
old="const MEAL_QUEUE='icrMealDashboard_v1',FOOD_QUEUE='icrFoodQueue_v241',FOOD_CACHE='icrFoodCache_v241',LEGACY_FOOD='icrSmartFoodLibrary_v24',LEGACY_MIGRATED='icrLegacyFoodMigrated_v242';"
assert old in s
s=s.replace(old,old+"\nconst NIGHTSCOUT_URL_KEY='icrNightscoutUrl_v251',NIGHTSCOUT_TOKEN_KEY='icrNightscoutToken_v251';",1)
oldlet="let sb=window.supabase.createClient(SUPABASE_URL,SUPABASE_KEY,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}}),session=null,cloudRows=[],foodRows=[],foodCloudReady=false,actualEdited=false,scanner=null,currentSmart=null,syncBusy=false,foodFilter='all';"
assert oldlet in s
s=s.replace(oldlet,oldlet[:-1]+",latestCgm=null;",1)
insert_after="function offlineState(){$('offlineBar').classList.toggle('hidden',navigator.onLine);if(!navigator.onLine)setNotice('Offline. Changes will queue safely and sync automatically when online.','warn');updateQueueUI()}"
funcs=r'''
function nightscoutConfig(){return{url:(localStorage.getItem(NIGHTSCOUT_URL_KEY)||'').trim().replace(/\/$/,''),token:(localStorage.getItem(NIGHTSCOUT_TOKEN_KEY)||'').trim()}}
function mapNightscoutTrend(direction){const m={DoubleUp:'↑↑ Rapidly rising',SingleUp:'↑ Rising',FortyFiveUp:'↗ Slightly rising',Flat:'→ Stable',FortyFiveDown:'↘ Slightly falling',SingleDown:'↓ Falling',DoubleDown:'↓↓ Rapidly falling'};return m[direction]||''}
function mmolFromSgv(sgv){return Number(sgv)/18}
function readingAgeMinutes(entry){const t=Number(entry?.date)||Date.parse(entry?.dateString||entry?.sysTime||'');return Number.isFinite(t)?Math.max(0,(Date.now()-t)/60000):Infinity}
function fillFromLive(force=false){if(!latestCgm)return false;const age=readingAgeMinutes(latestCgm),trend=mapNightscoutTrend(latestCgm.direction);if(age>10||!Number.isFinite(Number(latestCgm.sgv))||!trend)return false;if(force||!$('bg').value)$('bg').value=mmolFromSgv(latestCgm.sgv).toFixed(1);if(force||!$('cgmTrend').value)$('cgmTrend').value=trend;return true}
function renderLiveCgm(){const cfg=nightscoutConfig();if(!cfg.url||!cfg.token){$('nightscoutBadge').textContent='NOT SET UP';$('liveCgmValue').textContent='-- mmol/L';$('liveCgmMeta').textContent='Add your Nightscout connection below.';$('useLiveCgm').disabled=true;return}if(!latestCgm){$('nightscoutBadge').textContent='READY';$('liveCgmMeta').textContent='Connection saved. Refreshing live CGM...';$('useLiveCgm').disabled=true;return}const mmol=mmolFromSgv(latestCgm.sgv),age=readingAgeMinutes(latestCgm),trend=mapNightscoutTrend(latestCgm.direction),fresh=age<=10&&Number.isFinite(mmol)&&!!trend;$('liveCgmValue').textContent=`${mmol.toFixed(1)} mmol/L ${trend?trend.split(' ')[0]:''}`;$('liveCgmMeta').textContent=`Nightscout ${latestCgm.direction||'trend unavailable'} | ${age<1?'less than 1':Math.round(age)} min old | ${new Date(Number(latestCgm.date)||latestCgm.dateString).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})}`;$('nightscoutBadge').textContent=fresh?'LIVE':'STALE / CHECK';$('useLiveCgm').disabled=!fresh}
async function refreshLiveCgm(autoFill=true){const cfg=nightscoutConfig();renderLiveCgm();if(!cfg.url||!cfg.token)return false;try{const endpoint=`${cfg.url}/api/v1/entries.json?count=1&token=${encodeURIComponent(cfg.token)}`,r=await fetch(endpoint,{cache:'no-store'});if(!r.ok)throw new Error(`Nightscout HTTP ${r.status}`);const data=await r.json(),entry=Array.isArray(data)?data[0]:null;if(!entry||!Number.isFinite(Number(entry.sgv)))throw new Error('No current SGV returned');latestCgm=entry;renderLiveCgm();if(autoFill)fillFromLive(false);return true}catch(e){console.error('Nightscout',e);latestCgm=null;$('nightscoutBadge').textContent='CONNECTION ERROR';$('liveCgmValue').textContent='-- mmol/L';$('liveCgmMeta').textContent='Could not read Nightscout. Check the site URL, readable token and connection.';$('useLiveCgm').disabled=true;return false}}
function saveNightscoutConfig(){let url=$('nightscoutUrl').value.trim(),token=$('nightscoutToken').value.trim();if(!url||!token)return alert('Enter both your Nightscout site URL and readable token.');url=url.replace(/\/$/,'');localStorage.setItem(NIGHTSCOUT_URL_KEY,url);localStorage.setItem(NIGHTSCOUT_TOKEN_KEY,token);latestCgm=null;refreshLiveCgm(true)}
function forgetNightscoutConfig(){if(!confirm('Forget the Nightscout connection on this device?'))return;localStorage.removeItem(NIGHTSCOUT_URL_KEY);localStorage.removeItem(NIGHTSCOUT_TOKEN_KEY);$('nightscoutUrl').value='';$('nightscoutToken').value='';latestCgm=null;renderLiveCgm()}
'''
assert insert_after in s
s=s.replace(insert_after,insert_after+funcs,1)
s=s.replace("$('cgmTrend').value='';$('fatLevel').disabled=false;", "$('cgmTrend').value='';$('fatLevel').disabled=false;refreshLiveCgm(true);",1)
oldinit="async function init(){offlineState();$('email').value=localStorage.getItem('icrCloudEmail')||'';session=(await sb.auth.getSession()).data.session||null;"
newinit="async function init(){offlineState();$('email').value=localStorage.getItem('icrCloudEmail')||'';const ns=nightscoutConfig();$('nightscoutUrl').value=ns.url;$('nightscoutToken').value=ns.token;renderLiveCgm();if(ns.url&&ns.token)await refreshLiveCgm(true);session=(await sb.auth.getSession()).data.session||null;"
assert oldinit in s
s=s.replace(oldinit,newinit,1)
event_anchor="$('exportBtn').onclick=exportCsv;"
assert event_anchor in s
s=s.replace(event_anchor,event_anchor+"\n$('saveNightscout').onclick=saveNightscoutConfig;$('forgetNightscout').onclick=forgetNightscoutConfig;$('refreshLiveCgm').onclick=()=>refreshLiveCgm(true);$('useLiveCgm').onclick=()=>{if(fillFromLive(true))setNotice('Live Nightscout glucose and trend copied into this meal.','good')};",1)
oldlisteners="window.addEventListener('online',syncAll);window.addEventListener('offline',offlineState);window.addEventListener('focus',syncAll);document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')syncAll()});setInterval(syncAll,60000);"
newlisteners="window.addEventListener('online',()=>{syncAll();refreshLiveCgm(false)});window.addEventListener('offline',offlineState);window.addEventListener('focus',()=>{syncAll();refreshLiveCgm(false)});document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible'){syncAll();refreshLiveCgm(false)}});setInterval(syncAll,60000);setInterval(()=>refreshLiveCgm(false),60000);"
assert oldlisteners in s
s=s.replace(oldlisteners,newlisteners,1)
vh='<section class="card"><h2>Version history</h2><div class="versionGrid">'
assert vh in s
s=s.replace(vh,vh+'<div class="versionItem"><strong>v2.5.1 - Live Nightscout CGM</strong><ul><li>Added direct read-only Nightscout live CGM support for current glucose, trend and reading age.</li><li>Fresh Nightscout readings can fill the meal glucose and trend fields while keeping manual override.</li><li>The app refreshes the live feed on demand, when returning to the app and every 60 seconds.</li><li>Read-only Nightscout credentials are stored only in local browser storage on the device and are never committed to GitHub or saved to Supabase.</li><li>Readings older than 10 minutes are flagged stale and are not offered for meal auto-fill.</li></ul></div>',1)
p.write_text(s)

def append_once(path, marker, text):
    q=Path(path); body=q.read_text() if q.exists() else ''
    if marker not in body:
        q.write_text(body.rstrip()+"\n\n"+text.strip()+"\n")

append_once('CHANGELOG.md','## v2.5.1','''## v2.5.1 - 2026-09-05
- Added live read-only Nightscout CGM integration.
- Current glucose, trend direction and reading age are retrieved from the latest SGV endpoint.
- Fresh live readings can populate the meal glucose and CGM trend fields with manual override retained.
- Nightscout site URL and readable token are stored only in local browser storage, not GitHub or Supabase.
- Readings older than 10 minutes are treated as stale and are not used for meal auto-fill.''')
append_once('README.md','### Live Nightscout CGM','''### Live Nightscout CGM
v2.5.1 can read the latest CGM value and direction from a user's Nightscout site using a dedicated `readable` subject token. The connection is configured per device in the browser. The token must never be replaced with `API_SECRET` and must never be committed to the public repository. Fresh readings may populate meal-start glucose and trend, but remain manually editable.''')
append_once('PROJECT_BRAIN.md','## v2.5.1 live Nightscout','''## v2.5.1 live Nightscout
- Live Nightscout API access was proven on 5 Sep 2026 using `/api/v1/entries.json?count=1&token=...` and repeated 5-minute SGV data.
- Production app now supports a per-device Nightscout URL + dedicated readable token held in browser localStorage only.
- Live readings supply mmol/L, Nightscout direction and reading age. Supported direction mapping: DoubleUp, SingleUp, FortyFiveUp, Flat, FortyFiveDown, SingleDown, DoubleDown.
- A reading older than 10 minutes is stale and must not be auto-filled into a meal.
- Manual glucose/trend entry remains available and takes precedence when the user edits it.
- Do not place Nightscout `API_SECRET` or readable tokens in public GitHub source or Supabase meal records.
- This feature is data capture/supportive only. Dexcom remains the treatment-decision source.''')
Path('NIGHTSCOUT_LIVE_CGM.md').write_text('''# Nightscout Live CGM integration - v2.5.1

## Purpose
Use Nightscout as a near-real-time read-only CGM source so a meal can capture the glucose and direction that existed when it was logged.

## Endpoint
`/api/v1/entries.json?count=1&token=<READABLE_TOKEN>`

## Security
Use a dedicated Nightscout subject with role `readable`. Never use or expose `API_SECRET`. The browser stores the site URL and token in localStorage on that device only. Credentials are not written to Supabase meal records and are not committed to GitHub.

## Freshness
A current reading is usable for meal auto-fill only when it is no more than 10 minutes old and has a recognised trend direction. Stale or unrecognised data remains visible as a warning and is not offered as a live meal value.

## Direction mapping
- DoubleUp -> rapidly rising
- SingleUp -> rising
- FortyFiveUp -> slightly rising
- Flat -> stable
- FortyFiveDown -> slightly falling
- SingleDown -> falling
- DoubleDown -> rapidly falling

## Clinical boundary
This is observational/supportive data capture. It does not calculate correction insulin or recommend a pre-bolus interval. Dexcom remains the treatment-decision source. Trend and meal outcome evidence can inform later clinician discussion and the existing pre-bolus evidence protocol.
''')
