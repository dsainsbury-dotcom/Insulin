#!/usr/bin/env python3
"""Build restaurant nutrition data from official UK sources.

Safety rule: rows are emitted only when portion kcal, fat, carbohydrate and protein
can be parsed from an official published source. Missing/ambiguous rows are reported
and are not guessed.
"""
import io,json,re,time,requests
from bs4 import BeautifulSoup
import pdfplumber
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

GREGGS='https://a.storyblok.com/f/94904/x/7dd8489dab/nutritional-information.pdf'
PEX='https://cdn.sanity.io/files/lj3txstz/production/230f6a921a100e32ad47e5f9f92e1fdbd01fef23.pdf'
MCD_MENU='https://www.mcdonalds.com/gb/en-gb/menu.html'
UA={'User-Agent':'Mozilla/5.0 (compatible; CGM-App-menu-verifier/2.8; +https://github.com/dsainsbury-dotcom/Insulin)'}

SESSION=requests.Session()
SESSION.headers.update(UA)
SESSION.mount('https://',HTTPAdapter(max_retries=Retry(total=4,connect=4,read=4,backoff_factor=1.5,status_forcelist=[429,500,502,503,504],allowed_methods=['GET'])))

def get(url,timeout=60):
 r=SESSION.get(url,timeout=timeout)
 r.raise_for_status()
 return r

def meal_type(name,cat=''):
 s=(name+' '+cat).lower()
 if 'pizza' in s:return 'Pizza'
 if any(x in s for x in ['fries','chips','wedges','hash brown','potato']):return 'Potato / chips'
 if any(x in s for x in ['baguette','sandwich','burger','wrap','roll','mcmuffin','toastie','flatbread']):return 'Bread / sandwich'
 if any(x in s for x in ['cake','doughnut','donut','cookie','brownie','muffin','dessert','mcflurry','ice cream','sweet','danish','biscuit']):return 'Dessert / sweet food'
 if any(x in s for x in ['pasta','lasagna']):return 'Pasta'
 if 'rice' in s:return 'Rice / noodles'
 if 'curry' in s:return 'Curry'
 return 'Balanced / mixed'

def greggs():
 b=get(GREGGS).content; out=[]
 with pdfplumber.open(io.BytesIO(b)) as pdf:
  text='\n'.join(p.extract_text(x_tolerance=1,y_tolerance=3) or '' for p in pdf.pages)
 for ln in text.splitlines():
  ln=' '.join(ln.split())
  m=re.match(r'^(.+?)\s+(\d+(?:\.\d+)?)\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+(\d+(?:\.\d+)?)\s+\d+%\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+\d+%\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+\d+%\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+\d+%',ln)
  if not m: continue
  name,portion,kcal,fat100,fat,carb100,carbs=m.groups()
  toks=re.findall(r'\d+(?:\.\d+)?%?',ln[len(name):])
  plain=[x for x in toks if not x.endswith('%')]
  if len(plain)<15: continue
  try: protein=float(plain[-3])
  except (ValueError,IndexError): continue
  out.append(dict(restaurant='Greggs',category='National menu',name=name,portion=f'1 portion ({portion}g/ml)',carbs=float(carbs),fat=float(fat),protein=protein,kcal=float(kcal),mealType=meal_type(name),source='Greggs official Nutritional Information Guide',sourceDate='2026-08',sourceUrl=GREGGS,evidence='official'))
 print('Greggs parsed',len(out))
 return out

def pizzaexpress():
 b=get(PEX).content; out=[]; category='Menu'
 with pdfplumber.open(io.BytesIO(b)) as pdf:
  for p in pdf.pages[2:]:
   text=p.extract_text(x_tolerance=1,y_tolerance=3) or ''
   for ln in text.splitlines():
    ln=' '.join(ln.split())
    m=re.match(r'^(.+?)\s+(\d+(?:\.\d+)?)\s+\d+(?:\.\d+)?\s+(\d+(?:\.\d+)?)\s+\d+(?:\.\d+)?\s+(\d+(?:\.\d+)?)\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+(\d+(?:\.\d+)?)\s+\d+(?:\.\d+)?(?:\s|$)',ln)
    if not m: continue
    name,kcal,fat,carbs,protein=m.groups()
    if name.lower().startswith(('energy','per portion','adults need','july 2026')): continue
    out.append(dict(restaurant='PizzaExpress',category=category,name=name,portion='1 published portion',carbs=float(carbs),fat=float(fat),protein=float(protein),kcal=float(kcal),mealType=meal_type(name),source='PizzaExpress official Nutritional Information - England, Wales & Scotland',sourceDate='2026-07',sourceUrl=PEX,evidence='official'))
 print('PizzaExpress parsed',len(out))
 return out

def mcdonalds():
 html=get(MCD_MENU,timeout=90).text
 soup=BeautifulSoup(html,'html.parser'); urls=[]
 for a in soup.select('a[href]'):
  h=a.get('href','')
  if '/gb/en-gb/product/' in h:
   if h.startswith('/'): h='https://www.mcdonalds.com'+h
   urls.append(h.split('?')[0])
 urls=list(dict.fromkeys(urls)); out=[]; failed=[]
 print("McDonald's product URLs",len(urls))
 for i,u in enumerate(urls,1):
  try:
   page=get(u,timeout=60).text
   soup=BeautifulSoup(page,'html.parser')
   t=soup.get_text(' ',strip=True)
   h1=soup.find('h1')
   name=h1.get_text(' ',strip=True) if h1 else ''
   def grab(label):
    m=re.search(label+r'.{0,100}?(\d+(?:\.\d+)?)\s*(?:g|grams)',t,re.I)
    return float(m.group(1)) if m else None
   km=re.search(r'(\d+)\s*kcal',t,re.I)
   carbs=grab('carbohydrates'); fat=grab(r'(?<!saturated )fat'); protein=grab('protein')
   if not (name and km and carbs is not None and fat is not None and protein is not None):
    failed.append((u,'nutrition fields not confidently parsed'))
    continue
   out.append(dict(restaurant="McDonald's",category='Current UK menu',name=name,portion='1 published portion',carbs=carbs,fat=fat,protein=protein,kcal=float(km.group(1)),mealType=meal_type(name),source="McDonald's UK official product page",sourceDate='2026-09-05',sourceUrl=u,evidence='official'))
  except Exception as e:
   failed.append((u,type(e).__name__))
  if i%20==0: time.sleep(.5)
 print("McDonald's parsed",len(out),'failed/skipped',len(failed))
 for u,why in failed[:20]: print('MCD_SKIP',why,u)
 return out

def dedupe(rows):
 seen=set(); out=[]
 for r in rows:
  k=(r['restaurant'].lower(),r['name'].lower(),r['portion'].lower())
  if k not in seen: seen.add(k); out.append(r)
 return out

rows=dedupe(greggs()+pizzaexpress()+mcdonalds())
rows.sort(key=lambda r:(r['restaurant'],r['category'],r['name']))
counts={}
for r in rows: counts[r['restaurant']]=counts.get(r['restaurant'],0)+1
print('COUNTS',counts,'TOTAL',len(rows))
if counts.get('Greggs',0)<80 or counts.get('PizzaExpress',0)<60 or counts.get("McDonald's",0)<20:
 raise SystemExit('Safety threshold failed: parser did not capture enough verified menu rows')
open('restaurant_foods_v2.8.0.json','w').write(json.dumps({'verified':'2026-09-05','counts':counts,'items':rows},indent=2,ensure_ascii=False))
js='window.RESTAURANT_FOODS_V280 = '+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+';\n'
open('restaurant_foods_v2.8.0.js','w').write(js)
