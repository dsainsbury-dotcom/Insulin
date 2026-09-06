from pathlib import Path

# v2.8.2 live CGM autofill reliability hotfix
p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Version bump for the published hotfix. Keep the older version-history entry intact.
s = s.replace('<title>ICR Meal Dashboard v2.8.1</title>', '<title>ICR Meal Dashboard v2.8.2</title>', 1)
s = s.replace('<h1>ICR Meal Dashboard <small style="font-size:.48em;color:#0b5cab">v2.8.1</small></h1>', '<h1>ICR Meal Dashboard <small style="font-size:.48em;color:#0b5cab">v2.8.2</small></h1>', 1)
s = s.replace('<div class="badge">v2.8.1 LIVE</div>', '<div class="badge">v2.8.2 LIVE</div>', 1)

old = "function mapNightscoutTrend(direction){const m={DoubleUp:'↑↑ Rapidly rising',SingleUp:'↑ Rising',FortyFiveUp:'↗ Slightly rising',Flat:'→ Stable',FortyFiveDown:'↘ Slightly falling',SingleDown:'↓ Falling',DoubleDown:'↓↓ Rapidly falling'};return m[direction]||''}"
new = "function mapNightscoutTrend(direction){const m={DoubleUp:'↑↑ Rapidly rising',SingleUp:'↑ Rising',FortyFiveUp:'↗ Slightly rising',Flat:'→ Stable',FortyFiveDown:'↘ Slightly falling',SingleDown:'↓ Falling',DoubleDown:'↓↓ Rapidly falling','↑↑':'↑↑ Rapidly rising','↑':'↑ Rising','↗':'↗ Slightly rising','→':'→ Stable','↘':'↘ Slightly falling','↓':'↓ Falling','↓↓':'↓↓ Rapidly falling',Stable:'→ Stable',Rising:'↑ Rising',Falling:'↓ Falling'};return m[String(direction||'').trim()]||''}"
assert old in s, 'Nightscout trend mapper changed unexpectedly'
s = s.replace(old, new, 1)

old = "function fillFromLive(force=false){if(!latestCgm)return false;const age=readingAgeMinutes(latestCgm),trend=mapNightscoutTrend(latestCgm.direction);if(age>10||!Number.isFinite(Number(latestCgm.sgv))||!trend)return false;if(force||!bgManualEdited)$('bg').value=mmolFromSgv(latestCgm.sgv).toFixed(1);if(force||!trendManualEdited)$('cgmTrend').value=trend;return true}"
new = "function fillFromLive(force=false){if(!latestCgm)return false;const age=readingAgeMinutes(latestCgm),trend=mapNightscoutTrend(latestCgm.direction),validGlucose=age<=10&&Number.isFinite(Number(latestCgm.sgv));if(!validGlucose)return false;let filled=false;const bgEmpty=!$('bg').value.trim(),trendEmpty=!$('cgmTrend').value;if(force||!bgManualEdited||bgEmpty){$('bg').value=mmolFromSgv(latestCgm.sgv).toFixed(1);filled=true}if(trend&&(force||!trendManualEdited||trendEmpty)){$('cgmTrend').value=trend;filled=true}return filled}"
assert old in s, 'fillFromLive changed unexpectedly'
s = s.replace(old, new, 1)

old = "function renderLiveCgm(){const cfg=nightscoutConfig();if(!cfg.url||!cfg.token){$('nightscoutBadge').textContent='NOT SET UP';$('liveCgmValue').textContent='-- mmol/L';$('liveCgmMeta').textContent='Add your Nightscout connection below.';$('useLiveCgm').disabled=true;return}if(!latestCgm){$('nightscoutBadge').textContent='READY';$('liveCgmMeta').textContent='Connection saved. Refreshing live CGM...';$('useLiveCgm').disabled=true;return}const mmol=mmolFromSgv(latestCgm.sgv),age=readingAgeMinutes(latestCgm),trend=mapNightscoutTrend(latestCgm.direction),fresh=age<=10&&Number.isFinite(mmol)&&!!trend;$('liveCgmValue').textContent=`${mmol.toFixed(1)} mmol/L ${trend?trend.split(' ')[0]:''}`;$('liveCgmMeta').textContent=`Nightscout ${latestCgm.direction||'trend unavailable'} | ${age<1?'less than 1':Math.round(age)} min old | ${new Date(Number(latestCgm.date)||latestCgm.dateString).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})}`;$('nightscoutBadge').textContent=fresh?'LIVE':'STALE / CHECK';$('useLiveCgm').disabled=!fresh}"
new = "function renderLiveCgm(){const cfg=nightscoutConfig();if(!cfg.url||!cfg.token){$('nightscoutBadge').textContent='NOT SET UP';$('liveCgmValue').textContent='-- mmol/L';$('liveCgmMeta').textContent='Add your Nightscout connection below.';$('useLiveCgm').disabled=true;return}if(!latestCgm){$('nightscoutBadge').textContent='READY';$('liveCgmMeta').textContent='Connection saved. Refreshing live CGM...';$('useLiveCgm').disabled=true;return}const mmol=mmolFromSgv(latestCgm.sgv),age=readingAgeMinutes(latestCgm),trend=mapNightscoutTrend(latestCgm.direction),fresh=age<=10&&Number.isFinite(mmol);$('liveCgmValue').textContent=`${mmol.toFixed(1)} mmol/L ${trend?trend.split(' ')[0]:''}`;$('liveCgmMeta').textContent=`Nightscout ${trend?(latestCgm.direction||'trend available'):'trend unavailable'} | ${age<1?'less than 1':Math.round(age)} min old | ${new Date(Number(latestCgm.date)||latestCgm.dateString).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})}`;$('nightscoutBadge').textContent=fresh?'LIVE':'STALE / CHECK';$('useLiveCgm').disabled=!fresh}"
assert old in s, 'renderLiveCgm changed unexpectedly'
s = s.replace(old, new, 1)

