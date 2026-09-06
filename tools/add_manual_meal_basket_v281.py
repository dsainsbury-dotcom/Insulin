from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Visible version bump only. Restaurant dataset remains v2.8.0 because its data file is unchanged.
s = s.replace('<title>ICR Meal Dashboard v2.8.0</title>', '<title>ICR Meal Dashboard v2.8.1</title>')
s = s.replace('ICR Meal Dashboard <small style="font-size:.48em;color:#0b5cab">v2.8.0</small>', 'ICR Meal Dashboard <small style="font-size:.48em;color:#0b5cab">v2.8.1</small>')
s = s.replace('<div class="badge">v2.8.0 LIVE</div>', '<div class="badge">v2.8.1 LIVE</div>')

old = '<section class="card"><h2>Add meal</h2><form id="mealForm"><div class="grid">'
new = '<section class="card"><h2>Add meal</h2><div class="actions" style="margin-top:-4px;margin-bottom:12px"><button id="startManualBasket" class="secondary" type="button">Build multi-item meal</button></div><form id="mealForm"><div class="grid">'
assert old in s, 'Add meal header marker missing'
s = s.replace(old, new, 1)

old = '<div><label>Fat level if grams unknown</label><select id="fatLevel"><option>Unknown / not entered</option><option>Low</option><option>Medium</option><option>High</option><option>Very high</option></select></div>\n<div><label>Current glucose (mmol/L)</label>'
new = '''<div><label>Fat level if grams unknown</label><select id="fatLevel"><option>Unknown / not entered</option><option>Low</option><option>Medium</option><option>High</option><option>Very high</option></select></div>
<div id="manualBasketPanel" class="restaurantBasket hidden full"><div class="reviewHead"><div><strong>Manual meal basket</strong><div class="sectionNote">Build the whole meal item by item. No per-item insulin suggestion is shown while basket mode is active.</div></div><span id="manualBasketCount" class="pill">0 items</span></div><div class="sectionNote">Enter one food above, including its carbohydrate and fat if known, then tap Add current item. When the whole meal is in the basket, tap Use combined meal.</div><div class="actions"><button id="addManualBasketItem" class="primary" type="button">Add current item to basket</button></div><div id="manualBasketItems"></div><div id="manualBasketTotals" class="basketTotals"></div><div class="basketActions"><button id="useManualBasket" class="primary" type="button">Use combined meal</button><button id="cancelManualBasket" class="secondary" type="button">Cancel basket</button></div><div class="sectionNote">Carbohydrates are totalled first. Your normal meal-dose calculation and whole-unit rounding are then applied once to the combined meal.</div></div>
<div><label>Current glucose (mmol/L)</label>'''
assert old in s, 'Fat/current glucose marker missing'
s = s.replace(old, new, 1)

old = '<button class="primary" type="submit">Save meal</button>'
new = '<button id="saveMealBtn" class="primary" type="submit">Save meal</button>'
assert old in s, 'Save button marker missing'
s = s.replace(old, new, 1)

old = 'const uid=()=>crypto.randomUUID?crypto.randomUUID():'
assert old in s, 'uid marker missing'
s = s.replace(old, "let manualBasketMode=false,manualBasket=[];\n" + old, 1)

