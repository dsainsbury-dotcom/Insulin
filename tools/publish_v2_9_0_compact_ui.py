from pathlib import Path

index_path = Path('index.html')
html = index_path.read_text(encoding='utf-8')

old_nav = '<div class="navTabs"><button class="viewBtn active" data-view="tracker">Meal Tracker</button><button class="viewBtn" data-view="intelligence">Live Intelligence</button><button class="viewBtn" data-view="progress">CGM Progress</button></div>'
new_nav = '<div class="navTabs compactNav" aria-label="Main navigation"><button class="compactNavBtn active" data-compact-view="tracker" type="button"><span>Meal</span></button><button class="compactNavBtn" data-compact-view="intelligence" type="button"><span>CGM</span></button><button class="compactNavBtn" data-compact-view="foods" type="button"><span>Foods</span></button><button class="compactNavBtn" data-compact-view="more" type="button"><span>More</span></button></div>'
assert old_nav in html, 'Expected v2.8.7 navigation not found'
html = html.replace(old_nav, new_nav, 1)

html = html.replace('<title>ICR Meal Dashboard v2.8.7</title>', '<title>ICR Meal Dashboard v2.9.0</title>', 1)
html = html.replace('>v2.8.7</small></h1>', '>v2.9.0</small></h1>', 1)
html = html.replace('<div class="badge">v2.8.7 LIVE</div>', '<div class="badge">v2.9.0 LIVE</div>', 1)
html = html.replace('Pre-filled by rounding the calculated meal dose up to the next whole unit. Change it to what was actually taken.', 'Pre-filled using nearest-whole-unit rounding: below 0.5 rounds down and 0.5 or above rounds up. Change it to what was actually taken.', 1)

compact_css = r'''
/* v2.9.0 compact app shell */
.compactNav{z-index:40}
.compactNavBtn{flex:1;border:1px solid var(--line);background:#fff;color:#344054;border-radius:12px;padding:10px 12px;font-weight:850;cursor:pointer}
.compactNavBtn.active{background:var(--blue);color:#fff;border-color:var(--blue)}
.compactStatusBar{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:0 0 12px}
.compactStatusCell{background:#fff;border:1px solid var(--line);border-radius:12px;padding:9px 10px;min-width:0}
.compactStatusCell span{display:block;font-size:.65rem;color:var(--muted);font-weight:750;text-transform:uppercase;letter-spacing:.03em}
.compactStatusCell strong{display:block;font-size:.9rem;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.compactPageIntro{padding:12px 14px;margin-bottom:10px}
.compactPageIntro h2{margin:0 0 3px;font-size:1.08rem}
.compactQuickActions{display:flex;gap:7px;flex-wrap:wrap;margin:0 0 10px}
.compactQuickActions button{flex:1;min-width:105px;padding:9px 10px}
.compactAdvancedToggle,.compactSectionToggle{width:100%;display:flex;align-items:center;justify-content:space-between;text-align:left;background:#f8fafc;color:#344054;border:1px solid var(--line);margin-top:10px}
.compactSectionToggle{margin:0;padding:10px 12px}
.compactCollapsible{padding:0;overflow:hidden}
.compactCollapsible>.compactBody{padding:12px 13px 13px}
.compactCollapsible.compactCollapsed>.compactBody{display:none}
.compactChevron{font-size:.8rem;color:var(--muted)}
.mealAdvanced{margin-top:10px;border-top:1px solid var(--line);padding-top:10px}
.cgmProgressDrawer{margin-top:10px}
.compactProgressToggle{margin-bottom:10px}
#tracker>.card,#foods>.card,#more>.card,#intelligence>.card{margin-bottom:10px}
@media(max-width:800px){
  .shell{padding:10px 10px 92px}
  .top{flex-direction:row;align-items:center;margin-bottom:6px;gap:8px}
  .top .logo{width:38px;height:38px;border-radius:11px;font-size:17px}
  .top h1{font-size:1.12rem}
  .top .sub{display:none}
  .top .badge{padding:6px 8px;font-size:.68rem}
  .navTabs.compactNav{position:fixed;left:8px;right:8px;bottom:8px;top:auto;margin:0;padding:6px;background:rgba(244,247,251,.96);border:1px solid var(--line);border-radius:16px;box-shadow:0 8px 28px #0002;backdrop-filter:blur(10px)}
  .compactNavBtn{border:0;background:transparent;padding:10px 6px;border-radius:11px;font-size:.78rem}
  .compactNavBtn.active{background:var(--blue);color:#fff}
  .compactStatusBar{grid-template-columns:repeat(2,1fr);gap:6px;margin-bottom:8px}
  .compactStatusCell{padding:7px 9px}
  .card{padding:12px;border-radius:14px;margin-bottom:9px}
  .grid{gap:8px}
  input,select,textarea{padding:10px 11px}
  .liveDose{padding:11px;margin-top:9px}
  .liveDose strong{font-size:1.65rem}
  .smartGrid{grid-template-columns:1fr 1fr;gap:7px}
  .smartAction{padding:10px}
  .smartAction span{display:none}
  .restaurantChains{grid-template-columns:repeat(2,1fr)}
  .compactQuickActions{position:sticky;top:0;z-index:12;background:var(--bg);padding:4px 0}
  .chartWrap{height:240px}
}
'''
assert '</style>' in html
html = html.replace('</style>', compact_css + '\n</style>', 1)

