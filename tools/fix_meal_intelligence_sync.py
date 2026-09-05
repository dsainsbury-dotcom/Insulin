from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = "if(session&&navigator.onLine&&await pushMeal(r)){write(MEAL_QUEUE,read(MEAL_QUEUE).filter(x=>(x.client_id||x.clientId)!==r.client_id));await fetchMeals();setNotice('Meal saved to cloud.','good')}else setNotice('Meal queued safely and will sync automatically.','warn');"
new = "if(session&&navigator.onLine&&await pushMeal(r)){cloudRows=[r,...cloudRows.filter(x=>(x.client_id||x.clientId)!==r.client_id)];renderMeals();const refreshed=await fetchMeals(),confirmed=refreshed&&cloudRows.some(x=>(x.client_id||x.clientId)===r.client_id);if(confirmed){write(MEAL_QUEUE,read(MEAL_QUEUE).filter(x=>(x.client_id||x.clientId)!==r.client_id));renderMeals();setNotice('Meal saved to cloud and confirmed.','good')}else{setNotice('Meal saved, but the local safety copy is being kept until cloud refresh confirms it.','warn')}}else setNotice('Meal queued safely and will sync automatically.','warn');"
assert old in s, 'save confirmation block not found'
s = s.replace(old, new, 1)

old = "try{$('intelState').textContent='Reading Nightscout history and matching meals...';$('intelState').className='notice warn';await fetchCgmHistory(intelligenceHours);"
new = "try{$('intelState').textContent='Refreshing meals and Nightscout history...';$('intelState').className='notice warn';if(session)await fetchMeals();await fetchCgmHistory(intelligenceHours);"
assert old in s, 'intelligence refresh block not found'
s = s.replace(old, new, 1)

old = "$('intelState').textContent=`Live intelligence updated · ${cgmHistory.length} CGM readings analysed · ${intelligenceOutcomes.length} meal outcomes matched.`;"
new = "$('intelState').textContent=`Live intelligence updated · ${cgmHistory.length} CGM readings analysed · ${mergedMeals().length} logged meals visible · ${intelligenceOutcomes.length} meal outcomes matched.`;"
assert old in s, 'intelligence status block not found'
s = s.replace(old, new, 1)

old = "$('outcomeCards').innerHTML=rows.length?rows.map(o=>`<div class=\"outcomeCard\"><strong>${esc(o.meal.meal_name||'Meal')}</strong>"
if old not in s:
    # no functional change required here; current messaging remains valid until enough CGM history exists
    pass

p.write_text(s, encoding='utf-8')
print('meal intelligence sync reliability patch applied')
