from pathlib import Path

p=Path('index.html')
s=p.read_text()
s=s.replace('ICR Meal Dashboard v2.8.4','ICR Meal Dashboard v2.8.5')
s=s.replace('v2.8.4</small>','v2.8.5</small>')
s=s.replace('v2.8.4 LIVE','v2.8.5 LIVE')

# Favourite rename
old="async function toggleFavourite(f){f=normalizeFood(f);f.favourite=!f.favourite;if(session&&navigator.onLine&&foodCloudReady&&await upsertFood(f)){await fetchFoods();setNotice(f.favourite?'Added to favourites.':'Removed from favourites.','good');return}queueFood(f);foodRows=[f,...foodRows.filter(x=>x.client_id!==f.client_id)];write(FOOD_CACHE,foodRows);renderLibrary();setNotice(f.favourite?'Favourite queued and will sync automatically.':'Favourite change queued and will sync automatically.','warn')}"
new=old+"\nasync function renameFavourite(f){f=normalizeFood(f);if(!f.favourite)return;const next=prompt('Rename favourite',f.name);if(next===null)return;const name=next.trim();if(!name)return setNotice('Favourite name was not changed.','warn');if(name===f.name)return;f.name=name;f.updated_at=new Date().toISOString();if(session&&navigator.onLine&&foodCloudReady&&await upsertFood(f)){await fetchFoods();setNotice('Favourite renamed to '+name+'.','good');return}queueFood(f);foodRows=[f,...foodRows.filter(x=>x.client_id!==f.client_id)];write(FOOD_CACHE,foodRows);renderLibrary();setNotice('Favourite rename saved on this device and queued to sync automatically.','warn')}"
if old not in s: raise SystemExit('toggleFavourite anchor missing')
s=s.replace(old,new)
oldq='<button class="primary favQuickUse" data-i="${i}" type="button">Use</button></div>'
newq='<div class="actions" style="margin-top:8px"><button class="primary favQuickUse" data-i="${i}" type="button">Use</button><button class="secondary favQuickRename" data-i="${i}" type="button">Rename</button></div></div>'
if oldq not in s: raise SystemExit('quick favourite anchor missing')
s=s.replace(oldq,newq)
oldh="document.querySelectorAll('.favQuickUse').forEach(b=>b.onclick=()=>openSavedFood(visible[Number(b.dataset.i)]));"
s=s.replace(oldh,oldh+"document.querySelectorAll('.favQuickRename').forEach(b=>b.onclick=async()=>{await renameFavourite(visible[Number(b.dataset.i)]);renderLibrary()});")
oldlib='<button class="${f.favourite?\'fav\':\'secondary\'} libFav" data-i="${i}" type="button">${f.favourite?\'★ Favourite\':\'☆ Favourite\'}</button><button class="secondary libUse" data-i="${i}" type="button">Use</button>'
newlib=oldlib+'${f.favourite?`<button class="secondary libRename" data-i="${i}" type="button">Rename</button>`:\'\'}'
if oldlib not in s: raise SystemExit('library favourite anchor missing')
s=s.replace(oldlib,newlib)
oldlh="document.querySelectorAll('.libUse').forEach(b=>b.onclick=()=>openSavedFood(list[Number(b.dataset.i)]));document.querySelectorAll('.libFav')"
s=s.replace(oldlh,"document.querySelectorAll('.libUse').forEach(b=>b.onclick=()=>openSavedFood(list[Number(b.dataset.i)]));document.querySelectorAll('.libRename').forEach(b=>b.onclick=async()=>{await renameFavourite(list[Number(b.dataset.i)]);renderLibrary()});document.querySelectorAll('.libFav')")