insert_before = 'function syncFat(){'
assert insert_before in s, 'syncFat marker missing'
manual_funcs = r'''function setManualBasketMode(on){manualBasketMode=on;$('manualBasketPanel').classList.toggle('hidden',!on);$('startManualBasket').classList.toggle('hidden',on);$('saveMealBtn').disabled=on;if(on){actualEdited=false;$('actualInsulin').value=''}updateDose()}
function startManualBasketMode(){manualBasket=[];renderManualBasket();setManualBasketMode(true);setNotice('Manual meal basket started. Add every part of the meal, then calculate once from the combined carbohydrate total.','good')}
function manualBasketTotals(){return manualBasket.reduce((a,x)=>{a.carbs+=Number(x.carbs||0);if(x.fatGrams==null)a.unknownFat++;else a.fat+=Number(x.fatGrams||0);a.count++;return a},{carbs:0,fat:0,unknownFat:0,count:0})}
function renderManualBasket(){const t=manualBasketTotals();$('manualBasketCount').textContent=t.count+' item'+(t.count===1?'':'s');$('manualBasketItems').innerHTML=manualBasket.map((x,i)=>`<div class="basketRow"><div><strong>${esc(x.name)}</strong><div class="foodMeta">${Number(x.carbs).toFixed(1)}g carbs · ${x.fatGrams==null?esc(x.fatLevel||'fat not entered'):Number(x.fatGrams).toFixed(1)+'g fat'}</div></div><button class="danger manualBasketRemove" data-i="${i}" type="button">Remove</button></div>`).join('')||'<div class="sectionNote" style="margin-top:10px">Basket is empty.</div>';$('manualBasketTotals').innerHTML=`<div class="restaurantMacro"><span>Items</span><strong>${t.count}</strong></div><div class="restaurantMacro"><span>Carbs</span><strong>${t.carbs.toFixed(1)}g</strong></div><div class="restaurantMacro"><span>Known fat</span><strong>${t.fat.toFixed(1)}g</strong></div><div class="restaurantMacro"><span>Fat unknown</span><strong>${t.unknownFat}</strong></div>`;document.querySelectorAll('.manualBasketRemove').forEach(b=>b.onclick=()=>{manualBasket.splice(Number(b.dataset.i),1);renderManualBasket();updateDose()})}
function addManualBasketItem(){if(!manualBasketMode)return;const name=$('mealName').value.trim(),rawCarbs=$('carbs').value.trim(),rawFat=$('fatGrams').value.trim();if(!name)return alert('Enter a description for this food item.');if(rawCarbs==='')return alert('Enter the carbohydrate for this food item.');const carbs=Number(rawCarbs);if(!Number.isFinite(carbs)||carbs<0)return alert('Enter a valid carbohydrate amount.');const fatGrams=rawFat===''?null:Number(rawFat);if(fatGrams!=null&&(!Number.isFinite(fatGrams)||fatGrams<0))return alert('Enter a valid fat amount or leave it blank.');manualBasket.push({name,carbs,fatGrams,fatLevel:$('fatLevel').value,mealType:$('mealType').value});renderManualBasket();$('mealName').value='';$('carbs').value='';$('fatGrams').value='';$('fatLevel').value='Unknown / not entered';$('mealType').value='Balanced / mixed meal';syncFat();actualEdited=false;$('actualInsulin').value='';updateDose();setNotice(`${name} added to the manual meal basket.`,'good')}
function useManualBasket(){if(!manualBasket.length)return alert('Add at least one food item to the basket first.');const t=manualBasketTotals(),parts=manualBasket.map(x=>x.name),summary=manualBasket.map(x=>`${x.name} (${Number(x.carbs).toFixed(1)}g carbs${x.fatGrams==null?`; fat ${x.fatLevel||'not entered'}`:`; ${Number(x.fatGrams).toFixed(1)}g fat`})`);$('mealName').value=parts.join(' + ');$('carbs').value=Number(t.carbs.toFixed(1));if(t.unknownFat===0){$('fatGrams').value=Number(t.fat.toFixed(1));$('fatLevel').value='Unknown / not entered'}else{$('fatGrams').value='';$('fatLevel').value='Unknown / not entered'}$('mealType').value=inferMealType(parts.join(' '),t.carbs,t.unknownFat===0?t.fat:null);const existing=$('notes').value.trim(),tag=`Manual meal basket: ${summary.join(' + ')}`;$('notes').value=existing?`${existing} | ${tag}`:tag;manualBasket=[];manualBasketMode=false;renderManualBasket();$('manualBasketPanel').classList.add('hidden');$('startManualBasket').classList.remove('hidden');$('saveMealBtn').disabled=false;syncFat();actualEdited=false;updateDose();setNotice(`Combined manual meal ready: ${t.carbs.toFixed(1)}g carbs. The meal dose is calculated once from the combined total.`,'good')}
function cancelManualBasket(){manualBasket=[];manualBasketMode=false;renderManualBasket();$('manualBasketPanel').classList.add('hidden');$('startManualBasket').classList.remove('hidden');$('saveMealBtn').disabled=false;actualEdited=false;updateDose();setNotice('Manual meal basket cancelled.','warn')}
'''
s = s.replace(insert_before, manual_funcs + insert_before, 1)

old = 'function updateDose(){const c=Number($(\'carbs\').value),i=Number($(\'icr\').value||15);'
new = "function updateDose(){if(manualBasketMode){$('liveDose').textContent='Basket active';$('calc').textContent='Add all meal items to the basket, then tap Use combined meal. No per-item insulin suggestion is shown while basket mode is active.';if(!actualEdited)$('actualInsulin').value='';return}const c=Number($('carbs').value),i=Number($('icr').value||15);"
assert old in s, 'updateDose marker missing'
s = s.replace(old, new, 1)

old = 'async function saveMeal(e){e.preventDefault();'
new = "async function saveMeal(e){e.preventDefault();if(manualBasketMode)return alert('Finish or cancel the manual meal basket before saving the meal.');"
assert old in s, 'saveMeal marker missing'
s = s.replace(old, new, 1)

old = "$('mealForm').addEventListener('submit',saveMeal);"
new = "$('mealForm').addEventListener('submit',saveMeal);$('startManualBasket').onclick=startManualBasketMode;$('addManualBasketItem').onclick=addManualBasketItem;$('useManualBasket').onclick=useManualBasket;$('cancelManualBasket').onclick=cancelManualBasket;"
assert old in s, 'mealForm event marker missing'
s = s.replace(old, new, 1)

# Add release note before v2.8.0 history.
old = '<div class="versionGrid"><div class="versionItem"><strong>v2.8.0 - Expanded restaurant database + safe demo</strong>'
new = '<div class="versionGrid"><div class="versionItem"><strong>v2.8.1 - Manual multi-item meal basket</strong><ul><li>Added a manual meal basket so mixed meals can be built item by item before carbohydrate is totalled.</li><li>Suppresses per-item insulin suggestions while basket mode is active to reduce accidental dose stacking.</li><li>Combined carbohydrate is calculated first and the existing meal-dose calculation is applied once.</li><li>Known fat is totalled when available; unknown fat is kept explicitly unknown rather than invented.</li></ul></div><div class="versionItem"><strong>v2.8.0 - Expanded restaurant database + safe demo</strong>'
assert old in s, 'version history marker missing'
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
print('v2.8.1 manual meal basket patch applied')