compact_js = r'''
<script>
(function(){
  function initCompactUi(){
    if(document.getElementById('foods')) return;
    const $=id=>document.getElementById(id);
    const tracker=$('tracker'), intelligence=$('intelligence'), progress=$('progress');
    const nav=document.querySelector('.compactNav');
    if(!tracker||!intelligence||!nav) return;

    const foods=document.createElement('div'); foods.id='foods'; foods.className='viewPane';
    const more=document.createElement('div'); more.id='more'; more.className='viewPane';
    tracker.insertAdjacentElement('afterend',foods); foods.insertAdjacentElement('afterend',more);

    const directSections=root=>Array.from(root.children).filter(el=>el.tagName==='SECTION'&&el.classList.contains('card'));
    const sectionByText=(root,text)=>directSections(root).find(s=>s.textContent.includes(text));
    const cloud=$('cloudCard');
    const smart=sectionByText(tracker,'Smart Food System');
    const night=$('nightscoutCard');
    const addMeal=sectionByText(tracker,'Add meal');
    const context=sectionByText(tracker,'Quick context note');
    const log=sectionByText(tracker,'Unified meal log');

    if(smart) foods.appendChild(smart);
    [cloud,night,context,log].forEach(s=>{if(s) more.appendChild(s)});

    const intro=(title,text)=>{const d=document.createElement('div');d.className='card compactPageIntro';d.innerHTML=`<h2>${title}</h2><div class="sectionNote">${text}</div>`;return d};
    foods.insertBefore(intro('Foods','Favourites, barcode and label scanning, manual nutrition, restaurant foods and your full saved library.'),foods.firstChild);
    more.insertBefore(intro('More','Cloud and Nightscout settings, context notes, meal history and backup/export tools.'),more.firstChild);

    const showView=(target,scrollTop=true)=>{
      document.querySelectorAll('.viewPane').forEach(p=>p.classList.remove('active'));
      const pane=$(target); if(pane) pane.classList.add('active');
      nav.querySelectorAll('.compactNavBtn').forEach(b=>b.classList.toggle('active',b.dataset.compactView===target));
      if(scrollTop) window.scrollTo({top:0,behavior:'auto'});
    };
    nav.querySelectorAll('.compactNavBtn').forEach(b=>b.addEventListener('click',()=>showView(b.dataset.compactView)));

    const expandSection=s=>{if(!s)return;s.classList.remove('compactCollapsed');const ch=s.querySelector(':scope > .compactSectionToggle .compactChevron');if(ch)ch.textContent='Hide'};
    const makeCollapsible=(section,label,open=false)=>{
      if(!section||section.dataset.compactReady)return;
      section.dataset.compactReady='1'; section.classList.add('compactCollapsible');
      const body=document.createElement('div'); body.className='compactBody';
      while(section.firstChild) body.appendChild(section.firstChild);
      const btn=document.createElement('button');btn.type='button';btn.className='compactSectionToggle';btn.innerHTML=`<strong>${label}</strong><span class="compactChevron">${open?'Hide':'Show'}</span>`;
      section.append(btn,body); if(!open)section.classList.add('compactCollapsed');
      btn.addEventListener('click',()=>{section.classList.toggle('compactCollapsed');btn.querySelector('.compactChevron').textContent=section.classList.contains('compactCollapsed')?'Show':'Hide'});
    };
    makeCollapsible(cloud,'Cloud & sign-in',false);
    makeCollapsible(night,'Nightscout connection',false);
    makeCollapsible(context,'Quick context note',false);
    makeCollapsible(log,'Meal log & CSV export',false);

    if(addMeal){
      const form=$('mealForm'), mainGrid=form?form.querySelector('.grid'):null;
      if(form&&mainGrid){
        const advanced=document.createElement('div');advanced.className='grid mealAdvanced hidden';advanced.id='mealAdvanced';
        ['fatGrams','fatLevel','icr','bolusTiming','target','notes'].forEach(id=>{const el=$(id);if(el&&el.parentElement)advanced.appendChild(el.parentElement)});
        const toggle=document.createElement('button');toggle.type='button';toggle.className='compactAdvancedToggle';toggle.innerHTML='<strong>Meal details</strong><span class="compactChevron">Fat, ICR, timing, target & notes</span>';
        mainGrid.insertAdjacentElement('afterend',toggle);toggle.insertAdjacentElement('afterend',advanced);
        toggle.addEventListener('click',()=>{advanced.classList.toggle('hidden');toggle.querySelector('.compactChevron').textContent=advanced.classList.contains('hidden')?'Fat, ICR, timing, target & notes':'Hide details'});
      }
      const quick=document.createElement('div');quick.className='compactQuickActions';quick.innerHTML='<button type="button" class="foodBtn" data-compact-go="foods">Choose / scan food</button><button type="button" class="secondary" data-compact-go="context">Context note</button><button type="button" class="secondary" data-compact-go="log">Meal log</button>';
      const h=addMeal.querySelector('h2'); if(h) h.insertAdjacentElement('afterend',quick); else addMeal.prepend(quick);
      quick.addEventListener('click',e=>{const b=e.target.closest('[data-compact-go]');if(!b)return;const dest=b.dataset.compactGo;if(dest==='foods')showView('foods');else{showView('more',false);const sec=dest==='context'?context:log;expandSection(sec);setTimeout(()=>sec&&sec.scrollIntoView({behavior:'smooth',block:'start'}),30)}});
    }

    if(progress){
      const toggleCard=document.createElement('section');toggleCard.className='card compactProgressToggle';
      const btn=document.createElement('button');btn.type='button';btn.className='compactAdvancedToggle';btn.style.marginTop='0';btn.innerHTML='<strong>CGM Progress & review history</strong><span class="compactChevron">Show</span>';
      toggleCard.appendChild(btn);
      const drawer=document.createElement('div');drawer.className='cgmProgressDrawer hidden';drawer.id='cgmProgressDrawer';
      while(progress.firstChild) drawer.appendChild(progress.firstChild);
      intelligence.append(toggleCard,drawer);
      btn.addEventListener('click',()=>{drawer.classList.toggle('hidden');btn.querySelector('.compactChevron').textContent=drawer.classList.contains('hidden')?'Show':'Hide'});
    }

    directSections(intelligence).forEach((s,i)=>{
      const txt=s.textContent;
      if(i>2 && !txt.includes('CGM Progress & review history')){
        const h=s.querySelector('h2');makeCollapsible(s,h?h.textContent.trim():'CGM detail',false);
      }
    });

    const status=document.createElement('div');status.className='compactStatusBar';status.innerHTML='<div class="compactStatusCell"><span>Glucose</span><strong id="compactGlucose">--</strong></div><div class="compactStatusCell"><span>Trend</span><strong id="compactTrend">--</strong></div><div class="compactStatusCell"><span>ICR</span><strong id="compactIcr">1:15</strong></div><div class="compactStatusCell"><span>Cloud</span><strong id="compactCloud">Checking</strong></div>';
    nav.insertAdjacentElement('afterend',status);
    const syncStatus=()=>{
      const live=$('liveCgmValue')?.textContent?.trim(); const bg=$('bg')?.value;
      $('compactGlucose').textContent=(live&& !live.startsWith('--'))?live:(bg?bg+' mmol/L':'--');
      $('compactTrend').textContent=$('cgmTrend')?.value||'--';
      $('compactIcr').textContent='1:'+($('icr')?.value||'15');
      $('compactCloud').textContent=$('statusText')?.textContent||'Checking';
    };
    ['bg','cgmTrend','icr'].forEach(id=>$(id)?.addEventListener('input',syncStatus));
    ['liveCgmValue','statusText'].forEach(id=>{const el=$(id);if(el)new MutationObserver(syncStatus).observe(el,{childList:true,subtree:true,characterData:true})});
    syncStatus();
    showView('tracker',false);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initCompactUi);else initCompactUi();
})();
</script>
'''
assert '</body>' in html
html = html.replace('</body>', compact_js + '\n</body>', 1)
index_path.write_text(html, encoding='utf-8')