old = "async function refreshLiveCgm(autoFill=true){const cfg=nightscoutConfig();renderLiveCgm();if(!cfg.url||!cfg.token)return false;try{const endpoint=`${cfg.url}/api/v1/entries.json?count=1&token=${encodeURIComponent(cfg.token)}`,r=await fetch(endpoint,{cache:'no-store'});if(!r.ok)throw new Error(`Nightscout HTTP ${r.status}`);const data=await r.json(),entry=Array.isArray(data)?data[0]:null;if(!entry||!Number.isFinite(Number(entry.sgv)))throw new Error('No current SGV returned');latestCgm=entry;renderLiveCgm();if(autoFill)fillFromLive(false);return true}catch(e){console.error('Nightscout',e);latestCgm=null;$('nightscoutBadge').textContent='CONNECTION ERROR';$('liveCgmValue').textContent='-- mmol/L';$('liveCgmMeta').textContent='Could not read Nightscout. Check the site URL, readable token and connection.';$('useLiveCgm').disabled=true;return false}}"
new = "async function refreshLiveCgm(autoFill=true){const cfg=nightscoutConfig();renderLiveCgm();if(!cfg.url||!cfg.token)return false;try{const endpoint=`${cfg.url}/api/v1/entries.json?count=1&token=${encodeURIComponent(cfg.token)}`,r=await fetch(endpoint,{cache:'no-store'});if(!r.ok)throw new Error(`Nightscout HTTP ${r.status}`);const data=await r.json(),entry=Array.isArray(data)?data[0]:null;if(!entry||!Number.isFinite(Number(entry.sgv)))throw new Error('No current SGV returned');latestCgm=entry;renderLiveCgm();if(autoFill)fillFromLive(false);return true}catch(e){console.error('Nightscout',e);if(latestCgm&&readingAgeMinutes(latestCgm)<=10){renderLiveCgm();if(autoFill)fillFromLive(false);return true}$('nightscoutBadge').textContent='CONNECTION ERROR';$('liveCgmValue').textContent='-- mmol/L';$('liveCgmMeta').textContent='Could not read Nightscout. Retrying shortly; you can enter the Dexcom reading manually if needed.';$('useLiveCgm').disabled=true;return false}}\nlet liveCgmRetryPromise=null;const wait=ms=>new Promise(resolve=>setTimeout(resolve,ms));async function refreshLiveCgmReliable(force=false){if(liveCgmRetryPromise)return liveCgmRetryPromise;liveCgmRetryPromise=(async()=>{for(const delay of [0,1200,3000]){if(delay)await wait(delay);const ok=await refreshLiveCgm(false);if(ok){fillFromLive(force);if($('bg').value.trim()&&$('cgmTrend').value)return true}}return Boolean($('bg').value.trim()||$('cgmTrend').value)})();try{return await liveCgmRetryPromise}finally{liveCgmRetryPromise=null}}"
assert old in s, 'refreshLiveCgm changed unexpectedly'
s = s.replace(old, new, 1)

old = "if(ns.url&&ns.token)await refreshLiveCgm(true);"
new = "if(ns.url&&ns.token)await refreshLiveCgmReliable(false);"
assert old in s, 'init live CGM call changed unexpectedly'
s = s.replace(old, new, 1)

