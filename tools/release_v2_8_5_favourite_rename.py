from pathlib import Path

p=Path('index.html')
s=p.read_text()
s=s.replace('ICR Meal Dashboard v2.8.4','ICR Meal Dashboard v2.8.5')
s=s.replace('v2.8.4</small>','v2.8.5</small>')
s=s.replace('v2.8.4 LIVE','v2.8.5 LIVE')
old="async function toggleFavourite(f){f=normalizeFood(f);f.favourite=!f.favourite;if(session&&navigator.onLine&&foodCloudReady&&await upsertFood(f)){await fetchFoods();setNotice(f.favourite?'Added to favourites.':'Removed from favourites.','good');return}queueFood(f);foodRows=[f,...foodRows.filter(x=>x.client_id!==f.client_id)];write(FOOD_CACHE,foodRows);renderLibrary();setNotice(f.favourite?'Favourite queued and will sync automatically.':'Favourite change queued and will sync automatically.','warn')}"
new=old+"\nasync function renameFavourite(f){f=normalizeFood(f);if(!f.favourite)return;const next=prompt('Rename favourite',f.name);if(next===null)return;const name=next.trim();if(!name)return setNotice('Favourite name was not changed.','warn');if(name===f.name)return;f.name=name;f.updated_at=new Date().toISOString();if(session&&navigator.onLine&&foodCloudReady&&await upsertFood(f)){await fetchFoods();setNotice('Favourite renamed to '+name+'.','good');return}queueFood(f);foodRows=[f,...foodRows.filter(x=>x.client_id!==f.client_id)];write(FOOD_CACHE,foodRows);renderLibrary();setNotice('Favourite rename saved on this device and queued to sync automatically.','warn')}"
if old not in s: raise SystemExit('toggleFavourite anchor missing')
s=s.replace(old,new)
oldq="<button class=\"primary favQuickUse\" data-i=\"${i}\" type=\"button\">Use</button></div>"
newq="<div class=\"actions\" style=\"margin-top:8px\"><button class=\"primary favQuickUse\" data-i=\"${i}\" type=\"button\">Use</button><button class=\"secondary favQuickRename\" data-i=\"${i}\" type=\"button\">Rename</button></div></div>"
if oldq not in s: raise SystemExit('quick button anchor missing')
s=s.replace(oldq,newq)
oldh="document.querySelectorAll('.favQuickUse').forEach(b=>b.onclick=()=>openSavedFood(visible[Number(b.dataset.i)]));"
newh=oldh+"document.querySelectorAll('.favQuickRename').forEach(b=>b.onclick=async()=>{await renameFavourite(visible[Number(b.dataset.i)]);renderLibrary()});"
s=s.replace(oldh,newh)
oldlib="<button class=\"${f.favourite?'fav':'secondary'} libFav\" data-i=\"${i}\" type=\"button\">${f.favourite?'★ Favourite':'☆ Favourite'}</button><button class=\"secondary libUse\" data-i=\"${i}\" type=\"button\">Use</button>"
newlib=oldlib+"${f.favourite?`<button class=\"secondary libRename\" data-i=\"${i}\" type=\"button\">Rename</button>`:''}"
if oldlib not in s: raise SystemExit('library button anchor missing')
s=s.replace(oldlib,newlib)
oldlh="document.querySelectorAll('.libUse').forEach(b=>b.onclick=()=>openSavedFood(list[Number(b.dataset.i)]));document.querySelectorAll('.libFav')"
newlh="document.querySelectorAll('.libUse').forEach(b=>b.onclick=()=>openSavedFood(list[Number(b.dataset.i)]));document.querySelectorAll('.libRename').forEach(b=>b.onclick=async()=>{await renameFavourite(list[Number(b.dataset.i)]);renderLibrary()});document.querySelectorAll('.libFav')"
s=s.replace(oldlh,newlh)
p.write_text(s)

c=Path('CHANGELOG.md')
cs=c.read_text()
entry='''# v2.8.5 - Favourite renaming\n\n- Added a Rename button to favourite quick-access cards.\n- Added Rename beside favourite items in My food library.\n- Renaming preserves the food nutrition, usual portion, favourite status and usage history.\n- Renames sync through the existing Supabase food-library path, with the existing offline queue as fallback.\n- No insulin, ICR, CGM or clinical-analysis logic changed.\n\n'''
if not cs.startswith('# v2.8.5'):
    c.write_text(entry+cs)

b=Path('PROJECT_BRAIN.md')
bs=b.read_text()
brain='''\n\n## v2.8.5 - Favourite renaming (7 Sep 2026)\n- Favourite foods can now be renamed from the quick-access favourites panel or My food library.\n- Rename changes only the saved food name; nutrition, portion, favourite state and use history are retained.\n- Uses the existing food-library Supabase upsert/offline queue.\n- No dosing or clinical logic changed.\n'''
if '## v2.8.5 - Favourite renaming' not in bs:
    b.write_text(bs.rstrip()+brain+'\n')