# Changelog
changelog = Path('CHANGELOG.md')
cl = changelog.read_text(encoding='utf-8')
entry = '''# v2.9.0 - Compact mobile-first navigation - 13 Sep 2026\n\n- Reorganised the existing app into four main destinations: Meal, CGM, Foods and More.\n- Kept every existing feature while reducing vertical scrolling and making everyday meal logging the default focus.\n- Moved Smart Food, favourites, barcode/OCR/manual nutrition, restaurant foods and the full food library into Foods.\n- Consolidated Live Intelligence and CGM Progress under CGM, with detailed evidence/history collapsed until requested.\n- Moved cloud sign-in, Nightscout settings, context notes, meal log and CSV export into More with compact collapsible sections.\n- Added a compact status strip for glucose, trend, ICR and cloud state.\n- Added a Meal details expander for fat, ICR, bolus timing, target and notes while keeping the core logging fields immediately visible.\n- Added quick Meal shortcuts to Foods, context notes and the meal log.\n- Corrected the insulin-field helper text so it describes the v2.8.7 nearest-whole-unit rounding rule rather than the old always-round-up behaviour.\n- No Supabase schema, Nightscout data, ICR, rounding, correction-dose, food data or CGM analysis logic changed.\n- Rollback branch: `backup/pre-v2.9.0-compact-ui-2026-09-13`.\n\n'''
if not cl.startswith('# v2.9.0'):
    changelog.write_text(entry + cl, encoding='utf-8')