# Quick context note UI. Stored in existing cloud log, explicitly tagged and excluded from ICR intelligence.
anchor='<section class="card"><div class="reviewHead"><div><h2 style="margin:0">Unified meal log</h2>'
panel='''<section class="card"><div class="reviewHead"><div><h2 style="margin:0">Quick context note</h2><div class="hint">Log food or missed insulin you did not track properly, so later CGM rises have context. These entries are excluded from meal/ICR evidence.</div></div><span class="pill">CONTEXT ONLY</span></div><div class="grid" style="margin-top:12px"><div><label for="contextType">What happened?</label><select id="contextType"><option>Untracked food</option><option>Missed insulin</option><option>Untracked food + missed insulin</option><option>Other context</option></select></div><div><label for="contextCarbs">Approx carbs if known (g)</label><input id="contextCarbs" type="number" min="0" step="0.1" placeholder="Optional"></div><div class="full"><label for="contextNote">Short note</label><textarea id="contextNote" rows="2" placeholder="e.g. Ate biscuits and did not log them or take insulin"></textarea></div></div><div class="actions"><button id="saveContextNote" class="secondary" type="button">Save context note</button></div><div class="sectionNote">No insulin dose is calculated from this. It is a review marker only and is clearly labelled in the CSV export.</div></section>\n'''
if anchor not in s: raise SystemExit('unified log anchor missing')
s=s.replace(anchor,panel+anchor,1)

# Context helpers inserted before normal meal rendering.
anchor2='function mergedMeals(){const m=new Map();cloudRows.map(r=>normMeal(r,\'cloud\')).forEach(r=>m.set(r.client_id,r));read(MEAL_QUEUE).map(r=>normMeal(r,\'queued\')).forEach(r=>{if(!m.has(r.client_id))m.set(r.client_id,r)});return [...m.values()].sort((a,b)=>new Date(b.timestamp)-new Date(a.timestamp))}'
helpers="""function isContextEvent(r){return r?.meal_type==='Context event'||String(r?.notes||'').includes('[CONTEXT_EVENT]')}\nfunction contextLabel(r){const m=String(r?.notes||'').match(/\\[Context type: ([^\\]]+)\\]/);return m?m[1]:'Context note'}\nasync function saveContextEvent(){const type=$('contextType').value,note=$('contextNote').value.trim(),raw=$('contextCarbs').value.trim();if(!note)return alert('Add a short note about what happened.');const carbs=raw===''?0:Number(raw);if(!Number.isFinite(carbs)||carbs<0)return alert('Approx carbs must be a valid number or left blank.');let bg=0,trend='Not recorded';if(latestCgm&&readingAgeMinutes(latestCgm)<=15){bg=Number((Number(latestCgm.sgv)/18).toFixed(1));trend=mapNightscoutTrend(latestCgm.direction)||latestCgm.direction||'Not recorded'}const missed=type.includes('Missed insulin')||type.includes('missed insulin');const r={client_id:uid(),timestamp:new Date().toISOString(),meal_name:'Context: '+type,meal_type:'Context event',fat_level:'Unknown / not entered',fat_grams:null,carbs, bg, cgm_trend:trend,icr:15,target:8,calculated_dose:0,actual_insulin:missed?0:null,bolus_timing:'Context only - excluded from ICR analysis',notes:`[CONTEXT_EVENT] [Context type: ${type}] [Approx carbs: ${raw===''?'unknown':carbs+'g'}] ${note}`};const q=read(MEAL_QUEUE);q.unshift(r);write(MEAL_QUEUE,q);renderMeals();if(session&&navigator.onLine&&await pushMeal(r)){cloudRows=[r,...cloudRows.filter(x=>(x.client_id||x.clientId)!==r.client_id)];const refreshed=await fetchMeals(),confirmed=refreshed&&cloudRows.some(x=>(x.client_id||x.clientId)===r.client_id);if(confirmed){write(MEAL_QUEUE,read(MEAL_QUEUE).filter(x=>(x.client_id||x.clientId)!==r.client_id));renderMeals();setNotice('Context note saved to cloud. It will be visible in future CGM reviews.','good')}else setNotice('Context note saved; local safety copy kept until cloud confirmation.','warn')}else setNotice('Context note queued safely and will sync automatically.','warn');$('contextNote').value='';$('contextCarbs').value=''}\n"""
if anchor2 not in s: raise SystemExit('mergedMeals anchor missing')
s=s.replace(anchor2,anchor2+'\n'+helpers,1)

