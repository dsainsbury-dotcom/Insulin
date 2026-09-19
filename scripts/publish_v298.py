from pathlib import Path
p=Path('index.html')
s=p.read_text().replace('v2.9.7','v2.9.8')

# Never ship an initially empty Personal meal memory container.
old='<div id="mealMemory" class="memoryGrid" style="margin-top:12px"></div>'
new='<div id="mealMemory" class="memoryGrid" style="margin-top:12px"><div class="sectionNote">Meal memory is waiting for Live Intelligence to match your logged meals with CGM outcomes.</div></div>'
if old not in s: raise SystemExit('mealMemory empty container not found')
s=s.replace(old,new,1)

# Keep Personal meal memory expanded in compact UI so its status/cards are actually visible.
old="const h=s.querySelector('h2');makeCollapsible(s,h?h.textContent.trim():'CGM detail',false);"
new="const h=s.querySelector('h2'),label=h?h.textContent.trim():'CGM detail';makeCollapsible(s,label,label==='Personal meal memory');"
if old not in s: raise SystemExit('compact intelligence collapse hook not found')
s=s.replace(old,new,1)

# Make no-family state diagnostic and explicit, rather than looking blank.
old="if(!fams.length){el.innerHTML='<div class=\"mini\">Meal memory is building. Similar meal names are now grouped into families, so they do not need to be exact text matches. A family appears after at least two matched CGM outcomes.</div>';return;}"
new="if(!fams.length){const matched=(outcomes||[]).length,unique=Object.keys(groups).length;el.innerHTML=`<div class=\"memoryCard\"><strong>Meal memory is building</strong><div class=\"mini\">${matched} matched meal outcome${matched===1?'':'s'} reached Personal Meal Memory, grouped into ${unique} meal famil${unique===1?'y':'ies'}. A family card appears after at least two matched outcomes from similar meals. Similar names are grouped automatically, so exact text matches are not required.</div></div>`;return;}"
if old not in s: raise SystemExit('meal memory empty-state branch not found')
s=s.replace(old,new,1)

# Add visible pipeline evidence above real family cards too.
old="el.innerHTML=fams.slice(0,8).map(([family,a])=>{"
new="const pipeline=`<div class=\"mini\" style=\"grid-column:1/-1\">Live pipeline: ${(outcomes||[]).length} matched meal outcomes · ${fams.length} repeated meal ${fams.length===1?'family':'families'} found.</div>`;el.innerHTML=pipeline+fams.slice(0,8).map(([family,a])=>{"
if old not in s: raise SystemExit('meal memory card render not found')
s=s.replace(old,new,1)

p.write_text(s)
assert 'v2.9.8' in s
assert 'Meal memory is waiting for Live Intelligence' in s
assert "label==='Personal meal memory'" in s
assert 'matched meal outcome${matched' in s
assert 'Live pipeline:' in s
print('v2.9.8 visible meal memory patch OK')