# Project brain
brain = Path('PROJECT_BRAIN.md')
b = brain.read_text(encoding='utf-8')
b = b.replace('- Current production release: v2.8.7.', '- Current production release: v2.9.0.', 1)
ui_note = '''\n## v2.9.0 compact navigation - 13 Sep 2026\n- Production UI is organised into four main destinations: Meal, CGM, Foods and More.\n- This is a presentation/navigation release. Existing clinical calculations, v2.8.7 nearest-whole-unit rounding, Supabase data model, Nightscout behaviour, food data and CGM analysis logic are preserved.\n- Meal is the everyday default. Foods holds food capture/library tools. CGM combines live intelligence with expandable progress/review history. More holds lower-frequency settings, context, history and export.\n- On mobile the main navigation is fixed at the bottom to reduce long-scroll navigation.\n- Future UI additions should fit this information hierarchy rather than adding another long permanent section to Meal.\n'''
marker='\n## Current verified CGM baseline\n'
if '## v2.9.0 compact navigation' not in b:
    assert marker in b
    b=b.replace(marker,ui_note+marker,1)
brain.write_text(b,encoding='utf-8')

# README top-level production info (the file had become stale).
readme=Path('README.md')
r=readme.read_text(encoding='utf-8')
r=r.replace('# ICR Meal Dashboard v2.5.0','# ICR Meal Dashboard v2.9.0',1)
r=r.replace('- v2.4.8 is the current production version on the repository root.','- v2.9.0 is the current production version on the repository root.',1)
r=r.replace('- Meal Tracker remains the default view; CGM Progress is a separate tab.','- The app uses four compact main destinations: Meal, CGM, Foods and More. Meal remains the default view.',1)
readme.write_text(r,encoding='utf-8')

print('Prepared v2.9.0 compact UI release')
