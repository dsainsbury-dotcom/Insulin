from pathlib import Path
p=Path('index.html')
s=p.read_text().replace('v2.9.9','v2.10.0')

s=s.replace('Cloud meals plus any offline queued entries. Use Delete to remove an incorrect entry.','Cloud meals plus any offline queued entries. Use Edit to correct a meal or Delete to remove an incorrect entry.',1)
old='<button type="button" class="danger mealDelete" data-id="${esc(r.client_id)}">Delete</button>'
new='<button type="button" class="secondary mealEdit" data-id="${esc(r.client_id)}">Edit</button> <button type="button" class="danger mealDelete" data-id="${esc(r.client_id)}">Delete</button>'
if old not in s: raise SystemExit('delete action markup not found')
s=s.replace(old,new,1)
old="}).join('');document.querySelectorAll('.mealDelete').forEach(b=>b.onclick=()=>deleteMeal(b.dataset.id));updateQueueUI()}"
new="}).join('');document.querySelectorAll('.mealEdit').forEach(b=>b.onclick=()=>editMeal(b.dataset.id));document.querySelectorAll('.mealDelete').forEach(b=>b.onclick=()=>deleteMeal(b.dataset.id));updateQueueUI()}"
if old not in s: raise SystemExit('render action bindings not found')
s=s.replace(old,new,1)
anchor='async function deleteMeal(clientId){'
if anchor not in s: raise SystemExit('deleteMeal anchor not found')
edit=r'''async function editMeal(clientId){
  const row=mergedMeals().find(r=>r.client_id===clientId);if(!row)return;
  if(isContextEvent(row))return setNotice('Context-only entries are not editable yet.','warn');
  const mealName=prompt('Meal / food description',row.meal_name||'');if(mealName===null)return;
  const cleanName=mealName.trim();if(!cleanName)return alert('Meal name cannot be blank.');
  const carbsRaw=prompt('Carbohydrate (g)',String(row.carbs??''));if(carbsRaw===null)return;const carbs=Number(carbsRaw);if(!Number.isFinite(carbs)||carbs<0)return alert('Carbohydrate must be a valid number.');
  const fatRaw=prompt('Fat grams (leave blank if unknown)',row.fat_grams==null?'':String(row.fat_grams));if(fatRaw===null)return;const fat=fatRaw.trim()===''?null:Number(fatRaw);if(fat!==null&&(!Number.isFinite(fat)||fat<0))return alert('Fat must be a valid number or blank.');
  const insulinRaw=prompt('Insulin actually taken (units, leave blank if unknown)',row.actual_insulin==null?'':String(row.actual_insulin));if(insulinRaw===null)return;const insulin=insulinRaw.trim()===''?null:Number(insulinRaw);if(insulin!==null&&(!Number.isFinite(insulin)||insulin<0))return alert('Insulin must be a valid number or blank.');
  const updated={...row,meal_name:cleanName,carbs,fat_grams:fat,actual_insulin:insulin,meal_type:inferMealType(cleanName,carbs,fat)};
  if(row.source==='queued'){
    const q=read(MEAL_QUEUE).map(x=>(x.client_id||x.clientId)===clientId?{...x,meal_name:updated.meal_name,mealName:updated.meal_name,carbs:updated.carbs,fat_grams:updated.fat_grams,fatGrams:updated.fat_grams,actual_insulin:updated.actual_insulin,actualInsulin:updated.actual_insulin,meal_type:updated.meal_type,mealType:updated.meal_type}:x);write(MEAL_QUEUE,q);renderMeals();setNotice('Queued meal updated.','good');return;
  }
  if(!session)return setNotice('Sign in before editing a cloud meal.','bad');
  if(!navigator.onLine)return setNotice('Reconnect before editing a cloud meal so the correction can be saved safely.','warn');
  const patch={meal_name:updated.meal_name,meal_type:updated.meal_type,carbs:updated.carbs,fat_grams:updated.fat_grams,actual_insulin:updated.actual_insulin};
  const {error}=await sb.from('meal_entries').update(patch).eq('user_id',session.user.id).eq('client_id',clientId);
  if(error){console.error('meal edit',error);setNotice('Edit failed: '+error.message,'bad');return}
  cloudRows=cloudRows.map(x=>(x.client_id||x.clientId)===clientId?{...x,...patch}:x);renderMeals();setNotice('Meal updated in cloud. Refresh Intelligence to rebuild its CGM outcome and meal memory.','good');await fetchMeals();
}
'''
s=s.replace(anchor,edit+anchor,1)
p.write_text(s)
assert 'v2.10.0' in s
assert 'class="secondary mealEdit"' in s
assert 'async function editMeal(clientId)' in s
assert ".update(patch).eq('user_id',session.user.id).eq('client_id',clientId)" in s
print('v2.10.0 meal editing patch OK')
