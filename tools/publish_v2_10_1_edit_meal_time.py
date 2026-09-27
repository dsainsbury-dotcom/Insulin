from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="""  const insulinRaw=prompt('Insulin actually taken (units, leave blank if unknown)',row.actual_insulin==null?'':String(row.actual_insulin));if(insulinRaw===null)return;const insulin=insulinRaw.trim()===''?null:Number(insulinRaw);if(insulin!==null&&(!Number.isFinite(insulin)||insulin<0))return alert('Insulin must be a valid number or blank.');
  const updated={...row,meal_name:cleanName,carbs,fat_grams:fat,actual_insulin:insulin,meal_type:inferMealType(cleanName,carbs,fat)};
"""
new="""  const insulinRaw=prompt('Insulin actually taken (units, leave blank if unknown)',row.actual_insulin==null?'':String(row.actual_insulin));if(insulinRaw===null)return;const insulin=insulinRaw.trim()===''?null:Number(insulinRaw);if(insulin!==null&&(!Number.isFinite(insulin)||insulin<0))return alert('Insulin must be a valid number or blank.');
  const existingTime=new Date(row.timestamp);const localParts=new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/London',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(existingTime).reduce((a,x)=>(a[x.type]=x.value,a),{});const defaultDate=`${localParts.year}-${localParts.month}-${localParts.day}`,defaultTime=`${localParts.hour}:${localParts.minute}`;
  const dateRaw=prompt('Meal date (YYYY-MM-DD)',defaultDate);if(dateRaw===null)return;if(!/^\\d{4}-\\d{2}-\\d{2}$/.test(dateRaw.trim()))return alert('Enter the meal date as YYYY-MM-DD.');
  const timeRaw=prompt('Actual meal time (24-hour HH:MM)',defaultTime);if(timeRaw===null)return;if(!/^([01]\\d|2[0-3]):[0-5]\\d$/.test(timeRaw.trim()))return alert('Enter the actual meal time as HH:MM, for example 15:00.');
  const wallClock=new Date(`${dateRaw.trim()}T${timeRaw.trim()}:00`);if(Number.isNaN(wallClock.getTime()))return alert('That meal date/time is not valid.');const timestamp=wallClock.toISOString();
  const updated={...row,timestamp,meal_name:cleanName,carbs,fat_grams:fat,actual_insulin:insulin,meal_type:inferMealType(cleanName,carbs,fat)};
"""
if old not in s: raise SystemExit('edit block not found')
s=s.replace(old,new,1)
oldq="""meal_type:updated.meal_type,mealType:updated.meal_type}:x);write(MEAL_QUEUE,q);renderMeals();setNotice('Queued meal updated.','good');return;"""
newq="""meal_type:updated.meal_type,mealType:updated.meal_type,timestamp:updated.timestamp}:x);write(MEAL_QUEUE,q);renderMeals();setNotice('Queued meal updated, including its actual meal date/time.','good');return;"""
if oldq not in s: raise SystemExit('queue block not found')
s=s.replace(oldq,newq,1)
oldp="""const patch={meal_name:updated.meal_name,meal_type:updated.meal_type,carbs:updated.carbs,fat_grams:updated.fat_grams,actual_insulin:updated.actual_insulin};"""
newp="""const patch={timestamp:updated.timestamp,meal_name:updated.meal_name,meal_type:updated.meal_type,carbs:updated.carbs,fat_grams:updated.fat_grams,actual_insulin:updated.actual_insulin};"""
if oldp not in s: raise SystemExit('patch block not found')
s=s.replace(oldp,newp,1)
s=s.replace("Meal updated in cloud. Refresh Intelligence to rebuild its CGM outcome and meal memory.","Meal updated in cloud, including its actual meal date/time. Refresh Intelligence to rebuild its CGM outcome and meal memory.",1)
s=s.replace('<title>ICR Meal Dashboard v2.10.0</title>','<title>ICR Meal Dashboard v2.10.1</title>',1).replace('v2.10.0</small>','v2.10.1</small>',1).replace('v2.10.0 LIVE','v2.10.1 LIVE',1)
marker='<div class="versionGrid">'
item='<div class="versionGrid"><div class="versionItem"><strong>v2.10.1 - editable meal date &amp; time</strong><ul><li>Edit now lets you correct the actual meal date and 24-hour meal time as well as the existing meal details.</li><li>Useful for meals entered retrospectively after forgetting to log them at eating time.</li><li>The corrected timestamp is saved to queued entries or Supabase and is then used by CGM matching, meal outcomes and meal memory.</li><li>No insulin calculation or dosing logic changed.</li></ul></div>'
if marker in s and 'v2.10.1 - editable meal date' not in s:s=s.replace(marker,item,1)
p.write_text(s,encoding='utf-8')
