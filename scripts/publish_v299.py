from pathlib import Path
p=Path('index.html')
s=p.read_text().replace('v2.9.8','v2.9.9')
start=s.find('function renderMealMemory(')
if start<0: raise SystemExit('renderMealMemory not found')
end=s.find('\nfunction renderPatterns()',start)
if end<0: raise SystemExit('renderPatterns boundary not found')
new=r'''function renderMealMemory(outcomes=intelligenceOutcomes){
  const el=$('mealMemory'); if(!el)return;
  const rows=(outcomes||[]).slice().sort((a,b)=>new Date(b.meal.timestamp)-new Date(a.meal.timestamp));
  if(!rows.length){el.innerHTML='<div class="memoryCard"><strong>No matched meal history yet</strong><div class="mini">Personal Meal Memory will build automatically as logged meals collect enough CGM follow-up.</div></div>';return;}
  const groups={};
  rows.forEach(o=>{const name=String(o.meal?.meal_name||'Meal').trim();const key=mealFamilyName(name);(groups[key]||(groups[key]=[])).push(o)});
  const cards=Object.entries(groups).sort((a,b)=>new Date(b[1][0].meal.timestamp)-new Date(a[1][0].meal.timestamp));
  const f=n=>Number.isFinite(Number(n))?Number(n):null;
  const mean=a=>{const z=a.filter(v=>v!=null);return z.length?z.reduce((x,y)=>x+y,0)/z.length:null};
  const fmt=v=>v==null?'-':v.toFixed(1);
  el.innerHTML=`<div class="mini" style="grid-column:1/-1">${rows.length} matched meal outcome${rows.length===1?'':'s'} available. Every matched meal is shown now; repeated similar meals are combined as evidence grows.</div>`+cards.slice(0,12).map(([family,a])=>{
    const latest=a[0], names=[...new Set(a.map(o=>o.meal.meal_name||'Meal'))];
    const label=a.length>1?family.replace(/\b\w/g,c=>c.toUpperCase()):(latest.meal.meal_name||'Meal');
    const carbs=mean(a.map(o=>f(o.meal.carbs))),fat=mean(a.map(o=>f(o.meal.fat_grams))),ins=mean(a.map(o=>f(o.meal.actual_insulin));
    const startv=mean(a.map(o=>f(o.start))),peak=mean(a.map(o=>f(o.peak))),rise=mean(a.map(o=>f(o.rise))),peakMin=mean(a.map(o=>f(o.peakMin))),h2=mean(a.map(o=>f(o.h2))),h4=mean(a.map(o=>f(o.h4))),h6=mean(a.map(o=>f(o.h6)));
    const delayed=a.filter(o=>o.lateRise).length,lows=a.filter(o=>o.low).length,high=a.filter(o=>o.above10>=30).length;
    const confidence=a.length>=5?'stronger':a.length>=3?'developing':a.length===2?'early':'single outcome';
    let interpretation=a.length===1?'Early evidence only. One meal is not enough to establish your usual response.':`This is based on ${a.length} comparable outcomes. Confidence is ${confidence}.`;
    if(delayed)interpretation+=` Delayed rise seen in ${delayed}/${a.length}.`;
    if(high)interpretation+=` At least 30 minutes above 10 mmol/L in ${high}/${a.length}.`;
    if(lows)interpretation+=` Low seen in ${lows}/${a.length}.`;
    const dose=ins==null?'-':ins.toFixed(1)+'U', fatTxt=fat==null?'fat not logged':fat.toFixed(0)+'g fat';
    return `<div class="memoryCard"><strong>${esc(label)}</strong><div class="mini">${a.length} previous matched outcome${a.length===1?'':'s'} · ${carbs==null?'-':carbs.toFixed(0)+'g carbs'} · ${fatTxt} · ${dose}</div><div style="margin-top:8px"><b>Your response:</b> start ${fmt(startv)} → peak ${fmt(peak)} mmol/L ${rise==null?'':`(${rise>=0?'+':''}${rise.toFixed(1)})`}</div><div class="mini">Typical peak ${peakMin==null?'-':Math.round(peakMin)+' min'} · 2h ${fmt(h2)} · 4h ${fmt(h4)} · 6h ${fmt(h6)}</div><div class="mini" style="margin-top:7px"><b>${a.length===1?'What this means':'Pattern'}:</b> ${interpretation}</div>${names.length>1?`<div class="mini" style="margin-top:5px">Grouped names: ${names.map(esc).join(' · ')}</div>`:''}</div>`;
  }).join('');
}'''
# fix typo in generated JS expression before writing
new=new.replace("mean(a.map(o=>f(o.meal.actual_insulin));","mean(a.map(o=>f(o.meal.actual_insulin)))")
s=s[:start]+new+s[end:]
p.write_text(s)
assert 'v2.9.9' in s
assert 'Every matched meal is shown now' in s
assert 'Early evidence only' in s
assert 'Your response:' in s
print('v2.9.9 useful meal memory cards patch OK')
