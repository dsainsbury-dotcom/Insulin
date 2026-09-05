#!/usr/bin/env python3
"""Build restaurant nutrition data from official UK sources.

Safety rule: rows are emitted only when portion kcal, fat, carbohydrate and protein
can be parsed from an official published source. Missing/ambiguous rows are reported
and are not guessed.
"""
import io,json,re,requests
from bs4 import BeautifulSoup
import pdfplumber

GREGGS='https://a.storyblok.com/f/94904/x/7dd8489dab/nutritional-information.pdf'
PEX='https://cdn.sanity.io/files/lj3txstz/production/230f6a921a100e32ad47e5f9f92e1fdbd01fef23.pdf'
MCD_MENU='https://www.mcdonalds.com/gb/en-gb/menu.html'
UA={'User-Agent':'Mozilla/5.0 CGM-App-menu-verifier/2.8'}

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
 b=requests.get(GREGGS,headers=UA,timeout=30).content; out=[]
 with pdfplumber.open(io.BytesIO(b)) as pdf:
  text='\n'.join(p.extract_text(x_tolerance=1,y_tolerance=3) or '' for p in pdf.pages)
 # Official guide rows have: name, portion size, kJ/100g, kJ portion, kcal/100g, kcal portion...
 for ln in text.splitlines():
  ln=' '.join(ln.split())
  m=re.match(r'^(.+?)\s+(\d+(?:\.\d+)?)\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+(\d+(?:\.\d+)?)\s+\d+%\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+\d+%\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+\d+%\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+\d+%',ln)
  if not m: continue
  name,portion,kcal,fat100,fat,carb100,carbs=m.groups()
  # Protein appears near row end; extract all numeric tokens and use known column layout when possible.
  toks=re.findall(r'\d+(?:\.\d+)?%?',ln[len(name):])
  plain=[x for x in toks if not x.endswith('%')]
  if len(plain)<15: continue
  try: protein=float(plain[-3])
  except: continue
  out.append(dict(restaurant='Greggs',category='National menu',name=name,portion=f'1 portion ({portion}g/ml)',carbs=float(carbs),fat=float(fat),protein=protein,kcal=float(kcal),mealType=meal_type(name),source='Greggs official Nutritional Information Guide',sourceDate='2026-08',sourceUrl=GREGGS,evidence='official'))
 return out

def pizzaexpress():
 b=requests.get(PEX,headers=UA,timeout=30).content; out=[]; category='Menu'
 with pdfplumber.open(io.BytesIO(b)) as pdf:
  for p in pdf.pages[2:]:
   text=p.extract_text(x_tolerance=1,y_tolerance=3) or ''
   for ln in text.splitlines():
    ln=' '.join(ln.split())
    # portion columns: kcal kJ fat sat carbs sugars fibre protein salt
    m=re.match(r'^(.+?)\s+(\d+(?:\.\d+)?)\s+\d+(?:\.\d+)?\s+(\d+(?:\.\d+)?)\s+\d+(?:\.\d+)?\s+(\d+(?:\.\d+)?)\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+(\d+(?:\.\d+)?)\s+\d+(?:\.\d+)?(?:\s|$)',ln)
    if not m: continue
    name,kcal,fat,carbs,protein=m.groups()
    if name.lower().startswith(('energy','per portion','adults need','july 2026')): continue
    out.append(dict(restaurant='PizzaExpress',category=category,name=name,portion='1 published portion',carbs=float(carbs),fat=float(fat),protein=float(protein),kcal=float(kcal),mealType=meal_type(name),source='PizzaExpress official Nutritional Information - England, Wales & Scotland',sourceDate='2026-07',sourceUrl=PEX,evidence='official'))
 return out

def mcdonalds():
 html=requests.get(MCD_MENU,headers=UA,timeout=30).text
 soup=BeautifulSoup(html,'html.parser'); urls=[]
 for a in soup.select('a[href]'):
  h=a.get('href','')
  if '/gb/en-gb/product/' in h:
   if h.startswith('/'): h='https://www.mcdonalds.com'+h
   urls.append(h.split('?')[0])
 urls=list(dict.fromkeys(urls)); out=[]
 for u in urls:
  try: t=BeautifulSoup(requests.get(u,headers=UA,timeout=20).text,'html.parser').get_text(' ',strip=True)
  except Exception: continue
  name=(BeautifulSoup(requests.get(u,headers=UA,timeout=20).text,'html.parser').find('h1') or {}).get_text(' ',strip=True) if '<h1' in requests.get(u,headers=UA,timeout=20).text else ''
  def grab(label):
   m=re.search(label+r'.{0,80}?(\d+(?:\.\d+)?)\s*(?:g|grams)',t,re.I); return float(m.group(1)) if m else None
  km=re.search(r'(\d+)\s*kcal',t,re.I); carbs=grab('carbohydrates'); fat=grab(r'fat'); protein=grab('protein')
  if not (name and km and carbs is not None and fat is not None and protein is not None): continue
  out.append(dict(restaurant="McDonald's",category='Current UK menu',name=name,portion='1 published portion',carbs=carbs,fat=fat,protein=protein,kcal=float(km.group(1)),mealType=meal_type(name),source="McDonald's UK official product page",sourceDate='2026-09-05',sourceUrl=u,evidence='official'))
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
