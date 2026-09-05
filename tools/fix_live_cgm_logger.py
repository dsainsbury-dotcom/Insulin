from pathlib import Path

# v2.8.0 live CGM logger hotfix
p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = "let sb=window.supabase.createClient(SUPABASE_URL,SUPABASE_KEY,{auth:{persistSession:!DEMO_MODE,autoRefreshToken:!DEMO_MODE,detectSessionInUrl:!DEMO_MODE}}),session=null,cloudRows=[],foodRows=[],foodCloudReady=false,actualEdited=false,scanner=null,currentSmart=null,syncBusy=false,foodFilter='all',favouriteExpanded=false,favouritePanelOpen=localStorage.getItem('icrFavouritePanelOpen_v261')!=='0',latestCgm=null,cgmHistory=[],cgmChart=null,intelligenceOutcomes=[],intelligenceHours=24,foodLibraryOpen=localStorage.getItem('icrFoodLibraryOpen_v262')==='1';"
new = "let sb=window.supabase.createClient(SUPABASE_URL,SUPABASE_KEY,{auth:{persistSession:!DEMO_MODE,autoRefreshToken:!DEMO_MODE,detectSessionInUrl:!DEMO_MODE}}),session=null,cloudRows=[],foodRows=[],foodCloudReady=false,actualEdited=false,bgManualEdited=false,trendManualEdited=false,scanner=null,currentSmart=null,syncBusy=false,foodFilter='all',favouriteExpanded=false,favouritePanelOpen=localStorage.getItem('icrFavouritePanelOpen_v261')!=='0',latestCgm=null,cgmHistory=[],cgmChart=null,intelligenceOutcomes=[],intelligenceHours=24,foodLibraryOpen=localStorage.getItem('icrFoodLibraryOpen_v262')==='1';"
assert old in s
s = s.replace(old, new, 1)
old = "function fillFromLive(force=false){if(!latestCgm)return false;const age=readingAgeMinutes(latestCgm),trend=mapNightscoutTrend(latestCgm.direction);if(age>10||!Number.isFinite(Number(latestCgm.sgv))||!trend)return false;if(force||!$('bg').value)$('bg').value=mmolFromSgv(latestCgm.sgv).toFixed(1);if(force||!$('cgmTrend').value)$('cgmTrend').value=trend;return true}"
new = "function fillFromLive(force=false){if(!latestCgm)return false;const age=readingAgeMinutes(latestCgm),trend=mapNightscoutTrend(latestCgm.direction);if(age>10||!Number.isFinite(Number(latestCgm.sgv))||!trend)return false;if(force||!bgManualEdited)$('bg').value=mmolFromSgv(latestCgm.sgv).toFixed(1);if(force||!trendManualEdited)$('cgmTrend').value=trend;return true}"
assert old in s
s = s.replace(old, new, 1)
old = "$('mealForm').reset();$('icr').value=DEMO_MODE?'':15;$('target').value=DEMO_MODE?'':8;"
new = "$('mealForm').reset();bgManualEdited=false;trendManualEdited=false;$('icr').value=DEMO_MODE?'':15;$('target').value=DEMO_MODE?'':8;"
assert old in s
s = s.replace(old, new, 1)
old = "$('mealForm').addEventListener('submit',saveMeal);['carbs','icr'].forEach(id=>$(id).addEventListener('input',updateDose));$('actualInsulin').addEventListener('input',()=>actualEdited=true);"
new = "$('mealForm').addEventListener('submit',saveMeal);['carbs','icr'].forEach(id=>$(id).addEventListener('input',updateDose));$('bg').addEventListener('input',()=>bgManualEdited=true);$('cgmTrend').addEventListener('change',()=>trendManualEdited=true);$('actualInsulin').addEventListener('input',()=>actualEdited=true);"
assert old in s
s = s.replace(old, new, 1)
old = "window.addEventListener('online',()=>{syncAll();refreshLiveCgm(false)});window.addEventListener('offline',offlineState);window.addEventListener('focus',()=>{syncAll();refreshLiveCgm(false)});document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible'){syncAll();refreshLiveCgm(false)}});setInterval(syncAll,60000);setInterval(()=>refreshLiveCgm(false),60000);"
new = "window.addEventListener('online',()=>{syncAll();refreshLiveCgm(true)});window.addEventListener('offline',offlineState);window.addEventListener('focus',()=>{syncAll();refreshLiveCgm(true)});document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible'){syncAll();refreshLiveCgm(true)}});setInterval(syncAll,60000);setInterval(()=>refreshLiveCgm(true),60000);"
assert old in s
s = s.replace(old, new, 1)
s = s.replace("Greggs, PizzaExpress & McDonald's UK", "Greggs, PizzaExpress & Burger King UK")
s = s.replace("436 verified entries across Greggs, PizzaExpress and McDonald's UK.", "659 verified entries across Greggs, PizzaExpress and Burger King UK.")
p.write_text(s, encoding='utf-8')
print('live CGM logger fix applied')
