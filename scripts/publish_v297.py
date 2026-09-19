from pathlib import Path

p=Path('index.html')
s=p.read_text()

# Release version
s=s.replace('v2.9.6','v2.9.7')

# BUG 1: fat fields must remain visible on the main meal screen.
old="['fatGrams','fatLevel','icr','bolusTiming','target','notes'].forEach(id=>{const el=$(id);if(el&&el.parentElement)advanced.appendChild(el.parentElement)});"
new="['icr','bolusTiming','target','notes'].forEach(id=>{const el=$(id);if(el&&el.parentElement)advanced.appendChild(el.parentElement)});"
if old not in s:
    raise SystemExit('compact Meal details field list not found')
s=s.replace(old,new,1)
s=s.replace("<span class=\"compactChevron\">Fat, ICR, timing, target & notes</span>","<span class=\"compactChevron\">ICR, timing, target & notes</span>",1)
s=s.replace("?'Fat, ICR, timing, target & notes':'Hide details'","?'ICR, timing, target & notes':'Hide details'",1)

# BUG 2: refreshIntelligence calls renderMealMemory() without an argument.
# Make the renderer use the already-calculated global intelligenceOutcomes by default.
old_sig='function renderMealMemory(outcomes){\n  const el=document.getElementById(\'mealMemory\'); if(!el) return;\n  const groups={};\n  (outcomes||[]).forEach'
new_sig='function renderMealMemory(outcomes=intelligenceOutcomes){\n  const el=document.getElementById(\'mealMemory\'); if(!el) return;\n  const groups={};\n  (outcomes||[]).forEach'
if old_sig not in s:
    raise SystemExit('meal memory renderer signature not found')
s=s.replace(old_sig,new_sig,1)

# Never allow a silent blank memory box, even if a future render problem occurs.
old_call='calculateOutcomes();renderRightNow();renderOutcomeCards();renderMealMemory();renderPatterns();renderIcrEvidence();renderEvents();renderLearned();'
new_call="calculateOutcomes();renderRightNow();renderOutcomeCards();try{renderMealMemory(intelligenceOutcomes)}catch(memoryError){console.error('meal memory render',memoryError);$('mealMemory').innerHTML='<div class=\"sectionNote\">Meal memory could not be rendered. The rest of Live Intelligence is still available.</div>'}renderPatterns();renderIcrEvidence();renderEvents();renderLearned();"
if old_call not in s:
    raise SystemExit('refresh intelligence render chain not found')
s=s.replace(old_call,new_call,1)

p.write_text(s)

# Release checks
assert 'v2.9.7' in s
assert "['icr','bolusTiming','target','notes'].forEach" in s
assert "['fatGrams','fatLevel','icr','bolusTiming','target','notes'].forEach" not in s
assert 'function renderMealMemory(outcomes=intelligenceOutcomes)' in s
assert 'renderMealMemory(intelligenceOutcomes)' in s
assert 'Meal memory could not be rendered' in s
assert 'Similar meal names are now grouped into families' in s
print('v2.9.7 combined repair patch OK')