old = "refreshLiveCgm(true);$('fatGrams').disabled=false;actualEdited=false;currentSmart=null;"
new = "refreshLiveCgmReliable(false);$('fatGrams').disabled=false;actualEdited=false;currentSmart=null;"
assert old in s, 'post-save live CGM refresh changed unexpectedly'
s = s.replace(old, new, 1)

old = "document.querySelectorAll('.viewBtn').forEach(b=>b.onclick=()=>{document.querySelectorAll('.viewBtn').forEach(x=>x.classList.toggle('active',x===b));document.querySelectorAll('.viewPane').forEach(x=>x.classList.toggle('active',x.id===b.dataset.view));if(b.dataset.view==='intelligence')refreshIntelligence();window.scrollTo({top:0,behavior:'smooth'})});"
new = "document.querySelectorAll('.viewBtn').forEach(b=>b.onclick=()=>{document.querySelectorAll('.viewBtn').forEach(x=>x.classList.toggle('active',x===b));document.querySelectorAll('.viewPane').forEach(x=>x.classList.toggle('active',x.id===b.dataset.view));if(b.dataset.view==='tracker')refreshLiveCgmReliable(false);if(b.dataset.view==='intelligence')refreshIntelligence();window.scrollTo({top:0,behavior:'smooth'})});"
assert old in s, 'view tab handler changed unexpectedly'
s = s.replace(old, new, 1)

old = "$('toggleNightscoutSettings').onclick=()=>setNightscoutSettings($('nightscoutSettings').classList.contains('hidden'));$('saveNightscout').onclick=saveNightscoutConfig;$('forgetNightscout').onclick=forgetNightscoutConfig;$('refreshLiveCgm').onclick=()=>refreshLiveCgm(true);$('useLiveCgm').onclick=()=>{if(fillFromLive(true))setNotice('Live Nightscout glucose and trend copied into this meal.','good')};"
new = "$('toggleNightscoutSettings').onclick=()=>setNightscoutSettings($('nightscoutSettings').classList.contains('hidden'));$('saveNightscout').onclick=saveNightscoutConfig;$('forgetNightscout').onclick=forgetNightscoutConfig;$('refreshLiveCgm').onclick=()=>refreshLiveCgmReliable(false);$('useLiveCgm').onclick=async()=>{if(await refreshLiveCgmReliable(true))setNotice('Fresh Nightscout glucose copied into this meal; trend is copied too when Nightscout provides it.','good');else setNotice('Live CGM is not available yet. Check the Nightscout status or enter the Dexcom reading manually.','warn')};"
assert old in s, 'Nightscout button handlers changed unexpectedly'
s = s.replace(old, new, 1)

old = "window.addEventListener('online',()=>{syncAll();refreshLiveCgm(true)});window.addEventListener('offline',offlineState);window.addEventListener('focus',()=>{syncAll();refreshLiveCgm(true)});document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible'){syncAll();refreshLiveCgm(true)}});setInterval(syncAll,60000);setInterval(()=>refreshLiveCgm(true),60000);setInterval(()=>{if(document.getElementById('intelligence').classList.contains('active'))refreshIntelligence()},300000);"
new = "window.addEventListener('online',()=>{syncAll();refreshLiveCgmReliable(false)});window.addEventListener('offline',offlineState);window.addEventListener('focus',()=>{syncAll();refreshLiveCgmReliable(false)});window.addEventListener('pageshow',()=>{syncAll();refreshLiveCgmReliable(false)});document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible'){syncAll();refreshLiveCgmReliable(false)}});setInterval(syncAll,60000);setInterval(()=>refreshLiveCgm(false),60000);setInterval(()=>{if(document.getElementById('intelligence').classList.contains('active'))refreshIntelligence()},300000);"
assert old in s, 'resume listeners changed unexpectedly'
s = s.replace(old, new, 1)

history_anchor = '<section class="card"><h2>Version history</h2><div class="versionGrid">'
history_item = '<div class="versionItem"><strong>v2.8.2 - Live CGM autofill reliability</strong><ul><li>Refreshes Nightscout again when the iPhone/PWA resumes via pageshow, focus, visibility and when Meal Tracker is reopened.</li><li>Adds short automatic retries for transient Nightscout/network delays instead of silently leaving the meal fields blank.</li><li>Fresh glucose can populate even if a Nightscout trend string is temporarily missing or unrecognised; the trend remains manual until a valid direction is available.</li><li>Background refreshes preserve a non-empty glucose or trend value that you entered manually.</li></ul></div>'
assert history_anchor in s, 'version history anchor missing'
s = s.replace(history_anchor, history_anchor + history_item, 1)

p.write_text(s, encoding='utf-8')
print('v2.8.2 live CGM autofill reliability fix applied')