# Do not let context notes become meal evidence or meal markers in Live Intelligence.
s=s.replace("const meal=mergedMeals()[0];$('intelLastMeal').textContent=meal?", "const meal=mergedMeals().find(m=>!isContextEvent(m));$('intelLastMeal').textContent=meal?")
s=s.replace("intelligenceOutcomes=mergedMeals().filter(m=>new Date(m.timestamp).getTime()>=oldest-15*60000", "intelligenceOutcomes=mergedMeals().filter(m=>!isContextEvent(m)).filter(m=>new Date(m.timestamp).getTime()>=oldest-15*60000")
s=s.replace("meals=mergedMeals().filter(m=>new Date(m.timestamp).getTime()>=cutoff)", "meals=mergedMeals().filter(m=>!isContextEvent(m)).filter(m=>new Date(m.timestamp).getTime()>=cutoff)")

# Render context rows clearly and exclude them from average meal carbs.
oldrender="function renderMeals(){const rows=mergedMeals();$('statMeals').textContent=rows.length;$('statCloud').textContent=rows.filter(r=>r.source==='cloud').length;$('statLocal').textContent=rows.filter(r=>r.source==='queued').length;$('statCarbs').textContent=rows.length?(rows.reduce((a,r)=>a+r.carbs,0)/rows.length).toFixed(1)+' g':'-';$('logBody').innerHTML=rows.map(r=>`<tr><td>${new Date(r.timestamp).toLocaleString()}</td><td class=\"${r.source==='cloud'?'cloud':'local'}\">${r.source==='cloud'?'Cloud':'Queued'}</td><td>${esc(r.meal_name||'-')}</td><td>${esc(r.meal_type)}</td><td>${r.fat_grams!=null?esc(r.fat_grams+' g'):esc(r.fat_level)}</td><td>${r.carbs} g</td><td>${r.bg.toFixed(1)}</td><td>${esc(r.cgm_trend||'Not recorded')}</td><td>1:${r.icr}</td><td>${r.calculated_dose.toFixed(2)} U</td><td>${r.actual_insulin==null?'-':r.actual_insulin.toFixed(2)+' U'}</td><td>${esc(r.bolus_timing)}</td><td>${esc(cleanTrendNotes(r.notes))}</td><td><button type=\"button\" class=\"danger mealDelete\" data-id=\"${esc(r.client_id)}\">Delete</button></td></tr>`).join('');document.querySelectorAll('.mealDelete').forEach(b=>b.onclick=()=>deleteMeal(b.dataset.id));updateQueueUI()}"
newrender="function renderMeals(){const rows=mergedMeals(),meals=rows.filter(r=>!isContextEvent(r));$('statMeals').textContent=rows.length;$('statCloud').textContent=rows.filter(r=>r.source==='cloud').length;$('statLocal').textContent=rows.filter(r=>r.source==='queued').length;$('statCarbs').textContent=meals.length?(meals.reduce((a,r)=>a+r.carbs,0)/meals.length).toFixed(1)+' g':'-';$('logBody').innerHTML=rows.map(r=>{const ctx=isContextEvent(r);return `<tr><td>${new Date(r.timestamp).toLocaleString()}</td><td class=\"${r.source==='cloud'?'cloud':'local'}\">${r.source==='cloud'?'Cloud':'Queued'}</td><td>${ctx?'📝 '+esc(contextLabel(r)):esc(r.meal_name||'-')}</td><td>${ctx?'Context only':esc(r.meal_type)}</td><td>${ctx?'-':(r.fat_grams!=null?esc(r.fat_grams+' g'):esc(r.fat_level))}</td><td>${ctx?(r.carbs?('~'+r.carbs+' g'):'Unknown'):r.carbs+' g'}</td><td>${ctx?(r.bg?r.bg.toFixed(1):'-'):r.bg.toFixed(1)}</td><td>${esc(r.cgm_trend||'Not recorded')}</td><td>${ctx?'-':'1:'+r.icr}</td><td>${ctx?'-':r.calculated_dose.toFixed(2)+' U'}</td><td>${ctx?(r.actual_insulin===0?'0 U / missed':'-'):(r.actual_insulin==null?'-':r.actual_insulin.toFixed(2)+' U')}</td><td>${ctx?'Excluded from ICR':esc(r.bolus_timing)}</td><td>${esc(cleanTrendNotes(r.notes))}</td><td><button type=\"button\" class=\"danger mealDelete\" data-id=\"${esc(r.client_id)}\">Delete</button></td></tr>`}).join('');document.querySelectorAll('.mealDelete').forEach(b=>b.onclick=()=>deleteMeal(b.dataset.id));updateQueueUI()}"
if oldrender not in s: raise SystemExit('renderMeals anchor missing')
s=s.replace(oldrender,newrender,1)

