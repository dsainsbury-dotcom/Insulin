from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

repls=[
('ICR Meal Dashboard v2.9.0','ICR Meal Dashboard v2.9.1'),
('v2.9.0</small>','v2.9.1</small>'),
('v2.9.0 LIVE','v2.9.1 LIVE'),
('intelligenceOutcomes=[],intelligenceHours=24,','intelligenceOutcomes=[],intelligenceHours=168,'),
("nav.querySelectorAll('.compactNavBtn').forEach(b=>b.addEventListener('click',()=>showView(b.dataset.compactView)));", "nav.querySelectorAll('.compactNavBtn').forEach(b=>b.addEventListener('click',()=>{const target=b.dataset.compactView;showView(target);if(target==='intelligence'&&typeof refreshIntelligence==='function')refreshIntelligence();}));"),
]
for old,new in repls:
    if old not in s:
        raise SystemExit(f'Missing expected text: {old[:100]}')
    s=s.replace(old,new,1)

# Make the intelligence history label reflect the seven-day evidence window.
s=s.replace('<strong id="historyHours">24h</strong>','<strong id="historyHours">168h</strong>',1)

# Add release note at the top of version history.
needle='<div class="versionGrid">'
note='''<div class="versionItem"><strong>v2.9.1 - Live Intelligence population fix</strong><ul><li>Fixed the compact CGM tab so opening it now triggers a Live Intelligence refresh.</li><li>Expanded Nightscout evidence history from 24 hours to 7 days so meal outcomes, repeated-meal memory and pattern cards have enough history to populate.</li><li>Context-only events remain excluded from meal and ICR evidence.</li><li>No insulin calculation, correction-dose or dosing recommendation logic changed.</li></ul></div>'''
if needle not in s: raise SystemExit('Version history anchor missing')
s=s.replace(needle,needle+note,1)

p.write_text(s,encoding='utf-8')
print('v2.9.1 intelligence fix applied')