# Add explicit event_type field to CSV while preserving existing columns for full CGM review compatibility.
oldh="['timestamp','meal_description','meal_type','fat_level','fat_grams','carbs_g','starting_glucose_mmol_l','cgm_trend','icr_denominator','calculated_meal_dose_u','actual_insulin_u','dose_difference_u','bolus_timing','target_glucose_mmol_l','notes']"
newh="['timestamp','event_type','meal_description','meal_type','fat_level','fat_grams','carbs_g','starting_glucose_mmol_l','cgm_trend','icr_denominator','calculated_meal_dose_u','actual_insulin_u','dose_difference_u','bolus_timing','target_glucose_mmol_l','notes']"
if oldh not in s: raise SystemExit('csv header anchor missing')
s=s.replace(oldh,newh,1)
oldrow="[r.timestamp,r.meal_name,r.meal_type,r.fat_level,r.fat_grams??'',r.carbs,r.bg,r.cgm_trend||trendFromNotes(r.notes),r.icr,r.calculated_dose,r.actual_insulin??'',r.actual_insulin==null?'':(r.actual_insulin-r.calculated_dose).toFixed(2),r.bolus_timing,r.target,r.notes]"
newrow="[r.timestamp,isContextEvent(r)?'context':'meal',r.meal_name,r.meal_type,r.fat_level,r.fat_grams??'',r.carbs,r.bg||'',r.cgm_trend||trendFromNotes(r.notes),isContextEvent(r)?'':r.icr,isContextEvent(r)?'':r.calculated_dose,r.actual_insulin??'',isContextEvent(r)?'':(r.actual_insulin==null?'':(r.actual_insulin-r.calculated_dose).toFixed(2)),r.bolus_timing,r.target,r.notes]"
if oldrow not in s: raise SystemExit('csv row anchor missing')
s=s.replace(oldrow,newrow,1)

# Button wiring.
wire="$('mealForm').addEventListener('submit',saveMeal);"
if wire not in s: raise SystemExit('mealForm wiring anchor missing')
s=s.replace(wire,wire+"$('saveContextNote').onclick=saveContextEvent;",1)

p.write_text(s)

c=Path('CHANGELOG.md')
cs=c.read_text()
entry='''# v2.8.5 - Favourite rename + quick context notes\n\n- Added Rename controls to favourite quick-access cards and favourite items in My food library.\n- Added Quick context note for untracked food, missed insulin, both, or other context.\n- Context notes can include optional approximate carbs and a plain-language description.\n- Context notes sync through the existing meal log and are tagged `[CONTEXT_EVENT]`.\n- Added `event_type` to CSV export so context rows are easy to identify during CGM review.\n- Context events are excluded from Live Intelligence meal outcomes, meal memory, ICR evidence and meal markers.\n- No correction-dose logic or insulin recommendation behaviour changed.\n\n'''
if not cs.startswith('# v2.8.5 - Favourite rename + quick context notes'):
    c.write_text(entry+cs)

b=Path('PROJECT_BRAIN.md')
bs=b.read_text()
brain='''\n\n## v2.8.5 - Favourite rename + quick context notes (8 Sep 2026)\n- Favourite foods can be renamed from quick favourites or My food library without changing nutrition, portion or usage history.\n- Quick context notes capture untracked food, missed insulin, both, or other confounders without pretending they are normal meal/ICR tests.\n- Context rows are stored in the existing meal_entries sync path with `meal_type=Context event` and `[CONTEXT_EVENT]` in notes.\n- CSV export now has an `event_type` column (`meal` or `context`).\n- Context rows are excluded from Live Intelligence meal outcomes, meal memory and ICR evidence.\n- Future 3-file CGM reviews should use context rows to explain otherwise-unmatched glucose rises and should never treat them as clean ICR evidence.\n- No dosing logic changed.\n'''
if '## v2.8.5 - Favourite rename + quick context notes' not in bs:
    b.write_text(bs.rstrip()+brain+'\n')
